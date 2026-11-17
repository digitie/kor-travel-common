# ADR-019: 프론트 guard는 정책과 Node/npm 축을 호출자가 고정한 common 커밋에서 읽는다

- 상태: accepted
- 날짜: 2026-11-17
- 결정자: 소유자(2026-11-17, "ADR-019 … 추천안은 검사기가 각 서비스가 고정해 둔 common 버전에서 정책과 Node/npm 버전을 읽는 것입니다 … 이것들은 추천안 대로")
- 근거 문서: [공통화 재조사·계획](../plan/commonization-plan-2026-11-17.md) §2.2·§4.1(K-01·K-02·K-78), [T-023](../tasks/T-023-frontend-guard-release-model-adr.md)
- Supersedes: [ADR-018](018-exact-node-npm-build-toolchain.md)의 "재사용 frontend guard는 live 중앙 도구 축으로 runtime을 검증한다" 한 문장(축을 읽는 자리만). [frontend-libraries](../standards/frontend-libraries.md) '검사와 갱신' 절의 "비교할 데이터는 현재 common main을 읽는다"와 "오래된 workflow를 유지해도 최신 정본과 다르면 실패한다"

이 ADR은 kor-travel-common의 ADR-019다. `docs/architecture/consumers.md`·`docs/architecture/adoption-readiness.md`·`docs/plan/design-brief.md`에 나오는 "ADR-019"는 kor-travel-geo 저장소의 ADR이며 이것과 무관하다.

## 컨텍스트

2026-11-17 common #57이 `vworld-map-web` 1.0.4·`vworld-map-rn` 1.0.2를 정책에 넣었다(02:07 UTC 병합). 그 순간부터 옛 버전을 가진 소비자의 다음 guard 실행이 실패했고, pinvi #763(파일 26개)·docker-manager #605(8개)·transport #205(20개)·map #1504(12개)·weather #243(14개)까지 재vendor PR 5개·파일 80개가 필요했다. `ui`·`tokens`·`toast`는 실행 코드와 CSS가 그대로인데 내장 정책 사본 때문에 patch 버전을 올렸다. 원인은 넷이다(계획 §4.1).

- (가) guard는 검사 **코드**를 호출자가 고정한 커밋에서 받지만 정책 데이터 세 파일(`versions.json`·`frontend-dependencies.json`·`frontend-artifacts.json`)은 항상 `main`에서 받는다. `97f8ed9` 판은 Node/npm 도구 축(`axes.node.recommended`·`axes.npm.recommended`)도 `main`에서 읽는다. 그래서 다음 Node/npm patch가 main에 들어가면 여섯 소비자가 같은 날 실패한다.
- (나) 정책은 패키지마다 버전 하나만 허용한다.
- (다) tarball이 정책 전체의 사본을 싣고 있어 무관한 패키지 한 줄이 세 패키지를 다시 pack하게 만든다.
- (라) 소비자는 자기가 고정한 옛 검사기를 실행하고, 그 검사기는 현재 값 하나만 읽는다. Map은 `55a921b`에 머물러 도구 규칙이 없다.

weather·transport는 `ci.yml` 안의 guard 호출이 PR을 막으므로, main 정책이 움직이면 다른 팀의 Python만 바꾼 PR도 막힌다.

## 결정

