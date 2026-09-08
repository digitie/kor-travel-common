# T-103 수정 후 적대적 리뷰 32 기준선

- 리뷰 단계: post-fix-31에서 발견된 짧은 marker 행의 TypeError와 prose triple-backtick 오판을 수정한 뒤의 독립 재검토
- 불변 코드 후보 commit: `2375c8b052c94ec8982e0a4be294a747e75835b1`
- 불변 코드 후보 tree: `21a1ca16b806149842777f6c8f597cab5c0433fa`
- delta 기준: `b2fc22b352a1122f465852737f6f0ae7a228ddae`
- 이전 manifest: `910599ec8760515c4810bb0df5f64e450c8c4c93`의 [post-fix-31 manifest](2026-09-08-t103-post-fix-31-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-31-reviewer-a.md), [B](2026-09-08-t103-post-fix-31-reviewer-b.md)

## 이번 후보의 수정

`tools/ux_lint.py`의 Markdown fence 탐색기가 짧은 1·2자 marker 후보를 유효 fence로 반환하지 않고 계속 탐색한다. invalid backtick info opener는 prose의 inline 문맥을 보존하되, opener와 matching delimiter 사이에 plain·blockquote·중첩 blockquote의 유효 fence가 있으면 inline 연결을 끊고 이후 P6/P8 실행식을 검사한다. backtick·tilde, 3·4자 run, LF/CRLF/CR, 일반·중첩 blockquote 회귀시험을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-31 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: 짧은 marker의 반환 계약·CommonMark 중간 block fence 선행 감지·prose/inline 문맥·marker/container 전환·P6/P8·LF/CRLF/CR
- Reviewer B 전문 범위: 독립 Markdown parser 대조·Git added-line/base·중간 tilde/backtick fence·plain/blockquote/nested·indent/tab-stop·오류/redaction
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-32-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `2375c8b`에서 coordinator가 실행한 결과다.

```text
Windows Python:      py -3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 305 OK, skip 0
WSL Python 3.11:     python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 305 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 67 OK
WSL focused:         tests.test_kt_contrast tests.test_ux_lint -> 67 OK
validate_document_links.py -> 487 documents, 2484 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 619 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check 2375c8b -> no output
```

리뷰어는 invalid info의 matching delimiter 전에 시작한 다른 marker fence를 건너뛰어 실행식을 숨기지 않는지, 같은 문단의 정상 inline span은 계속 가리는지, 짧은 marker가 호출자 계약을 깨지 않는지, container·indent·run 길이와 `--base`를 양 OS에서 직접 재현한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
