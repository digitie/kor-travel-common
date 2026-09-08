<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-14 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST14-B-20260908-122742.
- 최종 판정: **NO-GO**. 누적 13개 ID 중 12개 FIXED, **B-P1-03 OPEN**. 신규 ID 0; 현재 잔여 P0 0 / P1 1 / P2 0 / P3 0.
- 시작: 2026-09-08T12:27:42.8140543+09:00. 제품 검토 종료: 2026-09-08T12:30:38.6267489+09:00.
- 제품 시작·종료 SHA: 0b2330e93d2b05a954593c82ef0ea230821adf28.
- 제품 시작·종료 tree: 688332816480e217b3615dd6426e063c223e365a.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post14-b의 새 detached worktree. 시작·종료 git status --porcelain=v1 출력 없음.
- manifest: commit 507328aa615f68b7828e9da543f80a6c805c4d3a의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-14-manifest.md를 git show로 읽었다. 원문 blob SHA256: ee8f5befb9b3208471308126f39f8246301215fbe0bea714a99d52bff901b44f.
- 수정 delta: e8137efd8f4b53465b8cf9a1d333127e4186b73c..0b2330e93d2b05a954593c82ef0ea230821adf28. 제품 수정은 tools/ux_lint.py와 tests/test_ux_lint.py뿐이다. 다른 3개 manifest/raw는 경로만 확인하고 상대·과거 raw 본문을 읽지 않았다.
- source .git/config 시작·종료 SHA256 동일: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B.
- 후보·manifest·소비자·Git 설정을 수정하지 않았다. 제품 검토 종료 후 이 보고서 한 파일만 별도 branch에 커밋한다. push 없음.

## 전달 요청 원문

> T-103 post-fix-14 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 0b2330e93d2b05a954593c82ef0ea230821adf28, tree 688332816480e217b3615dd6426e063c223e365a로 detached clean checkout하고, 공통 manifest는 commit 507328a의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-14-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw를 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 full/focused/static gate와 누적 CSS/JSON/redaction/diff/symlink/airport corpus, 특히 미종결 1/2자 Markdown span 뒤 직접/단항/키워드/논리/숫자/정규식/소수/나눗셈·xor/Unicode 일반·결합문자·ZWNJ/ZWJ·\uXXXX·\u{...} escape·주석 선행 MDX expression, 여러 줄 JSX expression 및 정상 닫힌 span 음성 대조를 독립 재현하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-14-reviewer-b.md에 기록하고 immutable raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정/커밋/푸시하지 마세요. PASS/NO-GO와 모든 finding ID/disposition을 명확히 보고하고 완료 후 메시지를 주세요.

## B-P1-03 — JavaScript 식별자 분류와 Python 분류가 달라 P8을 누락함

**P1, OPEN, 수정 필요.** 위치: [ux_lint.py](../../../../tools/ux_lint.py) 172~186행, 217~230행, 253~273행. 계약: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md) 22행의 실행 코드 P8 검사·백틱 인용 제외.

이번 수정으로 기존 escape·결합문자·ZWNJ 반례는 닫혔다. 그러나 바깥 분기의 isalpha 검사, Python isidentifier의 XID 기반 판정, 직접 나열한 연속 문자 category가 JavaScript 식별자와 같은 집합이 아니다. 합법적인 식별자를 읽지 못하면 미종결 백틱 뒤의 실행 표현식을 문단 끝까지 지운다. 신규 위반이 있는 입력을 exit 0/PASS로 처리하는 기존 B-P1-03의 원인이 남았으므로 새 ID를 만들지 않았다.

최소 입력 Page.mdx:

~~~~mdx
export const Ⅳ = 1

