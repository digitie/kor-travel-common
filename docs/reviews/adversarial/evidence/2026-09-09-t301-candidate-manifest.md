# T-301 OpenAPI 정본 candidate 공통 manifest

- Review ID: `T301-20260909-candidate`
- 기준선: `afc8d1bf166d0ddcbee059252eb5cee245157dcd` (`origin/main`)
- candidate commit: `0c0c189017989065fd8ced9e6e84ad9c6e7b7756`
- candidate tree: `e5a3ff3466dc13e25a9cce3fcdde50d6ff213f3f`
- 대상 PR: [#22](https://github.com/digitie/kor-travel-common/pull/22)
- 검토일: 2026-09-09 (Asia/Seoul)

## 검토 범위

candidate commit의 변경 파일 전체를 검토한다. 핵심 범위는 다음과 같다.

- `docs/standards/openapi.md` — ADR-009/D-14와 core M1~M9·S1~S13·N1~N8, M10 교차 pin, 헤더·`X-Request-ID`, 429/O-14
- `docs/standards/openapi-exceptions.yaml` — 정본 7키 레지스트리, 기존 46건의 근거·기한
- `tools/openapi_exceptions.py` — PyYAML 없는 fail-closed parser, schema/date/rule/sunset 검증, 생성물 drift
- `docs/standards/openapi-exceptions.md` — 생성물 불변성·표 escape·SPDX
- `tests/test_openapi_exceptions.py` — canonical·malformed·drift·문서 계약 회귀
- 색인·survey 정정·task/resume/journal/changelog의 수치·상태·링크 정합성

## 공통 재현 명령

```text
python -B -X utf8 tools/openapi_exceptions.py --check
python -B -X utf8 -m unittest discover -s tests -p "test_openapi_exceptions.py" -v
python -B -X utf8 tools/validate_document_links.py .
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
git diff --check
```

소비자 저장소 build/e2e·OpenAPI 실제 export·npm/PyPI·GitHub Release는 이 common PR 범위 밖이며 `NOT_RUN`으로 판정한다. 각 reviewer는 상대 reviewer의 결과를 읽지 않고, 이 manifest의 candidate SHA/tree를 기준으로 독립 실행한다. finding은 P0~P3와 `FIXED`/`OPEN` disposition을 명시한다.
