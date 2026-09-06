# T-004 ADR-001~012 + `docs/adr/README.md` 단일 색인

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 2인 리뷰
- 선행: 없음

## 목표

브리프 §1의 확정 결정을 canview ADR 형식 12편으로 고정하고, `docs/adr/README.md`를 단일 색인(다음 후보 번호 명시)으로 둔다. 이번 PR에서 산출되며 2인 리뷰 통과 후 coordinator가 `DONE` 처리한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) §4 ADR 목록(번호·제목·상태·핵심 결정)과 D-02(`decisions.md` 미보유, `adr/README.md` 단일 색인, 다음 후보 번호 명시).
- 형식은 [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §3.2 R2.1~R2.10: 파일당 1개 `NNN-<slug>.md`, H1 `# ADR-NNN: 제목`, 머리 불릿 `상태`·`날짜` 필수, 상태 어휘 `accepted`/`proposed`/`superseded by ADR-XXX`, 본문 컨텍스트 → 결정 → 결과.
- [문서 유지보수 runbook](../runbooks/documentation-maintenance.md) §3(뒤집을 때 새 ADR·옛 ADR 유지·번호 갱신)과 [문서 규약 비교](../survey/cross/docs-conventions.md) §2 C8(001부터, 타 저장소 번호 미러 금지).
- 열린 결정은 본문에 "열림(사용자 확인 필요)" + 기본값으로 적는다(ADR-005 O-5, ADR-006 O-4, ADR-007 O-3, ADR-012 O-8 `proposed`).

## 구현 범위

| ADR | 대응 결정 | 상태 |
|---|---|---|
| 001 목적·경계·배포 단위 | D-01 | accepted |
| 002 canview 계층·누적 리뷰 아카이브(차이: decisions.md 미보유·5열 원장·상대 링크·Python 도구) | D-02·D-04·D-05·D-27 | accepted |
| 003 개발 환경 정본·Windows Tier 2·임시 worktree | D-03 | accepted |
| 004 GPL-3.0-or-later·출처 고지·추출 gate | D-17 | accepted |
| 005 배포 채널·태그 불변·SemVer 0.x | D-11·D-31 | accepted(패키지명 잠정, O-5) |
| 006 디자인 토큰 계약 | D-12 | accepted(O-4 기본값) |
| 007 React UI 패키지 배포 방식 | D-09·D-10 | accepted(O-3 기본값) |
| 008 버전 일치 정책 | D-06·D-07·D-30 | accepted |
| 009 OpenAPI/REST 3계층·예외 레지스트리·health 경로 | D-14 | accepted |
| 010 소비자 채택 모델 | D-16·D-19·D-21·D-24·D-25 | accepted |
| 011 Python 공통 패키지 구조 | D-15·D-22 | accepted |
| 012 Tailwind v4 전환 정책 | D-08·D-29 | proposed(O-8 대기) |

`docs/adr/README.md`: 규칙(대상·형식·뒤집기·동기화·번호) + 표 `ADR | 제목 | 상태` + 상단 "다음 후보 번호는 ADR-013".

## 범위 밖

- 결정 본문의 재설계. ADR은 브리프의 "채택 사유"를 근거로 옮겨 적되 조사 문서 절을 인용한다.
- `docs/decisions.md`(두지 않음), architecture 문서(T-008), standards 문서(T-104~T-107·T-301·T-302).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/adr/README.md`, `docs/adr/001-*.md` ~ `docs/adr/012-*.md`(slug는 영문 kebab-case).

## 수용 기준

- `docs/adr/` 파일 수 13(README + 12), 파일명이 `NNN-<slug>.md`, 각 파일에 H1 `# ADR-NNN: …`가 정확히 1개.
- 각 ADR 머리 불릿에 `상태`·`날짜`(2026-09-06)가 있고 `근거 문서` 불릿이 브리프 D-ID와 조사 문서 절(`dt`·`vm`·`lic` 등 약칭 + §)을 가리킨다.
- 열림 항목은 "열림(사용자 확인 필요)"과 기본값이 같은 문단에 있으며, pinvi mobile Tailwind 3 예외는 "사용자 승인 대기"로만 적는다(브리프 §7).
- `docs/adr/README.md` 표의 12행 상태가 각 파일 머리 `상태`와 글자 단위로 같고 "다음 후보 번호는 ADR-013"이 있다.
- `docs/decisions.md`가 없다. 링크는 저장소 상대 경로만.
- 리뷰어 2인(문서 규약 · 결정 정합) 독립 리뷰 verdict `PASS`.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
ls docs/adr | wc -l
rg -n "^# ADR-" docs/adr | wc -l
rg -n "다음 후보 번호는 ADR-013" docs/adr/README.md
rg -n "^- 상태:" docs/adr/0*.md
test ! -e docs/decisions.md && echo "no decisions.md"
```

Git Bash에서 동일.

## evidence

- 검증 출력과 리뷰 report 경로(`docs/reviews/adversarial/2026-09-06-adr-set.md`, evidence `…-reviewer-{a,b}.md`)를 이 절·`docs/journal.md`·PR 본문에 남긴다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- ADR 상태와 README 색인이 어긋나거나 리뷰 P0/P1이 `OPEN`이면 merge하지 않는다. ADR-012가 `accepted`로 바뀌려면 O-8 사용자 승인 기록이 먼저 있어야 한다.
