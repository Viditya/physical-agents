# Gemini ER 2 versus Azure AI Foundry Vision: qualitative drawing comparison

**Run date:** 2026-09-18
**Status:** Completed qualitative review; not a benchmark or accuracy claim.
**Scope:** Six locally available engineering and operational PDFs, one rendered
page per PDF, and the same point-and-label prompt for both providers.

## Purpose

Assess whether the Azure AI Foundry deployment configured as `4Omni` can be
presented as comparable to Gemini Robotics ER 2 for the current drawing
pointing demo.

It cannot be presented that way from this experiment. The two providers
sometimes produce useful observations, but their output reliability and the
kind of value observed differ.

## Conditions

| Item | Gemini | Azure Foundry vision |
|---|---|---|
| Provider result | Previously saved Gemini ER 2 response | Fresh 2026-09-18 response |
| Model/deployment | `gemini-robotics-er-2-preview` | `4Omni` |
| Prompt | Same point-and-label drawing prompt, limited to 20 items | Same |
| Input | Same PDF page rendered to PNG | Same |
| Output accepted for overlay | Valid JSON list of point-bearing objects | Valid JSON list of point-bearing objects, including a Markdown-fenced list |
| Evaluation method | Visual review of points over the page | Visual review of points over the page |

The Foundry provider is retained under the demo name `magma` for compatibility.
It is an Azure AI Foundry vision deployment used as a stand-in, **not**
Microsoft Magma.

With explicit approval for internal sharing, fresh Foundry comparison responses
and their rendered pages are published under
`demo-results/<document>/magma/`. Every folder now includes a renderable
overlay after two same-prompt retries succeeded. The malformed first attempts
remain preserved as `fresh-comparison-result.json`; no points were invented
from those responses. MON-23's earlier renderable response is retained
separately as `earlier-valid-result.json`.

Compressed, labelled visual comparison sheets are published under
`demo-results/<document>/comparison/gemini-er2-vs-foundry-4omni.jpg`. They
show Gemini on the left and a renderable Foundry run on the right for all six
documents. For MON-23 and MON-90, the right panel is the successful
same-prompt retry. The first malformed attempts are retained in separately
named `*-first-attempt-malformed.jpg` sheets for those two documents. MON-23 also includes
`gemini-er2-vs-foundry-4omni-earlier-valid-run.jpg`, which compares Gemini
against its earlier renderable Foundry overlay. The adjacent comparison README
distinguishes that visual overlay comparison from the fresh-run reliability
check.

## Result summary

| Measure | Gemini ER 2 | Azure Foundry 4Omni |
|---|---:|---:|
| Documents with a successful service response | 6/6 saved runs | 6/6 first attempts; 2/2 retries |
| Documents with a renderable point list | 6/6 | 4/6 first attempts; 6/6 after same-prompt retries |
| Documents with 20 rendered points | 6/6 | 4/6 first attempts; 6/6 after same-prompt retries |
| Documents with malformed JSON on the first attempt | 0/6 | 2/6 |

The two Foundry malformed first attempts were not silent failures: they returned
coordinate-looking text that was not valid JSON. The adapter preserved the raw
responses and correctly declined to create point evidence from them. Retrying
the same original prompt once returned valid lists for both, but the first-run
parse failure remains a reliability limitation.

## Per-document observations

| Document identifier | Gemini ER 2 visual review | Azure Foundry 4Omni visual review | Finding |
|---|---|---|---|
| `MON-23-70912` | Points align broadly with pile symbols, grid bubbles, dimensions, title-block fields, and revision area. | First response was malformed JSON; the same-prompt retry returned 20 points and supports the current side-by-side sheet. An earlier renderable run contains visibly misplaced title-block and revision claims. | A current overlay-to-overlay comparison exists, but Foundry localisation is visibly inconsistent across its runs. |
| `MON-24-13900` | Generic component, section, and title-block labels are broadly associated with visible regions. | Returned a renderable point list; section/title-block labels appear broadly associated with the expected areas in this visual review. | Foundry is plausible here, but unscored. |
| `MON-24-70900` | Generic component and dimension labels are broadly placed near drawing features. | Returned richer labels such as dimensions, a title, and title-block fields. Many appear near relevant features, but some labels need a labelled review to establish coordinate correctness. | Foundry text specificity is promising; localisation is not validated. |
| `MON-25-13101` | Generic labels are placed on the table, logo/title area, and selected cells. | Returned detailed table/header/logo/value labels whose markers broadly align with visible table areas. | Foundry is promising for structured table/image reading; this is not a spatial-accuracy score. |
| `MON-25-13102` | Points identify selected embedded images and visible document areas. | Returned detailed SOP metadata and image labels; markers broadly align with the header, text blocks, and embedded images. | Foundry is promising for content description on this operational-document input. |
| `MON-90-33900` | Points align broadly with drawing identifiers and structural regions. | First response was malformed JSON; the same-prompt retry returned 20 points and supports the current side-by-side sheet. | A current overlay-to-overlay comparison exists; first-run parsing reliability remains a limitation. |

“Broadly align” is a human visual observation from this small sample. It does
not mean all coordinates or labels are correct.

## What can be claimed

- Gemini ER 2 produced a parseable, rendered point list on all six saved
  sample runs under the current prompt.
- Azure Foundry 4Omni produced parseable point lists in four of six fresh runs;
  two responses were malformed and could not be safely rendered.
- Foundry returned more detailed text labels on some table- and SOP-like
  inputs, but its coordinate quality was inconsistent in the reviewed drawing
  cases.
- A JSON-shaped response or a rendered overlay is not, by itself, evidence of
  accurate spatial grounding.

## What must not be claimed

- That `4Omni` is Microsoft Magma.
- That `4Omni` matches Gemini ER 2 spatial-grounding quality.
- A percentage accuracy, production-readiness conclusion, or general model
  ranking.
- That either provider solves complex-document retrieval, metadata-agent
  integration, or the DI/CU evaluation tracked in
  `complex-document-grounding-poc`.

## Implications for the current demo

Use Gemini ER 2 as the spatial-pointing demonstration. Present the Foundry
4Omni result only as an Azure-bound comparison: it can produce useful,
detailed visual/text observations, but its current coordinate output requires
validation before it can support source attribution or a spatial-grounding
claim.

The adapter now parses valid Markdown-fenced point JSON and refuses malformed
JSON. This protects the demo from presenting a partial model response as
verified coordinates.

## Cookbook-inspired follow-up, outside this repository

The original
[Gemini Robotics ER notebook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/gemini-robotics-er.ipynb)
is now a redirect to the
[Gemini Robotics samples repository](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb).
That robotics quickstart documents normalized points, `box_2d` output, and
crop/zoom/re-inspect workflows.

The general cookbook’s
[spatial-understanding notebook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Spatial_understanding.ipynb)
adds explicit bounding-box instructions and uses the current Interactions API.
Its [PDF notebook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/PDF_Files.ipynb)
shows direct PDF input through the Interactions/File APIs. Those are useful
implementation references, but are untested in this repository.

A separate cookbook-inspired experiment repository is appropriate for direct
PDF, bounding-box, crop/re-inspect, general spatial, and video experiments.
It should start with an approved scope, local-only data handling, a shared
evaluation rubric, and an explicit relationship to this repository rather than
importing this prototype wholesale.

## Required next step for a quantitative comparison

Create a labelled test set with expected regions and labels, define matching
tolerance and scoring rules, run each provider with versioned prompts, and
record both successful and failed responses. Until then, the findings here are
qualitative evidence only.
