# T-103 수정 후 적대적 리뷰 31 기준선

- 리뷰 단계: post-fix-30에서 확인된 matching delimiter 이전의 중간 tilde/backtick fence 연결 누락을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `b2fc22b352a1122f465852737f6f0ae7a228ddae`
- 불변 코드 후보 tree: `be501ae5592c6c20edc235cc6f3516f8817ce9ac`
- delta 기준: `620e477bf841f881e6090cccefcbad81cfffe6e7`
- 이전 manifest: `43d5c3d8ba6b2f31edc4b7b28a331150200d4e1e`의 [post-fix-30 manifest](2026-09-08-t103-post-fix-30-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-30-reviewer-a.md), [B](2026-09-08-t103-post-fix-30-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`가 invalid backtick info opener와 선택된 matching delimiter 사이의 각 줄에서 유효한 plain/blockquote fence를 먼저 찾는다. 중간 tilde 또는 더 긴 backtick fence가 있으면 inline span으로 연결하지 않고 opener 줄만 격리해 이후 실행식 P6/P8을 검사한다. matching delimiter 자체의 container·marker·marker 뒤 콘텐츠 열도 함께 확인한다. 일반·중첩 blockquote와 3·4자 run, LF/CRLF/CR 회귀시험을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-30 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: CommonMark 중간 block fence 선행 감지, marker/container 전환, 3·4자 inline span, P6/P8·LF/CRLF/CR
- Reviewer B 전문 범위: 독립 Markdown parser 대조, Git added-line/base, 중간 tilde/backtick fence·plain/blockquote/nested·indent/tab-stop·오류/redaction
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-31-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `b2fc22b`에서 coordinator가 실행한 결과다.

```text
Windows Python:      python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 304 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 304 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 66 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint -> 66 OK
validate_document_links.py -> 484 documents, 2481 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 616 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check 620e477 b2fc22b -> no output
```

리뷰어는 invalid info의 matching delimiter 전에 시작한 다른 marker fence를 건너뛰어 실행식을 숨기지 않는지, 같은 문단의 정상 inline span은 계속 가리는지, container·indent·run 길이와 `--base`를 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
