# T-024 ADR-019가 정한 프론트 guard 모델 구현과 채택 커밋 지정

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 도구 단위·selftest workflow·2인 리뷰
- 선행: T-023
- 소유 저장소: kor-travel-common
- 병렬: T-023 뒤. T-025의 선행(같은 파일을 고친다)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1(K-01)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

ADR-019의 결정을 재사용 workflow와 문서에 구현한다. ADR-019는 2026-11-17 소유자 결정으로 권고안(정책과 도구 축을 `common-ref`에서 읽기 + 막지 않는 지연 보고)을 accepted로 정했다. 아래 범위는 그 결정 그대로다. 어느 안이든 이 task는 소비자가 올릴 **채택 커밋 하나**를 지정한다.

## 고정 결정

- 결정 정본은 T-023의 ADR-019다.
- 옛 SHA를 호출하는 소비자의 동작은 바뀌지 않는다(그 workflow 판은 계속 `main`을 읽는다). 새 동작은 호출 SHA를 올린 소비자만 얻는다.
- 지금 고정된 검사기는 둘이다: `55a921b`(map)와 `97f8ed9`(나머지와 geo·concierge. `9e16393`은 `tools/`가 같다). CI checkout은 얕으므로 두 판의 검사기를 시험 fixture로 저장소에 둔다.
- 수렴을 막는 강제로 다시 만들지 않는다. 지연은 보고로만 본다.

> 구현 메모(2026-11-18): '두 판의 검사기를 시험 fixture로 저장소에 둔다'와 수용 기준 4는 고정 사본 대신 실제 옛 판(`97f8ed9`, map은 `55a921b`) workflow의 대조 단계 원문을 일곱 소비자 main에 병합 전후 정책으로 돌린 판정 표로 확인했다(전후 동일, [evidence](../evidence/t024-guard-model.md)). 옛 판은 main 정책을 읽으므로 영구 selftest로 두면 다음 정책 변경 PR마다 결과가 바뀐다. 이 PR은 정책 세 파일을 바꾸지 않는다.

## 구현 범위

1. `.github/workflows/frontend-consumer-guard.yml`: `main` 정책 checkout 단계를 없애고 `--policy`·`--canonical`·도구 검사의 `--registry`를 `common-ref` checkout에서 읽는다. 검사기를 돌리는 `setup-node`의 `node-version: 22.23.1`과 `npm@12.0.1` 설치 줄도 적어 두지 않고 `common-ref`의 `.nvmrc`(`node-version-file`)와 `axes.npm.recommended`를 읽는다. 그래야 축을 올린 커밋(T-029)을 고정한 소비자가 common의 `npm ci --engine-strict`와 `check:toolchain --runtime`에서 실패하지 않는다.
2. 지연 보고: 소비자별 `common-ref`와 벤더 버전을 정본과 비교해 표로 내는 주간 job(실패시키지 않음). 입력은 `consumers.pins.json` 또는 각 저장소의 workflow 파일이다.
3. 채택 커밋 지정: 이 task의 병합 커밋을 채택 커밋으로 문서에 적는다. 그 커밋의 검사기를 각 소비자의 현재 main(P, M, W, T, D, geo, concierge)에 읽기 전용으로 돌려, 걸리는 규칙을 소비자별로 적는다.
4. [frontend-libraries](../standards/frontend-libraries.md) '검사와 갱신' 절, [versions](../standards/versions.md) §3.1.1, [release](../runbooks/release.md), [consumer-adoption](../runbooks/consumer-adoption.md)을 결정에 맞춘다.
5. ADR이 예고 필드를 골랐다면 추가로: `tools/check_versions.py`가 axis의 모르는 필드를 거절하므로(`:318-319`) 그 파일과 시험, `tools/sync_frontend_policy.mjs`, `packages/{ui,tokens,toast}`의 생성 사본을 함께 고친다.

## 범위 밖

패키지 실행 코드·CSS·공개 API. 소비자 저장소(호출 SHA 갱신은 T-417·T-424·T-436·T-467·T-474). 내장 정책(T-025).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/frontend-consumer-guard.yml, .github/workflows/workflows-selftest.yml
.github/workflows/<지연 보고>.yml 또는 tools/<지연 보고 도구>
tests/fixtures/guard-checkers/{55a921b,97f8ed9}/*          # 고정 검사기 사본
docs/standards/frontend-libraries.md, docs/standards/versions.md, docs/runbooks/release.md, docs/runbooks/consumer-adoption.md
CHANGELOG.md, docs/journal.md, docs/integration-map.md
```

## 수용 기준

- [ ] selftest: 새 workflow를 고정 ref로 호출한 fixture 소비자가, 그 뒤 `main`의 정책 값과 `axes.node.recommended`를 바꿔도 통과한다.
- [ ] selftest: 같은 fixture가 자기 `common-ref`의 정책과 어긋나면 실패한다(검사는 그대로 엄격하다).
- [ ] selftest: Node 축이 22.23.1이 아닌 ref(시험용 커밋 또는 fixture)를 고정한 소비자에서 guard 자신의 Node·npm이 그 ref의 값으로 선택되고 통과한다.
- [ ] 옛 판(`97f8ed9`) workflow를 호출하는 fixture의 판정이 이 변경 전과 같다.
- [ ] 채택 커밋이 문서에 40자리로 적혀 있고, 일곱 소비자 main에 대한 읽기 전용 실행 결과(통과 또는 걸린 규칙 목록)가 evidence에 있다.
- [ ] 지연 보고가 소비자별 호출 ref·벤더 버전·정본과의 차이를 표로 내고, 차이가 있어도 exit 0이다.
- [ ] `npm run check:policy`·`npm run test:toolchain`·`npm test --workspace packages/ui`가 통과한다.

## 검증 명령

```bash
npm ci --ignore-scripts --engine-strict
npm run check:policy && npm run test:toolchain
npm test --workspace packages/ui
gh workflow run workflows-selftest.yml --ref <브랜치>   # 또는 PR의 selftest 결과
python3 -B -X utf8 tools/validate_document_links.py && git diff --check
```

## evidence

selftest 실행 링크, 일곱 소비자에 대한 읽기 전용 실행 표, 지연 보고 출력. 실제 소비자 채택은 `NOT_RUN(소비자 저장소)`.

## rollback·release 차단 조건

- `git revert` 1회로 workflow가 `main`을 읽는 판으로 돌아간다. 이미 새 판을 호출하는 소비자는 그 SHA를 계속 쓰므로 영향이 없다.
- 옛 판 호출 fixture의 판정이 달라지면 병합하지 않는다.
