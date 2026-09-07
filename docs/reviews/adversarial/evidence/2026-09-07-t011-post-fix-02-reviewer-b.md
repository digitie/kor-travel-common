# T-011 post-fix-2 독립 리뷰 B 원본

최종 verdict: **BLOCK**. 기존 B-P2-04의 공백 경로 parity가 남으며, 새 B-P2-08에서 전이 lock 경로의 DEL 제어 문자 재출력을 확인했다. P1 root containment와 기존 비밀 형식 문자열 노출 반례는 수정됐다.

## 기준선·격리

- 실행 ID: `T011-POST2-B-20260907-201250-KST`.
- candidate: `767db839d8638c99a1034ebdd633e2a43b9794c6`.
- parent/base: `c781117190b98fbba0036509806a39d50d64e4a3`.
- tree: `47d6439a68bb483d318fc3ef60c194d43087a79d`.
- detached worktree: `F:/dev/kor-travel-common-wt/review-t011-post2-b`.
- 시작: `2026-09-07T20:12:50.1185380+09:00`.
- 종료: `2026-09-07T20:18:32.7155922+09:00`.
- 시작·종료 SHA/tree와 clean 상태를 직접 확인했다. source/candidate 파일·소비자 저장소를 수정하지 않았고 commit/push/게시를 하지 않았다. reviewer의 임시 fixture는 별도 임시 디렉터리에만 생성했다.
- source `.git/config`는 수정하지 않았다. 확인한 SHA256은 시작과 종료 모두 `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A`다.
- 상대 reviewer 결과·개별 원본을 읽거나 요청하지 않았다. 요청된 경계를 코드·tests·schema·정본 diff와 자체 재현으로 판정했다. archive에 추가된 상대 원본 본문은 읽지 않았다.

## 요청 원문

> 새 immutable candidate `767db839d8638c99a1034ebdd633e2a43b9794c6`를 독립 post-fix-2 리뷰해 주세요. parent/base는 `c781117190b98fbba0036509806a39d50d64e4a3`입니다. 이전 post-fix 후보의 잔여 경계(제어문자 schema parity, strict requirements 재귀 root containment, 전이 lock scope redaction, 통합 보고서 집계 정정)가 닫혔는지 Windows/WSL에서 재현하고 새로운 P0–P3 finding도 공격해 주세요. 상대 reviewer 결과는 읽지 말고, source checkout의 파일과 `.git/config`는 수정하지 마세요. 시작/종료 SHA/tree/clean, 명령·출력·NOT_RUN과 최종 PASS/BLOCK을 원본 evidence로 확정해 주세요.

## 실행 명령·결과

