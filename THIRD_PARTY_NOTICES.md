# THIRD_PARTY_NOTICES

이 문서는 kor-travel-common이 의존하거나 파생한 서드파티 구성요소의 라이선스 고지 목록이다(브리프 D-17, ADR-004; 근거 `docs/survey/cross/licensing.md` §2.4·§3.3). 확정 task는 T-003(★이번 PR; 라이선스 원문 사본 `LICENSES/`와 `tools/check_spdx.py`는 잔여). 배포되는 tarball·wheel에 `LICENSE`·`NOTICE`와 함께 동봉한다. 마지막 갱신 2026-09-06.

## 규칙

- 구성요소를 새로 의존하거나 코드를 파생할 때 이 표에 행을 추가하고, 라이선스 원문 사본을 `LICENSES/<SPDX-ID>.txt`에 둔다(REUSE 관행; 원문 확보는 T-003 잔여).
- 파생 코드(shadcn/ui 레시피, lucide SVG 등)는 파일 헤더에 `Derived-From:` 행을 두고 이 문서를 가리킨다([CONTRIBUTING §2](CONTRIBUTING.md)).
- 버전은 조사 기준(2026-09-06, `docs/survey/cross/version-matrix.md` §1.3~§1.5·§4.2)의 소비자 설치 버전 또는 최신 안정 버전이며, common 패키지의 실제 의존 버전은 각 `package.json`·`uv.lock`이 정본이다. 패키지 실물이 생기면 이 표를 lock과 대조한다.
- 원문 URL은 각 프로젝트 저장소의 라이선스 파일 경로다. "미확인"으로 표시한 URL은 T-003에서 원문 사본을 받을 때 검증한다.
- 소비 앱이 직접 쓰는 의존성(예: `sonner`, `recharts`, `next-intl`)은 앱의 책임이며 여기에 적지 않는다. 벤더 tgz·`maplibre-vworld-*`·`python-*-api`·Hallmark 스킬 본문은 common에 포함하지 않으므로 고지 대상이 아니다(D-17 B2·B3).

## 목록

