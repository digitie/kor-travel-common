# T-103 수정 후 적대적 리뷰 1 기준선

- 리뷰 단계: 최초 NO-GO finding 수정 후 독립 재검토
- 기준선 commit: `f9666078f49ea0745f485d6d0c88206048675aae`
- 기준선 tree: `6bcda765a470f0aed8a314512edefa7fae2fb0e9`
- 최초 구현 후보: `d12ccba48f67ad8ac863dbc97d85dda289c1e09c`
- 최초 manifest: `94ca2f1730b270721eb6242bfcdd9362b51d45e5`
- 수정 commit: `19dbdfd`(리뷰 경계·입력 검증)
- 최초 원본 report 기록 commit: A `041384dce46c8b923e0255d17ec5fa7f0bfe55f4`, B `c5c99e733f5f4e455ade03b0d261e00bab3f0031`
- 최초 원본 report SHA256: A `DDF408BD80DBAC8482850B9CF21AB3A6DDC9B223D29D0116B1D0B8099815255B`, B `f9eeff355a684f7861043e5252195c52973c54567799a8df355a9f236322a053`

## 재검토 범위

수정 후보의 CSS 적용 범위·cascade·문자열 파싱·OKLCH 백분율·sRGB alpha source-over·추가 muted 읽기 표면·baseline schema와 유한 수치·Git root/ref/diff·앞 삽입 예외 예산·실행 template/interpolation·출력 redaction·4앱 evidence를 독립적으로 다시 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

## 고정 명령

```text
python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
python -B -X utf8 -m unittest tests.test_kt_contrast tests.test_ux_lint -v
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/kt_contrast.py packages/tokens/tokens.css --json
python -B -X utf8 tools/ux_lint.py --root tests/fixtures/ux --json
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 f9666078f49ea0745f485d6d0c88206048675aae
```

최종 판정은 두 reviewer의 post-fix 원본 report와 이 기준선의 tree가 일치한 뒤 기록한다. 검증하지 않은 소비자 gate는 `NOT_RUN`으로 유지한다.
