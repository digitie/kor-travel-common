# T-006 npm scope `@kor-travel`·PyPI 이름 가용성 확인·확보(사용자 계정 작업; 실패 시 개명)

- 상태: BLOCKED
- 우선순위: P1
- Gate: 외부 확인
- 선행: 없음
- 외부 선행: 사용자가 npm·PyPI 계정으로 직접 확인·확보한다(O-5). 에이전트는 명령과 기록 형식만 준비한다.

## 목표

잠정 패키지명 `@kor-travel/tokens`·`@kor-travel/ui`·PyPI `kor-travel-common`이 실제로 확보 가능한지 첫 소비자 PR 전에 확인하고, 실패하면 비용 0인 지금 `@digitie/kor-travel-<pkg>`로 개명한다. 1차 배포 채널은 GitHub Release tarball이므로(D-11) 이 task는 게시가 아니라 이름 확보·기록만 한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-01(패키지명 잠정, 실패 시 `@digitie/kor-travel-<pkg>`), D-11(공개 npm/PyPI 게시는 Phase 5 T-507), D-15(배포 이름 `kor-travel-common`, import `kortravelcommon`), O-5.
- ADR-005(패키지명 잠정 표기) — [docs/adr/README.md](../adr/README.md).
- [UI 컴포넌트 조사](../survey/cross/ui-components.md) §6.2·[선행 보고서 관계](../survey/README.md) §5(npm 게시 미결 상태를 조사가 확인).

## 구현 범위

1. 확인 절차를 `docs/runbooks/release.md`(T-007) "이름 확보" 절에 1회성 명령으로 남기지 않고, 이 task의 evidence에만 기록한다: `npm view @kor-travel/tokens` 결과(404 = 미점유), npm 조직 `kor-travel` 생성 가능 여부(웹 UI, 사용자), PyPI `https://pypi.org/project/kor-travel-common/` 404 여부(`pip index versions kor-travel-common` 보조).
2. 결과 기록: ADR-005 머리 상태 보충 문구("패키지명 확정 2026-MM-DD" 또는 "개명"), `docs/architecture/packages.md` 이름 표, `docs/standards/frontend-stack.md`·`consumer-adoption.md`의 import 예시.
3. 실패 시 개명: `packages/*/package.json` `name`, `docs/standards/*`·`docs/runbooks/*`·`templates/*`의 `@kor-travel/` 문자열 전수 치환(`docs/survey/**`·`docs/plan/**`는 역사 기록이므로 제외), `@source "../node_modules/@digitie/kor-travel-ui"` 경로 갱신.

## 범위 밖

- 실제 `npm publish`·`twine upload`(T-507), 조직 권한·2FA 설정 문서화, PyPI 이름 예약을 위한 placeholder 업로드(태그 불변·재발행 금지 원칙과 충돌하므로 하지 않음).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/adr/005-*.md`(상태 보충 1줄), `docs/architecture/packages.md`; 개명 시 `packages/tokens/package.json`, `packages/ui/package.json`, `docs/standards/frontend-stack.md`, `docs/runbooks/consumer-adoption.md`, `templates/consumer-adoption-checklist.md`.

## 수용 기준

- evidence에 확인 일시·명령·응답(HTTP 상태 또는 `npm view` 출력 요약)·확인 주체(사용자)가 있다.
- 세 이름(npm scope, `@kor-travel/tokens`·`@kor-travel/ui`, PyPI `kor-travel-common`)의 판정이 각각 "확보/미확보"로 적혀 있다.
- 개명한 경우 `rg "@kor-travel/" --glob '!docs/survey/**' --glob '!docs/plan/**'`가 0건이고 T-101·T-201의 `npm pack` 스모크가 새 이름으로 통과한다(T-101 이후라면).
- 확보한 경우 ADR-005 상태 보충 문구가 갱신되고 `docs/architecture/packages.md`가 "잠정" 표기를 지운다.

## 검증 명령

```bash
npm view @kor-travel/tokens version; echo "exit=$?"
npm view @kor-travel/ui version; echo "exit=$?"
pip index versions kor-travel-common; echo "exit=$?"
rg -n "@kor-travel/" --glob '!docs/survey/**' --glob '!docs/plan/**' . | head
python3 -B -X utf8 tools/validate_document_links.py
```

Git Bash에서 동일. 네트워크 명령은 사용자 환경에서 실행한다.

## evidence

- 사용자 확인 결과를 이 절에 인용하고 `docs/journal.md`에 남긴다. 에이전트가 대신 실행하지 못한 항목은 `NOT_RUN(사용자 계정 필요)`로 둔다.

## rollback 또는 release 차단 조건

- 문서·`package.json` 이름만 바뀌므로 `git revert` 1회로 원복한다.
- 이름 판정이 없는 상태에서는 첫 소비자 PR(T-410·T-461)을 merge하지 않는다(개명 비용이 0에서 벗어남).
