# T-011 post-fix-4 독립 리뷰 A 원본

- 실행 ID: A-T011-POST4-20260907-203542
- 최종 판정: **BLOCK**. 기존 A-T011-P2-10은 FIXED이며 새 P2 1건을 확인했다.
- Candidate: `22f9333b5f3b7d61cf7af5d454d396c2b15dc540`
- Parent/base: `e03d38faabfdb03b5b636ef78897b368df70d7a3`
- 시작·종료 SHA: candidate와 동일. 시작·종료 tree: `b5c6e77e2ff1f0481f889550896932aa5dd254c6`.
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post4-a`, 새 detached worktree. 시작·종료 `git status --porcelain=v1` 빈 출력.
- 시작 KST: 2026-09-07 20:35:42.154 +09:00
- 종료 KST: 2026-09-07 20:41:31.550 +09:00
- 요청 범위: lockfiles path 자체·동반 선언·app self-symlink의 양 OS 일반 exit 2 처리, 기존 반례와 인접 P0~P3 경계. SHA/tree/clean·명령·출력·NOT_RUN 및 PASS/BLOCK을 독립 확정한다.
- 독립성: 상대 reviewer 원본/결과를 읽거나 요청하지 않았다. 후보·source checkout 파일·`.git/config`·소비자는 수정하지 않았다. worktree 메타데이터와 후보 밖 A probe/report만 작성했다. 기존 uv 임시 환경을 이용했으며 commit/push/게시 없음.

## 기존 finding disposition

A-T011-P1-01/02, P2-03/04/05/06/07, P1-08, P3-09, P2-10/11은 **FIXED**로 판정한다. 원 ID와 심각도는 변경하지 않는다.

- 이전 requirements 내부 `-r loop.txt`와 직접 requirements/npm lock 경로의 자기 symlink는 두 환경에서 exit 2, traceback 없음이다.
- 동반 package.json/pyproject.toml과 app 디렉터리 자체의 자기 symlink도 두 환경에서 exit 2, JSON report 없음이다.
- manifest·registry·입력 root 자기 symlink도 두 환경에서 exit 2, traceback 없음이다.
- 일반 누락 lock은 기존처럼 report 모드 exit 0/NO_LOCK으로 보존된다. 이를 설치본 정상 판정으로 계산하지 않았다.
- workspace 멤버 선언의 BELOW_FLOOR/FLOATING_REF, ETL의 NO_LOCK, 잘못된 kind/date/path, 민감한 전이 scope·DEL 출력 차단은 재현 또는 전체 회귀에서 유지됐다.
- 경로 corpus 395개와 날짜 corpus 9개에서 두 엔진 불일치 0건이다. 초안 10개는 두 환경의 stdlib/JSON Schema 모두 통과했다.

## 새 finding

### A-T011-P2-12 — workspace 및 lock 경로의 중간 디렉터리 loop는 OS별 입력 분류가 다르다

- 심각도 P2, disposition OPEN. 기존 RuntimeError traceback 문제와 구분되는 새 경계다. 새로운 P0/P1은 발견하지 않았다.
- 위치: `tools/check_versions.py:1371`~1376의 기본 `path.resolve()`, `:1886`의 최종 항목 is_symlink 검사, `:1898`의 workspace 경로 해석, `:1808`~1815의 동반 선언 처리.
- 최소 재현 1: root/loop를 자기 자신을 가리키는 디렉터리 symlink로 만들고 정상 root package-lock v3를 둔다. v1 manifest의 npm lock entry를 `{kind:npm,path:package-lock.json,scope:loop}`로 두어 workspace를 선택한다.
- 최소 재현 2: 같은 디렉터리 loop를 두고 npm lock entry를 `{kind:npm,path:loop/package-lock.json,scope:root}`로 바꾼다. 이 경우 loop는 최종 파일이 아니라 경로 중간 구성 요소다.
- 두 경우의 호출: `check_versions.py <root> --manifest <root>/manifest.json --mode report --json <root>/report.json --quiet --no-step-summary`.
- Windows Python 3.14.3 실제 결과: 두 경우 모두 exit 0, traceback 없음, JSON report 생성, `package.json NO_LOCK` 1행.
- WSL Python 3.11.15 실제 결과: 두 경우 모두 exit 2, traceback 없음, JSON report 없음.
- 원인: Windows 런타임의 기본 non-strict resolve가 해석 못한 경로를 반환할 때 helper는 성공으로 처리한다. 후속 검사는 최종 파일의 is_symlink만 보기 때문에 중간 디렉터리 순환을 구별하지 못한다. workspace 경로 자체에도 같은 검사가 빠져 있다.
- 영향: 순환 경로를 입력 오류로 닫는 계약과 두 OS 동일 결과 수용 기준이 충족되지 않는다. Windows는 malformed 경로를 일반 누락 선언 NO_LOCK으로 분류하고 WSL은 입력 오류로 처리한다. Windows report 모드 exit 0은 정상 설치본 OK를 뜻하지 않으며, 이 반례에서 외부 파일 읽기나 민감 값 노출은 확인하지 않았다.
- 권고: 입력 경로를 해석할 때 진짜 누락 파일과 symlink loop를 구별하고 중간 구성 요소까지 검사한다. 예를 들어 strict 해석의 순환 오류와 일반 FileNotFound를 분리하는 공통 처리를 검토할 수 있다. 기존 일반 missing-lock NO_LOCK 동작은 보존하면서 workspace/중간 디렉터리 loop는 양 OS 일반 exit 2로 고정한다.

## 실제 검증

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 200 tests, 56.201초, OK/skip 0 | 200 tests, 37.836초, OK/skip 0 |
| focused test_validate_manifest.py | 21 tests, 3.812초, OK | 21 tests, 2.950초, OK |
| plan | task 106/오류 0 | 동일 |
| link | 341 문서/2285 target/오류 0 | 동일 |
| SPDX | 32 파일/오류 0 | 동일 |
| secret·prod redaction --all | 각 431 파일/발견 0 | 동일 |
| check_versions --self-check | exit 0 | exit 0 |
| base..HEAD diff --check | exit 0 | exit 0 |
| 경로/날짜 corpus | 395개/9개, 불일치 0 | 동일 |
| 초안 stdlib/JSON Schema | 각각 10/10 | 각각 10/10 |
| requirements 재귀 corpus | 22개 실행, 기존 실패·정상 경계 유지 | 동일 |
| symlink 진입점/누락 9종 | 위 결과대로 | 위 결과대로 |

두 환경의 JSON Schema 엔진은 jsonschema 4.26.0이다. WSL은 `uv run --no-project --python 3.11 --with jsonschema==4.26.0` 임시 환경을 사용했고 skip을 성공에 포함하지 않았다.

후보 root에서 실행한 gate:

```text
python -B -X utf8 -m unittest discover -s tests -q
python -B -X utf8 -m unittest discover -s tests -p test_validate_manifest.py -q
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
git diff --check e03d38faabfdb03b5b636ef78897b368df70d7a3 HEAD
```

후보 밖 `.git/codex-audit/`의 A 전용 파일을 새 cwd에서 실행했다.

- `t011-post4-a-paths.py`: 동반 npm/Python, app, workspace, 중간 lock 디렉터리, root, manifest, registry self-symlink 및 일반 missing-lock 9종. exit/traceback/report 생성/판정 행을 출력한다.
- `t011-post-a-probes.py`: 초안 10개, 날짜/kind/path, workspace/ETL/동반 symlink 최초 반례.
- `t011-post2-a-boundaries.py`, `t011-post2-a-dates.py`: 공백·requirements 22종·날짜 9종.
- `t011-post3-a-adjacent.py`: 경로 395개·DEL 4개 출력 채널·직접 lock symlink.
- `t011-post4-a-gates.py`: worktree용 GIT_DIR/GIT_WORK_TREE 환경과 같은 gate. source `.git/config` 변경 없음.

WSL 명령은 `wsl -- bash -lc 'cd /mnt/f/dev/kor-travel-common-wt/review-t011-post4-a && uv run --no-project --python 3.11 --with jsonschema==4.26.0 python -B -X utf8 <명령/스크립트>'`다. 합성 민감 값은 분할 생성하고 포함 여부만 출력한다.

읽기 전용 `gh pr view 10 --repo digitie/kor-travel-common --json headRefOid,statusCheckRollup`으로 exact candidate와 run 34117388862의 5개 check SUCCESS를 확인했다. 이 성공과 위 직접 실패 반례는 별도로 판정했다.

## 범위·NOT_RUN

- 5파일 delta의 코드·시험과 기존 계약을 대조했다. 상대 reviewer 원본/결과는 독립성 조건에 따라 미열람했다.
- 소비자 build/e2e·실제 의존성 설치·package/릴리스/registry gate는 범위 밖 NOT_RUN. 소비자 쓰기 및 npm/PyPI 게시 없음.
- 원격 CI 전체 로그의 세부 집계는 NOT_RUN. exact HEAD와 5개 check 결론만 직접 조회했다.

요청한 기존 직접 symlink 반례는 해결됐다. 다만 workspace/중간 경로의 입력 오류 분류가 여전히 OS별로 달라 새 P2 1건을 OPEN으로 남기고 BLOCK으로 확정한다.
