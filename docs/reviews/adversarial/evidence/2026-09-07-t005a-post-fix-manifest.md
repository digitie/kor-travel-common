# T-005a 첫 수정 후 적대적 리뷰 manifest

- 기준 commit: `902750016d157bb195fb05c01358c4b8a6ffe812`
- base: `6e1881b86f017d604ccfa416bd368e5aba24c669`
- 이전 immutable 기준: `3bc0f473833aa51a8656b045b705891debf8cf13`
- 범위: 최초 finding A-P1-01/02·A-P2-03/04 및 B-P1-01/02 수정, 입력 fail-close·공유 lock·PEP 735·git 참조·오류 출력.
- 결과: A BLOCK(잔여 A-P1-02·A-P2-03·신규 A-P2-05), B BLOCK(잔여 B-P1-02). 이 기준은 병합 후보가 아니며 후속 수정 기준으로만 보존한다.
- 리뷰어: A 입력 경계·workspace·출력, B lock ref·정본·Python 축. 서로의 결과를 보지 않은 별도 detached worktree.
