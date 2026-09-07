# kor-travel-docker-manager 라이선스 정렬 요청(L8)

- 결정 상태: **common 결정 완료, docker-manager 저장소 반영 대기**
- 결정일: 2026-09-08
- 대상: kor-travel-docker-manager 공개 배포 기준
- common 기준: GPLv3 계열의 정본 표기는 GPL-3.0-or-later다.

사용자 지시인 “t020 021 관련해서 모두 gplv3로 바꿀꺼야 참고해서 이번에 한번에 닫아”에 따라 docker-manager 루트 라이선스를 GPL-3.0-or-later로 정렬한다. §7 추가 허가는 두지 않는다. 규칙 문서만 참조하는 동안에는 외부 gate를 열지 않지만 common 코드 링크 전에는 정렬 PR이 필요하다. 이 문서는 common의 결정·요청 기록이며 docker-manager 저장소를 직접 수정하지 않는다.

## 대상 외부 PR(라이선스만)

docker-manager에서 agent/<agent>-license-l8 branch로 LICENSE·metadata·고지만 다루는 PR을 만든다. common 코드 링크·tokens/ui/py 채택은 이 PR에 넣지 않고 T-472·T-473·T-486 후속으로 분리한다.

1. 루트 LICENSE를 GPL-3.0 전문으로 교체한다.
2. package.json·pyproject.toml 등 실제 metadata가 있으면 license를 GPL-3.0-or-later로 명시한다.
3. MIT 원천 파일과 서드파티 저작권·허가문은 THIRD_PARTY_NOTICES로 보존한다.
4. 이 LICENSE-only PR에는 common 토큰·UI·Python 코드 링크를 넣지 않는다. 코드 채택은 L8 evidence 이후 T-472·T-473·T-486에서 별도로 수행한다.
5. PR의 LICENSE·metadata·고지 검증 결과와 되돌리기 명령을 기록한다.

## 외부 evidence 기록

외부 PR이 머지되면 이 요청 문서와 [T-021](../../tasks/T-021-ktc-ktdm-license-l8.md)의 ktdm 행에 PR URL, 40자리 main merge SHA, LICENSE 첫 줄, CI·license 검사 결과를 기록한다. 기록 전 G-LIC는 OPEN이다.

## 해제 조건

docker-manager 담당 PR에서 다음을 확인한 40자리 commit SHA와 CI/evidence 링크를 common의 T-473 선행 evidence에 기록한다.

- 루트 LICENSE가 GPL-3.0-or-later와 호환되는 GPLv3 전문임
- metadata·고지 파일·서드파티 고지가 일치함
- common 코드 링크와 함께 필요한 provenance가 기록됨
- 소비자 build/quality 검증 결과가 기록됨

외부 PR과 SHA가 없으면 G-LIC의 docker-manager 적용 gate는 OPEN으로 유지한다. common은 docker-manager 코드를 복사하거나 수정하지 않는다. 되돌리기는 해당 저장소에서 git revert 1회로 수행한다.

관련: [T-021](../../tasks/T-021-ktc-ktdm-license-l8.md), [T-472](../../tasks/T-472-ktdm-tokens-adoption.md), [T-473](../../tasks/T-473-ktdm-ui-partial.md), [T-486](../../tasks/T-486-ktdm-py-second.md), [docker-manager 인벤토리 §8·§9](../../survey/inventory/kor-travel-docker-manager.md), [이관 판정 §3.1](../../plan/design-panel/judge-migration-feasibility.md), [라이선스 표준](../../standards/licensing.md), [ADR-004](../../adr/004-gpl-3-0-or-later-and-provenance-gate.md)
