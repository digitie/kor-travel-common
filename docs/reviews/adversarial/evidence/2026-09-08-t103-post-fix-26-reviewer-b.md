<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# T-103 post-fix-26 독립 적대적 리뷰 B 원본

## 실행 기준선

- 실행 ID: `T103-PF26-B-20260908-152414`.
- 시작 KST: `2026-09-08T15:24:14.4432844+09:00`; 제품 검증 완료 관찰 KST: `2026-09-08T15:30:30.4725531+09:00`.
- 시작·종료 제품 HEAD: `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`.
- 시작·종료 제품 tree: `a08e12fc66c67dfe65015f714a69c5fc0740a3f0`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post26-b`, detached checkout. 시작·검증 종료 후 재확인한 `git status --porcelain` 출력은 비어 있다. 이후 이 원본 한 파일만 별도 branch에서 커밋한다.
- delta base: `155941045a077529cb12f875cad5ab2b2f7639da`.
- manifest: commit `af9ffdce3e9edc107572b050576a6735f0c3bdb8`의 [post-fix-26 manifest](2026-09-08-t103-post-fix-26-manifest.md). `git show` blob SHA256: `51bd7f32251033151d438e600b7c89a498f2c12eb6ba9c6274e233f5962a8e3e`.
- source `.git/config` 시작·종료 SHA256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. 후보·manifest·소비자·Git 설정·공유 branch·기존 evidence를 수정하지 않았다.
- 이전 post25 B 보고서 본문을 기준선으로 재사용하거나 읽지 않았다. 현재 제품·manifest·공식 문법과 새 실행 결과로 판단했다. 상대 reviewer의 post26 결과/raw 및 과거 상대 raw 본문을 읽거나 요청하지 않았다.

## 전달받은 요청 원문

> post-fix-26 독립 적대적 리뷰를 시작해 주세요. 후보 기준선은 코드 commit `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`, tree `a08e12fc66c67dfe65015f714a69c5fc0740a3f0`, manifest commit `af9ffdce3e9edc107572b050576a6735f0c3bdb8` (`docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-26-manifest.md`)입니다. 자신의 worktree에서 해당 tree를 확인하고, 전문 영역은 Markdown/CommonMark·ECMAScript fence masking과 경계조건입니다. 이전 post-25 B 보고서를 기준선으로 재사용하지 말고 현재 candidate를 독립적으로 검토하세요. 제품 코드/후보/공유 branch는 수정하지 말고, 원본 보고서는 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-26-reviewer-b.md`에 한국어로 작성한 뒤 report-only commit을 만들고 commit SHA와 SHA-256을 보내 주세요. manifest의 검토 규칙과 exit severity를 지키고, PASS/NO-GO를 명확히 판정하세요.

> 위 post-fix-26 리뷰 요청을 지금 실행하고, report-only commit까지 완료해 주세요. 동일 고정 기준선에서 독립 검토 후 raw report SHA/SHA-256을 회신하세요.

## 코드·문서 대조와 실행

