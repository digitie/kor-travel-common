# 공통화 재조사와 실행 계획 — 2026-11-17

- 정본 지위: 다섯 저장소(pinvi·kor-travel-map·kor-travel-weather·kor-travel-transport·kor-travel-docker-manager)의 코드에서 **무엇을 공통으로 만들 수 있고 무엇은 만들면 안 되는지**를 고정 커밋 기준으로 다시 조사한 결과와 실행 순서다. 이 문서는 근거와 계획이며 규범이 아니다. 규칙은 [standards](../standards/README.md)·[ADR](../adr/README.md), 실행 범위와 수용 기준은 [task 원장](../tasks.md)과 상세 task가 정본이다.
- 상태: **초안**. 소유자 요청(2026-11-17)에 따른 1차 작성본이며 독립 적대 리뷰 2건을 아직 거치지 않았다. 판정은 제안이고 ADR·task로 옮겨지기 전에는 결정이 아니다.
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
| Python 공통 | 후보 C1~C21, 실행 task T-302~T-312, 소비 T-480~T-486. 1차는 C12 export·C4 health·C13 time·C20 quality | 계획한 모듈은 하나도 구현되지 않았다. 실물 `kortravelcommon`은 운영 장애가 요구한 다른 묶음이다: Dagster 복구·coalescing·회수 sensor, code-server·HTTP·gRPC probe, 응답 상한 HTTP, deadline, 정체 시계, 역지오코딩 갱신(T-319 계열). 원장은 T-302를 READY, T-303~T-312를 BLOCKED로 둔 채다 |
| React UI | T-201~T-214(base-ui 전제) | T-218이 Radix 기반 `@kor-travel/ui` 0.2.1·`tokens` 0.1.2·`toast` 0.1.1과 중앙 guard를 실물로 만들었다. 원장은 T-201(골격)을 BLOCKED로 둔 채다. [ui-contract](../standards/ui-contract.md)가 약속한 관리자 부품은 패키지에 없다 |
| 공유 비용 | 배포 방식 후보 비교까지. 채택 뒤 운영 비용은 다루지 않음 | 2026-11-17 실측: 정책 한 번 바꾸자 다섯 저장소에 재vendor PR 5개·파일 80개(§2.2) |
| 판정 근거 | 저장소 수와 함수 동일성 | 다섯 저장소의 현재 줄 번호와 차이 분석. C1·C4·C5·C9·C10·C3은 "공유하지 않음"으로 바꿀 것을 제안(§3, §5) |
| 새로 본 것 | — | 수집 결과 run tag, probe 사본 세 종류, 관리자 부품 45개 파일 동일 사본, 로컬 경로 정규화 사본 차이, 공용 Dagster instance 설정 공백, Valkey, 빌드 영수증 생산자 fork |

이 문서는 기존 ADR과 task를 고치지 않는다. 기존 계획과 어긋나는 판정은 "제안"으로 적고, 반영은 [T-022](../tasks/T-022-ledger-reality-reconcile.md)(원장 정합)와 ADR 개정이 소유한다.

### 1.4 판정에 쓴 제약

| # | 제약 | 출처 |
|---|---|---|
| R1 | 내부 서비스끼리 서로의 계약을 핀하지 않는다(vendored OpenAPI·SHA 결박 금지). 런타임 검증과 자기 fixture로 대신한다 | 소유자 지시(2026-10-03) |
| R2 | 단순함이 결박보다 우선이다. 강제 계층을 더 쌓지 않는다 | 소유자 지시(2026-09-22); `AGENTS.md` Simplicity First |
| R3 | Manager는 범용으로 유지한다. 렌더링된 모델에서 유도하고 서비스별 리터럴을 넣지 않는다 | 소유자 지시 |
| R4 | npm·PyPI에 게시하지 않는다. 프론트 패키지는 벤더 tarball이다 | [ADR-014](../adr/014-common-implementation-without-registry-publishing.md) |
| R5 | common main의 버전을 하나 바꾸면 모든 소비자의 guard가 재vendor 전까지 실패한다. 이 수단으로 공유하는 비용은 실제다 | 2026-11-17 실측(§2.2) |
| R6 | Map 라이브러리 계층은 `fastapi`·`starlette`를 import하지 않고(`M:pyproject.toml:311-328` ✔) provider adapter·wrapper를 만들지 않는다 | Map ADR-006·ADR-020 |
| R7 | weather·transport는 다른 팀(Codex)이 주로 유지한다. 그 저장소의 채택 비용과 시점은 그 팀이 정한다 | 소유자 지시 |
| R8 | 소비자 한 곳의 관찰만으로 공통으로 올리지 않는다. env 이름·헤더 이름·지표 이름·오류 형식은 배포 계약이다 | `AGENTS.md` §6-7·§6-9 |

## 2. 공유 수단과 비용

### 2.1 지금 쓰는 수단

| 수단 | 쓰는 곳 | 한 번 바꿀 때 | 함대 결합 |
|---|---|---|---|
| A. Python git 커밋 핀 | `P:apps/api/pyproject.toml:9`·`P:apps/etl/pyproject.toml:12`(`c289b46`), `M:packages/kor-travel-map-api/pyproject.toml:31`·`M:packages/kor-travel-map-dagster/pyproject.toml:25`(`aa232ad`), `W:pyproject.toml:15,55`(`aa232ad`), `T:backend/pyproject.toml:11`(`c289b46`) ✔ | 새 기능이 필요한 소비자만 핀 PR 1개 | 없음 |
| A'. 벤더 wheel + hash | `D:docker/dagster-host/vendor/kor_travel_common-0.1.0.dev0-py3-none-any.whl`, `D:docker/dagster-host/requirements.txt:555-556` ✔ | wheel 교체 PR | 없음 |
| B. 벤더 tarball + 중앙 원장 guard | 프론트 7개 표면(`<frontend>/vendor/*.tgz`, `common-artifacts.json`) | **모든** 소비자 재vendor PR. 그 전까지 guard 실패 | 강함 |
| C. 재사용 workflow를 커밋으로 호출 | `frontend-consumer-guard.yml@<sha>` 호출 5곳 | 호출 SHA PR(검사 코드에 한함) | 코드는 없음, 정책 데이터는 B와 같음 |
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
| 조사 시점 | map #1504(파일 12개)·weather #243(파일 14개)은 열려 있음. 두 저장소는 후보 11에 머문다 |

