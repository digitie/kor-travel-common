# T-301 post-fix 독립 적대적 리뷰 B 원본 evidence

- Review ID: `T301-20260909-B-post-fix`
- 실행 ID: `T301-B-postfix-20260909-1107`
- 실행 시각: 2026-09-09 10:35~11:09 (Asia/Seoul)
- 검토자: B (문서 규약·계획·생성물·계약)
- candidate commit: `fedf7f8cbad55302183708aa4c9dd514ffba466d`
- candidate tree: `e40c59e99eb367fb79893587e7dbd7489a7d2ff8`
- base commit: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- base tree: `3eddd2ad90d10813bb37cd00f5ac9be5a1ef13ba`
- candidate worktree: `F:/dev/kor-travel-common-review-b-t301-postfix` (detached during review)
- manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-manifest.md`
- manifest SHA256: `b04e93badcd6cb8b7aa0312e2eb998980aea02e6de3a35d582a424eb78d90c6e`
- 최초 reviewer A/B report와 통합 report는 읽지 않았다. candidate에 있던 기존 evidence의 내용도 읽지 않고, 현재 코드·정본·manifest만 대조했다.

## 기준선·범위

`git merge-base --is-ancestor afc8d1bf166d0ddcbee059252eb5cee245157dcd fedf7f8cbad55302183708aa4c9dd514ffba466d`가 exit 0이고 candidate SHA/tree가 manifest와 일치했다. evidence 파일을 쓰기 전 `git status --porcelain=v1 --branch`는 `## HEAD (no branch)`만 출력해 candidate tree가 clean이었다. base 대비 전체 diff와 post-fix 기능 delta를 읽었으며, 상대 reviewer의 결과는 사용하지 않았다.

검토 대상은 `tools/openapi_exceptions.py`, `tests/test_openapi_exceptions.py`, `docs/standards/openapi.md`, YAML 정본·생성 Markdown, ADR-009/D-14/T-301 문서 계약, task provenance·SHOULD 외부 계약 예외, parser fail-closed 경계, 생성 Markdown 안전성, 날짜·원자 출력·alias, 색인·resume·journal의 실행 수치다.

## 검증 명령과 결과

모든 명령은 candidate worktree 루트에서 실행했다.

