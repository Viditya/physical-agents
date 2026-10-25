# Complex public engineering fixtures: Gemini ER 2 versus Azure Foundry 4Omni

**Run date:** 2026-09-25
**Status:** Small qualitative comparison; not an accuracy benchmark.

## Shared conditions

Both providers received the exact same source fixture and its manifest-recorded
prompt. The prompts requested no more than 20 labelled features and required
only this normalized coordinate shape:

```json
[{"point": [y, x], "label": "short label"}]
```

| Demo provider name | Actual model/deployment |
|---|---|
| `gemini` | `gemini-robotics-er-2-preview` |
| `magma` | Azure AI Foundry deployment `4Omni`; this is not Microsoft Magma |

Every result includes the manifest prompt, source SHA-256, title, source URL,
licence/rights value, raw provider response, rendered source page, and overlay.

## Result matrix

| Fixture | Gemini points | Foundry points | Side-by-side overlay |
|---|---:|---:|---|
| LEVIA H7 Sensors schematic | 14 | 20 | `demo-results/public-levia-h7-sensors-schematic-page/comparison/gemini-er2-vs-foundry-4omni.jpg` |
| Titan I cutaway, sheet 3 | 20 | 20 | `demo-results/public-titan-i-missile-complex-sheet-3/comparison/gemini-er2-vs-foundry-4omni.jpg` |
| Bollman bridge, sheet 4 | 14 | 19 | `demo-results/public-bollman-truss-bridge-sheet-4/comparison/gemini-er2-vs-foundry-4omni.jpg` |

All six responses in this small complex-fixture run were parseable point lists
and all six overlays were rendered.

## Qualitative observations

- **LEVIA sensor schematic:** Gemini groups sensors, buses, blocks, and title
  information. Foundry returns more granular individual nets/reference
  designators. The different label granularity is not a correctness score.
- **Titan cutaway:** both overlays point to structures, rooms, sections, scale,
  and title-block/cutaway concepts. Foundry labels a broader range of requested
  architectural and mechanical features; visual plausibility does not prove
  every point is correctly grounded.
- **Bollman bridge:** both overlays cover structural members, joints, detail
  views, dimensions, material notes, and title-block regions. Foundry returns
  closer to the requested maximum item count.

## Limits

- Point count and label specificity do not measure spatial accuracy.
- Three complex drawings are insufficient to rank models, measure robustness,
  or make a production-readiness claim.
- The model outputs are unannotated claims. A future labelled region set and
  matching tolerance are required for accuracy measurement.
- The result calls the Foundry provider `magma` only for legacy demo routing;
  it must not be represented as a hosted Microsoft Magma model.
- Preserve the CERN-OHL-S and Library of Congress provenance/rights records in
  the fixture manifest when reusing the assets or derivative overlays.
