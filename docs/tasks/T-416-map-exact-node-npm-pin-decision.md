# T-416 map: 정확 Node/npm 핀 채택 여부 결정

- 상태: BLOCKED
- 우선순위: P1
- Gate: 소유자 결정 기록
- 선행: 없음
- 외부 선행: 소유자 결정은 2026-11-17에 났다(채택, Node 26.13.1). 남은 것은 결정 기록과 핀을 담은 Map PR의 병합이다
- 소유 저장소: kor-travel-map
- 병렬: 결정이 나오면 T-417이 풀린다. 다른 task는 이 결정을 기다리지 않는다

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§3.6(K-78)·§4.1이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 결정(2026-11-17)

- 소유자: "Map의 Node 버전 고정 (T-416): .nvmrc와 engines를 22.23.1로 고정할지입니다 … 이것들은 추천안 대로 node는 최신버전으로". **채택**이고, 고정값은 22.23.1이 아니라 최신 버전이다.
- '최신 버전'은 nodejs.org 공식 릴리스 색인(`https://nodejs.org/dist/index.json`, 2026-11-17 조회)에서 가장 새 LTS 줄의 최신 patch로 읽었다: **Node 26.13.1**(26 'Lithium' LTS, 2026-11-10 보안 릴리스). 색인의 가장 새 항목 `v27.0.0-alpha.0.1.1`(2026-11-16)은 alpha라 운영 핀 대상이 아니다.
- npm은 공통 축 12.0.1을 유지한다. Map은 이미 `packageManager: npm@12.0.1`과 `engines.npm` 12.0.1을 쓰고, npm 12.0.1은 Node 26을 받는다(`engines.node` `^22.22.2 || ^24.15.0 || >=26.0.0`). Node 26.13.1 동봉 npm(11.20.0)으로 내리면 공통 축과 어긋난다.
- 공통 축(`axes.node.recommended`)은 22.23.1이다. Map이 새 guard로 옮기려면 축이 26.13.1인 common 커밋이 필요하다([T-029](T-029-node-axis-to-latest-lts.md)). 그래서 [T-417](T-417-map-guard-ref-toolchain.md)의 선행에 T-029를 더했다. 그 전까지 Map은 옛 guard(`55a921b`, 도구 단계 없음)에 남으므로 이 핀이 Map의 guard를 깨지 않는다.
- Map 쪽 기록과 핀(루트 `.nvmrc`, 정확 `engines.node`, CI `node-version`, Node Docker 이미지, live e2e 실행 이미지의 Node)은 Map ADR-124의 PR이 담는다.

## 목표

map은 guard workflow를 `55a921b`로 호출한다. 그 뒤 판은 도구 규칙(루트 `.nvmrc`, 정확 `engines.node`·`engines.npm`)을 요구하는데 map 루트는 `engines`가 범위 선언이고 `.nvmrc`가 없다. 2026-11-17 재vendor PR(#1504)이 호출 SHA를 올렸다가 도구 규칙에서 실패해 되돌렸고 이관을 별도 결정으로 남겼다. 이 task는 map이 정확 핀(`.nvmrc` + 정확 `engines.node`, 질의 당시 값 22.23.1, 결정 값 26.13.1)을 채택할지 **결정만** 한다. 가정으로 진행하지 않는다.

## 고정 결정

- 도구 규칙의 정본은 [ADR-018](../adr/018-exact-node-npm-build-toolchain.md)과 [versions](../standards/versions.md) §3.1.1이다.
- 결정 주체는 소유자다. 에이전트가 기본값으로 대신 정하지 않는다.

## 구현 범위

1. 선택지를 적는다(질의 당시 값). (가) 채택: 루트 `.nvmrc` 22.23.1(결정 값은 26.13.1), 정확 `engines`, `packageManager`. map의 범위 선언(`^22.22.2 || ^24.15.0 || >=26.0.0`)을 버린다. (나) 미채택: 사유를 map ADR로 남긴다.
2. 각 선택의 결과를 적는다. (가)면 T-417로 호출 SHA를 올릴 수 있고(값이 공통 축과 달라 T-029 뒤), ADR-019(2026-11-17 accepted)에 따라 그 뒤로 main 정책 변경이 map을 깨지 않는다. (나)면 map은 옛 guard에 남아 지금처럼 main 정책이 바뀌는 날마다 재vendor한다. 다른 task는 어느 쪽이든 진행된다.
3. 결정을 map의 ADR 색인에 기록한다(map PR).
4. common 후속 PR(문서 전용): [integration map](../integration-map.md)에 결정을 적고 T-417의 상세 파일을 결정에 맞춘다. (나)이고 예외 등록이 필요하면 `versions.json`의 `exceptions[]`도 이 후속 PR이 고친다.

## 범위 밖

guard 호출 SHA와 남은 도구 규칙 입력(T-417), 부품 채택(T-415). 결정이 채택이고 소유자가 값을 정했으므로 `.nvmrc`·정확 `engines`·CI·이미지의 Node는 결정 기록과 같은 Map PR에 넣었다(2026-11-17).

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.
- PR은 둘이다: map의 결정 기록 PR, common의 문서 전용 후속 PR.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/adr/README.md 또는 새 ADR(map)
docs/journal.md, docs/resume.md(map)
docs/integration-map.md(common)
```

## 수용 기준

- [ ] 소유자의 결정(채택/미채택)과 날짜가 map 문서에 인용과 함께 있다.
- [ ] 미채택이면 사유가 map ADR에 있다.
- [ ] common 후속 PR이 병합돼 integration map과 T-417이 결정을 가리킨다.

## 검증 명령

```bash
# 결정 기록만 있다. 실행할 검증 명령은 없다.
git diff --stat
```

## evidence

결정 인용과 기록 위치.

## rollback·release 차단 조건

- 문서 기록. 결정이 바뀌면 새 기록을 더한다(지우지 않는다).
