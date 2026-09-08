<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-15 독립 적대적 리뷰 B 원본

- 실행 ID: T103-POST15-B-20260908-124149.
- 판정: **NO-GO**. 누적 13개 ID 중 12개 FIXED, **B-P1-03 OPEN**. 새 ID 0개; 현재 잔여 P0 0 / P1 1 / P2 0 / P3 0.
- 시작: 2026-09-08T12:41:49.8199626+09:00. 제품 검토 종료: 2026-09-08T12:45:03.6572839+09:00.
- 제품 시작·종료 SHA: 210c2de324b18fcaa4e3f8b18fe5965226cb79d7.
- 제품 시작·종료 tree: 58418960efa7e486d60fa95d9a3e7f335e0ad74b.
- 새 detached worktree: F:/dev/kor-travel-common-wt/review-t103-post15-b. 시작·종료 git status --porcelain=v1 출력 없음.
- manifest: e72b7466d02e2fcfe6f9811fd3ca4cfa4478fd60의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-15-manifest.md를 git show로 읽음. blob SHA256: dd8442a90df2f638d9973ac97efdb2361d1887bec0eb583ff8d2f8687dc48042.
- delta: 0b2330e93d2b05a954593c82ef0ea230821adf28..210c2de324b18fcaa4e3f8b18fe5965226cb79d7. 제품 수정은 tools/ux_lint.py와 tests/test_ux_lint.py뿐. 다른 3개는 이전 manifest/raw 경로이며 상대·과거 raw 본문을 읽지 않았다.
- source .git/config 시작·종료 SHA256 동일: 0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B.
- 후보·manifest·소비자·Git 설정 수정 없음. 제품 검토 종료 후 이 원본 한 파일만 별도 branch에 커밋하며 push하지 않는다.

## 전달 요청 원문

> T-103 post-fix-15 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit 210c2de324b18fcaa4e3f8b18fe5965226cb79d7, tree 58418960efa7e486d60fa95d9a3e7f335e0ad74b의 detached clean checkout으로 고정합니다. 공통 manifest는 commit e72b746의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-15-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw는 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate와 누적 corpus를 독립 재현하고, 특히 post-fix-14의 ℘/Ⅳ/ͺ/a·/a·/async x => 표현식 및 1·2자 미종결 span과 정상 닫힌/개방 대조를 검증하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-15-reviewer-b.md에 기록하고 raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정·커밋·푸시하지 마세요. 상대 원본을 읽지 않은 상태로 완료 메시지에 commit/hash/verdict를 알려 주세요.

## B-P1-03 — Python Unicode 데이터와 공백 판정으로 실행 표현식이 가려짐

**P1, OPEN, 수정 필요.** [ux_lint.py](../../../../tools/ux_lint.py) 138~160행(_skip_mdx_expression_leading), 180~201행(식별자 판정), 223~254행(표현식 시작 판정), 275행 이후(미종결 span 마스킹). 계약은 [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md) 22행의 P8 실행 코드 검사와 수용 기준의 Linux·Windows 결과 일치다.

기존 post-fix-14의 ℘/Ⅳ/U+037A/a·/a·는 모두 FIXED다. async arrow, 주석 뒤 매개변수, 구조분해 매개변수 대조도 검출된다. 그러나 미종결 span 뒤에서 인식하지 못한 표현식을 지워 성공시키는 기존 B-P1-03의 경계가 두 형태로 남았다. 같은 마스킹 finding이므로 새 ID를 만들지 않았다.

### 반례 1: 실행 Python에 따라 신규 Unicode 이름이 통과함

식별자를 chr(0x11F02) 또는 chr(0x2EBF0)로 생성하여 선언과 사용을 일치시켰다.

~~~~python
ident = chr(0x11F02)  # 두 번째 반례는 0x2EBF0
source = ("export const " + ident + " = 1\n\nExample " +
          chr(96) + " unmatched {" + ident + ' && window.confirm("확인")}\n')
~~~~

명령: python -B -X utf8 <후보>/tools/ux_lint.py --root <Page.mdx 임시 폴더> --fail-new --json.

| 대조 | Windows Python 3.14.3 | WSL Python 3.11.15 | 기대 |
|---|---|---|---|
| 미종결 1자 span 뒤 각 이름 | exit 1, FAIL, P8 1건 | **exit 0, PASS, 0건** | P8 1건 |
| 미종결 2자 span 뒤 각 이름 | exit 1, FAIL, P8 1건 | **exit 0, PASS, 0건** | P8 1건 |
| opener 없음 | exit 1, P8 1건 | exit 1, P8 1건 | P8 1건 |
| 정상 닫힌 span | exit 0, 0건 | exit 0, 0건 | 인용 제외 |

