# T-106 docs/standards/responsive-web.md 확정

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: 2인 리뷰
- 선행: 없음

## 목표

PC/Mobile Web 규약의 정본 `docs/standards/responsive-web.md`를 규칙 ID `RW-n`으로 확정한다. 이번 PR에서는 초안으로 산출하고(브리프 §7) 2인 리뷰로 확정한다. 표면별 기본 자세·breakpoint·검사 폭·터치 타깃·안전영역·가로 overflow·셸 전략을 한 곳에 두고, 시각 회귀 기준선 절차는 T-108 템플릿과 상수를 공유한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-13 `responsive-web.md` 절(admin PC-first + ≥320px 컨테인·문서 가로 스크롤 금지 / 사용자 웹 mobile-first(하단 탭바·44px·16px 입력·안전영역) / 모바일 앱 48px; breakpoint sm 640·md 768·lg 1024(셸 전환)·xl 1280(inspector rail); 검사 폭 320/375/414/768/1024/1440; 터치 admin 36/30(히트 ≥24, micro는 의사요소 확장)·사용자 44·모바일 48; `overflow-x: clip`; light 기본), D-21(6폭 기준선 = PR evidence), D-29(pinvi 사용자 표면 값은 pinvi 소유), O-21.
- 근거: [ux 조사](../survey/cross/ux-patterns.md) §3.1(표면 분류), §3.2(breakpoint·검사 폭·weather 62rem/42rem·kta 860 등 불일치 사실), §3.3(터치·타이포·안전영역·overflow·다크), §3.4(모바일 셸 strip/drawer/탭바), §4 C1(접힌 rail 4rem, pinvi 5rem)·C2(weather 17rem 불일치)·C3(1024 통일)·C4(strip 기본 + drawer 옵션)·C6(36/30 vs 44 vs 48, pinvi admin 2쪽 예외)·C11(빈 상태 정렬)·C14(light 기본); U6·U7은 [velocity 레지스터](../plan/design-panel/register-velocity-first.md) D-13 표.
- 복제 금지: 셸·목록·피드백 규칙은 [ux-guide.md](../standards/ux-guide.md), 토큰 값은 [design-tokens.md](../standards/design-tokens.md), 기준선 캡처 절차는 [consumer-adoption runbook](../runbooks/consumer-adoption.md)·`templates/playwright.baseline.ts`(T-108)로 링크.

## 구현 범위

1. 머리: 정본 선언·초안 문장·조사 기준 커밋·적용 범위(신규 코드 MUST, 잔존은 예외 등록).
2. RW-1 표면 분류와 기본 자세(admin / 사용자 웹 / 사용자 대시보드 kta / 모바일 앱) 표 + MUST/SHOULD.
3. RW-2 breakpoint 표(sm/md/lg/xl 값·용도·근거)와 "lg = 셸 전환"(MUST U7), 앱별 비표준 값(weather 62rem·kta 860)은 예외 표로.
4. RW-3 검사 폭 6 + 320px 컨테인 게이트(문서 가로 스크롤 금지, 표·지도·작업면만 자체 overflow) — MUST.
5. RW-4 터치 타깃·최소 히트·본문/최소 폰트·안전영역 표(admin/사용자 웹/모바일 앱), pinvi admin 44px 2쪽 영구 예외(O-21).
6. RW-5 가로 overflow `clip`(MUST U6), RW-6 light 기본(dark는 토큰 계약 슬롯), RW-7 모바일 셸 전략(strip 기본·drawer 옵션·탭바는 사용자 웹 전용·a11y 계약은 UX-G4.8 동일), RW-8 접힌 rail 4rem(pinvi 5rem 예외).
7. RW-9 시각 회귀 기준선: 6폭 스크린샷은 PR evidence(저장소 파일 아님), 템플릿·절차 링크, 판정 "diff 0 또는 원인 설명".
8. 예외 등록 형식(앱·규칙·위치·사유·until·review)과 열림 표.

## 범위 밖

- 템플릿 코드(T-108), UX 규칙 본문(T-105), 앱별 예외 확정(T-421·T-431·T-441·T-461·T-472), pinvi 사용자 웹·모바일 값 정본화(D-29).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/standards/responsive-web.md`, `docs/standards/README.md`(행 추가·standards-fe 소유).

## 수용 기준

- RW-2 breakpoint 4값·RW-3 검사 폭 6값이 D-13과 글자 단위로 같고, T-108 템플릿의 상수(`[320, 375, 414, 768, 1024, 1440]`)와 일치한다.
- RW-4 표에 admin 36/30·히트 24·사용자 44·모바일 48·본문 15/16·최소 12가 있고 pinvi 44px 예외가 O-21로 표기된다.
- U6·U7 대응 규칙이 MUST이고, 4앱 이상 사실 근거 규칙은 MUST, 나머지는 SHOULD로 표기된다.
- ux-guide.md와 중복 규칙 0(셸·피드백은 링크만).
- validator 오류 0, 리뷰어 2인(접근성 · 프론트 구현) verdict `PASS`, 초안 문장 제거.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -n "640|768|1024|1280" docs/standards/responsive-web.md | head
rg -n "320.*375.*414.*768.*1024.*1440" docs/standards/responsive-web.md templates/playwright.baseline.ts
rg -o "RW-[0-9]+" docs/standards/responsive-web.md | sort -u | wc -l
```

Git Bash에서 동일.

## evidence

- 규칙 수·리뷰 report(`docs/reviews/adversarial/YYYY-MM-DD-responsive-web.md`)를 이 절과 `docs/journal.md`에 남긴다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- 검사 폭 상수가 템플릿과 어긋나면 T-108·T-402 기준선이 무효가 되므로 두 문서를 같은 PR에서 맞추기 전에는 merge하지 않는다.
