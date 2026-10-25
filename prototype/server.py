"""Web UI for the vision-spatial prototype -- Flask, single process.

Wraps the same providers the CLI uses (`prototype/cli.py`) in a browser
demo: pick one of the sample engineering drawings in `OCR/` (or upload
your own), run a provider, and see the detected points drawn back onto
the drawing next to the raw JSON.

Every successful provider response is cached locally by document content,
provider, and prompt. Re-selecting the same document with the same request
reuses its saved response and overlay rather than spending more model tokens.

Every analyzed document also gets a human-readable, git-tracked copy of its
latest finding under `demo-results/<document-name>/` (result.json, the
rendered page, and the labeled overlay), so results can be reviewed straight
from the GitHub repo without re-running or sharing API keys.

Usage:
    python -m prototype.server
    python -m prototype.server --port 5000
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import traceback
import uuid

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request, send_file

from prototype.cli import PROVIDERS, _load_provider
from prototype.overlay import draw_points
from prototype.render import UnsupportedDocumentError, render_to_png

load_dotenv()

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(REPO_ROOT, "OCR")
FIXTURES_PATH = os.path.join(REPO_ROOT, "fixtures", "public-fixtures.json")
ARTIFACTS_DIR = os.path.join(tempfile.gettempdir(), "vman-vision-demo")
CACHE_DIR = os.path.join(REPO_ROOT, ".vman-vision-cache")
DEMO_RESULTS_DIR = os.path.join(REPO_ROOT, "demo-results")

DEFAULT_PROMPT = (
    "Point to no more than 20 items in this engineering drawing. Prefer "
    "components, dimension callouts, revision marks, and title-block "
    'fields. The answer should follow the json format: [{"point": '
    '<point>, "label": <label>}, ...]. The points are in [y, x] format '
    "normalized to 0-1000."
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024


def _artifact_path(artifact_id: str) -> str:
    """Resolve an artifact id to a path, refusing anything path-like."""
    if not artifact_id.isalnum():
        abort(404)
    return os.path.join(ARTIFACTS_DIR, f"{artifact_id}.png")


def _sample_path(name: str) -> str:
    """Resolve a sample filename, refusing traversal outside OCR/."""
    candidate = os.path.abspath(os.path.join(SAMPLES_DIR, name))
    if os.path.dirname(candidate) != os.path.abspath(SAMPLES_DIR):
        abort(400, "Invalid sample name.")
    if not os.path.isfile(candidate):
        abort(404, "Sample not found.")
    return candidate


def _fixture_metadata() -> dict[str, dict]:
    """Return public-fixture metadata indexed by selected sample filename."""
    with open(FIXTURES_PATH, encoding="utf-8") as fixture_file:
        payload = json.load(fixture_file)

    fixtures = payload.get("fixtures")
    if not isinstance(fixtures, list):
        raise ValueError("Public fixture manifest must contain a 'fixtures' list.")

    metadata = {}
    for fixture in fixtures:
        if not isinstance(fixture, dict):
            raise ValueError("Each public fixture manifest entry must be an object.")
        fixture_path = fixture.get("file")
        prompt = fixture.get("prompt")
        title = fixture.get("title")
        if not all(isinstance(value, str) and value for value in (fixture_path, prompt, title)):
            raise ValueError("Each public fixture requires file, title, and prompt strings.")
        metadata[os.path.basename(fixture_path)] = fixture
    return metadata


def _list_samples() -> list[dict]:
    if not os.path.isdir(SAMPLES_DIR):
        return []
    metadata = _fixture_metadata()
    return [
        {
            "name": name,
            "size_kb": round(os.path.getsize(os.path.join(SAMPLES_DIR, name)) / 1024),
            "title": metadata.get(name, {}).get("title", name),
            "prompt": metadata.get(name, {}).get("prompt", DEFAULT_PROMPT),
        }
        for name in sorted(os.listdir(SAMPLES_DIR))
        if name.lower().endswith((".pdf", ".png", ".jpg", ".jpeg"))
    ]


def _provider_status() -> dict:
    """Report which providers have credentials, so the UI can say so up front."""
    return {
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "magma": bool(os.getenv("FOUNDRY_API_KEY") and os.getenv("FOUNDRY_ENDPOINT")),
    }


def _cache_key(source_path: str, provider_name: str, prompt: str) -> str:
    """Return a stable key for the exact document and model request."""
    digest = hashlib.sha256()
    with open(source_path, "rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    digest.update(b"\0")
    digest.update(provider_name.encode("utf-8"))
    digest.update(b"\0")
    digest.update(prompt.encode("utf-8"))
    return digest.hexdigest()


def _source_sha256(source_path: str) -> str:
    """Return the stable content hash recorded with a saved demo result."""
    digest = hashlib.sha256()
    with open(source_path, "rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cache_paths(cache_key: str) -> tuple[str, str, str]:
    """Return the result JSON, rendered page, and overlay paths for one run."""
    cache_path = os.path.join(CACHE_DIR, cache_key)
    return (
        os.path.join(cache_path, "result.json"),
        os.path.join(cache_path, "rendered.png"),
        os.path.join(cache_path, "overlay.png"),
    )


def _load_cached_response(cache_key: str) -> dict | None:
    """Restore a complete cached run, if one is available."""
    result_path, rendered_path, overlay_path = _cache_paths(cache_key)
    if not os.path.isfile(result_path) or not os.path.isfile(rendered_path):
        return None

    try:
        with open(result_path, encoding="utf-8") as result_file:
            result = json.load(result_file)
    except (json.JSONDecodeError, OSError):
        return None

    run_id = cache_key
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    shutil.copyfile(rendered_path, _artifact_path(run_id))
    response = {
        "run_id": run_id,
        "provider": result["provider"],
        "rendered_url": f"/api/artifact/{run_id}",
        "result": result["result"],
        "cache_hit": True,
    }
    if os.path.isfile(overlay_path):
        overlay_id = f"{run_id}o"
        shutil.copyfile(overlay_path, _artifact_path(overlay_id))
        response["overlay_url"] = f"/api/artifact/{overlay_id}"
        response["points_drawn"] = result.get("points_drawn", 0)
    return response


def _save_cached_response(cache_key: str, response: dict) -> None:
    """Persist the response and visual artifacts after a successful model call."""
    result_path, rendered_path, overlay_path = _cache_paths(cache_key)
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    shutil.copyfile(_artifact_path(response["run_id"]), rendered_path)
    if "overlay_url" in response:
        shutil.copyfile(_artifact_path(f"{response['run_id']}o"), overlay_path)

    with open(result_path, "w", encoding="utf-8") as result_file:
        json.dump(
            {
                "provider": response["provider"],
                "result": response["result"],
                "points_drawn": response.get("points_drawn", 0),
            },
            result_file,
            indent=2,
        )


def _demo_result_slug(display_name: str) -> str:
    """Turn a document's display name into a filesystem- and URL-safe folder name."""
    stem = os.path.splitext(os.path.basename(display_name))[0]
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-") or "document"
    return slug


