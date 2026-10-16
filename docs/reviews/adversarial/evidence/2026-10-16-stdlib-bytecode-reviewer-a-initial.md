# Common37 build_bytecode 독립 FULL 검토 A — 제품 후보

- 대상: 084585796bc4428dc9a3347f08f8ebaaa04bdfa3 / 기준 200a350101665f44246422c7102c087fdfb3222e.
- 범위: FULL4(새 helper·테스트·Dagster 가이드 §17·T319 수용 설계). 최신 C manifest/docs commit은 아직 미수신이므로 그 추가 delta/최종 HEAD 승인은 별도다.
- 판정: SOURCE_PASS / 열린 P0·P1·P2 0. 운영 효과/소비자 빌드 채택은 NOT_RUN이다.
- 요청: root의 Common37 독립 FULL 요청 및 0845857 대상 변경 메시지를 기준으로, 상대 D 검토 결과/저자 모형은 읽지 않았다. 원본 checkout 변경·운영 접근·SDK/DB/Docker/실제 stdlib 컴파일 0.

## 직접 확인

helper SHA b07c7f94565147f619bffba7f1f9871106c0ee07d3683974393d596ffda5d266.
원 immutable Git object에서 네 파일 전체를 읽고, AGENTS→docs README/resume→T319·관련 workflow 순서를 따랐다. 제품 archive는 원 checkout 밖 전용 디렉터리에 만들었다.

main의 필수 --stdlib만 명시 컴파일을 허용하며 임의 source path/기본 자동 작업은 없다. sysconfig stdlib를 resolve하고 비디렉터리/빈 대상/오류를 거절한다. compileall workers1·force·optimize0·CHECKED_HASH·quiet2를 직접 확인했다. 기존 timestamp cache를 checked-hash로 교체하고, 소스를 실행하지 않는다. compileall의 실제 walk/compile_file 경로와 rx의 stdlib-relative component 경계·limit_sl_dest 동작을 대조했다. root 부모 이름 tests 때문에 전체를 생략하는 원 후보 결함은 수정됐다.

preflight os.walk onerror는 읽기 실패를 숨기지 않고, source/목적지 resolve로 외부 cache·기존 pyc symlink·별도 pycache prefix를 막는다. 디렉터리 symlink를 따르지 않고 외부 source symlink를 compileall도 건너뛴다. 이 검사는 신뢰한 단일 writer 빌드용이며 동시 공격자 교체의 원자 sandbox라고 주장하지 않는다. 실패 전 일부 cache가 생길 수 있다는 가이드와 구현이 일치한다.

optimize0은 명시 계약이다. 실제 consumer가 -O/-OO로 실행한다면 다른 optimization cache가 필요할 수 있으므로 이 후보만으로 모든 interpreter argv의 효과를 보장하지 않는다. 실제 최종 이미지 pyc/magic/source·보존 및 cold health/self CPU/RSS 비교가 후속이다. 가이드의 약3.06→0.93~0.94는 별도 prefix 단일 import 관측으로 한정하며 서비스 전체 절감을 주장하지 않는다. 기존 런타임/격리 옵션·재시도 정책은 변경하지 않는다.

## 독립 실행

- actual-function 자체 tiny fixture 22조건 × Python3.11.15 / 3.13.14 / 3.14.4 각각 PASS. 서로 다른 interpreter 결과를 동일 시험의 독립 표본처럼 합산하지 않는다.
- checked-hash flags3·source hash/magic·source/env 보존, 컴파일 중 임의 source 실행 없음, 부모 tests 경로, 제외5종/접두 이름 비제외, 외부 lookalike/디렉터리 symlink, 내부 정상 경로, 외부 cache/기존·dangling pyc symlink/prefix 거절, syntax/빈 작업/제외만 있는 작업/비root 권한/읽기 실패, CLI 잘못된 인수, worker1/compileall False 전파를 검사했다.
- immutable archive 신규 test_build_bytecode.py: Python3.13.14 pytest 26 PASS / skip0 / 0.10s.
- 해당 helper+test ruff --no-cache PASS, exact Git diff --check PASS.
- 주의: 초기 결과파일 model-py311.json은 명령 python3의 실제 버전이 3.14.4였다. 파일명으로 3.11이라 집계하지 않았다. 실제 JSON의 version을 읽고 별도 model-real-py311.json에서 3.11.15를 검증했다. 원문은 덮어쓰지 않았다.

실제 stdlib compile·wheel build/install·운영 이미지·Docker·SSH·DB·provider·성능·consumer smoke는 NOT_RUN(이번 독립 source/fixture 범위). 저자 full suite/패키징 수치는 본인의 실행 수로 세지 않는다. 모든 소유 tool은 terminal이다.
