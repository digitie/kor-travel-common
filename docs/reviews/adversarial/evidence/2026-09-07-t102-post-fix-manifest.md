# T-102 post-fix 적대적 리뷰 공통 manifest

- Review ID: `t102-post-fix-20260907`
- 수리 기준 commit: `1a57b15` (`fix: T-102 별칭 검사와 weather 호환 계약 보강`)
- review 전 evidence 보존 parent: `9807fab`
- 초기 candidate/base: `8bc8179f728de88fd9327f9d4e8159188a95f9c3` / `843c404d79fd748cf6f8e40ce3e385fcabb0179f`
- branch: `codex/t102-aliases`
- 범위: 초기 BLOCK finding 전체의 수리 delta, `tools/check_aliases.py` parser·import·symlink/read/redaction 경계, alias root/dark 완전성·radius 계약, weather 고정 원천 예제·spacing 소유 경계·PROVENANCE, package README와 회귀 시험
- 범위 밖: 소비자 저장소 변경·T-461 실제 앱 build/e2e·6폭 시각 diff·npm/PyPI 게시·release/tag
- 공통 요청: 이 commit만 detached clean worktree에서 읽고 초기 A/B 원본 결과를 참고하되 상대 reviewer의 post-fix 결과는 열람하지 않는다. 초기 finding이 실제로 닫혔는지와 전체 delta의 새로운 회귀를 P0–P3로 다시 판정한다.

## 초기 finding disposition을 확인할 항목

- weather `--space-*` 8개는 앱마다 값이 달라 common shim에서 제외하고 비배포 weather 예제에 보존했다. T-102 수용 기준과 시험은 이 경계를 명시한다.
- weather 예제는 고정 commit의 light/dark common 값·brand·rail·sans/mono·spacing을 `--kt-*`/앱 소유 변수로 재표현하고 `PROVENANCE.md`에 PV-014를 추가했다. 소비자 화면 diff는 여전히 `NOT_RUN(T-461)`이다.
- alias `--radius-md`는 map/weather의 panel 의미인 `var(--kt-radius-panel)`로 정렬했다.
- checker는 문자열·주석·괄호를 인식하는 최소 CSS parser, 대소문자 `VAR`, 마지막 세미콜론 생략, url()/media/한 줄 복수 import, 재귀 closure 정책, root containment와 symlink loop/read failure, 안전한 진단 출력을 검증한다.
- alias 직접 선언의 `:root`/`.dark` 이름 집합 완전성과 import된 비정본 helper의 금지 정의·충돌을 시험한다. canonical `shadcn.css` import만 중복 예외다.

## 실행 가능한 검증

```text
python -B -X utf8 -m unittest discover -s tests -p 'test_check_aliases.py'
python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'
python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/check_spdx.py
python -B -X utf8 tools/scan_secrets.py --all
python -B -X utf8 tools/check_prod_redaction.py --all
python -B -X utf8 tools/check_versions.py --self-check
git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f 1a57b15
npm ci --ignore-scripts
npm run check --workspace packages/tokens
npm run build --workspace packages/tokens
npm test --workspace packages/tokens
npm pack --workspace packages/tokens --pack-destination <temporary-directory>
```

- Reviewer A 영역: legacy shared vocabulary·weather/map values·dark/profile·Tailwind/shadcn contract·visual regression risk.
- Reviewer B 영역: parser/graph/symlink/read/redaction·package/tarball·CI portability·GPL/SPDX/PROVENANCE·docs 정합.
- 두 reviewer는 각자 시작·종료 SHA/tree/status와 실제 실행 결과를 raw evidence에 남긴다.
