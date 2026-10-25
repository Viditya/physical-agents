# Appendix B — Sources and verification status

Every bracketed number in this book points here. Numbers [1]–[12] match the VMAN Vision pitch deck's Sources slide so the two stay consistent.

**How to read the "Verified" column:** the date the claim was last checked against the source itself. Anything older than about a month should be re-checked before it's repeated to a stakeholder — especially preview model capabilities and competitor moves.

## External sources

| # | Source | Used for | Verified |
|---|---|---|---|
| [1] | Jim Fan (NVIDIA), "Robotics' End Game," Sequoia Capital AI Ascent 2026 — youtube.com/watch?v=3Y8aq_ofEVs | Robotics repeating the LLM playbook; data ladder; world action models | 2026-09 (transcript) |
| [2] | Starship Technologies / S-Group, 1M+ grocery deliveries in Finland — starship.xyz | Pitch deck context | 2026-09 |
| [3] | Wolt + Coco robot delivery launch, Turku, Finland — cocodelivery.com | Pitch deck context | 2026-09 |
| [4] | Waymo scaling targets — forbes.com, techcrunch.com | Pitch deck context | 2026-09 |
| [5] | McKinsey Live, "Physical AI's Hidden Value Pools Leaders Miss" (Ani Kelkar & Mark Patel), Sept 2026 — youtube.com/watch?v=Lt7K3jdBsNo | $370B 2040 market; data pyramid; reliability ladder | 2026-09 (transcript + frames) |
| [6] | This repository — github.com/M-Files-AI/physical-agents-research | All "demonstrated" claims | 2026-09-28 |
| [7] | Google DeepMind, Gemini Robotics — deepmind.google/models/gemini-robotics | Model family overview | 2026-09-18 |
| [8] | LinkedIn Learning, "Physical AI Architecture Foundations: Designing Autonomous Machines with Agentic AI" | Background reading (pitch deck) | — |
| [13] | SAP News, physical-AI robotics pilots; SAP Sapphire 2026 announcements — news.sap.com | SAP Knowledge Graph; Tetra Pak / RobotEra lab PoC | 2026-09-25 (web search) |
| [14] | Palantir Ontology / AIP — palantir.com/platforms/ontology | Factory → line → machine → part ontology | 2026-09-25 (web search) |
| [15] | Siemens CES 2026 industrial-AI announcements; NVIDIA physical-AI ecosystem announcements; PTC Onshape → Isaac Sim | Digital twins, OpenUSD, partner ecosystem | 2026-09-25 (web search) |
| [16] | Industry reporting on factory humanoid deployments (Schaeffler/Humanoid, BMW, Samsung, Hyundai/Boston Dynamics, Tesla) — artificialintelligence-news.com, idc.com | "Real deployments are underway" | 2026-09-25 (web search) |
| [17] | Google Gemini API docs — robotics overview, ER 2 model page, spatial reasoning, agentic vision, Interactions API; google-gemini/robotics-samples quickstart | ER 2 capabilities, limits, data-handling rules | 2026-09-18 (via `docs/gemini-robotics-model-guide.md`) |
| [18] | Microsoft Learn — Document Intelligence layout model; Content Understanding; multimodal search in Azure AI Search | Azure-native options | 2026-09-11 (via `docs/complex-document-retrieval-visual-grounding-proposal.md`) |
| [19] | Model Context Protocol — modelcontextprotocol.io | MCP concepts | General reference |
| [21] | Yang et al., "Magma: A Foundation Model for Multimodal AI Agents," arXiv 2502.13130 (Feb 2025); `microsoft/Magma-8B` model card; `microsoft/Magma` repository; Foundry catalog entry `microsoft-magma-8b`; Microsoft Learn, "Hugging Face models in Microsoft Foundry" | Magma architecture, Set-of-Mark grounding, results, hosting via managed compute — collected in `docs/magma-readiness.md` | 2026-09-29 (paper read in full) |
| [20] | Competitive landscape: Acuvate DiagramIQ, Pathnovo, LlamaParse, SymphonyAI IRIS Foundry, Autodesk Vault 2027 Assistant, Bluebeam Max + Claude via MCP | Chapter 11 landscape | 2026-08-23 → 2026-09-25 (`RESEARCH_LOG.md`, `pitch/README.md`, web search) |

## Internal M-Files sources

| # | Source | Used for | Verified |
|---|---|---|---|
| [9] | Confluence (Product space), "Product Strategy 2025-26: Unleashing our Knowledge Graph Like Architecture combined with AI & Microsoft to win!" — Tony Grout, Aug 2025 | Knowledge-graph-like architecture; "knowledge graphs are a favored format for AI"; Microsoft alignment | 2026-09-25, read directly (in a separate session) |
| [10] | Confluence (VMAN space), "Manufacturing Blueprint" — Ville Somppi, status 2026-09-17 | Installed Base & Maintenance Knowledge (planned); non-compete stance; "records outcomes and recommends actions; it does not execute transactions" | 2026-09-25, read directly (in a separate session) |
| [11] | Confluence (APPS space), "2027 forward looking thoughts" — modified 2026-09-24 | "Validated design work, not yet built"; Forward Deployed Engineering | 2026-09-25, read directly (in a separate session) |
| [12] | Confluence, "CAD Integration Roadmap 2026–2029" — Sivaram Reddy, May 2026 | SMB/mid-market first; "wrap around PDM, not replace"; L3 engineering knowledge graph H1 2028; drawings as "opaque blobs" | 2026-09-25, read directly (in a separate session) |
| — | Confluence (AI space), "Beta Release for MCP server" — owner Vatsal Kariya | "Image reading is not available in Beta" | 2026-08-22 |
| — | Confluence, Aino architecture pages; "AI Foundation Platform for VTAX & VMAN: Multi-Agent Enablement" | Aino Search on text embeddings; planned Asset Management / Installed Base Intelligence Agent | 2026-08-22 — **re-verify** |
| — | AI-Metadata team `metadata-poc` design documents, as reviewed in `docs/differentiation-plan-vs-metadata-poc.md` | Images mode ≤10 MB; no region-level attribution concept | 2026-09-08 |
| — | Sibling repository `complex-document-grounding-poc`, `docs/evaluation-plan.md` | DI adapter status; evaluation phases | 2026-09-28 |

## Known gaps in verification

- Confluence could not be re-read while this edition was written (the connector needed re-authorisation), so [9]–[12] rely on the 2026-09-25 direct read. Re-check before quoting them externally.
- The Aino and AI Foundation facts date from 2026-08-22 and may have moved.
- Microsoft Magma's hosting status was re-checked 2026-09-29. It's listed in the Foundry catalog, and Hugging Face-collection models use Foundry Managed Compute (preview) where available. Availability in our project and region, the deployment SKU and the price were not visible without signing in.
- Preview model capabilities ([17]) can change without notice.
