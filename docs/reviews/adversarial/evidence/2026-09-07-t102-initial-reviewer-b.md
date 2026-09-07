# T-102 초기 독립 적대적 리뷰 B 원본

- 실행 ID: `reviewer_b-t102-initial-8bc8179-20260907-231226`
- 최종 verdict: **BLOCK**. P0 0건, P1 4건, P2 3건, P3 1건.
- 후보 시작·종료 SHA: `8bc8179f728de88fd9327f9d4e8159188a95f9c3`
- 후보 시작·종료 tree: `8e7a66aeb2875b74cec2a98afc4b7fdeb1edcf97`
- base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`
- 시작 KST: `2026-09-07T23:12:26.2079659+09:00`
- 종료 검증 KST: `2026-09-07T23:21:52.7943516+09:00`
- 격리: 후보에서 생성한 detached `F:/dev/kor-travel-common-wt/review-t102-b`. 시작·종료 `git status --porcelain=v1` 출력 없음.
- reviewer A 원본·finding·결과 미열람. 후보 코드·문서·시험 수정, 후보 commit/push, 소비자 쓰기, registry 게시 없음. 자체 probe/report는 후보 밖 source checkout의 `.git/codex-audit/`에 보존했다.

## 요청·범위

요청 원문: T-102 초기 적대적 리뷰를 독립적으로 수행. 후보 `8bc8179f728de88fd9327f9d4e8159188a95f9c3`, base `843c404d79fd748cf6f8e40ce3e385fcabb0179f`, branch `codex/t102-aliases`. B 영역은 Python checker parser/경계·import traversal/symlink/read failures/exit code, npm files/exports/tarball, CI Windows/Ubuntu, SPDX/GPL/secret/redaction, docs/tool integration/source drift. CSS comments/one-line/multiple import/duplicate root-dark, package 밖 import, examples 유출·미게시 경계를 공격하고 원본·SHA/tree/status·명령·한계·verdict를 남길 것.

변경 8파일 전체를 읽고 T-102, agent-workflow §5.3, licensing LIC-12/16/24·§5.2, package 공개 계약, 도구 README, 실제 workflow와 비교했다. 정본 tokens.css·기존 dist·versions.json의 base 대비 변경 없음도 확인했다. 현재 정상 fixture 결과를 신뢰 근거로 삼기 전에 독립 합성 입력 27건을 양 OS에서 직접 실행했다.

## 유효 검증 결과

| 항목 | Windows | WSL |
|---|---|---|
| runtime | Python 3.14.3, Node v25.9.0/npm 11.12.1 | Python 3.11.15, Node v22.22.2/npm 11.19.1 |
| 전체 unittest | 212 tests, OK, skip 0 (57.754초) | 독립 /tmp 사본에서 212개 실행, 210 pass·2 skip, 오류 0 (14.695초) |
| aliases focused | 9 tests OK (0.278초) | 위 전체 실행에 9개 모두 포함 |
| 후보 checker CLI | CSS 1개, 오류 0, exit 0 | 동일 |
| 독립 checker probe | 27건 실행, 아래 false PASS/오류 재현 | 27건 실행, 아래 false PASS/오류 재현 |
| npm ci/check/build/check/test | 모든 명령 0, package 7 tests/skip 0 | 동일 |
| pack/install | 모두 exit 0 | 모두 exit 0 |
| 설치 후 exports·ESM | 구체 subpath 14개 resolve, tokenValues 44개 | 동일 |
| 내용물 | 19파일, aliases/map-vocabulary.css·shadcn.css 포함, examples 없음 | 동일 |
| LICENSE | tarball LICENSE bytes가 repo LICENSE와 동일 | 동일 |
| link | 366문서, 2331대상, 오류 0 | 동일 |
| plan | 106 tasks, 오류 0 | 동일 |
| SPDX | 45파일, 오류 0 | 동일 |
| secret/redaction | 각각 481파일, 발견 0·예외 0 | 동일 |
| versions self-check / diff check | exit 0 / exit 0 | 동일 |

Windows Node engine 경고는 존재하며 정확한 권장 runtime 성공으로 세지 않는다. WSL 두 skip은 jsonschema 미설치에 따른 기존 manifest schema parity 시험(`test_json_schema_rejects_control_character_paths_like_stdlib`, `test_json_schema_rejects_non_ascii_and_trailing_newline_dates`)이다. 212개 전부 pass로 집계하지 않는다.

임시 tarball SHA256: Windows `6aad65017a9e6bb0b50999e818fde279644b4fac76c9b9cdc7d2e71115e4d648`, WSL `0c2b51b52ad7abf27956c75c57bd518124bf55961c2b04e6c7ee8b0ac901370e`. 런타임/npm이 달라 byte 동일성을 주장하지 않는다. 파일 배포 설치만 실행했고 npm/PyPI에 게시하지 않았다.

## Finding

### B-P1-01 — 유효한 CSS 선언/함수 문법을 놓쳐 금지 선언과 미정의 참조를 통과시킨다

- 위치: `tools/check_aliases.py:14–15,33–41,121–123`.
- 양 OS 최소 반례: 정상 임시 tokens/theme/shadcn 파일 옆 aliases/map.css에 `:root { --kt-brand: red }`를 쓰면 exit 0/오류 0이다. 세미콜론을 붙인 동일 선언은 금지 오류 exit 1이다. `:root { --color-kt-brand: red }`도 충돌인데 통과한다.
- `:root { --brand: VAR(--kt-missing); }` 역시 exit 0이며, 반대로 `:root { --brand: "var(--kt-missing)"; }`의 문자열 내용은 실제 참조가 아닌데 미정의 참조로 exit 1이다.
- Chromium 실험에서 마지막 세미콜론 없는 custom property는 실제 적용되고 대문자 `VAR()`는 참조를 해석한다. 문자열은 그대로 문자열이다. 따라서 단순 비정상 CSS 입력에 대한 관용 문제가 아니다.
- 영향: `--kt-*` 선언 금지·namespace 충돌·미정의 참조 차단이라는 T-102 필수 gate를 정상 CSS 문법으로 우회한다.
- 권고/disposition: **FIX_REQUIRED**. 문자열·주석·함수·선언 경계를 인식하는 최소 파서를 사용하고, 지원하지 않는 구문은 조용히 누락시키지 말고 명시적으로 실패시킨다. 블록 마지막 선언과 함수명의 대소문자 규칙을 포함한 회귀를 추가한다.

### B-P1-02 — import 인식이 줄 시작의 단순 따옴표 형식으로 한정되어 package 경계를 우회한다

- 위치: `tools/check_aliases.py:16,45–48,69–70`.
- 양 OS 최소 반례: `@import "../shadcn.css"; @import "../../outside.css";`를 같은 줄에 두면 exit 0이다. `@import url("../../outside.css");` 및 `@import "../../outside.css" screen;`도 각각 exit 0이다. 단독 줄의 단순 `@import "../../outside.css";`는 exit 1로 차단된다.
- Chromium CSSOM은 한 줄에 두 import rule을 인식하고 url()/media 조건 형식도 import rule로 인식했다. 네트워크 요청은 전부 abort해 외부 파일을 가져오지 않았다.
- 영향: checker가 알려진 표현 한 종류만 경계 검사한다. 브라우저가 소비하는 import 그래프와 검사 그래프가 달라 package 밖 파일·누락 의존성·공급 파일을 성공으로 표시한다.
- 권고/disposition: **FIX_REQUIRED**. 모든 import rule을 찾아 동일 root/누락/순환 정책을 적용한다. url·조건·복수 rule을 지원하지 않기로 하면 명시적 오류로 거부한다.

### B-P1-03 — 재귀 import한 별칭의 정의 정책을 전부 건너뛴다

- 위치: `tools/check_aliases.py:104–119,131–165`.
- 양 OS 최소 반례: aliases/map.css가 `@import "./nested/evil.css";`로 `aliases/nested/evil.css`의 `:root { --kt-brand: blue; }`를 가져오면 exit 0이다. 같은 내용을 map.css에 직접 쓰면 exit 1이다.
- `../extra.css`에서 `--color-kt-brand: blue;`를 정의하거나, imported `--brand: blue;`와 직접 `--brand: var(--kt-brand);`를 함께 두어도 exit 0이다.
- 원인: imported_defs는 수집하지만 금지/namespace/shadcn/값 drift 검사는 alias_defs만 사용한다. all_defs를 만든 뒤 버린다. `shadcn.css`의 의도적 정본 import와 임의 imported file을 구별하지 않는다.
- 영향: 이름 충돌·정본 토큰 재정의·root/dark 값 drift를 파일 하나로 분리하는 것만으로 필수 gate에서 숨긴다.
- 권고/disposition: **FIX_REQUIRED**. 재귀 alias 소스에도 같은 정책을 적용하고, 필요한 정본 import 면제는 정확한 canonical 파일/소유 계약으로 제한한다. 직접·간접 선언 사이 중복도 검사한다.

### B-P2-04 — 필수 정본 CSS는 root containment 검사 없이 외부 symlink를 따라간다

- 위치: `tools/check_aliases.py:89–103`.
- 양 OS 최소 반례: 정상 fixture의 tokens.css를 패키지 밖 `../outside.css`로 향하는 symlink로 바꾸고 그 파일에 필요한 `--kt-brand`를 정의하면 CLI exit 0이다. alias CSS 자체를 외부 symlink로 바꾸면 package 밖 오류 exit 1이다.
- 영향: 같은 checker 안에서 별칭과 정본의 파일 경계가 다르다. 패키지 밖 값으로 검사한 결과를 해당 패키지 자체의 계약 검증처럼 보고한다. tarball에 외부 정본이 포함되는지는 이 성공으로 보증되지 않는다.
- 권고/disposition: **FIX_REQUIRED**. tokens/theme/shadcn에도 동일 root containment·파일 종류·symlink 정책을 적용한다. CLI가 package 밖 정본을 허용할 필요가 있다면 별도 명시 입력과 범위를 먼저 계약화한다.

### B-P2-05 — 읽기 실패와 symlink loop가 통제된 진단 대신 traceback으로 종료된다

- 위치: `tools/check_aliases.py:35,47,59,79–82,99–103,122,175`.
- 양 OS 최소 반례: alias 파일을 invalid UTF-8 byte로 쓰면 exit 1 + UnicodeDecodeError traceback. `aliases/map.css -> map.css` self-symlink도 양 OS exit 1 + traceback이며 WSL에서는 RuntimeError가 나타난다.
- WSL에서 alias chmod 000은 PermissionError traceback이다. Windows chmod 000은 ACL 읽기를 막지 않으므로 Windows 접근 거부 시험으로 세지 않는다.
- 정상 누락 import와 required self-symlink는 통제된 오류로 반환되므로 경로 종류마다 실패 형식이 다르다.
- 영향: API인 check_aliases가 예외를 호출자에게 흘리고 CLI는 절대경로/구현 trace를 출력한다. 플랫폼별 결과 동일과 사람이 이해할 수 있는 오류 목록 계약이 깨진다.
- 권고/disposition: **FIX_REQUIRED**. 전체 파일 선택/resolve/read 경계에서 OSError·UnicodeError·symlink RuntimeError를 처리하고 문서화된 nonzero exit와 원문 없는 요약으로 반환한다. 이 task의 기존 0/1 계약을 검토 없이 다른 도구의 0/1/2로 바꾸라고 요구하는 finding은 아니다.

### B-P2-06 — 오류 출력에 경로와 CSS 값 원문을 그대로 싣는다

- 위치: `tools/check_aliases.py:63,82–87,161,177–179`.
- 최소 반례: runtime에 분할 생성한 식별 marker를 누락 디렉터리 이름, package 밖 import target, root/dark 사이의 다른 CSS 값에 각각 넣는다. 양 OS 모두 captured stdout/stderr에서 `marker_exposed=true`다. 실제 비밀·운영 주소는 사용하거나 출력하지 않았다.
- 원인: 전체 Path와 sorted(values)를 직접 f-string에 넣는다. 출력 전 정책 검사/비식별화가 없다.
- 영향: 입력 오류를 설명하는 과정에서 파일명·CSS 값에 든 운영 정보나 자격증명 형태가 CI 로그에 복제될 수 있다. source secret scanner가 별도라는 사실이 앞서 실행한 checker의 출력 유출을 복구하지 않는다. 실제 비밀 사고가 발생했다는 P0 주장은 아니다.
- 권고/disposition: **FIX_REQUIRED**. 경로/값을 제한 없이 echo하지 않고 규칙 ID·안전한 위치·개수로 설명한다. 직접 CLI stdout/stderr를 캡처해 synthetic secret/host 형식이 보존되지 않는 회귀를 둔다.

### B-P1-07 — weather에서 가져온 예제 값의 파일 단위 고정 출처가 빠져 있다

- 위치: `packages/tokens/examples/weather-overrides.css:1–23`, `PROVENANCE.md`.
- 원천 직접 확인: weather 고정 commit `6003da995fa4b35799f9dadc406c6ba2878bfbae`, 경로 `packages/kor-travel-weather-admin/frontend/app/tokens.css`를 Git object로 읽었다. 예제의 `--kt-` 접두를 원 이름으로 대응하면 12개 선언 모두 동일 이름/값 쌍이 원천에 존재한다. navy light/dark 8값·rail·긴 font 스택을 추출한 예제다. source 저장소는 읽기만 했다.
- 예제 헤더에는 SPDX/저작권/Modified만 있고 Origin이 없다. PROVENANCE에는 이 경로·weather 원천 행이 없다. 기존 PV-013은 map에서 가져온 tokens.css 한 파일에만 적용된다.
- 근거: licensing LIC-12/LIC-16 및 §5.2는 이식 파일의 고정 원천과 PROVENANCE 대조를 요구한다. 자체 작성 파일에 무조건 Origin을 만들라는 요구가 아니라 이번 명시적 원천 추출의 추적성 문제다.
- 영향: 다음 에이전트가 "현재 weather 값"이라는 문구를 고정 원천 없이 재사용할 수 있고 SPDX checker도 미등록 이식을 자동 발견하지 못한다. GPL 전문 미동봉이나 제3자 권리 침해가 확인됐다는 주장은 아니다.
- 권고/disposition: **FIX_REQUIRED**. 예제에 weather commit/path Origin을 추가하고 PROVENANCE에 추출·접두 변경·비배포 범위를 기록한다. README의 "현재"도 기준 commit에 연결한다.

### B-P3-08 — 설치되는 README가 alias를 아직 없는 후속 작업으로 설명한다

- 위치: `packages/tokens/README.md:14`.
- 재현: 이번 tarball은 aliases/map-vocabulary.css를 포함하고 설치 후 해당 export도 resolve되지만, 동봉 README는 별칭이 T-102에서 추가될 예정이며 이 산출물에 포함하지 않는다고 설명한다.
- 영향: package 수령자는 새 선택형 entrypoint의 존재·사용법을 문서에서 확인하기 어렵다.
- 권고/disposition: **FIX_REQUIRED 또는 명시적 문서 후속 추적**. alias가 이미 포함된 상태와 선택 import 경로, shadcn 정본을 내부 import한다는 계약을 간단히 갱신한다.

## 재현 명령과 보조 파일

모든 합성 입력은 TemporaryDirectory 안에 만들었다. marker 원문은 probe 출력이나 이 report에 싣지 않았다.

```text
git worktree add --detach F:/dev/kor-travel-common-wt/review-t102-b 8bc8179f728de88fd9327f9d4e8159188a95f9c3
py -3.14 -B -X utf8 tools/check_aliases.py packages/tokens/aliases
py -3.14 -B -X utf8 -m unittest discover -s tests -p test_check_aliases.py -v
py -3.14 -B -X utf8 -m unittest discover -s tests -p test_*.py
py -3.14 -B -X utf8 .git/codex-audit/review-t102-b-probe.py F:/dev/kor-travel-common-wt/review-t102-b
py -3.14 -B -X utf8 .git/codex-audit/review-t102-b-gates.py F:/dev/kor-travel-common-wt/review-t102-b
py -3.14 -B -X utf8 .git/codex-audit/review-t101-b-pack.py F:/dev/kor-travel-common-wt/review-t102-b
node .git/codex-audit/review-t102-b-css.cjs
git -C F:/dev/kor-travel-weather show 6003da995fa4b35799f9dadc406c6ba2878bfbae:packages/kor-travel-weather-admin/frontend/app/tokens.css
git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f 8bc8179f728de88fd9327f9d4e8159188a95f9c3
```

WSL probe/pack/gates는 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`로 같은 보조 파일을 `/mnt/f/...` 경로에서 실행했다. 유효 전체 unittest는 `review-t102-b-wsl-unittest.py`가 모든 GIT_* 환경을 제거하고 `/tmp`의 독립 사본·별도 임시 Git index에서 실행했다. 임시 index의 stage는 구체 파일 목록을 명시했으며 후보 저장소에 stage/commit하지 않았다.

