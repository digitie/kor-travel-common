<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-19 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST19-B-20260908T133256-KST.
- 판정: **NO-GO**. 누적 16개 중 15개 FIXED, **B-P1-03(P1) REOPENED/OPEN** 1개다. 새 ID를 부여한 finding은 없으며 P0/P2/P3 미해결은 0개다.
- 제품 검증 시작: 2026-09-08T13:32:56.4932959+09:00. 종료: 2026-09-08T13:36:39.3925129+09:00.
- 시작/종료 제품 HEAD: 415984bf7cb450d44d7661424884d6641fef8309.
- 시작/종료 제품 tree: 9c07d86aea28e130ad58b912d72ad99152795c31.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post19-b에 새 detached worktree. 시작/종료 git status --porcelain=v1 --untracked-files=all은 모두 빈 출력(clean)이었다.
- manifest: a0d12d2299e3cb4e55ea560e6c24ea5aff3167c7의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-19-manifest.md를 git show로 읽었다. Git blob SHA256: 9ddfe9233ffc79b2a88626b1b1398d7375f6999a227aeecdad5e226f42809fd7.
- 수정 delta: 31ad7a5876ff0d5714d4094cb4a402718d02a33f..415984bf7cb450d44d7661424884d6641fef8309. 제품 2파일(tools/ux_lint.py, tests/test_ux_lint.py)의 전체 diff와 현재 task/정본 관련 절을 확인했다. 나머지 이전 manifest/raw 3파일은 경로만 확인했다.
- source .git/config 시작/종료 SHA256: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B. 설정을 변경하지 않았다.
- 상대 이번/이전 raw 본문이나 미확정 분석 결과는 읽거나 요청하지 않았다. manifest의 commit/hash와 coordinator의 진행 상태만 접했다.
- 후보·manifest·소비자 수정, registry·workflow dispatch·push는 수행하지 않았다. 이 보고서 한 파일만 별도 branch의 evidence commit에 포함한다.

## 요청 원문

> T-103 post-fix-19 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 415984bf7cb450d44d7661424884d6641fef8309, tree 9c07d86aea28e130ad58b912d72ad99152795c31의 detached clean checkout으로 고정합니다. 공통 manifest는 commit a0d12d2의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-19-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw는 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate와 누적 corpus를 독립 재현하고, 특히 실제 CR/CRLF/LS/PS와 문자열 @@ 가짜 hunk가 plain scan 및 --base added mapping을 보존하는지 검증하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-19-reviewer-b.md에 기록하고 raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정·커밋·푸시하지 마세요. 상대 원본을 읽지 않은 상태로 완료 메시지에 commit/hash/verdict를 알려 주세요.

## B-P1-03 재개방 — bare CR 문단/fence가 실행 JSX를 인용 영역으로 숨긴다

