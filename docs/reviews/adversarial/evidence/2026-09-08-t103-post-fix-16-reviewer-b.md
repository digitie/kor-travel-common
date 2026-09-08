<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-16 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST16-B-20260908-125246.
- 판정: **NO-GO**. 기존 13개 ID 전부 FIXED, 신규 **B-P1-14 OPEN** 1개. 현재 잔여 P0 0 / P1 1 / P2 0 / P3 0.
- 시작: 2026-09-08T12:52:46.5818551+09:00. 제품 검토 종료: 2026-09-08T12:55:57.0845512+09:00.
- 제품 시작·종료 SHA: 73b9cf68788066742e8df99dfad2433cbe6bf5fc.
- 제품 시작·종료 tree: 70143a39a0ed31dd44a2b28aa81a2a58f23248d3.
- 격리: F:/dev/kor-travel-common-wt/review-t103-post16-b의 새 detached worktree. 시작·종료 git status --porcelain=v1 출력 없음.
- manifest: 4f3bb3d0b530e9486405a22b879a9786c0913b79의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-16-manifest.md를 git show로 읽었다. blob SHA256: 5d04f552088c31bde61ce1b94a42c6759f5bddadcd520ca495b130369b16c642.
- delta: 210c2de324b18fcaa4e3f8b18fe5965226cb79d7..73b9cf68788066742e8df99dfad2433cbe6bf5fc. 제품 변경은 tools/ux_lint.py와 tests/test_ux_lint.py, 나머지 3개는 이전 manifest/raw 경로다. 상대·과거 raw 본문은 읽지 않았다.
- source .git/config 시작·종료 SHA256 동일: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B.
- 후보·manifest·소비자·Git 설정 수정 없음. 제품 검토 종료 후 이 원본 한 파일만 별도 branch에서 커밋한다. push 없음.

## 전달 요청 원문

> T-103 post-fix-16 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 73b9cf68788066742e8df99dfad2433cbe6bf5fc, tree 70143a39a0ed31dd44a2b28aa81a2a58f23248d3의 detached clean checkout으로 고정합니다. 공통 manifest는 commit 4f3bb3d의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-16-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw는 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate와 누적 corpus를 독립 재현하고, 특히 U+11F02/U+2EBF0 최신 식별자, U+FEFF 선행·식별자 뒤 공백, post-fix-15 반례의 1·2자 미종결 span과 정상 닫힌/개방 대조를 검증하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-16-reviewer-b.md에 기록하고 raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정·커밋·푸시하지 마세요. 상대 원본을 읽지 않은 상태로 완료 메시지에 commit/hash/verdict를 알려 주세요.

## B-P1-14 — Unicode 줄 종결자 뒤 실행 코드가 줄 주석으로 가려짐

**P1, OPEN, 수정 필요.** 직접 원인: [ux_lint.py](../../../../tools/ux_lint.py) 533~538행의 line-comment 상태는 LF만 종료문자로 인정한다. 같은 가정이 153행의 MDX 선행 주석 탐색, 337행의 JSX expression 탐색, 470행 이후 template 보간 주석 처리에도 있다. 계약: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md) 22행의 .ts/.tsx/.mdx 실행 코드 P8 검사와 주석 제외.

U+2028(Line Separator) 또는 U+2029(Paragraph Separator)는 실행 JavaScript에서 줄 주석을 끝낸다. 하지만 검사기는 그 뒤의 window.confirm을 계속 주석으로 지워 신규 위반 0건으로 통과시킨다. 미종결 span뿐 아니라 백틱이 없는 plain TypeScript에서도 발생하므로, 기존 B-P1-03의 식별자·span 수정과 구분해 새 ID를 부여했다. 해당 LF 전용 상태 처리는 이번 수정 delta에서 바뀌지 않았으며 post-fix-16이 새로 도입한 회귀라고 주장하지 않는다.

최소 재현은 아래 코드로 Page.ts를 생성하고 CLI를 실행하는 것이다. 눈에 보이지 않는 줄 종결자를 보고서에 그대로 숨기지 않고 생성식으로 표시했다.

~~~~python
from pathlib import Path
source = '// 설명' + chr(0x2028) + 'window.confirm("확인")'
Path("Page.ts").write_text(source, encoding="utf8")
# 두 번째 반례: chr(0x2029)
~~~~

명령: python -B -X utf8 <후보>/tools/ux_lint.py --root <Page.ts가 있는 임시 폴더> --fail-new --json.

