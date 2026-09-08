# T-103 상태 스택 구조 수정 독립 적대적 리뷰 B

## 판정과 실행 기준

- 최종 판정: **BLOCK**. 신규 `B-P1-30` 1건, `B-P2-31` 1건과 별도로 작성자가 제보하여 직접 재현한 기존 evidence 오류 `B-P2-32`가 OPEN이다. P0/P3 신규 0건이다.
- 실행 ID: `T103-ROOT-B-20260908-191918`; 시작 KST `2026-09-08T19:19:18.9092077+09:00`, 제품 검증 종료 KST `2026-09-08T19:29:22.6385755+09:00`.
- 제품 시작·종료 HEAD: `b013ab0d2e95e3d892f6dbfa42042389582ea8a9`; 시작·종료 tree: `de5b30f25840bd9da19f073f62ae6bc9607fa7ef`.
- 격리: `review-t103-root-b` detached worktree. 시작과 제품 검증 종료의 `git status --porcelain`은 모두 빈 출력이다. 시험용 Git 저장소·파일은 별도 임시 디렉터리에서 만들고 후보의 `git archive`로 시험했다. 소비자 파일에는 접근하거나 쓰지 않았다.
- 수정 delta 기준: `841ee985db564deb0d571edb6f0f9330311a35d6`; 전체 7파일, 987줄 추가·551줄 삭제를 검토했다. 후보 제품·manifest·기존 evidence는 수정하지 않았다. 이 원본 한 파일만 후속 커밋한다.
- 공통 manifest: `4ddb9601149a85202486719e7ab16dbb4448b8ac:docs/reviews/adversarial/evidence/2026-09-08-t103-root-fix-manifest.md`. Git blob SHA-256: `aad8f0866039131e5e9571f4c108356144fdb84666bd676add42a638368a17c9`.
- source `.git/config` 시작·종료 SHA-256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. Git 환경 변수를 제거한 별도 시험 프로세스를 사용했고 `core.worktree`나 다른 Git 설정을 변경하지 않았다.
- 상대 reviewer의 이번 원본/결과를 열람·요청하지 않았다. 과거 상대 raw 본문도 사용하지 않았다. 아래 airport 항목은 coordinator 제보를 명시하고 직접 재현한 결과다.

전달받은 공통 요청 원문:

> 상태 추정 helper를 상태 스택으로 교체한 전체 delta와 자신의 누적 finding closure를 독립적으로 검사한다. 상대 reviewer의 이번 결과는 두 원본 확정 전 읽거나 전달받지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인한다. 제품 코드는 수정하지 않고 한국어 raw report 한 파일만 별도 commit한다. 기준선 관찰·실행 ID·시각·실제 명령·미검증 범위·finding의 위치/재현/영향과 최종 verdict를 기록한다.

