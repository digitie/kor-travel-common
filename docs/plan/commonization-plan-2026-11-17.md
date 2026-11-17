# 공통화 재조사와 실행 계획 — 2026-11-17

- 정본 지위: 다섯 저장소(pinvi·kor-travel-map·kor-travel-weather·kor-travel-transport·kor-travel-docker-manager)의 코드에서 **무엇을 공통으로 만들 수 있고 무엇은 만들면 안 되는지**를 고정 커밋 기준으로 다시 조사한 결과와 실행 순서다. 이 문서는 근거와 계획이며 규범이 아니다. 규칙은 [standards](../standards/README.md)·[ADR](../adr/README.md), 실행 범위와 수용 기준은 [task 원장](../tasks.md)과 상세 task가 정본이다.
- 상태: **초안(적대 리뷰 2회 반영)**. 소유자 요청(2026-11-17)에 따른 작성본이다. 1회차 finding 19건과 2회차 finding 25건을 반영했다. 판정은 제안이고 ADR·task로 옮겨지기 전에는 결정이 아니다.
- **소유자 결정(2026-11-17).** 열린 결정 넷이 정해졌다. 이 문서의 '결정 대기' 표현보다 아래가 우선한다.
  - ADR-019: 안 1(정책과 Node/npm 축을 호출자의 `common-ref`에서 읽기 + 막지 않는 지연 보고) accepted → [ADR-019](../adr/019-frontend-policy-guard-model.md). T-023 DONE, T-024 READY.
  - ADR-020: §1.5 15행을 권고대로(수락 12·보류 2·수락과 보류로 나눈 것 1·거부 0) accepted → [ADR-020](../adr/020-python-ui-scope-after-resurvey.md). T-027의 외부 선행 충족, T-022는 대조표·task 분할이 남았다.
  - T-416: 채택. 값은 22.23.1이 아니라 **Node 26.13.1**(2026-11-17 nodejs.org 색인의 최신 LTS 줄 최신 patch)·npm 12.0.1(공통 축 유지). 공통 축을 26.13.1로 올리는 [T-029](../tasks/T-029-node-axis-to-latest-lts.md)를 더했고 T-417의 선행이 됐다.
  - T-486b: 권고대로. 영향 자료를 먼저 만들고, 자료가 권고를 뒷받침하면 구현한다. 2026-11-17 자료가 차단 조건(map worker의 같은 job tag 값 동시 run이 설계상 4, 실측 2)에 걸려 구현하지 않았고 소유자 재결정을 기다린다([T-486b](../tasks/T-486b-ktdm-shared-dagster-per-job-limit.md)의 "영향 자료와 결정").
- 성격상 §1~§3·§7은 조사 스냅샷(survey), §4~§6은 계획(plan)이다. 소유자가 문서 하나를 요청해 한 파일에 두었다. 기준 커밋을 바꿔 다시 조사할 때는 이 문서를 고치지 않고 새 문서를 만든다.
- 인용 형식: `<저장소 약칭>:<저장소 상대 경로>:<줄>`. 약칭과 경로 접두는 §1.1 표를 따른다. `✔`는 작성자가 하위 조사 뒤 같은 커밋에서 직접 다시 읽거나 `diff`·`cmp`로 재확인한 인용이다. 표시가 없는 인용은 하위 조사 결과이며 한계는 §7에 적었다.

## 1. 범위·방법·기준

### 1.1 대상과 기준 커밋

모든 관찰은 2026-11-17에 받은 각 저장소 `origin/main`의 아래 커밋에 고정한다. 로컬 작업 checkout은 읽지 않았다.

| 약칭 | 저장소 | 기준 커밋 | 이 문서의 경로 접두 |
|---|---|---|---|
| P | pinvi | `b160594972dafe9458f220499552ff539c4c70d7` | `PW`=`apps/web`, `PM`=`apps/mobile`, `etl/`=`apps/etl/pinvi/etl/` |
| M | kor-travel-map | `f1788da922c118650fc93e05aae42b3d0f5159f3` | `MA`=`packages/kor-travel-map-admin/frontend`, `api/`=`packages/kor-travel-map-api/src/kortravelmap/api/`, `dag/`=`packages/kor-travel-map-dagster/src/kortravelmap/dagster/`, `lib/`=`src/kortravelmap/` |
| W | kor-travel-weather | `e68f16a75b033ecb2ceaf83b6d87a3d73bb614f4` | `WA`=`packages/kor-travel-weather-admin/frontend`, `wapi/`=`packages/kor-travel-weather-api/src/kortravelweather_api/`, `wdag/`=`packages/kor-travel-weather-dagster/src/kortravelweather_dagster/`, `wlib/`=`src/kortravelweather/` |
| T | kor-travel-transport | `6009537986d59bd8b401e165f5d81a1007e5ba29` | `TA`=`packages/kor-travel-transport-admin/frontend`, `TP`=`frontend`, `app/`=`backend/app/` |
| D | kor-travel-docker-manager | `31d56e4e6c43b14258cad93495c94630f4b82035` | `DM`=`frontend`, `kdm/`=`backend/src/kor_travel_docker_manager/` |
| C | kor-travel-common(이 저장소) | `97f8ed98360518e7afc96e89a5b45a6a478ac955` | `cpy/`=`packages/py/kor-travel-common/src/kortravelcommon/` |

transport는 2026-09 조사의 `kor-travel-airport`가 이름을 바꾼 저장소다. 원장의 airport 대역(T-430~T-439, T-482)을 그대로 잇는다. geo·concierge는 이번 범위가 아니어서 다시 조사하지 않았다. 두 저장소가 근거였던 2026-09 판정은 이 문서가 뒤집지도 확인하지도 않는다.

기준 커밋 뒤에 바뀐 것 가운데 판정에 닿는 것은 셋이다. map #1504와 weather #243이 병합돼 두 저장소도 후보 12를 벤더한다. weather의 guard 호출은 `97f8ed9`로 올랐고 map은 `55a921b` 그대로다. kor-travel-weather #244(`8c3b4744`)가 K-51의 검증 차이를 고쳤다.

### 1.2 방법

1. 여섯 저장소를 새로 받아 위 커밋에 고정했다. 읽기 전용이며 테스트·빌드·설치·배포와 운영 호스트 접근은 하지 않았다.
2. 일곱 영역(백엔드 골격, 백엔드 횡단, 도메인 헬퍼, Dagster, 프론트 셸·UI·API client, 프론트 지도·e2e·lint, Ops·CI)을 나눠 조사했다. 각 영역은 다섯 저장소의 위치, 같은 점, 다른 점, 떨어져 있어야 하는 이유를 줄 번호와 함께 보고했다.
3. 작성자가 판정에 쓰는 인용을 골라 같은 커밋에서 다시 읽었다(`✔`). 다시 읽은 인용에서 어긋난 것은 없었다. GitHub의 PR 병합 시각과 CI 결과는 `gh`로 조회했다.
4. 판정은 세 가지다. **지금 공유**(공유 수단의 비용을 감안해도 이득이 분명하고 선행 결정이 없다), **나중에 공유**(이득은 있으나 선행 결정·배치 릴리스·세 번째 소비자 같은 조건이 붙는다), **공유하지 않음**(사본처럼 보여도 계약·도메인·보안 경계가 달라 합치면 손해다).

"지워지는 줄 수"는 인용한 줄 범위에서 어림한 값이며 시험 리팩터링으로 잰 값이 아니다.

### 1.3 이전 조사·계획과의 관계 — 무엇이 새로운가

| 축 | 2026-09-06 조사·계획([매트릭스](../survey/commonality-matrix.md), [백엔드 횡단](../survey/cross/backend.md), [브리프](design-brief.md)) | 이번 재조사에서 달라진 것 |
|---|---|---|
| 대상 | 7 저장소(airport·concierge·docker-manager·geo·map·weather·pinvi) | 5 저장소. airport는 transport로 개명. geo·concierge 제외 |
| Python 공통 | 후보 C1~C21, 실행 task T-302~T-312, 소비 T-480~T-486. 1차는 C12 export·C4 health·C13 time·C20 quality | 계획한 1차·2차 모듈(C12·C4·C13·C20, C1·C9·C7·C2·C3)은 구현되지 않았다. `http`(C15 자리)와 `dagster`(C18 자리) 모듈은 있지만 내용이 계획과 다르다. 실물 `kortravelcommon`은 운영 장애가 요구한 묶음이다: Dagster 복구·coalescing·회수 sensor, code-server·HTTP·gRPC probe, 응답 상한 HTTP, deadline, 정체 시계, 역지오코딩 갱신(T-319 계열). 원장은 T-302를 READY, T-303~T-312를 BLOCKED로 둔 채다 |
| React UI | T-201~T-214(base-ui 전제) | T-218이 Radix 기반 `@kor-travel/ui` 0.2.1·`tokens` 0.1.2·`toast` 0.1.1과 중앙 guard를 실물로 만들었다. 원장은 T-201(골격)을 BLOCKED로 둔 채다. [ui-contract](../standards/ui-contract.md)가 약속한 관리자 부품은 패키지에 없다 |
| 공유 비용 | 배포 방식 후보 비교까지. 채택 뒤 운영 비용은 다루지 않음 | 2026-11-17 실측: 정책 한 번 바꾸자 다섯 저장소에 재vendor PR 5개·파일 80개(§2.2) |
| 판정 근거 | 저장소 수와 함수 동일성 | 다섯 저장소의 현재 줄 번호와 차이 분석. accepted ADR·standards와 어긋나는 판정은 §1.5 표에 모두 모았다 |
| 새로 본 것 | — | 수집 결과 run tag, probe 사본 세 종류, 관리자 부품 45개 파일 동일 사본, 로컬 경로 정규화 사본 차이, 공용 Dagster instance 설정 공백, Valkey, 빌드 영수증 생산자 fork |

이 문서는 기존 ADR·standards·task를 고치지 않는다. 기존 결정과 어긋나는 판정은 §1.5에 "제안"으로 모았다. 반영은 [T-022](../tasks/T-022-ledger-reality-reconcile.md)(원장 재분류와 ADR-020 초안)와 [T-027](../tasks/T-027-standards-after-reclassification.md)(standards 본문)이 소유한다.

### 1.4 판정에 쓴 제약

| # | 제약 | 출처 |
|---|---|---|
| R1 | 내부 서비스끼리 서로의 계약을 핀하지 않는다(vendored OpenAPI·SHA 결박 금지). 런타임 검증과 자기 fixture로 대신한다 | 소유자 지시(2026-10-03) |
| R2 | 단순함이 결박보다 우선이다. 강제 계층을 더 쌓지 않는다 | 소유자 지시(2026-09-22); `AGENTS.md` Simplicity First |
| R3 | Manager는 범용으로 유지한다. 렌더링된 모델에서 유도하고 서비스별 리터럴을 넣지 않는다 | 소유자 지시 |
| R4 | npm·PyPI에 게시하지 않는다. 프론트 패키지는 벤더 tarball이다 | [ADR-014](../adr/014-common-implementation-without-registry-publishing.md) |
| R5 | common main의 버전을 하나 바꾸면 그 패키지를 선언한 모든 소비자의 guard가 재vendor 전까지 실패한다. Node/npm 도구 축을 바꿔도 같다(§2.2). 이 수단으로 공유하는 비용은 실제다 | 2026-11-17 실측(§2.2) |
| R6 | Map 라이브러리 계층은 `fastapi`·`starlette`를 import하지 않고(`M:pyproject.toml:311-328` ✔) provider adapter·wrapper를 만들지 않는다 | Map ADR-006·ADR-020 |
| R7 | weather·transport는 다른 팀(Codex)이 주로 유지한다. 그 저장소의 채택 비용과 시점은 그 팀이 정한다 | 소유자 지시 |
| R8 | 소비자 한 곳의 관찰만으로 공통으로 올리지 않는다. env 이름·헤더 이름·지표 이름·오류 형식은 배포 계약이다 | `AGENTS.md` §6-7·§6-9 |

### 1.5 기존 ADR·standards와 어긋나는 판정(제안)

아래 판정은 accepted [ADR-011](../adr/011-python-common-package.md)·[backend-stack](../standards/backend-stack.md)·[openapi](../standards/openapi.md)·[ci-deploy](../standards/ci-deploy.md)·[ui-contract](../standards/ui-contract.md)와 어긋난다. 이 문서가 그 결정을 바꾸는 것이 아니다. T-022가 ADR-020 초안으로 올리고, 채택된 것만 T-027이 standards에 옮긴다. 채택 전에는 기존 결정이 유효하다.

| 모듈 | 기존 결정 | 이 문서의 판정 | 근거 절 |
|---|---|---|---|
| C12 OpenAPI export CLI | ADR-011 1차, openapi의 export drift 행, ci-deploy의 `openapi-drift.yml`, T-303·T-309 | 나중에 공유(작게). 직렬화 규칙이 셋 다 달라 맞추는 비용이 줄 수 이득보다 크다 | K-16 |
| C4 health 라우터 | ADR-011 1차, BE-15, T-304 | 공유하지 않음. probe만 공유(K-10) | K-15 |
| C13 time | ADR-011 1차, BE-19, T-304 | 나중에 공유(낮음). 저장소 안 정리가 먼저 | K-35 |
| C20 quality(ruff·mypy 베이스, `python-quality.yml`) | ADR-011 1차, BE-6~BE-11, T-305, T-401의 Python 절반 | 공유하지 않음. 베이스의 공통 부분은 이미 같고 나머지는 저장소별 선택이다 | K-71 |
| C1 settings 베이스 | ADR-011 2차, BE-12, T-306 | 공유하지 않음 | K-12 |
| C9 db 엔진 팩토리 | ADR-011 2차, BE-23, T-306 | 공유하지 않음 | K-13 |
| C2 logging | ADR-011 2차, BE-13, T-307 | request-id 미들웨어만 나중에 공유. 로깅 설정은 공유하지 않음 | K-23, K-24 |
| C3 metrics | ADR-011 2차, BE-14, T-307 | 공유하지 않음 | K-24 |
| C5 errors·problem | ADR-011 3차, BE-16, T-308 | 공유하지 않음 | K-19 |
| C10 alembic 템플릿 | ADR-011 3차, BE-24, T-308 | 공유하지 않음. 규약 문장만 | K-14 |
| C15 http(재시도·circuit 정책) | ADR-011 3차, BE-20, T-308 | 공유하지 않음. 응답 상한 요청(`bounded_request`)은 이미 있다 | K-18 |
| C18 dagster(Definitions 3단 폴백·`dagster.yaml` 템플릿) | ADR-011 3차, BE-21, T-308 | 공유하지 않음. 복구·coalescing·회수 sensor는 이미 있다 | K-47, K-49 |
| `validateForm`(헤드리스 폼 검증) | ui-contract §4.6, T-210 | 공유하지 않음. 규칙 기반 구현은 map 한 곳이다 | K-55 |
| UI 엔진 표기 | ui-contract §2·§3이 `@base-ui/react` | 실물은 `radix-ui`(ADR-017). 문서를 실물에 맞춘다 | K-50 |
| C16 security headers·C17 cors | ADR-011 3차, BE-17, T-308 | 공유하지 않음. 헤더 값이 제품별이고 CORS는 이미 Starlette `CORSMiddleware`가 공통이다 | K-25 |

기존 결정과 **같은 방향**인 것: C6 pagination(보류 → 코덱만 나중에, K-20), C7 `public_api_key`(유지, K-17), C8 `trusted_proxy`(유지, K-17), C11 testing(유지, K-75), C14 좌표 경계(금지, K-34), `ConfirmDialog`(앱 소유·T-508, K-50), 세션·로그인(ADR-015·BE-22, K-53).

## 2. 공유 수단과 비용

### 2.1 지금 쓰는 수단

