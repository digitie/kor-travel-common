# Common #39 독립 적대적 리뷰 — Popper r1

판정: **CONDITIONAL — P0 0 / P1 0 / OPEN P2 2**. 아래 두 정상 무결과 처리·호출 예산 문제를 고치거나, 소유자가 명시적으로 계약을 정정하고 회귀 및 수용 조건을 확정하기 전에는 무조건 PASS로 집계하지 않는다. PostgreSQL 실경합과 소비자 통합 게이트에 대한 승인도 아니다.

## 실행·불변 범위

- 리뷰어: /root/review_finish_b, 독립 Popper 관점. 다른 리뷰어의 결과·모형·리뷰 원문은 열람하지 않았다.
- 실행일: 2026-10-18 KST. 종료 기록: 2026-10-18T01:32:17.766374+00:00. 시작 시각은 별도로 고정하지 않았으므로 정밀한 소요 시간은 주장하지 않는다.
- Manifest: /home/digitie/dev/reverse-address-review-manifest-20261018-r1.json
- Manifest SHA256: 92f7e3b810c510e5ad26d109e294414ffa44db81ebd2edbe907af0fbf544a486
- 정식 범위: Common #39, base c48595880aaad4367802ad71af2525a8a5e17c6a → head 812b291659e40564595c3c28b7e8d51cbcc46df9.
- Common AGENTS.md / CLAUDE.md / SKILL.md, 문서 라우터·리뷰 템플릿·agent-workflow runbook 및 기능 가이드를 읽고 변경 11파일의 delta와 연결 구현을 검토했다.
- Common 작업 트리에 다른 작업자의 미커밋 변경이 있으므로 제품·테스트는 반드시 git show HEAD:path의 불변 객체를 사용했다. 기존 WIP·branch·index·source를 수정하거나 되돌리지 않았다.
- Weather 3516a89 / Transport e1e6035의 연결 모듈은 호출 계약을 이해하는 맥락 참조뿐이다. 소비자 CI 완료나 소비자 정식 리뷰 PASS로 계산하지 않는다.
- 운영 SSH·Docker·SDK 실행·실 DB·provider 네트워크·브라우저·private/env/auth/proc 접근 0. Daemon 기동·정지 0. 기존 Daemon OFF 정책 유지.
- 유일한 영구 작성물은 이 보고서다. 테스트의 임시 소스/SQLite는 소유 TemporaryDirectory 안에만 만들고 종료 때 제거했다. 실제 SDK 라이브러리는 일부 public .py 구현을 읽기만 했다.

## 지적

### B-P2-01 — VWorld 오류 뒤 정상 Kakao 무결과도 오류로 남아 짧은 재시도가 반복된다

- 위치: packages/py/kor-travel-common/src/kortravelcommon/address_providers.py:200–210, 특히 204–210. 저장 결과 연결: reverse_address.py:323,332,337–342,627–630.
- 재현 조건: 두 키가 설정된 resolver에서 VWorld 조회가 예외로 실패하고, Kakao coord2address가 정상 HTTP 200 및 documents=[]를 반환한다. 제공자 정상 무결과 자체는 기존 reverse()의 반환 계약인 None으로 표현된다.
- 독립 재현: exact812b의 실제 reverse()를 호출했다. _vworld만 합성 실패 async 함수로 주입하고 HTTPX MockTransport가 정상 Kakao documents=[]를 반환하도록 했다. pacing만 제거했으며 네트워크와 SDK 호출은 없었다. 이후 실제 refresh_reverse_addresses / 파일 SQLite 저장까지 연결했다.
- 결과: failure='vworld_failed'가 남으므로 ReverseAddressError('vworld_failed')가 발생했다. DB status='error', error_code='vworld_failed', next_retry_at=현재+120초, next_refresh_at=None, run status='partial_failure'/failed=1이었다.
- 기대와 영향: docs/reverse-address-refresh.md의 VWorld 실패 시 Kakao fallback 및 정상 무결과의 달력 6개월 확인 계약에 따르면, 정상 fallback 무결과를 오류와 구분해야 한다. 현재는 Kakao가 정상 응답해도 6개월 확인이 성립하지 않아 같은 좌표를 backoff마다 다시 호출한다. 과거 정상 payload가 있으면 실패/stale로 남는 반면 이번 확인은 완료로 기록되지 않는다. 잘못된 주소나 fact 변경은 재현하지 않았으며 자료 보존 침해 P1로 확대하지 않는다.
- 최소 정정 방향: Kakao가 예외 없이 정상 None을 반환한 경우 이전 VWorld 실패를 어떻게 종결할지 명시하고 구현한다. 보수적으로 '설정된 모든 제공자의 무결과만 정상'이라는 의도라면 현재 가이드의 일반 fallback/무결과 계약을 그 의미로 좁히고 회귀·UI 상태·재시도 quota를 명시해야 한다.
- 회귀: VWorld 실패+Kakao 정상 empty, VWorld empty+Kakao empty, 두 제공자 실패, Kakao 정상 주소 성공을 구분하고 저장되는 status/next_refresh_at/next_retry_at까지 검증한다. 정상 fallback empty의 기대값을 정하는 것은 정책 결정이며 이 리뷰가 임의로 서비스를 바꾸지는 않았다.

