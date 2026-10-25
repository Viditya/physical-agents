# Gemini Robotics-ER hardware demo survey

**Surveyed:** 2026-09-30
**Purpose:** Find what people have actually built with Gemini Robotics-ER on
physical (or simulated) hardware, how long they have been building, and what
that implies for scoping a VMAN Vision hackathon demo.

This is a reading list built from YouTube search results and video
descriptions. None of the videos below have been watched or transcribed yet;
observations come from titles, channels, dates, and descriptions only. Tick
the **Read** column as each one is reviewed, and add findings under
[Review notes](#review-notes).

## Adoption timeline

| Model | Released | Community builds found on YouTube |
|---|---|---|
| Gemini Robotics-ER 1.5 | ~Sep–Oct 2025 | Most hobbyist/developer builds (~12 months of community activity) |
| Gemini Robotics-ER 1.6 | ~Apr 2026 | Boston Dynamics Spot inspections (AIVI-Learning) |
| Gemini Robotics-ER 2 | 2026-07-30 | Google's own videos and explainers only — no community hardware builds found yet |

A working ER 2 hardware demo would therefore be early relative to the
public community.

## Reading list

| Read | # | Video | Channel / date / length | Why it matters |
|---|---|---|---|---|
| [ ] | 1 | [Smarter Inspections Powered by Google Gemini Robotics](https://www.youtube.com/watch?v=kBwxmlI2yHQ) | Boston Dynamics · 2026-04-14 · 1:40 | Closest to manufacturing: Spot facility visual inspections using Gemini Robotics (ER 1.6). [Announcement](https://bostondynamics.com/blog/aivi-learning-now-powered-google-gemini-robotics/). |
| [ ] | 2 | [Power the future of robotics with Gemini](https://www.youtube.com/watch?v=kCXQce1dtNE) | Google for Developers (I/O 2026) · 2026-05-21 · 18:05 | Official developer talk: spatial awareness, Live API, MuJoCo simulation, safety — the recommended stack end to end. |
| [ ] | 3 | [Give your robot a Voice with Gemini Live](https://www.youtube.com/watch?v=jkdvMEvG8T8) | Google for Developers · 2026-04-13 · 12:38 | Live API on Reachy Mini (open-source, Hugging Face / Pollen): voice, vision, and function calls driving actuators. Most copyable hackathon setup. |
| [ ] | 4 | [Gemini Robotics ER 1.5 × NVIDIA Isaac Lab × Enactic OpenArm](https://www.youtube.com/watch?v=o8ESyjf4VAg) | Kimate Richards · 2025-12-14 · 26:58 | Full stack: ER reasons and plans, Isaac Lab simulation validates, a real 7-DoF arm executes. |
| [ ] | 5 | [Introducing Gemini Robotics 2](https://www.youtube.com/watch?v=-rYFDefcq3k) | Google for Developers · ~2026-08 · 39:14 | DeepMind researchers on embodied reasoning, whole-body control, and dexterity — realistic ER 2 capability boundaries. |
| [ ] | 6 | [I Gave My Robot AI Vision (GPT vs Gemini vs Grok)](https://www.youtube.com/watch?v=ZYJ5TQJbUMo) | Nikodem Bartnik · 2025-11-28 · 22:58 | Hobbyist Raspberry Pi robot comparing vision models; shows hardware effort and failure modes. |
| [ ] | 7 | [Gemini Robotics-ER 1.5: Build Physical AI Apps & Agents in Python](https://www.youtube.com/watch?v=B7565KdDczI) | Stream Developers · 2025-10-03 · 11:30 | Software-only point-and-label app with a Streamlit UI; close to this repository's current prototype. |
| [ ] | 8 | [Animating an AI-Controlled Robot Arm with Gemini Robotics, SVG, and GSAP](https://www.youtube.com/watch?v=skgsBdRTLSU) | Ashot Abrahamyan · 2025-12-29 · 15:25 | Zero-hardware option: ER 1.5 drives an animated browser arm. [Code](https://github.com/Ashot72/AI-Controlled-Robot-Arm). Captions are auto-generated Armenian only. |
| [ ] | 9 | [Robot Arm + Gemini AI — Gemini API Competition](https://www.youtube.com/watch?v=R9uF_zbBAPQ) | Gabe Catalfo · 2024-08-12 · 4:33 | Competition entry with a low-cost desk arm; calibrates hackathon-level scope (pre-ER, general Gemini). |
| [ ] | 10 | [ASRS Simulation Guided by Gemini Robotics](https://www.youtube.com/watch?v=vk7D4aHpunU) | Jason Kung · 2026-03-08 · 1:07 | Entry from a Google DeepMind Gemini hackathon: warehouse storage/retrieval, simulation only. No captions. |

Also surfaced but lower priority: [New Gemini Robotics-ER 1.5 for Object
Detection](https://www.youtube.com/watch?v=Rveer-93ql0) (Nicolai Nielsen),
[AI Meets Robotics: Control Robots with Gemini for AI
Hackathons](https://www.youtube.com/watch?v=MKvOHcpj8Uc) (lablab.ai, 1:23
promo), and Google DeepMind's official Gemini Robotics 2 clips
([whole-body](https://www.youtube.com/watch?v=4lSQnrMC6nY),
[multi-robot](https://www.youtube.com/watch?v=CiTPDm7PKW0),
[dexterity](https://www.youtube.com/watch?v=O9-650iHAls)).

## Other lead checked: Trocatics

[trocatics.in](https://www.trocatics.in/) is a four-founder student hardware
startup (Atria IT, Bengaluru). The site shows one 33-second test clip of a
self-balancing chassis and two planned platforms (heavy-duty chassis,
humanoid); all specifications are marked classified. No evidence of Gemini or
any vision model — a balancing/kinematics demo, not a physical-agent demo. At
most a possible local hardware partner, unverified.

## Initial scoping read (to be confirmed after review)

Demos in the list fall into three tiers:

1. **Simulation only** (browser, MuJoCo, Isaac Lab) — no purchase; #8, #10.
2. **Small open-source robot** (Reachy Mini, SO-101 arm, Raspberry Pi robot) —
   Google's own chosen path in #3.
3. **Industrial robot** (Spot) — strongest story (#1), unrealistic for a
   hackathon budget.

Candidate VMAN Vision angle combining #1 and #3: a small robot or camera rig
points at a machine; ER 2 locates the part and reads its gauge; VMAN resolves
it to the asset record and surfaces its manual and maintenance history. Not
yet validated; hardware list pending video review.

## Review notes

_Add per-video findings here as each is reviewed (hardware used, cost signals,
latency, failure modes, reusable code)._

## Sources

- Google: [Introducing Gemini Robotics ER 2](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/)
- Google Gemini API: [Gemini Robotics overview](https://ai.google.dev/gemini-api/docs/robotics-overview)
- Boston Dynamics: [AIVI-Learning now powered by Google Gemini Robotics](https://bostondynamics.com/blog/aivi-learning-now-powered-google-gemini-robotics/)
- The Gadgeteer: [Google's Gemini Robotics ER 2 Wants to Run the Whole Robot Crew](https://the-gadgeteer.com/2026/08/01/google-gemini-robotics-er-2/)
