# SynQor

**Last seen in top 5:** Week of 2026-10-04
**ARR:** USD 137,107, United States
**Website:** synqor.com
**Industry:** Power conversion electronics manufacturer (verified via search snippets only -- direct site fetch was blocked, not independently confirmed from the company's own site). Based in Boxborough, Massachusetts, founded 1997; designs and manufactures AC-DC/DC-DC converters, filters, ruggedized UPSs, power conditioners and inverters for military, aerospace, industrial, rail and medical markets in a 100,000 sq ft AS9100/ISO 9001 facility (Military & Aerospace Electronics directory, Australian Defence guide, GlobalSpec).

**Why it fits Physical Agents:** Hi-rel power electronics production runs on dense, image-heavy documents — PCB assembly drawings, mechanical outline drawings, datasheet pin-out diagrams — under aerospace-grade documentation control.

**Demoable use cases:**
1. Upload a converter mechanical outline / pin-out drawing (PDF) to `prototype/server.py`; it is rasterised server-side and the Gemini Robotics-ER 2 provider (`gemini_robotics.py`) points to labelled pins and mounting features, drawn back as an overlay.
2. Show the raw JSON alongside `overlay.png` in `demo-results/` as a traceable record of what was detected — relevant to AS9100 audit expectations.
3. Run the same drawing through the Azure AI Foundry vision provider and compare overlays, for a customer that may prefer staying inside an existing Microsoft tenancy.
