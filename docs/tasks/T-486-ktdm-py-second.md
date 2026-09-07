# T-486 ktdm: py 2차(request-id `trust_incoming=False`·quality baseline)

- 상태: BLOCKED
- 우선순위: P3
- Gate: ci.yml
- 선행: T-471, T-311
- 외부 선행: ktdm 루트 GPL-3.0-or-later 정렬(L8, O-2; T-021 결과) — 브리프 선행 열에는 없으나 D-16이 L8 전 코드 소비를 금지하므로 common 모듈 import는 L8 후에만

## 목표

docker-manager 백엔드가 py 2차 모듈 중 C2 request-id를 `trust_incoming=False`(서버 발급만, 수신 헤더 불신 — ktdm 기존 동작)로 채택하고, T-471에서 도입한 C20 quality baseline(ruff per-file-ignores·mypy `ignore_errors`)을 축소한다. 오류 envelope `{detail:{code,message,stage,mutation_applied,...}, request_id}`·`/api/v1` prefix·수기 Prometheus exposition(`ktdm_`)은 예외 유지. 교차 저장소 pin 계약(pinset·manifest v6·journal v8)은 건드리지 않는다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-14(M4 X-Request-ID 즉시 MUST, `trust_incoming=False`는 앱 옵션(ktdm); 예외 초기 등록 ktdm `/api/v1`·`{detail}`)·D-15(C2 `trust_incoming`·형식 검증; C20 baseline; 메트릭 접두는 기존 예외 규칙 — ktdm은 prometheus-client 미사용이라 C3 적용 대상 아님)·D-16(ktdm Python 3차, L8 후)·D-24.
- ADR-009·ADR-011 — [ADR 색인](../adr/README.md). 정본: [openapi](../standards/openapi.md), `docs/standards/openapi-exceptions.yaml`, [backend-stack](../standards/backend-stack.md).
- 사실: `request_context.py` 서버 발급 `X-Request-ID` + contextvar 로그 필터 + CORS expose + envelope `request_id`; envelope `{detail:{code,message,stage,mutation_applied}, request_id}` + 409/500 매핑(base 케이스 평문 문자열 — 테스트 부분 문자열 단언 때문); 수기 text exposition `ktdm_`(prometheus-client 미사용); `ruff format` 미적용본; pinset/manifest/journal 교차 저장소 결박(SKILL DO NOT 10) — [inv/ktdm §4.1·§8-10~13·§9](../survey/inventory/kor-travel-docker-manager.md), [oa §2.5·§2.10·§4](../survey/cross/openapi.md), [cm §4.1 B10](../survey/commonality-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 ktdm #6](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- `backend/pyproject.toml`에 `kor-travel-common[api] @ git+…@py-v0.2.0#subdirectory=…`(C2 포함 태그), `uv.lock` 갱신(T-471 전제).
- `request_context.py` → `kortravelcommon.request_id` 미들웨어(`trust_incoming=False`)로 교체하되 contextvar 이름·로그 필터·CORS expose·envelope `request_id` 주입 계약을 어댑터로 유지(호출부 무변경). 형식은 UUID v4(기존과 동일한지 확인, 다르면 로그 소비자 영향 기록).
- quality baseline 축소: T-471 baseline 중 자동 수정 가능한 ruff 규칙(`I`·`UP` 등)만 파일 단위로 정리 — 재포맷성 diff 금지, 리뷰 가능한 크기(≤10 파일)로.
- `openapi-exceptions.yaml` ktdm 항목(`/api/v1`·`{detail}`) `review` 갱신; `docs/bindings.md`에 request-id 결박(값·계약·생애) 등록 + `test_normative_docs_cite_real_symbols` 통과.

## 범위 밖

envelope 변경(평문 base 케이스 포함), metrics 공통화, 앱별 인증 정책·저장소, pin registry·pinset 계약(B10), `ruff format`, Node/프론트. 공용 인증 프리미티브 채택은 T-312 후속으로 기록한다.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-docker-manager`, Linux/WSL, 브랜치 `agent/T-486-request-id`, `main`에서 분기. PR 1개(≤10 파일 + lock); baseline 축소가 크면 별도 PR.
- 되돌리기 = `git revert <merge-sha>` + wheelhouse 재프로비저닝(운영은 systemd + venv).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
backend/pyproject.toml, backend/uv.lock
backend/src/kor_travel_docker_manager/request_context.py, main.py
backend/tests/test_request_context.py            # 계약 테스트 갱신
docs/bindings.md
kor-travel-common.lock.json, docs/standards/openapi-exceptions.yaml(common)
```

## 수용 기준

- [ ] `ci.yml` green(pytest 수 기록, ruff·mypy baseline 통과, 규범 문서 테스트 통과).
- [ ] 계약 테스트: 수신 `X-Request-ID`를 무시하고 서버 발급 값이 응답 헤더·envelope `request_id`·로그에 동일하게 나타남; 오류 envelope 본문 byte 무변경(부분 문자열 단언 테스트 통과).
- [ ] `git diff --stat backend/src`에서 request_context·main 외 변경은 baseline 축소 파일뿐이며 재포맷성 diff 0.
- [ ] `check_versions` ktdm Python 행 `OK`; L8 evidence PR 본문 기재.
- [ ] pinset/manifest/journal 관련 테스트 무변경 통과(교차 저장소 계약 미접촉 증명).

## 검증 명령

```bash
# kor-travel-docker-manager/backend (Linux/WSL)
uv sync --locked --extra dev && uv run pytest -q && uv run ruff check --ignore EXE001 . && uv run mypy <targets>
uv run pytest tests/test_request_context.py tests/test_normative_docs_cite_real_symbols.py -q
uv export --frozen --format requirements-txt > /tmp/ktdm-req.txt   # wheelhouse 입력 재생성
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-docker-manager/kor-travel-common.lock.json
```

## evidence

PR 본문(CI run·계약 테스트 출력·baseline 축소 표·L8 링크), `consumers.pins.json`·`docs/journal.md`, 이 파일 "실행 기록".

## rollback·release 차단 조건

- L8(T-021) 미완이면 PR을 열지 않는다(B9). envelope 본문 변화·규범 문서 테스트 실패면 머지 금지; 머지 후 운영 로그 상관관계 회귀 시 revert + 재프로비저닝.
