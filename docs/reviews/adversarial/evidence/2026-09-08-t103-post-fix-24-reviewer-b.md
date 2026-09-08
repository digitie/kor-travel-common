<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# T-103 post-fix-24 독립 적대적 리뷰 B 원본

## 실행과 불변 기준선

- 실행 ID: `T103-PF24-B-20260908-145205`; Reviewer B 독립 실행.
- 시작: `2026-09-08T14:52:05.0188832+09:00`; 제품 검토 종료: `2026-09-08T14:57:28.6674656+09:00`.
- 제품 시작·종료 HEAD: `535beecaeaf06296df3c8c1e108c1b86564e48d7`.
- 제품 시작·종료 tree: `7934214ea8584500670a7808ebb68b53dec29d63`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post24-b`, detached checkout. 시작·종료 `git status --porcelain` 출력 없음. 제품 검토 종료 후 이 원본 한 파일만 별도 branch에서 커밋한다.
- delta base: `3a8b569889fcaf4429cc70a7bafec779181aac6f`.
- 공통 manifest: commit `4fac62b3b40f7cd36a7e3b80e399611b0aa30fff`의 [post-fix-24 manifest](2026-09-08-t103-post-fix-24-manifest.md). `git show`로 읽은 blob SHA256: `c7fba42ac359447d967c9271e6be6e5290f3a11867fe265c3593fae12824f777`.
- 원본 source `.git/config` 시작·종료 SHA256: `0a0f849e7874cf0a25926856f9d2e381ccbf4c2dcb5999869c57b86e0f5beb5b`. 변경하지 않았다. fixture는 후보 밖 임시 디렉터리에 만들고 `GIT_*` 환경변수를 제거했다.
- 상대 reviewer의 post24 결과·raw 및 과거 상대 raw 본문을 읽거나 요청하지 않았다. 후보·manifest·소비자·기존 evidence를 수정하지 않았고 push하지 않았다.

## 전달받은 요청 원문

> T-103 post-fix-24 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit `535beecaeaf06296df3c8c1e108c1b86564e48d7`, tree `7934214ea8584500670a7808ebb68b53dec29d63`; 공통 manifest는 commit `4fac62b3b40f7cd36a7e3b80e399611b0aa30fff`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-24-manifest.md`입니다. 별도 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post24-b`에서 candidate와 clean을 확인하세요. 전문 범위는 Git added-line/base·입력 오류·redaction·JSON/오류 채널·문서/task/scope 정합과 fence opener info/backtick·tilde·indentation/tab-stop·suffix·CR/CRLF 교차 재현입니다. 코드·문서를 직접 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer의 post24 결과/raw를 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-24-reviewer-b.md` 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO raw를 확정하고 작업을 멈추세요.

## 직접 확인한 변경과 정본

`git diff 3a8b569 535beec -- tools/ux_lint.py tests/test_ux_lint.py` 전체를 읽었다. 제품 delta는 backtick info string 거부 4줄과 시험 30줄이다. 나머지 변경 3개는 직전 manifest·A/B raw의 추가이며 경로만 확인하고 상대 raw 본문은 읽지 않았다. backtick을 포함한 info string을 거부하는 조건이 tilde에는 적용되지 않는 것을 확인했다. Git 출력의 UTF-8 bytes decode, LF만 사용하는 diff hunk·finding 좌표, root/ref/error 처리도 직접 읽었다.

[T-103](../../../../docs/tasks/T-103-kt-contrast-ux-lint.md)의 CLI·백틱 인용 제외·추가 행 fail 계약, [도구 evidence](../../../../docs/evidence/t103-kt-contrast-ux-lint.md)의 airport 1.320934·geo 8건·NOT_RUN, resume의 IN_PROGRESS와 소비자 이관/T-010 경계는 일치한다. GPL-3.0-or-later·common 도구만 구현·npm/PyPI 미게시·소비자 무수정 경계가 유지된다. 공통 gate를 실제 소비자 build/e2e 성공으로 바꿔 쓰지 않았다.

## 실행 명령과 결과

아래 `ROOT`는 위 격리 worktree이며 `AUDIT`는 source checkout의 `.git/codex-audit`다. WSL에서는 `/mnt/f/` 경로를 사용했다. helper는 fixture와 검사 로그만 후보 밖에 만들며 제품 소스를 바꾸지 않는다.

