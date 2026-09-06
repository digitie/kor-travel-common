# 횡단 비교 — canview 구조 체크리스트

canview 저장소의 파일 구조·`AGENTS.md`·문서 규약·검증 도구를 **기계적으로 대조 가능한 체크리스트**로 추출한다. 목적은 `kor-travel-common`이 canview의 프로젝트 구조와 `AGENTS.md` 내용을 충실히 가져왔는지를 나중에 항목 단위로 확인하는 것이다. 모든 항목은 **사실 / 후보 / 추정 / 미확인**으로 구분하며, 별도 표기가 없는 서술은 아래 기준 커밋에서 직접 확인한 사실이다. 하드웨어·차량·firmware 항목은 common에 불필요한 것으로 판단하되 판단 근거를 적는다.

## 기준

| 저장소 | 경로 | 기준 커밋 | 비고 |
|---|---|---|---|
| canview (참조 모델) | `F:/dev/canview` | `1f93b8adb34a48537db69b950c8a99ce89859760` (2026-09-06, "fix: revoke SPORT ownership across gaps and align evidence contracts") | 추적 파일은 모두 HEAD와 동일. 작업 트리에 **미추적 파일 6개**가 있음: `docs/reviews/adversarial/2026-09-06-plan-ui.md`, `evidence/2026-09-06-plan-ui-{probes,reviewer-a,reviewer-a-postfix,reviewer-b,reviewer-b-postfix}.md`. 이 6개를 인용할 때는 "미추적(작업 트리)"로 표기한다 |
| kor-travel-common (대조 대상) | `F:/dev/kor-travel-common` | `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0` ("Initial commit"), branch `feat/bootstrap-survey-and-integration-plan` | 추적 파일은 `LICENSE` 1개. `.editorconfig`, `.gitattributes`, `.github/`, `.gitignore`, `docs/`, `tests/`, `tools/`는 모두 **미추적 작업 트리**. 빈 디렉터리 `docs/adr`, `docs/architecture`, `docs/plan`, `docs/standards` 존재 |
| 선행 조사 | `docs/survey/cross/docs-conventions.md` | canview `d078437` 기준 | 본 문서 기준 `1f93b8a`는 `d078437`의 직후 커밋 1개(`git log d078437..HEAD` = 1건)로, 문서 규약 파일의 차이는 없다(사실: 해당 커밋은 review 색인·evidence 계약 정렬만 변경) |
| 선행 검토 보고서 | `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` | 2026-09-05 | `canview` 문자열 0회(사실). 본 주제와 직접 겹치는 절이 없어 재검증 대상이 아니다 |

## 방법

- 읽기 명령: `git log -1`, `git status --short`, `git ls-files`, `cat`/`head`/`sed -n`/`grep -n` (Git Bash). canview·common 어느 쪽에도 파일을 쓰지 않았다.
- 대조 명령: `diff --strip-trailing-cr -u canview/<f> kor-travel-common/<f>` (13개 파일), `file`로 개행 형식 확인.
- 검증 도구 실행(읽기 전용, `python -B -X utf8`, Python 3.14.3): canview에서 `tools/validate_plan.py`(상세 task 46, 오류 0)와 `tools/validate_document_links.py`(139 문서, 959 local target, 오류 0); common에서 `validate_plan.py`(오류 3), `validate_document_links.py`(22 문서, 28 target, 오류 17), `unittest discover -s tests -p test_plan_validation.py`(35 tests OK). 실행 전후 `git status`와 `__pycache__` 검색으로 부산물이 없음을 확인했다.
- 읽은 canview 파일: `AGENTS.md`, `SKILL.md`, `README.md`, `CHANGELOG.md`, `.gitignore`, `.gitattributes`, `tokens.css`, `docs/README.md`, `docs/resume.md`, `docs/tasks.md`, `docs/tasks-rule.md`, `docs/tasks-done.md`, `docs/tasks/README.md`, `docs/tasks/T-001-host-toolchain-ci.md`, `docs/tasks/T-100a-pcb-production-design.md`, `docs/adr/README.md`, `docs/adr/001…007`(전문 또는 머리), `docs/decisions.md`, `docs/journal.md`, `docs/runbooks/{README,agent-workflow,documentation-maintenance,agent-failure-patterns}.md`, `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`, 통합 report 2개와 evidence 4개, `docs/architecture/README.md`, `docs/development/windows.md`, `docs/ui/design.md`(§1–§5), `tools/README.md`, `tools/toolchain-versions.json`, `tools/validate_document_links.py`, `tools/validate_plan.py`, `tests/test_plan_validation.py`.
- 선행 조사 문서 `docs/survey/cross/docs-conventions.md` §1.6–1.9, §1.19, §2(C1–C11), §3, §4, §5를 읽고 인용한다. 그 문서 §4는 common 작업 트리 파일의 **내용을 검토하지 않았다**고 밝히고 있으므로(Q11), 본 문서 §1.2가 그 공백을 채운다.

## 1. 파일 목록 체크리스트

### 1.1 canview 파일과 common 필요 여부

판단 어휘: **필수**(구조·규약상 같은 경로에 있어야 함), **변형**(역할은 필요하지만 내용·경로를 common 용도로 바꿈), **불필요**(하드웨어·차량·firmware·임베디드 전용). 상태 어휘: **있음**(같은 경로에 존재), **변형됨**(존재하되 내용이 canview와 다름), **없음**.