Windows는 `py -3.14 -B -X utf8`, WSL은 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`을 사용했다. 전체 시험은 `-m unittest discover -s tests -q`로 실행했다. WSL 전체 실행에서는 `GIT_DIR`·`GIT_WORK_TREE`·`GIT_COMMON_DIR`를 제거해 임시 Git fixture에 source 설정을 전달하지 않았다. 읽기 전용 validator subprocess에만 detached worktree의 Linux Git 경로를 지정했다.

| 검증 | Windows Python 3.14.3 | WSL Python 3.11.15 |
|---|---|---|
| 전체 회귀 | 198 tests, 57.084초, OK, skip 0 | 198개 수집, 197개 실행 성공, 1개 skip, 36.287초 |
| plan | 106 tasks, 오류 0 | 동일 |
| 문서 링크 | 335문서·2,281 target, 오류 0 | 동일 |
| SPDX | 32파일, 오류 0 | 동일 |
| secret / production redaction | 각각 425파일, 발견 0·예외 0 | 동일 |
| registry self-check | exit 0 | exit 0 |

validator 명령은 `tools/validate_plan.py`, `tools/validate_document_links.py`, `tools/check_spdx.py`, `tools/scan_secrets.py --all`, `tools/check_prod_redaction.py --all`, `tools/check_versions.py --self-check`다. `git diff --check HEAD^ HEAD`는 exit 0이다.

- WSL skip은 새 `test_json_schema_rejects_control_character_paths_like_stdlib`의 jsonschema 미설치 때문이다. 이 1개를 통과로 세지 않는다. Windows에서는 설치된 jsonschema 4.26.0의 Draft202012Validator로 직접 실행했다. WSL에서도 schema의 실제 pattern과 stdlib 결과를 별도로 대조했지만 외부 엔진 실행으로 표현하지 않는다.
- 최초 corpus `.git/codex-audit/review-t011-b-cases.py`, post-fix corpus `review-t011-post-b-cases.py`, 이번 corpus `review-t011-post2-b-cases.py`를 양쪽 Python에 이번 worktree 경로를 전달해 실행했다. 아래 최소 반례와 stdout boolean 결과를 포함한다. 합성 비밀은 문자열을 분할 생성했으며 원문을 보고서에 쓰지 않았다.
- Windows schema 초안 10/10 통과. stdlib 초안 10개 CLI 검증은 전체 회귀에 포함됐다.
- `gh run list --commit <candidate>`와 `gh run view 34115370093 --json headSha,conclusion,jobs`: exact candidate, 5개 job success. [CI 실행](https://github.com/digitie/kor-travel-common/actions/runs/34115370093). 원격 성공과 로컬 skip/반례는 별도로 기록한다.
- `.github`·`versions.json`·`LICENSE`·`NOTICE`는 parent 대비 불변이다.

## 기존 finding disposition

| ID | 기존 심각도 | 결과 |
|---|---:|---|
| B-P1-01 | P1 | FIXED 유지. 미지 field와 민감한 scope 원문이 validator·CLI·JSON·Markdown·summary에 나오지 않음 |
| B-P1-02 | P1 | FIXED 유지. package.json/pyproject.toml의 root 밖 symlink, manifest/lock/workflow 외부 경로는 exit 2 |
| B-P1-03 | P1 | FIXED 유지. 멤버 package.json 선택·Node >=18.0.0 BELOW_FLOOR·fail exit 1 재현 |
| B-P2-04 | P2 | OPEN. 제어 문자 corpus와 날짜는 수정됐으나 앞뒤 공백 경로의 schema/stdlib 불일치가 남음 |
| B-P2-05 | P2 | FIXED 유지. kind 배열·객체는 오류 목록·exit 1, traceback 없음 |
| B-P1-06 | P1 | FIXED. 빈 lockfiles·명시 requirements scope 모두 외부 재귀 include는 exit 2·보고서 없음. root 안 symlink가 밖을 가리키는 include도 exit 2, 외부 파일명·내용 미출력. root 내부 shared include는 NO_LOCK의 정상 report로 유지 |
| B-P3-07 | P3 | FIXED. 통합 보고서 본문이 P1 3건·P2 4건으로 수정돼 R01–R07 표와 일치 |

선언 전용 ETL은 Python 선언을 읽고 NO_LOCK을 유지한다. 전이 lock path의 합성 비밀 문자열도 이번 `_display_lock_location`을 통해 stdout·JSON·Markdown·summary 모두 숨겨진다. 아래 DEL 문자 문제는 credential 문자열 노출이 재발했다는 주장이 아니다.

## B-P2-04 — 앞뒤 공백에서 경로 검증기의 판정이 여전히 다름

- 심각도: 원 P2 유지. disposition: OPEN.
- 위치: `tools/manifest_schema.py:68`; `templates/kor-travel-common.lock.schema.json:11`, `:16`.
- 최소 재현: 정상 manifest의 app 또는 상대 경로 필드에 ` /etc/fixture`, ` ../fixture`, `apps/ `, `apps/. `, ` ./apps`를 각각 넣는다. Windows Draft202012Validator는 5개 전부 통과시키고 stdlib validator는 5개 전부 거절한다. WSL pattern/stdlib 결과도 동일하다. 정상 `apps/etl`·`a b/etl`은 양쪽 모두 통과한다.
- 원인: stdlib은 원문을 `strip()`한 뒤 slash/dot segment를 검사하지만 schema는 원문 그대로 검사한다. 지난 원본에 이미 있던 ` /etc/fixture` 반례도 아직 남아 있다.
- 영향: T-011 수용 기준의 동일한 상대 경로 음성 corpus 계약을 충족하지 못한다. 이는 이 입력으로 root를 탈출했다는 finding이 아니라 같은 v1을 검사하는 두 도구의 승인 결과가 다르다는 finding이다.
- 권고: 앞뒤 공백의 허용 정책을 정한 뒤 raw 문자열에 같은 규칙을 적용한다. 예를 들어 경계 공백을 양쪽에서 거절하거나, 양쪽 모두 trim 없이 같은 경로 문법을 검사한다. embedded space의 정상 대조군도 유지하고 다섯 음성 사례를 두 엔진에서 검사한다.

## B-P2-08 — 전이 lock 경로의 DEL 제어 문자가 모든 보고 채널에 남음

- 심각도: P2. disposition: OPEN, 새 finding.
- 위치: `tools/check_versions.py:1345`, `:1353`, `:2096`.
- 최소 재현: root package.json의 Node는 정상 범위로 둔다. package-lock v3의 packages에 `marker = 'fixture' + chr(127) + 'member'` 경로와 `marker + '/node_modules/react'` 경로를 넣고 React version은 19.2.8로 둔다. strict manifest는 root package-lock을 선택한다.
- 실행: `check_versions.py <repo> --manifest <repo>/manifest.json --mode fail --json <out.json> --markdown <out.md>`와 `GITHUB_STEP_SUMMARY`를 사용했다.
- Windows/WSL 모두 exit 0, 2개 판정 행을 냈으며 DEL을 포함한 원 경로가 **stdout·JSON·Markdown·step summary 네 채널 모두**에 남았다. 동일한 위치에 합성 비밀 문자열을 넣은 음성 대조는 네 채널 모두 원문 미포함으로 수정 확인했다.
- 원인: 새 lock 위치 조립 함수가 사용하는 `_workflow_display_value`는 일부 C0 제어 문자만 거르고 DEL(0x7F)은 거르지 않는다. strict manifest 경로 검증에는 DEL 금지가 있으나 lock 내부 경로는 그 검증을 통과하지 않는다.
- 영향: 이번 versions 정본의 scope 제어 문자 미출력 계약과 보고 채널 처리가 다르다. 실제 자격증명이나 코드 실행 취약점으로 과장하지 않는다.
- 권고: 입력 경로의 표시 함수에 C0/DEL 정책을 일관되게 적용해 안전한 대체값으로 표시하거나 입력 오류로 닫는다. manifest label만 아니라 전이 lock 경로에도 같은 네 채널 회귀를 둔다.

## NOT_RUN·한계

- WSL jsonschema 외부 엔진은 NOT_RUN(미설치, 회귀 1개 skip). pattern 대조로 대체한 범위를 구분했다.
- 소비자 저장소 build/e2e/설치, 공용 패키지 실물, release tag/asset, npm/PyPI 게시는 NOT_RUN(범위 밖). 소비자에 쓰지 않았다.
- 기존 duplicate JSON key/lock scope 허용은 변경되지 않았다. 명시적인 중복 거부 계약이 없어 별도 finding으로 추가하지 않았다.
- 새 기능으로 범위를 확대하지 않고 두 개의 재현 가능한 계약 불일치에서 검토를 종료한다. 수정 후보의 재검토가 필요하며 이 candidate는 BLOCK이다.
