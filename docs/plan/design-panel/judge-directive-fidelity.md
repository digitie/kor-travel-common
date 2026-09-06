# 판정 보고서 — 사용자 지시·canview 충실도·GPL (directive-fidelity)

- 작성일: 2026-09-06 · 판정자 관점: 사용자 지시 (1)~(7)의 완전 충족 여부, canview 구조·AGENTS.md 채택 여부(`cross/canview-structure-checklist.md` 대조), GPL-3·`licensing.md` 조치 반영, "코드+규칙" 네 축(색상 톤·UX·OpenAPI·PC/Mobile Web) 완전성, 버전 일치 정책의 검증 가능성.
- 입력: coordinator 초안(D-01~D-18, F절), risk-first(D-01~D-27, E·F·G·H절), velocity-first(D-01~D-24, F·G·H절), `docs/survey/README.md`·`commonality-matrix.md`·`cross/*.md` 10편·`inventory/*.md` 7편(§1·§8·§9·§11), `docs/tasks-rule.md`, `docs/runbooks/documentation-maintenance.md`, `docs/reviews/README.md`, `tools/validate_plan.py`, 선행 보고서(geo `docs/kor-travel-common-library-review.md`).
- 이 판정에서 직접 실측한 것(읽기 전용, 2026-09-06): (a) common 작업 트리 `git rev-parse` = `b92fabe`, 추적 파일 1개(`LICENSE`), scaffold 전부 미추적, `tools/validate_plan.py`·`tests/test_plan_validation.py`는 여전히 CRLF(`file` 출력) — risk-first 머리와 `cv` §1.2 서술 일치. (b) `curl` PyPI `kor-travel-common` → 404, `kortravelcommon` → 404(미점유 확인). (c) npm `@kor-travel/tokens` → 404(미발행), `www.npmjs.com/org/kor-travel` → 403, `-/user/org.couchdb.user:kor-travel` → 401 — **scope 소유 여부는 여전히 미확인**.
- 표기: **사실** = 조사 문서·파일에서 확인 / **후보** = 이 판정의 권고 / **추정** = 정황 / **열림** = 사용자 확인 필요(§11). 근거 약칭은 `commonality-matrix.md` 머리 규약(`vm`·`dt`·`ui`·`ux`·`be`·`oa`·`ci`·`dc`·`cv`·`lic`·`cm`·`inv/<app>`·`prior`).
- 심각도: P0 = 틀리면 법적·불가역·전 소비자 차단 / P1 = 사용자 지시 완화·축소 또는 핵심 아키텍처 오류 / P2 = 절차·gate·문서 결함 / P3 = 명명·세부.

## 1. 채점

| 레지스터 | 점수 | 강점 | 약점 |
|---|---:|---|---|
| coordinator | 55 | 배포 단위 8종을 한 표에 펼쳐 산출물 지도가 가장 넓다. 규칙 문서 9종(`docs/standards/*`)을 명시해 지시 (4)의 네 축을 전부 이름 붙였다. F절이 인벤토리에서 확인된 사실(airport Admin 실체, map 잠금 테스트, 헤더 형식 규칙)을 결정에 반영했다 | 조사 3편을 "작성 중"으로 둔 채 결정해 D-17·D-18이 결론 대기 상태(§10 E5). 기준선 표가 단일 정확값이라 map exact 핀·3.11 floor 3곳·npm 동봉 버전(10.9.8)과 충돌(E1·E4·E6). D-16이 `lic` B1(pinvi 추출 금지)·L6를 무시하고 pinvi admin을 Phase 1에 둔다(E13). task 목록이 없어 지시 (7)을 충족하지 못한다. `decisions.md` 유지 근거로 `dc` §4를 인용하나 §4는 "불필요"라고 적었다(E15) |
| risk-first | 86 | 지시 (1)~(7)을 "후퇴 없이" 달성하는 순서를 실패 시나리오→결정→소비자 영향으로 잠갔다. D-08의 대상별 4단 PR·중단 조건·weather preflight 제외 단계, D-07의 판정 코드 8종·report→fail 승격 조건, D-17의 `lic` L1~L16·B1~B10 완전 반영, D-25 NOT_RUN(cv R1.12·R1.13)까지 canview 규약을 가장 깊게 옮겼다. 79 task가 `tasks-rule` 대역에 맞는다 | pinvi admin을 Phase 4 T-420 뒤로 미뤄 지시 (3)의 "포함"이 계획상 3단계 뒤로 밀린다(L6가 1 PR 규모 사용자 결정임에도 Phase 0 외부 확인으로 승격하지 않음). npm floor 11.19를 두면서 동봉 10.9를 사실로 적어 4 CI가 첫날 `BELOW_FLOOR`(E3). 소비자 채택 상태의 기계 판독 위치(매니페스트)가 없고, `bg-surface-page` 공통 이름은 pinvi 사용자 표면 충돌 위험(`dt` §3.1.1)을 `base.scoped.css`만으로 막는다 |
| velocity-first | 74 | 소비자 매니페스트(D-19)·registry drift·`kt-` 유틸리티 네임스페이스(D-10)·이관 PR 규격(D-23)·회수 측정(D-24)은 세 안 중 가장 실행 가능한 도구 설계다. 첫 릴리스 PR·파일 수를 추정으로 표기해 검증 가능하게 했다. 80 task | 지시 (2)를 완화한다: fail 전환을 "앱이 매니페스트에서 선언"으로 두어 정렬이 영구 report로 남을 수 있다(D-07·D-20, P1). 지시 (4) UX 규칙을 MUST 8개로 얇게 만든다(D-13, P2). registry 복사 소유는 공통화 동기였던 geo 반복 동기화 비용(`prior` §3.2)과 27/27 상이(`ui` §2.1)를 재생산한다. Python 소비 task 7개를 앱 대역에 두어 `tasks-rule` §2.1을 위반(E9). npm 동봉 11.19 오기(E2) |

## 2. 사용자 지시 (1)~(7) 충족 매트릭스