| # | canview 경로 | 역할(사실) | common 필요 | 근거 | common 상태(`b92fabe` 작업 트리) |
|---|---|---|---|---|---|
| F01 | `AGENTS.md` | 8절 정책 정본(§2 체크리스트) | 변형 | 도메인 §1·§6·§7이 차량 종속 | 없음 |
| F02 | `SKILL.md` | 5절 작업 라우터(최소 컨텍스트·작업별 시작점 표·저장소 영역·핵심 용어·종료 경로), 정책 복제 금지 | 변형 | 시작점 표·용어를 common 도메인으로 교체. docs-conventions C4/Q2 참조 | 없음 |
| F03 | `README.md` | 5절: 문서 / UI prototype / 저장된 DBC / 저장소 상태 / 주요 원문 | 변형 | "문서" 절(문서 지도 링크 6개)과 "저장소 상태" 절만 구조로 재사용 | 없음 |
| F04 | `CHANGELOG.md` | `## [Unreleased]` + `### Added` / `### Changed`, 사용자 가시 변경만 | 필수 | 라이브러리 릴리스와 직결 | 없음 |
| F05 | `LICENSE` | GPL-3.0 | 필수 | — | 있음(GPL-3.0) |
| F06 | `.gitignore` | firmware build / 편집기 상태(`.vscode/ .claude/ .codegraph/`) / 비밀·evidence(`.env*`, `*.local.md`, `.tools/` 등) 4그룹 | 변형 | firmware·KiCad 항목 제거, Node/Python 추가 | 변형됨(§1.2) |
| F07 | `.gitattributes` | `hardware/**` KiCad 텍스트 eol=lf, pdf/png binary만 | 변형 | 전역 `* text=auto eol=lf` 필요 | 변형됨(§1.2) |
| F08 | `tokens.css` | 루트 CSS custom property 57개(color 25, font 2, space 7, text 5, radius 4, rule 2, touch 2, ease 3, dur 3, z 4). `docs/ui/design.md` §5가 정본으로 지정 | 변형 | 토큰은 패키지 산출물(docs-conventions §4 동일 판단) | 없음 |
| F09 | `docs/README.md` | 문서 지도: 읽기 단계 표(반드시/필요 시/특수) → 정본 관계 트리 → 분야별 표 → 작업·운영·이력 표(읽는 시점 열) → 탐색 규칙 5 | 필수 | 3단계 읽기 정책의 구현체 | 없음 |
| F10 | `docs/resume.md` | 5절: 현재 진척도 / 다음 한 작업 / 현재 열린 핵심 경로 / 알려진 차단 조건 / 문서 정본 | 필수 | — | 없음 |
| F11 | `docs/journal.md` | H1 + `## YYYY-MM-DD (agent[, 주제])` newest-first 9건 | 필수 | — | 없음 |
| F12 | `docs/tasks.md` | 6절: 사용법(상태 표) / 공통 실행 규칙 10 + 검사 명령 3 / task 목록(5열 표, 그룹별 6표) / critical path / gate 현황(G0–G6) / 완료와 변경 기록. 본문에 "46개의 상세 작업" 1회 | 필수 | validator 입력 | 없음 |
| F13 | `docs/tasks-done.md` | newest-first archive(현재 표 없음, 산문 2문장) | 필수 | validator 입력 | 변형됨(§1.2) |
| F14 | `docs/tasks-rule.md` | 6절 규약(§3.1) | 필수 | — | 변형됨(§1.2) |
| F15 | `docs/tasks/README.md` | 포인터 2단락 | 필수 | — | 변형됨(§1.2) |
| F16 | `docs/tasks/T-*.md` ×46 | 상세 task(§4 문법) | 변형 | 내용은 전부 canview 도메인. 형식만 채택 | 없음(0개) |
| F17 | `docs/adr/README.md` | 규칙 5 + 목록 표(ADR·제목·상태) | 필수 | — | 없음(디렉터리만) |
| F18 | `docs/adr/001…007-<slug>.md` | ADR 7개 | 변형 | 형식만 채택; 내용 불필요(ADR-002/004의 문서구조 결정은 common ADR-001 후보 소재) | 없음 |
| F19 | `docs/decisions.md` | ADR 색인 중복 표(ADR·상태·제목·위치) + "다음 후보 번호는 ADR-008" | 후보 | canview는 `adr/README.md`와 이중 관리. docs-conventions §4는 "불필요"로 판단했으나 common의 `documentation-maintenance.md` §2·§3은 `decisions.md` 갱신을 요구한다(충돌, 열린 질문 Q1) | 없음 |
| F20 | `docs/architecture/README.md` | 문서 사용법 표 → §1 시스템 범위 → §2 데이터 흐름 → §3 책임과 신뢰 경계 → §4 안전 상태 → §5 저장소 구조 → §6 문서 정본 | 변형 | 절 골격(사용법 표·범위·흐름·경계·저장소 구조·정본)만 채택 | 없음(디렉터리만) |
| F21 | `docs/architecture/{system,features,automation,ota,diagnostic-bridge,controller-can-pipeline}.md`, `protocols/*` ×4 | 차량·protocol 설계 | 불필요 | 임베디드 도메인 | — |
| F22 | `docs/architecture/implementation-readiness.md` | "구현자가 다시 결정하지 않을 사항", 정본과 생성물, repository 목표 구조, 장치별 책임 | 변형 | "채택 준비 기준"으로 역할 이식 가능(docs-conventions §4 `adoption-readiness.md` 후보) | 없음 |
| F23 | `docs/architecture/requirements-coverage.md` | 요구→정본→task→검증 상태→남은 gate 추적표(R-01…) | 변형 | 소비자별 채택 gate 추적표로 형식 재사용 후보 | 없음 |
| F24 | `docs/development/windows.md`, `toolchains.md` | Windows 정본 환경·검증 계층·장치별 SDK | 변형 | `docs/dev-environment.md`(docs-conventions C1) | 없음 |
| F25 | `docs/hardware/**` ×9, `docs/vehicle/**` ×3, `docs/images/*.png` ×14 | 회로·차량·UI 스크린샷 | 불필요 | 하드웨어·차량. `images/`는 UI 스크린샷이 생기면 선택 | — |
| F26 | `docs/ui/design.md` | 8절: 목표와 기준 / LVGL 데모 검토 / 정보 구조 / 제한속도·야간·유휴 / 시각·동작 token / Web·LVGL 매핑 / 화면 prototype / 실제 보드 검증 기준 | 변형 | §1(원칙)·§3(정보 구조)·§5(token 정본 지정) 골격만 채택; docs-conventions §4는 루트 `DESIGN.md` + `docs/standards/*`로 배치 | 없음 |
| F27 | `docs/ui/lvgl-demo-review.md` | LVGL 데모 채택 근거 | 불필요 | 임베디드 UI | — |
| F28 | `docs/runbooks/README.md` | 표(문서·읽는 시점·책임) 3행 | 필수 | — | 변형됨(§1.2) |
| F29 | `docs/runbooks/agent-workflow.md` | 8절(§3.4) | 필수 | OS·worktree 경로만 변형 | 없음 |
| F30 | `docs/runbooks/documentation-maintenance.md` | 7절 | 필수 | — | 변형됨(§1.2) |
| F31 | `docs/runbooks/agent-failure-patterns.md` | 단일 표(증상·먼저 확인할 것·복구) 14행 + 추가 규칙 1문장 | 변형 | 14행 중 12행이 임베디드; 링크 깨짐·WSL/Windows 차이·worktree 잔존 3행만 재사용 | 없음 |
| F32 | `docs/reviews/README.md` | 기록 규칙 9 + 리뷰 목록 표(날짜·종류·기준선·범위·리뷰어·결과) + 새 리뷰 시작 | 필수 | — | 변형됨(§1.2) |
| F33 | `docs/reviews/adversarial/TEMPLATE.md` | 머리 불릿 11 + 7절 | 필수 | — | 있음(diff 0) |
| F34 | `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md` ×5(추적) + 1(미추적) | 통합 report | 변형 | 형식만; 내용 불필요 | 없음 |
| F35 | `docs/reviews/adversarial/evidence/*.md` ×18(추적) + 5(미추적) | reviewer 원본·manifest·probe | 변형 | 디렉터리와 명명 규칙만 | 디렉터리 + `.gitkeep` |
| F36 | `tools/README.md` | Windows toolchain manifest 설명·SDK 준비·대상별 빌드·KiCad 재생성 | 변형 | 문서 검증 도구 설명으로 교체 | 변형됨(전면 재작성, §1.2) |
| F37 | `tools/validate_document_links.py` | Markdown 로컬 링크 검사(§4.2) | 필수 | — | 변형됨(§1.2) |
| F38 | `tools/validate_plan.py` | task metadata·DAG 검사(§4.1) | 필수 | — | 변형됨(docstring 1줄) |
| F39 | `tests/test_plan_validation.py` | validator 회귀 35 tests | 필수 | — | 변형됨(식별자 2곳) |
| F40 | `tools/toolchain-versions.json` | `schemaVersion`, `checkedAt`, `host`, `tools`, `eda`, `sdk`(버전 + `gitCommit` pin) | 변형 | "라이브러리/플랫폼 버전 일치" 정책의 machine-readable 정본 형식으로 재사용 후보(docs-conventions §4 `versions.json` 후보) | 없음 |
| F41 | `tools/environment/setup-windows.ps1`, `tools/hardware/**` ×15, `tools/protocol/**` ×2, `tools/ui/**` ×2 | SDK·KiCad·codec·UI 검사 | 불필요 | 임베디드 전용. 단 "manifest 버전 대조 스크립트"라는 역할은 F40과 함께 변형 후보 | — |
| F42 | `tests/automation/**` ×5, `tests/lvgl/**` ×3, `tests/ui/**` ×1 | host C·LVGL·브라우저 시험 | 불필요 | — | — |
| F43 | `dbc/` ×5, `firmware/` ×31, `hardware/` ×210, `protocol/` ×2, `ui/` ×12 | 제품 소스 | 불필요 | 라이브러리 구조는 별도 조사 범위 | — |
| F44 | `.tools/`(gitignore) | 로컬 빌드·리뷰 부산물 | 불필요 | — | — |
| F45 | (없음) `CLAUDE.md` | canview는 `.claude/` 전체를 gitignore하고 `CLAUDE.md`가 없다 | 추가 | docs-conventions C3(40줄 이하 포인터) | 없음 |
| F46 | (없음) `.editorconfig` | canview에 없음 | 추가 | common이 신규 작성 | 있음(canview 원본 없음) |
| F47 | (없음) `.github/workflows/*` | canview에 CI 없음(T-001 READY, `docs/tasks.md` §2 검사 3개는 수동 실행) | 추가 | — | `docs.yml` 있음(canview 원본 없음) |

### 1.2 이미 옮겨진 파일의 변형 내용(diff 결과)

`diff --strip-trailing-cr` 기준. "개행" 열은 `file` 출력. common의 `.gitattributes`가 `*.py text eol=lf`를 선언하므로 작업 트리의 CRLF는 `git add` 시 정규화될 것으로 **추정**한다(미확인: 아직 add되지 않음).

