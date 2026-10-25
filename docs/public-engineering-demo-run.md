# Public engineering demo run

**Run date:** 2026-09-24
**Provider/model:** Gemini Robotics ER 2,
`gemini-robotics-er-2-preview`
**Hypothesis:** The existing point-and-label demonstration can operate on a
small, licence-recorded public engineering corpus.

## Inputs and prompts

The exact source URLs, licences, transformations, and prompts are recorded in
[`../fixtures/public-fixtures.json`](../fixtures/public-fixtures.json).

| Fixture | Discipline | Points rendered |
|---|---|---:|
| ISO 5457 technical drawing template | Drawing-layout conventions | 3 |
| P&ID tank | Process engineering | 4 |
| NASA Appendix A nonmandatory symbols | Aerospace/mechanical drawing practices | 4 |

## Evidence

For every fixture, `demo-results/<fixture>/gemini/` contains:

- `result.json`: source hash, source/licence reference, prompt, model result,
  and point count;
- `rendered.png`: the exact raster image sent to the provider;
- `overlay.png`: the returned points drawn on that image.

The original NASA source PDF is retained under `fixtures/`; the selected public
fixture is a declared page-40 rasterization, not the cover page.

Each fixture also has an Azure AI Foundry 4Omni run and a labelled
Gemini-versus-Foundry sheet under `demo-results/<fixture>/comparison/`. See
[the shared-prompt comparison report](public-engineering-gemini-foundry-comparison.md).

## Observations and limits

- The model returned the requested number of parseable point observations for
  all three fixtures in this run.
- The P&ID was composited on white before it was sent to the provider because
  its source PNG has transparency. The output preserved its visible process
  symbols and produced points for the requested tank and control loops.
- This is a compact demonstration, not a labelled spatial-accuracy benchmark.
  It does not establish performance across engineering disciplines, input
  qualities, or model versions.
- The assets are public/reusable under the individual terms recorded in the
  manifest. The CC-BY-SA P&ID requires the stated attribution/share-alike
  treatment in any redistribution; the NASA asset must not imply NASA
  endorsement.
