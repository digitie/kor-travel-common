# T-204 docs/standards/ui-contract.md 확정(data-slot·testid·heading·sr-only·geo 셀렉터 대응·SemVer 0.x)

- 상태: BLOCKED
- 우선순위: P0
- Gate: 2인 리뷰
- 선행: T-203

## 목표

[ui-contract](../standards/ui-contract.md)를 "정본 초안"(이번 PR, standards-fe 작성자)에서 T-203 실물과 대조한 "확정본"으로 올린다. 문서의 모든 `data-slot`·testid·heading 구조·sr-only 문구·geo e2e 셀렉터 대응이 `packages/ui/src`의 실제 값과 1:1로 일치하고, 무엇이 SemVer 0.x 파괴 변경인지 열거되어야 T-212 릴리스가 가능하다. 초안 작성은 이번 PR에서 끝나지만 확정은 T-203이 DONE이 된 뒤에만 가능하다.

## 고정 결정

- ADR-005(SemVer 0.x)·ADR-007 — [ADR 색인](../adr/README.md); [브리프](../plan/design-brief.md) D-10(마크업 계약 정본 = ui-contract, 변경은 0.x minor(이관 절 필수)/1.x major)·D-31(파괴 항목: 토큰 이름/의미·data-slot/testid·prop 기본값·정렬 모드·CSS 파일 경로; 폐기는 1 minor alias 유지).
- 사실 근거: pinvi e2e가 잠근 testid(`admin-table-scroll`·`admin-table-sort-<key>`·`admin-mobile-cards`)와 sr-only 로딩 문구, `containerTestId` — [ui-components](../survey/cross/ui-components.md) §3.2·§3.3·§7-6; geo e2e 셀렉터(`section.panel .panel-header h2`, `pre.json-box`) — [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3 geo 행·§3.1 geo PR 4; 헤더 밴드 heading 순서 — [ux-patterns](../survey/cross/ux-patterns.md) G1.5; "SemVer 공개 API에 정렬 기본값·키보드 동작·토큰 계약 포함" — 선행 보고서 §8 E7([survey README](../survey/README.md) §5).
- 작성 규칙: 규칙 ID는 문서 소유자가 정한다(후보 `UC-n`, 브리프 §7의 `TK-n`·`UX-Gn.m`과 같은 방식). 같은 규범을 [ux-guide](../standards/ux-guide.md)·[design-tokens](../standards/design-tokens.md)와 복제하지 않고 링크한다.

## 구현 범위

- 컴포넌트별 `data-slot` 표(13종 + T-205~T-210 예정분은 "예정" 표기), testid 규약(`data-testid` 전달 prop 이름·고정 testid 없음·앱 어댑터가 공급하는 값의 예), heading 구조(`SectionCard headingLevel`, 페이지당 h1 유일, 헤더 밴드 순서), sr-only 문구 사전(한국어 고정 문자열; 예 "불러오는 중…", "복사됨"), geo 셀렉터 대응표(공통 컴포넌트가 어떤 셀렉터를 보장하지 않는지 명시), SemVer 0.x 파괴 항목 목록과 CHANGELOG 이관 절 형식.
- T-201 base-ui 사실 확인 3건의 결론을 "엔진 사실" 절로 흡수(Button `type` 기본·Checkbox hidden input·Toast).
- 대조 절차: `rg -o 'data-slot="[^"]+"' packages/ui/src | sort -u` 결과와 문서 표를 비교하는 스크립트(`packages/ui/scripts/check-contract-doc.mjs`, 후보) 또는 수동 대조표를 evidence로 남긴다.
- 문서 머리의 "실물 패키지와 대조해 확정하는 task가 남아 있다" 문장을 제거하고 기준 커밋·패키지 버전을 적는다.

## 범위 밖

- v0.2 컴포넌트(overlay·DataTable·Header·Form)의 계약 확정 — T-213 전 같은 절차로 갱신(별도 리뷰).
- 앱 어댑터(pinvi `AdminTable`) 계약, 토스트 정책(ux-guide UX-G4.1), 토큰 이름 규칙(design-tokens).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/standards/ui-contract.md
docs/standards/README.md  (상태 "초안"→"확정" 1행)
packages/ui/scripts/check-contract-doc.mjs  (후보)
docs/reviews/adversarial/YYYY-MM-DD-ui-contract.md  + evidence/…-reviewer-{a,b}.md
docs/reviews/README.md  (표 1행)
CHANGELOG.md  (규약 확정 항목)
```

## 수용 기준

- 문서의 `data-slot`·testid·sr-only 문구 집합이 `packages/ui/src` grep 결과와 집합 단위로 같다(누락·잉여 0).
- 파괴 변경 목록이 D-31의 다섯 축을 모두 다루고, 각 항목에 "minor에서 허용 + 이관 절 필수" 또는 "1.0 전 금지"가 표시된다.
- geo 셀렉터 대응표가 "보장함/보장하지 않음/앱 어댑터 책임" 3분류로 채워진다.
- 전문 영역이 다른 리뷰어 2인 독립 리뷰 verdict `PASS`(P0/P1 finding 0), report와 evidence가 [리뷰 아카이브](../reviews/README.md) 규칙대로 존재.
- `tools/validate_document_links.py` 오류 0(절대 경로 링크 없음).

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -o 'data-slot="[^"]+"' packages/ui/src | sort -u
rg -o 'data-testid=\{[^}]+\}|data-testid="[^"]+"' packages/ui/src | sort -u
node packages/ui/scripts/check-contract-doc.mjs
git diff --check
```

## evidence

리뷰 report 경로, 대조 스크립트 출력(또는 수동 대조표), 기준 커밋과 패키지 버전을 PR 본문과 `docs/journal.md`에 남긴다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 revert는 단일 커밋. 확정 전 상태로 되돌리면 머리 문장("초안")을 복원한다.
- 차단: 실물과 문서 불일치가 1건이라도 남으면 확정하지 않으며 T-212 rc 태그를 만들지 않는다. 선행 T-203이 DONE이 아니면 이 task는 IN_PROGRESS로 남는다(`validate_plan.py` 규칙).
