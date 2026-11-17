# T-417 map: guard 검사 코드 ref 갱신과 정확 Node/npm 도구 규칙 이관

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(공통 프론트엔드 정책)
- 선행: T-416, T-024, T-029
- 소유 저장소: kor-travel-map
- 병렬: T-029 뒤(묶음 B의 다른 task와 달리 공통 축 상향을 기다린다)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§3.6(K-78)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 2026-11-17 결정 반영

T-416은 **채택**으로 정해졌고 값은 Node 26.13.1·npm 12.0.1이다. 루트 `.nvmrc`, 정확 `engines`, CI `node-version`, Node Docker 이미지는 T-416의 Map PR(ADR-124)이 먼저 바꾼다. 그래서 이 task의 구현 범위 2는 그 PR이 빠뜨린 도구 규칙 입력(`toolchain-manifests`·`node-dockerfiles`)만 남는다. 호출 SHA는 공통 축이 26.13.1인 커밋이어야 하므로 T-024의 채택 커밋이 아니라 [T-029](T-029-node-axis-to-latest-lts.md)의 병합 커밋(그 뒤 common이 지정한 커밋)으로 올린다. 그 커밋의 정책이 그때 Map이 벤더한 판과 같아야 한다(T-025 릴리스 뒤면 T-419로 받은 `ui` 0.2.2·`tokens` 0.1.3). 다르면 같은 PR에서 재vendor한다.

## 목표

T-416이 채택(2026-11-17, Node 26.13.1)으로 정해졌으므로 map의 guard 호출 SHA를 공통 축이 26.13.1인 커밋으로 올리고 남은 도구 규칙 입력을 채운다.

## 고정 결정

- 도구 규칙의 정본은 [ADR-018](../adr/018-exact-node-npm-build-toolchain.md)과 [versions](../standards/versions.md) §3.1.1이다.
- 전제는 T-416의 '채택' 결정(2026-11-17)이다. `.nvmrc`·정확 `engines`·CI·이미지의 Node는 T-416의 Map PR이 이미 26.13.1로 바꿨다.
- 호출 SHA는 '최신'이 아니라 common이 지정한 커밋 하나로 올린다: T-029의 병합 커밋. 그 뒤 T-025 동결이나 T-221(admin-kit)이 병합돼 Map이 그 판을 벤더했다면, common이 그 뒤에 지정한 커밋(공통 축 26.13.1을 포함)으로 올린다. 그 커밋의 정책이 그때 Map이 벤더한 판과 같아야 한다.

## 구현 범위

1. `.github/workflows/common-frontend-policy.yml`의 호출 SHA와 `common-ref`를 위 고정 결정의 커밋으로 올린다.
2. 도구 규칙이 요구하는 것 가운데 T-416의 Map PR이 하지 않은 것(`toolchain-manifests`·`node-dockerfiles` 입력, 검사기가 더 요구하는 항목)을 채운다.
3. map의 기존 검증 스크립트(`verify-npm-tree.mjs`·`verify-next-sharp.mjs`)와 겹치는 검사가 있으면 어느 쪽을 남기는지 적는다.
4. common 후속 PR(문서 전용): [integration map](../integration-map.md)의 map 호출 SHA를 갱신한다.

## 범위 밖

공통 부품 채택(T-415), map의 다른 CI.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-map`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
.github/workflows/common-frontend-policy.yml
.nvmrc, package.json, packages/kor-travel-map-admin/frontend/package.json
docker/frontend.Dockerfile            # 도구 규칙이 요구하면
docs/journal.md, docs/resume.md
```

## 수용 기준

- [ ] PR의 '공통 프론트엔드 정책' check가 새 호출 SHA로 통과한다.
- [ ] `frontend` workflow와 `docker-images` workflow가 통과한다.
- [ ] 호출 SHA와 `common-ref`가 같은 40자리 값이다.

## 검증 명령

```bash
# kor-travel-map
npm ci --ignore-scripts --engine-strict   # 프론트 workspace
npm run check:dependencies
gh pr checks <PR>
```

## evidence

map PR의 check 결과. common 쪽 기록은 문서 전용 후속 PR로 남긴다.

## rollback·release 차단 조건

- `git revert` 1회로 호출 SHA가 `55a921b`로 돌아간다.
- 도구 규칙 때문에 `frontend`·`docker-images`가 실패하면 병합하지 않는다.
