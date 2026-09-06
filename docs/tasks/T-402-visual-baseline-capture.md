# T-402 7앱 시각 회귀 기준선 초기 캡처(앱별 evidence; 미실행 NOT_RUN)

- 상태: BLOCKED
- 우선순위: P2
- Gate: NOT_RUN 허용
- 선행: T-108

## 목표

`templates/playwright.baseline.ts`(T-108)로 7개 소비 앱 admin 표면의 6폭(320/375/414/768/1024/1440) 스크린샷 기준선을 한 번씩 캡처해 "토큰·스타일·셸을 바꾸는 첫 소비자 PR"이 비교할 원점을 만든다. 캡처 파일은 저장소에 넣지 않고(D-21) 폭·페이지·digest·환경만 기록한다. 실행하지 못한 앱은 `NOT_RUN(사유)`로 남긴다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-21(기준선은 PR evidence, 저장소 파일 아님; Playwright 없는 wx·ktdm은 템플릿 사용)·D-13(검사 폭 6종)·D-25(NOT_RUN 표기).
- ADR-010(소비자 채택 모델) — [ADR 색인](../adr/README.md). 절차 정본: [consumer-adoption runbook](../runbooks/consumer-adoption.md) 기준선 캡처 절, [responsive-web](../standards/responsive-web.md).
- 판정 보고서 [judge-migration-feasibility §4.2](../plan/design-panel/judge-migration-feasibility.md): 기준선 캡처는 앱 task의 evidence이며 T-402는 다른 앱의 채택을 막지 않는다(T-410·T-461의 선행이 아님).
- 앱별 실행 수단(사실): map mocked suite(`playwright.config.ts`, 서버 외부 기동) — [inv/map §3.1](../survey/inventory/kor-travel-map.md); pinvi `playwright.config.ts`(`next build && next start -p 12805`) — [inv/pinvi §3.1](../survey/inventory/pinvi.md); geo `127.0.0.1:12505` — [inv/geo §3.1](../survey/inventory/kor-travel-geo.md); concierge `tests/` 별도 패키지 — [inv/ktc §3.1](../survey/inventory/kor-travel-concierge.md); airport `frontend/e2e` — [inv/kta §3.1](../survey/inventory/kor-travel-airport.md); weather·ktdm Playwright 없음 — [inv/weather §3.1](../survey/inventory/kor-travel-weather.md), [inv/ktdm §3.1](../survey/inventory/kor-travel-docker-manager.md).

## 구현 범위

- 앱마다 대표 페이지 2~4개(로그인·목록·상세·대시보드)를 정해 `templates/playwright.baseline.ts`의 페이지 목록 입력으로 넘긴다. 목록은 이 파일의 "실행 기록" 표에 고정한다.
- 캡처 결과(PNG)는 scratchpad 또는 gitignore된 `.tools/baseline/<app>/<sha>/`에 두고, 표에는 앱·기준 커밋·폭·페이지·파일 digest(sha256)·브라우저 버전·실행 환경(WSL/n150)을 적는다.
- weather·ktdm은 앱에 Playwright를 추가하지 않고 common 체크아웃의 템플릿을 `npx playwright test -c templates/playwright.baseline.ts`로 외부에서 실행한다(앱 서버는 로컬 기동).
- 로그인이 필요한 앱은 각 앱의 mock 로그인 절차(map storageState, geo `PLAYWRIGHT_MOCK_LOGIN=1` 등)를 그대로 쓴다. 운영(n150) 대상 캡처는 하지 않는다.

## 범위 밖

시각 diff 판정 자체(각 앱 채택 task), 저장소에 PNG 커밋, 사용자 표면·모바일 캡처(pinvi 사용자 표면은 D-29로 코드 소비 대상 아님), 템플릿 작성(T-108).

## 대상 저장소·브랜치·PR·되돌리기

소비 저장소에는 커밋이 없다(읽기 전용 실행). common 측 변경은 이 task 파일과 `docs/journal.md`뿐이므로 별도 브랜치 없이 작업 브랜치에서 처리한다. 되돌리기 = 기록 삭제.

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
docs/tasks/T-402-visual-baseline-capture.md   # 실행 기록 표 추가
docs/journal.md
.tools/baseline/<app>/<sha>/*.png              # gitignore, 저장소 밖 보관
```

## 수용 기준

- [ ] 7앱 × 6폭 표가 있고 각 셀이 `digest` 또는 `NOT_RUN(사유)` 중 하나다. 빈 셀·"예정"은 허용하지 않는다.
- [ ] 실행한 앱은 기준 커밋 SHA·브라우저 버전·서버 기동 명령이 함께 기록돼 재현 가능하다.
- [ ] 캡처 PNG가 common 또는 소비 저장소에 커밋되지 않았다(`git status --porcelain`에 PNG 없음).
- [ ] 0장 캡처를 "통과"로 표기하지 않았다(D-25).

## 검증 명령

```bash
# common 체크아웃, 앱 서버는 별도 터미널에서 기동(각 앱 README·dev-environment 참조)
BASELINE_APP=map BASELINE_URL=http://127.0.0.1:12705 npx playwright test -c templates/playwright.baseline.ts
sha256sum .tools/baseline/map/*/**.png
python3 -B -X utf8 tools/validate_plan.py
```

## evidence

이 파일 하단 "실행 기록" 표 + `docs/journal.md` 1항목. 각 앱의 첫 토큰 PR(T-410·T-421·T-431·T-441·T-453·T-461·T-472)은 이 표의 digest를 PR 본문에서 인용하고 완료 diff를 첨부한다.

## rollback·release 차단 조건

- 기록만 있는 task라 rollback은 기록 삭제다.
- 앱 채택 PR이 이 기준선 없이 열리면 해당 PR 안에서 착수 전 캡처를 먼저 수행해야 하며(D-21), 그 경우 이 task의 해당 행을 PR 링크로 갱신한다.
