# pinvi 라이선스 정렬 요청(L6)

- 결정 상태: **common 결정 완료, pinvi 저장소 반영 대기**
- 결정일: 2026-09-08
- 대상: pinvi 저장소의 공개 배포 기준
- common 기준: GPLv3 계열의 정본 표기는 GPL-3.0-or-later다.

사용자 지시인 “t020 021 관련해서 모두 gplv3로 바꿀꺼야 참고해서 이번에 한번에 닫아”에 따라 pinvi는 공개 배포를 유지하고 루트 라이선스를 GPL-3.0-or-later로 정렬한다. 이 문서는 common의 결정·요청 기록이며 pinvi 저장소를 직접 수정하거나 외부 gate를 통과한 것으로 표시하지 않는다.

## 대상 외부 PR(라이선스만)

pinvi에서 agent/<agent>-license-l6 branch로 LICENSE·metadata·고지만 다루는 PR을 만든다. common 코드 링크·tokens/ui/py 채택은 이 PR에 넣지 않고 T-420 후속으로 분리한다.

1. 루트 LICENSE를 GPL-3.0 전문으로 추가한다.
2. README와 AGENTS의 공개/비공개 문구를 공개 GPL 배포와 일치시킨다.
3. apps/api/pyproject.toml의 license를 GPL-3.0-or-later로 바꾼다.
4. docs/integrations/maplibre-vworld.md의 MIT 표기를 실제 원천 고지와 GPL 정책에 맞게 고친다.
5. map 이식 파일과 수정분의 Origin·Derived-From·Modified·NOTICE 고지를 보존한다.
6. GPL 코드를 사내 전용으로 표시하는 문구를 남기지 않는다.

## 외부 evidence 기록

외부 PR이 머지되면 이 요청 문서와 [T-420](../../tasks/T-420-pinvi-license-l6.md)에 PR URL, 40자리 main merge SHA, LICENSE 첫 줄, CI·license 검사 결과를 기록한다. 기록 전 G-LIC는 OPEN이다.

## 해제 조건

pinvi 담당 PR에서 다음을 확인한 40자리 commit SHA와 CI/evidence 링크를 common의 T-420에 기록한다.

- 루트 LICENSE 첫 줄이 GPL-3.0-or-later와 호환되는 GPLv3 전문임
- README·AGENTS·apps/api/pyproject.toml·maplibre 문서의 라이선스 표기가 서로 일치함
- pinvi 수정분과 제3자 고지가 누락되지 않음
- 소비자 build/e2e와 저장소의 자체 license 검사 결과가 기록됨

외부 PR과 SHA가 없으면 G-LIC의 pinvi 적용 gate는 OPEN으로 유지한다. common의 PROVENANCE에는 pinvi 유래 코드 행을 추가하지 않는다. 되돌리기는 해당 저장소에서 git revert 1회로 수행한다.

관련: [T-020](../../tasks/T-020-pinvi-license-l6.md), [T-420](../../tasks/T-420-pinvi-license-l6.md), [pinvi 인벤토리 §8·§9](../../survey/inventory/pinvi.md), [이관 판정 §3.1](../../plan/design-panel/judge-migration-feasibility.md), [라이선스 표준](../../standards/licensing.md), [ADR-004](../../adr/004-gpl-3-0-or-later-and-provenance-gate.md)