| 파일 | 변경 줄 | 변형 내용(사실) | 개행(canview→common) |
|---|---|---|---|
| `tools/validate_plan.py` | 2 | docstring "G0–G6 통과" → "gate 통과". 파서·규칙 무변경 | LF → CRLF |
| `tools/validate_document_links.py` | 7 | 대상: `docs/**` + `hardware/**` + 루트 + `tools/README.md` → `docs/**` + `packages/**` + `tools/**` + 루트, `node_modules` 제외. 절대 접두 `/mnt/f/dev/canview/`·`F:/dev/canview/` → `…/kor-travel-common/`으로 **유지·치환**(docs-conventions C11의 "접두 허용 제거" 제안과 불일치, 열린 질문 Q2) | LF → CRLF |
| `tests/test_plan_validation.py` | 4 | 모듈명 `canview_plan_validation` → `kor_travel_common_plan_validation`, tempdir prefix 변경. 35 tests 무변경 | LF → CRLF |
| `docs/tasks-rule.md` | 34 | §머리: validator 명령·"문법 규칙은 검사기 형식과 일치" 추가. §2 ID 대역을 common 도메인 6대역 + §2.1 소비 앱 이관 대역표(T-400~T-489) 신설. §3 외부 대기 예시 교체·`외부 선행` 명시. §4 **canview의 체크박스 예시를 5열 표 문법으로 교체**하고 "N개의 상세 작업" 규칙 명문화. §5 파일명·H1·metadata 4줄 문법과 Gate 예시 명문화, 이관 task 필수 기재 추가, READY/DONE 선행 조건 추가. §6 DONE 처리 시 요약 이동 명시 | LF → LF |
| `docs/runbooks/README.md` | 12 | 제목·서문(`standards` 링크 추가). 표: agent workflow 책임에서 "Windows" 삭제; `consumer-adoption.md`, `release.md` 행 추가; failure patterns 책임을 "환경·패키징·스타일·소비자 통합"으로 교체. 링크 대상 5개(`agent-workflow.md`, `consumer-adoption.md`, `release.md`, `agent-failure-patterns.md`, `../standards/README.md`, `../architecture/README.md`, `../tasks.md`, `../README.md`)가 아직 없음 | LF → LF |
| `docs/runbooks/documentation-maintenance.md` | 29 | §1 표에 `CLAUDE.md`, `SKILL.md`, `docs/standards/`, `docs/survey/`, `docs/plan/` 행 추가, 문구를 패키지·계약 용어로 치환. §2 표에 "공통 규칙 변경", "조사 기준 커밋 갱신" 행 추가, ADR 행에 `decisions.md` 추가. §3 제목에 standards 추가, superseded 표기 `superseded by ADR-XXX` 명시, machine-readable 정본 예시를 `packages/*/tokens.css`·`standards/versions.md`로 교체. §4 journal에 "소비 저장소 상태(커밋·브랜치·dirty)" 추가. §6 6단계에 validator 명령 명시. §7 언어 예외에 "패키지명" 추가, 비밀 항목을 운영 호스트·자격증명·`*.local.md`로 교체, 최종 점검에 두 validator 통과 추가 | LF → LF |
| `docs/reviews/README.md` | 10 | 제목·서문(`standards` 추가). 리뷰 목록 6행 삭제(빈 표). 기록 규칙 9개·새 리뷰 시작 절 무변경 | LF → LF |
| `docs/reviews/adversarial/TEMPLATE.md` | 0 | 동일 | LF → LF |
| `docs/tasks-done.md` | 7 | 제목 변경, 산문 → "## 완료 목록" + 5열 빈 표(헤더 `ID|상태|우선순위|작업|선행`, 우선순위 `---:`) | LF → LF |
| `docs/tasks/README.md` | 2 | 마지막 문장에 validator 통과 조건 추가 | LF → LF |
| `.gitignore` | 43 | firmware/KiCad/provisioning/captures 삭제; Node(`node_modules/ dist/ .next/ out/ coverage/ *.tsbuildinfo .turbo/`), Python(`__pycache__/ .venv/ .pytest_cache/ .mypy_cache/ .ruff_cache/ build/ *.egg-info/`), 편집기(`.idea/ .playwright-mcp/ test-results/ playwright-report/`), `*.local.sh`, OS 파일 추가. `.vscode/ .claude/ .codegraph/ .env .env.* !.env.example *.local.md`는 유지 | LF → LF |
| `.gitattributes` | 25 | `hardware/**` 10줄 → `* text=auto eol=lf` + md/json/yml/yaml/css/ts/tsx/py/toml eol=lf, `*.ps1 eol=crlf`, png/jpg/woff2/pdf binary | LF → LF |
| `tools/README.md` | 49 | 전면 재작성: 두 validator의 검사 내용·실행 명령 표, "canview 동명 도구를 적응" 명시, 회귀 시험 명령 | LF → LF |
| `.editorconfig` | 신규 | `root=true`, utf-8, lf, 최종 개행, 공백 제거, indent 2(`*.py` 4, 100열), `*.md` 공백 유지, `*.ps1` crlf | — |
| `.github/workflows/docs.yml` | 신규 | ubuntu-latest, `actions/checkout@v6`, `setup-python@v6`(3.12), 링크 검사 → plan 검사 → unittest → `git diff --check` 4단계 | — |

### 1.3 common 현재 상태에서의 검증 도구 결과(사실, 2026-09-06 실행)

| 도구 | 결과 | 원인 |
|---|---|---|
| `validate_plan.py` | 오류 3: `docs/tasks: 상세 task 파일이 없음`, `docs/tasks.md: 읽기 실패`, `상세 task 수 불일치 (실제 0)` | `docs/tasks.md`와 상세 task가 아직 없음 |
| `validate_document_links.py` | 22 문서, 28 target, 오류 17 | 미작성 문서 링크 16건(`agent-workflow.md` 6회, `../README.md` 2회, `../tasks.md` 2회, `../architecture/README.md`, `../standards/README.md`, `consumer-adoption.md`, `release.md`, `agent-failure-patterns.md`, `docs/tasks-rule.md → runbooks/agent-workflow.md`) + 산문 오탐 1건(`docs/survey/cross/design-tokens.md`에서 대괄호 바로 뒤에 소괄호가 오는 일반 문장을 링크로 오인) |
| `unittest` | 35 tests OK | — |

docs.yml은 이 세 단계를 모두 실행하므로, 현재 상태로 push하면 CI가 실패한다(추정: 워크플로가 아직 커밋되지 않았으므로 실행 이력 없음).

## 2. AGENTS.md 절별 체크리스트

각 행은 canview `AGENTS.md`의 검증 가능한 규칙 1개다. "변형 방향"은 후보이며, docs-conventions §3.1의 공통 절 배치(A–I)를 함께 표기한다.

### 2.1 §1 목표와 안전 경계

| ID | 핵심 규칙(사실) | common 변형 방향(후보) |
|---|---|---|
| A1.1 | 첫 문장이 제품 정의 1문장 | "kor-travel 제품군의 UI·백엔드 공통 코드와 규칙(색상 톤·UX·OpenAPI·PC/Mobile Web·버전 일치)을 정의하는 GPL-3.0 라이브러리" 1문장 |
| A1.2 | 3열 표(장치·기준 하드웨어·책임) 3행 | 배포 단위(패키지·규칙 문서)·소비자·책임 표. 소비자 7 + kor-travel-airport Admin·PinVi Admin 명시 |
| A1.3 | 1차 대상과 "DBC에 있다는 이유만으로 확정하지 않는다" 경계 | "소비자 한 곳에 있다는 이유만으로 공통화하지 않는다"(선행 보고서 §3의 도입 근거 원칙과 정합) |
| A1.4 | 송신 허용 조건 열거 + Controller는 의미 명령만 요청 | 기존 공유 라이브러리(`maplibre-vworld-react/js`, `python-*-api`, `python-kraddr-base`)와 중복 금지, 소비자 저장소 직접 수정 금지 같은 경계로 치환 |

### 2.2 §2 작업 원칙

| ID | 핵심 규칙(사실) | common 변형 방향 |
|---|---|---|
| A2.1 | 모호하면 가정을 드러내고 확인 | 그대로(공통 절 A) |
| A2.2 | 최소 범위 변경, 무관한 코드·문서·형식 불변 | 그대로 |
| A2.3 | 사용자 변경·dirty worktree 보존 | 그대로 |
| A2.4 | 버그=재현+회귀시험, 리팩터링=동작 보존 근거, 설계 변경=검증 가능한 수용 기준 | 그대로 |
| A2.5 | 실행 못 한 gate를 통과로 표시하지 않음 | 그대로(공통 절 F에도 중복 배치됨, docs-conventions §3.1) |
| A2.6 | 근거 우선; 확인된 사실·후보 해석·실차 evidence를 다른 상태로 관리 | "실차 evidence" → "소비자 저장소 실측(빌드·e2e) evidence" |
| A2.7 | Ruthless Review 4불릿(동작≠검증 완료 / 적대적 리뷰어 / 가정 의심 / 소명 전 미완료) | 문구 그대로(공통 절 B) |

### 2.3 §3 문서 읽기 정책