| 입력 대조 | Windows Python 3.14.3 | WSL Python 3.11.15 | 기대 |
|---|---|---|---|
| plain .ts, U+2028/U+2029 | **exit 0, PASS, 0건** | **exit 0, PASS, 0건** | exit 1, P8 1건 |
| .mdx의 {expression}, opener 없음 | **exit 0, PASS, 0건** | 동일 | exit 1, P8 1건 |
| .mdx 미종결 1/2자 span 뒤 {expression} | **exit 0, PASS, 0건** | 동일 | exit 1, P8 1건 |
| 정상 닫힌 문서 span | exit 0, 0건 | 동일 | 인용 제외 |
| 같은 실행 입력의 LF/CR 대조 | exit 1, P8 1건 | 동일 | P8 검출 |

MDX expression은 위 source를 중괄호로 감쌌고, 앞에 Example 및 0/1/2개 백틱을 넣었다. 정상 인용은 백틱으로 전체 expression을 감쌌다. 네 종류 줄 종결자 × 다섯 문맥으로 각 OS 20회 CLI를 실행했다.

Windows Node v25.9.0·WSL Node v22.22.2에 아래 스텁과 각 source를 넣어 실행했다. 네 줄 종결자 모두 exit 0이며 called=1이었다. 실제 브라우저 대화상자는 호출하지 않았다.

~~~~javascript
let called = 0;
const window = {confirm() { called++; return true; }};
// 이 위치에 각 source를 삽입한다.
console.log(called);
~~~~

권고: JavaScript 줄 주석 종료를 LF/CR/U+2028/U+2029로 일관되게 처리하고, MDX 선행 주석·JSX 문맥·template 보간의 동일한 가정을 함께 정리한다. plain TS와 MDX의 직접/미종결/정상 인용 대조를 회귀 시험으로 고정한다. 전체 입력에서 줄 구분자를 무조건 치환하면 문자열 내용과 보고 위치가 달라질 수 있으므로 lexer의 주석 경계와 행 보고를 구분해 수정한다.

## 기존 finding disposition

| ID | 원 심각도 | 현재 판정·직접 재현 |
|---|---|---|
| B-P1-01 | P1 | FIXED — 외부 root/CWD·Git diff 범위 |
| B-P1-02 | P1 | FIXED — 앞삽입 위반이 baseline 건수로 면제되지 않음 |
| B-P1-03 | P1 | **FIXED** — 누적 MDX 반례, 최신 Unicode 이름·FEFF 선행/후행도 양 OS에서 P8 검출·정상 인용 제외 |
| B-P1-04 | P1 | FIXED — path/값·stdout/JSON/Markdown/step summary redaction |
| B-P2-05 | P2 | FIXED — 명시한 muted 읽기 표면 4쌍 추가 |
| B-P2-06 | P2 | FIXED — 숫자/schema/huge/deep JSON 일반 입력 오류 2 |
| B-P3-07 | P3 | FIXED — geo 예제/evidence 8건 |
| B-P1-08 | P1 | FIXED — diff 추가 내용 +++ 접두 위반 검출 |
| B-P1-09 | P1 | FIXED — CSS media 교집합·specificity/source order·string/comment/nested |
| B-P2-10 | P2 | FIXED — airport 현재 1.320934와 역사 1.15 분리 |
| B-P1-11 | P1 | FIXED — selector 대소문자·인용 내부 공백 |
| B-P1-12 | P1 | FIXED — 빈 selector 목록·root descendant 입력 오류 |
| B-P2-13 | P2 | FIXED — 파일 첫·3자 inline span 정상 제외 |

## 실행 명령·결과

전체 시험과 tracked-file 정적 gate는 후보를 OS 임시 폴더에 복사하고 독립 Git 저장소에 경로별 stage한 뒤 GIT_* 환경변수를 제거해 실행했다. source Git 설정을 상속·변경하지 않았다. focused 시험과 CLI는 후보 코드를 읽고 임시 fixture만 생성했다. 이전 raw 결과를 재사용하지 않았다.