전문 범위는 참조 파서와 기대값 독립성, Git 추가행, 컨테이너·줄 종결자, TS/TSX/CSS·입력 오류·CLI·의존성·evidence 정합이다. [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 현재 수용 기준과 [agent workflow](../../../runbooks/agent-workflow.md)의 심각도·disposition·판정을 적용했다.

## 실제 실행과 재사용 구분

| 검증 | 독립 실행 결과 |
|---|---|
| Windows Python | `py -3.14 --version`: 3.14.3 |
| WSL Python | 명시 경로 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`: 3.11.15 |
| 집중 회귀 | `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint tests.test_ux_mdx_context`: 양 OS 79 실행·성공, skip 0; Windows 69.309초, WSL 16.024초 |
| 별칭 회귀 | `python -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py`: Windows 35 실행·성공/skip 0, WSL 35 수집·34 실행·성공/Windows 전용 skip 1 |
| 계획·링크 | 양 OS `validate_plan.py`: 106 task/오류 0; `validate_document_links.py`: 503문서·2506대상/오류 0 |
| 고지·정보 검사 | 양 OS `check_spdx.py`: 58파일/오류 0; `scan_secrets.py --all`, `check_prod_redaction.py --all`: 각각 638파일/finding 0 |
| 정본·기존 CLI | 양 OS `check_versions.py --self-check` exit 0, `check_aliases.py packages/tokens/aliases` CSS 1/오류 0, `kt_contrast.py packages/tokens/tokens.css --json` light 27쌍 PASS, `ux_lint.py --root tests/fixtures/ux --json` finding 12/fail_count 0 |
| 후보 제공 참조 자료 | Windows Node 25.9.0에서 `node tests/verify_mdx_reference.mjs <고정 @mdx-js/mdx/index.js>`: 398대조 항목 중 396 PASS, 호환 문법 2건 NOT_RUN, exit 0 |
| 별도 파서 대조 | 후보 기대값을 읽어 복제하지 않은 12개 입력 × plain/blockquote/nested 3종 × LF/CRLF/CR 3종 = 108개 모두 MDX 3.1.1 구문 트리 생성 성공. AST code/inlineCode 및 주석 범위를 제외해 독립 기대값 생성 |
| 추가 CLI | 양 OS 각 108파일 × 일반 fail-new/새 추가행/기존행 3모드 = 324행 대조. 아래 두 결함에 따른 54행 불일치, 나머지 270행 일치. 기존행 모드의 fail 합계 0. 6개 최소 입력의 JSON/Markdown/step-summary 18회 및 airport light/dark 2회도 각각 실행 |
| diff·고정성 | `git diff --check 841ee985db564deb0d571edb6f0f9330311a35d6 b013ab0d2e95e3d892f6dbfa42042389582ea8a9`: exit 0. 제품과 manifest head 사이 diff는 manifest 한 파일 추가뿐 |

집중 회귀에는 CSS selector·media 교집합, `+++`·Unicode 줄 종결자와 Git 추가행, JSON 거대 정수·깊이, baseline 수량/만료, 외부 root, 오류·경로 redaction 검사가 포함된다. 새로운 동일 반례를 양 OS에서 확인했고, 운영 정보와 비밀 원문을 출력하거나 보고서에 넣지 않았다.

첫 WSL 실행에서 기본 `python3`가 3.14.4임을 확인했다. 그 결과를 WSL 3.11 실행으로 세지 않고 명시적인 3.11.15 경로로 집중 시험·정적 gate·324행 CLI를 다시 실행했다. 위 표는 3.11.15 결과다. 추가 3.14.4 관찰도 반례의 결과는 같았다.

**전체 317시험은 이번 reviewer가 재실행하지 않았다.** manifest에 기록된 동일 제품의 작성자 Windows 317 실행/skip 0, WSL 317 수집·316 실행/skip 1을 재사용 evidence로만 보존한다. `gh run view <run> --json headSha,status,conclusion,jobs`를 직접 실행해 다음을 별도로 확인했다.

- 제품 SHA `b013ab0...`의 run `34214642467`: completed/**cancelled**. Windows tools job이 취소됐으므로 전체 CI PASS로 세지 않는다.
- manifest SHA `4ddb960...`의 run `34214737342`: completed/**success**, 6개 job 전부 success. 제품과 시험 변경이 없는 별도 SHA의 성공이다. 이를 제품 SHA 자체의 완료 run으로 바꾸어 기록하지 않는다.

## 이전 B finding disposition

| 원 ID·심각도 | 이번 판정 | 직접 근거 |
|---|---|---|
| B-P1-28 | FIXED | 미종결 1·2자 span 뒤 URL/prose와 실제 실행식이 있는 입력의 18변형에서 P8 유지. 정상 MDX AST와 일반/추가행/기존행 report 일치 |
| B-P2-27 | FIXED | apostrophe가 있는 본문 뒤 fence의 18변형에서 문서 P8 제외. 실제 파서도 code block으로 분류 |
| B-P2-29 | FIXED | apostrophe 본문 뒤 실제 JS 주석과 fence의 18변형에서 주석·문서 P8 제외. 실제 파서 comment 범위와 일치 |

위 54입력은 각 3모드에서 재현했다. 더 앞선 누적 finding은 후보가 제공한 집중 회귀와 참조 자료 및 동일 제품의 전체 시험 evidence로 회귀를 확인했다. 이 회차에 모든 과거 raw의 최소 입력을 다시 수작업으로 실행했다고 주장하지 않는다. 위 closure는 새 JS 문법 경계의 완전성을 뜻하지 않는다.

## B-P1-30 — `in` 뒤 정규식을 잘못 분류하여 실행 template를 문서로 제외

- 심각도·상태: **P1 / OPEN / 수정 필요**.
- 위치: [tools/ux_lint.py](../../../../tools/ux_lint.py) 666~686행(정규식), 708~718행(단어 뒤 operand 상태), 특히 716행.
- 최소 정상 MDX 파일:

````mdx
{"test" in /}/ && `outline-none`}
````

- 실제 명령: `python -B -X utf8 tools/ux_lint.py --root <위 파일만 둔 임시 root> --fail-new --json`.
- 기대: P6 1건, fail_count 1, exit 1. 실제: findings 빈 배열, status PASS, fail_count 0, **exit 0**. Markdown·step-summary도 동일하게 PASS를 표시한다. stderr는 비어 있다.
- 참조 파서: `@mdx-js/mdx` 3.1.1 `createProcessor().parse(source)` 성공. code/inlineCode/comment 범위가 없고 `outline-none`의 offset 19가 실행식 template 안에 남는다. `"test" in /}/` 자체도 RegExp의 `test` 속성을 검사하는 정상 표현식이다.
- 원인: `in`이 operand를 요구하는 이항 연산자로 분류되지 않는다. 다음 `/`를 정규식으로 소비하지 않아 그 안의 `}`가 MDX 표현식을 닫고, 이후 백틱이 prose inline span으로 마스킹된다.
- 교차 재현: LF/CRLF/CR × plain/`> `/`>> `의 9변형 모두 일반 및 `--base <빈 파일 기준 commit>` 추가행에서 P6 누락. 이미 커밋한 파일도 report 자체에서 누락된다. 직접 정규식 시작 대조 ``{/}/.test("}") && `outline-none`}``는 P6를 검출한다. 양 OS 결과 동일.
- 영향: 정상 MDX 실행 코드의 금지 패턴이 일반·PR 신규행 gate를 통과한다. 단순 잘못된 문법의 복구 문제가 아니다.
- 최소 수정 방향: 정규식/나눗셈 선택을 실제 JS 토큰 문맥에 따라 결정하고 `in`을 포함한 연산자 뒤 operand 상태를 검증한다. 문법을 지원하지 못하는 상태에서 조용히 Markdown으로 복귀하지 않는다. 외부 파서를 런타임에 채택한다면 현재 stdlib 계약과 설치·오류·CI 요구 변경을 ADR/task에 먼저 명시한다. 위 9변형 및 정규식/나눗셈 양성·음성 대조를 고정 회귀에 추가한다.

## B-P2-31 — 공백 없는 비교 연산자를 JSX 시작으로 오해하여 fence 오탐

- 심각도·상태: **P2 / OPEN / 수정 필요**.
- 위치: [tools/ux_lint.py](../../../../tools/ux_lint.py) 687~692행.
- 최소 정상 MDX 파일:

````mdx
{1<a ? "yes" : "no"}

~~~js
{window.confirm("doc")}
~~~
````

- 같은 CLI의 기대: finding 0, exit 0. 실제: fenced 문서의 P8 1건, fail_count 1, **exit 1**. JSON/Markdown/summary에 같은 오탐이 나타난다. `--base`에서도 새 위반으로 실패 처리된다.
- 정상 대조: 첫 줄을 `{1 < a ? "yes" : "no"}`로만 바꾸면 finding 0/exit 0이다. MDX 파서는 두 입력 모두 정상으로 처리하며 no-space 입력의 22~55 offset을 code block으로 분류한다.
- 원인: JS 상태에서 `<` 뒤 영문자가 있다는 이유만으로 tag frame에 진입한다. 직전 토큰이 값이고 현재 위치가 비교 연산자 자리인지 확인하지 않아 표현식 닫힘 및 이후 Markdown fence가 tag 안에 갇힌다.
- 교차 재현: LF/CRLF/CR × plain/blockquote/nested 9변형 모두 같은 오탐. 기존행 모드에서는 P8 report가 남되 added=false/fail=false이므로 추가행 필터 자체는 보존된다. 양 OS 결과 동일.
- 영향·권고: 정상 문서가 검사 실패하며 의미가 같은 공백 편집으로 verdict가 달라진다. JSX는 실제 operand 위치에서만 열고 `<`, `<=`, shift와 JSX의 문맥 대조를 넣는다. 예제의 식별자 `a`가 앱에서 정의됐는지 실행 평가할 필요는 없으며 파서 수준에서 정상인 입력이다.

## B-P2-32 — airport dark 검증 evidence가 실제 실패를 성공으로 기록

- 심각도·상태: **P2 / OPEN / evidence 정정 필요**. coordinator가 독립 종료 점검에서 제보했고 reviewer가 현재 후보로 양 OS에서 재현했다. 이번 7파일 구조 변경에 도입된 코드 결함으로 분류하지 않는다.
- 위치: [docs/evidence/t103-kt-contrast-ux-lint.md](../../../evidence/t103-kt-contrast-ux-lint.md) 13행.
- 실제 명령: `python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css packages/tokens/examples/airport-overrides.css --dark --baseline packages/tokens/examples/airport.contrast-baseline.example.json --fail-new --json`.
- 실제: 27쌍 중 **10미달, control-line 예외 4건 + 신규 미달 6건**, status FAIL, exit 1. 표는 dark 미달 4건과 baseline exit 0을 적었다. `--dark`를 뺀 light 대조는 4미달/예외 4건/exit 0이다.
- 신규 미달: text-primary/secondary/strong/tertiary × surface-subtle 4쌍, icon × surface-subtle/muted 2쌍. 예: primary/subtle 1.030161565..., secondary/subtle 1.854142677...이며 기준 미만이다.
- 영향·권고: 이관 담당이 예제의 dark gate도 통과한 것으로 오인한다. light/dark 결과와 baseline 적용 후 실패 건수를 구분하고 명령·후속 소유 task를 정정한다. 기존 조사 스냅샷을 성공시키려고 임의로 토큰이나 baseline 예외를 늘리지 않는다.

## 재현 자료와 한계

독립 보조 입력·결과는 제품 바깥의 `.git/codex-audit/`에 보관했다. 실제 실행은 `py -3.14 -B -X utf8 .git/codex-audit/t103-root-b-probe.py win`, WSL에서는 명시한 3.11 실행 파일로 같은 스크립트에 `wsl311`을 주었다. 보조 스크립트는 Git object에서 정확한 후보를 archive하고 임시 저장소의 빈 파일 commit → 입력 추가 → 현재 입력 commit 순서로 일반/추가행/기존행을 검사한다. 참조 파서는 `node .git/codex-audit/t103-root-b-oracle.mjs .git/codex-audit/t103-root-b-expanded.json`으로 실행했다.

| 로컬 보조 자료 | SHA-256 |
|---|---|
| `t103-root-b-probe.py` | `90986022267ad629eb6cff61e6c831420c159b5163474b0c38335421efce2591` |
| `t103-root-b-oracle.mjs` | `78025362a85d4558b6d6c2c2f661cb7cabf91360a2bd93137703225f32c3838e` |
| `t103-root-b-expanded.json` | `4f66f6a1aa9fa8746734968ec0f6cbec0e39dfb2f2af50077975496a9ee4cfae` |
| `t103-root-b-oracle-results.json` | `3420c090b43afc57f0e8cda30dfb73c507d630a61ac0f4263f0c7f267517d640` |
| `t103-root-b-win-probes.json` | `28e69fffb1d3af320e46d91d8fa040b8e9ac251369bd62c769cb330978a2817e` |
| `t103-root-b-wsl311-probes.json` | `9aed178ee9d0631f2a7c6bf0fd8d2ba922316032eef44d06a5ac8565c35cb796` |

두 OS의 입력별 pattern/expected/fail/exit 튜플은 모두 같았다. 참조 파서는 개발용 임시 의존이며 package manifest/lock·배포 자산을 변경하지 않았다. stdlib/GPL 고지·공용 라이브러리·소비자 분리 경계는 유지된다.

- `NOT_RUN(Windows Python 3.11 실행 파일 부재)`.
- `NOT_RUN(이번 reviewer의 전체 317시험 중복 실행)`: 작성자 동일 후보 evidence와 manifest head CI를 위와 같이 구분하여 재사용했다.
- `NOT_RUN(실제 MDX compile/render/browser·런타임 평가)`: AST 구문 및 범위만 대조했다. 개발 파서 oracle 실행과 혼동하지 않는다.
- `NOT_RUN(소비자 build/e2e·버전 검사·외부 이관 gate)`, `NOT_RUN(npm/PyPI 게시·workflow dispatch)`: 이 리뷰의 권한·범위 밖이며 수행하지 않았다.

원본을 확정한 뒤 후보 수정은 수행하지 않는다. P1 미해결 상태이므로 merge 가능한 PASS로 해석할 수 없다.
