# T-221 ui 0.3.0 단일 후보를 예고로 동결

- 상태: BLOCKED
- 우선순위: P1
- Gate: 패키지 빌드·tarball 설치·consumer-smoke·2인 리뷰
- 선행: T-219, T-220, T-024, T-025
- 소유 저장소: kor-travel-common
- 병렬: 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.3·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

T-219·T-220의 부품을 **한 버전**으로 낸다. 부품마다 버전을 올리지 않는다. 정책에는 0.3.0을 예고 필드에 싣고 현재 값 0.2.1은 그대로 둔다(T-024). 그래서 어느 검사기를 고정한 소비자도 동결 시점에 실패하지 않는다.

## 고정 결정

- 기존 2단계(source PR → main push의 `packages` job artifact로 동결 PR)를 그대로 쓴다([release](../runbooks/release.md)).
- 현재 값은 바꾸지 않는다. 현재 값 전환은 소비자 채택 뒤 T-222가 한다(ADR-019).
- T-025가 `tokens`·`toast`도 함께 올리기로 정했으면 같은 후보에 넣는다. 소비자가 재vendor를 한 번만 하게 한다.
- 같은 버전의 bytes를 다시 만들지 않는다.

## 구현 범위

1. `packages/ui` 버전 0.3.0(과 T-025가 정한 `tokens`·`toast` 버전), CHANGELOG(추가 부품 목록, Breaking 없음 확인).
2. `versions.json`·`frontend-dependencies.json`·`frontend-artifacts.json`에 예고 값을 추가한다. 현재 값은 그대로다.
3. 동결 PR: artifact의 tarball을 예고 산출물로 기록하고 SHA-256을 PR 본문에 적는다.
4. 소비자에게 알릴 것(채택 PR이 할 일: 호출 SHA를 T-024 이후 커밋으로 + 재vendor, 채택 task 번호, 마감 예정일)을 `docs/journal.md`와 [integration map](../integration-map.md)에 적는다.

## 범위 밖

소비자 재vendor·부품 채택(T-415·T-424·T-435·T-466·T-474), 현재 값 전환(T-222).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/package.json, package-lock.json, CHANGELOG.md
versions.json, frontend-dependencies.json, frontend-artifacts.json
docs/journal.md, docs/resume.md, docs/integration-map.md
```

## 수용 기준

- [ ] 동결 직후, 0.2.1을 벤더한 소비자 fixture가 **세 고정 검사기**(`55a921b`, `9e16393`, `97f8ed9`)와 최신 검사기 모두에서 통과한다.
- [ ] 0.3.0을 벤더한 소비자 fixture가 최신 검사기에서 통과한다.
- [ ] PR head와 main push artifact의 tarball SHA-256이 같다.
- [ ] CHANGELOG에 `### Breaking`이 없거나, 있다면 이관 절이 있다.

## 검증 명령

```bash
npm ci --engine-strict && npm run build --workspaces && npm test --workspaces
npm run check:policy
npm pack --workspace packages/ui && sha256sum kor-travel-ui-0.3.0.tgz
```

## evidence

tarball SHA-256, 검사기 네 판별 fixture 통과 출력, artifact 링크와 마감 예정일.

## rollback·release 차단 조건

- 동결 전이면 source PR revert. 동결 뒤에는 예고 필드를 지우는 PR로 되돌린다(현재 값이 그대로라 소비자 영향이 없다).
- 세 고정 검사기 중 하나라도 0.2.1 fixture를 실패시키면 동결하지 않는다.
