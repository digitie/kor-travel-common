# T-025 tarball 내장 정책 사본이 무관한 패키지 버전을 올리지 않게 분리

- 상태: BLOCKED
- 우선순위: P1
- Gate: 패키지 빌드·tarball 설치·2인 리뷰
- 선행: T-023
- 소유 저장소: kor-travel-common
- 병렬: 묶음 B

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§4.1(K-02)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

`ui`·`tokens`·`toast` tarball은 전체 정책 사본(`dependency-policy.json`)을 싣는다. 그래서 `vworld-map-web` 한 줄이 바뀐 날 실행 코드가 같은 세 패키지가 patch 버전을 올렸고, 지도가 없는 소비자도 재vendor했다. 이 task는 패키지 버전이 **그 패키지의 내용이 바뀔 때만** 오르게 한다.

## 고정 결정

- 방식은 ADR-019가 정한다. 후보: (가) tarball에서 정책 사본을 빼고 소비자 로컬 검사가 정책 파일 경로를 인자로 받는다, (나) 사본에 그 패키지 자신의 peer 범위만 남긴다.
- 소비자의 로컬 `check:dependencies`가 계속 동작해야 한다. 중앙 guard의 판정은 바뀌지 않는다.
- 이미 낸 버전(0.2.1·0.1.2·0.1.1)의 bytes는 바꾸지 않는다. 변경은 다음 버전부터다.

## 구현 범위

1. `packages/{ui,tokens,toast}`의 pack 구성과 `check-dependencies.mjs` 진입점을 결정에 맞게 바꾼다.
2. 소비자 로컬 검사 명령의 새 형태를 [frontend-libraries](../standards/frontend-libraries.md)에 적고 이관 절(`### Breaking` 여부 포함)을 CHANGELOG에 둔다.
3. 회귀: 정책에서 무관한 패키지 한 줄만 바꾼 뒤 세 패키지를 pack하면 tarball SHA-256이 이전과 같다.

## 범위 밖

정책 내용 자체, 중앙 guard workflow, 소비자 저장소.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/package.json, packages/tokens/package.json, packages/toast/package.json
packages/*/check-dependencies.mjs, packages/*/dependency-policy.json
tools/sync_frontend_policy.mjs
docs/standards/frontend-libraries.md, CHANGELOG.md
```

## 수용 기준

- [ ] 시험: `versions.json`의 `vworld-map-web` 축만 바꾸고 생성·pack했을 때 `ui`·`tokens`·`toast` tarball의 SHA-256이 바꾸기 전과 같다.
- [ ] 시험: pack한 tarball을 임시 프로젝트에 설치하고 문서에 적은 로컬 검사 명령이 통과한다.
- [ ] `npm run build --workspaces`·`npm test --workspaces`·`npm run check:policy`가 통과한다.
- [ ] 이관 절이 소비자가 바꿀 명령 한 줄을 전후로 보여 준다.

## 검증 명령

```bash
npm ci --engine-strict && npm run check:toolchain
npm run build --workspaces && npm test --workspaces
npm pack --workspace packages/ui --workspace packages/tokens --workspace packages/toast && sha256sum *.tgz
```

## evidence

정책 변경 전후 tarball SHA-256 표, 설치 스모크 출력. 소비자 채택은 `NOT_RUN(소비자 저장소)`.

## rollback·release 차단 조건

- `git revert` 1회. 새 버전을 아직 동결하지 않았다면 소비자 영향이 없다.
- 로컬 검사 명령이 바뀌는데 이관 절이 없으면 병합하지 않는다.
