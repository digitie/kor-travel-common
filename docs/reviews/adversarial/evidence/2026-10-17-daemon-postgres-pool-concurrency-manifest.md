# daemon pool thread·fork·재생성 최종 manifest

- base: `57dd89a7a857e73b39ff2c3243636caaf16359c3`; 제품: `e0c13894ad798c7d4e90267d788f01c8bdfedda0`.
- [원 FULL](2026-10-17-daemon-postgres-pool-manifest.md)과 [첫 postfix](2026-10-17-daemon-postgres-pool-postfix-manifest.md)의 원문·실패 이력은 보존한다.
- 이번 제품 delta는 아래5파일이다. 최종 문서 commit은 이 manifest1개만 추가한다.
- pool별 connect/dispose/recreate 직렬화, 생성 PID의 잠금 이전 검사, 퇴역 pool 접속 거절과 원 scope 계승으로 세대·thread 경합을 차단한다.
- plugin/activation도 fork PID를 전역 잠금 이전에 검사하며 자식 finally는 부모 잠금·연결 I/O를 하지 않는다.
- pre_ping/세 engine의2+2 상한/원 URL timeout·CLI·InstanceRef 계약은 유지한다.
- CI는 daemon-pool extra를 설치해 PostgreSQL lazy engine 회귀 driver를 제공한다. placeholder URL 사용으로 secret-scan 예외0을 유지한다.
- 자체 실제 SQLAlchemy2.0.54/fakeDBAPI: 새6회귀 옛1aada에서5FAIL/1PASS, 옛scope 재생성1FAIL을 별도 보존; 수정본 전체30PASS/1.24초.
- Ruff/lock/링크746문서2923targets/plan109/secret·redaction1158파일0발견0예외 PASS. 기존 docs unit336PASS1SKIP은 새제품 전체 실행으로 재집계하지 않는다.
- 최초 잘못된 check_links.py 경로 호출은 file-not-found였고 검증0이며, 정본 validate_document_links.py/validate_plan.py로 위 수치를 확인했다.
- C의 실제 fork·SDK·PG·소비자 운영 실행0. root가 exactSDK/격리PG/CLI·signal·fork 검증을 별도 수행하고 소비자 CPU 효과는 미확정이다.

| 파일 | SHA256 |
| --- | --- |
| `.github/workflows/python-package.yml` | `66b3ab3c003641b644327f1f2a127560bbd0bf4d20c287f2af659c68595384cd` |
| `docs/runbooks/dagster-adoption.md` | `682fc3bb6a65a3cd1f89b9def68922f490f34efb179e515621f3823d8e6086c7` |
| `docs/tasks/T-319-dagster-recovery.md` | `f960083f7ba331057d87df94af1ff7600564298e08582f486e1ec96b9e41d4cd` |
| `packages/py/kor-travel-common/src/kortravelcommon/_daemon_pool_plugin.py` | `d6457a90d72f894644e591c1f541126fe037735a523a66cf1fa3e1f379763d7a` |
| `packages/py/kor-travel-common/tests/test_daemon_pool.py` | `2766b84c3ae466f0bc2fef3ebf4cdc836d64d0c271246160c8548eb70e5a50aa` |

## Wheel 정적 검증

- wheel SHA256: `0bd62cca5b5a2493e532113f0ae603c430a5f56e7d42428005096f0bdc811229`, bytes45405.
- RECORD nonself18행의 hash/size와 package13파일의 Git bytes, CLI/plugin entry point를 확인했다.
- 이것은 로컬 오프라인 wheel packaging 검증이며 실제 설치·소비자 동작 PASS를 뜻하지 않는다.
