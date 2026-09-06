# T-003 두 번째 post-fix Reviewer A 독립 재검토 원본

- Review ID: `2026-09-07-t003-post-fix-02`
- 실행 ID: `/root/reviewer_a` / `t003-postfix02-a-20260907T065023+0900`
- 전문 영역: 경로·SPDX·Python·실패 경계·회귀
- 시작: `2026-09-07T06:50:23.9140766+09:00`
- 검토 종료: `2026-09-07T06:52:33.2896120+09:00`
- Candidate: `a2c189185870b3b1ea124531feb36b59b5533f65`
- Base: `951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a`
- 격리: `F:/dev/kor-travel-common-wt/review-t003-a` detached worktree. 시작·종료의 실제 `git rev-parse HEAD`는 candidate와 일치하고 `git status --porcelain=v1` 출력은 모두 비었다.
- 독립성: 상대의 이번 원본·메시지·finding을 읽거나 요청하지 않았다. 이전 확정 판정은 재사용했다. 이 파일 하나만 주 checkout evidence에 작성하고 코드·정책·이전 원본·소비자·다른 에이전트 변경은 보존했다. 추가 subagent 없음.
- 최종 verdict: **PASS**. A finding 3건 모두 FIXED 또는 FIXED 유지, 신규 finding 없음.

## 요청 원문

> T-003 두 번째 post-fix 독립 재검토입니다. 공통 manifest F:/dev/kor-travel-common/docs/reviews/adversarial/evidence/2026-09-07-t003-post-fix-02-manifest.md. candidate a2c189185870b3b1ea124531feb36b59b5533f65, base 951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a, 기존 review-t003-a detached에 준비했습니다. A-T003-P1-01 확장자 경계 수정과 전체 10파일 delta·기존 수정 회귀를 확인하세요. Windows/WSL 작성자 100 tests 성공이지만 직접 경계를 재현하세요. 이번 상대 결과 미열람 상태로 자기 원본 docs/reviews/adversarial/evidence/2026-09-07-t003-post-fix-02-reviewer-a.md만 작성합니다. ID·시각·요청 원문·실제 SHA/clean·finding disposition·검증/NOT_RUN·verdict 포함. 다른 에이전트가 있으니 제품·문서·다른 파일·소비자 변경이나 되돌리기 금지. 이번 사용자 GPLv3 통일 예정은 미래 방향 기록이며 현재 원천/권리 gate 변경은 없습니다.

[공통 manifest](2026-09-07-t003-post-fix-02-manifest.md)와 전체 10파일 delta(220 insertions/4 deletions)를 읽었다. 원본 finding과 직전 잔여 재현은 [최초 A](2026-09-07-t003-reviewer-a.md), [직전 A](2026-09-07-t003-post-fix-reviewer-a.md)에 보존돼 있다.

## 원 finding별 disposition과 직접 재현

| Finding | 이번 판정 | 독립 확인 |
|---|---|---|
| A-T003-P1-01 경로 별칭·확장자 잔여 | **FIXED** | source 확장자와 `.editorconfig` 식별이 casefold되어 `.PY` 행도 실제 파일 대소문자 검사에 도달한다. 끝 점/공백은 별도로 거부한다. 기존 잘못된 표기가 모두 exit 1이며 실제 대문자 파일의 정확한 등록은 exit 0 |
| A-T003-P1-02 qualified geo·색인 -only | **FIXED 유지** | qualified geo·대문자 geo·다른 저장소의 -only 원천 각각에서 잘못된 -or-later 1, 올바른 -only/AND 0 |
| A-T003-P2-03 PV 표 공백 | **FIXED 유지** | 공백 1개·3개·tab에서 누락 Origin 1, 정상 Origin 0 |

Windows Python 3.14.3과 WSL Python 3.14.4 각각 독립 임시 디렉터리를 만들어 **26개씩, 총 52개 CLI 사례**를 실행했다. 각 실행의 실제 exit를 기대값과 assertion으로 대조했고 모두 일치했다. 파일은 `TemporaryDirectory`로 생성·정리했으며 소비자 파일을 사용하지 않았다.

| 사례 묶음 | OS별 건수 | 실제 결과 |
|---|---:|---|
| 정상 경로의 Origin 누락, `./`, 중복 `/`, 디렉터리/stem 대소문자, `.PY`, `SAMPLE.PY`, 끝 점/공백 | 9 | 전부 exit 1 |
| 실제 `.editorconfig`의 `.EDITORCONFIG` 별칭 | 1 | exit 1 |
| 실제 `tools/sample.PY`와 색인의 정확한 동일 경로·정상 Origin | 1 | exit 0 |
| qualified/대문자 geo·다른 repo의 색인 -only × 잘못된/only/AND 헤더 | 9 | 각각 1/0/0 |
| 공백 1개·3개·tab × 누락/정상 Origin | 6 | 각각 1/0 |

