# Public engineering fixtures: Gemini ER 2 versus Azure Foundry 4Omni

**Run date:** 2026-09-24
**Status:** Small qualitative comparison; not an accuracy benchmark.

## Conditions

Both providers received the same rendered source image and the exact prompt
recorded for that fixture in
[`../fixtures/public-fixtures.json`](../fixtures/public-fixtures.json).

| Provider name in results | Actual model/deployment |
|---|---|
| `gemini` | `gemini-robotics-er-2-preview` |
| `magma` | Azure AI Foundry deployment `4Omni`; this is a stand-in name, not Microsoft Magma |

Every prompt required the same JSON array format:

```json
[{"point": [y, x], "label": "short label"}]
```

Coordinates are normalized to 0-1000. Each provider result retains source
hash, prompt, raw response, rendered page, and overlay under
`demo-results/<fixture>/<provider>/`.

## Result matrix

| Public fixture | Gemini points | Foundry points | Side-by-side artifact |
|---|---:|---:|---|
| ISO 5457 technical drawing template | 3 | 3 | `demo-results/public-technical-drawing-templates-iso-5457/comparison/gemini-er2-vs-foundry-4omni.jpg` |
| P&ID tank | 4 | 4 | `demo-results/public-pid-tank/comparison/gemini-er2-vs-foundry-4omni.jpg` |
| NASA Appendix A drawing symbols | 4 | 4 | `demo-results/public-nasa-engineering-drawing-symbols-page/comparison/gemini-er2-vs-foundry-4omni.jpg` |

All six provider responses in this small run were parseable point lists and
were rendered as overlays.

## Qualitative observations

- **ISO template:** both providers identified the border/title-block-style
  regions. This is a simple layout case and should not be used to distinguish
  spatial-grounding quality.
- **P&ID tank:** both providers placed labels near the tank and requested
  heating/outlet-control regions. The Foundry run labelled a downstream outlet
  valve; Gemini labelled the downstream outlet-control valve. A labelled region
  rubric is needed before deciding whether either placement is correct enough
  for process-engineering use.
- **NASA symbols:** both providers returned points near the requested drawing
  symbols. The overlays are useful visual evidence, but the source is a
  reference-symbol page rather than a complex assembly drawing.

## Limits

- Three public fixtures are insufficient for an accuracy, robustness, or cost
  comparison.
- Point lists show model claims; they are not source attribution guarantees.
- `4Omni` is not Microsoft Magma and must not be described as such.
- The public P&ID carries CC-BY-SA requirements recorded in the fixture
  manifest. NASA material must not imply NASA endorsement.

Do not combine this small public-fixture result into a headline model ranking.
