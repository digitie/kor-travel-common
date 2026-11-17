# T-416 map: 정확 Node/npm 핀 채택 여부 결정

- 상태: BLOCKED
- 우선순위: P1
- Gate: 소유자 결정 기록
- 선행: 없음
- 외부 선행: 소유자 결정. 2026-11-17에 질의했고 답이 아직 없다
- 소유 저장소: kor-travel-map
- 병렬: 결정이 나오면 T-417·T-415가 풀린다

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§3.6(K-78)·§4.1이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

map은 guard workflow를 `55a921b`로 호출한다. 그 뒤 판은 도구 규칙(루트 `.nvmrc`, 정확 `engines.node`·`engines.npm`)을 요구하는데 map 루트는 `engines`가 범위 선언이고 `.nvmrc`가 없다. 2026-11-17 재vendor PR(#1504)이 호출 SHA를 올렸다가 도구 규칙에서 실패해 되돌렸고 이관을 별도 결정으로 남겼다. 이 task는 map이 정확 핀(`.nvmrc` + `engines.node` 22.23.1)을 채택할지 **결정만** 한다. 가정으로 진행하지 않는다.

## 고정 결정

- 도구 규칙의 정본은 [ADR-018](../adr/018-exact-node-npm-build-toolchain.md)과 [versions](../standards/versions.md) §3.1.1이다.
- 결정 주체는 소유자다. 에이전트가 기본값으로 대신 정하지 않는다.

## 구현 범위

1. 선택지를 적는다. (가) 채택: 루트 `.nvmrc` 22.23.1, 정확 `engines`, `packageManager`. map의 범위 선언(`^22.22.2 || ^24.15.0 || >=26.0.0`)을 버린다. (나) 미채택: 사유를 map ADR 또는 `versions.json` 예외로 남긴다.
2. 각 선택의 결과를 적는다. (가)면 T-417로 호출 SHA를 올릴 수 있고 예고 창 동안 새 버전을 받을 수 있다. (나)면 map은 옛 검사기에 남아 창 동안 새 버전을 받을 수 없고, 정책의 현재 값이 바뀌는 날마다 같은 날 재vendor해야 한다(T-222 참조).
3. 결정을 map의 ADR 색인과 common [integration map](../integration-map.md)에 기록한다.

## 범위 밖

도구 규칙 이관 구현(T-417), 부품 채택(T-415).

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/adr/README.md 또는 새 ADR(map)
docs/journal.md, docs/resume.md(map)
docs/integration-map.md(common)
```

## 수용 기준

- [ ] 소유자의 결정(채택/미채택)과 날짜가 map 문서에 인용과 함께 있다.
- [ ] 미채택이면 사유와 `versions.json` 예외(또는 map ADR) 위치가 있다.
- [ ] T-417·T-415·T-222의 상세 파일이 이 결정을 가리키도록 갱신됐다.

## 검증 명령

```bash
# 결정 기록만 있다. 실행할 검증 명령은 없다.
git diff --stat
```

## evidence

결정 인용과 기록 위치.

## rollback·release 차단 조건

- 문서 기록. 결정이 바뀌면 새 기록을 더한다(지우지 않는다).
