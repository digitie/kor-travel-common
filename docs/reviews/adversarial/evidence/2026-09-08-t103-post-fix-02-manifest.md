# T-103 수정 후 적대적 리뷰 2 기준선

- 리뷰 단계: post-fix-01 NO-GO finding 수정 후 두 번째 독립 재검토
- 기준선 commit: `01c3c3f84aa80fa677f40787f8cfe5582f1eeeb8`
- 기준선 tree: `a022eb86a493857d7eefbeb8a35f79cc672013a7`
- post-fix-01 기준선: `f9666078f49ea0745f485d6d0c88206048675aae`
- post-fix-01 tree: `6bcda765a470f0aed8a314512edefa7fae2fb0e9`
- post-fix-01 수정 commit: `972ae4a`(CSS scope·media·오류 redaction·실행 template·diff 경계)
- post-fix-01 A 원본 report commit: `9b916339f29c565b676a44c11d46e522722a2a19`
- post-fix-01 B 원본 report commit: `02b3d263caccc4af9e3a8a24360d53cf3b7ceff6`
- post-fix-01 A 원본 report SHA256: `7D22EFD9D67FA9C0FBAB2A535E465CAD687BBD07E2C94EB01F35C6525DF23D28`
- post-fix-01 B 원본 report SHA256: `e95a6385e869b6cc2a70a401e881381c6370b77f3c5d4ca22a997f2e356ecacf`
- 최초 구현 후보: `d12ccba48f67ad8ac863dbc97d85dda289c1e09c`
- 최초 manifest: `94ca2f1730b270721eb6242bfcdd9362b51d45e5`
- 최초 A/B 원본 report SHA256: A `DDF408BD80DBAC8482850B9CF21AB3A6DDC9B223D29D0116B1D0B8099815255B`, B `f9eeff355a684f7861043e5252195c52973c54567799a8df355a9f236322a053`

## 재검토 범위

새 후보의 CSS selector·media 조건·중첩 블록·문자열/주석 lexer, OKLCH·sRGB alpha, muted 읽기 표면, baseline JSON 입력과 generic 오류, MDX 실행 template·보간 주석, Git diff `+++` 행, symlink root·경로 redaction, 4앱 evidence를 양 OS에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

## 고정 명령

```text
python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 01c3c3f84aa80fa677f40787f8cfe5582f1eeeb8
```

두 reviewer의 post-fix-02 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
