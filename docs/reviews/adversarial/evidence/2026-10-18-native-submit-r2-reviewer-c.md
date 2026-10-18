# Common41 C — 2704830 수정본 중간 검증

## 고정 범위와 판정

원23e FULL 원문과 반례는 그대로 보존했다. 이번 범위는 23e4775cf883b672ababad1b291bddd3441c9c63→2704830e98c4353e9770368eb1aea21833015b4a의7파일 delta와 연결 경계다. 제품 수정은 하지 않았다.

**SOURCE_HOLD_PENDING_NEW_FIX**다. 원 C41-C-P1-01은 두 SDK의 실제 SQLite에서 수정 효과를 확인했으나, root가 별도 PG 잠금 세션 유실 P1을 수용하여 작성자가 추가 수정 중이다. 그 다른 리뷰 원문/모형은 읽지 않았으며 이번 원문으로 전체 SOURCE_PASS를 집계하면 안 된다.

## 독립 확인

새 모듈의 SQLite 파일 잠금과 PG 별도 NullPool session advisory try-lock, 잠금 안 fresh status→submit, busy 오류 경계를 전체 읽었다. 원 함수8개(version·shape·identity·scope·schema·CLI)는 AST가 같고 _launch만 새 잠금 구간을 쓴다. 기존 lock 외부 package의 version/source/artifact는 바뀌지 않았으며 dagster-postgres와 psycopg2-binary 두 package만 추가되었다.

불변 Git 모듈을 소유 scratch에 복사해 두 readonly SDK interpreter로 직접 실행했다.

| SDK | 새 원집중 회귀 직접 실행 | 본인 독립 회귀 | 결과 |
|---|---:|---:|---|
| 1.13.24 | 44 | 11 | 55 PASS |
| 1.13.25 | 44 | 11 | 55 PASS |

원 P1 순서에서 다른 요청이 stale context로 coordinator에 두 번째 진입하기 전에 SubmissionBusyError로 거절됨을 확인했다. 첫 제출 뒤 공식 RUN_START 이벤트를 소유 SQLite에 기록하고 같은 요청을 다시 제출해도 STARTED와 단일 run이 유지됐다. 동시 호출의 busy 오류는 같은 UUID 재시도 후 성공/충돌 여부를 검사하며 성공으로 무시하지 않았다. 원 권한·config·태그·UUID·scope·재시작·늦은 생성·schema/CLI/lazy import 회귀도 포함한다.

## 실제 PostgreSQL 부분 검증과 fixture 오류

root가 허용한 loopback PostgreSQL의 전용 DB common_native_review_c를 새로 만들었다. SDK.24 실제 storage/native submit에서 다음 구간까지 실행했다.

- NOT_STARTED 영속화 후 병렬 복구 busy 거절과 STARTED 비회귀.
- 공식 optimize_for_webserver로 native run pool size1/max_overflow0를 만들고 그 유일 연결을 대여 중이어도 별도 잠금을 얻음. 새 잠금이 native engine checkout을 추가하지 않음.
- 본문 예외 원본 보존과 해제, 다른 run의 동시 잠금 및 같은 run busy.
- 소유 자식 프로세스의 os._exit(7) 뒤 PG session 잠금 해제/재획득.
- 자기 DB에서 본인이 만든 잠금 session 하나만 종료한 경우 본문 원예외 보존과 후속 재획득.

마지막 전체 연결0 assertion은 FAIL했다. 제 fixture의 psycopg2 connection context가 transaction만 닫고 관측 연결 자체를 닫지 않아 자기 관측 연결1이 남았다. 원 실패 fixture/log를 보존하고 contextlib.closing으로 명시 close하도록 수정했으나, 추가 제품 fix 대기 및 자기 DB 정리 대기로 재실행하지 않았다. 이 실패를 제품 결함이나 PG 최종 PASS로 집계하지 않는다.

첫 자기 DROP은 외부 controller15초 대기를 초과했다. 후속 RO에서 자기 DB 세션0, OID681906에 PID8162의 AccessExclusiveLock granted만 확인했다. root는 이 PID가 정확 자기 DROP DATABASE이며 CheckpointStart 대기임을 추가 RO 확인했다. root의 다른 suite가 끝난 뒤 자연 완료를 기다리기로 했고 다른 session의 취소·종료나 추가 DROP은 하지 않는다. 현재 DB 제거 완료를 주장하지 않는다.

## 증거와 제한

- 원문/원반례: /home/digitie/dev/common41-independent-review-c-r1-20261018.md.
- 이번 scratch: /tmp/common41-review-c-7f11mf80/r2.
- 기계 증거: /home/digitie/dev/common41-independent-review-c-r2-interim-20261018.safe.json.
- 기계 증거 SHA256: 7f0edc7795a2efc857bc8888dbda538f5cdfc55339a85b18534fb04f39f2205f.

운영/SSH/provider/daemon/worker 실행과 원본 source/index/branch 변경은0이다. PG는 root가 별도 허용한 local 전용 DB만 사용했고 기존 공유 DB를 변경하지 않았다. 다른 reviewer/작성자의 판정이나 root의 소비자 실측을 본인 독립 근거로 합산하지 않았다. 새 제품 exact HEAD가 오면 기존 원문 보존 후 후속 closure가 필요하다.
