# T-301 post-fix-04 적대적 리뷰 입력 manifest

- Review ID: `T301-20260909-post-fix-04`
- 기준선(base): `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- 최초 후보(candidate): `0c0c189017989065fd8ced9e6e84ad9c6e7b7756`
- post-fix-01 후보: `fedf7f8cbad55302183708aa4c9dd514ffba466d`
- post-fix-02 후보: `bf51790b87e578516d1c7f3ef741aa8a63ccc72c`
- post-fix-03 기능 후보: `36509d3835a459993ad13b5a10a0340e48178b86`
- post-fix-04 최종 후보: `59a0fbc3ae426ec7a166ac34cbacbf2f9d6eaec5`
- post-fix-04 tree: `15c3f3c90f881f4454caa18e24df603c4af52bf5`
- PR: `#22` (draft)
- 작성일: 2026-09-09
- 공통 범위: `tools/openapi_exceptions.py`, `tests/test_openapi_exceptions.py`, `docs/standards/openapi.md`, `docs/standards/openapi-exceptions.yaml`, 생성물 `docs/standards/openapi-exceptions.md`, T-301 상태·journal·resume evidence
- 리뷰 범위: 후보 전체 diff와 OpenAPI 정본·ADR-009/D-14·T-301 계약, parser fail-closed 경계, YAML 숫자·timestamp·BOM scalar, task 파일명 provenance, SHOULD 외부 계약 증명·surface 정규화, Unicode 제어·format 문자, 생성 Markdown 안전성, 날짜·원자 출력·alias, 회귀 시험, 현재 실행 evidence
- 기준 명령: `python -B -X utf8 tools/openapi_exceptions.py --check`; `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v`; `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -v`; 문서 link/plan/SPDX/redaction/secret scan; `git diff --check`; PR CI checks
- 입력 고정: reviewer A/B는 이 manifest와 `post-fix-04 최종 후보` SHA/tree를 사용하고 서로의 결과·통합 report를 읽지 않는다. reviewer는 후보 파일을 수정하지 않고 별도 detached worktree에서 검토한다. post-fix-01/02의 BLOCK finding과 post-fix-03의 BOM·timezone 회귀를 새 기준선에서 재현한다.
- 외부 선행: 7개 소비자 저장소 export/build/e2e, GitHub Actions 원격 재실행·actionlint, npm/PyPI 게시와 GitHub Release는 이 common task 범위 밖이며 `NOT_RUN(사유)`로 기록한다.
