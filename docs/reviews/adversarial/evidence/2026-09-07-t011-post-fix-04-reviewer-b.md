# T-011 post-fix-4 독립 적대적 리뷰 B 원본

- 실행 ID: `T011-POST4-B-20260907-203608-KST`
- 판정: **BLOCK**. 새 P2 finding 1건(B-P2-10). 기존 B-P1-09의 직접 경로 반례 3종은 수정됐지만 중간 디렉터리 symlink 순환은 Windows에서 일반 report로 처리된다.
- 시작: `2026-09-07T20:36:08.6006604+09:00`; 종료: `2026-09-07T20:42:12.9922047+09:00`.
- candidate: `22f9333b5f3b7d61cf7af5d454d396c2b15dc540`
- tree: `b5c6e77e2ff1f0481f889550896932aa5dd254c6`
- parent/base: `e03d38faabfdb03b5b636ef78897b368df70d7a3`
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post4-b` detached worktree. 시작·종료 SHA/tree 동일, 두 번의 `git status --porcelain=v1` 출력 모두 빈 값.
- source `.git/config` 시작·종료 SHA256 동일: `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A`.
- 후보·소비자 파일 수정, commit, push, registry 게시 없음. 반례 입력은 OS 임시 디렉터리, 자체 실행 스크립트와 이 원본은 기본 checkout의 `.git/codex-audit`에만 저장했다. 상대 reviewer 원본과 결과는 읽지 않았다.

## 전달 요청 원문

> 새 immutable candidate `22f9333b5f3b7d61cf7af5d454d396c2b15dc540`를 post-fix-4 독립 리뷰해 주세요. parent/base는 `e03d38faabfdb03b5b636ef78897b368df70d7a3`입니다. lockfiles path 자체·동반 선언·app self-symlink가 양 OS에서 일반 exit 2 입력 오류가 되는지, 기존 모든 반례와 새 P0-P3를 확인해 주세요. 상대 결과는 읽지 말고 source checkout/.git/config는 수정하지 마세요. 시작/종료 SHA/tree/clean, 검증 명령·출력·NOT_RUN, 최종 PASS/BLOCK 원본을 확정해 주세요.

## 검토 범위와 실행

코드·시험 delta와 관련 strict manifest/버전 계약을 읽었다. 이번 5개 변경 파일 중 상대 원본은 읽지 않았고, 이전에 검토한 불변 schema/표준은 직접 반례 회귀로 재검증했다. `_resolve_input_path`, `scopes_from_manifest`, `_safe_declared_file`, app 선언 scope, workflow/root resolution 및 CLI 오류 경로를 확인했다.

Windows Python 3.14.3 명령은 worktree에서 `py -3.14 -B -X utf8` 접두사로 실행했다. WSL Ubuntu-26.04는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`(3.11.15)을 사용했다. WSL 전체 unittest에서는 `GIT_DIR`, `GIT_WORK_TREE`, `GIT_COMMON_DIR`를 해제해 테스트가 만드는 Git fixture와 분리했다. 읽기 전용 WSL validator에만 해당 worktree의 Git 메타데이터 경로를 명시했다. Git 설정 파일은 수정하지 않았다.

