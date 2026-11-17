# T-417 map: guard 검사 코드 ref 갱신과 정확 Node/npm 도구 규칙 이관

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(공통 프론트엔드 정책)
- 선행: T-416, T-024
- 소유 저장소: kor-travel-map
- 병렬: 묶음 B. T-416이 '채택'일 때만 진행

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§3.6(K-78)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

T-416이 정확 핀 채택을 결정하면 map의 guard 호출 SHA를 올리고 도구 규칙이 요구하는 것을 채운다. T-416이 미채택이면 이 task는 그 결정으로 닫는다.

## 고정 결정

- 도구 규칙의 정본은 [ADR-018](../adr/018-exact-node-npm-build-toolchain.md)과 [versions](../standards/versions.md) §3.1.1이다.
- 전제는 T-416의 '채택' 결정이다. 결정 없이 `engines`를 바꾸지 않는다.
- 호출 SHA는 '최신'이 아니라 T-024가 지정한 채택 커밋 하나로 올린다. 그 커밋에서 map이 걸리는 규칙은 T-024의 evidence에 미리 적혀 있다.

## 구현 범위

1. `.github/workflows/common-frontend-policy.yml`의 호출 SHA와 `common-ref`를 T-024가 지정한 채택 커밋으로 올린다.
2. 도구 규칙이 요구하는 것(루트 `.nvmrc`, 정확 `engines.node`·`engines.npm`, `packageManager`, `toolchain-manifests`·`node-dockerfiles` 입력)을 채운다.
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
