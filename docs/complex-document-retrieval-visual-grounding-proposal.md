# Complex-Document Retrieval Bridge: Visual Grounding as Metadata-Agent Enrichment

**Status (2026-09-11): Proposal and experiment design.** This document separates demonstrated Gemini point-and-label output from the untested hypothesis that visual evidence improves metadata extraction or retrieval.

## Context

Q4 planning item (owners: Vatsal Kariya, Antti Nivala, Raphaël Allègre, Brian Remmington):

> **Complex Document Retrieval and Foundation:** Align the MCP, metadata-agent and platform teams on the ownership and implementation boundary for complex-document retrieval, and return with a unified proposal.

I am not formally part of this working group, but the vision-PoC in this repo can contribute bounded, demonstrated evidence to that discussion — not by replacing metadata-agent/MCP, but by evaluating a bridge layer they can consume.

## Claim status: demonstrated versus unproven

### Demonstrated in this repository

Gemini Robotics ER 2 has been run against the six customer PDFs in `OCR/`. Each corresponding `demo-results/<document>/gemini/result.json` contains a rendered-page response with normalized `[y, x]` point coordinates and a free-text label, for example:

```json
{
  "point": [665, 929],
  "label": "title block field"
}
```

The generated `rendered.png` and `overlay.png` files make those points inspectable. This demonstrates the model's ability to return point-and-label observations for the current engineering-drawing prompt. It does **not** prove accuracy for customer financial documents, charts, logos, KPI screenshots, PPTs, Excel, or metadata extraction.

### Hypothesis to test

> Gemini (or an equivalent spatial-grounding-capable model) **may** provide a visual grounding layer for complex documents. Metadata-agent / MCP / platform retrieval work could consume that layer as structured evidence to improve extraction and source attribution, without replacing their parsing/retrieval architecture.

This is an untested hypothesis. No metadata-agent baseline, enriched run, labelled evaluation set, or measured improvement currently exists in this repository.

## Why this matters for the customer requirements

The customer (source of the OCR-folder PDFs) asked for documents containing:
- pictures
- logotypes
- graphs
- financial KPIs in various formats (some of which are pictures)
- financial KPIs in tables within PPTs
- financial KPIs in tables within PDFs
- financial KPIs in Excel sheets in varying formats
- improved source attribution across the board

The AI-Metadata team's `metadata-poc` (LlamaParse parser + existing "Images" processing mode) is architected for parsing fidelity — clean text/tables/page-images out of documents. It is not architected for *visual semantic reasoning* — understanding what a chart/graph/KPI-picture/logo actually communicates, or pointing back to exactly where an answer came from on a page.

That reasoning + pointing capability is the area Gemini Robotics ER 2 is intended to address, and the current PoC demonstrates point-and-label output on engineering drawings. Its value on the stated customer requirements must still be evaluated.

## Proposed artifact: visual evidence enrichment (**illustrative; not produced today**)

Before or alongside metadata-agent's text extraction, an integration could transform Gemini output into a structured visual-evidence layer per page/image:

```json
{
  "document": "customer-report.pdf",
  "page": 4,
  "visual_evidence": [
    {
      "label": "Revenue growth chart showing 18% YoY increase",
      "point": [412, 690],
      "region_hint": "chart",
      "source": "gemini-robotics-er"
    }
  ]
}
```

`page`, `region_hint`, and the enclosing `visual_evidence` representation above are integration-owned fields, not the raw Gemini response. In particular, the current Gemini response has no confidence score; do not create or imply one without a separately defined scoring method. Metadata-agent/MCP retrieval could then use this alongside text/OCR/table output as additional context, or as a candidate citation/attribution source. That integration has not been implemented or tested.

## What this could plausibly help with (**hypothesis; requires evaluation**)

- pictures inside documents
- logos / branded visual elements
- graphs and charts
- KPI screenshots (KPIs embedded as images)
- visual tables where OCR/parsing is weak
- source attribution: "this answer came from page 4, chart area near this coordinate"

## What visual grounding will not solve by itself

- **Excel with complex formulas:** use a spreadsheet-native parser and formula-aware processing. OCR or a vision model can help with screenshots, but cannot be the source of truth for workbook semantics.
- **Native PPT table semantics:** use a PPTX-native parser for tables, or render slides to page images only when visual reasoning is needed. Rendering loses native table structure.
- **Document-retrieval architecture:** MCP, metadata-agent, and platform still own chunking, indexing, retrieval, ranking, tenancy, and citation contracts.
- **Foundry governance:** Gemini is not deployable in Microsoft Foundry today. The choices are an approved external Gemini/Vertex dependency, a Foundry-native substitute such as Azure Content Understanding, or using Gemini only in an offline benchmark.

