# T-108 templates/playwright.baseline.ts(6폭 스크린샷) + 기준선 캡처 절차(consumer-adoption 절)

- 상태: READY
- 우선순위: P1
- Gate: 도구 테스트
- 선행: 없음

## 목표

토큰·스타일·셸을 바꾸는 소비자 PR이 착수 전 6폭 스크린샷 기준선을 잡고 완료 후 diff를 PR evidence로 남길 수 있도록, Playwright 템플릿과 캡처 절차를 제공한다. Playwright가 없는 앱(weather·docker-manager)도 같은 템플릿으로 기준선을 만들 수 있게 한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-21(6폭 320/375/414/768/1024/1440·PR evidence·저장소 파일 아님·`templates/playwright.baseline.ts`), D-24(PR 본문에 스크린샷·되돌리기), D-13 검사 폭, D-08(4단 별도 PR의 1단 = 시각 기준선 캡처), D-25(`NOT_RUN`).
- ADR-010 — [docs/adr/README.md](../adr/README.md). 검사 폭 정본은 [responsive-web.md](../standards/responsive-web.md) RW-3(T-106)이며 템플릿 상수는 그 값을 복제한 것이므로 두 곳을 같은 PR에서 맞춘다.
- 근거: [ux 조사](../survey/cross/ux-patterns.md) §3.2(검사 폭 합집합), [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §9.1(playwright 없음·수동 검증 위험), [docker-manager 인벤토리](../survey/inventory/kor-travel-docker-manager.md) §3.1(e2e 부재), [map 인벤토리](../survey/inventory/kor-travel-map.md) §3.1(e2e 30·Playwright 1.60 exact), [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1("evidence는 PR 본문 첨부").
- Playwright 버전은 `versions.json`(1.60 floor·1.63 recommended)을 따르고 템플릿은 두 버전에서 동작해야 한다.

## 구현 범위

1. `templates/playwright.baseline.ts`: `WIDTHS = [320, 375, 414, 768, 1024, 1440]`, 라우트는 env `KT_BASELINE_ROUTES`(쉼표 구분, 기본 `/`), 로그인 필요 시 `KT_BASELINE_STORAGE_STATE`(storageState 경로), 출력 `KT_BASELINE_DIR`(기본 `.kt-baseline/`; gitignore 대상), 파일명 `<route-slug>-<width>.png`, `fullPage: true`, `animations: "disabled"`, `reducedMotion: "reduce"`, 폰트 로딩 대기(`document.fonts.ready`); `KT_BASELINE_MODE=compare`면 `expect(page).toHaveScreenshot`(`maxDiffPixels: 0`)로 기준선과 대조.
2. `templates/playwright.baseline.config.ts`: chromium 단일 프로젝트, `baseURL` env `KT_BASELINE_URL`, `retries: 0`, `reporter: list`.
3. `docs/runbooks/consumer-adoption.md` "6폭 기준선 캡처" 절(runbooks 작성자 소유 문서에 절 추가): 착수 전 캡처 → 변경 → 완료 캡처 → diff(픽셀 diff 0 또는 원인 설명) → PR 본문 첨부 → 저장소에 png 커밋 금지 → 미실행은 `NOT_RUN(사유)`. 앱별 라우트 목록은 `templates/consumer-adoption-checklist.md`에 표로.
4. selftest: `tests/fixtures/baseline-page/index.html`(정적 페이지)을 `python3 -m http.server`로 띄우고 템플릿을 실행해 6개 png 생성·compare 모드 통과를 `workflows-selftest`(T-010) 또는 `packages` job에서 검증. Windows에서는 도구 테스트 범위 밖(`NOT_RUN(브라우저 설치)` 허용).
5. `.gitignore`에 `.kt-baseline/` 추가는 coordinator 소유 파일이므로 open item으로 보고하고 템플릿 주석에 안내.

## 범위 밖

- 소비자 앱 실제 기준선 캡처(T-402·각 이관 task), 시각 diff 도구 선택(Playwright 내장으로 한정), 레지스트리 채널의 playwright 기준선 템플릿 배포(T-211), 로그인 자동화(앱 소유).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `templates/playwright.baseline.ts`, `templates/playwright.baseline.config.ts`, `tests/fixtures/baseline-page/index.html`, `docs/runbooks/consumer-adoption.md`(절 추가), `templates/consumer-adoption-checklist.md`(라우트 표), `templates/README.md`(행 추가).

## 수용 기준

- 템플릿이 `@playwright/test` 1.60과 1.63 타입으로 `tsc --noEmit` 통과(fixture `package.json` 두 벌 또는 devDependency 교체 실행).
- 정적 fixture에서 6개 png가 생성되고 compare 모드가 diff 0으로 통과하며, 의도적으로 바꾼 fixture에서는 실패한다(selftest evidence).
- `WIDTHS` 상수가 responsive-web.md RW-3 값과 같다.
- 절차 절이 "PR evidence·저장소 파일 아님·`NOT_RUN` 규칙·되돌리기"를 담고 D-24 파일 상한과 충돌하지 않는다(png는 파일 수에 들어가지 않음).
- SPDX 헤더(`check_spdx.py` exit 0).

## 검증 명령

```bash
cd tests/fixtures/baseline-page && python3 -m http.server 13005 &
KT_BASELINE_URL=http://127.0.0.1:13005 KT_BASELINE_ROUTES=/ npx playwright test --config templates/playwright.baseline.config.ts
KT_BASELINE_URL=http://127.0.0.1:13005 KT_BASELINE_MODE=compare npx playwright test --config templates/playwright.baseline.config.ts; echo "exit=$?"
ls .kt-baseline | wc -l
rg -n "320, 375, 414, 768, 1024, 1440" templates/playwright.baseline.ts docs/standards/responsive-web.md
python3 -B -X utf8 tools/check_spdx.py
```

Git Bash에서 동일(포트 13005는 실행 시 주입하는 테스트 fixture 예시이며 운영 대역 등록을 전제하지 않는다).

## evidence

- Playwright 버전·생성 파일 수·compare 결과·selftest 링크를 이 절과 `docs/journal.md`에 남긴다. 브라우저를 설치하지 못한 환경은 `NOT_RUN(브라우저 설치)`.

## rollback 또는 release 차단 조건

- 템플릿·fixture·문서만 바뀌므로 `git revert` 1회로 원복한다.
- selftest가 통과하지 못한 템플릿으로는 T-402(7앱 기준선 캡처)를 착수하지 않는다.
