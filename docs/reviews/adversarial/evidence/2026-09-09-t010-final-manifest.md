# T-010 최종 적대적 리뷰 기준 manifest

- Review ID: `T010-20260909-final`.
- 종류: 전문 리뷰어 2인 독립 적대적 리뷰.
- 기준선 commit: `ddb4b7479c39d049688a095a0febe7dfd12e02c3`.
- 기준선 tree: `d62c387c3ebd590d25c882a7b474f451de377145`.
- 최종 후보 commit: `f220bb5` (기능 후보 `54b5ac47ec3accb0fa44108a5d76d6389c07cb22` 위의 evidence-only closure).
- 최종 후보 tree: `68c8a8f19517dacf0a53d86e1efb5d85e22f464f`.
- 요청 범위: `.github/workflows/versions-check.yml`, `docs-check.yml`, `contrast-check.yml`, `workflows-selftest.yml`, `consumer-smoke.yml`, `tools/check_versions.py`, `tools/consumer_smoke.py`, `consumers.pins.json`, 관련 fixture·테스트·T-010 문서와 새 closure evidence.
- 수용 기준: T-010 상세 task, GPL-3.0-or-later 전역 규칙, 재사용 workflow의 SHA action pin·권한·timeout·runner·동시성, consumer checkout과 common artifact provenance 분리, fixture fail-closed 경계.
- 검증 요청: static YAML·secret·SPDX·redaction·link·plan 검사, fixture 실행, 전체 unittest와 consumer/version focused unittest, 실제 `npm pack` tarball 입력 경계·GPL·repository provenance·설치 실패 재현, `git diff --check`.
- 범위 밖: 실제 소비자 저장소 checkout/build/e2e와 dispatch, npm/PyPI 게시·GitHub Release 업로드, 주간 smoke 활성화, consumer adoption, actionlint(도구 미설치).
- 공통 규칙: 각 reviewer는 이 manifest와 immutable 기준선에서 상대 결과를 보지 않고 독립 detached clean worktree로 판정한다. P0/P1은 수정·재검토 전 merge하지 않는다.
