# CLAUDE.md

Claude 계열 에이전트의 진입 포인터다. 규칙·금지선의 정본은 [AGENTS.md](AGENTS.md)이며 이 파일은 사실을 복제하지 않는다. 두 파일이 상충하면 `AGENTS.md`가 맞고 이 파일을 고친다. 확정 task: T-001 · 마지막 갱신: 2026-09-06.

## 진입 순서

1. [AGENTS.md](AGENTS.md) — 목표·경계·작업 원칙·읽기 정책·절대 금지·완료 조건
2. [docs/README.md](docs/README.md) — 문서 지도와 정본 관계
3. [docs/resume.md](docs/resume.md) — 현재 상태·다음 한 작업·차단 조건
4. 지정된 `docs/tasks/T-NNN-*.md` 한 파일(task를 고를 때만 [docs/tasks.md](docs/tasks.md))

작업 종류별 시작점은 [SKILL.md](SKILL.md)의 표에서 고른다. `docs/` 전체·모든 ADR·`docs/survey/` 전체를 한꺼번에 읽지 않는다.

## 정본 링크

| 질문 | 정본 |
|---|---|
| 배포 단위·의존 방향·소비자 | [architecture](docs/architecture/README.md) |
| 공통 규칙(토큰·UX·반응형·UI 계약·OpenAPI·CI·라이선스·버전·스택) | [standards](docs/standards/README.md) |
| 확정 결정과 근거 | [ADR 색인](docs/adr/README.md), [설계 브리프](docs/plan/design-brief.md) |
| 개발 환경·검증 명령 사다리 | [dev-environment](docs/dev-environment.md) |
| branch·worktree·2인 리뷰·PR·정리 | [agent workflow](docs/runbooks/agent-workflow.md) |
| 소비자 이관·릴리스 | [consumer adoption](docs/runbooks/consumer-adoption.md), [release](docs/runbooks/release.md) |
| task 규칙·문서 유지 | [tasks rule](docs/tasks-rule.md), [documentation maintenance](docs/runbooks/documentation-maintenance.md) |

## 절대 금지

공통 5(main 직접 push · 비밀·`.env`·`*.local.md` 커밋 · `git add -A`/`git add .` · 미실행 gate를 통과로 표시 · 한 사실 두 곳 선언)와 라이브러리 특화 5는 [AGENTS.md §6](AGENTS.md#6-절대-하지-말-것)이 정본이다. 여기에 다시 적지 않는다.

## 종료

검증·2인 리뷰·기록 갱신·보안 점검·PR·worktree 정리는 [AGENTS.md §8](AGENTS.md#8-완료와-push)과 [agent workflow](docs/runbooks/agent-workflow.md)를 따른다.
