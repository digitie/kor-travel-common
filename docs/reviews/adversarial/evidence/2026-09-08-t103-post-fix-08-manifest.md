# T-103 수정 후 적대적 리뷰 8 기준선

- 리뷰 단계: post-fix-07 NO-GO finding 수정 후 여덟 번째 독립 재검토
- 불변 코드 후보 commit: `559a9e8a0e49feca2dab9d59df29039bbb0acfd3`
- 불변 코드 후보 tree: `322fb840ac458c8fc7a0c69f90b0d1bdb77495d6`
- post-fix-07 기준선 commit: `63fe3d5c969b28bab4d528d3e24a054e3a8e30e6`
- post-fix-07 기준선 tree: `c9fb07160de150d7a4cfbbb31fc226cb6a9fb3af`
- post-fix-07 manifest commit: `dbfb036ed054d6f591ad295be4db148177956fd8`
- post-fix-07 A 원본 report commit: `73263674942360ec100953c6e2da4688bd17326d`
- post-fix-07 B 원본 report commit: `f78bb3173234ae9f80b5cd76613825205895a13d`
- post-fix-07 A 원본 report SHA256: `E7AB11DC89AFADC098C0B3C58944E8E0BB08CF84B94600F6BB1CB8D9C4067116`
- post-fix-07 B 원본 report SHA256: `d8f67021c707c71f13329921a9e9e44e617c550a11434b91cdc745d8142b34b1`
- 이번 수정: JSX 중괄호 상태 추적에서 line/block 주석을 제외하고, 닫히지 않은 단일 backtick span을 EOF까지 실행 영역으로 가리지 않으며, Markdown code span 내부의 selector 문맥 누수를 차단

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·미종결 span·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 559a9e8a0e49feca2dab9d59df29039bbb0acfd3
```

두 reviewer의 post-fix-08 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
