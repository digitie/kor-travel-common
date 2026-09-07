# T-102 최종2 후보 적대적 리뷰 공통 manifest

- Review ID: `t102-final2-20260908`.
- 후보 선행 commit: `0b50a63` (`fix: T-102 mode stack과 비ASCII 별칭 검사를 닫는다`). 이 manifest를 포함한 다음 immutable commit의 정확한 SHA·tree는 각 reviewer 원본에 기록한다.
- 전체 base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`.
- branch: `codex/t102-aliases`.
- 범위: T-102 구현 전체, 이전 A/B BLOCK 원본과 최종2 수정의 parser·mode scope·duplicate·Unicode 경계, weather/map 토큰 의미, GPL/PROVENANCE·package·CI 회귀.
- 범위 밖: 소비자 저장소 변경·T-461 실제 앱 build/e2e·6폭 시각 diff·npm/PyPI 게시·release/tag.
- 직전 A 원본: `2026-09-08-t102-final-reviewer-a.md`, SHA256 `AC38FE23D924EB8AA1F2B7987116ADB6731607C246A6AFD7D36B2B17C4679C5C`.
- 직전 B 원본: `2026-09-08-t102-final-reviewer-b.md`, SHA256 `DEACCAED247797E78B87677C212B7DC316DE2F43D46E2A4D9A036590DF5F0A79`.

## 최종2 수용 기준

- alias custom property가 `@media`·`@supports` 등 조건부 at-rule 안에 있거나 `.wrapper` 같은 부모 selector 안에 있으면 mode로 집계하지 않고 fail closed 한다. 최상위 `:root`, `.dark`, `:root, .dark`만 성공한다.
- `:root, .dark`의 `both` 선언은 root와 dark 각각의 identity로 중복 검사를 받아 `both`+root 또는 `both`+dark를 통과시키지 않는다. 중복 없는 단일 `both`는 성공한다.
- CSS custom property와 `var(--kt-…)` 검사에는 비ASCII identifier가 포함된다. `--kt-한글` 정의는 금지되고, 정본에 없는 `var(--kt-없는)` 참조는 실패한다. 주석·문자열의 일반 Unicode는 구조 토큰으로 오인하지 않는다.
- 이전 수용 기준(escape 거부, import closure/경계, redaction, Windows 8.3, map control/weather panel radius, weather dark shadow 상속, spacing 앱 소유)은 그대로 유지한다.

## 실행 가능한 검증

```text
python -B -X utf8 -m unittest tests/test_check_aliases.py -q
python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
git diff --check
npm run check --workspace packages/tokens
npm run build --workspace packages/tokens
npm test --workspace packages/tokens
npm pack --workspace packages/tokens --pack-destination <temporary-directory>
```

- 직전 후보 로컬 결과: focused 35개 통과, 전체 unittest 238개 통과, checker 오류 0, 문서 375개·local target 2333개 오류 0, plan 106개 오류 0, SPDX 45개 오류 0, secrets/redaction 490개 파일 발견 0, versions self-check 통과.
- 두 reviewer는 각자 detached clean에서 시작·종료 SHA/tree/status와 실제 명령 결과를 기록하고 상대 결과를 읽지 않는다. final2 반례와 누적 finding이 모두 닫힌 경우에만 PASS로 판정한다.
- 소비자 build/e2e·T-461 6폭 diff는 `NOT_RUN(T-461)`이며, npm/PyPI 게시와 release도 실행하지 않는다.
