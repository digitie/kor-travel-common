# T-103 수정 후 적대적 리뷰 12 기준선

- 리뷰 단계: post-fix-11에서 확인한 MDX 표현식 시작 문법 우회 수정 후 열두 번째 독립 재검토
- 불변 코드 후보 commit: `386d815f54b79102954a695b0d65dda093bdfbec`
- 불변 코드 후보 tree: `1236efa499a5a8fd75198745e4e3161f39cfcf33`
- post-fix-11 코드 후보 commit: `c0c93c47e5f25aa0879fd0fb4e56261f6f624138`
- post-fix-11 코드 후보 tree: `f9b16a3d03f3fca49ba8048cc9d0328e78aadda4`
- post-fix-11 manifest commit: `f21b200`
- post-fix-11 A 원본 report commit: `fc12b5c8f6ad7f9f846cdb90989bb70a229a872e`
- post-fix-11 A 원본 report SHA256: `BC4E900E659412E8AB0F53EF6C7DD2DEDEC1D0A588757B8E5C6D55C7AA7FEA3D`
- post-fix-11 B 원본 report commit: `dda403194b6c372ac8997e26059cf3b158df6378`
- post-fix-11 B 원본 report SHA256: `49500d49d2740e546ff1f63d4b5207f3797ff95b1e55d9430969ff6d83f204aa`
- 누적 raw 기준선(post-fix-08) A commit: `0e9e2dad84759afcd3728756c73f35580054e029`
- 누적 raw 기준선(post-fix-08) B commit: `0da67bb82a1044c524bafbf413425850bcc61021`
- 이번 수정: 미종결 Markdown span 뒤 MDX 중괄호 표현식을 공백·JavaScript 주석 뒤의 단항 연산자, 숫자, 키워드, 논리식, 문자열·배열·객체·JSX 시작까지 보존하도록 재개 판정을 일반화했다. `window.confirm`의 직접 호출·단항·키워드·논리·주석 선행 최소 반례를 회귀 시험에 추가했다.

## 재검토 범위

동일한 두 reviewer가 새 불변 후보에서 CSS selector 정규화·specificity·조건 교집합·주석 gap·빈 목록과 descendant 오류, JSON 숫자·깊이·오류 채널, `--json=` 입력 redaction, MDX inline·blockquote·fenced·tilde·tagged·배열·삼항·중첩 object·다중행·들여쓰기 없는 ESM·JS 주석·문단 밖 delimiter·같은 문단의 미종결 span 뒤 HTML/JSX·직접 MDX expression·단항/키워드/논리/숫자/주석 선행 expression·여러 줄 JSX expression·blockquote 빈 문단·파일 첫 span·3자 inline span·backslash delimiter·escaped template과 보간 주석, Git diff 추가 행, symlink root, airport task/evidence를 Windows Python 3.14와 WSL Python 3.11에서 독립 재현한다. 소비자 저장소, npm/PyPI registry, workflow dispatch와 실제 소비자 build/e2e는 호출하지 않는다.

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
git diff --check e47f48e 386d815f54b79102954a695b0d65dda093bdfbec
```

두 reviewer는 이 manifest와 candidate commit/tree를 읽은 뒤 상대 결과를 보지 않고 각각 원본 report를 확정한다. 실행하지 않은 소비자 gate와 registry·게시 검증은 `NOT_RUN`으로 유지한다.
