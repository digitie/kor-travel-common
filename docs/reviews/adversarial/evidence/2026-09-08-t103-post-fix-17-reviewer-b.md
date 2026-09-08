<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-17 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST17-B-20260908T130413-KST
- 최종 판정: **NO-GO**. 이전 14개 finding의 원 반례는 FIXED, 신규 P1 1개(B-P1-15)가 재현됐다. 신규 P0/P2/P3는 0개다.
- 시작: 2026-09-08T13:04:13.4419525+09:00. 제품 검증 종료: 2026-09-08T13:11:56.7932478+09:00.
- 제품 시작/종료 HEAD: 34c0abfbdf695258d53a1015ff4b73926d1ebcd1.
- 제품 시작/종료 tree: 8bc05556808a5b970d8f0ac659f7fd934ac88167.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post17-b에 새 detached worktree. 시작/종료 status --porcelain=v1 --untracked-files=all 출력은 모두 비어 있었다.
- manifest: 1c6091d7a6ef518764ba58808cae4e4777638c36의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-17-manifest.md를 git show로 읽었다. Git blob 바이트 SHA256: d698962ea98bd1f0f47c65730b70ffb7e311b05c324f8e37f18c480488e6632e.
- 수정 delta: 73b9cf68788066742e8df99dfad2433cbe6bf5fc..34c0abfbdf695258d53a1015ff4b73926d1ebcd1. 제품 2파일(tools/ux_lint.py, tests/test_ux_lint.py)의 전체 diff를 읽었다. 나머지 3개 과거 manifest/raw는 경로만 확인하고 raw 본문을 읽지 않았다.
- source .git/config SHA256 시작/종료 동일: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. git config를 변경하지 않았다.
- 보고서만 별도 branch에 커밋한다. 이 evidence commit은 제품 candidate와 별개다. 제품·manifest·소비자 수정, push, registry 및 workflow dispatch는 실행하지 않았다.

## 전달받은 요청 원문

> T-103 post-fix-17 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 34c0abfbdf695258d53a1015ff4b73926d1ebcd1, tree 8bc05556808a5b970d8f0ac659f7fd934ac88167의 detached clean checkout으로 고정합니다. 공통 manifest는 commit 1c6091d의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-17-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw는 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate와 누적 corpus를 독립 재현하고, 특히 U+2028/U+2029가 plain TS·MDX·template 보간·JSX 중첩 주석에서 줄 주석을 끝내는지, 이전 Unicode/FEFF/async 반례를 재검증하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-17-reviewer-b.md에 기록하고 raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정·커밋·푸시하지 마세요. 상대 원본을 읽지 않은 상태로 완료 메시지에 commit/hash/verdict를 알려 주세요.

독립성: 상대 raw 본문이나 분석 결과를 읽거나 요청하지 않았다. manifest에 기재된 원본 commit/hash 및 coordinator의 완료 상태 메타데이터만 접했다. 이전 probe 코드는 재사용했으며 각 입력을 이번 후보에서 새로 실행했다.

## 신규 B-P1-15 — Unicode 줄 종결자가 Git diff 추가 행 판정을 어긋나게 한다

- 심각도/상태: **P1 / OPEN**, 수정 필요. 위치: tools/ux_lint.py:756, 764~768. 관련 계약: docs/tasks/T-103-kt-contrast-ux-lint.md:22, 39 및 docs/standards/ux-guide.md:15.
- 원인: Git patch는 LF로 행을 구분하는데 output.splitlines()는 U+2028/U+2029도 나눈다. 추가된 파일 행 내부의 Unicode 줄 종결자 뒤 문자열이 공백으로 시작하면 이를 patch context 행으로 오인해 current_line만 증가시킨다. 다음 실제 추가 행의 번호가 밀린다.
- 영향: 신규 금지 호출을 findings에 발견하고도 added_lines에 없는 기존 행으로 취급한다. --base 모드가 exit 0 / PASS를 출력하므로 신규 위반 차단 수용 기준을 충족하지 못한다.
- 최소 입력은 임시 Git 저장소의 Page.ts를 export {}; 한 줄로 커밋한 뒤 아래 Python 문자열로 바꾸는 것이다. U+2028을 U+2029로 바꾸어도 같다.

~~~python
source = 'const n=1;// 설명' + chr(0x2028) + ' void 0;\nwindow.confirm("확인");\n'
~~~

정확한 최소 재현 절차(후보 도구의 절대 경로를 tool에 지정, 실제 소비자와 무관한 임시 저장소):

