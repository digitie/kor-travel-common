# kor-travel-common 개발 환경

이 문서는 [문서 지도](README.md)의 개발 환경 정본이며 D-03([설계 브리프](plan/design-brief.md) §1 A)을 규칙으로 옮긴다: 정본 OS, 경로 표기, 임시 worktree 프로필, 도구 설치, Windows Tier 2, 검증 명령 사다리. branch·worktree 명령, CodeGraph 수명주기, 2인 리뷰, PR 절차는 [agent workflow](runbooks/agent-workflow.md)에만 둔다. 확정 task: T-001(문서 확정) · 마지막 갱신: 2026-09-06. 소비 저장소의 개발 환경은 이 문서가 규정하지 않는다(각 저장소의 `docs/dev-environment.md`와 ADR이 프로필을 선언한다).

## 1. 실행 원칙

- common의 정본 개발 환경은 Linux/WSL bash다. CI는 GitHub Actions ubuntu이며 목표 러너는 `ubuntu-24.04`다. 현재 `.github/workflows/docs.yml`은 `ubuntu-latest`·Python 3.12로 돌며(사실) T-009에서 러너·액션 SHA 핀·`permissions`를 정렬한다.
- Windows 지원은 Tier 2다 — 열림(사용자 확인 필요, O-17; 기본값 Tier 2). `tools/*.py`(문서 validator 2종·`check_versions`·`kt_contrast`·`ux_lint`·`check_spdx`)는 Windows Python 3.11+ 표준 라이브러리에서 동작해야 하고, CI `tools` job이 ubuntu+windows 매트릭스로 보증한다(T-009). 패키지 빌드·`consumer-smoke`는 ubuntu에서만 실행한다.
- runbook·task·journal의 명령은 bash 표기 한 벌(`python3 -B -X utf8 …`, `uv run …`, `npm …`)로 쓰고 "Git Bash에서 동일" 한 줄만 덧붙인다. PowerShell 블록은 두지 않는다. Windows 전용 표기는 이 문서 §5에만 둔다.
- 근거: 소비자 7개 중 6개가 Linux/WSL을 정본으로 선언하고(`docs/survey/cross/docs-conventions.md` §1.11·§2 C1), 전 앱 CI가 ubuntu이며(`docs/survey/cross/version-matrix.md` §3.2), 현재 유지자 환경은 Windows다(`docs/survey/cross/canview-structure-checklist.md` §5 Q4). canview는 Windows PowerShell 정본이지만 그 논거 중 OS와 무관한 부분(임시 worktree 정리)만 §3에서 채택한다.

## 2. 경로 표기

| 환경 | 저장소 경로 | 비고 |
|---|---|---|
| Windows(Git Bash·PowerShell) | `F:/dev/kor-travel-common` | NTFS checkout이 Git source of truth |
| WSL | `/mnt/f/dev/kor-travel-common` | 같은 checkout을 마운트로 접근. ext4 미러는 필수가 아니다 |
| 임시 worktree | `F:/dev/kor-travel-common-wt/<agent>-<task>`(WSL `/mnt/f/dev/kor-travel-common-wt/<agent>-<task>`) | §3. 리뷰 기준선은 `…-wt/review-<id>` |

- Markdown 링크는 저장소 상대 경로만 쓴다. 절대 경로 링크(`F:/…`, `/mnt/…`, `/…`)는 `tools/validate_document_links.py`가 오류로 보고한다. journal·evidence에 실행 위치를 남길 때는 backtick 산문으로만 적고 링크로 만들지 않는다.
- 다른 저장소의 파일은 GitHub URL(커밋 고정)로 인용한다. 소비자 로컬 체크아웃 경로는 조사 문서의 기준 표(`docs/survey/README.md` §2.1)에만 둔다.
- 경로 구분자는 문서에서 `/`로 통일한다. `.editorconfig`가 utf-8·LF·최종 개행을 강제하고 `*.ps1`만 CRLF다.

## 3. 임시 worktree 프로필

common은 canview ADR-003 계열의 **임시 worktree 프로필**을 쓴다(`docs/survey/cross/docs-conventions.md` §2 C2). 소비 저장소의 고정 worktree 프로필(geo·map·pinvi·ktdm)은 각 저장소가 선언하며 common 공통 절은 불변 조건만 배포한다.