def _save_demo_result(
    display_name: str, provider_name: str, response: dict, source_path: str
) -> str | None:
    """Write a git-trackable copy of the latest finding for this document.

    Unlike ``.vman-vision-cache`` (gitignored, keyed by exact request), this
    always reflects the *most recent* run for a document + provider pair, so
    it stays small and reviewable straight from the GitHub repo.

    Adds a content hash and, for a known public sample, its fixture provenance.
    Returns a warning when Windows cannot replace an open result image. The
    analysis artifact remains available from ``ARTIFACTS_DIR`` in that case.
    """
    try:
        result_dir = os.path.join(DEMO_RESULTS_DIR, _demo_result_slug(display_name), provider_name)
        os.makedirs(result_dir, exist_ok=True)

        shutil.copyfile(_artifact_path(response["run_id"]), os.path.join(result_dir, "rendered.png"))
        overlay_path = os.path.join(result_dir, "overlay.png")
        if "overlay_url" in response:
            shutil.copyfile(_artifact_path(f"{response['run_id']}o"), overlay_path)
        elif os.path.isfile(overlay_path):
            # A previous run for this document had detected points but this one
            # didn't; don't leave a stale overlay image behind.
            os.remove(overlay_path)

        fixture = _fixture_metadata().get(os.path.basename(source_path))
        saved_result = {
            "source_document": display_name,
            "source_sha256": _source_sha256(source_path),
            "provider": response["provider"],
            "prompt": response.get("prompt", ""),
            "result": response["result"],
            "points_drawn": response.get("points_drawn", 0),
        }
        if fixture:
            saved_result["fixture_title"] = fixture["title"]
            saved_result["fixture_source_url"] = fixture.get("source_url")
            saved_result["fixture_license"] = fixture.get(
                "license", fixture.get("rights_advisory")
            )

        with open(os.path.join(result_dir, "result.json"), "w", encoding="utf-8") as result_file:
            json.dump(
                saved_result,
                result_file,
                indent=2,
            )
    except OSError as exc:
        return (
            "Analysis completed, but the demo-results copy could not be updated. "
            f"Close any program displaying that result and retry: {exc}"
        )
    return None


