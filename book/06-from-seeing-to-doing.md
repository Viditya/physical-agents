# Chapter 6 — From seeing to doing: how robots learn to act

## Learning to cook by watching

How did you learn to crack an egg? Probably not from a textbook. Someone showed you — maybe a few times — and then you tried, made a mess, and tried again.

Robots learn in the same two ways:

1. **Watching** — copying demonstrations (imitation learning).
2. **Trying** — trial and error with a reward (reinforcement learning).

Modern robot "brains" combine both, plus a third ingredient that changed everything: **pre-training on the internet**, so the robot already knows what an egg *is* before it ever sees one.

---

## The key term: VLA

To formalise: **a vision-language-action model (VLA) takes camera images and a plain-language instruction, and outputs robot actions.**

```mermaid
flowchart LR
    CAM["Camera image"] --> VLA{"VLA model"}
    INS["'Put the blue block<br/>in the orange bowl'"] --> VLA
    ST["Robot's own state<br/>(joint angles)"] --> VLA
    VLA --> ACT["Actions<br/>move arm → open gripper<br/>→ lower → close"]
```

It's a VLM (Chapter 3) with an extra output: instead of only answering in words, it answers in motor commands.

The family tree:

| Year | Model | What was new |
|---|---|---|
| 2022 | **RT-1** (Google) | One transformer trained on lots of real robot demos, many tasks |
| 2023 | **RT-2** (Google) | Started from a web-trained VLM — the robot inherits internet knowledge |
| 2023–24 | **Open X-Embodiment** | 20+ labs pooled robot data across many robot types |
| 2024 | **OpenVLA**, **Octo** | Open-source VLAs anyone can fine-tune |
| 2025–26 | **Gemini Robotics 2**, **π-series**, others | General-purpose policies, whole-body control, multi-robot coordination |

---

## Two tricks that made VLAs work

### Trick 1 — Action chunks

Instead of predicting one tiny motor command at a time (jerky, slow), models predict a short *chunk* of future actions at once — say, the next half-second of movement. Smoother, faster, and fewer chances to wobble.

### Trick 2 — Diffusion policies

Often there are several good ways to do a task — grab the cup from the left or the right. A normal model averages them and grabs the air in the middle. **Diffusion policies** (borrowing the technique from image generators) produce a *distribution* of possible action sequences and pick one coherent option.

```mermaid
flowchart LR
    subgraph N["Averaging model"]
        N1["Left grip"] --> NA["average →<br/>grabs air ✗"]
        N2["Right grip"] --> NA
    end
    subgraph D["Diffusion policy"]
        D1["Left grip"] --> DP["pick one<br/>coherent option ✓"]
        D2["Right grip"] --> DP
    end
```

---

## The data problem: the data pyramid

Language models were trained on the whole internet. Robots don't have an internet of robot data. This is the central bottleneck of the field.

Two independent sources describe the same shape. Jim Fan (NVIDIA) calls it a data ladder [1]; McKinsey calls it a data pyramid [5]:

```mermaid
flowchart TB
    T["Real-world deployment & teleoperation data<br/>SCARCE · EXPENSIVE · MOST VALUABLE"]
    M["Simulation & synthetic data<br/>mid-cost · scalable · 'sim-to-real' gap"]
    B["Video — web & wearable cameras<br/>CHEAP · ABUNDANT · no action labels"]
    B --> M --> T
    style T fill:#0072CE,color:#fff
    style M fill:#1C243A,color:#fff
    style B fill:#55B4BC,color:#fff
```

- **Bottom:** human video is everywhere and nearly free, but it shows no robot actions.
- **Middle:** simulation can generate unlimited data, but simulated physics never perfectly matches reality.
- **Top:** real robot data is gold, and painfully slow to collect.

McKinsey adds a reliability ladder that describes how any physical-AI system matures [5]:

```mermaid
flowchart TB
    R1["1. Capability<br/>demo"] --> R2["2. Reliable in a<br/>controlled setting"] --> R3["3. Dependable in<br/>production"] --> R4["4. Scalable<br/>unit economics"]
```

Most pilots die between steps 2 and 4. Keep this ladder in mind — it applies to our work too (Chapter 11).

---

## Where reinforcement learning fits (briefly)

Reinforcement learning (RL) is learning from reward: try something, get a score, adjust. It produced famous results in games and simulated robots (DQN, PPO, SAC). In real-world robotics it's usually used to *fine-tune* a policy that was first learned by imitation, because pure trial-and-error on real hardware is slow and can break things.

You don't need to master RL for VMAN Vision. You need to recognise the words and know that "the robot learned it with RL" usually means "in simulation, then carefully transferred" — which is exactly where the sim-to-real gap bites.

---

## What this means for the industry — and for us

The robotics race is being run on these layers:

```mermaid
flowchart TB
    H["Hardware — arms, humanoids, grippers<br/>Boston Dynamics, Figure, Tesla, FANUC, KUKA…"]
    P["Robot policies — VLAs, world models<br/>Google, NVIDIA, Physical Intelligence, Skild AI…"]
    S["Simulation & digital twins<br/>NVIDIA Isaac/Omniverse, Siemens, PTC…"]
    E["Enterprise context — what is this asset,<br/>what's approved, what happened before"]
    H --- P --- S --- E
    style E fill:#0072CE,color:#fff
```

Every layer above the last one is crowded and extremely well-funded. The last layer — enterprise context — is where a robot or a technician finds out *what this specific machine is and what the approved procedure is*. That's the layer this book keeps returning to.

---

> ### Where M-Files stands
> **Deliberately out of scope — correctly.** M-Files has no robot training data, no robotics team, and no reason to acquire either. The Manufacturing Blueprint's own words set the boundary: M-Files "records outcomes and recommends actions; it does not execute transactions" [10]. Understanding VLAs matters for two reasons only: to speak credibly with robotics partners, and to recognise that every VLA-driven robot in a factory still needs someone to tell it which machine is which and what the approved procedure is.
