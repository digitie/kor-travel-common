# stdlib bytecode 빌드 CLI 독립 리뷰 manifest

## 요청과 불변 기준선

사용자 CPU 우선 개선 요청에 따른 opt-in 빌드 CLI다. 작성자 C, PR37 초안이며
Common36 feature를 base로 한다. 기존 source/API/수집·복구·health 동작과 환경은 유지한다.

- base: 200a350101665f44246422c7102c087fdfb3222e
- 제품·가이드 후보: 084585796bc4428dc9a3347f08f8ebaaa04bdfa3
- 제품4파일 전체 diff SHA256: 9949db4a1fda6080b660cec21fb02207967629dd54608a64b9b6841434460791
- 이 manifest를 추가한 최종 commit은 PR의 불변 HEAD로 확인한다. 제품4파일 bytes는 위 후보와 같다.
- 전문 리뷰어 A/D는 같은 manifest와 source를 독립 검토하고 상대 원문을 보지 않는다.
  작성자 테스트를 두 독립 리뷰로 세지 않는다. 최종 리뷰·finding disposition·CI·merge는 별도 gate다.

| 파일 | SHA256 |
| --- | --- |
| packages/py/kor-travel-common/src/kortravelcommon/build_bytecode.py | b07c7f94565147f619bffba7f1f9871106c0ee07d3683974393d596ffda5d266 |
| packages/py/kor-travel-common/tests/test_build_bytecode.py | b29c5de25bbacaae7a3146f922ddf457e0f8fb567d3502e25c575a6435dd1110 |
| docs/runbooks/dagster-adoption.md | 51b5abd4e06d95087be31a56153db7a208752c955eb7fc10b98a0b2f4de3ca91 |
| docs/tasks/T-319-dagster-recovery.md | c3644891876a45b713af22f51e44e925525c4e52a76c2e786e62be5f0fc09eb9 |

## 수용 계약과 공격 범위

명령은 python -m kortravelcommon.build_bytecode --stdlib 한 가지이며 임의 path 인자는 없다.
실제 interpreter의 sysconfig stdlib를 worker1/force/checked-hash/optimize0으로 준비한다.
site-packages/dist-packages/test/tests/idle_test는 stdlib 상대 범위에서 제외한다.
외부 source/directory symlink 및 cache 목적지 escape·별도 pycache prefix, 읽기/쓰기 권한 실패,
empty tree·syntax error·timestamp cache·같은 크기/mtime source 변경을 공격한다.
실패 nonzero와 기존 flags/Env 불변, 기존 모듈 byte 동등성, Python3.11/core-only wheel을 확인한다.

이 기능은 신뢰하는 단일 writer 이미지 빌드용이며 concurrent source mutation의 sandbox가 아니다.
경로 guard·컴파일 실패를 성공으로 숨기지 않는다. 실패 전 일부 pyc 생성 가능성과 삭제/rollback
미제공을 가이드에 기록했다. 실제 stdlib 빌드/이미지 배포·HC CPU 효과를 source PASS로 승격하지 않는다.
제품·태스트·빌드 API·명령 의미와 가이드 §17/T319 수용 기준 전체가 리뷰 범위다.

범위 밖: 소비자 source/핀·Dockerfile·실제 빌드·배포, provider/DB/schema/PK/CAS,
payload·작업 cadence/concurrency, 런타임 자동 compile·환경 변경·health timeout 상향.

## 작성자 실제 검증과 한계

- package Ruff 전체 PASS.
- 새 작은 stdlib fixture26 PASS: 비root 권한·scope·source 해시 무효화·CLI opt-in 포함.
- Python 전체476 PASS/114.57초, module bytes 전후 동일. uv.lock의 Dagster1.13.25 환경이며
  실제 운영1.13.24 드릴을 새로 실행했다고 주장하지 않는다.
- 문서 links735/plan109 PASS. 문서 unittest 첫337 실행은 새WT node_modules 부재 때문에
  MDX parser38failure/3error/1skip로 실패했다. 원문을 보존한 뒤 npm ci --ignore-scripts 설치 후
  전체337 중336PASS/1SKIP/65.330초로 재검증했다. skip은 PASS로 세지 않는다.
- uv build PASS. 빈 Python3.11.15 core-only wheel 설치·pip check·installed module SHA 동일·
  실제 tiny fixture checked-hash flags3·선택 의존 import0·잘못된 CLI2종 exit2 PASS.
- wheel SHA256: fc8250fbb78d93afcf2447958290522222a2ce6faf403a390638a02a0f46b677.
- 기존 모든 Python 모듈은 base와 byte 동일하며 새 모듈만 추가됐다. pyproject/lock/기존 tests 변경0.
- 운영/SSH/DB/provider 호출·실제 stdlib 전체 컴파일·Docker build는0. 해당 소비자 gate NOT_RUN.
  UI/TypeScript 미변경으로 프런트엔드 제품 검증은 이번 변경 범위 밖이다.

실행 명령은 repository 루트에서 문서4종 및 package 디렉터리에서 uv sync --locked --all-extras,
uv run --no-sync ruff check ., uv run --no-sync pytest -q, uv build다.
CodeGraph init/status/impact(새 symbol 미존재)와 변경 후 sync를 수행했다.
최종 manifest 이후 link/plan/diff는 다시 확인한다. 최신 HEAD 원격 CI는 이전 후보와 구분한다.
