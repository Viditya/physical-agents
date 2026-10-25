# Oklo Inc.

**Last seen in top 5:** Week of 2026-09-25
**ARR:** USD 99,360 (≈ EUR 84,626), United States
**Website:** oklo.com
**Industry:** Advanced nuclear fission power company (verified via search snippets only — direct site fetch was blocked, not independently confirmed from the company's own site). Publicly traded (NYSE: OKLO), building small modular "Aurora Powerhouse" fast fission reactors, nuclear fuel recycling, and critical-isotope production; holds a DOE site use permit for its first Idaho plant.

**Why it fits Physical Agents:** Oklo is designing and building a first-of-a-kind reactor and fuel-recycling supply chain, which means dense engineering drawings — reactor component schematics, fuel assembly diagrams, plant layout drawings — moving through licensing, manufacturing, and NRC review. That's the image-heavy, high-stakes document type this prototype is built to read.

**Demoable use cases:**
1. Run a reactor-component or plant-layout style engineering drawing through the Gemini Robotics-ER 2 provider and show detected parts/callouts overlaid on the page via `prototype/server.py`.
2. Use the Azure AI Foundry vision provider on a fuel-assembly schematic to demonstrate point-detection accuracy on safety-critical technical drawings.
3. Show the PDF-rendering + point-overlay pipeline end to end on a multi-page drawing set, framed as a triage aid for regulatory/manufacturing document review at nuclear scale.