| 지시 | coordinator | risk-first | velocity-first | 최고 충족 | 완화·축소 여부 |
|---|---|---|---|---|---|
| (1) Tailwind v4 전환 | D-08 대상 7곳 서술, 순서·검증 없음 | D-08 순서 6단 + 4단 PR + 중단 조건 + weather preflight 제외 단계 | D-08 순서·규모 추정, weather를 registry 안정 후로 지연 | **risk** | 세 안 모두 pinvi mobile(NativeWind 4=Tailwind 3)을 예외 등록 — 지시 (1)의 유일한 축소, **P1, 사용자 승인 필요**(§11 O8). pinvi 사용자 표면 `@config` v3 preset 유지는 엔진이 v4(4.3.3)이므로 지시 위반 아님(P2 정리 항목) |
| (2) 버전 일치 정책 | D-06 단일 정확 기준선 + D-07 P3 | D-06 floor/recommended/consumer-pin 3열 + D-07 판정 8종·승격 규칙·blocked | D-06 floor/target + D-07 lock 파서·매니페스트, **fail 전환 앱 자율** | **risk** | velocity의 "앱이 enforce 선언"은 일치화를 선택 사항으로 만든다 → **P1 완화**. coordinator의 정확값 강제는 첫날 CI red(`vm` §7.4 "보고 단계가 먼저") |
| (3) airport Admin·PinVi Admin 포함 | D-16 1차 map+pinvi(라이선스 무시), F절 airport 실체 보정 | D-16 pinvi를 L6 뒤 Phase 4, airport WIP 1차; D-20 airport 정의 | D-16 1차 map+pinvi(L6 critical path), D-21 airport 정의 | **velocity**(포함 시점) / **risk**(정의·정확성) | risk는 pinvi를 계획상 뒤로 미룸 — L6가 1 PR 규모 사용자 결정이라 Phase 0 외부 확인으로 승격하면 지시 (3)과 `lic` B1을 동시에 만족(§4 D-16). airport "Admin"은 세 안 모두 백업 패널+`/v1/admin/*`로 해석(사실: `inv/airport` §1-4), 셸·로그인 소비는 T-035 이후 |
| (4) 코드 + 규칙 4축 | `docs/standards/` 9종 이름 | design-tokens·ux-guide·responsive-web·openapi(+exceptions.yaml)·ui-contract·versions·backend-stack·agent-conventions·ci-deploy | 동일 + `standards/README.md`, MUST 8 | **risk** | 네 축 모두 세 안에 있음. velocity MUST-8은 규칙 존재는 유지하되 강제 수준 축소(P2). 색상 톤 축은 세 안 모두 값이 아니라 역할·대비·형태 규칙(사실: `dt` §3.3 "색상톤은 유지" 5앱 선언) |
| (5) canview 구조·AGENTS.md | D-02 한 줄, `decisions.md` 유지 | D-02~D-05·D-25·D-27, `cv` R1.12/R1.13/Q1/Q2/Q5/Q6 반영 | D-02~D-05, `cv` §1.3·Q1·Q3 반영 | **risk** | 세 안 모두 `cv` §2 AGENTS 절별(A1.1~A8.5)·§3 규약(R1~R6) **항목별 채택/변형/제외 대조표**를 산출물로 두지 않음 → §9 M-05 누락 |
| (6) GPL-3 | D-17 결론 대기(stale) | D-17 L1~L16·B1~B10, SPDX 헤더·PROVENANCE·LICENSES/·check_spdx·cva Apache | D-17 동일 + drift 정규화·MIT 저장소 결합 규칙 | **risk** | coordinator는 cva·pg-aiguide Apache-2.0 누락(E8). 세 안 모두 pg-aiguide 스킬 배포 여부(`lic` Q7)·패키지 tarball LICENSE 동봉(`lic` §3.3 마지막 행) 미결정 → §9 M-03 |
| (7) 바로 이어갈 구체성 | Phase 표만, task 없음 | 79 task(ID·선행·gate·대상), critical path | 80 task, critical path, PR 규격 | **risk ≈ velocity** | coordinator 미충족(P1). velocity는 대역 위반 정정 필요(E9) |

## 3. canview 체크리스트 대조(`cv` §1~§4)

| cv 항목 | coordinator | risk-first | velocity-first | 판정 |
|---|---|---|---|---|
| §1.1 필수 파일(AGENTS·SKILL·README·CHANGELOG·docs/README·resume·journal·tasks 3종·adr/README·architecture/README·runbooks 4·reviews 3·validator 2) | D-02 "계층형 채택" 한 줄 | T-001·T-002·T-007·T-008에 파일명 열거 | T-001·T-009·T-010에 열거(+`resume.md`·`journal.md`) | risk·velocity 충족. **누락**: `CHANGELOG.md` 형식(R5.5 Keep a Changelog, `[Unreleased]`)을 T-001 acceptance에 넣은 안 없음 |
| §1.1 F19 `decisions.md` | 유지(canview 동일) | 미보유, `adr/README.md` 단일 색인, runbook 문구 정정 T-002 | 동일 | risk·velocity. 단 R2.7 "다음 후보 번호" 문장은 `adr/README.md`로 이전해야 규칙 보존(§4 D-02) |
| §1.1 F22·F23 readiness·coverage 변형 | `docs/integration-map.md` | `docs/architecture/adoption-readiness.md` + integration-map | integration-map + 매니페스트 | 병합: 매니페스트(앱) → integration-map(common, 생성) → adoption-readiness(gate 표) |
| §1.1 F40 `toolchain-versions.json` 변형 | `versions.json` + `check_versions.py` | 동일 + 스키마 예시 | 동일 + 스키마 예시 | 세 안 충족(`cv` Q8) |
| §1.2 `.py` CRLF(Q6) | 없음 | D-03 첫 커밋 확인, T-002 | D-03, T-003 | risk·velocity. 실측: 두 `.py`가 여전히 CRLF |
| §1.3 `docs.yml` 링크 17건 red(Q7) | 없음 | T-002 해소 | D-02 "필수 체크로 두지 않음" + T-003 | 병합: T-002에서 해소하고 그 전까지 required 아님 |
| §2 AGENTS 절별(A1~A8) | "공통 AGENTS 절" | 공통 절 A~I + 로컬 경계 절, A2.5·R1.13 NOT_RUN 채택 | 공통 절 A~I 원문 + `templates/AGENTS-common-section.md` | `dc` §3.1 A~I는 canview §2·§3·§4·§6·§8을 흡수하나, §6 추상화 재사용 5항(A6.1·A6.4·A6.9·A6.13·A6.15, `cv` Q9)과 §7 외부 원문(A7.1·A7.4) 채택 여부는 어느 안도 미결 → §9 M-05 |
| §3.1 task 규약 R1.1~R1.18 | D-05 5열 표 | D-05 무변경 + R1.12·R1.13 후보 이식(D-25) | D-05 무변경 | risk. R1.14(PR 본문 6항목)·R1.17(`docs/tasks.md` §2 검사 명령 3개 문장)은 T-001 acceptance에 명시 필요 |
| §3.2 ADR R2.1~R2.10 | — | T-004 ADR-001~006, README 단일 색인 | T-002 ADR-001~006 | 병합. R2.4 상태 어휘·R2.5 절 골격을 `adr/README.md` 규칙에 명문화 |
| §3.3 review R3.1~R3.18 | D-04 full gate | D-04 비면제 목록·상태 어휘·post-fix 명명(Q5) | D-04 full/light, 소비자 미부과 | risk. R3.14 object-only 명령 4개·detached worktree는 `agent-workflow.md` §5에 원문 이식 필요 |
| §3.4 runbook R4.1~R4.12 | — | T-007 4종 | T-009 4종 + `templates/consumer-pr.md` | R4.6 검증 사다리 변형(문서→패키지 빌드→단위→tarball→소비자 빌드·e2e→배포 스모크)은 두 안 모두 문장으로만 — `agent-workflow.md` §4 정본으로 명시 |
| §3.5 journal·resume·README R5.1~R5.9 | — | 파일명만 | 파일명만 | R5.4 resume 5절·R5.7 docs/README 3단계 표·정본 관계 트리·R5.8 정본 5문장은 어느 안도 acceptance에 없음 → §9 M-05 |
| §3.6 링크·Git R6.1~R6.10 | — | D-27 상대 링크만, 절대 접두 오류 | D-03 | R6.10(경로 공존 시 Windows 정본)은 common에서 뒤집힘(Linux/WSL 정본) — ADR에 명시 |
| §4 validator 문법 | ID 대역만 | 상태·선행 규칙 인지 | 동일 + "원장 80 초과 금지" | 세 안 모두 `validate_plan.py` 무변경. `tasks-done.md` 5열 고정(날짜 열 금지)을 아는 안 없음 → runbook에 "완료 날짜는 4열 제목 뒤 괄호"로 규정 |

## 4. D-ID별 대조와 최종 권고

형식: 세 안 요약 → **승자** → 최종 권고 문안 → 근거 → 틀렸을 때 심각도.

### D-01 배포 단위
- coordinator 5패키지(tokens·ui·config·api-client-core·py) + standards + templates + versions.json. risk 3단위(tokens·ui·py), config·api-client-core 미생성, lucide 비의존, scope gate. velocity tokens + registry + rules/tools, ui npm 보류.
- **승자: merged(risk 골격)**. 권고: 배포 단위는 `packages/tokens`(npm, React 무관)·`packages/ui`(npm, React 19 전용)·`packages/py/kor-travel-common`(extras `api/db/dagster/testing/http`) 3종 + `docs/standards/*` 9종 + `templates/` + `versions.json`/`tools/*.py`. `config` npm은 만들지 않고 `templates/eslint/*.mjs` 조각 + `frontend-stack.md`로, `api-client-core`는 Phase 5 재평가(`cm` §2.3 `ApiError` 4형). lucide는 peer가 아니라 인라인 SVG. package `name`은 `@kor-travel/<pkg>` 잠정, T-006 scope 확인 실패 시 `@digitie/kor-travel-<pkg>`(개명 비용은 첫 소비자 PR 전이면 0).
- 근거: `prior` §7.1, `ui` §4.1~4.3·§6.2, `be` §3, `vm` §1.3(lucide 0.363~1.41), `inv/map` §3.1(ESLint effective-config 잠금).
- 심각도: P1(패키지 경계는 소비자 `package.json` 계약).

