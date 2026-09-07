# T-005a post-fix 독립 리뷰 B 원본

- 실행 ID: `B-T005A-POST-20260907-122151-9027500`
- 판정: **BLOCK**. `B-P1-01` FIXED, `B-P1-02` OPEN(기존 재현은 수정됐으나 유효한 branch 이름으로 우회 가능). 별도 새 finding ID는 없다.
- 시작: 2026-09-07T12:21:51.3042822+09:00. 종료: 2026-09-07T12:25:25.3157322+09:00.
- immutable candidate: `902750016d157bb195fb05c01358c4b8a6ffe812`. 실제 시작·종료 HEAD와 일치한다.
- base: `6e1881b86f017d604ccfa416bd368e5aba24c669`. candidate tree: `0e3d4517540a9f707d3996dd638c5d518fbf3380`.
- 새 detached worktree: `F:/dev/kor-travel-common-wt/review-t005a-post-b`. `git worktree add --detach ... 9027500`으로 생성했다. 시작·종료 `git status --porcelain=v1` 출력은 비어 있었다.
- 후보·제품·소비자 파일을 수정하지 않았다. 합성 입력 및 고정 소비자 Git object 사본은 임시 디렉터리에서만 검사했다. 원본 보고서는 지정된 `.git/codex-audit` 경로에만 작성했다.
- 초기 B 원본만 읽었다. 이번 A 결과와 다른 reviewer 결과를 읽거나 요청·공유하지 않았다.

## 전달 요청 원문

> T-005a post-fix 독립 리뷰를 시작해 주세요. immutable candidate는 `9027500`이며 base는 `6e1881b86f017d604ccfa416bd368e5aba24c669`입니다. 새 detached worktree `F:/dev/kor-travel-common-wt/review-t005a-post-b`를 candidate에서 만들고 clean 시작/종료 SHA를 기록하세요. 초기 B finding(B-P1-01/02)을 읽되 A 결과나 다른 리뷰 결과는 읽거나 공유하지 말고, uv lock git ref 고정·복수 marker/source·branch/tag/rev 의미·Python requires floor·versions.json 대조와 회귀를 중심으로 공격적으로 재현하세요. Windows와 WSL 전체 테스트 및 관련 validator를 실행하고 실제 소비자 쓰기는 하지 마세요. 결과는 `.git/codex-audit/2026-09-07-t005a-post-fix-reviewer-b.md`에 원본 보고서로 남기고, PASS/BLOCK과 finding ID·재현·NOT_RUN을 메시지로 보고하세요. 수정은 하지 마세요.

후속 메시지에서 full SHA `902750016d157bb195fb05c01358c4b8a6ffe812`를 전달받았으며 실제 HEAD와 일치함을 확인했다.

## 검토 범위·재사용

base 대비 10파일(385행 추가·48행 삭제)의 경계와 초기 후보 대비 3파일(171행 추가·39행 삭제) 전체 수정 내용을 확인했다. 변경된 코드·회귀 시험·버전 정본을 직접 읽고 T-005a 수용 기준과 resume의 IN_PROGRESS·common 범위를 대조했다. `versions.json`, AGENTS, docs/README는 base와 동일하므로 앞 리뷰의 읽기 결과를 재사용했다. Python floor 3.11, uv floor 0.11/recommended 0.12와 미지원 형식의 입력 오류 정책을 유지한다.

초기 후보 SHA를 첫 diff 명령에 옮길 때 한 문자를 누락하여 조회에 실패했다. 이후 `3bc0f47`로 재조회해 3파일 delta를 읽었으며 실패한 명령을 성공 검증으로 세지 않았다. 초기 리뷰의 고정 uv source·공식 Git branch/tag/rev 의미 대조는 재사용했다. 새 네트워크 조회·실제 uv 설치는 수행하지 않았다.

## 실행 결과

| 명령·검사 | 결과 |
|---|---|
| Windows `py -3.14 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.14.3, 140 tests, 33.333초, OK, skip 0 |
| WSL `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | Python 3.11.15, 140 tests, 14.921초, OK, skip 0 |
| Windows·WSL 각각 `tools/validate_document_links.py` | 각각 269문서·2150대상·오류 0 |
| Windows·WSL 각각 `tools/validate_plan.py` | 각각 102 task·오류 0 |
| Windows·WSL 각각 `tools/check_spdx.py` | 각각 20파일·오류 0 |
| Windows `tools/check_versions.py --self-check` | exit 0, 레지스트리 자체 검사 통과 |
| `git diff --check 6e1881b86f017d604ccfa416bd368e5aba24c669 HEAD` | 출력 없음, exit 0 |
| 독립 Windows Git CLI 주입 9개 | 아래 disposition의 누락·짧은 SHA, 정상 SHA, 두 marker 순서 교체, 원 branch, `@` 및 `%40` branch, 전체 rev를 직접 실행 |
| WSL에서 `branch="topic@v1.2.3"` CLI 재현 | custom-lib OK, fail 모드 exit 0, error annotation 없음; Windows와 동일한 우회 |
| 독립 Python 하한 5개·marker registry 1개 | 아래 결과 |
| airport 고정 Git object 임시 사본 | 아래 digest와 14행 OK 재현; 소비자 원본에 쓰지 않음 |

Windows·WSL의 전체 시험 140개는 같은 시험 집합이다. 280개 서로 다른 시험으로 집계하지 않는다. WSL은 `wsl.exe --exec bash -lc`로 격리 worktree의 `/mnt/f/.../review-t005a-post-b`에 진입하고 위 절대 Python 경로로 실행했다. 모든 Python 실행에 `-B -X utf8`를 사용했다.

