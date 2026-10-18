# Common39 FULL post-fix 독립 적대 리뷰 — Popper r4

판정: **PASS — COMMON_SOURCE_ONLY**, OPEN **P0 0 / P1 0 / P2 0**. 본인 r3의 **B-P1-03·B-P2-04 CLOSED**. 현재 진행 중 CI나 소비자 merge/deploy·운영 게이트의 PASS를 뜻하지 않는다.

## 불변 범위·격리

- 리뷰어 /root/review_finish_b, DB/lease/retry/fairness·누락 관점. 새로운 r4 상대 결과·모형·보고서를 보지 않았다.
- 보고서 고정: 2026-10-18T02:25:34.246184+00:00. 정밀 시작 timestamp는 별도 고정하지 않았다.
- Manifest /home/digitie/dev/reverse-address-common-review-manifest-20261018-r4.json
- Manifest SHA256 **509036aca1b4d83ce190a42317cb007c3ca6515d3c7a225ae8151b89eb20659f**
- Common base **c48595880aaad4367802ad71af2525a8a5e17c6a** → exact head **c067a7f6a11b106931a73cd7465503d90e54d976**. 이전 검토 제품 **14115ba99ab5d72d4f381d25b2dca810b24914d6**.
- base→head 전체 변경21파일을 대상으로 기존 FULL 검토를 재결박하고, r3→r4 변경3파일(구현/테스트/가이드) 전체와 연결 함수를 검토했다. Common AGENTS/CLAUDE/SKILL·리뷰/runbook 지침을 적용했다.
- 고정 git object만 읽었다. 원본 WIP·소비자 미커밋 보정·제품/index/branch 변경0. 이전 역사적 리뷰 보존 문서는 아카이브 검토일 뿐 새 독립 검증으로 합산하지 않았다.
- 모든 실행은 소유 TemporaryDirectory의 고정 모듈/파일SQLite/합성 provider·시각에서만 수행하고 종료 때 제거했다. -I -B, 소유 HOME/TMPDIR/cwd, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, /dev/null pytest config와 읽기 전용 Common venv interpreter를 사용했다.
- 운영 SSH/Docker/DB/proc, 실제 provider/key/SDK/브라우저/private/env/auth 접근0. Daemon start/restore0. OFF 정책을 변경하지 않았고 실제 현재 OFF 상태를 재관측한 것으로 주장하지 않는다.
- 영구 작성물은 이 보고서 하나다. 소비자는 문맥일 뿐 정식 source/CI/deploy 게이트가 별도다.

## 이전 지적 closure

### B-P1-03 CLOSED — cursor 앞 신규 위치의 기아 해소

- 수정 경계: reverse_address.py의 DatabaseAddressSource._work/has_work/page, refresh_reverse_addresses 시작·종료 cursor wrap.
- 같은 기존 반례를 실제 source SELECT/SQLite에 재현했다. 활성 z의 force 실패로 cursor=z/수동 cycle을 보존한 뒤 a(<z)를 INSERT했다.
- r4에서는 automatic=True와False 양쪽에서 a가 즉시 pending으로 잡혔다. batch_size=1의 다음 실행이 a를 정상 저장했다. z가 계속 오류여도 앞쪽 정상 작업이 막히지 않았다.
- a의 좌표를 다시 변경한 뒤에도 현재 좌표129를 재저장했다.
- provider가 m을 처리하는 도중 a(<m)를 INSERT한 별도 경계에서는 마지막 검사에서 remaining=1/cursor=''를 내구화했고 다음 실행이 a를 저장했다. 시작에서만 wrap하고 종료 직전 새 원천을 놓치는 경계도 확인했다.
- 따라서 r3의 고정 cursor/force early return로 신규 위치를 영구 누락시키던 반례는 해소됐다. 무한 유입·모든 동시 source 변경을 수학적으로 보장한 것은 아니다.

### B-P2-04 CLOSED — backoff-only 페이지에서 sensor run 억제

- 같은 자연 backoff 반례를 사용했다. 실제 store.save의10번째 실패로 next_retry_at=T+61,440초가 된 활성 a/b/c를 두고 force batch_size=1을 실행했다.
- r4는 실제 eligible SQL을 먼저 적용하므로 대기 행만 있다고 provider 호출이나 뒤쪽 페이지 소진 작업을 만들지 않았다. T+10분 has_work(automatic=False)=false, retries=[]였다.
- initial force의 requests=0/provider호출0/remaining=1은 수동 실패 재개 상태를 보존한다는 의미이며, 이것만으로 sensor가 계속 run을 만드는 것은 아니다.
- 정확한 backoff 만료 시각T+61,440초에는 다시 pending=true였다. 대기를 무시해 provider를 재호출하거나 기존 수동 cycle을 잃는 수정은 아니다.

## 추가 공격적 검증

