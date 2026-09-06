# 판정 보고서 — 소비자 이관 실현성·비용 (lens: migration-feasibility)

- 작성일: 2026-09-06 · 판정자 초점: 7개 앱 각각에서 결정을 실행할 때의 **PR 수·변경 규모·회귀 위험·순서 의존성(DAG)**. "여러 번 일하지 않게 하는가"를 최우선 기준으로 둔다.
- 입력: coordinator 초안(D-01~D-18, F절), risk-first(D-01~D-27, 79 task), velocity-first(D-01~D-24, 80 task). 근거는 `docs/survey/*`(약칭 `vm`·`dt`·`ui`·`ux`·`be`·`oa`·`ci`·`dc`·`cv`·`lic`·`cm`·`inv/<app>`), `docs/tasks-rule.md`, `tools/validate_plan.py`, 선행 보고서(`prior`).
- 표기: **사실** = 조사 문서 확인 / **추정** = 이 보고서의 규모 추정(실측 아님) / **열림** = 사용자 확인 필요. PR 수·파일 수는 전부 추정이다.

## 0. 한 줄 결론

| 항목 | 판정 |
|---|---|
| "여러 번 일하지 않게" 하는 레지스터 | **코드 배포는 risk-first**(npm 패키지 = 수정 1회 전파), **프로세스·게이트는 velocity-first**(report 기본·앱 선언 승격·매니페스트·앱당 job 1개 추가). velocity의 "레지스트리 복사 1차"는 `patched≥3 → npm 전환` 트리거를 스스로 두고 있어 **두 번 일하게 되는 설계**다 |
| 즉시 시작 가능한 첫 5 task | risk·velocity 모두 "선행 없음"으로 적었지만 각 1~2개가 실제로는 다른 task나 사용자 결정에 묶여 있다(§4). 보정안 §4.3 |
| 가장 큰 실행 병목(공통) | pinvi 라이선스(L6)·airport WIP 병합·geo React 19 ADR·ktc/ktdm 라이선스(L8) — common 쪽에서 대체 불가한 **외부 선행 4개**. coordinator 초안은 이 중 L6·L8을 반영하지 않아 첫 소비자 순서가 성립하지 않는다(P0) |
| 세 안 모두 공통 오류 | npm floor를 11.19로 두면서 Node 22를 기준선으로 삼음 — Node 22 동봉 npm은 10.9.x(`vm` §3.2·§4.4)라 kta·ktdm·geo·wx 4곳이 도입 첫날 `BELOW_FLOOR` |

## 1. 레지스터 채점(초점: 이관 실현성·비용)

| 레지스터 | 점수 | 강점 | 약점 |
|---|---|---|---|
| coordinator | **44** | 범위가 완전하고 F절 보정(airport Admin 실체, map 잠금 테스트, 헤더 형식 규칙, weather 정량)이 정확하다. Phase 골격은 세 안의 공통 뼈대가 됐다 | 5패키지 동시 출범(`config`는 map ESLint 검증 스크립트·airport TS7·ktdm ESLint 8과 즉시 충돌, `api-client-core`는 `ApiError` 4형 어댑터), 단일 정확 기준선(airport TS 하향·map npm 하향 PR 유발), Python `>=3.12` floor(map·wx·ktdm 설치 불가, `be` §5.3), lucide `^1` peer(4앱 0.x, `vm` §1.3), 첫 소비자 map+pinvi가 L6 gate를 무시. **task 목록·DAG가 없어** 실현성 판정 자체가 불가 |
| risk-first | **72** | 대상별 순서·4단 PR·중단 조건(D-08), 라이선스 gate를 소비자 순서에 반영(D-16), base-ui 미확인 3건을 릴리스 전 확인 task로 고정(T-201), 79 task에 외부 선행을 분리, weather preflight 제외 단계가 2,495행 무스타일 사고를 막는다 | `FLOATING_REF`·`latest`·`blocked` 즉시 fail은 pinvi(etl `@main`)·dm/map/ktc/pinvi-dev(RustFS `latest`)를 도입 첫날 red로 만든다(자기 원칙 R3 위반). DataTable `sortMode` 필수 prop은 map 호출부 전수 수정. 재사용 워크플로 5종을 Phase 0에 두면 map 8·pinvi 5 required check 재구성이 선행 조건이 된다. T-402(7앱 기준선)가 T-410 map 채택을 막고, T-461(weather tokens)이 불필요하게 T-460(Next 16)에 묶인다 |
| velocity-first | **69** | 소비자 PR 최소(앱당 워크플로 job 1개·매니페스트 1파일), report→warn→fail 앱 선언 모델, `kt-` 유틸리티 네임스페이스(pinvi 사용자 preset 충돌 0), weather를 registry 2차 안정 후로 미룬 순서, 첫 릴리스 소비 규모를 결정마다 적음 | **레지스트리 복사 1차**는 27/27 상이를 만든 바로 그 방식이며 `patched` 아이템은 상류 수정을 못 받는다 → DataTable·Button 같은 2차 부품은 결국 npm으로 두 번 옮긴다. `@kor-travel/ui` 보류로 pinvi·concierge는 재수입 PR을 두 번 연다. map+pinvi 1차는 여전히 L6에 걸린다(대체안은 있음). T-002(ADR)가 자기 열림 O3·O4에 차단. `npm 11.19 동봉` 오류, map Dockerfile git 부재 단정(미확인 사항) |

## 2. D-ID별 대조·최종 권고

### 2.0 결정별 소비자 비용 지표(추정) — 세 안 비교

"소비자 PR" = 결정 때문에 7앱에 추가로 열리는 PR 수(추정). "재작업" = 나중에 되돌리거나 두 번 하게 될 확률(높/중/낮). "첫날 red" = 도입 즉시 CI 실패를 만드는지.

| ID | coordinator | risk-first | velocity-first | 병합안 |
|---|---|---|---|---|
| D-01 | 소비자 PR +5(config 예외 5·api-client 어댑터), 재작업 높 | +0, 재작업 낮 | +0 지금, 재작업 **높**(registry→npm) | risk 기반 |
| D-04 | +6(리뷰 표준 PR), 재작업 낮 | +6 | +0 | velocity + 판정 주체 |
| D-06 | +3 하향 PR(airport TS·map npm·Python floor), 첫날 red 3~4 | 첫날 red 4(npm floor) | 첫날 red 4(npm floor) | 3열 + npm floor 10.9 |
| D-07 | +6(정확 핀 재작성) | 첫날 red 5(즉시 fail) | +0 | velocity 모드 + risk 어휘 |
| D-08 | weather 재작업 높(셸 손 이식) | 재작업 낮, PR +1(preflight 단계) | 재작업 낮 | risk 단계 + velocity 순서 |
| D-09 | +0 | map 호출부 전수(`sortMode`) | +0 | velocity 기본값 + risk 계약 |
| D-10 | +0, `@source`·peer 정렬 | 동일 + `base.scoped.css` | map sed ~40파일, 재작업 높(2차 부품) | npm + `kt-` 내부 클래스 |
| D-12 | dark 값 발명 3앱, contrast 첫날 red 4 | contrast baseline 파일 4 | +0 | velocity dark + report |
| D-13 | 기존 위반 7건이 차단 조건 | baseline 파일 4 | +0(diff-based) | velocity |
| D-14 | pinvi·ktc·ktdm breaking | +0(예외 yaml) | +0 | risk 3계층(M1은 Phase 3) |
| D-16 | pinvi 트랙 **정지**(L6) | +0 | L6 대기 시 airport 승격 | GPL 3곳 → pinvi 합류 |
| D-18 | map·pinvi required check 재구성 | 동일(5종 Phase 0) | +0(job 1개) | velocity + 하드닝 |

각 행: 세 안 요약 → 실현성 판정 → 승자 → **권고 문안** → 틀렸을 때 심각도.

### A. 저장소 범위·구조

| ID | coordinator | risk-first | velocity-first |
|---|---|---|---|
| D-01 배포 단위 | 5 npm/py + docs + templates | tokens·ui·py 3 + scope gate, lucide 비의존 | tokens + registry + rules; ui npm 보류 |
| D-02 구조 | canview + `decisions.md` 유지 | `adr/README.md` 단일 색인 | 동일(단일 색인) |
| D-03 개발 환경 | Linux/WSL 정본, Windows 보조 | 동일 + `.gitattributes` LF 확인 | 동일 + 도구 Windows 동작 |
| D-04 리뷰 gate | common full; 소비자 full/light 표준 | 동일 + 판정 주체 merge 담당 | common full; 소비자 미규정 |
| D-05 task 원장 | 5열 표; 소비자 체크박스 허용 | 동일 + `validate_task_ledger` Phase 5 | 5열 표; 소비자 미규정 |

