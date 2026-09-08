# T-103 수정 후 18 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post18-20260908T131910+0900`.
- 판정: **NO-GO**. 누적 16개 중 15개 FIXED, `A-P1-16`(P1)은 **PARTIALLY_FIXED / OPEN**. U+2028/U+2029 원 반례는 해결됐지만 단독 CR 입력에서 같은 추가 행 판정 결함이 남는다. 신규 ID 및 신규 P0/P2/P3 0개.
- 제품 후보: commit `31ad7a5876ff0d5714d4094cb4a402718d02a33f`, tree `60bbe9546e1561aa5aee4f0bfbdd834fdd9cf58c`.
- 직전 제품 후보: `34c0abfbdf695258d53a1015ff4b73926d1ebcd1`. 구현·시험 delta인 `tools/ux_lint.py`, `tests/test_ux_lint.py` 전체를 읽었다. 나머지 delta는 이전 manifest·원본 evidence이며 상대 raw 본문을 열지 않았다.
- 공통 manifest: commit `64ad46575aee5d4a3dcc07e23512f91de4129694`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-18-manifest.md`를 `git show`로 읽었다.
- 격리: 새 detached checkout `F:/dev/kor-travel-common-wt/review-t103-post18-a`. 시작 2026-09-08 13:19:10.384 KST에 위 HEAD/tree 및 clean을 직접 확인했다. 직전 제품 반례 대조 후 제품 검토 종료·원본 생성 직전인 13:24:48.059 KST에도 동일 HEAD/tree 및 clean을 확인했다.
- 후보·manifest·소비자·Git config는 수정하지 않았다. 상대의 이번 결과·미확정 원본·과거 상대 raw를 읽지 않았다. 이 원본 한 파일만 별도 커밋하며 제품 검토 종료 SHA와 evidence commit SHA는 구분한다.

## 요청과 실제 범위

Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate 및 누적 CSS/JSON/redaction/diff/symlink/airport corpus를 실행했다. U+2028/U+2029 문자열의 가짜 `@@` hunk, `--base` 신규 P8 line 2, LF 대조, ESM·Unicode·FEFF·async·주석 경계를 직접 재현했다. 후보 source/시험 delta와 T-103·UX-G9의 추가 행 fail 계약을 직접 대조했다.

## A-P1-16 — P1 / PARTIALLY_FIXED / OPEN

**단독 CR을 자동 LF로 바꾸는 입력 처리 때문에 신규 위반이 기존 행으로 판정된다.**

- 위치: `tools/ux_lint.py:673`의 `Path.read_text`, 699행의 `subprocess.run(..., text=True)`, 752행의 untracked 입력 읽기, 760행의 `output.split("\n")` 및 hunk 처리.
- 수정 확인: U+2028/U+2029 뒤에 가짜 `@@ -0,0 +99,1 @@` 문자열이 있는 원 반례는 양 OS 모두 P8 line 2 / `added: true` / `fail: true` / exit 1이다. literal escape 대조도 정상이다.
- 잔여 원인: 소스 `read_text`와 Git subprocess의 text 모드는 단독 CR을 LF로 자동 변환한다. 이후 `split("\n")`로만 분리해도 이미 Git의 물리 LF 경계가 바뀐 상태다. 소스의 LF 기준 2행에 있는 호출은 scan 결과에서 3행으로 이동한다. diff의 추가 행 집합과 불일치하며, CR 뒤 가짜 hunk까지 있으면 header로 재해석된다.
- 범위: 같은 바이트 fixture를 직전 제품 `34c0abf`의 작업 트리에 있는 도구로도 양 OS 실행했다. 단독 CR의 동일 실패를 확인했다. 이번 수정이 도입한 회귀라고 주장하지 않으며, 원 finding의 줄 경계 보존 수용 기준이 부분적으로만 충족됐다고 판정한다.

임시 Git 저장소에 `case.ts`를 아래 두 행으로 커밋한다.

```typescript
const text = "old";
const safe = 1;
```

그 뒤 아래 Python으로 같은 파일에 쓴다. 실제 CR 바이트를 보존하려고 `write_bytes`를 사용한다.

```python
body = 'const text = `a\rb`;\nwindow.confirm("x");\n'
fixture.write_bytes(body.encode('utf-8'))
```

`b`를 `@@ -0,0 +99,1 @@`로 바꾼 가짜 hunk 변형도 같은 실패다. 명령은 임시 root에서 `python -B -X utf8 <후보>/tools/ux_lint.py --root <임시-root> --base <fixture-commit> --fail-new --json`이다.

| template 내부 구분자 | 가짜 hunk 없음 / 있음 | 양 OS 실제 결과 | 기대 |
|---|---|---|---|
| 실제 U+2028 | 두 경우 모두 | exit 1, P8 line 2, added/fail true | 정상 |
| 실제 U+2029 | 두 경우 모두 | exit 1, P8 line 2, added/fail true | 정상 |
| LF | 두 경우 모두 | exit 1, P8 line 3, added/fail true | 정상 |
| CRLF | 두 경우 모두 | exit 1, P8 line 3, added/fail true | 정상 |
| **단독 CR** | **두 경우 모두** | **exit 0, PASS, fail_count 0; P8 line 3, added/fail false** | **새 호출이므로 exit 1; Git의 LF 행을 따를 때 line 2** |

잔여 두 경우의 finding은 `file: case.ts`, `column: 1`, `pattern: P8`, `baseline: 0`, `exempt: false`다. Node `v25.9.0`의 `new Function`으로 단독 CR이 있는 위 template 소스를 평가해 문법 승인과 로컬 `window.confirm` stub 호출 1회를 확인했다. 금지 호출이 주석이나 단순 인용으로 숨은 입력이 아니다.

- 영향: 유효한 JavaScript template의 단독 CR만으로 실제 신규 P8을 추가 행 fail 대상에서 제외한다. 전체 report에서 위반을 보여도 CLI/CI는 PASS이므로 원 P1을 유지한다.
- 수정 방향: Git 출력과 소스 입력을 읽는 단계부터 원래 LF 경계를 보존하고, 동일 좌표계로 report·tracked diff·untracked 행을 계산한다. `splitlines` 교체뿐 아니라 universal newline 변환까지 처리해야 한다. 줄 주석의 ECMAScript CR/LF/U+2028/U+2029 종료 의미는 유지한다.
- 수용 기준: 위 열 가지 template 대조와 기존 double-quoted LS/PS 네 대조 모두 신규 P8 1개 / exit 1이어야 한다. CR에서 가짜 header 유무와 무관하게 추가 행으로 판정하며, LF·CRLF·ESM·baseline 앞 삽입·실제 `+++`·인용 파일명 회귀를 유지한다.

정확한 helper는 후보 밖 `F:/dev/kor-travel-common/.git/codex-audit/t103-post18-diff-a.py`이며 SHA256은 `F448020147EBE83F356ECD7A18E97C25E5C1820F1408DDDF5935134929187270`이다. `python -B -X utf8 <helper> <후보-worktree>`로 Windows에서 실행하고 WSL은 `/mnt/f/...` 경로 및 `uv run --no-project --python 3.11` 접두로 실행했다. 같은 명령의 후보 경로를 `review-t103-post17-a`로 바꿔 직전 제품도 대조했다. fixture의 `git init`, 경로를 명시한 `git add`, `git -c user.name=Review fixture -c user.email=fixture@example.invalid commit`은 임시 저장소만 사용하며 source config를 바꾸지 않는다.

## 누적 disposition

| 원 ID | 원 심각도 | 이번 판정과 실제 대조 |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS root/dark·specificity·media 교집합·unsupported selector·빈 목록·descendant·comment-gap 회귀 유지. |
| A-P1-02 | P1 | FIXED — OKLCH chroma `25%`와 `0.1` RGB 일치. |
| A-P1-03 | P1 | FIXED — 흰색 20% / 검정 sRGB source-over 대비 1.6620953314177012 및 `#333` 대조 일치. |
| A-P1-04 | P1 | FIXED — baseline 앞 신규 행 fail, 기존 행 면제 유지. |
| A-P1-05 | P1 | FIXED — 같은 basename 외부 임시 Git root 판정 유지. |
| A-P2-06 | P2 | FIXED — 누적 MDX span/fence/JSX/template/ESM, Unicode 일반·escape·Other_ID·Cn·FEFF·async 양성 및 닫힌 인용 음성 대조 유지. |
| A-P2-07 | P2 | FIXED — 옵션 형태 base 일반 오류 2. |
| A-P2-08 | P2 | FIXED — WSL quoting/tab 파일명 추가 행 탐지. Windows tab 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED — NaN/Infinity/음수/bool/중복·400/5000자리 JSON 일반 오류 2. |
| A-P2-10 | P2 | FIXED — 합성 marker의 오류·JSON·summary·argparse 비공개 유지. |
| A-P2-11 | P2 | FIXED — muted 읽기 표면 추가 시 31쌍과 미달 확인. |
| A-P3-12 | P3 | FIXED — geo 미달 8개, airport 현재 1.32와 과거 조사 1.15의 문서 경계 유지. |
| A-P1-13 | P1 | FIXED — 실제 `++counter;` 추가 행에 따른 diff `+++` 후속 신규 P6 탐지. |
| A-P2-14 | P2 | FIXED — 양 OS self-symlink root 일반 오류 2/traceback 없음. Windows 직접 링크 probe 포함. |
| A-P2-15 | P2 | FIXED — 깊이 2000 JSON에서 두 도구 모두 일반 오류 2/traceback 없음. |
| A-P1-16 | P1 | PARTIALLY_FIXED / OPEN — LS/PS 원 반례 해결, 단독 CR의 신규 행 false PASS 잔여. |

