# T-102 post-fix 독립 적대적 리뷰 A 원본

- 실행 ID: A-T102-POST-20260907-234336
- verdict: BLOCK.
- candidate: b864eeb7feb8124aad40c78719da738939e4dcb7
- tree: b47be30f88648229485482f37234c5c103da8467
- repair parent: 1a57b15a043094960eb712ea73256ce487d7ad94
- 초기 candidate: 8bc8179f728de88fd9327f9d4e8159188a95f9c3
- immutable PR base: 843c404d79fd748cf6f8e40ce3e385fcabb0179f
- 격리: F:/dev/kor-travel-common-wt/review-t102-post-a, detached worktree.
- 시작: 2026-09-07 23:43:36.804 KST. 종료: 2026-09-07 23:50:20.220 KST.
- 시작·종료 git rev-parse HEAD/HEAD^{tree}는 위 값과 일치, git status --porcelain=v1은 모두 빈 출력.
- 후보 코드/문서/branch·source config·소비자 저장소 수정 없음. commit/push/publish 없음. 시험 변조와 raw/probe는 후보 밖에만 작성했다.
- 상대 reviewer의 이번 결과 또는 원본은 읽거나 요청하지 않았다.

## 기준과 범위

공통 manifest docs/reviews/adversarial/evidence/2026-09-07-t102-post-fix-manifest.md를 읽었다. 전달 요청은 최초 A spacing/weather fidelity/dark/url/imported kt finding을 재현하고 전체 수정 delta의 토큰 이름·radius-md·dark/profile·패키지/시각 회귀를 검토하는 것이다. consumer/T-461 gate는 실행하지 않은 상태로 분리한다.

초기 후보 대비 제품/정책/시험 수정과 새 manifest를 읽었다. 원본 B evidence는 열람하지 않았다. tokens.css/dist/theme.css/shadcn.css/package.json은 초기 후보 대비 불변임을 git diff --name-only로 확인했다. 새로운 CSS 파일/예제와 checker 564줄, 회귀 및 task/README/PROVENANCE를 직접 검토했다.

## 최초 finding disposition

| 원 ID / 심각도 | 판정 | 직접 재현 결과 |
|---|---|---|
| A-T102-P1-01 / P1 | FIXED | spacing 8개를 비배포 weather 예제에 두고 task의 소유 경계를 수정했다. 고정 geo1d9d74 spacing8값이 고정 weather6003da9와 실제로 모두 다름을 직접 확인했다. 설치 CSS+예제의 weather 이름 누락은 light/dark 모두 0이고 padding16px가 복원된다. |
| A-T102-P2-02 / P2 | OPEN, 부분 수정 | light 전체 legacy 값은 일치하고 mono/radius-md/spacing은 복원됐다. 그러나 dark 그림자 두 alpha가 원천과 다르다. 아래 잔여 반례 참조. |
| A-T102-P2-03 / P2 | FIXED(원 반례) | .dark 전체 삭제는 양 OS exit1/76 errors, 다른 dark brand 값은 exit1. 새 selector 오분류는 A-T102-P2-06으로 별도 기록했다. |
| A-T102-P2-04 / P2 | FIXED | url("../absent.css") import가 양 OS exit1이고 경로 해석 오류로 보고된다. |
| A-T102-P2-05 / P2 | FIXED(원 반례) | 임의 extra.css의 --kt-brand:red를 import하면 양 OS exit1. escaped identifier 우회는 A-T102-P2-07로 별도 기록했다. |

### 잔여 A-T102-P2-02 — dark 그림자 alpha를 원천에 없는 값으로 변경

