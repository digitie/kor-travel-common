# T-025 내장 정책을 패키지 자기 것으로 줄이고 ui·tokens·toast 릴리스

- 상태: BLOCKED
- 우선순위: P1
- Gate: 패키지 빌드·tarball 설치·2인 리뷰
- 선행: T-023, T-024
- 외부 선행: T-424·T-474 병합. T-467·T-436은 병합됐거나 weather·transport 팀이 당일 재vendor를 확인함. Map은 T-417 병합 또는 T-419 PR 준비. geo·concierge에는 릴리스 예정일 공지(두 저장소의 작업은 선행이 아니다)
- 소유 저장소: kor-travel-common
- 병렬: T-024 뒤. T-219의 선행

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§4.1(K-02)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

`ui`·`tokens`·`toast` tarball은 정책 전체의 사본(`dependency-policy.json`)을 싣는다. 그래서 정책의 어느 줄이 바뀌어도 세 패키지가 다시 pack되고 모든 소비자가 재vendor한다. 각 패키지가 자기 것만 싣게 줄이고, 줄인 판을 한 번 릴리스한다. 그 뒤로는 무관한 정책 변경이 세 패키지를 건드리지 않는다.

## 고정 결정

- 방식은 ADR-019가 정한다. 권고(계획 문서 §4.1): 내장 사본에는 그 패키지 자신의 peer 범위와 자기 식별만 남기고, tarball 안의 검사기는 그것만 검사한다. 함대 전체의 정확 버전 대조는 중앙 guard가 한다.
- 소비자 일곱 프론트는 인자 없이 tarball 안의 검사기를 실행하고(`check:dependencies`) CI가 그것을 막는다. 그 명령 줄이 **바뀌지 않아야** 한다. 바꿔야 하는 방식을 택했다면 정확한 교체 줄을 이관 절에 적는다.
- 이미 낸 버전(`ui` 0.2.1·`tokens` 0.1.2·`toast` 0.1.1)의 bytes는 바꾸지 않는다. 줄인 판은 세 패키지의 **patch 올림**이다(`ui` 0.2.2·`tokens` 0.1.3·`toast` 0.1.2). 공개 API·CSS·peer 범위에 breaking 변경이 없고 CHANGELOG에 `### Breaking` 절을 두지 않는다.
- 이 릴리스는 세 패키지의 현재 값을 바꾼다. 새 guard(T-024)로 옮긴 소비자는 영향이 없다. 옮기지 않은 소비자(main 정책을 읽는 옛 guard)는 그날 `ui`·`tokens`를 재vendor해야 한다(지금과 같다). 그래서 외부 선행의 각 항목을 확인한 뒤에 동결 PR을 병합한다. Map이 `55a921b`에 남아 있으면 T-419가 그날의 재vendor다.

## 구현 범위

1. `tools/sync_frontend_policy.mjs`와 `packages/{ui,tokens,toast}`의 `scripts/sync-policy.mjs`·`dependency-policy.json`·`check-dependencies.mjs`·`package.json`(files·버전)을 결정에 맞게 바꾼다.
2. 회귀: `versions.json`에서 무관한 패키지 한 줄을 바꾸거나 새 패키지를 더한 뒤 세 패키지를 pack하면 tarball SHA-256이 그대로다.
3. 소비자 일곱 프론트의 현재 `check:dependencies` 명령 줄(pinvi web·mobile, map, weather, transport 둘, docker-manager)을 이관 절에 그대로 적고, 새 tarball에서 각 줄이 통과하는 fixture 시험을 둔다.
4. 세 패키지의 버전을 patch로 올리고(`ui` 0.2.2·`tokens` 0.1.3·`toast` 0.1.2) 기존 2단계(source PR → 동결 PR)로 릴리스한다. `packages/ui/smoke/next-app`의 `package.json`·lock도 함께 바꾼다.
5. 동결 PR을 병합하기 전에 지연 보고(T-024)로 옛 guard에 남은 소비자를 뽑아 외부 선행의 각 항목을 확인하고 공지한다(이 저장소 journal·integration map, 각 저장소에는 이슈 또는 포인터). source PR의 main push artifact가 나오면 옛 guard에 남은 소비자가 재vendor PR을 미리 준비할 수 있다.
6. [frontend-libraries](../standards/frontend-libraries.md)와 CHANGELOG에 이관 절.
7. 동결 병합 커밋을 40자리로 문서에 적는다. T-025 판을 벤더한 뒤에 새 guard로 옮기는 소비자가 고정할 커밋이다.

## 범위 밖

중앙 guard workflow(T-024), 소비자 저장소의 재vendor, 새 패키지(T-219~T-221).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
tools/sync_frontend_policy.mjs
packages/{ui,tokens,toast}/{package.json,dependency-policy.json,check-dependencies.mjs,scripts/sync-policy.mjs}
packages/ui/smoke/next-app/{package.json,package-lock.json}, package-lock.json
versions.json, frontend-dependencies.json, frontend-artifacts.json
docs/standards/frontend-libraries.md, CHANGELOG.md, docs/journal.md, docs/integration-map.md
```

## 수용 기준

- [ ] 시험: `versions.json`의 `vworld-map-web` 축만 바꾸고 생성·pack했을 때, 그리고 새 패키지 축을 하나 더했을 때, `ui`·`tokens`·`toast` tarball의 SHA-256이 바꾸기 전과 같다.
- [ ] 시험: 일곱 소비자 프론트의 `check:dependencies` 명령 줄이 새 tarball에서 수정 없이 통과한다(또는 이관 절에 정확한 교체 줄이 있고 그 줄이 통과한다).
- [ ] 시험: 새 tarball의 내장 검사가, 중앙 정책에는 있지만 그 패키지와 무관한 의존성의 버전 차이를 실패시키지 않는다. 자기 peer 위반은 실패시킨다.
- [ ] `npm run build --workspaces`·`npm test --workspaces`·`npm run check:policy`가 통과하고 PR head와 main push artifact의 tarball SHA-256이 같다.
- [ ] 동결 PR 본문에 외부 선행의 각 항목(T-424·T-474 병합, T-467·T-436 병합 또는 당일 재vendor 확인, Map의 T-417 또는 T-419, geo·concierge 공지)의 상태와 근거 링크가 있다.
- [ ] 세 패키지의 새 버전이 `ui` 0.2.2·`tokens` 0.1.3·`toast` 0.1.2이고 CHANGELOG에 `### Breaking` 절이 없다.

## 검증 명령

```bash
npm ci --engine-strict && npm run check:toolchain
npm run build --workspaces && npm test --workspaces && npm run check:policy
npm pack --workspace packages/ui --workspace packages/tokens --workspace packages/toast && sha256sum *.tgz
```

## evidence

정책 변경 전후 tarball SHA-256 표, 일곱 명령 줄의 fixture 결과, 공지 링크. 소비자 재vendor는 `NOT_RUN(소비자 저장소)`.

## rollback·release 차단 조건

- 동결 전이면 source PR revert. 동결 뒤에는 버전을 내리지 않고 다음 patch로 고친다.
- 일곱 명령 줄 가운데 하나라도 이관 절 없이 실패하면 병합하지 않는다.
