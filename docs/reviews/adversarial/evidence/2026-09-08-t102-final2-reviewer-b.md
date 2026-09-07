# T-102 final2 독립 적대적 리뷰 B

- 실행 ID: `T102-FINAL2-B-20260908-001711`.
- 요청: 최종2 후보 `ded1631b81d464ed919d36d73ab9c2a1111d38f4`만 대상으로 공통 manifest·구현을 읽고 이전 B-P1-12/B-P2-13/B-P1-14와 누적 finding을 재현한다. @media/@supports/부모 selector, both 중복, 비ASCII 정의/참조, escape/8.3/redaction/import/radius/dark shadow를 확인한다. detached clean에서 후보·소비자 수정·commit/push 금지, reviewer A 결과 미열람, raw·SHA256·verdict 보고.
- 시작 KST: `2026-09-08T00:17:11.0689647+09:00`.
- 검증 종료 KST: `2026-09-08T00:20:41.5759041+09:00`.
- 시작/종료 SHA: `ded1631b81d464ed919d36d73ab9c2a1111d38f4`.
- 시작/종료 tree: `41dd1c6551994b62d94a04c8a3c1f8bf98414de7`.
- 전체 base: `843c404d79fd748cf6f8e40ce3e385fcabb0179f`. 이번 delta base: `09162025140991d24775abc76571f35de9974022`.
- 격리: `F:/dev/kor-travel-common-wt/review-t102-final2-b`, 새 detached worktree. 시작/종료 `git status --porcelain=v1` 빈 출력.
- 전체 unittest·gate는 후보를 Windows 임시 디렉터리/WSL `/tmp` 독립 사본에 복사하고 모든 `GIT_*` 자식 환경을 제거하여 실행했다. 별도 사본의 `.git`만 초기화/index 작성했다. pack/install도 임시 사본이며 source/candidate/소비자 파일을 수정하지 않았다.
- source `.git/config` 시작/종료 SHA256은 `7689A8DF4F1D9EC7C8E237C66B66BF717375A03E248C050692CB4D4BA25A62CF`로 동일하다.
- 공통 manifest: `docs/reviews/adversarial/evidence/2026-09-08-t102-final2-manifest.md`, 읽은 파일 SHA256 `FF9228051138BDC6FE63F9D10081871F8E7B86E679EF15470D78A325346906EA`.
- 독립성: 상대 reviewer 보고서 본문·판정을 읽거나 요청하지 않았다. 과거 raw 보존은 byte hash만 계산했다. 이 원본은 parent에게 다른 reviewer와 공유하기 전에 독립 확정했다.

## 최종 판정

**PASS**. 누적 B finding 14건의 구체 반례는 모두 FIXED이며, 이번 6파일 delta 및 관련 공개 계약 재검토에서 새로운 P0/P1/P2/P3 finding은 0건이다. 이 판정은 T-102 common 후보 범위에 한정되며 소비자 채택·화면 diff·registry 발행 완료를 뜻하지 않는다.

## 실제 실행

