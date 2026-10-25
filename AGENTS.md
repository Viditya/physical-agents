# Repository guidance

## Purpose and boundaries

This repository researches physical-agent capabilities, including visual and
spatial reasoning for engineering drawings. Keep the DI, CU, Gemini
complex-document comparison and metadata-agent integration work in
`complex-document-grounding-poc`.

Reusable, provider-neutral code may be extracted only after it is proved useful
in both repositories. Do not import this repository wholesale into a
document-experiment pipeline.

## Data and credentials

- Do not commit credentials, `.env`, customer documents, raw provider output,
  screenshots, or generated overlays unless explicitly approved.
- Preserve the current repository's existing result conventions and do not
  overwrite results created by another contributor.

## Engineering conventions

- Keep provider implementations isolated under `prototype/providers/`.
- Preserve normalized coordinate definitions and render visual output when
  making spatial-grounding claims.
- Treat model output as experimental evidence; report failure modes and avoid
  invented confidence values.
- Add focused tests when changing parsing, coordinate conversion, rendering,
  or provider response normalisation.

## Agent workflow

### Branches, review, and progress

- Start new work on a topic branch based on current remote `main`. Use a separate
  worktree when another agent or contributor has pending changes.
- Commit and push only the topic branch; never push implementation directly to
  `main`. Use an explicit destination ref when upstream configuration is unclear.
- Open or update a pull request with scope, verification commands/results, and
  limitations. Do not merge automatically; the user reviews and merges.
- **Exception — scheduled analysis routines:** the recurring cloud routines
  (nightly `RESEARCH_LOG.md` research check-in, weekly research-synthesis note,
  weekly manufacturing win strategist) push their append-only/update-in-place
  output files directly to `main`, no PR. This is intentional: they only
  produce dated log entries or update-in-place profile pages (`RESEARCH_LOG.md`,
  `pitch/README.md`'s "Pitch-relevant updates" section, `sales/**/README.md`
  logs, `sales/**/<company>.md` profiles) — never code, tests, providers, or
  `AGENTS.md`/agent-role files themselves. Any change to actual code
  (`prototype/`, `tests/`, `sales/research_agent.py`, CI/agent config, etc.)
  still requires a topic branch and a PR under the rule above, even from a
  routine. If a routine's prompt is ever changed to touch code, add PR review
  to that routine's instructions at the same time — don't let the exception
  silently expand.
- Keep [the handoff checklist](docs/repository-handoff-checklist.md) current.
  Check an item only after verifying its outcome; distinguish implemented,
  offline-tested, live-tested, and merged states.
- Document research owned by the document repository in its own plan rather
  than duplicating an implementation checklist here.

Use repository-local agents proportionately:

- `research-producer` for scope and evidence boundaries.
- `physical-agent-developer` for a bounded implementation and self-review.
- `experiment-qa` for independent validation of an experiment or demo claim.

Detailed role instructions live in `.github/agents/*.agent.md`; Claude Code
wrappers must read the corresponding file so both tools use the same role
boundaries. Repository rules in this file apply to every role.

Load the `physical-agent-experiment` skill before a new physical-agent
experiment. Copilot's entry point is `.github/skills/physical-agent-experiment/`;
Claude Code's compatible entry point is `.claude/skills/physical-agent-experiment/`.
