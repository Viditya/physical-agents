# Pitch Deck Source Notes

This folder holds raw notes, outlines, and supporting material for the pitch deck.

The deck itself (slides) is kept separately. Add content here as bullet points,
narrative sections, or supporting data that feeds into the presentation.

## Sections to cover

- Problem statement
- Solution overview
- Technology: Gemini Robotics-ER 2 & Microsoft Magma
- M-Files integration approach
- Demo / prototype walkthrough
- Roadmap
- Team

## Pitch-relevant updates

- **2026-08-23**: Competitive landscape check found point-solution vendors already shipping VLM-based engineering-drawing/P&ID digitization — Acuvate's "DiagramIQ," Pathnovo, and LlamaIndex/LlamaParse (all marketed in 2026). A Springer *AI Review* survey (94 studies, 2020–2026) confirms this is now an established sub-area, not a gap. None of them appear to integrate with a DMS/vault metadata layer — that integration is still the open differentiator. **Action for the pitch**: stop leading with "we can read engineering drawings with a VLM" (no longer novel) and lead instead with the M-Files vault/metadata/workflow integration, since that's where no competitor identified so far is playing. See RESEARCH_LOG.md 2026-08-23 for sources.
- **2026-08-24**: Autodesk shipped "Autodesk Assistant" as a Tech Preview built directly into **Vault 2027** (released March 2026) — a conversational AI assistant inside a major engineering-vault/PDM product, doing natural-language search over parts/drawings/project data and task automation (e.g. flagging which associated drawings need updating after a change) by reasoning over Vault's existing file/item relationships. It is **not** vision-spatial extraction of drawing *content* (no evidence it reads pixels with a VLM — it works off metadata Vault already tracks), so it doesn't directly compete with VMAN Vision's core capability. But it's the closest real analog yet found to "a major vault vendor puts a conversational AI assistant in front of engineering files," and it raises the bar for the pitch: the differentiator now has to be demonstrably *reading what's in the drawing* (extracting structure/content a VLM sees that the vault's existing metadata graph doesn't already know), not just *conversing about what the vault already knows*. **Action for the pitch**: sharpen the demo to visibly show extraction of information that isn't already in vault metadata (e.g. reading dimensions, callouts, or revision marks directly off the drawing image) — a "chat with your vault" framing alone is no longer differentiated now that Autodesk has one. See RESEARCH_LOG.md 2026-08-24 for sources.
- **2026-08-26 (correction to the 2026-08-23 entry)**: found an existing product — **SymphonyAI's IRIS Foundry** "P&ID Ingestion" (platform launched 2024, still Azure-based and actively marketed) — that pairs VLM-based P&ID extraction *with* integration into a structured downstream system: it matches extracted tags/valves/instruments to the customer's existing CMMS/EAM/industrial knowledge graph (or builds one from the diagrams if none exists). That means the 2026-08-23 claim "none of these appear to integrate with a DMS/vault metadata layer" is no longer fully accurate — at least one vendor already does extraction-plus-integration, just for industrial asset-management systems (CMMS/EAM), not a general document/records vault like M-Files. **Action for the pitch**: keep leading with the M-Files vault/metadata/workflow integration angle (still not directly matched for a *document management* system), but stop claiming no one combines extraction with system integration at all — narrow the differentiation claim to "no one is doing this for a general-purpose document/records vault," since that's the part still true. See RESEARCH_LOG.md 2026-08-26 for sources.
