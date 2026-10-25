# Rauma Marine Constructions Oy

**Last seen in top 5:** Week of 2026-09-18
**ARR:** EUR 88,196 — Finland
**Website:** rmcfinland.fi
**Industry:** Shipbuilding manufacturer (verified via search snippets only — direct site fetch was blocked, not independently confirmed from the company's own site). Builds car ferries, icebreakers, and naval vessels (including multi-purpose corvettes) at the Rauma shipyard; ~342 employees, €253M 2025 revenue.

**Why it fits Physical Agents:** Shipbuilding runs on dense, image-heavy technical drawings — hull sections, steel-fabrication diagrams, corvette/naval-vessel assembly schematics. That's exactly the class of document this prototype is built to read, and a shipyard scaling up production capacity (new multi-purpose hall, steel production investment) is likely generating and reviewing a large volume of such drawings.

**Demoable use cases:**
1. Run a hull-section or steel-fabrication drawing through the Gemini Robotics-ER 2 provider and show detected structural callouts overlaid on the page via `prototype/server.py`.
2. Use the Azure AI Foundry provider on a naval-vessel assembly schematic to compare point-detection accuracy against Gemini on the same drawing.
3. Show the cached-result feature (`.vman-vision-cache/`) so repeated QA review of the same fabrication drawing during a build cycle doesn't burn API tokens.
