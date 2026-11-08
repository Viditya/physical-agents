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

## 2026-11-08 prototype validation follow-up

- [x] Work isolated in `physical-agents-demo-validation` on
  `fix/demo-validation-and-env`, based on remote `main` (`8557e18`). The existing
  `feature/figure-5-1-and-env-setup` worktree was left on its original branch.
- [x] Baseline: 55 offline tests passed in the existing Python environment.
- [x] Reproduced overlay failures from non-finite coordinates and oversized
  integers, and negative PDF indices selecting the last page unintentionally.
- [x] Overlay now skips invalid values while retaining valid points; extreme
  finite coordinates are clamped before pixel conversion. Negative PDF indices
  receive a clear zero-based-index error.
- [x] Added the missing `.env.example`, local-artifact ignores and explicit
  Windows setup instructions. Included `requests` and `beautifulsoup4`, which
  the sales module imports during full-suite collection.
- [x] Fresh Python 3.12 environment installed only from
  `prototype/requirements.txt`; `pip check` found no broken requirements.
- [x] Fresh-environment offline suite: **66 passed**. Added cases exercise the
  rendering boundary and HTTP response with synthetic invalid provider points.
- [x] Real local process smoke: `/` and `/api/config` returned HTTP 200; public
  samples were available. The owned smoke-test process was stopped afterward.
- [ ] Live provider/camera experiment: not performed. No Gemini/Azure model
  request or Claude execution is established by these offline checks.
- [ ] Restore/locate the role and experiment-skill entry points referenced by
  `AGENTS.md` before a new physical-agent experiment. Neither `.github/agents/`
  nor the referenced `.github/skills/`/`.claude/skills/` entry points is present
  in this checkout.
- [ ] User reviews and merges this follow-up. No automatic merge.
- [ ] Publish topic branch and open PR after GitHub write access is restored.
  On 2026-11-08 both local HTTPS push and the connected GitHub integration's
  branch-create request returned HTTP 403. Implementation is committed locally;
  no remote topic branch or PR was created by this pass.
