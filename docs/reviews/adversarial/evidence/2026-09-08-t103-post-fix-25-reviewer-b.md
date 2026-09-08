<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# T-103 post-fix-25 독립 적대적 리뷰 B 원본

## 실행과 기준선

- 실행 ID: `T103-PF25-B-20260908-150732`.
- 시작 KST: `2026-09-08T15:07:32.8974679+09:00`; 제품 검토 종료 KST: `2026-09-08T15:13:16.1750770+09:00`.
- 시작·종료 제품 HEAD: `155941045a077529cb12f875cad5ab2b2f7639da`.
- 시작·종료 제품 tree: `4fb87fcc870402df48ac3f336f5f9c2a6ede7767`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post25-b`, detached checkout. 시작·종료 `git status --porcelain` 출력 없음. 종료 후 이 원본 한 파일만 별도 branch에 커밋한다.
- delta base: `535beecaeaf06296df3c8c1e108c1b86564e48d7`.
- manifest: commit `0e3238ce37e496ec5e88773ffc5e4add90b6dab0`의 [post-fix-25 manifest](2026-09-08-t103-post-fix-25-manifest.md), `git show` blob SHA256 `6773ff14b4e7eca3029e235292bb5b2ee1d39e71174cd7efc35002712ebdfc79`.
- source `.git/config` 시작·종료 SHA256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. 후보·manifest·소비자·Git 설정·기존 evidence를 바꾸지 않았다. 상대 post25 결과/raw 및 과거 상대 raw 본문을 읽거나 요청하지 않았다.

## 전달 요청 원문

> T-103 post-fix-25 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit `155941045a077529cb12f875cad5ab2b2f7639da`, tree `4fb87fcc870402df48ac3f336f5f9c2a6ede7767`; 공통 manifest는 commit `0e3238ce37e496ec5e88773ffc5e4add90b6dab0`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-25-manifest.md`입니다. 별도 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post25-b`에서 candidate와 clean을 확인하세요. 전문 범위는 Git added-line/base·입력/오류/redaction·문서/task/scope 정합과 quoted fence opener/closer·nested depth·blank quoted row·container boundary·P6/P8·CR/CRLF 교차 재현입니다. 코드와 문서를 직접 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer의 post25 결과/raw를 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-25-reviewer-b.md` 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO raw를 확정하고 작업을 멈추세요.

## 확인 범위와 실행

`git diff 535beec 1559410 -- tools/ux_lint.py tests/test_ux_lint.py` 전체를 읽었다. 제품 delta는 컨테이너 helper 2개·fence 호출/종료 처리와 시험 2개이며, 나머지 3개 변경은 직전 manifest·A/B raw 추가다. 상대 raw 본문은 읽지 않았다. [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md)의 추가 행 fail·인용 제외·외부 의존 0·airport 1.320934 계약과 [evidence](../../../evidence/t103-kt-contrast-ux-lint.md)의 geo 8건·소비자/T-010 NOT_RUN, resume의 IN_PROGRESS를 직접 대조했다. GPL-3.0-or-later·common 도구 범위·npm/PyPI 미게시·소비자 무수정 경계는 유지된다. CI·versions·공개 패키지 파일은 이번 delta에서 바뀌지 않았다.

