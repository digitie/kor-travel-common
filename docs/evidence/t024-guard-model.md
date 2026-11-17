# T-024 guard 모델 구현 evidence

기준일은 2026-11-18이다. 구현 정본은 [ADR-019](../adr/019-frontend-policy-guard-model.md)와 [T-024](../tasks/T-024-guard-model-implementation.md)다. 소비자 저장소는 수정하지 않았고, 아래 소비자 결과는 각 저장소 main의 얕은 clone에 대한 읽기 전용 실행이다. 실제 소비자 채택은 `NOT_RUN(소비자 저장소)`.

## 채택 커밋

채택 커밋은 PR #63의 squash 병합 커밋 **`e18d1892dcc3915a5e6e57ccad550a852b793780`**이다. 병합 커밋의 트리는 리뷰·CI를 마친 PR head(`989946a`)와 같다. 병합 뒤 이 커밋을 checkout해 아래 소비자 실행을 다시 돌렸고 결과가 같았다(map main은 그사이 `efe9c43ad8ba5200b11ca1e0bc7b71a99732fb14`로 움직였고 결과·호출 줄은 그대로).

## 무엇이 바뀌었나

| 항목 | 옛 판(`55a921b`·`97f8ed9`·`9e16393`) | 새 판(채택 커밋) |
|---|---|---|
| 정책 세 파일 | main sparse checkout | `common-ref` checkout |
| `--registry`(Node/npm 축) | main `versions.json` | `common-ref` `versions.json` |
| guard 자신의 Node | `node-version: 22.23.1` | `common-ref`의 `.nvmrc`(`node-version-file`) |
| guard 자신의 npm | `npm@12.0.1` 고정 | `common-ref`의 `axes.npm.recommended` |
| 호출 SHA = `common-ref` | 확인 없음 | 다른 저장소 호출에서 `job.workflow_sha`로 확인(읽을 수 없으면 경고) |
| 검사 기준 디렉터리 | 저장소 루트 고정 | 선택 입력 `root`(기본 `.`) |
| 최신 정본과의 차이 | 실패 | 주간 지연 보고(exit 0) |

## selftest(PR CI)

시험 전용 고정 ref `81810cc3462435d73e683de7ce85c4f11557747b`(브랜치 `selftest/t024-guard-ref-fixture`, 삭제 금지)는 main `ec021bf`와 세 가지만 다르다: Node 축 24.22.3, npm 축 11.20.0, `zustand` 정본 5.0.16(main 5.1.0). 그 커밋에서 `npm ci --ignore-scripts --engine-strict`·`check:toolchain`·`check:policy`·`test:toolchain`(90 pass)이 Node 24.22.3/npm 11.20.0으로 통과함을 로컬에서 확인했다. fixture 소비자 `tests/fixtures/guard-consumer`(mobile 프로필, 산출물 tokens 0.1.2·lightningcss fix4)는 이 ref의 값만 맞춘다.

| 수용 기준 | 시험 | 판정 |
|---|---|---|
| 고정 ref 소비자는 main의 정책 값·`axes.node.recommended`가 달라도 통과 | `frontend-guard-pinned-ref`: 새 guard를 `common-ref: 81810cc…`로 호출. fixture의 zustand·Node·npm은 main과 다르다 | PR CI |
| 자기 `common-ref`와 어긋나면 실패 | `frontend-guard-strict`: guard workflow의 대조 단계 원문을 꺼내 실행한다. 같은 fixture는 통과, zustand를 main 값으로·`.nvmrc`를 22.23.1로·`packageManager`를 npm@12.0.1로·원장 tokens 버전을 바꾼 네 변형과 `root` 탈출은 각각 기대한 오류 문구로 실패 | PR CI(로컬 사전 실행 동일) |
| Node 축이 22.23.1이 아닌 ref에서 guard 자신의 Node·npm이 그 ref 값 | `frontend-guard-pinned-ref`의 "중앙 검사 환경" 로그 `Node v24.22.3 / npm 11.20.0`과 `check:toolchain --runtime` PASS | PR CI |
| 옛 판(`97f8ed9`) 호출자의 판정이 그대로 | 아래 절 | 변경 없음 |

## 옛 판 판정 불변

옛 판 workflow는 자기 SHA의 파일이라 이 PR이 바꿀 수 없다. 옛 판이 main에서 읽는 것은 정책 세 파일뿐이고(`versions.json`·`frontend-dependencies.json`·`frontend-artifacts.json`), 이 PR은 셋 다 바꾸지 않는다(`git diff origin/main -- versions.json frontend-dependencies.json frontend-artifacts.json` 빈 출력). 따라서 병합 전후 main의 정책 bytes가 같고 옛 판 호출자의 판정도 같다. 과제 문서가 예시한 옛 검사기 사본(`tests/fixtures/guard-checkers/`)은 두지 않았다. 사본으로 확인할 수 있는 것이 위 bytes 동일성과 같고, 사본은 정책이 바뀌는 다음 PR마다 결과가 달라져 영구 시험이 되지 못한다.

대신 실제 옛 판을 실제 호출자에 돌려 전후를 비교했다. 각 옛 판(`97f8ed9`, map은 `55a921b`)의 workflow에서 "중앙 버전·산출물과 소비자 대조" 단계 원문을 꺼내, 그 SHA의 검사기와 정책 디렉터리(`common-policy`) 하나로 일곱 소비자 main의 호출 입력에 실행했다. 정책 디렉터리는 병합 전(main `565646d`)과 병합 후(이 PR head)의 세 파일이며 `diff -r`로 bytes가 같다. Node 22.23.1·npm 12.0.1.