~~~python
from pathlib import Path
import os, subprocess, sys, tempfile
tool = Path("F:/dev/kor-travel-common-wt/review-t103-post17-b/tools/ux_lint.py")
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, env=env, text=True).strip()
    git("init", "-q")
    path = root / "Page.ts"
    path.write_text("export {};\n", encoding="utf8")
    git("add", "--", "Page.ts")
    git("-c", "user.name=reviewer-b", "-c", "user.email=reviewer-b@example.invalid",
        "commit", "-qm", "probe baseline")
    base = git("rev-parse", "HEAD")
    for cp in (0x2028, 0x2029):
        path.write_text('const n=1;// 설명' + chr(cp) +
                        ' void 0;\nwindow.confirm("확인");\n', encoding="utf8")
        for options in ([], ["--base", base]):
            result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool),
                "--root", str(root), "--fail-new", "--json", *options],
                cwd=root, env=env, capture_output=True, text=True, encoding="utf8")
            print(cp, options, result.returncode, result.stdout)
~~~

WSL에서는 tool만 /mnt/f/dev/kor-travel-common-wt/review-t103-post17-b/tools/ux_lint.py로 바꾼다. 실제 실행은 동일 절차를 확장한 외부 probe t103-post17-b-new.py로 양 OS에서 수행했다.

| 대조 | Windows 3.14 / WSL 3.11 관찰 | 기대 |
|---|---|---|
| U+2028 일반 --fail-new | exit 1, FAIL, P8 line 2 | 동일 |
| U+2028 --base | **exit 0, PASS, P8 line 2** | exit 1, FAIL |
| U+2029 일반 --fail-new | exit 1, FAIL, P8 line 2 | 동일 |
| U+2029 --base | **exit 0, PASS, P8 line 2** | exit 1, FAIL |
| LF 대조 일반/--base | 둘 다 exit 1, FAIL, P8 line 3 | 동일 |
| Node 실행 의미 대조 | 세 입력 모두 exit 0, stub confirm 호출 1회 | 실제 실행 식 |

이 결함은 이번 수정의 줄 주석 스캐너 자체에서 발생한 것이 아니다. added_lines 구현은 직전 후보와 동일하며, 확대된 diff 경계 재현에서 발견한 기존 잠복 결함이다. 직전 후보를 재실행해 새 finding 수치로 집계하지 않았다.

권고: patch 행 분리는 LF만 사용하고 실제 파일의 Git 행 번호와 일치시킨다. 공백·플러스·마이너스·hunk처럼 보이는 Unicode 이후 텍스트가 patch 구문으로 해석되지 않는 양성/음성 diff 시험을 추가한다. JavaScript의 줄 주석 종료 규칙과 Git patch 행 구분 규칙을 각각 유지해야 한다.

## 누적 finding 재판정

| ID | 원 심각도 | 이번 disposition 및 직접 확인 |
|---|---|---|
| B-P1-01 | P1 | FIXED — --root/CWD의 Git 기준, 외부 root와 신규 행 |
| B-P1-02 | P1 | FIXED — 앞에 삽입한 위반이 기존 baseline 건수를 소비하지 못함 |
| B-P1-03 | P1 | FIXED — MDX 실행/인용, 미종결 1·2자 span, 단항·논리·정규식·Unicode·async·FEFF 누적 반례 |
| B-P1-04 | P1 | FIXED — 입력 경로·값 오류의 JSON/Markdown/summary 노출 없음 |
| B-P2-05 | P2 | FIXED — 기본 muted 장식 표면과 추가 읽기 표면 31쌍 구분 |
| B-P2-06 | P2 | FIXED — baseline 숫자/타입/거대 정수/깊은 JSON 입력 오류 exit 2 |
| B-P3-07 | P3 | FIXED — geo 예제 미달 8건과 evidence 일치 |
| B-P1-08 | P1 | FIXED — 기존 +++ 실제 추가 행 반례는 fail. 새로운 Unicode patch 분리는 B-P1-15 |
| B-P1-09 | P1 | FIXED — media 조건/교집합/specificity/source order 및 string/comment 경계 |
| B-P2-10 | P2 | FIXED — airport 현재 source-over 1.320934와 역사 값 1.15의 구분 |
| B-P1-11 | P1 | FIXED — selector 대소문자·인용 공백 및 comment-gap 오류 |
| B-P1-12 | P1 | FIXED — 빈 selector 목록과 root descendant fail-closed |
| B-P2-13 | P2 | FIXED — 파일 첫 span·3자 inline 문서 인용 음성 대조 |
| B-P1-14 | P1 | FIXED — CR/LF/LS/PS plain TS·MDX·template 보간·중첩 JSX 주석 종료, 인용/주석 음성 대조 |

B-P1-14의 독립 새 probe는 4개 줄 종결자 × (TS template, MDX template, 중첩 JSX, 보간 주석 음성, 닫힌 span 음성) 20개 CLI 대조다. 실행 형태는 P8/exit 1, 음성은 0건/exit 0으로 양 OS 일치했다. 이전 plain TS 및 미종결 MDX 1·2자 span 대조 24개 관찰도 이번 후보에서 재실행했다.

## 실행 명령과 결과

