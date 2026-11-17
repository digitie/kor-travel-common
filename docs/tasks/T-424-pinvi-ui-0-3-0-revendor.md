# T-424 pinvi: ui 0.3.0 재vendor와 guard 호출 SHA 갱신

- 상태: BLOCKED
- 우선순위: P2
- Gate: 소비자 CI(web·mobile·공통 프론트엔드 정책)
- 선행: T-221
- 소유 저장소: pinvi
- 병렬: 채택 묶음(T-435·T-466·T-474와 동시 가능)

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §4.1·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

pinvi 웹은 `@kor-travel/ui` 0.2.1을 벤더한다. T-222가 현재 값을 0.3.0으로 바꾸면 0.2.1은 실패한다. 그 전에 0.3.0으로 재vendor하고 guard 호출 SHA를 T-024 이후로 올린다. 관리자 부품의 채택은 이 task의 필수 범위가 아니다.

## 고정 결정

- 예고 창 동안 0.3.0 소비자는 새 검사기에서만 통과한다. 호출 SHA 갱신과 재vendor를 **한 PR**에 둔다.
- pinvi 관리자의 부품은 재도색 이식본이다. 공통 부품으로 바꿀지는 pinvi가 따로 정한다. 사용자 표면과 모바일 UI는 대상이 아니다([ui-contract](../standards/ui-contract.md)).
- 모바일 프로필은 `@kor-travel/ui`를 금지한다. 모바일은 T-221이 `tokens`를 함께 올렸을 때만 영향이 있다.

## 구현 범위

1. `apps/web/vendor/`의 ui tarball(과 T-221이 함께 올린 패키지), `common-artifacts.json`, `package.json`·lock.
2. `.github/workflows/common-frontend-policy.yml`의 호출 SHA와 `common-ref`.
3. 0.3.0에 Breaking이 없다는 것을 타입 검사·단위·e2e로 확인한다.

## 범위 밖

관리자 부품의 공통 부품 전환, 사용자·모바일 UI.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/pinvi`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
apps/web/vendor/*, apps/web/common-artifacts.json, apps/web/package.json, package-lock.json
apps/mobile/common-artifacts.json            # tokens가 함께 오를 때만
.github/workflows/common-frontend-policy.yml
docs/journal.md, docs/resume.md, docs/tasks.md
```

## 수용 기준

- [ ] '공통 프론트엔드 정책' check가 새 호출 SHA로 통과한다(web·mobile 두 항목).
- [ ] `web`·`mobile` workflow와 Aggregate CI가 통과한다.
- [ ] 호출 SHA와 `common-ref`가 같은 40자리 값이고 T-024 병합 커밋 이후다.

## 검증 명령

```bash
# pinvi
npm ci --engine-strict && npm run check:dependencies --workspace apps/web
gh pr checks <PR>
```

## evidence

PR의 check 결과.

## rollback·release 차단 조건

- `git revert` 1회(lock·vendor·호출 SHA 포함). 현재 값이 0.2.1인 동안은 되돌려도 guard가 통과한다.