Python 하한 직접 대조:

| manifest / lock 하한 | 결과 |
|---|---|
| `>=3.12` / `>=3.10` | manifest OK, lock BELOW_FLOOR |
| `>=3.10` / `>=3.12` | manifest BELOW_FLOOR, lock OK |
| `>=3.11` / `>=3.11` | Python 3.11 OK |
| `>=3.12` / `>=3.12,!=3.13.*` | 지원하지 않는 범위이므로 ValueError |
| `>=3.12` / 빈 문자열 | ValueError |

fastapi registry 항목 두 개(0.114.0·0.141.1, platform marker 포함)는 각각 BELOW_FLOOR·OK로 남았다. 공유 lock·dependency group·복수 source·virtual source 및 기존 npm 회귀는 전체 140개 시험에 포함해 양 플랫폼에서 실행했다.

airport는 `2bb1111fc322843de40a35276613feb4d67bac5b`의 `backend/pyproject.toml`과 `backend/uv.lock`을 `git show`로 바이트 캡처했다. SHA-256은 각각 `770a59163b17cbb9139fba6e0f7230fd0c3a5c86adf7d3dd27426a02a9e62103`, `d4488e8ea8dffd71bd71e38cc7460786e6d0cc1e651c56ae7422ed26a857c2f5`로 초기 입력과 동일하다. 새 checker에서도 14행 모두 OK였다. 이 값은 고정 입력의 정적 대조이며 현재 소비자 환경의 검증 결과가 아니다.

## 원 finding disposition

### B-P1-01 — FIXED

원 심각도 P1을 유지한다. `tools/check_versions.py:762`에서 선언 고정과 lock 고정을 함께 확인하고 `:1059` 이후 모든 Git lock 항목을 순회한다.

초기와 같은 `tag="v1.2.3"` 선언에 SHA 없는 lock source를 주입하면 FLOATING_REF·error annotation·fail exit 1이다. 7자리 SHA도 같은 결과다. 서로 다른 marker의 두 Git 항목에 전체 SHA와 누락을 하나씩 넣고 순서를 뒤집어도 FLOATING_REF와 OK 두 행이 유지되고 exit 1이다. 40자리 전체 SHA만 있는 양성 대조와 `rev` 전체 SHA 선언은 OK·exit 0이다. 초기 반례가 모두 해소됐다.

### B-P1-02 — OPEN, 원 branch 종류 보존 결함의 잔여 우회

원 심각도 P1을 유지한다. 새 ID로 나누거나 심각도를 낮추지 않는다.

- 위치: `tools/check_versions.py:999`의 `branch:` 문자열 접두와 `:585`의 `path.rsplit("@", 1)[1]`, `:762`의 선언 판정.
- 원 반례 `branch="v1.2.3"`는 이제 FLOATING_REF·error annotation·fail exit 1이다.
- 그러나 Git이 허용하는 `branch="topic@v1.2.3"`를 사용하면 내부 표현이 `git+https://github.com/example/custom-lib.git@branch:topic@v1.2.3`이 된다. 마지막 `@` 뒤만 버전형 태그로 판정하므로 branch 종류 표시가 다시 사라진다.
- `git check-ref-format --branch 'topic@v1.2.3'`는 exit 0으로 성공했다. 비정상 Git 이름을 전제로 한 반례가 아니다.
- 재현 입력: `requires-python=">=3.12"`, `dependencies=["custom-lib"]`, `[tool.uv.sources] custom-lib={git="https://github.com/example/custom-lib.git", branch="topic@v1.2.3"}`. lock은 version 1/revision 3, 같은 Python 하한, 해당 package의 `source.git="https://github.com/example/custom-lib.git?branch=topic%40v1.2.3#<40자리 SHA>"`로 둔다. 실제 합성 SHA는 Python `'a' * 40`으로 만들었다.
- 명령: 해당 임시 디렉터리에 대해 `tools/check_versions.py <임시 입력> --repo weather --mode fail --no-step-summary --json <임시 보고>`를 실행한다.
- 실제 결과: Windows Python 3.14.3·WSL Python 3.11.15 모두 Python OK·custom-lib OK, exit 0, error annotation 없음. `branch="topic%40v1.2.3"`도 Windows에서 같은 결과였다.
- 기대: T-005a와 버전 정본 §3.8에 따라 명시적 branch는 lock SHA와 이름 형태에 무관하게 FLOATING_REF여야 한다.
- 영향: 유효하고 이동 가능한 branch가 필수 fail gate를 계속 통과한다. source 배열도 동일한 문자열 변환을 사용한다.
- 권고: branch 종류를 URL 문자열에 특수 접두로만 끼워 넣지 말고 구조적 값 또는 명시적 branch 판정으로 보존한다. 마지막 `@` 및 URL 디코딩이 branch 종류를 바꾸지 않도록 `topic@v1.2.3`, `%40`, 정상 tag·rev를 함께 대조하는 회귀 시험을 둔다.

## NOT_RUN·경계·최종 판정

NOT_RUN: 이 후보의 원격 CI 조회, 실제 `uv sync --locked`, 모든 upstream lock 생성 형식의 동등성 시험, 소비자 설치·빌드·e2e·배포·registry 게시. 실제 소비자 파일 변경은 하지 않았다. Windows·WSL 전체 시험과 validator는 실행했으므로 NOT_RUN에 포함하지 않는다.

후보와 과거 원본을 수정하지 않았다. 다른 reviewer의 결과를 읽지 않은 상태로 이 결과를 확정했다. **BLOCK**: B-P1-02를 수정하고 새 immutable 후보에서 원 reviewer 재확인을 받기 전 완료·merge로 처리할 수 없다.
