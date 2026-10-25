# Agilera Pharma AS

**Last seen in top 5:** Week of 2026-10-11
**ARR:** EUR 29,127, Norway — deal note: "Additional license for Agilera"
**Website:** agilera.no
**Industry:** Radiopharmaceutical CDMO/CMO and manufacturer (verified via search snippets only -- direct site fetch was blocked, not independently confirmed from the company's own site). Based in Kjeller, Norway; spun out of the Institute for Energy Technology (IFE) in 2023; three business areas: CDMO development of radiopharmaceuticals from early phase to clinical production, CMO commercial production, and wholesale/distribution as Norway's national radiopharmaceutical wholesaler; GMP certified and licensed by the Norwegian Medicines Agency; ~130+ employees. PharmaLogic acquired a majority stake in 2025 (1881.no registry listing under pharmaceutical production, Mergr, Outsourced Pharma, 2026 job listing).

**Why it fits Physical Agents:** GMP radiopharmaceutical production relies on controlled batch records, cleanroom and hot-cell layouts, equipment drawings and labelled process diagrams — image-heavy documents where locating specific elements matters for audits and tech transfer. An existing customer adding licenses is a warm demo audience.

**Demoable use cases:**
1. Upload a cleanroom/hot-cell layout PDF to the prototype web demo (`prototype/server.py`), render it server-side, and have the Gemini Robotics-ER 2 provider point to named equipment, with the point overlay on the page.
2. Point-detect labelled valves, vessels and instruments on a process/P&ID-style diagram from a tech-transfer package.
3. Run the same page through the Azure AI Foundry provider and compare detections side by side for a regulated-industry (GMP) audience.
