# T-103 수정 후 독립 적대적 리뷰 24 — Reviewer A

## 판정·기준선·격리

- 실행 ID: `T103-POST24-A-20260908-145208-KST` (`reviewer_a`).
- 최종 verdict: **PASS**. 이번 검토에서 신규 P0/P1/P2/P3 각각 0개. 누적 A 18개 finding의 실행한 반례는 모두 FIXED다.
- immutable 제품 candidate: `535beecaeaf06296df3c8c1e108c1b86564e48d7`, tree `7934214ea8584500670a7808ebb68b53dec29d63`.
- delta base: `3a8b569889fcaf4429cc70a7bafec779181aac6f`.
- manifest: commit `4fac62b3b40f7cd36a7e3b80e399611b0aa30fff`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-24-manifest.md`를 `git show`로 읽었다.
- 별도 detached worktree: `F:/dev/kor-travel-common-wt/review-t103-post24-a`.
- 시작: 2026-09-08 14:52:08.805 KST. 제품 검토 종료: 14:55:56.501 KST. 시작·종료 HEAD/tree는 위 candidate와 같고 `git status --porcelain=v1` 출력은 비어 있었다.
- 상대 post24 결과·raw와 이전 상대 원문은 읽지 않았다. 변경 목록에 표시된 상대 원본의 파일명만 확인했다. 후보·manifest·소비자·기존 evidence·Git config는 수정하지 않았으며, 이 원본 한 파일만 report-only commit으로 추가한다.

## 요청 원문

> T-103 post-fix-24 독립 적대적 리뷰를 시작해 주세요. immutable 제품 후보는 commit `535beecaeaf06296df3c8c1e108c1b86564e48d7`, tree `7934214ea8584500670a7808ebb68b53dec29d63`; 공통 manifest는 commit `4fac62b3b40f7cd36a7e3b80e399611b0aa30fff`의 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-24-manifest.md`입니다. 별도 detached worktree `F:/dev/kor-travel-common-wt/review-t103-post24-a`에서 candidate와 clean을 확인하세요. 전문 범위는 CommonMark backtick fence info string의 backtick 금지, tilde info 허용, 3/4자 delimiter, 0~3열·tab-stop·4열, ASCII/LS/PS suffix, LF/CRLF/CR, inline span 뒤 MDX P8, fence 내부 P6/P8 및 누적 T-103 finding 회귀입니다. 코드·문서를 직접 확인하고 작성자 evidence를 맹신하지 마세요. 상대 reviewer의 post24 결과/raw를 읽거나 요청하지 말고, 제품·manifest·소비자·기존 evidence를 수정하지 마세요. 본인 원본 `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-24-reviewer-a.md` 한 파일만 작성해 report-only commit으로 확정하세요. 실행 ID/시각/요청 원문/실제 SHA·tree·clean/명령/검증/NOT_RUN/각 finding disposition/verdict(PASS 또는 NO-GO)를 포함하고 commit hash와 SHA256을 부모에게 보내 주세요. 후보에 수정이 필요하면 먼저 NO-GO raw를 확정하고 작업을 멈추세요.

## 전체 delta와 정본 대조

전체 delta 5파일 중 제품 수정은 `tools/ux_lint.py`의 4행과 `tests/test_ux_lint.py`의 30행이다. 나머지 3파일은 이전 manifest·A/B 원본 기록이며 상대 본문은 열지 않았다. `_mask_mdx_fence`가 opener의 같은 Markdown 줄 나머지에서 backtick을 찾고, marker가 backtick일 때만 fence 진입을 거부하는지 직접 읽었다. 검사 후 기존 inline span 경로로 돌아가는 분기도 확인했다. 테스트는 LF/CRLF/CR의 후속 P8 검출과 tilde info의 backtick 허용을 다룬다.

AGENTS·문서 라우터·resume·T-103 task·standards·runbooks·versions·CI의 delta가 없음을 확인하고 직전의 동일 정본 검토를 재사용했다. 제품의 3열 들여쓰기 상한·4열 tab-stop, Markdown CR/LF/CRLF와 ECMAScript LS/PS 경계 분리도 변경되지 않았다. [CommonMark 0.31.2 §4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks)의 backtick info 금지·tilde 예외와 일치한다(공식 원문 확인일 2026-09-08).

## 직전 finding의 직접 재현

### A-P1-20 — FIXED

