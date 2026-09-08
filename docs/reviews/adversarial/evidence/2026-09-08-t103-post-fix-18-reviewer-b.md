<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-18 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST18-B-20260908T131930-KST.
- 최종 판정: **NO-GO**. 기존 15개 finding의 원 반례는 FIXED, 신규 **B-P1-16(P1) OPEN** 1개다. 신규 P0/P2/P3는 0개다.
- 제품 검증 시작: 2026-09-08T13:19:30.7685969+09:00. 종료: 2026-09-08T13:22:41.3588297+09:00.
- 시작/종료 제품 HEAD: 31ad7a5876ff0d5714d4094cb4a402718d02a33f.
- 시작/종료 제품 tree: 60bbe9546e1561aa5aee4f0bfbdd834fdd9cf58c.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post18-b에 새 detached worktree를 생성했다. 시작/종료 git status --porcelain=v1 --untracked-files=all은 모두 빈 출력(clean)이었다.
- manifest: 64ad46575aee5d4a3dcc07e23512f91de4129694의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-18-manifest.md를 git show로 읽었다. Git blob 바이트 SHA256: d2ff614240f6a6a9ce3761b3eb6e155141b068eac5c687ee23a5e410e8fe277e.
- 검토 delta: 34c0abfbdf695258d53a1015ff4b73926d1ebcd1..31ad7a5876ff0d5714d4094cb4a402718d02a33f. tools/ux_lint.py와 tests/test_ux_lint.py 전체 변경 및 관련 현재 정본을 읽었다. 나머지 이전 manifest/raw 3파일은 경로만 확인하고 raw 본문을 읽지 않았다.
- source .git/config 시작/종료 SHA256: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. 설정을 변경하지 않았다.
- 상대 raw 본문·분석 결과를 열람하거나 요청하지 않았다. manifest의 원본 commit/hash와 coordinator의 진행 상태만 접했다. 후보·manifest·소비자 파일 수정 및 push·registry·workflow dispatch를 하지 않았다.
- 아래 결과를 확정한 뒤 이 원본 파일만 별도 branch에 커밋한다. 보고서 commit은 위 제품 candidate와 구분한다.

## 요청 원문

> T-103 post-fix-18 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 31ad7a5876ff0d5714d4094cb4a402718d02a33f, tree 60bbe9546e1561aa5aee4f0bfbdd834fdd9cf58c의 detached clean checkout으로 고정합니다. 공통 manifest는 commit 64ad465의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-18-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw는 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate와 누적 corpus를 독립 재현하고, 특히 U+2028/U+2029가 들어간 문자열의 @@ 가짜 hunk와 --base 신규 P8 line2, LF 대조, ESM/Unicode/FEFF/async/주석 경계를 검증하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-18-reviewer-b.md에 기록하고 raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정·커밋·푸시하지 마세요. 상대 원본을 읽지 않은 상태로 완료 메시지에 commit/hash/verdict를 알려 주세요.

후속 지시에 따라 검증 종료 후 제품 시험을 재실행하지 않고 완료된 관찰만 이 원본으로 정리했다.

## 신규 B-P1-16 — bare CR의 텍스트 변환으로 신규 diff 위반이 통과한다

- 심각도/상태: **P1 / OPEN**, 수정 필요.
- 위치: tools/ux_lint.py:699의 subprocess.run(text=True), :673의 Path.read_text, :760~772의 diff parser. 계약: docs/tasks/T-103-kt-contrast-ux-lint.md:22, 39 및 docs/standards/ux-guide.md:15.
- 원인: split("\n") 전에 subprocess의 universal newline 처리가 bare CR(U+000D)을 LF로 바꾼다. 따라서 원래 Git의 한 LF 행 안에 있던 가짜 hunk가 독립 patch 행이 된다. 소스 read_text도 bare CR을 LF로 바꾸어 실제 Git line 2의 finding을 line 3으로 보고한다.
- 영향: 유효한 JavaScript template을 포함한 새 파일 변경에서 P8을 발견해도 added=false, fail_count=0, exit 0/PASS가 된다. 전체 report에서는 P8을 발견하므로 parser보다 앞선 입력 변환과 diff 좌표 정합성 문제다.
- 기존 B-P1-15의 LS/PS 반례는 이번 수정으로 닫혔다. 이 finding은 별도 입력 변환 지점의 bare CR 경계다. 두 읽기 함수는 이번 delta에서 변하지 않았으므로 이번 수정이 새로 도입한 회귀라고 단정하지 않는다.

