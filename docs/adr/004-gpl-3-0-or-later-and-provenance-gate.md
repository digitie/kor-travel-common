# ADR-004: 라이선스 GPL-3.0-or-later와 출처 고지·추출 gate

- 상태: accepted
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-17·O-1·O-2·O-20, `docs/survey/cross/licensing.md` §2.1~§2.5·§3.1~§3.7·§4·§6, `docs/survey/commonality-matrix.md` §4.1 B1~B10, `docs/survey/README.md` §6.2 항목 8~11

## 컨텍스트

사용자는 common을 GPL-3로 지시했다(지시 (6)). 조사 결과 소비자 라이선스는 갈라져 있다: map·weather·airport·geo는 GPL(단, map은 25행 요약본, airport는 버전 미지정, geo는 `-only`), ktc·ktdm은 MIT, pinvi는 루트 `LICENSE`가 없고 README "비공개"와 AGENTS "공개"가 상충하며 `apps/api`만 MIT다(`lic` §2.1·§2.2). common으로 옮길 후보 파일은 map 유래(GPL), shadcn 생성물(MIT), cva(Apache-2.0), pinvi 이식본(원천 GPL이나 pinvi 자체 선언 미결), 벤더 tgz(`vworld-map-*`, 라이선스 표기 없음), Hallmark 스킬(저작자 미확인)이 섞여 있다. GPL 라이브러리를 링크한 프로그램은 배포 시 전체가 GPL이어야 하므로(`gpl-faq #IfLibraryIsGPL`) MIT 앱이 common 코드를 소비하려면 정렬 결정이 필요하다. 어떤 저장소에도 SPDX 헤더가 없다.

## 결정

1. common은 `GPL-3.0-or-later`다. 루트 `LICENSE` 전문 외에 `NOTICE`(저작권자 `Youn-sok Choi (digitie)`·버전·연락처), `THIRD_PARTY_NOTICES.md`(shadcn/ui MIT·@base-ui/react MIT·radix MIT·class-variance-authority Apache-2.0(NOTICE 유지)·lucide ISC·tailwind-merge/clsx/tw-animate-css MIT·maplibre-gl BSD-3·pretendard OFL-1.1·TanStack MIT·zod MIT — 버전·URL), `LICENSES/`(SPDX 파일명 원문), `PROVENANCE.md`(파일군·원천 저장소·커밋·경로·라이선스·수정), `CONTRIBUTING.md`(AI 보조 생성물은 권리자가 GPL로 배포)를 둔다.
2. 파일 헤더는 `SPDX-License-Identifier: GPL-3.0-or-later` + `SPDX-FileCopyrightText`에 `Origin:`/`Derived-From:`/`Modified:` 행을 더한다. `tools/check_spdx.py`가 common 파일에서 헤더 부재를 즉시 fail로 잡는다. Hallmark 스탬프는 common 파일에 두지 않는다(SPDX만).
3. 추출 규칙: GPL 원천(map·weather·airport)은 그대로; geo `-only` 유래는 `-only`를 병기(권리자 재선언 시 `-or-later`, O-20); MIT 원천(ktc·ktdm)은 고지 보존; pinvi는 L6 전 추출 금지(B1); 벤더 tgz·`maplibre-vworld-*`·`python-*-api`는 영구 금지(B2, 의존만); Hallmark SKILL 본문 인용 금지(B3, 스탬프 형식만); ktc AppShell은 map 코드 복사 여부를 diff로 확정 후(B4); shadcn 생성물은 MIT 고지(B6); 봇 커밋분은 CONTRIBUTING 문구(B8).
4. 패키지 메타데이터: npm `license: "GPL-3.0-or-later"`, tarball에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉; Python `license = "GPL-3.0-or-later"` + PEP 639 `license-files`.
5. 소비 앱 정렬 권고: ktc·ktdm 루트 `GPL-3.0-or-later` 정렬(common §7 추가 허가는 기각, O-2); pinvi는 공개 + GPL-3.0-or-later로 common 결정을 완료하고 실제 반영을 T-420 외부 확인으로 둔다(O-1); map `LICENSE` 전문 복원(L9); 전 앱 `license` 필드(L11); pg-aiguide 스킬은 common이 배포하지 않는다(L12).
6. 앱 사본 drift 비교는 선두 주석 블록(SPDX·Origin·Hallmark)을 정규화한 뒤 수행한다.

## 대안 검토

- **common §7 추가 허가로 MIT 앱 링크 허용**: 가능하지만 common 모든 파일에 예외 문구를 유지·검증하는 비용이 크고 "GPL common" 전제와 어긋난다. 7개 중 5개가 이미 GPL이므로 정렬이 단순하다(`lic` §3.6).
- **헤더 없이 `PROVENANCE.md`만**: 파일 단위 수정 고지(GPLv3 §5(a))와 앱 사본 drift 비교에 불리하다. shadcn CLI 재생성이 헤더를 지우므로 소스 소유 방식과 함께 헤더를 채택했다.
- **pinvi 이식본을 "원천이 GPL이니 바로 추출"**: 원천은 GPL이지만 pinvi 수정분의 선언이 미결이고 저장소 고지가 모순이라 수령자 권리가 불명확하다. L6 전에는 금지한다.

## 결과

- 고지 파일·헤더·메타데이터가 갖춰져 tarball·wheel 수령자가 권리를 판단할 수 있다.
- pinvi·ktc·ktdm 코드 채택은 common 결정과 각 소비자 LICENSE evidence에 종속되며, evidence 전에는 규칙 문서·`tokens.json` 참조까지만 허용한다(ADR-010).
- geo 유래 파일에 `-only` 병기가 남는 동안 해당 파일의 결합물은 사실상 v3-only다.
- `check_spdx.py`가 CI에 들어가면 헤더 없는 파일은 머지되지 않는다.

## 후속·적용 위치

- 고지 파일: `NOTICE`, `THIRD_PARTY_NOTICES.md`, `PROVENANCE.md`, `CONTRIBUTING.md`, `LICENSES/`(T-003; `check_spdx.py`·`LICENSES/` 원문은 잔여)
- 규칙: `docs/standards/licensing.md`
- 외부 확인: T-420(pinvi L6), T-454·T-473(ktc·ktdm L8 evidence), T-410(map L9·`license` 필드)
- 패키지 실물: T-101·T-201·T-302(메타데이터 적용)

## 후속 결정(2026-09-08)

사용자는 T-020·T-021에 대해 모든 라이브러리를 GPLv3로 통일하라고 지시했다. 이에 O-1은 공개 pinvi + GPL-3.0-or-later, O-2는 concierge·docker-manager 루트 GPL-3.0-or-later 정렬과 GPLv3 §7 추가 허가 없음으로 닫았다. common은 [pinvi 요청](../plan/requests/pinvi-license-l6.md), [concierge 요청](../plan/requests/concierge-license-l8.md), [docker-manager 요청](../plan/requests/docker-manager-license-l8.md)을 작성했지만 소비자 저장소는 수정하지 않았다. 실제 반영은 pinvi T-420과 concierge·docker-manager의 외부 PR evidence(T-454·T-473에서 링크)에서 LICENSE 첫 줄, 40자리 SHA, 자체 검증 evidence를 확인한 뒤 G-LIC gate를 닫는다.
