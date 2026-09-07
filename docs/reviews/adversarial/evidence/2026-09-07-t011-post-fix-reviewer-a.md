# T-011 post-fix 독립 리뷰 A 원본

- 실행 ID: A-T011-POSTFIX-20260907-195602
- 최종 판정: **BLOCK**.
- Candidate: `c781117190b98fbba0036509806a39d50d64e4a3`
- Parent/base: `7f715b0efb7c422f0b6212eea612f0c95dcf6fff`
- 시작·종료 SHA: candidate와 동일. 시작·종료 tree: `d9d777cfc93db2ef4e02c4f84b45793aba741462`.
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post-a`, 새 detached worktree. 시작·종료 `git status --porcelain=v1` 빈 출력.
- 시작 KST: 2026-09-07 19:56:02.186 +09:00
- 종료 KST: 2026-09-07 20:03:20.118 +09:00
- 요청 범위: c781117의 정확한 SHA를 확인하고 최초 A 7건 및 pre-fix 통합 report 전체 finding의 수정 여부와 새 경계를 Windows/WSL에서 재현한다. 시작/종료 SHA·tree·clean, 명령, NOT_RUN과 PASS/BLOCK을 남긴다.
- 독립성: 요청에 따라 확정된 pre-fix 통합 report의 ID·요약을 대조했다. B 원본과 이번 post-fix 결과는 읽거나 요청하지 않았다. 후보·소비자·source checkout의 `.git/config`를 수정하지 않았다. Git의 worktree 추가 메타데이터 외 변경은 후보 밖 A 전용 probe·원본 report뿐이며 commit/push/게시하지 않았다.

## 결론과 이전 finding disposition

최초 반례 자체는 모두 수정된 동작을 보였다. 그러나 상대 경로 검사기의 동등성에는 제어 문자 반례가 남고, 민감한 workspace 문자열이 전이 lock 행을 만들 때 재출력된다. 추가로 새 통합 report의 심각도 건수와 실제 표가 불일치한다.

아래 짧은 A ID는 최초 원본의 `A-T011-` 접두를 생략한 같은 ID이며, 원 심각도를 보존한다.

| 원 ID | 원 심각도 | disposition | 실제 재검증 |
|---|---:|---|---|
| A-P1-01 | P1 | FIXED | workspace 멤버 Node `>=18`의 BELOW_FLOOR와 react `latest`의 FLOATING_REF를 보고한다. map/pinvi 초안도 실제 workspace selector로 바뀌었다. |
| A-P1-02 | P1 | FIXED | 실제 존재하는 root 밖 package.json symlink를 내용 읽기 전 exit 2로 거부한다. `_safe_declared_file`이 Python 동반 선언에도 적용된 것을 코드로 확인했다. |
| A-P2-03 | P2 | FIXED | key/rule 예외의 잘못된 review 형식 및 `2026-02-30`은 stdlib/CLI에서 거부되고 Windows JSON Schema에서도 거부된다. |
| A-P2-04 | P2 | OPEN(부분 수정) | 최초 drive/빈 segment/끝 slash/공백/NUL 반례는 양쪽에서 거부한다. TAB/LF/CR/U+001F/DEL 반례는 여전히 서로 다르다. 아래 잔여 반례 참조. |
| A-P2-05 | P2 | FIXED | kind 배열·객체가 traceback 없이 오류 목록/exit 1을 반환한다. |
| A-P2-06 | P2 | FIXED | 기존 ETL 초안 그대로 Python 선언과 NO_LOCK 행을 보고하며 root 자동 탐색과 일치한다. |
| A-P2-07 | P2 | FIXED(원 미지 필드 반례) | 합성 민감 문자열을 미지 key로 넣어도 validator와 checker 오류에 포함되지 않는다. 통합 R03의 scope 부분은 별도 A-P1-08로 잔존한다. |

통합 report 대조: T011-R01/R02/R04/R06/R07는 FIXED, **T011-R03(P1), T011-R05(P2)는 OPEN**이다. R03의 원 통합 심각도 P1을 유지한다.

## 남은 finding

### A-T011-P2-04 / T011-R05 — 제어 문자 경로의 JSON Schema/stdlib 불일치

- 심각도: P2, OPEN. 최초 finding의 연속 재현이다.
- 위치: `templates/kor-travel-common.lock.schema.json:11`, `:16`; 비교 대상 `tools/manifest_schema.py:65`~72. 수용 기준: `docs/tasks/T-011-consumer-manifest-schema.md:56`의 동일 음성 corpus.
- 최소 재현: 정상 초안의 lockfiles[0].path를 `'apps/a' + chr(9) + 'b/package-lock.json'`으로 바꾼다. 같은 입력을 `validate_manifest(data)`와 `jsonschema.Draft202012Validator(schema).iter_errors(data)`에 넣는다.
- 실제: stdlib 오류 1개, JSON Schema 오류 0개. chr(10), chr(13), chr(31), chr(127)도 같은 결과다. Windows에서 두 엔진으로 직접 재현했고 WSL stdlib의 거부도 확인했다.
- 원인/영향: Python validator는 내부 ASCII 제어 문자를 거부하지만 schema는 NUL만 금지하고 전체 문자열 소비도 강제하지 않는다. 소비자가 strict schema로 정상 판정받은 경로가 실제 checker 진입 시 거절된다.
- 권고: schema의 relativePath·nullableRelativePath에 같은 제어 문자 범위와 전체 문자열 조건을 적용하고, 양쪽 검증기를 실제로 호출하는 동등성 시험을 추가한다. 새 `test_schema_path_edge_cases_are_rejected`는 이름과 달리 stdlib만 호출하므로 schema 회귀를 잡지 못한다.

### A-T011-P1-08 / T011-R03 — 전이 lock scope에서 민감 workspace 원문이 재등장한다

- 심각도: P1, OPEN. A가 이번에 독립 재현한 통합 R03의 잔여 출력 경계다.
- 위치: `tools/check_versions.py:1854`의 최초 label 처리 이후 `:2076`, `:2082`의 lock 경로 재조합, `:1904`의 Finding 생성.
- 최소 재현: 분할 생성한 합성 사설 주소 형식 문자열을 변수 `marker`로만 보관한다. root/marker/package.json에 정상 Node 선언과 빈 dependencies를 두고, manifest의 app/scope를 marker로 지정한다. root package-lock v3의 packages에는 `marker` 멤버와 `marker + '/node_modules/react'`의 version `19.2.8`을 둔다. root+manifest CLI를 `--json report.json --markdown report.md`와 GITHUB_STEP_SUMMARY 지정 상태로 호출한다.
- 실제: exit 0. stdout·report.json·report.md·step summary에서 모두 원 marker 포함 여부가 True다. Windows/WSL 동일하다. 합성 값 자체는 도구 로그와 이 보고서에 출력하지 않았다.
- 원인/영향: 최초 scope label은 비식별화하지만 나중에 raw lock package 경로를 `[lock:{path}]`로 붙여 민감한 workspace 값을 복구한다. 신규 task/versions 계약이 금지한 scope 원문이 CI 보고·artifact·summary로 노출된다.
- 권고: 전이 행을 포함해 최종 scope와 진단을 만드는 모든 경로에 비식별화를 적용한다. 내부 lookup identity와 출력용 문자열은 별도로 유지하고, 직접 행만이 아니라 중첩·전이 lock 행까지 stdout/JSON/Markdown/summary를 검사한다.

### A-T011-P3-09 — pre-fix 통합 finding 건수가 표와 다르다

- 심각도: P3, OPEN.
- 위치: `docs/reviews/adversarial/2026-09-07-t011.md:11` 및 15~21행.
- 재현: 본문은 중복 제거 결과를 P1 3건·P2 5건이라고 적지만 7개 통합 ID 표에는 P1 3건·P2 4건이 있다.
- 영향/권고: 독립 원본은 보존하고 통합 보고서의 중복 제거 집계를 표와 맞춘다. 종료 시 원 ID·통합 ID·원 심각도 변환을 그대로 유지한다. 이 P3만으로 코드의 안전성을 부정하는 것은 아니지만 문서 delta의 정정 대상이다.

## 실행한 검증

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 unittest | 195 tests, 54.220초, OK, skip 0 | 195 tests, 36.783초, OK, skip 0 |
| focused test_validate_manifest.py | 16 tests, 2.973초, OK | 16 tests, 2.168초, OK |
| plan | task 106, 오류 0 | 동일 |
| link | 332 문서/2279 target, 오류 0 | 동일 |
| SPDX | 32 파일, 오류 0 | 동일 |
| secret/prod redaction --all | 각 422 파일, 발견 0 | 동일 |
| check_versions --self-check | exit 0 | exit 0 |
| base..HEAD diff --check | exit 0 | exit 0 |
| 초안 validator | 10/10 통과 | 10/10 통과 |
| 초안 JSON Schema | 10/10 통과 | NOT_RUN(jsonschema 미설치) |
| 기존 반례 + 추가 출력·경로 반례 | 위 표/결과대로 | JSON Schema 엔진 외 동일 |

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
git diff --check 7f715b0efb7c422f0b6212eea612f0c95dcf6fff HEAD
```

