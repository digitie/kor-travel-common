# 2026-09-07 T005c post-fix workflow 정적 보고 공통 review manifest

- Review ID: T005C-20260907-03f2cae
- Candidate: `03f2cae9a817da96a0eb28ae6487c721464d202f`
- Base/parent: `3ef3fc4f91ba2b6320ba6197176f54917227c31e`
- Branch: `codex/t005c-workflow-static-report`
- Task: `docs/tasks/T-005c-workflow-static-report.md`
- Scope: `tools/check_versions.py`, `tests/test_check_versions.py`, `docs/standards/versions.md`, plus prior candidate context from `5526c018380023afd362bd3993d110ee81c3b10a`
- Goal: T005c workflow static report with constrained YAML fail-close, output redaction, lexical root/symlink containment, non-empty target enforcement, canonical setup-node matching, and remote/Docker target validation.
- Required post-fix semantics: all initial findings A-P1-01/B-P1-01, A-P1-02, A-P2-03/B-P1-03, A-P2-04, A-P2-05, A-P2-06, B-P1-02, B-P2-04 are fixed or an evidence-backed new disposition is recorded. Sensitive/unsupported workflow values and paths must not appear in stdout, JSON, Markdown, annotations, or GITHUB_STEP_SUMMARY. Malformed/unsupported YAML and empty target workflows must exit 2; valid constrained YAML remains accepted; symlink escape is rejected before read; setup-node leading-space refs still produce the Node finding; malformed Docker/remote refs cannot be OK.
- Out of scope: full YAML parser, remote action/version lookup, workflow execution, Docker image inspection, consumer repository edits, package build/install/publish, `versions.json.actions.checked` activation.
- Acceptance: existing tests pass with no skips; Windows/Linux parity; every initial reproduction is rerun; post-fix full validators and exact PR CI are recorded; no candidate edits by reviewers.
- Review request A: independently attack parser boundaries, YAML quote/escape/flow/list indentation, empty structures, setup-node semantics, output redaction regression, and consumer-facing line/source behavior.
- Review request B: independently attack symlink/root containment, Docker/remote target validation, output channels/redaction, manifest integration, docs/registry consistency, CI evidence, and Windows/Linux parity.
- Rule: use detached clean worktree at exact candidate; do not edit candidate; do not read the other review or prior raw post-fix result; record exact SHA and clean status at start/end. Save raw report with execution ID, timestamps, commands, findings P0-P3, all NOT_RUN gates, and verdict.
