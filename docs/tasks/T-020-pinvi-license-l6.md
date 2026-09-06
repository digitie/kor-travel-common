# T-020 pinvi 라이선스 결정(L6) 반영: 결정 기록·pinvi PR 요청 문서·common 소비 gate 해제 조건

- 상태: BLOCKED
- 우선순위: P0
- Gate: 문서
- 선행: 없음
- 외부 선행: 사용자 결정 O-1(pinvi 공개 여부·라이선스). 기본값 "공개 + GPL-3.0-or-later, 1 PR"로 문서를 준비하되 확정 기록은 사용자 답이 있어야 한다.

## 목표

pinvi 전 트랙(T-420·T-421·T-422·T-484, ui 1차 T-212의 pinvi 경로)을 여는 유일한 조건 L6를 결정 기록·요청 문서·검증 가능한 해제 조건으로 정리한다. 결정 전에는 pinvi 유래 코드가 common에 들어오지 않도록 gate를 유지한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-16(L6를 Phase 0 외부 확인으로 승격; L6 미결 시 ui 1차는 airport 소형 부품으로 대체), D-17(B1: pinvi는 L6 전 추출 금지), O-1 기본값.
- ADR-004·ADR-010 — [docs/adr/README.md](../adr/README.md).
- [라이선스 조사](../survey/cross/licensing.md) §2.3 P1(map 이식 50파일, GPL 원천), §3.6 pinvi 행(공개 유지 시 GPL 채택 + 루트 `LICENSE` + `apps/api/pyproject.toml` MIT 수정 + `docs/integrations/maplibre-vworld.md:23` 정정; 사유 유지 시 GPL 코드 제거), §3.7 L6, §4 B1.
- [판정 보고서](../plan/design-panel/judge-migration-feasibility.md) §3.1 pinvi admin PR 0(3파일, 사용자 결정 O-1).
- [pinvi 인벤토리](../survey/inventory/pinvi.md) §8·§9(공통화 후보·고유 차이), 정정값 pinvi admin ui 28파일([조사 안내](../survey/README.md) §6.2 항목 1).

## 구현 범위

1. 결정 기록: `docs/architecture/adoption-readiness.md` gate 표의 pinvi L6 행에 결정 일자·내용·근거(사용자 답 인용) 기입, ADR-010 "정본과 수용 조건" 절에 1줄 보충(뒤집히면 새 ADR). 두 선택지(공개 GPL / 사내 비공개)와 각 경우의 common 영향(비공개면 pinvi 트랙 취소·ui 1차 airport 대체)을 명시.
2. 요청 문서 `docs/plan/requests/pinvi-license-l6.md`: 대상 저장소 pinvi, 브랜치 `agent/<agent>-license-l6`, 1 PR 범위(루트 `LICENSE` GPL 전문, README/AGENTS 공개·사내 문구 정합, `apps/api/pyproject.toml` `license`, `docs/integrations/maplibre-vworld.md:23` 정정, map 이식분 출처 고지), 되돌리기 `git revert` 1회, 인벤토리 §8/§9 링크, 판정 §3.1 PR 순서 링크.
3. 결정·요청 문서와 두 리뷰어 gate가 완료되면 T-020을 DONE으로, T-420을 READY로 전환한다. 이 시점의 L6는 "결정 완료·실제 반영 대기"다. T-420의 pinvi merge SHA·LICENSE·공개 문구·패키지 필드 정합 evidence를 확인한 뒤에만 소비·추출 gate를 해제한다. 그 전에는 PROVENANCE의 pinvi 유래 행 0을 유지한다([ADR-013](../adr/013-package-release-execution-contract.md)).

## 범위 밖

- pinvi 저장소 직접 수정(T-420이 pinvi 쪽 PR), pinvi 사용자 웹·모바일 코드 소비(D-29), 벤더 tgz·`maplibre-vworld-*` 취급(B2 영구 금지).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `docs/plan/requests/pinvi-license-l6.md`, `docs/architecture/adoption-readiness.md`, `docs/adr/010-*.md`(1줄 보충), `docs/journal.md`.

## 수용 기준

- 결정 기록에 일자·선택지·채택값·근거(사용자 답 원문 또는 요약)가 있고 "기본값으로 진행" 상태와 "확정" 상태가 구분된다.
- 요청 문서가 대상 파일 4개의 경로를 정확히 적고 되돌리기 방법·인벤토리·판정 링크를 포함한다.
- 해제 조건이 커밋 SHA + `LICENSE` 첫 줄 검사로 검증 가능하게 적혀 있다.
- 해제 전 PROVENANCE 표의 원천 저장소가 pinvi인 행이 0건이다. 금지 규칙 설명에 있는 단어를 추출 행으로 세지 않는다.
- validator 오류 0, 운영 정보 없음.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
rg -n "pinvi" PROVENANCE.md || echo "no pinvi provenance rows"
rg -n "L6" docs/architecture/adoption-readiness.md
```

Git Bash에서 동일.

## evidence

- 이 task는 사용자 답·결정·요청 문서를 기록한다. pinvi PR·실제 해제 SHA는 T-420 evidence로 연결하며 T-020 완료 조건에 넣지 않는다. 답이 없으면 `NOT_RUN(사용자 O-1 대기)`.

## rollback 또는 release 차단 조건

- 문서만 바뀌므로 `git revert` 1회로 원복한다.
- L6 해제 기록 없이 pinvi 유래 파일이 `packages/*`나 `PROVENANCE.md`에 들어오면 즉시 revert하고 관련 릴리스(T-212·T-213)를 차단한다.