최소 재현은 별도 임시 Git 저장소에서 Page.ts의 안전한 2행을 커밋한 뒤 아래 bytes로 바꾸는 것이다. chr(96)은 template backtick이다.

~~~python
source = ('const text = ' + chr(96) + 'a\r@@ -0,0 +99,1 @@' +
          chr(96) + ';\nwindow.confirm("확인");\n')
path.write_bytes(source.encode("utf8"))
~~~

직접 실행한 외부 probe는 .git/codex-audit/t103-post18-b-new.py다. 다음과 같은 절차를 양 OS에서 실행했다.

~~~python
from pathlib import Path
import os, subprocess, sys, tempfile
tool = Path("F:/dev/kor-travel-common-wt/review-t103-post18-b/tools/ux_lint.py")
env = {k:v for k,v in os.environ.items()
       if not k.startswith("GIT_") and k != "GITHUB_STEP_SUMMARY"}
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, env=env, text=True).strip()
    git("init", "-q")
    path = root / "Page.ts"
    path.write_bytes(b'const text = "base";\nconst safe = 1;\n')
    git("add", "--", "Page.ts")
    git("-c", "user.name=reviewer-b", "-c", "user.email=reviewer-b@example.invalid",
        "commit", "-qm", "probe baseline")
    base = git("rev-parse", "HEAD")
    for payload in ("@@ -0,0 +99,1 @@", "-content"):
        source = ('const text = ' + chr(96) + 'a\r' + payload +
                  chr(96) + ';\nwindow.confirm("확인");\n')
        path.write_bytes(source.encode("utf8"))
        for options in ([], ["--base", base]):
            result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool),
                "--root", str(root), "--fail-new", "--json", *options],
                cwd=root, env=env, capture_output=True, text=True, encoding="utf8")
            print(payload, options, result.returncode, result.stdout)
~~~

WSL의 tool은 /mnt/f/dev/kor-travel-common-wt/review-t103-post18-b/tools/ux_lint.py다. 입력은 write_bytes로 저장하여 Windows 출력 변환이 반례를 바꾸지 않게 했다. 임시 baseline 커밋은 -c 옵션으로 신원을 지정했으며 source 설정은 수정하지 않았다.

| 대조 | 양 OS 실제 결과 | 기대 |
|---|---|---|
| bare CR + 가짜 @@ hunk, --base | exit 0 / PASS / fail_count 0 / P8 line 3 / added=false | exit 1 / FAIL / 실제 LF line 2 / added=true |
| bare CR + -content, --base | 위와 동일 | 위와 동일 |
| bare CR + 가짜 hunk, 전체 --fail-new | exit 1 / FAIL / fail_count 1 / P8 line 3 | 차단하되 Git 좌표는 line 2 |
| 같은 가짜 hunk의 LS/PS/FF/NEL 대조, --base | exit 1 / FAIL / P8 line 2 / added=true | 동일 |
| LF 정상 2행 대조, --base | exit 1 / FAIL / P8 line 2 / added=true | 동일 |
| Node 실행 의미 대조 | 5개 구분자 모두 exit 0, stub confirm 호출 1회 | 유효한 실행 template |