| ID | 핵심 규칙(사실) | common 변형 방향 |
|---|---|---|
| A3.1 | `AGENTS.md`=짧은 규칙 정본, `docs/README.md`=상세 라우터, 전체 선제 읽기 금지 | 그대로 |
| A3.2 | 반드시 참조 4: AGENTS → docs/README → docs/resume → 지정 task 1파일 | 그대로. `CLAUDE.md`를 두면 그것은 포인터이며 순서에 추가하지 않는다(C3) |
| A3.3 | task를 고를 때만 `docs/tasks.md`; 지정됐으면 backlog 재독 금지 | 그대로 |
| A3.4 | 필요할 때만 참조 표 6행(구조 / branch·PR / Windows toolchain / 하드웨어·차량·UI / 기존 결정 변경 / 문서 유지) | 6행 중 "Windows toolchain·빌드"→"개발 환경·패키지 빌드(`docs/dev-environment.md`)", "하드웨어·차량·UI"→"규칙 산출물(`docs/standards/`)·소비자 이관(runbook)" |
| A3.5 | 특수 참조 5: reviews / journal / adr 전체 / tasks 전체+tasks-done / raw DBC·capture·datasheet | 5번째를 "소비자 저장소 원본·조사 문서(`docs/survey/`) 전체"로 치환 |
| A3.6 | 토큰 절약 5: 인덱스→상세→절 순서 / `rg` 우선 / 링크 연쇄 금지 / review·journal·ADR는 역사 / 문서 충돌 시 정본 우선순위와 충돌 위치 명시 | 그대로 |

### 2.4 §4 문서 정본과 우선순위

| ID | 핵심 규칙(사실) | common 변형 방향 |
|---|---|---|
| A4.1 | 9단계 우선순위: 사용자 > AGENTS > accepted ADR > architecture > 선택한 task > hardware·vehicle·UI·development 문서 > 코드·테스트 > review·journal > 최소 가정 | 6단계를 "standards·dev-environment 문서"로 치환. `SKILL.md` 위치는 docs-conventions C5(architecture와 동급) 채택 여부가 열린 질문(Q3) |
| A4.2 | `SKILL.md`는 라우터이지 정책 정본이 아님 | 그대로(C4 결론 대기) |
| A4.3 | 결정=ADR, 현재 설계=architecture, 범위·수용 기준=task, 반복 절차=runbook; 복제 금지 | 그대로 + "공통 규칙=standards" 1항 추가 |
| A4.4 | 모든 Markdown/RST는 한글; 공식 필드명·코드 식별자·명령어·URL·제공자 원문은 영어 유지 | RST 삭제, "패키지명" 추가(common `documentation-maintenance.md` §7과 일치) |

### 2.5 §5 개발·worktree·리뷰 진입점

| ID | 핵심 규칙(사실) | common 변형 방향 |
|---|---|---|
| A5.1 | 정본 환경 = Windows PowerShell·native 도구; 상세는 `docs/development/windows.md`에만 | OS를 AGENTS에 고정하지 않고 `docs/dev-environment.md`로 위임(C1). common 자체 정본 OS는 열린 질문 Q4 |
| A5.2 | 기본은 메인 checkout 작업 branch; 병렬·격리·독립 리뷰 때만 임시 worktree, merge/abandon 후 제거; 명령은 agent-workflow에만 | 불변 조건(같은 branch 이중 checkout 금지, 종료 후 정리)만 두고 프로필은 dev-environment로 위임(C2) |
| A5.3 | 비단순 변경은 분야가 다른 리뷰어 서브에이전트 2인 독립 적대적 리뷰; 범위·산출물·면제는 agent-workflow와 review archive | 그대로 |

### 2.6 §6 절대 하지 말 것(15항)

| ID | canview 금지 항목(요지) | 판단 | common 대응(후보) |
|---|---|---|---|
| A6.1 | schema/generator 있는 header와 생성물을 수동 불일치 | 추상화 재사용 | 토큰 원본(예: `tokens.css`)과 생성물(Tailwind theme·TS 상수)의 수동 불일치 금지 |
| A6.2 | 임의 CAN ID/data 즉시 송신 | 불필요 | — |
| A6.3 | build mode를 flag 하나로 승격 | 불필요 | — |
| A6.4 | DBC 이름·단일 capture만으로 신호 승격 | 추상화 재사용 | 소비자 1곳 관찰만으로 공통 규칙·컴포넌트 승격 금지 |
| A6.5 | sender precondition을 최종 권한으로 신뢰 | 불필요 | — |
| A6.6 | installation-wide 공유 secret | 불필요 | — |
| A6.7 | GPIO 초기화만으로 안전 주장 | 불필요 | — |
| A6.8 | 데이터시트 미대조 pin 확정 | 불필요 | — |
| A6.9 | upstream DBC 원본 수정 금지, profile·evidence 분리 | 추상화 재사용 | 벤더링 원본(shadcn 생성 컴포넌트·외부 스킬) 수정 시 출처·변경 표기; 조사(`docs/survey/`)와 규범 분리 |
| A6.10 | VIN·위치·key·Wi-Fi secret·capture를 public Git에 넣지 않음 | 재사용 | 운영 호스트·자격증명·`*.local.md`·`.env`로 치환(공통 절 F) |
| A6.11 | 불완전 block diagram을 제작용으로 표시 | 불필요 | — |
| A6.12 | Bridge에 TX 권한 부여 | 불필요 | — |
| A6.13 | stale·candidate·estimated 값을 확정값처럼 표시 | 추상화 재사용 | UX 규칙: 미검증·stale 값을 정상값처럼 렌더링 금지(ux-patterns 조사와 연결) |
| A6.14 | observer stream이 safety queue 잠식 | 불필요 | — |
| A6.15 | wire 변경을 golden·malformed·version 시험 없이 완료 | 추상화 재사용 | 공개 API·OpenAPI 계약 변경을 계약 시험·버전 표기 없이 완료 금지 |
| A6.16 | (절 형식) 번호 목록, 각 항이 "…하지 않는다"로 끝남 | 형식 | 공통 5 + 라이브러리 특화 ≤5로 유지(docs-conventions §3.1 F) |

### 2.7 §7 외부 원문과 evidence

| ID | 핵심 규칙(사실) | 판단 | common 대응 |
|---|---|---|---|
| A7.1 | 외부 원문은 공식 URL + version/commit/revision 기록 | 재사용 | Tailwind·shadcn·Next·FastAPI 등 문서 인용에 그대로 |
| A7.2 | upstream DBC 라이선스·digest 보존, profile과 evidence 분리 | 변형 | 벤더링 코드 라이선스·출처 commit 기록(선행 보고서 §9 라이선스 논점과 연결) |
| A7.3 | datasheet pin과 symbol pin 대조 전 확정 금지 | 불필요 | — |
| A7.4 | 네트워크·차량·하드웨어 필요 검증은 미실행 사유·영향 gate·후속 task 기록 | 재사용 | "소비자 저장소·registry·CI 필요 검증"으로 치환 |

### 2.8 §8 완료와 push

| ID | 핵심 규칙(사실) | common 변형 방향 |
|---|---|---|
| A8.1 | 변경 범위에 맞는 host/target/UI/KiCad/profile 검증 | "문서 검증·패키지 빌드·tarball 설치·소비자 스모크" |
| A8.2 | 비단순 변경은 2인 finding 수정·ADR/task disposition·재검증 | 그대로 |
| A8.3 | 관련될 때만 resume / tasks / 상세 task / ADR / journal / CHANGELOG 갱신 | 그대로(+standards) |
| A8.4 | push 전 staged diff 직접 읽기; secret·VIN·key·로컬 파일 확인; **`git add -A`·`git add .` 금지** | 검사 대상만 치환, 금지 문장 그대로 |
| A8.5 | 실패 검증·미해결 P0/P1·닫히지 않은 gate를 숨긴 채 완료·release 표시 금지 | 그대로 |

## 3. 규약 체크리스트

각 항목은 "예/아니오"로 판정 가능한 문장으로 쓴다. "검사" 열은 canview 도구가 기계적으로 검사하는지(자동/수동). "common" 열은 `b92fabe` 작업 트리 기준 상태.

### 3.1 task 문서 규약(`docs/tasks-rule.md`, `docs/tasks.md`, validator)