- 위치: packages/tokens/examples/weather-overrides.css:97–98.
- 고정 weather 6003da995fa4b35799f9dadc406c6ba2878bfbae의 app/tokens.css는 :root의 elevated alpha0.1/modal alpha0.14를 .dark에서 재정의하지 않아 그대로 상속한다.
- 후보 예제는 .dark에 alpha0.12/0.18을 새로 선언한다. 실제 설치 CSS browser 비교에서 light changed=[]/missing=[], dark missing=[]지만 shadow-elevated 및 shadow-modal 두 값만 changed로 남는다.
- 영향: task와 예제 README의 고정 원천 light/dark 값 보존 계약을 아직 만족하지 않는다.
- 수정 수용 기준: dark의 두 원천 상속값을 실제로 보존하고, root만 대조하거나 .dark 텍스트 선언만 읽지 않는 브라우저/계산값 기반 전수 대조가 light/dark 모두 차이0임을 단언한다. 원 ID와 P2 심각도를 유지한다.

## 신규 findings

### A-T102-P2-06 — .dark 후손 선택자를 dark 표면 선언으로 오분류

- 심각도 P2 / OPEN. 위치: tools/check_aliases.py:116–124.
- 최소 재현: 정상 alias의 .dark {를 .dark .child {로 바꾸고 CLI를 실행한다. Windows/WSL 모두 exit0, CSS1/오류0.
- 실제 CSS: class=dark인 표면 자체는 이 선택자에 매치하지 않는다. Chromium에서 해당 표면의 --kt-brand는 dark oklch(76% 0.085 169)이지만 --brand는 light oklch(51.4% 0.081 169)이고 실제 배경도 light다.
- 원인: _scope가 selector 어디에든 .dark 토큰이 포함됐다는 이유로 dark mode라고 판정한다. 단순 이름 집합은 실제 표면 적용 여부를 증명하지 않는다.
- 수정 수용 기준: 지원하는 :root/.dark 직접 selector 문법을 정확히 한정하거나 selector를 의미적으로 해석한다. 지원하지 않는 복합·조건부 selector는 fail closed로 중단한다. 후손 .dark .child/조건부 selector가 direct dark 계약으로 인정되지 않는 회귀를 추가한다.

### A-T102-P2-07 — CSS escape identifier로 금지 정의와 미정의 참조를 우회

- 심각도 P2 / OPEN. 위치: tools/check_aliases.py:15–16, :320, :433.
- 최소 재현 A: 정상 alias에 :root { --\6b t-brand: red } 및 .dark의 같은 선언을 추가한다. CSS escape \6b 는 k로 해석된다. 양 OS CLI exit0인데 Chromium은 실제 --kt-brand와 --brand를 red, 배경 rgb(255,0,0)로 만든다.
- 최소 재현 B: var(--kt-brand)를 var(--\6b t-missing)으로 바꾼다. 양 OS CLI exit0인데 browser --brand는 빈 값이 되고 배경은 transparent다. literal --kt-brand:red 대조군은 exit1.
- 원인: CSS가 동일 이름으로 해석하는 escape를 raw ASCII 정규식이 인식하지 못하고, 미지원 identifier를 오류로 처리하지도 않는다.
- 수정 수용 기준: identifier escape를 CSS 규칙대로 정규화해서 검사하거나 지원하지 않는 escape identifier가 나오면 명시 오류로 중단한다. 선언/var 참조 두 경계가 같은 semantic 이름 검사로 귀속돼야 한다.

### A-T102-P1-08 — Windows 8.3 경로를 정상 디렉터리여도 패키지 밖으로 오판

- 심각도 P1 / OPEN. 위치: tools/check_aliases.py:358–384, :447–449.
- 최소 재현: 실제 정상 패키지 임시 사본의 aliases를 GetShortPathNameW로 변환해 같은 CLI에 전달한다. 긴 경로는 exit0, 짧은 8.3 표기는 exit1('별칭 경로를 읽을 수 없음')이다.
- 최초 실패 호출은 _safe_real(alias_lexical.parent, alias_lexical.parent, directory=True). lexical.is_relative_to(root)는 True지만 root.resolve(strict=True)는 긴 경로로 바뀌어 아직 짧은 root에 대한 is_relative_to가 False다. samefile은 True다.
- 직접 repr 요지: alias_lexical의 .../T102-S~1/PACKAG~1/aliases, root_lexical의 .../T102-S~1/PACKAG~1, root_resolved의 .../t102-shortpath-review-a-hxsqhj7g/package directory for path check는 같은 실제 디렉터리를 가리킨다. 첫 CSSInputError는 '패키지 밖 파일 경로'다.
- exact 후보 CI34134500500 Windows job도 225 tests 중 failures14/skipped2이며 정상 fixture가 ['별칭 경로를 읽을 수 없음']으로 실패한다. 로컬 long temp 경로의 225 성공을 CI portability 성공으로 대신할 수 없다.
- 수정 수용 기준: root를 독립적으로 canonicalize한 뒤 lexical/real containment 비교가 같은 좌표계에서 이뤄지게 한다. 8.3/long 동일 경로는 같은 정상 결과여야 하며 실제 외부 symlink/탈출은 계속 실패해야 한다. Windows CI와 direct short-path 회귀를 모두 재실행한다.

### A-T102-P2-09 — weather radius-md 수정으로 map의 고정 의미를 변경

- 심각도 P2 / OPEN. 위치: packages/tokens/aliases/map-vocabulary.css:48, :131; post-fix manifest의 radius 계약 설명.
- manifest는 map/weather 모두 radius-md=panel이라고 서술하지만 실제 고정 map c494e227e010565be295de3f9670b2f7c8c20944의 packages/kor-travel-map-admin/frontend/src/app/globals.css는 --radius-md:var(--radius-control)이다. weather6003da9만 panel이다.
- 후보 공용 shim은 두 모드 모두 panel로 바꿔 map 의미를 control6px → panel8px로 변경한다. 실제 Tailwind fixture의 rounded-md는 shim 없이6px, 새 shim과 함께8px이며 초기 shim의6px와도 다르다.
- 영향: weather 한 소비자의 수정을 공용 alias에 반영하면서 map의 값 무변경 이관 계약을 깨뜨린다.
- 수정 수용 기준: 양 원천의 차이를 문서로 정확히 기록하고 공용 map 의미와 weather 소유 호환 override를 분리한다. 같은 legacy 이름의 서로 다른 의미를 조용히 한 값으로 통일하지 않는다. 두 고정 원천 각각의 radius-md 계산값을 검증한다.

## 패키지·CSS·검증 결과

Windows Python3.14.3/Node25.9.0/npm11.12.1, WSL uv Python3.11.15/Node22.22.2/npm11.19.1에서 실행했다. Windows npm engine 경고는 숨기지 않았고 local exact Node22.23.1 검증으로 세지 않았다.

| gate | Windows | WSL |
|---|---|---|
| 전체 unittest | 225 tests / 68.658초 / OK / skip0 | 225 tests / 46.492초 / OK / skip0 |
| focused aliases | 22 tests / 0.592초 / OK | 22 tests / 0.317초 / OK |
| 후보 checker | 정상 exit0 | 정상 exit0 |
| npm ci/check/build/check/test | 모두0, 7 package tests/skip0 | 동일 |
| pack/install/alias export | tarball19파일, alias 포함·examples 제외, resolve 성공 | 동일 |
| plan | 106 task/오류0 | 동일 |
| 문서 링크 | 370문서/2333대상/오류0 | 동일 |
| SPDX | 45파일/오류0 | 동일 |

Windows scan_secrets --all / check_prod_redaction --all은 각각485파일/발견0/예외0이고 check_versions --self-check는 exit0이다.

별도 실패 gate: base..candidate git diff --check는 docs/reviews/adversarial/evidence/2026-09-07-t102-initial-reviewer-a.md:118의 new blank line at EOF로 exit1이다. 이 artifact 오류는 이번 후보에 실제 존재하는 실패이며 NOT_RUN 또는 PASS가 아니다. coordinator의 후속 raw 보존/속성 예외 계획은 아직 이 후보에 없으므로 해결된 것으로 세지 않는다.

실제 설치 CSS의 shadcn 상대 import는 --card/--border/--destructive/--input/--primary를 정상 제공한다. Tailwind4.3.3 package import도 해결되고 bg-kt-brand가 생성된다. shadow-card/shadow-card-hover none, navy brand4종·17rem·sans/mono·radius 및 spacing의 light 재현은 정상이다. 전체 소비자 화면을 실행한 것은 아니다.

## 원격 CI

gh pr view 14로 exact headRefOid=b864eeb7feb8124aad40c78719da738939e4dcb7를 확인했다. [CI34134500500](https://github.com/digitie/kor-travel-common/actions/runs/34134500500)의 docs 및 tools(windows-2025)는 FAILURE, tools(ubuntu-24.04)·secret-scan·check-versions·packages는 SUCCESS다.

Windows 실패 job101782212673의 실제 로그를 직접 읽었다. 225 tests / failures14 / skipped2이며 정상 alias fixture도 경로 오류다. 이는 docs 공백 오류와 별개의 실행 실패다. 정확한 로컬 short-path 원인 재현은 A-T102-P1-08에 기록했다.

## 명령·보존 probe

기본 cwd는 detached 후보이며 Python 전체/focused/checker와 manifest의 각 validator를 실행했다. WSL은 같은 경로의 /mnt/f 표기에서 uv run --no-project --python 3.11 python -B -X utf8로 실행했고 전체 unittest에 --with jsonschema==4.26.0을 추가했다.

    python -B -X utf8 -m unittest discover -s tests -q
    python -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py -q
    python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-a-package.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-post-a-original-negative.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-post-a-negative.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-post-a-shortpath.py

shortpath helper는 Windows 전용이며 GetShortPathNameW/각 repr/samefile/첫 _safe_real 오류/long·short CLI 결과를 재현한다. 나머지 original/new negative는 양 OS 실행했다.

브라우저 fixture: F:/dev/kor-travel-common/.git/codex-audit/t101-css-a/t102-post에서 node probe.mjs. probe-output.txt·tarball 설치본·고정 weather.css·후보 예제·HTML/CSS 반례를 보존했다. 값 비교 원천은 이전에 고정 Git object에서 추출한 동일 weather.css를 재사용했다. map radius와 geo spacing은 이번에 고정 Git object에서 새로 직접 읽었다.

WSL 원 반례 출력을 head -c로 자른 최초 시도는 helper의 BrokenPipeError로 중단됐으며 checker 오류가 아니다. 이후 출력 요약 helper를 별도로 만들어 모든 원 반례를 끝까지 다시 실행했고 exit1 결과를 확인했다. 잘못된 F:/dev/kor-travel-geo 조회는 저장소가 아니어서 실패했고, inventory의 실제 F:/dev/kor-travel-geo-fixes에서 동일 고정 SHA를 읽어 보완했다.

## NOT_RUN과 결론

- NOT_RUN: 실제 소비자/T-461 build/e2e·6폭 시각 diff, 폰트 파일 로딩과 glyph 비교. 이번 browser는 작은 CSS fixture이며 소비자 gate 완료가 아니다.
- NOT_RUN: WSL browser, local exact Node22.23.1, WSL secret/redaction 전체 재실행, release/main push run 관찰.
- NOT_RUN: npm/PyPI 게시·Release/tag 생성·소비자 수정. 요청 범위 밖.

최초 A 5건 중4건은 원 반례가 FIXED, A-T102-P2-02는 잔여 OPEN이다. 신규 A-T102-P2-06/07/09와 A-T102-P1-08이 OPEN이며 docs diff/Windows CI gate도 실패했다. 이 후보에 대한 독립 최종 판정은 BLOCK이다.
