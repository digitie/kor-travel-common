# T-011 post-fix-3 독립 리뷰 B 원본

최종 verdict: **BLOCK**. 기존 공백·날짜 parity와 DEL 보고 문제는 수정됐다. 재귀 requirements 내부의 self-symlink 처리도 수정됐으나, 초기 scope 생성 단계의 self-symlink에서 새로운 B-P1-09를 재현했다.

## 기준선·격리·요청

- 실행 ID: `T011-POST3-B-20260907-202625-KST`.
- candidate: `e03d38faabfdb03b5b636ef78897b368df70d7a3`.
- parent/base: `767db839d8638c99a1034ebdd633e2a43b9794c6`.
- tree: `15dd9df9abb504b25991ea16e63902914935305c`.
- detached worktree: `F:/dev/kor-travel-common-wt/review-t011-post3-b`.
- 시작: `2026-09-07T20:26:25.9816040+09:00`.
- 종료: `2026-09-07T20:31:20.4565591+09:00`.
- 시작·종료 SHA/tree 일치와 clean 상태(`git status --porcelain=v1` 출력 없음)를 확인했다. source/candidate 파일·소비자 저장소를 수정하지 않았고 commit/push/게시를 하지 않았다. 임시 합성 입력만 별도 임시 디렉터리에 만들었다.
- source `.git/config`의 시작·종료 SHA256은 모두 `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A`다. 수정하지 않았다.
- 상대 reviewer의 이번 결과와 개별 원본은 읽거나 요청하지 않았다. 관련 코드·schema·회귀·task delta를 직접 읽었고 own corpus로 재검증했다.

요청 원문:

> 새 immutable candidate `e03d38f` (full SHA는 `git rev-parse e03d38f`로 확인)를 post-fix-3 독립 리뷰해 주세요. parent/base는 `767db839d8638c99a1034ebdd633e2a43b9794c6`입니다. 공백 path parity, requirements self-symlink RuntimeError, date schema parity, DEL lock path redaction 및 새로운 P0-P3 반례를 Windows/WSL에서 확인해 주세요. 상대 reviewer 결과는 읽지 말고 source checkout/.git/config는 수정하지 마세요. 시작/종료 SHA/tree/clean, 검증 명령·출력·NOT_RUN, 최종 PASS/BLOCK 원본을 확정해 주세요.

## 실제 검증

Windows Python 3.14.3은 `py -3.14 -B -X utf8`, WSL Python 3.11.15는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`으로 실행했다.

| 검증 | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -q` | 200 tests, 56.589초, OK, skip 0 | 200개 수집·198개 실행 성공·2개 skip, 36.144초 |
| plan | 106 tasks, 오류 0 | 동일 |
| 문서 링크 | 338문서·2,283 target, 오류 0 | 동일 |
| SPDX | 32파일, 오류 0 | 동일 |
| secret / production redaction | 각각 428파일, 발견 0·예외 0 | 동일 |
| registry self-check | exit 0 | exit 0 |

validator 명령: `tools/validate_plan.py`, `tools/validate_document_links.py`, `tools/check_spdx.py`, `tools/scan_secrets.py --all`, `tools/check_prod_redaction.py --all`, `tools/check_versions.py --self-check`. WSL 전체 시험에서 `GIT_DIR`·`GIT_WORK_TREE`·`GIT_COMMON_DIR`를 제거했다. Git 읽기가 필요한 validator subprocess에만 detached worktree의 Linux Git 경로를 주었다.

