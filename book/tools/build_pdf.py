"""Render the book's Markdown chapters (with Mermaid diagrams) into one PDF.

Uses only the standard library plus a local Chrome/Chromium/Edge. Markdown and
Mermaid are rendered in the browser from jsDelivr, so the build needs network.

    python book/tools/build_pdf.py            # rebuild the current volume's PDF
    python book/tools/build_pdf.py --release  # also freeze it under book/volumes/
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BOOK_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = BOOK_DIR / "physical-agents-zero-to-hero.pdf"
VOLUME_FILE = BOOK_DIR / "volume.json"
VOLUMES_DIR = BOOK_DIR / "volumes"

CHAPTERS = [
    "README.md",
    "01-the-map.md",
    "02-what-is-a-physical-agent.md",
    "03-how-machines-see.md",
    "04-pointing-not-describing.md",
    "05-world-models.md",
    "06-from-seeing-to-doing.md",
    "07-knowledge-graphs.md",
    "08-retrieval-that-can-see.md",
    "09-agents-tools-mcp.md",
    "10-trust.md",
    "11-vman-vision.md",
    "12-the-heros-path.md",
    "13-the-handover.md",
    "appendix-a-glossary.md",
    "appendix-b-sources.md",
    "VOLUMES.md",
]

BROWSER_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

CSS = """
@page { size: A4; margin: 18mm 17mm 20mm 17mm; }
body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; color: #1F1F29;
       font-size: 10.5pt; line-height: 1.55; }
.chapter { page-break-before: always; }
.chapter:first-of-type { page-break-before: avoid; }
h1 { color: #1C243A; font-size: 24pt; border-bottom: 3px solid #0072CE; padding-bottom: 6px; }
h2 { color: #0072CE; font-size: 15pt; margin-top: 22px; page-break-after: avoid; }
h3 { color: #1C243A; font-size: 12pt; page-break-after: avoid; }
a { color: #0072CE; text-decoration: none; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9pt; }
tr { page-break-inside: avoid; }
thead { display: table-header-group; }
th { background: #1C243A; color: #fff; text-align: left; padding: 6px; }
td { border: 1px solid #d6dbe4; padding: 5px 6px; vertical-align: top; }
tr:nth-child(even) td { background: #f4f7fb; }
blockquote { margin: 14px 0; padding: 10px 14px; background: #eaf3fc;
             border-left: 4px solid #0072CE; page-break-inside: avoid; }
code { font-family: Consolas, 'Courier New', monospace; font-size: 9pt;
       background: #f1f3f6; padding: 1px 4px; border-radius: 3px; }
pre { background: #f1f3f6; padding: 10px; border-radius: 4px; overflow-x: hidden;
      white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
pre.mermaid { background: none; text-align: center; white-space: normal; }
.mermaid svg { max-width: 100%; max-height: 190mm; height: auto; }
h2 + pre.mermaid, h3 + pre.mermaid, p + pre.mermaid { page-break-before: avoid; }
img { max-width: 100%; display: block; margin: 10px auto; }
hr { border: none; border-top: 1px solid #d6dbe4; margin: 18px 0; }
"""

TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Physical Agents &amp; World Models - Zero to Hero</title>
<style>{css}</style>
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
</head><body><div id="book"></div>
<script>
const chapters = {chapters};
const renderer = new marked.Renderer();
const baseCode = renderer.code.bind(renderer);
renderer.code = function (token) {{
  const text = typeof token === 'object' ? token.text : token;
  const lang = typeof token === 'object' ? token.lang : arguments[1];
  if (lang === 'mermaid') {{
    const div = document.createElement('pre');
    div.className = 'mermaid';
    div.textContent = text;
    return div.outerHTML;
  }}
  return baseCode.apply(this, arguments);
}};
const book = document.getElementById('book');
for (const ch of chapters) {{
  const section = document.createElement('section');
  section.className = 'chapter';
  section.id = ch.id;
  section.innerHTML = marked.parse(ch.markdown, {{ renderer }});
  book.appendChild(section);
}}
mermaid.initialize({{ startOnLoad: false, theme: 'default', securityLevel: 'strict',
  themeVariables: {{ fontSize: '15px' }},
  flowchart: {{ useMaxWidth: true }} }});
mermaid.run({{ querySelector: 'pre.mermaid' }})
  .catch(e => console.error(e))
  .finally(() => {{ document.title = 'RENDERED'; }});
</script></body></html>
"""


def chapter_id(filename: str) -> str:
    return "ch-" + re.sub(r"[^a-z0-9]+", "-", filename.lower().removesuffix(".md")).strip("-")


def rewrite_links(markdown: str) -> str:
    """Point links between chapters at in-document anchors instead of files."""
    names = set(CHAPTERS)

    def replace(match: re.Match) -> str:
        text, target = match.group(1), match.group(2)
        if target in names:
            return f"[{text}](#{chapter_id(target)})"
        return match.group(0)

    return re.sub(r"(?<!!)\[([^\]]+)\]\(([^)#\s]+\.md)\)", replace, markdown)


def find_browser() -> str:
    for candidate in BROWSER_CANDIDATES:
        if not candidate:
            continue
        if Path(candidate).is_file():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    sys.exit("No Chrome/Chromium/Edge found. Set CHROME_PATH to a Chromium-based browser.")


def read_volume() -> tuple[int, str]:
    meta = json.loads(VOLUME_FILE.read_text(encoding="utf-8"))
    volume, date = int(meta["volume"]), str(meta["date"])
    readme = (BOOK_DIR / "README.md").read_text(encoding="utf-8")
    if f"Volume {volume} ·" not in readme:
        sys.exit(f"README.md has no 'Volume {volume}' line; update it to match volume.json.")
    return volume, date


def frozen_path(volume: int, date: str) -> Path:
    return VOLUMES_DIR / f"volume-{volume:02d}-{date}.pdf"


def build(release: bool) -> None:
    volume, date = read_volume()
    target = frozen_path(volume, date)
    if release and target.exists():
        sys.exit(f"{target.name} already exists; past volumes are never overwritten. Bump volume.json.")
    chapters = []
    for name in CHAPTERS:
        text = (BOOK_DIR / name).read_text(encoding="utf-8")
        chapters.append({"id": chapter_id(name), "markdown": rewrite_links(text)})

    html = TEMPLATE.format(css=CSS, chapters=json.dumps(chapters).replace("</", "<\\/"))
    # The HTML must sit in book/ so relative image paths like ../demo-results/ resolve.
    html_path = BOOK_DIR / "_build.html"
    html_path.write_text(html, encoding="utf-8")

    browser = find_browser()
    try:
        with tempfile.TemporaryDirectory() as profile:
            subprocess.run(
                [
                    browser,
                    "--headless=new",
                    "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--user-data-dir={profile}",
                    "--virtual-time-budget=60000",
                    f"--print-to-pdf={OUTPUT_PDF}",
                    html_path.resolve().as_uri(),
                ],
                check=True,
                capture_output=True,
            )
    finally:
        html_path.unlink(missing_ok=True)
    print(f"Wrote Volume {volume} to {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size // 1024} KB)")
    if release:
        VOLUMES_DIR.mkdir(exist_ok=True)
        shutil.copyfile(OUTPUT_PDF, target)
        print(f"Froze {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--release", action="store_true",
                        help="also save an immutable copy under book/volumes/")
    build(parser.parse_args().release)
