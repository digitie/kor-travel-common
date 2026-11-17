# T-022 UI·Python task 원장을 실물과 대조해 재분류

- 상태: READY
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 A(T-023·T-026·T-313과 동시 가능)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §1.3·§4.2(K-03)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

원장은 T-201(ui 골격)을 BLOCKED, T-302(Python 골격)를 READY, T-303~T-312를 BLOCKED로 두고 있다. 실물은 `@kor-travel/ui` 0.2.1(Radix 기반, T-218)과 `kortravelcommon` 0.1.0.dev0(T-319 계열 모듈)이다. 또 재조사의 판정 여럿이 accepted ADR·standards와 어긋난다(계획 문서 §1.5). 이 task는 T-201~T-214와 T-302~T-312를 실물·재조사 결과와 대조해 재분류하고, 어긋나는 판정을 ADR 초안으로 올린다. 코드와 standards 본문은 바꾸지 않는다(standards 반영은 T-027).

## 고정 결정

- 원장 문법과 상태 어휘는 [task 규칙](../tasks-rule.md)을 그대로 따른다. 새 상태를 만들지 않는다.
- 기존 결정은 지우지 않는다. [ADR-011](../adr/011-python-common-package.md)을 부분 대체하는 초안은 **ADR-020**으로 쓴다. ADR-019는 T-023이 쓴다. 두 task의 병합 순서가 바뀌어도 번호는 이대로다.
- 실물이 있다는 사실만으로 DONE으로 바꾸지 않는다. 해당 task의 수용 기준을 실물에서 하나씩 확인한 것만 DONE이다([task 규칙](../tasks-rule.md) §6).
- 계획 문서 §1.5의 판정은 제안이다. ADR-020이 accepted가 되기 전에는 기존 ADR·standards가 유효하다.

## 구현 범위

1. `docs/plan/`에 대조표 한 장을 추가한다: T-201~T-214, T-302~T-312 각 행에 실물 위치, 판정(실물로 충족 / 범위 재정의 / 철회 제안 / 그대로), 근거를 적는다.
2. ADR-020 초안: 계획 문서 §1.5 표의 **모든 행**(C1·C2·C3·C4·C5·C9·C10·C12·C13·C15·C18·C20, `validateForm`, UI 엔진 표기)을 결정 항목으로 옮기고 행마다 채택·기각·보류를 적을 자리를 둔다.
3. T-306을 나눈다: C7 `public_api_key`를 독립 task로 남기고, C1·C9는 ADR-020의 결정에 따른다. C8 `trusted_proxy`와 C11 `testing`이 든 T-308도 항목별로 나눈다. T-307은 request-id와 지표를 나눈다. T-304는 health 라우터와 time을 나눈다.
4. T-219·T-220과 겹치는 기존 task(T-203·T-205·T-206·T-208·T-209·T-210)의 범위를 겹치지 않게 다시 적는다. `ConfirmDialog`는 T-508에 그대로 둔다.
5. `docs/resume.md`·`docs/journal.md` 갱신.

## 범위 밖

패키지 코드, `versions.json`, 소비자 저장소, `docs/standards/*` 본문(T-027), 새 기능 task의 구현.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/plan/ledger-reality-2026-11.md            # 대조표(신규)
docs/adr/020-python-ui-scope-after-resurvey.md, docs/adr/README.md
docs/tasks.md, docs/tasks/T-2xx-*.md, docs/tasks/T-3xx-*.md
docs/resume.md, docs/journal.md
```

## 수용 기준

- [ ] 대조표에 T-201~T-214(14개 파일)와 T-302~T-312(12개 파일)가 한 행씩 빠짐없이 있다.
- [ ] 계획 문서 §1.5 표의 행 수와 ADR-020 초안의 결정 항목 수가 같다.
- [ ] T-306을 나눈 뒤 C7(`public_api_key`)만 가진 task가 원장에 있다.
- [ ] DONE으로 바꾼 task마다 수용 기준별 실물 근거(파일 경로 또는 PR 번호)가 상세 파일에 있다.
- [ ] `python3 -B -X utf8 tools/validate_plan.py`가 오류 0이고 READY task의 선행이 모두 DONE이다.
- [ ] ADR-020이 색인에 `proposed`로 등록돼 있고 ADR-011 본문은 지워지지 않았다.
- [ ] T-219·T-220과 범위가 겹치는 기존 task가 0개다(대조표의 '겹침' 열이 모두 해소).

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_plan_validation.py" -v
git diff --check
```

## evidence

PR 본문에 대조표 요약(판정별 개수)과 검증 출력. 이 파일 하단 '실행 기록'.

## rollback·release 차단 조건

- 문서 전용이라 `git revert` 1회로 원복된다.
- 수용 기준을 실물에서 확인하지 못한 task를 DONE으로 옮겼다면 병합하지 않는다.
