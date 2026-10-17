# daemon pool 수명·fork postfix 독립 리뷰 manifest

- base 후보: `b4e419b71e77f03f0409be3d110f238bc27d2bae` / 제품44cf.
- 새 제품: `1aada9978027e88294e8847c723089e4a0336064`.
- 검토 범위: base 대비 plugin 모듈·회귀·가이드3파일. [원 FULL manifest](2026-10-17-daemon-postgres-pool-manifest.md)의 나머지 계약을 보존한다.
- 원44cf/b4·38db와 실패 반례는 보존한다. 이전 candidate의 PASS로 새 lifecycle 판정을 대신하지 않는다.
- 수정: public QueuePool.connect의 선행 PID 검사로 pre_ping 이전 child I/O 차단,
  dispose/recreate의 생성 PID·대여/유휴 검사, activation별 scope identity로 과거 pool 재사용 차단.
- SDK/controller/_engine monkeypatch0·pool2+2/pre_ping/원 timeout/원 CLI·DSN/ref 계약 불변.
- 자체 회귀: fork pre_ping 반례1RED→GREEN, lifecycle 새4반례4RED→GREEN;
  최종24 focused PASS/1.21초, Ruff PASS. 실제 SDK·DB·fork·운영 실행은 C에서0이다.
- root가 별도 격리 SDK/PG/CLI 검증을 수행한다. 소비자 실제 CPU 효과는 아직 미검증이다.
- 리뷰 요청: 원 FULL delta와 이 좁은3파일을 두 명이 독립 검토한다. 총 연결 상한·
  retired pool·close=False·busy cleanup·원 예외·scope 재활성화·creator PID 경계를 공격한다.