Example ` unmatched {Ⅳ && window.confirm("확인")}
~~~~

명령: python -B -X utf8 <후보>/tools/ux_lint.py --root <임시 fixture 폴더> --fail-new --json.

- 기대: exit 1, P8 1건. 닫는 백틱이 없어 문서 인용 span이 성립하지 않는다.
- 실제 Windows Python 3.14·WSL Python 3.11: **exit 0, status PASS, findings 0**.
- 미종결 백틱을 2개로 바꾸어도 동일. opener를 제거한 대조는 exit 1/P8 1건이고, 정상 닫힌 span은 exit 0/0건이다.
- 다음 다섯 이름 각각을 선언과 표현식에 함께 사용했으며 모두 같은 결과다.

| 이름 구성 | 분류 경계·원인 |
|---|---|
| chr(0x2163), Ⅳ | Nl 시작 문자를 바깥 isalpha 분기가 거부 |
| chr(0x2118), ℘ | Other_ID_Start를 바깥 isalpha 분기가 거부 |
| chr(0x037A) | JavaScript에서 유효하지만 Python isidentifier가 거부하는 시작 문자 |
| "a" + chr(0x00B7) | 중점의 Other_ID_Continue 누락 |
| "a" + chr(0x0387) | Greek ano teleia의 Other_ID_Continue 누락 |

Windows Node v25.9.0·WSL Node v22.22.2에서 다섯 표현식 모두 정상 구문으로 실행되고 confirm 스텁이 1회 호출됨을 확인했다. 다음 스텁의 선언·사용 이름을 각 ident로 바꿔 실행했다. 실제 브라우저 대화상자는 호출하지 않았다.

~~~~javascript
let called = 0;
const window = {confirm() { called++; return true; }};
const Ⅳ = 1;
Ⅳ && window.confirm("확인");
console.log(called);
~~~~

후보 밖 probe 핵심은 다음과 같다. 식별자 선언을 넣어 미정의 변수 반례와 구분했고, 환경에서 GIT_*와 GITHUB_STEP_SUMMARY를 제거했다.

~~~~python
names = [chr(0x2163), chr(0x2118), chr(0x037A),
         "a" + chr(0x00B7), "a" + chr(0x0387)]
for ident in names:
    expr = "{" + ident + ' && window.confirm("확인")}'
    for run in (0, 1, 2, 3):
        tail = ("`" + expr + "`" if run == 3 else
                ("`" * run + " unmatched " if run else "") + expr)
        source = "export const " + ident + " = 1\n\nExample " + tail + "\n"
        (fixture / "Page.mdx").write_text(source, encoding="utf8")
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(candidate / "tools/ux_lint.py"),
             "--root", str(fixture), "--fail-new", "--json"],
            cwd=fixture, env=isolated_env, capture_output=True, text=True, encoding="utf8")
~~~~

권고: JavaScript IdentifierStart/IdentifierPart를 부분적인 Python 문자 판정과 동일시하지 말고 경계를 일관되게 처리한다. 특히 바깥 isalpha와 안쪽 식별자 판정을 분리하지 않는다. 미종결 span에서 인식하지 못한 표현식을 조용히 지워 성공으로 만드는 구조도 제거하거나 입력 오류로 명시한다. 위 다섯 이름 각각 opener 0/1/2와 정상 닫힌 span 대조를 회귀 시험에 추가한다.

## 누적 finding disposition

| ID | 원 심각도 | 이번 독립 재현·판정 |
|---|---|---|
| B-P1-01 | P1 | FIXED — 외부 root/CWD·Git diff 범위 |
| B-P1-02 | P1 | FIXED — 앞삽입 신규 위반이 baseline 건수로 면제되지 않음 |
| B-P1-03 | P1 | **OPEN** — 기존 명시 expression 및 결합·ZWNJ·escape는 FIXED, 위 다섯 식별자 경계 잔여 |
| B-P1-04 | P1 | FIXED — path/값·stdout/JSON/Markdown/step summary redaction |
| B-P2-05 | P2 | FIXED — 명시한 muted 읽기 표면 4쌍 추가 |
| B-P2-06 | P2 | FIXED — 숫자/schema/huge/deep JSON 일반 입력 오류 2 |
| B-P3-07 | P3 | FIXED — geo 예제와 evidence 8건 일치 |
| B-P1-08 | P1 | FIXED — diff 추가 내용의 +++ 접두 위반 검출 |
| B-P1-09 | P1 | FIXED — media 교집합·specificity/source order·CSS string/comment/nested 경계 |
| B-P2-10 | P2 | FIXED — airport 현재 1.320934와 역사 1.15 분리 |
| B-P1-11 | P1 | FIXED — selector 대소문자·인용 내부 공백 보존 |
| B-P1-12 | P1 | FIXED — 빈 selector 항목·root descendant 입력 오류 |
| B-P2-13 | P2 | FIXED — 파일 첫·3자 inline span 정상 제외 |

## 실제 실행 결과

전체 시험·tracked-file 정적 gate는 후보를 OS 임시 디렉터리에 복사한 뒤 새 Git 저장소에 경로별 stage하고 GIT_* 환경변수를 제거하여 실행했다. source .git/config는 상속·변경하지 않았다. focused 및 직접 CLI는 후보 코드를 읽고 후보 밖 임시 fixture를 생성했다. 이전 raw의 시험 결과를 재사용하지 않고 현재 후보에서 재실행했다.