- `git diff --check HEAD^ HEAD`: exit 0. `.github`·`versions.json`·`LICENSE`·`NOTICE`는 parent 대비 불변.
- 기존 세 corpus `review-t011-b-cases.py`, `review-t011-post-b-cases.py`, `review-t011-post2-b-cases.py`를 이번 worktree에 대해 Windows/WSL에서 다시 실행했다. 파일은 주 checkout `.git/codex-audit/`에 있다.
- 이번 추가 corpus는 `.git/codex-audit/review-t011-post3-b-cases.py <이번 worktree>`다. 날짜 5,082개와 별도 날짜 edge 4개, self-symlink 위치 4종을 실행한다.
- 날짜 5,082개는 연도 0001·0004·0100·0400·1900·2000·2024·2026·2100·2400·9999, 월 00–13, 일 00–32를 조합해 `date.fromisoformat`의 실제 달력 판정과 대조했다. Windows Draft202012Validator의 isoDate schema와 불일치 0개, WSL schema pattern과 불일치 0개다.
- 끝 newline·끝 공백·전각 숫자·아랍어 숫자 날짜는 schema와 stdlib 모두 거절했다. 초기 schema 초안 10개는 Windows 실제 엔진에서 모두 통과했다.
- `gh run list --commit <candidate>` 및 `gh run view 34116567561 --json headSha,conclusion,jobs`: exact candidate, 5개 job success. [CI 실행](https://github.com/digitie/kor-travel-common/actions/runs/34116567561). 정상 CI를 아래 반례 해결 증거로 세지 않는다.

## 기존 finding disposition

| ID·경계 | 결과 |
|---|---|
| B-P1-01, B-P1-02, B-P1-03, B-P2-05 | FIXED 유지. 기존 field/scope 비밀 출력, 외부 동반 선언 symlink, workspace 선택, kind 타입 반례 모두 수정 결과 유지 |
| B-P2-04 | FIXED. 기존 경계 공백 5종·제어 문자·날짜 corpus가 양쪽에서 같은 결과를 냄. 정상 embedded space 경로는 계속 허용 |
| B-P1-06 | FIXED 유지. 외부 재귀 include와 외부를 가리키는 include symlink는 exit 2·보고서 없음, root 내부 shared include는 NO_LOCK report 유지 |
| B-P3-07 | FIXED 유지. 통합 집계 P1 3건·P2 4건은 변경되지 않음 |
| B-P2-08 | FIXED. DEL·tab·비밀 형식 문자열을 가진 전이 lock 경로 모두 stdout·JSON·Markdown·summary에 원문이 남지 않음 |
| 요청된 재귀 self-symlink | FIXED(해당 경로). 정상 requirements가 `-r loop.txt`로 self-symlink를 포함하면 양쪽 exit 2, traceback·보고서 없음 |

## B-P1-09 — 초기 scope의 self-symlink는 traceback·민감한 파일명을 출력함

- 심각도: P1. disposition: OPEN. 이번 신규 독립 finding.
- 위치: `tools/check_versions.py:1864`(직접 lock 경로), `:1799`(동반 선언), `:1812`(선언 전용 app), `:2837`(입력 오류 catch).
- 최소 재현: 임시 `repo/apps/etl/` 아래 requirements 파일을 자기 자신을 가리키는 symlink로 만든다. strict manifest는 이 파일을 `lockfiles[0].path`로 직접 지정한다. 파일명은 `'requirements-' + ('gh' + 'p_' + 'A' * 36) + '.txt'`처럼 합성 민감 값을 분할 생성했다. 원문 값은 로그·보고서에 기록하지 않고 포함 여부만 확인했다.
- 명령: `check_versions.py <repo> --manifest <repo>/manifest.json --mode fail --json <out.json> --no-step-summary`.
- WSL Python 3.11.15: **exit 1, traceback=true, 합성 민감 파일명 포함=true, JSON 생성=false**. `scopes_from_manifest`의 초기 `Path.resolve()`에서 발생한 RuntimeError가 main의 catch 범위 밖으로 나간다.
- Windows Python 3.14.3: 같은 입력은 **exit 1, traceback=false, JSON 생성=true, NO_LOCK**이다. 순환 symlink를 정상적인 lock 부재와 구분하지 못한다. 양쪽 모두 기대하는 안전한 입력 오류 exit 2와 다르다.
- 추가 위치 대조: lock 옆 `pyproject.toml` self-symlink도 WSL traceback/exit 1, Windows NO_LOCK report/exit 1이다. 빈 lockfiles에서 app 디렉터리 self-symlink는 WSL traceback/exit 1, Windows exit 2다. 반면 include 내부 self-symlink는 새 read_requirements 예외 변환 덕분에 양쪽 exit 2로 수정됐다.
- 영향: 원문 비공개가 필요한 입력 오류가 WSL 로그에 경로를 다시 노출하고, 동일 잘못된 입력의 report/exit 의미가 OS별로 달라진다. 이 finding은 실제 비밀 접근이나 코드 실행을 주장하지 않는다.
- 권고: 초기 root/manifest/lock/workspace/app/동반 선언의 resolve에도 공통의 안전한 경로 오류 처리를 적용한다. RuntimeError를 catch하는 것만으로는 Windows의 `resolve(strict=False)`·`is_file()`이 loop를 누락으로 처리하는 문제가 남으므로, 순환/오류 symlink와 정상 미존재 파일을 구분한다. 오류 메시지는 고정 진단으로 바꾸고 원 경로를 출력하지 않는다. 직접 lock·동반 선언·app·재귀 include 각각의 self-symlink와 일반 누락 파일을 Windows/WSL에서 회귀로 고정한다.

## NOT_RUN·한계

- WSL jsonschema 외부 엔진 2개 시험은 미설치로 skip됐다. 200개 전부 실행 성공이라고 세지 않는다. Windows 실제 엔진 실행과 WSL pattern 대조를 구분했다.
- 소비자 build/e2e/설치, 공용 패키지 실물 build/install, release tag/asset, npm/PyPI 게시: NOT_RUN(범위 밖). 소비자 저장소를 수정하지 않았다.
- 기존 duplicate JSON key/lock scope 허용은 이전과 같으며 이번에 별도 finding을 추가하지 않았다.
- 추가 범위를 확대하지 않고 위 하나의 재현된 입력 오류 경계에서 검토를 종료한다. 새 immutable 수정 후보의 재검토가 필요하며 본 후보는 BLOCK이다.