| 명령 | exit | 결과 |
|---|---:|---|
| `git rev-parse HEAD` / `git rev-parse 'HEAD^{tree}'` | 0 | candidate SHA/tree 일치 |
| `git merge-base --is-ancestor <base> HEAD` | 0 | base 선행 관계 확인 |
| `git diff --check <base> HEAD --` | 0 | 공백 오류 없음 |
| `python -B -X utf8 tools/openapi_exceptions.py --check` | 0 | 예외 39건·Markdown 54줄, drift 없음 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | 0 | focused 20 tests 성공, 1.060초 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q` | 0 | 전체 357 tests 성공, 306.442초 |
| `python -B -X utf8 tools/validate_document_links.py .` | 0 | 527 documents / 2582 local targets, errors=0 |
| `python -B -X utf8 tools/validate_plan.py --root .` | 0 | 상세 task 106, 오류=0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | 0 | 70개 파일, 오류=0 |
| `python -B -X utf8 tools/check_prod_redaction.py --root . --patterns .prod-redaction-patterns --all` | 0 | 678개 파일, 발견 0건 |
| `python -B -X utf8 tools/scan_secrets.py --root . --patterns .secret-scan-patterns --all` | 0 | 678개 파일, 발견 0건 |
| `npm ci --ignore-scripts --no-audit --no-fund` | 0 | 전체 test 준비 성공; 선언 Node 22 대비 실행 Node 25라 EBADENGINE 경고 |
| escaped pipe를 고려한 OpenAPI 표 구조 검사 | 0 | 39행, 모든 행 7열, M10은 `교차 저장소 MUST` |
| `gh pr checks 22 --repo digitie/kor-travel-common` | 0 | PR checks 모두 pass; run `34301155628`/`34301156038`의 docs/tools(ubuntu·windows)·packages·secret-scan·check-versions·fixture jobs 확인 |

## post-fix closure 대조

- 최초 B provenance 대상은 현재 YAML 39건 모두 정합 task ID를 갖고, focused test가 누락·미정의 ID를 거부하는 것으로 재현했다.
- 최초 B SHOULD 예외 대상은 현재 `geo S1`과 concierge features export `S1/S2` 3건만 남아 있고 모두 구체적 표면·외부 계약·동반 PR 근거를 갖는다. `surface: "*"`인 S 예외는 없다.
- 최초 B plain numeric·제어 문자·surrogate 대상은 decimal numeric, 제어 문자, lone surrogate 회귀 시험이 추가되어 현재 정상 입력과 공격 입력이 모두 의도대로 처리된다. 다만 아래 B-P2-02의 YAML 숫자 표기 일부는 남아 있다.
- 최초 B 표 회귀 대상은 현재 7열 표 3개, 39행, core ID와 M10 tier를 검사하는 test가 추가되어 통과했다.
- parser quote escape, Markdown HTML/링크/표시 문자 escape, input/output 동일 파일·hardlink alias 차단, atomic temporary write, 미래 `updated` 차단, 기존 output 보존 공격은 focused test와 직접 실행으로 통과했다.

## Findings

### B-P1-01 — task·resume·journal evidence가 post-fix 정본 수치와 stale

- 심각도: P1
- 위치: `docs/tasks/T-301-openapi-standard.md:73-76`, `docs/resume.md:11`, `docs/journal.md:7-9`
- 재현: 현재 정본을 `python -B -X utf8 tools/openapi_exceptions.py --check`로 실행하면 `예외 39건·Markdown 54줄`, focused suite는 `Ran 20 tests`를 출력한다. 그러나 상세 task는 46건·61줄·8 tests를, resume는 46건·8개 회귀 시험을, 최신 T-301 journal 항목은 46건·61줄·8개를 계속 선언한다.
- 영향: 다음 작업자가 task evidence와 실제 생성물·시험 결과를 혼동하고, post-fix closure를 immutable candidate에 연결할 수 없다. 문서 링크 gate가 통과해도 감사 수치·완료 판단이 정본과 충돌한다. 실제 실행한 357 full tests, 527/2582 link, 678 redaction 등 closure 결과도 T-301 기록에 없다.
- 권고/disposition: post-fix candidate SHA/tree, 실행 ID, 39/54/20 및 full/link/plan/SPDX/redaction/secret/CI 결과를 task·resume·journal에 최신 항목으로 기록하고 reviewer B evidence와 통합 report 링크를 연결한다. 이전 46/61/8 문장은 역사 기록임을 표시하거나 correction으로 분리한다. `OPEN`; P1이므로 `BLOCK`.

### B-P2-02 — YAML plain non-string 차단이 모든 숫자·timestamp 표기를 포괄하지 않음

- 심각도: P2
- 위치: `tools/openapi_exceptions.py:44-48,259-261`, `tests/test_openapi_exceptions.py:96-100`
- 재현: canonical YAML의 첫 `owner: kor-travel-geo`를 임시 입력에서 다음 값으로 바꿔 `load_registry(..., as_of=date(2026, 9, 9))`를 실행하면 모두 exit 0으로 문자열로 수용된다: `0x10`, `0o10`, `0b10`, `0123`, `2026-09-06T00:00:00Z`. 현재 정규식은 decimal·일부 float/date/time만 거부하고 YAML의 hexadecimal/octal/binary/leading-zero/timestamp 형태는 놓친다.
- 영향: 도구 docstring의 “문자열·null subset” 및 fail-closed 계약과 달리, 문자열 필드에 YAML 숫자·timestamp scalar를 무인용으로 넣어도 통과한다. 생성 Markdown·후속 매니페스트에 schema 의미가 조용히 달라질 수 있다. 현재 canonical 값은 정상이며 merge 안전 경계를 직접 깨지는 P2다.
- 권고/disposition: 지원할 YAML scalar grammar를 명시하고 숫자·timestamp로 해석되는 모든 plain 형태를 reject하거나, 문자열 입력은 모두 quote로 강제한다. YAML 1.1/1.2 경계(0x/0o/0b/leading zero/시간대 포함 timestamp)와 회귀 시험을 추가한다. `OPEN`.

### B-P2-03 — task ID 검사가 실제 task 파일 존재를 보장하지 않음

- 심각도: P2
- 위치: `tools/openapi_exceptions.py:389-399,439-443`
- 재현: `_task_ids()`는 `docs/tasks.md`와 모든 `docs/tasks/T-*.md` 본문의 문자열을 수집한다. 현재 `ids - task filename IDs`가 `T-034`, `T-035`, `T-308a`, `T-356`으로 출력된다. canonical 첫 entry의 reason에 `T-483` 대신 `T-034`를 넣은 임시 YAML도 `load_registry()`가 exit 0으로 수용한다. `T-034`는 task 본문에서 언급될 뿐 common `docs/tasks/T-034-*.md` 파일이 없다.
- 영향: “정의된 task ID” 검사가 문서 본문의 임의 참조를 task 정본으로 오인한다. 잘못된 후속 task·소비자 task ID를 reason에 넣어도 validator가 통과시켜 provenance closure가 다시 흔들릴 수 있다.
- 권고/disposition: common task 정본은 `docs/tasks/T-*.md` 파일명에서만 수집하고, consumer task ID를 허용해야 한다면 별도 namespace/source 필드와 존재성 gate를 명시한다. 파일명·정본 ID가 없는 ID는 fail해야 한다. `OPEN`.

## P0/P1/P2/P3 집계와 미실행

- 신규/잔여 P0: 0건
- 신규/잔여 P1: 1건 (`B-P1-01`)
- 신규/잔여 P2: 2건 (`B-P2-02`, `B-P2-03`)
- 신규/잔여 P3: 0건. 표 7열·M10 분류 회귀는 현재 test와 직접 구조 검사로 닫혔다.
- 7개 소비자 저장소의 실제 OpenAPI export/build/e2e, pinvi Zod 대조, map 산출물 변경과 pinvi·ktdm SHA256 동반 PR은 `NOT_RUN(외부 저장소/후속 T-480~T-486)`이다.
- GitHub Actions는 PR checks 상태만 읽었고 원격 재실행·actionlint는 `NOT_RUN`; npm/PyPI 게시·GitHub Release 업로드도 `NOT_RUN`이다.

## 최종 판정

`BLOCK` — P1 1건과 P2 2건이 남았다. stale evidence를 최신 수치·candidate/tree·실행 ID로 갱신하고, plain scalar 및 task 정본 존재성 경계를 보강한 post-fix candidate에서 B가 독립 재검토해야 한다.
