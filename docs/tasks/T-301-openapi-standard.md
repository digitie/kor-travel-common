# T-301 docs/standards/openapi.md 확정 + `openapi-exceptions.yaml` 초기 등록 + 헤더·X-Request-ID 형식 규칙

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 2인 리뷰
- 선행: 없음

## 목표

7개 FastAPI 백엔드가 에러 본문 7종·페이지네이션 4형·health 경로 4형·요청 ID 정책 4형으로 갈라져 있고 그 불일치가 저장소 간 sha256 pin 비용으로 이미 나타난다([oa §3.5](../survey/cross/openapi.md)). 이 task는 조사 [oa §3](../survey/cross/openapi.md)의 M1~M9 / S1~S13 / N1~N8을 D-14의 3계층으로 배치한 규칙 정본 `docs/standards/openapi.md`를 확정하고, 기존 표면의 위반을 `docs/standards/openapi-exceptions.yaml`에 초기 등록하며, 헤더 이름·`X-Request-ID` 형식 규칙을 문서화한다. 이번 PR 산출물은 "정본 초안"이며 T-303(export CLI)·T-304(health)·T-308(problem) 실물과 대조해 확정하는 후속이 남는다(브리프 §7).

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(3계층·예외 레지스트리·`X-Request-ID` 형식·헤더 형식 규칙·map 산출물 pin 동반), D-22(AppId·메트릭 접두는 앱 소유), D-25(NOT_RUN). ADR-009 — [ADR 색인](../adr/README.md).
- 3계층 배치: 즉시 MUST(additive, 응답 본문 불변) = M2·M4·M9·N6·N7. 신규 표면 MUST / 기존 표면 SHOULD + 예외 등록 = M1·M3·M5·M6·M7·M8·N1~N5·N8. SHOULD = S1~S13. 규칙 ID는 조사 번호를 유지한다.
- 예외 레지스트리 항목 스키마 `{app, rule, surface, reason, sunset|null, review, owner}`. 초기 등록: geo v1(VWorld 호환)·geo v2 envelope(`query_id`↔`request_id`)·geo `/v1/healthz` 별칭(무기한)·geo 검증 오류 400·pinvi `{error:{}}`·비버저닝 경로·concierge `/api/v1`·`{detail}`·features export(map provider 외부 계약)·ktdm `/api/v1`·`{detail}`·airport 스펙 422 불일치·map `starlette<1.0`(근거: [oa §2.5·§2.10·§4](../survey/cross/openapi.md)). SHOULD는 소비자 매니페스트에 기록하고 외부 계약 표면만 레지스트리에 둔다.
- 검증 오류 422 기본·geo 400 예외. 429 코드 사전은 common 기본 `TOO_MANY_REQUESTS` + 앱 덮어쓰기 — **열림(O-14, 사용자 확인 필요)**, 기본값으로 진행.
- `X-Request-ID`: UUID v4/v7 또는 ULID, ≤128자 ASCII, 검증 실패 시 서버 발급, `trust_incoming=False`는 앱 옵션(ktdm 근거 [be §2.3](../survey/cross/backend.md)). 헤더 이름은 형식 규칙만 `X-<AppId>-Api-Key|Service-Token|Actor|Admin-Proxy-Secret|Ops-Token|Ops-Scope`, AppId(풀네임/약어)는 앱 소유([inv/map §8-18](../survey/inventory/kor-travel-map.md)).
- 프론트 typegen: `openapi-typescript` 7.x 단일 버전, `gen:types`/`gen:types:check`; pinvi Zod 이중 유지는 "OpenAPI↔Zod 일치 테스트"(O-14 기본값). 재사용 워크플로는 T-309.

## 구현 범위

