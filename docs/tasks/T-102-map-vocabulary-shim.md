# T-102 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`) + weather `--rail`·font 오버라이드 예제 + 별칭 충돌 검사 스크립트

- 상태: BLOCKED
- 우선순위: P0
- Gate: 도구 테스트
- 선행: T-101

## 목표

map 어휘를 그대로 쓰는 앱(weather 294회, geo 별칭 층)이 호출부를 바꾸지 않고 `tokens.css`로 갈아탈 수 있도록 선택 파일 `aliases/map-vocabulary.css`를 제공하고, weather가 값 무변경으로 교체할 때 필요한 `--rail 17rem`·font 스택 오버라이드 예제를 둔다. 별칭이 `--kt-*`나 Tailwind 네임스페이스와 충돌하지 않음을 스크립트로 보증한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-12(별칭 shim은 선택 파일, 앱 고유 접두 `--ktc-*`·`--color-admin-*`·`--ui-*`는 앱 파일, font 스택은 앱이 현재 스택으로 오버라이드), D-08 ⑥(weather는 `tokens.css` 교체 + shim + font·`--rail` 오버라이드 동반), D-16(tokens 1차 map + weather).
- ADR-006 — [docs/adr/README.md](../adr/README.md).
- [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §3.1(map 어휘 294회·`--rail` 17rem·shadcn 이름 보유)·§8 항목 1(`tokens.css`가 map 복사본)·§9(폰트 미로딩·Geist 1순위)·§9.1(토큰 1:1 이전 가능 추정), [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.2.1·§3.2.3(map 이름 열)·§3.6.4(오버라이드 예), [UI 컴포넌트 조사](../survey/cross/ui-components.md) §6.3(토큰 이름 정합 표), [ux 조사](../survey/cross/ux-patterns.md) §4 C2(rail 16 vs 17rem)·C12(폰트 스택).
- 정본 `tokens.css`는 T-101 산출물이며 이 task는 값을 추가·변경하지 않는다.

## 구현 범위

1. `packages/tokens/src/aliases/map-vocabulary.css`: map·weather·geo가 공유하는 이름(`--surface-page`… `--text-primary`… `--brand`… `--control-line`·`--border`·`--focus`·status 4+tint·`--radius-control/panel`·`--control-h/-sm`·`--rail`·`--duration-*`·`--ease-*`·`--shadow-*`·`--z-*`·`--font-sans/mono`)을 `var(--kt-*)`로 재선언. 목록은 `dt` §3.2.1·§3.2.3의 map 이름 열 전수 + weather `app/tokens.css`(조사 커밋)에서 재grep해 확정. `.dark` 블록도 동일 이름으로.
2. `packages/tokens/examples/weather-overrides.css`: `--kt-brand` 4종(navy)·`--kt-rail: 17rem`·`--kt-font-sans`(현재 weather 스택)·`.dark` 대응. `examples/README.md`에 "예제이지 배포 대상 아님·6폭 diff 0 검증은 T-461 evidence".
3. `tools/check_aliases.py` + `tests/test_check_aliases.py`(stdlib): (a) 별칭 파일의 모든 `var(--kt-…)` 대상이 `tokens.css`에 정의됨, (b) 별칭 파일이 `--kt-*` 이름을 정의하지 않음, (c) 별칭 이름이 `theme.css`의 `@theme` 네임스페이스(`--color-*`·`--spacing-*`·`--radius-*`·`--text-*`·`--font-*`)와 겹치지 않음, (d) `shadcn.css`와 중복 정의 없음. 출력 목록 + exit 0/1.
4. `package.json` `exports`에 `./aliases/map-vocabulary.css` 추가(T-101 골격에 이미 예약), `npm run check`에 `check_aliases` 호출은 Node 빌드 외 Python이므로 CI `tools` job에서 실행.

## 범위 밖

- geo `--ui-*`·concierge `--ktc-*`·pinvi `--color-admin-*` 별칭(앱 파일; T-441·T-453·T-421), 폰트 파일 배포·로딩 코드, weather 실제 교체 PR(T-461), 값 변경.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `packages/tokens/src/aliases/map-vocabulary.css`, `packages/tokens/examples/weather-overrides.css`, `packages/tokens/examples/README.md`, `tools/check_aliases.py`, `tests/test_check_aliases.py`, `tools/README.md`(행 추가), `packages/tokens/package.json`.

## 수용 기준

- `check_aliases.py`가 `packages/tokens/src`에서 exit 0이고, 미정의 대상·`--kt-*` 정의·네임스페이스 충돌 fixture 각각에서 exit 1(테스트로 고정).
- 별칭 이름 집합이 weather `app/tokens.css`(조사 커밋 `6003da9`)의 변수 이름 집합을 포함한다(누락 목록 0; 재grep 결과를 evidence에 첨부).
- weather 예제가 `tokens.css` + shim + 예제만으로 weather 현재 값(navy·17rem·font)을 재현한다는 대조표(변수별 원값/결과값)가 evidence에 있다.
- `npm pack` tarball에 `aliases/map-vocabulary.css`가 포함되고 `examples/`는 포함되지 않는다.
- Linux·Windows 결과 동일.

## 검증 명령

```bash
python3 -B -X utf8 tools/check_aliases.py packages/tokens/src; echo "exit=$?"
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_aliases.py" -v
npm pack --workspace packages/tokens --pack-destination /tmp/kt && tar -tzf /tmp/kt/kor-travel-tokens-0.1.0.tgz | grep -E "aliases/|examples/"
```

Git Bash에서 동일.

## evidence

- 별칭 수·재grep 결과·대조표·테스트 수를 이 절과 `docs/journal.md`에 남긴다. weather 실제 화면 diff는 T-461 evidence이므로 여기서는 `NOT_RUN(T-461)`.

## rollback 또는 release 차단 조건

- 패키지 내부 파일·도구만 바뀌므로 `git revert` 1회로 원복한다.
- 별칭 충돌 검사 실패 상태로는 T-109 rc를 발행하지 않는다. 별칭 파일에 `--kt-*` 정의가 들어오면 계약 위반이므로 merge 차단.
