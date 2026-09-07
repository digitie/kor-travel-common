# T-005a 두 번째 수정 후 적대적 리뷰 manifest

- 기준 commit: `735efed760d2703b3f5769e58270954352566f39`
- base: `6e1881b86f017d604ccfa416bd368e5aba24c669`
- 이전 immutable 기준: `902750016d157bb195fb05c01358c4b8a6ffe812`
- 범위: URL hostname/port·lock group 내부 구조·PEP 735 group 정규화/중복/순환/include key·branch 이름 경계.
- 결과: A PASS(누적 A 5개 FIXED), B BLOCK(B-P1-01/02 FIXED·신규 B-P1-03 OPEN: `rev/tag=topic@v1.2.3`). 후속 수정 기준으로만 보존한다.
- 리뷰어는 서로의 결과를 보지 않은 별도 detached worktree에서 Windows/WSL 회귀와 독립 CLI 반례를 실행했다.