## Recommended PoC experiment (Python first, target >90% threshold)

**Baseline (no Gemini):** Run metadata-agent, or a faithful equivalent, over the OCR/customer documents using its existing text/OCR/parser output only. This is the control condition; it does **not** use the existing Gemini output in `demo-results/`.

**Enriched:** Run the same metadata-agent input and prompt, then add Gemini visual labels/points (or boxes, if evaluated) as structured context:

```text
Document text:
...

Visual evidence:
- Page 2, chart area: "Financial KPI table showing ARR, churn, and gross margin"
- Page 3, logo area: "Customer company logo appears in top-left"
- Page 5, graph area: "Line chart indicates EBITDA margin decline from 2022 to 2024"
```

**Measure:** For each customer requirement, compare baseline vs. enriched.

| Requirement | Baseline metadata-agent | With Gemini visual evidence | Improved? |
|---|---:|---:|---|
| Pictures | ? | ? | |
| Logos | ? | ? | |
| Graphs | ? | ? | |
| KPI screenshots | ? | ? | |
| KPI PDF tables | ? | ? | |
| KPI PPT tables | ? | ? | |
| KPI Excel sheets | ? | ? | |
| Source attribution | ? | ? | |

Define an annotated evaluation set and scoring rubric before running this test; “accuracy/usefulness” must specify what counts as correct for each requirement and attribution. A >90% threshold is a proposed decision criterion, not a current result. It should be calculated only on a representative held-out customer sample and preferably jointly reviewed with the metadata-agent/MCP team.

## Scoped follow-up enabled by the Gemini Robotics ER 2 notebook

The [current Gemini Robotics ER 2 quickstart](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb) (the originally linked cookbook notebook now redirects here) documents both normalized point output and normalized `box_2d` output. It also describes code-execution patterns for zooming/cropping images before further inspection.

For this PoC, only two static-document experiments are in scope:

1. **Box versus point:** ask for boxes around chart, logo, KPI screenshot, and table regions on a small, labelled subset of the customer documents. Verify each box visually against the rendered page.
2. **Crop and re-inspect:** crop only a verified chart/KPI/table box at higher resolution, then ask a second focused extraction question. Compare the response to a full-page, one-shot response.

Robot orchestration and video-progress features from the notebook are out of scope. Neither bounding boxes nor crop-and-reinspect should be presented as an improvement until they are evaluated with the rubric above.

## Positioning statement

> "I have a working Python PoC that produces Gemini point-and-label visual observations on engineering drawings. It does not replace metadata-agent or MCP retrieval. I propose evaluating whether a governed visual-evidence layer can improve complex-document extraction and attribution beyond text/OCR-only retrieval."

## Open questions

1. Does this get positioned as a permanent architectural layer, or first as an offline evaluation/benchmark tool to determine whether visual grounding is worth building or buying into the platform?
2. If the org requires everything to run through Microsoft Foundry, Gemini is a blocker today (Gemini cannot be deployed from Foundry — see companion note on Foundry vs. Gemini). Options:
   - accept an external Gemini/Vertex API dependency for this layer,
   - wait for an equivalent Microsoft/Foundry-hosted grounding model,
   - or use Gemini-generated annotations purely as an offline benchmark/training/evaluation layer, not a production dependency.
3. Who validates the proposed >90% threshold — a joint evaluation with metadata-agent/MCP team using labelled test documents is preferred over self-reported PoC numbers.
4. Should this be proposed as an amendment/addendum to the existing differentiation plan (`docs/differentiation-plan-vs-metadata-poc.md`), or as a separate proposal directly addressed to the Q4 planning group?

## Addendum: Gemini vs. Azure Document Intelligence / Content Understanding

### Short answer

Gemini and Azure Document Intelligence are not the same class of tool.

- **Azure Document Intelligence** is the stronger enterprise-first parser/OCR/layout tool. It reliably returns structured JSON/Markdown for pages, text, words, tables, cells, selection marks, figures, sections, bounding polygons, spans, and reading/layout structure. It supports PDFs, images, Word, Excel, PowerPoint, and HTML in the v4.0 layout model.
- **Azure Content Understanding** is now the more relevant Azure-native direction for complex-document retrieval. It can extract text and images with location metadata, preserve tables including cross-page tables, do semantic chunking, and, in newer preview API versions, generate AI descriptions for embedded images, charts, diagrams, and figures using an Azure OpenAI deployment attached to the Foundry resource.
- **Gemini** is stronger where the task is open-ended visual reasoning and spatial grounding: "look at this page/image/chart/drawing and tell me what visually matters, where it is, and why." Gemini document processing can analyze PDFs using native vision, including text, images, diagrams, charts, and tables, and can return structured output. Gemini spatial/grounding examples use normalized point/box coordinates, which is why it works well for the current visual-pointing PoC.

