# Differentiation Plan: VMAN Vision PoC vs. AI-Metadata Team (`metadata-poc`)

**Date:** 2026-09-08
**Author:** Prepared by AI assistant (Copilot SDK) for review by [Vidit / independent reviewer]
**Purpose:** Assess whether our vision-spatial PoC and the AI-Metadata team's parsing/extraction roadmap overlap, and — if not — define where we should focus to serve the customer's stated demands without duplicating in-flight work.

---

## 1. Customer's stated demands (verbatim, from `OCR` folder context)

- Process complex documents containing **pictures**
- Process complex documents containing **logotypes**
- Process complex documents containing **graphs**
- Process complex documents containing **financial KPIs in various formats** (some of which are pictures)
- Process complex documents containing **financial KPIs in tables within PPTs**
- Process complex documents containing **financial KPIs in tables within PDFs**
- Process **financial KPIs in Excel sheets** in varying formats
- **Improved source attribution** across the board

## 2. What the AI-Metadata team (`metadata-poc`, owner: Abhijit Singh's team) is already building

Repos reviewed: `metadata-poc`, `ai-evaluation-workbench-poc`, `mf-aino-metadata`, `aino-metadata-api`, `aino-metadata-iac`. All docs in `metadata-poc/docs/` were read in full:

| Document | What it covers | Status |
|---|---|---|
| `parsing_engine_discovery_for_layout_aware_parsing.md` | LlamaParse-based parser engine (self-hosted per-region for data residency). Converts documents → Markdown, **structured tables**, and **page images**. Content-addressed cache, tenant isolation, full test plan. | v1.0, dated Jun 25 2026 — **implementation-ready architecture**, heading toward production in `mf-aino-metadata` |
| `aino-metadata-extraction-workflow.md` | Documents the *existing* production extraction pipeline. Confirms Aino **already has an "Images" processing mode**: when `ContentProcessingMode=Images` and total file size ≤10MB, raw `FileData` (binary page images) is sent to the LLM alongside plain text. Files >10MB silently downgrade to text-only. | Existing/shipped behavior |
| `get-automatic-metadata-api-trace.md` | Full request/response contract trace for the `/objects/get-automatic-metadata` API, IDL → RPC/gRPC/REST → Intelligence Service (Aino) providers. | Existing/shipped |
| `proactive-property-suggestions-final-architecture.md` + `...provisional-properties-creation-approach.md` | New "Proactive Additional Property Suggestions" (PAPS) — LLM discovers new candidate metadata properties beyond the pre-configured card, transient until user accepts. | In design/early build |
| `semantic-deduplication-design.md` | Engine to stop PAPS suggesting properties that are semantic near-duplicates of existing ones. | Design doc for PAPS |

### Coverage against the customer's demands

| Demand | Covered by metadata-poc? | Evidence |
|---|---|---|
| Pictures in documents | Partial | "Images" mode already sends raw page images to the LLM; parser engine also renders page images. But **no doc describes what the LLM does with the image content** (no chart/KPI/photo comprehension logic described) |
| Logotypes | No | Not mentioned anywhere |
| Graphs (charts) | No | Parser extracts table *structure*, not chart *semantics*. No chart-reading capability described |
| Financial KPIs as images | Partial/unclear | Falls under "Images" mode by default, but no KPI-specific extraction logic exists; capped at 10MB before silent downgrade to text-only (would likely fail on image-heavy financial decks) |
| Financial KPIs in PPT tables | No | Parser doc explicitly targets "table-heavy documents" generically — no PPT-specific handling called out, and PPT isn't named as a supported input format |
| Financial KPIs in PDF tables | Yes (structurally) | `StructuredContent.Tables` is an explicit deliverable of the LlamaParse parser |
| Financial KPIs in Excel | No | Not mentioned in any doc reviewed |
| Improved source attribution | No | Not mentioned in any doc reviewed — no citation/provenance/grounding-back-to-source-location concept appears anywhere in the 6 docs |

## 3. What our PoC currently does

- Spatial-pointing / visual grounding on **engineering drawings** using Gemini (real capability) and a GPT-4o stand-in mislabeled "magma" (no real spatial grounding — see Section 5).
- Takes an image/PDF page, asks a vision-language model to return `{point, label}` pairs, draws them back onto the rendered page.
- Not currently pointed at financial documents, KPIs, charts, Excel, or PPTs at all — this is 100% new-application-of-the-technique territory relative to the current repo.

