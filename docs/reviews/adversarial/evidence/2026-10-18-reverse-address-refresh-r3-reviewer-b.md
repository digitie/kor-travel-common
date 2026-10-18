# Common39 FULL post-fix 독립 적대 리뷰 — Popper r3

판정: **BLOCK**. 새 OPEN **P0 0 / P1 1 / P2 1**. 수동 실패 재개 자체는 해소됐지만, 지속 실패를 보존하는 cycle이 새 위치의 자동 갱신을 무기한 막는 P1과 backoff-only 페이지의 빈 run 반복 P2를 재현했다. 현재 exact14115에 대한 무조건 PASS는 불가하다.

## 불변 범위와 실행 격리

- 리뷰어 /root/review_finish_b, 복구·DB·동시성·누락 관점. r3 새 상대 리뷰 결과·모형은 읽거나 공유받지 않았다.
- 보고서 고정: 2026-10-18T02:15:34.330593+00:00. 정밀 시작 timestamp는 별도 고정하지 않았다.
- Manifest /home/digitie/dev/reverse-address-common-review-manifest-20261018-r3.json
- Manifest SHA256 **90eb2c39add81093deee1cc4ff84a9bf4655a8c4852e6333a18bf00018a3047e**
- Common base **c48595880aaad4367802ad71af2525a8a5e17c6a** → head **14115ba99ab5d72d4f381d25b2dca810b24914d6**. 이전 본인 검토 제품 **0f768a1974a65bfade4c0fa3c79b897c9663e1a6**.
- base→head 변경21파일의 전체 변경을 검토했다. 이전 제품 대비 새 reverse_address.py·테스트·가이드 전체와 연결 함수를 읽고, 이전 검토의 불변 부분은 객체/AST 동일성으로 재결박했다. 이전 Common AGENTS/CLAUDE/SKILL·리뷰/runbook 지침을 적용했다.
- 모든 제품·테스트는 git show exact head:path의 불변 객체만 사용했다. 원본 WIP/소비자 미커밋 보정/제품/인덱스/branch 변경0.
- git diff에는 공개된 과거 r1/r2 원문 보존 문서도 포함됐다. 역사 기록·링크·byte hash 대상으로만 다뤘고, 과거 원문/저자 결론을 현재 r3 독립 검증으로 합산하지 않았다. 새 r3 상대 결과는 미열람이다.
- 운영 SSH/Docker/DB/proc, 실제 provider/key/SDK/브라우저/private/env/auth 접근0. Daemon start/restore0. OFF 정책을 변경하지 않았다.
- 소유 TemporaryDirectory의 고정 모듈·파일 SQLite·합성 resolver/시각만 실행하고 종료 시 제거했다. 유일한 영구 작성물은 이 보고서다.

## 새 지적

### B-P1-03 — 실패 수동 cycle의 고정 cursor가 앞쪽 신규 위치를 영구 기아시킨다

- 위치: packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py:472–483,510–518,628–638,696–702.
- 조건: 마지막 key z에 대한 수동 force가 실패한다. 새 정책이 cursor='z'/force_refresh=true를 유지한다. 이후 현재 활성 원천에 a(<z)가 새로 생기고 automatic=True 상태에서 z만 계속 실패한다.
- 독립 재현: 실제 DatabaseAddressSource·ReverseAddressStore·refresh_reverse_addresses, 소유 파일 SQLite의 enabled 원천 SELECT를 사용했다. 처음 활성 z 한 행에서 force 실행→합성 provider가 z에만 실패. 다음 활성 a 행을 실제 INSERT했다. provider는 a에 정상 결과를 줄 수 있도록 작성했다.
- 결과: a 삽입 직후 has_work(T+1초,automatic=True)=false였다. 이후 각 backoff가 만료되도록 합성 시각을 하루씩 전진시켜4회 실행해도 calls=[z,z,z,z,z], a row=None, cursor='z'/force_refresh=true였다. 실제4일을 대기하거나 외부 API를 부른 것이 아니다.
- 원인: force branch가 뒤쪽 key 또는 기존 error의 due만 보고 먼저 반환하여 자동 모드의 일반 due 검사를 가린다. retries도 status='error'만 고르고 page는 고정 cursor 뒤만 읽는다. z 실패가 지속되는 한 동일 상태가 유지돼 a를 선택할 경로가 없다.
- 영향: 정상적인 위치 추가 후 다른 한 위치의 지속 오류 때문에 자동 주소 확인이 영구히 누락될 수 있다. 자동 갱신 ON도 이를 해소하지 못한다. 원천/fact 손상은 아니지만 「실패1건이 신규 위치를 영구 차단하지 않음」이라는 liveness 계약이 깨지는 P1이다.
- 권고: 수동 실패 보존과 전체 활성 원천의 eligible 작업 선택·cursor wrap을 함께 설계한다. 기존 실패 cycle을 잃거나 성공 위치를 매 tick 재호출하지 않으면서 앞쪽 신규/좌표변경/일반 due를 발견해야 한다. 실패가 끝날 때만 cursor를 초기화하는 것으로는 영구 오류를 해결하지 못한다.
- 필수 회귀: z 지속 실패+새 a(<cursor)+automatic ON에서 a가 유한 tick 안에 저장되어야 한다. 앞쪽 기존 위치의 좌표 변경, 비활성→활성 전환, 오래 유지된 같은 manual cycle의6개월 만료와 cache expiry도 함께 검증한다. 현재 직접 재현한 실패는 신규 활성 a 케이스다.