1. `docs/standards/openapi.md`: 머리 1문장(정본 초안, T-303·T-304·T-308 대조 후 확정) → 적용 범위·용어 → 규칙 표(ID·계층·문장·근거 앱·검사 수단·예외 여부) → 헤더 형식 규칙 절 → `X-Request-ID` 형식·발급 규칙 절 → 검증 오류·429·health 경로 규칙 절 → 예외 레지스트리 사용법·review 주기 → typegen 규약 절 → 관련 task·도구 링크.
2. `docs/standards/openapi-exceptions.yaml`: 위 초기 등록 항목을 스키마대로 기록(`review` 필수, `sunset`은 `null` 허용).
3. 예외 레지스트리의 사람이 읽는 표 `docs/standards/openapi-exceptions.md`를 yaml에서 생성하는 `tools/openapi_exceptions.py`(`--check`로 생성물 drift 검사). D-03(Windows·stdlib) 제약 때문에 PyYAML을 쓰지 않고 "flat mapping 목록" 서브셋만 파싱한다 — 후보이며 리뷰에서 "생성 md 수기 유지 + 대조 검사"로 바꿀 수 있다.
4. `docs/standards/README.md` 색인 행(standards-fe 소유자와 합의)과 `docs/survey/README.md` §6.2 정정값(airport 21 paths, readiness `/readyz`) 인용.

## 범위 밖

export CLI·`--check`·profile 콜백 구현(T-303), health 라우터·time(T-304), problem+json 핸들러·request-id 미들웨어 코드(T-307·T-308), `openapi-drift.yml`·`typegen-drift.yml`(T-309), 각 앱의 예외 해소 PR(T-480~T-486), 헤더 AppId 통일(앱 소유), geo v2 problem+json 채택 시점(geo ADR-060 묶음, O-14).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/standards/openapi.md
docs/standards/openapi-exceptions.yaml
docs/standards/openapi-exceptions.md        # 생성물(후보)
tools/openapi_exceptions.py                 # yaml → md 생성 + --check(후보)
tests/test_openapi_exceptions.py            # 파서·drift 회귀(후보)
docs/standards/README.md                    # 색인 행(standards-fe 소유자와 합의)
```

## 수용 기준

- [ ] `openapi.md`의 규칙 표에 M1~M9·S1~S13·N1~N8 30개 전부가 있고, 각 행에 계층(즉시 MUST / 신규 MUST·기존 SHOULD / SHOULD / MUST NOT)·근거 앱·검사 수단·예외 여부 열이 채워져 있다.
- [ ] 즉시 MUST 5개(M2·M4·M9·N6·N7)는 "응답 본문 불변(additive)"임이 규칙 문장에서 확인된다.
- [ ] `openapi-exceptions.yaml`의 모든 항목이 `{app, rule, surface, reason, sunset, review, owner}` 7키를 갖고, `reason`이 실제 task 원장의 `T-NNN`을 포함하며, `rule`이 규칙 표의 ID와 일치하고, 외부 계약 SHOULD만 구체 surface로 등록되어 있다.
- [ ] `X-Request-ID` 절에 형식(UUID v4/v7·ULID·≤128자 ASCII)·실패 시 서버 발급·`trust_incoming` 옵션이 있고, 헤더 형식 절에 6종 접미와 "AppId는 앱 소유"가 있다.
- [ ] 429 코드 사전과 pinvi Zod 항목이 "열림(O-14, 사용자 확인 필요)·기본값"으로 표기돼 있다.
- [ ] `python3 -B -X utf8 tools/validate_document_links.py`가 이 문서군에서 0 오류(절대 경로 링크 없음).
- [ ] 2인 독립 리뷰(백엔드 계약·문서 규약 영역) report가 `docs/reviews/adversarial/`에 있고 P0/P1이 없다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 tools/openapi_exceptions.py --check      # 생성 md drift(후보 도구)
python3 -B -X utf8 -m unittest discover -s tests -p "test_openapi_exceptions.py" -v
grep -c '^| \(M[1-9]\|S[0-9]\+\|N[1-8]\) |' docs/standards/openapi.md   # 30이어야 함
```

## evidence

2026-09-06 T-013 인계: OpenAPI 규칙·예외 초안은 존재한다. 이 task가 tools/openapi_exceptions.py와 tests/test_openapi_exceptions.py의 규칙 ID·필수 필드·생성 문서 drift 검증을 함께 소유한다. 아직 없는 도구를 실행한 것으로 세지 않으며 표의 실제 규칙 ID 집합을 대조한 뒤 수용 기준을 확정한다.

