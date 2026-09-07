# T-101 packages CI 순서 표준 문서 독립 리뷰 B

- 실행 ID: `reviewer_b-t101-ci-doc-6ab650d-20260907-223355`
- 최종 판정: **PASS**. 이번 1파일/1행 변경에 대한 신규 P0–P3 finding 없음.
- 요청: immutable `6ab650d`(parent `0cf352a`)의 `docs/standards/ci-deploy.md` packages job 순서 한 줄만 실제 workflow·T-101/T-201 범위와 독립 대조. 후보 수정/commit/push 금지, 초기·상대 리뷰 결과 미사용.
- 후보 시작·종료 SHA: `6ab650d76c4e40944085a79dde12e016d43e494b`
- 후보 시작·종료 tree: `2610acbd28f2b80cfc0d52097b3bfe7e25a4b7fc`
- parent/base: `0cf352ad4ee6640329dc46a06aa0a88402d42b86`
- 시작 KST: `2026-09-07T22:33:55.1989226+09:00`
- 종료 검증 KST: `2026-09-07T22:34:11.8784229+09:00`
- 격리: 후보에서 생성한 detached `F:/dev/kor-travel-common-wt/review-t101-ci-doc-b`. 시작·종료 `git status --porcelain=v1` 출력 없음.
- 후보 소스/문서/시험과 source `.git/config`를 수정하지 않았다. 자체 원본은 후보 밖 `.git/codex-audit/`에만 작성했다. 초기 및 상대 review 원문·finding을 읽지 않았다. task 검색 결과의 이전 evidence 집계는 이번 판정 근거로 사용하지 않았다.

## 직접 확인

`git diff 0cf352a 6ab650d -- docs/standards/ci-deploy.md`는 §9 packages 행 하나만 바꾼다. `.github`, `packages`, `tools`, `tests`, `versions.json`의 같은 범위 diff는 비어 있다.

- 표준의 `npm@11.19.1` 설치 → `npm ci` → 커밋 생성물 check → build → check → 생성물 Git diff → test → pack → 임시 tarball 설치 순서는 `.github/workflows/docs.yml:175–219`의 실제 실행과 일치한다. 생성물 검사를 build 전에 명시하므로 재생성으로 원래 drift를 덮어쓰는 해석을 허용하지 않는다.
- workflow의 lint/type-check 명령은 `--if-present`이며 현재 tokens package에 그 scripts가 없다. 이번 표가 이를 실행된 필수 검사처럼 열거하지 않는 것은 현재 tokens 계약과 맞는다. UI의 별도 타입 검사 의무는 T-201 수용 기준 58행과 검증 명령 72행에 남아 있다.
- trigger는 PR 및 main/codex/release-* push, runner는 ubuntu-24.04로 workflow와 일치한다. 정확한 source SHA 확인 및 권한·checkout 계약은 변경하지 않는다.
- T-101은 tokens package의 check/build/pack/install을 맡는다. webpack·Turbopack 스모크를 이미 실행되는 T-101 기능처럼 적지 않고 T-201 UI 추가 범위로 명시한 문구는 T-201 목표 10행·구현 26행·수용 기준 61행과 일치한다. UI 구현이나 소비자 저장소 변경을 지금 승인하는 문장이 아니다.
- 표준 행의 순서 변경은 T-201의 tsc·지시문 보존·단위 시험·tarball 설치 및 두 Next 빌드 수용 기준을 면제하지 않는다. task 완료 상태·외부 gate·릴리스 권한도 바꾸지 않는다.

## 실제 명령·결과

```text
git rev-parse 6ab650d
git rev-parse '6ab650d^{tree}'
git rev-parse '6ab650d^'
git diff --stat 0cf352a 6ab650d
git diff 0cf352a 6ab650d -- docs/standards/ci-deploy.md
git worktree add --detach F:/dev/kor-travel-common-wt/review-t101-ci-doc-b 6ab650d
git diff --name-only 0cf352ad4ee6640329dc46a06aa0a88402d42b86 HEAD -- .github packages tools tests versions.json
py -3.14 -B -X utf8 tools/validate_document_links.py
py -3.14 -B -X utf8 tools/validate_plan.py
git diff --check 0cf352ad4ee6640329dc46a06aa0a88402d42b86 6ab650d76c4e40944085a79dde12e016d43e494b
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --porcelain=v1
```

- 변경 범위: 1파일, 1 insertion / 1 deletion.
- links: 361 documents, 2323 local targets, errors 0.
- plan: 상세 task 106, 오류 0.
- diff check: exit 0.
- SHA/tree 및 시작·종료 clean 일치.
- `gh run view 34128018010 --json headSha,status,conclusion,jobs` 직접 조회: 정확한 후보 head의 [PR CI](https://github.com/digitie/kor-travel-common/actions/runs/34128018010)가 completed/success이고 6개 job 모두 success. 이는 원격 관찰이며 새 로컬 코드 시험으로 집계하지 않는다.

`NOT_RUN(이번 범위는 표준 한 줄이며 코드·workflow 불변)`: 로컬 npm build/test/pack·전체 Python unittest·WSL 반복 시험. 이전 코드 리뷰 PASS를 재판정하거나 이전 실행을 새 SHA에서 실행한 것처럼 집계하지 않았다. `NOT_RUN(범위 밖)`: 소비자 build/e2e·npm/PyPI 게시·Release/태그 생성.

이 문서 리뷰의 PASS는 변경된 packages 행의 정합성에 대한 판정이다. 코드 후보의 별도 리뷰, 실제 CI 완료, main/release 실행 및 T-101 closure gate를 대신하지 않는다.