@app.get("/")
def index():
    return INDEX_HTML, 200, {"Content-Type": "text/html; charset=utf-8"}


@app.get("/api/config")
def config():
    return jsonify(
        {
            "providers": sorted(PROVIDERS),
            "configured": _provider_status(),
            "samples": _list_samples(),
            "default_prompt": DEFAULT_PROMPT,
        }
    )


@app.get("/api/artifact/<artifact_id>")
def artifact(artifact_id: str):
    path = _artifact_path(artifact_id)
    if not os.path.isfile(path):
        abort(404)
    return send_file(path, mimetype="image/png")


@app.post("/api/analyze")
def analyze():
    """Render the chosen document, run a provider on it, and overlay the result."""
    provider_name = request.form.get("provider", "gemini")
    prompt = (request.form.get("prompt") or DEFAULT_PROMPT).strip()

    if provider_name not in PROVIDERS:
        return jsonify({"error": f"Unknown provider '{provider_name}'."}), 400

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    run_id = uuid.uuid4().hex

    try:
        source_path, display_name = _resolve_source(run_id)
    except UnsupportedDocumentError as exc:
        return jsonify({"error": str(exc)}), 400
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    cache_key = _cache_key(source_path, provider_name, prompt)
    cached_response = _load_cached_response(cache_key)
    if cached_response:
        cached_response["prompt"] = prompt
        if warning := _save_demo_result(display_name, provider_name, cached_response, source_path):
            cached_response["warning"] = warning
        return jsonify(cached_response)

    try:
        rendered_path = os.path.join(ARTIFACTS_DIR, f"{run_id}.png")
        render_to_png(source_path, rendered_path)
    except UnsupportedDocumentError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001 - surfaced to the UI verbatim
        return jsonify({"error": f"Could not render document: {exc}"}), 400

    try:
        provider = _load_provider(provider_name)
    except EnvironmentError as exc:
        # Missing credentials is the single most likely demo failure --
        # report it as a clean 400 rather than a stack trace.
        return jsonify({"error": str(exc), "kind": "missing_credentials"}), 400

    try:
        result = provider.describe_image(rendered_path, prompt)
    except Exception as exc:  # noqa: BLE001 - preview APIs fail in varied ways
        traceback.print_exc()
        return jsonify({"error": f"{type(exc).__name__}: {exc}", "kind": "provider_error"}), 502

    response = {
        "run_id": run_id,
        "provider": provider_name,
        "prompt": prompt,
        "rendered_url": f"/api/artifact/{run_id}",
        "result": result,
        "cache_hit": False,
    }

    points = result.get("points") or []
    if points:
        overlay_id = f"{run_id}o"
        overlay_path = os.path.join(ARTIFACTS_DIR, f"{overlay_id}.png")
        drawn = draw_points(rendered_path, points, overlay_path)
        if drawn:
            response["overlay_url"] = f"/api/artifact/{overlay_id}"
            response["points_drawn"] = drawn

    _save_cached_response(cache_key, response)
    if warning := _save_demo_result(display_name, provider_name, response, source_path):
        response["warning"] = warning
    return jsonify(response)


