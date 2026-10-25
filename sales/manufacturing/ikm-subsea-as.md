# IKM Subsea AS

**Last seen in top 5:** Week of 2026-10-04
**ARR:** EUR 56,194, Norway — deal note: "(PULL FORWARD) IKM Subsea AS - asset document managment"
**Website:** ikm.com
**Industry:** ROV and trencher manufacturer and subsea operator (verified via search snippets only -- direct site fetch was blocked, not independently confirmed from the company's own site). Head office in Bryne, Norway, established 2007, ~250 employees; builds and operates work-class ROVs and trenchers (e.g. the electric Merlin WROV) and rents them out with crews (Rigzone directory, NORWEP partner listing, Offshore Magazine).

**Why it fits Physical Agents:** The deal is explicitly for asset document management. ROV/trencher fleets carry GA drawings, hydraulic/electrical schematics and maintenance diagrams per asset — exactly the image-heavy content this prototype targets.

**Demoable use cases:**
1. Run an ROV general-arrangement drawing through the Gemini Robotics-ER 2 provider in the web demo (`prototype/server.py`) and overlay points on named components (thrusters, manipulator, tether termination).
2. Use the Azure AI Foundry provider on a hydraulic schematic and compare its overlay with Gemini's in `demo-results/`.
3. Show cached re-runs (`.vman-vision-cache/`) to illustrate how repeated lookups on the same asset drawing avoid repeat API cost.
