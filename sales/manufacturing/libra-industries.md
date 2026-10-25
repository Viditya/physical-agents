# Libra Industries

**Last seen in top 5:** Week of 2026-10-04
**ARR:** USD 33,480, United States — deal note: "Extension Kit and Additional Expert Services"
**Website:** libraind.com
**Industry:** Electronics contract manufacturer / systems integrator (verified via search snippets only -- direct site fetch was blocked, not independently confirmed from the company's own site). Dayton, Ohio, founded 1980, four facilities (three in Ohio, one in Texas); PCBA, box build, precision machining, sheet metal and electro-mechanical assembly for aerospace/defence, medical, semiconductor capital equipment and industrial OEMs (Electronic Specifier, EMSNow, CB Insights).

**Why it fits Physical Agents:** An EMS provider receives assembly drawings, PCB layouts and wiring diagrams from many OEM customers; locating and labelling features on customer-supplied drawings is a recurring intake task.

**Demoable use cases:**
1. Upload a customer PCB assembly drawing to the web demo (`prototype/server.py`) and have the Gemini Robotics-ER 2 provider point to reference designators or connectors, shown as an overlay.
2. Use the CLI (`python -m prototype.cli --provider gemini --image ...`) to check sample box-build drawings one by one.
3. Compare Gemini and Azure AI Foundry overlays on the same sheet-metal drawing in `demo-results/`.
