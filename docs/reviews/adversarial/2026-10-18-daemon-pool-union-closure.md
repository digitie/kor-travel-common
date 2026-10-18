# daemon 연결 풀과 영속 제출 webserver 통합 검토

상태: COMPLETE. 두 독립 SOURCE PASS, 열린 P0/P1/P2/P3=0.
최종 기준은 ff849ea8447c6d2cca1ffa653cfcbe2b2ffa6b32이며,
기존061008f의 daemon 풀과 main f914873의 webserver를 일반 merge했다.
작성자 C와 별개인 A(/root/review_finish_a, 계약·의존성)와
B(/root/review_finish_b, 설치·패키징)가 같은 불변 기준을 독립 검토했다.
두 원문 고정 전에 상대 판정을 공유하지 않았다.

r1은061008f 전체 조정을 검토했고 r2는 main41 통합 delta를 검토했다.
A의 C38-A-P3-01(daemon 기능 CHANGELOG 누락)은 최종 변경 기록으로 FIXED다.
기존 daemon 구현과 main의 주소·webserver 구현은 각각 byte 동일하다.
기존 외부 의존64개의 version·artifact를 보존하고 webserver 관련18개를 합쳤다.
Dagster1.13.24/Postgres0.29.24/SQLAlchemy2.0.54를 유지한다.

작성자 locked 전체599개, A의 실제 SQLAlchemy·격리 계약40개,
B의 새 wheel 설치 후 독립68개가 통과했다.
각 실행 범위를 구분하며 합산해 단일 전체 suite 결과로 표시하지 않는다.
정식 wheel은 Python16개·RECORD23행이며 두 CLI와 pool plugin을 제공한다.
B가 독립 재빌드한 wheel도 작성자 산출물과 byte 동일하다.
SHA256: 1abf0547a7b7fbe76284b69c375e83d953788b83a05fbd6720957a869f865b53,
크기63,151B. 실제 CLI help와 lazy import·process 분리도 검증했다.

최종 소스의 CI14개 모두 SUCCESS를 merge 담당이 확인했다.
이 후속은 원문·판정·index 보존만 하므로 사용자 요청대로 CI를 생략한다.
Manager 소비·운영 배포·실제 작업 실행·CPU/RSS 개선은 후속이며 이번 판정에 포함하지 않는다.
Daemon OFF를 유지한다. Common41만 포함한 wheel로 daemon 기능을 덮지 않고 이 통합본을 사용한다.

## 원문·CI 무결성

| 파일 | SHA256 |
| --- | --- |
| [2026-10-18-daemon-pool-r1-reviewer-a.md](evidence/2026-10-18-daemon-pool-r1-reviewer-a.md) | f4b192ea76c0c17d1d24703aad9fe172563dfbff75ad6c7a4830fe04b3cf7031 |
| [2026-10-18-daemon-pool-r1-reviewer-b.md](evidence/2026-10-18-daemon-pool-r1-reviewer-b.md) | 90835861892c9197f1e047751479c8d4ca312dbf8de99eb1337e8591a3a72675 |
| [2026-10-18-daemon-pool-r2-reviewer-a.md](evidence/2026-10-18-daemon-pool-r2-reviewer-a.md) | 3ae028a02e6aafe218fcbbda595e2126d9169b924b53abab44c7bb7525f1be97 |
| [2026-10-18-daemon-pool-r2-reviewer-b.md](evidence/2026-10-18-daemon-pool-r2-reviewer-b.md) | 0a4339f963df03383938e8364bd0b4f8dd4aba1ad8919390df862bcc98b333b7 |
| [2026-10-18-daemon-pool-source-ci.json](evidence/2026-10-18-daemon-pool-source-ci.json) | 5710c567cd09b272f9bed23ad13a7cea51953a9504344551db6b4942a289bf3e |
