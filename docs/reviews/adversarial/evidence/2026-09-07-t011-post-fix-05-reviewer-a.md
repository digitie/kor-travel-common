# T-011 post-fix-05 독립 적대적 리뷰 A 원본

- 실행 ID: A-T011-POST5-20260907-205025
- 판정: **BLOCK**. 새 P2 2건(A-T011-P2-13, A-T011-P2-14)이 남아 있다. P0/P1 신규 발견 없음.
- 정확한 candidate: `94c445ec98aff74acbf1389c46a575dcb2bfa102`
- 전체 diff 기준 base: `3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5`
- candidate tree: `a72e4b74fcf565019e3d25120252c7043e75ea98`
- 격리: `F:/dev/kor-travel-common-wt/review-t011-post5-a`, candidate detached worktree.
- 시작: 2026-09-07 20:50:25.338 KST. 종료: 2026-09-07 20:57:48.229 KST(최종 상태 확인 시각).
- 시작/종료 HEAD와 tree는 위 값으로 동일하며 `git status --porcelain=v1`는 두 번 모두 빈 출력이었다.
- candidate 소스·문서·시험·source `.git/config`는 수정하지 않았다. 소비자 저장소 쓰기·commit·push·게시를 하지 않았다. 재현용 입력은 임시 디렉터리에만 만들었고 reviewer probe와 이 원본만 main `.git/codex-audit/`에 썼다.
- 상대 reviewer 결과 및 이전 review 원문은 읽지 않았다. 이전부터 보유한 A 실행용 probe를 현재 candidate에서 새로 실행했으며, 과거 성공 결과를 재사용하지 않았다.

## 전달 요청과 범위

요청은 post-fix-05에서 `_path_contains_symlink`가 manifest/lock/app/workspace와 중간 디렉터리 symlink loop를 양 OS의 일반 입력 오류(exit 2, traceback 없음)로 만드는지 검토하는 것이다. direct lock·direct manifest·companion pyproject/package·empty-lock app·workspace·중간 loop·외부 symlink·requirements 재귀와 기존 corpus, Windows/WSL 시험·정적 gate·정확한 후보 CI를 확인하며 미실행은 NOT_RUN으로 기록하도록 지시받았다. 최초 placeholder는 사용하지 않고 후속으로 전달된 위 full SHA를 고정했다.

전체 base..candidate의 39파일(+2400/-58) 목록과 구현·schema·초안·현재 규범/task/resume delta를 확인했다. 과거 review/report 16파일의 내용은 이번 비열람 지시 때문에 통독하지 않았으며, 전체 tracked 문서는 링크·plan·SPDX·비밀·redaction gate로 검사했다. 현재 task는 IN_PROGRESS이며 소비자 채택·설치·실행 성공으로 바꾸지 않았다.

## 직접 실행 검증

모든 Python 실행에 `-B -X utf8`를 사용했다. Windows는 Python 3.14.3, WSL은 uv managed Python 3.11.15이다. schema parity는 jsonschema 4.26.0을 사용했다. WSL 전체·focused 검증은 `uv run --no-project --python 3.11 --with jsonschema==4.26.0 python`으로 실행해 선택 의존성 부재 skip을 없앴다.

| 명령/검증 | Windows 실제 결과 | WSL 실제 결과 |
|---|---|---|
| `python -B -X utf8 -m unittest discover -s tests -q` | 201 tests, 59.782초, OK, skip 0 | 201 tests, 39.168초, OK, skip 0 |
| `python -B -X utf8 -m unittest discover -s tests -p test_validate_manifest.py -q` | 22 tests, 5.976초, OK, skip 0 | 22 tests, 3.912초, OK, skip 0 |
| `tools/validate_plan.py` | 106 task, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 344 documents, 2287 targets, 오류 0 | 동일 |
| `tools/check_spdx.py` | 32파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 434파일, 발견 0, 예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 434파일, 발견 0, 예외 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0 | exit 0 |
| `git diff --check 3977c00a5b4ffa21a8d29f96dd9531efbe3a0cb5 HEAD` | exit 0 | exit 0 |

위 정적 명령을 실행하는 보존 harness는 `.git/codex-audit/t011-post5-a-gates.py`이다. WSL의 Windows worktree 포인터 해석은 프로세스 환경 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t011-post5-a`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t011-post5-a`로만 지정했다. git config를 고치지 않았다.

정확한 CI는 다음 명령으로 확인했다.

