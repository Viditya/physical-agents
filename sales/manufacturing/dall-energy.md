# Dall Energy

**Last seen in top 5:** Week of 2026-09-07
**ARR:** EUR 81,900 — Engineering DMS, Denmark
**Website:** dallenergy.com
**Industry:** Danish biomass energy equipment manufacturer — engineers and builds patented low-emission, multifuel biomass furnaces.

**Why it fits Physical Agents:** The deal itself is for an "Engineering DMS," meaning Dall Energy already has engineering drawings as a core part of the sale — a natural fit for a vision-spatial layer that reads and annotates those drawings inside M-Files.

**Demoable use cases:**
1. Upload one of the sample engineering drawings in `OCR/` (or one of Dall Energy's own furnace/plant drawings) and run the CLI (`python -m prototype.cli --provider gemini`) to extract labeled points.
2. Show the web demo's PDF-to-image rendering step, since Dall Energy's engineering drawings are likely delivered as PDFs that need rasterizing before AI review.
3. Demonstrate the git-tracked `demo-results/` folder as a way to share extracted findings on a furnace schematic with a reviewer who doesn't have API keys.