### D-02 저장소 구조(canview 대응)
- coordinator canview 계층 + `decisions.md` 유지. risk `adr/README.md` 단일 색인 + validator 절대 접두 제거 + adoption-readiness. velocity 동일 + tools 5종.
- **승자: merged(risk)**. 권고: canview 계층(AGENTS → docs/README → resume → 지정 task)과 `docs/{adr,architecture,runbooks,reviews,tasks}` + validator 2종을 채택하고 하드웨어·차량 항목 제외. `docs/decisions.md`는 두지 않되 canview R2.7의 "다음 후보 번호는 ADR-NNN" 문장을 `docs/adr/README.md` 상단에 둔다. `documentation-maintenance.md` §2·§3의 `decisions.md` 문구는 T-002에서 정정하고 ADR-001에 canview와의 차이 사유(`dc` §4)를 기록. 추가: `CLAUDE.md`(≤40줄), `docs/standards/`, `docs/survey/`(규범 아님), `docs/plan/`, `docs/dev-environment.md`, `docs/integration-map.md`, `docs/architecture/adoption-readiness.md`, `packages/`, `templates/`, `versions.json`. **T-001 acceptance에 `cv` §1~§3 항목별 채택/변형/제외 대조표(`docs/architecture/canview-checklist.md`)를 포함**(§9 M-05).
- 근거: `cv` §1.1 F19·Q1, `dc` §4, `cv` §5 Q2.
- 심각도: P2.

### D-03 개발 환경 정본
- 세 안 일치(Linux/WSL 정본, CI ubuntu). risk `.gitattributes`·CRLF 확인·`ubuntu-24.04`. velocity 도구 Python stdlib로 Windows 동작.
- **승자: merged**. 권고: common 정본 = Linux/WSL bash, CI `ubuntu-24.04` 고정, 임시 worktree 프로필(ADR-003 방식). 공통 절은 OS 미규정(`dc` C1·C2). 검사 도구 3종(`check_versions`·`kt_contrast`·`ux_lint`)은 Python 3.11 stdlib만 사용하고 **Windows에서 동작을 CI 매트릭스(`windows-latest`)로 보증**(§9 M-04, 현재 사용자 환경이 Windows). 첫 커밋에서 `.py` LF 정규화 확인(실측: 현재 CRLF).
- 근거: `dc` §1.11·§2 C1·C2·C12, `cv` Q4·Q6, 실측.
- 심각도: P2.

### D-04 리뷰 gate
- coordinator common full + 소비자 full/light. risk 비면제 목록 + merge 담당 판정 + 상태 어휘. velocity 소비자 미부과.
- **승자: risk**(소비자 부과 수준은 velocity 절충). 권고: common 자체는 canview full gate를 비면제 목록(`docs/standards/*`, `versions.json`, `packages/*` 공개 API·CSS, `.github/workflows/*`, AGENTS/SKILL/ADR/runbook/task·review 규칙)에 적용. 판정 주체는 merge 담당(작성자 ≠ 판정자). 상태 어휘(`IN_REVIEW/COMPLETE/POST_FIX_REVIEW`, verdict `BLOCK/CONDITIONAL/PASS`, post-fix는 `-post-fix` report)를 TEMPLATE·README에 명시. 소비자에게는 full/light 표준과 TEMPLATE을 **배포하되 채택은 SHOULD**(리뷰 절차 신설 PR을 이관 선행조건으로 두지 않음).
- 근거: `dc` §1.5·C7·Q4, `cv` R3.1~R3.18·Q5.
- 심각도: P2.

### D-05 task 원장
- 세 안 일치(5열 표 + `validate_plan.py` 무변경).
- **승자: risk**. 권고: common은 `tasks-rule.md` 현행. 소비자 표준은 체크박스 원장 허용 + 상태 대응표 + "요약에 acceptance 복제 금지·비단순은 상세 파일"만 배포(`validate_task_ledger.py`는 Phase 5 opt-in). `docs/tasks-done.md`는 5열 고정이므로 완료 날짜는 제목 열 괄호로.
- 근거: `cv` §4.1·Q3, `dc` §1.7(map 평면화 사고).
- 심각도: P3.

### D-06 정렬 기준선
- coordinator 단일 정확값(Node 22 + npm "동봉 11.19", TS 5.9, Python ≥3.12, Actions v7). risk floor/recommended/consumer-pin 3열, 공통 3.11, Actions 강제 없음. velocity floor/target 2열 + 예외.
- **승자: merged(risk 3열)**. 권고: `versions.json` 각 축은 `floor/recommended/max?` + 소비자 `exceptions[]{repo,key,installed,reason,review}`. 2026-09 값: Node floor 22.12 / recommended 22.23.x(이미지 digest); **npm floor 10.9(Node 22 동봉 10.9.8) / recommended 11.19.x / map 12.0.1 예외**; Next 16.2/16.3.4; React 19.0/19.2.8; TS 5.9/5.9.3 + airport 7.0.2 예외(`until`: typescript-eslint peer 확장 또는 2026-12 재판정); Tailwind 4.3.0/4.3.3; base-ui 1.8; Vitest 4.1; Playwright 1.60/1.63(map exact 예외); **Python common 3.11 호환**(앱 floor 3.12 상향은 앱 결정), uv 0.12; fastapi 0.141 + starlette **미핀**(map `<1.0` 재검증 T-414 전); PostgreSQL/PostGIS 별도 트랙; Actions v7+SHA는 common 재사용 워크플로 내부만. 분기별 baseline 상향 task(T-502/T-507).
- 근거: `vm` §3.2(동봉 10.9.8)·§4.4·§5.1·§6·§7.4, `be` §2.1·§5.3(3.11 floor 3곳), `inv/map` §9(exact 핀·pytest 잠금).
- 심각도: P1(coordinator 값 채택 시 map·weather·ktdm 설치 실패, 4 CI npm 위반).

