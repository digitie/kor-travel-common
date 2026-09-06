# 판정 보고서 — 사실 정합·내부 일관성 (fact-consistency)

- 작성일: 2026-09-06 · 판정자 초점: 세 레지스터(coordinator / risk-first / velocity-first)의 각 결정이 조사 문서(`docs/survey/*`)와 원 저장소 파일의 **사실**과 일치하는가, 레지스터 내부에 모순이 없는가, 조사 문서 간 불일치를 잘못 옮기지 않았는가.
- 입력: 세 레지스터 전문, `docs/survey/README.md`·`commonality-matrix.md`·`cross/*.md` 10편·`inventory/*.md` 7편(§1·§8·§9·§10·§11), `docs/tasks-rule.md`, `docs/runbooks/documentation-maintenance.md`, `docs/reviews/README.md`, `tools/validate_plan.py`, `tools/README.md`, `.github/workflows/docs.yml`, 선행 보고서(geo `docs/kor-travel-common-library-review.md`).
- 원 저장소 직접 확인(읽기 전용): `ktm-main/package.json`(engines·packageManager), `kor-travel-concierge/frontend/node_modules/tailwindcss/package.json`(v4 exports), `pinvi/apps/web/package.json`·`ktm-main/packages/kor-travel-map-admin/frontend/package.json`(lucide 버전).
- 표기: **사실** = 파일·조사 문서에서 확인 / **후보** = 이 보고서의 권고 / **추정** = 정황 / **열림** = 사용자 확인 필요. 약칭은 `commonality-matrix.md` 머리 규약(`vm`·`dt`·`ui`·`ux`·`be`·`oa`·`ci`·`dc`·`cv`·`lic`·`cm`·`inv/<app>`·`prior`).
- 심각도(틀렸을 때): P0 = 첫 소비자 PR·라이선스·CI 전면 red, P1 = 소비자 회귀 또는 재작업 1주 이상, P2 = 문서·도구 정정, P3 = 표기.

## 0. 요약

| 레지스터 | 점수(0~100, 사실 정합 기준) | 강점 | 약점 |
|---|---|---|---|
| coordinator | **58** | F절 보정 사실(airport Admin 실체, map 잠금 스크립트, concierge CI 부재, weather 정량, pinvi webpack, geo asChild 계수)은 조사 문서와 전부 일치. 결정 범위가 넓고 D-ID 골격을 제공 | D-06 기준선 표에 사실 오류 4건(npm 동봉 11.19, `eslint-config-next` map 선례, engines 전사, Python `>=3.12`를 `be` §5.3에 귀속), D-01 lucide peer `^1` ↔ D-16 pinvi 1차(0.460) 내부 모순, D-17이 cva Apache-2.0 누락, D-02 `decisions.md` 유지가 인용한 `dc` §4와 반대 |
| risk-first | **84** | 버전값·라이선스·계수·파일 경로가 조사 문서와 거의 전부 일치(npm 동봉 10.9, Python 3.11 floor, cva Apache, Actions 현행 v4/v5, window.confirm 7건). 조사 문서의 "미확인"을 결정으로 승격하지 않고 `외부 선행`·NOT_RUN으로 분리. 사실/후보/추정 구분이 가장 엄격 | D-16 "pinvi는 B1·B9에 걸려 첫 소비자 PR 불가"는 `lic` §4·`cm` §4.1 정의를 넘어선 해석(B1=추출, B9=ktc·ktdm 링크)을 사실처럼 씀. pinvi AdminTable 36 vs `ui` §3.3 35 불일치 미표기. T-461 "값 diff 0"은 weather `--rail 17rem`·map 어휘 참조 294회 앞에서 성립하지 않음(별칭 shim 누락). "PyPI 404 사실"은 조사 문서 근거 없음 |
| velocity-first | **72** | 매니페스트·drift·3단 강제·회수 지표 설계가 구체적이고 조사 근거(`vm` §7.4, `ui` §2.1·§6)와 정합. 추정을 추정으로 명시(PR 수·파일 수). task 수 80 검산 일치 | npm 동봉 11.19(Node 22는 10.9)를 사실처럼 표기, `window.confirm` 8건(`ux` §1.12는 실제 7 + 주석 1), "Docker에 git이 없는 map api.Dockerfile"(`be` §5.2는 미확인), Python 백엔드 소비 task를 `tasks-rule` §2.1 대역(T-480~489) 밖 앱 UI 대역에 배치(7건). `kt-` 접두 전면 도입은 map·geo·concierge 3앱이 이미 같은 클래스 문자열을 쓴다는 `ui` §6.3 사실과 비용 방향이 반대 |

핵심 결론 3개:
1. **버전 기준선은 risk-first의 3열(floor/recommended/consumer pin) 표를 채택**하되 npm 행을 "Node 22 동봉 10.9 → CI에서 명시 설치(pinvi 모델)"로 고치고, common Python floor는 3.11로 둔다(`be` §5.3). coordinator의 단일 정확값 표는 map exact 핀·3.11 앱 3곳과 즉시 충돌한다.
2. **UI 배포 방식(O3)은 사용자 결정**이지만, 사실 기준으로는 npm 1차(risk-first)가 우세하다: 같은 클래스 문자열이 map·geo·concierge에서 그대로 동작(`ui` §6.3)하므로 velocity의 `kt-` 접두는 4앱 개명, 무접두는 pinvi 1앱 개명이다. 다만 velocity의 소비자 매니페스트·drift 도구·3단 강제는 어느 쪽에서도 채택할 가치가 있다.
3. **세 레지스터 모두 빠진 결정** 중 첫 소비자 PR을 막는 것은 (a) 순수 CSS·구 어휘 소비자용 별칭 shim(weather·concierge·pinvi·geo 4앱 전부 필요), (b) SemVer 0.x 파괴적 변경 규칙, (c) common 자체 npm workspace·`packageManager` 선언, (d) Windows 개발자 프로필(현재 `tools/README.md`·`documentation-maintenance.md`가 PowerShell fence와 `python`을 쓰고 있어 세 레지스터의 "bash·`python3`" 결정과 이미 어긋남).

## 1. 대조 방법

- D-01~D-18은 세 레지스터를 같은 ID로 정렬해 (i) 인용 절이 실제로 그 사실을 말하는지, (ii) 값이 `vm` §1~§4·`lic` §2·`dt` §3·`ui` §2~§6·`be` §2~§5·`oa` §2~§4와 같은지, (iii) 같은 레지스터 안의 다른 D-ID와 충돌하지 않는지 확인했다.
- 의심 값은 원 저장소 파일을 열어 확인했다(§3 근거 열에 경로 기재). 네트워크 조회(npm org·PyPI)는 하지 않았고, 레지스터의 "403/404" 주장은 조사 문서에 근거가 없으므로 미확인으로 분류했다.
- 조사 문서 간 불일치(`README.md` §6.2에 없는 것)를 별도로 모았다(§5).

## 2. D-ID별 판정

열: 승자 = coordinator / risk-first / velocity-first / merged. 권고 = 최종 문안(1~3문장). 심각도 = 틀렸을 때.

