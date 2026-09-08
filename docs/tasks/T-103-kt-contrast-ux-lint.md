# T-103 tools/kt_contrast.py(report·`contrast-baseline.json`) + `tools/ux_lint.py`(금지 7종+window.confirm, 전체 report·diff fail) + 4앱 오버라이드 예제 보고

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: 도구 테스트
- 선행: T-101

## 목표

색상 톤 규칙과 UX 규칙의 기계 검사 2종을 만든다. `kt_contrast.py`는 앱 오버라이드의 WCAG 대비를 report하고 신규 미달만 fail할 수 있게 baseline을 지원하며, `ux_lint.py`는 금지 패턴 7종 + `window.confirm`을 전체 report·diff 기반 fail로 검사한다. 4앱(ktdm·concierge·geo·airport)의 알려진 미달 값으로 도구를 검증한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-12 대비 절(light 쌍 필수·dark는 dark 활성 앱만·report 기본·`contrast-baseline.json` 미달 쌍 + `until`·신규 미달만 fail), D-13(금지 패턴 7종: raw hex/oklch·`text-[Npx]`·`rounded-2xl+`·팔레트 alpha·`outline-none`·`transition-all/colors`·`aria-disabled:opacity-` + `window.confirm`; 전체 report + `--base <sha>` diff fail; baseline 7건), D-30, D-19(매니페스트 `contrast{baseline,dark}`·`ux_gate{baseline}`).
- ADR-006 — [docs/adr/README.md](../adr/README.md). 규칙 정본은 [design-tokens.md](../standards/design-tokens.md)·[ux-guide.md](../standards/ux-guide.md).
- [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.4.1(운용 규칙)·§3.4.2(대비 재검증: map 통과, geo 2.29/2.41·concierge 2.06/1.93·ktdm brand 3.59·airport line 1.15 미달)·§3.6.3(`kt-contrast` 역할), [ux 조사](../survey/cross/ux-patterns.md) §2 G0.3(grep 가능한 금지 목록·백틱 인용 제외)·G9.1·G9.4·G9.6·§4 C7(`window.confirm` 잔존 map 2·ktdm 3·kta 1·wx 1), [map 인벤토리](../survey/inventory/kor-travel-map.md) §9(금지 패턴 게이트 미자동화 — common이 제공하면 map이 첫 소비자).
- stdlib만, Windows 동작(D-03). OKLCH→sRGB 변환은 CSS Color 4 공식 수식을 구현하고 map 문서의 실측 수치와 대조한다.

## 구현 범위

1. `tools/kt_contrast.py`: 입력 `tokens.css` + 오버라이드 CSS(0..n) + `--dark`; 파서(`:root`/`.dark` 블록의 `--kt-*` 값, OKLCH·hex·`var()` 1단 참조); 검사 쌍과 기준은 [디자인 토큰 TK-8](../standards/design-tokens.md#6-대비와-값-형식)을 그대로 사용한다(text primary/secondary/strong/tertiary × 읽기 표면 page/subtle/card → 4.5:1, `--read-surface muted` 등으로 선언한 추가 읽기 표면은 text 쌍을 더하고, disabled 제외, icon × surface 4 → 3:1, control-line × surface 4 → 3:1, brand-foreground × brand → 4.5:1, brand × brand-tint mark·icon → 3:1, status 4 × tint 위 텍스트 → 4.5:1, focus × surface-page → 3:1). CSS Color 4 변환 후 alpha는 sRGB source-over로 합성하며, 조사 수치 대조의 ±0.03은 검사기 판정에 적용하지 않고 반올림으로 기준 미만을 합격 처리하지 않는다. `--baseline <json>`(미달 쌍 + `until`; 만료는 `EXEMPT_EXPIRED`); `--fail-new`; 출력 Markdown·`--json`·step summary.
2. `tools/ux_lint.py`: 대상 확장자 `.tsx .ts .css .mdx`; [UX-G9 금지 규칙](../standards/ux-guide.md) P1~P8(`P4a/P4b` raw 색상·`P8`은 `window.confirm`과 bare `confirm()` 포함); 백틱·주석 안 인용 제외; `--root`·`--token-files` 범위/allowlist; `--base <sha>`면 `git diff -U0 <sha>`의 추가 행만 fail 대상, 전체는 report; `--baseline <json>`(`schema`, 규칙·경로·건수·reason·until·task); 출력 동일 형식.
3. 테스트: `tests/test_kt_contrast.py`(변환 정확도: map 문서 수치 ±0.05, 쌍 판정, baseline 만료), `tests/test_ux_lint.py`(패턴별 양성·음성 fixture, diff 모드).
4. 4앱 예제: `packages/tokens/examples/{docker-manager,concierge,geo,airport}-overrides.css`(조사 문서 값) + 각 `contrast-baseline.example.json`; 실행 결과 표(미달 쌍·수치)를 evidence와 `docs/journal.md`에 보고. 실제 앱 baseline 등록은 각 이관 task.
5. `templates/contrast-baseline.json`·`templates/ux-baseline.json` 빈 형식 + `tools/README.md` 행.

## 범위 밖

- 재사용 워크플로 `contrast-check.yml` 구현(T-010이 이 task 완료 후 실제 검사기를 연결), 규칙 문서 본문(T-104·T-105), 앱별 baseline 확정·등록(T-421·T-431·T-441·T-453·T-472), `fail` 승격(T-502), 마커 팔레트 검사.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `tools/kt_contrast.py`, `tools/ux_lint.py`, `tests/test_kt_contrast.py`, `tests/test_ux_lint.py`, `tests/fixtures/ux/*`, `packages/tokens/examples/*-overrides.css`, `packages/tokens/examples/*.contrast-baseline.example.json`, `templates/contrast-baseline.json`, `templates/ux-baseline.json`, `tools/README.md`가 이 task의 변경 대상이다. 재사용 워크플로 `.github/workflows/contrast-check.yml`은 T-010 소유이므로 이 task에서 만들지 않는다.

## 수용 기준

### MDX 문맥 검사 기준

반복 리뷰의 문법 추정을 대체하는 실행 기준이다. 제품은 stdlib 패턴 검사기이며 MDX 컴파일 성공을 보증하는 구문 검사기가 아니다. 정상 문서·코드의 검사 제외 범위를 다음처럼 고정한다.

| 입력 문맥 | 진입·종료와 기대 동작 |
|---|---|
| Markdown 본문 | URL, `src/*`, 아포스트로피, `for example,` 등은 JS 주석·문자열을 열지 않는다. 뒤의 JSX·표현식을 계속 검사한다 |
| fenced code·정상 inline code | 블록 fence의 container·marker·길이·들여쓰기를 먼저 판정한다. 정상 닫힌 문서 인용만 제외하며 미종결 inline delimiter 뒤 본문을 통째로 가리지 않는다 |
| MDX 표현식·JSX 속성 | escape되지 않은 중괄호에서 JS 문맥에 들어가고 해당 닫힘에서 복귀한다. 주석 앞 공백·Unicode 식별자·중첩·빈 줄이 이 문맥을 초기화하지 않는다 |
| ESM | 최상위 줄의 `import`·`export`에서 시작한다. default/named export와 여러 줄 import를 포함하고 열린 괄호가 닫히기 전 빈 줄을 문단 종료로 쓰지 않는다 |
| JS 내부 | 문자열·template·보간식·주석·정규식·JSX 태그의 수명을 구분한다. 주석만 제외하고 실제 패턴 문자열과 template 내용은 검사한다 |
| 좌표·CLI | 마스킹 전후 길이와 줄 종결자 위치가 같고 `--base`는 기존 finding을 보고하되 추가 행의 finding만 실패시킨다 |

기존 도구의 최상위 `const/let/var 식별자 =` 예제와 줄 전체 JS 주석은 호환 동작으로 유지한다. 표준 MDX 문법과 동일하다고 주장하지 않는다. 임의의 잘못된 MDX를 복구하거나 MDX 플러그인 문법 전체를 해석하는 것은 이 도구의 역할이 아니며 소비자 컴파일을 대체하지 않는다.

누적 실행 자료는 `tests/fixtures/ux/mdx-contexts.json`, 시험은 `tests/test_ux_mdx_context.py`다. 기대값을 고정 버전 `@mdx-js/mdx` 3.1.1과 별도 대조하는 `tests/verify_mdx_reference.mjs`는 개발 검증 전용이며 제품 외부 의존 0 조건에 포함되지 않는다. 정상 MDX 대조, 호환 시험, 실행하지 못한 검증은 각각 기록한다. 실제 누락·오탐을 시험 범위에서 제거하는 방법으로 통과시키지 않는다.

문법 근거: [MDX 공식 설명](https://mdxjs.com/docs/what-is-mdx/)(문서 수정 2025-01-27, 조회 2026-09-08)의 표현식·ESM·Markdown 구분과 [CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/)의 block/inline 우선순위를 사용한다. 참조 파서 재현은 공통 저장소에서 `npm install --prefix .git/codex-audit/mdx-oracle --ignore-scripts --no-audit --no-fund @mdx-js/mdx@3.1.1` 후 `node tests/verify_mdx_reference.mjs .git/codex-audit/mdx-oracle/node_modules/@mdx-js/mdx/index.js`로 실행한다. 설치 경로는 검증용 Git 내부 임시 자료이며 배포·커밋 대상이 아니다.

### 최종 확인

- map 기본값(`tokens.css` 단독)에서 `kt_contrast` 전 쌍 통과(exit 0), 변환값이 map 문서 실측과 ±0.05 이내.
- 4앱 예제에서 조사 문서의 미달(ktdm brand 3.59, concierge 2.06/1.93, geo 2.29/2.41)이 재현되고 baseline 등록 시 `--fail-new`가 exit 0, baseline `until` 만료 fixture는 exit 1. Airport line은 기존 조사 스냅샷의 선형 합성 값 1.15를 보존하되, 현재 결정된 CSS sRGB source-over 계산의 수용 기준을 1.32(실측 1.320934, 오차 ±0.05)로 둔다.
- `ux_lint` fixture에서 7 패턴 + `window.confirm` 각각 양성 1·음성(백틱 인용) 1이 기대대로 판정되고, `--base`는 추가 행만 fail한다.
- 두 도구 모두 `--json`·step summary 출력, Linux·Windows 결과 동일, 외부 의존 0.
- 검사기 정상·대비 미달 fixture가 재사용 워크플로에서 호출 가능한 CLI 계약을 검증한다. 워크플로 자체 selftest는 후행 T-010이 소유하며 이 task의 완료 선행이 아니다.

## 검증 명령

```bash
python3 -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css; echo "exit=$?"
python3 -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css packages/tokens/examples/docker-manager-overrides.css --baseline packages/tokens/examples/docker-manager.contrast-baseline.example.json --fail-new; echo "exit=$?"
python3 -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --base HEAD~1; echo "exit=$?"
python3 -B -X utf8 -m unittest discover -s tests -p "test_kt_contrast.py" -v
python3 -B -X utf8 -m unittest discover -s tests -p "test_ux_lint.py" -v
```

Git Bash에서 동일.

## evidence

- 테스트 수·exit code·4앱 결과 표·변환 검증 표를 이 절과 `docs/journal.md`에 남긴다. 실제 앱 저장소에서의 실행은 각 이관 task evidence이며 여기서는 `NOT_RUN(앱 task)`.

## rollback 또는 release 차단 조건

- 도구·예제만 바뀌므로 `git revert` 1회로 원복한다.
- map 기본값이 통과하지 못하면 토큰 값 또는 검사 쌍 정의 중 하나가 틀린 것이므로 T-109 rc 발행을 차단한다. 검사를 끄는 옵션은 두지 않는다([실패 패턴](../runbooks/agent-failure-patterns.md) `kt-contrast` 행).
