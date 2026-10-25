"""Tests for the demo UI's document-prep, overlay, and HTTP layers.

None of these call a provider, so the whole suite runs without API keys --
which is the point: the parts that break a live demo (rendering, coordinate
mapping, error handling) stay verifiable offline.
"""

from __future__ import annotations

import json
import os

import pymupdf
import pytest
from PIL import Image

from prototype import server
from prototype.overlay import draw_points
from prototype.render import UnsupportedDocumentError, page_count, render_to_png


@pytest.fixture
def sample_pdf(tmp_path):
    path = tmp_path / "drawing.pdf"
    document = pymupdf.open()
    page = document.new_page(width=400, height=300)
    page.insert_text((60, 120), "VALVE V-101")
    document.save(str(path))
    document.close()
    return str(path)


@pytest.fixture
def sample_png(tmp_path):
    path = tmp_path / "photo.png"
    Image.new("RGB", (240, 160), (200, 200, 200)).save(path)
    return str(path)


@pytest.fixture
def transparent_png(tmp_path):
    path = tmp_path / "transparent.png"
    Image.new("RGBA", (20, 20), (0, 0, 0, 0)).save(path)
    return str(path)


class TestRender:
    def test_pdf_renders_to_png_at_zoom(self, sample_pdf, tmp_path):
        output = str(tmp_path / "out.png")
        render_to_png(sample_pdf, output)

        with Image.open(output) as image:
            assert image.format == "PNG"
            # 400x300 at RENDER_ZOOM=2.0
            assert image.size == (800, 600)

    def test_image_passes_through_as_png(self, sample_png, tmp_path):
        output = str(tmp_path / "out.png")
        render_to_png(sample_png, output)

        with Image.open(output) as image:
            assert image.format == "PNG"
            assert image.size == (240, 160)

    def test_transparent_image_is_composited_on_white(self, transparent_png, tmp_path):
        output = str(tmp_path / "out.png")
        render_to_png(transparent_png, output)

        with Image.open(output) as image:
            assert image.getpixel((0, 0)) == (255, 255, 255)

    def test_unsupported_extension_is_rejected(self, tmp_path):
        source = tmp_path / "notes.txt"
        source.write_text("not a drawing")

        with pytest.raises(UnsupportedDocumentError):
            render_to_png(str(source), str(tmp_path / "out.png"))

    def test_out_of_range_page_is_rejected(self, sample_pdf, tmp_path):
        with pytest.raises(UnsupportedDocumentError):
            render_to_png(sample_pdf, str(tmp_path / "out.png"), page_number=5)

    def test_page_count(self, sample_pdf, sample_png):
        assert page_count(sample_pdf) == 1
        assert page_count(sample_png) == 1


class TestOverlay:
    def test_draws_each_valid_point(self, sample_png, tmp_path):
        points = [
            {"point": [500, 500], "label": "center"},
            {"point": [100, 900], "label": "top right"},
        ]
        drawn = draw_points(sample_png, points, str(tmp_path / "overlay.png"))
        assert drawn == 2

    def test_marker_lands_at_the_mapped_pixel(self, sample_png, tmp_path):
        output = str(tmp_path / "overlay.png")
        draw_points(sample_png, [{"point": [500, 500], "label": ""}], output)

        with Image.open(output) as image:
            # [y=500, x=500] on a 240x160 image maps to the exact center.
            assert image.getpixel((120, 80)) != (200, 200, 200)

    def test_malformed_points_are_skipped_not_fatal(self, sample_png, tmp_path):
        points = [
            {"point": [500, 500], "label": "good"},
            {"point": "nonsense", "label": "bad"},
            {"point": [1, 2, 3], "label": "wrong arity"},
            {"label": "no point"},
            "not even a dict",
        ]
        drawn = draw_points(sample_png, points, str(tmp_path / "overlay.png"))
        assert drawn == 1

    def test_out_of_range_coordinates_are_clamped(self, sample_png, tmp_path):
        output = str(tmp_path / "overlay.png")
        drawn = draw_points(sample_png, [{"point": [5000, -200], "label": "x"}], output)

        assert drawn == 1
        with Image.open(output) as image:
            assert image.size == (240, 160)


