# Common35 다중 job 재시도 독립 적대 리뷰 D

- execution ID: `common35-review-finish-b-d-03396709-20261016`.
- 기준 HEAD: `03396709ce2d81644a6ceb1bd12021a0b4014df2`.
- base: `d1aa4bbacab87af9ebae08757bd3fcb80f748fe9`.
- manifest: `docs/reviews/adversarial/evidence/2026-10-16-multi-job-retry-manifest.md`.
- 검증 시작: 2026-10-16T02:01:27.127199Z(detached worktree `.git` 생성 mtime). 앞선 정책·소스 읽기의 별도 시작 시각은 계측하지 않았다.
- 검증 종료 기록: 2026-10-16T02:04:58.578615Z. 이후 core lazy-import 단일 확인과 이 원문 기록을 마쳤다.
- 전문 영역: 다중 target 귀속·실패 분류·예산·cursor·중복 인계·SDK 호환·검증 주장 범위.
- **verdict: PASS / OPEN0. P0=0, P1=0, P2=0, P3=0.** 소비자 채택·운영 승인·실제 복구 성공을 뜻하지 않는다.

## 독립성과 기준선

Common34의 작성자는 본인이다. 이번 독립 판정은 **Common35 base→HEAD의 전체9파일 delta**에 한정한다. 변경되지 않은 Common34 incarnation 정산 소스를 새 독립 리뷰 수로 세지 않았다. 작성자 C 및 다른 Common35 리뷰어 raw는 읽지 않았다. AGENTS/SKILL/문서 라우터·T-319·agent workflow·manifest와 source/test/가이드·장부의 해당9파일 전체 diff를 읽었다.

immutable Git object를 먼저 읽고 `/home/digitie/dev/common35-review-d-03396709-20261016`에 detached 검증 트리를 만들었다. 시작·종료 tracked status는 clean이고 HEAD는 위 고정값이다. 전체 binary diff SHA는 `db8c75c2a3d348f37b35b87441cfc0d04b8dcc284f3fb1c677da874637c0092e`이다. 파일별 Git blob SHA와 검증 결박은 `common35-review-binding-d-20261016.json`, SHA `cc1c5a2a8514404a1495de382281c5fae0530c467c7e87cc51412f02cfe10c2d`에 남겼다. 타인 제품·작업장·설정은 수정하지 않았다.

## 검토한 경계

`dagster.py`의 새 공개 factory와 private dispatcher(약205~259행)는 명시 mapping/pair를 등록 시 복사한다. 빈 mapping·key/job.name 불일치·비멱등/0재시도 policy·partition target을 거절한다. 각 후보에서 `(job,policy)`를 해당 실패 run의 job_name으로 선택하므로 다른 target의 config·runtime·retry 예산을 빌리지 않는다.

기존 실패 판정 본문(약260~448행)은 같은 내부 함수를 사용한다. project/location/repository/job origin, 부분 op/asset/check/실행 계획, 엄격 인프라 reason과 선행 STEP/provider 실패, retry 횟수, native/manual/Common child, 같은 job active를 유지한다. native ON에서는 기존 durable pending만 마무리한다. 다중 요청은 선택한 `job_name`을 명시하며 단일 API는 기존 `job_name=None`을 유지한다. source의 Common34 `dagster_recovery.py`·기존 health·HTTP·phase·의존성 파일은 변하지 않았다.

다중 scan(약455~548행)은 project FAILURE 최대100행 초기 page와 cursor/협력 budget을 공유한다. 목록 밖 job은 event 조회 전에 건너뛰고, page가 목록 밖100개여도 cursor가 전진해 더 오래된 적격 실패에 도달한다. 요청은 전역 tick당 최대1개이다. 단일 factory의 job filter/target도 유지한다. 전체 metadata SQL을1회로 만들거나 blocking 조회를5초 안에 강제 중단하는 구현은 아니며 가이드가 이 한계를 정확히 설명한다.

