# T-101 CI 표준 문서 후속 리뷰 manifest

- 기준 commit: `6ab650d76c4e40944085a79dde12e016d43e494b`
- 기준 tree: `2610acbd28f2b80cfc0d52097b3bfe7e25a4b7fc`
- parent: `0cf352ad4ee6640329dc46a06aa0a88402d42b86`
- 범위: `docs/standards/ci-deploy.md` `packages` 행의 검사 순서와 T-101/T-201 소유 경계
- 요청: 실제 `.github/workflows/docs.yml`와 표준 문서의 순서를 대조하고, 다른 코드·이전 reviewer 결과를 열람하지 않은 채 신규 P0–P3 finding을 찾는다.
- 공통 확인: detached clean worktree, `validate_plan`, `validate_document_links`, `git diff --check`, 정확한 CI run `34128018010`.
- 수정·commit·push·publish는 금지한다.