권고: Git 출력과 소스 UTF-8 읽기 모두에서 원본 줄 구분 바이트를 보존한다. 예를 들어 subprocess bytes를 명시적으로 decode하고 소스는 newline 변환 없이 읽은 뒤 Git 좌표 계산에는 LF만 쓴다. JavaScript 주석 종료(CR/LF/LS/PS)와 Git 행 좌표(LF)를 구분해 유지한다. bare CR/CRLF/LF 및 LS/PS의 가짜 hunk·공백·+·- 접두어, 실제 신규/기존 행 양성·음성을 함께 회귀로 고정하는 것이 최소 수정 방향이다.

## 누적 finding disposition

| ID | 원 심각도 | 결과·이번 직접 대조 |
|---|---|---|
| B-P1-01 | P1 | FIXED — --root/CWD·외부 root Git 기준 |
| B-P1-02 | P1 | FIXED — 앞 삽입 신규 위반과 baseline 건수 분리 |
| B-P1-03 | P1 | FIXED — MDX 실행/인용, span/fence/JSX/ESM·Unicode·async·FEFF 전체 corpus |
| B-P1-04 | P1 | FIXED — JSON/Markdown/summary 입력 경로·값 redaction |
| B-P2-05 | P2 | FIXED — muted 장식 기본·추가 읽기 표면 31쌍 |
| B-P2-06 | P2 | FIXED — baseline 숫자/타입/거대·깊은 JSON exit 2 |
| B-P3-07 | P3 | FIXED — geo 예제 미달 8건과 evidence |
| B-P1-08 | P1 | FIXED — 실제 +++ 추가 행 차단 |
| B-P1-09 | P1 | FIXED — CSS media/교집합/specificity/source order/string/comment |
| B-P2-10 | P2 | FIXED — airport 현재 source-over 1.320934와 역사 1.15 |
| B-P1-11 | P1 | FIXED — selector 대소문자·인용 공백·comment-gap |
| B-P1-12 | P1 | FIXED — 빈 selector 목록·root descendant 입력 오류 |
| B-P2-13 | P2 | FIXED — 파일 첫 span·3자 inline 인용 음성 |
| B-P1-14 | P1 | FIXED — 네 줄 종결자 plain TS/MDX/template 보간/중첩 JSX 주석 종료 |
| B-P1-15 | P1 | FIXED — LS/PS 뒤 공백·가짜 hunk·+·-·+++의 신규 diff 행 차단 |

기존 B-P1-15의 정확한 원 입력인 const n=1 주석 뒤 LS/PS와 공백, 다음 LF 행 window.confirm은 일반/--base 모두 exit 1, P8 line 2다. LF 대조도 두 모드 exit 1이다. 추가로 untracked MDX의 마지막 LF 없음, ESM의 이전 LS/PS 문자열과 다중행 template, 닫힌 문서 span 음성을 확인했다.

## 실행 환경·명령·결과

Windows Python 3.14.3 / Node v25.9.0, WSL Python 3.11.15 / Node v22.22.2. Unicode DB 16.0.0/14.0.0의 차이를 관찰했으나 해당 Unicode 판정 corpus의 결과는 같았다. 모든 소비자 입력은 common fixture 또는 임시 생성물이며 실제 소비자 파일에는 쓰지 않았다.

아래 python은 Windows의 py -3.14 및 WSL의 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11을 뜻한다.

| 실행 | Windows | WSL |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p "test_*.py" | 290개 실행·통과, skip 0, 109.551초 | 수집 290 / 실행·통과 287 / skip 3, 33.319초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v | 52개 통과, 18.069초 | 52개 통과, 9.227초 |
| tools/validate_plan.py | 상세 task 106, 오류 0 | 동일 |
| tools/validate_document_links.py | 문서 445, 대상 2420, 오류 0 | 동일 |
| tools/check_spdx.py | 파일 56, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 파일 577, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 파일 577, 발견 0 | 동일 |
| tools/check_versions.py --self-check | exit 0, registry 자체 검사만 | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1, 오류 0 | 동일 |
| aliases focused unittest | 35개 통과, 2.908초 | 수집 35 / 실행·통과 34 / skip 1, 0.229초 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report 모드 exit 0, 발견 12건 | 동일 |
| git diff --check 6a274c18aa7bffe6fa21ce1b4c8e06bdf848bb56 31ad7a5876ff0d5714d4094cb4a402718d02a33f | exit 0, 출력 없음 | 동일 |