```text
gh pr view 10 --repo digitie/kor-travel-common --json headRefOid,statusCheckRollup
```

반환 head는 candidate full SHA와 일치했다. 실제 run [34118599300](https://github.com/digitie/kor-travel-common/actions/runs/34118599300)의 docs, tools(ubuntu-24.04), tools(windows-2025), secret-scan, check-versions 5개가 모두 SUCCESS였다. 원격 job 내부 시험 건수/런타임을 별도로 읽지는 않았으며 위 201건은 독립 로컬 실행 결과다.

## 기존 반례의 현재 결과

다음 실행 harness를 두 OS에서 각각 실행했다.

```text
Windows cwd: F:/dev/kor-travel-common-wt/review-t011-post5-a
python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t011-post5-a-run.py

WSL cwd: /mnt/f/dev/kor-travel-common-wt/review-t011-post5-a
uv run --no-project --python 3.11 --with jsonschema==4.26.0 python -B -X utf8 /mnt/f/dev/kor-travel-common/.git/codex-audit/t011-post5-a-run.py
```

- 10개 초안: stdlib와 JSON Schema 모두 오류 0.
- schema 경로 395 corpus: 두 OS 모두 mismatch 0. 제어문자·DEL·경계 공백·절대경로·빈 segment·dot/dotdot 경계를 포함했다.
- 유효/윤년/0000/9999/끝 LF/비ASCII 날짜 9개: 두 엔진 판정 일치. 잘못된 review 날짜 3개도 거부.
- kind `[]`/`{}`: validator exit 1, traceback 없음. enforce·repo alias·잘못된 app·미지 필드 거부. 미지 key 값은 두 CLI에서 재노출되지 않았다.
- 선택 workspace의 node 하한/react 이동 선언은 각각 BELOW_FLOOR/FLOATING_REF; 명시 root selector는 root만 읽는 대조군으로 보존됐다. 원 발견의 잘못된 root 선택 회귀 없음.
- 빈 lockfiles ETL 선언은 Python/NO_LOCK을 root workflow와 함께 보고했으며 autodiscovery 결과와 일치했다.
- 외부 동반 package.json 및 외부 lock symlink는 exit 2, traceback/보고서 없음.
- requirements 11형식 × 명시 lock/빈 lock app = 22개: 재귀 root 이탈·외부 symlink·순환·누락·self-symlink는 exit 2, traceback/외부 값/보고서 없음. 정상 root 내부 상위 include 2개는 exit 0 보고서 생성.
- 민감한 workspace+transitive lock scope, DEL lock path는 stdout/stderr/JSON/Markdown/step summary에 원문이 다시 나타나지 않았다. 시험 비밀형 값은 문자열을 분할 생성했고 출력에는 leak boolean만 남겼다.
- direct requirements/npm lock self-symlink, 동반 package.json/pyproject.toml self-symlink, 직접 app self-symlink, workspace self-symlink, 중간 lock 디렉터리 self-symlink, root/manifest/registry의 checker 입력은 두 OS에서 exit 2, traceback 없음, 보고서 없음.
- 정상 내부 디렉터리 symlink로 읽는 app 선언·npm lock은 정상 보고했다. 일반 missing lock은 report 모드 exit 0 + NO_LOCK이며 설치 성공으로 해석하지 않았다.

누적 A 코드 반례 disposition: A-T011-P1-01/02/08, A-T011-P2-03/04/05/06/07/10/11은 위 실행 범위에서 FIXED. A-T011-P2-12의 원 workspace/intermediate lock 반례도 두 OS exit 2로 FIXED. 과거 문서 집계 A-T011-P3-09는 이전 결과 비열람 지시 때문에 이번 재판정 NOT_RUN이며 과거 disposition을 새 검증으로 주장하지 않는다.

## 새 finding A-T011-P2-13 — 빈 lock 앱의 중간 symlink는 존재 검사에서 사라짐

- 심각도: P2. disposition: OPEN, 수정 필요.
- 위치: `tools/check_versions.py:1839-1844`, `_manifest_declaration_scopes`.
- 원인: `candidate.exists()`와 마지막 component의 `candidate.is_symlink()`가 모두 false이면 `_resolve_input_path`, root containment 및 새 `_path_contains_symlink` 이전에 반환한다. `loop/etl`의 마지막 `etl`은 symlink 자체가 아니어서 중간 loop를 보지 못한다.
- 최소 재현: 초안 pinvi.apps-etl를 복제해 `lockfiles=[]`, `app="loop/etl"`로 두고 root/loop를 자기 자신을 가리키는 디렉터리 symlink로 만든다. root에는 정상 setup-node workflow와 manifest를 둔 후 `check_versions.py <root> --manifest <root>/manifest.json --mode report --json <root>/report.json --quiet --no-step-summary`를 실행한다. 모든 입력은 임시 디렉터리다.
- 실제 실행 파일: `.git/codex-audit/t011-post5-a-adjacent.py`의 `app_intermediate_loop`.
- Windows/WSL 동일 출력:

```text
app_intermediate_loop exit 0 traceback False report True rows [('uses', 'OK'), ('node', 'NOT_RECOMMENDED')]
app_intermediate_external_missing exit 0 traceback False report True rows [('uses', 'OK'), ('node', 'NOT_RECOMMENDED')]
```

- 두 번째 반례는 root/alias를 root 밖 디렉터리로 연결하고 `app="alias/missing"`으로 설정한다. 외부 파일을 읽지는 않지만 최종 app 경로의 root 이탈 검사도 실행하지 않는다.
- 영향: 손상된 앱 경로를 정상 부재로 취급해 앱 검사 전체를 누락하고 workflow 보고서만 생성한다. 이번 요청의 중간 app symlink 입력 오류 통일이 완성되지 않았다. exit 0은 report 모드 결과이지 모든 축 OK를 의미하지 않지만, 원래 입력 오류 2로 닫혀야 할 경로가 소거된다는 점이 결함이다.
- 권고: ordinary absent app를 허용하는 조기 반환 전에 lexical 경로 전체의 symlink와 resolved root containment를 확인한다. 중간 loop/외부 missing target은 일반 입력 오류로 닫고, 정상 내부 alias 및 symlink 없는 일반 missing app 대조군은 함께 고정한다.

## 새 finding A-T011-P2-14 — validator registry resolve가 WSL traceback과 경로를 노출

- 심각도: P2. disposition: OPEN, 수정 필요.
- 위치: `tools/validate_manifest.py:33`, `args.registry.resolve()`.
- 최소 재현: 임시 registry.json을 자신을 가리키는 symlink로 만든 뒤 정상 초안을 인자로 `validate_manifest.py <candidate>/templates/manifests/pinvi.apps-etl.lock.json --registry <temp>/registry.json`을 실행한다.
- 보존 명령: 앞의 두 OS 실행 형식에서 스크립트 경로를 `.git/codex-audit/t011-post5-a-validator.py`로 바꾼다.
- 실제 결과:

```text
Windows: validator-registry-loop exit 1 traceback False runtime-error False path-leak False
WSL:     validator-registry-loop exit 1 traceback True runtime-error True path-leak True
```

- 원인/영향: Python 3.11 Path.resolve의 RuntimeError가 validate_manifest_file의 읽기 오류 처리에 도달하기 전에 전파된다. WSL이 일반 validator 오류 목록 대신 traceback과 입력 경로를 출력한다. 종료 숫자 1 자체는 validator 계약과 같지만 처리된 오류·출력 비공개·두 OS 동작이 다르다. checker의 동일 registry 반례는 수정되어 이 문제를 대신 검증하지 못한다.
- 권고: 이 CLI의 registry resolve도 OSError/RuntimeError를 원문 없는 validator 오류로 변환하고 exit 1을 유지한다. leaf와 중간 디렉터리 loop를 시험하며 두 OS에 traceback·입력 경로가 없는지 assert한다.

## 미검증과 한계

- NOT_RUN: 실제 소비자 build/e2e·npm ci·uv sync·패키지 설치/게시·release. common 독립 리뷰이고 소비자 쓰기 및 registry 게시가 허용 범위 밖이다.
- NOT_RUN: 원격 CI 개별 job 로그의 내부 시험 건수 재집계. exact head/status 5개는 직접 확인했다.
- NOT_RUN: 이전 raw/report 내용 재감사. 비열람 지시를 준수했다. 문서 정적 gate 결과와 후보 구현의 새 실행을 대신 기록했다.
- probe runner 자체 exit 0은 각 CLI의 기대 동작 통과를 자동 뜻하지 않는다. 위 개별 반환 코드/보고서/누출 결과를 직접 판독했고, 새 반례 2건 때문에 최종 BLOCK이다.
