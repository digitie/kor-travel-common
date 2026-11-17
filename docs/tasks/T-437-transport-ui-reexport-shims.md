# T-437 transport-admin: ui 순수 재수출 shim을 공통 경로 직접 import로

- 상태: READY
- 우선순위: P3
- Gate: 소비자 lint·type-check·단위·build
- 선행: 없음
- 소유 저장소: kor-travel-transport
- 병렬: 묶음 A. 릴리스가 필요 없다

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §3.5(K-66)·§4.8이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

transport 관리자 프론트의 `components/ui/*`에는 map과 byte 동일한 순수 재수출 shim 13개가 있다. 호출부가 공통 경로를 직접 import하게 하고 shim을 지운다. 릴리스가 필요 없다.

## 고정 결정

- 동작과 화면이 바뀌지 않는다. import 경로만 바뀐다.
- 로컬 클래스를 덧붙인 wrapper와 `button.tsx`·`sonner.tsx`·폼, transport만 가진 `empty.tsx`·`spinner.tsx`는 대상이 아니다.
- 이 저장소는 다른 팀이 유지한다.

## 구현 범위

1. 대상 13개: `tabs-variants`·`alert-dialog`·`breadcrumb`·`checkbox`·`data-table`·`native-select-option`·`popover`·`separator`·`skeleton`·`table`·`tabs`·`textarea`·`tooltip`. 호출부 import를 `@kor-travel/ui/<이름>`으로 바꾸고 파일을 지운다.
2. `lib/utils.ts`의 `cn`을 쓰는 호출부를 `@kor-travel/ui/utils`로 바꾸고 파일을 지운다.
3. 시험·mock의 경로 갱신.

## 범위 밖

wrapper·폼·부품 채택(T-435), 패키지 버전.

## 대상 저장소·브랜치·PR·되돌리기

- 저장소 `digitie/kor-travel-transport`. 이 저장소(common)의 작업이 아니다. 그 저장소의 규칙·리뷰·CI를 따른다.
- 브랜치: `docs/…` 또는 `agent/<agent>-<task>` 형식의 작업 브랜치, `origin/main`에서 분기. PR 1개.
- 되돌리기: `git revert <merge-sha>` 1회.
- 그 저장소의 backlog에는 이 task를 가리키는 포인터 한 줄만 두고 수용 기준을 복제하지 않는다.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
packages/kor-travel-transport-admin/frontend/components/ui/{13개 shim}          # 삭제
packages/kor-travel-transport-admin/frontend/lib/utils.ts                      # 삭제
packages/kor-travel-transport-admin/frontend/**                               # import 경로
```

## 수용 기준

- [ ] 13개 shim과 `lib/utils.ts`가 없고 `@/components/ui/<그 이름>`·`@/lib/utils` import가 0개다(grep).
- [ ] lint·type-check·단위·`next build`·`check:dependencies`가 통과한다.
- [ ] `vendor/`·`common-artifacts.json`·lock이 바뀌지 않았다.

## 검증 명령

```bash
# kor-travel-transport/packages/kor-travel-transport-admin/frontend
npm run check:dependencies && npm run lint && npm run type-check && npm test && npm run build
```

## evidence

PR의 CI 결과와 지운 파일 수.

## rollback·release 차단 조건

- `git revert` 1회.
