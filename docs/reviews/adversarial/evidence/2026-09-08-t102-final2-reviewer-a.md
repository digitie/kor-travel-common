# T-102 최종2 독립 적대적 리뷰 A 원본

- 실행 ID: `A-T102-FINAL2-20260908-001654`.
- 시작: 2026-09-08 00:16:54.149 KST. 종료: 2026-09-08 00:21:13.265 KST.
- 후보: `ded1631b81d464ed919d36d73ab9c2a1111d38f4`.
- tree: `41dd1c6551994b62d94a04c8a3c1f8bf98414de7`.
- parent: `0b50a6387e8e4269dc60b53041de0d65cd2086cb`.
- 직전 리뷰 기준: `09162025140991d24775abc76571f35de9974022`.
- 전체 base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`.
- 격리: `F:/dev/kor-travel-common-wt/review-t102-final2-a`를 exact candidate에서 새 detached worktree로 생성했다. 시작과 종료 `git rev-parse HEAD 'HEAD^{tree}'`가 위 값과 일치하고 `git status --porcelain=v1`은 두 번 모두 빈 출력이었다.
- 후보·소비자 파일과 source `.git/config`를 수정하지 않았다. build/pack/install과 고장 주입은 임시 사본 및 reviewer A 소유 `.git/codex-audit` fixture에서 실행했다. commit/push/publish는 수행하지 않았다. Reviewer B 결과는 읽거나 요청하지 않았다.

## 전달 요청 원문

> 최종2 후보 `ded1631b81d464ed919d36d73ab9c2a1111d38f4`(tree `41dd1c6551994b62d94a04c8a3c1f8bf98414de7`)를 독립 적대적으로 재리뷰하라. 공통 manifest `docs/reviews/adversarial/evidence/2026-09-08-t102-final2-manifest.md`를 읽고, 이전 A-T102-P2-06 및 전체 누적 finding을 재현하라. 특히 @media/@supports/부모 selector nested fail-closed, `:root,.dark`+root/dark 중복, 비ASCII --kt 정의/var 참조, 기존 escape/8.3/radius/dark shadow를 확인하라. detached clean에서 reviewer B 결과를 보지 말고, 후보·소비자 수정/commit/push 금지. raw는 `.git/codex-audit/2026-09-08-t102-final2-reviewer-a.md`에 저장하고 SHA256·verdict를 보고하라.

## 범위와 근거

공통 manifest, AGENTS, 문서 라우터, resume, T-102 task, TK-16, 구현 및 시험을 직접 확인했다. 직전 후보 대비 6파일 delta 중 구현·시험·manifest·attributes 전체를 검토했다. 추가된 A 원본은 자신의 확정 근거이며 B 원본 내용은 독립성 때문에 읽지 않았다. `git diff --exit-code 09162025140991d24775abc76571f35de9974022 HEAD -- packages package.json package-lock.json docs/tasks docs/standards .github/workflows`는 빈 출력·exit 0이다. 변경 없는 패키지/정본/CI의 이전 전체 검토를 동일성 근거로 재사용하되, 아래 실행 가능한 누적 반례와 package gate는 다시 실행했다.

수정 핵심은 `tools/check_aliases.py:116`의 stack 길이 1 제한, Unicode custom property/참조 토큰 인식, both 선언의 root/dark identity 확장이다. 모두 실제 CLI로 공격했다.

## 판정

**PASS.** 누적 A finding 9개가 모두 FIXED이며 이 후보에서 새 P0/P1/P2/P3 finding은 발견하지 않았다. 소비자 T-461의 실제 화면·build/e2e와 게시·release 성공을 의미하지 않는다.

| 원 ID | 원 심각도 | disposition | 이번 확인 |
|---|---|---|---|
| A-T102-P1-01 | P1 | FIXED | 앱별 spacing은 common 승격 대신 weather 예제에 보존. 실제 CSS 대조에서 누락 0, `space-md` 16px |
| A-T102-P2-02 | P2 | FIXED | weather light/dark 변수 전수 대조 changed 0. dark elevated/modal shadow alpha는 원천 상속값 0.1/0.14 유지 |
| A-T102-P2-03 | P2 | FIXED | dark 블록 삭제 CLI exit 1, 오류 76개; 정상 중첩 `.dark`의 alias/semantic 실제 값 일치 |
| A-T102-P2-04 | P2 | FIXED | 누락 대상을 가리키는 `@import url(...)` CLI exit 1 |
| A-T102-P2-05 | P2 | FIXED | 추가 import CSS의 `--kt-brand` 정의 CLI exit 1 |
| A-T102-P2-06 | P2 | FIXED | `.dark .child`, media print, supports, 부모 selector, layer, 다중 조건 stack 모두 exit 1. 정상 직접/결합 선택자는 exit 0 |
| A-T102-P2-07 | P2 | FIXED | escape를 쓴 kt 정의와 var 참조 모두 exit 1, traceback 없음 |
| A-T102-P1-08 | P1 | FIXED | 실제 Windows GetShortPathNameW 8.3 경로와 long 경로 모두 exit 0; 같은 파일임을 확인 |
| A-T102-P2-09 | P2 | FIXED | map shim `radius-md` control 6px, weather 예제 panel 8px. 패키지 CSS/예제 byte 동일성 및 실제 CSS 계산 확인 |

## 직접 고장 주입

Reviewer A 소유 `F:/dev/kor-travel-common/.git/codex-audit/t102-final2-a-probe.py`를 candidate cwd에서 실행했다. 파일은 package 임시 사본에만 입력을 쓰고 실제 CLI를 subprocess로 호출하며 예상 exit와 redaction을 assert한다. Windows Python 3.14.3 및 WSL Python 3.11.15에서 다음 결과가 동일했다.

| 입력 | 기대/실제 |
|---|---|
| 독립 `:root`·`.dark`, 단일 `:root,.dark`, 순서 반대의 결합 선택자 | exit 0 |
| both+root / both+dark / both+both | exit 1, 중복 오류 각각 1/1/2개 |
| `.dark`를 `@media print`, `@supports (display:grid)`, `.wrapper`로 감쌈 | exit 1, 각각 오류 3개 |
| 전체 root/dark를 `@layer`로 감쌈 | exit 1, 오류 4개 |
| 결합 선택자를 media로 감쌈 / media+supports 다중 중첩 | exit 1, 각각 오류 3개 |
| `--kt-한글`, `--kt-😀` 정의 | exit 1, 각각 오류 2개 |
| 미정의 `var(--kt-없는)`, `var(--kt-brand한글)`, `var(--kt-😀)` | exit 1, 각각 오류 2개 |
| 문자열과 주석에만 Unicode 및 var 모양 텍스트 | exit 0 |
| CSS escape가 있는 kt 참조 | exit 1 |
| 분할 생성한 marker를 경로·이름·값에 주입 | exit 1; stdout/stderr marker·경로 누출 없음, traceback 없음 |

원 P2-06 최소 반례는 정상 파일의 `.dark {`를 `@media print { .dark {`로 바꾸고 닫는 괄호를 하나 추가하는 것이다. 이전 후보는 exit 0이었으나 이번 후보는 exit 1이다. `.wrapper`·supports에도 같은 결과다. 브라우저에서 이 변형이 실제 screen의 dark alias를 light로 남긴다는 영향도 다시 확인했다. 현재 검사기가 해당 변형을 거부하므로 잔여 실패가 아니다.

기존 `t102-post-a-original-negative.py`, `t102-post-a-negative.py`도 양 OS에서 재실행했다. missing-dark, different-dark, exact Tailwind namespace, imported-kt, missing-url, dark-descendant, escaped-kt, escaped-ref, literal-kt 총 9개가 모두 exit 1이고 stderr/traceback이 없었다.

Windows `t102-post-a-shortpath.py`: short 경로에 실제 `~`가 있었고 `same-existing-directory=True`, lexical 경로와 resolve된 long 경로가 다른 상황을 재현했다. `long exit 0`, `short exit 0`이다.

## 실행 명령과 검증 결과

모든 Python 명령에 `-B -X utf8`을 사용했다. WSL은 candidate 경로 `/mnt/f/dev/kor-travel-common-wt/review-t102-final2-a`에서 `uv run --no-project --python 3.11 python`으로 실행했다.

| 명령·gate | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -p 'test_*.py' -q` | 238 tests, 62.011s, OK, skip 0 | 238 discovered, 40.475s, OK, skip 3; 최초 실행은 235개 실행 통과 |
| `-m unittest tests/test_check_aliases.py -q` | 35 tests, 0.966s, OK, skip 0 | 35 discovered, 0.387s, OK, Windows 8.3 전용 1 skip; 34개 실행 통과 |
| `tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 문서 376개, local targets 2333개, 오류 0 | 동일 |
| `tools/validate_plan.py` | task 106개, 오류 0 | 동일 |
| `tools/check_spdx.py` | 45개 파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 491개 파일, 발견 0, 예외 0 | 이번 별도 전체 실행 NOT_RUN |
| `tools/check_prod_redaction.py --all` | 491개 파일, 발견 0, 예외 0 | 이번 별도 전체 실행 NOT_RUN |
| `tools/check_versions.py --self-check` | exit 0 | 이번 별도 실행 NOT_RUN |
| `git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f HEAD` | 빈 출력, exit 0 | Windows Git 결과 재사용 |

WSL 전체 시험의 추가 2 skip은 uv 런타임에 jsonschema가 없어서였다(`python -m pip show jsonschema`: 미설치 확인). `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest tests.test_validate_manifest.ValidateManifestTests.test_json_schema_rejects_control_character_paths_like_stdlib tests.test_validate_manifest.ValidateManifestTests.test_json_schema_rejects_non_ascii_and_trailing_newline_dates -v`로 해당 2개를 직접 보완했다: 2 tests, 0.090s, OK, skip 0. 따라서 WSL에서 실제 실행한 고유 시험은 237개이고 Windows 전용 1개만 해당 OS에서 미실행이다. skip을 성공으로 집계하지 않았다.

`t102-a-package.py`를 양 OS에서 실행했다. 임시 사본에서 `npm ci --ignore-scripts --no-audit --no-fund`, `npm run check`, `npm run build`, `npm run check`, `npm test` 전부 exit 0; package 시험 7개 통과, skip 0. `npm pack --workspace packages/tokens --pack-destination <temp> --json` 19파일, alias 포함·examples 제외 assert 성공. 임시 consumer fixture tarball 설치 및 `require.resolve('@kor-travel/tokens/aliases/map-vocabulary.css')` 성공. Windows Node 25.9.0/npm 11.12.1은 `^22.12.0` engine 경고가 있었고, WSL Node 22.22.2/npm 11.19.1이었다. 정확한 고정 CI 런타임과 로컬 런타임을 혼동하지 않았다.

## 실제 CSS·패키지 대조

`node probe.mjs`를 A 소유 `F:/dev/kor-travel-common/.git/codex-audit/t101-css-a/t102-final`에서 다시 실행했다. fixture의 tokens.css/theme.css/shadcn.css/alias CSS/날씨 예제 5개가 현재 candidate와 byte 단위로 모두 같음을 SHA256 및 byte equality로 확인했다. 실제 CSS 결과를 이전 후보의 다른 파일에 잘못 귀속하지 않았다.

- Chromium에서 고정 weather 원천 commit `6003da995fa4b35799f9dadc406c6ba2878bfbae`, `packages/kor-travel-weather-admin/frontend/app/tokens.css`의 보존 사본과 tokens+shim+weather 예제의 모든 원천 custom property를 대조했다: light `missing=[] changed=[]`, dark `missing=[] changed=[]`.
- 표본 computed 값은 양 모드 모두 spacing 16px, weather radius 8px, rail 272px(17rem), mono 스택, card 배경이 원천과 같다. shadow-card는 정상 `none`이다. dark shadow 변수도 위 전수 값 대조에 포함된다.
- shadcn import의 card/border/destructive/input/primary 값이 실제로 제공된다.
- Tailwind 4.3.3 package `@import` compile 성공, `bg-kt-brand` 출력 확인. map 의미의 `rounded-md`는 shim 전후 6px이다. 선택 shim의 `rounded-sm` 4→6px는 기존 map 별칭 의미이며 이번 radius-md 회귀와 구분했다.
- 정상 nested `.dark`의 brand/semantic은 모두 `oklch(76% 0.085 169)`이다. 삭제·자손·조건부·escape 고장 주입의 실제 CSS 실패는 재현했으나 현재 CLI가 모두 거부한다.

## CI·한계

`gh run list --commit ded1631b81d464ed919d36d73ab9c2a1111d38f4 --json databaseId,status,conclusion,headSha,url`, 이어 `gh run view 34137474603 --json status,conclusion,headSha,jobs,url`로 exact SHA를 직접 확인했다. [CI run 34137474603](https://github.com/digitie/kor-travel-common/actions/runs/34137474603)은 completed/success이며 docs, tools Ubuntu, tools Windows, secret-scan, check-versions, packages 6개 job 모두 success이고 source SHA 확인 step도 success다.

- NOT_RUN: 실제 소비자 저장소 build/e2e·T-461 6폭 화면 diff, 실제 폰트 파일/glyph 로딩, WSL 브라우저 렌더링, 로컬 정확한 고정 Node 22.23.1 실행. common fixture 검증이 이를 대체하지 않는다.
- NOT_RUN: npm/PyPI 게시, release/tag, release/main push CI, 소비자 변경. 사용자 범위 밖이다.
- 진단 중 unquoted PowerShell `HEAD^{tree}`, Windows rg glob 경로, WSL 중첩 quote 명령이 각각 파싱/경로 오류를 냈다. 올바른 quoted git ref·rg glob 옵션·pip 조회로 수정해 확인했으며 이를 후보 실패나 성공 시험으로 세지 않았다.
- Reviewer B 본문·결과는 미열람. 후보 종료 SHA/tree/clean과 diff check를 다시 확인한 뒤 이 원본을 확정했다.