def _resolve_source(run_id: str) -> tuple[str, str]:
    """Return (path, display_name) for whichever input the request supplied."""
    upload = request.files.get("file")
    if upload and upload.filename:
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        extension = os.path.splitext(upload.filename)[1].lower() or ".pdf"
        upload_path = os.path.join(ARTIFACTS_DIR, f"{run_id}-upload{extension}")
        upload.save(upload_path)
        return upload_path, upload.filename

    sample = request.form.get("sample")
    if sample:
        return _sample_path(sample), sample

    raise ValueError("Choose a sample drawing or upload a file.")


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VMAN Vision — drawing understanding demo</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: "Segoe UI", system-ui, sans-serif;
    background: #0b0f17; color: #e6edf6;
  }
  header {
    padding: 20px 28px; border-bottom: 1px solid #1e2836;
    display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap;
  }
  header h1 { margin: 0; font-size: 19px; letter-spacing: .2px; }
  header p { margin: 0; color: #8ea0b8; font-size: 13px; }
  main { display: grid; grid-template-columns: 340px 1fr; gap: 24px; padding: 24px 28px; align-items: start; }
  @media (max-width: 900px) { main { grid-template-columns: 1fr; } }
  .panel { background: #121926; border: 1px solid #1e2836; border-radius: 12px; padding: 18px; }
  label { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: .6px; color: #8ea0b8; margin: 14px 0 6px; }
  label:first-of-type { margin-top: 0; }
  select, textarea, input[type=file] {
    width: 100%; background: #0b1220; color: #e6edf6;
    border: 1px solid #24324a; border-radius: 8px; padding: 9px 10px; font: inherit;
  }
  textarea { min-height: 108px; resize: vertical; font-size: 13px; line-height: 1.45; }
  button {
    margin-top: 18px; width: 100%; padding: 11px; font: inherit; font-weight: 600;
    background: #2563eb; color: #fff; border: 0; border-radius: 8px; cursor: pointer;
  }
  button:disabled { background: #24324a; color: #7c8ba3; cursor: not-allowed; }
  .status { margin-top: 14px; font-size: 13px; min-height: 20px; color: #8ea0b8; }
  .status.error { color: #ff8f7a; white-space: pre-wrap; }
  .badge { display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 999px; margin-left: 6px; }
  .badge.ok { background: #10371f; color: #56d67f; }
  .badge.missing { background: #3a1c1c; color: #ff8f7a; }
  .tabs { display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
  .tabs button { margin: 0; width: auto; padding: 7px 14px; background: #1a2434; color: #b8c6da; font-weight: 500; }
  .tabs button.active { background: #2563eb; color: #fff; }
  .viewer { min-height: 320px; display: flex; align-items: center; justify-content: center; }
  .viewer img { max-width: 100%; border-radius: 8px; border: 1px solid #1e2836; }
  .viewer .empty { color: #64748b; font-size: 14px; text-align: center; padding: 60px 20px; }
  pre {
    margin: 0; background: #0b1220; border: 1px solid #1e2836; border-radius: 8px;
    padding: 14px; overflow: auto; max-height: 460px; font-size: 12.5px; line-height: 1.5;
  }
  .hint { font-size: 12px; color: #64748b; margin-top: 10px; line-height: 1.5; }
</style>
</head>
<body>
<header>
  <h1>VMAN Vision</h1>
  <p>Vision-spatial extraction on engineering drawings — Gemini Robotics-ER 2 / Azure AI Foundry</p>
</header>

<main>
  <section class="panel">
    <label for="provider">Provider</label>
    <select id="provider"></select>

    <label for="sample">Sample drawing</label>
    <select id="sample"></select>

    <label for="upload">…or upload your own (PDF / image)</label>
    <input type="file" id="upload" accept=".pdf,.png,.jpg,.jpeg,.webp,.tif,.tiff">

    <label for="prompt">Prompt</label>
    <textarea id="prompt"></textarea>

    <button id="run">Analyze drawing</button>
    <div class="status" id="status"></div>
    <p class="hint">
      PDFs are rasterised server-side before being sent to the model.
      Gemini returns labelled points, which are drawn back onto the drawing.
    </p>
  </section>

  <section class="panel">
    <div class="tabs">
      <button data-view="overlay" class="active">Detected points</button>
      <button data-view="rendered">Rendered page</button>
      <button data-view="json">Raw response</button>
    </div>
    <div class="viewer" id="viewer">
      <div class="empty">Run an analysis to see results.</div>
    </div>
  </section>
</main>

<script>
const $ = (id) => document.getElementById(id);
let lastResult = null;
let activeView = "overlay";
let samplePrompts = new Map();
let defaultPrompt = "";

async function loadConfig() {
  const res = await fetch("/api/config");
  const cfg = await res.json();
  defaultPrompt = cfg.default_prompt;

  $("provider").innerHTML = cfg.providers.map((name) => {
    const ready = cfg.configured[name];
    const suffix = ready ? "" : "  (no API key)";
    return `<option value="${name}">${name}${suffix}</option>`;
  }).join("");

  $("sample").innerHTML = cfg.samples.length
    ? cfg.samples.map((s) => `<option value="${s.name}">${s.title} (${s.size_kb} KB)</option>`).join("")
    : `<option value="">No samples found in OCR/</option>`;
  samplePrompts = new Map(cfg.samples.map((sample) => [sample.name, sample.prompt]));
  applySamplePrompt();

  const missing = cfg.providers.filter((n) => !cfg.configured[n]);
  if (missing.length) {
    setStatus(`No API key configured for: ${missing.join(", ")}. Copy .env.example to .env and fill it in.`, true);
  }
}

function applySamplePrompt() {
  $("prompt").value = samplePrompts.get($("sample").value) || defaultPrompt;
}

function setStatus(message, isError = false) {
  const el = $("status");
  el.textContent = message;
  el.className = isError ? "status error" : "status";
}

function render() {
  const viewer = $("viewer");
  if (!lastResult) {
    viewer.innerHTML = `<div class="empty">Run an analysis to see results.</div>`;
    return;
  }

  if (activeView === "json") {
    viewer.innerHTML = `<pre>${escapeHtml(JSON.stringify(lastResult.result, null, 2))}</pre>`;
    return;
  }

  const url = activeView === "overlay"
    ? (lastResult.overlay_url || lastResult.rendered_url)
    : lastResult.rendered_url;

  const note = (activeView === "overlay" && !lastResult.overlay_url)
    ? `<div class="empty">This provider returned prose rather than points — see “Raw response”.</div>`
    : "";

  viewer.innerHTML = note || `<img src="${url}" alt="analysis result">`;
}

function escapeHtml(text) {
  return text.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

document.querySelectorAll(".tabs button").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tabs button").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    activeView = btn.dataset.view;
    render();
  });

  $("sample").addEventListener("change", () => {
    if (!$("upload").files[0]) {
      applySamplePrompt();
    }
  });

  $("upload").addEventListener("change", () => {
    if ($("upload").files[0]) {
      $("prompt").value = defaultPrompt;
    } else {
      applySamplePrompt();
    }
  });
});

$("run").addEventListener("click", async () => {
  const body = new FormData();
  body.append("provider", $("provider").value);
  body.append("prompt", $("prompt").value);

  const file = $("upload").files[0];
  if (file) {
    body.append("file", file);
  } else if ($("sample").value) {
    body.append("sample", $("sample").value);
  } else {
    setStatus("Choose a sample drawing or upload a file.", true);
    return;
  }

  $("run").disabled = true;
  setStatus("Checking saved findings, then calling the model if needed…");

  try {
    const res = await fetch("/api/analyze", { method: "POST", body });
    const contentType = res.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      setStatus(`The server returned ${res.status} instead of an API response. Check the server log and retry.`, true);
      return;
    }
    const data = await res.json();
    if (!res.ok) {
      setStatus(data.error || "Request failed.", true);
      return;
    }
    lastResult = data;
    const drawn = data.points_drawn;
    const source = data.cache_hit ? "Loaded saved finding" : "Saved finding";
    setStatus(drawn
      ? `${source} — ${drawn} point(s) detected and drawn.`
      : `${source} — see “Raw response”.`);
    if (data.warning) {
      setStatus(`${$("status").textContent} ${data.warning}`, true);
    }
    render();
  } catch (err) {
    setStatus(String(err), true);
  } finally {
    $("run").disabled = false;
  }
});

loadConfig();
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the vision prototype web UI.")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to.")
    args = parser.parse_args()

    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    print(f"VMAN Vision demo UI -> http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
