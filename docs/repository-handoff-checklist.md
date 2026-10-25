# Repository separation and review checklist

Updated: 2026-09-11. Checkmarks mean the stated outcome was verified; they do
not imply live-service validation or production readiness.

## Verified foundations

- [x] Private [complex-document-grounding-poc](https://github.com/M-Files-AI/complex-document-grounding-poc)
  created for document-service comparisons, separate from physical-agent research.
- [x] Document repository Python scaffold and Copilot/Claude guidance committed
  and pushed (`b354492`); no DI implementation claimed by that bootstrap.
- [x] Physical-research guidance and corrected proposal merged in
  [PR #8](https://github.com/M-Files-AI/physical-agents-research/pull/8).
- [x] Follow-up work isolated in a fresh topic-branch worktree, leaving the
  existing demo worktree's pending changes untouched.

## This follow-up

- [x] Canonical guidance requires topic branches, PR review, and user-controlled merge.
- [x] PR template requests verification, evidence, limitations, and progress updates.
- [x] Claude role wrappers reference the same detailed role definitions as Copilot.
- [ ] User reviews and merges this follow-up PR.
- [ ] End-to-end role/skill discovery exercised in both Copilot and Claude Code.

## Document experiment handoff (tracked there)

Use the [document evaluation plan](https://github.com/M-Files-AI/complex-document-grounding-poc/blob/main/docs/evaluation-plan.md)
for implementation and validation status. Pending PRs may carry newer checklist
updates than `main`.

The document repository owns DI (Azure Document Intelligence), CU (Azure Content
Understanding), Gemini comparisons, and local metadata setup discovery. Its
first implementation PR covers DI extraction and offline verification; live
service validation, LLM reasoning, and downstream metadata consumption are
distinct milestones, not implied by a working parser.

Do not move customer files or publish raw results as part of this handoff.
Extract a shared module only after both repositories demonstrate a concrete
need; no cross-repository runtime dependency is currently required.