| 소비자 frontend | 옛 판 | 병합 전 | 병합 후 |
|---|---|---|---|
| pinvi `apps/web`·`apps/mobile` | `97f8ed9` | PASS·PASS | PASS·PASS |
| weather `packages/kor-travel-weather-admin/frontend` | `97f8ed9` | PASS | PASS |
| transport `frontend`·`packages/kor-travel-transport-admin/frontend` | `97f8ed9` | PASS·PASS | PASS·PASS |
| docker-manager `frontend` | `97f8ed9` | PASS | PASS |
| geo `kor-travel-geo-ui` | `97f8ed9` | PASS | PASS |
| concierge `frontend` | `97f8ed9` | PASS | PASS |
| map `packages/kor-travel-map-admin/frontend` | `55a921b` | PASS | PASS |

## 일곱 소비자 main 읽기 전용 실행

새 guard의 "common-ref 정책·산출물과 소비자 대조" 단계 원문을 workflow에서 그대로 꺼내, 각 소비자 main의 호출 입력(`frontends`·`toolchain-manifests`·`node-dockerfiles`)으로 실행했다. common 쪽은 이 브랜치(정책·검사기가 main `ec021bf`와 bytes 동일)를 Node 22.23.1·npm 12.0.1로 설치했다.

| 소비자 | main 커밋 | guard 호출 SHA 위치(호출 / `common-ref`) | 결과 | 걸린 규칙 |
|---|---|---|---|---|
| pinvi | `6d9674397ee4b89891d749656d71f47b808791b6` | `.github/workflows/common-frontend-policy.yml:13` / `:15` | PASS(web·mobile) | — |
| map | `fbc4b24237653b247830a12d58c632cc461b7280` | `.github/workflows/common-frontend-policy.yml:13` / `:15`(`55a921b`) | FAIL | 의존성·산출물은 통과. 도구 규칙 `.nvmrc Node 버전 불일치`, `package.json engines Node/npm 선언 누락·불일치`(Map은 이미 26.13.1, 축은 22.23.1 — T-029 커밋으로 옮긴다, T-417) |
| weather | `5b8801719e5f6c98726059232f3de2868374d6b2` | `.github/workflows/ci.yml:13` / `:15`, `.github/workflows/common-frontend-policy.yml:10` / `:12` | PASS | — |
| transport | `6f9a947e496b49522bb12a3c4166e0e37af5e922` | `.github/workflows/ci.yml:23` / `:25`, `.github/workflows/common-frontend-policy.yml:10` / `:12` | PASS(두 frontend) | — |
| docker-manager | `79032717046241a1dd698d385b59376d68a45289` | `.github/workflows/common-frontend-policy.yml:13` / `:15` | PASS | — |
| geo | `a0f2608e6a7373758cc38f896b78aa0c7a827112` | `.github/workflows/ci.yml:13` / `:15` | PASS | — |
| concierge | `3fa128ada3d7725b7cf10851edc2bdeafa108705` | `.github/workflows/common-frontend-policy.yml:13` / `:15` | PASS | — |

## 지연 보고 출력(2026-11-18, 정본 main `ec021bf`)

`GITHUB_TOKEN=… python3 -B tools/frontend_guard_lag_report.py --main-sha <main>`의 출력이다. 모든 소비자가 아직 옛 판을 호출한다. exit 0.

| 저장소 | 호출 위치 | 호출 SHA | common-ref | guard 판 | main보다 뒤 커밋 | 정책 파일 차이 | 벤더 버전 차이(벤더→정본) |
|---|---|---|---|---|---|---|---|
| digitie/pinvi | `.github/workflows/common-frontend-policy.yml:13` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-map | `.github/workflows/common-frontend-policy.yml:13` | `55a921b55d24` | `55a921b55d24` | 옛 판(main 읽음) | 47 | versions.json, frontend-dependencies.json, frontend-artifacts.json | 없음 |
| digitie/kor-travel-weather | `.github/workflows/ci.yml:13` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-weather | `.github/workflows/common-frontend-policy.yml:10` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-transport | `.github/workflows/ci.yml:23` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-transport | `.github/workflows/common-frontend-policy.yml:10` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-docker-manager | `.github/workflows/common-frontend-policy.yml:13` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-geo | `.github/workflows/ci.yml:13` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |
| digitie/kor-travel-concierge | `.github/workflows/common-frontend-policy.yml:13` | `97f8ed983605` | `97f8ed983605` | 옛 판(main 읽음) | 3 | 없음 | 없음 |

## 소비자가 SHA 말고 바꿀 것

- 호출 줄(`uses: …@<sha>`)과 `common-ref:` 두 자리를 같은 채택 커밋으로 올린다. 다르면 새 guard가 실패한다.
- 채택 커밋의 정책은 지금 main과 같으므로 pinvi·weather·transport·docker-manager·geo·concierge는 다른 파일을 바꿀 필요가 없다(위 표 PASS).
- weather·transport는 `ci.yml`과 `common-frontend-policy.yml` 두 파일에 호출이 있다. 둘 다 올린다.
- map은 채택 커밋이 아니라 Node 축이 26.13.1인 T-029 커밋으로 옮긴다(T-417).
