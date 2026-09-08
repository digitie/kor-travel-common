# T-103 수정 후 적대적 리뷰 28 기준선

- 리뷰 단계: post-fix-27에서 확인된 무효 backtick info fence의 inline span 연결을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `71a6f99de297e809c165f005d4d6b1753468d157`
- 불변 코드 후보 tree: `b0ba565c1fe6d6002c7a983307853f2bb1999c39`
- delta 기준: `009ec5dcf70e55b6c736ccaeabbfeb71a08836f6`
- 이전 manifest: `64505d70f7f976d238dc6dee5a9f061789c2dc39`의 [post-fix-27 manifest](2026-09-08-t103-post-fix-27-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-27-reviewer-a.md), [B](2026-09-08-t103-post-fix-27-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`가 CommonMark 규칙상 무효한 backtick info string을 발견하면 해당 줄의 delimiter만 공백으로 가리고 줄 끝에서 재개한다. 무효한 첫 fence의 backtick을 다음 줄의 닫힘 delimiter로 연결하지 않아, 뒤의 실행식 P8과 별도의 유효 fence opener를 가리지 않는다. plain·blockquote·nested 및 LF/CRLF/CR 회귀시험을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-27 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark blockquote/fence와 invalid backtick info fallback, inline span 경계·P6/P8, nested·CR/LF/CRLF
- Reviewer B 전문 범위: 위 경계의 독립 parser 대조와 Git added-line/base, plain/blockquote/nested·오류/redaction·누락 방지
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-28-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `71a6f99`에서 coordinator가 실행한 결과다.

```text
Windows Python 3.14: python -B -X utf8 -m unittest discover -s tests       -> 301 OK, skip 0
WSL Python 3.11:     uv run --no-project --python 3.11 --with jsonschema ... -> 301 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint              -> 63 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint              -> 63 OK
validate_document_links.py                                                 -> 475 documents, 2464 targets, errors 0
validate_plan.py                                                           -> 106 tasks, errors 0
check_spdx.py                                                              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all                       -> 607 files, findings 0
check_versions.py --self-check                                              -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases                                    -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css --json                            -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json                                  -> fail_count 0, checked-in findings 12
git diff --check cc171bb 71a6f99                                            -> no output
```

리뷰어는 invalid backtick info string이 inline span·다음 fence와 연결되지 않는지, plain/blockquote/nested·P6/P8·LF/CRLF/CR·`--base`를 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows 3.14와 WSL 3.11 결과로 대체 표기하지 않음)
