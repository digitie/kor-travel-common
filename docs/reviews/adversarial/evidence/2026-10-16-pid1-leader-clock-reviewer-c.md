# Common36 PID1 leader clock 독립 적대 리뷰 C

- 판정: SOURCE_PASS / 열린 P0·P1·P2 0 / 제품 수정 요구 없음.
- reviewer: C (/root/geo_timeout_analysis). 작성자 D와 독립이며 다른 reviewer 원문은 읽지 않았다.
- immutable 대상: 5d2ad2bb45e64197ea359e0e5136b84780dab97a / 제품 a34cbd8e2242542abecad3987fb7e9aa87993ab7 / base eaf83e965ee837a277d5d7b370ecde0d4897f1cd.
- manifest 포함 FULL4를 읽었다. 제품·테스트·가이드3 + manifest1이며 기존 전체 정산 모듈과83개 회귀도 함께 확인했다.

## 결과

dagster_recovery.py:140–159는 PID1 시작 tick의 두 읽기를 /proc/1/task/1/stat로 옮긴다. 동일 경로를 두 번 검증하며 _start_ticks의 PID1·양수 확인을 유지한다. 경로 부재·권한·손상·변경은 None이며 일반 stat fallback이 없다. 호출 스레드나 user-code child 시작 tick을 새 incarnation으로 고르지 않는다. cursor 형식은 유지하며 옛 cursor와 identity가 다르면 원래 계약대로 첫 tick은 기록만 하고 정산하지 않는다.

reader 밖 전체 모듈 AST는 base와 동일함을 독립 비교했다. NTP·boot/epoch·namespace·cgroup·clock guard, exact DefaultRunLauncher·persisted origin/tag 검사, STARTED만 정산, 쓰기 직전 재조회, 공식 RUN_WORKER_RESTART, 기본 STOPPED·page·협력적 예산·cursor는 확대하지 않는다. 가이드 §15의 singleton/exclusive origin·serial 교체·구 init/worker/cgroup 소멸 전제를 보존한다. 물리 사망이나 원자 CAS를 clock만으로 증명하지 않는다.

저장된 QEMU 원문 SHA3ada39c0baaaba11f621a374e0ec7c57022a491ba0e9a997c51e2dcf0770012d의 세 canonical leader tick이 host PID1 tick280141436과 같음을 메모리 투영으로 확인했다. 새 LIVE 실행으로 집계하지 않는다. 가이드는 일반 stat의 호출 스레드 차이와 native Dockerexec에서 미재현한 한계를 구분한다. 공식 [Linux procfs 문서](https://docs.kernel.org/filesystems/proc.html)의 PID/task/TID 경로·start_time 설명을 독립 조회했다(2026-10-16). QEMU 자체 현상은 저장된 실험 근거에 한정한다.

## 독립 검증

- exact Git archive의 자체 디렉터리에서 PYTHONPATH를 고정하고 실제 설치 SDK1.13.24로 pytest --noconftest -c /dev/null test_native_incarnation.py -q: 90 PASS, test2.56초/wrapper3.263초. Weather conftest·PG 접속0. /dev pytest cache 권한 warning1은 원문에 보존했다.
- 추가10조건 PASS: 닫는 괄호 포함 comm의 정상 leader, boot 변경, leader 두 표본 변경, leader PermissionError와 fallback 금지, 최종 cgroup 변경, NTP UNKNOWN, epoch 표본 차이, HZ0, 저장된 QEMU3표본 귀속, reader 밖 AST 동일성. 저자90개에 합쳐 전체100개 회귀라고 표시하지 않는다.
- core import 후 Dagster 미import를 모델에서 확인했다. 실제 adjtimex/운영 센서/DB/SSH/Docker0.

시험 원문 common36-independent-native-tests-c-r1-20261016.log
SHA529549e0ca99f4e98399c17e596d0ca5c536df144b88bdbec5ad1f56c6454180.
모형 common36-independent-models-c-r1-20261016.json
SHAa3cff79d280d5b2a0eab08c40520a9e676375ae727e67e53ab930c51b2892c59.
archive SHA7ec4a328d934b92227c2f9b99089793ab2255fdbc4f56a068559a9c4c04fb76f.

저자 전체450·문서336+1SKIP·wheel 수치는 manifest의 저자 검증으로 구분한다. 소비자 pin/이미지·QEMU 재드릴·운영 복구·CPU/RSS/속도 효과는 NOT_RUN이며 이번 SOURCE_PASS가 그 gate를 대신하지 않는다.

## 파일 결박

- packages/py/kor-travel-common/src/kortravelcommon/dagster_recovery.py: c9b06b628c1dd9d428049cc56e6ff468c6ff2638c25f076bf0586ccc0dbc8844
- packages/py/kor-travel-common/tests/test_native_incarnation.py: fba3b91c61ce8cf80d93a94cacf3204ad025d3cf0b831fd5c1eea68f255694be
- docs/runbooks/dagster-adoption.md: b25086a3751323c1884704414f4f0f5d18bb589cbbcd17001be4ed8b5ddb98e3
- docs/reviews/adversarial/evidence/2026-10-16-pid1-leader-clock-manifest.md: 34788bdd44297c9c6029a5679ff0fdb92908043791bfc20639aa3c26d031a221
