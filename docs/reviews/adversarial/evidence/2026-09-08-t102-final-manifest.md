# T-102 최종 후보 적대적 리뷰 공통 manifest

- Review ID: `t102-final-20260908`.
- 후보 선행 commit: `46b52d5` (`fix: T-102 별칭 검사 경계와 모드 판정을 보강한다`). 이 manifest를 포함한 다음 immutable commit의 정확한 SHA·tree는 각 reviewer 원본에 기록한다.
- 전체 base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`.
- branch: `codex/t102-aliases`.
- 범위: T-102 구현과 초기·post-fix BLOCK finding의 수정, 별칭 parser·import closure·경로 경계·진단 redaction, root/dark 계약, map/weather radius 의미, weather 예제와 GPL/PROVENANCE, package export와 회귀 시험.
- 범위 밖: 소비자 저장소 변경·T-461 실제 앱 build/e2e·6폭 시각 diff·npm/PyPI 게시·release/tag.
- 초기 A 원본: `2026-09-07-t102-initial-reviewer-a.md`, SHA256 `256CD82C484E2DD12D35CA857724164C876FA4E91D0A1367288FDB95DF2EE32C`.
- 초기 B 원본: `2026-09-07-t102-initial-reviewer-b.md`, SHA256 `183B46D33DD71E9FA67EFF1BFFCAE423A0DB493F81B61BC22E108D8BDAAC5AF3`.
- 직전 post-fix A 원본: `2026-09-07-t102-post-fix-reviewer-a.md`, SHA256 `DEE997451D47817060C835D34467EDEEE078ED0FA37A145CA857CFFB392BF98A`.
- 직전 post-fix B 원본: `2026-09-07-t102-post-fix-reviewer-b.md`, SHA256 `66147039D062736C2A5A0F40B51CEA83B2A6613DB8140BD18316B44B225910E2`.

## 확인할 수정 수용 기준

- weather에만 있고 geo와 값이 다른 `--space-3xs..2xl` 8개는 common shim에서 제외하고 비배포 weather 예제에 보존한다.
- weather 예제는 고정 원천 `6003da995fa4b35799f9dadc406c6ba2878bfbae`의 light/dark common 값·navy brand·17rem rail·sans/mono·상속 shadow·spacing을 보존하며 PV-014와 `Origin`을 가진다.
- map의 `--radius-md`는 `--kt-radius-control`을 유지하고, weather의 서로 다른 panel 의미는 예제에서 `--radius-md: var(--kt-radius-panel)`로 재선언한다.
- checker는 마지막 세미콜론 생략·대소문자 `VAR`·url/media/복수 import·재귀 closure·symlink/read failure를 제어하고, 지원하지 않는 CSS escape는 정의·참조·import 위치와 문자열 모두에서 거부한다.
- checker는 `:root`, `.dark`, `:root, .dark` 직접 선택자만 mode로 인정하고 후손·조건부 선택자는 fail closed 한다. 입력 경로·식별자·값을 진단에 재출력하지 않는다.
- lexical 경로와 canonical 경계를 같은 좌표계로 비교해 Windows 8.3 경로를 정상 처리하면서 외부 symlink와 import 탈출은 계속 거부한다.

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

- 현재 로컬 결과: focused 31개 통과, 전체 unittest 234개 통과, checker 오류 0, 문서 372개·local target 2333개 오류 0, plan 106개 오류 0, SPDX 45개 오류 0, secrets/redaction 487개 파일 발견 0, versions self-check 통과, tokens package test 7개 통과.
- reviewer A는 토큰 의미·값 보존·CSS 적용 범위를, reviewer B는 parser/graph·경로·redaction·package/CI·GPL evidence를 독립적으로 재검토한다. 두 reviewer는 상대 결과를 읽지 않고 시작·종료 SHA/tree/status와 원시 명령 결과를 남긴다.
- consumer build/e2e·T-461 6폭 diff는 `NOT_RUN(T-461)`이며, npm/PyPI 게시와 release도 실행하지 않는다.