### D-07 핀 정책·검증 스크립트
- coordinator P3 + 보고→실패 2단. risk 금지 3종 즉시 fail·판정 8종·2회 green 승격·registry 소유. velocity lock 파서 3종·매니페스트·report/warn/fail 앱 자율.
- **승자: merged(risk 규칙 + velocity 도구)**. 권고: P3 계층별 하이브리드 + lockfile 의무(`package-lock.json` v3, `uv.lock`, CI·Docker `--locked`/`npm ci`). `check_versions.py`는 매니페스트(D-19)의 `lockfiles[]{kind,path,scope}`를 읽고 npm lock v3·`uv.lock`·`poetry.lock` 파서로 설치본을 대조, 판정 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/FLOATING_REF/BLOCKED/EXEMPT(만료)`, Markdown+JSON+`$GITHUB_STEP_SUMMARY`. **`BLOCKED`·`FLOATING_REF`·만료 예외는 Phase 2부터 report 모드에서도 exit 1**. `enforce`는 `versions.json` `consumers.<repo>.enforce`가 소유하고 승격 조건(소비자 CI report 2회 연속 위반 0)을 충족하면 common PR로 `fail` 전환 — 앱이 자율 선언하는 방식은 기각(지시 (2) 완화). Renovate 미확인 → `templates/dependabot.yml`.
- 근거: `vm` §2.1·§7.1~7.4·Q10~12, `be` §5.1(`@main`), `inv/ktc` §4.1(`mcp<2`), `inv/ktdm` §8-18·19.
- 심각도: P1.

### D-08 Tailwind v4 전환
- coordinator 대상별 서술. risk 순서(airport→dm→geo→concierge→pinvi→weather) + 4단 PR + 중단 조건 + weather preflight 제외. velocity 순서·규모 추정, weather 지연.
- **승자: risk**(velocity 규모 추정 병기). 권고: 모든 대상은 "시각 기준선 캡처(6폭) → 설정만 → 토큰만 → 컴포넌트" 4단 별도 PR. 순서·조건: ① airport WIP 병합(값 유지, `cn`→clsx+twMerge, shadcn/postcss devDeps) ② ktdm Next16/React19/ESLint9/Node22 선행 PR 후 `@theme`→`--kt-*` ③ geo `@config` 실효값 빌드 검증(T-441 ①) 후 `@theme` 단일화 ④ concierge CI 신설 후 fallback 블록·`@config` 제거·`--ktc-*` 재해석 ⑤ pinvi admin 스코프만 매핑, 사용자 preset 유지 ⑥ weather Next16/Vitest4/Node22 → `tokens.css` 교체(Phase 1) → `theme`+`utilities`만 도입(preflight 제외) → 페이지별 셸·패널·폼 교체 → preflight 활성화. **pinvi mobile은 NativeWind 4=Tailwind 3 예외 등록 — 지시 (1)의 축소이므로 사용자 명시 승인(§11 O8), 재평가 트리거 = NativeWind 5 GA**. weather를 "registry 안정 후"로 미루는 velocity 안은 npm 채택(D-10) 시 근거가 사라지므로 기각.
- 근거: `vm` §1.2·§1.7·§5.2·§5.3, `inv/weather` §9.1, `inv/airport` §3.2·§9, `inv/geo` §9·§11-2, `inv/pinvi` §3.2, `dt` §5-3.
- 심각도: P1.

### D-09 프리미티브·React·Button/DataTable 계약
- 세 안 일치(overlay base-ui, 비-overlay native, React 19 전용). risk `sortMode` 필수 prop·`type="button"` 명시·native Checkbox·VirtualTable 잔류. velocity `manualSorting` 기본 true + pinvi 확장 흡수 목록.
- **승자: risk**(velocity 흡수 목록 병합). 권고: Button `type="button"` 엔진 무관 명시, `loading`=aria-disabled+aria-busy+포커스 유지+`onClick` 차단, root opacity 금지, variant 7·size 4+icon(deprecated alias). Checkbox native + `data-slot="checkbox"`. DataTable `sortMode: "server"|"client"` **필수**, `enableSortingRemoval`·`initialSorting`·`rowTestId`·`containerTestId`·`stickyHeader`·sr-only 문구·`hasUnsavedInput`(Dialog)·`viewportProps` 흡수; 검색 툴바·`rowHeader`는 미포함(geo VirtualTable 잔류). base-ui 미확인 3건(`type` 기본·hidden input·Toast API)은 T-201 소스 확인 전 릴리스 금지.
- 근거: `ui` §3.1~3.4·§5.4·§7-1·2·6, `ux` C10.
- 심각도: P2.

### D-10 UI 배포 방식
- coordinator npm 1차·registry 2차, 클래스 공통 이름. risk npm만, `base.scoped.css`, webpack/Turbopack 스모크, ui-contract.md. velocity registry 1차, `kt-` 네임스페이스, drift 검사.
- **승자: merged(npm + `kt-` 네임스페이스)** — 열림 O3. 권고: 1차 배포는 npm(ESM+d.ts+Tailwind 소스 클래스+`'use client'`), 소비자 필수 2줄 `@import "@kor-travel/tokens/theme.css"` + `@source "../node_modules/@kor-travel/ui"`. **클래스는 `kt-` 접두 유틸리티만 사용**(`bg-kt-surface-subtle`, `h-kt-control`; `theme.css`가 `--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--text-kt-*` 정의) — 전 저장소 0회라 pinvi 사용자 표면·airport shadcn 기본명과 무충돌, 앱 별칭 계층 불필요. `base.css`/`base.scoped.css` 두 변형. `docs/standards/ui-contract.md`에 data-slot·testid·heading·geo e2e 셀렉터(`section.panel .panel-header h2`, `pre.json-box`) 대응표를 명시하고 마크업 변경=major. common CI `consumer-smoke`는 webpack·Turbopack 양쪽 `next build`. shadcn 레지스트리는 같은 소스에서 생성 가능하도록 `packages/ui/src` 구조를 유지하되 **Phase 5에서 "npm 소비자 우회 패치 2회 이상"일 때만** 도입 검토(velocity D-24 트리거의 역방향). 이유: 공통화 동기가 geo 반복 동기화 비용(`prior` §3.2)이며 복사 소유는 27/27 상이(`ui` §2.1)를 재생산한다.
- 근거: `ui` §6.2·§6.3·§7-8·9, `dt` §3.1.1(pinvi `admin-*` 회피 관찰)·§3.6.1(`kt-` 0회), `prior` §3.2·§7.3, `inv/pinvi` §9(ADR-066).
- 심각도: P1.

### D-11 배포 채널
- 세 안 일치(GitHub Release tarball + git+https py). velocity wheel 자산 병행, registry raw URL.
- **승자: merged**. 권고: npm = Release 자산 `kor-travel-<pkg>-X.Y.Z.tgz`(태그 `tokens-vX.Y.Z`/`ui-vX.Y.Z`) URL 설치 + lock `integrity`; Python = `git+https://…@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` + wheel 자산 병행(map api.Dockerfile git 부재 대비). 태그 immutable, 같은 버전 재발행 금지. T-006: npm scope 확인은 사용자 계정 작업(실측 403/401로 미확인), PyPI `kor-travel-common`은 404 확인(미점유). 공개 게시는 Phase 5.
- 근거: `be` §5.2, `prior` §8, `ci` §2.3, 실측.
- 심각도: P1(공개 게시는 불가역이므로 게시 시점 결정은 P0급 — 여기서는 tarball 선행으로 회피).

