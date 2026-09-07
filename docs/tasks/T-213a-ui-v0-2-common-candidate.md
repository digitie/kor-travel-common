# T-213a UI `v0.2.0` common 검증 후보 보존

- 상태: BLOCKED
- 우선순위: P1
- Gate: UI 타입·단위·접근성·pack 설치·계약 대조·2인 적대적 리뷰
- 선행: T-208, T-209, T-210, T-212a

## 목표

외부 소비자 채택이나 정식 릴리스에 의존하지 않고 UI `v0.2.0` 전체 common 구현 후보를 검증·보존한다. 이 task가 보존한 불변 후보는 공용 로그인 위젯(T-214)과 외부 rc·정식 릴리스(T-213)가 같은 검증 소스를 사용하게 한다.

## 고정 결정

- [ADR-014](../adr/014-common-implementation-without-registry-publishing.md)의 후보 보존·구현/외부 릴리스 분리와 [release §2.1](../runbooks/release.md#21-common-후보-보존과-후속-구현)을 따른다.
- npm/PyPI에 게시하지 않는다. 후보 tag·tarball은 common 내부 검증과 고정 Git/tarball 설치를 위한 것이며 소비자 채택·정식 Release를 뜻하지 않는다.
- `candidate-ui-0.2.0-<N>`은 T-208~T-210 구현과 T-212a의 common 후보를 포함한 실제 40자리 source commit에만 붙인다. T-212의 외부 소비자 evidence나 T-213의 정식 자산은 이 task의 선행이 아니다.

## 구현 범위

1. T-208·T-209·T-210의 공개 API·마크업·접근성·시험을 T-204 계약과 대조하고, T-212a 후보의 pack/고지 입력을 확인한다.
2. `packages/ui`의 `v0.2.0-dev.0` source를 빌드·타입 검사·unit/a11y·pack 설치 fixture로 검증한다. webpack·Turbopack smoke와 tokens tarball 입력은 실제 실행 결과로만 기록한다.
3. 같은 source와 도구로 산출물을 두 번 빌드해 digest를 대조하고, source commit·lock·툴체인·시험 수·CI artifact·만료를 evidence에 남긴다.
4. 검증한 merge commit에 불변 annotated tag `candidate-ui-0.2.0-<N>`을 보존하고 tag object와 peeled commit을 재확인한다. 후보 보존 뒤 외부 rc·정식은 T-213이 별도로 준비한다.

## 범위 밖

소비자 저장소 수정·설치·빌드·e2e·권리 gate, T-212의 `ui-v0.1.0` 정식, T-213의 rc·정식 GitHub Release, npm/PyPI 게시, 로그인 위젯 자체 구현(T-214), 레지스트리 채널(T-211).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/ui/**
packages/tokens/** (fixture 설치 입력만, tokens 소스 변경은 별도 task)
CHANGELOG.md
docs/reviews/adversarial/YYYY-MM-DD-ui-v0-2-common-candidate.md
docs/reviews/adversarial/evidence/YYYY-MM-DD-ui-v0-2-common-candidate-reviewer-{a,b}.md
docs/journal.md  docs/resume.md
```

## 수용 기준

- T-208·T-209·T-210의 공개 exports·props·`data-slot`·testid·sr-only 문구가 ui-contract와 일치하고 계약 시험이 통과한다.
- unit/axe·TypeScript·pack 설치·webpack/Turbopack smoke가 0 test·skip 없이 성공한다. 실행하지 못한 소비자 검증은 `NOT_RUN(소비자 저장소 미수정)`으로 둔다.
- 두 빌드 digest가 같고 후보 annotated tag object ID는 로컬·원격 조회값으로 기록해 일치시킨다. tag의 peeled commit만 검증한 40자리 source commit과 같아야 하며 tag object ID 자체는 별도 값이다. tag는 이동·덮어쓰지 않는다.
- 두 reviewer가 P0/P1 finding 없이 승인하고 문서·plan·diff gate가 통과한다. T-213은 이 evidence와 T-212 외부 evidence를 사용해 별도로 진행한다.

## 검증 명령

```bash
npm run build -w packages/ui
npx tsc --noEmit -p packages/ui
npm run test -w packages/ui
npm pack -w packages/ui --pack-destination dist/candidate
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
git diff --check
```

실제 패키지 스크립트·a11y·fixture 명령은 T-201~T-210에서 확정한 명령을 사용하며 존재하지 않는 명령을 성공으로 기록하지 않는다.

## evidence

후보 source commit·tag object/peeled commit·두 digest·도구/CI 버전·시험 수/skip·pack 목록·artifact 만료와 외부 gate의 `NOT_RUN`을 `docs/journal.md`와 리뷰 report에 기록한다.

## rollback 또는 release 차단 조건

공개 계약·고지·digest·tag 정합성·필수 리뷰가 깨지면 후보를 DONE으로 바꾸지 않는다. 결함은 후보 번호를 올려 재검증하고 기존 tag를 이동하지 않는다. 외부 소비자 증거가 없다는 이유로 이 내부 후보를 정식 릴리스로 표시하지 않는다.