아래 `ROOT`는 위 후보 worktree, `AUDIT`는 source checkout의 `.git/codex-audit`다. Windows는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`을 사용했다. WSL 경로는 `/mnt/f/`로 변환했다. helper·JSON 로그·합성 fixture는 후보 밖에 두었고 fixture 프로세스에서 `GIT_*` 환경변수를 제거했다.

| 검사·명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| `-m unittest discover -s tests` | 297 실행 성공, skip 0, 140.632초 | helper `AUDIT/review-t102-b-wsl-unittest.py ROOT`의 임시 독립 사본에서 297 수집·294 실행 성공·3 skip, 39.014초 |
| `-m unittest tests.test_kt_contrast tests.test_ux_lint` | 59 성공·skip 0, 37.891초 | 59 성공·skip 0, 25.158초 |
| `AUDIT/review-t102-post-b-gates.py ROOT` | plan 106/오류 0, links 466문서·2446대상/오류 0, SPDX 56/오류 0, secrets·redaction 각각 598파일/발견 0/예외 0 | 동일 |
| 위 helper의 registry self-check·aliases | `check_versions.py --self-check` exit 0; aliases CSS 1/오류 0 | 동일; 소비자 버전 검사 미실행 |
| 위 helper의 aliases focused | 35 성공/skip 0 | 35 수집·34 성공/skip 1 |
| `AUDIT/t103-post25-b-run-corpus.py ROOT win` 또는 `ROOT wsl` | 누적 1119개 관찰 | 같은 관찰 수·판정 |
| `AUDIT/t103-post25-b-new.py ROOT OUTPUT_JSON` | 새로운 교차 CLI 144개: 84개 기대 불일치, 60개 대조 일치 | 같은 입력 hash·판정·좌표 |
| `AUDIT/t103-post25-b-base-delta.py BASE_ROOT ROOT OUTPUT_JSON` | 3개 최소 반례 × base/candidate = 6개 관찰, base exit 1 → candidate exit 0 | 동일 |
| `git diff --check 535beec 1559410` | 출력 없음, exit 0 | 별도 WSL Git diff 실행은 재사용하지 않음 |

WSL skip 3개는 Windows 8.3 전용 1개와 jsonschema 미설치 2개다. 해당 WSL Python의 `importlib.util.find_spec("jsonschema")`가 `None`임을 직접 확인했다. coordinator manifest의 296실행/1skip을 이번 결과로 쓰지 않는다. WSL helper는 `.git`·`__pycache__`·`node_modules`를 제외해 임시 디렉터리에 복사하고 임시 Git에 파일 경로를 명시해 stage하므로 source Git 설정을 변경하지 않는다.

누적 1119개는 기존 543개(105·140·104·37·34·18·29·28·48), opener 함수/CLI 564개, 직전 B-P2-20·양성 대조 12개의 합이다. unittest 수가 아니며 564개 중 기대 미지정 탐색 CLI 12개는 합격 건수로 세지 않는다. wrapper의 이 12개 `expected_exit=null` 요약을 별도로 분리해 판정했다. 실제 기대 지정 함수 504개·CLI 48개는 모두 일치했고 B-P2-20 12개 대조도 모두 일치했다. 기존 543개의 판정은 직전 실행과 동일하다. 두 OS 전체 JSON에서 Unicode DB 메타데이터(16.0.0/14.0.0)만 다르고 결과는 같다.

기존 corpus에서 canonical 27쌍 exit 0, UX fixture 12개 의도된 report finding/fail_count 0, 4앱 baseline exit 0과 airport 1.320934를 재확인했다. JSON·Markdown·step summary의 합성 marker 노출 없음, malformed CSS/JSON/argparse·root self-symlink 입력 오류 exit 2·traceback 없음도 재현했다. Windows 임시 Git의 LF→CRLF 경고는 제품 오류로 세지 않았으며 CR/CRLF fixture는 `write_bytes`로 썼다.

## 기존 B finding disposition

| 원 ID·심각도 | 독립 재판정 |
|---|---|
| B-P1-01 | root/CWD Git 기준: FIXED |
| B-P1-02 | prepend baseline 증가 우회: FIXED |
| B-P1-03 | 기존 MDX template·배열·삼항·tag·ESM·중첩 JSX·미종결 span·Unicode/CR 반례: FIXED |
| B-P1-04 | 경로/값/argparse/오류 출력 redaction: FIXED |
| B-P2-05 | muted 추가 읽기 쌍: FIXED |
| B-P2-06 | baseline 비정상 수치·huge/deep JSON: FIXED |
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
| B-P2-18 | closing ASCII space/tab와 LS/PS suffix: FIXED |
| B-P2-19 | plain closing 4열/tab-stop: FIXED |
| B-P2-20 | quoted tilde P6/P8·빈 quoted backtick·외부 실행 양성 대조: 원 반례 FIXED |

FIXED는 해당 원 반례의 disposition이다. 새 컨테이너 구현에서 나타난 다음 회귀를 숨기지 않는다.

## B-P1-21 — 인용 깊이 감소·인용되지 않은 빈 행에서 fence를 끝내지 않음

- 심각도 **P1**, disposition **OPEN / FIX_REQUIRED**.
- 위치: `tools/ux_lint.py:293-295`(깊이 불일치를 `None`으로 합침), `:595-602`(행이 `>`로 시작하거나 비어 있으면 컨테이너가 유지됨).
- 최소 LF 입력 A: `'>> ~~~\n>> quoted\n> {window.confirm("x")}\n'`. SHA256 `50fb97e8b0bcc131be862d0bc3a6359c40db3c133890b9c9a5a6a17279fe02b5`.
- 최소 LF 입력 B: `'> ~~~\n> quoted\n\n> {window.confirm("x")}\n'`. SHA256 `9c03ca61e74b0f2fe634551246bcd2b70f5db65fb07dc7237b3ffed3981e5f73`.
- 재현: 임시 Git 저장소에서 `Page.mdx`의 `safe\n`을 커밋해 `BASE`를 기록하고 위 입력 bytes로 교체한다. `PYTHON ROOT/tools/ux_lint.py --root TEMP --fail-new --json` 및 여기에 `--base BASE`를 더한 명령을 실행한다.
- 기대: A에서는 안쪽 인용 fence가 끝나고 바깥 인용의 실행식 P8을 검출한다. B에서는 인용되지 않은 빈 행이 첫 인용 블록을 끝내며 다음 인용의 실행식 P8을 검출한다. 두 경우 exit 1이어야 한다.
- 실제: **exit 0, findings=[]**, plain/base 모두 동일. tilde/backtick × LF/CR/CRLF × plain/base에 깊이 감소 P8·P6와 빈 행·공백만 있는 행 변형을 더한 48개/OS가 같은 누락이다. 같은 깊이의 닫힌 인용 fence 및 빈 `>` 행은 정상 제외되며, 완전한 plain 컨테이너 밖 P8은 정상 검출되는 양성/음성 대조를 포함했다.
- 회귀 근거: base의 변경 없는 도구를 보존한 post24 worktree에서 A/B를 실행하면 각 P8/exit 1, 후보에서는 각 exit 0이었다. base와 그 raw-only commit 사이 `tools/ux_lint.py` diff가 없음을 확인했고 과거 raw는 읽지 않았다.
- 영향: 실제 MDX 실행 P6/P8 위반이 report에서도 사라져 신규 변경 gate가 잘못 통과한다.
- 최소 권고: opener가 속한 인용 깊이를 실제로 유지하는 행과 컨테이너 밖 행을 구분한다. 깊이가 줄거나 인용되지 않은 빈 행이면 fence를 그 행 앞에서 종료한다. 추가 `>`는 fence 내부 literal일 수 있으므로 깊이가 다르다는 이유만으로 모든 경우를 종료하지 말고 컨테이너 prefix를 먼저 정확히 소비한다.

## B-P1-22 — 인용 prefix 뒤의 모든 공백을 제거해 4열 opener/closer를 인정

- 심각도 **P1**, disposition **OPEN / FIX_REQUIRED**. 동일 원인의 closer 오검출은 P2 수준의 영향이지만, opener가 실제 실행식을 숨기므로 finding 전체를 P1로 분류한다.
- 위치: `tools/ux_lint.py:257-261`, `:288-292`의 `>` 다음 무제한 space/tab 소비. 최초 prefix만 열 수를 검사하고 내부 indentation은 검사하지 않는다.
- 최소 opener 입력: `'>     ~~~\n>\n> {window.confirm("x")}\n'`(첫 행 `>` 뒤 ASCII space 5개). SHA256 `ae5857c41dc528ff0b2e557683cb2d9427dad2c75c3b7780276be4769914cc4c`.
- 기대: blockquote marker의 선택적 공백 1개를 제외해도 4열이 남으므로 fence opener가 아니다. 다음 빈 quoted 행 뒤 실행식은 P8/exit 1이어야 한다. 실제 plain/base 모두 **exit 0, findings=[]**. base 도구는 P8/exit 1이었다.
- closer 반례: `'> ~~~\n> quoted\n>     ~~~\n> <div className="outline-none"/>\n> ~~~\n'`. SHA256 `b9826c7c8e7e01028dde0fd3c55ab06c7c3729954ad354ca4de8731bcbd230fb`. 실제 P6/line 4/added true/exit 1, 기대는 fenced 예제 제외·exit 0이다. `>\t\t~~~` closer도 같은 조기 종료를 재현했다.
- 범위: opener 4열·closer 4열·closer double-tab × tilde/backtick × LF/CR/CRLF × plain/base = 36개/OS 기대 불일치. `>` 뒤 space 4개(선택적 1개를 제외한 3열)의 opener/closer 대조는 기대 일치했다.
- 최소 권고: 컨테이너 marker에 속한 선택적 공백과 콘텐츠 indentation을 분리하고 각 단계의 tab-stop/열 수를 보존한다. fence 앞의 잔여 indentation이 0~3열인지 opener·closer에 동일하게 적용한다. quoted 행 전체를 무조건 가리지 말고 기존 정상 quoted JSX/외부 P8 대조를 유지한다.

두 finding의 문법 근거는 [CommonMark 0.31.2 §5.1](https://spec.commonmark.org/0.31.2/#block-quotes)의 인용 marker·빈 행·중첩 정의와 [§4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)의 fence·컨테이너 종료·3열 제한이다(revision 2024-01-28, 조회 2026-09-08). 공식 문법과 실제 CLI를 대조했으며 실제 MDX compiler/browser 실행을 한 것으로 주장하지 않는다.

## 미실행과 최종 판정

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 부재. WSL 3.11이나 Windows 3.14 결과를 대체 성공으로 세지 않는다.
- `NOT_RUN(정확한 candidate 원격 CI 독립 조회, WSL Git diff --check 별도 실행, 비 UTF-8 Git 출력 직접 주입)`: 로컬 tests/static 결과와 구분한다.
- `NOT_RUN(소비자 build/e2e·manifest, npm/PyPI 설치·게시, workflow dispatch, 실제 MDX compiler/browser)`: 허용된 common 리뷰 범위 밖.
- 기존 B 20건의 원 반례는 FIXED. 신규 **P1 2건(B-P1-21, B-P1-22)**, P0/P2/P3 신규 0건. 새 CLI 교차 144개 중 84개 불일치는 두 원인의 반복 재현이며 84개 별도 finding이 아니다.
- **verdict: NO-GO.** 후보를 수정하지 않고 이 원본 한 파일만 report-only commit으로 확정한다. 수정 후보의 두 독립 reviewer 재검토가 필요하다.