### Practical comparison for complex documents

| Capability | Azure Document Intelligence | Azure Content Understanding | Gemini / Gemini Robotics-style grounding |
|---|---|---|---|
| OCR / printed text extraction | Very strong, production-oriented | Strong, via document analyzers | Strong, but not primarily an OCR product |
| Layout JSON | Strong: pages, lines, words, spans, polygons | Stronger for retrieval pipelines: chunks plus location metadata | Prompt/schema-dependent |
| Tables | Strong for PDF/image tables; cell polygons and spans | Strong, including cross-page table handling | Good for visual/table reasoning, but less deterministic as a parser |
| Office docs | Layout model supports DOCX/XLSX/PPTX/HTML; note some embedded image behavior limits by file type | Supports PDF, images, DOCX, XLSX, PPTX, HTML, TXT, MD, RTF, EML | PDFs/images are the native sweet spot; non-PDF docs may lose visual context unless rendered |
| Charts/diagrams/images | Can identify figures and bounding regions, but not always explain chart semantics | Can generate AI descriptions for embedded charts/diagrams/images in newer preview APIs | Strong open-ended visual reasoning and pointing |
| Source attribution | Strong for text/table source polygons/spans | Stronger retrieval story: location metadata, image snippets, semantic chunks | Strong for visual point/box evidence, but needs external pipeline governance |
| Foundry/Azure governance | Native | Native | Not deployable in Microsoft Foundry today; external Google/Vertex/Gemini dependency |

### Would an LLM do a better job on JSON returned by Document Intelligence?

Yes - this is probably the best Azure-native architecture to test first.

A good pipeline is:

1. Use **Document Intelligence / Content Understanding** as the deterministic extraction layer.
   - It gives trustworthy page numbers, text spans, table cells, figures, and bounding polygons.
   - This is better than asking an LLM to invent document structure from pixels alone.
2. Convert the output into LLM-friendly Markdown or compact JSON.
   - Document Intelligence v4.0 can output Markdown.
   - Content Understanding already outputs tables/figures in Markdown and can generate retrieval-oriented chunks.
3. Ask an LLM to reason over that extracted structure.
   - The LLM can infer KPI meaning, normalize field names, summarize trends, compare periods, and produce business metadata.
4. Keep Document Intelligence / Content Understanding coordinates as the citation layer.
   - The LLM should not be trusted to invent source attribution. It should cite back to page/span/polygon IDs emitted by the parser.

This could beat Gemini for many enterprise document scenarios because it combines deterministic extraction + governed Azure hosting + LLM reasoning. It may still lose to Gemini-style grounding on open-ended visual questions like "which part of this engineering drawing indicates the issue?" or "point to the visual KPI/chart element that supports this conclusion."

### Recommendation before going outside Azure

Before arguing for Gemini as a dependency, run a three-way evaluation on the same customer documents:

1. **Azure baseline:** Document Intelligence layout JSON/Markdown + LLM reasoning.
2. **Azure advanced:** Azure Content Understanding + semantic chunks + AI-generated image/chart descriptions + LLM reasoning.
3. **Gemini visual grounding:** Gemini-generated labels/points, and boxes only if the scoped box experiment is run, used as extra visual evidence.

The key measurement should not be generic OCR accuracy. It should be whether each pipeline answers the customer's complex-document asks with evidence:

- Did it identify KPIs in text tables?
- Did it identify KPIs embedded as images?
- Did it understand charts/graphs, not just OCR labels?
- Did it preserve source attribution to page/region/span?
- Did it work on PPT/PDF/Excel samples?
- Did it reach the proposed >90% threshold on representative, labelled customer documents?

### Updated position

The strongest internal position is not "Gemini is better than Azure Document Intelligence." The stronger and safer position is:

> Start Azure-native: Document Intelligence / Content Understanding should be the extraction and citation foundation. Use an LLM on top of their JSON/Markdown to improve semantic answers. Use Gemini-style visual grounding only as a benchmark or add-on for the visual cases Azure still cannot solve well enough, especially open-ended chart/image/drawing pointing.

### Sources checked

- Microsoft Learn: [Document Intelligence layout model](https://learn.microsoft.com/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0)
- Microsoft Learn: [Azure Content Understanding skill](https://learn.microsoft.com/azure/search/cognitive-search-skill-content-understanding)
- Microsoft Learn: [Multimodal search in Azure AI Search](https://learn.microsoft.com/azure/search/multimodal-search-overview)
- Google AI for Developers: [Gemini document processing](https://ai.google.dev/gemini-api/docs/document-processing)
- Google Gemini robotics samples: [Gemini Robotics ER 2 quickstart](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb)