| 명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p "test_*.py" | 288/288 통과, skip 0, 108.446초 | 288 수집, 285 실행 통과·skip 3, 25.579초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v | 50/50 통과, 25.857초 | 50/50 통과, 11.212초 |
| 별칭 focused unittest discover -s tests -p test_check_aliases.py | 35/35 통과 | 35 수집, 34 실행 통과·skip 1 |
| tools/validate_plan.py | task 106개, 오류 0 | 동일 |
| tools/validate_document_links.py | 문서 439개·대상 2418개, 오류 0 | 동일 |
| tools/check_spdx.py | 파일 56개, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 파일 571개, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 파일 571개, 발견 0 | 동일 |
| tools/check_versions.py --self-check | exit 0, 소비자 검사 아님 명시 | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report mode exit 0, 12건 | 동일 |
| git diff --check a7814d747d2740efd6aa0e27dff1441923d0c1e5 73b9cf68788066742e8df99dfad2433cbe6bf5fc | exit 0 | exit 0 |

모든 Python 도구는 해당 OS의 -B -X utf8로 실행했다. 전체 시험의 -v만 출력량을 줄이려고 생략했다. WSL Git diff는 --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post16-b 옵션을 명시했으며 core.worktree 설정은 변경하지 않았다.

후보 밖 probe 명령: Windows는 py -3.14 -B -X utf8 .git/codex-audit/<script> F:/dev/kor-travel-common-wt/review-t103-post16-b, WSL은 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/<script> /mnt/f/dev/kor-travel-common-wt/review-t103-post16-b다.

- t103-post9-b-corpus.py: 기존 9개 자체 probe, 관찰 105행. 두 OS JSON 전체 동일, marker/traceback true 없음. root/symlink·모든 출력 채널 redaction·baseline/JSON/argparse/diff +++·CSS cascade/media/nested/string/selector·4앱 예제·ESM/배열/삼항/tag/다중행/blockquote JSX·fence·문서 span을 포함한다.
- t103-post15-b-late-corpus.py: 자체 post9/10/11/12/13/14 및 smoke/media probe, 관찰 140행. 두 OS JSON 전체 동일. 미종결 1/2자·문단·blockquote/CRLF/backslash·CSS comment-gap·직접/단항/void/논리/숫자/regex/소수/나눗셈/XOR/Unicode/escape/ZWNJ/ZWJ·정상 닫힌 span·Other_ID를 재현했다.
- t103-post15-b-new.py: async 단순/주석/구조분해 3종, 추가 Other_ID 3종, U+11F02/U+2EBF0의 32회 CLI·8회 Node 실행. 모두 opener 0/1/2에서 P8, 정상 인용은 0건. 실측 Python Unicode DB Windows 16.0.0/WSL 14.0.0에서도 이번 결과는 일치한다.
- t103-post15-b-space.py: FEFF 선행/식별자 후행의 8회 CLI·2회 Node 실행. 두 OS 모두 opener 0/1/2에서 P8, 정상 인용 제외.
- t103-post16-b-new.py: LF/CR/U+2028/U+2029의 20회 CLI·4회 Node 실행. 새 B-P1-14를 위 표대로 재현했다.
- canonical 27쌍, UX report 12건, airport 1.3209340364487114. 지원 dark media는 모드별 적용·배제, not/width 복합 조건은 입력 오류 2.
- probe 관찰 행과 unittest 건수를 합쳐 시험 수를 부풀리지 않았다.

현재 task/resume는 IN_PROGRESS·리뷰/PR/CI/merge 잔여로 일치한다. airport 수용 기준/evidence, GPL-3.0-or-later, common 예제와 소비자 baseline 외부 task 경계는 이번 delta에서 불변이다. T-010 workflow는 후행이며 소비자·registry gate를 이번 완료로 표시하지 않는다.

## NOT_RUN·한계

- **NOT_RUN Windows Python 3.11**: py -0p는 3.14/3.10만 제공한다.
- WSL skip 3은 Windows 8.3 전용 1개와 jsonschema 미설치 parity 2개다. find_spec("jsonschema")가 None임을 확인했고 skip을 통과 건수에 포함하지 않았다.
- **NOT_RUN exact candidate 원격 CI 독립 조회**, workflow dispatch, 소비자 build/e2e, npm/PyPI registry·게시. 로컬 성공을 외부 gate의 성공으로 계산하지 않는다.
- **NOT_RUN MDX 컴파일러·브라우저 통합 실행**. Node v25.9.0(Windows)/v22.22.2(WSL) 스텁 실행과 실제 CLI 결과를 구분했다.
- JSX 문맥/template 보간의 LF 전용 코드는 직접 확인했지만 새 U+2028/U+2029 probe는 plain TS·MDX 표현식까지 실행했다. 해당 추가 문맥의 새 직접 반례는 미실행이다.
- 상대 reviewer 결과·미확정 raw를 읽지 않았다. 이후 후보의 수정 여부와 배포 가능성을 추정하지 않는다.