**D-01** — 실현성: `config` 패키지는 도입 즉시 예외 5개(map `verify-frontend-eslint-config.mjs`, pinvi Hallmark `no-restricted-syntax`, airport TS 7·ESLint 부재, ktdm ESLint 8)를 만들고(`vm` §1.6, `inv/map` §3.1), `api-client-core`는 4앱 `ApiError` 형태가 달라(`cm` §2.3) 어댑터만 늘어난다. lucide `^1` peer는 dm 0.363·geo 0.468·wx 0.468·pinvi 0.460과 충돌한다(`vm` §1.3). velocity의 registry 1차는 D-10에서 판정.
승자: **merged(risk-first 기반)**. 권고: 배포 단위는 `packages/tokens`(npm, React 무관)·`packages/ui`(npm, React 19 전용, 컴포넌트별 subpath, 내부 아이콘 인라인 SVG)·`packages/py/kor-travel-common`(extras) 3개 + `docs/standards/*` + `versions.json`/`tools/*`. `templates/eslint/*.mjs`·`templates/agent-config/`는 opt-in 조각(패키지 아님). shadcn 레지스트리는 셸·로그인·Playwright 기준선 같은 "앱이 소유해야 하는 템플릿"에만 2차 채널로 둔다. `package.json` `name`은 `@kor-travel/*` 잠정, 첫 소비자 PR 전 T-006 scope 확인. 심각도 **P1**(패키지 경계를 나중에 바꾸면 소비자 import 경로 전면 개명).

**D-02** — 승자: risk/velocity(단일 색인). 권고: `docs/decisions.md` 없음, `documentation-maintenance.md` §2·§3 문구 정정, 절대 링크 = 오류. **P3**.

**D-03** — 승자: merged. 권고: common 정본 Linux/WSL bash·CI `ubuntu-24.04`; **`tools/*.py`는 Windows Python에서도 동작해야 한다**(현 사용자 환경 Windows, `cv` §1.2 CRLF 사고) — CI `tools` job만 ubuntu+windows 매트릭스(Python stdlib, 비용 낮음). runbook 명령은 bash 단일 표기. **P3**.

**D-04** — 실현성: 소비자 6곳에 리뷰 표준 PR을 여는 것은 이관 가치 0. 대신 채택 PR 템플릿에 "2인 요약" 칸만 두면 kta 관행·map 1-approval 규칙과 충돌 없이 흡수된다. 승자: **velocity + risk의 판정 주체 규칙**. 권고: common 자체 full gate(비면제 목록 = risk-first D-04). 소비자에는 AGENTS 공통 절 B 4불릿과 `templates/consumer-pr.md`의 리뷰 요약 칸만 배포, light/full 판정은 merge 담당. **P3**.

**D-05** — 승자: velocity(소비자 미규정) + **`docs/tasks-rule.md` §2.1 보정**(§5 M-12). **P3**.

### B. 프론트엔드 스택·버전 정렬

| ID | coordinator | risk-first | velocity-first |
|---|---|---|---|
| D-06 기준선 | 단일 정확값(예외는 산문) | floor/recommended/consumer pin 3열 | floor/target 2열 + exceptions[] |
| D-07 핀 정책 | P3 정확 핀 + report→fail | P3 + lockfile 의무 + 금지 3종 즉시 fail | P2+ lockfile + report/warn/fail 앱 선언 |
| D-08 Tailwind v4 | 앱별 서술 | 순서 6 + 4단 PR + 중단 조건 | 순서 6 + 규모; weather는 registry 2차 후 |
| D-09 프리미티브 | base-ui overlay·native·React 19 | 동일 + `sortMode` 필수 prop, VirtualTable 잔류 | 동일 + `manualSorting` 기본 true |
| D-10 배포 | npm 1차, 레지스트리 2차, 공통 클래스명 | npm + `base.scoped.css` + 마크업 계약 | 레지스트리 1차 + `kt-` 유틸리티 접두 |
| D-11 채널 | Release tarball + git+https | 동일 + 태그 불변 | 동일 + wheel 자산 + raw URL |
| D-12 토큰 | `--kt-`, 모든 semantic `.dark` 필수 | 동일 + 활성 파일 명시 import + contrast baseline | `--kt-`, 앱 오버라이드 dark 선택, contrast 앱 enforce |
| D-13 UX | G0~G9 전부 + C1~C22 제안대로 | 신규 MUST/기존 baseline, grep report | MUST 8 + diff-based 게이트 |

**D-06** — 실현성: 단일 정확값은 airport TS 7→5.9 하향·map npm 12→11 하향·map `next 16.2.12` exact와 충돌(`inv/map` §9). Python `>=3.12`는 map·wx·ktdm(3.11 floor) 설치 불가(`be` §2.1). 세 안 모두 npm floor 11.19 오류(§6 F-01/F-02). 승자: **risk-first 3열 + 보정**. 권고: `versions.json`은 축마다 `floor`(fail 후보)·`recommended`·앱별 `pin`을 두고, 강제는 floor 위반·blocked·floating만. 값: Node floor 22.12/rec 22.23; **npm floor 10.9(Node 22 동봉)/rec 11.19, map 12.0.1 예외**; Next 16.2/16.3; React 19.0/19.2; TS 5.9/5.9.3(airport 7 예외); Tailwind 4.3.0/4.3.3; base-ui 1.6/1.8; Vitest 4.1; Python common 3.11 호환·앱 rec 3.12; uv 0.11/0.12; fastapi 0.115/0.141(starlette 미핀); Actions major 강제 없음(SHA 핀 권고). **P1**(틀리면 도입 첫날 4~7 CI red 또는 py 설치 불가).

**D-07** — 실현성: 정확 핀 재작성은 6 저장소 `package.json`·`pyproject` PR 6개(가치 0). 즉시 fail 3종은 pinvi etl `@main`(`be` §5.1)과 RustFS/mc `latest`(dm·map·ktc·pinvi dev, `vm` §3.4) 때문에 첫날 red → 아무도 워크플로를 켜지 않는다. 승자: **velocity 모드 모델 + risk 판정 어휘·예외 만료**. 권고: `tools/check_versions.py` 판정 `OK/BELOW_FLOOR/ABOVE_MAX/NOT_RECOMMENDED/NO_LOCK/FLOATING_REF/BLOCKED/EXEMPT(만료)`, 기본 `report`(exit 0)이되 `FLOATING_REF`·`BLOCKED`는 `::error::` 주석으로 항상 표시; `fail` 전환은 매니페스트 `versions.enforce`로 앱이 선언하고, 그 앱의 lock/@main 정리 task(T-48x) 완료가 조건. lockfile 없는 4곳은 `NO_LOCK` report만. Renovate 미확인 → dependabot 템플릿. **P1**.

**D-08** — 실현성: weather는 `@import "tailwindcss"` 한 줄로 bare element 23종이 무스타일이 된다(`inv/weather` §9.1) → risk-first의 "theme+utilities만 먼저, preflight 마지막" 단계가 필수. 동시에 CSS 40~48%를 common 부품으로 바꾸는 작업은 ui v0.2(셸·패널·폼) 이후여야 두 번 하지 않는다(velocity 순서). geo `@config` 실효값 확인(T-441①)은 빌드 1회로 끝나는 싼 작업이며 없으면 색이 조용히 바뀐다(`dt` §5-3). dm은 Next 14→16·React 18→19를 v4 정리와 분리(세 안 합의). 승자: **merged(risk 단계 + velocity 순서)**. 권고 순서: ① airport WIP 병합(값 유지, `cn`→clsx+twMerge, devDeps 이동) ② geo `@config` 실효값 검증 → `@theme` 단일화(React 19와 독립) ③ concierge fallback 블록·`@config` 제거(CI 신설 후) ④ pinvi admin 스코프만 매핑, 사용자 preset·mobile 예외 ⑤ dm 업그레이드 PR 2개 후 `@theme`→`--kt-` 매핑, `ops-*` 잔존 허용 ⑥ weather: tokens.css 교체 → Next 16/Vitest 4/Node 22 → theme+utilities(preflight 제외) → ui v0.2 후 셸/패널/폼 3분할 → preflight. 모든 단계는 6폭 스크린샷 기준선 evidence. **P1**(weather 2,495행을 두 번 옮기게 됨).

