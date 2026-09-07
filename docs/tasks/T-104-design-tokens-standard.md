# T-104 docs/standards/design-tokens.md 확정(패키지 실물과 대조·규칙 ID TK-n)

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 2인 리뷰
- 선행: T-101

## 목표

색상 톤 규칙의 정본 docs/standards/design-tokens.md를 규칙 ID TK-1~TK-13으로 확정했다. T-101·T-102의 실제 tokens.css·theme.css·shadcn.css와 변수 집합·alias 의미·프로필 값을 대조하고, 두 독립 reviewer의 PASS까지 확인한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-12 전체(접두·계층 2단·역할·shadcn alias 의미·프로필·타입 스케일 `@theme`·오버라이드 허용 목록·다크·대비·값 형식·정본/생성물·별칭 shim·폰트·마커 팔레트 범위 밖), D-10(`kt-` 유틸리티·`theme.css` 네임스페이스·소비자 필수 2줄), D-08(전환 4단 PR), D-26, O-4·O-11·O-13.
- ADR-006 — [docs/adr/README.md](../adr/README.md). 검사 도구는 T-103(`kt_contrast`), 예외는 앱 `contrast-baseline.json`.
- 근거: [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.1(앱별 체계), §3.2.1~§3.2.3(역할·다크·alias), §3.3(브랜드 분리), §3.4(운용 규칙·대비), §3.5(도메인 팔레트 소유권), §3.6.1~§3.6.7, §5; 판정 M-1·M-3·M-11([판정 보고서](../plan/design-panel/judge-fact-consistency.md)).
- 규칙 복제 금지: UX 규칙은 [ux-guide.md](../standards/ux-guide.md), 반응형은 [responsive-web.md](../standards/responsive-web.md), 배포 형태는 [style-delivery.md](../architecture/style-delivery.md)로 링크.

## 구현 범위

1. 머리: 정본 선언·확정 task·조사 기준 commit을 기록하고 초안 문구는 두지 않는다.
2. 절: TK-1 접두·네임스페이스(`--kt-*`·`kt-`·앱 고유 접두 규칙) / TK-2 계층(semantic ← app override) / TK-3 역할 목록 표(변수명·의미·light/dark 필수 여부·오버라이드 가능 여부) / TK-4 shadcn alias 의미 고정 4항 / TK-5 프로필 admin(6/8·36/30·15px·7단) · consumer(의미 이름만, 값 pinvi 소유) / TK-6 오버라이드 허용 목록·금지 목록(형태·높이·모션은 프로필로만) / TK-7 다크(정의 필수·활성 opt-in·`color-scheme: light`) / TK-8 대비(쌍·임계·baseline·신규 미달만 fail) / TK-9 값 형식(OKLCH 권고·hex 허용) / TK-10 정본·생성물·빌드 diff / TK-11 별칭 shim(선택)·앱 접두 파일 / TK-12 폰트(스택은 common·로딩은 앱·Pretendard MUST는 로드 앱만) / TK-13 마커 팔레트 범위 밖(규칙만, hex 정본 map, O-13) / 예외·열림 표.
3. 각 규칙에 MUST/SHOULD와 근거 절(`dt` §n) 표기, 열림은 "열림(사용자 확인 필요)" + 기본값.
4. 실물 대조(T-101 이후): 변수 집합·기본값·alias·프로필 값을 `tokens.css`·`theme.css`·`shadcn.css`와 표로 대조하고 불일치는 코드 또는 문서 중 정본(코드가 값 정본, 문서가 의미 정본)에 맞춰 수정.

## 범위 밖

- 값 자체(T-101), 검사 도구(T-103), 별칭 파일(T-102), UX·반응형 규칙, consumer 프로필 값, Tailwind 전환 절차(ADR-012·consumer-adoption).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/standards/design-tokens.md`, `docs/standards/README.md`(행 추가·standards-fe 소유), `packages/tokens/shadcn.css`·`packages/tokens/test/values.test.mjs`(앱 소유 차트 슬롯 계약 회귀).

## 수용 기준

- TK-3 표의 변수명 집합이 packages/tokens/tokens.css에서 추출한 44개와 같다(실제 경로는 package root이며 src 경로가 아니다).
- TK-4 alias 4항이 `shadcn.css` 정의와 일치하고, TK-5 admin 값이 `tokens.css` 값과 같다.
- TK-8의 일반 텍스트·상태 텍스트 4.5:1과 비텍스트 3:1 기준이 T-103·style-delivery와 일치한다.
- `surface-muted`는 장식·선택 행 원천으로 기본 텍스트 읽기 표면에서 제외하고, 앱이 읽기 배경으로 쓰는 경우 4.5:1 쌍을 추가한다.
- `shadcn.css`가 `--chart-1..5`를 선언하지 않으며, 차트 팔레트 앱 소유 경계와 스코프 회귀 시험이 문서와 일치한다.
- 모든 TK 규칙에 MUST/SHOULD·근거 절이 있고, O-4·O-11·O-13이 열림 표에 기본값과 함께 있다.
- consumer 프로필 값(8/14/20/32·44·16)은 "pinvi 소유"로만 적고 정본화하지 않는다.
- Hallmark `SKILL.md` 인용 0, 링크 상대 경로만, validator 오류 0.
- 확정 시점: 문서에 초안 상태 문장이 없고 리뷰어 2인(디자인 시스템 · 접근성/대비) verdict `PASS`.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -o -- "--kt-[a-z0-9-]+" packages/tokens/tokens.css | sort -u > /tmp/kt-vars.txt
rg -o -- "--kt-[a-z0-9-]+" docs/standards/design-tokens.md | sort -u | diff - /tmp/kt-vars.txt && echo "vars match"
rg -n "TK-[0-9]+" docs/standards/design-tokens.md | wc -l
rg -n "Hallmark" docs/standards/design-tokens.md || echo "no hallmark"
```

Git Bash에서 동일.

## evidence

- 대조 결과는 tokens.css 44개 light/dark, shadcn 4 alias, admin profile 값이 모두 일치했다. 문서·plan·unittest·package check·diff 검증과 두 reviewer 원본 및 통합 report를 이 task와 journal에 연결한다. T-103 대비 도구, 소비자 build/e2e·6폭 시각 비교·npm/PyPI 게시는 NOT_RUN(후속 task 또는 사용자 범위)이다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- 문서와 실물의 변수 집합이 다르면 T-109 rc를 발행하지 않는다(A6.1 원본·생성물 불일치 금지의 문서판).
