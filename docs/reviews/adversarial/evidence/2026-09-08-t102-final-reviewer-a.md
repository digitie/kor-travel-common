# T-102 최종 후보 독립 적대적 리뷰 A 원본

- 실행 ID: A-T102-FINAL-20260908-000552.
- verdict: BLOCK. 잔여 A-T102-P2-06 1건, 신규 ID 0건.
- candidate: 09162025140991d24775abc76571f35de9974022.
- tree: db7e673bbd56191cdd2afdded75fba670e74c6c5.
- parent: 46b52d50b49f85da947998d8703f7586f83270c6.
- 직전 검토 후보: b864eeb7feb8124aad40c78719da738939e4dcb7.
- immutable 전체 base: 843c404d79fd748cf6f8e40ce3e385fcabb0179f.
- 격리: F:/dev/kor-travel-common-wt/review-t102-final-a, detached worktree.
- 시작: 2026-09-08 00:05:52.691 KST. 종료: 2026-09-08 00:09:32.774 KST.
- 시작·종료 HEAD/tree는 위 값과 일치하고 git status --porcelain=v1은 모두 빈 출력이다.
- 후보·소비자 파일·source .git/config 수정 및 commit/push/publish 없음. 변조·설치는 후보 밖의 임시 사본에만 수행했다.
- reviewer B의 이번 원본/결과를 열람하거나 요청하지 않고 판정했다.

## 요청과 검토 범위

공통 manifest docs/reviews/adversarial/evidence/2026-09-08-t102-final-manifest.md를 읽고 이전 A finding의 dark shadow·직접 selector·CSS escape·Windows8.3·map/weather radius 수정 및 전체 제품/정책 delta를 대조했다. 새 B raw는 읽지 않았다. manifest와 달라 보이는 경계를 작성자 설명 대신 실제 코드와 browser/CLI로 검증했다.

직전 후보 대비 수정된 .gitattributes·task·alias·예제·README·parser·tests를 직접 읽었다. tokens.css/dist/theme.css/shadcn.css/package.json은 동일함을 git diff --name-only로 확인했다. 고정 weather/map/geo 원천의 이전 직접 대조 결과를 재사용하되 현재 설치 패키지의 CSS 계산값과 negative CLI는 새 후보에서 전부 다시 실행했다.

## 잔여 finding

### A-T102-P2-06 — 외부 조건/부모 블록을 무시해 direct dark mode로 오판

- 원 심각도: P2. Disposition: OPEN, 부분 수정. 새로운 ID로 바꾸지 않는다.
- 위치: tools/check_aliases.py:116–137의 _scope.
- 고쳐진 부분: .dark .child 같은 하나의 복합 selector는 이제 거부된다.
- 잔여 최소 재현 1: 원본 aliases/map-vocabulary.css의 .dark 블록만 @media print { .dark { ... } } 안으로 옮긴다.
- 잔여 최소 재현 2: 같은 블록을 .wrapper { .dark { ... } } 안으로 옮긴다.
- Windows/WSL 양쪽 checker는 두 경우 모두 exit0, '별칭 검사 통과: CSS 1개, 오류 0개'를 출력했다.
- 실제 CSS 확인: Chromium screen에서 부모 .wrapper 없이 class=dark인 표면을 렌더링하면 semantic --kt-brand는 oklch(76% 0.085 169)이지만 alias --brand는 root light의 oklch(51.4% 0.081 169)이고 background는 oklch(0.514 0.081 169)다. 두 반례 모두 동일하다.
- 원인: _scope는 가장 안쪽의 .dark를 찾은 순간 그것만 판정한다. 바깥 @media print 조건이나 .wrapper 부모 선택자 스택이 실제로 적용 대상을 제한한다는 사실을 버린다.
- 계약: final manifest는 ':root, .dark 직접 선택자만 mode로 인정하고 후손·조건부 선택자는 fail closed'라고 명시한다. 현재 코드가 이 수용 기준을 아직 충족하지 않는다.
- 수정 수용 기준: 최상위의 지원된 직접 selector인지 스택 전체로 확인하거나 지원 범위를 명시적으로 해석한다. 지원하지 않는 외부 조건/중첩 부모가 있는 alias 선언은 성공으로 세지 않는다. 위 두 반례가 exit1이고 정상 :root/.dark 및 :root, .dark 대조군은 성공해야 한다.

## 누적 A finding disposition

| ID / 원 심각도 | 판정 | 이번 직접 검증 |
|---|---|---|
| A-T102-P1-01 / P1 | FIXED | spacing8개를 앱 예제로 보존하고 공용 승격에서 제외한 task 경계를 유지한다. weather light/dark 이름 누락0, padding16px. |
| A-T102-P2-02 / P2 | FIXED | weather 원천의 모든 legacy 값이 light/dark 모두 changed=[]로 일치한다. dark shadow의 .1/.14 상속값도 복원됐다. |
| A-T102-P2-03 / P2 | FIXED | 원 .dark 전체 삭제는 양 OS exit1/76 errors, 다른 brand 값은 exit1. |
| A-T102-P2-04 / P2 | FIXED | url() absent import는 양 OS exit1. |
| A-T102-P2-05 / P2 | FIXED | extra.css의 literal --kt-brand 정의 import는 양 OS exit1. |
| A-T102-P2-06 / P2 | OPEN | .dark .child는 실패하지만 외부 media/부모 nesting은 성공해 위 잔여 반례가 남는다. |
| A-T102-P2-07 / P2 | FIXED | escaped kt 선언과 escaped var 참조는 양 OS exit1. 함수명/import명/import target/string escape 거부의 checked-in 시험도 통과한다. |
| A-T102-P1-08 / P1 | FIXED | GetShortPathNameW로 만든 실제8.3/long 동일 aliases 경로가 모두 exit0. samefile=True이고 더 이상 lexical/real 혼합 때문에 거부되지 않는다. exact Windows CI도 성공했다. |
| A-T102-P2-09 / P2 | FIXED | 공용 map radius-md는 control6px, weather 예제는 panel8px로 분리됐다. 실제 map/Tailwind 표본6px와 weather 계산8px를 확인했다. task/README도 차이를 명시한다. |

