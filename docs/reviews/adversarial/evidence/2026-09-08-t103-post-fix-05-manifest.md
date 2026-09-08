# T-103 수정 후 적대적 리뷰 5 기준선

- 리뷰 단계: post-fix-04 NO-GO finding 수정 후 다섯 번째 독립 재검토
- 불변 코드 후보 commit: `ecad460db93a9369d96435a28b6cb48dd7516ace`
- 불변 코드 후보 tree: `6a903d346072ca951fe5146653addaa250fd44f5`
- post-fix-04 기준선 commit: `1625bf197486448f7dc6b7780a6c4f4c13b01368`
- post-fix-04 기준선 tree: `ee0626eb05e3e8dff3238f0de9ca71c3c2840563`
- post-fix-04 manifest commit: `8152395679290359c8ca6af2c3bb47903f07b4db`
- post-fix-04 A 원본 report commit: `1c45015f529387abcc8b9a5bcf5be7199c556378`
- post-fix-04 B 원본 report commit: `8ca3a26c4d35e94c511489dd9b460859ee6c6a1f`
- post-fix-04 A 원본 report SHA256: `81B878D7FC0ECC8B6CBD062E56960CDA8F75C662D8702B7B7EA74E30C7AF8B91`
- post-fix-04 B 원본 report SHA256: `ea097b2f2736a5e79d375eb477b2746d6ea03f9080b7e50ad103e614233c9ae1`
- 이번 수정: `.dark:root`·속성 selector 동치 표기와 지원 불가 토큰 selector 입력 경계, MDX JSX expression 내부의 배열·삼항·임의 tag template, fence opening run 길이와 닫힘 suffix, blockquote inline code 경계를 회귀 시험으로 고정

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 ecad460db93a9369d96435a28b6cb48dd7516ace
```

두 reviewer의 post-fix-05 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
