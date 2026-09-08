# T-103 수정 후 적대적 리뷰 4 기준선

- 리뷰 단계: post-fix-03 NO-GO finding 수정 후 네 번째 독립 재검토
- 기준선 commit: `1625bf197486448f7dc6b7780a6c4f4c13b01368`
- 기준선 tree: `ee0626eb05e3e8dff3238f0de9ca71c3c2840563`
- post-fix-03 기준선: `790bc3ec136b480c9cb95d796990ac1cbb07c596`
- post-fix-03 tree: `496e44bd27124255437ef265d29e29d680f29e94`
- post-fix-03 manifest commit: `826f6107fbb3d6a45fce348ad19dc1b25c7cfde7`
- post-fix-03 A 원본 report commit: `20f3e573f63148d29fde4beb8df71e4008d69e31`
- post-fix-03 B 원본 report commit: `608669bcaf3f84913a0668cfbe51393029f45763`
- post-fix-03 A 원본 report SHA256: `E5D9D5C86067E00F785A5B1412C42EF80953AC454007DAD6685A48D604CA56CC`
- post-fix-03 B 원본 report SHA256: `688f035df1bfcee718d070269d553e94c65eb91c3903df823da10e74dc906cd0`
- 이번 수정: media 조건 교집합과 `:root.dark` 지원, generic argparse 오류, 깊은 JSON `RecursionError`, MDX tagged template·colon/fence·escaped interpolation 경계

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS cascade와 조건 교집합, selector·media 모순, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline/fenced/tilde/tagged/escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 1625bf197486448f7dc6b7780a6c4f4c13b01368
```

두 reviewer의 post-fix-04 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
