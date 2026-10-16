# Common36 PID1 leader clock 독립 FULL 리뷰 A

판정: **SOURCE_PASS / 열린 P0·P1·P2 0**.

## 고정 범위

- review HEAD 5d2ad2bb45e64197ea359e0e5136b84780dab97a, 제품 a34cbd8e2242542abecad3987fb7e9aa87993ab7, base eaf83e965ee837a277d5d7b370ecde0d4897f1cd.
- 독립 archive /home/digitie/dev/common36-review-a-5d2ad2b-20261016.
- AGENTS·문서 라우터·resume·T319를 읽고 manifest 동일 SHA34788bdd 및 전체4파일 delta와 reader/복구 caller·기존 test90 전체 문맥을 확인했다. 원 WT clean/HEAD exact, git diff --check PASS. peer 리뷰·작성자 모델은 읽지 않았다.

## 결론과 공격 경계

dagster_recovery.py:140-158은 일반 /proc/1/stat 대신 /proc/1/task/1/stat의 leader를 동일 경로에서 두 번 읽는다. 자체 AST 비교로 reader의 Path 별칭/경로2개를 복원하면 base reader AST와 완전히 같고 나머지 모든 함수·클래스 AST도 같다. clock/NTP/부트 ID/namespace/cgroup·최소 grace/launcher exact DefaultRunLauncher/origin/원 STARTED 재조회·cursor·STOPPED 계약 변화가 없다. fallback을 추가하지 않았다.

본인 실제 ARM QEMU reader 증거3ada39c0…의 canonical host tick280141436과 일반 호출 thread tick280141442/280142033을 고정 대조했다. 원제품은280142033을 수용하고 새제품은280141436을 반환한다. 새제품은 legacy 값을 두 경우로 바꿔도 leader2회만 읽으며 동일 identity다. leader 부재·짧은 stat·PID1 아님·0/비정수/두 표본 변경·namespace/cgroup/boot/clock/NTP/marker owner 불확실성을 거절했다. ordinary native와 leader가 같은 정상 표본도 보존했다.

Linux PID1의 leader TID1 경로가 부재하거나 권한 문제면 None으로 보류하는 것이 의도다. 기존 일반 proc fallback이 없어 에뮬레이션 TID를 init으로 위조하지 않는다. 기존 cursor를 자동 고치거나 초기화하지 않으며, 이미 오염된 cursor의 실제 활성화/재정산은 소비자 별도 gate다. 가이드는 실제 QEMU 반례·일반 exec 반증·native 운영 미입증을 구분하고 singleton/origin/old worker/cgroup 소멸 전제를 그대로 유지한다. 새로운 성능 또는 LIVE 성공 주장 없음.

## 직접 실행

1. immutable archive에서 실제 SDK1.13.24로 --noconftest -c /dev/null native 파일 전체: **90 PASS**, warning1,2.53초. Weather conftest/PG 접근0. 실제 SQLite/합성 proc·SDK 이벤트/태그 회귀이며 physical worker loss LIVE가 아니다.
   - 원문 common36-native-tests-a-r1-20261016.private.log, SHA e0ce219b9393610a9a4e005a6776f8b4b3cbc1406823aea46ebe5b2f151613c0.
2. 본인 별도 actual reader/old-new AST 모형 **16조건 PASS**. 기존90과 겹치는 검증이라 합산 총시험 수로 세지 않는다.
   - source common36-own-reader-model-a-r1-20261016.py.
   - 결과 common36-own-reader-model-a-r1-20261016.private.json, SHA 3952988fd0c297a50b80cd103fb6211a4f505e8e7d94d0a67e1c4ba1c427fc76.
3. immutable Git manifest/clean/전 delta/AST 변경 한정 확인 PASS.

작성자 전체450/native90/wheel/docs 결과는 manifest에 기재된 별도 근거이고 본인 재실행으로 세지 않았다. 본인 전체 패키지·wheel 설치·실제 Docker/QEMU 새실행·운영 nativeARM·실제 복구 child1 성공·CPU/RSS·소비자 채택은 **NOT_RUN**. 실제 컨테이너/DB/SSH/HTTP/빌더/제품 수정0, 본인 도구 전부 terminal이다. Weather100 artifact는 Common eaf 고정이며 Common36과 섞지 않았다.