**D-09** — 실현성: 세 안이 엔진·React 범위·Button 계약에서 합의. 차이는 DataTable 정렬 기본값뿐. `sortMode` 필수 prop(risk)은 map DataTable 호출부 전수에 prop 추가를 강제한다(페이지 파일 변경 = velocity D-23 원칙 위반). pinvi는 이미 `AdminTable` 어댑터가 `manualSorting={false}`를 명시하므로(`ui` §3.3 사실) "조용한 기본값" 위험은 map·pinvi에 없다. 승자: **merged(velocity 기본값 + risk 계약 항목)**. 권고: overlay만 `@base-ui/react`, 비-overlay는 native; React 19 전용(peer `^19.0.0`); Button `type="button"` 명시 기본·`loading`=aria-disabled+포커스 유지·root opacity 금지; Checkbox native + `data-slot=checkbox`; DataTable `manualSorting` 기본 true + `enableSortingRemoval`·`rowTestId`·`containerTestId`·`stickyHeader`·sr-only 문구 계약 포함; geo `VirtualTable` 잔류. base-ui `type`·hidden input·Toast API는 T-201에서 소스 확인 후 릴리스. **P2**.

**D-10** — 실현성(핵심): registry 복사(A)는 "수정 1회 전파"를 포기한다 — geo가 T-302/T-303으로 이미 치른 반복 동기화 비용(`prior` §3.2)이 그대로 남고, velocity 자신이 `patched≥3 → npm 전환` 트리거를 둔다. npm(B)의 비용은 `@source` 1줄·peer 정렬(base-ui 1.5/1.6→1.8)·webpack/Turbopack 스모크·pinvi 확장 prop 흡수인데, 이는 A로 가도 결국 2차 부품에서 다시 치른다. 클래스 이름은 velocity의 `kt-` 네임스페이스가 옳다: pinvi 사용자 preset(`primary`·`ink`·`canvas`)과의 충돌 여부를 `@config` 병합 규칙 미확인 상태에서 검증할 수 없으므로(`dt` §5-3) 충돌 0인 이름이 안전하고, **npm 패키지 내부 클래스가 `kt-`면 map 페이지 파일은 한 줄도 바뀌지 않는다**(map ui/ 파일은 어차피 패키지 import shim으로 대체). 승자: **merged**. 권고: `@kor-travel/ui` = ESM + d.ts + Tailwind 소스 클래스(`bg-kt-surface-page`, `h-kt-control`, `rounded-kt-control`, `text-kt-2xs`), `theme.css`가 `--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--text-kt-*` 정의, 앱 별칭은 앱 소유. 소비자 필수 2줄(`@import "@kor-travel/tokens/theme.css"`, `@source "../node_modules/@kor-travel/ui"`), `base.css`/`base.scoped.css` 2변형, `@kor-travel/ui/cn`(extendTailwindMerge 등록형) 제공. 마크업 계약은 `docs/standards/ui-contract.md`. 레지스트리는 셸 골격·로그인 페이지·playwright 기준선 템플릿에만. **P1**(방식을 바꾸면 pinvi 28·map 32·concierge 18 파일을 두 번 만진다).

**D-11** — 승자: velocity(+wheel 자산). 권고: 태그 `tokens-vX.Y.Z`/`ui-vX.Y.Z`/`py-vX.Y.Z` 불변, Release 자산 tarball·wheel, Python `git+https@py-vX.Y.Z#subdirectory=…`(lock sha) 또는 wheel URL, 공개 npm/PyPI는 Phase 5. 전제: 저장소 공개(§7 O-16). **P2**.

**D-12** — 실현성: 앱 오버라이드에 `.dark` 값 필수는 geo·pinvi·ktdm에 값 발명 부담이고 검증 수단이 없다(`dt` §3.2.2). contrast 즉시 fail은 geo·concierge·ktdm·airport 첫날 red(`dt` §3.4.2). 승자: **merged(velocity 다크·risk 활성화 규칙·contrast report)**. 권고: `--kt-*` 2단(semantic ← app override); `tokens.css`는 map 기본값 + `.dark` 완비, 앱 오버라이드의 dark는 선택; 활성화 파일은 앱이 명시 import, 기본 `color-scheme: light`; shadcn alias 의미 고정(`--input`=control-line, `--accent`=brand-tint); `kt_contrast` report 기본·앱 `contrast.enforce` 선언; **font 스택 토큰은 v0.1 채택 시 앱이 현재 스택으로 오버라이드**(§5 M-03). **P2**.

**D-13** — 승자: **velocity(MUST 8 + diff-based) + risk C1~C22 판정표**. diff-based는 앱별 baseline 파일 유지가 필요 없어 더 싸고, `git diff -U0` 추가 줄만 검사하면 줄 이동 오탐도 없다. 권고: `ux-guide.md`(admin/사용자 장 분리, `UX-Gn.m` ID), `responsive-web.md`(1024 전환·검사 폭 6·터치 36/30·44·48), `tools/ux_grep_gate.py` diff-based report; 기존 `window.confirm` 7건은 목록화만. pinvi 예외 3건(C1·C5·C6) 등록. **P3**.

### C. 백엔드·API

| ID | coordinator | risk-first | velocity-first |
|---|---|---|---|
| D-14 OpenAPI | MUST 전면 + 예외 | 3계층(즉시 additive / 신규 MUST·기존 SHOULD / SHOULD) + yaml | 신규 MUST·기존 SHOULD + md |
| D-15 Python | 1차 C4·C12·C13·C20; 접두 이관 P2 | 동일 + format 미포함·C5 `exclude_paths` | 동일; 접두 영구 예외 |
| D-16 첫 소비자 | map + pinvi admin | tokens map+weather+airport / ui map+airport | map + pinvi(L6 지연 시 airport 승격) |

**D-14** — 승자: **merged(risk 3계층, 단 M1은 Phase 3 task)**. 권고: 즉시 MUST는 응답 본문을 바꾸지 않는 것만(M2·M4·M9·N6·N7); M1(export+`--check`)은 pinvi·ktc·ktdm에 파이프라인 신설이 필요하므로 Phase 3 앱 task; M3·M5·M6·M7·M8·N1~N5·N8은 신규 표면 MUST / 기존 표면 SHOULD + `openapi-exceptions.yaml`(review 날짜 필수); health 별칭 무기한; 429 코드명·헤더 AppId는 앱 소유(형식 규칙만). map 산출물 변경 시 pinvi/ktdm pin 갱신 PR 동반 없이는 머지 금지. **P1**(pinvi 모바일·concierge 외부 계약 파손).

**D-15** — 승자: **merged**. 권고: py-v0.1 = `quality`(ruff extend·mypy 베이스, format 미포함)·`openapi` export CLI·`time`·`fastapi.health`(별칭 인자); `[api]` extra는 starlette 미핀(map `<1.0` 상한, T-414 재검증까지); 2차 settings·db·request_id·problem(opt-in, `exclude_paths`); 메트릭 접두 map·pinvi **영구 예외**(대시보드 5종 회귀 > 통일 이득). **P2**.

**D-16** — 실현성: coordinator의 map+pinvi 1차는 B1/B9(`lic` §4)에 걸려 pinvi PR을 열 수 없다. L6은 사용자 단독 권리자의 1 PR·3파일 결정이므로 빨리 닫힐 수 있지만 common이 통제할 수 없다. weather `tokens.css` 교체는 순수 CSS 2~3파일이라 두 번째 tokens 소비자로 가장 싸다(Next 15 그대로 가능). airport는 WIP 병합이 외부 선행. 승자: **merged**. 권고: tokens 1차 = **map + weather**(즉시), airport는 WIP 병합 즉시 추가. ui 1차 = **map + pinvi admin, 단 T-2xx 착수 전 L6 PR 머지가 조건**; 미충족 시 airport 소형 부품(백업·collector 패널)으로 대체. Python 1차 = map-api·weather-api·airport. concierge·ktdm은 L8 후. **P0**(라이선스 미결 상태에서 GPL 코드를 pinvi에 넣으면 되돌리기 비용이 법적·기술적 모두 큼).

### D. 라이선스·운영·신규