최소 입력은 첫 줄의 정상 3자 code span 뒤에 빈 문단과 실행식을 둔다.

```python
body = '```a`b```\n\n{window.confirm("x")}\n'
```

양 OS의 CLI `python -B -X utf8 tools/ux_lint.py --root <temporary-fixture-root> --fail-new --json`에 해당 바이트를 넣었다. WSL은 uv Python3.11을 사용했다. 실제 결과는 이제 `P8` 1건/exit 1이다. 3·4자 delimiter × LF/CRLF/CR의 직전 6개 false PASS가 모두 기대대로 바뀌었다. 이전 제품에서 exit 0이던 동일 반례이며, 이번 변경으로 닫힌 것으로 판정한다.

추가 대조 84개는 3·4자 marker, 0·3열, LF/CRLF/CR, backtick/tilde와 plain/LS/PS info 및 tilde의 backtick info를 조합했다. 내부에는 P6/P8 문자열을 함께 넣고 정상 닫힘 뒤 실제 P8을 추가했다. 전부 내부 2개는 제외·외부 P8 1개만 검출·exit 1이었다. backtick 제한을 tilde에 잘못 적용하거나 fence 이후 실행식까지 가리는 회귀는 재현되지 않았다.

### A-P2-19 — FIXED 유지

직전의 102개 fence 행렬을 양 OS에서 그대로 실행했다. 4 space/tab/space+tab 선행의 닫힘 오인 18개는 발견 0이며, 0~3열 정상 닫힘 뒤 JSX는 P6으로 검출한다. ASCII space/tab 접미사는 닫힘, LS/PS/NBSP/VT/FF 접미사는 비닫힘이다. `failures=[]`가 양 OS에서 일치한다.

추가 opener 120개 행렬도 전부 기대와 일치했다. 0/1/2/3열 opener × 0/1/2/3열 closer × backtick/tilde × LF/CRLF/CR의 96개, 4 space/tab/space+tab 비opener 18개와 A-P1-20의 6개를 포함한다.

## 누적 finding별 disposition

FIXED는 실행한 각 반례·수용 경계에 한정한다. CommonMark/MDX 전체 문법의 완전성을 선언하지 않는다.

| ID | 원 심각도 | 이번 disposition·근거 |
|---|---|---|
| A-P1-01 | P1 | FIXED. CSS selector·specificity·media 교집합·comment gap·미지원/빈 목록 입력 오류 유지 |
| A-P1-02 | P1 | FIXED. OKLCH chroma 25%와0.1 변환값 일치 |
| A-P1-03 | P1 | FIXED. sRGB alpha 흰색20%/검정 대비1.6620953314177012 유지 |
| A-P1-04 | P1 | FIXED. 앞에 새로 추가한 위반이 기존 baseline 예산으로 면제되지 않음 |
| A-P1-05 | P1 | FIXED. 같은 이름의 외부 Git root 추가행 검출 |
| A-P2-06 | P2 | FIXED. MDX inline·JSX/ESM·Unicode/FEFF/async·주석·미종결 span·문단 corpus 유지 |
| A-P2-07 | P2 | FIXED. option 모양 base 일반 입력 오류 |
| A-P2-08 | P2 | FIXED(WSL). Git quoted/tab 파일명 검출; Windows tab 파일명은 NOT_RUN |
| A-P2-09 | P2 | FIXED. NaN/Infinity/음수/bool/중복·거대 숫자 JSON 거부 |
| A-P2-10 | P2 | FIXED. JSON/Markdown/annotation/summary/argparse 오류 비공개 |
| A-P2-11 | P2 | FIXED. muted 읽기 선언31쌍·text-tertiary 미달 검출 |
| A-P3-12 | P3 | FIXED. geo8개 미달, airport 현재 sRGB1.320934·과거 조사1.15의 문서 경계 |
| A-P1-13 | P1 | FIXED. 실제 `+++` 소스 추가행 유지 |
| A-P2-14 | P2 | FIXED. 양 OS self-symlink root exit2·traceback 없음 |
| A-P2-15 | P2 | FIXED. 깊이2000 JSON 두 도구 일반 입력 오류 |
| A-P1-16 | P1 | FIXED. CR/CRLF/LF/LS/PS 가짜 hunk·plain/tracked/untracked 매핑 |
| A-P2-19 | P2 | FIXED. 3열 상한·tab-stop 및102개 fence 대조 |
| A-P1-20 | P1 | FIXED. 6개 info-string 오판 해결·tilde 예외 유지 |

## 실행 명령과 실제 결과

- Windows Python3.14.3: 전용 프로세스 TEMP/TMP에서 `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v` — **295개 통과, skip0**, 136.332초.
- WSL Python3.11.15: 전용 TMPDIR에서 `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests` — **295개 실행, 294개 통과, skip1**, 71.403초. Windows8.3 API 전용 skip은 성공으로 집계하지 않았다.
- 양 OS `python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint` — 각각 **57개 통과**, Windows23.337초·WSL13.903초. WSL은 uv Python3.11 접두사를 사용했다.
- 양 OS 외부 누적 helper `t103-post17-reviewer-a-probe.py <candidate-root>` — Windows264/WSL263 출력 행(시험 개수 아님). 자신의 직전 label/값 전체 대조 변경0. 기존 CSS·색상 수학·JSON·redaction·symlink·MDX corpus를 후보에 새로 실행했다.
- `t103-post19-margins-a.py <candidate-root>` 21개, `t103-post18-diff-a.py <candidate-root>` 10개, `t103-post19-mapping-a.py <candidate-root>` 15개: 양 OS의 직전 기대 출력과 전체 동일.
- `t103-post21-boundary-a.py <candidate-root>` 44개, `t103-post22-fence-a.py <candidate-root>` 102개, `t103-post23-opener-a.py <candidate-root>` 120개: 양 OS 모두 실패 목록 비어 있음.
- 새 `t103-post24-info-a.py <candidate-root>` 84개: 양 OS 모두 실패 목록 비어 있음. helper SHA256 `B07F236B538760D81B68C522F8F21360121D4C59487A16EC8F26BEAFEF7EA549`.
- helper와 로그는 source checkout의 `.git/codex-audit/`에만 있다. Windows는 `python -B -X utf8`, WSL은 `/mnt/f/` 경로와 `uv run --no-project --python 3.11 python -B -X utf8`로 같은 helper를 실행했다. 중간 로그 집계 한 번은 아직 생성되지 않은 Windows 로그에 접근해 실패했으나 제품 실행 오류는 아니며, 모든 프로세스 종료 후 집계를 다시 실행해 위 결과를 확인했다.

다음 정적 gate를 양 OS 후보에서 실행했다. WSL Git 기반 검사에는 프로세스 `GIT_DIR`·`GIT_WORK_TREE`만 해당 detached worktree로 지정했으며 git config는 변경하지 않았다.

```text
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 3a8b569889fcaf4429cc70a7bafec779181aac6f 535beecaeaf06296df3c8c1e108c1b86564e48d7
```

양 OS 링크463문서/2440대상·plan106 task·SPDX56파일·secret/redaction 각각595파일 오류0. registry 자체 검사·별칭CSS1개 통과, diff-check 출력 없음. canonical light27쌍 PASS·full/focused의 dark 전수 시험 통과. checked-in UX fixture는 report12건·fail_count0이며 위반0으로 집계하지 않았다.

`gh run list --commit 535beecaeaf06296df3c8c1e108c1b86564e48d7 --json databaseId,headSha,status,conclusion,url --limit 5`로 [정확한 후보 CI34192047936](https://github.com/digitie/kor-travel-common/actions/runs/34192047936)의 headSha 일치·completed/success를 읽기 전용 확인했다. 개별 job 로그의 재감사는 하지 않았다.

## NOT_RUN·한계

- Windows Python3.11: 실행 환경 없음. Windows3.14·WSL3.11의 성공을 해당 환경의 성공으로 표기하지 않는다.
- 실제 MDX compiler/browser: 미실행. 기존 공식 CommonMark0.31.2 대조를 재사용했으며 이번에는 양 OS 제품 CLI를 새로 실행했다. 외부 파서를 설치하거나 제품 의존성으로 추가하지 않았다.
- 소비자 build/type/e2e·채택 gate, npm/PyPI registry 설치·게시, workflow dispatch: 요청 범위 밖. 소비자 이관 task와 T-010/T-502의 책임을 유지한다.
- PASS는 위 immutable 제품 후보의 독립 리뷰 범위에 대한 판정이다. 소비자 gate 완료·라이브러리 게시·실제 배포 승인이 아니다.
