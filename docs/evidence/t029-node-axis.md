# T-029 공통 Node 축 26.13.1 evidence

기준일은 2026-11-18이다. 정본은 [T-029](../tasks/T-029-node-axis-to-latest-lts.md)·[ADR-019](../adr/019-frontend-policy-guard-model.md)다. 소비자 저장소는 수정하지 않았다. 소비자 반영은 `NOT_RUN(소비자 저장소)`.

## 바뀐 값

| 자리 | 전 | 후 |
|---|---|---|
| `versions.json` `axes.node.recommended` | 22.23.1 | 26.13.1 |
| `versions.json` `axes.node.image` | `node:22.23.1-bookworm-slim` | `node:26.13.1-bookworm-slim` |
| `.nvmrc`·`package.json`·`package-lock.json` 루트 `engines.node` | 22.23.1 | 26.13.1 |
| `frontend.yml`·`consumer-smoke.yml` `setup-node` | `node-version: 22.23.1`, `npm@12.0.1` 리터럴 | `node-version-file`(`.nvmrc`), npm은 `axes.npm.recommended` |

`floor`(22.12)·npm 축(12.0.1)·`@types/node`(정책 22.20.5)는 그대로다.

## 공식 이미지 digest(2026-11-18 조회)

Docker Hub `library/node:26.13.1-bookworm-slim`의 OCI index digest는
`sha256:5df79989ed685e09f0a98019db4cebfb22fb9df1a53c0161664a011f7ff6b0f1`이다(registry `docker-content-digest`).
플랫폼별 manifest: linux/amd64 `sha256:18a166e2d50578afe933434857ed2d9059bd1aa398a223e9c89eb4302354f079`,
linux/arm64/v8 `sha256:8261241c4197285eaeca819863dab5042cd1f9147b000670f4e773f4d5fe7768`.
`versions.json`은 digest를 싣지 않는다(배포판·libc·digest는 앱이 고른다, ADR-018). bookworm-slim을 쓰는 앱은 index digest를 핀한다.

## guard: 이 판을 `common-ref`로 고정한 fixture 소비자

시험 브랜치 `selftest/t029-head-verify`(병합하지 않음)에서 재사용 guard를 호출 SHA·`common-ref` 모두 PR head로 고정하고,
`tests/fixtures/guard-consumer`를 새 축 쪽으로 바꾼 사본(`.nvmrc`·`engines.node` 26.13.1, `packageManager`·`engines.npm` 12.0.1, zustand 5.1.0)을 검사했다.

| 실행 | common-ref | 결과 |
|---|---|---|
| [44189997950](https://github.com/digitie/kor-travel-common/actions/runs/44189997950) | `bdde7069e121a56e18a1b189afbcd9b1db6b740e` | FAIL — 검사기 실행 Node v26.13.1·npm 12.0.1, 대조·도구 규칙 PASS, `test:toolchain` 1건 실패(아래) |
| [44190418059](https://github.com/digitie/kor-travel-common/actions/runs/44190418059) | `7f6052a758aa65308e5336eae6d6bd6a362f5960` | PASS — "Node 26.13.1 / npm 12.0.1 도구 규칙 PASS", `test:toolchain` 90/90 |

첫 실행의 실패는 `B2 alias default registry` 시험이 실제 `versions.json`을 기본 registry로 읽으면서 정합 선언은 상수 22.23.1로 만들던 결박이었다. 축을 올리면 언제나 깨지는 시험이라 정합 값을 실제 `versions.json`에서 읽게 고쳤다.

기존 selftest(`frontend-guard-pinned-ref`, 고정 시험 ref `81810cc`의 Node 24.22.3)는 guard 자신의 Node가 ref에서 선택됨을 계속 보인다.

## 생성 정책·tarball 불변

docs CI `packages` job이 보관한 배포 후보 pack(`common-release-packs-<source SHA>`)을 main과 PR head에서 내려받아 비교했다.

| 파일 | main `c9e57d6`([44188150909](https://github.com/digitie/kor-travel-common/actions/runs/44188150909)) | PR head `c31fcaa`([44192052384](https://github.com/digitie/kor-travel-common/actions/runs/44192052384)) |
|---|---|---|
| `kor-travel-ui-0.2.1.tgz` | `f1a8212bef2b171c0f7a209d2ee893750cb74f6cb8a89766bd6a62c73d62de6c` | 같음 |
| `kor-travel-tokens-0.1.2.tgz` | `c6e2e27d716d5db7c9157f412cfd28d941536c032ce702a8cceb32f2a0c16253` | 같음 |
| `kor-travel-toast-0.1.1.tgz` | `30a5b2ee7b391791474addda15fe4ce629e820889f02010123273dd4f9cda222` | 같음 |
| `frontend-dependencies.json` | `6aba422cf160ca8935c26101a2575e6b56c02ea9c117e67194acc3f29ffc00aa` | 같음(파일 미변경) |

## PR CI(Node 26.13.1)

`common frontend` job([44192052315](https://github.com/digitie/kor-travel-common/actions/runs/44192052315))이 `node: v26.13.1`로 `npm ci --engine-strict`, `check:toolchain`("Node 26.13.1 / npm 12.0.1 도구 규칙 PASS"), `check:policy`, `test:toolchain`(90/90), 워크스페이스 시험을 통과했다. selftest의 `frontend-guard-pinned-ref`·`frontend guard (자기 ref와 어긋나면 실패)`도 통과했다.