| 명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p "test_*.py" | 287/287 통과, skip 0, 99.960초 | 287 수집, 284 실행 통과, skip 3, 27.302초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v | 49/49 통과, 22.178초 | 49/49 통과, 10.451초 |
| 별칭 focused unittest discover -s tests -p test_check_aliases.py | 35/35 통과 | 35 수집, 34 실행 통과·skip 1 |
| tools/validate_plan.py | task 106개, 오류 0 | 동일 |
| tools/validate_document_links.py | 문서 433개·대상 2414개, 오류 0 | 동일 |
| tools/check_spdx.py | 파일 56개, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 파일 565개, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 파일 565개, 발견 0 | 동일 |
| tools/check_versions.py --self-check | exit 0, 소비자 검사 아님 명시 | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report mode exit 0, 12건 | 동일 |
| git diff --check 6da46d4fe3ceb7c82ad2000cffe9fcb160d6cdac 0b2330e93d2b05a954593c82ef0ea230821adf28 | exit 0 | exit 0 |

Python 도구 모두 해당 OS Python의 -B -X utf8을 사용했다. 전체 시험은 출력량을 줄이기 위해 -v만 생략했다. WSL diff는 Windows worktree 포인터를 변경하지 않고 --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post14-b 명령 옵션으로 실행했다.

후보 밖 직접 probe: Windows 명령은 py -3.14 -B -X utf8 .git/codex-audit/<script> F:/dev/kor-travel-common-wt/review-t103-post14-b, WSL 명령은 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/<script> /mnt/f/dev/kor-travel-common-wt/review-t103-post14-b다.

- t103-post9-b-corpus.py: 기존 자체 probe 9개, 관찰 105행을 각 OS에서 재생성했다. 두 JSON 전체가 같고 marker/traceback true가 없다. root·symlink·redaction 모든 출력 채널·JSON 숫자/깊이·baseline/diff +++·CSS cascade/media/nested/string·selector·4앱 예제·ESM/배열/삼항/임의 tag/다중행/blockquote JSX·fence·문서 span을 포함한다.
- t103-post9-b-new.py: 21행. CSS comment-gap·같은 문단 미종결 1/2자 span·빈 문단·blockquote·CRLF·backslash 대조.
- t103-post10-b-new.py: 7행. 직접 expression·여러 줄 JSX·정상 닫힌 span.
- t103-post11-b-new.py: 15행. 직접·단항 !·void·논리·숫자 각각 opener 0/1/2 모두 P8 검출.
- t103-post12-b-new.py: 21행. block/line comment·regex·소수·나눗셈·XOR·한글 각각 opener 0/1/2 모두 P8 검출.
- t103-post13-b-new.py: 16회 CLI + 4회 JS 실행. \u006e·결합문자·ZWNJ·보충 평면 이름 모두 opener 0/1/2에서 P8, 정상 닫힌 span은 제외된다.
- t103-post14-b-new.py: 9개 식별자 × 4회 CLI, 9회 JS 실행. \u{6e}·이름 계속 부분의 \u006e/\u{6e}·ZWJ 네 양성군은 정상 검출·인용 제외된다. 위 다섯 잔여군은 opener 1/2에서 false PASS다. 양 OS 결과 동일.
- t103-post3-b-smoke.py: canonical 27쌍, UX report 12건, airport line 1.3209340364487114.
- t103-post1-b-media.py: 8회. 지원 dark media는 모드별 적용·배제, not/width 복합 조건은 입력 오류 2.

관찰 행 수를 unittest 건수에 더하지 않았다. 현재 T-103은 IN_PROGRESS이며 resume도 독립 리뷰·PR/CI/merge가 남았다고 명시한다. airport 수용 기준/evidence, GPL-3.0-or-later, common 예제와 소비자 baseline 등록의 외부 task 경계는 이번 delta에서 바뀌지 않았다. T-010 워크플로는 후행 소유이고 npm/PyPI 게시·소비자 수정을 이번 완료로 표시하지 않는다.

## NOT_RUN·한계

- **NOT_RUN Windows Python 3.11**: py -0p가 3.14/3.10만 제공한다.
- WSL full skip 3은 Windows 8.3 전용 1개와 jsonschema 미설치 parity 2개다. find_spec("jsonschema")가 None임을 직접 확인했다. skip은 통과 수에서 제외했다.
- **NOT_RUN exact candidate 원격 CI 독립 조회**, workflow dispatch, 소비자 build/e2e, npm/PyPI registry·게시. 로컬 성공을 원격 또는 소비자 gate 성공으로 집계하지 않는다.
- **NOT_RUN MDX 컴파일러·브라우저 통합 실행**. 실제 CLI 결과와 Node JavaScript 스텁 실행을 근거로 삼았으며 둘을 구분했다.
- 상대 reviewer 결과·미확정 raw를 열람하지 않았다. 원본은 검토 후보의 판단이며 이후 commit의 수정 여부를 추정하지 않는다.
