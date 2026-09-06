<!-- kor-travel-common templates/consumer-pr.md 판 2026-09. 소비 저장소 채택·이관 PR 본문 규격(D-24). 6항목을 모두 채운다. 해당 없음은 "해당 없음(사유)"로 적고 비워 두지 않는다. -->

## 1. task와 목적

- common task: `T-NNN` (kor-travel-common `docs/tasks.md`) / 소비 저장소 task: `T-NNN`
- 산출물(한 PR = 한 산출물): tokens vX.Y.Z 채택 | ui vX.Y.Z 채택 | py vX.Y.Z 채택 | 규약 문서 반영 | 매니페스트 갱신 (하나만)
- 프레임워크 업그레이드(Next·React·Node·ESLint)는 이 PR에 섞지 않았다: 예 / 아니오(사유)
- 변경 파일 수: N (상한 tokens 10 · ui 30 · py 10; 초과 시 분할)

## 2. 통과한 gate와 정확한 명령

| gate | 명령 | 결과(tool version·test 수·exit code) |
|---|---|---|
| lockfile 무결성 | `npm ci` / `uv sync --locked` | |
| 버전 대조 | `python3 -B -X utf8 tools/check_versions.py <소비자-checkout> --repo <repo>` (common 체크아웃에서) | 실제 판정 요약·mode·exit code |
| 단위 | `npm test -- --run` / `pytest -q` | |
| 빌드·타입 | `next build` / `tsc --noEmit` / `mypy` | |
| e2e | `npx playwright test` | |
| 대비·UX(토큰 PR) | `kt_contrast.py` / `ux_lint.py --base <sha>` | |

## 3. 리뷰어 2인의 영역·report·disposition

- 단계: full / light (판정자: merge 담당, 작성자 아님)
- Reviewer A 영역: · verdict: `BLOCK`/`CONDITIONAL`/`PASS`
- Reviewer B 영역: · verdict:
- report: `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md`(full) 또는 journal 항목(light)
- 미해결 finding: 없음 / `A-P2-01 DEFERRED(owner·task·gate·기한)`

## 4. 실패·미실행 검증과 남은 위험

- `NOT_RUN(사유)`:
- 알려진 회귀·차이(시각 diff 원인 규명 여부 포함):
- 예외 등록(`versions.json exceptions`·`contrast-baseline.json`·`openapi-exceptions.yaml`):

## 5. evidence 위치와 digest

- 설치 tarball / wheel: `kor-travel-<pkg>-X.Y.Z.tgz` sha256 `…` (SHA256SUMS와 일치)
- lock 변경: `package-lock.json` / `uv.lock` 동반 커밋 `<sha>`
- 매니페스트: `kor-travel-common.lock.json` diff 요약
- 시각 회귀(토큰·스타일·셸 변경 시 필수, D-21 — 파일은 저장소에 넣지 않고 PR 첨부):

| 폭 | 기준선(착수 전) | 완료 후 | diff |
|---|---|---|---|
| 320 | 첨부 | 첨부 | 0 / 설명 |
| 375 | | | |
| 414 | | | |
| 768 | | | |
| 1024 | | | |
| 1440 | | | |

## 6. rollback

- 되돌리기: `git revert <merge-commit-sha>` 1회로 원복된다(lock 동반 커밋이므로 별도 조치 없음): 예 / 아니오(추가 명령)
- 배포 후 되돌릴 때 함께 되돌릴 것(이미지 태그·env·마이그레이션):
- 중단 조건(D-08): 시각 diff가 원인 불명으로 남으면 이 단계를 revert하고 확대하지 않는다.