| ID | 판정 |
|---|---|
| D-17 라이선스 | 세 안 합의(GPL-3.0-or-later, §7 예외 기각, pinvi 추출 금지 B1, SPDX 헤더·PROVENANCE·THIRD_PARTY_NOTICES). 승자: risk-first(추출 gate B1~B10을 task 선행 조건으로). **P0** |
| D-18 CI·릴리스 | 실현성: 재사용 워크플로로 앱 CI를 대체하면 map required check 8개·pinvi ruleset이 `Expected`에 갇힌다(`ci` §2.3). 승자: **velocity(앱당 job 1개 추가) + risk 하드닝**. 권고: Phase 1 `versions-check.yml`·`contrast-check.yml`(+registry-drift는 템플릿 채널용), Phase 3 `openapi-drift.yml`·`typegen-drift.yml`, `python-quality`/`node-quality`는 **concierge CI 신설(T-450) 직전**에만 필요(제로 베이스 앱에는 오히려 가장 싼 경로). 소비자는 태그/SHA 참조, job `name:` 입력 개방, 운영 호출 job required 금지. **P2** |
| D-19 pinvi 사용자·모바일 / 매니페스트 | 둘 다 채택: 사용자 표면·모바일은 코드 소비 대상 아님(`tokens.json`만); 소비자 매니페스트 `kor-travel-common.lock.json` 1파일이 버전·drift·contrast·UX 게이트의 단일 입력. **P2** |
| D-20 airport Admin 정의 | 합의: 현 백업 패널 + collector 패널 + `/v1/admin/*`. 셸·로그인 소비는 T-035 이후 BLOCKED. **P2** |
| D-21 시각 기준선 의무 | risk-first 채택하되 **저장소 파일이 아닌 PR evidence**로(7앱 PR 7개 유발 금지). Playwright 없는 wx·ktdm은 템플릿 스크립트 임시 사용. **P2** |
| D-22 헤더·메트릭 접두 | 합의: 형식 규칙만, 기존 접두 예외. **P3** |
| D-23 공유 라이브러리 정책 / 이관 PR 규격 | 둘 다 채택: `maplibre-vworld-*`·`python-*-api` SHA는 `providers` 절에 보고만, 정리는 T-5xx 결정 요청; 이관 PR은 1 PR = 1 산출물, 파일 상한(tokens 10 / ui 30 / py 10), 되돌리기 명령 명시. **P2** |
| D-24 되돌리기 / 회수 측정 | 둘 다 채택: 업그레이드 PR과 채택 PR 분리, 단일 revert 가능; 분기별 `docs/reports/adoption-*.md`에 drift·EXEMPT·enforce 전환 수. **P3** |
| D-25 NOT_RUN 표기 | risk-first 채택. **P2**(0 test를 pass로 집계하면 gate 형식화) |
| D-26 마커 팔레트 | 합의: map 소유, common은 16슬롯 규칙 문서만. **P3** |
| D-27 decisions.md·도구 언어·링크 | 합의: 미보유·Python·상대 링크만. **P3** |

## 3. 앱별 이관 비용 재추정(추정; 기준 = §2 병합안)

| 앱 | 외부 선행 | PR 수(추정) | 주요 변경 규모 | 회귀 게이트(사실) | 위험 |
|---|---|---|---|---|---|
| map | 없음 | 4~5: tokens(6) → ui v0.1 shim(~15) → ui v0.2(~20, Checkbox 3파일) → py(~4 + pinvi/ktdm pin 갱신) → `LICENSE` 전문(비차단) | 페이지 파일 무변경; `verify-*.mjs`·`test_frontend_dependency_security.py` 상수 갱신은 Next 상향 PR에만 | e2e 30·vitest 42·audit·verify 4종 | 낮~중. map 산출물 변경 = pinvi·ktdm pin 파손(P1) |
| pinvi admin | **L6**(1 PR 3파일) | 5: L6 → tokens(admin 블록·`base.scoped.css`·매니페스트 ~6) → ui v0.1(15 shim + `cn` 별칭) → ui v0.2(`AdminTable` 어댑터 유지 ~12) → py(export 신설·drift CI·`uv.lock` 소비 ~6) | 사용자 표면 무변경이 조건(`app-shell-mobile` e2e) | e2e 56 + 44px 단언·vitest 27·aggregate gate | 중. webpack 강제(ADR-066) 환경 스모크 필수 |
| airport | **WIP 병합**(사용자) | 4~5: WIP 정렬(~8) → tokens(`dark-media.css`·contrast baseline ~4) → 소형 ui(백업·collector ~6) → py(`code`/`request_id` additive·`--check` CI·`uv sync --locked` ~5) → TS7/ESLint 판정 | 셸·로그인 소비 없음 | vitest·tsc·build·live-e2e(required 제외 권고) | 낮~중 |
| weather | 없음 | 8~9: 기준선 evidence → tokens.css(2~3, font 스택 오버라이드) → Next 16/Vitest 4/Node 22 → v4 theme+utilities → 셸/패널/폼 3분할(ui v0.2 후) → preflight+잔존 CSS → py | CSS 2,495행·13 TSX·220 className(`inv/weather` §9.1) | Playwright 없음 → 수동 6폭 | **높음**(검증 수단 부재) |
| geo | **React 19 ADR** | 6~7: Node 22 CI + `uv.lock` → `@config` 실효값 evidence + `@theme` 단일화 + tokens → React 19 → radix→base-ui + ui(12파일·`asChild` 17곳) → py(health 별칭·securitySchemes+typegen) ; VirtualTable 잔류 | e2e 셀렉터 계약(`section.panel .panel-header h2`, `pre.json-box`) | unit 43·e2e 23·a11y 4 | **높음(UI)**. 셀렉터 diff evidence 필수 |
| concierge | **L8**, CI 신설 | 6~7: pyproject/uv + ruff baseline → CI 신설 → L8 → fallback/`@config`/`--ktc-` → ui 18종(base-ui 1.8) → py export/request-id | `ReviewWorkspace.tsx` 4,386줄 미접촉 | 로컬 4 gate → 신설 CI·e2e 45 | 중~높(제로 베이스) |
| ktdm | **L8**, 업그레이드 사유 문서 없음 | 6: Next 16/React 19/ESLint 9/Node 22(재포맷 금지) → Poetry→uv → L8 → tokens(Ember 유지·tint 4종) → ui 부분(StatStrip·AppErrorPanel) → py request-id | recharts 3·`target es5` 미검증(`inv/ktdm` §11-1) | vitest 8, Playwright 없음 | **높음**(업그레이드) |
| pinvi mobile | NativeWind 5 GA | 0 | 예외 등록 | — | — |

합계(추정): 소비자 PR 39~44개, 그중 외부 선행에 막힌 트랙 4개(pinvi·airport·geo·ktc/ktdm). common 자체 Phase 0~3 task 약 40개.

### 3.1 앱별 PR 순서(병합안; 각 PR = 단일 revert 단위)

규칙: 프레임워크 업그레이드 PR과 common 채택 PR을 한 PR에 묶지 않는다(`prior` §2, risk R2, velocity D-23). "evidence"는 PR 본문 첨부(저장소 파일 아님).

**map**(외부 선행 없음)

| # | PR | 선행 | gate | 되돌리기 |
|---|---|---|---|---|
| 1 | tokens: `globals.css` → `@import "@kor-travel/tokens"` + `brand.css`(빈 오버라이드) + 매니페스트 + `versions-check` job | tokens-v0.1 | 6폭 스크린샷 diff 0·e2e 30·vitest 42 | revert + lock 복원 |
| 2 | ui v0.1: `components/ui/{badge,skeleton,separator,card,alert,input,textarea,native-select,field}` → shim(`export * from "@kor-travel/ui/<x>"`), `@source` 1줄 | ui-v0.1 | e2e 30·`verify:frontend-eslint`(shim 파일 lint 대상 집합 갱신) | revert |
| 3 | ui v0.2: Button·overlay·Table·DataTable·Pager shim, Checkbox 호출부 3파일 시그니처 | ui-v0.2 | e2e 30·vitest 42·`data-table.test.tsx` 175줄 이관 | revert |
| 4 | py v0.1: export CLI 교체·health 팩토리·ruff extend; **동일 PR에 pinvi/ktdm pin 갱신 요청 링크** | py-v0.1 | `openapi.yml` 3 profile 무변경 단언 | revert |
| 5 | (비차단) `LICENSE` 전문 복원(L9)·`license` 필드 | — | docs | — |
| 별도 | Next 16.3·base-ui 1.8·Playwright 1.63 상향은 `verify-next-sharp.mjs` 상수·`test_frontend_dependency_security.py`·이미지 갱신 동반(`inv/map` §9) | — | 전 CI | — |

**pinvi admin**(외부 선행 L6)

