# T-103 수정 후 적대적 리뷰 3 기준선

- 리뷰 단계: post-fix-02 중단 후 CSS cascade 경계 재현을 반영한 새 독립 재검토
- 기준선 commit: `790bc3ec136b480c9cb95d796990ac1cbb07c596`
- 기준선 tree: `496e44bd27124255437ef265d29e29d680f29e94`
- post-fix-02 기준선: `01c3c3f84aa80fa677f40787f8cfe5582f1eeeb8`
- post-fix-02 tree: `a022eb86a493857d7eefbeb8a35f79cc672013a7`
- post-fix-02 manifest commit: `09851a25192dcb7b82d0ce6905c134fb2ef1cd74`
- 이번 수정: 지원 selector별 CSS specificity·cascade 보존, unclosed comment/string 입력 오류, MDX 보간 표시 예외 경계
- post-fix-01 A/B 원본 report SHA256: A `7D22EFD9D67FA9C0FBAB2A535E465CAD687BBD07E2C94EB01F35C6525DF23D28`, B `e95a6385e869b6cc2a70a401e881381c6370b77f3c5d4ca22a997f2e356ecacf`
- 최초 원본 report SHA256: A `DDF408BD80DBAC8482850B9CF21AB3A6DDC9B223D29D0116B1D0B8099815255B`, B `f9eeff355a684f7861043e5252195c52973c54567799a8df355a9f236322a053`

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS 전역 selector의 specificity·source order·media 조건·문자열과 중첩 경계, OKLCH·sRGB alpha, baseline 입력과 오류 redaction, MDX 실행 template·inline/fenced code와 보간 주석, Git diff `+++` 행, symlink root, 4앱 수용 기준을 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 790bc3ec136b480c9cb95d796990ac1cbb07c596
```

두 reviewer의 post-fix-03 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