| ID | 검증 가능한 문장 | 근거 | 검사 | common |
|---|---|---|---|---|
| R1.1 | 열린 task 요약은 `docs/tasks.md`, 완료는 `docs/tasks-done.md`(newest-first), 상세는 `docs/tasks/T-NNN-*.md`, 진척은 `docs/resume.md` | tasks-rule §1 | 위치는 자동(§4.1 S6) | tasks-rule 채택 |
| R1.2 | task ID는 `T-` + 3자리 숫자(+ 소문자 1자 하위). 참조된 ID는 재번호하지 않는다 | tasks-rule §2, validator `ID_PATTERN` | 자동 | 채택(대역은 common 도메인으로 변경) |
| R1.3 | 상태는 `READY`/`BLOCKED`/`IN_PROGRESS`/`DONE` 4값만 | tasks-rule §3, tasks.md §1 표, validator | 자동 | 채택 |
| R1.4 | 우선순위는 `P0`~`P3` 4값만 | validator `PRIORITIES`(tasks-rule에는 없음) | 자동 | common tasks-rule §5에 명문화됨 |
| R1.5 | 상세 task 상단 metadata는 `상태`·`우선순위`·`Gate`·`선행` 4개 필드가 각각 정확히 1줄 | validator `scalar` | 자동 | 명문화됨 |
| R1.6 | `선행`은 `없음` 또는 쉼표로 구분한 ID 목록만; 외부 조건은 `외부 선행` 줄 | validator `dependencies`, T-100a 예 | 자동 | 명문화됨 |
| R1.7 | 요약 표는 정확히 5열(ID 링크·상태·우선순위·작업·선행)이며 값이 상세와 글자 단위로 같다 | validator `summaries`, tasks.md §3 | 자동 | 명문화됨. canview tasks-rule §4는 체크박스 예시를 남겨 실제 형식과 **불일치**(사실) |
| R1.8 | `docs/tasks.md`에 "N개의 상세 작업" 문구가 정확히 1회, N = 상세 파일 수 | validator `counts` | 자동 | 명문화됨 |
| R1.9 | `READY`/`DONE` task의 선행은 모두 `DONE` | validator `check_graph` | 자동 | 명문화됨 |
| R1.10 | 선행 그래프에 사이클·자기 선행·없는 ID가 없다 | validator | 자동 | 채택 |
| R1.11 | 상세 파일은 목표·고정 결정·구현 범위·범위 밖·예상 변경 파일·수용 기준·검증 명령·evidence·rollback/release 차단 조건 9항목을 포함 | tasks-rule §5 | 수동(validator 미검사) | 채택 + 이관 task 추가 항목 |
| R1.12 | 상세 task에 적힌 미래 경로·명령은 존재·실행·성공의 증거가 아니다 | tasks.md §2-5, T-100a "예상 변경 파일" 서두 | 수동 | common tasks-rule에는 없음(후보: §2 공통 실행 규칙으로 이식) |
| R1.13 | 실행 기록에는 tool version·명령·test 수·exit code·artifact digest; 미실행은 NOT_RUN, 0 test/skip을 pass로 집계 금지 | tasks.md §2-6 | 수동 | 없음(후보) |
| R1.14 | PR에는 Task/Gate/Risk/Tests/Evidence/Rollback | tasks.md §2-7, agent-workflow §7 | 수동 | 없음(agent-workflow 미작성) |
| R1.15 | 완료 시 상세 `DONE` + 요약 행을 tasks-done으로 이동 + 상태가 바뀌면 journal·resume | tasks-rule §6 | 위치만 자동 | 채택 |
| R1.16 | 요약 entry와 상세 파일은 같은 PR에서 추가 | tasks/README.md | 수동 | 채택 |
| R1.17 | `docs/tasks.md` §2에 검사 명령 3개(`validate_plan`, `unittest`, `validate_document_links`)가 있고 "문서 metadata/DAG 검사이지 제품 gate 판정기가 아니다" | tasks.md §2-10 | — | tasks.md 없음 |
| R1.18 | 우선순위 열은 `---:`(우측 정렬) | tasks.md §3 표, common tasks-done.md | 미검사 | 채택 |

### 3.2 ADR·결정 색인 규약

| ID | 검증 가능한 문장 | 근거 | 검사 | common |
|---|---|---|---|---|
| R2.1 | ADR은 파일당 1개, 파일명 `NNN-<slug>.md`(3자리, 소문자 kebab) | adr/README.md 서두, 파일 7개 | 수동 | 디렉터리만 |
| R2.2 | H1은 `# ADR-NNN: 제목` | ADR 7개 모두 | 수동 | — |
| R2.3 | 머리 불릿에 `상태`·`날짜`가 필수; `결정자`·`근거 문서`·`Supersedes`·`배경`·`대체 범위`는 선택 | ADR-001(근거 문서), 003/005(결정자), 004(Supersedes), 006(배경), 007(배경·대체 범위) | 수동 | — |
| R2.4 | 상태 어휘: `accepted`, `superseded by ADR-XXX`, `partially superseded by ADR-XXX`; 상태 뒤에 ` — ` 보충 문구 허용 | ADR-002/006/007, decisions.md | 수동 | documentation-maintenance §3에 `superseded by ADR-XXX` 명시 |
| R2.5 | 본문 절은 `컨텍스트`(또는 `문맥`) → `결정` → `결과`(또는 `결과와 한계`)가 기본이고 `후속`·`대안 검토`·`적용 위치`·`대체`·`영향받는 문서와 task`·`정본과 수용 조건`이 선택 | 7개 ADR H2 목록 | 수동 | — |
| R2.6 | 결정을 뒤집을 때 새 ADR을 만들고 옛 ADR 상태만 바꾼다(삭제 금지) | adr/README.md 규칙 3, decisions.md 말미 | 수동 | 채택 |
| R2.7 | 다음 번호 = `docs/decisions.md` 최댓값 + 1이며 decisions.md에 "다음 후보 번호는 ADR-NNN" 명시 | adr/README.md 규칙 5, decisions.md | 수동 | decisions.md 없음(열린 질문 Q1) |
| R2.8 | ADR 본문과 코드·문서·테스트는 같은 PR에서 동기화 | adr/README.md 규칙 4 | 수동 | — |
| R2.9 | ADR 대상은 여러 subsystem(=여러 소비 저장소)에 영향을 주는 결정만; 공통 정책은 AGENTS, 작업 선택은 SKILL, 절차는 tasks-rule·runbooks | adr/README.md 규칙 1–2 | 수동 | documentation-maintenance §3 채택 |
| R2.10 | `adr/README.md` 표는 `ADR|제목|상태`, `decisions.md` 표는 `ADR|상태|제목|위치` | 두 파일 | 수동 | — |

### 3.3 review 규약(`docs/reviews/README.md`, TEMPLATE, agent-workflow §5)

| ID | 검증 가능한 문장 | 근거 | common |
|---|---|---|---|
| R3.1 | 통합 report 경로는 `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md`; 같은 날 같은 범위 반복은 `-02`, `-03` | reviews/README 규칙 1 | 채택 |
| R3.2 | 실제 관행(사실): post-fix 재검토를 별도 report `…-post-fix.md`로 둔 예 1건(`2026-09-05-latest-toolchain-bootstrap-post-fix.md`)이 있어 규칙 1의 `-02` suffix와 다른 명명이 공존한다 | 파일 목록 | 열린 질문 Q5 |
| R3.3 | reviewer 원본은 `evidence/YYYY-MM-DD-<scope>-reviewer-{a,b}.md`; 관행상 `-post-fix-reviewer-{a,b}`, `-postfix-reviewer-{a,b}`(표기 불일치), `-manifest`, `-postfix-manifest`, `-count-reviewer-{a,b}`, `-coordinator-audit`, `-probes`(미추적) 변형이 존재 | 규칙 5, 파일 목록 | 채택(규칙 5만) |
| R3.4 | 과거 report에 append 금지; 오탈자·링크 correction만 correction note와 날짜 | 규칙 2, documentation-maintenance §5-5 | 채택 |
| R3.5 | report 머리 불릿 11개(Review ID·종류·candidate·base/parent·post-fix·대상 범위·범위 밖·관련 task/요청·Coordinator·시작·종료 시각·상태) | TEMPLATE | 채택(TEMPLATE 동일) |
| R3.6 | 상태 어휘: `IN_REVIEW`(TEMPLATE 초기값), `COMPLETE`, `POST_FIX_REVIEW`(미추적 report), `**PASS**`(post-fix report) — 정본에 열거된 집합은 없음(사실) | 4개 report 머리 | 열린 질문 Q5 |
| R3.7 | finding ID는 `{A|B}-P{0-3}-{NN}`; finding 표 6열(ID·심각도·근거·위치·재현·실패 형태·영향·권고) | TEMPLATE §2–3 | 채택 |
| R3.8 | 심각도 P0(즉시 BLOCK)·P1(BLOCK)·P2(수정 권고·조건부 연기)·P3(수정 또는 추적) | agent-workflow §5.3 표 | agent-workflow 없음 |
| R3.9 | disposition은 `OPEN`/`FIXED`/`REJECTED_WITH_EVIDENCE`/`DEFERRED`; `DEFERRED`는 P2/P3만이며 owner·상세 task·gate·기한 필수 | §5.4 표, TEMPLATE §5 | TEMPLATE에만 |
| R3.10 | P0/P1은 원 reviewer 재확인 전 merge 금지; risk acceptance·"release 차단" 표시는 closure가 아님 | §5.4-4, reviews/README 규칙 7 | reviews/README 채택 |
| R3.11 | verdict는 `BLOCK`/`CONDITIONAL`/`PASS` | §5.3 | — |
| R3.12 | 두 reviewer는 전문 영역이 다르고, 같은 manifest·immutable 기준선(commit object-only 또는 detached worktree)을 쓰며, 원본 확정 전 상대 결과를 보지 않는다 | §5.1, reviews/README 규칙 4 | reviews/README 채택 |
| R3.13 | manifest에는 기준 commit·parent/base·task/요청·범위·범위 밖·관련 architecture·acceptance·실행 가능한 검증; evidence에 reviewer 실행 ID·역할·시작 시각·요청 원문 | §5.1-2·3 | — |
| R3.14 | object-only 명령 4개(`cat-file -e`, `rev-parse`, `diff --find-renames`, `show <commit>:<path>`); detached는 `worktree add --detach` + `rev-parse HEAD` + `status --porcelain=v1`(시작·종료 모두 비어 있어야 함) | §5.1 코드 블록 | — |
| R3.15 | 비면제 8종(architecture·wire/ABI·권한 / 차량 송신·safety / 회로 / 동시성·budget / 신호 승격 / 공용 UI state·넓은 refactor / 작업 정책·품질 gate / AGENTS·SKILL·docs README·ADR·runbook·task/review 규칙); 면제는 오탈자·동의 링크 수정뿐이고 비작성자 승인 필요 | §5 | docs-conventions §3.4는 하드웨어·차량 항목 치환을 제안 |
| R3.16 | closure artifact(원본 보존 + disposition·재검증 + index 1행)는 재귀 리뷰를 시작하지 않으며 규범 문구를 바꾸면 새 기준선 | §5 말미, reviews/README 규칙 9 | 채택 |
| R3.17 | post-fix commit을 두 reviewer가 자신의 finding + 전체 delta 회귀로 재검토하고 verdict를 report·task·PR에 반영 | §5.4-7·8, TEMPLATE §6 | 채택 |
| R3.18 | `reviews/README.md` 표는 `날짜|종류|기준선·범위|리뷰어|결과`이며 최신을 맨 위에 추가 | reviews/README | 채택(빈 표) |

