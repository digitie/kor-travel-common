# T-103 수정 후 적대적 리뷰 29 기준선

- 리뷰 단계: post-fix-28에서 확인된 invalid backtick info의 정상 inline span 오탐과 block fence 연결 누락을 함께 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `9afea549dd81cb23d3297f83d89df4b519734382`
- 불변 코드 후보 tree: `03cb65ba437848f279f542452705c235f19daaa8`
- delta 기준: `71a6f99de297e809c165f005d4d6b1753468d157`
- 이전 manifest: `f661de2db7419dba70170225e16a3c9f8ba3d021`의 [post-fix-28 manifest](2026-09-08-t103-post-fix-28-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-28-reviewer-a.md), [B](2026-09-08-t103-post-fix-28-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`가 CommonMark 규칙상 invalid backtick info string을 같은 문단의 정상 inline span으로 되돌린다. matching delimiter가 같은 줄 또는 문단 안의 비-fence 위치이면 opener·내용·닫힘을 함께 가리고, 줄 시작의 유효한 plain/blockquote/nested block fence이면 현재 줄만 격리해 이후 P6/P8 실행식을 검사한다. 일반·중첩 blockquote와 LF/CRLF/CR, inline·block 경계 회귀시험을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-28 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark invalid backtick info의 inline fallback, 정상 closed 3/4자 span, block fence 식별, plain/blockquote/nested·P6/P8·CR/LF/CRLF
- Reviewer B 전문 범위: 독립 Markdown parser 대조와 Git added-line/base, 정상 inline false positive·block fence false negative, 오류/redaction·plain/blockquote/nested 교차
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-29-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `9afea54`에서 coordinator가 실행한 결과다.

```text
Windows Python:      python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 302 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 302 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 63 OK (full run 포함)
WSL focused:         tests.test_kt_contrast tests.test_ux_lint -> 63 OK (full run 포함)
validate_document_links.py -> 478 documents, 2471 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 610 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check 71a6f99 9afea54 -> no output
```

리뷰어는 invalid info가 정상 same-line·same-paragraph inline code를 가리지 않고, line-start block fence와 연결되어 뒤의 P6/P8을 숨기지 않는지 plain/blockquote/nested·P6/P8·LF/CRLF/CR·`--base`로 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