1. **읽는 자리.** 재사용 guard는 정책 데이터 세 파일과 Node/npm 도구 축을 호출자가 넘긴 `common-ref` 커밋에서 읽는다. `main`을 checkout하지 않는다. 호출 SHA와 `common-ref`는 같은 40자리 값이어야 한다.
2. **검사의 엄격함은 그대로다.** 소비자의 선언·tarball 파일명·lock·원장은 자기 `common-ref`의 정책·정본과 정확히 같아야 하고, 다르면 실패한다. Node/npm도 자기 `common-ref`의 `axes.node.recommended`·`axes.npm.recommended`와 `.nvmrc`·`engines`·`packageManager`·Node 이미지가 같아야 한다.
3. **강제 수렴을 없애고 보고로 본다.** 최신 정본과의 차이는 실패가 아니라 주간 지연 보고(소비자별 호출 ref·벤더 버전·정본과의 차이, exit 0)로 본다. 수렴은 소비자가 ref를 올리는 PR로 일어난다.
4. **옛 판은 바꾸지 않는다.** 이미 고정된 workflow 판(`55a921b`, `97f8ed9`)은 지금처럼 `main`을 읽는다. 새 동작은 호출 SHA를 T-024가 지정한 채택 커밋으로 올린 소비자만 얻는다. 채택 커밋은 '최신'이 아니라 common이 지정한 커밋 하나다.
5. **Node/npm 축도 같은 규칙이다.** `main`의 Node/npm 값이 바뀌어도 ref를 올리지 않은 새 guard 소비자는 영향이 없다. 단, 옛 판(`main`을 읽는 판)을 호출하는 소비자가 남아 있는 동안 `main`의 정책 값이나 Node/npm 축을 바꾸면 그 소비자는 지금처럼 당일 실패한다. 그래서 공통 Node/npm 축의 상향([T-029](../tasks/T-029-node-axis-to-latest-lts.md))은 pinvi·weather·transport·docker-manager가 채택 커밋으로 옮긴 뒤(또는 그 팀이 당일 갱신을 확인한 뒤)에 병합하고 geo·concierge에는 미리 알린다.
6. **긴급 갱신 경로.** registry 보안 갱신은 common `main`에 정책을 반영한 뒤 각 소비자가 ref를 올리는 PR 하나로 받는다. 따로 예고 창이나 만료일을 두지 않는다.
7. **내장 정책의 자리.** `ui`·`tokens`·`toast` 각 패키지는 자기 것(자기 peer 범위와 자기 식별)만 싣고, tarball 안의 검사기(`check:dependencies`)는 그것만 검사한다. 함대 전체의 정확 버전 대조는 중앙 guard의 몫이다. 소비자의 `check:dependencies` 명령 줄은 바뀌지 않는다. 정책에 무관한 패키지를 더하거나 바꿔도 세 패키지의 tarball bytes는 바뀌지 않아야 한다. 구현과 한 번의 patch 릴리스(`ui` 0.2.2·`tokens` 0.1.3·`toast` 0.1.2)는 [T-025](../tasks/T-025-decouple-embedded-policy.md)다.
8. **선택형 산출물 패키지.** 일부 소비자만 쓰는 부품은 모든 소비자가 필수로 받는 `ui`·`tokens`를 키우지 않고 선택형 산출물 패키지로 낸다(`@kor-travel/toast` 선례: `artifactPackages`에는 있고 프로필 필수 목록에는 없다). 검사기는 소비자가 선언하지 않은 산출물을 건너뛰므로 쓰지 않는 소비자의 비용은 0이다.
9. **Map.** Map은 정확 Node/npm 핀을 채택한다([T-416](../tasks/T-416-map-exact-node-npm-pin-decision.md), 소유자 2026-11-17: Node는 최신 LTS 26.13.1, npm은 공통 축 12.0.1). Map이 새 guard로 옮기는 것([T-417](../tasks/T-417-map-guard-ref-toolchain.md))은 공통 축이 26.13.1인 커밋이 생긴 뒤다.

T-024·T-025의 수용 기준으로 옮길 문장:

- 새 guard를 고정 ref로 호출한 소비자는 그 뒤 `main`의 정책 값과 `axes.node.recommended`가 바뀌어도 통과한다.
- 같은 소비자가 자기 `common-ref`의 정책·도구 축과 어긋나면 실패한다.
- 옛 판(`97f8ed9`) workflow를 호출하는 소비자의 판정은 이 변경 전과 같다.
- 지연 보고는 차이가 있어도 exit 0이다.
- 정책의 무관한 한 줄을 바꾸거나 새 패키지를 더해도 `ui`·`tokens`·`toast` tarball SHA-256이 그대로다. 내장 검사는 자기 peer 위반은 실패시키고 무관한 의존성의 버전 차이는 실패시키지 않는다.

## 대안 검토

