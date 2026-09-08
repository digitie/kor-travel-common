<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# T-103 post-fix-13 독립 적대적 리뷰 B 원본

- 실행 ID: `T103-POST13-B-20260908-121334`
- 판정: **NO-GO**. 누적 finding 13개 중 12개 FIXED, **B-P1-03 OPEN**. 새 ID 0개; 현재 잔여 P0 0 / P1 1 / P2 0 / P3 0.
- 시작: 2026-09-08T12:13:34.3952201+09:00. 제품 검토 종료: 2026-09-08T12:19:34.9705172+09:00.
- 제품 시작·종료 SHA: `e8137efd8f4b53465b8cf9a1d333127e4186b73c`.
- 제품 시작·종료 tree: `091274064a82897f6f00ec8f3db2a8776379e13d`.
- 격리: `F:/dev/kor-travel-common-wt/review-t103-post13-b`의 새 detached worktree. 시작·종료 `git status --porcelain=v1` 출력 없음.
- manifest: commit `6cb95d01de6cd4d7f8274c38854e119f1e5395e7`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-13-manifest.md`를 `git show`로 읽음. 원문 blob SHA256: `236c74a358aacb59414938485c2a53e0db1dd95b582bb8c49699238cc5728494`.
- 수정 delta: `386d815f54b79102954a695b0d65dda093bdfbec..e8137efd8f4b53465b8cf9a1d333127e4186b73c`. 제품 수정은 `tools/ux_lint.py`·`tests/test_ux_lint.py`; 나머지 3개는 이전 manifest/raw 경로다. 상대·과거 raw 본문은 읽지 않았다.
- source `.git/config` 시작·종료 SHA256 동일: `0A0F849E7874CF0A25926856F9D2E381CCBF4C2DCB5999869C57B86E0F5BEB5B`. 설정·제품·소비자 파일 수정 및 push 없음. 제품 검토 종료 후 이 원본 파일만 별도 branch에서 커밋한다.

## 전달 요청 원문

> T-103 post-fix-13 독립 적대적 리뷰를 시작해 주세요. 제품 candidate는 commit e8137efd8f4b53465b8cf9a1d333127e4186b73c, tree 091274064a82897f6f00ec8f3db2a8776379e13d로 detached clean checkout하고, 공통 manifest는 commit 6cb95d0의 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-13-manifest.md를 git show로 읽으세요. 상대 reviewer의 이번 raw/결과나 미확정 raw를 읽지 말고 후보·manifest·소비자 저장소·git config를 수정하지 마세요. Windows Python 3.14와 WSL Python 3.11에서 full/focused/static gate와 누적 CSS/JSON/redaction/diff/symlink/airport corpus, 특히 미종결 1/2자 Markdown span 뒤 직접/단항/키워드/논리/숫자/정규식(/x/)/소수(.5)/나눗셈·xor/유니코드 식별자/주석 선행 MDX expression, 여러 줄 JSX expression 및 정상 닫힌 span 음성 대조를 독립 재현하세요. Windows Python 3.11은 NOT_RUN으로 명시하세요. 새 원본만 docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-13-reviewer-b.md에 기록하고 immutable raw-only commit/SHA256/HEAD·tree·clean·명령·verdict를 남겨 주세요. 제품 후보는 수정/커밋/푸시하지 마세요. PASS/NO-GO와 모든 finding ID/disposition을 명확히 보고하고 완료 후 메시지를 주세요.

## B-P1-03 — 유효한 JavaScript 식별자를 시작으로 하는 MDX 실행 표현식이 가려짐

**P1, OPEN, 수정 필요.** 위치: [ux_lint.py](../../../../tools/ux_lint.py) 38~41행, 154~177행, 199~219행. 계약: [T-103](../../../tasks/T-103-kt-contrast-ux-lint.md) 22행의 실행 코드 P8 검사·백틱 인용 제외.

`_MDX_IDENTIFIER`는 Python `\w`를 JavaScript 식별자 연속 문자로 사용하고, 첫 문자는 `isalpha` 등으로 분기한다. 따라서 escape로 작성한 식별자 시작, 결합문자 및 ZWNJ를 포함한 합법적인 식별자를 인식하지 못한다. 미종결 백틱 뒤의 실행 표현식 재개점을 찾지 못해 문단 끝까지 가린다. P8이 있는 실행 코드를 신규 위반 0건으로 통과시킨다. 기존 B-P1-03의 같은 마스킹 원인이므로 새 ID를 추가하지 않았다.

최소 입력 `Page.mdx`는 다음과 같다. 파일에서 `\u006e`는 역슬래시와 ASCII 문자로 보존한다.

~~~~mdx
export const n = 1

Example ` unmatched {\u006e && window.confirm("확인")}
~~~~

명령: `python -B -X utf8 <후보>/tools/ux_lint.py --root <Page.mdx가 있는 임시 폴더> --fail-new --json`.

