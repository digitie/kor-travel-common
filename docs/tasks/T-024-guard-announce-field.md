# T-024 프론트 정책 예고 필드 구현(옛 검사기 호환·검사기·생성기·정본 형식)

- 상태: BLOCKED
- 우선순위: P0
- Gate: 도구 단위·selftest workflow·2인 리뷰
- 선행: T-023
- 소유 저장소: kor-travel-common
- 병렬: 묶음 B(T-025와 동시 가능, 같은 파일을 건드리면 순차)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1(K-01)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

ADR-019가 예고 필드를 채택하면, 새 버전을 정책의 **추가 필드**에 먼저 싣고 현재 값은 그대로 둔다. 소비자가 고정한 옛 검사기는 현재 값만 읽으므로 계속 통과한다. 새 검사기는 '현재 묶음' 또는 '예고 묶음' 중 하나와 통째로 맞으면 통과시킨다. 채택이 끝난 뒤 별도 마감 PR이 현재 값을 새 버전으로 바꾼다. ADR이 다른 안을 고르면 이 task의 범위를 그 결정으로 고친 뒤 시작한다.

## 고정 결정

- 결정 정본은 T-023의 ADR-019다.
- 예고 필드가 없는 정책은 지금과 **같은 판정**을 낸다(동작 보존).
- 정본 파일에는 키를 추가만 한다. 소비자가 지금 고정한 검사기 세 판(`55a921b`, `9e16393`, `97f8ed9`)은 `policy.versions`·`policy.profiles`·`policy.forbidden`·`policy.artifactPackages`·`policy.patchedRadixPackages`와 `canonical.packages`만 읽는다. 이 키들의 뜻을 바꾸지 않는다.
- 날짜로 판정을 바꾸는 논리는 넣지 않는다. 창은 마감 PR이 닫는다.

## 구현 범위

1. `versions.json`의 npm 축에 선택 필드(예고 버전)를 둔다. `tools/sync_frontend_policy.mjs`가 `frontend-dependencies.json`에 예고 버전 표를 추가 키로 생성한다. 기존 `versions` 키는 현재 값 그대로다.
2. `frontend-artifacts.json`에 예고 산출물(버전·파일명·integrity)을 추가 키로 둔다. 기존 `packages` 키는 현재 값 그대로다.
3. `tools/check_frontend_dependencies.mjs`: 선언·tarball 파일명·lock·원장·중앙 정본 비교가 '현재 묶음 전부' 또는 '예고 묶음 전부'를 통과시킨다. 예고가 걸린 패키지에 대해 현재와 예고를 섞은 소비자(예: 원장은 예고, lock은 현재)는 거절한다.
4. `packages/ui`·`packages/tokens`의 생성 checker 사본을 같은 소스에서 다시 만든다(T-025가 사본 자체를 없애면 그 결정에 따른다).
5. [versions](../standards/versions.md)·[frontend-libraries](../standards/frontend-libraries.md)·[release](../runbooks/release.md)에 절차(정책 변경 PR은 예고로 시작하고, 소비자 채택 뒤 마감 PR이 현재 값을 바꾼다)를 반영한다.

## 범위 밖

패키지 실행 코드·CSS·공개 API. 소비자 저장소. 날짜 기반 만료. 마감 PR 자체(T-222).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
versions.json, frontend-dependencies.json, frontend-artifacts.json
tools/sync_frontend_policy.mjs, tools/check_frontend_dependencies.mjs
packages/ui/test/dependency-policy.node.test.mjs          # 정책 회귀 시험
docs/standards/versions.md, docs/standards/frontend-libraries.md, docs/runbooks/release.md
CHANGELOG.md, docs/journal.md
```

## 수용 기준

- [ ] 회귀 시험: 예고 필드가 없는 정책에서 기존 정책 시험 전체가 수정 없이 통과한다(동작 보존).
- [ ] 회귀 시험: 예고 필드가 든 정본을 **세 고정 검사기 각각**(커밋 `55a921b`, `9e16393`, `97f8ed9`의 `tools/check_frontend_dependencies.mjs`와, 뒤의 둘은 `tools/check_node_toolchain.mjs`도)으로 읽었을 때 현재 버전 소비자 fixture가 통과한다.
- [ ] 회귀 시험: 새 검사기에서 현재 버전 소비자와 예고 버전 소비자가 각각 통과하고, 혼합 소비자·예고에 없는 제3 버전·integrity만 다른 예고 버전이 실패한다.
- [ ] 회귀 시험: 예고 버전 소비자를 옛 검사기(`97f8ed9`)로 검사하면 실패한다는 것을 문서와 시험에 명시한다(채택 PR이 호출 SHA를 함께 올려야 하는 이유).
- [ ] `workflows-selftest`가 통과하고 `npm run check:policy`·`npm run test:toolchain`이 통과한다.

## 검증 명령

```bash
npm ci --ignore-scripts --engine-strict
npm run check:policy && npm run test:toolchain
npm test --workspace packages/ui      # dependency-policy 회귀 포함
python3 -B -X utf8 tools/validate_document_links.py && git diff --check
```

## evidence

시험 이름별 전후 결과, 세 고정 검사기별 통과 출력, selftest 실행 링크. 실제 소비자 채택은 `NOT_RUN(소비자 저장소)`로 남긴다.

## rollback·release 차단 조건

- `git revert` 1회로 검사기·생성기·정본이 이전 형식으로 돌아간다. 정본에 추가한 키는 옛 검사기가 읽지 않으므로 소비자 쪽 되돌리기는 없다.
- 동작 보존 시험이 하나라도 수정돼야 통과하거나 세 고정 검사기 중 하나라도 실패하면 병합하지 않는다.