### B-P2-02 — 동일 좌표의 정상 무결과를 재사용하지 않아 위치 수만큼 제공자를 다시 호출한다

- 위치: packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py:258–281, 특히 273; 호출 경로 618–626.
- 재현 조건: 서로 다른 50 target_key가 동일한 longitude/latitude를 가진다. 모두 미확인 상태이며 resolver가 각 호출에 정상 None을 반환한다. 같은 좌표에는 같은 provider 응답을 재사용한다는 가이드 계약을 적용했다.
- 독립 재현: exact812b의 실제 DatabaseAddressSource.page/lookup, ReverseAddressStore, refresh_reverse_addresses를 사용했다. 파일 SQLite targets 50행을 삽입하고 실제 SQL 문자열 키셋 정렬을 거쳤다. 정상 None resolver와 정상 address payload resolver를 각각 새 DB에서 대조했다.
- 결과:
  - 정상 None: processed=50, provider calls/requests=50, reused=0, failed=0, remaining=0, has_work=False.
  - 정상 address payload 양성 대조: processed=50, provider calls/requests=1, reused=49, failed=0, remaining=0, has_work=False.
- 원인·영향: None 결과는 status='not_found' 및 6개월 next_refresh_at으로 정상 저장되고 같은 target에서는 재호출을 억제하지만, reuse()는 status=='ok'만 고른다. 정상 무결과도 좌표만으로 결정되는데 다른 target_key에서는 같은 조회를 반복한다. 수동 전체 갱신·좌표가 중복된 위치에서 quota와 실행 시간을 최대 위치 수에 비례해 낭비하며 배치/시간 한도에 더 빨리 걸린다. 이것이 운영 quota 고갈이나 CPU 장애를 이미 일으켰다는 주장은 하지 않는다.
- 최소 정정 방향: 정상 not_found를 캐시 후보에 포함하되 payload=None을 보존하고 checked_at/resolved_at/next_refresh_at, 현재 force cycle 및 좌표 일치 계약을 유지한다. 기존 호출부 622행은 cached.status에 따라 None을 처리할 분기가 이미 있으므로 해당 분기와 함께 검토한다.
- 회귀: 동일 좌표 정상 empty 50행에서 한 번 조회, 다른 좌표는 별도 조회, 6개월 due 시 재조회, manual cycle별 재조회, error는 정상 negative cache로 재사용하지 않는 조건을 검증한다.

## 독립 검증과 반례 배제

Common venv의 읽기 전용 interpreter를 사용하되 -I -B, sterile HOME/TMPDIR/cwd, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, /dev/null pytest config로 실행했다. git show로 뽑은 두 제품 모듈과 기존 테스트만 소유 임시 디렉터리에 두고 빈 package __init__로 다른 제품·SDK 초기화를 차단했다.

- pinned 기존 test_reverse_address.py 전체 및 provider의 body-budget/slow-drip 2개: **14 passed / 0 failed**. 원저자 495 전체 통과나 CI green은 이 숫자에 합산하지 않았다.
- 독립 파일 SQLite 두 동시 최초 claim: 정확히 winner true 1개 / loser false 1개. SQLite에서의 재현이며 PG 행락 PASS가 아니다.
- 만료 후 새 owner를 획득시킨 뒤 이전 owner의 save/advance/complete 모두 OwnershipLost; 이전 release 후에도 새 owner 유지.
- 결과 commit 직후 cursor advance에 합성 예외를 넣고 재개: provider 총 1회, 두 번째 실행 requests=0.
- 새 Engine으로 재연결: 수동 cycle ID/cursor/force가 보존되고 자동 호출도 그 cycle을 이어간다.
- 저장 payload JSON 변환 오류: 파생 row가 남지 않음. 원천/fact 테이블 쓰기는 제품 경로 자체에 없다.
- B-P2-01은 정상 fallback transport → 실제 SQLite error/backoff 저장까지 재현했다.
- B-P2-02 최종 반례는 실제 DatabaseAddressSource SQL 키셋을 사용했다. 초기 임의 list callback의 정렬 불충족으로 생긴 remaining 수치는 근거에서 제외하고 DB 키셋으로 다시 검증했다.
- git diff --check base..head: PASS (exit 0).

## 나머지 경계·배포 판단