### 3.4 runbook·workflow 규약(`docs/runbooks/*`)

| ID | 검증 가능한 문장 | 근거 | common |
|---|---|---|---|
| R4.1 | runbooks에는 반복 절차만; 설계·일회성 로그 금지. README는 `문서|읽는 시점|책임` 표 | runbooks/README | 채택(행 추가) |
| R4.2 | agent-workflow는 8절: 범위·기준선 / branch·worktree / CodeGraph / 구현·검증 / 2인 리뷰(5.1–5.4) / 기록 갱신 / stage·보안·PR / 정리 | agent-workflow H2 | 없음 |
| R4.3 | 작업 branch 명명 `agent/<agent>-<task>`, `origin/main`에서 분기; main 직접 push 금지 | §2, §7-5 | — |
| R4.4 | 임시 worktree 경로 `<repo>-wt/<agent>-<task>`, 리뷰용 `<repo>-wt/review-<id>`; 같은 branch 이중 checkout 금지; 종료 후 `worktree remove` + `prune` | §2, §8 | — |
| R4.5 | CodeGraph는 설치돼 있을 때만: 최초 `init -i`, 전환·pull·merge 후 `sync`, 전후 `status`; 없으면 `rg`·compiler·test로 대체하고 한계 기록 | §3 | — |
| R4.6 | 검증 사다리 7층(schema → generator·golden·malformed → host test → target compile → ERC/UI static → HIL → bench/vehicle)에서 범위에 맞는 층만 실행; host simulation으로 실물 gate 대체 금지 | §4 | 후보: 문서 → 패키지 빌드·타입 → 단위 → tarball 설치 → 소비자 빌드·e2e → 소비자 배포 스모크 |
| R4.7 | 기록 갱신 6조건(resume / tasks+상세 / ADR+index+decisions / journal 최상단 / CHANGELOG / review report+index) | §6, documentation-maintenance §2 표 | documentation-maintenance 채택 |
| R4.8 | stage는 경로별 명시; `git add .`·`git add -A` 금지; `git status` → `git diff --staged` 전체 읽기 → 비밀 검사 → 생성물·링크·task index 정합 → push·PR | §7 | agent-workflow 없음 |
| R4.9 | PR 본문 6항목(task·목적 / gate·명령 / 리뷰어 2인 영역·report·disposition / 실패·미실행·위험 / evidence·digest / rollback) | §7 | — |
| R4.10 | CI·필수 reviewer gate·미해결 P0/P1 확인 전 merge 금지 | §7 말미 | — |
| R4.11 | failure patterns는 `증상|먼저 확인할 것|복구` 단일 표; 반복 시 새 task로 분리 | agent-failure-patterns | 없음 |
| R4.12 | 문서 이동 7단계(`git mv`, backtick·plain path 검색 `rg -n "old-name\.md|docs/old/path" -g "*.md"`, 서두에 상위 인덱스 명시, 상대 링크 재계산, link 검사 + `git diff --check`, 정본 변경 시 ADR); label도 새 역할로 | documentation-maintenance §6 | 채택 |

### 3.5 journal·resume·CHANGELOG·README·docs 지도

| ID | 검증 가능한 문장 | 근거 | common |
|---|---|---|---|
| R5.1 | journal H1 `# <제품> 작업 일지`; 항목 H2는 `## YYYY-MM-DD (agent[, 주제])`; **newest-first**; 기존 항목은 사실 오류 correction 외 수정 금지 | journal 9항목(모두 `(codex…)`), documentation-maintenance §4 | 없음 |
| R5.2 | journal 항목 본문은 굵은 라벨 불릿(`**작업**`·`**변경**`·`**결정**`·`**검증**`·`**환경**`·`**적대적 리뷰**`·`**발견**`·`**다음**` 등, 고정 집합 없음) 또는 산문 + "작성자 실제 검증" 표(`명령/환경|결과`) | journal 본문 | 후보: geo/map 5필드(docs-conventions §3.2)와 병합 |
| R5.3 | journal에는 도구 fallback·미실행 검증·사용자 변경 보존 여부를 남긴다 | documentation-maintenance §4 | 채택(+소비 저장소 상태) |
| R5.4 | resume는 5절(현재 진척도 / 다음 한 작업 / 현재 열린 핵심 경로 / 알려진 차단 조건 / 문서 정본)이며 "다음 한 작업"에 시작 문서·확인 대상·완료 조건 3불릿 | resume.md | 없음 |
| R5.5 | CHANGELOG는 `## [Unreleased]` 아래 `### Added`/`### Changed`(Keep a Changelog 계열), 사용자 가시 변경만, 한글. 항목 순서 규칙은 문서화되어 있지 않음(미확인) | CHANGELOG, documentation-maintenance §1 | 없음 |
| R5.6 | 루트 README "문서" 절은 문서 지도 + 아키텍처·resume·tasks·decisions·reviews·agent-workflow 링크 6개 | README §문서 | 없음 |
| R5.7 | `docs/README.md`는 읽기 단계 표(반드시/필요 시/특수) → 정본 관계 트리(`AGENTS.md └─ docs/README.md ├─ …`) → 분야별 표 → 작업·운영·이력 표(읽는 시점 열 포함) → 탐색 규칙 5 | docs/README | 없음 |
| R5.8 | 정본 관계 5문장: architecture=현재 설계 / ADR=이유(뒤집어도 삭제 없음) / task=원자 범위·acceptance(architecture 재정의 금지) / review=특정 commit의 역사(현재 정본으로 사용 금지) / runbook=방법만 | docs/README "정본 관계" | 없음 |
| R5.9 | 하위 디렉터리 README(architecture·runbooks·reviews·tasks·adr)는 서두 1단락에서 상위 인덱스와 자기 책임을 밝힌다 | 각 README 서두, documentation-maintenance §6-4 | runbooks·reviews·tasks 채택 |

### 3.6 언어·링크·Git·파일 규약