| ID | 승자 | 최종 권고 문안 | 근거·판정 이유 | 심각도 |
|---|---|---|---|---|
| D-01 배포 단위 | merged(risk-first 기반) | 첫 릴리스는 `packages/tokens`(npm, React 무관) · `packages/ui`(npm, React 19 전용, subpath exports, 인라인 아이콘) · `packages/py/kor-travel-common`(`kortravelcommon`, extras) 3 단위 + `docs/standards/*` + `versions.json`/`tools/*`. `config`·`api-client-core`는 만들지 않고 Phase 5 재평가. 패키지명 `@kor-travel/*`는 잠정이며 T-006 scope 확인 결과를 첫 소비자 PR 전에 기록. velocity의 소비자 매니페스트(§2 M-28)는 배포 방식과 무관하게 채택 | coordinator의 `config` 패키지는 map `verify-frontend-eslint-config.mjs`(`inv/map` §3.1)·pinvi ESLint 가드(`inv/pinvi` §3.1)와 충돌하고, `lucide-react ^1` peer는 pinvi 0.460(`vm` §1.3, `apps/web/package.json:35` 확인)을 배제해 D-16과 모순. `api-client-core`는 `cm` §2.3 "앱별 ApiError 형태 상이" | P1 |
| D-02 저장소 구조 | merged(risk-first = velocity) | canview 계층(AGENTS → docs/README → resume → task 1파일) + `docs/{adr,architecture,runbooks,reviews,tasks,standards,survey,plan}` + validator 2종 채택, 하드웨어·차량·firmware 제외. `docs/decisions.md`는 **두지 않고** `docs/adr/README.md` 단일 색인(다음 번호 명시). T-002에서 `documentation-maintenance.md` §2·§3의 `decisions.md` 문구, `validate_document_links.py` 절대 접두, `.py` CRLF, **`documentation-maintenance.md` §6 PowerShell fence와 `tools/README.md`·`docs.yml`의 `python` 표기**를 함께 정정 | coordinator D-02는 `dc` §4를 인용하면서 그 문서가 "불필요"로 판정한 `decisions.md`를 유지해 이중 색인(ktdm DO NOT 15 계열)을 만든다. `cv` Q1이 충돌을 명시 | P2 |
| D-03 개발 환경 | merged | common 자체 정본 = Linux/WSL bash, CI `ubuntu-24.04`. 공통 절은 OS 미규정(`dc` C1). 검사 도구는 Python 3.11+ stdlib(`tomllib` 포함)로 Windows에서도 실행 가능하게 하고, `docs/dev-environment.md`에 **Windows 보조 프로필**(Git Bash, `py -3 -B -X utf8`, `.gitattributes` LF)을 1절 둔다. runbook 명령은 bash fence 1벌만 | 세 레지스터 모두 동의. 다만 현재 사용자 환경이 Windows이고 common 기존 파일이 PowerShell fence를 쓰므로(§3 E13) "보조"의 실체를 명시해야 함 | P2 |
| D-04 리뷰 gate | merged | common 자체: canview full gate를 **비면제 목록**(`docs/standards/*`, `versions.json`, `packages/*` 공개 API·CSS, 재사용 워크플로, AGENTS/SKILL/ADR/runbook/task·review 규칙)에 적용, 면제는 오탈자·동의 링크. light 판정 주체 = merge 담당(작성자≠판정자). 상태 어휘(`IN_REVIEW/COMPLETE/POST_FIX_REVIEW`, verdict `BLOCK/CONDITIONAL/PASS`, `-post-fix` 별도 report)를 TEMPLATE·README에 명시. 소비자에게는 공통 절 B + TEMPLATE만 배포, 채택은 로컬 | risk-first가 `cv` R3.2·R3.6·Q5의 미정본화 어휘를 닫음. velocity V7(소비자 프로세스 미규정)은 `dc` §3.5와 정합 | P2 |
| D-05 task 원장 | merged(합의) | common은 5열 표 + `READY/BLOCKED/IN_PROGRESS/DONE` + `validate_plan.py` 무변경. 소비자 원장 형식은 규정하지 않고 "ID 재번호 금지·완료 시 evidence 보존"만 SHOULD. **레지스터 task ID는 `tasks-rule` §2.1 대역을 지켜야 하며 Python 백엔드 소비는 T-480~T-489**(§3 E9) | `cv` Q3: validator 무변경이면 5열 표 확정. velocity 계획의 T-413/414/423/432/443/454/463은 대역 위반 | P3 |
| D-06 정렬 기준선 | risk-first(수정 적용) | `versions.json`은 **floor / recommended / consumer pin 3열**. 2026-09 값: Node floor 22.12·recommended 22.23.x(24/26 승격은 Phase 5; 2026-10-28 이후 Active LTS는 26) · **npm floor 11.19은 CI에서 `npm install -g npm@11.19.1` 명시 설치를 전제**(Node 22 동봉은 10.9.x) · Next 16.2/16.3.x · React 19.0/19.2.x · TS 5.9.x(airport 7.0.2 등록 예외) · Tailwind 4.3.0/4.3.3 · base-ui 1.8 · Vitest 4.1 · Playwright 1.60 floor(map exact 예외)/1.63 · **common Python floor 3.11**(앱 3.12 상향은 앱 결정) · fastapi 0.115/0.141 · starlette 미핀 · alembic 1.19(map `<1.20` 존중) · Actions 현행 v4/v5+SHA, common 내부만 v7 | coordinator 표는 (a) `Node 동봉 11.19.x`(`vm` §3.2·§4.4: v22.23.2→npm 10.9.8), (b) `eslint-config-next 16.3.x \| map 선례`(map은 미사용, `inv/map` §3.1 테스트 단언), (c) Python `>=3.12 \| backend §5.3`(그 절은 3.11 floor 권고), (d) map engines `^22.22.0`(실제 `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0`, `ktm-main/package.json:7`). velocity도 (a)를 반복 | P1 |
| D-07 핀 정책·스키마 | merged | 계층별 하이브리드는 **common 자체 패키지에만 정확 핀**, 소비자 선언 형식은 자유(velocity P2+), **lockfile 의무 + 설치본 대조**가 규칙. 스키마 = risk-first(`floor/recommended/image/exceptions[until]/blocked/consumers.enforce`) + velocity 파서(npm lock v3·`uv.lock`·`poetry.lock`, workspace `scope`). 판정 어휘 `OK/BELOW_FLOOR/NOT_RECOMMENDED/NO_LOCK/FLOATING_REF/BLOCKED/EXCEPTION`. 모드 report→warn→fail, 단 `FLOATING_REF`·`BLOCKED`·만료 예외는 report에서도 1. 승격은 소비자별 2회 green 후 common PR | `vm` §7.4 "격차를 보고로", `be` §5.1 `@main` 위반, `inv/ktc` §4.1 `mcp<2` 사고. coordinator "정확 핀 강제"는 lock 없는 4곳(`vm` §2.1)에서 검증 대상이 없다 | P1 |
| D-08 Tailwind v4 전환 | risk-first(+velocity 순서 조정) | 대상은 미도입→도입 2(airport WIP, weather) + `@config` 정리 3(geo·concierge·pinvi web) + 외부 대기 1(pinvi mobile). 각 대상은 "시각 기준선 캡처 → 설정만 → 토큰만 → 컴포넌트" 별도 PR. airport WIP는 값(16/10, alpha line) **유지**하고 병합, 값 수렴은 D-12 task로 분리(coordinator의 "alpha line 제거" 기각). geo는 `@config` 실효값 빌드 검증(T-441 ①) 선행. weather는 Next16·Vitest4·Node22 PR → `theme`+`utilities`만(preflight 제외) → 셸·패널·폼 교체(registry/ui 2차 안정 후) → preflight. **weather·concierge·pinvi·geo 모두 별칭 shim 파일이 선행**(§6 M-1) | `inv/weather` §9.1 bare element 23종·2,495행, `dt` §5-3 `@config` 우선순위 미확인, `inv/airport` §3.2 `tokens.css` 무변경, `inv/pinvi` §3.2 Dockerfile 중첩 의존. Tailwind 4.3.1 `package.json` exports에 `./theme`→`./theme.css`, `./utilities`→`./utilities.css` 별칭이 있어 risk-first의 import 표기는 유효 | P1 |
| D-09 프리미티브·React·Button·DataTable | merged(합의 + risk-first 강화) | overlay만 `@base-ui/react` 1.8, 비-overlay는 native + `useRender` 선택. React 19 전용(peer `^19.0.0`, 18 앱은 tokens만). Button: `type="button"` 명시 기본, `loading`=`aria-disabled`+`aria-busy`+포커스 유지+`onClick` 차단, root opacity 금지, variant 7·size 8(alias deprecated). Checkbox native + `data-slot=checkbox`. **DataTable `sortMode: "server"\|"client"` 필수 prop**(기본값 없음), `enableSortingRemoval`·`rowTestId`·`containerTestId`·`stickyHeader`·sr-only 문구 포함. geo VirtualTable 잔류. base-ui `type`·hidden input·Toast API는 T-201에서 소스 확인 후 릴리스 | `ui` §3.1·§3.3·§5.4·§7-1. velocity의 `manualSorting=true` 기본은 pinvi `AdminTable`(`manualSorting=false`, 35~36 소비처)과 e2e testid 계약(`ui` §3.3)을 깨뜨릴 수 있어 필수 prop이 안전 | P1 |
| D-10 UI 배포 방식 | **열림(O3)** — 기본값 risk-first | npm 패키지(ESM+d.ts+Tailwind 소스 클래스, `'use client'` 보존) 1차. 소비자 2줄(`@import "@kor-travel/tokens/theme.css"`, `@source`). `base.css`/`base.scoped.css` 2변형. consumer-smoke는 webpack·Turbopack 양쪽. `docs/standards/ui-contract.md`에 data-slot·testid·heading 계약, 변경=major. **클래스 이름은 무접두 공통 이름**(map 어휘) + T-101에서 소비자 4앱 `@theme` 충돌 검사 스크립트로 검증, 충돌 시에만 `kt-` 접두 전환. shadcn 레지스트리는 같은 소스에서 **생성물**로 Phase 5 재평가 | `ui` §6.3: 같은 클래스 문자열이 map·geo·concierge에서 그대로 동작(무접두 = 1앱 개명, `kt-` = 4앱 개명). `ui` §6.2·`prior` §3.2: 복사 후 drift가 27/27 상이의 원인, 전파가 공통화 동기. velocity의 충돌 우려(pinvi 사용자 preset)는 이름 집합이 다르고(`canvas/ink/hairline/primary/cta` vs `surface-*/text-*/control-line/brand`) `[data-pv-surface]` 스코프로 완화됨 — 단 `focus`·`primary`류 동명은 검사 필요 | P1 |
| D-11 배포 채널 | merged(합의) | npm = GitHub Release tarball(`tokens-vX.Y.Z`, `ui-vX.Y.Z`, 자산 `kor-travel-<pkg>-X.Y.Z.tgz`) + lock `integrity`. Python = `git+https://…@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common` + `uv.lock` sha, **wheel도 릴리스 자산으로 첨부**(git 없는 Docker 대비 — 단 map api.Dockerfile의 git 유무는 미확인). 같은 태그 재발행 금지, `@main` 금지. 공개 npm/PyPI는 Phase 5 | `be` §5.2 A안, `prior` §8. velocity의 "map api.Dockerfile에 git 없음"은 `be` §5.2가 미확인이라 밝힌 항목 | P2 |
| D-12 토큰 | merged | 접두 `--kt-*`(0회). 2단 계층. `shadcn.css` alias 의미 고정(`--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control). 프로필 `admin`/`consumer`(값은 문서·`tokens.json`만, pinvi 소유). 타입 스케일은 `@theme`(비inline). 오버라이드 허용 = brand 4·focus·paper 4·ink 4 + **status 4+tint(허용, 대비 검사 대상)**. 다크: `tokens.css`는 `.dark` 값 필수(map 기본), **앱 오버라이드의 dark 값은 선택**, 활성화 파일은 앱 명시 import, 기본 `color-scheme: light`. `kt_contrast` report 기본 + 앱별 `contrast-baseline.json`, 신규 미달만 fail | `dt` §3.4.2(geo 2.29/2.41·concierge 2.06/1.93·airport 1.15 미달), §3.6.4(status 기본값 유지 "권장"이지 금지 아님 — pinvi admin·concierge가 이미 자기 값), §3.6.5·§3.6.6. coordinator "모든 semantic dark 필수"는 dark 값 없는 geo·pinvi·ktdm에 값 발명 부담 | P1 |
| D-13 UX·PC/Mobile | merged | `ux` §2 G0~G9 → `ux-guide.md`(admin/사용자 장 분리), §3 → `responsive-web.md`. **MUST 소집합 U1~U8**(velocity) + 나머지 SHOULD. 규칙 ID `UX-Gn.m` 신규 발급, 앱 M/C 번호는 출처 인용. 게이트 `tools/ux_lint.py`는 **diff 기반(신규·변경 줄) report 기본** + 앱별 baseline 목록(잔존 `window.confirm` map 2·ktdm 3·kta 1·weather 1 = 7). C1~C22는 risk-first 표를 채택하되 강제 수준은 velocity 표(SHOULD 위주) | `ux` §1.12 계수(7건 실제 + ktc 주석 1), §4 C1~C22, `dt` §3.4.1 map 게이트 스크립트 미확인. 두 게이트 방식은 상호 보완(diff = 신규 차단, baseline = 전량 감사) | P2 |
| D-14 OpenAPI | merged(risk-first 3계층 = velocity 표) | `oa` §3 M/S/N 채택. 즉시 MUST(additive): M1·M2·M4·M9·N6·N7. 신규 표면 MUST / 기존 표면 SHOULD + 예외 등록: M3·M5·M6·M7·M8·N1~N5·N8. 예외 레지스트리 `docs/standards/openapi-exceptions.yaml`(`app, rule, surface, reason, sunset|null, owner, review`). 검증 오류 422 기본·geo 400 예외. 429 코드 사전은 common 기본(`TOO_MANY_REQUESTS`) + 앱 덮어쓰기. **health 경로는 `/health`·`/readyz`·`/version`으로 확정**(`ci` §3.2의 `/ready` 표기는 `oa` M5·geo 선례 `/readyz`로 통일). 헤더는 형식 규칙만, AppId는 앱 소유 | `oa` §4(pinvi 모바일 결합, concierge features export는 map provider 소비, map 산출물 변경 = pinvi·ktdm sha256 pin 파손), `be` §2.5 `/v1/healthz` probe 결합. §5 S1 조사 문서 불일치 | P1 |
| D-15 Python 모듈 | merged | 배포 `kor-travel-common`, import `kortravelcommon`, **core는 stdlib+pydantic, 3.11 문법**. 1차 C12 openapi export·C4 health(alias 옵션)·C13 time·C20 quality(ruff `extend` 베이스, **format 규칙 미포함**, per-file-ignores baseline). 2차 C1 settings·C9 db·C7 public_api_key·C2 request_id(`trust_incoming`)·C3 metrics(접두 인자, 이름 변경 강제 없음). 3차 C5 errors(`exclude_paths`)·C16(HSTS 전달 헤더 불신 기본)·C17·C8·C11·C10 템플릿·C15·C18. 보류 C6·C14·C19·C21. `[api]`는 starlette 범위 미선언 + 0.4x/1.6 CI 매트릭스. 메트릭: 신규 `kt<x>_`, map·pinvi는 예외 등록(영구 여부는 O12) | `be` §3·§4·§5.3·§7-1·2·4, `inv/ktdm` §4.1 `ruff format` 금지, `inv/geo` §8-23. coordinator의 3.12 floor는 map·weather·ktdm(3.11) 설치 불가 | P1 |
| D-16 첫 소비자 | **열림(F-1/O1)** — merged 기본값 | tokens 1차 = **map + weather**(GPL, 순수 CSS는 별칭 shim 동반) + **pinvi admin(조건부: L6 결정을 같은 Phase 안에서 완료)** + airport(WIP 병합 후). ui 1차 = **map + pinvi admin**(L6 후)이며 L6가 Phase 2 시작까지 미결이면 airport 소형 부품(Alert·StatStrip·SectionCard·EmptyState·Button)을 2번째 검증자로 승격. Python 1차 = map-api·weather-api·airport, 2차 geo, 3차 pinvi·concierge·ktdm | `prior` §1 map↔pinvi 이식 관계가 "두 앱 동일 의미 API"의 가장 강한 근거(`ui` §2.1 27쌍). airport는 대응 부품이 없어(`inv/airport` §3.1 6파일) 검증 가치가 낮다. risk-first의 "B1·B9로 pinvi 소비 불가"는 §3 E10 참조 — 위험은 실재하나 정의상 차단 항목은 아님 | P1 |
| D-17 라이선스 | risk-first(+velocity drift 정규화) | common `GPL-3.0-or-later`; `NOTICE`(저작권자·버전·연락처), `THIRD_PARTY_NOTICES.md` + `LICENSES/`(MIT·**Apache-2.0(cva)**·OFL-1.1·BSD-3·ISC), `PROVENANCE.md`(`lic` §2.3 표), SPDX 헤더 + `Origin/Derived-From/Modified` + `tools/check_spdx.py`(Phase 1부터 fail). 추출: GPL 원천 그대로(geo `-only` 병기 또는 재선언), MIT 원천 고지 보존, **pinvi는 L6 전 추출 금지**, tgz·vworld·Hallmark 본문 금지, ktc AppShell diff 후. ktc·ktdm은 루트 GPL 정렬 권고(§7 예외 기각). 소비 앱 사본의 선두 주석 블록은 drift 비교에서 정규화 | `lic` §2.2 D1~D10·§2.4(cva Apache-2.0, "MIT 가정과 다름" 명시)·§3.2·§3.6·§4 B1~B8·§6. coordinator D-17은 cva를 MIT 계열에 묻어 NOTICE 누락 위험 | P1 |
| D-18 CI·릴리스·포트 | merged | common CI: `docs`·`tools`·`packages`(pack→tarball 설치, webpack/Turbopack)·`python-package`(starlette 매트릭스)·`consumer-smoke`(pinned SHA, 주간)·`secret-scan`·`check-versions(report)`; 하드닝(`permissions`·`concurrency`·`timeout`·`ubuntu-24.04`·SHA 핀 — **현 `docs.yml`은 `checkout@v6`·`setup-python@v6` 태그 참조, 정비 대상**). 재사용 워크플로는 **단계 배포**: Phase 1 `versions-check`·`contrast-check`·`docs-check`, Phase 3 `openapi-drift`·`typegen-drift`, Phase 5 `node-quality`·`python-quality`. 태그/SHA 참조, job `name:` 입력 개방, 운영 호출 job required 금지. 릴리스: 패키지별 태그·rc→소비자 PR→정식·덮어쓰기 금지. 포트 정본 ktdm 유지, common `130xx`는 T-014 점유 확인 후 | `ci` §1.1~§1.3·§2.1~§2.3·§3·§4, `cv` §1.3(링크 17건). velocity 단계 배포는 map 8·pinvi aggregate ruleset 결박(`ci` §2.3)을 피함 | P2 |

### 2.1 초안에 없던 결정(신규 ID 병합)

| ID(병합) | 출처 | 최종 권고 | 심각도 |
|---|---|---|---|
| M-19 pinvi 사용자·모바일 취급 | risk D-19 / vel D-22·O21 | 사용자 웹·모바일은 코드 소비 대상 아님. `consumer` 프로필은 규칙 + `tokens.json` 의미 이름만, 값은 pinvi. 모바일은 `exceptions`(Tailwind 3, RN 정확 핀, NativeWind 5 GA 재평가) | P2 |
| M-20 airport Admin 정의 | risk D-20 = vel D-21 | 현 실체 = 무인증 백업 패널 + collector 패널 + `/v1/admin/*`(ADR-003). 1차 = tokens + 소형 부품. AdminPageHeader/skip-link/셸 소비는 airport T-035 이후 BLOCKED. 사용자 확인(O15) | P2 |
| M-21 시각 회귀 기준선 의무 | risk D-21 / vel D-23 | 토큰·스타일·셸 변경 소비자 PR은 6폭(320/375/414/768/1024/1440) 스크린샷 기준선 → diff evidence. Playwright 없는 weather·ktdm은 `templates/playwright.baseline.ts` | P1 |
| M-22 헤더·메트릭 접두 | risk D-22 / vel D-15 | 형식 규칙만 공통(`X-<AppId>-…`), AppId 앱 소유. 메트릭 신규 `kt<x>_`, 기존 예외 등록 + `review` 날짜 | P2 |
| M-23 공유 라이브러리 배포 정책 | risk D-23 = vel D-22/T-506 | common 범위 밖. `versions.json` `providers` 절은 보고만. T-5xx로 `maplibre-vworld-react` npm·`vworld-style.ts` 중복·airkorea 이중 경로·kma/kasi SHA 정렬 요청 | P3 |
| M-24 채택 PR 규격·되돌리기 | risk D-24 + vel D-23 | 한 PR = 한 산출물, 업그레이드와 분리, 단일 revert, lock 동반, 본문에 되돌리기 명령·검사 결과·스크린샷, 파일 상한(tokens 10·ui 30·py 10, 초과 시 분할) | P2 |
| M-25 NOT_RUN 표기 | risk D-25 | common에서 실행 못 한 검증은 evidence에 `NOT_RUN(사유)`, DONE 전 `외부 선행` 승격, 0 test/skip을 pass 집계 금지 | P2 |
| M-26 마커 팔레트 | risk D-26 = vel D-22 | common 소유 아님. 16슬롯·라벨 대비 규칙만 ux-guide. hex 정본은 map 확정(T-5xx 요청) | P3 |
| M-27 decisions.md·도구 언어·링크 | risk D-27 = vel D-02/D-03 | `decisions.md` 미보유, 도구 Python(`python3`/`uv run` 표기 — Windows 절에 `py -3` 병기), 상대 링크만 | P3 |
| M-28 소비자 매니페스트 + 3단 강제 | vel D-19·D-20 | 각 소비 저장소에 `kor-travel-common.lock.json`(schema `consumer-manifest.v1`: tokens 버전·override 경로·ui 버전 또는 registry 항목 sha256·lockfiles[]·`versions/contrast/ux_gate` enforce·exceptions[]). `docs/integration-map.md`는 매니페스트에서 생성. 검사 모드 report→warn→fail은 매니페스트에서 앱 선언 | P2 |
| M-29 회수 측정 | vel D-24 | `prior` §11 지표 + drift 지표를 분기 `docs/reports/adoption-YYYY-QN.md`로. "순절감 ≤0 2분기 → 범위 축소", "patched ≥3 → 배포 방식 재검토" 중단 조건 | P3 |

## 3. 사실 오류·근거 없는 단정

| # | 위치 | 주장 | 근거(사실) | 심각도 |
|---|---|---|---|---|
| E1 | coordinator D-06 npm 행; velocity D-06·D-07(`11.19.x(동봉)`, target `11.19.1`) | "npm은 Node 동봉 11.19.x 기준" | `vm` §3.2·§4.4: Node v22.23.2 동봉 npm은 **10.9.8**; 11.19.0은 Node 24/26 동봉. Node 22 기준선에서 11.19은 CI 명시 설치가 필요(pinvi `web.yml:71-73`이 그 이유를 적음). risk-first D-06은 정확 | P1 |
| E2 | coordinator D-06 ESLint 행 | "`eslint-config-next 16.3.x` — map 선례" | `inv/map` §3.1: map은 `eslint-config-next` **미사용**(`test_frontend_dependency_security.py`가 부재 단언), `@next/eslint-plugin-next` + `typescript-eslint` 직접 조합. `vm` §1.6 map 열 "—" | P2 |
| E3 | coordinator D-01(peer `lucide-react ^1`)·D-16(pinvi admin 1차) | 내부 모순 | pinvi web `lucide-react ^0.460.0`(`vm` §1.3; `apps/web/package.json:35` 확인), geo 0.468·weather 0.468·ktdm 0.363. `^1` peer는 1차 소비자 pinvi를 설치 단계에서 막는다. lucide 0.x→1.x breaking은 `vm` 열린 질문 13(미조사) | P1 |
| E4 | coordinator D-06 Python 행 | "`requires-python >=3.12` — backend §5.3·Q1" | `be` §5.3: "파이썬 floor: **3.11**(map·ktw·ktdm 때문) — 앱 floor 3.12 정책이 확정되면 3.12". `be` §2.1: map·weather·ktdm `>=3.11`, map CI 3.11 매트릭스. `vm` §5.1 후보 A의 "`>=3.12`"는 앱 정렬 목표이지 common 패키지 floor가 아님 | P1 |
| E5 | coordinator D-06 Node 행 | map engines `^22.22.0 \|\| ^24.15.0` | `ktm-main/package.json:7` = `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0`(`vm` §1.1 동일). 전사 오류 | P3 |
| E6 | coordinator D-17 | 서드파티를 "shadcn·base-ui·radix MIT, tw-animate-css MIT, Pretendard OFL"로만 열거 | `lic` §2.4: `class-variance-authority` 0.7.1은 **Apache-2.0**(NOTICE 유지 의무), lucide ISC, maplibre-gl BSD-3. `lic` §2.4가 "임무 지시문의 'shadcn 계열 MIT' 가정과 다름"을 명시 | P1 |
| E7 | coordinator D-02 | `docs/decisions.md` 유지 + "다음 번호 정본" | 인용한 `dc` §4 대응표는 `decisions.md`를 "불필요"로 판정. `cv` Q1이 common `documentation-maintenance.md`와의 충돌을 열린 질문으로 둠. map 관행(`inv/map` §5 "다음 후보는 README 상단이 정본, 다른 문서에 박지 않음")과도 반대 | P2 |
| E8 | velocity D-11 | "Docker에 git이 없는 map api.Dockerfile 대비" | `be` §5.2 A안: "map api.Dockerfile은 **미확인**". 사실이 아니라 미확인 | P3 |
| E9 | velocity F.2 task ID | T-413/T-414(map-api), T-423(pinvi api), T-432(airport py), T-443(geo py), T-454(concierge py), T-463(weather-api)를 앱 UI 대역에 배치 | `docs/tasks-rule.md` §2.1: T-410~469는 각 앱 **admin/frontend/ui**, Python 백엔드 소비는 **T-480~T-489**(앱별 `a`/`b` suffix). risk-first T-480~T-485는 준수. risk-first T-452(concierge·ktdm 라이선스)는 ktdm을 concierge 대역에 섞음(경미) | P3 |
| E10 | risk-first D-16·H-1 | "pinvi는 B1과 B9에 걸려 첫 소비자 PR을 열 수 없다"(사실처럼 서술) | `lic` §4 B1 = "pinvi의 모든 파일" **추출** 금지(해제 = L6). `cm` §4.1 B9 = "ktc·ktdm이 common 코드를 링크하는 것"(MIT 앱). pinvi가 common을 **소비**하는 것은 두 항목의 정의 밖. `lic` §3.6 pinvi 행은 "먼저 README/AGENTS 상충 해소" 권고이며 이미 GPL 코드(P1~P3)가 있으므로 소비로 상태가 악화되지 않음. 위험은 실재(사유 유지 시 충돌)하나 "차단 사실"이 아니라 "추정·정책 판단"으로 재분류 | P2 |
| E11 | velocity D-13 요약·C7·O20 | "`window.confirm` 잔존 8건" | `ux` §1.12: kta 1·ktc 1(**주석**)·ktdm 3·map 2(+주석 1)·weather 1 → 실제 코드 7건. `ux` §4 C7도 map 2·ktdm·kta·weather만 열거. risk-first "7"이 정확 | P3 |
| E12 | risk-first D-09(d)·T-422; coordinator F절 없음 | "pinvi 36페이지 `AdminTable`" | `ui` §3.3 "35 파일", `ux` §1.3·`inv/pinvi` §3.1 "36페이지/36곳". 조사 문서 간 불일치를 한쪽만 옮김(§5 S2). 계약 결론은 동일 | P3 |
| E13 | 세 레지스터 D-03·D-27 vs common 기존 파일 | "runbook 명령은 bash 표기, PowerShell 블록 없음, `python3`/`uv run`" | common 작업 트리 `docs/runbooks/documentation-maintenance.md` §6(88~91행) ```powershell fence, `tools/README.md` 회귀 시험 ```powershell fence, `tools/README.md`·`docs/tasks-rule.md:3`·`.github/workflows/docs.yml`는 `python -B -X utf8`. 결정과 기존 파일이 이미 어긋나며 어느 레지스터도 T-002 범위에 넣지 않음(risk-first T-002는 `decisions.md`·절대 접두·CRLF만) | P2 |
| E14 | risk-first T-461("값 diff 0") · coordinator D-08 weather("`@kor-travel/tokens`") · velocity D-08(b)("tokens.css만 먼저") | weather `app/tokens.css`를 common `tokens.css`로 교체하면 값이 그대로 | `inv/weather` §3.1: `globals.css`가 `var(--…)` **294회** 참조하는 이름은 map 어휘(`--surface-page`, `--control-h`, `--space-*`, `--rail`)와 legacy `--color-ink/paper/…` 15종이며 `--rail`은 **17rem**(map 22rem). common은 `--kt-*`이므로 별칭 shim 없이는 전 화면 무스타일, `--rail`은 값 diff 발생. 세 레지스터 모두 shim 파일을 결정하지 않음(§6 M-1) | P1 |
| E15 | risk-first D-01·D-11, velocity D-01(`PyPI 404 = 미점유 사실`), coordinator D-11(`@kor-travel` 403) | 레지스트리 조회 결과를 "사실"로 표기 | `docs/survey/*` 어디에도 npm org·PyPI 이름 조회 기록이 없음(`vm` §4.1 외부 조회 목록에 없음). 레지스터 작성 시 자체 조회로 보이나 명령·시각 미기재 → **미확인**으로 두고 T-006 evidence로 재확인 | P3 |
| E16 | coordinator D-06 Node 행; velocity D-06 Node 행 | "2026-10 이후 24로 상향 검토" | `vm` §4.4: Node 24 **Active 종료 2026-10-20**(이후 Maintenance), Node 26이 2026-10-28 LTS 전환. "2026-10 이후"의 Active LTS는 26이며 24는 Maintenance. 상향 재평가 시점 표현만 정정(risk-first "24/26 Phase 5 재평가"가 정확) | P3 |
| E17 | coordinator D-06 `@base-ui/react ^1.8 \| ui-components §5.4` | 인용 절 불일치 | `ui` §5.4는 엔진 결정 근거(파일 수 29 vs 12)이며 버전은 `vm` §1.3·`ui` §2.3. 값은 맞고 인용만 오기 | P3 |
| E18 | coordinator D-06 Vitest 행 | "Node 22.12+ 전제" | `vm` §4.2: Node `^22.12`는 **Vitest 5.0.0** engines. Vitest 4.1의 engines는 조사에 없음 | P3 |

## 4. 레지스터 내부 모순

| # | 레지스터 | 모순 | 해소 |
|---|---|---|---|
| I1 | coordinator | D-01 `ui` peer `lucide-react ^1` ↔ D-16 pinvi admin 1차(0.460) ↔ D-06 lucide `^1.41` 기준선(4앱 0.x, breaking 미조사) | 아이콘 인라인 SVG(risk-first) 또는 peer 미선언 |
| I2 | coordinator | D-06 Python `>=3.12` ↔ D-16 Python 1차 = map-api·weather-api(둘 다 `>=3.11`, map CI 3.11 매트릭스) | common floor 3.11 |
| I3 | coordinator | D-03 "PowerShell 블록 없음" ↔ D-02가 유지하는 canview 사본(`documentation-maintenance.md`)의 PowerShell fence | T-002 범위 확장 |
| I4 | coordinator | D-08 airport "alpha line 제거·admin 프로필 정렬" ↔ F절 "airport 1차 = tokens + 소형 부품" ↔ `prior` §5 "업그레이드와 공통화는 독립 작업" | 값 유지(risk-first), 수렴은 별도 task |
| I5 | coordinator | D-02 `decisions.md` 유지 ↔ 인용 `dc` §4 "불필요" | 단일 색인 |
| I6 | risk-first | D-16 "ui 1차 = map + airport"로 "두 소비자 검증" 충족 주장 ↔ D-20 "airport 1차 = 소형 부품, 셸 BLOCKED" ↔ `inv/airport` §3.1(대응 부품 없음). 검증 폭이 Button·Alert·StatStrip·SectionCard·EmptyState 5종에 그침 | pinvi admin을 L6 조건부 1차로 복귀(§2 D-16) |
| I7 | risk-first | T-461 "값 diff 0" ↔ D-12 접두 `--kt-*` + weather `--rail 17rem` | 별칭 shim + weather override 파일 |
| I8 | velocity | V3 "클래스는 `kt-` 접두, 앱 별칭은 앱 소유" ↔ D-10 "map ~40파일 접두 치환(페이지 무변경 조건)" ↔ `ui` §6.3(map·geo·concierge 동일 클래스 무변경 가능) — 접두 도입이 곧 3앱 개명 | 무접두 + 충돌 검사(§2 D-10) |
| I9 | velocity | D-06 `@base-ui/react` floor 1.6 ↔ concierge 1.5 설치(2차 소비자) → 채택 전 `FLOOR` 판정 | 인지하고 있음(예외 등록); 문제 없음 |
| I10 | velocity | F.2 task 대역(E9) ↔ D-05 "`docs/tasks-rule.md` 무변경" | 대역 재배치 |
| I11 | 셋 모두 | health 경로 `/readyz`(D-14) ↔ `ci` §3.2 초안 `/ready` — 레지스터는 `oa`만 따르고 `ci` 불일치를 표기하지 않음 | `/readyz` 확정 + `ci-deploy.md` 정정 메모 |

## 5. 조사 문서 간 불일치(레지스터에 영향)

| # | 축 | 문서 A | 문서 B | 판정 | 레지스터 영향 |
|---|---|---|---|---|---|
| S1 | readiness 경로 | `oa` §3.1 M5 `/readyz`, `be` C4 `/readyz`(geo) | `ci` §3.2 `/ready` | `/readyz`(geo 선례, `inv/geo` §4.1 사실) | D-14 문안에 명시 |
| S2 | pinvi AdminTable 소비처 | `ui` §3.3 35 파일 | `ux` §1.3·`inv/pinvi` §3.1·§8-3 36 | 미확정(파일 vs 페이지 단위 차이 추정) | D-09 문안은 "35~36" |
| S3 | `window.confirm` 잔존 | `ux` §1.12 kta1·ktc1(주석)·ktdm3·map2·weather1 | velocity "8건" | 코드 7건 | D-13 baseline 목록 7건 |
| S4 | Actions major | `vm` §3.1 현행 v4/v5, §4.4 최신 v7 | common `docs.yml` v6(`ci` §4 사실) | common 자체는 v6 태그 → SHA 핀 정비 | D-18 |
| S5 | Python floor 표현 | `vm` §5.1 후보 A `requires-python >=3.12`(앱 정렬) | `be` §5.3 common 3.11 | 두 문서는 대상이 다름(앱 vs common 패키지) | D-06/D-15 |
| S6 | weather tokens 소비 | `dt` §3.6.3 "Tailwind 없는 앱 포함 즉시 소비" | `inv/weather` §3.1 map 어휘 294회 참조·`--rail` 17rem | `dt` 문장은 별칭 shim 전제 생략 | §6 M-1 |
| S7 | Node 승격 시점 | `vm` §4.4(24 Active 종료 2026-10-20, 26 LTS 2026-10-28) | coordinator·velocity "2026-10 이후 24" | 26이 차기 Active LTS | D-06 |

## 6. 세 레지스터 모두에서 빠진 결정

| ID | 빠진 결정 | 왜 첫 릴리스에 필요한가(근거) | 기본값 제안 |
|---|---|---|---|
| M-1 | **레거시 어휘 별칭 shim** | weather(map 어휘 294회·legacy 15종·`--rail` 17rem, `inv/weather` §3.1), concierge(`--ktc-*` 125회, `dt` §3.6.1), pinvi admin(`--color-admin-*` 19종), geo(`--ui-*` 54회 + `--color-*` 원색)는 `--kt-*`로 직접 갈아탈 수 없다. 세 레지스터는 "앱이 별칭 소유"라고만 적고 파일·소유·검증을 정하지 않음 | common이 `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`) 1개를 **선택 파일**로 제공, 앱 고유 접두(`--ktc-*`, `--color-admin-*`, `--ui-*`)는 앱 파일. 시각 diff 0 판정은 shim 포함 상태로 |
| M-2 | SemVer 0.x·파괴적 변경 정의·deprecation | `prior` §8 [E7] "0.x라도 무통보 파괴 금지, 정렬 기본값·키보드·토큰 계약도 공개 API". 레지스터는 "마크업 변경=major"(risk-first T-204)만 | 0.x 동안: minor = 파괴 허용(rc + 소비자 PR 검증 + 마이그레이션 노트 필수), patch = 비파괴. 파괴 항목 = 토큰 이름/의미·data-slot/testid·prop 기본값·정렬 모드·CSS 파일 경로. 토큰 이름 폐기는 1 minor 동안 alias 유지 |
| M-3 | common 자체 npm workspace·툴체인 선언 | `packages/tokens`·`packages/ui` 두 npm 패키지의 lock·`packageManager`·`.nvmrc`를 어느 레지스터도 정하지 않음. D-06 npm 결정(E1)과 직결 | 루트 `package.json` `workspaces: ["packages/*"]`, `packageManager: "npm@11.19.1"`, `engines.node ^22.12.0`, `.nvmrc 22.23.1`, 루트 `package-lock.json` 커밋, CI `npm install -g npm@11.19.1` 후 `npm ci` |
| M-4 | Windows 개발자 프로필(현 사용자 환경) | 세 레지스터는 Linux/WSL 정본만 결정. 현재 common 파일은 PowerShell fence·`python`(E13). 검사 도구가 Windows에서 돌아야 한다는 velocity D-03만 있음 | `docs/dev-environment.md` §"Windows 보조 프로필": Git Bash + `py -3 -B -X utf8` 등가표, `.gitattributes` LF·`*.ps1 crlf`, `git config core.autocrlf false`, npm은 nvm-windows. runbook fence는 bash 1벌 + "Git Bash 동일" 주석 |
| M-5 | 코드 주석 언어 | `inv/ktdm` §9 "코드 주석·docstring·커밋까지 한국어 → common 코드 주석 언어 정책 결정 필요"(조사가 직접 요구). `dc` C10은 Markdown만 | 주석·docstring 한국어 기본, SPDX/Origin 헤더 키워드·식별자·외부 인용은 영어. 커밋 제목은 Conventional Commits 영어 type + 한국어 문장(map·ktdm 관행) |
| M-6 | Hallmark 스탬프의 common 파일 내 취급 | risk-first C21 "SPDX 다음 줄에 common 스탬프" vs velocity C21 "registry 아이템에 미포함". `lic` B3(원천 미확인)·`ux` Q7 | common 배포 파일에는 스탬프 **미포함**(B3 미해결, 스탬프는 앱 산출물). 소비자가 사본에 붙이는 것은 허용, drift 비교는 선두 주석 블록 정규화. 형식·위치 규칙만 ux-guide에 |
| M-7 | 폰트 파일·OFL 고지 위치 | `lic` Q10 "pretendard 번들 시 OFL 사본 위치". 레지스터는 "로딩은 앱 책임"까지만 | common은 폰트 파일 미배포(스택 문자열만). `THIRD_PARTY_NOTICES`에 OFL 항목 + "번들하는 앱이 npm `pretendard` 패키지 내 LICENSE를 산출물에 유지" 규칙 |
| M-8 | e2e 셀렉터 계약 등재 범위 | risk-first ui-contract.md(pinvi testid), velocity(pinvi 확장 흡수). geo `section.panel .panel-header h2`·`pre.json-box`(`inv/geo` §9)는 어느 쪽도 계약에 없음 | ui-contract.md에 "계약 등재 = 소비자 채택 시 e2e가 실제 참조하는 셀렉터"로 규칙화. geo 셀렉터는 geo가 ui를 채택하는 T-444에서 등재 여부 판정 |
| M-9 | AGENTS 공통 절 세부(dc Q1~Q3, cm D26) | geo Goal-Driven 추가 불릿 2개, SKILL 라우터화, pinvi "ADR > AGENTS" — 세 레지스터 모두 침묵 | 공통 절 A는 6개 저장소 동일 문구 유지(geo 불릿은 로컬 추가 허용), SKILL은 `dc` C4(매뉴얼+DO NOT 유지, 시작점 표 추가), pinvi ADR 우선순위는 로컬 예외 |
| M-10 | 문서 언어 예외(design.md 영문) | `dc` C10 판정 존재, `inv/airport` §9·`inv/weather` §5 영문 문서. 레지스터 미언급 | `dc` C10 채택: 벤더링 원문·원칙 소제목·인용 reference 3종 예외, `design.md` 본문은 한국어 요구(kta·pinvi·weather 이행 대상) |
| M-11 | `@config`/`@theme` 실효값 검증 절차의 일반화 | risk-first T-441(geo)만. concierge·pinvi web도 `@config` 보유(`cm` §3.3) | `docs/runbooks/consumer-adoption.md`에 "`@config` 보유 앱은 빌드 산출 CSS로 동명 utility 실효값 확인 후 제거" 공통 단계 |
| M-12 | CHANGELOG 구조(패키지 3개) | `dc` §1.10·`cv` R5.5는 단일 파일 규약만 | 루트 `CHANGELOG.md` 단일, `## [Unreleased]` 아래 패키지별 H3(`tokens`/`ui`/`py`/`standards`), 릴리스 절 제목에 태그명 |
| M-13 | 접근성 자동 검사 도구 | `ux` G9·`inv/pinvi` e2e a11y 스펙 존재. 레지스터는 대비 검사만 | Phase 2 ui 단위 테스트에 `axe-core` 기본 검사 1회(smoke), 필수 gate는 아님 |
| M-14 | npm scope·PyPI 이름 확인 evidence | E15 | T-006 evidence에 `npm view @kor-travel/tokens`·`pip index versions kor-travel-common` 명령·시각·출력 기록 |

## 7. 사용자 확인이 필요한 열린 결정(기본값 포함)

| # | 결정 | 선택지 | 기본값(이 판정) | 막히는 것 |
|---|---|---|---|---|
| O1 | pinvi 라이선스·공개(L6) | 공개 + GPL-3.0-or-later / 사내 비공개 | 공개 + GPL-3.0-or-later(이미 GPL 이식 코드·AGENTS "공개") | pinvi 추출(B1)·pinvi 1차 소비 여부(D-16) |
| O2 | ktc·ktdm 라이선스(L8) | GPL 정렬 / common §7 추가 허가 | GPL 정렬 | concierge·ktdm 코드 채택 |
| O3 | UI 배포 방식 | npm 1차 / shadcn 레지스트리 1차 | npm 1차(`ui` §6.3 무접두 비용 우위) + 매니페스트·drift 도구는 공통 채택 | D-10·Phase 2 전부 |
| O4 | 클래스 네임스페이스 | 무접두 공통 이름 / `kt-` 접두 | 무접두 + T-101 충돌 검사, 충돌 시 접두 | D-10 |
| O5 | TS 기준선·airport 7.0.2 | 5.9 통일(하향) / 예외 등록 | 예외 등록, ESLint 도입 시 재판정 | T-433 |
| O6 | Node/npm | 22 + npm 11.19(CI 명시 설치) / 22 + 동봉 10.9 floor / 24 | 22 + 11.19 명시 설치(pinvi 모델), map 12.0.1 예외 | D-06·M-3 |
| O7 | Python 앱 floor 3.12 시점 | 지금 / Phase 4 / 미정렬 | Phase 4(앱별) — common은 3.11 | D-15 |
| O8 | 다크 모드 | 앱 오버라이드 dark 필수 / 선택 | 선택, light 기본, common tokens는 `.dark` 완비 | D-12 |
| O9 | 메트릭 접두 map·pinvi | 영구 예외 / 기한부 | 기한 없는 예외 + `review` 날짜 필드(대시보드 평가 task 후 재판정) | D-15 |
| O10 | health 경로 geo `/v1/healthz` 별칭 기간 | 무기한 / 기한부 | 무기한(probe·Prometheus 결합) | D-14 |
| O11 | 429 코드명·422/400 | 통일 / 앱 소유 | common 기본 사전(`TOO_MANY_REQUESTS`, 422) + 앱 덮어쓰기, geo 400 예외 | D-14 |
| O12 | airport Admin 정의 | 현 백업 패널 / 신설 admin | 현 실체 | M-20 |
| O13 | 마커 팔레트 정본 | map Tableau / pinvi Material | map 소유 확정 요청 | M-26 |
| O14 | Renovate 설치 | 설치 / dependabot 템플릿 | 템플릿 | D-07 |
| O15 | 재사용 워크플로 cross-repo 호출 조건 | 공개 확인 / fallback | 공개 전제 + 체크아웃 fallback 문서 | D-18 |
| O16 | dirty 이탈 경고 | 규약 포함 / 미포함 | 미포함(8표면 모두 없음) | D-13 |
| O17 | pinvi admin 44px 예외 2쪽 | 영구 / 36px 복귀 | 영구 예외 등록 | D-13 C6 |
| O18 | Hallmark 스탬프 common 파일 포함 | 포함(SPDX 다음 줄) / 미포함 | 미포함 | M-6 |
| O19 | Windows 프로필 수준 | 보조(문서·검증만) / 동등 | 보조 + 도구 실행 보장 | M-4 |
| O20 | 포트 `130xx`·airport 14002·`-latest` | — | 예외 등록·`-latest`는 ktdm 결정·130xx는 점유 확인 후 | T-014 |
| O21 | prod redaction 범위 | `docs/`만 / 전체 트리 | common 전체 트리, 소비자 opt-in | T-009 |

## 8. 통합 계획에 반영할 수정 지시(레지스터 → 최종안)

| 대상 | 지시 |
|---|---|
| coordinator D-06 | npm 행·ESLint 행·Python 행·engines 값 정정(E1·E2·E4·E5), 표를 3열(floor/recommended/consumer pin)로 교체 |
| coordinator D-01·D-09 | `lucide-react` peer 제거(인라인 SVG), `config`·`api-client-core` 보류 |
| coordinator D-02·D-17 | `decisions.md` 미보유, cva Apache-2.0 고지 추가 |
| risk-first D-16 | "B1·B9로 pinvi 소비 불가" → "L6 미결 시 pinvi 채택 PR은 BLOCKED(정책)"로 재서술, ui 1차에 pinvi admin(L6 조건부) 복귀 |
| risk-first T-461·T-101 | 별칭 shim 파일(`aliases/map-vocabulary.css`) 산출물 추가, "값 diff 0"은 shim + weather `--rail` override 포함 조건으로 |
| risk-first T-002 | PowerShell fence 제거·`python3` 표기·`tools/README.md`·`docs.yml`(`python`, `@v6` 태그) 정정을 범위에 추가; T-452의 ktdm 항목을 T-47x로 분리 |
| velocity D-06·D-07 | npm "동봉" 문구 정정(E1); Python floor 표기는 이미 3.11로 정합 |
| velocity D-11 | "git 없는 map api.Dockerfile" → "미확인" |
| velocity D-13·O20 | `window.confirm` 8 → 7(+주석 1) |
| velocity F.2 | T-413/414/423/432/443/454/463 → T-480a~T-485 계열로 재배치(§2.1 대역) |
| velocity D-10 | `kt-` 접두는 O4 결정 전 후보로 강등, 충돌 검사 스크립트를 T-101에 추가 |
| 세 레지스터 공통 | §6 M-1~M-14를 결정 레지스터에 추가(최소 M-1·M-2·M-3·M-4는 Phase 0/1 task로) |
| 조사 문서 정정 메모(수정 금지, 설계 문서에서 인용 시) | S1 `/readyz`, S2 "35~36", S3 7건, S5 "앱 floor vs common floor", S6 shim 전제, S7 Node 26 |

## 9. 근거 파일

- 레지스터 3편(scratchpad), `docs/survey/README.md` §2·§5·§6, `commonality-matrix.md` §1~§4, `cross/version-matrix.md` §1.1~§1.8·§2.1~§2.7·§3.1~§3.6·§4.2~§4.4·§5.1~§5.3·§6·§7·열린 질문, `cross/licensing.md` §2.1~§2.6·§3.1~§3.7·§4·§5·§6, `cross/design-tokens.md` §3.1~§3.6·§5, `cross/ui-components.md` §2~§7, `cross/ux-patterns.md` §1.11~§1.14·§2~§5, `cross/backend.md` §2.1·§3~§7, `cross/openapi.md` §2~§6, `cross/ci-deploy.md` §1.1~§1.3·§2~§4·열린 질문, `cross/docs-conventions.md` §1·§2·§3·§4·§5, `cross/canview-structure-checklist.md` §1~§5, `inventory/*.md` 7편 §1·§3·§8·§9·§10·§11.
- common 작업 트리: `docs/tasks-rule.md`, `docs/runbooks/documentation-maintenance.md`(88~91행 PowerShell fence), `docs/reviews/README.md`, `tools/validate_plan.py`, `tools/README.md`, `.github/workflows/docs.yml`.
- 원 저장소(읽기 전용): `F:/dev/kor-travel-common-survey/ktm-main/package.json`(5~8행), `F:/dev/kor-travel-concierge/frontend/node_modules/tailwindcss/package.json`(exports 55~60행), `F:/dev/kor-travel-common-survey/pinvi/apps/web/package.json`(35행), `F:/dev/kor-travel-common-survey/ktm-main/packages/kor-travel-map-admin/frontend/package.json`(34행).
- 선행 보고서 `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` §1·§3·§5·§7·§8·§9·§10·§11.
