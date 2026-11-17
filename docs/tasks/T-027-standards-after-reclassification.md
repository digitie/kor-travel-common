# T-027 재분류 결정을 표준 문서에 반영(backend-stack·openapi·ci-deploy·ui-contract)

- 상태: BLOCKED
- 우선순위: P1
- Gate: 문서 검증·2인 리뷰
- 선행: T-022
- 외부 선행: 없음. ADR-020(소유자의 행별 결정)은 2026-11-17 accepted다([ADR-020](../adr/020-python-ui-scope-after-resurvey.md)). 남은 선행은 T-022다
- 소유 저장소: kor-travel-common
- 병렬: T-022 뒤. T-219와 동시 가능

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §1.5·§4.2(K-03)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

T-022의 ADR-020이 accepted가 되어도 `docs/standards/backend-stack.md`의 BE 규칙과 다른 standards는 철회된 모듈을 계속 요구한다. 결정된 항목만 standards 본문에 옮긴다.

## 고정 결정

- ADR-020이 채택한 항목만 고친다. 기각·보류한 항목의 규칙은 그대로 둔다.
- standards는 비면제 대상이라 두 리뷰어의 독립 리뷰를 거친다(`AGENTS.md` §5).
- 규칙을 지울 때는 규칙 ID를 재사용하지 않고 '철회(ADR-020)'로 남긴다.

## 구현 범위

1. [backend-stack](../standards/backend-stack.md): BE-6~BE-11(C20), BE-12(C1), BE-13(C2), BE-14(C3), BE-15(C4), BE-16(C5), BE-17(C16·C17), BE-19(C13), BE-20(C15), BE-21(C18), BE-23(C9), BE-24(C10)와 §8 모듈 표·§8.1 앱별 표·§10 금지 목록을 ADR-020 결정대로 고친다.
2. [openapi](../standards/openapi.md)의 export drift 행과 health 규칙(M5), [ci-deploy](../standards/ci-deploy.md)의 `python-quality.yml`·`openapi-drift.yml` 절을 같은 결정에 맞춘다.
3. [ui-contract](../standards/ui-contract.md): 엔진 표기를 실물(Radix)로, §4의 부품 표를 실물과 T-219·T-220 범위에 맞춘다. `ConfirmDialog`·`validateForm` 행은 결정대로 둔다.
4. [packages](../architecture/packages.md) §4의 모듈 우선순위 표를 동기화한다.
5. CHANGELOG에 규약 변경 절을 둔다.

## 범위 밖

코드, task 원장(T-022), 새 규칙 추가.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/standards/backend-stack.md, docs/standards/openapi.md, docs/standards/ci-deploy.md, docs/standards/ui-contract.md
docs/architecture/packages.md, CHANGELOG.md, docs/journal.md
```

## 수용 기준

- [ ] ADR-020의 채택 항목마다 고친 standards 위치(문서·규칙 ID)가 PR 본문 표에 있다.
- [ ] standards에 ADR-020이 철회한 모듈을 MUST로 요구하는 문장이 남아 있지 않다(규칙 ID별 확인표).
- [ ] `tools/validate_document_links.py` 오류 0, `tests/test_frontend_policy_docs.py` 통과.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_frontend_policy_docs.py" -v
git diff --check
```

## evidence

PR 본문의 규칙 ID별 확인표와 두 리뷰 report.

## rollback·release 차단 조건

- 문서 전용. `git revert` 1회.
- ADR-020이 accepted가 아니면 병합하지 않는다.
