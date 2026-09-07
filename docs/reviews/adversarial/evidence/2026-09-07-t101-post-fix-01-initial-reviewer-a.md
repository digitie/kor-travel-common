# T-101 독립 적대적 리뷰 A 원본

- 실행 ID: A-T101-20260907-214918
- 판정: **BLOCK**. P1 1건, P2 7건(총 8건). P0/P3 신규 발견 없음. 모든 finding은 OPEN이며 수정 후 같은 새 후보에서 재검토해야 한다.
- immutable candidate: `f8894e293ca9677f457011197052cd55dbdc9696`
- base/parent: `cf2c610cecfa7a9b8f7a035c9529d7a296e27527`
- tree: `30a25801de43472d322f560897cc6dc8e29daa52`
- 격리: `F:/dev/kor-travel-common-wt/review-t101-a`, 새 detached worktree.
- 시작: 2026-09-07 21:49:18.589 KST. 종료 상태 확인: 2026-09-07 21:55:49.012 KST.
- 시작/종료 HEAD와 tree는 위 값으로 동일하고 `git status --porcelain=v1`는 빈 출력(clean).
- candidate 소스·문서·테스트·source `.git/config`는 수정하지 않았다. 빌드/test가 dist에 쓰므로 패키지를 임시 사본에 복사한 뒤 실행했다. 소비자 저장소는 고정 map 원천만 읽었으며 쓰기·commit·push·게시 없음. 상대 reviewer 결과 비열람.

## 요청과 검토 범위

T-101 npm package exports/build generator, CSS token·dark·shadcn·base 계약, generated drift, 정확한 수용 기준을 독립 검토했다. 28개 candidate delta, task, 관련 architecture/standards 및 `kor-travel-map@c494e227e010565be295de3f9670b2f7c8c20944`의 `packages/kor-travel-map-admin/frontend/src/app/globals.css`를 직접 읽었다. 기존 테스트의 성공 주장이나 작성자 evidence로 아래 실패를 대체하지 않았다.

## 실행 검증과 한계

| 검증 | Windows | WSL |
|---|---|---|
| Python 전체 `python -B -X utf8 -m unittest discover -s tests -q` | 203 tests, 69.389초, OK, skip 0 | 203 tests, 44.992초, OK, skip 0 |
| 임시 사본 npm ci/build/check/test | exit 0, 6 tests/skip 0 | exit 0, 6 tests/skip 0 |
| npm pack → 임시 프로젝트 install | 성공 | 성공 |
| 공개 subpath 11개 resolve 및 ESM import | 성공, tokenValues 44개 | 동일 |
| plan | 106 task, 오류 0 | 동일 |
| 문서 links | 355 documents, 2306 targets, 오류 0 | 동일 |
| SPDX | 41파일, 오류 0 | 동일 |
| secret/redaction `--all` | 각 466파일, 발견 0, 예외 0 | 동일 |
| check_versions self-check | exit 0 | exit 0 |
| base..candidate diff check | exit 0 | exit 0 |

- Windows: Python 3.14.3, Node v25.9.0/npm 11.12.1. npm ci의 엔진 경고를 숨기지 않았다. WSL: Python 3.11.15/jsonschema 4.26.0, Node v22.22.2/npm 11.19.1. 로컬 exact Node 22.23.1은 NOT_RUN(미설치); WSL은 선언된 ^22.12.0 범위 안이다.
- tarball은 LICENSE/NOTICE/THIRD_PARTY_NOTICES·CSS 7종·JSON/TS/JS/preset·index.d.ts를 포함했다. aliases는 후속 T-102 범위임을 확인했다.
- exact PR #11 head는 candidate이고 draft=true. [CI 34123916314](https://github.com/digitie/kor-travel-common/actions/runs/34123916314)의 docs, tools 양 OS, secret-scan, check-versions, packages **6개 최종 SUCCESS**를 직접 조회했다.
- 아래 실제 CSS 컴파일은 임시 audit 사본에서 registry 권장 Tailwind 4.3.3 및 Tailwind 3.4.19, PostCSS 8.5.8로 실행했다. 브라우저 검증은 로컬 Playwright Chromium headless에서 수행했다. WSL의 CSS 브라우저 검증은 NOT_RUN이며 Windows 실제 컴파일/계산값과 양 OS 생성기/패키지 검증을 구분한다.
- NOT_RUN: 실제 main/release push CI의 이번 변경에 대한 head/source 실행 증명, kt_contrast(T-103 전), 소비자 build/e2e, 실제 Release·npm/PyPI 게시. task/초안을 종료하거나 이 외부 gate를 통과로 표시하지 않았다.
- WSL 첫 npm probe는 Windows npm.cmd를 먼저 고른 reviewer harness 경로 오류로 실패했다. OS별 npm 선택을 수정한 후 WSL 전 명령이 성공했다. 이는 candidate 실패로 집계하지 않았다.

보존 재현 명령(후보 루트 cwd):

```text
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-a-package.py
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-a-values.py
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-a-gates.py
```