| # | PR | 선행 | gate | 비고 |
|---|---|---|---|---|
| 0 | L6: 루트 `LICENSE`·`apps/api/pyproject` license·README/AGENTS 정합·`maplibre-vworld.md:23` | 사용자 | docs | 3파일, 사용자 결정 O-1 |
| 1 | tokens: admin `@theme` `--color-admin-*` → `--kt-*` 오버라이드 + 기존 이름 별칭 유지, `base.scoped.css`, 매니페스트, job | 0, tokens-v0.1 | `app-shell-mobile` e2e(사용자 표면 무변경)·admin e2e | 페이지 무변경 |
| 2 | ui v0.1: `components/admin/ui/*` 15파일 shim, `@/lib/admin/cn` → `@kor-travel/ui/cn` 재수출 | 1, ui-v0.1 | e2e 56·vitest 27·webpack 빌드 | `AdminPage` 어댑터 무변경 |
| 3 | ui v0.2: overlay(`hasUnsavedInput`·`viewportProps` 흡수 확인)·Table·DataTable shim, `AdminTable` 어댑터 유지 | 2, ui-v0.2 | e2e 5파일 testid 계약·44px 단언 | `manualSorting={false}` 어댑터 그대로 |
| 4 | py: export 신설·`openapi-drift.yml`·securitySchemes(additive)·`uv.lock` CI/Docker 소비·etl `@main` 제거 | py-v0.1 | api.yml·etl.yml·contract-pin | 이후 `versions.enforce` 전환 가능 |

**airport**(외부 선행 WIP 병합)

| # | PR | 선행 | gate |
|---|---|---|---|
| 0 | WIP `codex/shadcn-ui-foundation` 병합(값 유지) | 사용자 | frontend CI(vitest·tsc·build) |
| 1 | 정렬: `cn`→clsx+twMerge, `shadcn`/`postcss`/`@tailwindcss/postcss` devDeps, `engines`, Button을 D-09 레시피로 | 0 | build·vitest 10 |
| 2 | tokens: alias 재매핑 30곳 유지 + `dark-media.css` + contrast baseline(line 1.15 등록) | 1, tokens-v0.1 | build·320px 게이트 evidence |
| 3 | 소형 ui: 백업 패널·collector 패널에 Alert·StatStrip·SectionCard·EmptyState | 2, ui-v0.1 | build·vitest |
| 4 | py: `code`/`request_id` additive·스펙 422 정합·`--check` CI·Docker `uv sync --locked` | py-v0.1 | backend CI(alembic check 유지) |
| 5 | TS 7 예외 등록 + ESLint 도입 판정 + 절대 링크 상대화 + placeholder 치환 | T-004 | CI |

**weather**(외부 선행 없음; 가장 긴 트랙)

| # | PR | 선행 | gate |
|---|---|---|---|
| 1 | tokens: `app/tokens.css` → 패키지 `tokens.css` + navy 오버라이드 + **font 스택 오버라이드(M-03)** + 매니페스트 | tokens-v0.1 | 6폭 스크린샷 diff 0(수동) |
| 2 | Next 16·Vitest 4·Node 22 CI·`eslint-config-next` 16·`moduleResolution: bundler`·react-query 미사용 정리·CI에 vitest/mypy 추가 | — | ci.yml |
| 3 | v4 도입: `@import "tailwindcss/theme" layer(theme)` + `utilities`만(preflight 제외), `@theme inline` 1:1 매핑 | 2 | 스크린샷 diff |
| 4~6 | 셸 / 패널·표 / 폼·로그인 → common 부품, 해당 CSS 절 삭제(3분할, 각 ≤30파일) | 3, ui-v0.2 | 스크린샷 diff·vitest |
| 7 | preflight 활성화 + 잔존 도메인 CSS `@layer components`(workbench·Dagster·마커 ~800행) + 마커 색 토큰화 | 6 | 스크린샷 diff |
| 8 | py: export `--check` 전환·`code` 사전·L15 airkorea 정본 결정 | py-v0.1 | ci.yml |

**geo**(외부 선행 React 19 ADR)

| # | PR | 선행 | gate |
|---|---|---|---|
| 1 | Node 22 CI + `uv.lock` 도입 + pre-commit `language: system` | — | ci.yml |
| 2 | `@config` 실효값 빌드 evidence → `@theme` 단일화 + `tailwind.config.ts` 삭제 + tokens(`--ui-*` 별칭 유지) + contrast baseline(2.29/2.41 등록) | tokens-v0.1 | 시각 diff·e2e 23 |
| 3 | React 19 업그레이드(ADR-019 갱신) | 사용자 | unit 43·e2e 23 |
| 4 | radix→base-ui(12파일·`asChild` 17곳) + ui v0.1/0.2 shim; `Panel`→`SectionCard`는 **셀렉터 diff evidence 후에만**(`section.panel .panel-header h2`) | 3, ui-v0.2 | e2e·a11y 4 spec |
| 5 | py: health 별칭 병행·export 교체·securitySchemes + typegen 재생성 | py-v0.1 | openapi drift·`gen:types` |

**concierge**(외부 선행 L8; CI 제로 베이스)

| # | PR | 선행 | gate |
|---|---|---|---|
| 1 | `pyproject.toml`·`uv.lock`(`mcp<2` blocked 반영)·ruff/mypy baseline(per-file-ignores) | — | 로컬 4 gate |
| 2 | CI 신설(`python-quality`·`node-quality` 재사용 호출 + `versions-check`) + production `frontend/Dockerfile` | 1, 워크플로 | CI green |
| 3 | L8: 루트 GPL-3.0-or-later + `THIRD_PARTY_NOTICES` | 사용자 | docs |
| 4 | fallback 블록 제거 → `@config`→`@theme inline` → `--ktc-*`를 `--kt-*` 오버라이드로(이름만) + contrast baseline(2.06/1.93) | 2, tokens-v0.1 | e2e 45·시각 diff |
| 5 | ui 18종 shim + base-ui 1.5→1.8 + `render` 9줄 관용구 | 3·4, ui-v0.2 | e2e 45 |
| 6 | py: export 신설·request-id; features export 계약 문서화(map provider 동시 수정 계획) | py-v0.1 | CI |

**ktdm**(외부 선행 L8; 업그레이드 위험 최대)

| # | PR | 선행 | gate |
|---|---|---|---|
| 1 | Next 14→16·React 18→19·ESLint 8→9·Node 22 CI(재포맷 금지; recharts 3·`target es5` 실검증) | 사용자(사유 문서 없음) | vitest 8·build |
| 2 | Poetry→`uv.lock`·하한 상향·CI 핀 정리 | — | ci.yml |
| 3 | L8 | 사용자 | docs |
| 4 | tokens: `@theme` 20색 → `--kt-*` 별칭(Ember 유지) + tint 4종 + contrast baseline(brand 3.59) | 1, tokens-v0.1 | 스크린샷 diff(수동) |
| 5 | ui 부분: StatStrip·AppErrorPanel·SectionCard(`ops-*` 잔존 허용) | 3·4, ui-v0.2 | vitest |
| 6 | py: request-id(`trust_incoming=False`)·quality baseline | py-v0.1 | ci.yml |

## 4. task DAG 실현성

### 4.1 두 레지스터의 "첫 5개" 검증

| 레지스터 | task | 선행 없음 주장 | 실제 |
|---|---|---|---|
| risk | T-001 AGENTS/CLAUDE/SKILL/README/docs README | ✓ | 즉시 가능 |
| risk | T-002 tasks.md 초기화 + docs.yml 링크 17건 해소 + validator 정정 | △ | 링크 17건 중 대부분이 T-007 runbook(`agent-workflow.md`·`consumer-adoption.md`·`release.md`) 부재(`cv` §1.3) → **T-007에 묶임**. stub 파일 생성을 T-002 범위에 명시해야 무선행이 성립 |
| risk | T-003 NOTICE·THIRD_PARTY·PROVENANCE·SPDX 린트 | ✓ | 즉시 가능 |
| risk | T-004 ADR-001~006 | △ | ADR-001(배포 단위·scope 이름)·006(채널)은 T-006 scope 확인과 사용자 열림에 의존 → `proposed` 상태로 작성하면 성립 |
| risk | T-005 versions.json + check_versions(판정 8종) + 7 소비자 현재값·예외 | △ | 무선행이지만 범위 과대(3 lock 파서 + 7 저장소 등록). npm lock v3 파서 + report만 먼저, uv/poetry 파서는 `T-005a/b` |
| velocity | T-001 문서 골격 + resume/journal/tasks.md | ✓ | 즉시 가능 |
| velocity | T-002 ADR-001~006(레지스트리 1차·`kt-`·floor/target·강제 3단·라이선스) | ✗ | 자기 열림 O3(배포 방식)·O4(네임스페이스)가 "설계 차단"으로 표기돼 있어 사용자 답 전에는 accepted 불가 |
| velocity | T-003 validator 정정·LF·docs.yml 시점 | ✓ | 즉시 가능 |
| velocity | T-004 versions.json + npm/uv/poetry 파서 + report/warn/fail + 테스트 | △ | 과대. 분할 필요 |
| velocity | T-005 고지 파일 + check_spdx | ✓ | 즉시 가능 |

### 4.2 선행 관계가 비현실적인 항목

