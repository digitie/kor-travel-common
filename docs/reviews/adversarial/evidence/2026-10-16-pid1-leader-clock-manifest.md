# Common36 PID1 leader clock 판독 리뷰 manifest

- 요청: QEMU의 호출 스레드별 일반 proc stat rewrite를 incarnation 변경으로 오인하는 결함 수정.
- immutable 제품 후보: a34cbd8e2242542abecad3987fb7e9aa87993ab7
- base: eaf83e965ee837a277d5d7b370ecde0d4897f1cd (Common35 스택)
- task: [T-319](../../../tasks/T-319-dagster-recovery.md), [적용 계약 §15](../../../runbooks/dagster-adoption.md#15-컨테이너-재시작-뒤-native-실행-정산)
- PR: [#36](https://github.com/digitie/kor-travel-common/pull/36), draft. 두 독립 리뷰·CI·운영 드릴·소비자 pin/이미지는 후속이다.
- 범위: 아래3파일. 제품 clock reader만 최소 수정하며 공개 API·cursor·launcher/ownership·namespace/cgroup/NTP·복구 predicate·기본 STOPPED는 유지한다. 이 manifest 추가는 문서만이다.

| 파일 | SHA256 |
|---|---|
| packages/py/kor-travel-common/src/kortravelcommon/dagster_recovery.py | c9b06b628c1dd9d428049cc56e6ff468c6ff2638c25f076bf0586ccc0dbc8844 |
| packages/py/kor-travel-common/tests/test_native_incarnation.py | fba3b91c61ce8cf80d93a94cacf3204ad025d3cf0b831fd5c1eea68f255694be |
| docs/runbooks/dagster-adoption.md | b25086a3751323c1884704414f4f0f5d18bb589cbbcd17001be4ed8b5ddb98e3 |

## 수용 조건과 실제 반례

PID1 leader TID1을 명시한 /proc/1/task/1/stat를 두 번 읽고 기존 _start_ticks의 PID1·양수 검증을 적용한다. 같은 boot/namespace/cgroup/clock 가드를 우회하지 않는다. leader 경로 부재·손상·불일치는 None이며 일반 stat fallback은 없다. user-code reload나 호출 thread의 시작 tick을 선택하지 않는다. Linux procfs의 task 경로 의미는 가이드 링크를 따른다.

root/A의 격리된 ARM64 QEMU PID1-only 실제 관측 원문 SHA256은 3ada39c0baaaba11f621a374e0ec7c57022a491ba0e9a997c51e2dcf0770012d다. host PID1 시작 tick과 canonical leader3개 표본은 모두280141436이었고, 일반 stat는 main280141442/thread280142033이었다. D는 해당 고정 원문을 읽고 해시·필드 일치를 검증했으며 운영 조회를 하지 않았다. 일반 Dockerexec 스레드에서는 이 현상이 재현되지 않았다는 별도 관측과 혼동하지 않는다.

## 실행한 검증

- 구제품 + 새 anchor 회귀: 7 FAIL / 6 PASS / 77 deselected (1.17초). 새7개가 legacy thread 변화/canonical stable, PID mismatch·zero·문자열·짧은 stat·부재·두 표본 변화다.
- 새 native 복구 파일:90 PASS (2.67초). 기존83개 포함이며 신규7개와 합산해180개라고 세지 않는다.
- 전체 Python 패키지:450 PASS (113.24초), warning1. actual Dagster1.13.24의 로컬 SQLite/합성 proc; Weather conftest/PG/운영0.
- Ruff0.16.4 변경 Python2파일 PASS.
- 문서 링크725문서/2884targets 오류0, plan109 오류0.
- 문서 unittest337실행/336 PASS/1 SKIP (65.108초). 최초 Node 의존성 미설치로38failures/3errors였고 npm ci --ignore-scripts 뒤 재실행 통과. 최초 실패를 성공으로 덮어 세지 않는다.
- uv wheel/sdist build + 새 core-only Python3.13 venv 설치 PASS. wheel source에 canonical 경로 포함/Dagster import0 확인.
- git diff --check PASS. CodeGraph init/sync/status 사용; fallback 아님.
- 신규 API·consumer·운영 드릴/복구·CPU/RSS 개선은 NOT_RUN. 기존 실제 실패/커서 변경0.

실제 패키지 명령은 repo root에서 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1과 PYTHONPATH=packages/py/kor-travel-common/src를 명시하고, SDK1.13.24 환경의 python -m pytest --noconftest -c /dev/null packages/py/kor-travel-common/tests -q를 사용했다. 이는 새 SDK 설치 증명이 아니며 별도 core wheel 설치만 새 환경에서 수행했다. lock/pin/consumer image를 바꾸지 않는다.

## 리뷰 요청

A와 C가 동일 immutable 후보의 전체3파일·기존 reader를 독립적으로 읽는다. thread/leader 귀속, malformed/unstable failclosed, 기존 clock/namespace/cgroup 보존·cursor 호환·증거 범위 과장을 공격한다. 상대 원문은 두 결과 확정 전 미공유한다. 두 리뷰 원문과 disposition은 완료 후 별도 closure로 보존한다. 현재 리뷰 판정은 PENDING이며 작성자 시험은 독립 리뷰로 집계하지 않는다.

## 독립 리뷰 종결 후속

고정5d2의 A/C FULL4 SOURCE_PASS/OPEN0·원문SHA와 CI8SUCCESS를 [통합 판정](../2026-10-16-pid1-leader-clock-closure.md)에 보존했다. 위 PENDING은 최초 요청 시점이며 이번 closure로 소스 리뷰만 해소됐다. 제품/규범/수용 기준은 같고 실제 lab·소비자 배포·운영 효과/최종closure CI는 별도다.
