# daemon PostgreSQL 연결 풀 독립 리뷰 manifest

- 요청: CPU 개선을 위해 공식 SQLAlchemy plugin과 동일 프로세스 daemon 진입점을 추가한다.
- base: `c48595880aaad4367802ad71af2525a8a5e17c6a`
- 제품·가이드·회귀 고정: `44cf0d1c9295c118fe8bd4ddbd2b546b4ebe3549`
- 범위: 아래7파일 및 이 manifest. SDK monkeypatch·private engine/controller 대입·공유 설정·소비자 코드는 변경하지 않는다.
- 수용 기준: [T-319](../../../tasks/T-319-dagster-recovery.md), [가이드 §18](../../../runbooks/dagster-adoption.md#18-daemon-전용-postgresql-연결-재사용).
- 검토 요청: daemon scope/같은 프로세스·CLI 위임·원 timeout/DSN/ref 보존·pool 상한/포화/pre_ping·thread/fork/정리·wheel/core-only 경계를 두 명이 독립 검토한다.
- 실제 운영 적용·Manager 통합·소비자 성능은 NOT_RUN이며 별도다. 실제 SDK 실행·격리 PG는 root만 수행한다.

| 파일 | SHA256 |
| --- | --- |
| `docs/runbooks/dagster-adoption.md` | `f48f9c7313a1fd16077164337e0d7d335a9011f0c61a1b47c5d9c4bf1982dfa4` |
| `docs/tasks/T-319-dagster-recovery.md` | `ce40d83081165f84d8ff6735f1ee80ae8ba37d49eaddfe553b81c4572a0ce1c1` |
| `packages/py/kor-travel-common/pyproject.toml` | `da3a623f397b3880f4adae81431b64b93bcd890a2796ccab3974e65e60d5d0de` |
| `packages/py/kor-travel-common/src/kortravelcommon/_daemon_pool_plugin.py` | `d60ff0762658742b7ba469ce3c3fa88d6aaa73024cf68abaf5dc02226e11a2d6` |
| `packages/py/kor-travel-common/src/kortravelcommon/daemon_pool.py` | `b16fd932b13a029f466633b6e31dd25936898c23041e964734c2c058f5d85313` |
| `packages/py/kor-travel-common/tests/test_daemon_pool.py` | `07124e12dca4ccb9c8685e9c4d8661dc23cc9979aefba38ecb1d58fc05e83b67` |
| `packages/py/kor-travel-common/uv.lock` | `86755140d6345437b122e26e9f660d27dd8033a2f13e1ac844a8e58fbea479d7` |

## 작성자 검증

- SQLAlchemy2.0.54의 fake DBAPI/lazy engine18 focused PASS/1.21초, 실제 SDK/PG/socket0.
- Ruff PASS, offline wheel build PASS, source-only 실제 SDK ref AST의4개 StringSource env 보존 PASS.
- 문서 링크744/오류0, plan109/오류0, git diff --check PASS.
- 문서 도구 전체 unittest는 최초 Node MDX 의존 미설치 상태38FAIL/3ERROR/1SKIP를 보존했다.
  자체 checkout에서 잠금 npm 의존을 offline 설치한 뒤 최종336PASS/1SKIP(337개)/71.662초다.
- 초기8cbc wheel의 core-only 설치/import·entrypoint·RECORD18 검사 PASS. 최종44cf wheel은 별도 경로에 다시 빌드했으며 최종 산출물 검증은 인계에 따로 기록한다.
- 전체 Python 패키지의 SDK 의존 시험은 C에서 NOT_RUN(SDK 실행 금지); root가 exact runtime에서 별도로 확인한다.
- uv lock 기존 버전 이동은 지원 runtime의 Dagster/pipes/shared1.13.25→1.13.24, SQLAlchemy2.1.3→2.0.54다.
  신규 PG/psycopg2/greenlet 외 무관 패키지의 upgrade는 없다.

root는 초기8cbc에서 격리 PG 동등 읽기/공식 CLI 정상 종료를 수행했다고 보고했다.
이는 C 직접 실행 결과가 아니며 운영 CPU나 최종 pre_ping gate를 대체하지 않는다.
pre_ping=False의 유휴 연결 단절 반례는 root가 보존했고44cf가 이를 보강한다.
mid-query/transaction 장애 재시도는 확대하지 않는다.
