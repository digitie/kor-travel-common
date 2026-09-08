# T-103 수정 후 적대적 리뷰 36 기준선

- 리뷰 단계: post-fix-35에서 확인된 Markdown 본문과 JavaScript lexer의 문맥 혼합을 분리한 뒤의 독립 재검토
- 불변 코드 후보 commit: `d8027917e4cb88b72d5d5c98d571ef3522e808c8`
- 불변 코드 후보 tree: `3e9d2614629eafddd8b2cf126d9e8234d1ab48c8`
- delta 기준: `aedfdd659255c27bcc4377bd15b39452c004417d`
- 이전 manifest: `ea60635fa9472afb5a5ac10eb24b4c33a1660ab4`의 [post-fix-35 manifest](2026-09-08-t103-post-fix-35-manifest.md)
- 직전 raw 원본: [A](2026-09-08-t103-post-fix-35-reviewer-a.md), [B](2026-09-08-t103-post-fix-35-reviewer-b.md)

## 이번 후보의 수정

닫힘 없는 Markdown inline span의 재개 후보를 찾을 때 전체 JavaScript lexer를 적용하지 않고, 확인된 MDX 표현식의 주석만 가리는 전용 경로로 분리했다. 일반 본문의 아포스트로피·따옴표는 JavaScript 문자열 상태를 열지 않고, URL의 `//`와 일반 문장의 slash도 line comment가 되지 않는다. 반대로 `{...}` 표현식, JSX 속성, ESM 선언과 그 안의 block/line comment는 기존 마스킹을 유지한다. URL, 아포스트로피, MDX block comment의 회귀시험과 plain/blockquote/nested container·1/2자 run·LF/CRLF/CR 조합을 추가했다.

## 리뷰 요청

두 reviewer는 동일한 immutable 코드 후보에서 post-fix-35 원본을 기준으로 독립 재검토하되 상대 reviewer의 새 결과·raw를 읽지 않는다. 별도 detached worktree에서 시작·종료 HEAD/tree와 clean을 확인하고 자신의 원본 report 한 파일만 작성한다. 제품·manifest·소비자·기존 evidence는 수정하지 않는다.

- Reviewer A 전문 범위: 본문/표현식 문맥 전환, URL·apostrophe·block comment, 닫힘 없는 span의 재개 후보, P6/P8, 문단·줄바꿈·container
- Reviewer B 전문 범위: 독립 Markdown parser 대조, `--base` 추가행, 짧은 run·tilde/backtick, plain/blockquote/nested·indent/tab-stop·오류·redaction
- 원본 산출물: `docs/reviews/adversarial/evidence/2026-09-08-t103-post-fix-36-reviewer-a.md`와 `...-reviewer-b.md`
- verdict 어휘: `PASS` 또는 `NO-GO`; finding ID·심각도·위치·재현·영향·최소 수정·disposition을 기록한다.

## 고정 검증과 관찰

다음은 후보 `d8027917`에서 coordinator가 실행한 결과다.

```text
Windows Python:      python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -> 314 OK, skip 0
WSL Python 3.11:     wsl.exe --cd /mnt/f/dev/kor-travel-common -- python3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -> 314 OK, skip 1
Windows focused:     tests.test_kt_contrast tests.test_ux_lint -> 76 OK
validate_document_links.py -> 499 documents, 2496 targets, errors 0
validate_plan.py           -> 106 tasks, errors 0
check_spdx.py              -> 56 files, errors 0
scan_secrets.py --all / check_prod_redaction.py --all -> 631 files, findings 0
check_versions.py --self-check -> registry self-check PASS; consumer check NOT_RUN
check_aliases.py packages/tokens/aliases -> CSS 1, errors 0
kt_contrast.py packages/tokens/tokens.css -> 27 pairs PASS
ux_lint.py --root tests/fixtures/ux --json -> fail_count 0, checked-in findings 12
git diff --check d802791^ d802791 -> no output
```

리뷰어는 닫힘 없는 span에서 URL·일반 slash가 실제 `{...}` 표현식을 숨기지 않는지, 본문 아포스트로피·따옴표가 다음 fence를 실행 코드로 오인하게 하지 않는지, 실제 표현식 안 주석은 계속 가려지는지 확인한다. checked-in UX fixture의 12개 finding은 report 모드의 의도된 예시이며 fail_count 0으로 집계한다.

## 범위 밖과 NOT_RUN

- 정확한 후보 원격 CI: manifest 작성 시점에는 `NOT_RUN(실행 중)`; merge 전 PR head SHA와 6개 job을 다시 확인한다.
- 실제 소비자 저장소 빌드·타입·e2e와 소비자 manifest 검증: `NOT_RUN` (common checkout만 허용된 범위)
- npm/PyPI registry 설치·게시와 실제 MDX compiler/browser 실행: `NOT_RUN` (라이브러리 게시를 수행하지 않음)
- Windows Python 3.11: `NOT_RUN` (실행 파일 부재; Windows와 WSL 결과로 대체 표기하지 않음)