| 수단 | 쓰는 곳 | 한 번 바꿀 때 | 함대 결합 |
|---|---|---|---|
| A. Python git 커밋 핀 | `P:apps/api/pyproject.toml:9`·`P:apps/etl/pyproject.toml:12`(`c289b46`), `M:packages/kor-travel-map-api/pyproject.toml:31`·`M:packages/kor-travel-map-dagster/pyproject.toml:25`(`aa232ad`), `W:pyproject.toml:15,55`·`W:packages/kor-travel-weather-dagster/pyproject.toml:11`(`aa232ad`), `T:backend/pyproject.toml:11`(`c289b46`) ✔ | 새 기능이 필요한 소비자만 핀 PR 1개 | 없음 |
| A'. 벤더 wheel + hash | `D:docker/dagster-host/vendor/kor_travel_common-0.1.0.dev0-py3-none-any.whl`, `D:docker/dagster-host/requirements.txt:555-556` ✔ | wheel 교체 PR | 없음 |
| B. 벤더 tarball + 중앙 원장 guard | 프론트 7개 표면(`<frontend>/vendor/*.tgz`, `common-artifacts.json`) | **모든** 소비자 재vendor PR. 그 전까지 guard 실패 | 강함 |
| C. 재사용 workflow를 커밋으로 호출 | `frontend-consumer-guard.yml@<sha>` 호출 7곳(P·M·D 하나씩, W·T는 `ci.yml`과 독립 workflow에 하나씩) | 호출 SHA PR(검사 코드에 한함) | 코드는 없음, 정책 데이터는 B와 같음 |
| D. 출처를 적은 복사 | `T:TA/lib/vendor/map-marker-react/`(Map 사본) ✔, `D:docker/dagster-host/build-bytecode.py`(`C:cpy/build_bytecode.py`와 동일 ✔), Manager↔transport code-server probe(스크립트가 일치를 강제) | 손으로 다시 복사 | 약함. 표류 가능 |
| E. 규약 문서 | `docs/standards/*` | 없음 | 없음 |

A의 핀 세 가지(`aa232ad`, `c289b46`, wheel 원천 `b4f7f3d`)는 `packages/py` 내용이 서로 같고 `97f8ed9`와도 같다(`git diff aa232ad c289b46 -- packages/py` 빈 결과, `c289b46..HEAD -- packages/py` 커밋 0개 ✔). 패키지 버전은 어느 커밋에서나 `0.1.0.dev0`이라 버전으로는 구분되지 않는다(`C:packages/py/kor-travel-common/pyproject.toml:9` ✔).

### 2.2 2026-11-17 실측: 정책 한 줄의 함대 비용

guard는 검사 **코드**를 호출자가 고정한 커밋에서 받고(`C:.github/workflows/frontend-consumer-guard.yml:44` ✔), 비교할 **정책 데이터** 세 파일은 항상 `main`에서 받는다(`:49-56`, `:98-99`, `:106` ✔). 정책은 패키지마다 버전 하나만 갖는다. 생성기가 둘 이상이면 던지고(`C:tools/sync_frontend_policy.mjs:14-15` ✔), 검사기는 선언·tarball 파일명·lock·원장·중앙 정본을 그 한 값과 대조한다(`C:tools/check_frontend_dependencies.mjs:26`, `:102-111`, `:147`, `:152-153` ✔). 이 구조는 의도다([frontend-libraries](../standards/frontend-libraries.md)의 "검사와 갱신" 절: 앱이 오래된 정책을 유지해도 최신 정본과 다르면 중앙 CI에서 실패한다).

| 시각(UTC) | 일 |
|---|---|
| 02:07:28 | common #57 병합. `vworld-map-web` 1.0.3→1.0.4·`vworld-map-rn` 1.0.1→1.0.2 정책. 이 순간부터 옛 버전을 가진 소비자의 다음 guard 실행은 실패한다 |
| 02:24:10 | common #58 병합(산출물 동결) |
| 02:38:06 | pinvi #763 병합(파일 26개) |
| 03:09:25 | docker-manager #605 병합(파일 8개) |
| 03:11:05 | transport #205 병합(파일 20개) |
| 조사 시점 | map #1504(파일 12개)·weather #243(파일 14개)은 열려 있음. 두 저장소는 후보 11에 머문다(둘 다 그 뒤 병합됐다) |

