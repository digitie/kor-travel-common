# T-103 수정 후 적대적 리뷰 26 기준선

- 리뷰 단계: post-fix-25에서 확인된 blockquote 깊이 감소와 `>` 뒤 4열 닫힘 오판을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `2a32dc7e07a4c36e2b0e92402f05019b31f6c3cb`
- 불변 코드 후보 tree: `a08e12fc66c67dfe65015f714a69c5fc0740a3f0`
- delta 기준: `155941045a077529cb12f875cad5ab2b2f7639da`
- 이전 manifest: `0e3238ce37e496ec5e88773ffc5e4add90b6dab0`의 [post-fix-25 manifest](2026-09-08-t103-post-fix-25-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-25-reviewer-a.md), [B](2026-09-08-t103-post-fix-25-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 blockquote fence parser가 opener의 마지막 `>` 뒤 들여쓰기와 각 candidate 줄의 컨테이너 깊이를 열 단위로 검증한다. opener와 같은 깊이의 `>`가 부족한 줄(인용되지 않은 빈 줄 포함)을 만나면 인용 fence를 종료해 다음 문단을 검사한다. 같은 깊이를 유지하면서 `>` 뒤 들여쓰기가 4열 이상인 줄은 body로 남기고 closing marker로 인정하지 않는다. nested blockquote body는 outer 컨테이너를 소비한 뒤 남은 `>`를 literal 내용으로 보존한다. 회귀시험은 nested depth 감소·unquoted blank·4 space/tab/space+tab opener·closer·LF/CRLF/CR을 고정한다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 서로의 post-fix-26 원본을 읽지 않고 독립 실행한다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고, 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark blockquote/fence container 깊이·종료·nested literal, opener/closer post-marker tab-stop, 빈 줄·새 quote block, CR/LF/CRLF와 누적 P6/P8 회귀
- Reviewer B 전문 범위: Git added-line/base·입력/오류/redaction·문서/task/scope 정합과 quoted fence·depth decrease·4열·plain/--base 교차 재현
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-26-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `2a32dc7`에서 coordinator가 실행한 결과다.

```text
Windows Python 3.14: python -B -X utf8 -m unittest discover -s tests       -> 298 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests      -> 298 collected, 297 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint              -> 60 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint              -> 60 OK
validate_document_links.py                                                 -> 469 documents, 2452 targets, errors 0
validate_plan.py                                                           -> 106 tasks, errors 0
check_spdx.py                                                              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all                       -> 601 files, findings 0
check_versions.py --self-check                                              -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases                                    -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css --json                            -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json                                  -> fail_count 0, checked-in findings 12
git diff --check 1559410 2a32dc7                                           -> no output
```

리뷰어는 plain/blockquote/nested blockquote fence, depth 감소·인용되지 않은 빈 줄·새 quote block, marker 뒤 ASCII/Unicode suffix, 0~3열·4열·tab·space+tab, LF/CRLF/CR, `--base`와 외부 P6/P8을 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows 3.14와 WSL 3.11 결과로 대체 표기하지 않음)