직전 P1 재현과 같은 `tools/sample.PY` 색인 + 실제 `tools/sample.py` + 기본 SPDX/저작권만 있는 fixture가 이제 Windows·WSL 모두 실패한다. 잘못된 별칭을 막는 대신 정상 대문자 소스를 제외하거나 Python/TS/CSS 주석을 오인하는 회귀도 없다. 전체 시험의 새 `test_uppercase_source_extensions_keep_comment_syntax`가 `.PY`·`.TSX`·`.CSS` 3개를 실제 CLI로 검사해 성공하며, 직접 실행한 대문자 등록 사례도 통과했다.

## 전체 delta 검토

- 코드 변경은 source 확장자/특수 파일 이름·주석 문법 판별의 casefold와 색인 경로 끝 점/공백 거부다. licensing §5.2의 대소문자 무관 대상 검사와 일치한다. 나머지 Origin/Modified/Derived-From 및 geo 판정은 이전 수정 상태를 유지한다.
- 원문 사본·NOTICE·PROVENANCE·서드파티 목록·설정 전달 절차·CI에는 diff가 없다. 이전 B finding의 수정 이력·전달 계약을 뒤집지 않는다.
- journal은 새 항목을 위에 추가했다. base의 이전 첫 H2부터 끝까지가 candidate와 동일함을 Python으로 대조했다. 이전 두 원본·manifest·통합 판정은 새 이력으로 보존되며 당시 BLOCK을 PASS로 덮어쓰지 않는다.
- T-003은 IN_PROGRESS이고 상세 evidence는 이번 수정의 독립 재확인 전 완료하지 않는다고 기록한다. 제품·소비자·T-009 CI 연결의 후속 gate를 닫지 않는다.
- 모든 라이브러리 GPLv3 통일 예정은 journal의 미래 방향 기록뿐이다. 현재 common의 -or-later와 geo의 -only, 원문 사본·권리 gate에는 변경이 없다.

## 실제 검증

| 환경·명령 | 결과 |
|---|---|
| Windows `python --version` | Python 3.14.3 |
| Windows `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 100 tests, 6.619초, OK, skip 0 |
| WSL Ubuntu-26.04 `python3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.4, 100 tests, 5.003초, OK, skip 0 |
| Windows `python -B -X utf8 tools/check_spdx.py` | exit 0, 13개 파일·오류 0 |
| Windows 문서/plan validator | 각각 exit 0, 223개 문서·1874개 local target·오류 0, 96개 상세 task·오류 0 |
| WSL uv managed Python 3.11.15 전체 unittest | 100 tests, 5.564초, OK, skip 0, exit 0 |
| WSL Python 3.11.15 SPDX·문서·plan | 각각 exit 0, SPDX 13개·오류 0, 문서 223개/1874 target·오류 0, task 96개·오류 0 |
| `git diff --check 951b4432bc8eb4391caf15ad0eb2e8f8f58eb02a HEAD` | exit 0, 출력 없음 |
| `git diff --quiet <base> HEAD -- LICENSES PROVENANCE.md NOTICE THIRD_PARTY_NOTICES.md templates .github` | exit 0, 해당 원문·고지·전달·CI 불변 |
| `gh pr view 2 --json number,isDraft,headRefOid,statusCheckRollup` | [PR #2](https://github.com/digitie/kor-travel-common/pull/2) draft, candidate head 일치. [CI run 34062228366](https://github.com/digitie/kor-travel-common/actions/runs/34062228366)의 validate-docs SUCCESS |

Python 3.11 추가 검증은 coordinator가 런타임 존재를 알려 준 뒤 직접 수행했다. 최초 WSL `uv run --no-project --python 3.11 ...` 호출은 `uv: command not found`로 실패했다. `Path.home() / '.local/bin/uv'`가 실제 존재함을 확인한 뒤 `/home/digitie/.local/bin/uv run --no-project --python 3.11 python ...`으로 `--version`, SPDX·문서·plan 및 전체 unittest를 실행했다. 성공한 3.11 결과는 작성자의 실행을 재사용한 수치가 아니다. 이전 Python 3.11 NOT_RUN은 이번 candidate의 위 직접 검사로 해소됐다.

## 한계와 최종 판정

원문 재다운로드·소비자 원본 재대조·고지 전달 fixture의 새 실행은 **NOT_RUN(관련 파일 불변, 이전 확정 원본의 검증 재사용)**이다. Windows 네이티브 ACL/심볼릭 링크의 추가 검사, SPDX 필수 CI·Windows matrix(T-009), 패키지 build·pack/wheel·소비자 설치/e2e/배포는 **NOT_RUN**이며 기존 후속 gate로 유지한다. 현재 validate-docs 성공은 그 gate의 성공이 아니다.

**PASS. A finding 3건 모두 닫혔고 신규 finding은 없다.** 이 판정은 위 immutable candidate의 T-003 코드·문서 변경에 한정하며, 완료 원장 이동·최종 review 기록과 이후 commit의 CI/PR 정합은 coordinator의 종료 작업이다. 제품 릴리스나 다른 저장소 변경 승인으로 확대하지 않는다.
