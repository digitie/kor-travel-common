# T-103 수정 후 적대적 리뷰 18 기준선

- 리뷰 단계: post-fix-17에서 확인한 Git diff의 U+2028/U+2029 가짜 hunk 경계 수정 후 열여덟 번째 독립 재검토
- 불변 코드 후보 commit: `31ad7a5876ff0d5714d4094cb4a402718d02a33f`
- 불변 코드 후보 tree: `60bbe9546e1561aa5aee4f0bfbdd834fdd9cf58c`
- post-fix-17 후보 commit: `34c0abfbdf695258d53a1015ff4b73926d1ebcd1`
- post-fix-17 후보 tree: `8bc05556808a5b970d8f0ac659f7fd934ac88167`
- post-fix-17 manifest commit: `1c6091d`
- post-fix-17 A 원본 report commit: `5ca0cf6e7c091e1c5ee0867a94194814244ea97d`
- post-fix-17 A 원본 report SHA256: `7C80A012943AD647611EA25402B79405FDCDDEC76F0B7FA5AD42CC541057EC0D`
- post-fix-17 B 원본 report commit: `309b613c6fa3bfc56e6fb0408fcbe1e56f83fc67`
- post-fix-17 B 원본 report SHA256: `4F9663944D96ACA60A4435AF0616A6D36912782330F56E6BBA5D8C9BB143AF65`
- 이번 수정: 소스 줄 번호 계약을 LF 기준으로 고정해 `splitlines()`의 U+2028/U+2029 분리를 제거하고, ESM 이전 행·untracked line count·Git diff hunk parser를 모두 같은 LF 규칙으로 맞췄다. 실제 추가행 P8이 `--base`에서 실패하는 두 줄 종결자 회귀 시험을 추가했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접/단항/키워드/논리/숫자/정규식/소수/연산자/유니코드/결합 문자/ZWNJ/ZWJ/Unicode escape/Other_ID_Start·Other_ID_Continue/구버전 Unicode `Cn`/U+FEFF/`async` arrow/CR/LF/U+2028/U+2029 줄 종결자/주석 선행 MDX expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가행·가짜 hunk 문자열, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check 6a274c1 31ad7a5876ff0d5714d4094cb4a402718d02a33f
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