helper는 모두 기본 checkout `.git/codex-audit/`에만 존재하는 reviewer 검증 코드다. `<candidate>`는 위 detached 후보의 OS별 절대 경로다. Windows 접두사는 `py -3.14 -B -X utf8`, WSL은 `wsl -d Ubuntu-26.04 -- bash -lc` 내부의 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`다.

| 실행 명령 | Windows 결과 | WSL 결과 |
|---|---|---|
| `review-t102-b-wsl-unittest.py <candidate>` → 독립 사본의 `-m unittest discover -s tests -p test_*.py` | exit 0, 238 tests 통과·skip 0, 62.812초 | exit 0, 238 수집 중 235 통과·3 skip, 16.873초 |
| `review-t102-post-b-gates.py <candidate>` → focused `test_check_aliases.py` | 35 통과·skip 0 | 34 통과·Windows 전용 1 skip |
| `tools/validate_plan.py` | 106 tasks, 오류 0 | 동일 |
| `tools/validate_document_links.py` | 376 문서·2333 targets, 오류 0 | 동일 |
| `tools/check_spdx.py` | 45 파일, 오류 0 | 동일 |
| `tools/scan_secrets.py --all` | 491 파일, 발견/예외 0 | 동일 |
| `tools/check_prod_redaction.py --all` | 491 파일, 발견/예외 0 | 동일 |
| `tools/check_versions.py --self-check` | exit 0 | 동일 |
| `tools/check_aliases.py packages/tokens/aliases` | CSS 1개, 오류 0, exit 0 | 동일 |
| `review-t102-b-probe.py <candidate>` | 기존 27종 CLI 실행 | 동일 |
| `review-t102-post-b-probe.py <candidate>` | escape·문자열·합동 selector 등 11종 재현 | 동일 |
| `review-t102-post-b-redaction.py <candidate>` | 합성 민감 relative target/identifier 2종 모두 미노출 | 동일 |
| `review-t102-post-b-short.py <candidate>` | GetShortPathNameW 실제 별칭·samefile true, long/short 모두 exit 0 | Windows API 전용 |
| `review-t102-final-b-probe.py <candidate>` | mode/Unicode/중복 경계 11종 재현 | 동일 |
| `review-t102-final2-b-positive.py <candidate>` | 정상 Unicode/합동 selector·잘못된 이름/colon 7종 실행 | 동일 7종 실행, 뒤 Git metadata 단계는 아래 한계에 별도 기록 |

- `git diff --check 843c404d79fd748cf6f8e40ce3e385fcabb0179f HEAD`: exit 0, 출력 없음.
- `gh run view 34137474603 --json headSha,status,conclusion,jobs`: headSha가 정확히 `ded1631b81d464ed919d36d73ab9c2a1111d38f4`; completed/success. [exact CI](https://github.com/digitie/kor-travel-common/actions/runs/34137474603)의 docs·tools Ubuntu·tools Windows·secret-scan·check-versions·packages 6개 job 모두 성공을 직접 확인했다.
- `review-t101-b-pack.py <candidate>`를 양 OS에서 새로 실행했다. `npm ci --ignore-scripts --no-audit --no-fund`, build 전 check → build → check, Node tests 7개·skip 0, `npm pack`, 빈 프로젝트 tgz 설치, concrete exports 14개 resolve 및 tokenValues 44개 import 모두 성공했다.
- Windows Node 25.9.0/npm 11.12.1은 engine 경고가 있는 추가 실행이다. WSL Node 22.22.2/npm 11.19.1에서도 성공했다. 로컬 Windows를 정본 Node 실행으로 표시하지 않는다.
- tarball 19개 파일, alias CSS 포함·examples 제외·LICENSE/NOTICE/THIRD_PARTY_NOTICES 포함, LICENSE bytes는 repo와 일치했다. Windows tgz SHA256 `725fd590b9bcbd361b9a798aaa99187cf86812ecba64004e110adeee9686c409`; WSL `4a6cde260c32248d10a6bfc51fe6e14e265c6295bb8967fa5cda2024a17a487a`. 이는 임시 검사 산출물이며 설치 뒤 제거했다.
- helper의 추가 생성물 drift 주입은 build 전 check exit 1로 탐지됐다. 이후 build의 생성물 복구 결과를 전체 CI 성공과 혼동하지 않았다.

## 핵심 수정 반례와 정상 대조

기준 fixture는 tokens.css에 `--kt-brand:red`, 정상 theme/shadcn을 둔다. 아래 CSS를 aliases/map.css로 저장하고 후보 `check_aliases.py`를 호출했다.

| 입력 | 수정 전 관찰 | 이번 Windows/WSL 관찰 |
|---|---|---|
| `@media(max-width:1px){:root{--brand:var(--kt-brand)} .dark{--brand:var(--kt-brand)}}` | exit 0 | exit 1, mode 밖·root/dark 누락 |
| 같은 두 블록을 `@supports(display:impossible)`로 감쌈 | exit 0 | exit 1 |
| 같은 두 블록을 `.shell{...}`로 감쌈 | exit 0 | exit 1 |
| `:root,.dark{--brand:var(--kt-brand)} :root{--brand:var(--kt-brand)}` | exit 0 | exit 1, root 중복 |
| 두 번째 블록을 `.dark`로 변경 | exit 0 | exit 1, dark 중복 |
| 양 모드에 `--kt-한글:blue` 추가 | exit 0 | exit 1, --kt 정의 금지 |
| 양 모드에서 정본에 없는 `var(--kt-한글)` 사용 | exit 0 | exit 1, 미정의 참조 |
| 단일 `:root,.dark` 또는 `.dark,:root` | 정상 대조 | exit 0 |
| 정본에 정의된 `--kt-한글`을 `--별칭`에서 참조 | 정상 대조 | exit 0 |
| 한국어 문자열/주석 속 미정의 var 텍스트 | 정상 대조 | exit 0 |
| 잘못된 `--:red` 또는 `--brand red` | 구조 오류 대조 | exit 1, traceback 없음 |

`_scope`가 전체 stack 깊이 1만 인정하고, both identity를 root/dark로 펼치며, custom property/var 이름을 Unicode까지 소비하는 수정이 실제 반례 결과와 일치했다. escape 지원 범위를 넓히지 않고 명시적 거부를 유지한 것도 확인했다.

## 누적 B disposition

| ID / 원 심각도 | 판정 | 재확인 근거 |
|---|---|---|
| B-P1-01 / P1 | FIXED | 마지막 세미콜론·VAR·문자열/주석·escaped 정의/함수/참조 corpus, 정상 대조 통과 |
| B-P1-02 / P1 | FIXED | escaped at-keyword 거부, one-line/url/media/복수 import·외부 경계 거부 유지 |
| B-P1-03 / P1 | FIXED | recursive helper 금지 --kt/theme/shadcn/중복 반례 탐지 유지 |
| B-P2-04 / P2 | FIXED | 필수 tokens 외부/self symlink 제어 오류 |
| B-P2-05 / P2 | FIXED | alias UTF-8/누락/self/read failure 제어 오류·traceback 없음; Windows ACL 한계는 별도 |
| B-P2-06 / P2 | FIXED | relative import/identifier의 합성 민감 패턴 stdout/stderr 미노출 |
| B-P1-07 / P1 | FIXED | weather Origin/PV-014/Modified/GPL 고지 불변 확인 |
| B-P3-08 / P3 | FIXED | README의 aliases·비배포 예제 설명과 실제 tarball 일치 |
| B-P1-09 / P1 | FIXED | 실제 Windows 8.3 경로 재현 성공, exact Windows CI 성공 |
| B-P2-10 / P2 | FIXED | 단일 combined selector 정상 통과 |
| B-P2-11 / P2 | FIXED | 지정 raw attribute·해시 보존 유지, 전체 base diff-check 성공 |
| B-P1-12 / P1 | FIXED | @media/@supports/부모 selector 세 반례 exit 1, top-level 양 모드 정상 통과 |
| B-P2-13 / P2 | FIXED | both+root/both+dark 중복 각각 exit 1, 정상 both exit 0 |
| B-P1-14 / P1 | FIXED | Unicode 금지 정의/미정의 참조 exit 1, 정의된 Unicode 참조·주석·문자열 정상 통과 |

신규 finding: P0 0 / P1 0 / P2 0 / P3 0. 미해결 B finding 0.

## 전체 delta·문서·출처 확인

- 이번 delta는 checker·tests, 지정 B raw attribute, 이전 확정 raw A/B·final2 manifest 총 6파일이다. package 공개 API/CSS·workflow·versions·PROVENANCE·T-102 task는 `git diff --name-only 0916202 HEAD -- ...` 빈 출력으로 불변을 확인했다.
- radius/dark shadow는 직전 후보에서 읽기 전용으로 고정 weather source와 대조한 결과를 동일 파일이라는 근거로 재사용했다. map shim의 radius-md control, weather 예제의 panel 재선언·light shadow 상속, 예제 spacing 8개 앱 소유·미배포, GPL/PV-014는 변경되지 않았다. 실제 소비자 시각 diff를 실행한 것으로 세지 않는다.
- package/CI 실물은 새로 pack/install·exact CI를 실행했다. templates·소비자 파일·publish 설정으로 범위가 번지지 않았다.
- Windows에서 이전 final A/B raw의 Git blob SHA256과 checkout SHA256을 계산해 manifest와 일치를 확인했다. A `AC38FE23D924EB8AA1F2B7987116ADB6731607C246A6AFD7D36B2B17C4679C5C`, B `DEACCAED247797E78B87677C212B7DC316DE2F43D46E2A4D9A036590DF5F0A79`. 본문을 표시하거나 판정을 읽지 않았다. `.gitattributes` 예외는 해당 B 원본 파일 한 곳에 한정된다.
- manifest의 선행 로컬 건수와 exact 후보의 이번 건수를 혼합하지 않았다. 이번 manifest 추가 후 실제 검사는 문서 376개·파일 491개다.

## 한계 / NOT_RUN

- WSL은 Windows 8.3 전용 test 1개 skip, jsonschema 미설치로 schema parity 2개 `NOT_RUN`. 238 전부 통과로 세지 않았다. Windows에서는 전체 238·skip 0이며 실제 short spelling도 별도 생성해 성공했다.
- Windows 실제 ACL 읽기 거부: `NOT_RUN(chmod는 Windows ACL 의미가 아님)`. Linux chmod 거부와 양 OS UTF-8/누락/symlink 오류는 실행했다.
- `review-t102-final2-b-positive.py` WSL 실행에서 7개 CLI case는 모두 기대 결과를 출력한 뒤, Windows 형식 `.git` 포인터를 Linux git이 읽지 못해 hash metadata 단계가 exit 128로 실패했다. 이는 후보 checker 오류가 아니라 reviewer helper의 마지막 read-only metadata 단계다. 그 단계는 WSL 성공으로 세지 않았고 Windows Git blob/checkout 해시 검증으로 확인했다. source config를 고치거나 환경을 상속시키는 우회는 하지 않았다.
- 브라우저 CSS 의미 자체는 변경이 없어 직전 Windows Chromium 대조를 재사용했다. 이번에 새 브라우저/소비자 화면 실행은 `NOT_RUN`이다.
- 소비자 build/e2e/6폭 diff: `NOT_RUN(T-461 등 소비자 task)`; npm/PyPI·Release/tag 게시: `NOT_RUN(사용자 범위 밖)`. 소비자 저장소를 쓰거나 common을 발행하지 않았다.
- PASS는 이 immutable common 후보의 검토 범위에 한정한다. 다음 task 구현·소비자 채택·릴리스 승인은 별도 gate다.
