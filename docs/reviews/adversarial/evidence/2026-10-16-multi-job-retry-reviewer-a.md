# Common35 다중 job 인프라 재시도 독립 FULL 리뷰 A

**merge verdict: PASS — 고정 소스 범위 / 열린 P0·P1·P2·P3 0.** 소비자 채택·운영 복구·성능 및 다른 reviewer/CI gate의 완료를 뜻하지 않는다.

## 실행·요청과 기준선

- execution ID: common35-A-03396709-20261016T020746Z
- 시작 근거: 별도 archive 생성 2026-10-16T02:07:46Z / 원문 고정 2026-10-16T02:12:08Z 이후.
- 전문 영역: 실제 Dagster SDK 계약, job별 귀속·cursor/예산·pending/native 전이, 실패 격리와 재시도 확대 방지.
- 전달 요청 원문: “다음 Common35 exact03396709ce2d81644a6ceb1bd12021a0b4014df2/base d1aa 독립 specialist FULL9 delta 리뷰를 시작해 주세요. Common AGENTS 먼저 읽고 immutable object/detached archive 자체환경, SDK1.13.24 실제 테스트/모형, peerraw 읽지 마세요. C author이므로 A+D 2subagent 필요. C의 Weather96 r5 continuation source가 곧 나오면 그 운영 복구 리뷰를 최우선으로 전환합니다. 운영/DB/HTTP/빌더/제품수정0. 다른 작업자 변경 되돌리지 않기. 리뷰원문 P/common35-multi-job-retry-review-a-20261016.md. 기존 handoff/checkpoint는 summary 참조.”
- commit `03396709ce2d81644a6ceb1bd12021a0b4014df2`, product `1b599c4663737c468ce163af03d446beb3d210fc`, base `d1aa4bbacab87af9ebae08757bd3fcb80f748fe9`.
- manifest: `docs/reviews/adversarial/evidence/2026-10-16-multi-job-retry-manifest.md` SHA256 `6c5499f3098d1eafcce9a4a419f80bff192c73a212519b32c01155ea8413a93e`.
- 격리: git show/diff와 exact Git archive. `/home/digitie/dev/common35-review-a-03396709-20261016` / archive SHA256 `729fbbbc388c8b24f4bdc7ff6210f376fba401e0eda2e8482d8eb3b834821e10`. 9개 실제 blob/hash를 전부 대조했다. 원본 checkout HEAD exact/마지막 clean 확인, 원본 및 소비자 제품 편집0. archive의 import cache는 검증 입력으로 사용하지 않았다.
- AGENTS→docs/README→resume→T319→workflow→동일 manifest 순으로 읽었다. CodeGraph 실행파일은 존재하나 이 object/archive 리뷰에서 mutable graph index를 만들지 않고 git diff/rg/직접 호출 경로·AST로 대체했다. peer raw/상대 검증 결과는 읽지 않았다.

## FULL9 범위

`packages/py/kor-travel-common/src/kortravelcommon/dagster.py`, `tests/test_multi_job_retry.py`, `CHANGELOG.md`, `docs/journal.md`, `docs/resume.md`, `docs/runbooks/dagster-adoption.md`, `docs/runbooks/dagster-multi-job-retry.md`, `docs/tasks/T-319-dagster-recovery.md`, 동일 review manifest를 모두 읽었다. 기존 deadline과 단일 재시도 전체 body도 대조했다.

## 공격한 계약과 판단

