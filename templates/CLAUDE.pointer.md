# CLAUDE.md — 진입 포인터

<!-- kor-travel-common templates/CLAUDE.pointer.md 판 2026-09. 40줄 이하 유지. 규칙·사실을 이 파일에 복제하지 않는다. -->

이 파일은 Claude 계열 에이전트의 진입 포인터다. 정책·금지선의 정본은 `AGENTS.md`이며, 이 파일이 `AGENTS.md`와 상충하면 이 파일을 고친다.

## 시작 순서

1. `AGENTS.md` — 공통 절 A~I와 로컬 절
2. `docs/README.md` — 문서 지도와 정본 위치
3. `docs/resume.md` — 현재 상태·다음 한 작업·차단 조건
4. 지정된 상세 task 한 파일(`docs/tasks/T-NNN-*.md`); task를 고를 때만 `docs/tasks.md`

## 정본 위치

| 질문 | 문서 |
|---|---|
| 작업 종류별로 무엇을 먼저 여는가 | `SKILL.md` |
| 현재 설계·의존 방향 | `docs/architecture/README.md` |
| 왜 그렇게 결정했는가 | `docs/adr/README.md` |
| branch·검증·2인 리뷰·PR | `docs/runbooks/agent-workflow.md` |
| 개발 환경·worktree 프로필 | `docs/dev-environment.md` |
| 문서·task·journal 갱신 규칙 | `docs/runbooks/documentation-maintenance.md` |
| 저장소 간 공통 규칙(토큰·UX·OpenAPI·버전·에이전트 규약) | kor-travel-common `docs/standards/README.md` |
| 리뷰 기록 | `docs/reviews/README.md` |

## 종료 경로

검증, 2인 독립 적대적 리뷰, 기록 갱신, push 전 보안 감사, PR 본문은 `AGENTS.md` G·H 절과 `docs/runbooks/agent-workflow.md`를 따른다. `git add -A`·`git add .`·`main` 직접 push는 사용하지 않는다.