### B-P2-04 — backoff 대기 행만 남았는데 cursor 뒤 존재만으로 빈 run을 계속 만든다

- 위치: reverse_address.py:472–478,629–638,666–674. 가이드 docs/reverse-address-refresh.md의 backoff 대기 중 sensor run 억제 계약.
- 조건: 활성 a/b/c 모두 과거 오류이고 아직 backoff 대기 중이다. 수동 force를 batch_size=1로 시작하면 첫 a를 waiting skip하고 cursor='a'가 된다. 뒤 b/c도 모두 같은 대기 상태다.
- 독립 재현: 오류 횟수10의 상태를 실제 store.save 호출로 생성했다. 임의 retry timestamp를 최종 근거로 주입하지 않았다. 실제 식이 만든 next_retry_at=T+61,440초였다. force는T+30초, 다음 sensor 확인/실행은T+10분으로 두었다.
- 결과: source.retries(T+10분,10)=[]인데 has_work(automatic=False)=true였다. 다음 run은 requests=0/skipped=1/remaining=1, provider 총호출0이었다. 최초의 +24시간 임의 시각 fixture에서도 보였으나 최종 근거는 위 자연 생성61,440초 상태다.
- 원인·영향: page에 아직 뒤쪽 행이 있다는 사실을 실제 수행할 수 있는 작업으로 간주한다. 대기 행을 batch_size만큼 넘기기 위한 provider0 run이 필요 이상으로 반복된다. 유한한 반복이며 무한 루프라고 주장하지 않는다. 기본 배치50도 대기 행이50보다 많으면 같은 경계가 생긴다. 실제 운영 CPU/RSS 증가를 측정한 것은 아니다.
- 권고: 뒤쪽 페이지 존재가 아닌 실제 eligible 여부를 SQL에서 확인하고, 신규 유효 작업은 진행시키되 기다리는 오류뿐이면 기한까지 sensor run을 만들지 않는다. pending_failures는 cycle 보존, has_work는 지금 실행할 작업 판별이라는 역할을 분리한다.
- 회귀: 대기 오류만 N>batch에서 반복 has_work=false·provider0·불필요 run0, 일부 신규 위치가 섞이면 신규 작업 진행, 정확한 backoff 만료 시 다시true를 확인한다. 삭제/비활성 오류의1회 cleanup과 구별한다.

## 원래 수정의 closure와 통과 경계

### Weather W111-B-P2-01의 공통 원인 경계 — 제한된 재현에서 CLOSED

- force 실패 후 remaining=1/control.force_refresh=true를 보존한다.
- T+119.999999초에는 has_work(automatic=False)=false, 정확히T+120초에는true였다.
- 회복 resolver로 재개하면 기존 cycle ID를 유지하며 해당 오류만 처리하고 remaining=0이 된다.
- cycle 종료 뒤 automatic=False는200일 뒤 일반 달력 due도 다시 시작하지 않으며 automatic=True는 그 due를 발견한다.
- 이 closure는 Common의 단일 실패 재개 원인 경계다. 새 소비자 immutable head/API 연결의 정식 판정을 대신하지 않으며, 위 P1/P2가 남으므로 전체 Common PASS도 아니다.

### 비활성/삭제 오류가 retry limit을 독점하는 원인 경계 — CLOSED

- 삭제 오류11개·비활성 원천 오류11개와 활성 live1개를 함께 둔 실제 source join에서 retries(limit1)는 live만 반환했다.
- live 회복은 requests1로 완료됐다. source join을 limit 전에 적용한 효과를 확인했다.
- 유일한 오류 원천을 삭제하거나 비활성화하면 한 번의 cleanup pending이 생기고, provider 추가호출 없이 cycle이 끝난 뒤 pending=false가 된다.
- 대기 중 좌표 변경은 새 identity로 즉시 eligible이며 현재 좌표로 다시 저장됐다.

## 직접 실행한 검증

| 검사 | 본인 결과 |
| --- | --- |
| pinned test_reverse_address.py 전체 + provider body-budget/slow-drip2개 | **21 PASS / 0 FAIL** |
| 독립 manual/cleanup/orphan/동적좌표/callback/lease/cache/API 경계 | **명명19조건 PASS** |
| 신규 앞쪽 위치 기아 반례 | 실패 동작 재현: a 미저장, z만5회 |
| backoff-only 뒤쪽 페이지 반례 | 실패 동작 재현: due0인데 pendingtrue/빈run |
| git diff --check base..head | PASS |
| 실제 PG/SDK/provider/브라우저/운영/소비자 CI | NOT_RUN |