gate helper는 validate_plan, validate_document_links, check_spdx, scan_secrets, check_prod_redaction, check_versions --self-check, check_aliases, git diff --check를 실행한다. pack helper의 마지막 예전 T-101 build→check→test 주입 순서는 이번 T-102 CI 검증으로 집계하지 않았다.

정상 반례 대조: 직접 --kt 선언, 직접 namespace/shadcn 중복, 단순 단독 outside import, missing import, root/dark 값 drift는 nonzero로 차단된다. 주석 안 가짜 --kt 선언은 무시된다. 빈 alias 파일·dark 블록 없는 alias는 통과하지만 이 관찰만으로 별도 finding을 추가하지 않았다. 이번 finding은 T-102에 명시된 참조/금지/충돌/경계 계약의 재현 가능한 실패에 집중했다.

## CI·한계·검증 환경 기록

- [exact PR CI 34131587507](https://github.com/digitie/kor-travel-common/actions/runs/34131587507)은 후보 head에서 6개 job success였다. Ubuntu tools job `101772745007`와 Windows tools job `101772745351` 로그의 checkout ref/SOURCE_SHA, 212 tests, 실제 check_aliases 실행·오류 0을 직접 확인했다. 이 녹색 CI가 위 추가 반례를 검증한다는 뜻은 아니다.
- `NOT_RUN`: local exact Node 22.23.1, Windows ACL 접근 거부, WSL jsonschema 2개 시험, 소비자 build/e2e·6폭 시각 비교(T-461), 실제 Release/태그 발행·npm/PyPI 게시. 소비자 원천값 일부 직접 대조는 전체 weather 채택 검증이 아니다.
- 검증 환경 사고: 최초 WSL 전체 실행은 리뷰 worktree의 GIT_DIR/GIT_WORK_TREE를 기존 fixture subprocess가 상속하여 shared source config의 core.worktree를 간접 변경했다. 즉시 parent에게 알렸고 parent가 원래 설정으로 복구했다. 이 실행은 폐기했으며 위 검증 건수·성공 근거에 포함하지 않는다. 독립 /tmp 사본에서 다시 실행한 결과만 표에 기재했다.
- source `.git/config` 시작 및 parent 복구 후 최종 SHA256은 동일한 `7689A8DF4F1D9EC7C8E237C66B66BF717375A03E248C050692CB4D4BA25A62CF`다. 후보 시작/종료 SHA/tree/clean도 동일함을 재확인했다. source config가 검토 도중 한 번도 변하지 않았다고 주장하지 않는다.

최종 **BLOCK**. 정상 fixture·pack·SPDX·CI 성공을 보존하지만, 정상 CSS 문법 및 import 분리로 필수 검사 정책을 우회하는 P1과 고정 원천 기록 누락이 남아 있다.
