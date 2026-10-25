# Volume history

The book is published in numbered **volumes**. Each volume is a complete, readable snapshot of the whole book at a point in time. The Markdown chapters always show the **current** volume; every past volume's PDF is kept unchanged in [`volumes/`](volumes/), so you can see exactly what a reader had in front of them on a given date.

A new volume is cut when the book's substance changes: new chapters or sections, new facts that change a conclusion, or corrected claims. Typo fixes don't need a new volume.

| Volume | Date | What changed | Pull requests | PDF |
|---|---|---|---|---|
| **2** (current) | 2026-09-29 | Microsoft Magma. A new Chapter 4 section explains mark-based ("Set-of-Mark") grounding. Magma rows added to Chapters 1, 4, 10, 12 and 13. Glossary adds Set-of-Mark and Trace-of-Mark. New source [21]. Availability wording made precise: Foundry Managed Compute is preview, and availability depends on project, region and quota. Companion guide: `docs/magma-readiness.md` | #17, #18 | [volume-02-2026-09-29.pdf](volumes/volume-02-2026-09-29.pdf) |
| **1** | 2026-09-28 | First release. 13 chapters and 2 appendices: the capability map, the concepts, the re-weighted curriculum, and the handover guide | #16 | [volume-01-2026-09-28.pdf](volumes/volume-01-2026-09-28.pdf) |

Before Volume 1 there was a six-page personal guide, *Physical Agents and World Models: Zero-to-Hero* (curated 2026-09-25). It is not in this repository.

## How to cut a new volume

1. Edit the chapters on a topic branch as usual. All the steps below go in the same pull request.
2. Bump `volume` and `date` in [`volume.json`](volume.json).
3. Update the volume line at the top of [README.md](README.md) to match. The build refuses to run if they disagree.
4. Add a row at the **top** of the table above.
5. Build and freeze the PDF:

   ```bash
   python book/tools/build_pdf.py --release
   ```

   This writes the current PDF and also saves `volumes/volume-NN-YYYY-MM-DD.pdf`. It will not overwrite an existing frozen volume. Past volumes are never edited.
