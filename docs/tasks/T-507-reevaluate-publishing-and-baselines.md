# T-507 재평가: Renovate·Vitest 5·Node 24/26·react-table 9·lucide 1.x·mypy 2·TS 7 → `versions.json` 갱신

- 상태: BLOCKED
- 우선순위: P3
- Gate: 문서·도구 테스트
- 선행: T-005
- 외부 선행: 2026-12 재평가 시점의 공식 버전·peer·소비자 evidence가 필요하다. 미래 결과를 현재 조회로 대신하지 않는다.

## 목표

Phase 0에서 의도적으로 보류한 7개 항목을 정해진 시점(airport TS 예외 `until` 2026-12 도래)에 사실 재조사 → 판정 → `versions.json` `floor`/`recommended`/`exceptions` 갱신 PR로 닫는다. 결정이 ADR-008(버전 정책)을 바꾸면 새 ADR로 supersede한다. npm/PyPI 게시는 사용자 지시와 ADR-014로 재평가 범위에서 제외했다.

## 고정 결정

- 2026-09 기준선과 보류 항목: Node 24/26 승격은 Phase 5(T-507), react-table 9는 breaking 미조사, lucide 0.363~1.41 혼재(ui는 인라인 SVG로 peer 회피), Vitest 4.1 floor, mypy 1.13 floor: 브리프 D-06·D-01, [versions 규칙](../standards/versions.md), ADR-008([ADR 색인](../adr/README.md)).
- TS 기준선 5.9.3 + airport 7.0.2 예외(`until`: typescript-eslint peer 확장 또는 2026-12 재판정): 브리프 O-6.
- Renovate는 Phase 5(T-507)에서 재평가한다. 미확인 상태에서는 `templates/dependabot.yml`을 유지한다(브리프 D-07·O-18). npm/PyPI 미게시·이름 확정은 [ADR-014](../adr/014-common-implementation-without-registry-publishing.md)를 따른다.
- `versions.json`은 2인 리뷰 비면제(D-04); 태그 불변·같은 버전 재발행 금지(D-11)는 유지한다.
- 근거: `docs/survey/cross/version-matrix.md` §4.2~4.4(2026-09-06 최신값: Node 26.8.1/24.20.0/22.23.2, vitest 5.0.0 engines `^22.12`, typescript-eslint peer `<6.1.0`, react-table 9.2.4, lucide 1.41.0, mypy 2.3.1, npm 12.0.2), §7.4·열린 질문 12·13(Renovate 미확인, breaking 미조회), `docs/survey/cross/backend.md` §5.2(배포 채널 후보 A~D), 선행 보고서 §8(GitHub Packages 인증 제약; `docs/survey/README.md` §2.2 참조).

## 구현 범위

1. 재평가 문서 `docs/plan/reevaluation-2026-12.md`: 항목별 (2026-09 결정·현재 값·최신 값·breaking 요약·peer/engines 제약·소비자 영향·판정 `채택/보류/거부`·근거 URL+버전+조회일).
2. 항목: ① Renovate 설치 가능 여부(설치 가능하면 `templates/renovate.json` preset 초안, 아니면 dependabot 유지) ② Vitest 5(engines·vite peer; ui 하네스 영향) ③ Node 24/26(Active LTS 전환일·동봉 npm·이미지 digest 7곳) ④ react-table 9(DataTable `manualSorting` 계약 영향) ⑤ lucide 1.x(ui 인라인 SVG이므로 소비자 정렬 축으로만) ⑥ mypy 2(strict 베이스 영향) ⑦ TS 7(typescript-eslint peer·Next `useTypeScriptCli`; airport 예외 해제 또는 `until` 연장).
3. `versions.json` 갱신 PR: `floor`/`recommended` 상향, `exceptions[].until` 갱신, 필요 시 `blocked[]`. 7 소비자 report 재실행으로 신규 `BELOW_FLOOR`가 0이거나 예외로 등록됐음을 확인.
4. `tests/test_check_versions.py` 갱신(새 floor에 대한 fixture).

## 범위 밖

- 소비자 저장소 업그레이드 PR(각 앱 T-4xx 또는 신규 task).
- npm/PyPI 게시·게시 재평가·이름 확보(사용자 지시로 제외).
- PostgreSQL/PostGIS major(별도 트랙, D-06).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/plan/reevaluation-2026-12.md          (신설)
versions.json                              (floor/recommended/exceptions/blocked)
docs/standards/versions.md                 (정책 의미 변경 때만; 숫자 정본은 versions.json)
tests/test_check_versions.py
templates/renovate.json                    (Renovate 채택 시만)
docs/adr/<다음-번호>-<slug>.md, docs/adr/README.md (버전 정책 결정이 바뀔 때만)
CHANGELOG.md, docs/journal.md, docs/resume.md, docs/tasks/T-507-reevaluate-publishing-and-baselines.md
```

## 수용 기준

- 7개 항목 모두 판정과 근거(공식 URL·버전·조회일)가 있고, 미조회 항목은 `미확인`으로 표기해 판정을 `보류`로 둔다.
- `versions.json` 변경 뒤 `tests/test_check_versions.py`가 통과하고, 7 소비자 report에서 신규 `BELOW_FLOOR`·`EXEMPT_EXPIRED`가 0이거나 `exceptions[]`에 `until`·`reason`과 함께 등록돼 있다.
- TS 7 항목에 typescript-eslint peer 범위 확인 결과가 있고 airport 예외가 해제되거나 `until`이 갱신됐다.
- Renovate 항목에 설치 가능 여부 확인 방법(조직/개인 계정)과 결과가 있다.
- 2인 리뷰 report가 [review archive](../reviews/README.md)에 있고 `CHANGELOG.md`에 기준선 변경 항목이 있다.
- 두 validator가 통과한다.

## 검증 명령

```bash
npm view typescript-eslint peerDependencies.typescript && npm view vitest engines.node && npm view @tanstack/react-table version && npm view lucide-react version
curl -s https://endoflife.date/api/nodejs.json | python3 -c "import json,sys; [print(r['cycle'], r.get('lts'), r['eol']) for r in json.load(sys.stdin)[:4]]"
uv pip index versions mypy 2>/dev/null || python3 -m pip index versions mypy
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_versions.py"
for m in <consumer-checkout>/*/kor-travel-common.lock.json; do python3 -B -X utf8 tools/check_versions.py --registry versions.json --manifest "$m" --mode report; done
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

조회 결과는 조회일과 함께 재평가 문서에 옮겨 적는다. Git Bash에서 동일하게 실행한다.

## evidence

- 재평가 문서 §"조회 로그"에 명령·출력 요약·조회일. `docs/journal.md` 최신 항목에 도구 버전·NOT_RUN 목록.
- `versions.json` PR 본문에 7 소비자 report 요약 표(판정 어휘별 건수).

## rollback 또는 release 차단 조건

- `versions.json` 갱신으로 소비자 report에 예외 미등록 `BELOW_FLOOR`가 생기면 PR을 merge하지 않는다. merge 후 발견되면 `git revert` 1회로 되돌린다.
- npm/PyPI 게시를 이 task의 조사 결과로 재개하지 않는다. 새 사용자 지시와 별도 ADR이 필요하다.
- Renovate 설치가 확인되지 않으면 dependabot 템플릿을 유지하고 preset 파일을 만들지 않는다.