### D-12 토큰 접두·계층·다크·대비
- 세 안 `--kt-*` 일치. coordinator 다크 전 semantic 필수. risk 다크 값 포함·활성 명시 import·contrast report+baseline·`@theme` 비inline 타입. velocity 앱 오버라이드 dark 선택·status 오버라이드 허용·OKLCH 권고.
- **승자: merged**. 권고: 접두 `--kt-*`, 계층 semantic ← app override 2단, shadcn alias 의미 고정(`--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control). 프로필 admin(6/8, 36/30, 15px, 7단)·consumer(문서만, 값 pinvi 소유). 오버라이드 허용 = brand 4·focus·paper 4·ink 4 + status 4+tint(대비 검사 대상). 다크: `tokens.css`가 `.dark` 기본값(map) 포함, **앱 오버라이드의 dark 값은 선택**, 활성화 파일은 명시 import만, 기본 `color-scheme: light`. `kt_contrast`: light 쌍 필수, dark 쌍은 앱이 dark 활성 시; report 기본 + `contrast-baseline.json`(미달 쌍 + `until`), 새 미달만 fail. 값 형식 OKLCH 권고·hex 허용.
- 근거: `dt` §3.2.3·§3.4.2·§3.6.1~3.6.6·§5-1·5·6, `ux` C14.
- 심각도: P2.

### D-13 UX 가이드·PC/Mobile 규약
- coordinator G0~G9 전부 규약 + C1~C22 제안대로. risk 신규 MUST/기존 baseline + `ux_lint` report + C1~C22 판정표. velocity MUST 8 + SHOULD + diff-based gate.
- **승자: merged(risk 규칙 + velocity 게이트 기법)**. 권고: `ux-guide.md`는 G0~G9 전부를 규칙 ID `UX-Gn.m`로 수록하고 각 규칙에 MUST/SHOULD를 표기(velocity U1~U8은 MUST 핵심 집합, 그 외 G 규칙 중 사실 근거 4앱 이상은 MUST, 나머지 SHOULD). 신규 코드 MUST, 기존 잔존은 앱별 baseline 목록(`window.confirm` map 2·ktdm 3·kta 1·weather 1). `ux_lint.py`는 전체 파일 report + diff-based fail(`--base <sha>`). `responsive-web.md`: admin PC-first+≥320 컨테인, 사용자 웹 mobile-first, sm640/md768/lg1024/xl1280, 검사 폭 320/375/414/768/1024/1440, 터치 admin 36/30(히트 ≥24)·사용자 44·모바일 48. C1~C22는 risk 표 채택(C9 geo CANCELLED 보류, C21 Hallmark 본문 인용 금지·common 파일에는 스탬프 없음·SPDX만).
- 근거: `ux` §2·§3·§4·§5, `dt` §3.4.1, `lic` B3.
- 심각도: P2.

### D-14 OpenAPI/REST
- coordinator MUST 전면 + 예외. risk 3계층(즉시 MUST additive / 신규 MUST·기존 SHOULD+예외 / SHOULD) + `openapi-exceptions.yaml`. velocity 신규/기존 분리 + `openapi-exceptions.md` + review 날짜.
- **승자: risk**(velocity review 날짜 병합). 권고: `oa` §3 M1~M9/S1~S13/N1~N8을 3계층으로 채택. 예외 레지스트리는 YAML(기계 판독) `{app, rule, surface, reason, sunset|null, review, owner}` + 생성 md. 헤더는 형식 규칙만(`X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token|Ops-Scope`), `X-Request-ID` 형식 규칙(uuid/ulid, ≤128자)을 M4에 명시(§9 M-09). 422 기본·geo 400 예외, 429 `TOO_MANY_REQUESTS` 기본 사전 + 앱 덮어쓰기. health 별칭은 2릴리스 병행이 아니라 **소비자 probe(ktdm compose·Prometheus) 갱신 확인 전까지 무기한**.
- 근거: `oa` §3·§4·§5·§6, `be` §2.5, `ci` §1.13.
- 심각도: P2.

### D-15 Python 모듈 우선순위
- 세 안 대체로 일치. 메트릭 접두: coordinator P2 이관, risk 신규만, velocity 영구 예외.
- **승자: risk**. 권고: core는 stdlib+pydantic만, `[api]` extra에 FastAPI 의존(geo·map import-linter 계약). 1차 C12·C4·C13·C20(format 규칙 미포함, `per-file-ignores` baseline) → 2차 C1·C9·C7·C2(`trust_incoming`)·C3(접두는 인자) → 3차 C5(`exclude_paths`)·C16(HSTS 전달 헤더 불신 기본)·C17·C8·C11·C10·C15·C18 → 보류 C6·C14(경계 상수 공통화 금지)·C19·C21. 메트릭 접두는 신규 서비스 MUST `kt<x>_`, map·pinvi는 **기한부 예외(review 2026-12, 대시보드 영향 평가 task)** — 영구 예외는 지시 (2)의 정신에 어긋남.
- 근거: `be` §3·§4·§7-4, `oa` §5.
- 심각도: P2.

### D-16 첫 소비자
- coordinator map+pinvi admin(L6 무시). risk tokens map+weather+airport, ui map+airport, pinvi Phase 4. velocity map+pinvi(L6 critical path), airport 대체.
- **승자: merged**. 권고: **L6(pinvi 라이선스 선언)를 Phase 0 외부 확인 T-006과 같은 급으로 승격**(T-020 "pinvi L6 결정 반영", 선행 없음, 외부 선행 = 사용자 결정 §11 O1). tokens 1차 = map + weather + pinvi admin(L6 완료 시) — weather는 `tokens.css` 교체만으로 채택 가능하고 airport WIP는 값 유지가 열림이라 1차 검증자로 약함. ui 1차 = map + pinvi admin(L6), L6 지연 시 airport 소형 부품(Alert·StatStrip·SectionCard·EmptyState·Button)으로 대체. Python 1차 = map-api·weather-api·airport. 이렇게 하면 지시 (3)의 "PinVi Admin 포함"과 `lic` B1·§3.6을 동시에 만족한다(pinvi에는 이미 GPL 이식 파일 50개가 있어 상태가 악화되지 않으나, 무라이선스 저장소에 GPL 링크를 늘리는 것은 L6 전 회피).
- 근거: `lic` §3.6·§4 B1·L6, `prior` §1, `ui` §4, `inv/weather` §8-1, `inv/airport` §1-4.
- 심각도: P1.

### D-17 라이선스
- coordinator 결론 대기(stale). risk L1~L16·B1~B10 완전 반영. velocity 동일 + drift 정규화.
- **승자: risk**(velocity 보강). 권고: common = GPL-3.0-or-later; `NOTICE`(저작권자·버전·연락처), `THIRD_PARTY_NOTICES.md`, `LICENSES/`(MIT·Apache-2.0(cva)·ISC·BSD-3·OFL-1.1), `PROVENANCE.md`(`lic` §2.3 형식), 파일별 SPDX + `Origin/Derived-From/Modified`, `tools/check_spdx.py`(common 파일은 즉시 fail). **각 npm tarball·wheel에 LICENSE·NOTICE·THIRD_PARTY_NOTICES 동봉 + `license: "GPL-3.0-or-later"` 필드 + PEP 639**(`lic` §3.3·§3.5). 추출 규칙: GPL 원천 그대로(geo는 `-only` 병기 또는 재선언 L10), MIT 원천 고지 보존, pinvi는 L6 전 추출 금지(B1), 벤더 tgz·maplibre-vworld-react 영구 금지(B2), Hallmark 본문 인용 금지(B3), ktc AppShell diff(B4). `CONTRIBUTING.md`에 AI 보조 생성물 권리 문구(B8). 소비 앱: ktc·ktdm은 GPL 정렬 권고(L8), §7 추가 허가 기각. 앱 사본의 선두 주석 블록은 drift 비교 시 정규화. **pg-aiguide 스킬은 common이 배포하지 않음**(L12는 앱 task, §9 M-03).
- 근거: `lic` §2.2 D1~D10·§2.4·§3.1~§3.7·§4·§6, `cm` §4.1.
- 심각도: P0.

### D-18 CI·릴리스·포트
- coordinator 5 재사용 워크플로. risk 7종 + 하드닝 + consumer-smoke + branch protection + 포트 130xx 확인. velocity 3종 우선(versions·registry-drift·contrast) + 순서.
- **승자: merged**. 권고: common 자체 CI = `docs`(link·plan·unittest·`git diff --check`·redaction 전체 트리)·`tools`(3종 자기 테스트, ubuntu+windows 매트릭스)·`packages`(build·`npm pack`·tarball 설치·webpack/Turbopack)·`python-package`(uv build·wheel·starlette 0.4x/1.6 매트릭스)·`consumer-smoke`(dispatch+주간, `consumers.pins.json`)·`secret-scan`; 하드닝(`permissions: contents: read`, concurrency, timeout, `ubuntu-24.04`, head SHA, 액션 SHA 핀). 재사용 워크플로 순서: **Phase 1 `versions-check`·`contrast-check`·`docs-check`**(지시 (2)의 검증 가능성 확보) → Phase 3 `openapi-drift`·`typegen-drift` → Phase 5 `node-quality`·`python-quality`(선택). job `name:` 입력 개방(map 8·pinvi 5 required check 보전), 태그/SHA 참조만, 운영 호출 job required 금지 권고. 릴리스: 패키지별 태그, `-rc.N` 소비자 PR 검증 후 정식. 포트 정본 ktdm `docs/ports.md`, common `130xx` 로컬 점유 확인(T-014).
- 근거: `ci` §1.3·§2.1~§2.3·§3·§4, `cv` §1.3.
- 심각도: P2.

### D-19~D-30 신규 결정(세 안 병합)

| ID | 출처 | 최종 권고 | 심각도 |
|---|---|---|---|
| D-19 소비자 매니페스트 | velocity D-19 | 각 소비 저장소(모노레포는 앱 디렉터리)에 `kor-travel-common.lock.json`(`consumer-manifest.v1`): `tokens{version,override}`, `ui{version}`, `python{version}`, `lockfiles[]{kind,path,scope}`, `contrast{baseline}`, `ux_gate{baseline}`, `exceptions[]`. `enforce` 필드는 두지 않고 `versions.json` `consumers`가 소유(D-07). `docs/integration-map.md`는 매니페스트에서 생성 | P2 |
| D-20 airport Admin 정의 | risk D-20 / velocity D-21 | 현 실체 = 무인증 백업 패널 + collector 패널 + `/v1/admin/*`. 1차 tokens + 소형 부품; AdminPageHeader/skip-link는 airport T-035 후 `T-431a`; 로그인·셸은 대상 아님 | P2(열림 O9) |
| D-21 시각 회귀 기준선 | risk D-21 | 토큰·스타일·셸 변경 PR은 6폭 스크린샷 기준선 + diff evidence 필수; Playwright 없는 앱은 `templates/playwright.baseline.ts` | P2 |
| D-22 헤더·메트릭 접두 | risk D-22 | 형식 규칙만 공통, AppId 앱 소유; 메트릭 신규 `kt<x>_`, 기존 기한부 예외 | P3 |
| D-23 공유 라이브러리 정책 | risk D-23 / velocity D-22 | common 범위 밖; `versions.json` `providers` 보고만; T-505/T-506 결정 요청 | P3(열림 O16) |
| D-24 이관 PR 규격·되돌리기 | risk D-24 + velocity D-23 | 한 PR = 한 산출물, 프레임워크 업그레이드와 분리, revert 1회로 원복, lock 동반, 본문에 evidence·되돌리기 명령, 파일 상한(tokens 10·ui 30·py 10) | P2 |
| D-25 NOT_RUN 표기 | risk D-25 | 실행 못 한 검증은 `NOT_RUN(사유)` + `외부 선행`; 0 test/skip을 pass로 집계 금지(cv R1.12·R1.13, A2.5) | P2 |
| D-26 마커 팔레트 | risk D-26 | common 소유 아님; 16슬롯·라벨 대비 규칙만 ux-guide; hex 정본은 map(T-505) | P3(열림 O15) |
| D-27 `decisions.md`·도구 언어·링크 | risk D-27 | 단일 색인, Python 도구(`python3`/`uv run`), 상대 링크만 | P3 |
| D-28 회수 측정 | velocity D-24 | `prior` §11 지표 + drift·EXEMPT·enforce 전환 수, 분기 `docs/reports/adoption-YYYY-QN.md`; 순절감 ≤0 2분기 → 범위 축소 | P3 |
| D-29 pinvi 사용자 표면·모바일 | risk D-19 | 코드 소비 대상 아님; consumer 프로필 규칙 + `tokens.json` 의미 이름만; 모바일 예외 등록(O8) | P1(지시 (1) 축소 포함) |
| D-30 강제 수준 3단 | velocity D-20 수정 | report→warn→fail 3단은 채택하되 승격은 common registry(D-07) | P1 |

## 5. GPL·`licensing.md` 조치 반영 대조

| 조치 | coordinator | risk | velocity | 판정 |
|---|---|---|---|---|
| L1 NOTICE(저작권자·버전·연락처) | 없음 | T-003 | T-005 | 채택 |
| L2 PROVENANCE | 없음 | T-003 | T-005 | 채택 |
| L3 THIRD_PARTY_NOTICES + LICENSES/(cva Apache) | NOTICE만, cva 누락 | ✓ | ✓ | risk/velocity |
| L4 SPDX 헤더 + 린트 | 없음 | `check_spdx.py` 즉시 fail | ✓ | 채택 |
| L5 패키지 메타데이터(npm `license`, PEP 639, tarball LICENSE 동봉) | 없음 | 부분(`license` 필드) | T-100 `license` | **보강 필요**(§9 M-03) |
| L6 pinvi 결정 | 무시(Phase 1 소비) | T-420(Phase 4) | O1 critical path | 병합: Phase 0 외부 확인으로 승격 |
| L7 maplibre-vworld-react 메타 | 없음 | T-505 요청 | T-506 | 범위 밖 요청 |
| L8 ktc·ktdm 정렬 | "licensing 결과로" | T-452(§7 기각) | T-451/T-471 | 채택(열림 O2) |
| L9 map LICENSE 전문 | 없음 | T-410 | 비차단 | 채택 |
| L10 geo -only | 없음 | F-2′ | O 없음 | 열림 O20 |
| L11 `license` 필드 전 앱 | 없음 | T-433 등 | 비차단 | Phase 4 앱 task |
| L12 pg-aiguide Apache 고지 | 없음 | 없음 | 없음 | **누락** — common 배포 여부 결정 필요(M-03) |
| L15 airkorea 정본 | 없음 | T-481 | T-506 | 채택 |
| L16/B3 Hallmark 인용 금지 | Q7 열림 | C21 | C21 | 채택 + common 파일 스탬프 없음 |
| B8 AI 생성물 권리 | 없음 | CONTRIBUTING | 없음 | risk |

## 6. 규칙 4축 완전성

| 축 | 정본 문서 | 검사 도구 | 예외 레지스트리 | 세 안 중 결함 |
|---|---|---|---|---|
| 색상 톤 | `design-tokens.md`(역할·대비·hairline 2종·불투명 tint·alpha 정책·raw 색 금지·오버라이드 허용·다크·shadcn alias 의미) | `kt_contrast.py` | `contrast-baseline.json`(앱) | coordinator는 즉시 fail 전제(첫날 4앱 red, `dt` §3.4.2) |
| UX 가이드 | `ux-guide.md` G0~G9(`UX-Gn.m`) + C1~C22 판정 | `ux_lint.py` | 앱 baseline 목록 | velocity MUST-8로 축소(P2) |
| OpenAPI | `openapi.md` 3계층 | `openapi-drift.yml`·`typegen-drift.yml`·export CLI `--check` | `openapi-exceptions.yaml` | coordinator 전면 MUST(pinvi 모바일·concierge provider 계약 파손, `oa` §4) |
| PC/Mobile Web | `responsive-web.md` 표면 분류·breakpoint·검사 폭·터치·안전영역·overflow | `templates/playwright.baseline.ts`(6폭) | pinvi 44px 2쪽·kta 860 | 세 안 동등; 모바일 앱은 규칙만 |

## 7. 버전 일치 정책의 검증 가능성

| 기준 | coordinator | risk | velocity | 병합 판정 |
|---|---|---|---|---|
| 정본 파일 스키마 | `version-registry.v1` 이름만 | floor/recommended/image/blocked/consumers/exceptions 예시 | floor/target/exceptions/blocked/providers 예시 | risk 스키마 + velocity `providers` |
| 설치본 읽기(선언 아님) | 언급 없음 | lock 파일 종류 명시 | npm lock v3·uv.lock·poetry.lock 파서 명세 | velocity 파서 명세 |
| lock 없는 4곳 처리 | 전환 task | `NO_LOCK` + 도입 선행 T-440/450/471/484 | `LOCK_MISSING` 보고 | 병합: 보고하되 Phase 4까지 `NO_LOCK` 해소를 앱 완료 조건에 포함 |
| 판정 어휘·종료 코드 | 보고→실패 2단 | 8종 + 즉시 fail 3종 | 5종 + 3모드 | risk |
| 승격 규칙 | 없음 | 2회 연속 green → common PR | 앱 선언 | risk(velocity는 지시 (2) 완화) |
| 예외 만료 | 없음 | `until` 만료 시 fail | `review` 날짜 | 병합: `until` 필수, 만료 = fail |
| 첫날 CI 영향 | 정확값 강제 → map·ktdm·weather 위반 | report 0 위반 3곳(map·pinvi·airport 예외) | report | risk |
| 검증 실행 위치 | 미정 | 소비자 CI + 로컬 경로 | `versions-check.yml` + `--repo` | 병합 |
| npm 축 정합 | 동봉 11.19 오기 | floor 11.19 vs 동봉 10.9 모순 | 동봉 11.19 오기 | **세 안 모두 수정**: floor 10.9 |

결론: 병합안(D-06·D-07·D-19·D-30)은 (a) 정본 JSON, (b) 설치본 파서, (c) 판정 어휘·exit code, (d) 승격·만료 규칙, (e) 소비자별 report 산출물 5요소를 갖춰 "일치"를 기계로 판정할 수 있다. velocity 단독안은 (d)가 없어 검증은 되나 강제되지 않고, coordinator 단독안은 (b)·(c)가 없다.

## 8. 사실 오류·근거 결함(§10 상세와 동일 번호)

E1~E15는 §10 표 참조.

## 9. 세 안 모두에서 빠진 결정(missing)과 제안

| # | 누락 결정 | 왜 필요한가(근거) | 제안 기본값 |
|---|---|---|---|
| M-01 | SemVer 0.x 취급·패키지 간 버전 결합 | `prior` §8 [E7] "0.x라는 이유로 무통보 파괴적 변경 금지"; risk D-01은 ui→tokens "같은 minor"만 언급 | 0.x 동안 minor = breaking 허용(이관 지침·CHANGELOG `### Breaking` 필수), patch = 비파괴; tokens·ui·py 독립 버전, ui peer `@kor-travel/tokens` 같은 minor; 마크업·토큰 이름·정렬 기본값·키보드 동작 변경 = minor(0.x)/major(1.x) |
| M-02 | 코드 주석·docstring·커밋 메시지 언어 | `inv/ktdm` §9 "코드 주석·docstring·커밋까지 한국어 → common 정책 결정 필요"; airport·weather 주석은 영어(`inv/weather` §9) | 문서 정책과 동일: 한국어 기본, 식별자·공식 용어·외부 인용 원문 유지; 커밋 제목은 Conventional Commits 영어 접두 + 한국어 본문(map·ktc 관례) |
| M-03 | 패키지 산출물의 라이선스 동봉·pg-aiguide 배포 여부 | `lic` §3.3 마지막 행·§3.5(npm `files`+LICENSE·NOTICE·THIRD_PARTY, PEP 639 `license-files`), `lic` Q7·L12(Apache NOTICE) | tarball·wheel에 3파일 동봉 + `license` 필드; pg-aiguide는 common 미배포(각 앱 L12) |
| M-04 | Windows 개발자 지원 수준 | 현재 사용자 환경 Windows(PowerShell), canview Windows 정본(`cv` A5.1), 소비자 6/7 Linux/WSL(`dc` §1.11) | Tier 1 = Linux/WSL(정본, 전 gate); Tier 2 = Windows native에서 Python 도구 3종·문서 validator 동작 보증(CI `windows-latest` job) + `npm pack` 스모크; 패키지 빌드·consumer-smoke는 WSL 권장. `dev-environment.md`에 tier 표 |
| M-05 | canview 항목별 대조표 산출물 | 지시 (5) "가져온다"의 검증 수단이 없음; `cv` §2 A1.1~A8.5·§3 R1~R6·Q9 미결 | `docs/architecture/canview-checklist.md`: 항목 ID별 채택/변형/제외/사유; T-001 acceptance. A6 추상화 5항은 공통 절 F(≤5)에 "생성물 수동 불일치 금지·1곳 관찰 승격 금지·조사/규범 분리·stale 값 정상 렌더 금지·계약 변경 시 시험·버전 표기" 로 이식 |
| M-06 | `docs/README.md` 3단계 읽기 표·정본 관계 트리·resume 5절·journal H2 형식·CHANGELOG 형식 | `cv` R5.1·R5.4·R5.5·R5.7·R5.8 | T-001 acceptance에 R5 항목 명시; journal 형식은 canview `## YYYY-MM-DD (agent, 주제)` + geo/map 5필드 병합 |
| M-07 | PR 본문 6항목·stage 규칙·검증 사다리 변형 | `cv` R4.6·R4.8·R4.9·R1.14 | `agent-workflow.md` §4 사다리 6층(문서→패키지 빌드·타입→단위→tarball 설치→소비자 빌드·e2e→배포 스모크), §7 stage 경로별 명시·`git add -A/.` 금지, PR 본문 6항목 + `.github/pull_request_template.md` |
| M-08 | common 파일의 Hallmark 스탬프 | risk C21(이식 파일에 common 스탬프) vs velocity C21(미포함) 상충; `lic` B3 | common 파일에는 스탬프 없음(SPDX·Origin만); 소비 앱이 자기 스탬프를 붙이는 것은 앱 소유 |
| M-09 | `X-Request-ID` 형식 규칙 | `oa` Q9(uuid/ulid·최대 길이만 공통이면 ktdm 불신·echo 양립) | 허용 = UUID v4/v7 또는 ULID, ≤128자 ASCII, 검증 실패 시 서버 발급; `trust_incoming=False`는 앱 옵션 |
| M-10 | 릴리스 산출물 무결성(provenance) | `ci` §1.2 pinvi wheel/image provenance, `be` §5.2 D(sha256) | Release 자산에 `SHA256SUMS` 첨부, 소비자 lock `integrity`/sha 기록 의무; npm provenance는 공개 게시 시 |
| M-11 | 토큰 값 정본(CSS vs JSON) | `dt` §3.6.3 "값 정본이 CSS인지 JSON인지 결정" | 정본 = `tokens.css`, `tokens.json/ts/preset.cjs`는 생성물(빌드 시 diff 검사) — risk T-101·velocity T-100과 일치, ADR로 고정 |
| M-12 | 조사 문서 재조사 주기 | `documentation-maintenance.md` §2 "조사 기준 커밋 갱신" 행만 존재 | 분기 감사(T-504)와 동시에 기준 커밋 갱신; 본문 불변·새 절 추가 |
| M-13 | `@source`·`transpilePackages` 표준 문구 | `prior` §7.3 [E1]·[E6], `inv/geo` §9 `source(none)` | `consumer-adoption.md`에 `@source "../node_modules/@kor-travel/ui"` 정확 경로(모노레포 상대 경로 표) + Next `transpilePackages` 불필요(사전 컴파일 ESM) 명시, pinvi webpack 검증 |

## 10. 사실 오류·근거 결함 목록

| # | 위치 | 주장 | 근거·정정 | 영향 |
|---|---|---|---|---|
| E1 | coordinator D-06 npm 행 | "Node 동봉 11.19.x 기준, 허용 `>=11.19 <13`" | `vm` §3.2·§4.4: Node v22.23.2 동봉 npm은 **10.9.8**, 11.19.0은 Node 24/26 동봉. Node 22 기준선과 모순 | 4 CI(airport·dm·geo·weather) 첫날 위반 |
| E2 | velocity D-06 npm 행 | "target 11.19.x(동봉)" | 동일 | 동일 |
| E3 | risk D-06 npm 행 | floor 11.19이면서 "동봉 npm 10.9(`vm` §3.2)" 병기 | 내부 모순: floor > 동봉이면 별도 설치 없는 CI 전부 `BELOW_FLOOR` | 설계 모순, floor 10.9로 정정 |
| E4 | coordinator D-06 Python 행 | "`requires-python >=3.12`… 근거 backend §5.3·Q1" | `be` §5.3 "파이썬 floor: 3.11(map·ktw·ktdm 때문)"; §2.1 3.11 floor 3곳 | common 설치 불가 3앱 |
| E5 | coordinator 머리·D-17·D-18 | "ci-deploy·licensing·canview-structure는 작성 중", "licensing 결론 반영(열림)" | 세 문서 존재(438·314·446행, 2026-09-06 10:34~10:41) | 라이선스·CI 결정 부재 |
| E6 | coordinator D-06 shadcn 행 | "shadcn CLI devDependencies에만" | `lic` §2.2 D9: map `tests/unit/test_frontend_dependency_security.py:78`이 shadcn **부재**를 단언 | map CI 충돌, 예외 필요 |
| E7 | coordinator D-06 Node 행 | engines `^22.22.0 \|\| ^24.15.0` | `vm` §1.1 map은 `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0` | 경미 |
| E8 | coordinator D-17 | 서드파티 "shadcn·base-ui·radix MIT, tw-animate-css MIT, Pretendard OFL" | `lic` §2.4: cva **Apache-2.0**(NOTICE 의무), pg-aiguide Apache-2.0 누락 | 고지 파일 결함(P0급) |
| E9 | velocity F.2 | T-413/414(map-api), T-423(pinvi api), T-432(airport py), T-443(geo py), T-454(concierge py), T-463(weather-api) | `docs/tasks-rule.md` §2.1: Python 백엔드 소비는 **T-480~T-489**(앱별 `a`/`b` suffix) | 원장 규약 위반 |
| E10 | risk D-01·velocity D-01/D-11 | "PyPI 404 = 미점유 사실" | 조사 문서에 해당 조회 없음(`vm` §4.1은 패키지 최신 조회만). 본 판정 실측(2026-09-06 curl) 404 → **사실로 확정**; npm scope는 403/401로 여전히 미확인 | 근거 인용 보강 |
| E11 | risk D-16 | "pinvi는 B1과 **B9**에 걸려" | `cm` §4.1 B9는 ktc·ktdm(MIT)의 GPL 링크 항목; pinvi는 B1/L6 | 결론 유지, 인용 정정 |
| E12 | coordinator D-01 | ui peer `lucide-react ^1` | `vm` §1.3: dm 0.363·geo 0.468·weather 0.468·pinvi 0.460 | 4앱 설치 차단 |
| E13 | coordinator D-16·E Phase 1 | "map·pinvi admin 토큰 채택" 1차 | `lic` §4 B1·L6, `cm` §4.1 B1 | 권리 확인 전 소비 |
| E14 | velocity D-08 vs `ui` §0 | airport WIP "61파일" vs `ui` §0 "8파일 추가/변경(frontend 한정)" | `inv/airport` §3.2 153행 `git show --stat HEAD` 61 files(사실) — 조사 문서 간 범위 차이, velocity 오류 아님 | 없음 |
| E15 | coordinator D-02 | "`docs/decisions.md`는 canview와 동일하게 유지 … 근거 docs-conventions §4" | `dc` §4 표: `decisions.md` **불필요**; `cv` Q1 충돌 | 근거 오인 |
| E16 | risk E.1 | T-480~T-485를 앱별 별도 번호로 사용 | `tasks-rule` §2.1 "앱별 하위 항목은 `a`, `b` suffix" — 대역 안이므로 경미 | P3 |
| E17 | coordinator D-06 Vitest 행 | "Vitest 4.1.x(Node 22.12+ 전제)" | `vm` §4.2: 22.12 engines는 Vitest **5.0.0** 기준 | 경미 |

## 11. 사용자 확인이 필요한 열린 결정(기본값)

| # | 결정 | 기본값 | 막히는 것 |
|---|---|---|---|
| O1 | pinvi 라이선스·공개(L6) | 공개 + GPL-3.0-or-later(루트 LICENSE·README/AGENTS 정합·api pyproject·maplibre 문서 정정, 1 PR) | pinvi admin 1차 소비(T-420 계열) |
| O2 | ktc·ktdm GPL 정렬 vs common §7 추가 허가 | 정렬(1 PR씩) | concierge·ktdm 코드 채택 |
| O3 | UI 배포 방식 | npm 1차 + `kt-` 네임스페이스, registry는 Phase 5 재평가 | Phase 2 설계 |
| O4 | 토큰 접두 | `--kt-*` | T-101 |
| O5 | npm scope `@kor-travel` 확보(사용자 계정 작업) | tarball 선행(비차단); 실패 시 `@digitie/kor-travel-*` | 공개 게시 |
| O6 | TS 기준선·airport 7.0.2 | 5.9.3 기준선 + airport 예외(`until` typescript-eslint peer 확장 또는 2026-12) | T-433 |
| O7 | Node·npm | Node 22 / npm floor 10.9·권장 11.19 / map 12.0.1 예외 / Node 24 승격 Phase 5 | T-005 |
| O8 | **pinvi mobile Tailwind 3 예외(지시 (1) 축소)** | 예외 등록 + NativeWind 5 GA 재평가 — **명시 승인 필요** | T-005 exceptions |
| O9 | airport "Admin" 정의 | 현재 실체(백업 패널) | T-430~432 |
| O10 | airport 토큰 값(16/10·alpha line) 수렴 여부 | 유지(오버라이드 밖 항목 문서화) | T-431 |
| O11 | 다크 모드 요구 수준 | 정의 필수(map 기본)·활성 opt-in·앱 오버라이드 dark 선택 | T-104 |
| O12 | gate fail 승격 주체 | common registry(2회 green 후 PR) | T-502 |
| O13 | 메트릭 접두 map·pinvi | 기한부 예외(review 2026-12) | T-307 |
| O14 | 429 코드명·geo v2 problem+json 시점 | `TOO_MANY_REQUESTS`; ADR-060 묶음 | T-301 |
| O15 | 마커 팔레트 정본 | map(Tableau) 확정 요청 | 없음 |
| O16 | 공유 라이브러리 배포 정책(`maplibre-vworld-react` npm 등) | 결정 요청 T-505 | 없음 |
| O17 | 코드 주석·커밋 언어 | 한국어 기본(식별자·원문 영어) | T-001 |
| O18 | pg-aiguide 스킬 common 배포 | 미배포 | T-003 |
| O19 | Windows 지원 tier | Tier 2(도구 3종 + validator) | T-003/T-009 |
| O20 | geo `GPL-3.0-only` 재선언 | `-or-later` 권고, 결정 전 `-only` 병기 | 없음 |
| O21 | pinvi admin 44px 예외 2쪽 | 영구 예외 | T-422 |
| O22 | dirty 이탈 경고 | 미포함 | T-105 |
| O23 | prod 도메인 redaction 범위 | common 전체 트리, 소비자 opt-in | T-009 |
| O24 | Renovate 설치 | dependabot 템플릿만 | T-507 |
| O25 | 재사용 워크플로 cross-repo 호출(common 공개 여부) | 공개 전제 + 체크아웃 fallback 문서 | T-010 |

## 12. 병합 레지스터 골격과 다음 액션

1. **레지스터 정본 = risk-first**를 기반으로 §4의 병합 문안을 반영한다(D-06 npm floor, D-07 매니페스트, D-10 `kt-` 네임스페이스, D-16 L6 Phase 0 승격, D-19/D-28/D-30 velocity 편입, M-01~M-13 추가).
2. task 원장은 risk E.1(79개)을 기준으로 velocity T-007(매니페스트 스키마)·T-209(registry_drift → `ui_drift`로 개명, npm 소비자 로컬 패치 탐지)·T-400(이관 절차)·T-503(회수 보고)을 흡수하고, 신규 T-020(pinvi L6 반영, 선행 없음·외부 선행 사용자)을 Phase 0에 추가한다. Python 소비 task는 T-480~T-489 대역만 사용.
3. 지시 완화 항목은 단 하나(pinvi mobile Tailwind 3 예외, O8)이며 사용자 승인 없이는 예외 등록하지 않는다. 그 외 완화로 보였던 항목(velocity enforce 앱 자율, MUST-8)은 병합에서 기각했다.
4. 첫 5개 task(T-001~T-005)는 세 안 모두 선행 없음으로 즉시 착수 가능하며, T-001 acceptance에 M-05·M-06·M-07(canview 대조표·docs/README·PR 템플릿)을 넣어 지시 (5)의 검증 수단을 만든다.
