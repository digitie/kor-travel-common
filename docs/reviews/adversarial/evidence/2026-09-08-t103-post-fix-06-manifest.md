# T-103 수정 후 적대적 리뷰 6 기준선

- 리뷰 단계: post-fix-05 NO-GO finding 수정 후 여섯 번째 독립 재검토
- 불변 코드 후보 commit: `a40668bfb4ecac66d141da2ff791947d77208bd7`
- 불변 코드 후보 tree: `9c5cbf93bc6b34c4895c98745404375becbc0b32`
- post-fix-05 기준선 commit: `ecad460db93a9369d96435a28b6cb48dd7516ace`
- post-fix-05 기준선 tree: `6a903d346072ca951fe5146653addaa250fd44f5`
- post-fix-05 manifest commit: `93b9eb1dfac9a3f2629c04b87e4f3cdb29a59738`
- post-fix-05 A 원본 report commit: `bf3650f8d25320c34be27832a9cb45ccd9e682a4`
- post-fix-05 B 원본 report commit: `a9ae591aab83d84e1d7f52bf95555e0d85f89b1c`
- post-fix-05 A 원본 report SHA256: `9C01997B3DE5EB44DB9EFC3A28920288260F1A47173F2A95DA32BDE17A83C146`
- post-fix-05 B 원본 report SHA256: `01f3951c9d300c1b9149e2f4df5ec357270180f3ca47a136fbf4acbe447805e4`
- 이번 수정: selector 문법 공백과 문자열 값 공백을 분리하고 selector 대소문자를 보존하며 지원 밖 토큰 selector 목록을 입력 오류로 닫음, 다중행 JSX/ESM 실행 문맥·blockquote JSX·2자 inline code span을 회귀 시험으로 고정

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·다중행·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 94ca2f1730b270721eb6242bfcdd9362b51d45e5 a40668bfb4ecac66d141da2ff791947d77208bd7
```

두 reviewer의 post-fix-06 원본 report가 이 기준선 commit/tree와 일치한 뒤 최종 판정을 기록한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