- 고정 소스를 빈 __init__의 소유 패키지로 추출해 무관한 SDK 초기화를 막았다. Common 읽기 전용 venv interpreter, -I -B, 소유 HOME/TMPDIR/cwd, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, /dev/null pytest config를 사용했다.
- 명명19조건에는 backoff 정확한 경계, auto OFF/ON 종료 구별,22orphan뒤 live1, 삭제/비활성 각각 cleanup, 좌표 이동, callback 예외 직후 재개, complete 직전 새 owner takeover 거절, negative cache partial resume, 필수 pending_failures 누락 시 TypeError/claim0이 포함된다.
- pending_failures에서 예외가 나도 저장 결과/cycle을 보존하고 다음 cleanup에서 provider 중복호출을 하지 않았다. 마지막 pending 확인 중+91초 takeover를 주입하자 old complete가 OwnershipLost로 막혔고 old release 뒤 replacement owner가 남았다.
- 기존 정상 무결과50개 수동 부분 재개는 provider1회·마지막 resolved_at=None·완료로 유지됐다. 기존 fallback·calendar·source 좌표 보존·lease 회귀는 pinned21검사에 포함됐다.
- AddressTarget/tables/six_months_after/address_engine/ReverseAddressStore는 이전0f와 AST가 같다. address_providers.py/address_dagster.py/pyproject.toml/uv.lock은 byte 동일함을 확인해 r2 검토에 재결박했다.
- 과거 공개 r1/r2 보고서4개의 archive SHA는 manifest 기록과 일치했다. 해당 보고서 수치/판정은 본인 r3 실행 수치에 합산하지 않았다.
- root의 Common505/Ruff/새4회귀 RED→GREEN은 별도 제공 증거다. 현재 CI가 일부 진행 중이라는 manifest를 따르며 green으로 집계하지 않았다.

## API·소비자·배포와 검증 한계

- 새 API는 page/retries callback과 필수 pending_failures callback을 요구한다. source.retries가 활성 원천 join/limit을 소유한다. 이번 미머지 신규 API 정리이며 base의 기존 공개 API를 임의로 호환된다고 주장하지 않는다.
- 두 소비자의 새 API/pin 연결은 WIP 문맥일 뿐, 이 Common 검토로 소비자 정식 PASS/CI/merge/deploy를 승인하지 않는다. Weather 동시requestId BFF 경합은 별도 소비자 지적이며 이 Common fix의 해결 범위가 아니다.
- 실제 PostgreSQL 동시 INSERT/savepoint/row lock·transaction isolation·NUMERIC/Float 계획·실driver/migration, 프로세스/전원 장애, provider timeout/quota·운영 RSS는 NOT_RUN이다. SQLite/fake 결과를 PG 실검증으로 바꾸지 않는다.
- source·좌표·fact 보존 원칙과 신규 schema 불변성은 이전 검토에 재결박했다. VWorld 외부 SDK 전체 body의 최대 메모리는 여전히 Common timeout만으로 증명하지 못한다.
- provider/키/Daemon/운영을 호출하거나 재개하지 않았다. 코드의 센서 등록 상태를 실제Daemon ON 또는 현재운영OFF 실관측으로 해석하지 않는다.
- 제품 변경은 없다. exact14115와 본인 이전 보고서를 보존하고 새 immutable head에서 P1/P2를 직접 closure해야 한다.

## 변경 git object SHA256

| 파일 | SHA256 |
| --- | --- |
| .github/workflows/python-package.yml | 0ca74a1ec6ee1adb89f3071b93cb3a11d007131de18f066f267b797bd5e881d5 |
| docs/README.md | b68c3b4e4f96acd2dc71e81103dfda316cfb828c6797df254c2dd4f13dd6fd20 |
| docs/reverse-address-refresh.md | 3a605e425095ed8c95103cfef25bcb159ad1b1afa8a56d9348172615a2af1176 |
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
| packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py | b31323d5a208abc1717a7e4dde2415d2328fcfc9cdbeded238f752c105455a75 |
| packages/py/kor-travel-common/tests/test_address_dagster.py | 165eeab8241843c5293ae86aaba86dbdeb331486c9b8a0b7d74ed6019bbc7885 |
| packages/py/kor-travel-common/tests/test_address_providers.py | 9dc413aadd1eefa3559b7d8072a55f7822a4526ea84fdfcb1a563bbf2fadbea4 |
| packages/py/kor-travel-common/tests/test_reverse_address.py | 18bf8f0859274d60840bb6937f9380b6b3fa2dd9acb2a53deee0e3b17bbb12b6 |
| packages/py/kor-travel-common/uv.lock | b982aa676a90d856a6dcf7a10ccfc6b5e1d8a37aedccf48cef0f62289e2e9599 |
