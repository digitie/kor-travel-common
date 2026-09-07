# T-011 post-fix-07 독립 적대적 리뷰 B 원본

- 실행 ID: `T011-POST7-B-20260907-210742-KST`
- 최종 판정: **PASS**. 새 P0/P1/P2/P3 finding 0건. B-P1-12와 B-P2-11 및 누적 B finding은 FIXED.
- candidate: `4680bacdf285f2cc86f1a18cc1de29ff4129f2a8`
- tree: `9aaede40d0905e2b989971650a806f1ba7f48aa0`
- immutable diff base: `3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5`
- parent: `56d6ae11d5917eb2b2e69f8f26f90b903bacceb6`
- 최초 조회: `2026-09-07T21:07:38.2698809+09:00`; detached 검증 시작: `2026-09-07T21:07:42.3210981+09:00`; 종료: `2026-09-07T21:11:00.9427093+09:00`.
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post7-b`. 시작·종료 SHA/tree 동일, `git status --porcelain=v1` 두 번 모두 빈 출력.
- source `.git/config` 시작·종료 SHA256 동일: `EDF33489791777FC04CB8F11CB627188653B86378FE26FF3B4A6F81179CB897A`. `core.worktree` 등 Git 설정 수정 없음.
- candidate/소비자 소스·문서·시험 수정, commit/push/게시 없음. 자체 fixture는 OS 임시 디렉터리에서 실행했고 원본·자체 스크립트는 source `.git/codex-audit`에만 기록했다. 상대 결과는 읽지 않았다.

## 요청과 범위

> Post-fix-06 findings on 56d6ae1 are fixed; 이제 post-fix-07 최종 독립 review를 수행해줘. 후보 SHA 4680bacdf285f2cc86f1a18cc1de29ff4129f2a8, base 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5. Focus: registry missing/self/intermediate symlink 및 schema/path/값 redaction이 양 OS에서 exit2·generic·no traceback/no marker인지, 기존 B-P2-11 corpus, direct/intermediate/external symlink for manifest/lock/app/workspace/requirements, 모든 report/annotation channels, schema parity를 재검증. base vs candidate 원인·수정 경계를 명확히 기록하고, 이전 상대 결과는 보지 말아. source .git/config core.worktree를 수정하지 말고 후보 소스 수정 금지. 정확한 CI·Windows/WSL tests/gates 확인, 미실행은 NOT_RUN. 원본 `.git/codex-audit/2026-09-07-t011-post-fix-07-reviewer-b.md`, 시작/종료 SHA/tree/clean/hash/verdict 기록. P0/P1/P2 신규 0이고 누적 finding FIXED면 PASS.

직접 parent 대비 변경은 `tools/check_versions.py` registry 오류 출력 2줄과 `tests/test_check_versions.py` 회귀 15줄이다. 오류의 `{exc}`를 고정된 일반 메시지로 대체하며 exception 처리 종류와 exit 2는 보존한다. Registry.load의 유효 데이터 판정과 정상 report 작성 경로는 불변이다. 앞서 독립 검토한 immutable base 이후의 schema/manifest/경로 수정은 이번 corpus로 다시 확인했다. base 대비 versions.json/CI/packages 변경 목록은 비어 있다.

B-P1-12의 missing registry 및 malformed schema 원문 노출은 고정 base에서도 직접 재현했던 기존 결함이다. 이 후보는 그 기존 오류 출력 경계를 보완한다. 따라서 이전 후보에서 새로 도입한 회귀를 되돌렸다고 설명하지 않는다. B-P2-11은 base 이후 추가된 빈 lock app 탐색의 조기 반환 문제였으며, 직전 수정의 구성 요소 검사를 유지하고 이번에 양 OS로 다시 확인했다.

## 새 실행과 검증 결과

Windows Python 3.14.3은 `py -3.14 -B -X utf8`, WSL Ubuntu-26.04 Python 3.11.15는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`을 사용했다. WSL 전체 테스트는 `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR`로 실행했다. 읽기 전용 WSL validator에만 해당 detached worktree의 Git 경로를 process 환경으로 전달했다. 설정 파일은 변경하지 않았다.

| 명령 | Windows | WSL |
|---|---|---|
| `-m unittest discover -s tests -q` | 203개, 104.249초, OK, skip 0 | 203개 발견, 62.351초, 201개 성공·2개 skip |
| `tools/validate_plan.py` | task 106, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 문서 344, target 2287, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32개, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 434개, 발견 0·예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 434개, 발견 0·예외 0 | 동일 |
| `tools/check_versions.py --self-check` | 자체 검사 통과 | 동일 |
| `git diff --check 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5 HEAD` | exit 0, 출력 없음 | exit 0, 출력 없음 |

`gh run list --commit <candidate>`와 `gh run view 34120043104 --json headSha,conclusion,jobs`를 직접 조회했다. head SHA 일치, run success, Windows/Ubuntu tools·docs·secret-scan·check-versions 5개 job 모두 success. URL: https://github.com/digitie/kor-travel-common/actions/runs/34120043104 . 로컬 반례 실행과 CI 관찰을 구분한다.

## 직접 반례와 출력 채널

아래 자체 스크립트는 source `.git/codex-audit`에 있고 candidate worktree 경로를 인자로 받아 실행했다. 두 OS에서 동일 corpus를 재실행했으며 상대 보고서는 읽지 않았다.

