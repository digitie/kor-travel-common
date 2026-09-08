# T-103 수정 후 19 — Reviewer A 독립 원본

- 실행 ID: `reviewer_a-t103-post19-20260908T133235+0900`.
- 판정: **NO-GO**. `A-P1-16`은 FIXED. 원 `A-P2-06`(P2)은 단독 CR의 MDX 문법 처리 회귀로 **OPEN**이다. 누적 16개 중 15개 FIXED / 1개 OPEN이며 새 ID·신규 P0/P1/P3는 없다.
- 제품 후보 commit: `415984bf7cb450d44d7661424884d6641fef8309`; tree: `9c07d86aea28e130ad58b912d72ad99152795c31`.
- 직전 제품 후보: `31ad7a5876ff0d5714d4094cb4a402718d02a33f`. 구현·시험 delta인 `tools/ux_lint.py`, `tests/test_ux_lint.py` 전체를 읽었다. AGENTS·문서 라우터·resume·T-103·standards·runbooks는 직전 후보와 동일함을 확인해 이미 읽은 계약을 재사용했다.
- 공통 manifest: commit `a0d12d2299e3cb4e55ea560e6c24ea5aff3167c7`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-19-manifest.md`를 `git show`로 읽었다.
- 격리: 새 detached checkout `F:/dev/kor-travel-common-wt/review-t103-post19-a`. 시작 2026-09-08 13:32:35.645 KST 및 제품 검토 종료 13:37:13.225 KST의 HEAD/tree는 위 후보와 같고, 두 시점의 `git status --porcelain=v1`은 빈 출력이었다.
- 제품·manifest·소비자·Git config를 변경하지 않았다. 상대 reviewer의 이번 결과·미확정 원본·과거 상대 raw를 읽지 않았다. 새 원본 한 파일만 별도 commit하며 raw commit과 제품 후보를 구분한다.

## 요청과 범위

Windows Python 3.14와 WSL Python 3.11에서 manifest의 full/focused/static gate 및 누적 corpus를 독립 실행했다. 실제 CR/CRLF/LF/U+2028/U+2029와 가짜 `@@` hunk의 plain scan·tracked diff·untracked added mapping을 대조하고, 읽기 방식 변경이 MDX fence·ESM·인용 구분에 미치는 회귀도 직접 공격했다.

## A-P1-16 — P1 / FIXED

`_read_text_preserving_newlines`와 Git bytes 직접 decode가 소스와 diff의 물리 LF 경계를 보존한다. 원 double-quoted LS/PS 가짜 hunk 2개 및 literal escape 대조 2개가 양 OS 모두 신규 P8 line 2 / added true / fail true / exit 1이다.

실제 template 내부 CR/CRLF/LF/LS/PS 각각 가짜 hunk 없음/있음의 10개 대조도 양 OS 모두 P8 1개 / exit 1이다. CR/LS/PS는 line 2, LF/CRLF는 line 3이다. 추가로 5개 구분자 × plain/tracked/untracked 3모드의 15개 결과에서도 양 OS가 같은 line·added true·fail true·exit 1을 반환했다. 단독 CR 뒤의 문자열이 다시 diff header로 해석되지 않는다.

## A-P2-06 — P2 / OPEN: CR 보존 후 MDX fence·문단 경계 회귀

원 MDX 실행 코드와 인용 구분 finding을 같은 ID·원 P2로 다시 연다. 이전 입력은 CR을 LF로 변환했지만 이번 후보는 원문 CR을 보존한다. 이에 맞춰 MDX 문법 경계를 갱신하지 않아 누락과 오탐이 생겼다.

- 위치: `tools/ux_lint.py:457` `_mask_mdx_fence`, 특히 460·463·477행의 LF 전용 행 탐색. `tools/ux_lint.py:378` `_is_executable_mdx_template`, 특히 381행의 LF 전용 line prefix와 404행의 LF 빈 문단 탐색.
- 이번 후보에서 양 OS 동일하게 재현했고, 같은 입력·helper를 직전 `31ad7a5` 제품에 양 OS 실행하면 아래 세 반례가 모두 기대대로였다. **이번 newline preservation 변경으로 드러난 회귀**이며 기존 단독 CR diff finding과 구분한다.

재현은 임시 root의 단일 `case.mdx`에 아래 Python 문자열을 UTF-8 `write_bytes`로 쓰고, `python -B -X utf8 <후보>/tools/ux_lint.py --root <임시-root> --fail-new --json`을 해당 root에서 실행한다. `\r`은 실제 단독 CR 바이트다.

### 반례 1·2: 닫힌 fence 밖 실행식을 가림

```python
source = '```ts\rwindow.confirm("quoted");\r```\r\r{window.confirm("x")}\r'
fixture.write_bytes(source.encode('utf-8'))
```

backtick fence를 `~~~`로 바꾼 변형도 동일하다. 첫 호출은 fence 안 인용이고 두 번째는 fence가 닫힌 뒤의 MDX 실행식이다.

| 입력 | 후보 Windows 3.14 / WSL 3.11 | 직전 제품 양 OS | 기대 |
|---|---|---|---|
| 단독 CR backtick fence | **exit 0, PASS, finding 0** | exit 1, P8 1개 | fence 밖 P8 1개 / exit 1 |
| 단독 CR tilde fence | **exit 0, PASS, finding 0** | exit 1, P8 1개 | fence 밖 P8 1개 / exit 1 |
| 같은 두 입력의 LF·CRLF 대조 | exit 1, P8 1개 | 동일 | 정상 |

LF opener 종료를 찾지 못하면 fence mask가 파일 끝까지 확장되어 실제 닫힘 이후 실행식도 가린다. 단독 CR은 Git의 추가 행 좌표에서는 같은 행을 유지하되 Markdown 문법에서는 줄을 끝내야 한다.

### 반례 3: ESM 뒤 정상 인용을 실행식으로 오탐

```python
source = 'export const x = {}\r\rExample: `window.confirm("quoted")`\r'
fixture.write_bytes(source.encode('utf-8'))
```

후보는 양 OS 모두 **exit 1, P8 1개(line 1)**다. 기대는 닫힌 Markdown 인용을 제외한 finding 0 / exit 0이며, 직전 제품과 후보의 LF·CRLF 대조는 모두 기대대로다. LF만 line prefix로 나누므로 빈 CR 문단 이전의 ESM 선언이 뒤쪽 code span을 실행 template으로 바꾼다.

- 영향: 단독 CR MDX에서 실행 금지 호출을 누락하거나 정상 문서를 차단한다. 기존 MDX 경계 finding의 원 심각도 P2를 유지한다.
- 수정 방향: Markdown의 CR/LF/CRLF 문법 경계와 Git/report의 LF 물리 행 좌표를 분리해 처리한다. 소스 전체를 다시 universal newline으로 변환해 A-P1-16을 되살리면 안 된다. fence 시작·종료, 문단, ESM의 이전 행과 prefix를 같은 문법 경계로 대조한다.
- 수용 기준: 위 3개 반례 및 LF·CRLF 대조에서 실행식만 각각 1개, 정상 인용은 0개다. Git CR/CRLF/LS/PS mapping·ESM·주석·미종결 1/2자 span과 닫힌 span·3/4자 fence·blockquote 회귀를 함께 유지한다.

후보 밖 helper는 `F:/dev/kor-travel-common/.git/codex-audit/t103-post19-margins-a.py`, SHA256 `66E400EDF34C840186B0E7FE69B186069FB61F99956DBA32620D7C7833E09394`다. `python -B -X utf8 <helper> <후보-worktree>`로 실행했고 WSL은 `/mnt/f/...` 경로 및 uv Python 3.11을 썼다. 첫 임시 helper 실행은 `--root`가 앞 fixture까지 함께 읽어 결과가 합산됐으므로 판정에서 버렸다. 매 입력 뒤 임시 fixture를 제거해 root에 하나만 존재하도록 교정한 뒤 3개 구분자 × 7개 양성/음성 21개 대조를 양 OS에서 재실행했으며, 그 결과만 위에 기록했다. 제품 파일은 수정하지 않았다.

## 누적 disposition

| 원 ID | 원 심각도 | 판정과 재검증 |
|---|---|---|
| A-P1-01 | P1 | FIXED — CSS scope·specificity·media 조건 교집합·unsupported selector·comment-gap·빈 목록·descendant. |
| A-P1-02 | P1 | FIXED — OKLCH chroma `25%`와 `0.1` RGB 일치. |
| A-P1-03 | P1 | FIXED — alpha sRGB source-over 대비 1.6620953314177012 및 `#333` 대조. |
| A-P1-04 | P1 | FIXED — baseline 앞 삽입된 신규 행만 fail. |
| A-P1-05 | P1 | FIXED — 같은 basename의 외부 Git root 구분. |
| A-P2-06 | P2 | OPEN — 누적 기존 lexer corpus는 유지되나 이번 CR fence·ESM 문단 회귀 3개 반례 발생. |
| A-P2-07 | P2 | FIXED — 옵션 형태 base 일반 오류 2. |
| A-P2-08 | P2 | FIXED — WSL quoted/tab 경로 diff; Windows tab 파일명은 NOT_RUN. |
| A-P2-09 | P2 | FIXED — 비유한/음수/bool/중복·400/5000자리 JSON 오류 2. |
| A-P2-10 | P2 | FIXED — 오류·JSON·summary·argparse 합성 marker 비공개. |
| A-P2-11 | P2 | FIXED — muted 읽기 표면 추가 31쌍 및 미달 판정. |
| A-P3-12 | P3 | FIXED — geo 미달 8개, airport 현재 1.32와 과거 조사 1.15 구분 유지. |
| A-P1-13 | P1 | FIXED — 실제 `++counter;` 추가 행의 diff `+++` 후속 P6 탐지. |
| A-P2-14 | P2 | FIXED — 양 OS self-symlink root 오류 2, traceback 없음. Windows 직접 링크 검사 포함. |
| A-P2-15 | P2 | FIXED — 깊이 2000 JSON 양 도구 오류 2, traceback 없음. |
| A-P1-16 | P1 | FIXED — CR/CRLF/LF/LS/PS 가짜 hunk와 plain/tracked/untracked 좌표 보존. |

