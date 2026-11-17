# T-029 공통 Node 도구 축을 최신 LTS(26.13.1)로 올림

- 상태: BLOCKED
- 우선순위: P2
- Gate: 도구 단위·패키지 빌드·2인 리뷰
- 선행: T-024, T-025
- 외부 선행: T-424·T-474 병합. T-467·T-436은 병합됐거나 weather·transport 팀이 당일 Node 갱신을 확인함. geo·concierge에는 병합 예정일 공지(두 저장소의 작업은 선행이 아니다)
- 소유 저장소: kor-travel-common
- 병렬: T-024·T-025 뒤(같은 정책 파일을 고치고, T-025 전이면 이 변경이 세 패키지를 다시 pack하게 만든다). T-417의 선행

출처는 [ADR-019](../adr/019-frontend-policy-guard-model.md) 결정 5·9와 [T-416](T-416-map-exact-node-npm-pin-decision.md)의 소유자 결정(2026-11-17)이다.

## 목표

소유자는 2026-11-17에 Map의 정확 Node 핀을 "최신 버전"으로 정했다. 그날 nodejs.org 공식 릴리스 색인(`https://nodejs.org/dist/index.json`)에서 가장 새 LTS 줄은 26(Lithium)이고 그 최신 patch는 26.13.1(2026-11-10, 보안 릴리스, 동봉 npm 11.20.0)이다. 색인의 가장 새 항목은 `v27.0.0-alpha.0.1.1`(alpha)이라 운영 핀 대상이 아니다. 공통 축(`axes.node.recommended`)은 22.23.1이다. Map이 새 guard로 옮기려면([T-417](T-417-map-guard-ref-toolchain.md)) 그 ref의 축이 26.13.1이어야 한다. 이 task는 공통 축을 26.13.1로 올리고 그 병합 커밋을 Map이 고정할 커밋으로 적는다.

## 고정 결정

- 축을 읽는 자리는 ADR-019다. 새 guard 소비자는 ref를 올릴 때만 이 값을 받는다. 옛 판(`main`을 읽는 판)을 호출하는 소비자는 병합 당일 실패하므로 외부 선행을 확인한 뒤 병합한다.
- npm 축은 12.0.1 그대로다(Node 26 동봉 npm 11.20.0으로 내리지 않는다). npm 12.0.1의 `engines.node`는 `^22.22.2 || ^24.15.0 || >=26.0.0`이라 Node 26.13.1을 받는다.
- `floor`(호환 하한)는 바꾸지 않는다. 정확 선택값만 바꾼다(ADR-018).
- Node 이미지의 배포판·libc는 각 앱이 유지한다. 공통 축의 `image`는 `node:26.13.1-bookworm-slim`이다.

## 구현 범위

1. `versions.json`의 `axes.node.recommended`를 `26.13.1`, `image`를 `node:26.13.1-bookworm-slim`으로 바꾸고 생성물(`tools/sync_frontend_policy.mjs`의 출력)을 다시 만든다.
2. common 자신의 private anchor(루트 `.nvmrc`, `package.json`의 `engines.node`, workflow의 `node-version`)를 같은 값으로 바꾼다. 재사용 guard가 검사기를 실행할 때 쓰는 Node도 T-024의 구현에 맞춰 `common-ref`의 축을 따르게 한다.
3. T-025 뒤이므로 이 변경이 `ui`·`tokens`·`toast`를 다시 pack하게 만들지 않아야 한다(T-025의 수용 기준). 다시 pack되면 멈추고 T-025의 결함으로 고친다.
4. 병합 커밋을 40자리로 문서([integration map](../integration-map.md), T-417)에 적는다. Map이 T-417에서 고정할 커밋이다.

## 범위 밖

소비자 저장소의 Node 갱신(각 저장소가 ref를 올리는 PR에서 한다), npm 축 변경, Map의 핀(T-416이 Map PR로 한다).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
versions.json, frontend-dependencies.json
.nvmrc, package.json, package-lock.json
.github/workflows/*.yml(node-version)
docs/standards/versions.md, docs/integration-map.md, CHANGELOG.md, docs/journal.md
```

## 수용 기준

- [ ] `npm ci --engine-strict && npm run check:toolchain`이 Node 26.13.1·npm 12.0.1에서 통과한다.
- [ ] `npm run check:policy`·`npm run test:toolchain`·`npm test --workspaces`가 통과한다.
- [ ] `ui`·`tokens`·`toast` tarball SHA-256이 바꾸기 전과 같다.
- [ ] 병합 PR 본문에 외부 선행 각 항목의 상태와 근거 링크가 있다.
- [ ] 병합 커밋이 40자리로 integration map과 T-417에 있다.

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