1. **공개 API 호환/선택 귀속** — 단일 factory의 signature·default RUNNING/60초·RunRequest.job_name=None을 유지한다. 다중 factory는 mapping을 등록 때 복사하고 job.name과 key, 비어 있지 않음, 멱등/양수 retry·비partition을 확인한다. SDK1.13.24 SensorDefinition이 실제17targets를 등록하며 요청은 선택 job_name/config/policy에만 귀속됐다. 입력 pair 변경이 등록 allowlist를 바꾸지 않는 코드와 회귀도 확인했다.
2. **원 판단 보존** — nested retry_failed_run의 기존 전체 AST가 dispatch 부분과 RunRequest의 새 job_name keyword를 제거하면 base와 exact임을 독립 계산했다. provider/불명 실패·부분 op/asset/plan·project/location/repository/job origin·시도 횟수·child·active·pending 판단을 다중화 명목으로 확대하지 않았다. Common34 incarnation 정산·health·phase·의존성 파일은 범위 밖이며 변경0이다.
3. **scan/cursor와 예산** — project FAILURE 초기 최대100 한 페이지만 공유한다. 허용 밖 job은 event 조회 없이 넘어가고 100페이지 끝 cursor/짧은 tail→head 및 여러 job 사이 다음 cursor가 전진했다. 5초 협력 예산에서 이미 처리한 run까지 저장하며 초기 scan이 job 수만큼 반복되지 않는다. 10초 wrapper와 8초 인계 여유는 그대로며 blocking metadata를 SQL hard timeout이라고 주장하지 않는다. event/child/active 조회까지 SQL1회로 오인하지 않는 가이드가 정확하다.
4. **최대1/pending/native/경쟁** — 한 tick RunRequest는 최대1개이며 parent pending/native 억제 태그를 기록한 뒤 deterministic key를 반환한다. 재생성 후 같은 pending은 같은 key/tags를 재제안한다. native ON은 pending 외 위임하고 기존 child는 새 인계를 막는다. 다른 job active는 선택 job을 막지 않는다. 여러 sensor origin/수동 launch와의 원자적 once를 보장하지 않으며 이전 개별 센서와 새 센서를 동시에 RUNNING으로 두지 않는 이관 문구가 있다. 기존 child 제출·physical worker 소멸을 이 factory가 증명한다고 쓰지 않는다.
5. **오류와 문서** — metadata 오류는 성공 cursor로 소비하거나 요청으로 바꾸지 않는다. default RUNNING 등록은 소비자 전이 gate임을 명시한다. 실제17개 Weather 채택/CPU·RSS 개선·운영 복구를 로컬 단위 결과로 완료 처리하지 않았다. author suite/1.13.24/wheel/문서 수치는 author evidence로 구분되어 있다.

## 실제 독립 실행과 원문

- 고정9 blob/hash/scope exact, 기존 retry 판단 AST 동일성, 원본 HEAD/clean: PASS.
- 실제 설치 Dagster **1.13.24**의 JobDefinition/SensorDefinition/RunRequest/RunsFilter/Event 객체 + 합성 metadata instance로 standalone **32조건 PASS**. 실제 tick 함수와 기존 deadline wrapper를 호출했다. DB·network 연결을 금지한 상태이며 실제 job body는 실행하면 실패하도록 했다.
- 확인:17targets 초기 scan1, 최대1요청, 선택config/예산, parent durable pending, 재생성 key/tags, 다중 cursor, 단일 None 호환, provider/불명/부분/foreign/예산/step 음성, native/Common child 중복, same/other job active, native ON pending, unknown job/noevent, 100+tail cursor, 5초 checkpoint, metadata 예외와 무쓰기.
- 모형은 SQL 구현이나 Dagster daemon을 대체하는 가짜 성공으로 집계하지 않는다. 실제 SDK의 public object 및 tick 반환 경계와 app이 주입하는 metadata protocol을 시험한 것이다.
- 모형: `common35-independent-sdk-model-a-20261016.py` SHA256 `a9b63549f1b939210534388ca1e8cfea3c4aa3774cce49e98fc1b60edfbf8696`.
- 결과: `common35-independent-sdk-model-a-20261016.private.json` SHA256 `53063f729d13640ff3293b1488ec3ec2b5413bfb11401d67563e4edbeafafa6c`.
- scope/AST 원문: `common35-scope-check-a-20261016.private.json` SHA256 `71b99f2e9373d214dc3a4021df7f390c45620ca8c6686fda0e7278a0e831c024`.
- 실제 DB/SQLite/HTTP/SDK 원격/PG/provider/Docker/builder/서비스/소비자 source 변경0. 모든 소유 도구 terminal.
- 보고서 고정 shell 명령1회가 quoting 오류로 Python 실행 전에 실패했다. 제품/검증 입력 및 결과 파일 쓰기0이었으며 이 Markdown을 별도 apply_patch로 생성했다. 시험 실패나 제품 결함으로 집계하지 않는다.

## 미실행·불확실성

독립 전체 pytest/SQLite suite·새 wheel 설치·ruff/docs gate·실제 소비자 이미지/daemon·pending 제출 후 crash·shared-origin 경쟁·운영 CPU/RSS/live는 NOT_RUN이다. 명시 DB0 범위 때문에 author SQLite 회귀를 새로 실행하지 않았으며 작성자443/161 또는 상대 결과를 본인32조건에 합산하지 않았다. baseline 자체의 여러 sensor 사이 원자적 once·SQL 호출 hard deadline·무제한 수동 launch의 배제는 이번 additive factory가 새로 보장하지 않는다. consumer가 실제 scope/pin/기존 센서 중지·pending 정산·lease/queue 계약을 확인해야 한다. 실행하지 못한 운영 gate를 PASS로 승격하지 않는다.