- 달력 월말/KST 경계, force의 같은 cycle 재개, 좌표 이동 시 이전 주소 미노출, 실패 시 이전 payload/resolved_at 보존, provider만 바뀐 결과의 changed 미증가는 위 pinned SQLite 회귀에서 통과했다.
- lease fencing은 control UPDATE의 owner와 lease 조건 및 같은 transaction의 저장으로 구성되고, 새 owner가 있으면 이전 worker가 저장·해제하지 못하는 경계를 확인했다. HTTP를 DB transaction 밖에서 수행한다. 실제 PG 동시 INSERT/savepoint/row-lock 및 statement/lock timeout 경합은 **NOT_RUN**.
- result 저장과 cursor 저장이 별개 transaction임을 확인했다. 저장 직후 중단의 중복 provider 억제는 위 fixture로 통과했지만 실제 프로세스 SIGKILL/DB 접속 단절/전원 손실의 모든 지점은 **NOT_RUN**.
- 기본 batch 50/최대500, run budget30/최대300초 및 provider 순차 호출을 읽었다. Kakao 128KiB body budget은 기존 회귀를 통과했다. VWorld는 외부 SDK에서 응답을 완전히 읽고 파싱하므로 Common timeout만으로 전 단계 메모리 상한을 증명할 수 없다. 실제 비정상 대형 SDK 응답·OS 메모리 상한은 **미검증 한계**로 남기며 운영 OOM 발생을 주장하지 않는다.
- address_engine PostgreSQL dialect 변환과 connect/statement/lock timeout은 소스로 검토했다. reverse-address extra의 SQLAlchemy/httpx/VWorld immutable git pin 및 uv.lock 정합, 기존 optional/core-only 설치 구조를 확인했다. 새 실제 wheel/모든 지원 Python 빌드 및 PostgreSQL driver 설치는 **NOT_RUN**.
- 새 테이블을 소비자 migration에서 고정해야 한다는 가이드는 있다. Weather/Transport migration·DB 실제 schema·Admin 수동 예약·원천/관리자 좌표/fact 보존·브라우저·공개 API 실제 동작은 **정식 소비자 게이트 NOT_RUN**.
- Dagster 센서/수동 job의 정적 호출·tag/run status/10분 주기 연결을 읽었으나 SDK를 실행하지 않았다. 센서 default RUNNING 선언은 코드 등록 상태이며 실제 Daemon 기동 증거가 아니다. Daemon OFF 상태의 운영을 바꾸지 않았다.
- 이번 판정은 exact Common head에만 결박한다. 향후 fix는 새 immutable head와 두 지적의 직접 회귀로 별도 closure가 필요하다. 소비자 CI 진행 중이라는 의뢰 범위를 넘겨 통합 PASS를 선언하지 않는다.

## 변경 객체 SHA256

| 파일 | SHA256 (git show exact head bytes) |
| --- | --- |
| .github/workflows/python-package.yml | 0ca74a1ec6ee1adb89f3071b93cb3a11d007131de18f066f267b797bd5e881d5 |
| docs/README.md | b68c3b4e4f96acd2dc71e81103dfda316cfb828c6797df254c2dd4f13dd6fd20 |
| docs/reverse-address-refresh.md | 7f49b7a42b1793dc399daed81312b6c2fde50eb47e62d6a48e47bcd72fd6e68c |
| packages/py/kor-travel-common/pyproject.toml | d0dc8ef64a6753f9e353918489ac39e273136196fa25ec41ca1119a9b033b9e9 |
| packages/py/kor-travel-common/src/kortravelcommon/address_dagster.py | 193cadfe6273dadd4161c9f6043679ced94dddb2ebb463dcb946105c38b89d02 |
| packages/py/kor-travel-common/src/kortravelcommon/address_providers.py | 8fbfe960f69d8d5110d6b1b7a10f47b63f4f7c267f0b6c2248ec0e30a9f8d627 |
| packages/py/kor-travel-common/src/kortravelcommon/reverse_address.py | 078a8d64c4e4e99354b968e23f4766e1292f720e4a9d8b0599c5964292acda3f |
| packages/py/kor-travel-common/tests/test_address_dagster.py | 165eeab8241843c5293ae86aaba86dbdeb331486c9b8a0b7d74ed6019bbc7885 |
| packages/py/kor-travel-common/tests/test_address_providers.py | c86645194afbbb89e21514d2b1f3a0bcc9947343cc3ef77c7bb73f59d7b371af |
| packages/py/kor-travel-common/tests/test_reverse_address.py | 26e228f9a1df2c65bf9655aafbee9412e9ebd98a9cbba617ba9f491ee063cc38 |
| packages/py/kor-travel-common/uv.lock | b982aa676a90d856a6dcf7a10ccfc6b5e1d8a37aedccf48cef0f62289e2e9599 |