| ID | 검증 가능한 문장 | 근거 | 검사 | common |
|---|---|---|---|---|
| R6.1 | Markdown 본문은 한글; 공식 필드명·코드 식별자·명령어·URL·제공자 원문은 영어 유지 | AGENTS §4, documentation-maintenance §7 | 수동 | 채택(+패키지명) |
| R6.2 | 문서 내 링크는 상대 경로; 검사 도구는 절대 접두 2종(`/mnt/f/dev/<repo>/`, `F:/dev/<repo>/`)을 저장소 상대로 해석하고 `:NN` 줄 번호 접미를 제거 | validate_document_links | 자동 | 접두 유지(C11과 불일치, Q2) |
| R6.3 | fenced code block 안의 링크·metadata는 검사 대상이 아니다 | 두 validator | 자동 | 채택 |
| R6.4 | 이동·이름 변경 후 모든 local link와 plain path reference를 검사한다 | docs/README 탐색 규칙 5 | 반자동 | 채택 |
| R6.5 | 사실·후보·추정·미검증을 구분해 표기 | AGENTS §2-6, documentation-maintenance §7 | 수동 | 채택(+조사 커밋 명시) |
| R6.6 | 외부 원문은 공식 URL + version/commit/revision | AGENTS §7, documentation-maintenance §7 | 수동 | 채택 |
| R6.7 | `.gitignore`에 `.vscode/ .claude/ .codegraph/ .env .env.* !.env.example *.local.md` | .gitignore | — | 유지 |
| R6.8 | `.gitattributes`로 텍스트 개행 LF 고정, 바이너리 명시 | .gitattributes(hardware 한정) | — | 전역화 |
| R6.9 | 로컬 부산물은 gitignore된 `.tools/`에만 생성(리뷰 probe 등) | .gitignore, 미추적 probes 문서 | — | 없음(후보) |
| R6.10 | Windows 경로 `F:/…`와 WSL `/mnt/f/…`가 문서에 공존할 때 Windows checkout을 정본으로 삼는다 | failure patterns 13행, ADR-003 | — | Q4 |

## 4. validate_plan.py가 요구하는 문법 명세

### 4.1 상세 task·요약 문법(정규식 수준, canview·common 동일)

| 항목 | 정확한 규칙(사실, `tools/validate_plan.py` 라인) |
|---|---|
| 대상 파일 | `docs/tasks/T-*.md`를 `glob`으로 수집·정렬(L79). 0개면 `docs/tasks: 상세 task 파일이 없음`(L81). 파일 수 `file_count`는 이 glob 개수(L171)로, 파일명이 잘못돼도 개수에 포함된다 |
| ID | `ID_PATTERN = r"T-\d{3}[a-z]?"` (L17). `fullmatch`로만 비교하므로 `T-22a`, `T-0001`, `T-001A`는 오류 |
| 파일명 | `FILE_RE = (T-\d{3}[a-z]?)-[A-Za-z0-9][A-Za-z0-9_.-]*\.md`를 파일명 전체에 `fullmatch`(L19, L83). slug 첫 글자는 영숫자, 이후 `_ . -` 허용, 한글 불가. 실패 시 `파일명/ID 문법 오류` |
| 인코딩·fence | `utf-8-sig`로 읽고(L48) 실패 시 `읽기 실패`. 이후 `^`{3,}[^\n]*\n.*?^`{3,}\s*$`(MULTILINE·DOTALL)로 **줄 첫 칸에서 시작하는** fenced block을 제거(L53). 들여쓴 fence는 제거되지 않는다(추정: 정규식 `^` 앵커 때문) |
| H1 | fence 제거 후 `^# .+$`가 **정확히 1줄**(L89–90). 그 줄은 `# (T-\d{3}[a-z]?) (\S.*)`에 `fullmatch`하고 ID가 파일명 ID와 같아야 한다(L20, L91). 제목 = 두 번째 그룹(공백 뒤 첫 글자가 비공백). 실패 시 `상세 제목 ID/파일명 불일치 또는 H1 개수 오류` |
| scalar 필드 | `^- {field}: (.*)$`(MULTILINE)가 **정확히 1회** 매치하고 값이 공백이 아니어야 한다(L58–60). 값은 `strip()` 후 양끝 backtick을 `strip("`")`(L62). 필드명은 `상태`, `우선순위`, `Gate`, `선행`(L96–99). 앞 공백·`*` 불릿·`- 상태 :`(콜론 앞 공백)은 매치 실패 → `{field} 필드는 정확히 1개 필요` |
| 상태 | `STATUSES = {"READY","BLOCKED","IN_PROGRESS","DONE"}`(L21), 아니면 `알 수 없는 상태 '…'` |
| 우선순위 | `PRIORITIES = {"P0","P1","P2","P3"}`(L22), 아니면 `알 수 없는 우선순위` |
| Gate | 비어 있지 않은 아무 문자열(L98). 어휘 검사 없음(사실). canview 관행: `G0`, `G1 제작 전`; common tasks-rule §5 예: `문서 검증`, `패키지 빌드·tarball 설치` |
| 선행 | 값이 정확히 `없음`이면 빈 목록(L66). 아니면 `,`로 나눠 각 토큰 `strip()`·backtick 제거 후 모두 `ID_RE.fullmatch`(L68–69); 실패 시 `선행 문법 오류 (ID 목록 또는 없음; 외부 조건은 외부 선행)`. 중복 토큰은 `중복 선행`(L72). 따라서 `T-001, 실물 PCB`는 오류, `없음, T-001`도 오류 |
| 외부 선행·병렬 가능 | 파서가 읽지 않는다(사실). `- 외부 선행: …`, `- 병렬 가능: …` 줄은 자유 형식 |
| 중복 ID | 같은 ID의 상세 파일 2개 → `중복 상세 ID`(L105) |
| 요약 파일 | `docs/tasks.md`와 `docs/tasks-done.md` 둘 다 필수(L167–169, 없으면 `읽기 실패`). fence 제거 후 `|`로 시작하는 줄만 본다(L114). `strip("|")` 후 `|`로 split, 각 열 `strip()`·backtick 제거(L116). 첫 열이 `[`로 시작하지 않으면 건너뜀(헤더·구분선 통과, L117) |
| 요약 행 | 첫 열은 `\[([^\]]+)\]\(([^)]+)\)` fullmatch, 링크 텍스트는 ID fullmatch, **열 수 정확히 5**(L119–121). 열 순서 `[0]`=링크 `[1]`=상태 `[2]`=우선순위 `[3]`=제목 `[4]`=선행. 실패 시 `task 요약 5열/ID/link 문법 오류`. 제목에 `|`가 있으면 열 수가 어긋난다(추정) |
| 개수 문구 | `docs/tasks.md`에서 `(\d+)개의 상세 작업`이 **정확히 1회**이고 값이 `file_count`와 같아야 한다(L170–173), 아니면 `상세 task 수 불일치 (실제 N)`. `tasks-done.md`는 검사하지 않음 |
| 요약↔상세 대조 | S1 요약 ID 중복 → `중복 요약 ID`. S2 상세 없음 → `상세 파일 없는 요약`. S3 위치: 상세 상태 `DONE`이면 `tasks-done.md`, 아니면 `tasks.md`에 있어야 함 → `상태에 맞지 않는 요약/archive 위치`(L185–187). S4 링크 target을 요약 파일 기준 상대 경로로 `unquote`·`resolve`해 상세 경로와 동일해야 함 → `상세 link 불일치`(L188–190). S5 제목·상태·우선순위는 문자열 완전 일치, 선행은 **집합** 비교(순서 무관) → `요약 {필드} 불일치`(L191–199). S6 요약 없는 상세 → `요약 누락`(L200–201) |
| 그래프 | 자기 선행 → `자기 선행`; 없는 ID → `없는 선행`; `READY`/`DONE`인데 선행이 `DONE`이 아니면 `{상태}인데 선행 {ID} 미완료`(L132–138). Kahn 위상정렬로 사이클 검출 → `선행 DAG 사이클 (연결된 차단 task 포함): …`(L141–159) |
| 출력·종료 | 오류 줄 출력 후 `상세 task={N}, 오류={E}; 읽기 전용 metadata/DAG 검사 (제품 gate 아님)`; 오류 있으면 exit 1(L206–214). `--root` 기본값은 스크립트 상위 디렉터리 |
| 검사하지 않는 것(사실) | 상세 파일의 9항목 절 존재, Gate 어휘, `외부 선행` 문법, 요약 표의 그룹 소제목·정렬 기호, 체크박스 원장(`- [ ] **T-NNN**`), slug와 제목의 대응, `docs/tasks-done.md`의 날짜·결과 열(5열 고정이므로 날짜 열을 추가하면 오류) |

최소 유효 예(`tests/test_plan_validation.py` L44–48의 fixture와 동일 형식):

```text
# T-001 기반

- 상태: `READY`
- 우선순위: `P0`
- Gate: `G0`
- 선행: 없음
```

```text
| ID | 상태 | 우선순위 | 작업 | 선행 |
|---|---|---|---|---|
| [T-001](tasks/T-001-fixture.md) | READY | P0 | 기반 | 없음 |
```

### 4.2 tests/test_plan_validation.py가 고정하는 계약(35 tests)