- 재vendor PR 5개, 파일 80개다. geo·concierge도 같은 guard의 소비자이지만 이번에 조회하지 않았다.
- **`ui`·`tokens`·`toast`는 실행 코드와 CSS가 바뀌지 않았다.** tarball이 정책 사본(`dependency-policy.json`)을 싣고 있어서, 무관한 `vworld-map-web` 한 줄 때문에 세 패키지가 patch 버전을 올렸다(common #57 변경 파일 17개 중 패키지 쪽은 `package.json`·`dependency-policy.json`·테스트뿐 ✔; `ui` 0.2.0과 0.2.1 tarball은 같은 94개 파일이고 다른 것은 `package.json`·`dependency-policy.json`·`check-dependencies.mjs` 셋).
- 검사기는 소비자가 선언하지 않은 산출물은 건너뛴다(`check_frontend_dependencies.mjs:145` ✔). 그래서 지도가 없는 docker-manager와 transport 공개 웹은 `vworld-map-web`만 바뀌었다면 영향이 없었다. 두 저장소가 PR을 내야 했던 이유는 위의 내장 사본 때문이다.
- map #1504의 첫 실행은 guard에서 실패했다. 호출 SHA를 최신으로 올리자 map에 없는 정확 Node/npm 도구 규칙이 걸렸고(`도구 규칙: 검사 파일·경로를 읽을 수 없습니다`), 두 번째 커밋이 호출 SHA를 `55a921b`로 되돌렸다 ✔. map은 검사 코드가 44커밋 뒤처진 채(`git rev-list --count 55a921b..97f8ed9` ✔) 정책만 최신을 따른다.
- 한 달 동안 정책 세 파일이 바뀐 날은 나흘(11-11, 11-12, 11-13, 11-17), 커밋 19개다(`git log --since=2026-10-17` ✔).
- common의 11-17 journal은 "기존 소비자는 고정 SHA를 쓰므로 영향이 없다"고 적었고(`C:docs/journal.md`의 후보12 두 항목 ✔), 같은 날 docker-manager의 journal은 "공통 guard는 고정 ref와 무관하게 common main의 정책·정본을 읽으므로" 옛 버전으로는 실패한다고 적었다(`D:docs/journal.md` 첫 항목 ✔). 정책을 바꾸는 쪽도 이 결합을 놓쳤다.

### 2.3 여기서 끌어낸 원칙

1. 새 공통 **코드**는 A(Python 핀)로 갈 수 있으면 A로 간다. 결합이 없다.
2. B로 가는 변경은 **한 번에 묶는다.** 부품 하나마다 버전을 올리지 않는다. 새 artifact 패키지는 만들지 않고 기존 `@kor-travel/ui`의 하위 경로에 넣는다.
3. B를 더 쓰기 전에 B 자체를 고친다(§4.1). 고치기 전에는 프론트 공유를 늘리지 않는다.
4. D(복사)는 소비자 2곳·작은 파일에만 쓰고 강제 검사를 붙이지 않는다(R2).
5. 계약을 건드리는 통합(오류 형식·헤더·지표·env)은 하지 않는다. 필요하면 E(규약)로 새 서비스에만 적용한다.

## 3. 인벤토리

### 3.1 요약 표

칸의 뜻: `●` 구현 있음, `◐` 일부·변형, `○` 공통 구현을 이미 씀, `×` 없음. 판정 뒤의 숫자는 §3.2 이하의 상세 절이다.

| ID | 후보 | P | M | W | T | D | 차이의 핵심 | 판정 |
|---|---|---|---|---|---|---|---|---|
| K-01 | 프론트 중앙 정책 guard(main 정본·단일 버전) | ○ | ○ | ○ | ○ | ○ | 수단 자체의 비용(§2.2) | 지금 공유(수단 수정) §4.1 |
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
| K-30 | geo REST client | ● | ● | ○ common | ○ common | × | 인증 위치·재시도·오류 계약이 다름 | 공유하지 않음 |
| K-31 | 역지오코딩 갱신 glue | × | × | ● | ● | × | 설정 모양만 다름 | 나중에 공유(작게) |
| K-32 | KASI·data.go.kr 호출·분류·재시도 | ● | ● | ● | ● | × | wrapper 금지, 분류는 provider 쪽 문제 | 공유하지 않음 |
| K-33 | 시도·행정코드 표 | ● | ● | ● | ● | × | 정본 방향이 다르고 2026 통합시 처리가 네 가지 | 나중에 공유(결정 선행) |
| K-34 | 좌표·bbox·haversine·한국 경계 | ● | ● | ● | ● | × | 상수가 정당하게 다름 | 공유하지 않음 |
| K-35 | 시간(KST) 헬퍼(C13) | ● | ● | ● | ● | ● naive | 저장소 안 중복이 더 큼 | 나중에 공유(낮음) |
| K-40 | 수집 결과 run tag | × | × | ● | ● | × | 함수 동일, 두 관리자 UI가 읽음 | 지금 공유 §3.4 |
| K-41 | 다중 job 인프라 재시도 sensor | ◐ job당 1개 | × | ○ | ◐ job당 1개 | — | 공통 구현 미채택 | 지금 공유(채택 공백) §3.4 |
| K-42 | 회수 sensor의 소비자 cursor·정체 시계 | × | ◐ 자체 | ◐ | ◐ | — | 공통 API 공백을 각자 우회 | 나중에 공유 §3.4 |
| K-43 | Dagster webserver 정의 로드 probe | ● | ● | ◐ | ● | ● ×4 | 같은 한 줄 7곳 | 나중에 공유 §3.4 |
| K-44 | code-server probe 세 세대 | — | ○ | ○ | ● 사본 | ● | 재시작 책임이 미정 | 나중에 공유(결정 선행) |
| K-45 | Map coalescing schedule | ○ | ● 자체 | ○ | ○ | — | 범위 판정 방식이 다름 | 나중에 공유 |
| K-46 | 공용 `dagster.yaml`의 job별 한도·`run_retries` | — | — | — | — | ● | 가이드가 요구한 규칙이 없음 | 나중에 공유(Manager 결정) |
| K-47 | Definitions 골격·schedule on/off·실패 sensor | ● | ● | ● | ● | — | 도메인 결선 | 공유하지 않음 |
| K-48 | 적재·수집 run 원장 | × | ● | ● | ● | — | 스키마가 도메인 | 공유하지 않음 |
| K-49 | standalone `dagster.yaml` 사본 | ● | ● | ● | ● | ● | 로컬 스택에 필요 | 공유하지 않음 |
| K-50 | 관리자 공통 부품 묶음 | ◐ 재도색 | ● | ● 동일 | ● 동일 | ◐ | 45개 파일 byte 동일 ×3 | 나중에 공유(한 번에) §3.5 |
| K-51 | 로컬 경로 정규화(`sanitizeLocalPath`) | × | × | ● | ● | × | 사본 세 벌, W 서버 쪽 사본에 검증 하나가 없음 | 지금 공유(채택 공백) §3.5 |
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

집계: 지금 공유 8, 나중에 공유 24, 공유하지 않음 29(합 61).

### 3.2 백엔드

**K-11 app factory·lifespan — 공유하지 않음.** `P:apps/api/app/main.py:50-127`, `M:api/app.py:769-1463`, `W:wapi/app.py:130-347`, `T:app/main.py:516-3732`, `D:kdm/main.py:174-244`. 코드 수준에서 같은 것이 없다. 문서 노출은 넷이 다르고(P 항상, M은 production에서 `/docs`만 끔 `api/app.py:827-828`, T는 `openapi_url`까지 `app/main.py:630-632`), 미들웨어 순서와 시작 시 fail-closed 검사도 저장소마다 다르다. 공통 factory는 일부러 다르게 둔 다섯 계약 위에 결박층을 하나 더 얹는다(R2).

**K-12 settings 베이스 — 공유하지 않음.** `P:apps/api/app/core/config.py:644-651`, `M:lib/settings.py:42-72`·`M:api/settings.py:380-395`, `W:wlib/settings.py:77,168-179`, `T:app/core/config.py:11-24`, D는 settings 클래스가 없다(`os.environ` 자리 66곳). compose의 `${X:-}`가 만드는 빈 문자열을 넷이 다르게 다룬다: M core는 `env_ignore_empty=True`(`lib/settings.py:71`), M api는 필드별 validator(`api/settings.py:767-800`), P는 토큰 필드 10개 validator(`config.py:1436-1463`)이고 공백은 남겨 뒤에서 거절, W는 13개 필드에서 공백까지 미설정으로 본다(`wlib/settings.py:664-684`), T는 없다. profile 기본값도 반대다(W `production` `wlib/settings.py:183`, M code 기본 `local-dev` `api/settings.py:412-414`). 공통 베이스는 P·W·T의 빈 env 의미를 조용히 바꾼다. 나중에 쓸 만한 것은 `mode="before"` validator로 쓰는 순수 함수 둘뿐이다(저장소당 10~25줄).

**K-13 DB 엔진 팩토리 — 공유하지 않음.** `P:apps/api/app/db/session.py:23-44`, `M:lib/infra/db.py:829-954`, `W:wlib/repository.py:1392-1416`(sync psycopg), `T:app/db/session.py:28-92`, `D:kdm/database.py:15-114`(SQLite). 드라이버가 셋이고 호출 모양이 다르다. `statement_timeout`·`lock_timeout`은 엔진마다 값과 단위가 다르고 각각 사고 기록에 묶여 있다. 저장소 **안**의 중복은 따로 정리할 만하다: Map Dagster의 같은 `server_settings` 리터럴 6곳(`M:dag/file_registry_hooks.py:93,140`, `file_registry_scan.py:109`, `manual_provider_dedup.py:77`, `resources.py:1317`, `runtime_preflight.py:23` ✔), transport의 DSN 정규화 2곳(`T:app/db/session.py:43-46`, `T:backend/alembic/env.py:29-32`).

**K-14 Alembic env·런타임 롤 — 공유하지 않음.** `P:apps/api/alembic/env.py`(89줄), `M:alembic/env.py`(261줄), `W:alembic/env.py`(47줄), `T:backend/alembic/env.py`(73줄), D는 없다. P와 M은 같은 위험을 반대로 다룬다: P는 `configure` 전에 SQL을 실행하고 명시 commit으로 보정한다(`env.py:52-54,75-78`). M은 `configure` 전 `execute()`가 commit을 건너뛰게 한다고 적고 `SET ROLE`·`search_path`를 `begin_transaction()` 안에 둔다(`env.py:187-222`). 템플릿은 둘 중 하나를 골라야 한다. 롤 이름·스키마 이름·제외 목록·lock 키는 DB별 계약이다. 남길 것은 규약 한 줄("`configure()` 전에 `execute()`하지 않는다. 한다면 명시 commit")이다.

**K-15 health 라우터 — 공유하지 않음.** `P:apps/api/app/api/v1/healthz.py:31-53`, `M:api/routers/public_status.py:60-90`·`M:api/routers/ops.py:334-360`, `W:wapi/app.py:198-208`, `T:app/main.py:854-862`, `D:kdm/main.py:398-400`. 같은 것은 경로 `/health`뿐이다. 본문이 다르고(`status`는 넷이 `ok`, D는 `healthy`; 커밋 키는 `git_sha`·`commit`·`git_commit`·`release_sha`), T의 `/health`는 DB가 죽으면 실패하지만 M은 반대 선택을 문서로 남겼다(`public_status.py:4-6`). 본문은 각 OpenAPI 산출물의 일부여서 공통 라우터는 모든 소비자의 산출물을 바꾼다. 공유할 것은 **probe 쪽**이다(K-10).

**K-16 OpenAPI export — 나중에 공유(작게).** `M:packages/kor-travel-map-api/scripts/export_openapi.py`(527줄), `W:packages/kor-travel-weather-api/scripts/export_openapi.py`(27줄), `T:scripts/export_openapi.py`(60줄) ✔. P·D는 없다. 같은 것은 `json.dumps(app.openapi(), indent=2, ensure_ascii=False)` 한 줄이다. M·T는 `sort_keys=True`(`export_openapi.py:438`, `:42` ✔), W는 없다(`:21` ✔). M은 끝 개행 없이 `.strip()` 비교, T는 개행을 쓰고 정확 비교, W는 스크립트 안 비교가 없고 CI가 `git diff`로 본다. 공유할 수 있는 부분은 25줄 정도의 `dump`·`check_or_write`인데, 직렬화를 맞추면 커밋된 산출물이 한 번 다시 써지고 그 사본을 가진 쪽이 따라 움직인다. 줄 수 이득보다 비용이 크다. 값싼 독립 개선은 W에 `sort_keys=True`를 넣는 것이다.

**K-17 인증 프리미티브 — 나중에 공유.** 공개 API 키 생성·해시 함수는 `M:lib/infra/public_api_keys.py:86-96`과 `D:kdm/services/public_api_key_service.py:20-27`이 본문까지 같다 ✔(길이 32, `ascii_letters+digits`). 그 밖은 정책이다: 키 전달(M은 헤더만, D는 query), 조회(M은 TTL 캐시, D는 요청마다 조회), 실패 코드(M 401/403/422, W 401, T·P 일부 404로 표면 은닉), 미설정 시 동작(M 미강제, W production에서 예외, T는 32자 미만이면 닫힘 `app/main.py:708`), proxy 신뢰(넷 다 다르고 IPv4-mapped 정규화는 T만 `app/service_exports.py:298-299`). 작은 `secrets` 모듈(바이트 안전 상수시간 비교, 키 생성·해시, CIDR 판정)은 저장소당 10~25줄을 지운다. D의 백엔드는 common에 의존하지 않고(Poetry) 이 이득으로 의존을 새로 만들 이유가 없다. [T-312](../tasks/T-312-auth-core-primitives.md)가 이미 이 범위를 갖고 있으므로 새 task를 만들지 않는다.

**K-18 outbound HTTP — 공유하지 않음.** 재시도 루프는 다섯 저장소 모두 손으로 쓴 것이고 서로 다르다. P는 client마다 `0.2·2^n`과 3회 실패·120초 circuit(`P:apps/api/app/clients/_resilience.py:18-61`), M은 실행 단위 예산(`M:dag/upstream_retry.py:102-117`)과 geo에 502/503/504만 선형 backoff(`M:lib/geocoding.py:1579-1611`), W는 thread를 재우는 sync(`W:wlib/providers/base.py:346-451`), T는 provider 라이브러리에 맡긴다. 재시도·circuit은 호출 자리의 결정이다. 공통 `bounded_request`를 쓰는 곳은 둘뿐이다(`M:api/dagster_graphql.py:915`, `P:apps/api/app/services/admin_etl.py:670` ✔). M의 `_read_capped`(`M:api/transport_state_service.py:231-255` ✔)는 gzip을 허용하고 공통은 모든 압축을 거절한다(`C:cpy/http.py:66-68` ✔). 소비자가 한 곳이라 공통 옵션으로 올리지 않는다(R8). P의 `tenacity` 선언은 import가 없다(`P:apps/api/pyproject.toml:23` ✔).

**K-19 오류 envelope — 공유하지 않음.** P `{"error":{code,message,details}}`(`P:apps/api/app/core/errors.py:25-76`), M problem+json에 `code`·`request_id`·`errors[]`(`M:api/app.py:619-691`), W problem+json(`type="about:blank"`, `W:wapi/app.py:110-127`), T problem+json에 `instance`만(`T:app/main.py:636-689`), D `{detail}`(`D:kdm/main.py:341-395`). 같은 상태의 기본 코드도 다르다(401: P `TOKEN_INVALID`, M `UNAUTHORIZED`). 프론트와 형제 client가 이 형식을 읽는다. 통합은 세 저장소 이상의 파괴적 변경이다.

**K-20 cursor 코덱 — 나중에 공유(코덱만).** `M:api/routers/curation_snapshots.py:216-231`과 `W:wlib/export_snapshots.py:263-300`은 같은 알고리즘이다(정렬·압축 JSON 뒤에 HMAC-SHA256 32바이트, base64url, padding 제거 ✔). T는 다른 배치 둘(`T:app/services/export_price_history.py:44-62`, `T:app/main.py:2504-2545`), P는 서명이 없다. 키 출처(M 전용 secret, W 관리자 토큰 파생, T `database_url` 파생), 이름(`page_size` 대 `limit`), meta(`next_cursor` 대 `cursor`+`has_more`)는 계약이라 합치지 않는다. 발급된 cursor는 배포를 넘어 살아야 하므로 코덱을 바꾸면 기존 cursor가 죽는다. 새 cursor에만 쓸 fastapi 무의존 `sign`·`verify`는 자리당 15~20줄이다. 기존 [T-508](../tasks/T-508-deferred-items-reevaluation.md)의 재평가 항목으로 남긴다.

**K-21 rate limit — 공유하지 않음.** 일반 limiter는 P 하나다(`P:apps/api/app/middleware/rate_limit.py`, 757줄, memory·Postgres backend). W·D는 로그인 한정, T는 상류 보호다. Valkey 기반은 어디에도 없다. 지워질 줄이 다른 저장소에 없다.

**K-22 Valkey·cache — 공유하지 않음(지금).** client는 `M:lib/infra/valkey_state.py`(1,244줄) 하나다. generation 교체 저장소이지 범용 cache가 아니다. P는 Valkey 상태를 Map의 HTTP로 읽는다. 두 번째 서비스가 Valkey 의존을 가질 때 `make_valkey_client`와 오류 매핑(약 45줄, `valkey_state.py:492-537`)을 다시 본다.

**K-23 request-id 미들웨어 — 나중에 공유.** P·M·W는 들어온 `X-Request-Id`를 길이·문자 검사 없이 신뢰한다(`P:apps/api/app/middleware/request_id.py:14-34`, `M:api/response.py:116-137`, `W:wapi/app.py:64-107`). D는 일부러 신뢰하지 않는다(`D:kdm/main.py:263-272`). T는 없다. `trust_incoming` 옵션과 길이·문자 제한을 가진 pure-ASGI 미들웨어는 M·W·P에서 20~35줄씩 지우고 T에 하나를 준다. starlette extra 뒤에 둬야 Map 라이브러리가 깨끗하다(R6). 기존 [T-307](../tasks/T-307-request-id-and-metrics.md)에서 **지표와 분리해** 진행하도록 T-022에서 정리한다.

**K-24 지표·로깅·redaction — 공유하지 않음.** 접두 `pinvi_api_`·`kor_travel_map_`·`ktw_`·`ktdm_`, 라벨 `route` 대 `path`, `status_code` 대 `status_class`, registry 방식이 다 다르고 대시보드와 경보가 그 이름에 묶여 있다. redaction은 전략이 넷이다(P 이름 정규식 `***`, W 키 이름 `[REDACTED]`, T·D 값 치환 `<redacted>`). 각자 자기 누출 표면과 문서화된 잔여 위험을 갖는다. 이름 목록을 합치면 각 저장소가 놓치는 것이 바뀐다.

### 3.3 probe와 도메인 헬퍼

**K-10 HTTP 생존 probe — 지금 공유(채택 공백).** 공통 `python -I -m kortravelcommon.http_health`(loopback, 헤더만, 전체 4초, shell 없음)를 이미 쓰는 곳: `W:compose.yaml:158`, `T:docker-compose.yml:100`, `T:docker-compose.shared.yml:274`, `D:docker-compose.yml:2998-3008`(weather-api) ✔. 아직 shell 형식인 곳: Map API의 인라인 `python -c urllib`(`M:docker-compose.yml:513-518` ✔, 같은 문장이 `D:docker-compose.yml:1738-1741` ✔), PinVi API의 `curl`(`D:docker-compose.yml:2204-2207` ✔). 두 API 이미지는 이미 `kor-travel-common[http]`를 설치하고 두 핀 모두 `http_health.py`를 갖는다(`git ls-tree` ✔). 남은 두 곳은 shell을 거치는 형식이고, 공통 probe는 exec 형식으로 큰 client·프레임워크 import 없이 한 예산 안에서 끝난다([http-health-probe](../runbooks/http-health-probe.md)). PinVi Dockerfile의 probe는 세 엔드포인트를 묶은 것이라(`P:apps/api/Dockerfile:99-102` ✔) 한 경로만 보는 공통 probe로 바꾸지 않는다. 이득: shell 형식 2종과 `curl` 의존 제거. 비용: compose 몇 줄. 위험: 이미지에 모듈이 없으면 재구축이 `compose up`에서만 죽는다. 그래서 채택 전에 고정 이미지에서 모듈 존재를 확인한다(§4.4).

**K-30 geo REST client — 공유하지 않음.** `P:apps/api/app/clients/kor_travel_geo.py:51-273`과 `M:lib/geocoding.py:1454-1745`. 인증 위치(P query `?key=`, M 헤더 `X-KTG-API-Key`), 요청 어휘, timeout(5초 대 read 10·connect 4초), 재시도(P는 모든 timeout과 5xx, M은 502/503/504만이고 connect 실패는 절대 재시도하지 않음), 실패 계약이 다르다. P는 사용자 요청이라 circuit 뒤에서 빨리 실패하고, M은 배치라 호출 수를 센다. 하나로 합친 client는 Map이 금지한 wrapper이고(R6) 두 서비스를 한 계약 해석에 묶는다(R1). W·T는 Python에서 geo를 부르지 않고 공통 역지오코딩을 쓴다.

**K-31 역지오코딩 갱신 glue — 나중에 공유(작게).** `W:wlib/address_refresh.py:1-62`와 `T:app/services/address_refresh.py:1-79`. `configured()`는 동일하고 호출 모양도 같다. 다른 것은 설정 모양(W는 `SecretStr`과 repository, T는 `str`과 5개 테이블 union·좌표 필터·FerryPort 제외)이다. `(select, settings)`를 받는 공통 factory는 W 30줄·T 25줄을 지운다. 두 저장소 모두 다른 팀 소유라 그 팀이 정한다(R7).

**K-32 KASI·data.go.kr — 공유하지 않음.** 호출은 넷 다 provider 라이브러리의 공개 client를 직접 쓴다(R6). 한도 분류는 저장소마다 다르고(M은 `failure_kind` 속성과 429 제외 `M:dag/quota_exhaustion.py:95-209`, W는 `failure_kind=="quota"`만 일일 한도 `W:wdag/definitions.py:630-638`, T는 문자열 표식 `T:app/services/collection.py:40,356-371`), 원인은 provider 라이브러리 절반에 `failure_kind`가 없다는 것이다. 고칠 자리는 상류다. 같은 라이브러리의 핀이 저장소마다 다른 것은 별도 사실이다(kasi: P `bc8fd49`·T `4259e57`; khoa: M `38a2b74`·W `9c952bb`; krforest: M `70814c9`·W `270ef7a`; krex: W `0fc9da9`·T `af045fa`; datagokr: M `6150932`·T `18864a3` ✔). 정렬 주체는 열린 결정 O-16이며 [T-505](../tasks/T-505-shared-library-marker-palette-request.md)·[T-506](../tasks/T-506-quarterly-drift-audit.md)이 소유한다.

**K-33 시도·행정코드 표 — 나중에 공유(결정 선행).** `P:apps/api/app/services/korea_regions.py:20-140`, `M:lib/core/curation_address.py:27-81`·`M:lib/core/search_region.py:63-139`, `W:wlib/alert_area_mapping.py:15-55`, `T:app/services/place_locations.py:28-40`. 방향이 다르다(P는 코드→약칭, M 큐레이션은 별칭→현재 정식명, M 검색은 DB 표본에서 유도, T는 접두 일치). 2026 `전남광주통합특별시`를 네 가지로 다룬다: M 큐레이션은 `전라남도`(`curation_address.py:67`), M 검색은 `전남`·`광주` 둘 다(`search_region.py:80`), T는 `전남`(`place_locations.py:31`), P·W TS는 항목이 없다. 17개 시도의 데이터 전용 표(현재 코드·옛 코드·정식명·약칭·별칭)는 P 40줄·M 50줄·T 13줄을 대신할 수 있지만 정본 방향과 통합시 처리가 먼저 정해져야 한다. Map 라이브러리는 common에 의존하지 않으므로(`git grep kortravelcommon -- src` 빈 결과 ✔) 새 의존에는 Map ADR이 필요하다. W의 특보 구역 매핑과 M의 검색 토큰은 이 표와 별개로 남는다.

**K-34 좌표·bbox·haversine·한국 경계 — 공유하지 않음.** 지구 반지름이 넷이다(6,371,000 / 6,371,008.8 / 6,371.0km / 6,372,797.560856). `M:api/routers/service_transport.py:91-92`는 Valkey GEO와 맞춰야 하고 `T:app/services/fuel_search.py:18`은 응답 필드로 공개돼 있다(`T:app/schemas.py:94`). 위도 경계도 질문이 다르다(입력 검증 33–43, 서비스 영역 33–39.5, provider 구제, transport 적재 32–39.5). 2026-09 판정("좌표 경계 상수 공통화 금지")을 값으로 다시 확인했다. 지울 수 있는 줄은 저장소 **안**에 있다(P haversine 5벌 약 25줄, M 약 15줄).

**K-35 시간 헬퍼 — 나중에 공유(낮음).** `P:apps/api/app/core/time.py:11-19` ✔, `M:lib/dto/_time.py:36-92` ✔, `W:wlib/models.py:20,324-325` ✔(고정 오프셋), `T:app/core/time_utils.py:7-85` ✔, `D:kdm/_time.py:4-11` ✔(naive UTC). `kst_now()`는 뜻이 같지만 W의 tzinfo 타입이 다르고, naive 값은 셋으로 갈린다(거절, KST 가정, UTC 가정). 공유 대상은 15줄이고 저장소당 10줄을 지운다. Map 라이브러리가 그 때문에 새 의존을 가져야 한다. 더 큰 이득은 저장소 안 정리다(M 고정 오프셋 KST 6곳, P 흩어진 상수 5곳, W 정의 2곳). [T-304](../tasks/T-304-health-and-time.md)의 time 절반으로 남기되 우선순위를 낮출 것을 제안한다.

### 3.4 Dagster

**K-40 수집 결과 run tag — 지금 공유.** `_record_collection_outcome`은 `W:wdag/definitions.py:399-418`과 `T:app/dagster/definitions.py:60-79`에서 본문이 같다(`suppress` 대 `contextlib.suppress` 한 줄 차이 ✔). tag `kortravel/collection-outcome`은 두 관리자 프론트가 읽는다(`W:WA/lib/dagster.ts:222`, `W:WA/components/dagster-console.tsx:86`, `T:TA/components/dagster-console.tsx:86` ✔). 사실상 저장소 사이 계약인데 정의가 두 곳에 있다. 이득: 정의 한 곳, 각 20줄 제거, 세 번째 소비자가 같은 값을 쓴다. 비용: common 함수 하나와 핀 PR 둘. 위험: 낮다(동작 보존, A 수단). 채택은 두 저장소의 유지 팀이 한다(R7).

**K-41 다중 job 인프라 재시도 sensor — 지금 공유(채택 공백).** 공통에 `infrastructure_retry_sensor_for_jobs`가 있다(`C:cpy/dagster.py:331` ✔). W는 쓴다. P는 job마다 sensor를 5개(`P:etl/definitions.py:88-97` ✔), T는 3개 만든다(`T:app/dagster/definitions.py:1041-1048` ✔). 하나로 합치면 실패 조회가 한 번이 되고 sensor tick 수가 준다. 비용: 저장소당 6줄 안팎. 위험: sensor 이름이 바뀌어 기존 sensor의 cursor·상태가 새로 시작한다. 채택 PR이 이 전환을 다뤄야 한다.

**K-42 회수 sensor의 소비자 cursor — 나중에 공유.** 공통 `reconciliation_sensor`가 sensor cursor를 소유해서, W와 T는 keyset 위치를 프로세스 메모리에 둔다(`W:wdag/sync_recovery.py:97-116` ✔, `T:app/dagster/recovery.py:206-223` ✔). W는 공통의 비공개 cursor 접두 `stall:`을 직접 다시 읽는다(`W:wdag/sync_recovery.py:64-65,119-127` ✔, 원본 `C:cpy/dagster.py:69` ✔). 비공개 형식에 묶인 것이라 공통이 형식을 바꾸면 조용히 깨진다. callback이 현재 정체 시계를 받고 작은 하위 cursor를 저장할 수 있게 공통 API를 넓히면 W 30줄·T 20줄이 준다. Map의 회수 sensor(`M:dag/feature_operation_sensors.py`)는 30초 주기·`RunRequest` 반환·시계 둘이 필요해 factory에 맞지 않는다. 의도된 불일치이므로 옮기지 않는다.

**K-43 webserver 정의 로드 probe — 나중에 공유.** `{repositoriesOrError{__typename}}`을 보내 `RepositoryConnection`인지 보는 한 줄이 7곳에 있다: `D:docker-compose.yml:2013,2432,2791,3259`, `M:docker-compose.yml:778`, `T:docker-compose.shared.yml:378`, `P:apps/etl/Dockerfile:98-102`(curl+grep) ✔. 공통에는 webserver probe가 없다. 운영은 Manager의 공용 webserver가 workspace를 읽는 별도 probe를 쓰므로(`D:docker-compose.yml:990-1010`) 이 사본들은 standalone·legacy 스택의 것이다. 그래서 이득이 작다. 공통 CLI 하나(`dagster_webserver_health`)는 만들 가치가 있으나 급하지 않다.

**K-44 code-server probe 세 세대 — 나중에 공유(결정 선행).** (1) Manager의 93줄 인라인 probe(`D:docker-compose.yml:103-196`)가 `T:docker-compose.shared.yml:118-211`에 그대로 복사돼 있고 ✔ 전환 스크립트가 일치를 강제한다. 이 probe는 PID 1에 SIGTERM을 보내고 고아 run을 거둔다. (2) `kortravelcommon.dagster_health`(`M:docker-compose.yml:675-681`). (3) `kortravelcommon.grpc_health --check live`(`W:compose.yaml:301`, `D:docker-compose.yml:2707,3155`). geo·weather 쪽 주석은 "PID 종료·DB reaper는 healthcheck 책임이 아니다"라고 적는다. (3)으로 모으면 T의 94줄과 D의 약 150줄이 준다. 그러나 멈춘 자식을 누가 다시 띄우는가가 먼저 정해져야 한다. 읽기 전용 대체물 `C:cpy/dagster_recovery.py`를 결선한 곳은 W뿐이다. Manager와 유지 팀의 결정이다.

**K-45 Map coalescing — 나중에 공유.** `M:dag/schedules.py:583-613` ✔은 공통 `coalescing_schedule`(`C:cpy/dagster.py:177` ✔)과 세 가지가 다르다: `NOT_STARTED`·`MANAGED`도 센다(`schedules.py:70-77` ✔), DB에서 `kor_travel_map.operation_key` tag로 좁힌다, `execution_fn`으로 `RunRequest`/`SkipReason`을 돌려준다. 공통이 tag 범위를 받거나 Map이 origin 범위를 받아들여야 옮길 수 있다(약 40줄).

**K-46 공용 `dagster.yaml` — 나중에 공유(Manager 결정).** 공용 instance 설정에는 `run_retries` 블록이 없고 `kortravelcommon/job`의 값별 한도가 없다. 그 key는 concierge 값 다섯 개의 리터럴로만 있다(`D:config/dagster-shared/dagster.yaml:96-110` ✔). standalone 사본 셋(P·W·T)에는 값별 한도가 있다. 공통 가이드는 daemon 소유 저장소에 그 규칙을 두라고 한다([dagster-adoption](../runbooks/dagster-adoption.md) §3). 호스트 override 렌더러는 한도의 `value`가 문자열이어야 통과시키므로(`D:kdm/services/shared_dagster_instance.py:92-96` ✔) dict 값(`applyLimitPerUniqueValue`)을 지금은 거절한다. 일반 규칙 하나가 리터럴 다섯을 대신하고 R3에 맞는다. 그러나 **모든** tenant의 job이 동시 1개로 묶인다. Map은 queue sensor가 한 tick에 여러 run을 낸다. 그 run들이 같은 job tag를 갖는지 먼저 확인해야 한다. 운영 동작을 바꾸므로 Manager의 결정 task로 둔다.

**K-47·K-48·K-49 — 공유하지 않음.** Definitions 조립·resource 결선·schedule on/off(M은 코드 상수와 DB override `M:dag/schedules.py:661-667` ✔, W는 env로 sensor 등록, T는 `SCHEDULER_MODE`)는 도메인이다. 같은 것은 `multiprocess_executor.configured({"max_concurrent": 1})` 한 줄이다. run 원장(`ops.import_jobs`, `weather_sync_runs`, `collection_runs`)은 스키마가 도메인이고 서로의 테이블을 핀하면 안 된다(R1). standalone `dagster.yaml`은 로컬 스택에 있어야 한다.

### 3.5 프론트엔드

**K-50 관리자 공통 부품 묶음 — 나중에 공유(한 번에).** MA·WA·TA 세 프론트에 **45개 파일(2,076줄)이 byte 단위로 같다** ✔(`cmp -s`로 다시 셈). `components/ui/*` 30개와 `confirm-dialog`·`copy-button`·`detail-list`·`empty-state`·`json-viewer`·`pagination-bar`·`stat-strip`·`status-badge`·`status-badge-variants`, `lib/{format,occurrence-key,string-list,utils}.ts`, `app/error.tsx`·`app/global-error.tsx`다. MA=WA만 같은 파일이 9개(1,317줄: `app-error-panel`·`filter-bar`·`section-card`·`selectable-row`·`multi-filter-combobox`·`lib/error-recovery.ts` 등) 더 있고 TA 쪽은 조금 다르다. 표류가 이미 보인다: `help-tip.tsx`는 W·T가 M보다 새 판이다. PW 관리자는 같은 묶음을 일부러 다시 칠한 이식본이다(약 2,330줄). [ui-contract](../standards/ui-contract.md) §4는 이 부품들(`EmptyState`·`StatStrip`·`StatusBadge`·`DetailList`·`JsonViewer`·`CopyButton`·`AppErrorPanel`·`HelpTip`·`FormField*`·`AdminPageHeader`·`AdminSkipLink`)을 계약으로 적었지만 `packages/ui/src`에는 없다 ✔. 같은 문서는 엔진을 `@base-ui/react`라고 적는데(`ui-contract.md:19,32` ✔) 실물은 `radix-ui`다. 기존 task T-203·T-205·T-209·T-210이 이 범위다. 이득: M·W·T에서 각 1,100~1,300줄, PW 관리자가 토큰 이름 매핑을 받아들이면 600~900줄. 비용: 클래스가 로컬 어휘(`text-text-secondary`, `rounded-control`)라 파일 이동이 아니라 이식이다. 그리고 `ui` 버전이 오르므로 함대 전체가 재vendor한다. 그래서 **한 버전으로 묶고**, §4.1의 전환 창이 생긴 뒤에 낸다. `status-label.ts`는 도메인 사전이라 앱에 남는다.

**K-51 로컬 경로 정규화(`sanitizeLocalPath`) — 지금 공유(채택 공백).** `@kor-travel/ui/navigation`이 `sanitizeLocalPath`를 내보낸다(`C:packages/ui/src/navigation.ts` ✔). W와 T는 client에서는 그것을 import하면서 서버 쪽에는 로컬 사본을 둔다(`W:WA/lib/navigation.ts` ✔, `T:TA/lib/navigation.ts` ✔). 같은 규칙이 세 벌이다. weather의 서버 쪽 사본에는 다른 두 사본에 있는 검증 하나가 빠져 있어 맞춰야 한다. 사본을 공통 export 하나로 바꾸면 다시 갈라지지 않는다. 패키지 변경이 없어 함대 비용이 0이다. 차이점: 공통 함수는 `fallback` 인자가 없고 로컬 사본보다 거절 범위가 넓다. 호출부가 맞춰야 한다.

**K-52 관리자 셸 조각 — 나중에 공유(K-50과 함께).** 다섯 관리자 표면 모두 nav를 공통 `AppMenu`로 그린다. 남은 로컬 셸(`M:MA/src/components/admin-shell.tsx` 556줄, `W:WA/components/admin-shell.tsx` 512줄, `T:TA/components/admin-shell.tsx` 254줄, `P:PW/app/(admin)/admin/layout.tsx`, `D:DM/src/components/layout/AppShell.tsx`)에서 같은 것은 skip link 문구와 접힘 저장 방식 정도다. nav 내용·권한·로그아웃 전송은 앱 소유다(`ui-contract.md:144`). skip link·header 띠·접힘 hook은 그것만으로 재vendor할 값이 안 된다. K-50의 버전에 싣는다.

**K-53 Next 계층 세션·로그인 crypto — 공유하지 않음.** `M:MA/src/lib/auth.ts`(554줄)와 `W:WA/lib/session.ts`(549줄)는 payload 모양·8시간 TTL·PBKDF2 310,000회·10분 5회 제한이 같지만 글자로 같은 줄은 97줄뿐인 재구현이다. 폐기 저장소(M 프로세스 메모리, W 백엔드, T 없음), 신뢰할 수 없는 proxy 헤더일 때의 제한 키, `Origin` 누락 처리, `secure` 규칙이 다 다르다. T는 PBKDF2가 없다(`T:TA/lib/session.ts:26-28`). 2026-09의 "상수 일치" 관찰은 M·W·D에서만 맞다. 공통 보안 모듈은 함대 전체의 결합이 된다.

**K-54·K-55 — 공유하지 않음.** API client는 오류 형식 넷과 인증 모델 셋 위에 있다(`M:MA/src/api/client.ts` 711줄, `P:packages/api-client/src/client.ts` 469줄 등). 공통 fetch wrapper는 앱당 60줄을 아끼려고 그것들을 추상화해야 한다. 타입 생성은 M만 `openapi-typescript`를 쓰고 P는 zod다. 형제 서비스의 OpenAPI를 벤더한 프론트는 없다(R1에 맞는 현 상태). `validateForm`은 M(규칙 기반)과 P(zod 기반)가 이름만 같다. `format.ts` 63줄은 M·W·T가 같고 K-50과 함께 간다.

**K-56 토큰 브리지 — 나중에 공유(기존 task).** D와 TP에는 `--kt-*` 정의가 없다(`git grep -- '--kt-'` 빈 결과). 공통 부품은 공통 기본 브랜드 색을, 로컬 화면은 앱 팔레트를 쓴다. 렌더링 결과는 확인하지 않았다. 기존 [T-472](../tasks/T-472-ktdm-tokens-adoption.md)·[T-431](../tasks/T-431-airport-tokens-adoption.md)이 이 범위다. M·T의 140줄 `@theme inline` alias 블록은 같고 K-50의 부품이 그 이름으로 쓰여 있어 함께 다룬다.

**K-57 Dagster 운영 콘솔 — 나중에 공유(T-216).** 공통 `DagsterOperations`는 M·P가 쓴다. 그 뒤에 나온 상세·액션 콘솔은 W와 T에 같은 파일로 있다(`components/dagster-console.tsx` 302줄, `lib/dagster-console-{client,model}.ts` ✔; `lib/dagster-failure-diagnostics.ts`는 6줄 차이 ✔). 진행 중인 [T-216](../tasks/T-216-dagster-operations.md)이 흡수할 대상이다.

**K-58 `map-marker-react` — 나중에 공유.** `T:TA/lib/vendor/map-marker-react/`는 `M:packages/map-marker-react/src/`의 사본이다(`index.ts`·`marker.ts`·`palette.ts` 동일, `maki.ts` 주석 한 줄 차이 ✔, 원본 커밋과 라이선스를 README에 기록). 소비자가 둘이고 파일이 작아 지금의 "출처를 적은 복사"로 충분하다. 세 번째 소비자가 생기거나 표류가 동작 차이가 되면 K-50의 버전에 `@kor-travel/ui` 하위 경로로 옮긴다.

**K-59 maplibre worker 복사·키 판정 — 나중에 공유(상류).** `scripts/copy-maplibre-worker.mjs`가 네 벌이다(P 49줄, M 43줄, W 28줄, T 44줄 ✔). VWorld 키 미설정 판정도 셋이 다르다. 자연스러운 자리는 `vworld-map-web` tarball이고 그 버전을 올리면 함대가 재vendor한다. 다음 정기 갱신에 싣는다. 요청 문서는 기존 T-505가 소유한다.

**K-60 지도 작업면 채택 — 공유하지 않음(기존 보류 유지).** W·T는 `MapWorkspace`·`MapStage`·`MapFilterPanel`을 쓰고 M의 `/features`는 쓰지 않는다. Map은 이것을 `T-UI-MAPWORKSPACE`로 보류해 뒀다(`M:docs/tasks.md:122` ✔: 고정 70dvh 지도 영역과 698px e2e 기준을 다시 설계해야 함). 다시 제안하지 않는다.

**K-61~K-65 — 공유하지 않음(K-64는 나중에).** 팔레트 코드 `P-01`은 M에서 `#1f77b4`, P에서 `#E53935`다(`M:packages/map-marker-react/src/palette.ts:38`, `P:packages/design-tokens/src/colors.ts:55` ✔). 같은 코드로 공유하면 한쪽 색이 조용히 바뀐다. 클러스터는 데이터 모양에 묶여 네 구현이다. e2e는 저장소별 운영 gate다. 다만 W·T 사이에는 같은 파일이 있다(`e2e/fixtures/native-delay-proxy.mjs` 동일, `address-refresh.spec.ts`는 기본 포트 한 줄 차이 ✔). 그것은 두 저장소 안의 정리다. vitest 설정은 9~33줄이고 중복은 import 한 줄이다. ESLint는 plugin 묶음 다섯·a11y 심각도 셋이 의도적이라 preset은 나중 일이다. doctor 플래그 한 줄은 [frontend-stack](../standards/frontend-stack.md)에 적는 것으로 충분하다.

### 3.6 Ops·CI

**K-70 Node CI job 골격 — 나중에 공유.** setup-node 22.23.1 → `npm install --global npm@12.0.1` → `npm ci --engine-strict` → 검사·빌드 순서가 W·T(2개 job)·D에서 같은 모양이다. P·M은 workspace 루트 설치라 모양이 다르다. main을 읽지 않는 재사용 workflow를 커밋으로 호출하면 함대 결합이 없다(수단 C). 기존 [T-401](../tasks/T-401-reusable-workflows-quality.md)의 `node-quality.yml`이 이 범위다.

**K-71·K-72 — 공유하지 않음.** Python 설치가 넷이고(uv 고정, uv 미고정, pip+constraints, pip+정확 핀) format은 P만 강제하고 mypy는 M·P만 돌린다. 공통 ruff·mypy 베이스는 Map을 다시 포맷·lint하게 하거나 T에 새 강제를 얹는다(R2, R7). Dockerfile은 핀 방식·사용자·잠금이 다르다.

**K-73·K-74 `build-images.py`·`.dockerignore` matcher — 나중에 공유(유지 팀 판단).** `W:scripts/build-images.py`(730줄)는 `T:scripts/build-images.py`(673줄)를 원형으로 적은 fork다(`W:scripts/build-images.py:31` ✔, 최상위 함수 이름 18개 공통 ✔). `.dockerignore` matcher는 W·T·D에 세 구현이 있고 지원 문법이 다르다. 발견한 것 중 가장 큰 글자 그대로의 중복이지만 두 사본 모두 다른 팀 소유이고 Manager의 서비스별 경로 둘에 물려 있다.

**K-75 비내구 테스트 PostgreSQL helper — 나중에 공유.** `M:tests/integration/_disposable_pg.py`(69줄)와 `P:apps/api/tests/integration/_disposable_pg.py`(72줄)는 서버 명령과 `make_nondurable` 본문이 같다 ✔. P에 PG 주 버전 분기가 더 있다. 소비자가 둘이고, 공유하면 테스트 시점에 git 핀 패키지 의존이 생긴다. 세 번째 소비자가 생기면 P 판을 기준으로 `[testing]` extra에 둔다.

**K-76·K-77·K-79 — 공유하지 않음.** 배포 스크립트는 호스트와 gate에 묶여 있다. Map의 `scripts/n150/*`는 이미 Manager launcher 위의 얇은 순서 스크립트다. 전체 트리 redaction을 도입하면 모든 소비자가 첫날 실패한다(운영 도메인 형식에 걸리는 추적 파일: P 2, M 3, W 19, T 37, D 8). 새 강제 계층이고(R2) 정리 빚의 대부분이 다른 팀 저장소에 있다(R7). Manager의 `build-bytecode.py`는 의도적으로 의존 없이 둔 사본이다.

**K-78 Map의 guard 검사 코드 지연 — 나중에 공유(결정 선행).** Map은 `55a921b`를 호출한다. 그 판에는 도구 규칙 단계가 없다. 최신으로 올리면 루트 `.nvmrc`와 정확 `engines.node`가 필요하다(Map 루트는 범위 선언). #1504의 커밋 메시지가 "정확 Node/npm 도구 규칙 이관은 별도 결정"이라고 적었다 ✔. §4.1의 결정과 함께 다룬다.

## 4. 공유 대상의 설계

### 4.1 프론트 정책 guard와 릴리스 모델(K-01·K-02·K-78)

문제는 §2.2다. 원인은 셋이다: (가) 정책 데이터를 `main`에서 읽는다, (나) 패키지마다 한 버전만 허용한다, (다) tarball이 정책 사본을 싣고 있어 무관한 패키지가 함께 오른다.

| 안 | 내용 | 얻는 것 | 잃는 것 |
|---|---|---|---|
| 1. 전환 창(권고) | 정책에 직전 버전과 만료일을 함께 둔다. 검사기는 만료 전까지 현재·직전 둘 다 통과시킨다 | 같은 날 함대 실패가 없다. 만료 뒤에는 지금과 같은 수렴 강제 | 검사기·생성기·정본 형식 변경. 날짜가 지나면 커밋 없이 실패가 생긴다(공지로 다룸) |
| 2. 정책을 고정 커밋에서 읽기 | guard가 정책도 `common-ref`에서 읽는다. 지연은 주간 보고로 본다 | 가장 단순. 소비자가 올릴 때만 바뀐다 | 수렴 강제가 사라진다. [frontend-libraries](../standards/frontend-libraries.md)의 현재 의도를 뒤집는다 |
| 3. 현행 + 절차 | common PR이 소비자 PR을 모두 준비한 뒤 병합 | 변경 없음 | 실패 구간이 남는다(11-17에도 일부 그렇게 했으나 두 저장소가 뒤처졌다) |

(다)는 어느 안과도 따로 고칠 수 있다. tarball이 **다른 패키지의** 버전 표를 싣지 않게 하고, 소비자의 로컬 검사는 소비자가 가진 정책 파일(또는 중앙 정본 경로)을 받는다. 그러면 `vworld-map-web`만 바뀐 날 지도 없는 소비자는 PR이 필요 없고 `ui`·`tokens`·`toast`는 버전을 올리지 않는다.

- 대상 저장소: common. 형식: ADR 1건([T-023](../tasks/T-023-frontend-guard-release-model-adr.md)) → 구현 2건([T-024](../tasks/T-024-guard-transition-window.md), [T-025](../tasks/T-025-decouple-embedded-policy.md)).
- 함대를 깨지 않는 채택: 새 검사기는 직전 버전 정보가 **없는** 정책을 지금과 똑같이 판정한다. 소비자는 호출 SHA를 올릴 때 새 동작을 얻는다. 호출 SHA를 올리지 않은 소비자는 옛 검사기로 현재 정책을 읽으므로 정본에 새 필드를 **추가만** 한다(옛 검사기가 모르는 키를 무시하는지 T-024가 회귀 시험으로 고정한다).
- Map의 검사 코드 이관([T-414](../tasks/T-414-map-guard-ref-toolchain.md))은 이 결정 뒤로 둔다.

### 4.2 원장을 실물에 맞춤(K-03)

- 대상: common 문서. [T-022](../tasks/T-022-ledger-reality-reconcile.md).
- 할 일: T-201~T-214와 T-302~T-312 각각을 실물(`packages/ui` 0.2.1, `packages/py` 0.1.0.dev0)과 대조해 "실물로 충족", "범위 재정의", "철회 제안" 중 하나로 표시한다. 이 문서의 판정 중 기존 계획과 어긋나는 것(C1 settings·C9 db·C10 alembic·C4 health 라우터·C5 errors·C3 metrics를 공유하지 않음으로, C13 time을 낮춤, C2 request-id를 지표와 분리)을 ADR-011 개정안으로 올린다.
- 이 정합이 끝나야 K-50의 실행 task가 기존 T-203·T-205·T-209·T-210과 겹치지 않는다.

### 4.3 Python 패키지 버전 규칙(K-04)

- 대상: common. [T-026](../tasks/T-026-python-version-rule.md).
- `packages/py`가 바뀌는 PR은 `pyproject.toml`의 버전을 올린다(`0.1.0.devN` 또는 다음 minor의 dev). 소비자 핀은 계속 40자리 커밋이다. 버전은 어느 핀이 어느 내용인지 사람이 구분하는 표지다.
- 새 CI 강제는 넣지 않는다(R2). 릴리스 runbook과 CHANGELOG 절에 적는다.
- 지금 세 핀은 내용이 같으므로 맞추기만 하는 PR은 내지 않는다. 각 저장소의 첫 채택 PR이 핀을 올린다.

### 4.4 HTTP 생존 probe 채택(K-10)

- 공통 코드는 이미 있다. 새 코드가 없다.
- 순서: [T-480a](../tasks/T-480a-map-api-http-health-probe.md)(Map 자체 compose)와 [T-486a](../tasks/T-486a-ktdm-api-http-health-probe.md)(Manager compose의 map-api·pinvi-api)는 서로 독립이다.
- 형식: `["CMD", "python", "-I", "-m", "kortravelcommon.http_health", "--port", "<포트>", "--path", "/health", "--timeout-seconds", "3"]`. 포트 env 기본값은 지금 probe와 같은 식을 쓴다.
- 함대를 깨지 않는 채택: compose가 요구하는 모듈이 고정 이미지에 없으면 재구축이 `compose up`에서만 죽는다. T-486a는 고정된 이미지 안에서 `python -I -c "import kortravelcommon.http_health"`가 0으로 끝나는지를 수용 기준에 둔다(`-m` 실행은 모듈이 없어도 1로 끝나서 '연결 거절'과 구분되지 않는다). Docker `timeout`은 Python 시작 비용을 감싸도록 probe timeout보다 크게 둔다(weather 블록과 같은 방식).

### 4.5 수집 결과 run tag(K-40)

- 대상: `kortravelcommon.dagster`(`[dagster]` extra). [T-313](../tasks/T-313-collection-outcome-tag.md).

```python
COLLECTION_OUTCOME_TAG = "kortravel/collection-outcome"

def record_collection_outcome(context, outcome: str) -> None:
    """자기 run의 관측 tag만 올린다. success < deferred < partial. 낮추지 않는다.
    instance·run 조회·tag 쓰기 실패로 수집을 실패시키지 않는다."""
```

- 동작은 두 사본과 같다: `partial`·`deferred`만 기록, 이미 같거나 높은 값이면 그대로, 모든 예외를 삼키고 경고 한 줄.
- 이관 순서: common 병합 → weather([T-481a](../tasks/T-481a-weather-collection-outcome.md))와 transport([T-482a](../tasks/T-482a-transport-collection-outcome.md))가 각자 핀을 올리며 로컬 함수를 지운다. 둘은 독립이다. tag 문자열이 같으므로 두 관리자 UI는 바뀌지 않는다.

### 4.6 다중 job 재시도 sensor 채택(K-41)

- 공통 코드는 이미 있다. [T-484a](../tasks/T-484a-pinvi-retry-sensor-for-jobs.md)(pinvi), [T-482b](../tasks/T-482b-transport-retry-sensor-for-jobs.md)(transport).
- sensor 이름이 바뀐다. 옛 sensor의 상태(RUNNING/STOPPED)와 cursor는 새 sensor로 넘어가지 않는다. 채택 PR은 새 sensor의 기본 상태를 옛 것과 같게 두고, 배포 뒤 옛 sensor가 사라졌는지와 새 sensor의 첫 tick을 확인한다. pinvi는 `with_updated_job`으로 asset job을 다시 주입하는 지금 방식을 유지해야 한다(`P:etl/definitions.py:95`).

### 4.7 로컬 경로 정규화 채택(K-51)

- 공통 코드는 이미 있다. [T-465](../tasks/T-465-weather-navigation-sanitize.md)(weather), [T-434](../tasks/T-434-transport-navigation-sanitize.md)(transport).
- 서버 쪽 호출부가 `@kor-travel/ui/navigation`을 import한다. 그 모듈은 React와 `"use client"`가 없는 순수 함수다(`C:packages/ui/src/navigation.ts` ✔). 서버 번들에 dist 하위 경로가 그대로 실리는지는 채택 PR이 빌드로 확인한다.
- 공통 함수에는 `fallback` 인자가 없다. 기본 경로가 `/`가 아닌 호출부는 `sanitizeLocalPath(x) === "/" ? fallback : …`로 감싼다.
- 패키지 버전이 바뀌지 않으므로 함대 비용이 없다.

### 4.8 관리자 공통 부품 묶음(K-50·K-52·K-56 일부)

- 대상: `@kor-travel/ui`의 한 버전(0.3.0 후보). 새 패키지를 만들지 않는다.
- 선행: T-022(원장 정합)와 T-024(전환 창). 전환 창 없이 내면 §2.2가 되풀이된다.
- 범위는 둘로 나눈다. [T-219](../tasks/T-219-ui-admin-display-kit.md): 표시 부품(`EmptyState`·`StatStrip`·`StatusBadge`와 variants·`DetailList`·`JsonViewer`·`CopyButton`·`PaginationBar`·`ConfirmDialog`)과 `format`. [T-220](../tasks/T-220-ui-admin-form-error-kit.md): 폼(`FormFieldInput`·`FormSelect`·`FormTextArea`)·`HelpTip`·`AppErrorPanel`과 `error-recovery`·`SectionCard`·`FilterBar`·skip link·header 띠.
- 원천은 M·W·T에서 같은 파일이다. `help-tip`은 W·T 판(더 새 것)을 쓴다. 클래스 어휘는 `--kt-*` 의미 토큰으로 옮긴다. 토스트는 주입(`onNotify`)으로 둔다([ui-contract](../standards/ui-contract.md) UC-3.7).
- [T-221](../tasks/T-221-ui-0-3-0-candidate-freeze.md)이 두 묶음을 한 후보로 얼리고 전환 창 만료일을 공지한다.
- 채택 순서: map([T-415](../tasks/T-415-map-admin-kit-adoption.md)) → weather([T-466](../tasks/T-466-weather-admin-kit-adoption.md))·transport([T-435](../tasks/T-435-transport-admin-kit-adoption.md)). map이 먼저인 이유는 원천이고 시각 회귀 기준이 있어서다. pinvi 관리자는 재도색 이식본이라 강제하지 않는다.

### 4.9 나중 묶음의 첫 걸음

- **회수 sensor API**([T-314](../tasks/T-314-reconciliation-sensor-consumer-cursor.md)): `reconciliation_sensor(..., reconcile=fn)`의 `fn`이 `ReconcileTick(clock: StallClock | None, cursor: str | None)`을 받고 새 하위 cursor를 돌려줄 수 있게 한다. 기존 호출 모양은 그대로 동작한다. 채택은 weather·transport가 이 API가 나온 뒤 정한다.
- **webserver probe**([T-315](../tasks/T-315-dagster-webserver-health-probe.md)): `python -I -m kortravelcommon.dagster_webserver_health --port <포트> [--timeout-seconds 4]`. stdlib만 쓰고 loopback GraphQL `{repositoriesOrError{__typename}}`의 `RepositoryConnection`을 0으로, 그 밖을 1로 끝낸다. 응답 크기 상한을 둔다.
- **공용 instance 설정**([T-486b](../tasks/T-486b-ktdm-shared-dagster-per-job-limit.md)): Manager가 일반 규칙의 영향(특히 Map의 job tag 수)을 확인하고 결정한다.

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
| Python 품질 설정·`python-quality` workflow | 설치 방식 넷. 재포맷 또는 새 강제를 부른다 | K-71 |
| Dockerfile 템플릿 | 핀·사용자·잠금 방식이 다르다 | K-72 |
| 배포·호스트 스크립트, 백업 스크립트 | 호스트·gate별. Map의 것은 이미 얇다 | K-76 |
| 소비자 전체 트리 redaction·task 원장 lint 강제 | 새 강제 계층. 도입 즉시 모든 소비자 실패 | K-77 |
| Manager의 `build-bytecode.py` 사본 | 의도된 무의존 사본 | K-79 |
| PinVi 사용자 표면 UI·모바일 UI, PinVi 관리자 재도색 이식본의 강제 통합 | 소비자 브랜드. [ui-contract](../standards/ui-contract.md)가 범위 밖으로 둠 | K-50 |
| Python 핀을 맞추기만 하는 PR | 세 핀의 내용이 같다 | §4.3 |

## 6. Task 목록

수용 기준·검증 명령·되돌리기는 각 상세 파일이 정본이다([task 규칙](../tasks-rule.md) §4·§5). 아래 표는 순서와 묶음만 준다. "병렬"이 같은 글자인 task는 동시에 진행할 수 있다.

| 순서 | Task | 소유 저장소 | 한 줄 | 선행 | 병렬 |
|---|---|---|---|---|---|
| 1 | [T-022](../tasks/T-022-ledger-reality-reconcile.md) | common | UI·Python 원장을 실물과 대조해 재분류 | 없음 | A |
| 1 | [T-023](../tasks/T-023-frontend-guard-release-model-adr.md) | common | guard·릴리스 모델 ADR(전환 창·내장 정책 분리) | 없음 | A |
| 1 | [T-026](../tasks/T-026-python-version-rule.md) | common | Python 패키지 버전 규칙 | 없음 | A |
| 1 | [T-313](../tasks/T-313-collection-outcome-tag.md) | common | 수집 결과 run tag 함수 | 없음 | A |
| 1 | [T-480a](../tasks/T-480a-map-api-http-health-probe.md) | kor-travel-map | Map API healthcheck를 공통 probe로 | 없음 | A |
| 1 | [T-486a](../tasks/T-486a-ktdm-api-http-health-probe.md) | kor-travel-docker-manager | map-api·pinvi-api healthcheck를 공통 probe로 | 없음 | A |
| 1 | [T-484a](../tasks/T-484a-pinvi-retry-sensor-for-jobs.md) | pinvi | 재시도 sensor 5개를 1개로 | 없음 | A |
| 1 | [T-482b](../tasks/T-482b-transport-retry-sensor-for-jobs.md) | kor-travel-transport | 재시도 sensor 3개를 1개로 | 없음 | A |
| 1 | [T-465](../tasks/T-465-weather-navigation-sanitize.md) | kor-travel-weather | 로컬 경로 정규화 사본을 공통 export로 | 없음 | A |
| 1 | [T-434](../tasks/T-434-transport-navigation-sanitize.md) | kor-travel-transport | 로컬 경로 정규화 사본을 공통 export로 | 없음 | A |
| 2 | [T-024](../tasks/T-024-guard-transition-window.md) | common | 전환 창 구현(검사기·생성기·정본) | T-023 | B |
| 2 | [T-025](../tasks/T-025-decouple-embedded-policy.md) | common | tarball 내장 정책 사본 분리 | T-023 | B |
| 2 | [T-481a](../tasks/T-481a-weather-collection-outcome.md) | kor-travel-weather | 로컬 결과 tag 함수를 공통으로 | T-313 | B |
| 2 | [T-482a](../tasks/T-482a-transport-collection-outcome.md) | kor-travel-transport | 로컬 결과 tag 함수를 공통으로 | T-313 | B |
| 2 | [T-414](../tasks/T-414-map-guard-ref-toolchain.md) | kor-travel-map | guard 검사 코드 ref와 도구 규칙 이관 | T-023 | B |
| 3 | [T-219](../tasks/T-219-ui-admin-display-kit.md) | common | 관리자 표시 부품 묶음 | T-022, T-024 | — |
| 4 | [T-220](../tasks/T-220-ui-admin-form-error-kit.md) | common | 관리자 폼·도움말·오류 부품 묶음 | T-219 | — |
| 5 | [T-221](../tasks/T-221-ui-0-3-0-candidate-freeze.md) | common | `ui` 0.3.0 단일 후보 동결과 전환 창 공지 | T-219, T-220, T-024 | — |
| 6 | [T-415](../tasks/T-415-map-admin-kit-adoption.md) | kor-travel-map | 관리자 부품 묶음 채택 | T-221 | C |
| 7 | [T-466](../tasks/T-466-weather-admin-kit-adoption.md) | kor-travel-weather | 관리자 부품 묶음 채택 | T-221 | C |
| 7 | [T-435](../tasks/T-435-transport-admin-kit-adoption.md) | kor-travel-transport | 관리자 부품 묶음 채택 | T-221 | C |
| 언제든 | [T-314](../tasks/T-314-reconciliation-sensor-consumer-cursor.md) | common | 회수 sensor의 소비자 cursor·정체 시계 전달 | 없음 | D |
| 언제든 | [T-315](../tasks/T-315-dagster-webserver-health-probe.md) | common | Dagster webserver 정의 로드 probe CLI | 없음 | D |
| 언제든 | [T-486b](../tasks/T-486b-ktdm-shared-dagster-per-job-limit.md) | kor-travel-docker-manager | 공용 instance의 job별 한도·`run_retries` 결정 | 없음 | D |

저장소별 수: common 11, kor-travel-map 3, pinvi 1, kor-travel-weather 3, kor-travel-transport 4, kor-travel-docker-manager 2(합 24).

새 task를 만들지 않고 기존 task에 맡긴 것: 인증 프리미티브(T-312), request-id(T-307, 지표와 분리해), time(T-304), cursor 코덱(T-508), 토큰 브리지(T-472·T-431), Dagster 콘솔(T-216), Node CI 골격(T-401), provider 핀·worker 스크립트 요청(T-505·T-506). 이들의 재분류는 T-022가 한다.

소비자 저장소의 task는 그 저장소의 backlog에 포인터 한 줄로 등록한다. 포인터는 이 문서와 상세 task를 가리키고 수용 기준을 복제하지 않는다.

## 7. 검증하지 못한 것

- **실행 확인이 없다.** 모든 판정은 소스 읽기다. 테스트·빌드·이미지 실행을 하지 않았다. "지워지는 줄 수"는 어림이다.
- **K-51**: 세 사본의 차이는 소스 비교로만 확인했다. 앱을 실행해 보지 않았다.
- **K-10**: 고정된 운영 이미지 안에서 probe가 도는지 보지 않았다. 핀 커밋에 모듈 파일이 있다는 것만 확인했다. PinVi API 이미지에서 `python`이 PATH의 어떤 해석기를 가리키는지도 보지 않았다.
- **K-46**: 호스트에 렌더링된 실제 instance 설정을 보지 않았다(호스트 접근 금지). 추적된 YAML과 override 표만 읽었다. Map의 queue run들이 같은 `kortravelcommon/job` 값을 갖는지 확인하지 않았다.
- **K-56**: D·TP에서 공통 부품이 어떤 색으로 그려지는지 보지 않았다(CSS 읽기만).
- **K-50**: 45개 파일의 동일성은 다시 셌지만 PW 관리자 이식본과의 차이는 하위 조사의 표본 diff다. 로컬 어휘를 `--kt-*`로 옮길 때의 시각 차이는 재지 않았다.
- **K-78**: 최신 도구 규칙 검사기가 Map의 범위 `engines`를 실제로 거절하는지 실행하지 않았다. #1504 첫 실행의 실패 문장만 읽었다.
- **guard의 현재 상태**: Map·Weather의 main은 common #57 이전 실행이 마지막이라 초록이다. "다음 실행이 실패한다"는 정책과 소비자 원장의 정적 비교에서 나온 예측이며, 재vendor PR 자체의 실행 결과만 직접 봤다.
- **provider 라이브러리 내부**(`failure_kind` 범위 등)와 geo·concierge 코드는 읽지 않았다.
- **`✔` 없는 인용**은 하위 조사가 `nl -ba`·`grep -n`으로 확인했다고 보고한 값이다. 작성자가 다시 읽은 표본에서는 모두 맞았지만 전수는 아니다.
- **TypeScript 쪽 시간·거리 헬퍼**는 표본만 봤다.

## 8. 근거

- 2026-09 조사: [commonality matrix](../survey/commonality-matrix.md), [backend](../survey/cross/backend.md), [ci-deploy](../survey/cross/ci-deploy.md), [survey README](../survey/README.md).
- 결정: [ADR-011](../adr/011-python-common-package.md), [ADR-014](../adr/014-common-implementation-without-registry-publishing.md), [ADR-015](../adr/015-common-shared-systems-scope.md), [ADR-017](../adr/017-shadcn-radix-shared-components.md), [ADR-018](../adr/018-exact-node-npm-build-toolchain.md).
- 규칙: [backend-stack](../standards/backend-stack.md) §8·§10, [frontend-libraries](../standards/frontend-libraries.md), [ui-contract](../standards/ui-contract.md), [versions](../standards/versions.md).
- 실물: `packages/py/kor-travel-common`, `packages/ui`, `tools/check_frontend_dependencies.mjs`, `.github/workflows/frontend-consumer-guard.yml`.
- 2026-11-17 PR: common #57·#58, pinvi #763, kor-travel-transport #205, kor-travel-docker-manager #605, kor-travel-map #1504, kor-travel-weather #243.
