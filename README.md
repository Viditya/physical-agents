# physical-agents-research

Research and prototype harness for evaluating vision-spatial AI (Gemini Robotics-ER 2, Microsoft Magma) as an image-understanding layer for M-Files document/metadata agents.

## Structure

- `book/` — **new here? start with this.** "Physical Agents & World Models — Zero to Hero": a diagram-led guide to the concepts, M-Files' capability map, and a handover chapter for new contributors (Markdown chapters + rendered PDF)
- `RESEARCH_LOG.md` — running dated log of findings and experiments
- `prototype/` — Python package with provider stubs, a CLI, and a web demo UI
- `tests/` — offline tests for the demo UI (no API keys required)
- `OCR/` — sample engineering drawings (PDF) used by the demo
- `fixtures/public-fixtures.json` — source, licence, and prompt provenance for
  the public demo corpus on the `demo/public-engineering-fixtures` branch
- `pitch/` — placeholder for pitch deck source notes
- `sales/` — target-account research: domain folders like `sales/manufacturing/` (one profile page per company; more verticals auto-discovered) and `research_agent.py` (per-company research tool, output nested in `sales/accounts/<domain>/`)
- `.env.example` — required API key placeholders

## Quickstart

```bash
cp .env.example .env
# fill in your API keys
pip install -r prototype/requirements.txt
```

### Web demo UI

```bash
python -m prototype.server
# open http://127.0.0.1:5000
```

Pick one of the sample drawings in `OCR/` (or upload your own PDF/image),
choose a provider, and run it. PDFs are rasterised server-side before being
sent to the model. When Gemini returns points, they're drawn back onto the
drawing so you can see *what it read*, alongside the raw JSON response.

The UI shows up front which providers have credentials configured, so a
missing key surfaces as a readable message rather than a stack trace.
Every successful request is saved locally in `.vman-vision-cache/`, keyed by
the document contents, provider, and prompt. Selecting the same drawing with
the same prompt later loads the saved result instead of using API tokens. The
cache is intentionally gitignored because it can contain uploaded documents
and model output.

Every analyzed document also writes/overwrites a small, git-tracked copy of
its **latest** finding under `demo-results/<document-name>/<provider>/`:
`result.json` (detected points + raw response), `rendered.png` (the plain
page), and `overlay.png` (the labeled drawing), when points were found. This
folder is meant to be committed and pushed so results can be reviewed —
including by a separate session/reviewer — straight from GitHub, without
re-running the model or sharing API keys. It uses each document's filename to
name its subfolder, so before pushing, check `demo-results/` for anything
saved from an uploaded file you don't want shared (e.g. a proprietary
drawing) and remove it if needed.

### CLI

```bash
python -m prototype.cli --provider gemini --image path/to/image.jpg
```

### Sales account research agent

`sales/research_agent.py` scrapes each target company's own website
(homepage plus discoverable about/news/investor pages) and writes a
markdown research brief to `sales/accounts/<domain>/<company-slug>.md`. It
uses `gemini-3.6-flash` to synthesize a brief when `GEMINI_API_KEY` is set
(loaded automatically from `.env`) and the call succeeds; otherwise it
falls back to raw scraped snippets so it still works without any key or
when Gemini's search/generation quota is exhausted.

Targets come from **domain folders** under `sales/` — e.g.
`sales/manufacturing/` today, with future verticals such as
`sales/construction/` or `sales/healthcare/` auto-discovered the same way
(one `# Company Name` profile page per company, plus a `README.md` index
that's skipped). No code changes are needed to add a new vertical: just
create the folder with company profile pages and re-run `--all`.

```bash
# Research every company across every domain folder under sales/
python -m sales.research_agent --all

# Restrict to a single domain (e.g. only sales/manufacturing/)
python -m sales.research_agent --all --domain manufacturing

# Research a single company
python -m sales.research_agent --company "Acme Corp" --website acme.com
```

Output is nested by domain: `sales/accounts/manufacturing/abbott-laboratories.md`,
`sales/accounts/healthcare/acme-health.md`, etc.

## Tests

```bash
python -m pytest tests -q
```

These cover document rendering, coordinate mapping, and the HTTP layer.
They don't call any provider, so they run without API keys.

## Public demo branch

The `demo/public-engineering-fixtures` branch contains a small,
licence-recorded public corpus: a CC0 technical drawing template, a public-use
NASA engineering-symbol page, and a CC-BY-SA P&ID. See
[`OCR/README.md`](OCR/README.md) and
[`fixtures/public-fixtures.json`](fixtures/public-fixtures.json) before
redistributing the assets or their derivatives.

The same public fixtures also have Gemini ER 2 and Azure Foundry 4Omni overlay
artifacts plus side-by-side sheets. Read
[`docs/public-engineering-gemini-foundry-comparison.md`](docs/public-engineering-gemini-foundry-comparison.md)
for the shared prompt, observed output, and limitations.

Selecting a known public fixture in the demo automatically loads that fixture's
recorded prompt from the manifest. The complex mechanical, structural, and
electrical fixture run is documented in
[`docs/public-complex-engineering-demo-run.md`](docs/public-complex-engineering-demo-run.md).
