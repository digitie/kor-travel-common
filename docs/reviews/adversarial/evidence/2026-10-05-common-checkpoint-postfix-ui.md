<!-- SPDX-License-Identifier: GPL-3.0-only -->

# Common STEP_FAILURE 체크포인트 — 독립 post-fix 적대 리뷰 원본

- 실행 ID: COMMON-CHECKPOINT-A-20261005-f801f01.
- 리뷰어: James (/root/review_ui).
- 시각: 2026-10-04 22:19:30~22:22:19 UTC / 2026-10-05 07:19:30~07:22:19 KST.
- 저장소: F:/dev/kor-travel-common-geo-dashboard.
- base: 92ebfa60ef976d830c08b353de633103650175ad.
- 실제 immutable candidate: f801f01b2dc34b642a64bbf847fa268ac172e4ed (Git rev-parse 확인).
- 범위: 고정 객체의 전체 7파일 delta. Dagster factory/child tests/guide 및 smoke dev.3 파일명·lock version 정정. 제품 UI426 런타임 변경 없음.

## 격리

상대 보고서·통합 판정은 읽지 않았다. Git show/diff/archive만 사용하고 소스·부모 mirror·설치·공유 DB·컨테이너는 변경하지 않았다. /tmp/james-common-checkpoint-f801f01에 자체 고정 snapshot과 공격 script를 생성했다. 기존 Geo venv의 Python3.12.13/Dagster1.13.24를 PYTHONPATH로 재사용했다. 모든 instance는 자체 local_temp SQLite이며 외부 provider/PG 접근은 없었다.

## 수행 검증 (EXECUTED)

1. 고정 candidate tests/test_child_crash.py + tests/test_recovery.py: **64 PASS, 23.87초**. 실제 multiprocess os._exit(42), fallback/native budget·pending ACK 유실·scope/부분선택·중복·기존 deadline 회귀를 포함한다.
2. 본인 기존 C-CHILD-P1-01의 실제 100+1 두 페이지/각5.1초 fixture를 그대로 유지하고 다음 tick에 반환 cursor를 전달하여 재실행했다. 실제 outer10초 제한을 단축하거나 모의하지 않았다. 첫 tick 5.11초에 steps:[run,"page-2",100] 반환, 요청0·태그 쓰기0. 두 번째 tick 5.11초에 요청1·child 잔여예산0·태그 쓰기1. 페이지 방문은 [null,"page-2"]이며 처음부터 재검사하지 않았다. 세 번째 tick에서 뒤의 오래된 eligible run이 진행함도 확인했다.
3. 별도 실제 evaluate_tick 공격 7개 PASS. 자체 clock만 모의해 checkpoint 경계를 빠르게 만들었고 storage/context는 실제 SQLite를 사용했다.
   - 뒤 페이지 USER_CODE_ERROR/ValueError: 요청0·태그 쓰기0, 부분 검사만으로 승인하지 않음.
   - 이어 읽는 metadata ConnectionError: 예외 전달·기존 checkpoint 유지·태그 쓰기0; 복원 후 같은 다음 페이지에서 요청1.
   - native retry ON으로 전환, pending이 없던 부모: 다음 STEP 페이지를 읽거나 억제 태그를 쓰지 않고 위임.
   - parent project 변경: scope 재검증으로 이어 읽기/요청/쓰기0.
   - 재시도 attempt 소진: 이어 읽은 뒤 예산 재검증으로 요청/쓰기0.
   - checkpoint parent 삭제: head로 복귀, 요청/쓰기0.
   - 검사가 끝났지만 인계 전 elapsed9초: 완료 cursor checkpoint, 요청/쓰기0; 다음 tick에서 end 이후를 읽어 요청1, child pending 태그 미상속.
4. 고정 smoke diff에서 package.json/lock/prepare-lock의 dev.3 파일명과 lock version 일치를 확인했다. 이 리뷰에서 Next smoke build는 실행하지 않았다.

재현 script:
- /tmp/james-common-checkpoint-f801f01/slow_pages_probe.py
  SHA256 ed2eeb21a3ad2096a34a71cd7d0a697629d102e3ee9178a74c2aae442108d1e9.
- /tmp/james-common-checkpoint-f801f01/checkpoint_boundary_probe.py
  SHA256 cc1131aac2bb4669ca1c63b571d6cc9157bdcea71c2915e6e05d9e510c714aff.

```bash
cd /tmp/james-common-checkpoint-f801f01
PYTHONPATH=/tmp/james-common-checkpoint-f801f01/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python slow_pages_probe.py
PYTHONPATH=/tmp/james-common-checkpoint-f801f01/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python checkpoint_boundary_probe.py

cd packages/py/kor-travel-common
PYTHONPATH=/tmp/james-common-checkpoint-f801f01/packages/py/kor-travel-common/src TMPDIR=/tmp TMP=/tmp TEMP=/tmp /home/digitie/dev/kor-travel-geo-codex-dagster-common-test/.venv/bin/python -m pytest -q tests/test_child_crash.py tests/test_recovery.py
```

## Finding disposition

**C-CHILD-P1-01 (기존 P1): CLOSED.** severity를 변경하지 않았다. 기존의 여러 정상 유한 페이지가 누적10초를 넘겨 동일 run을 영구 반복하던 재현이, durable sensor cursor 전달 후 실제 두 tick 요청1로 바뀌었고 첫 tick 늦은 pending/native 억제 쓰기가 없다. 뒤의 실패도 진행한다. 기존 원문은 변경하지 않았다.

**신규 P0/P1/P2/P3 finding 없음.** checkpoint는 resume 시 job/status/project/location/repository/선택 범위·실패 사유·native 위임과 총 재시도 예산을 다시 검증한다. 검사 중 요청과 native 억제 태그를 쓰지 않는다. 다음 페이지에서 provider 오류나 metadata 장애를 발견하면 안전하게 보류한다. 문서가 부분 검사를 승인한다고 설명하지 않는다.

## NOT_RUN·한계

Dagster1.9, 실제 PG/production daemon·native ON 동시 운영, live UI/전체 소비자 및 Next clean build/CI는 직접 실행하지 않았다. 부모64PASS를 본인 결과로 대체하지 않았고 위64건은 자체 실행 결과다.

단일 storage 호출 자체가10초를 넘는 경우에는 외부 deadline이 스레드를 강제 종료하거나 페이지 내부를 checkpoint하지 못한다. 기존 bounded4 worker 방식의 한계이며 이 리뷰에서 그 장애 조건을 정상 복구로 판정하지 않았다. 이번 폐쇄는 기존의 각 호출은 정상5.1초에 반환하지만 합계가10초를 넘는 본인 재현을 기준으로 한다. storage 장애·잘못된 checkpoint JSON은 예외가 유지되므로 운영자가 오류 상태를 관측할 수 있어야 한다. 임의로 sensor cursor를 위조·편집하는 운영자에 대한 보안 경계는 이번 범위가 아니다.

## 최종 판정

**PASS (고정 f801 delta의 독립 코드·실행 검증).** C-CHILD-P1-01은 실제 재현으로 폐쇄되었다. 소비자 Geo가 이 SHA로 pin을 갱신했는지와 publication guard·live/CI는 별도 고정 후보 리뷰 및 gate 대상이며 이 보고서는 이를 완료로 주장하지 않는다.
