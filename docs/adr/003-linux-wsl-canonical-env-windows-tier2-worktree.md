# ADR-003: 개발 환경 정본(Linux/WSL)·Windows Tier 2·임시 worktree

- 상태: partially superseded by ADR-016 — UX의 MDX 검사 실행 의존만 변경
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-03·O-17, `docs/survey/cross/docs-conventions.md` §1.11·§1.12·§2 C1·C2·C12, `docs/survey/cross/canview-structure-checklist.md` Q4·Q6·R6.10, `docs/survey/commonality-matrix.md` §1.5(개발 환경 정본 행), canview `docs/adr/003-windows-development-and-ephemeral-worktrees.md`(`1f93b8a`)

## 컨텍스트

canview ADR-003은 Windows PowerShell을 정본 환경으로 삼고 임시 worktree 프로필을 쓴다. 반면 소비자 7개 중 6개는 Linux/WSL을 정본으로 선언했고(ktc ADR-23/33, ktdm, geo ADR-065, map, pinvi ADR-051; airport는 WSL2 1차), 고정 worktree(geo·map·pinvi·ktdm)와 암묵 worktree(ktc)가 섞여 있다(`dc` §1.11·§1.12). common의 도구는 Python stdlib이라 OS 의존이 작지만, 현재 사용자 환경은 Windows이고 `.py` 사본이 CRLF로 만들어지는 문제가 관찰됐다(cv §1.2·Q6). 패키지 빌드·소비자 스모크는 CI(ubuntu)에서 검증된다.

## 결정

1. common 정본 환경은 Linux/WSL bash이며 CI는 `ubuntu-24.04`다. 저장소 경로 표기는 `/mnt/f/dev/kor-travel-common`(WSL)이고 Windows 체크아웃 `F:/dev/kor-travel-common`은 같은 트리의 보조 표기다.
2. Windows는 Tier 2다: `tools/*.py`(validator·`check_versions`·`kt_contrast`·`ux_lint`·`check_spdx` 등)는 Windows Python 3.11+ stdlib에서 동작해야 하며 CI `tools` job이 ubuntu+windows 매트릭스로 보증한다. 패키지 빌드·`consumer-smoke`는 ubuntu만 검증한다.
3. runbook 명령은 bash 표기 1벌(`python3 -B -X utf8 …`, `uv run …`, `npm …`) + "Git Bash에서 동일" 1줄만 둔다. Windows 절(`py -3 -B -X utf8`, nvm-windows, `.gitattributes` LF, `core.autocrlf=false`)은 `docs/dev-environment.md`에만 둔다.
4. worktree는 임시 프로필이다: 기본은 메인 체크아웃의 작업 브랜치이며, 병렬·격리·독립 리뷰 때만 `<repo>-wt/<agent>-<task>`(리뷰용 `<repo>-wt/review-<id>`)를 만들고 종료 후 `git worktree remove` + `git worktree prune`한다. 같은 브랜치 이중 checkout은 금지하고 리뷰 기준선은 `--detach`로만 만든다.
5. 개행은 `.gitattributes`(`* text=auto eol=lf`, `*.ps1` CRLF)가 정규화한다. `i/crlf`가 보이면 `git add --renormalize`한다.
6. 소비자에게 배포하는 공통 절은 OS를 규정하지 않는다. 불변 조건(같은 브랜치 이중 checkout 금지·종료 후 정리)만 공통이고 프로필은 각 저장소 `dev-environment.md`가 선언한다.

## 대안 검토

- **canview대로 Windows PowerShell 정본**: 현재 사용자 환경과 맞지만 소비자 6개의 Linux/WSL 정본·CI ubuntu와 어긋나고, runbook 명령을 두 벌 유지해야 한다.
- **Windows 완전 미지원(Tier 3)**: 문서 검증 도구조차 WSL을 요구하게 되어 현재 작업 흐름을 막는다. 도구는 stdlib이라 Tier 2 보증 비용이 작다.
- **고정 worktree(에이전트별 자산)**: 소비자 4곳 관례이지만 장기 잔존 브랜치·빌드 산출물·정리 누락을 구조적으로 남긴다(canview ADR-003과 같은 판단).

## 결과

- 명령과 경로가 CI와 같은 환경에서 재현되고 Windows에서는 도구만 같은 결과를 낸다.
- Windows에서 실행하지 못한 gate(패키지 빌드·스모크)는 성공으로 표시하지 않고 `NOT_RUN(사유)`로 기록한다.
- worktree 정리 확인이 PR 절차의 일부가 되며 실패 패턴 표에 잔존·이중 checkout 행이 있다.
- 소비자 공통 절이 OS를 규정하지 않으므로 airport(WSL2 1차·PowerShell 보조)처럼 혼합 프로필도 수용된다.

## 후속·적용 위치

- 환경 상세: `docs/dev-environment.md`(entry, T-001)
- 절차: `docs/runbooks/agent-workflow.md` §2·§8, `AGENTS.md` §5
- CI: T-009(`tools` windows 매트릭스), T-002(validator Windows 동작·LF)
- 실패 패턴: `docs/runbooks/agent-failure-patterns.md`(CRLF·worktree 행)
