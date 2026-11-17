# T-221 admin-kit 0.1.0 동결과 선택형 산출물 등록

- 상태: BLOCKED
- 우선순위: P1
- Gate: 패키지 빌드·tarball 설치·정책 검사·2인 리뷰
- 선행: T-219, T-220
- 소유 저장소: kor-travel-common
- 병렬: 병렬 없음

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.3·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

`@kor-travel/admin-kit` 0.1.0을 얼리고 중앙 정책에 선택형 산출물로 더한다. 새 패키지라 직전 현재 값이 없다. 선언하지 않은 소비자는 어느 검사기에서도 영향이 없고, 선언한 소비자는 옛 검사기에서도 main 정책으로 검사된다.

## 고정 결정

- 기존 2단계(source PR → main push의 `packages` job artifact로 동결 PR)를 그대로 쓴다([release](../runbooks/release.md)).
- `versions.json`에 정확 버전 축을 더하고 `frontendPolicy.packages`·`artifactPackages`에 넣는다. 프로필의 `required`·`runtimeRequired`에는 넣지 않는다. 모바일 프로필의 `forbidden`에 넣는다(`@kor-travel/ui`와 같다).
- `frontend-artifacts.json`의 `sources`는 기존 패키지의 출처를 설명한다. 덮어쓰지 않고 이 패키지의 출처 커밋을 따로 더한다.
- 같은 버전의 bytes를 다시 만들지 않는다.
- 새 guard(T-024)를 쓰는 소비자는 자기가 고정한 커밋의 정책으로 검사받는다. 그 커밋이 이 task보다 앞이면 정책에 admin-kit이 없어 검사기가 건너뛴다. 그래서 이 task의 동결 병합 커밋을 **admin-kit 채택 커밋**으로 지정한다. 채택하는 소비자는 호출 SHA를 이 커밋으로 올리고 그 정책의 `ui`·`tokens` 값(T-025 판)으로 재vendor한다.

## 구현 범위

1. `packages/admin-kit` 버전 0.1.0, CHANGELOG.
2. `versions.json`·`frontend-dependencies.json`(생성)·`frontend-artifacts.json`·[frontend-libraries](../standards/frontend-libraries.md)의 생성 표.
3. 동결 PR: artifact의 tarball을 원장에 기록하고 SHA-256을 PR 본문에 적는다.
4. 소비자에게 알릴 것(벤더할 파일, `common-artifacts.json` 항목, 채택 task 번호)을 `docs/journal.md`와 [integration map](../integration-map.md)에 적는다.
5. 동결 병합 커밋을 admin-kit 채택 커밋으로 문서에 40자리로 적는다. T-024 채택 커밋과 이 커밋 사이에 더해진 검사 규칙을 목록으로 적는다(없으면 없다고 적는다).

## 범위 밖

소비자 채택(T-415·T-435·T-466).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/admin-kit/package.json, package-lock.json, CHANGELOG.md
versions.json, frontend-dependencies.json, frontend-artifacts.json, docs/standards/frontend-libraries.md
docs/journal.md, docs/resume.md, docs/integration-map.md
```

## 수용 기준

- [ ] 등록 뒤, admin-kit를 선언하지 **않은** 소비자 fixture(지금의 pinvi·docker-manager 모양)가 두 고정 검사기(`55a921b`, `97f8ed9`)와 최신 검사기에서 통과한다.
- [ ] admin-kit를 선언한 소비자 fixture가 두 고정 검사기와 최신 검사기에서 통과한다(옛 검사기도 main 정책에서 새 산출물을 읽는다).
- [ ] `ui`·`tokens`·`toast`의 정책 값과 tarball SHA-256이 이 PR 전과 같다.
- [ ] PR head와 main push artifact의 admin-kit tarball SHA-256이 같다.
- [ ] 새 guard fixture: 호출 ref가 이 task 이전이면 선언된 admin-kit을 건너뛰고(대조 없음), admin-kit 채택 커밋이면 중앙 정본과 대조한다(시험).
- [ ] admin-kit 채택 커밋과, T-024 채택 커밋 뒤에 더해진 검사 규칙 목록이 문서에 있다.

## 검증 명령

```bash
npm ci --engine-strict && npm run build --workspaces && npm test --workspaces
npm run check:policy
npm pack --workspace packages/admin-kit && sha256sum kor-travel-admin-kit-0.1.0.tgz
```

## evidence

tarball SHA-256, 검사기 세 판별 두 fixture의 통과 출력, artifact 링크.

## rollback·release 차단 조건

- 어느 소비자도 채택하기 전이면 등록 PR을 revert한다.
- 채택한 소비자가 생긴 뒤에는 정책에서 빼지 않는다(빼면 채택한 소비자가 실패한다). 다음 patch로 고친다.
