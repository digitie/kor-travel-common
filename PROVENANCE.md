# PROVENANCE

이 문서는 다른 저장소에서 common으로 옮겨 온 파일군의 원천·커밋·경로·라이선스·수정 여부를 파일군 단위로 기록한다(브리프 D-17, ADR-004; 형식은 `docs/survey/cross/licensing.md` §2.3). 확정 task는 T-003(★이번 PR). 파일 단위 표기는 각 파일의 SPDX 헤더 `Origin:`/`Derived-From:`/`Modified:` 행이 정본이고, 이 표는 그 색인이다. 마지막 갱신 2026-09-06.

## 규칙

1. 코드·문서·CSS를 다른 저장소에서 옮기기 **전에** 이 표에 행을 추가한다. 행이 없는 이식은 리뷰 `P0`(라이선스 위반 후보)다.
2. 원천 커밋은 40자 또는 7자 이상 short hash로 적고, 경로는 원천 저장소 상대 경로다. 여러 파일이면 디렉터리 + 개수.
3. 추출 규칙(D-17): GPL 원천(map·weather·airport)은 그대로 옮기고 `Origin:`을 남긴다. geo(`GPL-3.0-only`) 유래는 헤더에 `GPL-3.0-only`를 병기하고 권리자가 `-or-later`로 재선언하기 전까지 유지한다(O-20). MIT 원천(concierge·docker-manager)은 MIT 고지를 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md) 또는 헤더에 보존한다. shadcn CLI 생성물은 MIT 고지(`Derived-From: shadcn/ui`)를 단다.
4. 금지 원천: pinvi 전체(L6 결정 전, B1), pinvi 벤더 tgz·`maplibre-vworld-*` 소스(영구, B2), Hallmark `SKILL.md` 본문(B3), `python-*-api`·`python-kraddr-base` 코드(의존만). concierge `AppShell.tsx`·`globals.css`의 map 참조는 diff로 복사 여부를 확정한 뒤에만 기록한다(B4).
5. 수정 열에는 "없음" 또는 바꾼 점의 요약과 날짜를 적고, 원천이 바뀌어도 이 표의 기존 행은 고치지 않는다(재이식은 새 행).
6. 앱 사본과의 drift 비교는 선두 주석 블록(SPDX·Hallmark 스탬프)을 정규화한 뒤 수행한다(D-17).

## 표

| ID | common 파일군 | 원천 저장소 | 커밋 | 원천 경로 | 원천 라이선스 | 수정 | 근거 |
|---|---|---|---|---|---|---|---|
| PV-001 | `tools/validate_plan.py` | canview | `1f93b8adb34a48537db69b950c8a99ce89859760` | `tools/validate_plan.py` | GPL-3.0(원문, 버전 미지정) → common `GPL-3.0-or-later`(권리자 동일) | docstring 1줄("G0–G6 통과" → "gate 통과"), 파서·규칙 무변경 (2026-09-06) | `docs/survey/cross/canview-structure-checklist.md` §1.2 |
| PV-002 | `tools/validate_document_links.py` | canview | `1f93b8a` | `tools/validate_document_links.py` | 동상 | 대상 경로(`docs/`·`packages/`·`tools/`·`templates/`·`tests/`·루트) 변경, 절대 경로 링크를 오류로 판정, 공백 포함 target(산문)·inline code span 제외 — 사실상 재작성 (2026-09-06) | 동상 §1.2·§4.3 |
| PV-003 | `tests/test_plan_validation.py` | canview | `1f93b8a` | `tests/test_plan_validation.py` | 동상 | 모듈명 `canview_plan_validation` → `kor_travel_common_plan_validation`, tempdir prefix; 35 tests 무변경 (2026-09-06) | 동상 §1.2·§4.2 |
| PV-004 | `docs/reviews/adversarial/TEMPLATE.md` | canview | `1f93b8a` | `docs/reviews/adversarial/TEMPLATE.md` | 동상 | 없음(diff 0) | 동상 §1.2 |
| PV-005 | `docs/tasks-rule.md`, `docs/tasks-done.md`, `docs/tasks/README.md`, `docs/runbooks/README.md`, `docs/runbooks/documentation-maintenance.md`, `docs/runbooks/agent-failure-patterns.md`, `docs/reviews/README.md`, `.gitignore`, `.gitattributes` | canview | `1f93b8a` | 동일 경로 9개 | 동상 | 도메인 치환(ID 대역·5열 문법·standards 행·Node/Python ignore·전역 LF); 변경 줄 수는 checklist §1.2 표 | 동상 §1.2 |
| PV-006 | `docs/runbooks/agent-workflow.md`, `docs/resume.md`(5절 구조), `docs/journal.md`(항목 형식·검증 표), `CHANGELOG.md`(형식), `AGENTS.md`·`SKILL.md`·`docs/README.md`(절 구조) | canview | `1f93b8a` | `docs/runbooks/agent-workflow.md`, `docs/resume.md`, `docs/journal.md`, `CHANGELOG.md`, `AGENTS.md`, `SKILL.md`, `docs/README.md` | 동상 | 절 제목·규칙 어휘만 채택하고 본문은 kor-travel-common으로 전면 치환(2026-09-06) | 동상 §2·§3, `docs/survey/cross/docs-conventions.md` §3 |

현재 소비 저장소(map·weather·airport·geo·concierge·docker-manager·pinvi)에서 옮겨 온 코드는 **없다**. 첫 이식은 T-101(`packages/tokens`, map `globals.css` 값)과 T-203(`packages/ui`, map admin `components/ui/*` 레시피)이며, 그때 PV-007 이후 행과 SPDX 헤더를 함께 추가한다. `tools/check_spdx.py`(T-003 잔여)는 common 파일에 헤더가 없으면 즉시 fail한다.
