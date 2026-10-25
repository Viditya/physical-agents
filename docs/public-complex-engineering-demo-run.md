# Complex public engineering demo run

**Run date:** 2026-09-25
**Provider/model:** Gemini Robotics ER 2,
`gemini-robotics-er-2-preview`
**Hypothesis:** Fixture-specific, up-to-20-label prompts can make the existing
point-and-label demo more informative on complex public engineering drawings
than a single generic prompt.

## New public fixtures

| Fixture | Discipline | Licence/rights record | Rendered Gemini points | Rendered Foundry points |
|---|---|---|---:|
| LEVIA H7 Sensors schematic, declared PDF page 7 | Electrical/PCB | CERN-OHL-S-2.0 | 14 | 20 |
| Titan I Missile Complex 3, sheet 3 | Structural/mechanical/architectural | LOC rights advisory: no known restrictions on publication | 20 | 20 |
| Bollman Truss Railroad Bridge, sheet 4 | Structural/civil | LOC rights advisory: no known restrictions on publication | 14 | 19 |

Exact source URLs, fixed source revisions where available, licences, rights
advisories, transformation details, attribution, and prompts are in
[`../fixtures/public-fixtures.json`](../fixtures/public-fixtures.json).

## Dynamic prompt selection

`/api/config` now provides every known fixture's title and prompt. The browser:

1. uses the selected sample's recorded prompt on page load and whenever the
   sample changes;
2. restores the generic fallback prompt only when a user chooses an uploaded
   file;
3. sends the displayed prompt with the analysis request, preserving it in the
   saved result.

This makes the prompt part of fixture provenance rather than an undocumented
operator choice.

## Evidence

For each fixture, `demo-results/<fixture>/gemini/` includes:

- `result.json`, containing source SHA-256, source/licence reference, prompt,
  model response, and point count;
- `rendered.png`, the actual image sent to the provider;
- `overlay.png`, the provider-returned normalized points rendered back onto
  that image.

Each new fixture also has a matching Azure Foundry 4Omni run under
`demo-results/<fixture>/magma/` and an overlay-to-overlay comparison sheet
under `demo-results/<fixture>/comparison/`. See
[the complex shared-prompt comparison report](public-complex-engineering-gemini-foundry-comparison.md).

## Observations and limitations

- The LEVIA overlay locates distinct sensors, accelerometer/magnetometer/
  barometer blocks, buses, and the title area. It produced 14 rather than the
  requested maximum of 20 labels.
- The Titan cutaway reached the 20-label limit across rooms, tunnels, cutaway
  sections, scale, portal, and title-block regions.
- The Bollman bridge sheet identified mixed structural/detail features,
  including chords, joints, members, beams, dimensions, and title-block area.
- Re-running a preview model can vary the exact observations and count. The
  table records the canonical UI-saved run committed with this branch; raw
  response and overlay remain paired with that run in `demo-results/`.
- These are model-provided claims reviewed visually for demo suitability. They
  are not an annotated accuracy score, an exhaustive extraction, or a
  production-readiness conclusion.
- The rights advisory on a Library of Congress item is not equivalent to a
  Creative Commons licence. Keep the recorded source record and advisory when
  reusing the archival sheets.
