# Patria Oyj

**Last seen in top 5:** Week of 2026-10-04
**ARR:** EUR 40,700, Finland — deal note: "SAP Connector - Patria Oyj" (previously in top 5 on Week of 2026-09-07 at EUR 19,812 for additional licenses)
**Website:** patriagroup.com
**Industry:** Finnish defence, security and aviation technology company (verified via search snippets only -- direct site fetch was blocked, not independently confirmed from the company's own site). 50.1% Finnish state / 49.9% Kongsberg owned; ~4,100 staff, 2025 net sales EUR 1,086.7M; manufactures 6x6 and AMV XP armoured vehicles in Hämeenlinna (Wikipedia, EDR Magazine, GlobalSecurity).

**Why it fits Physical Agents:** Defence/aerospace manufacturing and sustainment rely on dense technical and maintenance drawings under strict documentation control. The SAP connector purchase suggests documents are being tied to ERP/asset records, where data extracted from drawings is directly useful.

**Demoable use cases:**
1. Extract and label components from an armoured-vehicle or aircraft maintenance diagram using the Gemini Robotics-ER 2 provider (`gemini_robotics.py`) with the PDF rendering + point overlay in `prototype/server.py`.
2. Position the Azure AI Foundry provider for a defence customer wary of adding a second cloud vendor.
3. Show the raw JSON next to the overlay image (`demo-results/`) as an audit trail of what the model detected.
