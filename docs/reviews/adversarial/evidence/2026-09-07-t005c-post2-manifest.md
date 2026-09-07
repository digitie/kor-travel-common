# 2026-09-07 T005c post-fix 02 workflow 정적 보고 공통 review manifest

- Review ID: T005C-20260907-AE6D257
- Candidate: `ae6d25711ac04a03db7b8182bd7ffae4a1b2d852`
- Branch: `codex/t005c-workflow-static-report`
- Parent: `8a662a4a981f20d62c8ab98d9311a610bdb30b5c`
- Task: `docs/tasks/T-005c-workflow-static-report.md`
- Scope: `tools/check_versions.py`, `tests/test_check_versions.py`, `docs/standards/versions.md`, `docs/tasks/T-005c-workflow-static-report.md`, and prior T005c evidence context.
- Goal: close post-fix 01 findings for workflow output redaction, per-job/per-step structure validation, constrained YAML indicator/quote/Unicode boundaries, local symlink exit contract, and Docker image-name validation.
- Required semantics: policy-shaped password assignment/private address/root-derived repo values never appear in stdout, JSON, Markdown, annotations, or GITHUB_STEP_SUMMARY; every malformed sibling job/step/with map is input error even beside valid uses; documented 2-space block/trailing-free flow subset is enforced; plain internal quotes remain valid and leading indicators fail; invalid Unicode scalar escapes exit 2 without traceback; workflow and local path escapes exit 2; Docker uppercase/repository trailing separator/middle port are not OK while valid registry port remains OK.
- Out of scope: full YAML parser, remote action/version lookup, workflow execution, Docker image inspection, consumer repository edits, package build/install/publish, `versions.json.actions.checked` activation.
- Acceptance: Windows/Linux parity; all existing tests no skips; post-fix 01 direct reproductions rerun; full validators and exact PR CI recorded; reviewers use detached clean worktrees and do not edit candidate or read each other’s raw report.
- Review request A: parser quote-start context, plain indicators, Unicode scalar boundary, per-step/job empty structure, valid constrained YAML and source lines, all redaction channels.
- Review request B: redaction policy parity and repo derivation, local/workflow symlink modes and manifest, Docker reference grammar, docs/registry/CI consistency, Windows/Linux parity.
- Rule: exact candidate SHA only; record start/end HEAD/tree/clean, commands, P0-P3 findings, NOT_RUN, verdict, and raw report hash at `.git/codex-audit/2026-09-07-t005c-post2-reviewer-{a,b}.md`.