WSL은 `/mnt/f/...` 경로와 `uv run --no-project --python 3.11 python -B -X utf8`를 사용했다. 전체 Python 테스트만 `--with jsonschema==4.26.0`을 추가해 skip을 방지했다. WSL Git 읽기는 GIT_DIR/GIT_WORK_TREE 프로세스 환경만 지정했으며 source config를 수정하지 않았다.

CSS fixture cwd는 `F:/dev/kor-travel-common/.git/codex-audit/t101-css-a`이며 `node probe.mjs`로 재현한다. 이곳의 tokens 사본·compiled-v4.css·compiled-v3.css는 candidate 밖의 독립 probe 산출물이다.

## A-T101-P1-01 — 공개 tokens.json이 DTCG 값·계층 규격을 충족하지 못함

- 위치: `packages/tokens/scripts/build.mjs:67-105`, 특히 94행. 생성 대상 `dist/tokens.json`.
- 재현: `t101-a-values.py`. `z.nav.$type=number`인데 값은 문자열 `"30"`, radius.control은 dimension인데 `"0.375rem"`, ease.out은 cubicBezier인데 CSS 함수 문자열이다. brand는 `$value`를 가진 token이면서 hover/tint/foreground 자식 token을 함께 가진다.
- 출력: `DTCG z.nav actual str required number`, `radius.control actual str required object`, `ease.out actual str required 4-number array`, `DTCG-token-group-collision True`.
- 근거: task 구현 5·TK-1·architecture packages는 DTCG 전달을 요구한다. [DTCG 2025.10 Format §6.1, §8](https://www.designtokens.org/tr/2025.10/format/)은 token/group 혼합을 오류로 보고하고 number/dimension/cubicBezier 등의 실제 JSON 자료형을 정한다. 후보의 `$schema`가 가리키는 표준과도 호환되지 않는다(2026-09-07 공식 문서 확인).
- 영향: JSON을 parse하는 것만 성공하며 DTCG 도구가 공용 값·참조를 정상 교환할 수 없다. 이 task의 핵심 공개 산출물 계약 실패다.
- 권고/disposition: **OPEN, 수정 필요**. CSS를 DTCG 타입별 값으로 변환하고 계층 충돌은 `$root` 등 규격 구조로 풀며 alias와 profile metadata도 규격에 맞춰 배치한다. 실제 DTCG 구조/타입 검증을 시험에 추가한다.

## A-T101-P2-02 — Tailwind v4 z-kt-* 유틸리티가 생성되지 않음

- 위치: `packages/tokens/theme.css:47-51`.
- 재현: `node probe.mjs`, Tailwind 4.3.3에 theme.css를 import하고 z-kt-nav/z-kt-modal을 명시 후보로 build.
- 결과: `v4-utility z-kt-nav false`, `v4-utility z-kt-modal false`. ease/duration 대조군은 true.
- 영향: z 토큰은 존재하나 공개 사용 클래스가 무효라 nav/panel/overlay/modal/toast 계층 값이 CSS에 적용되지 않는다. TK-1의 파일 표도 `@utility z-kt-*`를 요구한다.
- 권고/disposition: **OPEN**. 각 z 역할을 실제 `@utility z-kt-* { z-index: var(--kt-z-*) }`로 발행하고 build 출력/계산값으로 검증한다.

## A-T101-P2-03 — v3 preset의 easing 설정 키가 틀림

- 위치: `packages/tokens/scripts/build.mjs:144` 및 생성 preset.
- 재현: `node probe.mjs`, Tailwind 3.4.19에 preset과 ease-kt-out/ease-kt-in을 넣어 CSS 생성.
- 결과: 두 easing 클래스 false; duration-kt-fast/bg-kt-brand/z-kt-modal 대조군은 true. 로컬 v3 corePlugins도 `transitionTimingFunction`을 읽는다.
- 근거: [Tailwind v3 timing function 문서](https://v3.tailwindcss.com/docs/transition-timing-function)의 설정 키와 실제 설치한 v3 구현을 대조했다.
- 영향: v3 소비자가 공용 ease 값을 선택할 수 없고 브라우저 기본 easing으로 떨어진다.
- 권고/disposition: **OPEN**. `timingFunction`을 `transitionTimingFunction`으로 고치고 preset 실제 CSS 생성 시험을 추가한다.

## A-T101-P2-04 — dark-media가 OS 토큰과 class 전용 dark variant를 섞음

- 위치: `packages/tokens/dark-media.css:5`.
- 재현: Tailwind 4.3.3 + theme/shadcn/base/dark-media를 컴파일하고 Chromium colorScheme=dark, html class 빈 상태에서 `bg-kt-surface-page dark:bg-kt-brand` 요소를 렌더한다.
- 실제 생성 selector는 `.dark\:bg-kt-brand:is(.dark *)`. 계산값은 OS dark=true, root color-scheme=dark지만 배경은 `oklch(0.19 0.006 150)`(page)이며 dark brand는 `oklch(76% 0.085 169)`이다.
- 영향: media 모드를 선택한 앱에서 semantic 토큰은 dark가 되는데 dark: 클래스는 class가 없어서 작동하지 않는다.
- 권고/disposition: **OPEN**. media 파일의 dark variant도 prefers-color-scheme 조건으로 발행하고 html class 없이 OS light/dark 모두 확인한다.

## A-T101-P2-05 — scoped base가 다크 표면의 네이티브 컨트롤을 light로 덮음

- 위치: `packages/tokens/base.scoped.css:7-8`.
- 재현: `node probe.mjs`, theme + base.scoped + dark-class import, html.dark 안 `[data-kt-surface=admin]`에 input을 둔다.
- 결과: `scoped-scheme { root: 'dark', surface: 'light', input: 'light' }`.
- 영향: base.css의 root 기본값과 달리 모든 scoped descendant에 light를 직접 선언하여 dark 상속을 차단한다. 공용 dark 색 위에서 네이티브 컨트롤·스크롤바는 light가 된다.
- 권고/disposition: **OPEN**. 기본 color-scheme 선언을 root/명시 표면 활성화 경계로 제한하고 다크 상속을 보존한다. scoped 기본과 dark 조합의 계산값을 시험한다.

## A-T101-P2-06 — 생성기의 profile·media 값은 tokens.css 변경을 따라가지 않음

- 위치: `packages/tokens/scripts/build.mjs:78-86`, `packages/tokens/dark-media.css:10-38`.
- 재현: `t101-a-package.py`는 임시 사본의 양 모드 radius-control을 0.625rem, dark brand를 77%로 바꾸고 build/check를 실행한다.
- 양 OS 결과: build/check exit 0인데 `profile-radius 0.375rem token-radius 0.625rem dark-media-old True`.
- 영향: CSS 단일 정본을 수정하고 생성물을 재생성해도 JSON profile와 media 모드가 별도 하드코딩 값으로 남는다. `--check`도 이를 clean으로 보고한다. task 목표·TK-1의 단일 정본/동기화 계약을 보장하지 못한다.
- 권고/disposition: **OPEN**. profile 값은 이미 읽은 정본 토큰에서 파생하고, media 값도 생성하거나 check에서 정본과 전수 대조한다. 타입 스케일 등 별도 하드코딩 값의 정본 위치도 같은 원칙으로 맞춘다.

## A-T101-P2-07 — CI가 drift를 검사 전에 덮어써서 통과시킴

- 위치: `.github/workflows/docs.yml:183-185`; `packages/tokens/test/values.test.mjs:129-132`도 생성물을 다시 쓴다.
- 재현: 임시 사본 `dist/tokens.json`을 `{}`로 바꾼 후 `t101-a-package.py`가 현재 CI 순서를 실행한다.
- 양 OS 결과: `tampered-precheck 1`이지만 `ci-build 0`, `ci-check 0`, `ci-test 0`.
- 영향: 잘못 커밋한 생성물을 CI가 고친 뒤 자기 결과만 비교한다. 저장소 생성물 drift 0이라는 gate가 없어지고 Git 의존 소비자가 받는 dist와 CI tarball의 파일이 달라질 수 있다.
- 권고/disposition: **OPEN**. build 전에 --check를 실행하거나 재생성 후 `git diff --exit-code -- packages/tokens/dist`를 수행한다. 시험이 먼저 drift를 지우지 않는 순서도 고정한다.

## A-T101-P2-08 — map 고정값 비교 시험이 다크 값 변경을 놓침

- 위치: `packages/tokens/test/values.test.mjs:80-99`.
- 재현: `t101-a-values.py`는 임시 tokens.css에서 `--kt-warning-tint: oklch(30% 0.045 80)`을 33%로 변경하고 전체 npm test 및 생성기 --check를 실행한다. 고정 map c494e227 원천은 직접 읽어 30%임을 확인했다.
- 양 OS 결과: `map-dark-value-mutated-test-exit 0`, 6 tests 전부 통과, `map-dark-value-mutated-check-exit 0`.
- 영향: dark expected 표는 일부 값만 대조하고 나머지는 존재성만 확인한다. task가 요구한 map 값 1:1·diff 0을 시험이 보장하지 못하므로 ADR 없이 값 변경이 통과할 수 있다.
- 권고/disposition: **OPEN**. 고정 원천에서 모든 대상 역할의 light/dark 값을 추출한 검증 가능한 매핑을 사용하고, 허용 파생 alias는 실제 의미값까지 비교한다. 비교 누락 역할을 바꿨을 때 시험이 실패해야 한다.

## 판정 범위

위 재현은 현재 후보의 문제다. candidate의 exports/tarball 기본 설치와 이미 실행한 정적·단위 gate는 성공했지만, 그 성공이 DTCG 상호운용·실제 Tailwind CSS·다크 합성·drift gate의 실패를 해소하지 않는다. 8개 OPEN finding을 수정 또는 정본 계약에 맞게 처분한 새 immutable 후보의 양 reviewer 재검토가 필요하다.