직접 반례 원문은 후보 밖 A 전용 `.git/codex-audit/t011-post-a-probes.py`, `t011-a-negative.py`, `t011-post-a-extra.py`다. probes의 공통 npm fixture는 scope를 root로 고정한 뒤 workspace 반례에서 명시적으로 apps/web으로 바꿔 이전 입력과 동일하게 유지했다. 마지막 extra probe의 누락된 workspace package.json 대조군은 fail 모드 exit 1/NO_LOCK으로 정상 닫혔다.

WSL 명령은 `wsl --cd /mnt/f/dev/kor-travel-common-wt/review-t011-post-a -- /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 <동일 명령/스크립트>` 형태다. Git을 읽는 gate는 후보 밖 `t011-post-a-gates.py`에서 worktree용 GIT_DIR/GIT_WORK_TREE 환경만 지정했다. source `.git/config`는 건드리지 않았다.

읽기 전용 `gh run view 34113919728 --repo digitie/kor-travel-common --json headSha,status,conclusion,jobs`로 exact candidate의 원격 CI 완료/success와 5개 job 성공을 확인했다. 전체 로그 및 소비자 실제 실행은 이 조회로 검증한 것이 아니다.

## NOT_RUN 및 한계

- WSL의 전체 JSON Schema 엔진 대조: jsonschema 미설치. Windows에서는 Draft202012Validator를 실제 사용했으며 WSL stdlib·CLI 반례는 실행했다.
- 소비자 build/e2e·실제 패키지 설치·registry/릴리스/package gate: 이번 common 도구 리뷰 범위 밖. 소비자 파일을 읽어 성공으로 계산하거나 쓰지 않았다.
- 15파일 delta 중 제품 코드·schema·초안·시험·문서 수정과 확정된 pre-fix 통합 report를 확인했다. B 원본은 독립성 조건 때문에 재열람하지 않았다. 같은 SHA에 대한 로컬 성공과 CI 성공은 별도로 기록했다.

위 P1/P2가 남아 있어 이 candidate는 BLOCK이다. 원본과 후보를 그대로 보존하고 새 immutable 후보에서 잔여 반례를 재검토해야 한다.
