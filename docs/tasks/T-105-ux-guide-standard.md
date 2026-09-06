# T-105 docs/standards/ux-guide.md 확정(UX-Gn.m·MUST/SHOULD·C1~C22·baseline·예외)

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: 2인 리뷰
- 선행: 없음

## 목표

admin·사용자 표면의 UX 규칙 정본을 `UX-Gn.m` ID로 확정한다. 이번 PR에서는 초안으로 산출하고(브리프 §7) 2인 리뷰로 확정한다. 신규 코드 MUST, 기존 잔존은 앱별 baseline으로 관리하며 검사는 T-103 `ux_lint`가 맡는다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-13(G0~G9 전부 수록·MUST = velocity U1~U8 + 4앱 이상 사실 근거·SHOULD 나머지·admin/사용자 장 분리·금지 패턴 7종 + `window.confirm`·baseline 7건·C1~C22 risk-first 판정·dirty 이탈 경고 미포함), D-26(마커 팔레트 16슬롯·라벨 대비 규칙만), D-30, O-21(pinvi admin 44px 2쪽 영구 예외), O-22.
- 근거: [ux 조사](../survey/cross/ux-patterns.md) §2 G0.1~G9.9(규칙·근거·수준), §4 C1~C22, §5; U1~U8은 [velocity 레지스터](../plan/design-panel/register-velocity-first.md) D-13 표; 정정값 `window.confirm` 7건([조사 안내](../survey/README.md) §6.2·브리프 §7).
- 범위 밖 사실: 토스트·모달 엔진은 앱 소유(정책만), 지도 스타일 빌더 범위 밖(C22), Hallmark 스탬프는 common 파일에 없고 `SKILL.md` 본문 인용 금지([라이선스 조사](../survey/cross/licensing.md) §4 B3).
- 복제 금지: 토큰 값은 [design-tokens.md](../standards/design-tokens.md), breakpoint·터치 타깃은 [responsive-web.md](../standards/responsive-web.md), 마크업 계약은 [ui-contract.md](../standards/ui-contract.md)로 링크.

## 구현 범위

1. 머리: 정본 선언·초안 문장·조사 기준 커밋·적용 범위(신규 코드 MUST, 잔존은 baseline).
2. 1장 admin 표면: G0 범위·소유(UX-G0.1~0.3) / G1 셸(1.1~1.8) / G2 목록(2.1~2.7) / G3 상세·편집(3.1~3.6; 3.6은 "미포함, O-22") / G4 피드백(4.1~4.8) / G5 상태(5.1~5.6) / G6 위험 작업(6.1~6.6) / G7 로그인(7.1~7.3) / G8 도움말·복사·JSON·지도(8.1~8.4) / G9 접근성·모션·타이포(9.1~9.9). 규칙마다 MUST/SHOULD·근거 앱 수·출처 절.
3. 2장 사용자 표면(pinvi 사용자 웹·모바일·kta 대시보드): 밀도·탭바·44/48px·빈 상태 가운데 허용(C11) — 값은 pinvi 소유, 의미 이름만.
4. 3장 충돌 판정 표 C1~C22(risk-first 채택값: 접힌 rail 4rem(pinvi 5rem 예외), 셸 전환 1024, strip 기본 + drawer 옵션, tint+mark, 36/30(pinvi 44px 2쪽 O-21), 동사 라벨 필수·`window.confirm` 금지, 성공은 조용히·엔진 앱 소유, 5-tone(geo CANCELLED 보류), 좌정렬, Pretendard 1순위(로딩 앱 책임), 15/12 하한, light 기본, 타이포 워드마크, breadcrumb, HelpTip popover-only 허용, 모달 행동 계약, AppErrorPanel 계보, nav 라벨만, SPDX만, 지도 빌더 범위 밖).
5. 4장 검사·baseline·예외: 금지 패턴 7종 + `window.confirm`의 정규식 정의(ux_lint 정본), baseline 표(map 2·ktdm 3·kta 1·wx 1), 예외 등록 형식(앱·규칙·위치·사유·until·review).
6. 5장 마커 팔레트: 16슬롯·라벨 대비 규칙만, hex 정본 map(O-13).

## 범위 밖

- 컴포넌트 구현(T-2xx), 반응형 수치(T-106), 토큰 값(T-104), 검사 도구(T-103), 앱 baseline 확정(각 이관 task), dirty 이탈 경고 규칙.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/standards/ux-guide.md`, `docs/standards/README.md`(행 추가·standards-fe 소유).

## 수용 기준

- UX-G 규칙 수가 `ux` §2의 규칙 수(G0 3·G1 8·G2 7·G3 6·G4 8·G5 6·G6 6·G7 3·G8 4·G9 9 = 60)와 같고 ID가 원 번호와 1:1이다.
- U1~U8에 대응하는 규칙(UX-G9.1·G4.6·G5.1·G2.2·G1.3·G9.9·responsive 위임 2건·C20)이 MUST이며, 4앱 이상 사실 근거 규칙이 모두 MUST, 나머지는 SHOULD로 표기된다.
- C1~C22 각 행에 채택값·근거·예외(O-21)가 있고 C22는 범위 밖으로 표기된다.
- baseline 표 합계 7, 예외 등록 형식에 `until`·`review`가 있다.
- Hallmark `SKILL.md` 문장 인용 0, 토큰 값·breakpoint 수치 복제 0(링크만).
- 리뷰어 2인(접근성 · 소비자 이관 비용) verdict `PASS`, validator 오류 0.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -o "UX-G[0-9]+\.[0-9]+" docs/standards/ux-guide.md | sort -u | wc -l
rg -n "MUST|SHOULD" docs/standards/ux-guide.md | wc -l
rg -n "^\| C(1|22) " docs/standards/ux-guide.md
rg -n "Hallmark" docs/standards/ux-guide.md || echo "no hallmark"
```

Git Bash에서 동일.

## evidence

- 규칙 수·MUST 수·리뷰 report(`docs/reviews/adversarial/YYYY-MM-DD-ux-guide.md`)를 이 절과 `docs/journal.md`에 남긴다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- MUST 목록이 확정되지 않으면 T-103 `ux_lint`의 fail 대상이 정해지지 않으므로 T-502 승격을 차단한다. 리뷰 P0/P1 `OPEN`이면 merge 금지.
