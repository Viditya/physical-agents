# Abbott Laboratories

**Last seen in top 5:** Week of 2026-09-07
**ARR:** USD 250,200 (≈ EUR 213,098) — License expansion, United States
**Website:** abbott.com
**Industry:** Healthcare manufacturer — pharmaceuticals, diagnostics, nutritionals, and medical devices, with 31 manufacturing sites and 12 development centers worldwide.

**Why it fits Physical Agents:** Abbott runs global manufacturing and quality operations that depend heavily on engineering drawings, device schematics, and equipment/facility diagrams — exactly the image-heavy document types this prototype targets. A manufacturer of this scale also has real document volume and regulatory pressure (device/drug manufacturing records) that make an AI-assisted document-reading layer attractive.

**Demoable use cases:**
1. Feed a medical-device assembly or panel drawing through the Gemini Robotics-ER 2 provider and show detected components/callouts overlaid on the page via `prototype/server.py`.
2. Use the Azure AI Foundry provider to describe/label parts on an equipment schematic, positioning it as the "stay-in-Azure" option for a customer already invested in Microsoft tooling.
3. Run the same drawing through both providers side by side in the web demo to compare point-detection accuracy for a manufacturing quality/compliance conversation.
