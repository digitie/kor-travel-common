# T-024 프론트 정책 전환 창 구현(검사기·생성기·정본 형식)

- 상태: BLOCKED
- 우선순위: P0
- Gate: 도구 단위·selftest workflow·2인 리뷰
- 선행: T-023
- 소유 저장소: kor-travel-common
- 병렬: 묶음 B(T-025와 동시 가능, 같은 파일을 건드리면 순차)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1(K-01)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

ADR-019가 전환 창을 채택하면, 정책이 바뀐 날 모든 소비자의 guard가 실패하지 않도록 직전 버전을 만료일까지 함께 통과시킨다. 만료 뒤에는 지금과 같이 현재 버전만 통과한다. ADR이 다른 안을 고르면 이 task의 범위를 그 결정으로 고친 뒤 시작한다.

## 고정 결정

- 결정 정본은 T-023의 ADR-019다.
- 직전 버전 정보가 없는 정책은 지금과 **같은 판정**을 낸다(동작 보존).
- 정본 파일에는 키를 추가만 한다. 호출 SHA를 올리지 않은 소비자의 옛 검사기가 새 정본을 읽고 실패하면 안 된다.

## 구현 범위

1. `versions.json`의 npm 축에 선택 필드(직전 정확 버전)와 전환 만료일을 둔다. `tools/sync_frontend_policy.mjs`가 `frontend-dependencies.json`에 직전 버전 표와 만료일을 생성한다.
2. `frontend-artifacts.json`에 직전 산출물(버전·파일명·integrity)과 만료일을 둔다.
3. `tools/check_frontend_dependencies.mjs`: 선언·tarball 파일명·lock·원장·중앙 정본 비교가 '현재 또는 (만료 전) 직전'을 통과시킨다. 한 소비자 안에서 현재와 직전을 섞는 조합(예: 원장은 현재, lock은 직전)은 거절한다.
4. 만료일이 지난 직전 버전은 거절하고 메시지에 만료일을 적는다. 날짜는 UTC 기준, 시험에서는 주입한다.
5. `packages/ui`·`packages/tokens`의 생성 checker 사본을 같은 소스에서 다시 만든다(T-025가 사본 자체를 없애면 그 결정에 따른다).
6. [versions](../standards/versions.md)·[frontend-libraries](../standards/frontend-libraries.md)·[release](../runbooks/release.md)에 절차(정책 변경 PR은 직전 버전과 만료일을 함께 적는다)를 반영한다.

## 범위 밖

패키지 실행 코드·CSS·공개 API. 소비자 저장소. 만료일의 자동 연장.

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

- [ ] 회귀 시험: 직전 정보가 없는 정책에서 기존 정책 시험 전체가 수정 없이 통과한다(동작 보존).
- [ ] 회귀 시험: 2026-11-17 상황을 재현한 fixture(정책 `ui` 0.2.1 + 직전 0.2.0, 소비자는 0.2.0)가 만료 전 통과, 만료 뒤 실패한다.
- [ ] 회귀 시험: 현재·직전 혼합 소비자, 두 세대 전 버전, integrity만 다른 직전 버전이 모두 실패한다.
- [ ] 회귀 시험: 새 키가 든 정본을 **직전 릴리스의 검사기**(커밋 `97f8ed9`의 `tools/check_frontend_dependencies.mjs`)로 읽어도 현재 버전 소비자가 통과한다.
- [ ] `workflows-selftest`가 통과하고 `npm run check:policy`·`npm run test:toolchain`이 통과한다.

## 검증 명령

```bash
npm ci --ignore-scripts --engine-strict
npm run check:policy && npm run test:toolchain
npm test --workspace packages/ui      # dependency-policy 회귀 포함
python3 -B -X utf8 tools/validate_document_links.py && git diff --check
```

## evidence

시험 이름별 전후 결과(수정 전 실패 → 수정 후 통과), selftest 실행 링크. 실제 소비자 채택은 `NOT_RUN(소비자 저장소)`로 남긴다.

## rollback·release 차단 조건

- `git revert` 1회로 검사기·생성기·정본이 이전 형식으로 돌아간다. 정본에 추가한 키는 옛 검사기가 무시하므로 소비자 쪽 되돌리기는 없다.
- 동작 보존 시험이 하나라도 수정돼야 통과한다면 병합하지 않는다.