- 원 ID/심각도/상태: **B-P1-03 / P1 / REOPENED(OPEN)**. 기존 MDX 실행/인용 분류 finding의 개행 회귀이므로 새 ID로 중복 집계하지 않는다.
- 위치: tools/ux_lint.py:21의 _MDX_PARAGRAPH_BOUNDARY, :463~477의 _mask_mdx_fence LF 탐색. 이번 :104~109 개행 보존 reader 도입으로 기존의 암묵적 CR→LF 변환이 사라졌는데 MDX lexer가 이를 따라가지 못한다.
- 근거: [CommonMark 0.31.2 §2.1](https://spec.commonmark.org/0.31.2/#line-ending)은 LF, bare CR, CRLF를 문서 줄 종결자로 정의한다(문서 버전 2024-01-28, 조회 2026-09-08). CR은 문단 및 fence 경계에도 반영되어야 한다. Git 좌표가 LF 기준이라는 사실과 문서의 논리 줄 경계는 별개의 계약이다.
- 영향: 닫히지 않은 span 뒤의 빈 문단, 또는 이미 닫힌 fence 뒤에 있는 실제 JSX를 검사에서 제거한다. 일반 --fail-new와 --base 모두 정상 PASS/0건이어서 신규 P6 위반을 차단하지 못한다.
- 현재 LF/CRLF 및 기존 Unicode/표현식 대조는 통과한다. 문제가 있는 바이트 입력을 양 OS에서 동일 SHA256으로 생성해 재현했으므로 OS별 생성기 차이로 판단하지 않았다.

최소 반례 1(문단):

~~~python
source = ('Example ' + chr(96)*2 + ' unmatched\r\r' +
          '<div className="outline-none"/>\r\rLater ' +
          chr(96)*2 + ' delimiter\r')
~~~

최소 반례 2(fence):

~~~python
source = ('~~~tsx\r<div className="outline-none"/>\r~~~\r' +
          '<div className="outline-none"/>\r')
~~~

두 번째 입력은 fence 안의 인용은 제외하고 fence 뒤 JSX 한 건을 발견해야 한다. 두 입력 모두 Path.write_bytes(source.encode("utf8"))로 Page.mdx에 저장했다. 정확한 CLI 대조는 아래와 같다. WSL에서는 tool의 경로를 /mnt/f/dev/kor-travel-common-wt/review-t103-post19-b/tools/ux_lint.py로 바꾼다.

~~~python
from pathlib import Path
import os, subprocess, sys, tempfile
tool = Path("F:/dev/kor-travel-common-wt/review-t103-post19-b/tools/ux_lint.py")
env = {k:v for k,v in os.environ.items()
       if not k.startswith("GIT_") and k != "GITHUB_STEP_SUMMARY"}
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    for eol in ("\n", "\r\n", "\r", "\r\r\n"):
        text = ("Example " + chr(96)*2 + " unmatched" + eol*2 +
                '<div className="outline-none"/>' + eol*2 +
                "Later " + chr(96)*2 + " delimiter" + eol)
        (root / "Page.mdx").write_bytes(text.encode("utf8"))
        result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(tool),
            "--root", str(root), "--fail-new", "--json"],
            cwd=root, env=env, capture_output=True, text=True, encoding="utf8")
        print(repr(eol), result.returncode, result.stdout)
~~~

임시 Git baseline을 만든 뒤 같은 untracked Page.mdx에 --base를 붙인 대조도 외부 probe t103-post19-b-new.py에서 실행했다. 관련 실제 관찰은 다음과 같다.

| 입력 | 양 OS 일반/--base 결과 | 기대 |
|---|---|---|
| LF 문단 | exit 1 / P6 1건, line 3 | 동일 |
| CRLF 문단 | exit 1 / P6 1건, line 3 | 동일 |
| bare CR 문단 | **둘 다 exit 0 / PASS / 0건** | exit 1 / P6 1건 |
| CR+CRLF 문단 | **둘 다 exit 0 / PASS / 0건** | exit 1 / P6 1건 |
| 닫힌 span 음성(LF/CRLF/CR/CR+CRLF) | exit 0 / 0건 | 동일 |
| span 없는 JSX 양성(네 종류) | exit 1 / P6 1건 | 동일 |
| LF/CRLF fence 뒤 JSX | 일반 exit 1 / P6 1건, line 4 | 동일 |
| bare CR fence 뒤 JSX | **일반 exit 0 / PASS / 0건** | exit 1 / P6 1건 |

동일 bytes 확인: bare CR 문단 SHA256 1604055117c91ce55ca93ebd1a74aac8e8460df87cb0a36c6d774603d0c23869, CR+CRLF 문단 45f7f37d241c67515701b9412fad657a191df860e16ed6ce098905c773556228, bare CR fence 3bdd5e71e81cce562321b72463fb23ccbdd2a6cbaa8ff06a02b6cb7992c8a113. 양 OS 결과와 입력 hash가 모두 일치했다.