- 기본은 메인 checkout `F:/dev/kor-travel-common`의 작업 branch(`agent/<agent>-<task>`, `origin/main`에서 분기)다. `main`에는 직접 push하지 않는다.
- 임시 worktree `<repo>-wt/<agent>-<task>`는 (1) 서로 다른 변경의 병렬 구현, (2) dirty checkout과의 격리, (3) 리뷰어의 immutable 기준선(`--detach`) 중 하나가 실제로 필요할 때만 만든다. 단순 문서·소규모 수정에는 만들지 않는다.
- 불변 조건: 같은 branch를 두 worktree에서 checkout하지 않는다. 사용자 변경이 있는 checkout을 정리·덮어쓰지 않는다. merge 또는 abandon 뒤 활성 프로세스·미커밋 변경·보존할 commit이 다른 ref에 도달했는지 확인하고 `git worktree remove` → `git worktree prune`으로 제거한다. worktree는 상시 자원이 아니다.
- 생성·삭제·detached 기준선 명령과 CodeGraph 수명주기(`init -i`·`sync`·`status`)는 [agent workflow](runbooks/agent-workflow.md)에만 둔다. 잔존 worktree 복구는 [failure patterns](runbooks/agent-failure-patterns.md)를 본다.

## 4. 도구

| 도구 | 기준 | 정본·근거 |
|---|---|---|
| Git | Git for Windows 또는 WSL git. `core.autocrlf=false`. 개행은 `.gitattributes`(`* text=auto eol=lf` + 확장자별 LF, `*.ps1` CRLF, 바이너리 명시)가 결정 | `.gitattributes`, `.editorconfig` |
| Node.js | 22.x — `.nvmrc` `22.23.1`, `engines.node ^22.12.0`(floor 22.12, recommended 22.23.x). nvm(Linux/WSL) 또는 nvm-windows | D-33·D-06; 값 정본은 `versions.json` |
| npm | `packageManager: "npm@11.19.1"`. Node 22 동봉 npm은 10.9.x(floor 10.9)이므로 `npm install -g npm@11.19.1` 후 `npm ci`(CI 동일) | D-33; `docs/survey/cross/version-matrix.md` §3.2·§4.4 |
| Python | 3.11+(공통 패키지 `requires-python >=3.11`, 3.11 문법). 개발·CI 기본 3.12. 실행은 항상 `python3 -B -X utf8` | D-06·D-15; `.github/workflows/docs.yml` |
| uv | 0.12.x(floor 0.11). `packages/py/kor-travel-common/uv.lock` + `uv sync --locked` | D-06; `docs/survey/cross/version-matrix.md` §2.1 |
| CodeGraph | 선택. 설치돼 있고 변경 범위 분석에 유용할 때만 쓴다. 없으면 `rg`·컴파일러·테스트·수동 추적으로 대체하고 한계를 journal에 기록한다. `.codegraph/`는 gitignore | `docs/survey/cross/docs-conventions.md` §1.13(canview 관행) |
| rg(ripgrep) | 문서·식별자·링크 검색 기본 도구 | `AGENTS.md` §3 토큰 절약 규칙 |

버전 축의 floor/recommended/exceptions 정본은 `versions.json`이고 의미는 [versions 규약](standards/versions.md)에 있다. 이 표는 common 자체 개발에 필요한 값만 옮긴 것이며 값이 다르면 `versions.json`이 맞다.

루트 `package.json`은 `workspaces: ["packages/*"]`이며 `package-lock.json`(v3)을 커밋한다(T-101에서 생성). Python 패키지는 hatchling + uv다(T-302). 패키지별 스크립트와 빌드 산출물은 [packages](architecture/packages.md)가 정본이다.

## 5. Windows Tier 2

Git Bash에서는 bash 표기 명령이 그대로 동작한다(`python3`가 없으면 `python -B -X utf8`). PowerShell에서는 아래 치환만 적용한다.

