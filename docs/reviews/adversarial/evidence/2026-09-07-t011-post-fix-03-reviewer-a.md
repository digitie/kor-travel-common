# T-011 post-fix-3 독립 리뷰 A 원본

- 실행 ID: A-T011-POST3-20260907-202618
- 최종 판정: **BLOCK**. A-T011-P2-10의 인접 진입 경계 1건이 남았다.
- Candidate: `e03d38faabfdb03b5b636ef78897b368df70d7a3`
- Parent/base: `767db839d8638c99a1034ebdd633e2a43b9794c6`
- 시작·종료 SHA: candidate와 동일.
- 시작·종료 tree: `15dd9df9abb504b25991ea16e63902914935305c`
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post3-a`, 새 detached worktree. 시작·종료 `git status --porcelain=v1` 빈 출력.
- 시작 KST: 2026-09-07 20:26:18.651 +09:00
- 종료 KST: 2026-09-07 20:32:01.620 +09:00
- 요청: exact e03d38f를 확인하고 공백 path parity, requirements self-symlink RuntimeError, date schema parity, DEL lock path redaction 및 인접 P0~P3 경계를 Windows/WSL에서 독립 검토한다.
- 독립성/변경: 상대 reviewer 결과를 읽거나 요청하지 않았다. source checkout 파일·`.git/config`, 후보, 소비자를 수정하지 않았다. worktree 메타데이터 및 후보 밖 A 전용 probe/report만 작성했으며, 기존 uv 임시 검증 환경을 사용했다. commit/push/게시 없음.

## Disposition

| 이전 ID/요청 경계 | 원 심각도 | disposition | 근거 |
|---|---:|---|---|
| A-T011-P2-04 공백·경로 schema parity | P2 | FIXED | 이전 공백·제어 문자 반례가 양쪽에서 거부된다. 추가 395개 경로 corpus도 Windows/WSL 모두 두 엔진 불일치 0건. |
| A-T011-P2-10 requirements self-symlink | P2 | OPEN(부분 수정) | `-r loop.txt`로 들어가는 기존 반례는 양 OS exit 2/traceback 없음. 하지만 lockfiles.path 자체가 자기 symlink이면 reader에 도달하기 전 resolve에서 WSL RuntimeError가 남는다. |
| A-T011-P2-11 date schema parity | P2 | FIXED | 끝 LF·전각/아랍 숫자 연도는 양쪽에서 거부한다. 정상 날짜·윤년·0000/1900/2000/9999 경계 대조군도 일치한다. |
| DEL lock path redaction | 요청 경계 | FIXED | 실제 전이 lock 경로의 DEL이 stdout/JSON/Markdown/step summary에 남지 않는다. |
| 이전 A-P1-01/02, P2-03/05/06/07, P1-08, P3-09 | 원 심각도 유지 | FIXED 유지 | 변경 범위 대조와 전체 200 tests, 미지 key·scope 출력·NO_LOCK·기존 경계 corpus에서 회귀를 발견하지 않았다. 변경 없는 이전 결과는 동일성 범위에 한해 재사용했다. |

## 잔여 finding

### A-T011-P2-10 — lockfiles.path 자체의 자기 symlink는 strict 진입점에서 여전히 traceback을 낸다

- 심각도 P2, disposition OPEN. 기존 순환 symlink 오류 처리 finding의 인접 진입 경계다. 새 P0/P1 또는 별도 finding은 발견하지 않았다.
- 위치: `tools/check_versions.py:1864`의 `(base / raw_path).resolve()` 및 `:2837` 부근 매니페스트 오류 처리. 같은 계열 resolve가 `:1799`, `:1849`에도 있다.
- 최소 재현: 정상 v1 manifest에 `lockfiles=[{kind: requirements, path: apps/etl/requirements.txt, scope: root}]`를 둔다. root/apps/etl/requirements.txt를 자기 자신을 가리키는 symlink로 만들고 `check_versions.py <root> --manifest <root>/manifest.json --mode report --json <root>/report.json --quiet --no-step-summary`를 실행한다. npm/package-lock.json 자기 symlink로 바꾼 대조군도 실행했다.
- Windows Python 3.14.3: 두 경우 모두 exit 0, traceback 없음, JSON report 있음, 각각 `pyproject.toml NO_LOCK`/`package.json NO_LOCK`. report 모드의 exit 0을 설치본 정상 판정으로 해석하지 않았다.
- WSL Python 3.11.15: 두 경우 모두 exit 1, RuntimeError traceback 있음, JSON report 없음.
- 원인: 새 예외 변환은 read_requirements 안에만 있다. 그보다 먼저 실행되는 scopes_from_manifest의 lock 경로 resolve가 순환 symlink에서 RuntimeError를 던지며, CLI 입력 오류 처리도 이를 받지 않는다.
- 영향: 지원 기준 Python 3.11의 strict 매니페스트 진입에서 문서화한 입력 오류 처리/비공개 진단과 Windows·Linux 동일 결과 계약이 깨진다. 외부 파일을 읽거나 버전 위반을 OK로 둔 우회는 이 반례에서 확인되지 않았다.
- 권고: strict 매니페스트에서 소비하는 경로를 해석하는 공통 경계에 순환 symlink 예외 정규화를 적용한다. read_requirements 내부뿐 아니라 manifest/lock/동반 선언/app/workspace 진입점이 같은 처리를 사용하도록 점검한다. 경로 오류 원문과 내부 stack을 출력하지 않고 두 OS에서 일관되게 닫는 직접 lock 경로 회귀를 추가한다.

## 실제 검증

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 200 tests, 57.321초, OK/skip 0 | 200 tests, 39.235초, OK/skip 0 |
| focused test_validate_manifest.py | 21 tests, 3.502초, OK | 21 tests, 2.572초, OK |
| plan | task 106/오류 0 | 동일 |
| link | 338 문서/2283 target/오류 0 | 동일 |
| SPDX | 32 파일/오류 0 | 동일 |
| secret·prod redaction --all | 각 428 파일/발견 0 | 동일 |
| check_versions --self-check | exit 0 | exit 0 |
| base..HEAD diff --check | exit 0 | exit 0 |
| schema 경로 corpus | 395개, 불일치 0 | 동일 |
| 날짜 corpus | 9개, 불일치 0 | 동일 |
| requirements include corpus | 22 CLI 실행, 기존 실패·정상 경계 일치 | 동일, 기존 self-symlink도 exit 2로 수정 |
| direct lock self-symlink | 위 잔여 finding 재현 | 위 잔여 finding 재현 |
| 민감 scope/DEL 보고 채널 | 원문/DEL 노출 False | 동일 |

두 환경에서 jsonschema 4.26.0을 사용했다. WSL은 후보 밖 `uv run --no-project --python 3.11 --with jsonschema==4.26.0` 환경으로 실행하여 이번 전체/focused 실행에는 skip이 없었다.

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
git diff --check 767db839d8638c99a1034ebdd633e2a43b9794c6 HEAD
```