권고: 원본 newline reader와 Git LF 좌표는 유지하고, Markdown 논리 줄·문단·fence 인식에서 CRLF를 하나의 끝, bare CR/LF를 각각 줄 끝으로 처리한다. 원본 길이/offset을 보존하는 lexer 경계 또는 별도 좌표 매핑을 사용해 이번 Git diff 수정이 되돌아가지 않게 한다. 정확한 bytes fixture로 LF/CRLF/CR/CR+CRLF 및 inline 음성·fence 뒤 실행 양성을 고정한다. 실제 MDX compiler 대조는 아래 NOT_RUN으로 분리한다.

## 누적 disposition 및 이번 수정 확인

| ID | 원 심각도 | 이번 결과 |
|---|---|---|
| B-P1-01 | P1 | FIXED — root/CWD 및 외부 Git 기준 |
| B-P1-02 | P1 | FIXED — 신규 앞 삽입과 baseline 건수 |
| B-P1-03 | P1 | **REOPENED** — 위 bare CR 문단/fence 경계. 나머지 누적 MDX 반례는 기대 결과 |
| B-P1-04 | P1 | FIXED — 경로·값 오류 JSON/Markdown/summary redaction |
| B-P2-05 | P2 | FIXED — muted 장식/추가 읽기 31쌍 |
| B-P2-06 | P2 | FIXED — baseline 타입/숫자/거대·깊은 JSON exit 2 |
| B-P3-07 | P3 | FIXED — geo 미달 8건 |
| B-P1-08 | P1 | FIXED — 실제 +++ diff 추가 행 |
| B-P1-09 | P1 | FIXED — CSS 조건·specificity·source order·string/comment |
| B-P2-10 | P2 | FIXED — airport 1.320934 및 역사 1.15 |
| B-P1-11 | P1 | FIXED — selector case·인용 공백·comment-gap |
| B-P1-12 | P1 | FIXED — 빈 selector 목록·root descendant 오류 |
| B-P2-13 | P2 | FIXED — 파일 첫 span·3자 inline 음성 |
| B-P1-14 | P1 | FIXED — JS 네 줄 종결자 주석 종료·template 보간·JSX 중첩 |
| B-P1-15 | P1 | FIXED — LS/PS의 가짜 patch hunk·공백·+·- |
| B-P1-16 | P1 | FIXED — bare CR의 가짜 hunk·-content, 정확한 LF line 2와 added=true |

B-P1-16 원 반례는 일반/--base 모두 exit 1, P8 line 2, added=true다. 실제 CR/LF/CRLF/LS/PS의 plain 주석 뒤 P8도 전체/--base/untracked 마지막 LF 없음에서 모두 차단했다. 좌표는 LF/CRLF일 때 line 2, bare CR/LS/PS일 때 Git LF 기준 line 1이다. baseline JSON 등 기존 입력 오류의 generic error/exit 2 corpus도 다시 확인했다. 새 Git bytes decode의 예외 처리는 코드로 확인했으며 비UTF-8 Git 출력 강제 주입은 실행하지 않았다.

## 실행 명령·검증 결과

환경은 Windows Python 3.14.3 / Node v25.9.0, WSL Python 3.11.15 / Node v22.22.2다. Python Unicode DB 메타데이터는 16.0.0/14.0.0이었다. 아래 python은 py -3.14 및 WSL /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11이다.

| 실행 | Windows | WSL |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p "test_*.py" | 290개 실행·통과, skip 0, 108.717초 | 수집 290 / 실행·통과 287 / skip 3, 32.049초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v | 52개 통과, 19.153초 | 52개 통과, 10.327초 |
| tools/validate_plan.py | task 106, 오류 0 | 동일 |
| tools/validate_document_links.py | 문서 448, 대상 2420, 오류 0 | 동일 |
| tools/check_spdx.py | 파일 56, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 파일 580, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 파일 580, 발견 0 | 동일 |
| tools/check_versions.py --self-check | exit 0, 자체 검사만 | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1, 오류 0 | 동일 |
| aliases focused unittest | 35개 통과, 2.735초 | 수집 35 / 실행·통과 34 / skip 1, 0.296초 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report 모드 exit 0, 발견 12건 | 동일 |
| git diff --check 538fc429301ddf5afd978640ce66f37517674150 415984bf7cb450d44d7661424884d6641fef8309 | exit 0, 출력 없음 | 동일 |

