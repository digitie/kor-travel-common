# Dagster 복구·UI post-fix manifest

요청·base·scope·격리와 acceptance는 [최초 manifest](2026-10-04-dagster-recovery-manifest.md)를
그대로 적용한다. commit object-only로 새 immutable candidate와 전체 delta를 확인한다.

| 저장소 | immutable post-fix candidate |
|---|---|
| common | `50d2db4c7c7e0154dd863defb62d4b9fa3b5bec3` |
| weather | `1218c8f656408d04f745bf5773ec910a36538bc5` |

두 원본 보고서는 [A](2026-10-04-dagster-recovery-reviewer-a.md),
[B](2026-10-04-dagster-recovery-reviewer-b.md)에 그대로 보존했다.
A-P2-01 destructive 토큰·토큰 존재 시험, A-P2-02 repository 복합 schedule identity/콜백,
A-P3-01 public slots/testId/상세 header, A-P3-02 소비자 gutter가 수정되었다.
B-P2-01 특보 bounded staging·누적 예산·어느 notice라도 skip이면 incomplete 집합 유지,
B-P2-02 회수 keyset pagination/tie-breaker, B-P2-03 strict 정수/boolean 정책 검증,
B-P2-04 기존 architecture의 부분 게시 계약이 수정되었다. 각각 회귀 시험/문서를 포함한다.

추가 delta: live 실제 Dagster GraphQL에서 기존 eventConnection limit2000이 서버 상한1000을
넘어 실패 원인이 사라지는 것을 재현했다. limit1000/cursor 페이지·최대20page/20초 시작
예산·요청10초 timeout을 넣고 후속 page의 failure 회귀 시험을 추가했다.
CI의 Python 출처 헤더 E501과 소비자 tgz integrity 불일치를 수정했다. weather Python
의존성은 위 common candidate SHA로 재고정했고 npm archive SHA256/lock도 재생성했다.
사용자 추가 요청의 [Dagster 적용 가이드](../../../runbooks/dagster-adoption.md)를 포함한다.

현재 실행 evidence: common Python21/UI34 PASS, Python3.11+Dagster1.9 floor21 PASS,
weather 회수/특보25 PASS. clean artifact install·최종 whole pytest·live runtime UI·최종 CI는
계속 진행 중이며 아직 통과를 주장하지 않는다. 최종 evidence는 closure에서 기록한다.
B 원본의 weather 1.13.20 표기는 정정: 실제 소비자 lock/runtime은 1.13.24다.

각 reviewer는 자기 finding closure와 전체 delta의 회귀를 독립적으로 확인하고 원본
post-fix report를 별도 제출한다. 상대 post-fix report는 양쪽 확정 전 공유하지 않는다.