## 실행 명령과 결과

Windows Python 3.14.3 / WSL uv Python 3.11.15. 아래 WSL 명령에는 `uv run --no-project --python 3.11`을 붙이고 전체 unittest에만 `--with jsonschema`를 추가했다.

| 명령 | Windows | WSL |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 290 실행/290 통과/skip 0, 112.254초 | 290 실행/289 통과/skip 1, 67.321초; Windows 8.3 전용 skip |
| `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` | 52 통과, 20.866초 | 52 통과, 11.393초 |
| `python -B -X utf8 tools/validate_document_links.py` | 문서 448/대상 2420/오류 0 | 동일 |
| `python -B -X utf8 tools/validate_plan.py` | task 106/오류 0 | 동일 |
| `python -B -X utf8 tools/check_spdx.py` | 파일 56/오류 0 | 동일 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 파일 580/발견 0 | 동일 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 파일 580/발견 0 | 동일 |
| `python -B -X utf8 tools/check_versions.py --self-check` | exit 0, 소비자 검사 아님 | 동일 |
| `python -B -X utf8 tools/check_aliases.py packages/tokens/aliases` | CSS 1/오류 0 | 동일 |
| `git diff --check 538fc42 415984bf7cb450d44d7661424884d6641fef8309` | exit 0 | exit 0 |