새 OPEN P0/P1/P2를 발견하지 않았다.

- **오래된 같은 cycle/6개월/캐시**: 같은 좌표 a/b와 오류 z를 한 수동 cycle로 유지했다. a/b의 최초 제공자 확인은1회였다. 기한1마이크로초 전에는 같은 cycle 캐시가 있고 정확히 만료 시각에는 reuse가None이었다. 만료 뒤 실행은 정상 같은 좌표를 새로1회 확인하고 alias는 이를 재사용했다. 두 행의 checked_at은 새 시각이면서 cycle ID는 그대로였다. z 오류 요청은 이 정상 좌표 호출 수와 구분했다.
- **과거 정상 prefix**: 정상100개 뒤에 새 z가 있는 경우 batch_size=1에서 z를 바로 조회했다. requests1/skipped0으로 정상 prefix를 다시 읽기 위한 여러 run을 소비하지 않았다.
- **commit 뒤 cursor 전 중단**: 실제 save 후 두 번째 advance에 합성 예외를 주입했다. SQL eligible은 이미 저장된 결과를 제외하여 재개 때 제공자를 중복 호출하지 않고 cleanup을 끝냈다.
- **늦은 응답/lease takeover**: provider 중+91초에 새 owner가 claim하도록 했다. old save는 OwnershipLost로 거절됐고 late row가 생기지 않았으며 old release 뒤 replacement가 유지됐다.
- **삭제·비활성 오류와 limit**: 삭제 오류11개 뒤의 활성 live 재시도를 limit1에서도 선택·회복했다. 관련 기존 cleanup/수동 backoff/만료 owner 회귀도 pinned 테스트에서 통과했다.
- **원본·스키마**: r4에서 새 table/열/원천 쓰기 경로를 추가하지 않았다. 대상 검증/table/calendar/engine AST는 r3와 같다. store의 reuse를 제외한12메서드도 AST가 같다. 바뀐 reuse는 같은 cycle에도 next_refresh_at>now를 요구하는 조건뿐이다.
- **독립 SQL truth table**: missing/ok/not_found/error × 좌표 일치/변경 × cycle(None/old/current) × 기한(과거/정확히현재/미래) × 활성/비활성의144상태를 실제 SQLite 원천/파생 테이블에 만들었다. 별도 기대 집합과 SQL page의 automatic/manual 선택,26개의 mode·cursor·limit 집합/슬라이스 비교 및 retry 집합이 일치했다. PostgreSQL dialect compile도 수행했으나 실제 PG 실행은 아니다.
- 대상 source의 unique key·활성 SELECT 계약은 유지했다. 사용자 callback이 limit/order/원천 계약을 위반하는 모든 구현까지 보장하지는 않는다.

## 직접 실행한 검사

| 검사 | 본인 결과 |
| --- | --- |
| exact test_reverse_address.py 전체 + provider body-budget/slow-drip2개 | **25 PASS / 0 FAIL** |
| 이전 두 반례와 wrap/expiry/interruption/lease/negative-cache/orphan의 독립 명명 조건 | **19 PASS** |
| 별도 SQL144상태 +26 mode/cursor/limit 비교 + retry 집합 | 기대 집합과 일치 PASS |
| PostgreSQL eligible statement dialect compile | PASS, 연결0 |
| git diff --check base..head | PASS |
| 실제PG/provider/SDK/운영/소비자 formal gate/진행CI | NOT_RUN 또는 미확정 |

25/19/144/26은 서로 다른 실행·입력 단위이므로 합쳐서 전체 테스트 수로 표시하지 않는다. root가 제공한 engine23/전체509/Ruff·새4회귀 RED→GREEN·소유PG17·소비자UI22도 위 독립 숫자에 합산하지 않는다. 현재CI가 진행 중이라는 manifest를 따르며 전부green이라고 하지 않는다.

## 전체 source 결박·API·한계