pending 원 parent의 native retry 억제·deterministic run_key·child 확인은 기존 경계를 사용한다. cursor가 유실되거나 sensor를 재구성해도 같은 parent/config/key를 재제안하며 이미 child가 있으면 새 요청을 억제한다. 단, 서로 다른 sensor origin과 동시 수동 launch의 원자적 once는 보장하지 않는다. 소비자는 이전 센서와 새 센서를 동시에 RUNNING으로 두지 말고 pending/child/cursor 전이를 정산해야 한다. 기본 RUNNING/60초는 기존과 같고, 소비자에 등록하는 순간의 역사 scan·실제 queue/worker 안전성은 별도 채택 gate이다.

Dagster target 등록이 기존 JobDefinition snapshot을 변경하는지 실제 SDK로 비교했다. 변경 없음이다. 공개 source import는 Dagster extra를 사용하는 모듈이고, core `import kortravelcommon`에는 새 eager Dagster/SQLAlchemy import가 추가되지 않았다.

## 본인이 실행한 검증

1. 실제 **Dagster1.13.24**의 읽기 전용 기존 Python 환경과 후보 src를 명시한 PYTHONPATH로, detached 패키지에서 `pytest --confcutdir=tests -q tests/test_multi_job_retry.py tests/test_recovery.py`: **78 PASS, 14.44초**. 신규22개와 기존56개의 합이며 각 집계를 다시 별도 합산하지 않는다. Common 로컬 SQLite fixture만 사용했고 Weather conftest·기본/공유 PG는 읽거나 실행하지 않았다. 로그 `common35-retry-tests-d-20261016.log`.
2. 추가 독립 모형 `common35-independent-models-d-20261016.py`: **12조건 PASS**. 서로 다른 op config/schema와 retry1/2·runtime301/601을 가진 두 target을 사용해 선택 job의 config/예산/parent를 검증했다. 예산 소진 job이 다른 job의 예산을 빌리지 않음, sensor 재생성 후 같은 key, 성공한 manual child 억제/pending 해제, 목록 밖100 failure의 event 조회0 및 다음 page 적격 run 도달, native ON pending 한정, 단일 `job_name=None`, 실제 JobSnap 불변, 정확한 두 target 등록을 확인했다. 결과 `common35-independent-models-d-20261016.result.json`, SHA `9904dbbc2d1f6df6aae5a05e7ed39a4129ce2dc9d6bbb7063495220238889202`.
3. 새 Python process에서 후보 core import 후 `dagster`/`sqlalchemy`가 sys.modules에 없음을 확인했다. `common35-core-lazy-d-20261016.json`, SHA `718c852adf824ec2a8930fa5112d005d0f8968984af72b6ea5eb34dff6d767fe`. SDK가 설치된 환경의 lazy-import 확인이며 core-only wheel 설치를 새로 수행했다고 주장하지 않는다.

모형 초기 두 번은 본인 fixture 오류였다. SDK1.13.24에 없는 `create_job_snap` import와 `sensor.targets`를 hashable set으로 취급한 오류를 각각 `.initial`/`.fixture2` source·log로 보존하고 실제 `JobDefinition.get_job_snapshot()`/`target.job_name` 계약으로 바로잡았다. 제품 실패나 성공 건수에 포함하지 않았다. 모델 성공은 실제 worker 실행/장애 주입/submit 완료 증거가 아니다.

## 문서·검증 주장과 잔여

신규 runbook은 한 초기 page와 tick 전체 SQL/하드 deadline을 구별하고 deterministic 제안과 실제 submit·worker 사망 증명을 구별한다. native 정책을 켜지 않으며 Common34 FAILED 정산과 retry RunRequest를 다른 책임으로 설명한다. journal/task/resume/CHANGELOG도 소비자 exact pin·센서 전이·실제 복구·CPU/RSS/live를 NOT_RUN/후속으로 둔다. 작성자의 전체443/별도161/core-only wheel·문서 gate는 작성자 evidence로 읽었으며 본인의78/12조건과 합산하지 않았다.

소비자 이미지·Weather17개 등록·pending 전이, 실제 run worker 유실 뒤 새 run 완주, 운영 CPU/RSS·live API/UI는 **NOT_RUN**이다. 실제 SDK1.13.25·별도 wheel 재설치·전체 Common suite·문서 validator 전체는 이번 독립 검토에서 반복하지 않았다. 운영 SSH/Docker/provider/HTTP/PG 호출0, 제품 수정0. 모든 도구·검증 process는 terminal이다.