- `review-t011-post7-b-cases.py`: missing/self/중간 registry, malformed schema, 민감 미지 field, null registry 6종 × report/warn/fail/self-check 4모드 = **OS별 24개 CLI**. 두 OS 모두 `total=24, fixed=24, failures=[]`. exit 2, stdout가 정확히 고정 일반 annotation, stderr 빈 값, 합성 marker 없음, JSON/Markdown/step summary 미생성.
- `review-t011-post6-b-cases.py`: 8 fixture × 2 CLI = **OS별 16개 CLI**. check_versions registry/manifest 실패는 exit 2·원문/traceback 없음, standalone validator는 고유 계약인 exit 1·원문/traceback 없음. missing lock의 NO_LOCK과 validator의 형식 검사 exit 0은 보존.
- `review-t011-post5-b-cases.py`: 8 fixture × 3모드 = **OS별 24개 CLI**. B-P2-11 app 중간 self-symlink와 외부 링크 아래 없는 app은 정상 root workflow를 동반해도 exit 2·report 미생성. 직접/중간 manifest, package companion, requirements 부모 순환도 동일. 정상 내부 app 링크는 선언과 NO_LOCK 판정을 보존한다.
- `review-t011-post6-b-corpus.py`: 기존 자체 `review-t011-b-cases.py`, `review-t011-post-b-cases.py`, `review-t011-post2-b-cases.py`, `review-t011-post3-b-cases.py`, `review-t011-post4-b-cases.py` 실행. 마지막 스크립트는 fail/report/warn 모두 실행했다. 모든 스크립트 정상 종료, 내부 의도된 CLI exit 1/2는 성공 실행과 구분했다.
- `review-t011-post7-b-valid.py`: 유효 registry의 파일명에 합성 marker를 넣고 정상 report를 생성했다. 양 OS 모두 예상 NO_LOCK exit 1, stdout/stderr 및 JSON/Markdown/step summary에서 marker 없음. 일반 report 경로를 막아 오류 비공개를 달성한 것이 아님을 확인했다.

반례 명령 예:

```text
py -3.14 -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/review-t011-post7-b-cases.py F:/dev/kor-travel-common-wt/review-t011-post7-b
wsl.exe -d Ubuntu-26.04 /home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/review-t011-post7-b-cases.py /mnt/f/dev/kor-travel-common-wt/review-t011-post7-b
```

## 누적 B finding disposition

| 원 ID·심각도 | 상태 | 이번 증거 |
|---|---|---|
| B-P1-01 | FIXED | 민감 unknown field·scope의 stdout/annotation·JSON·Markdown·summary 원문 미노출 |
| B-P1-02 | FIXED | 외부 package/pyproject companion, lock, manifest, workflow symlink exit 2 |
| B-P1-03 | FIXED | 실제 npm member의 Node 18 선언 BELOW_FLOOR, root 선언으로 가려지지 않음 |
| B-P2-04 | FIXED | 제어문자·경계 공백·날짜 schema/stdlib 반례; 달력 corpus 5,082개 불일치 0 |
| B-P2-05 | FIXED | kind 배열/객체 입력이 오류가 되며 TypeError traceback 없음 |
| B-P1-06 | FIXED | strict requirements 직접·재귀 root 이탈 exit 2, 내부 정상 include 보존 |
| B-P3-07 | FIXED 유지 | 집계가 수정된 767db839의 해당 통합 문서와 현재 파일이 동일함을 `git diff --name-only <767db839> HEAD -- docs/reviews/adversarial/2026-09-07-t011.md`의 빈 출력으로 확인. 상대 내용 재열람 없이 기존 확인을 재사용 |
| B-P2-08 | FIXED | 전이 lock scope의 DEL/tab/합성 토큰이 모든 report 채널에서 미노출 |
| B-P1-09 | FIXED | 직접 lock·pyproject companion·empty-lock app·requirements self-symlink 안전한 exit 2 |
| B-P2-10 | FIXED | 중간 lock 경로와 npm workspace 순환이 양 OS·3모드 exit 2 |
| B-P2-11 | FIXED | empty-lock app 중간 순환/외부 링크 누락 leaf가 조기 반환을 우회하지 않음 |
| B-P1-12 | FIXED | registry 오류 24개 matrix와 두 CLI corpus에서 일반 오류·no marker·no traceback |

정상 경로 control, 10개 draft의 validator CLI, 민감 전이 scope, calendar corpus도 다시 실행했다. Windows의 실제 Draft202012Validator와 WSL의 정규식 직접 대조를 서로 같은 실행으로 세지 않았다. 정책상 정상 누락 app에 workflow만 있으면 workflow report를 내는 동작, requirements의 선언 전용 NO_LOCK, 중복 scope fixture의 기존 처리에는 이번 변경으로 인한 회귀가 없었다.

## NOT_RUN과 판정 한계

- NOT_RUN: WSL 외부 jsonschema 엔진 시험 2개(모듈 미설치). 2 skip을 pass로 집계하지 않았다. Windows 실제 schema 엔진 및 WSL 정규식/date corpus는 각각 실행했다.
- NOT_RUN: 소비자 실제 채택/빌드/e2e, package 배포와 npm/PyPI 게시(범위 밖). 소비자 쓰기 없음.
- 재사용: B-P3-07은 이미 독립 확인한 정정 문서의 Git 동일성을 확인했다. 상대 리뷰 원문을 재열람하지 않았다.
- 이 PASS는 exact candidate의 T-011 도구·schema 및 요청된 오류/경로/출력 계약 범위다. 소비자 정책 준수나 제품 배포 gate의 PASS를 뜻하지 않는다.
- 새 finding 0건, 누적 B finding FIXED, 실제 실행 gate와 exact CI 성공으로 **PASS**를 확정한다.
