# T-102 초기 적대적 리뷰 공통 manifest

- Review ID: `t102-initial-20260907`
- 기준 commit: `8bc8179f728de88fd9327f9d4e8159188a95f9c3`
- base/parent: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`
- branch: `codex/t102-aliases`
- task: `docs/tasks/T-102-map-vocabulary-shim.md`
- 범위: `packages/tokens/aliases/map-vocabulary.css`, weather override 예제와 문서, alias checker와 stdlib 시험, package export/files, tools CI 호출 및 관련 README
- 범위 밖: 소비자 저장소 변경·T-461 실제 이관/시각 회귀·npm/PyPI 게시·인증 서버와 provider 코드
- 공통 요청: 동일 immutable candidate를 detached clean worktree에서 읽고, 소비자 계약·CSS 값·dark/profile·검사기 우회·import/symlink 경계·패키징·CI·GPL/SPDX·정본/문서 정합성을 고장 주입으로 검토한다. 후보 코드·문서·branch·registry를 수정하지 않는다.

## Acceptance와 실행 명령

- `check_aliases.py`가 정의되지 않은 `--kt-*` 참조, 직접 `--kt-*` 정의, Tailwind exact namespace 충돌, shadcn 중복을 차단하고 정상 alias는 exit 0이어야 한다.
- weather legacy vocabulary 집합이 기준 commit `6003da995fa4b35799f9dadc406c6ba2878bfbae`의 `packages/kor-travel-weather-admin/frontend/app/tokens.css` 변수 집합을 포함해야 한다. 예제는 navy brand, 17rem rail, 현재 font stack을 기준으로 한다.
- `npm pack --workspace packages/tokens` 결과에 `aliases/map-vocabulary.css`가 포함되고 `examples/`는 포함되지 않아야 한다.
- 양 OS 도구·문서·패키지 검증은 실제 실행한 결과만 기록하며 소비자 build/e2e와 T-461은 `NOT_RUN`으로 남긴다.

```text
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 -m unittest discover -s tests -p 'test_check_aliases.py'
python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'
npm ci --ignore-scripts
npm run check --workspace packages/tokens
npm run build --workspace packages/tokens
npm test --workspace packages/tokens
npm pack --workspace packages/tokens --pack-destination <temporary-directory>
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f 8bc8179f728de88fd9327f9d4e8159188a95f9c3
```

- Reviewer A 영역: 소비자 토큰 이름·값·계층, weather/map 계약, dark 값, 별칭 완전성, Tailwind/shadcn 충돌과 시각 회귀 위험.
- Reviewer B 영역: checker parser·import/symlink/read 경계·exit code, package files/exports/tarball, CI 양 OS, SPDX/GPL·출처·문서 정합.
- 원본 evidence: `2026-09-07-t102-initial-reviewer-a.md` SHA256 `256CD82C484E2DD12D35CA857724164C876FA4E91D0A1367288FDB95DF2EE32C`; `2026-09-07-t102-initial-reviewer-b.md` SHA256 `183B46D33DD71E9FA67EFF1BFFCAE423A0DB493F81B61BC22E108D8BDAAC5AF3`.