| 항목 | 문제 | 보정 |
|---|---|---|
| risk T-410(map tokens) ← T-402(7앱 기준선 캡처) | 다른 6앱의 캡처가 map 채택을 막는다 | 기준선 캡처를 앱 task 안으로(T-410 evidence), T-402는 템플릿만 |
| risk T-461(weather tokens.css) ← T-460(Next 16·Vitest 4·Node 22) | tokens.css는 순수 CSS라 Next 버전과 무관(`inv/weather` §8-1) | T-461 선행 = T-109만; T-460은 T-462(v4 도입) 선행으로 이동 |
| risk T-010 재사용 워크플로 5종(Phase 0) → T-403 7 저장소 CI 정렬 | `node-quality`/`python-quality`는 map·pinvi required check 재구성을 유발 | Phase 0에는 `versions-check`·`contrast-check`만; quality 2종은 T-450 직전 |
| risk D-07 즉시 fail 3종 | T-484(pinvi `@main` 제거)·`latest` 정리 전에는 fail 불가 | report + `::error::`; fail은 앱 선언 |
| velocity T-410 ← T-400(공통 이관 절차 확정) ← T-009 runbook | 절차 문서 완성이 첫 채택을 막음 | T-400은 T-410과 병행, 첫 채택 PR이 절차의 검증 사례 |
| velocity T-500(첫 정식 릴리스) ← T-420·T-421(pinvi) | L6 미결이면 정식 릴리스 자체가 지연 | 정식 릴리스 조건 = "GPL 소비자 2곳 스모크"(map + weather/airport) |
| 양쪽: Python 소비 task를 앱 대역(T-41x·T-42x…)에 배치 | `docs/tasks-rule.md` §2.1은 T-480~T-489 = Python 백엔드 소비 | §5 M-12 규칙 보정(앱 대역에 "버전 정렬·lock·CI"는 허용, 모듈 채택은 T-48x) |
| 양쪽: T-4xx 대역 31개(velocity)/33개(risk) | 앱당 10 슬롯(예: T-460~469)으로 weather 8~9 PR을 담기 빠듯 | 하위 `a~z` 접미(`validate_plan` 허용)로 흡수 |

### 4.3 즉시 시작 가능한 첫 5개(병합 제안, 전부 선행 없음·Windows Python으로 실행 가능)

| ID | 제목 | Gate |
|---|---|---|
| T-001 | 문서 골격: `AGENTS.md`(공통 절 A~I + 로컬 절)·`CLAUDE.md`(≤40줄)·`SKILL.md`·`README.md`·`docs/README.md`·`resume.md`·`journal.md`·`tasks.md` + runbook **stub 4종**(링크 17건 해소) | 문서 검증 |
| T-002 | 검증 도구 정정: `validate_document_links.py` 절대 접두 제거, `.py` LF 정규화, `docs.yml` 하드닝·필수화 시점, `tools` job ubuntu+windows 매트릭스 | 도구 단위 테스트·CI |
| T-003 | 고지·출처: `NOTICE`·`THIRD_PARTY_NOTICES.md`·`LICENSES/`·`PROVENANCE.md`·`CONTRIBUTING.md`(B8)·`tools/check_spdx.py` | 문서 검증·도구 테스트 |
| T-004 | `versions.json` v1(floor/recommended/pin·exceptions·blocked·providers) + `tools/check_versions.py` npm lock v3 파서·report 모드·판정 8종 + 7 소비자 현재값 등록 (`T-004a` uv.lock 파서, `T-004b` poetry.lock 파서) | 도구 단위 테스트 |
| T-005 | ADR-001~006 `proposed`(배포 단위·배포 방식·`--kt-`/`kt-`·floor/recommended·강제 모드·라이선스) + `docs/adr/README.md` 단일 색인; 사용자 답(§7) 반영 시 `accepted` | 2인 리뷰 |
| (T-006) | npm scope·PyPI 이름 확인(사용자 계정 작업) | 외부 |

critical path(병합): T-001/003/004 → T-101 tokens → T-108 릴리스 → **T-410 map tokens ∥ T-461 weather tokens** → T-201 ui 골격(base-ui 확인) → T-203 소형 → T-212 ui v0.1 → T-411 map ∥ (L6 후) T-421 pinvi → T-208 DataTable → T-213 ui v0.2 → T-412/T-422. 병행: T-302 → T-303/304/305 → T-311 py v0.1 → T-480 map-api/T-481 weather-api/T-482 airport. 외부 선행 4개(L6·WIP·React 19 ADR·L8)가 각 트랙의 실제 시작점을 정한다.

### 4.4 병합 DAG(common 측 task; ID는 `docs/tasks-rule.md` §2 대역, 상태는 `validate_plan.py` 규칙대로 선행 DONE 전 BLOCKED)

| ID | 제목(요약) | 선행 | 외부 선행 | Gate |
|---|---|---|---|---|
| T-001 | 문서 골격 + runbook stub 4종 | 없음 | — | 문서 검증 |
| T-002 | validator 정정·LF·docs.yml 하드닝·tools windows 매트릭스 | 없음 | — | 도구 테스트·CI |
| T-003 | 고지 파일·PROVENANCE·`check_spdx.py` | 없음 | — | 도구 테스트 |
| T-004 | `versions.json` v1 + `check_versions.py`(npm lock v3, report) + 7 소비자 등록 | 없음 | — | 도구 테스트 |
| T-004a/b | uv.lock / poetry.lock 파서 | T-004 | — | 도구 테스트 |
| T-005 | ADR-001~006(`proposed`) + 단일 색인 | 없음 | 사용자 O-3·O-4·O-1 답 시 accepted | 2인 리뷰 |
| T-006 | npm scope·PyPI 이름 확인 | 없음 | 사용자 계정 | 외부 |
| T-007 | runbooks 본문(agent-workflow·consumer-adoption·release·dev-environment) + `templates/consumer-pr.md` | T-001 | — | 문서 검증 |
| T-008 | 매니페스트 스키마 `consumer-manifest.v1` + `validate_manifest.py` | T-004 | — | 도구 테스트 |
| T-009 | 재사용 워크플로 `versions-check.yml`·`contrast-check.yml` + selftest fixture | T-004, T-008 | — | selftest |
| T-010 | `docs/standards/{agent-conventions,versions,ci-deploy}.md` + AGENTS 공통 절 템플릿 | T-005, T-007 | — | 2인 리뷰 |
| T-011 | `docs/integration-map.md` 생성기(`collect_manifests.py`) + `consumers.pins.json` | T-008 | — | 도구 테스트 |
| T-101 | `packages/tokens`(tokens.css·theme.css `kt-` 네임스페이스·shadcn.css·base/base.scoped·dark-class/media·생성물) + pack 스모크 | T-003, T-005 | — | 빌드·tarball 설치 |
| T-102 | `kt_contrast.py`(report, 앱 enforce 플래그) + map 기본값 전 쌍 통과 테스트 | T-101 | — | 도구 테스트 |
| T-103 | `ux_grep_gate.py`(diff-based, 금지 7종 + `window.confirm` + `outline-none`) | T-001 | — | 도구 테스트 |
| T-104 | `design-tokens.md`(접두·계층·프로필·alias 의미·오버라이드 목록·다크·font 오버라이드 규칙 M-03) | T-101 | — | 2인 리뷰 |
| T-105 | `ux-guide.md`(MUST 8·G0~G9·C1~C22 판정·예외 등록) + `responsive-web.md` | T-001 | — | 2인 리뷰 |
| T-108 | tokens-v0.1.0-rc → map·weather 스모크 → 정식 | T-101, T-102, T-104 | — | consumer-smoke |
| T-201 | `packages/ui` 골격(subpath exports·`cn`·인라인 아이콘·peer react ^19) + base-ui 3건 소스 확인 + webpack/Turbopack pack 스모크 + `noUncheckedIndexedAccess` 타입 검사 | T-101 | — | 빌드·tarball |
| T-203 | 소형 12종 + 단위 테스트 | T-201 | — | 단위 테스트 |
| T-204 | `ui-contract.md`(data-slot·testid·heading·sr-only·SemVer 0.x 규칙 M-01) | T-203 | — | 2인 리뷰 |
| T-205 | Button + AppErrorPanel + error-recovery | T-203 | — | 단위 테스트 |
| T-206 | overlay 세트(pinvi 확장 흡수) + Table + native Checkbox | T-205 | — | 단위 테스트 |
| T-208 | DataTable(`manualSorting` 기본 true·removal·testid·sr-only) + Pager | T-206 | — | 단위 테스트·2인 리뷰 |
| T-209 | CopyButton·JsonViewer·DetailList(`onNotify`)·StatusBadge | T-206 | — | 단위 테스트 |
| T-210 | AdminPageHeader·SkipLink·RailGrid + Form 3종 + form-validation | T-206 | — | 단위 테스트 |
| T-211 | 레지스트리 채널(셸 골격·로그인 템플릿·playwright 기준선 템플릿)·`registry_drift.py` | T-210 | — | selftest |
| T-212 | ui-v0.1.0(소형) rc → map(+pinvi if L6 / airport) → 정식 | T-203, T-204 | L6 또는 WIP | consumer-smoke |
| T-213 | ui-v0.2.0(Button·overlay·Table·DataTable·Pager) | T-208, T-209, T-210 | — | consumer-smoke·2인 리뷰 |
| T-301 | `openapi.md`(3계층) + `openapi-exceptions.yaml` 초기 등록 | T-007 | — | 2인 리뷰 |
| T-302 | py 골격(hatchling·extras·3.11 문법·starlette 0.4x/1.6 매트릭스) + `backend-stack.md` | T-003 | — | wheel 설치 |
| T-303~305 | openapi export CLI / health+time / quality 산출물 | T-302 | — | 패키지 테스트 |
| T-306~308 | settings+db+api key / request_id+metrics / problem(opt-in)·security_headers·cors·testing·alembic 템플릿 | T-304 | — | 패키지 테스트 |
| T-309 | `openapi-drift.yml`·`typegen-drift.yml` + selftest | T-303, T-009 | — | selftest |
| T-311 | py-v0.1.0(1차) → weather-api·map-api 검증 → 정식(wheel 자산) | T-303, T-304, T-305 | — | 소비자 스모크 |
| T-401 | `python-quality.yml`·`node-quality.yml`(concierge 신설용) | T-009 | — | selftest |
| T-410~T-486 | §3.1 앱별 PR 순서 그대로(앱 대역; Python 모듈 채택은 T-48x+접미) | 각 PR 표 | L6·WIP·React19·L8 | 앱 CI |
| T-501 | 릴리스 runbook 1회 완주(rc→PR→정식→되돌리기 리허설) | T-108, T-212 | — | consumer-smoke |
| T-502 | gate 승격 절차(앱 선언·2회 green·만료 예외 감사) + 분기 감사 runbook | T-009, T-011 | — | 문서 검증 |
| T-503 | 회수 지표 1회차 보고 | T-411, T-461 | — | 문서 검증 |
| T-505 | 공유 라이브러리·마커 팔레트 정본 결정 요청 문서 | T-011 | 사용자·map | 문서 |
| T-507 | 공개 npm/PyPI·Renovate·Vitest 5·Node 24·react-table 9·lucide 1·mypy 2 재평가 | T-006, T-004 | — | 문서·도구 테스트 |

