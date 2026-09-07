# T-102 레거시 어휘 별칭 shim `aliases/map-vocabulary.css`(map·weather·geo 공통 이름 → `--kt-*`) + weather `--rail`·font 오버라이드 예제 + 별칭 충돌 검사 스크립트 (2026-09-08, PR #15)

- 상태: DONE
- 우선순위: P0
- Gate: 도구 테스트
- 선행: T-101

## 목표

map 어휘를 그대로 쓰는 앱(weather 294회, geo 별칭 층)이 호출부를 바꾸지 않고 `tokens.css`로 갈아탈 수 있도록 선택 파일 `aliases/map-vocabulary.css`를 제공하고, weather가 값 무변경으로 교체할 때 필요한 앱 소유 오버라이드 예제를 둔다. 별칭이 `--kt-*`나 Tailwind 네임스페이스와 충돌하지 않음을 스크립트로 보증한다. 앱마다 값이 다른 `--space-*` 간격은 common semantic 토큰으로 승격하지 않고 weather 예제에만 보존한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-12(별칭 shim은 선택 파일, 앱 고유 접두 `--ktc-*`·`--color-admin-*`·`--ui-*`는 앱 파일, font 스택은 앱이 현재 스택으로 오버라이드), D-08 ⑥(weather는 `tokens.css` 교체 + shim + font·`--rail` 오버라이드 동반), D-16(tokens 1차 map + weather).
- ADR-006 — [docs/adr/README.md](../adr/README.md).
- [weather 인벤토리](../survey/inventory/kor-travel-weather.md) §3.1(map 어휘 294회·`--rail` 17rem·shadcn 이름 보유)·§8 항목 1(`tokens.css`가 map 복사본)·§9(폰트 미로딩·Geist 1순위)·§9.1(토큰 1:1 이전 가능 추정), [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.2.1·§3.2.3(map 이름 열)·§3.6.4(오버라이드 예), [UI 컴포넌트 조사](../survey/cross/ui-components.md) §6.3(토큰 이름 정합 표), [ux 조사](../survey/cross/ux-patterns.md) §4 C2(rail 16 vs 17rem)·C12(폰트 스택).
- 정본 `tokens.css`는 T-101 산출물이며 이 task는 값을 추가·변경하지 않는다.

## 구현 범위

1. `packages/tokens/aliases/map-vocabulary.css`: map·weather·geo가 공유하는 이름(`--surface-page`… `--text-primary`… `--brand`… `--control-line`·`--border`·`--focus`·status 4+tint·`--radius-control/panel`·`--control-h/-sm`·`--rail`·`--duration-*`·`--ease-*`·`--shadow-*`·`--z-*`·`--font-sans/mono`)을 `var(--kt-*)`로 재선언. 목록은 `dt` §3.2.1·§3.2.3의 map 이름 열 전수 + weather `app/tokens.css`(조사 커밋)에서 재grep해 확정한다. 앱마다 값이 다른 weather·geo의 `--space-3xs..2xl`은 이 shim에 넣지 않는다. `.dark` 블록은 shim이 직접 선언하는 모든 이름을 동일하게 갖는다.
2. `packages/tokens/examples/weather-overrides.css`: 고정 weather 원천의 light/dark 공통 토큰 값을 `--kt-*`로 재표현하고, navy brand 4종·`--kt-rail: 17rem`·현재 sans/mono 스택·`--radius-md` panel 호환·`--space-3xs..2xl` 호환 값을 앱 소유 예제로 둔다. `examples/README.md`에 예제 비배포·원천 commit·6폭 diff 0 검증은 T-461 evidence임을 적는다.
3. `tools/check_aliases.py` + `tests/test_check_aliases.py`(stdlib): (a) 별칭 파일의 모든 `var(--kt-…)` 대상이 `tokens.css`에 정의됨, (b) 별칭 파일이 `--kt-*` 이름을 정의하지 않음, (c) 별칭 이름이 `theme.css`의 `@theme` 네임스페이스(`--color-*`·`--spacing-*`·`--radius-*`·`--text-*`·`--font-*`)와 겹치지 않음, (d) `shadcn.css`와 중복 정의 없음. 출력 목록 + exit 0/1.
4. `package.json` `exports`에 `./aliases/map-vocabulary.css` 추가(T-101 골격에 이미 예약), `npm run check`에 `check_aliases` 호출은 Node 빌드 외 Python이므로 CI `tools` job에서 실행.

## 범위 밖

- geo `--ui-*`·concierge `--ktc-*`·pinvi `--color-admin-*` 별칭(앱 파일; T-441·T-453·T-421), 폰트 파일 배포·로딩 코드, weather 실제 교체 PR(T-461), 값 변경.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `packages/tokens/aliases/map-vocabulary.css`, `packages/tokens/examples/weather-overrides.css`, `packages/tokens/examples/README.md`, `tools/check_aliases.py`, `tests/test_check_aliases.py`, `tools/README.md`(행 추가), `packages/tokens/package.json`.

## 수용 기준

- `check_aliases.py`가 `packages/tokens/aliases`에서 exit 0이고, 미정의 대상·`--kt-*` 정의·네임스페이스 충돌 fixture 각각에서 exit 1(테스트로 고정).
- 별칭 이름 집합은 weather 원천에서 확인한 map·weather·geo 공유 이름의 누락 목록 0이어야 한다. weather에만 있고 geo와 값이 다른 `--space-3xs..2xl` 8개는 common shim에서 제외하고, 예제에 보존한 근거와 대조표를 evidence에 첨부한다.
- weather 예제가 `tokens.css` + shim + 예제만으로 고정 원천의 common 토큰·navy·17rem·sans/mono·`radius-md`·spacing·light/dark 값을 재현한다는 대조표(변수별 원값/결과값)가 evidence에 있다. map과 weather의 `radius-md` 의미가 다르므로 shim은 map의 control 값을 유지하고 weather 예제가 panel을 재선언한다. 실제 소비자 화면 6폭 diff는 T-461에서 검증하며 이 task에서는 `NOT_RUN(T-461)`이다.
- `npm pack` tarball에 `aliases/map-vocabulary.css`가 포함되고 `examples/`는 포함되지 않는다.
- Linux·Windows 결과 동일.

## 검증 명령

```bash
python3 -B -X utf8 tools/check_aliases.py packages/tokens/aliases; echo "exit=$?"
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_aliases.py" -v
npm pack --workspace packages/tokens --pack-destination /tmp/kt && tar -tzf /tmp/kt/kor-travel-tokens-0.1.0.tgz | grep -E "aliases/|examples/"
```

Git Bash에서 동일.

## evidence

- 최종 code candidate는 `ded1631b81d464ed919d36d73ab9c2a1111d38f4`(tree `41dd1c6551994b62d94a04c8a3c1f8bf98414de7`)이며 ready PR [#15](https://github.com/digitie/kor-travel-common/pull/15)에 반영했다. 초기 draft PR [#14](https://github.com/digitie/kor-travel-common/pull/14)는 동일 source의 기록을 보존한 뒤 닫는다. 반복 no-go의 근본 원인과 finding disposition은 [최종 통합 판정](../reviews/adversarial/2026-09-08-t102-post-fix-01.md)에 기록했다.
- 두 독립 reviewer의 final2 원본은 [A](../reviews/adversarial/evidence/2026-09-08-t102-final2-reviewer-a.md)(SHA256 `735D4718F53B8349A89638D3BCE1D4DF28593BD5418D14B56DA3EC5B3A03C63B`)와 [B](../reviews/adversarial/evidence/2026-09-08-t102-final2-reviewer-b.md)(SHA256 `B675AC97A9A9B9574B809008513BC187B0D18DA3368EF63CC66E53A1EDE6ECDA`)이며 모두 PASS·신규 P0–P3 finding 0건이다.
- exact candidate CI [34137474603](https://github.com/digitie/kor-travel-common/actions/runs/34137474603)의 docs·tools(Windows/Ubuntu)·packages·secret-scan·check-versions 6개 job이 모두 성공했다. Windows 전체 238 tests와 focused alias 35 tests, WSL 전체 235 pass와 focused 34 pass(+플랫폼 skip)는 reviewer 원본에 보존했다. `check_aliases`·문서 link/plan·SPDX·secret/redaction·versions self-check·`git diff --check`도 오류 0이다.
- tokens package check/build/test 7개, 임시 tarball 19개 파일의 alias 포함·examples 제외와 install smoke를 통과했으며 npm/PyPI 게시·소비자 저장소 변경은 하지 않았다. 별칭 수·원천 대조는 최종 통합 판정과 review evidence를 정본으로 한다.
- `NOT_RUN(T-461)`: 소비자 weather 실제 교체, build/e2e 및 6폭 visual diff. `NOT_RUN(사용자 범위)`: npm/PyPI 게시·GitHub Release/tag·소비자 installation. `NOT_RUN(후속 task)`: T-103 contrast/UX lint·T-104 standards 실물 대조. merge 후 main CI는 merge source SHA를 별도로 기록한다.

## rollback 또는 release 차단 조건

- 패키지 내부 파일·도구만 바뀌므로 `git revert` 1회로 원복한다.
- 별칭 충돌 검사 실패 상태로는 T-109 rc를 발행하지 않는다. 별칭 파일에 `--kt-*` 정의가 들어오면 계약 위반이므로 merge 차단.
