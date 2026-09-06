# T-508 보류 항목 재평가(api-client-core·pagination 코덱·VirtualTable 흡수·ConfirmDialog API·토스트·전면 레지스트리)

- 상태: BLOCKED
- 우선순위: P3
- Gate: 2인 리뷰
- 선행: T-213, T-310

## 목표

Phase 0 브리프가 "보류"로 판정한 6개 후보를 ui v0.2(T-213)·py v0.1(T-310) 채택 뒤의 사실(소비 현황·중복 구현 수·우회 패치 수)로 재평가하고, 항목마다 `채택(새 task)/계속 보류(다음 재평가 조건)/폐기` 중 하나로 판정한다. 판정은 2인 리뷰를 거치며, 채택은 새 task와(구조적이면) ADR로만 효력을 가진다.

## 고정 결정

- `api-client-core`는 만들지 않고 Phase 5 재평가; `cm` §2.3 ApiError 4형: 브리프 D-01, ADR-001([ADR 색인](../adr/README.md)).
- Python 보류 모듈 C6 pagination·C14 geo_primitives·C19 cli.mutex·C21 백업 규약: 브리프 D-15, [backend-stack](../standards/backend-stack.md). 이 task는 C6만 재평가(C14는 좌표 경계 상수 공통화 금지로 종결, C19·C21은 근거 약함).
- DataTable에 검색 툴바·`rowHeader` 미포함, geo `VirtualTable` 잔류: 브리프 D-09, [ui-contract](../standards/ui-contract.md).
- 토스트·모달 엔진은 앱 소유, 정책(UX-G4.1)과 행동 계약만 common: 브리프 D-09·D-13, [ux-guide](../standards/ux-guide.md).
- 전면 shadcn 레지스트리는 "npm 소비자 우회 패치 2회 이상"일 때만 재검토; 셸·템플릿 채널(T-211)은 별도: 브리프 D-10·D-28, ADR-007.
- 근거: `docs/survey/cross/ui-components.md` §4.3(보류 사유: ConfirmDialog API 4종, VirtualTable 13 소비 파일·`as="table"` 26회)·§7 Q4·Q5·Q8, `docs/survey/cross/ux-patterns.md` C7·C8·C18(확인 다이얼로그·토스트·모달 엔진), `docs/survey/cross/backend.md` §3 C6(cursor 인코딩 3형), `docs/survey/commonality-matrix.md` §2.3(ApiError 4형), 선행 보고서 §10 단계 3·5(복합 UI 흡수·범위 축소 조건; `docs/survey/README.md` §2.2 참조).

## 구현 범위

1. 재평가 문서 `docs/plan/deferred-items-reevaluation.md`. 항목마다 (보류 사유 원문 인용 절) / (재평가 시점 사실: 소비 앱 수·중복 구현 파일·우회 패치 수·관련 e2e 계약) / (재평가 기준 충족 여부) / (판정) / (후속: 새 task ID 후보·ADR 필요 여부·다음 재평가 조건).
2. 재평가 기준(후보; 브리프에 있는 것은 사실로 표기): ① api-client-core — typegen 채택 앱 수·ApiError 동형 유지 앱 수 ② pagination 코덱 — 동일 cursor 방식을 요구하는 소비자 수(현재 keyset/cursor/offset 3형) ③ VirtualTable — T-444(geo ui v0.2) 후 geo 잔류 파일 수·DataTable 4상태 계약과의 차이 ④ ConfirmDialog — 4앱 API를 D-13 행동 계약(동사 라벨 필수·`window.confirm` 금지)으로 수렴 가능한지 ⑤ 토스트 — 엔진 통일을 요구하는 앱 수·`onNotify` 주입(T-209)으로 충분한지 ⑥ 전면 레지스트리 — `tools/ui_drift.py` 우회 패치 수 ≥2(브리프 D-10, 사실).
3. 채택 항목은 [tasks-rule](../tasks-rule.md) §2 대역에 맞는 새 task 파일 초안(상태 BLOCKED)과 `docs/tasks.md` 요약 행을 같은 PR에 추가. 구조 변경(패키지 추가·배포 방식)은 ADR 초안.
4. 2인 리뷰([review archive](../reviews/README.md) 규칙; 리뷰어 영역: UI 계약 / 백엔드 계약).

## 범위 밖

- 판정 결과의 구현(새 task).
- `VirtualTable`·`ConfirmDialog` 코드 이관 자체, 토스트 엔진 선정.
- C14·C19·C21 재평가(각각 D-15에서 종결·근거 약함; 필요하면 T-506 감사에서 신호 수집).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/plan/deferred-items-reevaluation.md   (신설)
docs/tasks/T-NNN-<slug>.md, docs/tasks.md  (채택 항목만; ID는 tasks-rule §2 대역)
docs/adr/NNN-<slug>.md, docs/adr/README.md (구조 변경 채택 시만)
docs/reviews/adversarial/YYYY-MM-DD-deferred-items.md (+ evidence 2파일)
docs/journal.md, docs/resume.md, docs/tasks/T-508-deferred-items-reevaluation.md
```

## 수용 기준

- 6항목 모두 보류 사유 원문 절 번호·재평가 사실·기준 충족 여부·판정·후속이 있다. 사실 수집이 안 된 항목은 `NOT_RUN(사유)`로 표기하고 판정을 `계속 보류`로 둔다.
- 우회 패치 수는 `tools/ui_drift.py` 출력(또는 `NOT_RUN`과 grep 대체·한계)으로 뒷받침된다.
- ApiError·cursor·ConfirmDialog·토스트의 앱별 현황 표가 소비자 체크아웃 커밋 SHA와 함께 있다(읽기 전용 조사).
- 채택 판정마다 새 task 파일·요약 행이 같은 PR에 있고 `validate_plan.py`가 통과한다. 폐기 판정은 근거와 "재개 조건 없음"을 명시한다.
- 2인 리뷰 report와 disposition이 있고 P0/P1 미해결이 없다.
- 두 validator가 통과한다.

## 검증 명령

```bash
python3 -B -X utf8 tools/ui_drift.py --pins consumers.pins.json
rg -n "class ApiError|ApiError\b" <consumer-checkout>/*/frontend/src <consumer-checkout>/*/apps/web -g '*.ts' -g '*.tsx' | wc -l
rg -n "window\.confirm\(" <consumer-checkout> -g '*.tsx' -g '*.ts' | wc -l
rg -n "ConfirmDialog" <consumer-checkout> -g '*.tsx' -l
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

소비자 체크아웃은 읽기 전용이며 결과는 커밋 SHA와 함께 재평가 문서에 옮겨 적는다. Git Bash에서 동일하게 실행한다.

## evidence

- 재평가 문서 §"수집 로그"(명령·출력 요약·체크아웃 SHA·실행일)와 리뷰 report·evidence 2파일.
- `docs/journal.md` 최신 항목에 NOT_RUN 목록·도구 버전.

## rollback 또는 release 차단 조건

- 문서 task이므로 코드 rollback은 없다. 판정이 뒤집히면 재평가 문서를 덮어쓰지 않고 새 절(날짜)로 추가한다.
- 2인 리뷰에서 P0/P1이 열려 있으면 채택 판정의 새 task를 `docs/tasks.md`에 넣지 않는다.
- 전면 레지스트리는 우회 패치 ≥2 evidence 없이 채택하지 않는다(D-10).