후보 밖 `.git/codex-audit/`에 보존한 A 전용 재현 파일:

- `t011-post2-a-boundaries.py`: 이전 공백 및 requirements 포함 경계 22건 재실행.
- `t011-post2-a-dates.py`: 실제 stdlib/JSON Schema 날짜 9건.
- `t011-post-a-extra.py`, `t011-a-negative.py`: 이전 제어 문자·민감 scope·미지 key·오류 입력 재실행.
- `t011-post3-a-adjacent.py`: 395개 경로 corpus, DEL 전이 lock 채널, direct lock symlink 비교.
- `t011-post3-a-direct-loop.py`: 잔여 finding의 JSON report 생성 여부와 실제 판정을 포함한 최소 CLI 재현.
- `t011-post3-a-gates.py`: worktree GIT_DIR/GIT_WORK_TREE 환경으로 같은 gate 실행. source `.git/config`는 수정하지 않았다.

WSL 명령은 `wsl -- bash -lc 'cd /mnt/f/dev/kor-travel-common-wt/review-t011-post3-a && uv run --no-project --python 3.11 --with jsonschema==4.26.0 python -B -X utf8 <명령/스크립트>'` 형태다. 민감 합성 값은 원문을 출력하지 않고 출력 포함 여부만 기록했다.

읽기 전용 `gh pr view 10 --repo digitie/kor-travel-common --json headRefOid,statusCheckRollup`은 exact candidate와 run 34116567561의 5개 check SUCCESS를 반환했다. 로컬 성공·CI 성공과 별도 직접 실패 반례를 분리했다.

## 범위·NOT_RUN

- 8파일 delta 중 코드·schema·시험·task 계약의 변경을 직접 검토했고 상대 reviewer 원본/결과는 미열람했다.
- 소비자 build/e2e·실제 설치·package/릴리스/registry gate는 리뷰 범위 밖으로 NOT_RUN. 소비자 파일 쓰기·npm/PyPI 게시 없음.
- 원격 CI 전체 로그의 세부 test 집계는 NOT_RUN. exact HEAD와 5개 check 결론만 직접 조회했다.

나머지 요청 반례는 수정됐지만 strict 진입점에서 같은 RuntimeError 경계가 남아 있으므로 최종 판정은 BLOCK이다.