| 구성요소 | 버전(2026-09-06 기준) | 라이선스(SPDX) | 원문 URL | 원문 사본(`LICENSES/`, T-003 잔여) | common과의 관계 | 고지 의무 요지 |
|---|---|---|---|---|---|---|
| shadcn/ui | CLI 4.21.0(레시피 생성 시점 버전은 미기록, licensing B6) | MIT | `https://github.com/shadcn-ui/ui/blob/main/LICENSE.md`(미확인) | `LICENSES/MIT.txt` | `packages/ui` 컴포넌트 레시피의 파생 원천(`Derived-From`) | 저작권·허가문 유지 |
| @base-ui/react | 1.8.0 | MIT | `https://github.com/mui/base-ui/blob/master/LICENSE`(미확인) | `LICENSES/MIT.txt` | `packages/ui` peer(overlay 프리미티브만, D-09) | 저작권·허가문 유지 |
| radix-ui / @radix-ui/* | 1.6.0(geo 설치), 최신 1.6.7 | MIT | `https://github.com/radix-ui/primitives/blob/main/LICENSE`(미확인) | `LICENSES/MIT.txt` | 직접 의존 없음. geo 유래 레시피를 참조할 때 파생 원천 | 저작권·허가문 유지 |
| class-variance-authority | 0.7.1 | Apache-2.0 | `https://github.com/joe-bell/cva/blob/main/LICENSE`(2026-09-06 확인: 파일명 `LICENSE`, 저장소에 `NOTICE` 파일 없음) | `LICENSES/Apache-2.0.txt` | `packages/ui` 의존 | LICENSE 사본 제공(§4(a)). §4(d) NOTICE 유지 의무는 원천에 NOTICE가 없어 현재 해당 없음; 상향 시 재확인 |
| lucide (lucide-react·lucide-static) | 1.41.0(최신; 소비자 0.363~1.27) | ISC | `https://github.com/lucide-icons/lucide/blob/main/LICENSE`(미확인) | `LICENSES/ISC.txt` | `packages/ui`가 아이콘을 인라인 SVG로 가져 peer 없음(D-01) — SVG 파생 | 저작권·허가문 유지 |
| tailwind-merge | 3.6.0 | MIT | `https://github.com/dcastil/tailwind-merge/blob/main/LICENSE.md`(미확인) | `LICENSES/MIT.txt` | `@kor-travel/ui/cn` 의존(`extendTailwindMerge`) | 저작권·허가문 유지 |
| clsx | 2.1.1 | MIT | `https://github.com/lukeed/clsx/blob/master/license`(미확인) | `LICENSES/MIT.txt` | `@kor-travel/ui/cn` 의존 | 저작권·허가문 유지 |
| tw-animate-css | 1.4.0 | MIT | `https://github.com/Wombosvideo/tw-animate-css/blob/main/LICENSE`(미확인) | `LICENSES/MIT.txt` | `packages/ui` 애니메이션 유틸(채택 여부는 T-201) | 저작권·허가문 유지 |
| maplibre-gl | 5.24.0(소비자), floor 5.24 | BSD-3-Clause | `https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt`(미확인) | `LICENSES/BSD-3-Clause.txt` | common 직접 의존 없음. `versions.json` peer 정합 대상 | 저작권·허가문 유지, 이름 홍보 금지 조항 |
| Pretendard | 1.3.9 | OFL-1.1 | `https://github.com/orioncactus/pretendard/blob/main/LICENSE`(미확인) | `LICENSES/OFL-1.1.txt` | 토큰 font 스택 1순위 이름만 참조. 폰트 파일은 배포하지 않으며 로딩은 앱 책임(D-12) | 폰트 파일을 배포하는 쪽이 OFL 사본 동봉·Reserved Font Name 준수 |
| TanStack Table | 8.21.3(9.x는 breaking 미조사) | MIT | `https://github.com/TanStack/table/blob/main/LICENSE`(미확인) | `LICENSES/MIT.txt` | `packages/ui` DataTable 의존 | 저작권·허가문 유지 |
| TanStack Virtual | 3.14.x | MIT | `https://github.com/TanStack/virtual/blob/main/LICENSE`(미확인) | `LICENSES/MIT.txt` | `packages/ui` DataTable 가상화 의존 | 저작권·허가문 유지 |
| zod | 4.5.x | MIT | `https://github.com/colinhacks/zod/blob/main/LICENSE`(미확인) | `LICENSES/MIT.txt` | `packages/ui` form-validation(헤드리스) 의존 후보(T-210) | 저작권·허가문 유지 |
| canview(구조 참조) | `1f93b8a` | GPL-3.0(버전 미지정 원문) | `https://github.com/digitie/canview` | `LICENSES/GPL-3.0-or-later.txt`(= 루트 `LICENSE`) | 문서 구조·validator 2종·runbook 형식의 원천(같은 저작권자). 파일 단위 기록은 [PROVENANCE](PROVENANCE.md) | GPL 고지 유지; common에서 `-or-later`로 재선언(권리자 동일) |

`LICENSES/` 사본 열은 백틱 경로다(파일은 T-003 잔여에서 만들며 그 전까지는 링크로 만들지 않는다). 사본이 생기면 링크로 바꾸고 `tools/validate_document_links.py`로 확인한다.

## 고지하지 않는 것(의도적 제외)

| 항목 | 이유 |
|---|---|
| `python-*-api`(digitie), `python-kraddr-base`, `maplibre-vworld-react/js` | common은 의존만 하거나 의존하지 않는다(중복 금지, D-01·D-23). 소비 앱의 lock에 나타나며 앱이 고지한다 |
| pg-aiguide 스킬(Apache-2.0) | common이 배포하지 않는다(D-17 L12; 각 앱 책임) |
| Hallmark 스킬 본문 | 출처·라이선스 미확인, common 파일에 스탬프·인용 없음(D-17 B3) |
| TypeScript, Tailwind CSS, Next.js, React, Vitest, Playwright, FastAPI, pydantic 등 빌드 도구·peer 프레임워크 | 산출물에 코드가 포함되지 않거나 소비 앱이 설치하는 peer다. `packages/*`가 실제로 번들하는 항목이 생기면 추가한다 |