환경: Windows Python 3.14.3 / Node v25.9.0, WSL Python 3.11.15 / Node v22.22.2. Python Unicode DB는 각각 16.0.0/14.0.0이었다. GIT_* 상속을 제거한 임시 Git 사본에서 전체 시험·정적 검사를 실행했다. 후보의 .git 연결을 임시 시험에 사용하지 않았다.

명령의 python은 Windows에서 py -3.14, WSL에서 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11이다.

| 명령 | Windows | WSL |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p "test_*.py" | 289개 실행·통과, skip 0, 83.166초 | 수집 289, 실행·통과 286, skip 3, 23.175초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v | 51개 통과, 14.730초 | 51개 통과, 6.905초 |
| tools/validate_plan.py | task 106, 오류 0 | 동일 |
| tools/validate_document_links.py | 문서 442, 대상 2420, 오류 0 | 동일 |
| tools/check_spdx.py | 파일 56, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 파일 574, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 파일 574, 발견 0 | 동일 |
| tools/check_versions.py --self-check | exit 0, 자체 검사만 | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1, 오류 0 | 동일 |
| aliases focused unittest | 35개 통과, 1.803초 | 수집 35, 실행·통과 34, skip 1, 0.233초 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report 모드 exit 0, 발견 12건 | 동일 |
| git diff --check f2f55b12a6e3a830eb29874b6955e06e2353937f 34c0abfbdf695258d53a1015ff4b73926d1ebcd1 | exit 0, 출력 없음 | 동일 |

전체 실행의 -v 생략은 출력량만 줄이며 선택된 시험은 같다. 전체 및 정적 검사 외부 wrapper는 .git/codex-audit/review-t102-b-wsl-unittest.py와 review-t102-post-b-gates.py이며, 인자는 이번 detached 후보 경로다. WSL diff의 읽기 전용 명령은 git --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post17-b diff --check 위 두 SHA다. config는 수정하지 않았다.

추가 probe 명령은 python -B -X utf8 .git/codex-audit/<script> <candidate-root> <output-name>이다.

| wrapper | 양 OS 새 관찰 행 | 결과 |
|---|---:|---|
| t103-post9-b-corpus.py | 각각 105 | 전체 JSON 결과 동일. CSS/JSON/redaction/diff/symlink/기존 MDX corpus |
| t103-post15-b-late-corpus.py | 각각 140 | 전체 JSON 결과 동일. 문단·fence·CSS gap·Unicode·airport 등 |
| t103-post17-b-latest-corpus.py | 각각 104 | Unicode DB 메타데이터 1행 외 103개 관찰 결과 동일. 신규 B-P1-15 포함 |

위 349행은 unit test 수가 아니라 CLI·Node·계산값·환경 메타데이터 관찰 수다. 합성 비밀/사설 주소 원문은 출력·보고서에 넣지 않고 노출 여부만 검사했다. probe는 별도 임시 디렉터리에 입력을 생성·삭제했다. Python/rg 보조 명령 작성 오류는 검증 성공으로 집계하지 않았고 올바른 명령으로 재확인했다.

## 문서 정합성과 미실행

T-103 및 resume은 IN_PROGRESS다. task의 diff 신규 위반 차단 조건 때문에 신규 P1이 닫히기 전 완료로 변경할 수 없다. airport evidence의 1.32/1.320934와 수용 기준, geo 8건, muted 추가 읽기 표면, T-010 후행 재사용 workflow, common-only/GPL-3.0-or-later/소비자 baseline 외부 소유 구분을 확인했다. 관련 정본은 이번 제품 delta에서 변경되지 않았다.

- NOT_RUN(Windows Python 3.11): py -0p에서 3.14/3.10만 확인했다.
- NOT_RUN(WSL 3개 skip): Windows 8.3 경로 시험 1개와 jsonschema 기반 schema parity 2개. WSL importlib.util.find_spec("jsonschema")는 None이다. 전체 통과 수에서 제외했다.
- NOT_RUN(정확한 후보 원격 CI 독립 조회): 이 리뷰의 로컬 실행을 CI 성공으로 바꾸어 기록하지 않았다.
- NOT_RUN(MDX 실제 compiler/browser): 구문 문맥은 코드·CLI 및 Node의 실행 식 대조로 확인했다. 실제 MDX 컴파일/e2e 검증은 수행하지 않았다.
- NOT_RUN(소비자 build/e2e 및 앱 baseline 등록): 소비자 이관 task 소유이며 요청 범위 밖이다.
- NOT_RUN(npm/PyPI registry·게시·workflow dispatch·재사용 contrast-check workflow selftest): 호출 금지 및 후행 T-010 경계다.

최종 disposition은 B-P1-15 OPEN, 기존 14개 FIXED, **NO-GO**다. 후보 구현은 수정하지 않았으며 이 원본 report 한 파일만 evidence commit에 포함한다.