- 기대: exit 1, P8 1건. 닫는 백틱이 없어 인용 span이 성립하지 않으며, MDX expression은 실행 코드다.
- 실제 Windows 3.14·WSL 3.11: **exit 0, status PASS, findings 0**.
- 미종결 백틱을 2개로 바꿔도 동일하다. 백틱 opener만 제거하면 exit 1/P8 1건이다.
- 정상 닫힌 1자 span으로 표현식을 감싸면 exit 0/0건으로 제외된다.
- 선언 및 사용 이름을 `"a" + chr(0x0301)` 또는 `"a" + chr(0x200C)`로 바꾼 두 반례도 동일하다. 보충 평면 문자 `chr(0x10400)` 이름은 정상 검출되어 양성 대조가 된다.
- Windows Node v25.9.0·WSL Node v22.22.2에서 네 표현식 모두 exit 0, confirm 스텁 호출 1회를 직접 확인했다. MDX 컴파일러 실행과 이 JS 실행 확인은 구분한다.

후보 밖 Python probe의 핵심은 다음과 같다. 각 플랫폼의 `sys.executable`로 동일 CLI를 실행했다.

~~~~python
cases = {
    "escaped-name": ("n", r"\u006e"),
    "combining-name": ("a\u0301", "a\u0301"),
    "joiner-name": ("a\u200c", "a\u200c"),
    "astral-name": ("\U00010400", "\U00010400"),
}
for name, (decl, ident) in cases.items():
    expr = ident + ' && window.confirm("확인")'
    for run in (0, 1, 2, 3):
        body = "{" + expr + "}"
        tail = ("`" + body + "`" if run == 3 else
                ("`" * run + " unmatched " if run else "") + body)
        source = "export const " + decl + " = 1\n\nExample " + tail + "\n"
        (fixture / "Page.mdx").write_text(source, encoding="utf8")
        result = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(candidate / "tools/ux_lint.py"),
             "--root", str(fixture), "--fail-new", "--json"],
            cwd=fixture, env=isolated_env, capture_output=True, text=True, encoding="utf8")
~~~~

권고: 미종결 span의 나머지를 실행식 시작 문자 휴리스틱으로 지우는 방식을 제거하거나, JavaScript 식별자 escape 및 IdentifierPart 경계를 충분히 지원해 모르는 경계가 성공으로 사라지지 않게 한다. escape·결합문자·ZWNJ 각각 opener 0/1/2와 정상 닫힌 span 대조를 계약 시험에 추가한다. 실제 JS 표현식은 정상 코드이며 문법 오류 입력으로만 회피할 수 없다.

## 누적 disposition

| ID | 원 심각도 | 현재 판정·직접 재현 |
|---|---|---|
| B-P1-01 | P1 | FIXED — 외부 root에서 해당 Git diff 사용, CWD 대조 |
| B-P1-02 | P1 | FIXED — 앞삽입 신규 위반이 기존 baseline 건수로 면제되지 않음 |
| B-P1-03 | P1 | **OPEN** — 기존 직접/단항/void/논리/숫자/정규식/소수/나눗셈/XOR/한글/주석 선행은 FIXED; 위 식별자 세 경계가 남음 |
| B-P1-04 | P1 | FIXED — 입력 path/값·stdout/JSON/Markdown/step summary 원문 노출 없음 |
| B-P2-05 | P2 | FIXED — muted 읽기 표면은 명시 시 4쌍 추가 |
| B-P2-06 | P2 | FIXED — 잘못된 숫자·huge/deep JSON은 일반 입력 오류 2, traceback 없음 |
| B-P3-07 | P3 | FIXED — geo evidence 8건과 예제 결과 일치 |
| B-P1-08 | P1 | FIXED — diff 추가 내용의 `+++` 접두 위반 검출 |
| B-P1-09 | P1 | FIXED — media 교집합·specificity/source order·CSS string/comment 및 지원 밖 조건 오류 |
| B-P2-10 | P2 | FIXED — airport 현재 alpha 1.320934와 역사 1.15 분리 |
| B-P1-11 | P1 | FIXED — selector 값 대소문자·인용 내부 공백 보존 |
| B-P1-12 | P1 | FIXED — 빈 selector 항목·root descendant 입력 오류 2 |
| B-P2-13 | P2 | FIXED — 파일 첫 span·3자 inline 인용의 정상 제외 |

## 실제 검증과 명령

Windows는 Python 3.14.3, WSL은 uv Python 3.11.15다. 전체 시험·tracked-file 정적 gate는 후보를 OS 임시 디렉터리에 복사하여 새 Git 저장소에 파일을 경로별 stage한 후 실행했다. `GIT_*` 환경변수를 제거했으며 source Git 설정을 상속하거나 바꾸지 않았다. focused 시험 및 CLI probe는 후보 코드를 읽고 임시 fixture만 썼다.