| 항목 | Windows 표기 |
|---|---|
| Python 실행 | `py -3 -B -X utf8 tools/validate_document_links.py` |
| unittest | `py -3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v` |
| Node 버전 | nvm-windows `nvm install 22.23.1` → `nvm use 22.23.1`, 이후 `npm install -g npm@11.19.1` |
| uv | Windows 설치본에서 같은 명령(`uv sync --locked`, `uv run …`) |
| 개행 | `git config core.autocrlf false`. `.gitattributes`가 LF를 강제하므로 편집기가 CRLF로 저장해도 stage 시 정규화된다. 확인: `git ls-files --eol <path>`의 `i/`가 `lf`. `i/crlf`면 `git add --renormalize <path>` |
| 편집기 | `.editorconfig`(utf-8·lf·최종 개행·`*.ps1`만 crlf)를 적용한다 |

Windows에서 통과한 결과는 §6의 1·2층(문서·도구)에만 유효하다. 패키지 빌드·tarball 설치·소비자 스모크는 ubuntu(CI 또는 WSL)에서 다시 실행하고, 실행하지 못했으면 `NOT_RUN(Windows Tier 2)`로 남긴다.

## 6. 검증 명령 사다리

변경 범위에 맞는 층만 실행한다. 실제로 실행한 층만 통과로 기록하고 하위 층을 상위 층 결과로 대체하지 않는다(`AGENTS.md` §8). 검증 도구가 통과했다는 사실은 제품 gate 통과를 뜻하지 않는다([tools](../tools/README.md)).

| 층 | 대상 | 명령(bash; Git Bash 동일) | CI job(D-18) |
|---|---|---|---|
| 1 문서 | Markdown 링크·task metadata·DAG·validator 회귀·공백 | `python3 -B -X utf8 tools/validate_document_links.py` / `python3 -B -X utf8 tools/validate_plan.py` / `python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v` / `git diff --check` | `docs` |
| 2 도구 | `tools/*.py` 자기 테스트(ubuntu+windows) | 1층 unittest + 도구별 `tests/test_*.py` | `tools`(T-009) |
| 3 패키지 빌드·타입 | tokens·ui 빌드, `noUncheckedIndexedAccess` 타입 검사, 단위 테스트(vitest+RTL+jsdom), 생성물 diff | `npm ci` → `npm run build --workspaces` → `npm test --workspaces` | `packages`(T-101·T-201) |
| 3' Python | `uv build`·pytest·starlette 0.4x/1.6 매트릭스 | `uv sync --locked --all-extras` → `uv run pytest` → `uv build` | `python-package`(T-302) |
| 4 산출물 설치 | `npm pack` tarball을 임시 디렉터리에 설치해 import·CSS·d.ts 존재 확인; wheel 설치 | `npm pack -w packages/tokens` 후 임시 프로젝트에서 `npm install <tgz>` | `packages`, `python-package` |
| 5 소비자 빌드 | 패키지별 승인 소비자 pinned SHA에서 webpack·Turbopack `next build` | `consumer-smoke` dispatch(주간 schedule 병행) | `consumer-smoke`(T-010) |
| 6 소비자 실측 | 소비자 저장소의 e2e·6폭 시각 diff·배포 스모크 | 소비자 PR에서 실행 | 소비자 CI |
| 횡단 | 버전 정렬 report, 대비, UX 금지 패턴, SPDX, secret | `tools/check_versions.py`, `tools/kt_contrast.py`, `tools/ux_lint.py`, `tools/check_spdx.py` | `check-versions`(report), `secret-scan`(T-009·T-103·T-003) |

- 3층 이상의 정확한 스크립트명은 패키지를 만드는 task(T-101·T-201·T-302)에서 확정하고 [packages](architecture/packages.md)·[release](runbooks/release.md)에 반영한다. 그 전까지 위 3~4층 명령은 후보다.
- 5·6층은 소비자 저장소·registry·CI가 필요하다. common에서 실행하지 못하면 `NOT_RUN(사유)`로 남기고 DONE 전 `외부 선행`으로 승격한다(D-25). 0 test·skip은 pass로 집계하지 않는다.
- 횡단 도구의 인자·출력 형식은 각 규칙 문서([versions](standards/versions.md)·[design tokens](standards/design-tokens.md)·[ux guide](standards/ux-guide.md)·[licensing](standards/licensing.md))와 [tools](../tools/README.md)가 정본이다.