## 4. Where the two efforts genuinely overlap (avoid duplicating)

- **Both would need to get document pages into a model as images.** The AI-Metadata team already has this solved end-to-end in production (Aino's "Images" mode + the in-flight LlamaParse page-image renderer). **We should not re-build page rasterization/ingestion — reuse or interface with what they already ship**, rather than building a parallel pipeline.
- **Table extraction from PDFs is already covered** by the LlamaParse parser's `StructuredContent.Tables`. If the goal is "read financial KPI tables in PDFs," that's their lane, not a gap we should fill.

## 5. Where we can genuinely differentiate (the actual gaps)

These are asks the metadata-poc roadmap does **not** address, based on exhaustive doc review:

1. **Chart/graph semantic understanding** — reading a bar/line/pie chart and extracting the KPI values it represents. LlamaParse is a *parser* (converts layout to structured text), not a *vision-reasoning* model — it cannot interpret what a chart communicates. This is squarely a VLM-reasoning problem, which is exactly the muscle our PoC already exercises (pointing at + describing visual content in an image).
2. **Financial KPIs presented as pictures** (e.g., a screenshotted dashboard, an infographic) — same reasoning gap as above. The existing "Images" mode ships the picture to the LLM but nothing in the docs describes KPI-aware extraction logic on the far end.
3. **Financial KPIs in PPT tables specifically** — PPT isn't named as a supported format anywhere; this is an open gap regardless of who addresses it.
4. **Excel-native KPI extraction** — entirely unaddressed; note this is arguably *not* a vision problem at all (Excel is structured data, not an image) — likely doesn't need our vision approach, better solved with a spreadsheet parser.
5. **Logotype recognition/extraction** — unaddressed; a narrower, possibly lower-priority ask (brand/entity identification from a logo image).
6. **Source attribution** ("where did this KPI/value come from in the source document") — **unaddressed by either side**. This is a cross-cutting gap, not specific to vision vs. parsing — worth flagging as a shared risk regardless of which team builds the extraction itself.

## 6. Recommended focus for our differentiation

**Lean into what a spatial/visual-grounding model does that a text/table parser structurally cannot do:**

- Extend the current PoC pattern (point-and-label on an image) from engineering drawings to **financial pages containing charts, infographics, and KPI callouts** — the same "give the model an image, get back grounded, labeled findings" loop, just pointed at a different document domain.
- Explicitly do NOT attempt to rebuild PDF/PPT table extraction or page-rasterization — that's shipped/in-flight in `mf-aino-metadata`. If our PoC needs page images, prefer consuming the AI-Metadata team's parser output (once available) rather than parallel-building it.
- Treat Excel KPI extraction as **out of scope** for a vision-based approach — flag it to the customer/PM as needing a separate (non-vision) solution.
- Treat **source attribution** as a candidate second differentiator: since our approach already does spatial *pointing* (i.e., "this value is located here on the page"), we may be structurally closer to solving "attribution" (point back to exact source location) than a pure text-parsing pipeline is. Worth exploring as an explicit feature: every extracted KPI/value carries back a `{page, point}` grounding reference, not just a text answer.

## 7. Open questions for the reviewer

- Should we treat this as a formal proposal to extend PoC scope, or keep it exploratory until the AI-Metadata team's PAPS/parser work ships and we can test for real overlap?
- Is "financial documents" the right second domain to prove out, or should we confirm directly with the customer/PM which of the 8 demands is highest priority before committing engineering time?
- Should Excel KPI handling be explicitly routed to a different owner/approach (non-vision) rather than silently dropped from our scope?
- Is there existing budget/GPU-quota reality (per the earlier Magma-hosting research) that constrains which model we could use for a financial-KPI vision extension — i.e., does this need to run on Gemini (real spatial grounding) rather than the GPT-4o "magma" stand-in, which this session confirmed cannot reliably produce structured points?
  - *Update 2026-09-29:* real Magma-8B is listed in the Foundry catalog. It may be deployable inside Azure on Foundry Managed Compute (preview), which requires a managed-compute GPU quota request, but availability depends on project and region. That makes the GPU-quota question concrete rather than hypothetical. See `docs/magma-readiness.md`.
