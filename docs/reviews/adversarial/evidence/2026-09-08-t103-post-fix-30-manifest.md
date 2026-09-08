# T-103 수정 후 적대적 리뷰 30 기준선

- 리뷰 단계: post-fix-29에서 확인된 다른 container fence 연결과 blockquote marker 뒤 4열 closing 오판을 함께 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `620e477bf841f881e6090cccefcbad81cfffe6e7`
- 불변 코드 후보 tree: `ee2964452454b255a47a27aea1edb1a0c5ede2db`
- delta 기준: `9afea549dd81cb23d3297f83d89df4b519734382`
- 이전 manifest: `a1001947bb5eef864115ffb3061390c09307a131`의 [post-fix-29 manifest](2026-09-08-t103-post-fix-29-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-29-reviewer-a.md), [B](2026-09-08-t103-post-fix-29-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 invalid backtick info fallback이 닫힘 후보를 opener와 같은 container에 한정하지 않고 줄 자체가 시작하는 plain/blockquote fence인지 확인한다. 따라서 quote에서 plain, plain에서 quote, nested에서 다른 quote 깊이로 바뀌는 실제 block fence는 inline 닫힘으로 연결되지 않는다. blockquote marker 뒤 콘텐츠 들여쓰기 4열 이상(공백·탭 조합)은 fence가 아니라 inline span 내용으로 남긴다. run 길이 3·4와 plain/blockquote/nested·LF/CRLF/CR 회귀시험을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-29 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark container 전환, blockquote marker 뒤 0~3열/4열 fence 판정, 3·4자 inline span, plain/blockquote/nested·P6/P8·CR/LF/CRLF
- Reviewer B 전문 범위: 독립 Markdown parser 대조와 Git added-line/base, container depth 변화·indent/tab-stop·정상 inline false positive·실행식 누락, 오류/redaction
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-30-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `620e477`에서 coordinator가 실행한 결과다.

```text
Windows Python:      python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 303 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 303 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 64 OK (full run 포함)
WSL focused:         tests.test_kt_contrast tests.test_ux_lint -> 64 OK (full run 포함)
validate_document_links.py -> 481 documents, 2478 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 613 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check 9afea54 620e477 -> no output
```

리뷰어는 invalid info가 정상 same-line·same-paragraph inline code를 가리지 않고, 다른 container 깊이의 line-start block fence와 연결되어 뒤의 P6/P8을 숨기지 않는지, marker 뒤 4열 이상 closing을 inline code로 유지하는지 양 OS에서 `--base`와 함께 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