DAG 검증 포인트: (1) 사이클 없음 — 소비자 task는 common 릴리스 task만 선행으로 갖고 역방향 참조가 없다. (2) `READY`로 둘 수 있는 것은 T-001~T-006 6개뿐이며 나머지는 `BLOCKED`로 시작한다(`validate_plan.py` L137 규칙). (3) 외부 선행은 `선행` 열에 넣지 않고 `외부 선행` 줄로 적어야 파서를 통과한다(`cv` §4.1).

## 5. 세 레지스터 모두에서 빠진 결정(missing) + 기본값 제안

| ID | 빠진 결정 | 왜 이관 비용에 중요한가 | 기본값 제안 |
|---|---|---|---|
| M-01 | 패키지 릴리스 버전 규칙(SemVer 0.x 취급) | `prior` §8 E7이 "0.x라도 무통보 파괴 금지"를 권고했으나 세 안 모두 minor/patch 경계·패키지 간 호환 표를 정하지 않음 → 소비자가 어느 범위를 caret으로 둘지 모른다 | 0.x에서 **minor = 마크업·prop·토큰 이름 변경 허용(CHANGELOG 이관 절 필수)**, patch = additive만; `ui`는 `tokens` 같은 minor를 peer로 선언; 1.0은 GPL 소비자 3곳 채택 후. 소비자는 `~0.N` 범위 |
| M-02 | 소비자 채택 상태 추적의 단일 정본 | velocity 매니페스트·risk `integration-map.md`+`consumers.pins.json`·coordinator `integration-map.md`가 병존하면 세 곳이 어긋난다 | 기계 정본 = 각 앱 매니페스트; common `docs/integration-map.md`는 `tools/collect_manifests.py`가 `consumers.pins.json` 체크아웃에서 **생성**(수기 편집 금지), 분기 감사 시 갱신 |
| M-03 | 폰트 로딩 책임 **과 v0.1 토큰의 font 스택** | `--kt-font-sans` Pretendard 1순위를 tokens.css에 넣으면 weather(Geist 1순위, 미로딩)·ktdm(Noto 1순위)·airport·geo는 "값 diff 0" 채택이 깨진다(`dt` §3.1.4) | tokens.css는 스택 토큰을 제공하되 **채택 PR에서 앱이 현재 스택으로 오버라이드**; Pretendard 1순위 MUST는 앱이 Pretendard를 로드하는 경우(map·pinvi·ktc)에만; 로딩 방식 결정은 별도 앱 task |
| M-04 | 코드 주석·docstring 언어 | ktdm은 주석·커밋까지 한국어(`inv/ktdm` §9), 문서 정책은 Markdown만 다룸 | 코드 주석·docstring·사용자 문자열 한국어, 식별자·SPDX/Origin 헤더 키·CHANGELOG 절 제목 영어, 벤더링 원문 유지 |
| M-05 | Hallmark 스탬프 | risk C21(형식만)·velocity(registry 미포함)가 다르고, map은 styled 파일 전부에 스탬프를 강제(`inv/map` §9) → map이 ui 파일을 shim으로 바꿀 때 규칙 충돌 | common 소스는 SPDX 헤더만(스탬프 없음, common에 design.md 잠금 없음); map shim 파일은 map 규칙대로 스탬프 유지; drift 비교는 선두 주석 블록 정규화 |
| M-06 | e2e 셀렉터 계약 보존 | geo 40 스펙이 `section.panel .panel-header h2`·`pre.json-box`에, pinvi e2e가 testid에 결박(`inv/geo` §9, `ui` §3.3). velocity는 미언급 | `docs/standards/ui-contract.md`에 data-slot·testid·heading 구조·sr-only 문구를 계약으로; 채택 PR은 "셀렉터 diff" evidence 필수; 계약 변경은 0.x minor(이관 절 필수) |
| M-07 | `cn` 유틸 소유 | pinvi는 `extendTailwindMerge` 등록형(`inv/pinvi` §8-5) — 미등록 시 `h-kt-control`과 `h-8`이 충돌 해소 없이 병존 | `@kor-travel/ui/cn` = clsx + extendTailwindMerge(kt 커스텀 그룹 등록), 앱 `@/lib/utils`는 재수출 |
| M-08 | React Compiler·strict tsconfig 호환 | map은 `"use no memo"` 2곳(DataTable/VirtualizedTable, `inv/map` §3.1); pinvi는 `noUncheckedIndexedAccess`로 map 원문이 타입 오류(`ui` §3.3) | common CI 타입 검사는 `noUncheckedIndexedAccess: true`; 빌드는 React Compiler 미적용 + `'use client'`·`'use no memo'` 지시문 보존을 pack 스모크에서 단언 |
| M-09 | Windows 개발자 지원 수준 | 현 사용자 환경이 Windows(cwd `F:\dev`, PowerShell)이고 common 사본 `.py`가 CRLF였다(`cv` §1.2) | `tools/*.py`는 Windows Python 동작 필수(pathlib·`-X utf8`, `/tmp` 금지), CI `tools` job windows 매트릭스; 패키지 빌드·pack 스모크는 ubuntu만; runbook은 bash 표기 + "Git Bash에서 동일" 1줄 |
| M-10 | `docs/tasks-rule.md` §2.1 대역 보정 | Python 소비 task(앱당 2~3개)를 T-480~489 10슬롯에 담을 수 없어 두 레지스터가 앱 대역에 흩어 놓음 | 앱 대역에는 "버전 정렬·lock·CI·토큰·UI"만, Python 모듈 채택은 `T-48x` + `a~z` 접미(앱당 1 ID) — tasks-rule §2.1 한 줄 추가 |
| M-11 | 저장소 공개 여부 전제 | Release tarball 무인증 설치·raw URL·cross-repo 재사용 워크플로(`ci` §2.3 미확인) 모두 공개 전제 | common은 공개 GPL(기본); 비공개면 채널을 wheel/tarball + 토큰으로 재설계 |
| M-12 | 소비자 `engines` 선언 | 5앱이 `engines` 미선언(`vm` §1.1) → floor 검증 대상이 lock뿐 | `check_versions`가 `NO_ENGINES` report; 강제 없음, 채택 PR에서 선언 권고 |
| M-13 | common ui 테스트 하네스·showcase | risk "showcase 없음", velocity 13005 프리뷰 — 미결 | vitest + RTL + jsdom, axe는 opt-in; showcase는 1.0 전 없음(consumer-smoke가 대체) |
| M-14 | 담당 역할(공통 API·릴리스 vs 소비자 통합) | `prior` §8이 역할 명시를 권고; 세 안 모두 없음 | 단독 유지자 전제로 두 역할 겸임을 `AGENTS.md` 로컬 절에 명시, 긴급 패치 경로(앱 임시 복사 + 종료 조건) 기록 |
| M-15 | 마커 팔레트·공유 라이브러리 | 세 안 합의(범위 밖) — 누락 아님. T-5xx 결정 요청만 확인 | — |

