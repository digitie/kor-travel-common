# T-011 post-fix-2 독립 리뷰 A 원본

- 실행 ID: A-T011-POST2-20260907-201233
- 판정: **BLOCK**. 잔여 P2 3건이며 이번에 남은 P0/P1은 발견하지 않았다.
- Candidate: `767db839d8638c99a1034ebdd633e2a43b9794c6`
- Parent/base: `c781117190b98fbba0036509806a39d50d64e4a3`
- 시작·종료 HEAD: candidate와 동일.
- 시작·종료 tree: `47d6439a68bb483d318fc3ef60c194d43087a79d`
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post2-a`, 새 detached worktree. 시작·종료 `git status --porcelain=v1` 모두 빈 출력.
- 시작 KST: 2026-09-07 20:12:33.468 +09:00
- 종료 KST: 2026-09-07 20:21:12.405 +09:00
- 요청: 새 immutable 후보에서 제어 문자 schema parity, strict requirements 재귀 root containment, 전이 lock scope redaction, 통합 report 집계 정정과 새 P0~P3 경계를 독립적으로 재현한다. 상대 결과를 읽지 않고 SHA/tree/clean·명령·출력·NOT_RUN 및 PASS/BLOCK을 확정한다.
- 독립성/변경: 상대 reviewer의 이번 결과와 원본을 읽거나 요청하지 않았다. source checkout의 파일과 `.git/config`, 후보 파일, 소비자 저장소를 수정하지 않았다. worktree 생성 메타데이터와 후보 밖 A probe/report, uv 임시 검증 환경만 만들었다. commit/push/registry 게시 없음.

## 이전 finding 및 요청 경계

짧은 A ID는 최초 원본의 `A-T011-` 접두를 생략한 같은 ID다. 원 심각도를 유지한다.

| ID/경계 | 판정 | 재현 결과 |
|---|---|---|
| A-P1-01 npm workspace | FIXED | 멤버 Node BELOW_FLOOR·react FLOATING_REF를 직접 보고한다. map/pinvi workspace selector 수정 유지. |
| A-P1-02 동반 선언 symlink | FIXED | root 밖 실제 package.json symlink는 exit 2, 원문 미출력. |
| A-P2-03 review 날짜 stdlib 누락 | FIXED | 정상 아닌 형식·존재하지 않는 날짜는 CLI/API에서 거부한다. 아래 A-P2-11은 별도 JSON Schema 끝 경계다. |
| A-P2-04 경로 schema 동등성 | OPEN(부분 수정) | 최초 비정규 경로와 후속 TAB/LF/CR/U+001F/DEL은 양쪽에서 거부한다. 앞뒤 공백 경계는 여전히 불일치한다. |
| A-P2-05 kind 자료형 | FIXED | list/dict 입력이 traceback 없이 오류 목록과 exit 1을 반환한다. |
| A-P2-06 ETL 빈 lock | FIXED | 선언과 NO_LOCK을 보존하고 자동 탐색과 같은 보고를 낸다. |
| A-P2-07 미지 key 출력 | FIXED | 합성 민감 key가 validator/checker 오류에 나오지 않는다. |
| A-P1-08 전이 lock scope 출력 | FIXED | 기존 민감 workspace 반례가 stdout/JSON/Markdown/summary 전부 plaintext-leak=False다. |
| A-P3-09 통합 report 집계 | FIXED | P1 3건/P2 4건으로 정정되어 통합 ID 표와 일치한다. |
| strict requirements root containment | 요청 반례 FIXED | explicit lock entry와 empty-lock app 모두 root 밖 직접/중첩 include 및 바깥 symlink를 exit 2로 거부한다. root 안 다른 디렉터리 include는 정상 허용한다. 순환 symlink의 오류 처리 차이는 새 A-P2-10이다. |

## 남은 finding

### A-T011-P2-04 — 공백을 포함한 경로의 schema/stdlib 판정이 다르다

- 심각도: P2. disposition: OPEN, 기존 finding의 잔여 경계.
- 위치: `tools/manifest_schema.py:68`의 `text = value.strip()`와 `templates/kor-travel-common.lock.schema.json:11`, `:16`.
- 최소 재현: 정상 초안의 app 또는 lockfiles[0].path를 `' /a'`, `'a/ '`, `' .'`, `' ..'`, `'a/.. '`, `'a/. '` 중 하나로 바꾸고 stdlib validate_manifest와 jsonschema 4.26.0의 Draft202012Validator를 호출한다.
- 실제: 각 입력에서 stdlib 오류 1개, JSON Schema 오류 0개. U+00A0 뒤 `/a`도 같은 결과다. Windows와 WSL에서 두 엔진으로 직접 확인했다.
- 원인/영향: stdlib는 바깥 공백을 제거한 값을 검사하고 schema는 원문을 검사한다. 따라서 문서화한 같은 v1 상대 경로 계약의 음성 corpus가 일치하지 않는다. 일반 내부 공백 경로 `a b`와 양쪽에서 허용한 ` a `도 대조하여 모든 공백을 잘못된 입력이라고 단정하지 않았다.
- 권고: 원문과 정규화 후 문자열의 처리 계약을 하나로 정한다. 필요하면 양쪽에서 바깥 공백을 명시적으로 금지하고, 실제 두 검증기를 호출하는 corpus에 위 값을 포함한다.

### A-T011-P2-10 — requirements의 순환 symlink가 Python 3.11에서 traceback/exit 1을 낸다

- 심각도: P2. disposition: OPEN, 새 finding.
- 위치: `tools/check_versions.py:669`~677의 read_requirements 최종 경로 해석 및 main의 입력 오류 예외 처리.
- 최소 재현: root/apps/etl/requirements.txt에 `-r loop.txt`를 쓰고 같은 디렉터리의 loop.txt를 자기 자신을 가리키는 symlink로 만든다. strict root+manifest CLI를 explicit requirements entry와 empty-lock app 각각에 대해 실행한다.
- 실제: Windows Python 3.14.3은 exit 2/traceback 없음; WSL Python 3.11.15는 exit 1/traceback 있음. 별도 read_requirements API 호출에서 예외 종류 RuntimeError를 직접 확인했다. 두 경로 모두 JSON report는 생성하지 않았다.
- 영향: 지원 기준 Python 3.11에서 문서화한 경로 입력 오류 exit 2와 두 OS 동일 결과 계약을 깨며 내부 traceback과 로컬 경로를 노출한다. 외부 파일을 정상 판정으로 읽는 우회는 재현되지 않았다.
- 권고: Path.resolve의 순환 symlink 실패를 입력 경계에서 비식별화된 ValueError로 변환한다. Python 버전별 RuntimeError/OSError 차이를 처리하고 explicit/empty-lock 양 경로를 3.11 회귀에 포함한다.

### A-T011-P2-11 — JSON Schema의 ISO 날짜가 끝 LF와 비ASCII 연도를 허용한다

- 심각도: P2. disposition: OPEN, 새 finding.
- 위치: `templates/kor-travel-common.lock.schema.json:18`~21; 비교: `tools/manifest_schema.py`의 _check_date.
- 최소 재현: 정상 예외의 until을 `'2026-09-07' + chr(10)`, `'２０２６-09-07'`, `'٢٠٢٦-09-07'`로 바꿔 두 검증기에 넣는다. review도 같은 isoDate 정의를 참조한다.
- 실제: Windows/WSL의 stdlib는 모두 오류 1개이고 기본 Draft202012Validator는 모두 오류 0개다. 정상 날짜·2000-02-29·9999-12-31은 양쪽 허용, 1900-02-29·0000-01-01은 양쪽 거부하는 대조군도 확인했다.
- 원인/영향: 해당 JSON Schema 엔진의 `$`는 마지막 LF 앞에서도 매치하고 `\d`는 비ASCII 숫자도 허용한다. `format: date`는 기본 Draft202012Validator에서 assertion으로 강제되지 않는다. 배포 schema가 유효한 ISO 날짜 계약에 어긋나는 값을 승인한다.
- 권고: 기본 엔진에서도 실제 끝과 ASCII 숫자를 보장하도록 pattern을 수정하거나 format assertion을 의무화하는 검증 계약을 명확히 제공한다. 신규 corpus는 until/review와 두 예외 형태에 공통 적용한다.

## 실행 및 결과

| 검사 | Windows | WSL |
|---|---|---|
| 전체 unittest | 198 tests, 57.416초, OK/skip 0 | 최초 197 성공+1 skip. 임시 jsonschema 환경 재실행은 198 tests, 31.652초, OK/skip 0 |
| focused test_validate_manifest.py | 19 tests, 3.431초, OK | 최초 18 성공+1 skip. 같은 임시 환경은 19 tests, 2.207초, OK/skip 0 |
| plan | task 106/오류 0 | 동일 |
| link | 335 문서/2281 target/오류 0 | 동일 |
| SPDX | 32 파일/오류 0 | 동일 |
| secret·prod redaction --all | 각 425 파일/발견 0 | 동일 |
| check_versions --self-check | exit 0 | exit 0 |
| base..HEAD diff --check | exit 0 | exit 0 |
| 10개 초안 stdlib/Windows schema | 10/10 정상 | stdlib 10/10. schema 미설치였던 최초 실행은 NOT_RUN으로 기록하고 실제 parity는 아래 임시 환경에서 보완 |
| requirements 11종 × explicit/empty 2종 | 22 CLI 실행 | 22 CLI 실행 및 jsonschema 환경 재현 |

Windows Python은 3.14.3, WSL Python은 3.11.15다. 두 JSON Schema 엔진은 jsonschema 4.26.0이다. 초기 WSL skip을 통과 건수에 포함하지 않았고, 후보/설정 변경 없이 `uv run --no-project --python 3.11 --with jsonschema==4.26.0`의 별도 임시 환경으로 전체·focused·새 schema 반례를 실제 실행했다.

후보 root에서 실행한 명령:

```text
python -B -X utf8 -m unittest discover -s tests -q
python -B -X utf8 -m unittest discover -s tests -p test_validate_manifest.py -q
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
git diff --check c781117190b98fbba0036509806a39d50d64e4a3 HEAD
```

후보 밖 실행 보조 파일:

- `.git/codex-audit/t011-post-a-probes.py`, `t011-post-a-extra.py`, `t011-a-negative.py`: 누적 A 반례를 새 cwd에서 재실행했다.
- `.git/codex-audit/t011-post2-a-boundaries.py`: 공백 경로와 requirements 재귀/경계/순환 symlink 22건. 각 결과의 exit·traceback·외부 값 노출·report 생성 여부를 출력한다.
- `.git/codex-audit/t011-post2-a-dates.py`: 정상/음성 날짜 9건의 실제 두 엔진 오류 수.
- `.git/codex-audit/t011-post2-a-gates.py`: 동일 gate 및 worktree용 GIT_DIR/GIT_WORK_TREE 환경 지정. source `.git/config`는 변경하지 않았다.

WSL 실행 위치는 `/mnt/f/dev/kor-travel-common-wt/review-t011-post2-a`다. 기본 실행은 managed Python 절대 경로로, schema 보완은 `wsl -- bash -lc 'cd <위 경로> && uv run --no-project --python 3.11 --with jsonschema==4.26.0 python -B -X utf8 <명령/스크립트>'`로 했다. 민감 문자열 반례는 분할 생성하며 로그에는 포함 여부 boolean만 출력했다.

읽기 전용 `gh pr view 10 --repo digitie/kor-travel-common --json headRefOid,statusCheckRollup`은 exact candidate HEAD와 run 34115370093의 5개 check SUCCESS를 반환했다. 이는 로컬 실패 반례가 해결됐다는 증거로 사용하지 않았다.

## NOT_RUN과 범위 한계

- 실제 소비자 build/e2e, 설치 재현, package/릴리스/registry gate는 범위 밖이므로 NOT_RUN. 소비자 저장소 쓰기·npm/PyPI 게시 없음.
- 원격 CI job 전체 로그의 세부 test/skip 집계는 NOT_RUN. exact SHA와 5개 check 결론만 직접 조회했다.
- 전체 12파일 delta 중 코드·schema·시험·정본 문서·이전 통합 집계 수정과 관련 계약을 검토했다. 상대 reviewer 원본/새 결과는 독립성 조건에 따라 미열람이다.

기존 P1 반례와 이번 요구한 root 이탈·제어 문자 반례는 수정됐다. 다만 v1 schema 동등성과 지원 Python의 오류 처리에서 P2 3건이 남아 있으므로 이 후보의 최종 판정은 BLOCK이다.