## 실행 명령과 결과

Windows Python 3.14.3, WSL uv Python 3.11.15를 사용했다. WSL 전체 시험에만 `--with jsonschema`를 추가했다. 아래 명령은 detached 후보에서 실행했고 WSL은 `uv run --no-project --python 3.11 python -B -X utf8`를 사용한다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 290 실행/290 통과/skip 0, 113.572초 | 290 실행/289 통과/skip 1, 67.658초; skip은 Windows 8.3 전용 |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 52개, exit 0 | 52개, exit 0, 10.370초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 445/대상 2420/오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106/오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 파일 56/오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 파일 577/발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 파일 577/발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1/오류 0 | 동일 |
| `git diff --check 6a274c1 31ad7a5876ff0d5714d4094cb4a402718d02a33f` | exit 0 | exit 0 |

직접 CLI corpus는 자신의 후보 밖 `t103-post17-reviewer-a-probe.py`, `t103-post17-diff-a.py`에 이번 후보 절대 경로를 전달해 양 OS 실행했다. 과거 raw 본문을 읽지 않고 자신의 재현 프로그램만 재사용했다. 정본 light/dark 27쌍 미달 0, 4앱 light 예제 미달 4/8/8/4 및 등록 baseline의 exit 0, UX fixture 전체 report 12개/exit 0을 확인했다. report 기본 exit 0을 미달·위반 없음으로 세지 않는다. LF/CR/LS/PS 각각 plain TS/MDX, 미종결 1·2자 span 뒤 expression, template 보간, 중첩 JSX 및 주석·닫힌 span 음성의 36개 결과도 양 OS 기대대로다. diff 잔여는 앞 절에 별도로 기록했다.