이전 raw EOF 공백으로 실패하던 base..HEAD git diff --check는 현재 .gitattributes의 원본 경로 예외와 함께 exit0이다. raw 원본은 직접 편집하지 않았다.

## 패키지·CSS 직접 검증

Windows Python3.14.3 / Node25.9.0 / npm11.12.1, WSL uv Python3.11.15 / Node22.22.2 / npm11.19.1을 사용했다. Windows npm engine 경고를 버전 일치 성공으로 세지 않았다.

| gate | Windows | WSL |
|---|---|---|
| 전체 Python 회귀 | 234 tests /65.605초 /OK /skip0 | 234 discovered /40.907초 /OK /skip1(Windows8.3 API 전용; 실행 성공233) |
| focused aliases | 31 tests /0.781초 /OK /skip0 | 31 discovered /0.380초 /OK /skip1(Windows 전용; 실행 성공30) |
| original/new negative corpus | 이전 원 반례는 expected exit1, 잔여 conditional2개는 exit0 | 동일 |
| npm ci/check/build/check/test | 모두0, package tests7/skip0 | 동일 |
| pack/install/alias resolve | tarball19파일, alias 포함, examples 제외, resolve 성공 | 동일 |
| plan | 106 task/오류0 | 동일 |
| links | 373문서/2333대상/오류0 | 동일 |
| SPDX | 45파일/오류0 | 동일 |

Windows secret/prod-redaction --all은 각각488파일/발견0/예외0, versions self-check와 전체 base..candidate diff --check는 exit0이다.

Windows 실제 Tailwind4.3.3 package @import와 Chromium CSS link를 사용했다. shadcn 내부 상대 import는 card/border/destructive/input/primary 이름을 정상 제공한다. weather fixed source와 비교한 light missing/changed 및 dark missing/changed는 모두 빈 목록이다. map용 rounded-md6px, weather radius-md8px, navy4종·17rem·sans/mono·spacing·dark shadow가 각각 기대와 일치한다.

브라우저 probe에 과거 불량 CSS 자체의 렌더링도 보존돼 있다. 그 CSS가 여전히 잘못 보인다는 출력은 해당 불량 파일을 checker가 현재 거부하는지와 함께 해석했다. 현재 gate가 거부하는 escaped/삭제 원 반례를 잔여 finding으로 재집계하지 않았다.

## 실제 명령 및 원본 probe

기본 cwd는 detached 후보다.

    python -B -X utf8 -m unittest discover -s tests -q
    python -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py -q
    python -B -X utf8 tools/check_aliases.py packages/tokens/aliases
    python -B -X utf8 tools/validate_plan.py
    python -B -X utf8 tools/validate_document_links.py
    python -B -X utf8 tools/check_spdx.py
    python -B -X utf8 tools/scan_secrets.py --all
    python -B -X utf8 tools/check_prod_redaction.py --all
    python -B -X utf8 tools/check_versions.py --self-check
    git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f HEAD

후보 밖 main .git/codex-audit의 reviewer 소유 helper를 같은 cwd에서 실행했다.

    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-a-package.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-post-a-original-negative.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-post-a-negative.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-post-a-shortpath.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t102-final-a-conditional.py

WSL은 같은 detached /mnt/f 경로에서 uv run --no-project --python 3.11 python -B -X utf8로 실행했다. 전체 unittest는 --with jsonschema==4.26.0을 추가했다. shortpath helper만 Windows 전용이며 나머지 package·원/새 negative·conditional helper는 양 OS 실행했다.

브라우저 fixture: F:/dev/kor-travel-common/.git/codex-audit/t101-css-a/t102-final. node probe.mjs 결과를 probe-output.txt에 저장했다. 현재 tarball 설치본·후보 예제·고정 weather.css·각 HTML/CSS 반례를 보존했다. source fixture는 고정6003da9 object를 이전 직접 조사에서 추출한 동일 원천이며 consumer checkout을 수정하지 않았다.

## CI와 NOT_RUN

[PR14 CI34136465020](https://github.com/digitie/kor-travel-common/actions/runs/34136465020)의 headRefOid가 정확한 candidate SHA이며 docs·tools Ubuntu·tools Windows·secret-scan·check-versions·packages 6 jobs가 모두 SUCCESS임을 직접 관찰했다. 이 성공은 잔여 조건부 mode 반례를 탐지한다는 증거가 아니다.

- NOT_RUN: 실제 소비자/T-461 build/e2e·6폭 시각 diff·폰트 파일/glyph 검증. 작은 CSS fixture의 값 대조를 소비자 gate로 대신하지 않는다.
- NOT_RUN: WSL browser·local exact Node22.23.1·WSL 전체 secret/redaction 재실행·release/main push run 관찰.
- NOT_RUN: npm/PyPI 게시·Release/tag 생성·consumer write. 요청 밖이다.
- WSL의 Windows8.3 전용 skip1은 통과로 집계하지 않았다. 같은 기능은 Windows에서 실제 API/CLI로 실행했다.

누적 A 9개 ID 중8개가 FIXED이고 A-T102-P2-06은 조건부/중첩 부모에 대한 잔여 OPEN이다. 해당 P2 수용 기준이 닫히기 전 이 후보의 독립 verdict는 BLOCK이다.
