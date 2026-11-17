# T-221 ui 0.3.0 단일 후보 동결과 전환 창 공지

- 상태: BLOCKED
- 우선순위: P1
- Gate: 패키지 빌드·tarball 설치·consumer-smoke·2인 리뷰
- 선행: T-219, T-220, T-024
- 소유 저장소: kor-travel-common
- 병렬: 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.3·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

T-219·T-220의 부품을 **한 버전**으로 낸다. 부품마다 버전을 올리지 않는다. 전환 창(T-024)을 써서 소비자가 같은 날 실패하지 않게 한다.

## 고정 결정

- 기존 2단계(source PR → main push의 `packages` job artifact로 동결 PR)를 그대로 쓴다([release](../runbooks/release.md)).
- 정책에는 현재 0.3.0과 직전 0.2.1을 만료일과 함께 적는다(ADR-019).
- 같은 버전의 bytes를 다시 만들지 않는다.

## 구현 범위

1. `packages/ui` 버전 0.3.0, CHANGELOG(추가 부품 목록, Breaking 없음 확인).
2. `versions.json`·`frontend-dependencies.json`·`frontend-artifacts.json`에 현재·직전·만료일.
3. 동결 PR: artifact의 tarball을 `frontend-artifacts.json`에 기록하고 SHA-256을 PR 본문에 적는다.
4. 소비자에게 알릴 것(만료일, 재vendor할 파일, 채택 task 번호)을 `docs/journal.md`와 [integration map](../integration-map.md)에 적는다.

## 범위 밖

소비자 재vendor·부품 채택(T-415·T-466·T-435).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/package.json, package-lock.json, CHANGELOG.md
versions.json, frontend-dependencies.json, frontend-artifacts.json
docs/journal.md, docs/resume.md, docs/integration-map.md
```

## 수용 기준

- [ ] 동결 직후, **0.2.1을 벤더한 소비자 fixture**가 최신 검사기로 통과한다(전환 창 동작).
- [ ] PR head와 main push artifact의 tarball SHA-256이 같다.
- [ ] CHANGELOG에 `### Breaking`이 없거나, 있다면 이관 절이 있다.
- [ ] 만료일이 동결일로부터 ADR-019가 정한 기간 이상이다.

## 검증 명령

```bash
npm ci --engine-strict && npm run build --workspaces && npm test --workspaces
npm run check:policy
npm pack --workspace packages/ui && sha256sum kor-travel-ui-0.3.0.tgz
```

## evidence

두 tarball SHA-256, 0.2.1 fixture의 guard 통과 출력, artifact 링크와 만료일.

## rollback·release 차단 조건

- 동결 전이면 source PR revert. 동결 뒤에는 버전을 내리지 않고 0.3.1로 고친다.
- 0.2.1 소비자 fixture가 실패하면 동결하지 않는다.
