# T-022 UI·Python task 원장을 실물과 대조해 재분류

- 상태: READY
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 A(T-023·T-026·T-313과 동시 가능)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §1.3·§4.2(K-03)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

원장은 T-201(ui 골격)을 BLOCKED, T-302(Python 골격)를 READY, T-303~T-312를 BLOCKED로 두고 있다. 실물은 `@kor-travel/ui` 0.2.1(Radix 기반, T-218)과 `kortravelcommon` 0.1.0.dev0(T-319 계열 모듈)이다. 원장이 실물보다 뒤에 있어 새 작업이 기존 task와 겹치는지 판정할 수 없다. 이 task는 T-201~T-214와 T-302~T-312를 실물·재조사 결과와 대조해 재분류한다. 코드는 바꾸지 않는다.

## 고정 결정

- 원장 문법과 상태 어휘는 [task 규칙](../tasks-rule.md)을 그대로 따른다. 새 상태를 만들지 않는다.
- 기존 결정은 지우지 않는다. 모듈 우선순위를 바꾸려면 [ADR-011](../adr/011-python-common-package.md)을 대체하는 새 ADR 초안을 같은 PR에 둔다(색인의 다음 번호 사용).
- 실물이 있다는 사실만으로 DONE으로 바꾸지 않는다. 해당 task의 수용 기준을 실물에서 하나씩 확인한 것만 DONE이다([task 규칙](../tasks-rule.md) §6).

## 구현 범위

1. `docs/plan/`에 대조표 한 장을 추가한다: T-201~T-214, T-302~T-312 각 행에 실물 위치, 판정(실물로 충족 / 범위 재정의 / 철회 제안 / 그대로), 근거를 적는다.
2. 재조사 판정을 반영한 ADR 초안: C1 settings·C9 db·C10 alembic 템플릿·C4 health 라우터·C5 errors·C3 metrics는 공유하지 않음, C13 time은 우선순위 낮춤, C2 request-id는 지표와 분리, UI 엔진 표기는 Radix.
3. 범위 재정의로 판정한 task의 상세 파일과 요약 행을 고친다. T-203·T-205·T-209·T-210은 T-219·T-220과 겹치지 않게 범위를 나눈다.
4. [ui-contract](../standards/ui-contract.md)의 엔진 표기(`@base-ui/react`)와 실물(`radix-ui`)의 불일치를 고칠 후속을 T-204에 명시한다.
5. `docs/resume.md`·`docs/journal.md` 갱신.

## 범위 밖

패키지 코드, `versions.json`, 소비자 저장소. 새 기능 task의 구현.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/plan/ledger-reality-2026-11.md            # 대조표(신규)
docs/adr/019-*.md 또는 020-*.md, docs/adr/README.md  # ADR-011 부분 대체 초안
docs/tasks.md, docs/tasks/T-2xx-*.md, docs/tasks/T-3xx-*.md
docs/resume.md, docs/journal.md
```

## 수용 기준

- [ ] 대조표에 T-201~T-214(14개 파일)와 T-302~T-312(12개 파일)가 한 행씩 빠짐없이 있다.
- [ ] DONE으로 바꾼 task마다 수용 기준별 실물 근거(파일 경로 또는 PR 번호)가 상세 파일에 있다.
- [ ] `python3 -B -X utf8 tools/validate_plan.py`가 오류 0이고 READY task의 선행이 모두 DONE이다.
- [ ] ADR 초안이 색인에 `proposed`로 등록돼 있고 ADR-011 본문은 지워지지 않았다.
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