테스트는 오류 메시지 **부분 문자열**을 단언하므로 아래 문자열이 사실상 계약이다: `중복 상세 ID`, `파일명/ID`, `상세 제목 ID/파일명`, `H1 개수`, `{필드} 필드`(상태·우선순위·Gate·선행 각각), `알 수 없는 상태`, `알 수 없는 우선순위`, `없는 선행`, `중복 선행`, `선행 문법`, `자기 선행`, `DAG 사이클`, `READY인데 선행`, `DONE인데 선행`, `상세 task 수 불일치`, `요약 {필드} 불일치`(제목·상태·우선순위·선행), `요약 누락`, `중복 요약 ID`, `상세 파일 없는 요약`, `상세 link 불일치`, `요약 5열`, `요약/archive 위치`, `읽기 실패`, `파일이 없음`. 긍정 계약: 하위 ID `T-002a` 허용, `외부 선행` 줄 허용, fence 안 예시 무시, 선행 순서 차이 허용, DONE 상세를 archive에 두면 통과, 성공·실패 모두 파일 해시 불변(읽기 전용), CLI 종료 코드 0/1과 출력 `상세 task=3, 오류=0`. 테스트는 `python -B` subprocess로 CLI를 호출하고 `tempfile`만 사용한다.

### 4.3 validate_document_links.py 명세

| 항목 | canview(사실) | common 변형 |
|---|---|---|
| 대상 | `docs/**/*.md` + `hardware/**/*.md` + 루트 `*.md` + `tools/README.md` | `docs/**` + `packages/**` + `tools/**` + 루트, `node_modules` 제외 |
| fence 제거 | `'```.*?```'`(DOTALL, 앵커 없음) — validate_plan과 정규식이 다르며 인라인 삼중 backtick도 제거 범위에 들어간다 | 동일 |
| 링크 추출 | `!?\[[^\]\n]*\]\(([^)\n]+)\)`; target `strip()`·`<>` 제거 | 동일. 대괄호 바로 뒤에 소괄호가 오는 일반 문장을 링크로 오인(common 오탐 1건) |
| 절대 접두 | `/mnt/f/dev/canview/`, `F:/dev/canview/` → 저장소 상대로 변환, `:NN` 접미 제거 | 접두만 `kor-travel-common`으로 치환 |
| 제외 | scheme 있음(`http:` 등), path 비어 있음(`#fragment`만), `//`로 시작 | 동일 |
| 검사 | `urlsplit(...).path`만 `unquote`해 존재 확인 — **fragment(`#절-제목`)는 검증하지 않는다** | 동일 |
| 출력 | `Checked N documents, M local targets; errors=E` + 실패 목록; exit 1 | 동일 |

## 5. 열린 질문

- Q1. `docs/decisions.md`를 둘지: canview는 `adr/README.md`와 이중 색인(다음 번호는 decisions.md 최댓값 기준). docs-conventions §4는 불필요, common의 `documentation-maintenance.md` §2·§3은 필수 갱신 대상으로 적어 서로 충돌한다. 하나로 정해야 `agent-workflow.md` §6과 ADR 규칙 R2.7을 쓸 수 있다.
- Q2. `validate_document_links.py`의 절대 접두 허용: common 사본은 접두를 유지·치환했지만 docs-conventions C11은 제거를 제안한다. 유지하면 다른 체크아웃 경로에서 깨지는 링크를 허용하게 된다.
- Q3. task 원장 형식: docs-conventions §3.3은 체크박스 원장 + `validate_task_ledger.py`(후보)를, common의 `tasks-rule.md` §4와 무변경 `validate_plan.py`는 5열 표를 요구한다. validator를 바꾸지 않는 한 5열 표가 사실상 확정이며 docs-conventions §3.3-3·4·7은 갱신이 필요하다.
- Q4. common 자체 정본 OS·경로 표기(`F:/dev/…` vs `/mnt/f/dev/…`)와 `docs/dev-environment.md` 작성 시점. `agent-workflow.md` §2·§5.1의 PowerShell 명령을 bash로 옮길지, 두 벌 둘지.
- Q5. review 상태 어휘(`IN_REVIEW`·`COMPLETE`·`POST_FIX_REVIEW`·`PASS`)와 post-fix 명명(`-post-fix` 별도 report vs `-02` suffix vs `-postfix-reviewer` 표기)이 canview에서도 정본화되지 않았다. common TEMPLATE·README에 집합을 명시할지.
- Q6. common `.py` 사본의 CRLF: `.gitattributes`가 LF를 선언하므로 add 시 정규화될 것으로 추정하나, 첫 커밋에서 확인해야 한다.
- Q7. `docs/runbooks/README.md`가 가리키는 `consumer-adoption.md`·`release.md`는 canview에 없는 신규 runbook이다. 작성 전까지 링크 검사 17건 중 대부분이 실패하므로 docs.yml 활성화 순서를 정해야 한다.
- Q8. `tools/toolchain-versions.json` 형식(`schemaVersion`·`checkedAt`·`gitCommit` pin)을 "라이브러리/플랫폼 버전 일치" 정책의 machine-readable 정본으로 채택할지, 이름·경로(docs-conventions §4 `versions.json` 후보)와 대조 스크립트 소유 task를 누가 갖는지.
- Q9. `AGENTS.md` §6의 추상화 재사용 항목(A6.1·A6.4·A6.9·A6.13·A6.15)을 공통 절 F에 넣을지 `SKILL.md` §4 로컬 DO NOT으로 둘지(docs-conventions C4·Q2와 연동).

## 근거 파일 목록

canview `1f93b8a`(저장소 상대 경로; ★는 작업 트리 미추적):

1. `AGENTS.md`
2. `SKILL.md`
3. `README.md`
4. `CHANGELOG.md`
5. `.gitignore`
6. `.gitattributes`
7. `tokens.css`
8. `docs/README.md`
9. `docs/resume.md`
10. `docs/journal.md`
11. `docs/tasks.md`
12. `docs/tasks-rule.md`
13. `docs/tasks-done.md`
14. `docs/tasks/README.md`
15. `docs/tasks/T-001-host-toolchain-ci.md`
16. `docs/tasks/T-100a-pcb-production-design.md`
17. `docs/adr/README.md`
18. `docs/adr/001-canview-safety-boundary.md`
19. `docs/adr/002-documentation-and-task-structure.md`
20. `docs/adr/003-windows-development-and-ephemeral-worktrees.md`
21. `docs/adr/004-layered-documentation-and-review-archive.md`
22. `docs/adr/005-latest-windows-embedded-toolchain.md`, `006-compact-hardware-power-and-sensors.md`, `007-n16r8-independent-recoverable-ota.md`(머리 부분)
23. `docs/decisions.md`
24. `docs/runbooks/README.md`
25. `docs/runbooks/agent-workflow.md`
26. `docs/runbooks/documentation-maintenance.md`
27. `docs/runbooks/agent-failure-patterns.md`
28. `docs/reviews/README.md`
29. `docs/reviews/adversarial/TEMPLATE.md`
30. `docs/reviews/adversarial/2026-09-05-document-information-architecture.md`
31. `docs/reviews/adversarial/2026-09-05-latest-toolchain-bootstrap-post-fix.md`(머리)
32. ★ `docs/reviews/adversarial/2026-09-06-plan-ui.md`(머리)
33. `docs/reviews/adversarial/evidence/2026-09-05-document-information-architecture-post-fix-reviewer-a.md`
34. `docs/reviews/adversarial/evidence/2026-09-05-r1-hardware-navigation-manifest.md`
35. ★ `docs/reviews/adversarial/evidence/2026-09-06-plan-ui-reviewer-a.md`, ★ `…-plan-ui-probes.md`(머리)
36. `docs/architecture/README.md`
37. `docs/architecture/requirements-coverage.md`(§1–§2 머리), `implementation-readiness.md`(목차)
38. `docs/development/windows.md`, `docs/development/toolchains.md`(목차)
39. `docs/ui/design.md`(§1–§5)
40. `tools/README.md`
41. `tools/toolchain-versions.json`
42. `tools/validate_document_links.py`
43. `tools/validate_plan.py`
44. `tests/test_plan_validation.py`
45. `git ls-files` 전체 목록(디렉터리별 개수: docs 134, hardware 210, firmware 31, tools 24, ui 12, tests 10, dbc 5, protocol 2)

kor-travel-common `b92fabe` 작업 트리:

46. `.editorconfig`, `.gitattributes`, `.gitignore`, `.github/workflows/docs.yml`
47. `docs/tasks-rule.md`, `docs/tasks-done.md`, `docs/tasks/README.md`
48. `docs/runbooks/README.md`, `docs/runbooks/documentation-maintenance.md`
49. `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`, `docs/reviews/adversarial/evidence/.gitkeep`
50. `tools/README.md`, `tools/validate_document_links.py`, `tools/validate_plan.py`, `tests/test_plan_validation.py`
51. `docs/survey/cross/docs-conventions.md` §1.6–1.9, §1.19, §2, §3, §4, §5

기타:

52. `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(canview 언급 없음 확인)
