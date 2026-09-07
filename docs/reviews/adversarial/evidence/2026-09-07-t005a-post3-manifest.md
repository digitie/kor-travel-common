# T-005a 최종 post-fix 적대적 리뷰 manifest

- 기준 commit: `3c5801f14855a067080f257ec83d2279de32c74a`
- base: `6e1881b86f017d604ccfa416bd368e5aba24c669`
- 이전 immutable 기준: `735efed760d2703b3f5769e58270954352566f39`
- 범위: `@`가 포함된 branch/tag/rev와 인코딩 경계, 누적 uv lock·PEP 735·workspace·오류 출력 반례 및 전체 회귀.
- 결과: A PASS(누적 A-P1-01/02·A-P2-03/04/05 FIXED), B PASS(B-P1-01/02/03 FIXED), 신규 finding 0.
- 리뷰어는 같은 immutable candidate를 서로 다른 detached worktree에서 독립 검토했고 상대 결과를 읽지 않았다.
