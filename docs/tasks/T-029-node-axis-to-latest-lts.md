# T-029 공통 Node 도구 축을 최신 LTS(26.13.1)로 올림 (2026-11-18, PR #65)

- 상태: DONE
- 우선순위: P2
- Gate: 도구 단위·패키지 빌드·2인 리뷰
- 선행: T-024
- 외부 선행: 소유자 확인 — 2026-11-17 결정은 Map(T-416)에 대한 답이었으므로, 공통 축을 같은 값으로 올려 각 소비자가 ref를 올릴 때 Node 26으로 옮기게 하는 것을 소유자가 확인한다. 그리고 옛 판(`97f8ed9`·`9e16393`)을 호출하는 **모든** 소비자가 T-024 채택 커밋 이후로 호출 SHA를 올렸음: pinvi(T-424)·weather(T-467)·transport(T-436)·docker-manager(T-474)와 geo·concierge(이 계획에 task가 없어 각 저장소에 요청한다). 옛 판은 `node-version: 22.23.1`로 검사기를 돌리고 `check:toolchain --runtime`이 그 실행 Node를 main 축과 대조하므로, 소비자가 Node를 미리 올려도 축이 바뀐 날 실패한다. 당일 갱신으로 피할 길은 없다
- 외부 선행 충족(2026-11-18): 소유자 확인 2026-11-17. 옛 판 호출자 여섯 전부 병합 — pinvi [#778](https://github.com/digitie/pinvi/pull/778)(`78779c6462ab23c79893e14c11ec94414fd8ce71`)·weather [#250](https://github.com/digitie/kor-travel-weather/pull/250)(`91f95abeb2ddc69193494c6736621738708f09a6`)·transport [#209](https://github.com/digitie/kor-travel-transport/pull/209)(`1b64873daac3479bc73ccadff890a3855cd36f28`)·docker-manager [#612](https://github.com/digitie/kor-travel-docker-manager/pull/612)(`011f1fb94028fd4984fbab63d3b1fd7dc29a0726`)·geo [#640](https://github.com/digitie/kor-travel-geo/pull/640)(`f5b3003d82d4b2fed8e585a4df5d3a5ce8a022fb`)·concierge [#271](https://github.com/digitie/kor-travel-concierge/pull/271)(`9723689fdb45bc969ca8b6829176ab5ffe262037`). 병합 직전 여섯 기본 브랜치의 guard 호출은 모두 `e18d189`, map은 `55a921b`.
- 소유 저장소: kor-travel-common
- 병렬: T-024 뒤. T-025와는 독립이다(`tools/sync_frontend_policy.mjs`는 `ecosystem: npm` 축만 생성 정책에 넣고 Node 축은 `runtime`이라 `ui`·`tokens`·`toast`를 다시 pack하게 만들지 않는다). T-417의 선행

출처는 [ADR-019](../adr/019-frontend-policy-guard-model.md) 결정 5·9와 [T-416](T-416-map-exact-node-npm-pin-decision.md)의 소유자 결정(2026-11-17)이다.

## 목표

소유자는 2026-11-17에 Map의 정확 Node 핀을 "최신 버전"으로 정했다. 그날 nodejs.org 공식 릴리스 색인(`https://nodejs.org/dist/index.json`)에서 가장 새 LTS 줄은 26(Lithium)이고 그 최신 patch는 26.13.1(2026-11-10, 보안 릴리스, 동봉 npm 11.20.0)이다. 색인의 가장 새 항목은 `v27.0.0-alpha.0.1.1`(alpha)이라 운영 핀 대상이 아니다. 공통 축(`axes.node.recommended`)은 22.23.1이다. Map이 새 guard로 옮기려면([T-417](T-417-map-guard-ref-toolchain.md)) 그 ref의 축이 26.13.1이어야 한다. 이 task는 공통 축을 26.13.1로 올리고 그 병합 커밋을 Map이 고정할 커밋으로 적는다.

## 고정 결정

- 축을 읽는 자리는 ADR-019다. 새 guard 소비자는 ref를 올릴 때만 이 값을 받는다. 옛 판(`main`을 읽는 판)을 호출하는 소비자는 병합 당일 실패하므로 외부 선행(모든 옛 판 호출자의 이전)을 확인한 뒤 병합한다. Map은 `55a921b`에 도구 단계가 없어 이 날 영향이 없다.
- `@types/node`(정책상 22.20.5, npm 축)는 바꾸지 않는다. npm 축 변경은 옛 검사기 소비자(Map 포함)의 `policy.versions` 대조에 걸리므로 별도 task(T-025와 전 소비자 이전 뒤)다.
- npm 축은 12.0.1 그대로다(Node 26 동봉 npm 11.20.0으로 내리지 않는다). npm 12.0.1의 `engines.node`는 `^22.22.2 || ^24.15.0 || >=26.0.0`이라 Node 26.13.1을 받는다.
- `floor`(호환 하한)는 바꾸지 않는다. 정확 선택값만 바꾼다(ADR-018).
- Node 이미지의 배포판·libc는 각 앱이 유지한다. 공통 축의 `image`는 `node:26.13.1-bookworm-slim`이다.

## 구현 범위

1. `versions.json`의 `axes.node.recommended`를 `26.13.1`, `image`를 `node:26.13.1-bookworm-slim`으로 바꾼다. 생성 정책(`frontend-dependencies.json`)은 Node 축을 싣지 않으므로 바뀌지 않아야 한다.
2. common 자신의 private anchor(루트 `.nvmrc`, `package.json`의 `engines.node`, workflow의 `node-version`)를 같은 값으로 바꾼다. 재사용 guard가 검사기를 실행할 때 쓰는 Node도 T-024의 구현에 맞춰 `common-ref`의 축을 따르게 한다.
3. `ui`·`tokens`·`toast`의 tarball과 `frontend-dependencies.json`이 바뀌지 않음을 확인한다(Node 축은 생성 정책 밖이다). 바뀌면 멈추고 원인을 적는다.
4. 병합 커밋을 40자리로 문서([integration map](../integration-map.md), T-417)에 적는다. Map이 T-417에서 고정할 커밋이다.

## 범위 밖

소비자 저장소의 Node 갱신(각 저장소가 ref를 올리는 PR에서 한다), npm 축과 `@types/node` 변경, Map의 핀(T-416이 Map PR로 한다).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
versions.json
.nvmrc, package.json, package-lock.json
.github/workflows/*.yml(node-version)
docs/standards/versions.md, docs/integration-map.md, CHANGELOG.md, docs/journal.md
```

> 구현 메모(2026-11-18): 소유자가 2026-11-17에 모든 저장소의 Node 26 이전을 확인했다(조정 세션을 거친 구두 확인이라 저장소 안 링크는 없다)(외부 선행의 소유자 확인 충족). 옛 판 호출자 여섯의 이전 PR 상태는 병합 PR 본문에 적는다. `B2 alias default registry` 시험이 실제 `versions.json`을 읽으면서 정합 값을 상수 22.23.1로 두어 축 상향에 결박돼 있어 함께 고쳤다. [evidence](../evidence/t029-node-axis.md).

## 병합 커밋

`0dec9543c8c8730ce7b05837f2fbe6c31d4ede65`(PR #65 squash 병합, 2026-11-18). 트리는 리뷰·CI를 마친 head `9a6395e`와 같다. Map은 T-417에서 guard 호출 SHA와 `common-ref`를 이 값으로 올린다. 이 커밋을 고정한 fixture 소비자 guard 실행도 PASS다([evidence](../evidence/t029-node-axis.md)).

## 수용 기준

- [x] `npm ci --engine-strict && npm run check:toolchain`이 Node 26.13.1·npm 12.0.1에서 통과한다.
- [x] `npm run check:policy`·`npm run test:toolchain`·`npm test --workspaces`가 통과한다.
- [x] `frontend-dependencies.json`과 `ui`·`tokens`·`toast` tarball SHA-256이 바꾸기 전과 같다.
- [x] 이 커밋을 `common-ref`로 고정한 fixture 소비자에서 guard selftest가 Node 26.13.1로 통과한다(T-024가 guard 자신의 Node를 ref에서 고르게 했는지 확인. `frontend-consumer-guard.yml`·`frontend.yml`·`consumer-smoke.yml`의 적힌 `node-version`이 남아 있으면 이 task에서 고친다).
- [x] 병합 PR 본문에 외부 선행 각 항목의 상태와 근거 링크가 있다.
- [x] 병합 커밋이 40자리로 integration map과 T-417에 있다.

## 검증 명령

```bash
npm ci --engine-strict && npm run check:toolchain
npm run check:policy && npm run test:toolchain
npm test --workspaces
python3 -B -X utf8 tools/validate_document_links.py && git diff --check
```

## evidence

PR check 결과, 외부 선행 확인 링크. 소비자 반영은 `NOT_RUN(소비자 저장소)`.

## rollback·release 차단 조건

- `git revert` 1회로 축이 22.23.1로 돌아간다. 이미 이 커밋으로 ref를 올린 소비자는 그 ref를 계속 쓰므로 영향이 없다.
- 옛 판 guard를 호출하는 소비자 가운데 외부 선행에 적힌 저장소가 남아 있으면 병합하지 않는다.