| 명령·검증 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p "test_*.py"` | 287/287 통과, skip 0, 87.424초 | 287 수집, 284 실행 통과, skip 3, 26.569초 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v` | 49/49 통과, 13.310초 | 49/49 통과, 6.580초 |
| 별칭 focused `unittest discover -s tests -p test_check_aliases.py` | 35/35 통과 | 35 수집, 34 실행 통과, skip 1 |
| `tools/validate_plan.py` | task 106개, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 문서 430개·대상 2412개, 오류 0 | 동일 |
| `tools/check_spdx.py` | 파일 56개, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 562개, 발견 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 562개, 발견 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0, 소비자 검사 미실행 명시 | 동일 |
| `tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0 | 동일 |
| `tools/kt_contrast.py packages/tokens/tokens.css --json` | exit 0, 27쌍 | 동일 |
| `tools/ux_lint.py --root tests/fixtures/ux --json` | report mode exit 0, 12건 | 동일 |
| `git diff --check 081e89873deb13fe7853e31d30eac4ebf5e8a2c1 e8137efd8f4b53465b8cf9a1d333127e4186b73c` | exit 0 | exit 0 |

모든 Python 도구 명령은 해당 OS Python의 `-B -X utf8`로 실행했다. 전체 시험의 `-v`는 출력량만 줄이기 위해 생략했다. WSL Git diff는 Windows worktree 포인터를 재설정하지 않고 명령의 `--git-dir=/mnt/f/dev/kor-travel-common/.git --work-tree=/mnt/f/dev/kor-travel-common-wt/review-t103-post13-b`를 명시했다.

후보 밖 자체 probe 명령: Windows는 `py -3.14 -B -X utf8 .git/codex-audit/<script> F:/dev/kor-travel-common-wt/review-t103-post13-b`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/<script> /mnt/f/dev/kor-travel-common-wt/review-t103-post13-b`이다.

- `t103-post9-b-corpus.py`: 기존 9개 probe의 관찰 105행을 각 OS에서 다시 생성. Windows/WSL JSON 전체가 같고 marker/traceback true 없음. CSS cascade/media/nested/string/selector·baseline/schema/huge/deep JSON·argparse·root/symlink·출력 채널·diff `+++`·4앱 예제·ESM/배열/삼항/임의 tag/다중행·blockquote JSX/fence·문서 span 누적 반례를 포함한다.
- `t103-post9-b-new.py`: 21행. CSS comment-gap·같은 문단 미종결 1/2자 span/줄바꿈/빈 문단/blockquote/CRLF/backslash 대조.
- `t103-post10-b-new.py`: 7행. 미종결 span 뒤 직접 expression·여러 줄 JSX·정상 닫힌 span.
- `t103-post11-b-new.py`: 15행. 직접·단항 `!`·`void`·논리·숫자 표현식 각각 opener 0/1/2 모두 P8 검출.
- `t103-post12-b-new.py`: 21행. block/line comment·regex·소수·나눗셈·XOR·한글 이름 각각 opener 0/1/2 모두 P8 검출.
- `t103-post13-b-new.py`: 위 신규 식별자 반례 16회 CLI와 JS 스텁 실행 4회. OS 결과 동일; 세 이름×opener 1/2에서 실패를 통과로 판정한다.
- `t103-post3-b-smoke.py`: canonical 27쌍, UX report 12건, airport line 1.3209340364487114 대조.
- `t103-post1-b-media.py`: 8회. 지원 dark media는 light/dark 각각 적용·배제되고 `not`·width 복합 조건은 입력 오류 2.

probe 관찰 행과 unittest 건수는 합쳐 시험 수로 부풀리지 않았다. 실제 후보의 task 상태는 IN_PROGRESS다. GPL-3.0-or-later 고지, common 예제·도구 범위와 소비자 baseline 등록의 외부 task 경계는 유지된다. 정본에서 P8 면제를 새 식별자 문법까지 허용하지 않는다.

## 미실행·한계

- **NOT_RUN Windows Python 3.11**: `py -0p`는 3.14/3.10만 제공한다.
- WSL full 3 skip은 Windows 8.3 전용 1개와 `jsonschema` 미설치 parity 2개다. `find_spec("jsonschema")`가 None임을 확인했다. skip을 통과로 집계하지 않았다.
- **NOT_RUN 원격 exact candidate CI 독립 조회**, workflow dispatch, 소비자 빌드/e2e, npm/PyPI registry·게시. 로컬 성공을 원격 CI나 소비자 gate 성공으로 계산하지 않는다.
- **NOT_RUN MDX 컴파일러·브라우저 통합 실행**. CLI 결과와 JavaScript 표현식의 Node 실행은 직접 검증했다.
- 이 raw 확정 전에 상대 결과나 미확정 raw를 읽지 않았다. 작성자가 정한 후보를 수정하지 않았고 누적 corpus는 후보 코드로 재실행했다. 제품 전체의 무결점 또는 배포 준비를 주장하지 않는다.