실측 unicodedata.unidata_version은 Windows 16.0.0, WSL 14.0.0이다. _is_mdx_identifier_start가 실행 Python의 category/isidentifier에 의존하므로 오래된 Unicode 데이터에서 이름을 놓친다. 이것은 운영체제 자체가 아니라 지원 Python 런타임에 따라 달라지는 문제다. 두 Node 런타임에서 해당 선언·표현식은 모두 exit 0, confirm 스텁 호출 1회였다.

### 반례 2: JavaScript 공백 U+FEFF를 건너뛰지 못함

다음 두 표현식을 각각 파일에 삽입했다. 눈에 보이지 않는 문자를 보고서에 숨기지 않고 생성식으로 적는다.

~~~~python
expressions = [
    chr(0xFEFF) + 'window.confirm("확인")',
    'n' + chr(0xFEFF) + '&& window.confirm("확인")',
]
source = ('export const n=1\n\nExample ' + chr(96) +
          ' unmatched {' + expression + '}\n')
~~~~

두 OS 모두 미종결 1/2자 span에서는 **exit 0/PASS/0건**, opener 없는 대조는 exit 1/P8 1건, 정상 닫힌 span은 exit 0/0건이다. Node 양 OS에서 두 표현식 모두 정상 실행·confirm 스텁 1회 호출을 확인했다. _skip_mdx_expression_leading의 Python isspace는 이 JavaScript 공백을 인식하지 못하므로 첫 문자나 식별자 뒤 연산자 탐색이 실패한다.

확인한 JS 실행은 실제 대화상자 대신 다음 스텁을 사용했다. Unicode 이름 반례는 const n을 해당 이름으로 바꾸고, expression을 삽입했다.

~~~~javascript
let called = 0;
const window = {confirm() { called++; return true; }};
const n = 1;
// 이 위치에 각 expression을 삽입해 실행한다.
console.log(called);
~~~~

권고: 미종결 span에서 불완전한 JavaScript 어휘 판정에 실패했다는 이유로 나머지를 인용 처리하지 않는다. 런타임 Unicode 버전과 공백 정의 차이가 조용한 성공으로 이어지지 않도록 마스킹 경계를 단순화하거나 명시적 입력 오류로 처리한다. 식별자와 공백 파서를 유지한다면 지원 Unicode 기준을 고정하고 두 Python 버전에서 같은 입력 corpus를 비교해야 한다. 신규 이름 2종과 FEFF 선행/식별자 후행 각각 opener 0/1/2 및 정상 인용을 시험한다.

## 누적 disposition

| ID | 원 심각도 | 현재 판정·재현 |
|---|---|---|
| B-P1-01 | P1 | FIXED — 외부 root/CWD·Git diff 범위 |
| B-P1-02 | P1 | FIXED — 앞삽입 위반이 baseline 건수로 면제되지 않음 |
| B-P1-03 | P1 | **OPEN** — 기존 다섯 Unicode·async는 FIXED, 이번 두 경계 잔여 |
| B-P1-04 | P1 | FIXED — path/값·stdout/JSON/Markdown/step summary redaction |
| B-P2-05 | P2 | FIXED — 명시적 muted 읽기 표면 4쌍 추가 |
| B-P2-06 | P2 | FIXED — 숫자/schema/huge/deep JSON 일반 입력 오류 2 |
| B-P3-07 | P3 | FIXED — geo 예제/evidence 8건 |
| B-P1-08 | P1 | FIXED — diff 추가 내용 +++ 접두 위반 검출 |
| B-P1-09 | P1 | FIXED — CSS media 교집합·specificity/source order·string/comment/nested |
| B-P2-10 | P2 | FIXED — airport 현재 1.320934와 역사 1.15 분리 |
| B-P1-11 | P1 | FIXED — selector 대소문자·인용 내부 공백 |
| B-P1-12 | P1 | FIXED — 빈 selector 목록·root descendant 입력 오류 |
| B-P2-13 | P2 | FIXED — 파일 첫·3자 inline span 정상 제외 |

## 실행 명령·결과

전체 시험과 tracked-file 정적 gate는 후보를 OS 임시 폴더에 복사하고 별도 Git 저장소에 경로별 stage한 뒤 GIT_* 환경변수를 제거해 실행했다. source Git 설정을 상속·변경하지 않았다. focused 시험과 직접 CLI는 후보 코드를 읽고 임시 fixture만 생성했다. 이전 raw 결과를 재사용하지 않았다.