- 재vendor PR 5개, 파일 80개다. geo·concierge도 같은 guard의 소비자이지만 이번에 조회하지 않았다.
- **`ui`·`tokens`·`toast`는 실행 코드와 CSS가 바뀌지 않았다.** tarball이 정책 사본(`dependency-policy.json`)을 싣고 있어서, 무관한 `vworld-map-web` 한 줄 때문에 세 패키지가 patch 버전을 올렸다(common #57 변경 파일 17개 중 패키지 쪽은 `package.json`·`dependency-policy.json`·테스트뿐 ✔; `ui` 0.2.0과 0.2.1 tarball은 같은 94개 파일이고 다른 것은 `package.json`·`dependency-policy.json`·`check-dependencies.mjs` 셋).
- 검사기는 소비자가 선언하지 않은 산출물은 건너뛴다(`check_frontend_dependencies.mjs:145` ✔). 그래서 지도가 없는 docker-manager와 transport 공개 웹은 `vworld-map-web`만 바뀌었다면 영향이 없었다. 두 저장소가 PR을 내야 했던 이유는 위의 내장 사본 때문이다.
- 소비자는 **자기가 고정한 판의 검사기**를 실행한다. 지금 고정된 판은 둘이다(`55a921b` map, `97f8ed9` 나머지 넷과 geo·concierge; `9e16393`은 `tools/`가 `97f8ed9`와 같다). 두 판 모두 정책에서 `versions`·`profiles`·`forbidden`·`artifactPackages`·`patchedRadixPackages`와 정본의 `packages`만 읽고(각 커밋의 `tools/check_frontend_dependencies.mjs` ✔), 소비자가 선언하지 않은 산출물은 건너뛴다(`:145@97f8ed9` ✔, `:129@55a921b`).
- **Node/npm 도구 축도 `main`에서 읽는다.** `97f8ed9` 판의 guard는 `check:toolchain --registry common-policy/versions.json`을 main 값으로 실행하고(`C:.github/workflows/frontend-consumer-guard.yml:105-106` ✔), 그 검사는 소비자의 `.nvmrc`·`engines`·`packageManager`·Node 이미지가 `axes.node.recommended`·`axes.npm.recommended`와 같기를 요구한다(`C:tools/check_node_toolchain.mjs:247-248` ✔). 이 값은 2026-11-13에 바뀌었다(22.23 → 22.23.1, npm 11.19 → 12.0.1). 다음 Node/npm patch가 main에 병합되면 여섯 소비자가 같은 날 실패한다. map은 `55a921b`에 도구 단계가 없어 이 축에서는 빠진다.
- weather와 transport에서 PR을 막는 guard는 `ci.yml` 안의 호출이다. 독립 workflow는 `workflow_dispatch` 전용이다(`T:.github/workflows/common-frontend-policy.yml:4-5` ✔). 그래서 main 정책이 움직이면 다른 팀의 Python만 바꾼 PR도 막힌다.
- 정책에 패키지를 **더하기만 해도** `ui`·`tokens`·`toast`가 다시 pack된다. 세 패키지의 내장 사본은 생성된 정책 파일의 복사본이고(`C:packages/ui/scripts/sync-policy.mjs:5-6` ✔), smoke lock이 동결 pack의 integrity를 고정하기 때문이다(common journal 2026-11-17).
- map #1504의 첫 실행은 guard에서 실패했다. 호출 SHA를 최신으로 올리자 map에 없는 정확 Node/npm 도구 규칙이 걸렸고(`도구 규칙: 검사 파일·경로를 읽을 수 없습니다`), 두 번째 커밋이 호출 SHA를 `55a921b`로 되돌렸다 ✔. map은 검사 코드가 44커밋 뒤처진 채(`git rev-list --count 55a921b..97f8ed9` ✔) 정책만 최신을 따른다.
- 한 달 동안 정책 세 파일이 바뀐 날은 나흘(11-11, 11-12, 11-13, 11-17), 커밋 19개다(`git log --since=2026-10-17` ✔).
- common의 11-17 journal은 "기존 소비자는 고정 SHA를 쓰므로 영향이 없다"고 적었고(`C:docs/journal.md`의 후보12 두 항목 ✔), 같은 날 docker-manager의 journal은 "공통 guard는 고정 ref와 무관하게 common main의 정책·정본을 읽으므로" 옛 버전으로는 실패한다고 적었다(`D:docs/journal.md` 첫 항목 ✔). 정책을 바꾸는 쪽도 이 결합을 놓쳤다.

### 2.3 여기서 끌어낸 원칙

1. 새 공통 **코드**는 A(Python 핀)로 갈 수 있으면 A로 간다. 결합이 없다.
2. B로 가는 변경은 **한 번에 묶는다.** 부품 하나마다 버전을 올리지 않는다. 모든 소비자가 필수로 받는 패키지(`ui`·`tokens`)를 키우지 않는다. 일부 소비자만 쓰는 묶음은 **선택형 산출물 패키지**로 낸다(`@kor-travel/toast` 선례: `artifactPackages`에는 있고 프로필 필수 목록에는 없다). 검사기가 선언하지 않은 산출물을 건너뛰므로 쓰지 않는 소비자는 비용이 0이다.
3. B를 더 쓰기 전에 B 자체를 고친다(§4.1). 고치기 전에는 프론트 공유를 늘리지 않는다.
4. D(복사)는 소비자 2곳·작은 파일에만 쓰고 강제 검사를 붙이지 않는다(R2).
5. 계약을 건드리는 통합(오류 형식·헤더·지표·env)은 하지 않는다. 필요하면 E(규약)로 새 서비스에만 적용한다.

## 3. 인벤토리

### 3.1 요약 표

칸의 뜻: `●` 구현 있음, `◐` 일부·변형, `○` 공통 구현을 이미 씀, `×` 없음. 판정 뒤의 숫자는 §3.2 이하의 상세 절이다.

| ID | 후보 | P | M | W | T | D | 차이의 핵심 | 판정 |
|---|---|---|---|---|---|---|---|---|
| K-01 | 프론트 중앙 정책 guard(main 정본·단일 버전) | ○ | ○ | ○ | ○ | ○ | 수단 자체의 비용(§2.2). Node/npm 축 포함 | 지금 공유(수단 수정) §4.1 |
| K-02 | 패키지 내장 정책 사본 | ○ | ○ | ○ | ○ | ○ | 무관한 패키지의 버전을 끌어올림 | 지금 공유(수단 수정) §4.1 |
| K-03 | task 원장과 실물의 불일치(UI·Python) | — | — | — | — | — | 원장이 실물보다 뒤에 있음 | 지금 공유(정합) §4.2 |
| K-04 | Python 패키지 버전·핀 표기 | ○ | ○ | ○ | ○ | ○ | 버전이 `0.1.0.dev0` 고정 | 지금 공유(규칙) §4.3 |
| K-10 | HTTP 생존 probe(exec 형식) | ● curl | ● 인라인 python | ○ | ○ | ◐ 서비스별 혼재 | shell 형식 2곳이 남음 | 지금 공유(채택 공백) §3.3 |
| K-11 | FastAPI app factory·lifespan | ● | ● | ● | ● | ● | 문서 gating·미들웨어 순서·fail-closed가 모두 다름 | 공유하지 않음 |
| K-12 | settings 베이스(C1) | ● | ● | ● | ● | × `os.environ` | 빈 env 처리 네 방식, profile 기본값 반대 | 공유하지 않음 |
| K-13 | DB 엔진·세션 팩토리(C9) | ● asyncpg | ● asyncpg | ● psycopg sync | ● asyncpg/aiosqlite | ● SQLite | 드라이버 셋, timeout 값이 사고별 조정 | 공유하지 않음 |
| K-14 | Alembic env·런타임 롤(C10) | ● | ● | ● | ● | × | 같은 위험을 반대 방식으로 처리 | 공유하지 않음 |
| K-15 | health 라우터(C4) | ● | ● | ● | ● | ● | 본문이 각 OpenAPI 계약 | 공유하지 않음 |
| K-16 | OpenAPI export·drift(C12) | × | ● | ◐ | ● | × | 직렬화·비교 규칙이 셋 다 다름 | 나중에 공유(작게) |
| K-17 | 인증 프리미티브(C7·C8) | ◐ | ● | ◐ | ◐ | ● | 키 함수는 M=D 동일, 나머지는 정책 | 나중에 공유 |
| K-18 | outbound HTTP 재시도·circuit·상한(C15) | ● | ● | ● | ◐ | ◐ | 호출 자리마다 다른 정책 | 공유하지 않음 |
| K-19 | 오류 envelope(C5) | ● | ● | ● | ● | ● | 다섯 형식 | 공유하지 않음 |
| K-20 | cursor 서명 코덱·페이지 meta(C6) | ◐ 무서명 | ● | ● | ● | × | 코덱만 같은 알고리즘, meta·이름은 다름 | 나중에 공유(코덱만) |
| K-21 | rate limit | ● | × | ◐ | ◐ | ◐ | 일반 limiter는 P 하나 | 공유하지 않음 |
| K-22 | Valkey·cache | × | ● | × | × | × | 구현 하나 | 공유하지 않음(지금) |
| K-23 | request-id 미들웨어(C2 일부) | ● | ● | ● | × | ● 불신 | 신뢰 정책이 다름 | 나중에 공유 |
| K-24 | 지표·로깅·redaction(C3·C2) | ● | ● | ● | ◐ | ● | 이름·라벨이 대시보드 계약 | 공유하지 않음 |
| K-25 | 보안 헤더·CORS(C16·C17) | ● | ◐ CORS만 | ◐ | ● | ◐ CORS만 | 헤더 값·신뢰 정책이 제품별 | 공유하지 않음 |
| K-30 | geo REST client | ● | ● | ○ common | ○ common | × | 인증 위치·재시도·오류 계약이 다름 | 공유하지 않음 |
| K-31 | 역지오코딩 갱신 glue | × | × | ● | ● | × | 설정 모양만 다름 | 나중에 공유(작게) |
| K-32 | KASI·data.go.kr 호출·분류·재시도 | ● | ● | ● | ● | × | wrapper 금지, 분류는 provider 쪽 문제 | 공유하지 않음 |
| K-33 | 시도·행정코드 표 | ● | ● | ● | ● | × | 정본 방향이 다르고 2026 통합시 처리가 네 가지 | 나중에 공유(결정 선행) |
| K-34 | 좌표·bbox·haversine·한국 경계 | ● | ● | ● | ● | × | 상수가 정당하게 다름 | 공유하지 않음 |
| K-35 | 시간(KST) 헬퍼(C13) | ● | ● | ● | ● | ● naive | 저장소 안 중복이 더 큼 | 나중에 공유(낮음) |
| K-40 | 수집 결과 run tag | × | × | ● | ● | × | 함수 동일. tag는 각 저장소의 자기 관리자 UI만 읽음 | 나중에 공유(T-216과 함께) §3.4 |
| K-41 | 다중 job 인프라 재시도 sensor | ◐ job당 1개 | × | ◐ env로 꺼 둠 | ◐ job당 1개 | — | 공통 구현 미채택. P는 API 쪽 정적 목록이 묶임 | 나중에 공유 §3.4 |
| K-42 | 회수 sensor의 소비자 cursor·정체 시계 | × | ◐ 자체 | ◐ | ◐ | — | 공통 API 공백을 각자 우회 | 나중에 공유 §3.4 |
| K-43 | Dagster webserver 정의 로드 probe | ● | ● | ◐ | ● | ● ×4 | 같은 한 줄 7곳 | 나중에 공유 §3.4 |
| K-44 | code-server probe 세 세대 | ◐ Manager compose | ◐ standalone은 2세대 | ○ | ● 사본 | ● | 재시작 책임이 미정 | 나중에 공유(결정 선행) |
| K-45 | Map coalescing schedule | ○ | ● 자체 | ○ | ○ | — | 범위 판정 방식이 다름 | 나중에 공유 |
| K-46 | 공용 `dagster.yaml`의 job별 한도·`run_retries` | — | — | — | — | ● | 가이드가 요구한 규칙이 없음 | 나중에 공유(Manager 결정) |
| K-47 | Definitions 골격·schedule on/off·실패 sensor | ● | ● | ● | ● | — | 도메인 결선 | 공유하지 않음 |
| K-48 | 적재·수집 run 원장 | × | ● | ● | ● | — | 스키마가 도메인 | 공유하지 않음 |
| K-49 | standalone `dagster.yaml` 사본 | ● | ● | ● | ● | ● | 로컬 스택에 필요 | 공유하지 않음 |
| K-50 | 관리자 공통 부품 묶음 | ◐ 재도색 | ● | ● 동일 | ● 동일 | ◐ | 45개 파일 byte 동일 ×3 | 나중에 공유(선택형 패키지) §3.5 |
| K-51 | 로컬 경로 정규화(`sanitizeLocalPath`) | × | × | ● | ● | × | 구현 세 벌. 입력 타입·trim·길이 상한이 다름(검증 차이는 조사 뒤 맞춤) | 지금 공유(채택 공백) §3.5 |
| K-52 | 관리자 셸 조각(skip link·header·접힘) | ● | ● | ● | ● | ● | nav·로그아웃은 앱 소유 | 나중에 공유(K-50과 함께) |
| K-53 | Next 계층 세션·로그인 crypto | × | ● | ● | ● | × | 사본이 아니라 재구현, 폐기 저장소가 다름 | 공유하지 않음 |
| K-54 | API client·오류 파싱·타입 생성 | ● | ● | ● | ● | ● | 오류 형식 넷·인증 셋 | 공유하지 않음 |
| K-55 | 폼 검증·hook·KST 포맷 | ● | ● | ◐ | ◐ | ◐ | 이름만 같은 다른 모델 | 공유하지 않음 |
| K-56 | 토큰 `--kt-*` 브리지·alias 블록 | ◐ | ● | ● | ● | × | D·TP는 브리지 없음 | 나중에 공유(기존 task) |
| K-57 | Dagster 운영 콘솔(상세·액션) | × | × | ● | ● 동일 | × | W=T byte 동일 | 나중에 공유(T-216) |
| K-58 | `map-marker-react` | × | ● 원본 | × | ● 사본 | × | 주석 한 줄 표류 | 나중에 공유 |
| K-59 | maplibre worker 복사·VWorld 키 판정 | ● | ● | ● | ● | × | 같은 스크립트 4벌 | 나중에 공유(상류) |
| K-60 | 지도 작업면 채택(Map `/features`) | — | ◐ | ○ | ○ | — | Map의 보류 항목 | 공유하지 않음(기존 보류 유지) |
| K-61 | 마커 팔레트·클러스터·bbox | ● | ● | ● | ● | × | 같은 코드에 다른 색, 데이터 모양이 다름 | 공유하지 않음 |
| K-62 | e2e 하네스 | ● | ● | ● | ● | ● | 저장소별 운영 gate | 공유하지 않음 |
| K-63 | vitest 설정·test-utils | ● | ● | ● | ● | ● | 중복은 import 한 줄 | 공유하지 않음 |
| K-64 | ESLint preset·doctor 플래그 | ● | ● | ● | ● | ● | 다섯 plugin 묶음, 심각도가 의도적 | 나중에 공유 |
| K-65 | tsconfig·postcss·npmrc | ● | ● | ● | ● | ● | 2~8줄, 배치 종속 | 공유하지 않음 |
| K-66 | `@kor-travel/ui` 순수 재수출 shim | × | ● 13개 | ● 동일 | ● 동일 | × | 릴리스 없이 지울 수 있음 | 지금 공유(채택 공백) §3.5 |
| K-70 | Node CI job 골격 | ◐ | ◐ | ● | ● ×2 | ● | W·T·D만 같은 모양 | 나중에 공유 |
| K-71 | Python 품질 설정·CI job | ● | ● | ● | ◐ | ● | 설치 방식 넷, format·mypy 실행 여부가 다름 | 공유하지 않음 |
| K-72 | Dockerfile 템플릿 | ● | ● | ● | ● | ● | 핀·사용자·잠금 방식이 다름 | 공유하지 않음 |
| K-73 | `build-images.py` 생산자 | × | × | ● | ● 원형 | × | fork 한 쌍 | 나중에 공유(유지 팀 판단) |
| K-74 | `.dockerignore` matcher | × | × | ● | ● | ● | 세 구현, 지원 문법이 다름 | 나중에 공유(K-73과 함께) |
| K-75 | 비내구 테스트 PostgreSQL helper | ● | ● | × | × | × | 2곳, PG 주 버전 분기만 다름 | 나중에 공유 |
| K-76 | 배포·호스트 스크립트·백업 | ● | ● | ● | ● | ● | 호스트·gate별 | 공유하지 않음 |
| K-77 | 문서·원장 lint·redaction·secret scan | × | ● | × | × | × | 형식이 다르고 도입 즉시 실패 | 공유하지 않음(지금) |
| K-78 | Map의 guard 검사 코드 지연 | — | ◐ | — | — | — | 정확 Node/npm 규칙 미이관 | 나중에 공유(결정 선행) |
| K-79 | Manager의 `build_bytecode` 사본 | — | — | — | — | ● | 의도된 무의존 사본 | 공유하지 않음 |

집계: 지금 공유 7, 나중에 공유 26, 공유하지 않음 30(합 63).

### 3.2 백엔드

**K-11 app factory·lifespan — 공유하지 않음.** `P:apps/api/app/main.py:50-127`, `M:api/app.py:769-1463`, `W:wapi/app.py:130-347`, `T:app/main.py:516-3732`, `D:kdm/main.py:174-244`. 코드 수준에서 같은 것이 없다. 문서 노출은 셋으로 갈리고(P·W·D는 기본값대로 항상, M은 production에서 `/docs`·`/redoc`을 끔 `api/app.py:827-828` ✔, T는 `openapi_url`까지 설정으로 끔 `app/main.py:630-632`), 미들웨어 순서와 시작 시 fail-closed 검사도 저장소마다 다르다. 공통 factory는 일부러 다르게 둔 다섯 계약 위에 결박층을 하나 더 얹는다(R2).

**K-12 settings 베이스 — 공유하지 않음.** `P:apps/api/app/core/config.py:644-651`, `M:lib/settings.py:42-72`·`M:api/settings.py:380-395`, `W:wlib/settings.py:77,168-179`, `T:app/core/config.py:11-24`, D는 settings 클래스가 없다(`os.environ` 자리 66곳). compose의 `${X:-}`가 만드는 빈 문자열을 넷이 다르게 다룬다: M core는 `env_ignore_empty=True`(`lib/settings.py:71`), M api는 필드별 validator(`api/settings.py:767-800`), P는 토큰 필드 10개 validator(`config.py:1436-1463`)이고 공백은 남겨 뒤에서 거절, W는 13개 필드에서 공백까지 미설정으로 본다(`wlib/settings.py:664-684`), T는 없다. profile 기본값도 반대다(W `production` `wlib/settings.py:183`, M code 기본 `local-dev` `api/settings.py:412-414`). 공통 베이스는 P·W·T의 빈 env 의미를 조용히 바꾼다. 나중에 쓸 만한 것은 `mode="before"` validator로 쓰는 순수 함수 둘뿐이다(저장소당 10~25줄).

**K-13 DB 엔진 팩토리 — 공유하지 않음.** `P:apps/api/app/db/session.py:23-44`, `M:lib/infra/db.py:829-954`, `W:wlib/repository.py:1392-1416`(sync psycopg), `T:app/db/session.py:28-92`, `D:kdm/database.py:15-114`(SQLite). 드라이버가 셋이고 호출 모양이 다르다. `statement_timeout`·`lock_timeout`은 엔진마다 값과 단위가 다르고 각각 사고 기록에 묶여 있다. 저장소 **안**의 중복은 따로 정리할 만하다: Map Dagster의 같은 `server_settings` 리터럴 6곳(`M:dag/file_registry_hooks.py:93,140`, `file_registry_scan.py:109`, `manual_provider_dedup.py:77`, `resources.py:1317`, `runtime_preflight.py:23` ✔), transport의 DSN 정규화 2곳(`T:app/db/session.py:43-46`, `T:backend/alembic/env.py:29-32`).

**K-14 Alembic env·런타임 롤 — 공유하지 않음.** `P:apps/api/alembic/env.py`(89줄), `M:alembic/env.py`(261줄), `W:alembic/env.py`(47줄), `T:backend/alembic/env.py`(73줄), D는 없다. P와 M은 같은 위험을 반대로 다룬다: P는 `configure` 전에 SQL을 실행하고 명시 commit으로 보정한다(`env.py:52-54,75-78`). M은 `configure` 전 `execute()`가 commit을 건너뛰게 한다고 적고 `SET ROLE`·`search_path`를 `begin_transaction()` 안에 둔다(`env.py:187-222`). 템플릿은 둘 중 하나를 골라야 한다. 롤 이름·스키마 이름·제외 목록·lock 키는 DB별 계약이다. 남길 것은 규약 한 줄("`configure()` 전에 `execute()`하지 않는다. 한다면 명시 commit")이다.

**K-15 health 라우터 — 공유하지 않음.** `P:apps/api/app/api/v1/healthz.py:31-53`, `M:api/routers/public_status.py:60-90`·`M:api/routers/ops.py:334-360`, `W:wapi/app.py:198-208`, `T:app/main.py:854-862`, `D:kdm/main.py:398-400`. 같은 것은 경로 `/health`뿐이다. 본문이 다르고(`status`는 넷이 `ok`, D는 `healthy`; 커밋 키는 `git_sha`·`commit`·`git_commit`·`release_sha`), T의 `/health`는 DB가 죽으면 실패하지만 M은 반대 선택을 문서로 남겼다(`public_status.py:4-6`). 본문은 각 OpenAPI 산출물의 일부여서 공통 라우터는 모든 소비자의 산출물을 바꾼다. 공유할 것은 **probe 쪽**이다(K-10).

**K-16 OpenAPI export — 나중에 공유(작게).** `M:packages/kor-travel-map-api/scripts/export_openapi.py`(527줄), `W:packages/kor-travel-weather-api/scripts/export_openapi.py`(27줄), `T:scripts/export_openapi.py`(60줄) ✔. P·D는 없다. 같은 것은 `json.dumps(app.openapi(), indent=2, ensure_ascii=False)` 한 줄이다. M·T는 `sort_keys=True`(`export_openapi.py:438`, `:42` ✔), W는 없다(`:21` ✔). M은 끝 개행 없이 `.strip()` 비교, T는 개행을 쓰고 정확 비교, W는 스크립트 안 비교가 없고 CI가 `git diff`로 본다. 공유할 수 있는 부분은 25줄 정도의 `dump`·`check_or_write`인데, 직렬화를 맞추면 커밋된 산출물이 한 번 다시 써지고 그 사본을 가진 쪽이 따라 움직인다. 줄 수 이득보다 비용이 크다. 값싼 독립 개선은 W에 `sort_keys=True`를 넣는 것이다. 그 '값싼 개선'에도 비용이 있다. PinVi 백엔드가 weather OpenAPI 스냅샷을 SHA-256으로 고정해 두었으므로(`P:apps/api/tests/unit/test_kor_travel_weather_contract.py:40-42` ✔) weather 산출물을 다시 직렬화하면 PinVi가 스냅샷을 다시 받아야 한다. 이것은 이 문서가 제안한 것이 아니라 이미 있는 고정이다.

**K-17 인증 프리미티브 — 나중에 공유.** 공개 API 키 생성·해시 함수는 `M:lib/infra/public_api_keys.py:86-96`과 `D:kdm/services/public_api_key_service.py:20-27`이 본문까지 같다 ✔(길이 32, `ascii_letters+digits`). 그 밖은 정책이다: 키 전달(M은 헤더만, D는 query), 조회(M은 TTL 캐시, D는 요청마다 조회), 실패 코드(M 401/403/422, W 401, T·P 일부 404로 표면 은닉), 미설정 시 동작(M 미강제, W production에서 예외, T는 32자 미만이면 닫힘 `app/main.py:708`), proxy 신뢰(넷 다 다르고 IPv4-mapped 정규화는 T만 `app/service_exports.py:298-299`). 작은 `secrets` 모듈(바이트 안전 상수시간 비교, 키 생성·해시, CIDR 판정)은 저장소당 10~25줄을 지운다. D의 백엔드는 common에 의존하지 않고(Poetry) 이 이득으로 의존을 새로 만들 이유가 없다. 원장에서 C7(키 생성·해시)은 [T-306](../tasks/T-306-settings-db-api-key.md), C8(CIDR·proxy 신뢰)은 [T-308](../tasks/T-308-api-third-tier-modules.md)이 갖고 있다. [T-312](../tasks/T-312-auth-core-primitives.md)는 비밀번호·세션·JWT·RBAC다. T-306에는 이 문서가 공유하지 않음으로 둔 C1·C9가 함께 묶여 있으므로, T-022가 T-306을 나눠 C7을 남겨야 한다. 새 task는 만들지 않는다.

**K-18 outbound HTTP — 공유하지 않음.** 재시도 루프는 다섯 저장소 모두 손으로 쓴 것이고 서로 다르다. P는 client마다 `0.2·2^n`과 3회 실패·120초 circuit(`P:apps/api/app/clients/_resilience.py:18-61`), M은 실행 단위 예산(`M:dag/upstream_retry.py:102-117`)과 geo에 502/503/504만 선형 backoff(`M:lib/geocoding.py:1579-1611`), W는 thread를 재우는 sync(`W:wlib/providers/base.py:346-451`), T는 provider 라이브러리에 맡긴다. 재시도·circuit은 호출 자리의 결정이다. 공통 `bounded_request`를 쓰는 곳은 둘뿐이다(`M:api/dagster_graphql.py:915`, `P:apps/api/app/services/admin_etl.py:670` ✔). M의 `_read_capped`(`M:api/transport_state_service.py:231-255` ✔)는 gzip을 허용하고 공통은 모든 압축을 거절한다(`C:cpy/http.py:66-68` ✔). 소비자가 한 곳이라 공통 옵션으로 올리지 않는다(R8). P의 `tenacity` 선언은 import가 없다(`P:apps/api/pyproject.toml:23` ✔).

**K-19 오류 envelope — 공유하지 않음.** P `{"error":{code,message,details}}`(`P:apps/api/app/core/errors.py:25-76`), M problem+json에 `code`·`request_id`·`errors[]`(`M:api/app.py:619-691`), W problem+json(`type="about:blank"`, `W:wapi/app.py:110-127`), T problem+json에 `instance`만(`T:app/main.py:636-689`), D `{detail}`(`D:kdm/main.py:341-395`). 같은 상태의 기본 코드도 다르다(401: P `TOKEN_INVALID`, M `UNAUTHORIZED`). 프론트와 형제 client가 이 형식을 읽는다. 통합은 세 저장소 이상의 파괴적 변경이다.

**K-20 cursor 코덱 — 나중에 공유(코덱만).** `M:api/routers/curation_snapshots.py:216-231`과 `W:wlib/export_snapshots.py:263-300`은 같은 알고리즘이다(정렬·압축 JSON 뒤에 HMAC-SHA256 32바이트, base64url, padding 제거 ✔). T는 다른 배치 둘(`T:app/services/export_price_history.py:44-62`, `T:app/main.py:2504-2545`), P는 서명이 없다. 키 출처(M 전용 secret, W 관리자 토큰 파생, T `database_url` 파생), 이름(`page_size` 대 `limit`), meta(`next_cursor` 대 `cursor`+`has_more`)는 계약이라 합치지 않는다. 발급된 cursor는 배포를 넘어 살아야 하므로 코덱을 바꾸면 기존 cursor가 죽는다. 새 cursor에만 쓸 fastapi 무의존 `sign`·`verify`는 자리당 15~20줄이다. 기존 [T-508](../tasks/T-508-deferred-items-reevaluation.md)의 재평가 항목으로 남긴다.

**K-21 rate limit — 공유하지 않음.** 일반 limiter는 P 하나다(`P:apps/api/app/middleware/rate_limit.py`, 757줄, memory·Postgres backend). W·D는 로그인 한정, T는 상류 보호다. Valkey 기반은 어디에도 없다. 지워질 줄이 다른 저장소에 없다.

**K-22 Valkey·cache — 공유하지 않음(지금).** client는 `M:lib/infra/valkey_state.py`(1,244줄) 하나다. generation 교체 저장소이지 범용 cache가 아니다. P는 Valkey 상태를 Map의 HTTP로 읽는다. 두 번째 서비스가 Valkey 의존을 가질 때 `make_valkey_client`와 오류 매핑(약 45줄, `valkey_state.py:492-537`)을 다시 본다.

**K-23 request-id 미들웨어 — 나중에 공유.** P·M·W는 들어온 `X-Request-Id`를 길이·문자 검사 없이 신뢰한다(`P:apps/api/app/middleware/request_id.py:14-34`, `M:api/response.py:116-137`, `W:wapi/app.py:64-107`). D는 일부러 신뢰하지 않는다(`D:kdm/main.py:263-272`). T는 없다. `trust_incoming` 옵션과 길이·문자 제한을 가진 pure-ASGI 미들웨어는 M·W·P에서 20~35줄씩 지우고 T에 하나를 준다. starlette extra 뒤에 둬야 Map 라이브러리가 깨끗하다(R6). 기존 [T-307](../tasks/T-307-request-id-and-metrics.md)에서 **지표와 분리해** 진행하도록 T-022에서 정리한다.

**K-24 지표·로깅·redaction — 공유하지 않음.** 접두 `pinvi_api_`·`kor_travel_map_`·`ktw_`·`ktdm_`, 라벨 `route` 대 `path`, `status_code` 대 `status_class`, registry 방식이 다 다르고 대시보드와 경보가 그 이름에 묶여 있다. redaction은 전략이 넷이다(P 이름 정규식 `***`, W 키 이름 `[REDACTED]`, T·D 값 치환 `<redacted>`). 각자 자기 누출 표면과 문서화된 잔여 위험을 갖는다. 이름 목록을 합치면 각 저장소가 놓치는 것이 바뀐다.

**K-25 보안 헤더·CORS — 공유하지 않음.** 보안 헤더 미들웨어는 P(`P:apps/api/app/middleware/security_headers.py`)와 T(`T:app/main.py:731-741` ✔)에 있고 W는 응답별 `nosniff`만, M·D는 Python에서 넣지 않는다. 헤더 값(Permissions-Policy, CSP)과 HSTS 발급 조건이 제품마다 다르다. CORS는 M의 표면별 미들웨어를 빼면 모두 Starlette `CORSMiddleware`를 쓴다. 이미 공통인 것을 다시 감쌀 이유가 없다. ADR-011 3차·BE-17·T-308과 어긋나는 판정이다(§1.5). 공통화와 별개로, T의 HSTS 발급 조건은 P가 #344에서 일부러 피한 방식과 같다. transport 유지 팀에 알릴 결함 후보다.

### 3.3 probe와 도메인 헬퍼

**K-10 HTTP 생존 probe — 지금 공유(채택 공백).** 공통 `python -I -m kortravelcommon.http_health`(loopback, 헤더만, 전체 4초, shell 없음)를 이미 쓰는 곳: `W:compose.yaml:158`, `T:docker-compose.yml:100`, `T:docker-compose.shared.yml:274`, `D:docker-compose.yml:2998-3008`(weather-api) ✔. 아직 shell 형식인 곳: Map API의 인라인 `python -c urllib`(`M:docker-compose.yml:513-518` ✔, 같은 문장이 `D:docker-compose.yml:1738-1741` ✔), PinVi API의 `curl`(`D:docker-compose.yml:2204-2207` ✔). 두 API 이미지는 이미 `kor-travel-common[http]`를 설치하고 두 핀 모두 `http_health.py`를 갖는다(`git ls-tree` ✔). 남은 두 곳은 shell을 거치는 형식이고, 공통 probe는 exec 형식으로 큰 client·프레임워크 import 없이 한 예산 안에서 끝난다([http-health-probe](../runbooks/http-health-probe.md)). PinVi Dockerfile의 probe는 세 엔드포인트를 묶은 것이라(`P:apps/api/Dockerfile:99-102` ✔) 한 경로만 보는 공통 probe로 바꾸지 않는다. 이득: shell 형식 2종과 `curl` 의존 제거. 비용: compose 몇 줄. 위험: 이미지에 모듈이 없으면 재구축이 `compose up`에서만 죽는다. 그래서 채택 전에 고정 이미지에서 모듈 존재를 확인한다(§4.4).

**K-30 geo REST client — 공유하지 않음.** `P:apps/api/app/clients/kor_travel_geo.py:51-273`과 `M:lib/geocoding.py:1454-1745`. 인증 위치(P query `?key=`, M 헤더 `X-KTG-API-Key`), 요청 어휘, timeout(5초 대 read 10·connect 4초), 재시도(P는 모든 timeout과 5xx, M은 502/503/504만이고 connect 실패는 절대 재시도하지 않음), 실패 계약이 다르다. P는 사용자 요청이라 circuit 뒤에서 빨리 실패하고, M은 배치라 호출 수를 센다. 하나로 합친 client는 Map이 금지한 wrapper이고(R6) 두 서비스를 한 계약 해석에 묶는다(R1). W·T는 Python에서 geo를 부르지 않고 공통 역지오코딩을 쓴다.

**K-31 역지오코딩 갱신 glue — 나중에 공유(작게).** `W:wlib/address_refresh.py:1-62`와 `T:app/services/address_refresh.py:1-79`. `configured()`는 동일하고 호출 모양도 같다. 다른 것은 설정 모양(W는 `SecretStr`과 repository, T는 `str`과 5개 테이블 union·좌표 필터·FerryPort 제외)이다. `(select, settings)`를 받는 공통 factory는 W 30줄·T 25줄을 지운다. 두 저장소 모두 다른 팀 소유라 그 팀이 정한다(R7).

**K-32 KASI·data.go.kr — 공유하지 않음.** 호출은 넷 다 provider 라이브러리의 공개 client를 직접 쓴다(R6). 한도 분류는 저장소마다 다르고(M은 `failure_kind` 속성과 429 제외 `M:dag/quota_exhaustion.py:95-209`, W는 `failure_kind=="quota"`만 일일 한도 `W:wdag/definitions.py:630-638`, T는 문자열 표식 `T:app/services/collection.py:40,356-371`), 원인은 provider 라이브러리 절반에 `failure_kind`가 없다는 것이다. 고칠 자리는 상류다. 같은 라이브러리의 핀이 저장소마다 다른 것은 별도 사실이다(kasi: P `bc8fd49`·T `4259e57`; khoa: M `38a2b74`·W `9c952bb`; krforest: M `70814c9`·W `270ef7a`; krex: W `0fc9da9`·T `af045fa`; datagokr: M `6150932`·T `18864a3` ✔). 정렬 주체는 열린 결정 O-16이며 [T-505](../tasks/T-505-shared-library-marker-palette-request.md)·[T-506](../tasks/T-506-quarterly-drift-audit.md)이 소유한다.

**K-33 시도·행정코드 표 — 나중에 공유(결정 선행).** `P:apps/api/app/services/korea_regions.py:20-140`, `M:lib/core/curation_address.py:27-81`·`M:lib/core/search_region.py:63-139`, `W:wlib/alert_area_mapping.py:15-55`, `T:app/services/place_locations.py:28-40`. 방향이 다르다(P는 코드→약칭, M 큐레이션은 별칭→현재 정식명, M 검색은 DB 표본에서 유도, T는 접두 일치). 2026 `전남광주통합특별시`를 네 가지로 다룬다: M 큐레이션은 `전라남도`(`curation_address.py:67`), M 검색은 `전남`·`광주` 둘 다(`search_region.py:80`), T는 `전남`(`place_locations.py:31`), P·W TS는 항목이 없다. 17개 시도의 데이터 전용 표(현재 코드·옛 코드·정식명·약칭·별칭)는 P 40줄·M 50줄·T 13줄을 대신할 수 있지만 정본 방향과 통합시 처리가 먼저 정해져야 한다. Map 라이브러리는 common에 의존하지 않으므로(`git grep kortravelcommon -- src` 빈 결과 ✔) 새 의존에는 Map ADR이 필요하다. W의 특보 구역 매핑과 M의 검색 토큰은 이 표와 별개로 남는다.

**K-34 좌표·bbox·haversine·한국 경계 — 공유하지 않음.** 지구 반지름이 넷이다(6,371,000 / 6,371,008.8 / 6,371.0km / 6,372,797.560856). `M:api/routers/service_transport.py:91-92`는 Valkey GEO와 맞춰야 하고 `T:app/services/fuel_search.py:18`은 응답 필드로 공개돼 있다(`T:app/schemas.py:94`). 위도 경계도 질문이 다르다(입력 검증 33–43, 서비스 영역 33–39.5, provider 구제, transport 적재 32–39.5). 2026-09 판정("좌표 경계 상수 공통화 금지")을 값으로 다시 확인했다. 지울 수 있는 줄은 저장소 **안**에 있다(P haversine 5벌 약 25줄, M 약 15줄).

**K-35 시간 헬퍼 — 나중에 공유(낮음).** `P:apps/api/app/core/time.py:11-19` ✔, `M:lib/dto/_time.py:36-92` ✔, `W:wlib/models.py:20,324-325` ✔(고정 오프셋), `T:app/core/time_utils.py:7-85` ✔, `D:kdm/_time.py:4-11` ✔(naive UTC). `kst_now()`는 뜻이 같지만 W의 tzinfo 타입이 다르고, naive 값은 셋으로 갈린다(거절, KST 가정, UTC 가정). 공유 대상은 15줄이고 저장소당 10줄을 지운다. Map 라이브러리가 그 때문에 새 의존을 가져야 한다. 더 큰 이득은 저장소 안 정리다(M 고정 오프셋 KST 6곳, P 흩어진 상수 5곳, W 정의 2곳). [T-304](../tasks/T-304-health-and-time.md)의 time 절반으로 남기되 우선순위를 낮출 것을 제안한다.

### 3.4 Dagster

**K-40 수집 결과 run tag — 나중에 공유(T-216과 함께).** `_record_collection_outcome`은 `W:wdag/definitions.py:399-418`과 `T:app/dagster/definitions.py:60-79`에서 본문이 같다(`suppress` 대 `contextlib.suppress` 한 줄 차이 ✔). tag `kortravel/collection-outcome`은 두 관리자 프론트가 읽는다(`W:WA/lib/dagster.ts:222`, `W:WA/components/dagster-console.tsx:86`, `T:TA/components/dagster-console.tsx:86` ✔). 다만 각 관리자 UI는 자기 저장소의 run만 읽는다. 저장소 사이 계약이 아니고 이득은 저장소당 20줄이다. tag를 읽는 TypeScript 쪽(W=T 동일 콘솔, K-57)이 T-216으로 공통에 들어갈 때 Python 쪽 정의도 함께 옮기는 것이 맞다. 이득: 정의 한 곳, 각 20줄 제거. 비용: common 함수 하나와 핀 PR 둘. 위험: 낮다(동작 보존, A 수단). 채택은 두 저장소의 유지 팀이 한다(R7).

**K-41 다중 job 인프라 재시도 sensor — 나중에 공유.** 공통에 `infrastructure_retry_sensor_for_jobs`가 있다(`C:cpy/dagster.py:331` ✔). W는 env `KOR_TRAVEL_WEATHER_INFRA_RETRY_ENABLED`가 `true`일 때만 등록하고 기본값은 `false`다(`W:wdag/recovery.py:19-30` ✔). 추적된 compose 어디에도 그 env가 없다. P·T의 채택이 이 구현의 첫 운영 사용이 될 수 있다. P는 job마다 sensor를 5개(`P:etl/definitions.py:88-97` ✔), T는 3개 만든다(`T:app/dagster/definitions.py:1041-1048` ✔). 하나로 합치면 실패 조회가 한 번이 되고 sensor tick 수가 준다. 비용: 저장소당 6줄 안팎. 위험: sensor 이름이 바뀌어 기존 sensor의 cursor·상태가 새로 시작한다. 채택 PR이 이 전환을 다뤄야 한다. 또 합친 sensor는 한 tick에 RunRequest를 하나만 낸다(`C:cpy/dagster.py:658-661` ✔). 여러 job이 같은 때 실패하면 재시도가 60초 간격으로 하나씩 나간다. P는 묶인 것이 더 있다. API가 sensor 이름 다섯 개를 정적 목록으로 갖고 있고(`P:apps/api/app/services/admin_etl.py:257-282` ✔, sensor마다 `job_name` 하나) ETL 시험이 그 목록과 Definitions의 일치를 강제한다(`P:apps/etl/tests/test_admin_etl_definition_lists.py`). sensor를 합치면 관리자 API 모델과 화면, 두 배포물의 배포 순서가 함께 바뀐다. 이득(tick 수)에 비해 비용이 커서 '지금'에서 내렸다. weather가 운영에서 먼저 켜 본 뒤에 다시 본다.

**K-42 회수 sensor의 소비자 cursor — 나중에 공유.** 공통 `reconciliation_sensor`가 sensor cursor를 소유해서, W와 T는 keyset 위치를 프로세스 메모리에 둔다(`W:wdag/sync_recovery.py:97-116` ✔, `T:app/dagster/recovery.py:206-223` ✔). W는 공통의 비공개 cursor 접두 `stall:`을 직접 다시 읽는다(`W:wdag/sync_recovery.py:64-65,119-127` ✔, 원본 `C:cpy/dagster.py:69` ✔). 비공개 형식에 묶인 것이라 공통이 형식을 바꾸면 조용히 깨진다. callback이 현재 정체 시계를 받고 작은 하위 cursor를 저장할 수 있게 공통 API를 넓히면 W 30줄·T 20줄이 준다. Map의 회수 sensor(`M:dag/feature_operation_sensors.py`)는 30초 주기·`RunRequest` 반환·시계 둘이 필요해 factory에 맞지 않는다. 의도된 불일치이므로 옮기지 않는다. API를 넓힐 때 weather가 읽는 `stall:` 문자열 모양은 그대로 둬야 한다(T-314의 호환 수용 기준).

**K-43 webserver 정의 로드 probe — 나중에 공유.** `{repositoriesOrError{__typename}}`을 보내 `RepositoryConnection`인지 보는 한 줄이 7곳에 있다: `D:docker-compose.yml:2013,2432,2791,3259`, `M:docker-compose.yml:778`, `T:docker-compose.shared.yml:378`, `P:apps/etl/Dockerfile:98-102`(curl+grep) ✔. 공통에는 webserver probe가 없다. 운영은 Manager의 공용 webserver가 workspace를 읽는 별도 probe를 쓰므로(`D:docker-compose.yml:990-1010`) 이 사본들은 standalone·legacy 스택의 것이다. 그래서 이득이 작다. 공통 CLI 하나(`dagster_webserver_health`)는 만들 가치가 있으나 급하지 않다. 첫 채택자가 정해지지 않았으므로 task를 만들지 않는다(R8). standalone 스택을 고치는 저장소가 생기면 그때 공통 CLI와 채택을 한 묶음으로 연다.

**K-44 code-server probe 세 세대 — 나중에 공유(결정 선행).** (1) Manager의 93줄 인라인 probe(`D:docker-compose.yml:103-196`)가 `T:docker-compose.shared.yml:118-211`에 그대로 복사돼 있고 ✔ 전환 스크립트가 일치를 강제한다. 이 probe는 PID 1에 SIGTERM을 보내고 고아 run을 거둔다. Manager compose에서는 Map·PinVi·concierge의 code-server도 이 (1)을 쓴다(`D:docker-compose.yml:1929,2361,1443`). (2) `kortravelcommon.dagster_health`(`M:docker-compose.yml:675-681`, Map의 standalone compose만). (3) `kortravelcommon.grpc_health --check live`(`W:compose.yaml:301`, `D:docker-compose.yml:2707,3155`). geo·weather 쪽 주석은 "PID 종료·DB reaper는 healthcheck 책임이 아니다"라고 적는다. (3)으로 모으면 T의 94줄과 D의 약 150줄이 준다. 그러나 멈춘 자식을 누가 다시 띄우는가가 먼저 정해져야 한다. 읽기 전용 대체물 `C:cpy/dagster_recovery.py`를 결선한 곳은 W뿐이다. Manager와 유지 팀의 결정이다.

**K-45 Map coalescing — 나중에 공유.** `M:dag/schedules.py:583-613` ✔은 공통 `coalescing_schedule`(`C:cpy/dagster.py:177` ✔)과 세 가지가 다르다: `NOT_STARTED`·`MANAGED`도 센다(`schedules.py:70-77` ✔), DB에서 `kor_travel_map.operation_key` tag로 좁힌다, `execution_fn`으로 `RunRequest`/`SkipReason`을 돌려준다. 공통이 tag 범위를 받거나 Map이 origin 범위를 받아들여야 옮길 수 있다(약 40줄).

**K-46 공용 `dagster.yaml` — 나중에 공유(Manager 결정).** 공용 instance 설정에는 `run_retries` 블록이 없고 `kortravelcommon/job`의 값별 한도가 없다. 그 key는 concierge 값 다섯 개의 리터럴로만 있다(`D:config/dagster-shared/dagster.yaml:96-110` ✔). standalone 사본 셋(P·W·T)에는 값별 한도가 있다. 공통 가이드는 daemon 소유 저장소에 그 규칙을 두라고 한다([dagster-adoption](../runbooks/dagster-adoption.md) §3). 호스트 override 렌더러는 한도의 `value`가 문자열이어야 통과시키므로(`D:kdm/services/shared_dagster_instance.py:92-96` ✔) dict 값(`applyLimitPerUniqueValue`)을 지금은 거절한다. 일반 규칙 하나가 리터럴 다섯을 대신하고 R3에 맞는다. 그러나 **모든** tenant의 job이 동시 1개로 묶인다. Map은 queue sensor가 한 tick에 여러 run을 낸다. 그 run들이 같은 job tag를 갖는지 먼저 확인해야 한다. 운영 동작을 바꾸므로 Manager의 결정 task로 둔다.

**K-47·K-48·K-49 — 공유하지 않음.** Definitions 조립·resource 결선·schedule on/off(M은 코드 상수와 DB override `M:dag/schedules.py:661-667` ✔, W는 env로 sensor 등록, T는 `SCHEDULER_MODE`)는 도메인이다. 같은 것은 `multiprocess_executor.configured({"max_concurrent": 1})` 한 줄이다. run 원장(`ops.import_jobs`, `weather_sync_runs`, `collection_runs`)은 스키마가 도메인이고 서로의 테이블을 핀하면 안 된다(R1). standalone `dagster.yaml`은 로컬 스택에 있어야 한다.

### 3.5 프론트엔드

**K-50 관리자 공통 부품 묶음 — 나중에 공유(선택형 패키지).** MA·WA·TA 세 프론트에 **45개 파일(2,076줄)이 byte 단위로 같다** ✔(`cmp -s`로 다시 셈). `components/ui/*` 30개와 `confirm-dialog`·`copy-button`·`detail-list`·`empty-state`·`json-viewer`·`pagination-bar`·`stat-strip`·`status-badge`·`status-badge-variants`, `lib/{format,occurrence-key,string-list,utils}.ts`, `app/error.tsx`·`app/global-error.tsx`다. MA=WA만 같은 파일이 9개(1,317줄) 더 있다. 그중 다섯(`app-error-panel`·`filter-bar`·`section-card`·`lib/status-label.ts`·`lib/error-recovery.ts`)은 TA에 조금 다른 판이 있고(각 16·23·2·2·2줄 차이 ✔), 넷(`selectable-row`·`multi-filter-combobox`·`lib/admin-auth-events.ts`·`providers/query-client-provider.tsx`)은 TA에 없다 ✔. 표류가 이미 보인다: `help-tip.tsx`는 W·T가 M보다 새 판이다. PW 관리자는 같은 묶음을 일부러 다시 칠한 이식본이다(약 2,330줄). [ui-contract](../standards/ui-contract.md) §4는 이 부품들(`EmptyState`·`StatStrip`·`StatusBadge`·`DetailList`·`JsonViewer`·`CopyButton`·`AppErrorPanel`·`HelpTip`·`FormField*`·`AdminPageHeader`·`AdminSkipLink`)을 계약으로 적었지만 `packages/ui/src`에는 없다 ✔. 같은 문서는 엔진을 `@base-ui/react`라고 적는데(`ui-contract.md:19,32` ✔) 실물은 `radix-ui`다. 기존 task T-203·T-205·T-206(HelpTip)·T-208(Pager)·T-209·T-210이 이 범위와 겹친다. 그대로 옮길 수 없는 의존도 있다: `status-badge`·`status-badge-variants`·`stat-strip`은 앱 사전 `@/lib/status-label`을, `stat-strip`·`detail-list`는 `next/link`와 `help-tip`을, `copy-button`은 `sonner`를, `help-tip`은 `zustand`를 import한다 ✔. `@kor-travel/ui`에는 `next` peer가 없다. 그래서 사전·링크·토스트는 주입으로 바꿔야 한다. `confirm-dialog`는 ui-contract가 엔진 선택을 앱 소유로 두고 공통 API를 T-508로 미뤘으므로 묶음에서 뺀다. 45개 중 30개(846줄)는 `components/ui/*`이고 그 가운데 13개(68줄)는 `@kor-travel/ui/*`를 그대로 재수출하는 shim이다 ✔(K-66). 나머지 17개는 로컬 클래스를 덧붙인 얇은 wrapper·variants·폼이다. 묶음에 넣지 않고 앱에 남기는 동일 파일: `components/ui/sonner.tsx`(토스트 엔진은 앱 소유), `components/ui/button.tsx`(로컬 wrapper. 공통 `Button`에 spinner가 생기면 지운다), `lib/occurrence-key.ts`·`lib/string-list.ts`(도메인 보조), `lib/utils.ts`(`cn`은 `@kor-travel/ui/utils`로 바꾼다, K-66), `app/error.tsx`·`app/global-error.tsx`(Next 규약 파일. `AppErrorPanel`을 부른다). `empty-state`는 공통에 이미 `empty`가 있다(`C:packages/ui/src/empty.tsx` ✔). 둘 중 무엇을 남길지 T-219가 정한다. 이득: M·W·T에서 재수출 shim과 앱에 남는 파일을 빼고 각 800~1,000줄 안팎(어림), PW 관리자가 토큰 이름 매핑을 받아들이면 600~900줄. 비용: 클래스가 로컬 어휘(`text-text-secondary`, `rounded-control`)라 파일 이동이 아니라 이식이다. `ui`의 하위 경로로 넣으면 `ui` 버전이 올라 부품을 쓰지 않는 소비자(P·D·geo·concierge)까지 재vendor한다. 그래서 **선택형 산출물 패키지 `@kor-travel/admin-kit`**로 낸다(§4.8의 비교). 쓰는 소비자(M·W·T)만 벤더한다. `status-label.ts`는 도메인 사전이라 앱에 남는다.

**K-51 로컬 경로 정규화(`sanitizeLocalPath`) — 지금 공유(채택 공백).** `@kor-travel/ui/navigation`이 `sanitizeLocalPath`를 내보낸다(`C:packages/ui/src/navigation.ts:5-17` ✔). W와 T의 관리자 프론트는 같은 목적의 로컬 구현 `lib/navigation.ts`를 따로 둔다(`W:WA/lib/navigation.ts` ✔, `T:TA/lib/navigation.ts` ✔). W는 서버 쪽 호출부 셋이 로컬을, client 로그인 폼이 공통을 쓴다(`W:WA/components/login-form.tsx:5` ✔). T는 서버 쪽과 client 모두 로컬을 쓴다(`T:TA/components/login-form.tsx:7` ✔). 구현이 세 벌이고 모양이 다르다. 공통은 `string | null | undefined`를 받고 인코딩된 경계 문자와 제어 문자를 거절한다. 로컬 둘은 `unknown`을 받고 앞뒤 공백을 지우고 500자를 넘으면 거절한다(공통에는 길이 상한이 없다). 호출부는 `unknown`을 넘긴다(`W:WA/app/api/auth/login/route.ts:172,227` ✔, `T:TA/app/api/auth/login/route.ts:23` ✔). `fallback` 인자를 넘기는 호출부는 없다. 기준 커밋에서 W 로컬 구현에는 다른 두 구현에 있는 검증 하나가 빠져 있었고, 조사 뒤 kor-travel-weather #244(`8c3b4744`)가 그 검증을 더했다(운영 반영은 weather 배포 뒤). 남은 일은 중복 제거다. 로컬 구현을 통째로 지우면 타입 검사가 깨지고 trim·길이 상한이 사라지므로, 로컬에는 타입 좁히기·trim·길이 상한만 남기고 판정 본체는 공통 함수를 부르게 한다. 패키지 변경이 없어 함대 비용이 0이다. 동작은 달라진다. 공통 함수는 값 **어디에든**(query·hash 포함) `%20`·`%25`·공백·제어 문자가 있으면 거절한다(`C:packages/ui/src/navigation.ts:9` ✔). 지금 로컬 구현은 `/runs?q=a%20b`를 그대로 돌려주지만 바꾼 뒤에는 `/`가 된다. 이 변화가 받아들일 수 없으면 중복 제거를 하지 않는다(공통 규칙을 바꾸는 것은 `ui` 버전 변경이다).

**K-52 관리자 셸 조각 — 나중에 공유(K-50과 함께).** 다섯 관리자 표면 모두 nav를 공통 `AppMenu`로 그린다. 남은 로컬 셸(`M:MA/src/components/admin-shell.tsx` 556줄, `W:WA/components/admin-shell.tsx` 512줄, `T:TA/components/admin-shell.tsx` 254줄, `P:PW/app/(admin)/admin/layout.tsx`, `D:DM/src/components/layout/AppShell.tsx`)에서 같은 것은 skip link 문구와 접힘 저장 방식 정도다. nav 내용·권한·로그아웃 전송은 앱 소유다(`ui-contract.md:144`). skip link·header 띠·접힘 hook은 그것만으로 재vendor할 값이 안 된다. K-50의 패키지에 싣는다.

**K-53 Next 계층 세션·로그인 crypto — 공유하지 않음.** `M:MA/src/lib/auth.ts`(554줄)와 `W:WA/lib/session.ts`(549줄)는 payload 모양·8시간 TTL·PBKDF2 310,000회·10분 5회 제한이 같지만 글자로 같은 줄은 97줄뿐인 재구현이다. 폐기 저장소(M 프로세스 메모리, W 백엔드, T 없음), 신뢰할 수 없는 proxy 헤더일 때의 제한 키, `Origin` 누락 처리, `secure` 규칙이 다 다르다. T는 PBKDF2가 없다(`T:TA/lib/session.ts:26-28`). 2026-09의 "상수 일치" 관찰은 M·W·D에서만 맞다. Next 계층(TypeScript)의 공통 보안 모듈은 함대 전체의 결합이 된다. 이 판정은 [ADR-015](../adr/015-common-shared-systems-scope.md)의 Python 주입형 프리미티브(T-312)와 공용 로그인 UI 계약(`LoginForm`, 다섯 관리자 표면이 이미 쓴다)을 건드리지 않는다. BE-22가 적은 세션 상수(8시간·PBKDF2 310,000회·10분 5회)는 규약으로 남기되, T는 PBKDF2를 쓰지 않는다는 사실을 T-312가 계약을 고정할 때 반영해야 한다.

**K-54·K-55 — 공유하지 않음.** API client는 오류 형식 넷과 인증 모델 셋 위에 있다(`M:MA/src/api/client.ts` 711줄, `P:packages/api-client/src/client.ts` 469줄 등). 공통 fetch wrapper는 앱당 60줄을 아끼려고 그것들을 추상화해야 한다. 타입 생성은 M만 `openapi-typescript`를 쓰고 P는 zod다. 형제 서비스의 OpenAPI를 벤더한 **프론트**는 없다. 백엔드에는 있다: PinVi는 Map·weather OpenAPI 스냅샷을 시험 fixture로 갖고 weather 것은 SHA-256으로 고정한다(K-16). 이 문서는 그 고정을 늘리지도 줄이지도 않는다. `validateForm`은 M(규칙 기반)과 P(zod 기반)가 이름만 같다. `format.ts` 63줄은 M·W·T가 같고 K-50과 함께 간다.

**K-56 토큰 브리지 — 나중에 공유(기존 task).** D와 TP에는 `--kt-*` 정의가 없다(`git grep -- '--kt-'` 빈 결과). 공통 부품은 공통 기본 브랜드 색을, 로컬 화면은 앱 팔레트를 쓴다. 렌더링 결과는 확인하지 않았다. 기존 [T-472](../tasks/T-472-ktdm-tokens-adoption.md)·[T-431](../tasks/T-431-airport-tokens-adoption.md)이 이 범위다. M·W·T의 127줄 `@theme inline` alias 블록은 byte 동일하고 ✔ K-50의 부품이 그 이름으로 쓰여 있어 함께 다룬다.

**K-57 Dagster 운영 콘솔 — 나중에 공유(T-216).** 공통 `DagsterOperations`는 M·P가 쓴다. 그 뒤에 나온 상세·액션 콘솔은 W와 T에 같은 파일로 있다(`components/dagster-console.tsx` 302줄, `lib/dagster-console-{client,model}.ts` ✔; `lib/dagster-failure-diagnostics.ts`는 6줄 차이 ✔). 진행 중인 [T-216](../tasks/T-216-dagster-operations.md)이 흡수할 대상이다.

**K-58 `map-marker-react` — 나중에 공유.** `T:TA/lib/vendor/map-marker-react/`는 `M:packages/map-marker-react/src/`의 사본이다(`index.ts`·`marker.ts`·`palette.ts` 동일, `maki.ts` 주석 한 줄 차이 ✔, 원본 커밋과 라이선스를 README에 기록). 소비자가 둘이고 파일이 작아 지금의 "출처를 적은 복사"로 충분하다. 세 번째 소비자가 생기거나 표류가 동작 차이가 되면 `@kor-travel/admin-kit`에 넣는다.

**K-59 maplibre worker 복사·키 판정 — 나중에 공유(상류).** `scripts/copy-maplibre-worker.mjs`가 네 벌이다(P 49줄, M 43줄, W 28줄, T 44줄 ✔). VWorld 키 미설정 판정도 셋이 다르다. 자연스러운 자리는 `vworld-map-web` tarball이고 그 버전을 올리면 함대가 재vendor한다. 다음 정기 갱신에 싣는다. 요청 문서는 기존 T-505가 소유한다.

**K-60 지도 작업면 채택 — 공유하지 않음(기존 보류 유지).** W·T는 `MapWorkspace`·`MapStage`·`MapFilterPanel`을 쓰고 M의 `/features`는 쓰지 않는다. Map은 이것을 `T-UI-MAPWORKSPACE`로 보류해 뒀다(`M:docs/tasks.md:122` ✔: 고정 70dvh 지도 영역과 698px e2e 기준을 다시 설계해야 함). 다시 제안하지 않는다.

**K-61~K-65 — 공유하지 않음(K-64는 나중에).** 팔레트 코드 `P-01`은 M에서 `#1f77b4`, P에서 `#E53935`다(`M:packages/map-marker-react/src/palette.ts:38`, `P:packages/design-tokens/src/colors.ts:55` ✔). 같은 코드로 공유하면 한쪽 색이 조용히 바뀐다. 클러스터는 데이터 모양에 묶여 네 구현이다. e2e는 저장소별 운영 gate다. 다만 W·T 사이에는 같은 파일이 있다(`e2e/fixtures/native-delay-proxy.mjs` 동일, `address-refresh.spec.ts`는 기본 포트 한 줄 차이 ✔). 그것은 두 저장소 안의 정리다. vitest 설정은 9~33줄이고 중복은 import 한 줄이다. ESLint는 plugin 묶음 다섯·a11y 심각도 셋이 의도적이라 preset은 나중 일이다. doctor 플래그 한 줄은 [frontend-stack](../standards/frontend-stack.md)에 적는 것으로 충분하다.

**K-66 `@kor-travel/ui` 순수 재수출 shim — 지금 공유(채택 공백).** M·W·T의 `components/ui/*` 30개 가운데 13개(68줄)는 `export … from "@kor-travel/ui/…"`뿐이다 ✔(`tabs-variants`·`alert-dialog`·`breadcrumb`·`checkbox`·`data-table`·`native-select-option`·`popover`·`separator`·`skeleton`·`table`·`tabs`·`textarea`·`tooltip`). `lib/utils.ts`의 `cn`도 `@kor-travel/ui/utils`와 같다. 호출부 import를 각 shim이 재수출하던 원 경로와 원 이름으로 바꾸고 shim을 지우는 일은 릴리스가 필요 없고 함대 비용이 0이다. 넷은 경로나 이름이 shim과 다르다 ✔: `tabs-variants`는 `@kor-travel/ui/tabs`, `native-select-option`은 `@kor-travel/ui/native-select`, `data-table`은 `@kor-travel/ui/virtual-table`(`VirtualTable as DataTable`, `VirtualTableClampCell as DataTableClampCell`), `alert-dialog`는 `AlertDialogCancel as AlertDialogClose`다. `@kor-travel/ui`에는 `./tabs-variants`·`./native-select-option`·`./data-table` 하위 경로가 없다 ✔. 줄 수 이득은 작다. 가치는 K-50 채택 때 건드릴 파일을 줄이는 데 있다.

### 3.6 Ops·CI

**K-70 Node CI job 골격 — 나중에 공유.** setup-node 22.23.1 → `npm install --global npm@12.0.1` → `npm ci --engine-strict` → 검사·빌드 순서가 W·T(2개 job)·D에서 같은 모양이다. P·M은 workspace 루트 설치라 모양이 다르다. main을 읽지 않는 재사용 workflow를 커밋으로 호출하면 함대 결합이 없다(수단 C). 기존 [T-401](../tasks/T-401-reusable-workflows-quality.md)의 `node-quality.yml`이 이 범위다.

**K-71·K-72 — 공유하지 않음.** Python 설치가 넷이고(uv 고정, uv 미고정, pip+constraints, pip+정확 핀) format은 P만 강제하고 mypy는 M·P만 돌린다. ADR-011의 C20은 format 규칙을 이미 빼 두었으므로 재포맷은 쟁점이 아니다. 남는 사실은 이렇다: ruff 베이스의 공통 부분(`line-length=100`, `E,F,I,UP,B`)은 ruff를 쓰는 곳에서 이미 같아 공유해도 지워지는 것이 몇 줄이고, 그 밖의 규칙군·mypy 실행·import-linter·coverage는 저장소마다 다른 선택이다. 재사용 `python-quality.yml`은 네 설치 방식과 Map의 네 세션을 입력 행렬로 받아야 하고, ruff·mypy가 없는 T에는 새 강제가 된다(R2, R7). ADR-011 1차·BE-6~BE-11·T-305와 어긋나는 판정이다(§1.5). Dockerfile은 핀 방식·사용자·잠금이 다르다.

**K-73·K-74 `build-images.py`·`.dockerignore` matcher — 나중에 공유(유지 팀 판단).** `W:scripts/build-images.py`(730줄)는 `T:scripts/build-images.py`(673줄)를 원형으로 적은 fork다(`W:scripts/build-images.py:31` ✔, 최상위 함수 이름 18개 공통 ✔). `.dockerignore` matcher는 W·T·D에 세 구현이 있고 지원 문법이 다르다. 발견한 것 중 가장 큰 글자 그대로의 중복이지만 두 사본 모두 다른 팀 소유이고 Manager의 서비스별 경로 둘에 물려 있다.

**K-75 비내구 테스트 PostgreSQL helper — 나중에 공유.** `M:tests/integration/_disposable_pg.py`(69줄)와 `P:apps/api/tests/integration/_disposable_pg.py`(72줄)는 서버 명령과 `make_nondurable` 본문이 같다 ✔. P에 PG 주 버전 분기가 더 있고, env 이름(`KTM_…`/`PINVI_…`)·기본 크기(3g/2g)·빈 값 처리도 다르다. 소비자가 둘이고, 공유하면 테스트 시점에 git 핀 패키지 의존이 생긴다. 세 번째 소비자가 생기면 P 판을 기준으로 `[testing]` extra에 둔다.

**K-76·K-77·K-79 — 공유하지 않음.** 배포 스크립트는 호스트와 gate에 묶여 있다. Map의 `scripts/n150/*`는 이미 Manager launcher 위의 얇은 순서 스크립트다. 전체 트리 redaction을 도입하면 모든 소비자가 첫날 실패한다(운영 도메인 형식에 걸리는 추적 파일: P 2, M 3, W 19, T 37, D 8). 새 강제 계층이고(R2) 정리 빚의 대부분이 다른 팀 저장소에 있다(R7). Manager의 `build-bytecode.py`는 의도적으로 의존 없이 둔 사본이다.

**K-78 Map의 guard 검사 코드 지연 — 나중에 공유(결정 선행).** Map은 `55a921b`를 호출한다. 그 판에는 도구 규칙 단계가 없다. 최신으로 올리면 루트 `.nvmrc`와 정확 `engines.node`가 필요하다(Map 루트는 범위 선언). #1504의 커밋 메시지가 "정확 Node/npm 도구 규칙 이관은 별도 결정"이라고 적었다 ✔. Map이 정확 핀을 채택할지는 소유자에게 질의된 상태이고 답이 없다. 그래서 결정 task([T-416](../tasks/T-416-map-exact-node-npm-pin-decision.md))를 따로 두고, 이관([T-417](../tasks/T-417-map-guard-ref-toolchain.md))은 그 뒤에 둔다. Map이 옛 guard에 남으면 지금처럼 main 정책이 바뀔 때마다 당일 재vendor한다. 다른 task는 이 결정을 기다리지 않는다(§4.1).

## 4. 공유 대상의 설계

### 4.1 프론트 정책 guard와 릴리스 모델(K-01·K-02·K-78)

문제는 §2.2다. 원인은 넷이다: (가) 정책 데이터와 Node/npm 도구 축을 `main`에서 읽는다, (나) 패키지마다 한 버전만 허용한다, (다) tarball이 정책 전체의 사본을 싣고 있어 무관한 패키지가 함께 오른다, (라) 소비자는 자기가 고정한 옛 검사기를 실행하고 그 검사기는 현재 값 하나만 읽는다.

| 안 | 내용 | 얻는 것 | 잃는 것 |
|---|---|---|---|
| 1. 정책을 호출 커밋에서 읽기(권고) | guard가 정책 세 파일과 도구 축을 `main`이 아니라 호출자가 고정한 `common-ref`에서 읽는다. 지연은 주간 보고(막지 않음)로 본다 | 가장 단순하다. 정책·Node/npm·registry 패키지 어느 것이 바뀌어도 소비자는 자기가 ref를 올릴 때만 영향을 받는다. 긴급 보안 갱신은 ref를 올리는 PR 하나다. Python 핀(수단 A)과 같은 모양이 된다 | 최신 정본으로의 **강제** 수렴이 사라진다. [frontend-libraries](../standards/frontend-libraries.md) '검사와 갱신' 절의 의도를 바꾼다. 소비자가 한 번은 호출 SHA를 올려야 이 동작을 얻는다 |
| 2. 예고 필드 | 새 버전을 정책의 추가 필드에 싣고 현재 값은 채택 뒤 별도 PR이 바꾼다 | 예고 시점에 아무도 실패하지 않고 수렴 강제가 남는다 | 릴리스가 두 PR이 된다. 예고 자리가 하나면 창이 닫힐 때까지 다른 릴리스가 기다린다. 창 길이를 다른 팀의 채택이 정한다. Node/npm과 registry 패키지까지 같은 필드를 넓혀야 한다. 긴급 갱신 경로를 따로 정해야 한다. guard를 올릴 수 없는 소비자(Map)는 마감 당일 실패한다 |
| 3. 직전 버전 허용 + 만료일 | 현재 값을 올리고 직전 값을 추가 필드에 둔다 | 새 검사기 소비자만 보호된다 | 옛 검사기 소비자는 그날 실패한다((라)). 날짜로 실패가 생긴다 |
| 4. 현행 + 절차 | common PR이 소비자 PR을 모두 준비한 뒤 병합 | 변경 없음 | 실패 구간이 남는다(11-17에도 일부 그렇게 했으나 두 저장소가 뒤처졌다) |

안 1을 권고한다. 2회차 리뷰의 단계별 추적이 안 2의 숨은 비용을 드러냈다: 예고 자리 하나와 끝이 정해지지 않은 창, Node/npm 축 미포함, 긴급 경로 부재, 원장이 표현하지 못하는 조건부 순서. 안 1은 이 모두가 생기지 않는다. 잃는 것은 강제 수렴 하나이고, 그것은 보고로 본다. 소유자가 수렴 강제를 유지하기로 하면 안 2를 택하되 위 조건(최대 창 길이와 초과 시 처리, 긴급 경로, Node/npm 포함)을 ADR에 함께 정해야 한다. 결정은 ADR-019([T-023](../tasks/T-023-frontend-guard-release-model-adr.md))가 한다.

안 1에서 일어나는 일:

1. common이 새 guard workflow를 낸다([T-024](../tasks/T-024-guard-model-implementation.md)). 옛 SHA를 호출하는 소비자는 지금과 똑같이 동작한다(main을 읽는다). 아무도 실패하지 않는다.
2. 소비자가 호출 SHA를 그 커밋으로 올린다(pinvi [T-424](../tasks/T-424-pinvi-guard-ref.md), weather [T-467](../tasks/T-467-weather-guard-ref.md), transport [T-436](../tasks/T-436-transport-guard-ref.md), docker-manager [T-474](../tasks/T-474-ktdm-guard-ref.md), map [T-417](../tasks/T-417-map-guard-ref-toolchain.md)). 올린 뒤로는 main의 정책 변경이 그 소비자를 깨지 않는다.
3. 호출 SHA를 "최신"이 아니라 **T-024가 지정한 채택 커밋 하나**로 올린다. #1504는 SHA를 올리면서 그 뒤에 더해진 규칙까지 받아 실패했다. T-024는 그 커밋의 검사기를 각 소비자의 현재 main에 읽기 전용으로 돌려 걸리는 규칙을 미리 적는다. T-025 릴리스 뒤에 옮기는 소비자는 이미 T-025 판을 벤더했으므로 T-025가 적어 둔 동결 커밋으로 올린다.
4. Map은 호출 SHA를 올리면 도구 규칙에 걸린다(K-78). 정확 핀을 채택할지는 소유자 결정이다([T-416](../tasks/T-416-map-exact-node-npm-pin-decision.md)). 채택하지 않으면 Map은 옛 guard에 남아 지금처럼 main 정책 변경마다 당일 재vendor한다. 다른 task는 Map의 결정을 기다리지 않는다. **2026-11-17 결정: 채택, Node 26.13.1.** 공통 축(22.23.1)과 달라서 Map은 축을 26.13.1로 올리는 [T-029](../tasks/T-029-node-axis-to-latest-lts.md)의 커밋으로 옮긴다(T-417).
5. geo·concierge도 같은 guard의 소비자다(`97f8ed9` 호출). 이번 범위 밖이라 task가 없다. 올리지 않으면 지금과 같을 뿐이고, 이 계획의 어느 단계도 두 저장소의 채택을 선행으로 두지 않는다.

(다)는 따로 고친다([T-025](../tasks/T-025-decouple-embedded-policy.md)). 각 패키지는 **자기 것만**(자기 peer 범위와 자기 식별) 싣고, 소비자의 로컬 `check:dependencies`는 그것만 검사한다. 함대 전체의 정확 버전 대조는 중앙 guard의 몫으로 남긴다. 그러면 소비자의 `check:dependencies` 명령 줄은 바뀌지 않고, 정책에 무관한 패키지를 더하거나 바꿔도 `ui`·`tokens`·`toast`가 다시 pack되지 않는다. 다른 방식(tarball에서 사본을 빼고 정책 파일 경로를 인자로 받기)은 택하지 않는다: 일곱 소비자 프론트가 인자 없이 tarball 안의 검사기를 실행하고 CI가 그것을 막으므로 모든 소비자의 명령 줄을 바꿔야 하고, 정책 파일을 소비자가 벤더하면 K-02의 비용이 소비자로 옮겨갈 뿐이다.

T-025 자체는 세 패키지의 pack 내용을 바꾸므로 **한 번은** 세 패키지의 버전이 오른다. patch 올림이다(`ui` 0.2.2·`tokens` 0.1.3·`toast` 0.1.2, breaking 없음). 이 릴리스를 소비자가 새 guard로 옮긴 뒤에 내면 그 소비자는 깨지지 않는다. 옮기지 않은 소비자(main 정책을 읽는 옛 guard)는 그날 재vendor해야 한다(지금과 같다). 그래서 T-025의 외부 선행에 적었다: pinvi·docker-manager의 호출 SHA 갱신(T-424·T-474)이 병합됐을 것, weather·transport는 갱신(T-467·T-436)이 병합됐거나 그 팀이 당일 재vendor를 확인했을 것. Map은 T-416의 답을 기다리는 동안 옛 guard(`55a921b`)에 남으므로 그날의 재vendor를 task로 둔다([T-419](../tasks/T-419-map-ui-tokens-revendor-on-t025.md)). T-417이 먼저 끝나면 T-419는 필요 없다. geo·concierge에는 릴리스 전에 공지한다.

### 4.2 원장과 standards를 실물에 맞춤(K-03)

- 대상: common 문서. [T-022](../tasks/T-022-ledger-reality-reconcile.md) → [T-027](../tasks/T-027-standards-after-reclassification.md).
- T-022: T-201~T-214와 T-302~T-312 각각을 실물(`packages/ui` 0.2.1, `packages/py` 0.1.0.dev0)과 대조해 "실물로 충족", "범위 재정의", "철회 제안", "그대로" 중 하나로 표시한다. §1.5 표의 모든 행을 ADR-020 초안의 결정 항목으로 올리고, 행마다 **결정자(소유자)**와 채택·기각·보류에 따라 달라지는 후속 task를 적는다. ADR-019는 T-023이 쓰므로 번호가 겹치지 않는다. 두 task 모두 `docs/adr/README.md`를 고치므로 뒤에 병합하는 쪽이 rebase한다.
- T-022는 묶인 task를 나눈다. T-306(C1+C9+C7)에서 C7을 따로 남긴다. T-308(C5·C16·C17·C8·C11·C10·C15·C18), T-307(C2+C3), T-304(C4+C13)도 항목별로 나눈다. 그래야 "공유하지 않음"이 유지할 모듈까지 지우지 않는다.
- T-027: ADR-020이 **accepted가 된 뒤** 채택된 항목만 standards에 옮긴다. ADR-020을 accepted로 만드는 것은 소유자의 행별 결정이고 T-027의 외부 선행이다. T-022가 끝났다고 T-027이 바로 풀리지 않는다.
- 이 정합이 끝나야 K-50의 실행 task가 기존 T-203·T-205·T-206·T-208·T-209·T-210과 겹치지 않는다.

### 4.3 Python 패키지 버전 규칙(K-04)

- 대상: common. [T-026](../tasks/T-026-python-version-rule.md).
- `packages/py`가 바뀌는 PR은 `pyproject.toml`의 버전을 올린다(`0.1.0.devN` 또는 다음 minor의 dev). 소비자 핀은 계속 40자리 커밋이다. 버전은 어느 핀이 어느 내용인지 사람이 구분하는 표지다.
- BE-29는 `@py-vX.Y.Z` 태그 선언을 규정하지만 py 태그는 없고 소비자는 커밋을 직접 핀한다. T-026은 이 현황을 문서에 적는다. 규칙 문장을 바꿀지는 T-027의 몫이다.
- Python을 바꾸는 task(T-313·T-314)는 이 규칙을 따른다. 둘이 같은 때 진행되면 dev 번호가 겹치므로 뒤에 병합하는 쪽이 rebase해 번호를 다시 매긴다.
- 새 CI 강제는 넣지 않는다(R2). 지금 세 핀은 내용이 같으므로 맞추기만 하는 PR은 내지 않는다.

### 4.4 HTTP 생존 probe 채택(K-10)

- 공통 코드는 이미 있다. 새 코드가 없다.
- 순서: [T-480b](../tasks/T-480b-map-api-http-health-probe.md)(Map 자체 compose)와 [T-486a](../tasks/T-486a-ktdm-api-http-health-probe.md)(Manager compose의 map-api·pinvi-api)는 서로 독립이다.
- 형식: `["CMD", "python", "-I", "-m", "kortravelcommon.http_health", "--port", "<포트 식>", "--path", "/health", "--timeout-seconds", "3"]`.
- **포트 식은 서비스마다 확인한다.** exec 형식의 `${…}`는 compose가 호스트 env로 치환한다.
  - Map 자체 compose: 컨테이너 env와 게시 포트가 같은 변수 `KOR_TRAVEL_MAP_API_PORT`다(`M:docker-compose.yml:417,508`). `${KOR_TRAVEL_MAP_API_PORT:-12701}`를 쓴다.
  - Manager compose의 map-api: 지금 probe는 컨테이너 안 env를 실행 때 읽는다(`D:docker-compose.yml:1741`). 컨테이너 안 포트는 `${KOR_TRAVEL_MAP_API_CONTAINER_PORT:-12701}`이고(`:1667` ✔) `KOR_TRAVEL_MAP_API_PORT`는 호스트 게시 포트다(`:1736` ✔). probe에는 **컨테이너 포트 식**을 쓴다.
  - Manager compose의 pinvi-api: 지금 probe도 compose가 `${PINVI_API_PORT:-12801}`를 치환한 값이다(`:2207` ✔). uvicorn이 같은 식의 포트에서 듣는다(`:2143` ✔). 식이 바뀌지 않는다.
- `interval`·`retries`·`start_period`는 그대로 둔다(map-api는 10초이고 재구축의 준비 대기가 여기에 기댄다). `timeout`만 probe timeout에 Python 시작 시간을 더한 값 이상으로 맞춘다.
- Manager의 새 시험은 서비스 이름을 쓰지 않는 일반 규칙으로 쓴다: "exec 형식 HTTP probe의 `--port`는 그 서비스 포트 매핑의 컨테이너 쪽과 같다"(R3).
- 함대를 깨지 않는 채택: compose가 요구하는 모듈이 고정 이미지에 없으면 재구축이 `compose up`에서만 죽는다. 두 task 모두 이미지 안에서 `python -I -c "import kortravelcommon.http_health"`가 0으로 끝나는지를 수용 기준에 둔다(`-m` 실행은 모듈이 없어도 1로 끝나서 '연결 거절'과 구분되지 않는다).

### 4.5 수집 결과 run tag(K-40) — 나중

- 대상: `kortravelcommon.dagster`(`[dagster]` extra). [T-313](../tasks/T-313-collection-outcome-tag.md).

```python
COLLECTION_OUTCOME_TAG = "kortravel/collection-outcome"

def record_collection_outcome(context, outcome: str) -> None:
    """자기 run의 관측 tag만 올린다. success < deferred < partial. 낮추지 않는다.
    instance·run 조회·tag 쓰기 실패로 수집을 실패시키지 않는다."""
```

- 동작은 두 사본과 같다. tag를 읽는 콘솔(K-57)이 T-216으로 공통에 들어갈 때 함께 하는 것을 권한다. 그 전에 해도 되지만 이득은 저장소당 20줄이다.
- 이관 순서: common 병합 → weather([T-481a](../tasks/T-481a-weather-collection-outcome.md))와 transport([T-482a](../tasks/T-482a-transport-collection-outcome.md))가 각자 핀을 올리며 로컬 함수를 지운다. 핀을 올리면 그 사이 common에 들어간 다른 변경도 함께 온다. T-314가 들어 있어도 두 저장소는 그 PR에서 새 cursor 기능을 켜지 않는다(§4.9).

### 4.6 다중 job 재시도 sensor 채택(K-41) — 나중

- 공통 코드는 이미 있다. [T-484a](../tasks/T-484a-pinvi-retry-sensor-for-jobs.md)(pinvi), [T-482b](../tasks/T-482b-transport-retry-sensor-for-jobs.md)(transport).
- sensor 이름이 바뀐다. 옛 sensor의 상태와 cursor는 새 sensor로 넘어가지 않는다. 공통 구현은 기본 상태가 RUNNING이다.
- pinvi는 지금 sensor마다 `with_updated_job(job)`으로 asset job을 다시 주입한다(`P:etl/definitions.py:95` ✔). 다중 job sensor에서는 `with_updated_jobs([다시 주입할 asset job 전부])`를 써야 한다(공통 구현은 `jobs=[…]`를 대상으로 하고 job 이름으로 run을 요청한다, `C:cpy/dagster.py:572,669-673` ✔).
- pinvi는 API 쪽 정적 sensor 목록(`apps/api/app/services/admin_etl.py`의 `PINVI_ETL_SENSORS`)과 그 모델(`job_name` 하나), 관리자 화면, 그리고 목록과 Definitions의 일치를 강제하는 시험이 함께 바뀐다. 배포물이 둘(api, etl)이라 순서가 있다.
- 합친 sensor는 한 tick에 RunRequest를 하나만 낸다. weather가 이 구현을 꺼 둔 상태라 두 채택이 첫 운영 사용이 될 수 있다.

### 4.7 로컬 경로 정규화 채택(K-51)

- 공통 코드는 이미 있다. [T-465](../tasks/T-465-weather-navigation-sanitize.md)(weather), [T-434](../tasks/T-434-transport-navigation-sanitize.md)(transport).
- weather 로컬 구현의 검증 차이는 kor-travel-weather #244(`8c3b4744`)로 이미 맞췄다. 두 task는 중복 제거만 다룬다.
- 로컬 `lib/navigation.ts`를 지우지 않고 얇게 줄인다. 문자열이 아니면 기본 경로, trim, 500자 초과면 기본 경로, 그다음 공통 `sanitizeLocalPath`를 부른다. URL 파싱과 경계 검사는 로컬에 두지 않는다.
- 호출부 import는 바꾸지 않는다(`@/lib/navigation`). weather의 호출부는 넷이다(로그인 route, 로그인 page, `middleware.ts`, 그리고 공통을 직접 쓰는 client 폼). transport는 셋 모두 로컬을 쓴다.
- **달라지는 동작**: 공통 함수는 값 어디에든 `%20`·`%25`·공백·제어 문자·인코딩된 경계 문자가 있으면 거절한다. 예를 들어 `next=/runs?q=a%20b`는 지금 그대로 보존되지만 바꾼 뒤에는 `/`가 된다. 두 task는 이 경우들을 시험으로 적고, 받아들일 수 없으면 채택하지 않는다.
- 패키지 버전이 바뀌지 않으므로 함대 비용이 없다.

### 4.8 관리자 공통 부품 묶음(K-50·K-52·K-56 일부)과 재수출 shim(K-66)

부품을 어디에 둘지 두 안을 비교했다.

| 기준 | (a) `@kor-travel/ui` 0.3.0의 하위 경로 | (b) 선택형 산출물 패키지 `@kor-travel/admin-kit` |
|---|---|---|
| 재vendor해야 하는 소비자 | `ui`를 벤더하는 전부(P·M·W·T·D·geo·concierge) | 부품을 쓰는 M·W·T만 |
| 릴리스 절차 | 기존 패키지의 현재 값이 바뀌므로 §4.1의 모델에 묶인다. 안 2라면 예고·채택·마감 세 단계 | 새 패키지라 직전 현재 값이 없다. 정책에 더하기만 한다 |
| 마감이 기다리는 것 | 다른 팀 두 저장소와 범위 밖 두 저장소의 채택 | 없음 |
| Map의 T-416 결정 | 채택 전에 필요(옛 검사기로는 창 동안 새 버전을 못 받음) | 필요 없음. `55a921b` 검사기도 main 정책에서 새 산출물을 읽어 검사한다(`ui`·`tokens`는 T-419로 T-025 판) |
| 드는 것 | 없음 | `ui`·`tokens`에 대한 peer(`@kor-travel/ui` `>=0.2.1 <0.3.0`, `@kor-travel/tokens` `>=0.1.2 <0.2.0`. `ui` patch마다 올리지 않는다), 릴리스 파이프라인이 한 패키지를 더 pack, 원장·정책에 한 항목. 새 guard를 쓰는 소비자는 채택할 때 호출 SHA를 올린다(아래) |
| 선행 | T-024(모델) | T-025(내장 정책 축소). 지금은 정책에 패키지를 더하는 것만으로 `ui`·`tokens`·`toast`가 다시 pack된다(§2.2) |

**(b)를 택한다.** 부품을 쓰지 않는 네 소비자가 이 묶음 때문에 치르는 비용이 0이 되고, 마감 단계와 그 단계가 다른 팀을 기다리는 일이 없어지고, Map이 소유자 결정을 기다리지 않는다. `@kor-travel/toast`가 같은 모양의 선례다. 드는 것은 패키지 하나의 관리다. 유일한 선행은 T-025다.

- 대상: 새 패키지 `packages/admin-kit` → `@kor-travel/admin-kit`. `artifactPackages`에 넣고 프로필 필수 목록에는 넣지 않는다.
- 선행: T-022(원장 정합), T-025(내장 정책 축소).
- 소스는 둘로 나눈다. 나누는 기준은 앱 의존이다.
  - [T-219](../tasks/T-219-admin-kit-package-self-contained.md): 패키지 골격과 앱 모듈에 기대지 않는 부품. `CopyButton`(토스트 주입)·`JsonViewer`·`SectionCard`·`FilterBar`·`HelpTip`과 `format`. `EmptyState`는 공통 `Empty`와 겹치므로 여기서 어느 쪽을 남길지 정한다.
  - [T-220](../tasks/T-220-admin-kit-injected.md): 앱 사전이나 라우터 링크에 기대던 부품과 폼·오류. `StatusBadge`와 variants·`StatStrip`·`DetailList`(사전·링크 주입)·`PaginationBar`·`FormField*`·`AppErrorPanel`과 `error-recovery`·skip link·header 띠.
- 넣지 않는 것: `ConfirmDialog`(ui-contract가 앱 소유로 둠, T-508), `validateForm`(map 한 곳), `status-label.ts`(도메인 사전), §3.5 K-50에 적은 앱 잔류 파일.
- 원천은 M·W·T에서 같은 파일이다. `help-tip`은 W·T 판(더 새 것)을 쓴다. transport 판이 다른 다섯 파일은 차이를 읽고 고른다. 클래스 어휘는 `--kt-*` 의미 토큰으로 옮긴다.
- [T-221](../tasks/T-221-admin-kit-0-1-0-freeze.md)이 0.1.0을 얼려 정책에 선택형 산출물로 더한다.
- 채택은 쓰는 저장소만 한다: map([T-415](../tasks/T-415-map-admin-kit-adoption.md)) → weather([T-466](../tasks/T-466-weather-admin-kit-adoption.md))·transport([T-435](../tasks/T-435-transport-admin-kit-adoption.md)). map을 먼저 권한다(원천이고 시각 회귀 기준이 있다). 선행 관계는 아니다.
- **채택과 guard 호출 SHA.** admin-kit은 벤더한 날부터 중앙 정본과 대조돼야 한다. 옛 guard(main 정책을 읽음)는 그대로 대조한다. 새 guard(T-024)는 소비자가 고정한 커밋의 정책으로 검사하는데, 그 커밋이 T-221보다 앞이면 정책에 admin-kit이 없어 검사기가 건너뛴다(`check_frontend_dependencies.mjs:99-100,144-145@97f8ed9` ✔). 통과는 하지만 벤더한 bytes가 대조되지 않는다. 두 길을 비교했다: (1) 그 공백을 문서에 적어 두고 소비자가 나중에 SHA를 올릴 때 대조가 시작되게 둔다, (2) 호출 SHA를 T-221이 지정한 admin-kit 채택 커밋으로 올리는 것을 채택의 첫 단계로 넣는다. **(2)를 택한다.** 대조되지 않는 벤더 산출물을 두지 않는 것이 원장의 목적이고, '새 산출물을 받으려면 고정 커밋을 그 산출물을 아는 곳으로 옮긴다'는 고정 커밋 모델의 원래 뜻이다. 그 커밋의 정책은 `ui`·`tokens`가 T-025 판이므로 첫 단계에서 함께 재vendor한다(앞선 PR로 나누기를 권한다). 시점은 채택하는 저장소가 정하고 다른 저장소를 기다리지 않는다. 옛 guard에 남은 Map은 이 단계가 없다(T-419로 이미 T-025 판).
- pinvi 관리자는 재도색 이식본이고 docker-manager의 부품은 다른 구현이다. 둘은 이 묶음 때문에 할 일이 없다. T-025 릴리스 날의 조건은 §4.1에 있다(호출 SHA 갱신이 먼저 병합돼 있으면 그날도 할 일이 없다).
- **릴리스 없이 지금 할 수 있는 것**(K-66): `components/ui/*`의 순수 재수출 shim 13개와 `lib/utils.ts`의 `cn`을 각 shim의 원 경로·원 이름 직접 import로 바꾼다(map [T-418](../tasks/T-418-map-ui-reexport-shims.md), weather [T-468](../tasks/T-468-weather-ui-reexport-shims.md), transport [T-437](../tasks/T-437-transport-ui-reexport-shims.md)). 뒤의 채택 PR이 작아진다.

### 4.9 나중 묶음의 첫 걸음

- **회수 sensor API**([T-314](../tasks/T-314-reconciliation-sensor-consumer-cursor.md)): callback이 `ReconcileTick(clock, cursor)`을 받고 새 하위 cursor를 돌려줄 수 있게 한다. **켜는 호출자만** 새 형식을 쓴다. 켜지 않은 호출자의 cursor는 지금과 byte 단위로 같다(`stall:` 뒤에 시계 JSON). `StallClock.from_dict`는 필드가 하나라도 더 있으면 거절하므로(`C:cpy/stall.py:79-83`) weather가 직접 읽는 cursor 안에 구획을 끼워 넣을 자리가 없다. 그래서 켜는 호출자는 cursor를 직접 읽는 것을 그만두고 `ReconcileTick.clock`을 써야 한다. weather·transport는 핀만 올려서는 아무것도 바뀌지 않는다.
- **공용 instance 설정**([T-486b](../tasks/T-486b-ktdm-shared-dagster-per-job-limit.md)): 여러 tenant의 동작을 바꾸므로 결정자는 소유자다. Manager가 영향(특히 Map의 job tag 수)을 확인해 결정 자료를 만든다.
- **webserver probe**(K-43)와 그 밖의 "나중에 공유"는 첫 채택자가 정해질 때 task를 연다.

## 5. 공유하지 않는 목록

다시 제안하지 않도록 이유와 함께 적는다. 조건이 바뀌면(세 번째 소비자, 계약 개편 시점) 그 조건을 근거로 새로 제안한다.

| 대상 | 이유 | 상세 |
|---|---|---|
| FastAPI app factory·lifespan | 다섯 계약이 일부러 다르다. 공통 factory는 결박층이다 | K-11 |
| settings 베이스 클래스 | 빈 env 의미와 profile 기본값이 반대다. env 이름은 배포 계약이다 | K-12 |
| DB 엔진·세션 팩토리 | 드라이버 셋, timeout이 사고별 값 | K-13 |
| Alembic `env.py` 템플릿·롤 처리 | 같은 위험을 반대로 다룬다. 롤·스키마·lock 키는 DB별 계약 | K-14 |
| health 응답 라우터 | 본문이 각 OpenAPI 산출물의 일부 | K-15 |
| outbound HTTP 재시도·circuit 정책 | 호출 자리의 결정 | K-18 |
| 오류 envelope | 다섯 형식. 통합은 파괴적 변경 | K-19 |
| 페이지 meta envelope·query 이름 | 계약. 코덱만 따로 본다 | K-20 |
| rate limit | 일반 구현이 하나 | K-21 |
| Valkey·cache 헬퍼 | 구현이 하나이고 범용 cache가 아니다 | K-22 |
| 지표 이름·라벨, 로깅 설정, redaction 규칙 | 대시보드·경보·누출 표면에 묶임 | K-24 |
| geo REST client, 형제 서비스 client | wrapper 금지, 계약 핀 금지 | K-30 |
| provider 호출 wrapper·한도 분류기 | Map 규칙. 고칠 자리는 provider 라이브러리 | K-32 |
| 한국 좌표 경계 상수, 지구 반지름, 반경 상한, bbox 파서 | 값이 정당하게 다르다. 2026-09 판정을 값으로 재확인 | K-34 |
| Dagster Definitions 골격, schedule on/off 방식, run 실패 통지 sensor | 도메인 결선과 앱 소유 테이블 | K-47 |
| 적재·수집 run 원장 테이블 | 스키마가 도메인. 서로 핀하지 않는다 | K-48 |
| standalone `dagster.yaml` | 로컬 스택에 필요 | K-49 |
| Map 회수 sensor·in-step stall watchdog | 의도된 불일치(주기·반환형·시계 둘) | K-42 |
| Next 계층 세션 서명·PBKDF2·로그인 제한 | 재구현이고 폐기 저장소·신뢰 경계가 다르다 | K-53 |
| API client·fetch wrapper·타입 생성 방식 | 오류 형식 넷·인증 모델 셋 | K-54 |
| 폼 검증기·responsive hook | 이름만 같은 다른 모델 | K-55 |
| Map `/features`의 지도 작업면 채택 | Map이 사유를 적어 보류한 항목(`T-UI-MAPWORKSPACE`) | K-60 |
| 마커 팔레트 표, 클러스터 엔진, bbox 형식 | 같은 코드에 다른 색. 데이터 모양·API 계약 | K-61 |
| e2e 하네스 패키지, live runner | 저장소별 운영 gate와 증거 규칙 | K-62 |
| vitest 설정·test-utils, tsconfig·postcss·npmrc | 2~33줄, 배치 종속 | K-63, K-65 |
| Python 품질 설정·`python-quality` workflow | 공통 부분은 이미 같고 나머지는 저장소별 선택. 설치 방식 넷(§1.5와 어긋남) | K-71 |
| Dockerfile 템플릿 | 핀·사용자·잠금 방식이 다르다 | K-72 |
| 배포·호스트 스크립트, 백업 스크립트 | 호스트·gate별. Map의 것은 이미 얇다 | K-76 |
| 소비자 전체 트리 redaction·task 원장 lint 강제 | 새 강제 계층. 도입 즉시 모든 소비자 실패 | K-77 |
| Manager의 `build-bytecode.py` 사본 | 의도된 무의존 사본 | K-79 |
| PinVi 사용자 표면 UI·모바일 UI, PinVi 관리자 재도색 이식본의 강제 통합 | 소비자 브랜드. [ui-contract](../standards/ui-contract.md)가 범위 밖으로 둠 | K-50 |
| Python 핀을 맞추기만 하는 PR | 세 핀의 내용이 같다 | §4.3 |
| `ConfirmDialog` 공통 API, `validateForm` | ui-contract가 앱 소유로 둠(T-508). 규칙 기반 검증은 map 한 곳 | K-50, K-55 |
| 보안 헤더 미들웨어, CORS 헬퍼 | 헤더 값·신뢰 정책이 제품별. CORS는 이미 Starlette가 공통 | K-25 |
| 부품을 쓰지 않는 소비자까지 재vendor시키는 방식(`@kor-travel/ui`를 키우기) | 선택형 산출물 패키지가 같은 일을 함대 비용 없이 한다 | §4.8 |

## 6. Task 목록

수용 기준·검증 명령·되돌리기는 각 상세 파일이 정본이다([task 규칙](../tasks-rule.md) §4·§5). 아래 표는 순서와 묶음만 준다. "묶음" 글자가 같은 task는 동시에 진행할 수 있다. "—"는 앞뒤 순서가 정해진 task다.

**먼저 할 수 있는 것(선행 없음)**

| Task | 소유 저장소 | 한 줄 | 묶음 |
|---|---|---|---|
| [T-022](../tasks/T-022-ledger-reality-reconcile.md) | common | UI·Python 원장 재분류와 ADR-020 초안 | A |
| [T-023](../tasks/T-023-frontend-guard-release-model-adr.md) | common | guard·릴리스 모델 ADR-019 | A |
| [T-026](../tasks/T-026-python-version-rule.md) | common | Python 패키지 버전 규칙 | A |
| [T-480b](../tasks/T-480b-map-api-http-health-probe.md) | kor-travel-map | Map API healthcheck를 공통 probe로 | A |
| [T-486a](../tasks/T-486a-ktdm-api-http-health-probe.md) | kor-travel-docker-manager | map-api·pinvi-api healthcheck를 공통 probe로 | A |
| [T-418](../tasks/T-418-map-ui-reexport-shims.md) | kor-travel-map | 순수 재수출 shim 제거 | A |
| [T-468](../tasks/T-468-weather-ui-reexport-shims.md) | kor-travel-weather | 순수 재수출 shim 제거 | A |
| [T-437](../tasks/T-437-transport-ui-reexport-shims.md) | kor-travel-transport | 순수 재수출 shim 제거 | A |
| [T-465](../tasks/T-465-weather-navigation-sanitize.md) | kor-travel-weather | 로컬 경로 정규화의 판정 본체를 공통 호출로 | A |
| [T-434](../tasks/T-434-transport-navigation-sanitize.md) | kor-travel-transport | 로컬 경로 정규화의 판정 본체를 공통 호출로 | A |
| [T-416](../tasks/T-416-map-exact-node-npm-pin-decision.md) | kor-travel-map | 정확 Node/npm 핀 채택 여부 결정(2026-11-17 채택, Node 26.13.1. Map PR 병합 대기) | A |
| [T-486b](../tasks/T-486b-ktdm-shared-dagster-per-job-limit.md) | kor-travel-docker-manager | 공용 instance의 job별 한도·`run_retries` 결정 자료와 구현(2026-11-17 자료: 일반 규칙 미채택, 재결정 대기) | A |

**guard 모델과 내장 정책**

| 순서 | Task | 소유 저장소 | 한 줄 | 선행 | 묶음 |
|---|---|---|---|---|---|
| 1 | [T-024](../tasks/T-024-guard-model-implementation.md) | common | ADR-019가 정한 guard 모델 구현과 채택 커밋 지정 | T-023 | — |
| 2 | [T-424](../tasks/T-424-pinvi-guard-ref.md) | pinvi | guard 호출 SHA를 채택 커밋으로 | T-024 | B |
| 2 | [T-467](../tasks/T-467-weather-guard-ref.md) | kor-travel-weather | guard 호출 SHA를 채택 커밋으로 | T-024 | B |
| 2 | [T-436](../tasks/T-436-transport-guard-ref.md) | kor-travel-transport | guard 호출 SHA를 채택 커밋으로 | T-024 | B |
| 2 | [T-474](../tasks/T-474-ktdm-guard-ref.md) | kor-travel-docker-manager | guard 호출 SHA를 채택 커밋으로 | T-024 | B |
| 3 | [T-025](../tasks/T-025-decouple-embedded-policy.md) | common | 내장 정책을 패키지 자기 것으로 줄이고 세 패키지 patch 릴리스(외부 선행: 소비자 호출 SHA 갱신 또는 당일 재vendor 확인) | T-023, T-024 | — |
| 4 | [T-419](../tasks/T-419-map-ui-tokens-revendor-on-t025.md) | kor-travel-map | T-025 릴리스 당일 `ui`·`tokens` 재vendor(T-417 미완일 때) | T-025 | — |
| 4 | [T-029](../tasks/T-029-node-axis-to-latest-lts.md) | common | 공통 Node 축을 26.13.1로(외부 선행: geo·concierge 포함 옛 판 호출자 전부의 호출 SHA 갱신) | T-024 | — |
| 5 | [T-417](../tasks/T-417-map-guard-ref-toolchain.md) | kor-travel-map | guard 호출 SHA를 T-029 커밋으로, 남은 도구 규칙 입력(T-416 채택) | T-416, T-024, T-029 | — |

**원장·standards**

| 순서 | Task | 소유 저장소 | 한 줄 | 선행 |
|---|---|---|---|---|
| 1 | [T-027](../tasks/T-027-standards-after-reclassification.md) | common | 재분류 결정을 standards에 반영(ADR-020 accepted 뒤) | T-022 |

**관리자 부품 묶음(선택형 패키지)**

| 순서 | Task | 소유 저장소 | 한 줄 | 선행 | 묶음 |
|---|---|---|---|---|---|
| 1 | [T-219](../tasks/T-219-admin-kit-package-self-contained.md) | common | `@kor-travel/admin-kit` 골격과 앱 의존 없는 부품 | T-022, T-025 | — |
| 2 | [T-220](../tasks/T-220-admin-kit-injected.md) | common | 사전·링크 주입 부품과 폼·오류 | T-219 | — |
| 3 | [T-221](../tasks/T-221-admin-kit-0-1-0-freeze.md) | common | admin-kit 0.1.0 동결과 선택형 산출물 등록 | T-219, T-220 | — |
| 4 | [T-415](../tasks/T-415-map-admin-kit-adoption.md) | kor-travel-map | admin-kit 채택(먼저 권장. 옛 guard면 T-419 뒤) | T-221 | C |
| 4 | [T-466](../tasks/T-466-weather-admin-kit-adoption.md) | kor-travel-weather | admin-kit 채택(새 guard면 호출 SHA·`ui`·`tokens` 먼저) | T-221 | C |
| 4 | [T-435](../tasks/T-435-transport-admin-kit-adoption.md) | kor-travel-transport | admin-kit 채택(새 guard면 호출 SHA·`ui`·`tokens` 먼저) | T-221 | C |

**Dagster(나중)**

| Task | 소유 저장소 | 한 줄 | 선행 |
|---|---|---|---|
| [T-313](../tasks/T-313-collection-outcome-tag.md) | common | 수집 결과 run tag 함수 | T-026 |
| [T-481a](../tasks/T-481a-weather-collection-outcome.md) | kor-travel-weather | 로컬 결과 tag 함수를 공통으로 | T-313 |
| [T-482a](../tasks/T-482a-transport-collection-outcome.md) | kor-travel-transport | 로컬 결과 tag 함수를 공통으로 | T-313 |
| [T-314](../tasks/T-314-reconciliation-sensor-consumer-cursor.md) | common | 회수 sensor의 선택형 소비자 cursor | 없음 |
| [T-484a](../tasks/T-484a-pinvi-retry-sensor-for-jobs.md) | pinvi | 재시도 sensor 5개를 1개로(API 정적 목록 포함) | 없음 |
| [T-482b](../tasks/T-482b-transport-retry-sensor-for-jobs.md) | kor-travel-transport | 재시도 sensor 3개를 1개로 | 없음 |

저장소별 수: common 12, kor-travel-map 6, pinvi 2, kor-travel-weather 5, kor-travel-transport 6, kor-travel-docker-manager 3(합 34. T-029는 2026-11-17 소유자 결정 뒤에 더했다).

조건이 붙은 곳은 넷이다. T-417은 T-416이 "채택"일 때만 진행하고 "미채택"이면 그 결정으로 닫는다(2026-11-17 채택으로 정해졌고, T-029 뒤에 진행한다). T-419는 T-025 릴리스 날 Map이 옛 guard에 남아 있을 때만 실행하고 T-417이 먼저 끝났으면 닫는다. T-025의 동결은 외부 선행(소비자별 호출 SHA 갱신 또는 당일 재vendor 확인)을 확인한 뒤에 병합한다. T-027은 ADR-020이 accepted가 된 뒤에만 병합한다(소유자의 행별 결정, 상세 파일의 외부 선행). 그 밖의 선행은 모두 원장의 `선행` 열에 있다.

geo·concierge는 이번 범위 밖이라 task가 없다. 이 계획의 어느 task도 두 저장소의 작업을 선행으로 두지 않는다. 두 저장소가 guard 호출 SHA를 올리지 않으면 T-025의 릴리스 날 지금과 같이 당일 재vendor가 필요하다. T-025가 릴리스 전에 알린다. 이 계획에는 두 저장소의 재vendor task가 없다.

새 task를 만들지 않고 기존 task에 맡긴 것: 공개 API 키(T-306의 C7)·proxy 신뢰(T-308의 C8), request-id(T-307, 지표와 분리해), time(T-304), cursor 코덱(T-508), 토큰 브리지(T-472·T-431), Dagster 콘솔(T-216), Node CI 골격(T-401의 Node 절반), provider 핀·worker 스크립트 요청(T-505·T-506), docker-manager의 부품 전환(T-473). 이들의 재분류는 T-022가 한다.

task를 만들지 않은 "나중에 공유": webserver probe(K-43), code-server probe 수렴(K-44), Map coalescing(K-45), `map-marker-react`(K-58), 빌드 영수증 생산자(K-73·K-74), 테스트 PG helper(K-75), ESLint preset(K-64), 시도 표(K-33). 첫 채택자나 선행 결정이 정해질 때 연다.

ID는 [task 규칙](../tasks-rule.md) §2에 따라 이미 참조된 번호를 피했다. T-414·T-423·T-480a는 설계 패널 문서가 다른 뜻으로 쓴 적이 있어 쓰지 않았다. `docs/survey/`에 보이는 T-026·T-219·T-314는 geo·pinvi 저장소 자체의 task 번호라 이 저장소의 ID와 겹치지 않는다. "ADR-019"는 `docs/architecture/consumers.md`·`adoption-readiness.md`·`design-brief.md`에서 geo 저장소의 ADR을 가리킨다. T-023이 쓰는 ADR-019는 이 저장소의 것이고 T-023이 그 구분을 적는다.

소비자 저장소의 task는 그 저장소의 backlog에 포인터 한 줄로 등록한다. 포인터는 이 문서와 상세 task를 가리키고 수용 기준을 복제하지 않는다.

## 7. 검증하지 못한 것

- **실행 확인이 없다.** 모든 판정은 소스 읽기다. 테스트·빌드·이미지 실행을 하지 않았다. "지워지는 줄 수"는 어림이다.
- **K-51**: 세 구현의 차이는 소스 비교로 확인했다. kor-travel-weather #244(`8c3b4744`)의 단위 시험은 그 PR의 CI에서 통과했지만 운영 반영(weather 배포)은 확인하지 않았다.
- **K-10**: 고정된 운영 이미지 안에서 probe가 도는지 보지 않았다. 핀 커밋에 모듈 파일이 있다는 것만 확인했다. PinVi API 이미지에서 `python`이 PATH의 어떤 해석기를 가리키는지도 보지 않았다.
- **K-46**: 호스트에 렌더링된 실제 instance 설정을 보지 않았다(호스트 접근 금지). 추적된 YAML과 override 표만 읽었다. Map의 queue run들이 같은 `kortravelcommon/job` 값을 갖는지 확인하지 않았다.
- **K-56**: D·TP에서 공통 부품이 어떤 색으로 그려지는지 보지 않았다(CSS 읽기만).
- **K-50**: 45개 파일의 동일성은 다시 셌지만 PW 관리자 이식본과의 차이는 하위 조사의 표본 diff다. 로컬 어휘를 `--kt-*`로 옮길 때의 시각 차이는 재지 않았다.
- **K-78**: 최신 도구 규칙 검사기가 Map의 범위 `engines`를 실제로 거절하는지 실행하지 않았다. #1504 첫 실행의 실패 문장만 읽었다.
- **guard의 현재 상태**: 개정 시점에 다섯 저장소 모두 후보 12를 벤더하고 main의 guard가 통과한다(map은 #1504 병합 뒤, weather는 #243·#244 병합 뒤 실행을 `gh`로 확인). 11-17 오전의 실패 구간은 재vendor PR의 실행 결과로만 직접 봤다.
- **provider 라이브러리 내부**(`failure_kind` 범위 등)와 geo·concierge 코드는 읽지 않았다.
- **`✔` 없는 인용**은 하위 조사가 `nl -ba`·`grep -n`으로 확인했다고 보고한 값이다. 작성자가 다시 읽은 표본에서는 모두 맞았지만 전수는 아니다.
- **TypeScript 쪽 시간·거리 헬퍼**는 표본만 봤다.
- **K-25(보안 헤더·CORS)**: 위치와 값 차이는 2회차 리뷰의 인용을 받아 P·T 두 파일을 직접 읽어 확인했다. W·M·D의 '없음'은 다시 grep하지 않았다.
- **옛 검사기 동작**(§4.1·§4.8): 두 고정 검사기가 읽는 정책 키와 '선언하지 않은 산출물은 건너뛴다'는 소스에서 확인했다. 새 선택형 패키지가 든 정책으로 실제로 돌려 보지는 않았다. T-221의 수용 기준이다.
- **Dagster API**: `with_updated_job`이 대상을 job 하나로 바꾼다는 것은 리뷰어의 Dagster 소스 인용을 받아들인 것이고 직접 실행하지 않았다. 공통 구현 쪽(`jobs=[…]`, job 이름 요청, tick당 하나)은 직접 읽었다.
- **정책에 패키지를 더하면 세 패키지가 다시 pack된다**(§2.2)는 생성·복사 스크립트와 common journal의 기록에서 끌어낸 것이다. pack해서 bytes를 비교하지는 않았다. T-025의 수용 기준이 이것을 시험한다.
- **PinVi 관리자 화면**이 `PINVI_ETL_SENSORS`를 어떻게 그리는지는 보지 않았다(K-41).
- **K-66**: 순수 재수출 13개는 map 기준으로 셌다. weather·transport는 같은 파일이 byte 동일하다는 것(K-50)에서 같다고 본다.

## 8. 근거

- 2026-09 조사: [commonality matrix](../survey/commonality-matrix.md), [backend](../survey/cross/backend.md), [ci-deploy](../survey/cross/ci-deploy.md), [survey README](../survey/README.md).
- 결정: [ADR-011](../adr/011-python-common-package.md), [ADR-014](../adr/014-common-implementation-without-registry-publishing.md), [ADR-015](../adr/015-common-shared-systems-scope.md), [ADR-017](../adr/017-shadcn-radix-shared-components.md), [ADR-018](../adr/018-exact-node-npm-build-toolchain.md).
- 규칙: [backend-stack](../standards/backend-stack.md) §8·§10, [frontend-libraries](../standards/frontend-libraries.md), [ui-contract](../standards/ui-contract.md), [versions](../standards/versions.md).
- 실물: `packages/py/kor-travel-common`, `packages/ui`, `tools/check_frontend_dependencies.mjs`, `.github/workflows/frontend-consumer-guard.yml`.
- 2026-11-17 PR: common #57·#58, pinvi #763, kor-travel-transport #205, kor-travel-docker-manager #605, kor-travel-map #1504, kor-travel-weather #243·#244.