전체 시험은 -v만 생략했다. 전체·정적 검사 wrapper는 .git/codex-audit/review-t102-b-wsl-unittest.py 및 review-t102-post-b-gates.py에 후보 root를 전달했다. GIT_* 상속 없는 임시 Git 사본에서 실행해 source Git config와 후보 연결을 사용하지 않았다. WSL diff는 읽기 전용 --git-dir=/mnt/f/dev/kor-travel-common/.git 및 --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post19-b 인자를 사용했다.

추가 corpus 명령은 python -B -X utf8 .git/codex-audit/<script> <candidate-root> <output-name>이며 WSL은 /mnt/f 절대 경로다. 모두 이번 후보에서 새로 실행했다.

| script | OS별 관찰 행 | 결과 |
|---|---:|---|
| t103-post9-b-corpus.py | 105 | JSON 동일: CSS/JSON/redaction/diff/symlink/초기 MDX |
| t103-post15-b-late-corpus.py | 140 | 139개 동일. crlf-cross-paragraph 1개는 아래 생성 바이트 차이 |
| t103-post17-b-latest-corpus.py | 104 | Unicode DB 메타데이터 1개 외 103개 동일 |
| t103-post18-b-new.py | 37 | JSON 동일, CR/LS/PS/FF/NEL 가짜 hunk·Node 대조 포함 |
| t103-post19-b-new.py | 34 | bytes SHA256과 결과 전부 동일, CR 문단/fence 실패 5개 CLI 관찰 |

총 420행은 unit test 수가 아닌 CLI·Node·계산·환경 관찰이다. 이전 helper의 crlf-cross-paragraph는 write_text에 CRLF 문자열을 넘겨 Windows에서 CR+CRLF가 생성되고 WSL에서는 CRLF가 생성됐다. 따라서 해당 1개 차이를 같은 입력의 OS 결함으로 세지 않았다. 새 write_bytes 대조에서 실제 CRLF는 양 OS 차단, CR+CRLF는 양 OS 누락으로 확인했다. 이 5개 누락을 B-P1-03 하나로 집계했다. 합성 비밀/주소 원문은 출력·보고서에 넣지 않고 노출 여부만 확인했다.

## 문서와 미실행

T-103와 resume은 IN_PROGRESS다. 현재 task의 신규 UX 위반 차단 수용 기준은 B-P1-03 재개방 때문에 닫히지 않았다. airport 1.32/1.320934와 역사 값, geo 8건, muted 추가 쌍, common-only/GPL-3.0-or-later/소비자 baseline 외부 소유, 후행 T-010 workflow 경계는 변경 없는 정본과 fixture에서 일치했다.

- NOT_RUN(Windows Python 3.11): py -0p에 3.14/3.10만 있다.
- NOT_RUN(WSL skip 3개): Windows 8.3 경로 1개 및 jsonschema parity 2개. find_spec("jsonschema")는 None이며 통과 집계에서 제외했다.
- NOT_RUN(exact candidate 원격 CI 독립 조회): 로컬 성공을 CI 성공으로 집계하지 않았다.
- NOT_RUN(비UTF-8 Git 출력 강제 주입): decode 예외의 generic 오류 경로를 코드로만 확인했다.
- NOT_RUN(실제 MDX compiler/browser): 현재 CLI와 공식 Markdown 줄 문법을 대조했다. 실제 MDX compile/e2e를 실행한 것으로 표시하지 않는다.
- NOT_RUN(소비자 build/e2e·baseline 등록): 소비자 이관 task의 외부 gate다.
- NOT_RUN(npm/PyPI registry·게시·workflow dispatch·재사용 contrast-check selftest): 요청 범위 밖/호출 금지이며 workflow는 후행 T-010 소유다.

최종 원본 판정은 **NO-GO**, B-P1-03(P1) REOPENED, 나머지 누적 15개 FIXED다. 제품 후보는 변경하지 않았으며 이 보고서 한 파일만 evidence commit으로 보존한다.