`git diff 1559410 2a32dc7 -- tools/ux_lint.py tests/test_ux_lint.py` 전체를 읽었다. 변경은 fence 컨테이너 깊이/들여쓰기 계산과 시험 1개 추가다. 나머지 3개 변경은 직전 manifest·A/B raw의 추가이며 상대 raw는 경로만 확인했다. [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 인용 제외·추가 행 fail·CLI 계약, [evidence](../../../evidence/t103-kt-contrast-ux-lint.md)의 airport 1.320934·geo 8건·소비자/T-010 NOT_RUN, resume의 IN_PROGRESS를 직접 대조했다. GPL-3.0-or-later·common 도구·외부 의존 0·npm/PyPI 미게시·소비자 무수정 경계는 유지된다. CI·versions·공개 패키지 파일은 delta에서 불변이다.

아래 `ROOT`는 위 worktree, `AUDIT`는 source checkout의 `.git/codex-audit`다. Windows는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`을 사용했다. WSL 경로는 `/mnt/f/`로 바꿨다. helper·로그·fixture는 후보 밖에 두고 fixture 프로세스의 `GIT_*` 환경변수를 제거했다.

| 검사·명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `-m unittest discover -s tests` | 298 실행 성공, skip 0, 134.224초 | `AUDIT/review-t102-b-wsl-unittest.py ROOT` 임시 독립 사본에서 298 수집·295 실행 성공·3 skip, 34.344초 |
| `-m unittest tests.test_kt_contrast tests.test_ux_lint` | 60 성공·skip 0, 43.174초 | 60 성공·skip 0, 22.664초 |
| `AUDIT/review-t102-post-b-gates.py ROOT` | plan 106/오류 0, links 469문서·2452대상/오류 0, SPDX 56/오류 0, secrets·redaction 각각 601파일/발견 0/예외 0 | 동일 |
| 위 helper의 registry·aliases | `check_versions.py --self-check` exit 0, aliases CSS 1/오류 0 | 동일; 소비자 버전 검사 미실행 |
| 위 helper의 aliases focused | 35 성공/skip 0 | 35 수집·34 성공/skip 1 |
| `AUDIT/t103-post26-b-run-corpus.py ROOT win` 또는 `ROOT wsl` | 누적 1263개 관찰; 기대 지정 사례 중 24개 불일치 | 같은 수·입력 hash·판정 |
| `AUDIT/t103-post26-b-new.py ROOT OUTPUT_JSON` | 새 72개 CLI 교차 중 30개 불일치·42개 대조 일치 | 동일 |
| `AUDIT/t103-post26-b-base-delta.py BASE_ROOT ROOT OUTPUT_JSON` | 2개 최소 입력 × base/candidate = 4개 관찰, 아래 회귀 확인 | 동일 |
| `git diff --check 1559410 2a32dc7` | 출력 없음, exit 0 | 별도 WSL Git diff 검증은 미실행 |

WSL skip 3개는 Windows 8.3 전용 1개·선택적 jsonschema 미설치 2개다. 따라서 manifest의 WSL 297실행/1skip을 이번 독립 실행 결과로 쓰지 않는다. WSL helper는 후보에서 `.git`·`__pycache__`·`node_modules`를 제외해 임시 사본을 만들고 명시한 경로만 임시 Git에 stage한다. source Git 설정을 변경하지 않았다.

1263개 관찰은 기존 543개(105·140·104·37·34·18·29·28·48), opener 함수/CLI 564개, quoted fence 원 반례·대조 12개, 깊이/들여쓰기 CLI 144개다. unittest 수가 아니며 564개 중 기대 미지정 탐색 CLI 12개는 합격으로 세지 않는다. wrapper의 `expected_exit=null` 요약을 제외하고 실제 기대 지정 504개 함수·48개 CLI는 모두 일치했다. 144개에서 유효한 3열 opener/closer 대조 각 12개만 실패했고 120개는 일치했다. 두 OS JSON은 Unicode DB 메타데이터(16.0.0/14.0.0)만 다르고 판정은 같다.

canonical 27쌍 exit 0, UX fixture의 의도된 report finding 12개/fail_count 0, 4앱 baseline exit 0·airport 1.320934를 corpus에서 재현했다. JSON·Markdown·step summary의 합성 경로 marker 노출 없음, malformed CSS/JSON/argparse·root self-symlink 입력 오류 exit 2·traceback 없음도 재현했다. 실제 CR/CRLF fixture는 `write_bytes`로 보존했다. Windows 임시 Git LF→CRLF 경고는 제품 오류로 세지 않았다.

## 누적 finding disposition

| 원 ID·심각도 | 현재 후보의 독립 재판정 |
|---|---|
| B-P1-01 | root/CWD Git 기준: FIXED |
| B-P1-02 | prepend baseline 증가: FIXED |
| B-P1-03 | 기존 MDX template·배열·삼항·tag·ESM·중첩 JSX·미종결 span·Unicode/CR: FIXED |
| B-P1-04 | 경로·값·argparse·오류 채널 redaction: FIXED |
| B-P2-05 | muted 추가 읽기 쌍: FIXED |
| B-P2-06 | baseline 숫자·huge/deep JSON: FIXED |
| B-P3-07 | geo 8건 문서: FIXED |
| B-P1-08 | 추가 `+++` 행: FIXED |
| B-P1-09 | CSS media·specificity·순서·nested/string/comment: FIXED |
| B-P2-10 | airport 현재/역사 수치: FIXED |
| B-P1-11 | selector 대소문자·인용 공백: FIXED |
| B-P1-12 | 빈 selector list·root descendant: FIXED |
| B-P2-13 | 파일 첫·3자 inline 인용: FIXED |
| B-P1-14 | JS LS/PS 줄 주석 종료: FIXED |
| B-P1-15 | Unicode 가짜 hunk·added 행: FIXED |
| B-P1-16 | bare CR 읽기/Git decode: FIXED |
| B-P2-17 | LS/PS 안 닫힌 Markdown span: FIXED |
| B-P2-18 | ASCII space/tab·LS/PS closing suffix 구분: FIXED |
| B-P2-19 | plain closing 4열/tab-stop: FIXED |
| B-P2-20 | quoted tilde P6/P8·빈 quoted backtick·외부 대조: FIXED |
| B-P1-21 | 직접 깊이 감소·인용되지 않은 빈 행·공백 행의 원 반례: FIXED |
| B-P1-22 | quoted prefix 들여쓰기 계약: **OPEN(부분 수정)**; 4열 과잉 허용은 줄었으나 아래 정상 3열/중간 prefix 회귀가 남음 |

## B-P1-22 — 선택적 marker 공백과 콘텐츠 들여쓰기를 구분하지 못함

- 원 심각도 **P1** 유지, disposition **OPEN / FIX_REQUIRED**. 별도 새 ID로 중복 집계하지 않는다.
- 위치: `tools/ux_lint.py:261-270`(opener 마지막 `>` 다음 공백 전체 계산), `:298-306`(중간 `>` 앞 공백 무제한 소비 및 마지막 공백 전체 계산), `:613-616`(잘못 계산한 4열을 body로 처리). `tests/test_ux_lint.py:509-528`도 동일한 오해를 기대값으로 고정한다.
- 최소 closer 입력: `'> ~~~\n> quoted\n>    ~~~\n> {window.confirm("x")}\n'`. 셋째 행 `>` 뒤 ASCII space는 4개다. SHA256 `e480e10936f1f81c1c0d8b95bfb80e5a9e296f569a8d4d1f98a22af830a6072b`.
- 재현 명령: 임시 Git 저장소에 `Page.mdx`의 `safe\n`을 먼저 커밋하고 `BASE`를 기록한 뒤 위 bytes로 바꾼다. `PYTHON ROOT/tools/ux_lint.py --root TEMP --fail-new --json` 및 같은 명령의 `--base BASE` 변형을 실행한다.
- 기대: `>`와 선택적 공백 1개는 blockquote marker다. 남은 콘텐츠 들여쓰기는 3열이므로 정상 closer이며, 이후 실행 P8은 finding·exit 1이어야 한다. **실제는 exit 0, findings=[]**. tilde/backtick × LF/CR/CRLF × plain/base 12개/OS 모두 동일하게 누락됐다.
- 반대 방향의 opener 재현: `'>    ~~~\n> {window.confirm("x")}\n> ~~~\n'`는 유효한 3열 opener의 문서 코드 예제다. 기대 exit 0이나 실제 P8/line 2/added true/exit 1이다. LF SHA256 `c0fa997e0148e666114bd1d0d0ad7cb396e336c9e2ed2d7aaedeb379fa4323ed`. tilde × 줄바꿈 3개 × 두 모드 6개를 재현했다. backtick은 inline fallback 때문에 같은 표면의 일부 변형을 우연히 제외한다.
- 중간 prefix도 검증되지 않는다. `'>> ~~~\n>> quoted\n>     > {window.confirm("quoted")}\n>> {window.confirm("x")}\n'`에서 셋째 행의 과도한 들여쓰기는 안쪽 quote를 유지하지 않는다. 새 안쪽 인용의 넷째 행 P8을 검출해야 하나 실제 exit 0이다. SHA256 `b96721e509ff89f6e030081adb9bfd9ceb1398f7ee876c655c60a59bd6674bac`; tilde/backtick·LF/CR/CRLF·plain/base 12개/OS 동일. fence 안 추가 `>`를 literal로 두는 대조와 세 겹 정상 fence/깊이 감소 대조도 실행했다.
- 코드 base 대조: `1559410`과 raw-only commit 사이 도구 diff 없음으로 확인한 post25 worktree의 **코드만** 사용했다. closer 입력은 base P8/exit 1 → candidate exit 0, opener 입력은 base exit 0 → candidate P8/exit 1로 양 OS에서 직접 확인했다. 이전 보고서 본문을 기준선으로 삼지 않았다.
- 검사 자체의 오류: 새 시험은 `f">{indent}~~~"`에서 `indent="    "`인 정상 3열 closer를 무효로 기대하고, `">    ~~~tsx"` 정상 opener를 실행 P6으로 기대한다. 이 잘못된 기대값 때문에 298개 전체 시험과 60개 focused 성공만으로 계약을 충족했다고 볼 수 없다.
- 영향: 유효한 closer 뒤 실제 실행 P6/P8을 숨겨 신규 변경 gate가 잘못 통과하고, 정상 문서 코드 예제도 반대로 fail한다. 실행 누락이 있어 P1을 유지하며 단순 문서 오검출 P2로 낮추지 않는다.
- 최소 권고: 매 `>` 단계에서 marker의 선택적 indentation 1개와 콘텐츠 indentation을 분리하고 실제 tab-stop 열을 보존한다. 마지막 단계뿐 아니라 중간 nested prefix도 검증한다. 검증된 논리 콘텐츠 앞 0~3열만 fence opener/closer로 인정하고 quoted container 종료·LF 좌표를 보존한다. 기존 시험의 4개 space·tab 기대를 공식 문법과 다시 대조하여 고친 뒤 정상 3열/실제 4열/중간 prefix·P6/P8·plain/base 대조를 고정한다.

근거는 [CommonMark 0.31.2 §5.1](https://spec.commonmark.org/0.31.2/#block-quotes)의 marker 정의·중첩 구조와 [§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)의 fence 들여쓰기/컨테이너 경계다(revision 2024-01-28, 조회 2026-09-08). 실제 MDX compiler/browser는 실행하지 않았으며 공식 문법·코드·CLI를 대조한 결론이다.

## NOT_RUN과 최종 verdict

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 부재. 다른 OS/버전 결과로 대체 성공 표기하지 않았다.
- `NOT_RUN(정확한 candidate 원격 CI 독립 조회, WSL Git diff --check 별도 실행, 비 UTF-8 Git 출력 직접 주입)`.
- `NOT_RUN(소비자 build/e2e·manifest 검사, npm/PyPI 설치·게시, workflow dispatch, 실제 MDX compiler/browser)`: common 독립 리뷰 범위 밖이다.
- 기존 22개 ID 중 21개 원 반례 FIXED, **B-P1-22 OPEN**. 별도 신규 finding ID 0개, 미해결 심각도는 P1 1개이며 P0/P2/P3 0개다. 새 72개 교차 중 30개 불일치와 누적 144개 중 24개 불일치는 같은 finding의 반복/대조이며 별도 finding으로 세지 않는다.
- **verdict: NO-GO.** 후보·시험·문서를 수정하지 않고 이 원본 한 파일만 report-only commit으로 보존한다. 수정 후보를 다시 독립 검토해야 한다.
