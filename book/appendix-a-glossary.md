# Appendix A — Glossary

| Term | Plain-language meaning | Chapter |
|---|---|---|
| **Action chunk** | A short sequence of future robot actions predicted in one go, instead of one command at a time | 6 |
| **Agent** | A system where a model repeatedly decides what to do next — call a tool, observe, decide again — until the goal is met | 9 |
| **Agentic RAG** | RAG where an agent decides what to search, when, and whether to search again | 8 |
| **Attribution (source)** | Pointing back to where an answer came from — document, page, and ideally region | 4, 8 |
| **Box (bounding box)** | A rectangle around an object; in Gemini ER 2, `[ymin, xmin, ymax, xmax]` on a 0–1000 grid | 4 |
| **CLIP** | A 2021 model that put images and text into one shared "meaning space" | 3 |
| **CNN** | Convolutional neural network — slides small learned filters over an image to find edges, shapes, objects | 3 |
| **Compounding error** | Small prediction mistakes that snowball when a model predicts many steps ahead | 5 |
| **Content Understanding (Azure)** | Azure service that extracts content with location metadata and can describe figures | 8, 10 |
| **Crop and re-inspect** | Zoom into a located region and ask a second, focused question | 4 |
| **Data pyramid / ladder** | Cheap video at the base, simulation in the middle, scarce real robot data at the top | 6 |
| **Decoder** | Turns a compact internal representation back into an output (image, text, action) | 5 |
| **Diffusion policy** | A robot policy that generates a distribution of action sequences and picks one coherent option | 6 |
| **Document Intelligence (Azure)** | Azure's OCR and layout service — text, tables, regions, with reliable citations | 3, 8 |
| **Dynamics** | The part of a world model that predicts the next state given the current state and an action | 5 |
| **Embedding** | A list of numbers representing the meaning of text or an image, so similar things sit close together | 3, 8 |
| **Encoder** | Compresses a large input (an image) into a compact representation (latent state) | 5 |
| **Evaluation set (labelled)** | Real inputs with human-marked correct answers, used to measure accuracy | 10 |
| **Forward Deployed Engineering** | M-Files' route for proving ideas with a real customer ahead of the core roadmap [11] | 1, 11 |
| **Function calling / tool calling** | A model requesting that your system run a described function | 9 |
| **GraphRAG** | RAG that follows knowledge-graph relationships, not just nearest-text matches | 8 |
| **Grounding (spatial)** | Connecting words to locations — "where exactly is it?" as coordinates | 4 |
| **Hallucination** | A model confidently producing something untrue — in vision, including points on things that aren't there | 3, 10 |
| **Held-out set** | Evaluation data the prompts and models were never tuned on | 10 |
| **Installed Base & Maintenance Knowledge** | The planned M-Files module modelling equipment by serial number with procedures, bulletins, parts, suppliers and warranty [10] | 7 |
| **Interactions API** | Google's newer unified API for Gemini; stores requests by default unless `store=false` | 10 |
| **Knowledge graph** | Things (nodes) and named relationships between them (edges), queryable and explainable | 7 |
| **Latent state** | A model's compact internal summary of "what's going on" | 5 |
| **MCP (Model Context Protocol)** | An open standard for exposing tools, resources and prompts to any AI application | 9 |
| **MCP client / server** | The AI application that uses tools / the system that exposes them | 9 |
| **Model-based vs. model-free** | Learning how the world works then planning, vs. learning actions directly by trial and error | 5 |
| **Normalised coordinates** | Positions expressed as fractions of the image (0–1000), independent of image size | 4 |
| **OCR** | Optical character recognition — reading the characters on a page | 3 |
| **P&ID** | Piping and instrumentation diagram — the standard drawing of a process plant's pipes, valves and instruments | 3, 4 |
| **PAAS (Physical Agents as a Service)** | The long-term idea: any embodiment asks M-Files "what is this and what's allowed?" | 11 |
| **Perception vs. resolution** | Turning pixels into "a pump" vs. turning "a pump" into *this specific pump* in the graph | 7 |
| **Physical agent** | A system whose decisions work through sensors, bodies or tools in a real, changing environment | 2 |
| **Point** | A single `[y, x]` location on a 0–1000 grid with a label | 4 |
| **RAG** | Retrieval-augmented generation — retrieve your own content, then have a model answer from it | 8 |
| **ReAct** | The reason → act → observe loop behind most agents | 9 |
| **Reinforcement learning (RL)** | Learning actions from reward by trial and error | 6 |
| **Set-of-Mark (SoM)** | Overlay numbered marks on candidate regions of an image so the model answers by choosing a mark; Magma's grounding method [21] | 4 |
| **Sim-to-real** | Transferring a policy learned in simulation onto real hardware | 6 |
| **Tool** | A function or system action an agent is allowed to request | 9 |
| **Trace-of-Mark (ToM)** | Tracking marks across video frames so a model learns to predict where things will move next; Magma's planning method [21] | 4 |
| **Transformer** | The attention-based architecture behind modern language and vision models | 3 |
| **VLA** | Vision-language-action model — camera + instruction in, robot actions out | 6 |
| **VLM** | Vision-language model — sees images and talks about them | 3 |
| **ViT (Vision Transformer)** | A transformer that treats image patches like words | 3 |
| **World model** | A model that predicts how the world's state changes given an action | 5 |