| 검증 | 실행 명령·방법 | 독립 관찰 |
|---|---|---|
| Windows 전체 | `py -3.14 -B -X utf8 -m unittest discover -s tests` | Python 3.14.3, 295 실행 성공, skip 0, 137.300초 |
| WSL 전체 | `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 AUDIT/review-t102-b-wsl-unittest.py ROOT` | Python 3.11.15, 295 수집·292 실행 성공·3 skip, 35.877초 |
| 양 OS focused | 각 Python의 `-B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 각 57 성공·skip 0; Windows 36.266초, WSL 22.169초 |
| 정적 gate | 각 Python의 `AUDIT/review-t102-post-b-gates.py ROOT` | 양 OS plan 106/오류 0, link 463문서·2440대상/오류 0, SPDX 56/오류 0, secrets·redaction 각각 595파일/발견 0/예외 0 |
| registry·aliases | 위 helper가 `check_versions.py --self-check`, `check_aliases.py packages/tokens/aliases` 실행 | 양 OS exit 0, aliases CSS 1/오류 0; 소비자 버전 검사 미실행 |
| aliases 추가 focused | 위 helper의 `unittest discover -s tests -p test_check_aliases.py` | Windows 35 성공/skip 0, WSL 35 수집·34 성공/skip 1 |
| 누적 corpus | 각 Python의 `AUDIT/t103-post24-b-run-corpus.py ROOT win` 또는 `ROOT wsl` | OS당 543개 관찰, 이전 B 반례 재발 없음; 두 OS JSON의 판정 동일 |
| opener 교차 | 각 Python의 `AUDIT/t103-post24-b-new.py ROOT OUTPUT_JSON` | 504개 직접 fence 함수 판정 모두 기대 일치; CLI 60개 중 48개 기대 지정·12개 탐색 관찰, 지정한 48개 중 새 결함 6개 |
| 추가 최소 반례·대조 | 각 Python의 `AUDIT/t103-post24-b-repro.py ROOT OUTPUT_JSON` | 12개/OS 중 같은 새 결함 8개·양성 대조 4개 기대 일치 |
| canonical·UX·airport | 누적 helper의 `t103-post3-b-smoke.py`, `t103-post1-b-originals.py` 등 | canonical 27쌍/exit 0; UX fixture 12개 의도된 report finding/fail_count 0/exit 0; airport 1.320934·4앱 baseline exit 0 |
| diff | `git diff --check 3a8b569 535beec` | 출력 없음, exit 0 |

WSL 전체의 skip 3개는 Windows 8.3 전용 1개와 선택적 jsonschema 검사 2개다(`tests/test_check_aliases.py:228`, `tests/test_validate_manifest.py:164,179`). 따라서 coordinator manifest의 WSL 294실행/1skip 수치를 이번 독립 실행으로 재사용하지 않는다. Windows의 해당 검사는 실행됐다. 임시 사본은 `.git`·`__pycache__`·`node_modules`를 제외해 복사하고 임시 Git에 명시한 파일만 stage하므로 source Git 설정을 고치지 않는다.

543개 누적 관찰의 그룹별 수는 105·140·104·37·34·18·29·28·48이다. CLI exit·finding·added 및 Node 표현식 대조가 포함된 관찰 수이며 unittest 수가 아니다. 두 OS에서 Unicode DB 메타데이터(16.0.0/14.0.0)만 다르고 판정은 같다. JSON·Markdown·step summary의 합성 경로 marker 노출은 false, malformed CSS/JSON/argparse·root self-symlink는 exit 2 및 traceback 없음이었다. Windows fixture 준비 때의 LF→CRLF Git 경고는 관찰했으며 제품 traceback이 아니다. fixture의 실제 CR·CRLF bytes는 `write_bytes`로 보존했다.

## 기존 B finding disposition

| ID·원 심각도 | 이번 독립 재현과 disposition |
|---|---|
| B-P1-01 | root/CWD Git added-line 기준: FIXED |
| B-P1-02 | 앞부분 추가 시 baseline 증가 우회: FIXED |
| B-P1-03 | MDX 실행 template·배열·삼항·tag·중첩 object·ESM·JSX·미종결 span 표현식·CR paragraph: 기존 최소 반례 FIXED |
| B-P1-04 | 경로·값·argparse·오류 채널 redaction: FIXED |
| B-P2-05 | muted 읽기 쌍의 명시적 검사: FIXED |
| B-P2-06 | baseline 비정상 숫자·huge/deep JSON: FIXED |
| B-P3-07 | geo 예제 미달 8건 문서: FIXED |
| B-P1-08 | diff의 추가 `+++` 행: FIXED |
| B-P1-09 | CSS media·specificity·source order·nested/string/comment: FIXED |
| B-P2-10 | airport 현재 1.320934와 역사 1.15 구분: FIXED |
| B-P1-11 | selector 대소문자·인용 공백: FIXED |
| B-P1-12 | 빈 selector list·root descendant: FIXED |
| B-P2-13 | 파일 첫·3자 inline 문서 인용: FIXED |
| B-P1-14 | ECMAScript LS/PS 줄 주석 종료: FIXED |
| B-P1-15 | Unicode 가짜 hunk·`--base` added 좌표: FIXED |
| B-P1-16 | bare CR 읽기 변환·Git decode 우회: FIXED |
| B-P2-17 | LS/PS 안의 닫힌 1/2/3자 Markdown span: FIXED |
| B-P2-18 | closing fence ASCII space/tab와 LS/PS suffix 구분: FIXED |
| B-P2-19 | closing fence 4열/tab-stop 오판: FIXED |

이번 manifest의 backtick info 수정도 3·4자 marker, LF/CRLF/CR, info의 backtick/역슬래시-backtick/LS/PS/tab, 0~3열·4열·tab·space+tab 교차에서 의도한 조건을 만족했다. 12개 기대 미지정 CLI 탐색 관찰은 합격 건수로 세지 않는다.

## 신규 B-P2-20 — blockquote의 fenced code를 실행 코드로 잘못 검사

- 심각도: **P2**. disposition: **OPEN / FIX_REQUIRED**.
- 위치: `tools/ux_lint.py:522-524`(물리 행의 `> `를 indentation에 포함해 fence 거부), `:655-668`(tilde/backtick 호출), `:341`(backtick fallback은 빈 인용 문단을 넘지 못함).
- 최소 입력 bytes: `b'> ~~~tsx\n> <div className="outline-none"/>\n> ~~~\n'`.
- 입력 SHA256: `22fa8b1a1296cb3316efd46e9f3e6898cd2a2724a79a8cada0e2c1194eea6f27`.
- 재현 명령: 임시 Git 저장소에 `safe\n`인 `Page.mdx`를 먼저 커밋하고 `BASE`를 기록한 뒤 위 bytes로 바꾼다. `PYTHON ROOT/tools/ux_lint.py --root TEMP --fail-new --json`과 같은 명령에 `--base BASE`를 더한 두 경우 모두 실행한다.
- 실제 출력 핵심: `exit=1`, `findings=[{"pattern":"P6","line":2,"added":true}]`, traceback 없음. 기대는 문서 코드 예제 제외, finding 0·exit 0이다. LF·CR·CRLF × plain/base 6개가 각 OS에서 동일하게 실패했다(CR-only 좌표는 Git LF 기준 line 1).
- 확장 재현: fenced body를 `{window.confirm("x")}`로 바꾸면 P8/line 2로 잘못 fail한다. backtick fence도 `> ```tsx\n>\n> <div className="outline-none"/>\n> ```\n`처럼 빈 인용 행이 있으면 P6/line 3으로 잘못 fail한다. 이 변형 SHA256은 `f8d646f1dcc9b483eed08f2ffe474c537ee0a0ebc8ec5d2aeee38e059d3ab432`이다.
- 양성 대조: fence 없는 `> <div className="outline-none"/>`는 P6/exit 1, 닫히지 않은 blockquote fence 뒤 인용 블록 바깥의 `{window.confirm("x")}`는 P8/exit 1을 유지해야 하며 현재 양 OS에서 그렇다. blank가 없는 quoted backtick fence는 inline fallback 덕분에 exit 0이지만 tilde와 의미가 달라져 있다.
- 근거: [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)(revision 2024-01-28, 조회 2026-09-08)는 blockquote 안의 fence와 컨테이너 종료를 정의하며 내부를 literal code로 처리한다. 이 task는 MDX 인용을 검사에서 제외하는 계약이다. 실제 MDX compiler/browser 실행은 하지 않았고 공식 문법·코드·CLI 반례로 판정했다.
- 영향: 정상 문서 예제 추가만으로 소비자 `--fail-new`/`--base` gate를 막는다. report의 P6/P8 건수도 실제 실행 UX 위반으로 잘못 집계한다. 보안 정보 노출이나 실행 코드 누락은 이번 반례의 영향이 아니므로 P1로 올리지 않는다.
- 원인·수정 경계: 물리 행 prefix를 공백으로만 검증하는 경계는 delta base에도 존재했다. 이번 info 검사 4줄이 새로 만든 회귀라는 주장은 하지 않는다. 후보의 인용 제외 계약에서 새로 재현한 잔여 결함이다.
- 최소 권고: blockquote 컨테이너 prefix를 구분한 논리 행에서 opener·closer를 판정하고 원래 offset/LF 좌표를 보존한다. 인용 블록이 끝나면 미종결 fence도 함께 끝나야 한다. `>` 전체 행을 무조건 가리는 수정은 실제 quoted JSX 양성 대조를 깨므로 피한다. 위 P6/P8·빈 인용 행·컨테이너 밖 실행식·CR/CRLF/plain/base를 회귀로 고정한다.

## 한계와 최종 판정

- `NOT_RUN(Windows Python 3.11)`: 실행 파일 부재. Windows 3.14나 WSL 3.11로 대체 성공 표기하지 않았다.
- `NOT_RUN(정확한 candidate 원격 CI 독립 조회)`: 로컬 실행 성공을 CI 성공으로 세지 않는다.
- `NOT_RUN(소비자 저장소 build/e2e·manifest 검증, npm/PyPI 설치·게시, workflow dispatch, 실제 MDX compiler/browser)`: 허용된 common 리뷰 범위 밖이다.
- `NOT_RUN(비 UTF-8 Git 출력 직접 주입)`: 오류 변환 코드는 읽었으나 해당 외부 출력 변형을 직접 실행하지 않았다.
- 기존 B finding 19건은 명시한 원 반례에서 FIXED. 신규 P0 0·P1 0·**P2 1(B-P2-20)**·P3 0.
- **verdict: NO-GO.** 새 문서 인용 오검출을 수정한 immutable 후보의 독립 재검토가 필요하다. 제품 후보를 수정하지 않고 이 원본 한 파일만 커밋한 뒤 검토를 종료한다.