WSL 정적 gate의 최초 호출은 셸 전달 중 loop 변수가 소실되어 문서·plan·SPDX 3개가 실행되지 않았다. 이를 성공으로 집계하지 않았고 변수 없는 개별 명령으로 전체 정적 gate를 다시 실행하여 위 결과를 얻었다. 재실행은 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post18-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post18-a`를 해당 프로세스에만 설정했다. 시험/probe에는 Git 환경을 주입하지 않았다. Git config는 수정하지 않았다.

`gh run list --commit 31ad7a5876ff0d5714d4094cb4a402718d02a33f --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI 34186506842](https://github.com/digitie/kor-travel-common/actions/runs/34186506842)의 exact head 및 **cancelled**를 관찰했다. 로컬 성공을 이 후보 CI 성공으로 표시하지 않는다.

## 미실행과 종료

- NOT_RUN: Windows Python 3.11(런타임 부재), 소비자 build/e2e·adoption, registry 조회·게시, workflow dispatch. 후속 소비자 gate를 이 결과로 닫지 않는다.
- NOT_RUN: 실제 브라우저/MDX compiler 렌더링. Node 문법·stub 확인은 소비자 빌드 결과가 아니다.
- 원본 추가 후 경로를 명시해 stage하고 전체 staged diff·diff check·문서 링크·staged secret/redaction gate를 확인해 원본만 커밋한다. 후보·manifest·기존 evidence는 변경하지 않는다.