| 명령 또는 검사 | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -q` | 200 tests, 56.922초, OK, skip 0 | 200개 발견, 35.307초, 198개 실행 성공·2개 skip |
| `tools/validate_plan.py` | 상세 task 106, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 문서 341, local target 2285, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32개, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 431개, 발견 0, 예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 431개, 발견 0, 예외 0 | 동일 |
| `tools/check_versions.py --self-check` | 자체 검사 통과 | 동일 |
| `git diff --check <base> <candidate>` | exit 0, 출력 없음 | 별도 실행하지 않음 |

`.git/codex-audit`의 자체 스크립트 `review-t011-b-cases.py`, `review-t011-post-b-cases.py`, `review-t011-post2-b-cases.py`, `review-t011-post3-b-cases.py`를 두 OS에서 이번 candidate 경로를 인자로 다시 실행했다. 주요 결과는 다음과 같다.

- 직접 lock self-symlink, 동반 `pyproject.toml` self-symlink, app self-symlink, recursive requirements self-symlink 모두 exit 2, traceback 없음, 합성 민감값 출력 없음, JSON report 생성 없음.
- 선택 workspace의 member package 선언을 읽고 root의 더 높은 Node 선언에 가려지지 않는 BELOW_FLOOR 확인. 외부 companion/lock/manifest/workflow symlink는 exit 2.
- strict requirements 직접·재귀 root escape는 exit 2, 외부 선언을 읽은 report 없음. 정상 root 내부 include는 기존 판정을 유지.
- kind 배열/객체는 validation 오류이며 TypeError traceback 없음. 민감 unknown field, scope 및 전이 lock 경로는 stdout·JSON·Markdown·step summary에서 원문 미노출.
- 전이 scope의 tab/DEL과 합성 민감 문자열 모두 출력 채널에서 제거됨. manifest 제어문자와 앞뒤 공백 경로는 schema/stdlib에서 거부; 내부 정상 공백 경로는 허용.
- 달력 반례 5,082개에서 schema 날짜 정규식/stdlib calendar 기대 불일치 0. Windows는 실제 Draft202012Validator를 사용했고, WSL은 정규식만 직접 실행했다. 개행/뒤 공백/전각·아랍 숫자 날짜도 모두 거부.
- 10개 draft는 Windows의 실제 JSON Schema 검증에서 모두 유효. WSL JSON Schema 외부 엔진은 미설치로 재사용하거나 통과로 계산하지 않음.

정확한 candidate의 `gh run list --commit <candidate>` 및 `gh run view 34117388862 --json headSha,conclusion,jobs`를 직접 조회했다. head SHA 일치, run success, `tools (windows-2025)`, `tools (ubuntu-24.04)`, `secret-scan`, `check-versions`, `docs` 5개 job success를 확인했다. URL: https://github.com/digitie/kor-travel-common/actions/runs/34117388862 . 이는 CI 관찰이며 추가 직접 반례가 CI에 포함됐다는 뜻은 아니다.

## 기존 finding disposition

| 원 ID·심각도 | disposition | 이번 확인 |
|---|---|---|
| B-P1-01 | FIXED | unknown field/scope 원문 비공개 |
| B-P1-02 | FIXED | 외부 companion symlink exit 2 |
| B-P1-03 | FIXED | 실제 npm member 선언 선택 |
| B-P2-04 | FIXED | path/date schema와 stdlib 회귀·달력 corpus |
| B-P2-05 | FIXED | kind 배열/객체 입력이 traceback 없이 거부됨 |
| B-P1-06 | FIXED | requirements 재귀 root containment |
| B-P3-07 | FIXED 유지 | 이전 집계 정정은 이번 delta에서 변경되지 않음 |
| B-P2-08 | FIXED | DEL/tab 전이 scope의 모든 report 출력 원문 미노출 |
| B-P1-09 | FIXED | 원 직접 lock·companion·app self-symlink가 양 OS exit 2, traceback/원문/report 없음 |

## 새 finding B-P2-10 — 경로 중간 symlink 순환을 Windows에서 누락 파일로 분류

- 심각도: **P2**, disposition 권고: **수정 필요**.
- 위치: `tools/check_versions.py:1371` (`_resolve_input_path`), `:1813` (동반 선언 leaf 검사), `:1886` (lock leaf 검사), `:1898` (workspace resolve).
- 원인: `_resolve_input_path`는 기본 `strict=False`인 `Path.resolve()`에 의존한다. Windows Python 3.14는 순환을 미해결 경로로 반환할 수 있다. 후속 `is_symlink()`는 마지막 요소만 검사하므로 `loop/requirements.txt`의 부모 `loop`나 npm workspace 자체의 순환은 놓친다. leaf `is_file()`가 false가 되며 NO_LOCK scope/report로 처리된다.
- 최소 재현 A: 정상 strict v1 pinvi manifest, `lockfiles=[{"kind":"requirements","path":"loop/requirements.txt","scope":"apps/etl"}]`. 임시 root에서 `loop.symlink_to(loop, target_is_directory=True)`로 중간 디렉터리 self-symlink 생성. 실제 앱 디렉터리는 정상이다.
- 최소 재현 B: 정상 `package-lock.json`(lockfileVersion 3), `lockfiles=[{"kind":"npm","path":"package-lock.json","scope":"loop"}]`; `loop` workspace 디렉터리가 같은 self-symlink다.
- CLI 공통: `check_versions.py <root> --manifest <root>/manifest.json --mode <fail|report|warn> --json <root>/out.json --no-step-summary`.

| A·B 양 반례 결과 | Windows 3.14.3 | WSL 3.11.15 |
|---|---|---|
| fail | exit 1, JSON 생성, NO_LOCK | exit 2, JSON 미생성 |
| report | exit 0, JSON 생성, NO_LOCK | exit 2, JSON 미생성 |
| warn | exit 0, JSON 생성, NO_LOCK | exit 2, JSON 미생성 |
| traceback | 없음 | 없음 |

원본 입력값 유출은 이 새 반례에서는 관찰되지 않았다. 영향은 구조상 해석할 수 없는 입력이 Windows에서 모드에 따라 성공 종료하는 일반 비교 report로 바뀌고 양 OS 입력 오류 계약이 달라지는 것이다. 정상 누락 부모 디렉터리 control은 양 OS 모두 기존 NO_LOCK/모드 exit를 유지했다. 정상 root 내부 디렉터리 symlink control도 기존 requirements 판정을 유지했으므로 모든 symlink 또는 일반 누락 경로를 일괄 거부할 필요는 없다.

실행 스크립트: `.git/codex-audit/review-t011-post4-b-cases.py`. 두 OS에서 candidate worktree 경로와 각 mode를 인자로 실행했다. 예: `py -3.14 -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/review-t011-post4-b-cases.py F:/dev/kor-travel-common-wt/review-t011-post4-b report`. WSL에서는 두 경로를 `/mnt/f/...`로 바꾸고 위 3.11 실행기를 사용한다.

최소 수정 권고: 입력 경로의 leaf뿐 아니라 중간 경로 구성 요소/선택 workspace를 안전하게 해석하고 순환·I/O 실패를 일반 누락 파일과 구분해 기존 원문 없는 ValueError로 변환한다. 정상 누락 입력과 정상 root 내부 링크를 보존하며 A·B를 report/warn/fail 및 Windows/WSL 양쪽 회귀에 추가한다.

## NOT_RUN과 판정 한계

- NOT_RUN: WSL의 외부 `jsonschema` 엔진 검증 2건(모듈 미설치). skip은 pass로 계산하지 않았다. 동일 후보의 Windows 실제 엔진 검사와 WSL 직접 정규식/date corpus를 별도 기록했다.
- NOT_RUN: 소비자 원본 쓰기·실제 채택/빌드·npm/PyPI 게시·릴리스. common 도구 리뷰 범위 밖이다.
- NOT_RUN: 별도 WSL `git diff --check` 및 CI job 내부 모든 로그의 재독. Windows exact diff check와 CI exact SHA·5개 job 상태를 직접 확인했다.
- P0/P1 새 finding 없음. 기존 원 반례 수정에도 B-P2-10이 재현되어 최종 **BLOCK**. 후보와 source 설정은 보존했다.
