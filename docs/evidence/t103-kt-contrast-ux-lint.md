# T-103 도구 검증 evidence

검증 기준일은 2026-09-08이다. 입력은 common 저장소의 `packages/tokens/tokens.css`와 이 저장소에 커밋한 조사 스냅샷 오버라이드 예제다. 소비자 저장소 파일은 변경하거나 실행하지 않았다.

## 대비 계산

| 입력 | light 결과 | dark 결과 | baseline + `--fail-new` | 조사 수치 대조 |
|---|---:|---:|---:|---|
| canonical `tokens.css` | 27/27 PASS | 27/27 PASS | — | text-tertiary/page 4.73, control-line/page 3.54, focus/page 6.66 |
| docker-manager 예제 | 미달 4건 | — | exit 0 | brand foreground/brand 3.59, tertiary/card 3.82 |
| concierge 예제 | 미달 8건 | 미달 2건 | exit 0 | control-line/card 2.06, page 1.93, tertiary/card 3.53 |
| geo 예제 | 미달 8건 | — | exit 0 | control-line/page 2.29, card 2.41, tertiary/page 3.66 |
| airport 예제 | 미달 4건 | 미달 10건 | light exit 0 / dark exit 1(신규 6건) | sRGB alpha line/page·card 1.32; dark line/page 1.54 |

2026-09-08 정정: 이전 표의 airport dark 4건·baseline exit 0은 현재 구현의 결과와 달랐다. 후보 `b013ab0d2e95e3d892f6dbfa42042389582ea8a9`에서 `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css packages/tokens/examples/airport-overrides.css --dark --baseline packages/tokens/examples/airport.contrast-baseline.example.json --fail-new --json`은 10미달 중 control-line 예외 4건과 신규 6건으로 FAIL·exit 1이다. dark에서 subtle/muted 배경을 재선언하지 않은 예제의 text×subtle 4쌍·icon×subtle/muted 2쌍이 추가 미달이다. 이 결과를 맞추기 위해 조사 예제나 baseline을 늘리지 않았다. 실제 앱의 dark 값·baseline 검증은 외부 선행 T-431이며 여기서 통과한 것으로 세지 않는다. 표의 나머지 baseline exit는 light 실행 결과다.

OKLCH 수식은 CSS Color 4의 OKLab→선형 sRGB 행렬을 표준 라이브러리로 구현했다. hex와 OKLCH alpha는 CSS sRGB source-over로 합성한 뒤 휘도를 계산하고, 투명한 배경은 `surface-page`를 밑바탕으로 사용한다. 기준 미만 수치를 반올림해 통과시키지 않으며, 조사 대조 오차는 테스트에서 ±0.05로만 확인한다. Airport 조사 스냅샷의 1.15는 선형 합성 당시의 역사 값이고, 현재 계약은 CSS source-over 실측 1.320934(표의 1.32)를 사용한다. `--read-surface muted`를 주면 text×muted 4쌍을 추가한다. baseline `until`이 2000-01-01인 fixture는 `EXEMPT_EXPIRED`, exit 1을 반환한다.

## UX 검사

`tests/test_ux_lint.py`는 P1~P8(P4a/P4b 포함), `window.confirm`·bare `confirm()`, `aria-disabled/busy`, 주석·MDX 백틱 인용 제외와 실행 TS/TSX template 검사, baseline 건수, 임시 Git 저장소의 `--base` 추가 행을 검증한다. `tests/fixtures/ux/positive.*`에는 각 패턴 양성, `negative.tsx`에는 백틱 인용과 허용 패턴을 둔다. `tests/`·`e2e/`·`vendor/`·`*.test.*`·`*.gen.ts`는 기본 탐색에서 제외하며 `--root`를 fixture 루트로 주면 해당 루트 자체는 검사한다.

두 CLI 모두 `--json`은 기계 판독 payload만 출력하고 `--step-summary <path>` 또는 `$GITHUB_STEP_SUMMARY`에는 Markdown 표·상태·패턴별 건수를 append한다. malformed CSS/JSON, 잘못된 Git ref는 exit 2로 처리한다. [ADR-016](../adr/016-mdx-parser-for-ux-lint.md) 이후 UX의 MDX 검사만 고정 Node 파서를 사용하고, 잘못된 MDX·파서 실행 실패도 입력 오류 exit 2다. Python 패키지 추가 의존은 없다.

## 미실행 gate

- `NOT_RUN(소비자 저장소 build/e2e)`: common task 범위 밖이며 소비자 이관 task(T-410·T-431·T-441·T-453·T-461·T-472)가 소유한다.
- `NOT_RUN(.github/workflows/contrast-check.yml selftest)`: 재사용 workflow는 T-010 소유다. 이 task는 호출 가능한 CLI 계약과 회귀 시험만 확정했다.