| 명령 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| python -B -X utf8 -m unittest discover -s tests -p "test_*.py" | 288/288 통과, skip 0, 100.205초 | 288 수집, 285 실행 통과·skip 3, 25.414초 |
| python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v | 50/50 통과, 21.848초 | 50/50 통과, 10.061초 |
| 별칭 focused unittest discover -s tests -p test_check_aliases.py | 35/35 통과 | 35 수집, 34 실행 통과·skip 1 |
| tools/validate_plan.py | task 106개, 오류 0 | 동일 |
| tools/validate_document_links.py | 문서 436개·대상 2416개, 오류 0 | 동일 |
| tools/check_spdx.py | 파일 56개, 오류 0 | 동일 |
| tools/scan_secrets.py --all | 파일 568개, 발견 0 | 동일 |
| tools/check_prod_redaction.py --all | 파일 568개, 발견 0 | 동일 |
| tools/check_versions.py --self-check | exit 0, 소비자 검사 아님 명시 | 동일 |
| tools/check_aliases.py packages/tokens/aliases | CSS 1개, 오류 0 | 동일 |
| tools/kt_contrast.py packages/tokens/tokens.css --json | exit 0, 27쌍 | 동일 |
| tools/ux_lint.py --root tests/fixtures/ux --json | report mode exit 0, 12건 | 동일 |
| git diff --check 9f7dcf7c07c9dc964a91289ce4c5459190f12784 210c2de324b18fcaa4e3f8b18fe5965226cb79d7 | exit 0 | exit 0 |

모든 Python 도구는 해당 OS의 -B -X utf8로 실행했다. 전체 시험은 출력량만 줄이려고 -v를 생략했다. WSL Git diff는 명령에 --git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post15-b를 명시했으며 core.worktree 설정은 변경하지 않았다.

후보 밖 직접 probe 명령은 Windows의 py -3.14 -B -X utf8 .git/codex-audit/<script> F:/dev/kor-travel-common-wt/review-t103-post15-b, WSL의 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/<script> /mnt/f/dev/kor-travel-common-wt/review-t103-post15-b다.

- t103-post9-b-corpus.py: 기존 9개 자체 probe, 관찰 105행. 두 OS JSON 전체 동일, marker/traceback true 없음. root/symlink·모든 출력 채널 redaction·baseline/JSON/argparse/diff +++·CSS cascade/media/nested/string/selector·4앱 예제·ESM/배열/삼항/tag/다중행/blockquote JSX·fence·문서 span을 재현했다.
- t103-post15-b-late-corpus.py: 자체 post9/10/11/12/13/14 및 smoke/media probe를 실행한 관찰 140행. 두 OS JSON 전체 동일. 미종결 1/2자·같은/다른 문단·blockquote/CRLF/backslash·CSS comment-gap·직접/단항/void/논리/숫자/regex/소수/나눗셈/XOR/Unicode/escape/ZWNJ/ZWJ·정상 닫힌 span·다섯 post14 이름을 포함한다.
- t103-post15-b-new.py: async 단순/주석/구조분해 3종, 추가 Other_ID 3종, 신규 Unicode 이름 2종의 32회 CLI·8회 Node 스텁 실행. 기존·추가 Other_ID는 정상 검출되며 신규 이름 2종만 위 표처럼 Python 버전별 차이가 난다.
- t103-post15-b-space.py: FEFF 선행/식별자 후행의 8회 CLI·2회 Node 실행. 위 반례 2 결과를 양 OS에서 확인했다.
- canonical 27쌍·UX report 12건·airport 1.3209340364487114 확인. 지원 dark media는 light/dark별 적용·배제되고 not/width 복합 조건은 입력 오류 2다.
- 관찰 행과 unittest 건수를 합쳐 시험 수를 부풀리지 않았다.

현재 T-103과 resume는 IN_PROGRESS·리뷰/PR/CI/merge 잔여로 일치한다. airport 수용 기준/evidence, GPL-3.0-or-later, common 예제와 소비자 baseline 외부 task 경계는 이번 delta에서 불변이다. T-010 재사용 workflow는 후행이며 소비자·registry gate를 이번 완료로 표시하지 않는다.

## NOT_RUN·한계

- **NOT_RUN Windows Python 3.11**: py -0p는 3.14/3.10만 제공한다.
- WSL skip 3은 Windows 8.3 전용 1개와 jsonschema 미설치 parity 2개다. find_spec("jsonschema")가 None임을 직접 확인했다. skip을 성공 건수에 포함하지 않았다.
- **NOT_RUN exact candidate 원격 CI 독립 조회**, workflow dispatch, 소비자 build/e2e, npm/PyPI registry·게시. 로컬 성공을 이 gate의 성공으로 계산하지 않는다.
- **NOT_RUN MDX 컴파일러·브라우저 통합 실행**. Node v25.9.0(Windows)/v22.22.2(WSL) 스텁 실행과 CLI 결과를 분리해 기록했다.
- 상대 reviewer 결과·미확정 raw를 읽지 않았다. 이후 후보의 수정 여부와 배포 가능성을 추정하지 않는다.