누적 direct CLI는 자신의 후보 밖 `t103-post17-reviewer-a-probe.py`, `t103-post17-diff-a.py`, `t103-post18-diff-a.py`에 이번 후보 경로를 전달해 양 OS 실행했다. 전체 누적 출력의 양 OS 차이는 runtime·tab 파일명 가능 여부·플랫폼별 self-symlink probe뿐이었다. 자신의 재현 코드만 재사용했고 상대 raw/결과는 읽지 않았다. 정본 light/dark 27쌍 미달 0, 4앱 light 예제 미달 4/8/8/4 및 등록 baseline의 exit 0, UX fixture report 12개/exit 0을 확인했다. 기본 report의 exit 0을 위반 없음으로 세지 않는다.

추가 plain/tracked/untracked helper는 후보 밖 `t103-post19-mapping-a.py`다. Windows는 같은 본문을 stdin으로 실행했고 WSL은 저장한 helper를 실행했다. Git fixture에는 개별 경로만 stage하며 `git -c user.name=Review fixture -c user.email=fixture@example.invalid commit`을 사용했다. 소비자나 source Git config는 쓰지 않는다.

WSL 정적 gate에만 detached checkout의 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t103-post19-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t103-post19-a`를 프로세스 환경으로 설정했다. 시험/probe에는 주입하지 않았다.

`gh run list --commit 415984bf7cb450d44d7661424884d6641fef8309 --json databaseId,headSha,status,conclusion,url --limit 5`로 [CI 34187292432](https://github.com/digitie/kor-travel-common/actions/runs/34187292432)의 exact head 및 **cancelled**를 확인했다. 로컬 통과를 후보 CI 성공으로 집계하지 않는다.

## 미실행과 원본 보존

- NOT_RUN: Windows Python 3.11(런타임 부재), 소비자 build/e2e·adoption, npm/PyPI registry·게시, workflow dispatch, 실제 브라우저/MDX compiler 렌더링.
- 원본만 경로를 명시해 stage한 뒤 전체 staged diff·diff check·문서 링크·staged secret/redaction을 확인하고 별도 commit한다. 제품 후보·manifest·기존 원본은 변경하지 않는다.