전체 시험에서는 -v만 생략해 출력량을 줄였다. 시험 선택은 같다. 전체·정적 검사는 외부 wrapper .git/codex-audit/review-t102-b-wsl-unittest.py 및 review-t102-post-b-gates.py에 이번 후보 root를 전달했다. wrapper는 GIT_* 상속을 제거한 임시 사본을 만들고 자체 Git을 사용하며 후보/source의 Git 설정에 쓰지 않는다. WSL diff는 읽기 전용 --git-dir=/mnt/f/dev/kor-travel-common/.git 및 --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post18-b 인자로 실행했다.

독립 corpus 명령은 python -B -X utf8 .git/codex-audit/<script> <candidate-root> <output-name>이며 WSL에서는 절대 /mnt/f 경로를 사용했다.

| script | 양 OS 각각 관찰 수 | 대조 |
|---|---:|---|
| t103-post9-b-corpus.py | 105 | 전체 JSON 동일: CSS/JSON/redaction/diff/symlink/초기 MDX |
| t103-post15-b-late-corpus.py | 140 | 전체 JSON 동일: 문단/fence/JSX/CSS gap/Unicode/airport |
| t103-post17-b-latest-corpus.py | 104 | 환경 Unicode DB 1행 외 동일: 103개 실제 관찰 및 기존 B-P1-15 수정 |
| t103-post18-b-new.py | 37 | 전체 JSON 동일: 32 CLI·5 Node 관찰, CR 실패 2개 |

총 386행은 unit test 수가 아니라 CLI·Node·계산·환경 관찰 수다. 37개 새 관찰에서 기대 exit와 다른 경우는 CR 가짜 hunk 및 CR -content 2개이며 하나의 원인으로 집계했다. 합성 비밀/주소 값은 출력·보고서에 노출하지 않고 노출 여부만 검사했다. Windows 임시 Git의 LF→CRLF 안내 1건은 baseline stage 시 출력됐고 CLI 판정 실패와 구분했다.

## 정본·범위·미실행

현재 T-103 task와 resume은 IN_PROGRESS다. UX-G9 및 task의 --base 신규 행 차단 계약은 B-P1-16 때문에 아직 닫을 수 없다. airport 1.32/1.320934, geo 8건, muted 추가 쌍, GPL-3.0-or-later/common-only, 소비자 baseline 외부 소유 및 후행 T-010 workflow 경계는 현재 문서·fixture와 일치한다. 이 규범 문서들은 이번 delta에서 변경되지 않았다.

- NOT_RUN(Windows Python 3.11): py -0p는 3.14/3.10만 반환했다.
- NOT_RUN(WSL skip 3개): Windows 8.3 경로 1개, jsonschema parity 2개. importlib.util.find_spec("jsonschema")는 None이며 skip을 통과 수에서 제외했다.
- NOT_RUN(원격 exact candidate CI 독립 조회): 로컬 시험을 CI 성공으로 집계하지 않았다.
- NOT_RUN(MDX 실제 compiler/browser): CLI와 Node 실행 식 의미를 대조했으며 실제 MDX compile/e2e는 수행하지 않았다.
- NOT_RUN(소비자 build/e2e·앱 baseline 등록): 소비자 이관 task의 외부 gate다.
- NOT_RUN(npm/PyPI registry·게시·workflow dispatch·contrast-check workflow selftest): 요청 범위 밖/호출 금지이며 재사용 workflow는 후행 T-010 소유다.

제품 candidate는 수정하지 않았다. 원본 최종 판정은 **NO-GO**, 기존 15개 원 반례 FIXED, 신규 B-P1-16 OPEN이다.