- address_providers.py/address_dagster.py/pyproject.toml/uv.lock 및 workflow/review index는 이전14115와 byte 동일하다. 따라서 이전 본인 FULL의 provider fallback/로그 문맥 복원·정상 무결과 캐시·타임아웃/패키지 경계에 재결박했다. 핵심 변경은 eligible 선택·sensor predicate·wrap·동일cycle expiry다.
- 테스트 helper가 list predicate를 복제하던 방식에서 실제 DatabaseAddressSource SQL을 사용하도록 바뀐 것을 확인했다. 별도 truth table은 고정 row 상태의 의미를 기준으로 실제 SQL 결과를 대조했다.
- 새 page callback은 cursor/limit/now/cycle/force 5인자다. retries와 필수 pending_failures도 유지된다. 이 미머지 신규 API의 소비자 callback/pin은 최종 immutable 소비자 head에서 별도 확인해야 한다. 미커밋 WIP 연결을 소비자 PASS로 보지 않는다.
- Common 소스 PASS가 Weather의 동시 requestId 예약 지적이나 Admin UI/auth/session·OpenAPI·migration·deployment를 해결했다고 주장하지 않는다. 각 소비자 정식 gate가 필요하다.
- 실제 PostgreSQL 행락/동시 INSERT/savepoint/transaction isolation/NUMERIC 비교·권한·query plan, 실제 전원/프로세스 장애·provider quota/timeout·전체 RSS는 NOT_RUN이다. SQLite/fake와 PG compile을 실제 PG 수용으로 바꾸지 않는다.
- SQL LIMIT과 작은 순차 배치는 애플리케이션 row 상주량을 제한하지만, 큰 원천의 SQL plan·실DB CPU 및 VWorld 외부 SDK의 임의 대형 body/RSS 상한은 여기서 증명하지 않았다. 이전 메모리 한계를 유지한다.
- Daemon OFF를 재개할 권한·동작을 이 source 리뷰가 부여하지 않는다. 센서의 등록 RUNNING 선언은 실제Daemon ON 증거가 아니다.
- r3 BLOCK 원문과 두 반례는 그대로 보존한다. 현재 PASS는 exactc067에만 결박하며 향후 head·소비자·CI·운영 결과에 자동 확대하지 않는다.

## 변경 git object SHA256

| 파일 | SHA256 |
| --- | --- |
| .github/workflows/python-package.yml | 0ca74a1ec6ee1adb89f3071b93cb3a11d007131de18f066f267b797bd5e881d5 |
| docs/README.md | b68c3b4e4f96acd2dc71e81103dfda316cfb828c6797df254c2dd4f13dd6fd20 |
| docs/reverse-address-refresh.md | b3a3097b220f147f93ece80b42db4b34dc3bc5081b1af39c1bf796c2f6ab475e |
| docs/reviews/README.md | 8ba82451ec21577be4b38cc09e0e225db0a2fc2ccea1f0d5d0839c10b843232a |
| docs/reviews/adversarial/2026-10-18-reverse-address-refresh-post-fix.md | 394a026e5ab0524d0ef97f096d5dad8b3535829aa60059ae976b944d57998b75 |
| docs/reviews/adversarial/2026-10-18-reverse-address-refresh.md | 6c48e43afdc2f55c0ab57c368610c383f966b202c7c3465aa2de038eb882379f |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-manifest.md | d1d09256fa4260babac0bb9589685660d8894c0d4f321e30d083f866d3d54fb6 |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-r1-manifest.json | 92f7e3b810c510e5ad26d109e294414ffa44db81ebd2edbe907af0fbf544a486 |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-r1-reviewer-a.md | 287f22c998eb0a38cc8f223de5d88f3848e1cc66a3435dd71f8fcfcde28a4b65 |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-r1-reviewer-b.md | bba5179c431df1efeaeb6e81ca5904651d4853d8d2b9193fe4abe9bdda10c458 |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-r2-manifest.json | 3bbc3ae25d6c70a7fb36afc3229c81d411dc3f2c17117ef5386bc4de394d9d91 |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-r2-reviewer-a.md | 37c24ba0a0412bc1952248e77e65a60c65555153faee1d7c85758117ec4a76db |
| docs/reviews/adversarial/evidence/2026-10-18-reverse-address-refresh-r2-reviewer-b.md | 40e583ec972b72ec4a311c1ee5106cef2f50b29a0289efda09954adbfa579fc6 |
| packages/py/kor-travel-common/pyproject.toml | d0dc8ef64a6753f9e353918489ac39e273136196fa25ec41ca1119a9b033b9e9 |
| packages/py/kor-travel-common/src/kortravelcommon/address_dagster.py | 193cadfe6273dadd4161c9f6043679ced94dddb2ebb463dcb946105c38b89d02 |
| packages/py/kor-travel-common/src/kortravelcommon/address_providers.py | 76458d10de97ea48cb66bcd33049d8518d9907d4ab2aa3c16c5c2e8959200e4d |
| packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py | 96e4ea5bfaeecb08ee143c056f57a6ad99bda4d829015d8583a9e8089a21e31a |
| packages/py/kor-travel-common/tests/test_address_dagster.py | 165eeab8241843c5293ae86aaba86dbdeb331486c9b8a0b7d74ed6019bbc7885 |
| packages/py/kor-travel-common/tests/test_address_providers.py | 9dc413aadd1eefa3559b7d8072a55f7822a4526ea84fdfcb1a563bbf2fadbea4 |
| packages/py/kor-travel-common/tests/test_reverse_address.py | 6395d974b7cd22f8e64615857068d584b4078d841f0bbfa59658b36dca6b18a9 |
| packages/py/kor-travel-common/uv.lock | b982aa676a90d856a6dcf7a10ccfc6b5e1d8a37aedccf48cef0f62289e2e9599 |