## 6. 사실 오류(근거 포함)

| # | 위치 | 주장 | 근거·정정 |
|---|---|---|---|
| F-01 | coordinator D-06 npm 행 | "Node 동봉 11.19.x 기준, 허용 `>=11.19 <13`" | `vm` §3.2·§4.4: Node v22.23.2 동봉 npm은 **10.9.8**, 11.19.0은 Node 24/26 동봉. Node 22 기준선과 함께 두면 kta·ktdm·geo·wx가 첫날 위반 |
| F-02 | velocity D-06 표 npm 행 | "11.19.x(동봉)" floor 11.19 | 동일 정정. risk-first만 "동봉 npm 10.9" 사실을 적었으나 floor는 11.19로 두어 같은 결과 |
| F-03 | coordinator D-06 Node 행 | engines `^22.22.0 \|\| ^24.15.0` | map 실제 `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0`(`vm` §1.1). 사소하나 registry 값으로 복사되면 map과 불일치 |
| F-04 | coordinator D-06 Python 행 | `requires-python >=3.12` 기준선 | `be` §2.1·§5.3: map·wx·ktdm floor 3.11 → common 패키지 설치 불가. common 자체는 3.11 호환이어야 함 |
| F-05 | coordinator D-01 ui peer | `lucide-react ^1` | `vm` §1.3: dm 0.363·geo 0.468·wx 0.468·pinvi 0.460 → 4앱 peer 충돌 |
| F-06 | coordinator D-16 | "1차 공동 소비자 = map admin + pinvi admin" | `lic` §4 B1·B9: pinvi 라이선스 미결 상태에서 파일 이동·GPL 링크 금지. F절에도 언급 없음 → 순서 오류(P0) |
| F-07 | velocity D-11 | "Docker에 git이 없는 map api.Dockerfile 대비" | `be` §5.2: map `api.Dockerfile`의 git 설치 여부는 **미확인**. wheel 자산 근거로는 유효하나 사실 단정은 오류 |
| F-08 | velocity §0.2 D-13·D-13 대안 | "`window.confirm` 8건" | `ux` §1.12 표: 코드 히트 kta 1·ktdm 3·map 2·wx 1 = **7**(ktc 1·map +1은 주석). risk-first의 7건이 맞음 |
| F-09 | risk-first D-06 Node 행 | "floor 22.12(Vitest 4/5 engines)" | `vm` §4.2·§5.3은 **Vitest 5** engines(`^22.12`)만 기록. Vitest 4 engines는 조사에 없음(미확인) |
| F-10 | risk-first D-01 (c) | map `verify-frontend-eslint-config.mjs`가 "effective config 바이트 잠금" | `inv/map` §3.1: severity·`"use no memo"` 2곳·suppression 0건 **단언**이지 바이트 잠금이 아님. 결론(config 패키지 충돌)은 유지 |
| F-11 | coordinator D-09 | Button "size 4+icon" | `ui` §3.1: map size 8종(default/sm/xs/lg/icon/icon-sm/icon-xs/icon-lg, xs/lg deprecated). 계약 문안이 부정확 |
| F-12 | risk-first D-16·T-461 | weather `tokens.css` 교체 "값 diff 0" | `dt` §3.1.4: weather font 스택은 Geist 1순위, map/common은 Pretendard 1순위 → font 토큰을 포함하면 diff 0이 아님(M-03). 오버라이드 명시 필요 |

## 7. 사용자 확인이 필요한 열린 결정 + 기본값

| # | 결정 | 기본값(이 판정) | 막히는 것 |
|---|---|---|---|
| O-1 | pinvi 라이선스·공개 여부(L6) | 공개 + GPL-3.0-or-later, 1 PR(LICENSE·pyproject·README/AGENTS 정합) | pinvi 전 트랙(T-42x). **critical path** |
| O-2 | ktc·ktdm 루트 GPL 정렬 vs common §7 추가 허가 | 정렬(각 1 PR) | T-45x·T-47x 코드 채택 |
| O-3 | UI 배포 방식 | **npm 1차(`kt-` 내부 클래스) + 레지스트리는 셸·템플릿 2차** — velocity 제안과 반대이므로 확인 | T-201 설계 |
| O-4 | 유틸리티 네임스페이스 `kt-` / 변수 `--kt-` | 채택 | T-101 |
| O-5 | ui 1차 소비자 쌍 | map + pinvi(T-2xx 착수 전 L6 머지 조건), 미충족 시 map + airport 소형 부품 | T-411/T-421/T-432 |
| O-6 | airport WIP 병합·"Admin" 정의 | WIP를 값 유지로 병합; Admin = 현 백업·collector 패널 | T-430~432 |
| O-7 | geo React 19 승인 | 승인(ADR-019 갱신, 별도 PR, 실검증) | T-443/444 |
| O-8 | TS 기준선·airport 7.0.2 | 5.9 기준 + airport 예외(typescript-eslint peer 확장까지) | T-433 |
| O-9 | Node/npm | Node 22 + npm floor 10.9·rec 11.19, map 12.0.1 예외 | T-004 |
| O-10 | Python floor | common 3.11 호환, 앱 3.12 상향은 Phase 4 앱 결정 | T-302 |
| O-11 | 강제 승격 권한 | 앱이 매니페스트로 선언; common은 분기 보고서에서 "report 2분기 방치"만 목록화 | T-502 |
| O-12 | 다크 모드 | 앱 오버라이드 dark 선택, 활성 opt-in, light 기본 | T-104 |
| O-13 | 메트릭 접두 map·pinvi | 영구 예외 | T-307 |
| O-14 | Renovate | 미설치, dependabot 템플릿만 | T-507 |
| O-15 | Windows 도구 지원 | `tools` job windows 매트릭스 채택 | T-002 |
| O-16 | common 저장소 공개 여부 | 공개(GPL) | T-108 채널 |
| O-17 | npm scope `@kor-travel` | tarball 우선, org는 Phase 5(비차단) | T-006 |
| O-18 | weather 셸 문서-코드 불일치 | 문서 정정 먼저, 셸 교체는 T-463 | T-460 |
| O-19 | `docs/tasks-rule.md` §2.1 보정(M-10) | 채택 | T-001 |
| O-20 | 포트 `130xx`·airport 14002·`-latest` | 130xx 로컬 확인 후 확정; 14002 예외; `-latest`는 ktdm 결정 | T-014 |

## 8. 요약 — 어느 결정이 "한 번만 일하게" 하는가

| 축 | 한 번만 일하게 하는 선택 | 두 번 일하게 하는 선택(기각) |
|---|---|---|
| UI 배포 | npm 패키지 + `kt-` 내부 클래스 + shim import(map·pinvi 페이지 무변경) | 레지스트리 복사 후 `patched≥3`에 npm 재전환 |
| weather v4 | tokens.css → theme+utilities(preflight 제외) → **ui v0.2 후** 셸/패널/폼 → preflight | tokens·Next16·셸 교체 한 PR / registry 안정 전 손 이식 |
| 버전 정렬 | floor/recommended + lock 대조 + report 기본 | 정확 핀 재작성 6 PR / 즉시 fail |
| CI | 앱 기존 워크플로에 job 1개 추가, 태그 참조 | 재사용 워크플로로 앱 CI 대체(required check 재구성) |
| 첫 소비자 | GPL 3곳(map·weather·airport)으로 시작, pinvi는 L6 직후 합류 | map+pinvi 고정(L6 대기 중 전체 정지) |
| DataTable | `manualSorting` 기본 true 유지 + 계약 항목 추가 | `sortMode` 필수 prop(호출부 전수 수정) |
| 다크·대비 | 기본값 제공·검증 opt-in | 전 앱 dark 값 필수·contrast 즉시 fail |