이 파일 하단 "실행 기록"에 명령·exit code·날짜와 core 규칙 수(30)·초기 결정 범주(12)·실제 예외 항목 수를 남긴다. 리뷰 report 경로(`docs/reviews/adversarial/YYYY-MM-DD-openapi-standard.md`)와 reviewer evidence 2파일을 링크한다. 도구를 만들지 않고 md를 수기 유지하기로 결정하면 그 결정을 여기와 `docs/journal.md`에 적는다.

### 실행 기록

- 2026-09-09 시작(초기 후보의 역사 기록): `openapi.md`·ADR-009·D-14와 기존 YAML을 직접 대조했다. YAML은 초기 결정 항목에 더해 조사에서 확인된 항목을 포함한 46건이며, 각 항목의 7키를 유지한다. 공통 정본과 ADR에 없는 `M10`을 즉시 MUST에 섞지 않고 교차 저장소 MUST로 분리했다. 이 문단의 46건은 초기 후보 수치이며 현재 후보 수치가 아니다.
- 2026-09-09 구현: `tools/openapi_exceptions.py --write` exit 0(예외 39건·Markdown 54줄), `--check` exit 0. PyYAML 의존 없이 중복 키·미지원 YAML 문법을 fail-closed로 처리하며 실제 task ID와 SHOULD 외부 계약 표면을 검증한다.
- 2026-09-09 post-fix-01(역사 기록): focused 시험 20개, 전체 `test_*.py` 357개, 문서 링크(529/2582)·plan(106)·SPDX(70)·redaction/secret(680/0)을 통과했다. `fedf7f8cbad55302183708aa4c9dd514ffba466d`(tree `e40c59e99eb367fb79893587e7dbd7489a7d2ff8`)와 [post-fix-01 manifest](../reviews/adversarial/evidence/2026-09-09-t301-post-fix-manifest.md)(SHA-256 `b04e93badcd6cb8b7aa0312e2eb998980aea02e6de3a35d582a424eb78d90c6e`)를 기준으로 두 reviewer를 실행했으며 A/B 모두 BLOCK했다. 보고서에는 당시 candidate가 보지 못한 working-tree 문서와 실행 수치를 남겼다.
- 2026-09-09 post-fix-02/03/04 수정(역사 기록): YAML 숫자·timestamp 표기 우회, task 본문 기반 provenance, SHOULD surface/reason 문자열 우회와 Unicode 경계를 순차적으로 닫았다. post-fix-04 A/B는 추가 sexagesimal·부정문·`/**`·renderer top-level·stale 수치를 재현해 BLOCK했다. 이 이전 후보의 수치는 현재 evidence가 아니다.
- 2026-09-09 post-fix-05 수정: base prefix 직후 underscore·부호·short sexagesimal·timezone timestamp를 plain scalar로 거부하고, S 예외의 전역 wildcard(`*`·`/*`·`/**`)와 한국어·영어 부정 근거를 fail-closed로 막았다. renderer가 schema·updated·apps·exceptions top-level을 재검증하고 Markdown cell escape를 적용한다. focused 시험은 27개, 전체 unittest는 364개이며 현재 tree에서 문서(536/2583)·plan(106)·SPDX(70)·redaction/secret(687/0) gate가 통과했다. 기능 수정 commit `a8ea51f1462f189765f8ae0db9a9f8baf533ac15` 이후 이 실행 기록을 포함한 review candidate를 manifest로 고정하고, 같은 candidate SHA의 PR CI가 끝난 뒤 두 reviewer에게 재검토를 요청한다.
- 소비자 build/e2e·외부 저장소 수정·npm/PyPI 게시·Release 업로드는 `NOT_RUN(범위 밖)`이다.

## rollback·release 차단 조건

- 문서·yaml만 바꾸므로 `git revert` 1회로 원복된다. 규칙 문장이 바뀌면 새 기준선 리뷰가 필요하다([reviews/README](../reviews/README.md) 규칙 9).
- 예외 레지스트리에 `review` 날짜가 없는 항목이 있거나 규칙 표와 ID가 어긋나면 T-303·T-309(drift 워크플로)를 시작하지 않는다.
- map 산출물을 바꾸는 규칙(M3 `type` URI·429 코드명 등)은 pinvi·ktdm pin 갱신 PR 계획(T-480) 없이는 "기존 표면 MUST"로 승격하지 않는다.