| 안 | 얻는 것 | 잃는 것 | 판정 |
|---|---|---|---|
| 1. 정책·도구 축을 호출 커밋에서 읽기 + 막지 않는 지연 보고 | 가장 단순하다. 정책·Node/npm·registry 패키지 어느 것이 바뀌어도 소비자는 자기가 ref를 올릴 때만 영향을 받는다. 긴급 갱신이 ref PR 하나다. Python 핀(수단 A)과 같은 모양이다 | 최신 정본으로의 강제 수렴. 소비자가 한 번은 호출 SHA를 올려야 이 동작을 얻는다 | **채택** |
| 2. 예고 필드 | 예고 시점에 아무도 실패하지 않고 수렴 강제가 남는다 | 릴리스가 두 PR이 된다. 예고 자리가 하나면 다른 릴리스가 기다리고 창 길이를 다른 팀이 정한다. Node/npm·registry 패키지까지 필드를 넓혀야 하고 긴급 경로를 따로 정해야 한다. guard를 올릴 수 없는 소비자는 마감 당일 실패한다 | 기각. 숨은 조건이 많고 강제 계층을 더한다 |
| 3. 직전 버전 허용 + 만료일 | 새 검사기 소비자만 보호된다 | 옛 검사기 소비자는 그날 실패한다(라). 날짜가 실패를 만든다 | 기각 |
| 4. 현행 + 절차(common PR이 소비자 PR을 모두 준비한 뒤 병합) | 코드 변경이 없다 | 실패 구간이 남는다. 11-17에도 그렇게 하려 했으나 두 저장소가 뒤처졌다 | 기각 |

내장 정책을 tarball에서 빼고 정책 파일 경로를 인자로 받는 방식도 기각한다. 일곱 소비자 프론트가 인자 없이 tarball 안의 검사기를 실행하므로 모든 소비자의 명령 줄을 바꿔야 하고, 정책 파일을 소비자가 벤더하면 비용이 소비자로 옮겨갈 뿐이다.

## 결과

- 잃는 것은 강제 수렴 하나다. 오래된 정책에 머무는 소비자는 실패하지 않고 지연 보고에 나타난다. 수렴을 독촉하는 것은 보고를 읽는 사람의 몫이다.
- 옛 guard 판을 호출하는 소비자(geo·concierge와 아직 옮기지 않은 소비자)는 지금과 같다. 이 ADR은 그들을 깨지도 고치지도 않는다.
- Node/npm 축은 소비자마다 자기 ref의 값을 따른다. 공통 축을 올리는 것은 새 ref를 내는 일이고, 각 소비자는 ref를 올리는 PR에서 Node/npm을 함께 맞춘다.
- [frontend-libraries](../standards/frontend-libraries.md) '검사와 갱신' 절, [versions](../standards/versions.md) §3.1.1, [release](../runbooks/release.md), [consumer-adoption](../runbooks/consumer-adoption.md)의 본문 갱신은 구현과 같은 PR([T-024](../tasks/T-024-guard-model-implementation.md))에서 한다. 그 전까지 workflow는 `main`을 읽는다.

## 후속·적용 위치

- [T-024](../tasks/T-024-guard-model-implementation.md): `frontend-consumer-guard.yml`이 `common-ref`에서 읽게 하고, 지연 보고와 채택 커밋을 낸다.
- [T-025](../tasks/T-025-decouple-embedded-policy.md): 내장 정책 축소와 세 패키지 patch 릴리스. 외부 선행(소비자 호출 SHA 갱신 또는 당일 재vendor 확인)은 그대로다.
- [T-029](../tasks/T-029-node-axis-to-latest-lts.md): 공통 Node 축을 최신 LTS로 올린다. 소비자가 옮긴 뒤에 병합한다.
- 소비자 호출 SHA 갱신: [T-424](../tasks/T-424-pinvi-guard-ref.md)·[T-467](../tasks/T-467-weather-guard-ref.md)·[T-436](../tasks/T-436-transport-guard-ref.md)·[T-474](../tasks/T-474-ktdm-guard-ref.md)·[T-417](../tasks/T-417-map-guard-ref-toolchain.md).
