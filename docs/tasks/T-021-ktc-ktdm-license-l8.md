# T-021 ktc·ktdm 라이선스 정렬(L8) 결정 반영: 결정 기록·각 저장소 PR 요청 문서

- 상태: DONE
- 우선순위: P1
- Gate: 문서
- 선행: 없음
- 외부 선행: 사용자 결정 O-2 완료(2026-09-08). 실제 concierge·docker-manager 반영은 각 외부 task의 선행이다.

## 목표

MIT 저장소 두 곳(concierge·docker-manager)이 GPL common 코드를 링크하기 전에 필요한 라이선스 정렬 결정을 기록하고, 각 저장소에 보낼 PR 요청 문서를 만들어 T-454·T-473(코드 채택)의 외부 선행을 검증 가능한 조건으로 바꾼다. 외부 LICENSE 반영 전에는 두 앱이 규칙 문서·`tokens.json` 참조까지만 한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-16(concierge·ktdm은 L8 전 규칙 문서·`tokens.json` 참조까지만), D-17(ktc·ktdm 루트 GPL 정렬 권고, §7 추가 허가 기각), O-2 채택값.
- ADR-004 — [docs/adr/README.md](../adr/README.md).
- [라이선스 조사](../survey/cross/licensing.md) §3.6 ktc·ktdm 행(판단 근거·"같은 소유자니까 된다"는 성립하지 않음), §3.7 L8·L14, §4 B4(ktc `AppShell.tsx`·`globals.css` 복사 여부 diff 후 기록).
- [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1 concierge PR 3·ktdm PR 3(L8 = 사용자).
- [concierge 인벤토리](../survey/inventory/kor-travel-concierge.md) §8·§9, [docker-manager 인벤토리](../survey/inventory/kor-travel-docker-manager.md) §8·§9.

## 구현 범위

1. 결정 기록: `docs/architecture/adoption-readiness.md` gate 표의 ktc·ktdm L8 행에 결정 일자·채택값·근거; ADR-004 "결과" 절에 1줄 보충. ktdm은 "코드 미링크·규칙 문서만 참조 시 MIT 유지 가능(추정)" 대안을 함께 적는다.
2. 요청 문서 2편 `docs/plan/requests/concierge-license-l8.md`, `docs/plan/requests/docker-manager-license-l8.md`: 대상 저장소, 브랜치 `agent/<agent>-license-l8`, **LICENSE·metadata·고지만 다루는 독립 PR** 범위(루트 `LICENSE` GPL 전문, `package.json`·`pyproject.toml` `license` 필드, MIT 유래 파일 고지를 `THIRD_PARTY_NOTICES`로, ktc 저작권자 문구 통일 L14), common 코드 링크를 넣지 않는다는 경계, 되돌리기 `git revert` 1회, 인벤토리 §8/§9·판정 §3.1 링크.
3. 외부 license-only PR이 머지되면 요청 문서와 이 task의 ktc·ktdm 행에 PR URL·40자리 `main` merge SHA·LICENSE 첫 줄·CI/license 검사 결과를 기록한다. 이 common task의 결정 완료와 외부 evidence는 별도 상태다.
4. B4 처리: ktc `AppShell.tsx`·`globals.css`와 map admin 원본의 diff 결과(복사/개념 참조)는 후속 T-454 코드 채택 PR과 그 evidence에 기록한다. license-only PR이나 이 common task 완료가 B4 결과를 대신하지 않는다.
5. 외부 license evidence가 기록되면 G-LIC gate를 해제할 수 있으며, T-453·T-454·T-472·T-473·T-485·T-486의 코드 채택 상태 전환은 각 원장 작성자가 수행한다.

## 범위 밖

- 두 저장소 직접 수정, §7 추가 허가 문안 작성(기각), 코드 채택 자체(T-453·T-454·T-472·T-473), 라이선스 법률 자문.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/plan/requests/concierge-license-l8.md`, `docs/plan/requests/docker-manager-license-l8.md`, `docs/architecture/adoption-readiness.md`, `docs/adr/004-*.md`(1줄 보충), `docs/journal.md`.

## 수용 기준

- 결정 기록에 일자·선택지(정렬/추가 허가)·채택값·근거가 있고 기본값 진행 상태와 확정 상태가 구분된다.
- 요청 문서 2편이 대상 파일 경로·되돌리기·인벤토리 §8/§9·판정 §3.1 링크·license-only 경계를 포함하고, 외부 evidence 기록 형식을 정의한다.
- 외부 evidence가 저장소별 PR URL·40자리 커밋 SHA + `LICENSE` 첫 줄·검사 결과로 검증 가능하다. B4 diff는 후속 코드 채택 evidence로 별도 기록한다.
- 해제 전 `docs/standards/*`·runbook의 concierge·ktdm 절이 "규칙 문서·`tokens.json` 참조까지"로만 적혀 있다.
- validator 오류 0.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -n "L8" docs/architecture/adoption-readiness.md
ls docs/plan/requests/
```

Git Bash에서 동일. B4 diff는 조사 저장소 읽기 전용 체크아웃에서 `diff` 명령으로 수행한다.

## evidence

- 사용자 결정과 각 저장소 LICENSE-only PR 요청 문서를 이 task에 기록했다. 실제 license-only PR 링크·해제 SHA·LICENSE 첫 줄·검사 결과는 이 task의 소비자별 external evidence 행에 기록하고, B4 diff·코드 채택 evidence는 T-454·T-473에서 별도로 연결한다. 반영 전까지 G-LIC를 OPEN으로 유지한다.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- L8 해제 기록 없이 concierge·ktdm 코드 채택 PR(T-453·T-454·T-472·T-473·T-485·T-486)이 열리면 common 측에서 승인하지 않는다. LICENSE-only PR은 이 선행을 만들기 위한 독립 외부 작업으로 허용한다.

## 사용자 결정 반영(2026-09-08)

사용자는 “t020 021 관련해서 모두 gplv3로 바꿀꺼야 참고해서 이번에 한번에 닫아”라고 지시했다. 이에 O-2를 **concierge·docker-manager 루트 GPL-3.0-or-later 정렬, GPLv3 §7 추가 허가 없음**으로 확정하고 common 안에서 결정 기록과 두 요청 문서를 완료했다.

- 요청 문서: [concierge-license-l8.md](../plan/requests/concierge-license-l8.md), [docker-manager-license-l8.md](../plan/requests/docker-manager-license-l8.md)
- common은 두 소비자 저장소를 수정하지 않았고 실제 LICENSE·metadata·고지 반영은 concierge·docker-manager 외부 PR에서 수행하고 T-454·T-473 evidence로 남긴다.
- G-LIC의 ktc·ktdm 적용 gate는 각 외부 PR의 40자리 SHA·LICENSE 첫 줄·자체 검증 evidence를 받을 때까지 OPEN이다.
- T-021의 DONE은 라이선스 결정·요청 문서 gate를 닫았다는 뜻이며 소비자 코드 링크 gate를 닫았다는 뜻이 아니다.

## 외부 evidence(현재 OPEN)

| 소비자 | license-only PR | main merge SHA·LICENSE 첫 줄·검사 | 후속 코드 채택 |
|---|---|---|---|
| concierge | `NOT_RUN(소비자 저장소 외부 작업)` | `OPEN` | T-453·T-454·T-485 |
| docker-manager | `NOT_RUN(소비자 저장소 외부 작업)` | `OPEN` | T-472·T-473·T-486 |

이 표의 `OPEN`은 common 결정이 미완료라는 뜻이 아니라 소비자 저장소에서 아직 증거를 받지 못했다는 뜻이다. license-only PR과 후속 코드 채택 PR은 서로 다른 선행으로 기록한다.
