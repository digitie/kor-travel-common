# Workspace 갱신 주기 독립 리뷰 manifest

- immutable 기준선: `46b3bb1a0214d5815d5cf146a853e442bf169854`
- base: `e746e4b` (`origin/main` 분기 기준)
- 요청: 수집과 별개로 발생하는 shared daemon CPU를 실측하고 반복 workspace metadata 갱신 비용을 줄인다.
- 범위: `daemon_pool.py`의 명시적60/180초 opt-in, 원SDK failure grace/CLI/pool/신호 수명 보존, 실제SDK method·CLI단위 회귀, 가이드/T-319/기록.
- 범위 밖: worker/provider/DB schema/센서/heartbeat/실행monitoring 설정·소비자pin·운영배포·CPU 감소율 보장.
- 근거/계약: `AGENTS.md`, `docs/tasks/T-319-dagster-recovery.md`, `docs/runbooks/dagster-adoption.md` §18/20.
- 검증: 작성자 Python3.13 전체661 PASS155.87초, Ruff·문서/plan·wholewheel 별도설치 profile/restore PASS. 잠긴Python3.12 전체·도구unittest·CI진행.
- 리뷰 방식: 고정commit의gitshow/gitdiff object-only. 코드/DB/운영변경 없이 각자 원문 결과를 작성한다. 상대 결과는 원문 확정 전 전달하지 않는다.
- A관점: 실행/장애계약·프로세스범위·예외/종료원복·영향받지않아야할heartbeat/sensor/CLI.
- B관점: SDKprivate상수/설치profile·wheel·환경입력거부/비밀·문서수용gate·장애경계/유예.
- 판단: 비단순 공개설정 변경으로 FULL. 작성자가 아닌독립리뷰어가 범위/판정을확인한다.