class TestServer:
    @pytest.fixture
    def client(self, tmp_path, monkeypatch):
        monkeypatch.setattr(server, "ARTIFACTS_DIR", str(tmp_path / "artifacts"))
        monkeypatch.setattr(server, "CACHE_DIR", str(tmp_path / "cache"))
        monkeypatch.setattr(server, "DEMO_RESULTS_DIR", str(tmp_path / "demo-results"))
        server.app.config["TESTING"] = True
        return server.app.test_client()

    def test_index_serves_the_ui(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"VMAN Vision" in response.data
        assert b"content-type" in response.data
        assert b"instead of an API response" in response.data
        assert b"function applySamplePrompt()" in response.data

    def test_config_reports_providers_and_samples(self, client):
        payload = json.loads(client.get("/api/config").data)

        assert set(payload["providers"]) == {"gemini", "magma"}
        assert set(payload["configured"]) == {"gemini", "magma"}
        assert payload["default_prompt"]
        assert isinstance(payload["samples"], list)
        assert all(sample["title"] and sample["prompt"] for sample in payload["samples"])
        assert any(sample["name"].endswith(".jpg") for sample in payload["samples"])
        bollman = next(
            sample
            for sample in payload["samples"]
            if sample["name"] == "public-bollman-truss-bridge-sheet-4.jpg"
        )
        assert "no more than 20" in bollman["prompt"]
        assert "suspension link" in bollman["prompt"]

    def test_analyze_requires_a_document(self, client):
        response = client.post("/api/analyze", data={"provider": "gemini"})

        assert response.status_code == 400
        assert "upload" in json.loads(response.data)["error"].lower()

    def test_fixture_metadata_requires_prompt_title_and_file(self, tmp_path, monkeypatch):
        manifest = tmp_path / "public-fixtures.json"
        manifest.write_text('{"fixtures": [{"file": "OCR/a.png"}]}', encoding="utf-8")
        monkeypatch.setattr(server, "FIXTURES_PATH", str(manifest))

        with pytest.raises(ValueError, match="file, title, and prompt"):
            server._fixture_metadata()

    def test_analyze_rejects_unknown_provider(self, client):
        response = client.post("/api/analyze", data={"provider": "nope"})

        assert response.status_code == 400
        assert "nope" in json.loads(response.data)["error"]

    def test_analyze_reports_missing_credentials_cleanly(self, client, sample_pdf, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        with open(sample_pdf, "rb") as handle:
            response = client.post(
                "/api/analyze",
                data={"provider": "gemini", "file": (handle, "drawing.pdf")},
                content_type="multipart/form-data",
            )

        assert response.status_code == 400
        assert json.loads(response.data)["kind"] == "missing_credentials"

    def test_analyze_rejects_unsupported_upload(self, client, tmp_path):
        source = tmp_path / "notes.txt"
        source.write_text("not a drawing")

        with open(source, "rb") as handle:
            response = client.post(
                "/api/analyze",
                data={"provider": "gemini", "file": (handle, "notes.txt")},
                content_type="multipart/form-data",
            )

        assert response.status_code == 400

    def test_sample_name_cannot_escape_the_samples_dir(self, client):
        response = client.post(
            "/api/analyze",
            data={"provider": "gemini", "sample": "../README.md"},
        )
        assert response.status_code in (400, 404)

    def test_artifact_id_must_be_alphanumeric(self, client):
        assert client.get("/api/artifact/..%2Fsecret").status_code == 404

    def test_missing_artifact_is_404(self, client):
        assert client.get("/api/artifact/deadbeef").status_code == 404

    def test_artifact_round_trips(self, client, tmp_path):
        os.makedirs(server.ARTIFACTS_DIR, exist_ok=True)
        Image.new("RGB", (10, 10)).save(os.path.join(server.ARTIFACTS_DIR, "abc123.png"))

        response = client.get("/api/artifact/abc123")

        assert response.status_code == 200
        assert response.mimetype == "image/png"

    def test_same_document_provider_and_prompt_reuses_saved_finding(
        self, client, sample_pdf, monkeypatch
    ):
        class Provider:
            calls = 0

            def describe_image(self, image_path, prompt):
                Provider.calls += 1
                return {
                    "provider": "fake",
                    "points": [{"point": [500, 500], "label": "valve"}],
                    "raw_text": "[]",
                }

        monkeypatch.setattr(server, "_load_provider", lambda _: Provider())

        def analyze():
            with open(sample_pdf, "rb") as handle:
                return client.post(
                    "/api/analyze",
                    data={
                        "provider": "gemini",
                        "prompt": "find valves",
                        "file": (handle, "drawing.pdf"),
                    },
                    content_type="multipart/form-data",
                )

        first = json.loads(analyze().data)
        second = json.loads(analyze().data)

        assert Provider.calls == 1
        assert first["cache_hit"] is False
        assert second["cache_hit"] is True
        assert second["result"] == first["result"]
        assert second["overlay_url"]

    def test_analyze_writes_a_tracked_demo_result_for_the_document(
        self, client, sample_pdf, monkeypatch
    ):
        class Provider:
            def describe_image(self, image_path, prompt):
                return {
                    "provider": "fake",
                    "points": [{"point": [500, 500], "label": "valve"}],
                    "raw_text": "[]",
                }

        monkeypatch.setattr(server, "_load_provider", lambda _: Provider())

        with open(sample_pdf, "rb") as handle:
            response = client.post(
                "/api/analyze",
                data={
                    "provider": "gemini",
                    "prompt": "find valves",
                    "file": (handle, "drawing.pdf"),
                },
                content_type="multipart/form-data",
            )
        assert response.status_code == 200

        result_dir = os.path.join(server.DEMO_RESULTS_DIR, "drawing", "gemini")
        assert os.path.isfile(os.path.join(result_dir, "result.json"))
        assert os.path.isfile(os.path.join(result_dir, "rendered.png"))
        assert os.path.isfile(os.path.join(result_dir, "overlay.png"))

        with open(os.path.join(result_dir, "result.json"), encoding="utf-8") as handle:
            saved = json.load(handle)
        assert saved["source_document"] == "drawing.pdf"
        assert len(saved["source_sha256"]) == 64
        assert saved["provider"] == "gemini"
        assert saved["prompt"] == "find valves"
        assert saved["result"]["points"][0]["label"] == "valve"

    def test_analyze_returns_json_when_the_demo_result_copy_is_locked(
        self, client, sample_pdf, monkeypatch
    ):
        class Provider:
            def describe_image(self, image_path, prompt):
                return {
                    "provider": "fake",
                    "points": [{"point": [500, 500], "label": "valve"}],
                    "raw_text": "[]",
                }

        monkeypatch.setattr(server, "_load_provider", lambda _: Provider())
        monkeypatch.setattr(
            server,
            "_save_demo_result",
            lambda *_: "Analysis completed, but the demo-results copy could not be updated.",
        )

        with open(sample_pdf, "rb") as handle:
            response = client.post(
                "/api/analyze",
                data={
                    "provider": "gemini",
                    "prompt": "find valves",
                    "file": (handle, "drawing.pdf"),
                },
                content_type="multipart/form-data",
            )

        payload = response.get_json()
        assert response.status_code == 200
        assert payload["overlay_url"]
        assert "could not be updated" in payload["warning"]
