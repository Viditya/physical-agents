# Metromix

**Last seen in top 5:** Week of 2026-09-18
**ARR:** AUD 15,294 — Australia
**Website:** metromix.com.au
**Industry:** Ready-mix concrete and quarry-products manufacturer (verified via search snippets only — direct site fetch was blocked, not independently confirmed from the company's own site). Supplies concrete and quarry products to the Sydney construction-materials market, with 6 concrete plants and 3 quarries (Lithgow, Newcastle, Anna Bay). Note: multiple similarly-named Australian entities exist (a separate Melbourne-based "Metro Mix Concrete"); the win email does not disambiguate which entity, so this profile is based on the best-matching public identity.

**Why it fits Physical Agents:** Concrete/quarry manufacturing runs on batching sheets, mix-design specifications, and plant/equipment diagrams — image-heavy documents that fit this prototype's point-detection use case, particularly for multi-site operations tracking mix specs across plants and quarries.

**Demoable use cases:**
1. Run a concrete mix-design specification sheet through the Azure AI Foundry provider and show detected callouts overlaid via `prototype/server.py`.
2. Use the Gemini Robotics-ER 2 provider on a quarry/plant equipment diagram to detect labeled components.
3. Show the git-tracked `demo-results/` output so a plant-quality reviewer can check the latest overlay result from GitHub without re-running the model.
