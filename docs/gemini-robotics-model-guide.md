# Gemini Robotics model guide

**Sources checked:** 2026-09-18
**Purpose:** Explain the current Google model offerings relevant to this
repository, their documented capabilities, availability boundaries, and the
experiments needed before adopting a feature.

This is a guide to vendor-documented capabilities, not a claim that this
repository has demonstrated every capability.

## The model families are not interchangeable

| Offering | What Google describes | API availability established by the sources | Relevance here |
|---|---|---|---|
| Gemini Robotics 2 | A physical-world model combining spatial reasoning, long-horizon planning, and multi-robot collaboration. | The DeepMind model page describes the capability but does not provide a public Gemini API model ID or endpoint in the material checked. Do not assume it can be called from this prototype. | Future robot embodiment/control research; not the current image-pointing demo. |
| Gemini Robotics ER 2 | A multimodal embodied-reasoning vision-language model. | Available through the Gemini API as the preview endpoints listed below. | Directly relevant to the current VMAN Vision point-and-label demonstration. |
| General Gemini vision models | General multimodal models with image/PDF/video capabilities. | Available through their own documented Gemini API model IDs. | Useful comparison candidates, but not a substitute for an ER 2 result until evaluated on the same task. |

## Gemini Robotics ER 2 endpoints

| Endpoint | Documented purpose | Use in this repository |
|---|---|---|
| `gemini-robotics-er-2-preview` | Standard ER 2 model, built on Gemini 3.5 Flash with spatial reasoning, video moment finding, video-progress classification, multi-robot orchestration, and multi-step tool use. | This is the model used by the saved Gemini drawing runs. |
| `gemini-robotics-er-2-streaming-preview` | Low-latency, bidirectional streaming through the Live API for continuous audio/video and function calling. | Out of scope for the static-document demo; candidate only for a separate, approved video experiment. |

The ER 1.6 endpoint is documented as superseded by ER 2. No conclusion is made
here about earlier ER versions beyond that vendor migration guidance.

## What ER 2 is documented to do

| Capability | Vendor-documented behavior | Evidence in this repository | Next disciplined experiment |
|---|---|---|---|
| Pointing | Return object labels and normalized `[y, x]` coordinates on a 0-1000 grid. | Demonstrated on six saved engineering-drawing runs; overlays are present. | Score points against labelled expected regions. |
| Bounding boxes | Detect objects with boxes. | Not implemented or tested here. | Run a point-versus-box comparison in `physical-agents-perception-experiments`. |
| Spatial relationships and trajectories | Reason about object positions and plan trajectories. | Not tested. | Keep out of the document demo; evaluate only with a safe physical-agent task. |
| Video understanding | Track objects, find moments, and classify task progress. | Not tested. | Use only with an approved video corpus and privacy plan in the perception repository. |
| Agentic vision / code execution | Write/execute Python to manipulate images; examples include zoom/crop object detection, gauge reading, circuit-board text reading, and image annotation. | Not tested. | Test crop-and-reinspect against a fixed small-detail task and compare with one-shot inference. |
| Task/multi-robot orchestration | Use custom robot APIs and tools for long-horizon tasks; streaming endpoint supports low-latency function calling. | Not tested. | Out of scope for the static perception demo. |

## Practical model/API guidance

The Google cookbook's old `gemini-robotics-er.ipynb` now redirects to the
[Gemini robotics samples repository](https://github.com/google-gemini/robotics-samples/blob/main/Getting%20Started/gemini_robotics_er.ipynb).
Use that repository as the primary ER 2 code reference.

Google's current API documentation describes the
[Interactions API](https://ai.google.dev/gemini-api/docs/interactions-overview)
as generally available and recommended for new Gemini applications. It supports
multimodal inputs, structured outputs, tool orchestration, observable execution
steps, optional server-side state, and `store=false` for stateless requests.
The older `generateContent` API remains supported.

This repository currently uses `generate_content`. Do not replace it only
because a cookbook changed APIs: first compare the two interfaces on identical
approved inputs, prompt, model endpoint, and output parsing, and preserve raw
results/overlays.

## Operational and data-handling limitations

- ER 2 is a preview endpoint; output format and behavior can change.
- Google documents that spatial outputs can be wrong or hallucinated, especially
  for ambiguous or out-of-distribution inputs.
- Crop/zoom, high-resolution images, complex prompts, and higher thinking
  levels can increase latency and cost. Google recommends low thinking levels
  for basic spatial tasks and higher levels for complex counting/estimation.
- The API documentation says unrestricted API keys are rejected. Secure keys
  through AI Studio restrictions; never store one in Git.
- The Interactions API stores requests by default. Use `store=false` if the
  applicable data-handling policy requires stateless requests; this disables
  server-side continuity/background features. The vendor documentation states
  default retention differs by tier, so verify current organisational terms
  before using restricted inputs.
- Video/audio may involve personal data. Google requires notification/consent
  and minimisation practices for identifiable people in such input. Do not use
  people-containing media in an experiment without an approved privacy plan.

## How this fits the repository split

- Keep the current Gemini ER 2 engineering-drawing point demo and its selected
  internal results in `physical-agents-research`.
- Run public/permissively reusable box, crop/re-inspect, image-search, and
  video experiments in `physical-agents-perception-experiments`.
- Run direct PDF processing, Document Intelligence, Content Understanding, and
  metadata-agent integration experiments in `complex-document-grounding-poc`.

Promote a finding from an experiment repository back into this repository only
when it has reviewable evidence and changes the core physical-agent research
story.

## Sources

- Google DeepMind: [Gemini Robotics](https://deepmind.google/models/gemini-robotics/)
- Google Gemini API: [Gemini Robotics overview](https://ai.google.dev/gemini-api/docs/robotics-overview)
- Google Gemini API: [Gemini Robotics ER 2 model](https://ai.google.dev/gemini-api/docs/models/gemini-robotics-er-2-preview)
- Google Gemini API: [Spatial reasoning](https://ai.google.dev/gemini-api/docs/robotics-spatial)
- Google Gemini API: [Agentic vision](https://ai.google.dev/gemini-api/docs/robotics-agentic)
- Google Gemini API: [Interactions API overview](https://ai.google.dev/gemini-api/docs/interactions-overview)
- Google Gemini Cookbook: [Spatial understanding](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Spatial_understanding.ipynb)
- Google Gemini Cookbook: [PDF files](https://github.com/google-gemini/cookbook/blob/main/quickstarts/PDF_Files.ipynb)
