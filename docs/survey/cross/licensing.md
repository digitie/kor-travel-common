# 횡단 비교 — 라이선스·코드 출처 검토

작성일 2026-09-06. 읽기 전용 조사. 이 문서는 GPL-3.0 `kor-travel-common`으로 코드·규칙을 추출·배포할 때의 라이선스와 출처 문제를 정리한다. 법률 자문이 아니며, 각 판단은 GNU 공식 FAQ·라이선스 원문과 저장소의 실제 파일을 근거로 한 조사 결과다. 표기 규칙: **사실**(파일에서 직접 확인) / **후보**(선택지) / **추정**(근거는 있으나 확인 불완전) / **미확인**(확인하지 못함).

## 0. 기준

| 저장소 | 경로 | 기준 커밋 | 루트 `LICENSE` | 비고 |
|---|---|---|---|---|
| kor-travel-airport (kta) | `F:/dev/kor-travel-common-survey/kta-main` | `2bb1111` | GPL-3.0 원문 674행 | 작업 트리 clean |
| kor-travel-concierge (ktc) | `F:/dev/kor-travel-concierge` | `7945305` | MIT 21행 | |
| kor-travel-docker-manager (ktdm) | `F:/dev/kor-travel-common-survey/ktdm-main` | `862562d` | MIT 21행 | |
| kor-travel-geo (geo) | `F:/dev/kor-travel-geo-fixes` | `1d9d74d` | GPL-3.0 원문 674행 | |
| kor-travel-map (map) | `F:/dev/kor-travel-common-survey/ktm-main` | `c494e227` | **25행 요약본**(§2.2) | npm workspaces |
| kor-travel-weather (weather) | `F:/dev/kor-travel-weather` | `6003da9` | GPL-3.0 원문 674행 | |
| pinvi | `F:/dev/kor-travel-common-survey/pinvi` | `9af25e5` | **없음** | 단일 커밋 스냅샷 |
| canview (구조 참조) | `F:/dev/canview` | `1f93b8a` | GPL-3.0 원문 674행 | `dbc/opendbc/LICENSE` MIT 동봉 |
| kor-travel-common (새 저장소) | `F:/dev/kor-travel-common` | `b92fabe` | GPL-3.0 원문 674행 | 추적 파일이 `LICENSE` 하나뿐 |
| maplibre-vworld-react (기존 공유 lib) | `F:/dev/maplibre-vworld-react` | `95b49d3` | GPL-3.0 원문 674행 | pinvi 벤더 tgz 원천 |
| maplibre-vworld-js (기존 공유 lib) | `F:/dev/maplibre-vworld-js` | `2a13ce0` | MIT 21행 | `package.json`은 `ISC`(§2.2) |

## 1. 방법

실행한 읽기 명령(조사 대상 저장소에는 아무것도 쓰지 않았다):

- 루트 라이선스: `git rev-parse --short HEAD`, `ls`, `head/tail LICENSE`, `grep -c '<name of author>' LICENSE`(GPL "How to Apply" 자리표시자 잔존 여부), `git log -- LICENSE`.
- 패키지 메타데이터: `git ls-files | grep package.json` 후 `license`/`private`/`author` 필드 grep, `pyproject.toml`의 `license`/`classifiers` grep, `setup.py`/`requirements.txt` 존재 확인.
- 잠금 파일: Python으로 각 `package-lock.json`의 `packages[*].license`/`resolved`를 읽어 주요 UI 의존성의 라이선스를 추출(설치본 node_modules는 읽지 않음).
- 벤더 tgz: `tar -tzf`로 목록, `tar -xzOf <tgz> package/package.json`으로 표준출력에만 내용을 읽음(디스크 추출 없음).
- 출처 주석: `git grep`으로 `shadcn`, `Hallmark`, `SPDX`, `Copyright`, `이식`, `copied from`, `Origin:` 등을 소스(`*.ts *.tsx *.py *.css`)에서 검색하고 파일 첫 줄을 집계.
- 벤더링 스킬: `.agents/.claude/.codex/.opencode/.hallmark` 추적 파일 목록, `SKILL.md`의 `원본:`/`라이선스:` 행, 사용자 홈의 Hallmark 스킬 위치(`C:/Users/digit/.agents/skills/hallmark`, 심볼릭 링크 `~/.claude/skills/hallmark`).
- 기여자: `git shortlog -sne HEAD`.
- 네트워크(WebFetch, 2026-09-06): GNU GPL FAQ(`https://www.gnu.org/licenses/gpl-faq.en.html`) 앵커 확인, GitHub 저장소 페이지의 라이선스 표시 확인 — `timescale/pg-aiguide`(Apache-2.0), `digitie/python-kraddr-base`(GPL-3.0), `digitie/python-kma-api`(GPL-3.0-or-later), `digitie/python-vworld-api`(GPL-3.0), `digitie/python-kasi-api`(GPL-3.0-or-later). 그 외 python-*-api 저장소는 미확인.
- 선행 문서: `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` §9, `docs/survey/inventory/*.md`의 라이선스 행, `docs/survey/cross/backend.md` §(라이선스 행), `docs/survey/cross/ui-components.md` §2.3·§6.1·80행.

## 2. 산출 (1) — 저장소×파일군 출처/라이선스 표

### 2.1 저장소 단위 선언 현황(사실)

| 저장소 | 루트 `LICENSE` | npm `license` 필드 | Python `license`/classifier | README 라이선스 절 | 판정 |
|---|---|---|---|---|---|
| kta | GPL-3.0 원문(자리표시자 2곳 미기입, 저작권자 행 없음) | `frontend/package.json` 없음(`private: true`) | `backend/pyproject.toml` 없음 | 없음 | 파일은 GPL-3.0, 메타데이터 미표기 |
| ktc | MIT, `Copyright (c) 2026 kor-travel-concierge contributors` | `frontend/package.json`·`tests/package.json` 없음 | `backend/requirements.txt`만 존재, pyproject 없음 | `README.md:203-205` "MIT License" | MIT 일관, 단 GPL 의존성 보유(§2.4) |
| ktdm | MIT, `Copyright (c) 2026 Youn-sok Choi` | `frontend/package.json` 없음 | `backend/pyproject.toml`(poetry) 없음 | 없음 | MIT, GPL 의존성 없음 |
| geo | GPL-3.0 원문 | `kor-travel-geo-ui/package.json` 없음 | 루트·dagster `license = { text = "GPL-3.0-only" }` + classifier `GPLv3` | 없음 | **GPL-3.0-only** 선언 |
| map | 25행 요약본: GPL 머리말 + `Copyright (C) 2026 digitie` + "version 3 or any later version" + 원문 링크 | 루트·admin 없음; `packages/map-marker-react`·`packages/kor-travel-map-user-client`는 `"license": "MIT"`, `"private": true`, `author: digitie` | 루트·api·dagster `GPL-3.0-or-later` + classifier `GPLv3+` | `README.md:210-212` GPL-3.0-or-later; admin/api README도 동일 | GPL-3.0-or-later + 하위 2패키지 MIT |
| weather | GPL-3.0 원문 | `packages/kor-travel-weather-admin/frontend/package.json` 없음 | 루트 `GPL-3.0-or-later`(classifier 없음); api·dagster 하위 pyproject `license` 없음; `packages/python-airkorea-api` GPL-3.0-or-later + classifier + 자체 `LICENSE` | `README.md:165-167` GPL-3.0-or-later | GPL-3.0-or-later |
| pinvi | **없음** | 루트 + 9개 workspace 모두 없음(`private: true`) | `apps/api/pyproject.toml` `license = { text = "MIT" }`; `apps/etl` 없음 | `README.md:242-244` "별도 명시 전까지 비공개(사내). `LICENSE`는 v2 코드 작성 단계 진입 시 결정." | **미결**; `AGENTS.md:321` "이 repo는 **공개**다"와 상충 |
| canview | GPL-3.0 원문 | (package.json 없음) | (pyproject 없음) | `README.md:56`은 `dbc` upstream MIT만 언급 | GPL-3.0 + 벤더 MIT 고지 모델 |
| common | GPL-3.0 원문(자리표시자 미기입) | 아직 없음 | 아직 없음 | README 없음 | 초기 상태 |
| maplibre-vworld-react | GPL-3.0 원문 | `packages/vworld-map-{core,web,rn}/package.json` **없음**, `private` 없음 | — | `README.md:142-144` "GPL-3.0 — `LICENSE` 참고" | GPL-3.0, 패키지 메타데이터 미표기 |
| maplibre-vworld-js | MIT | `package.json:33` `"license": "ISC"` | — | `README.md:263` "MIT." | **MIT/ISC 불일치** |

근거: 각 저장소 `LICENSE`, `package.json`, `pyproject.toml`, `README.md`(§7 목록).

### 2.2 선언 불일치·결함 목록

| # | 항목 | 사실 | 영향 | 구분 |
|---|---|---|---|---|
| D1 | map 루트 `LICENSE`가 GPL 전문이 아님(25행) | `LICENSE:8-10` "full text ... available at <https://www.gnu.org/licenses/gpl-3.0.html>". `git log`상 `fc8145fd`에서 작성 | GPLv3 §4는 배포 시 "give all recipients a copy of this License"를 요구한다(`https://www.gnu.org/licenses/gpl-3.0.html#section4`). 링크만으로 충분한지는 미확인 → 전문 복원이 안전 | 사실 + 후보 |
| D2 | geo만 `GPL-3.0-only`, map·weather·python-*-api는 `-or-later` | `pyproject.toml:11`, `kor-travel-geo-dagster/pyproject.toml:10` | geo 코드를 or-later인 common에 넣으면 그 파일은 사실상 only로 남거나, 권리자가 재선언해야 함(§3.2) | 사실 |
| D3 | kta·weather·common·canview·maplibre-vworld-react의 GPL `LICENSE`는 원문 그대로이고 소스·README에 버전 고지가 없음 | `grep '<name of author>'` 2곳 잔존, kta README에 라이선스 절 없음 | GPLv3 §14: 프로그램이 버전을 명시하지 않으면 수령자가 "any version ever published"를 선택할 수 있음(`gpl-3.0.html#section14`) → `-or-later`/`-only`를 명시해야 함 | 사실 + 추정(해석) |
| D4 | pinvi 루트 `LICENSE` 부재 + README "비공개(사내)" vs AGENTS "공개" 상충 + api pyproject MIT | 위 표 | 라이선스 미표기 코드는 기본적으로 저작권자 유보 → 외부 수령자는 어떤 권리도 받지 못함. 반면 pinvi에는 GPL 코드가 복제돼 있음(§2.3 P1~P3) | 사실 |
| D5 | pinvi 문서가 벤더 tgz를 "MIT"로 기재 | `docs/integrations/maplibre-vworld.md:23` "라이선스 \| MIT"; 원천 `maplibre-vworld-react/README.md:144` "GPL-3.0"; tgz 내 `package.json`에 `license` 없음, `LICENSE` 파일 없음(`tar -tzf` 3개 모두) | 문서상 근거 없는 MIT 주장. 실제로 pinvi가 받은 권리는 GPL-3.0뿐(§2.5) | 사실 |
| D6 | maplibre-vworld-js `LICENSE`(MIT) vs `package.json`(ISC) | `package.json:33` | 조사 대상 7개 저장소는 이 패키지를 소비하지 않음(각 `package.json` grep 결과 없음; pinvi는 ADR-046으로 대체) → 당장 영향 없음, 정리 대상 | 사실 |
| D7 | maplibre-vworld-react 하위 패키지 `package.json`에 `license` 없음, `private` 없음 | `packages/*/package.json` | `npm pack` 결과물이 라이선스 정보 없이 유통됨(D5의 원인) | 사실 |
| D8 | ktc `LICENSE` 저작권자가 "kor-travel-concierge contributors" | `git shortlog`: Youn-sok Choi 219, OpenAI Codex 67, digitie 21 — 외부 사람 기여자 없음 | 재라이선스 결정권자는 사실상 한 명. 문구를 다른 저장소와 맞출 필요 | 사실 + 추정 |
| D9 | map `tests/unit/test_frontend_dependency_security.py:78`은 `shadcn`이 devDependencies에 없어야 한다고 검사; ktc는 `shadcn@^4.10.0`을 **dependencies**에 둠 | `frontend/package.json` | 라이선스 문제는 아니나(shadcn CLI MIT), common 정책이 CLI 설치 위치를 정할 때 두 저장소가 충돌 | 사실 |
| D10 | SPDX 헤더가 어느 저장소에도 없음 | `git grep SPDX` 0건(7개 저장소) | 파일 단위 라이선스·출처 추적 수단이 주석 관례뿐 | 사실 |

### 2.3 파일군별 출처·라이선스 표

아래는 common으로 옮길 후보가 되는 파일군을 저장소별로 묶고, 원천과 라이선스, 현재 붙어 있는 출처 표기를 적은 것이다.

| ID | 저장소 / 파일군 | 원천(사실) | 원천 라이선스 | 현재 출처 표기 | 구분 |
|---|---|---|---|---|---|
| M1 | map `packages/kor-travel-map-admin/frontend/src/components/ui/*` 32파일 | shadcn CLI 생성물(`components.json` style `base-nova`, `@base-ui/react`) + 자체 수정 | shadcn/ui MIT(참조: `https://github.com/shadcn-ui/ui/blob/main/LICENSE.md`, 네트워크 미확인) + map GPL-3.0-or-later | 첫 줄이 `"use client"` 또는 Hallmark 스탬프(10+4파일); shadcn 출처 주석 없음(`data-table.tsx:6`만 "shadcn Table primitive" 언급) | 사실 |
| M2 | map `src/kortravelmap/category/*` | `python-kraddr-base/src/kraddr/base/categories.py`에서 이전(ADR-023) | GPL-3.0-or-later(`docs/architecture/category.md:452-456`; GitHub 페이지 GPL-3.0 확인) | `category/__init__.py:1-5`, `_definitions.py:7,45` docstring에 원천 경로·ADR 명기 | 사실 |
| M3 | map `src/kortravelmap/core/address.py` | `python-kraddr-base` 흡수(ADR-041, PR#37) | GPL-3.0-or-later | `address.py:3,10` 함수 매핑 주석; `pyproject.toml:75` "흡수 완료 + archive 후보" | 사실 |
| M4 | map `packages/map-marker-react/src/*`(index/maki/marker/palette) | map 자체 작성, MIT로 의도적 분리(ADR-029, ADR-043 게시 보류) | MIT 선언(`package.json:6`), 패키지 디렉터리에 `LICENSE` 파일 없음 | `src/index.ts:2` "(ADR-029/043)"; README `:11-17` MIT 사유 "PinVi(proprietary)와 ... 양쪽에서 import" | 사실; pinvi는 현재 이 패키지를 소비하지 않음(pinvi `git grep map-marker-react` 0건) |
| M5 | map `packages/kor-travel-map-user-client` | 생성 타입(`gen:types`) | MIT 선언, `private: true` | README `:10` "npm 게시 안 함" | 사실 |
| M6 | map admin `globals.css`/`design.md`(토큰·Rail-Workbench) | Hallmark 스킬로 설계, 자체 작성 | map GPL-3.0-or-later | `globals.css:48-49,72,88,276` shadcn 별칭 주석; "Hallmark ·" 스탬프 88파일 | 사실 |
| P1 | pinvi `apps/web/components/admin/**`(ui 28 + 상위 22 = 50파일) | map admin에서 이식(T-356) | **GPL-3.0-or-later**(map) → pinvi(라이선스 없음) | 첫 6행에 "kor-travel-map admin `...`에서 이식(T-356)" 35/50파일; `ui-components.md:80`은 ui 28파일 전부라고 기록 | 사실 |
| P2 | pinvi `apps/web/app/(admin)/admin/layout.tsx:46` | "kor-travel-geo T-278 이식" | **GPL-3.0-only**(geo) | 인라인 주석 | 사실 |
| P3 | pinvi `apps/{web,mobile}/vendor/*.tgz` 3개 | `maplibre-vworld-react` `packages/vworld-map-{core,web,rn}` 1.0.0(`npm pack` 추정) | **GPL-3.0**(원천 LICENSE·README); tgz 자체엔 표기 없음 | `docs/integrations/maplibre-vworld.md:23` "MIT"(근거 없음, D5) | 사실(내용) + 추정(pack 경로) |
| P4 | pinvi `packages/design-tokens/*`, `apps/mobile/components/ui.tsx`, `apps/web/components/ui/{Button,ConfirmDialog,Dialog}.tsx` | pinvi 자체 작성(`ui.tsx:15` "웹 shadcn/ui 대응 — 각자 구현"; design-tokens에 KTM/이식 언급 0건) | pinvi 미표기(저작권자 유보) | Hallmark 스탬프 | 사실 |
| P5 | pinvi `apps/web/globals.css:22` | "KTM의 oklch 팔레트는 이식하지 않는다 — 사용자 요구가 '색상톤 제외'" | — | 인라인 | 사실 |
| P6 | pinvi `.agents/skills/*`, `.claude/skills/*`(pg-aiguide 8종) | `github.com/timescale/pg-aiguide` | **Apache-2.0**(`SKILL.md` "라이선스: Apache-2.0", GitHub 확인) | `SKILL.md:18-19` 원본 링크·라이선스 행; Apache 라이선스 전문·NOTICE 미동봉 | 사실 |
| G1 | geo `kor-travel-geo-ui/components/ui/*` 26파일 | shadcn CLI(style `radix-nova`, `radix-ui@^1.4.3`) + 자체(`JsonBlock`, `Panel`, `VirtualTable` 등 PascalCase 5파일) | shadcn MIT + geo GPL-3.0-only | 출처 주석 없음; `globals.css:1-2` Hallmark 스탬프, `:2440,2468` shadcn 언급, `:2959` "latest kor-travel-map의 Rail-Workbench 구조를 geo 도메인에" | 사실 |
| G2 | geo `src/kortravelgeo/core/address/codes.py` | 독립 구현. `python-legacy-address-base`(GPL-3.0-or-later, Git checkout 아님)에서 **복사하지 않음**(T-056, ADR-035) | geo GPL-3.0-only | `codes.py:1-7` docstring; `docs/architecture/backend-package.md:295` | 사실 — 클린룸 재구현 선례 |
| G3 | geo `kor-travel-geo-ui/package.json:26` `maplibre-vworld-react` | GitHub archive tarball `@95b49d3` | GPL-3.0 | lockfile `resolved` | 사실 |
| W1 | weather `packages/kor-travel-weather-admin/frontend/app/{tokens,globals}.css`, `components/admin-shell.tsx` | map admin 디자인 시스템 복사 | GPL-3.0-or-later → GPL-3.0-or-later | `tokens.css:2,14,25,38` "copied from kor-travel-map", `globals.css:2,1911`, `admin-shell.tsx:3,26` | 사실 |
| W2 | weather 백엔드 DTO·Dagster 패턴 | map `41aaa86c` 커밋 기반 이식 | GPL-3.0-or-later 동일 | `README.md:155-163` "원본 이식 기록" | 사실 |
| W3 | weather `packages/python-airkorea-api/` | GitHub `digitie/python-airkorea-api` 커밋 `9b00dd65` 스냅샷 복사 | GPL-3.0-or-later, 자체 `LICENSE` 동봉 | `README.md:129-131`; map은 같은 패키지를 git URL로 의존(`pyproject.toml`) | 사실 — 중복 벤더링 |
| C1 | ktc `frontend/src/components/ui/*` 18파일 | shadcn CLI(style `base-nova`) | shadcn MIT + ktc MIT | 출처 주석 없음; `AppShell.tsx:2`, `field-variants.ts:1` Hallmark 스탬프; `AppShell.tsx:38` "최신 kor-travel-map admin의 그룹형 IA를 ... 적용" | 사실(IA 참조는 코드 복사인지 미확인) |
| C2 | ktc `frontend/src/lib/youtube.ts` | 자체 백엔드 `ktc/etl/source_resolve.py` 이식 | MIT | `youtube.ts:1-3` | 사실 |
| C3 | ktc `frontend/src/app/globals.css:21,71` | "kor-travel-map admin frontend와 같은 웜 그레이 surface ... 토큰" | GPL 토큰 값 참조(값 복사 여부는 주석상 "같은") | 인라인 | 추정(색값 복사 여부 미확인) |
| K1 | kta `frontend/src/components/*` 6파일, `app/{globals,tokens}.css` | 자체 작성(Hallmark 스탬프 "parking-radar" 2026-08-22); shadcn·base-ui 미사용, `components.json` 없음 | GPL-3.0 | `tokens.css:1`, `globals.css:1` | 사실 |
| T1 | ktdm `frontend/src/components/*`, `tokens.css` | 자체 작성; `tokens.css:1` "kor-travel-map Rail-Workbench 구조, 오렌지 계통" — 구조 참조 | MIT | 인라인 | 사실(구조 참조는 코드 복사 아님 — 추정) |
| A1 | kta·ktc·ktdm·geo·map `.agents/.claude/.codex/.opencode` pg-aiguide 스킬 | P6과 동일 | Apache-2.0 | 동일 | 사실; weather는 `.github`만 추적(스킬 없음) |
| A2 | `.hallmark/{log,preflight}.json`(kta·geo·ktdm) + CSS/TSX "Hallmark ·" 스탬프 | Hallmark 스킬 실행 기록(자체 데이터) | 각 저장소 라이선스 | — | 사실; 스킬 본문은 저장소에 없음(§2.5) |
| V1 | canview `dbc/opendbc/*` | `commaai/opendbc` 스냅샷 `3e92d112` | MIT(Comma.ai) | `dbc/README.md:14-16,27,40` upstream commit·SHA-256·라이선스 표 | 사실 — 벤더링 고지 모델 |

### 2.4 서드파티 의존성 라이선스(lockfile `packages[*].license`, 사실)

| 패키지 | 라이선스 | 사용 저장소(설치 버전) | 고지 의무 요지 |
|---|---|---|---|
| `@base-ui/react` | MIT | ktc 1.5.0, map 1.6.0, pinvi 1.8.0 | 저작권·허가 고지 유지 |
| `radix-ui`(메타) / `@radix-ui/*` | MIT | geo 1.4.3 선언(락 73개 하위 패키지); pinvi 락에 `@radix-ui/react-slot` 1.3.3 등 21개(직접 선언 없음, 전이 경로 미확인) | 동일 |
| `class-variance-authority` 0.7.1 | **Apache-2.0** | ktc·map·geo·pinvi | Apache §4: LICENSE 사본·NOTICE 유지. GPLv3와 호환(참조: `https://www.gnu.org/licenses/license-list.html#apache2`, 미확인) — 임무 지시문의 "shadcn 계열 MIT" 가정과 다름 |
| `lucide-react` | ISC | 전 프런트(0.363~1.27) | 고지 유지 |
| `tailwind-merge`, `clsx`, `tw-animate-css`, `tailwindcss`, `next`, `react`, `sonner`, `zustand`, `zod`, `@tanstack/react-table`, `nativewind`, `use-supercluster`, `shadcn`(CLI) | MIT | 다수 | 고지 유지 |
| `maplibre-gl` | BSD-3-Clause | geo·map·pinvi·weather 5.24.0, ktc **6.0.0** | 고지 유지, 이름 홍보 금지 조항 |
| `supercluster` | ISC | pinvi(벤더 web 패키지 경유) | 고지 유지 |
| `pretendard` 1.3.9 | **OFL-1.1** | ktc·map·pinvi(npm 의존); 어느 저장소도 `.woff2/.ttf` 파일을 직접 추적하지 않음 | OFL: 폰트 소프트웨어 배포 시 라이선스 사본 동봉, Reserved Font Name 규칙(참조: `https://openfontlicense.org`, 미확인). 웹 앱 번들에 포함되면 배포에 해당(추정) |
| `typescript` | Apache-2.0 | 전 프런트 | 빌드 도구; 산출물에 포함되지 않음(추정) |
| `python-*-api`(digitie) | GPL-3.0(-or-later) | kta(kasi·krairport), ktc(vworld), map(13종), weather(kma, airkorea 스냅샷), pinvi(kasi) | GPL 결합 규칙(§3.1) |
| `python-kraddr-base` | GPL-3.0 | map이 흡수 완료(직접 의존 없음) | M2·M3 파생물 표기 유지 |

### 2.5 벤더링 산출물 상세

**pinvi 벤더 tgz(사실)**

| 파일 | 크기 | 내용 | `package.json` | 라이선스 흔적 |
|---|---|---|---|---|
| `apps/mobile/vendor/vworld-map-core-1.0.0.tgz` | 4,489B | `package/dist/*.js,*.d.ts` 7모듈 + `package.json` | `name: vworld-map-core`, `version 1.0.0`, `license` 없음 | 없음 |
| `apps/mobile/vendor/vworld-map-rn-1.0.0.tgz` | 7,508B | `dist/VWorldMapView.js`, `components/*` 8종 | `license` 없음, peer `@maplibre/maplibre-react-native ^11`, `react-native >=0.80` | 없음 |
| `apps/web/vendor/vworld-map-web-1.0.0.tgz` | 43,423B | `dist/components/*` 18종, `store/*`, `schemas.js`, `vworld.js` | `license` 없음, deps `supercluster`, `use-supercluster`, `zod ^4.4.3` | 없음 |

원천 `maplibre-vworld-react` `packages/vworld-map-{core,web,rn}/package.json`도 `version 1.0.0`, `license` 없음(사실). 원천 저장소 `LICENSE`는 GPL-3.0 원문, `README.md:144` "GPL-3.0". 따라서 pinvi가 이 tgz에 대해 보유한 권리는 원천 GPL-3.0뿐이고, `docs/integrations/maplibre-vworld.md:23`의 "MIT"는 근거가 없다(사실). 다만 원천과 pinvi의 저작권자가 같으므로(§2.6) 권리자가 MIT 또는 이중 라이선스로 **명시적으로** 재선언하면 해소된다(§3.2). tgz가 원천 소스와 바이트 단위로 일치하는지(수정 여부)는 미확인.

pinvi는 `apps/web/Dockerfile:22` `COPY --parents apps/*/vendor/ ./`로 tgz를 이미지에 넣고, `apps/mobile/package.json:23-26`에 `eas build --profile production` 스크립트가 있다(사실). 이미지·앱 바이너리를 외부에 배포하면 GPL의 "convey"에 해당하고, 사내 배포에 그치면 해당하지 않는다(FAQ `#InternalDistribution`, `#UnreleasedMods`). 실제 배포 여부는 미확인.

**벤더링 스킬(pg-aiguide, 사실)**: kta·ktc·ktdm·geo·map·pinvi가 `.agents/skills/{postgres,design-postgres-tables,design-postgis-tables,find-hypertable-candidates,migrate-postgres-tables-to-hypertables,pgvector-semantic-search,postgres-hybrid-text-search,setup-timescaledb-hypertables}` 8종을 `.claude/skills`(및 일부 `.opencode/skill(s)`)에 복제한다. 각 `SKILL.md`가 "원본: github.com/timescale/pg-aiguide/..." + "라이선스: Apache-2.0"(`.claude` 판은 front-matter `license: Apache-2.0`)을 적었고 GitHub 페이지도 Apache-2.0을 표시한다. Apache-2.0 §4(a)는 재배포 시 라이선스 사본 제공, §4(d)는 NOTICE 유지를 요구하는데 어느 저장소에도 Apache 전문·NOTICE 파일이 없다(사실). weather에는 스킬 디렉터리가 없다(`.github`만 추적).

**Hallmark(사실/미확인)**: 스킬 본문은 사용자 홈 `C:/Users/digit/.agents/skills/hallmark/SKILL.md`(v1.1.0, 558행; `~/.claude/skills/hallmark`는 여기로의 심볼릭 링크; `~/.codex/skills/hallmark/SKILL.md`는 내용이 다름)에 있고, 저작자·라이선스 표기가 없으며 "Powered by Together AI"라고만 적혀 있다. 조사 대상 저장소에는 스킬 본문이 없고 실행 기록(`.hallmark/*.json`)과 CSS/TSX 첫 줄 스탬프만 있다. 스탬프는 저장소 저작물이므로 별도 의무가 없다(추정). 스킬 본문의 출처·라이선스는 **미확인**.

**canview opendbc(사실)**: `dbc/opendbc/LICENSE`(MIT, Comma.ai 2020) 동봉 + `dbc/README.md`에 upstream commit·SHA-256·역할 표. common의 `THIRD_PARTY_NOTICES` 작성 모델로 쓸 수 있다(후보).

### 2.6 기여자·저작권자(`git shortlog -sne HEAD`, 사실)

| 저장소 | 사람 커밋 | 봇 계정 커밋 | 외부 사람 기여자 |
|---|---|---|---|
| kta | Youn-sok Choi 17, digitie 3 | 없음 | 없음 |
| ktc | Youn-sok Choi 219, digitie 21 | OpenAI Codex 67 | 없음 |
| ktdm | Youn-sok Choi 291, digitie 34 | ChatGPT Codex 422, OpenAI Codex 22, Claude 17 | 없음 |
| geo | Youn-sok Choi 482, digitie 141 | Claude 14 | 없음 |
| map | digitie 1,425, Youn-sok Choi 1,049 | Claude 59, OpenAI Codex 45 | 없음 |
| weather | digitie 46, Youn-sok Choi 25 | 없음 | 없음 |
| pinvi | Youn-sok Choi 1(스냅샷) | — | 없음(이력 없음) |
| canview | Youn-sok Choi 55 | 없음 | 없음 |

모든 저장소의 사람 기여자가 한 명(`digitie`/`Youn-sok Choi`, 동일 이메일)이다(사실). AI 도구 계정으로 커밋된 코드의 권리 귀속은 각 도구 약관과 관할법에 좌우되며 이 조사에서는 확인하지 않았다(미확인). 외부 인간 기여자가 없으므로 재라이선스 결정에 제3자 동의는 필요 없다(추정, 봇 커밋 제외).

## 3. 산출 (2) — 공통 라이브러리로 옮길 때 필요한 조치

### 3.1 법적 전제(GNU 공식 FAQ, 2026-09-06 확인)

| 앵커 | 요지 | 이 조사에서의 적용 |
|---|---|---|
| `gpl-faq.en.html#IfLibraryIsGPL` | GPL 라이브러리를 링크하는 프로그램은 배포 시 전체가 GPL이어야 한다 | GPL common을 소비하는 ktc·ktdm·pinvi(§3.6) |
| `#GPLStaticVsDynamic` | 정적·동적 링크 모두 "combined work" | npm 번들·Python import 모두 해당(추정) |
| `#LinkingWithGPL`, `#WhatIsCompatible` | GPL 호환 라이선스(MIT/Expat, BSD, ISC, Apache-2.0↔GPLv3)의 코드는 결합 가능하며 결합물은 GPL로 배포 | MIT 앱 코드·shadcn·base-ui·cva를 GPL common에 넣는 방향은 허용 |
| `#GPLInProprietarySystem` | GPL 코드를 사유 시스템에 포함해 배포할 수 없음 | pinvi가 "비공개·사유"를 택하면서 외부 배포도 하면 충돌 |
| `#ReleaseUnderGPLAndNF`, `#HeardOtherLicense` | 저작권자는 같은 코드를 여러 라이선스로 병행 배포할 수 있다 | 단일 권리자이므로 예외·이중 라이선스 선언이 가능 |
| `#DeveloperViolate` | 저작권자 본인은 GPL에 구속되지 않는다 | 소유자 내부 결합은 "위반"이 아니나, 수령자에게 전달되는 고지는 일관돼야 함 |
| `#GPLModuleLicense` | 모듈은 GPL 하에 이용 가능해야 하되 추가 허가를 줄 수 있다 | GPLv3 §7 additional permissions로 예외 부여 가능 |
| `#VersionThreeOrLater`, `#OnlyLatestVersion` | "version 3 or any later version" 권장 | D2·D3 정리 방향 |
| `#GPLRequireSourcePostedPublic`, `#UnreleasedMods`, `#InternalDistribution` | 공개 배포 시에만 소스 제공 의무; 사내 사용·복제는 배포가 아님 | pinvi 배포 형태(§2.5) 판단 기준 |
| `#RequiredToClaimCopyright`, `#HowIGetCopyright` | 저작권은 고정 시 자동 발생; 수정본은 GPL로 | 이식 파일의 저작권 표기 |

GPLv3 원문(`https://www.gnu.org/licenses/gpl-3.0.html`)에서 직접 관련되는 절: §4(라이선스 사본·고지 유지), §5(a)(수정 파일에 수정 사실·날짜 고지), §5(c)(전체를 GPL로), §7(추가 허가/추가 조건), §14(버전 미지정 시 임의 버전 선택).

### 3.2 재라이선스 가능 여부 판정

| 대상 | 원 라이선스 | common(GPL-3.0-or-later)으로 이동 | 근거·조건 | 구분 |
|---|---|---|---|---|
| map·weather·kta 자체 코드 | GPL-3.0-or-later / GPL-3.0(버전 미지정, D3) | 가능 | 동일 라이선스. kta는 common에서 `-or-later`로 명시하면 됨(권리자 동일) | 사실 |
| geo 자체 코드 | GPL-3.0-only | 가능하나 표기 필요 | only 코드와 or-later 코드의 결합은 허용되지만 결합물은 사실상 v3-only. 권리자가 common에서 해당 파일을 `-or-later`로 재선언하면 해소(`#HeardOtherLicense`) | 사실 + 후보 |
| ktc·ktdm 자체 코드 | MIT | 가능 | MIT → GPL 방향은 호환. MIT 고지(저작권·허가문)를 `THIRD_PARTY_NOTICES` 또는 파일 헤더에 유지. 권리자가 같으므로 아예 GPL로 재선언해도 됨 | 사실 |
| pinvi 자체 코드(P4) | 미표기(유보) | 권리자 결정 후 가능 | 제3자 권리 없음(§2.6). 다만 pinvi 라이선스 자체가 미결이므로 먼저 결정 | 사실 + 차단(§4) |
| pinvi 이식 코드(P1·P2) | 원천 GPL(map or-later, geo only) | common으로 "되돌리는" 것은 가능 | 원천이 이미 GPL. pinvi가 가한 수정분("원문에서 바꾼 부분", "pinvi 이식분 추가")의 권리도 같은 소유자 | 사실 |
| shadcn 생성 컴포넌트(M1·G1·C1) | MIT(shadcn) + 각 저장소 수정분 | 가능 | MIT 고지 유지. 생성 시점 shadcn 버전은 미기록(미확인) | 사실 + 미확인 |
| `python-kraddr-base` 파생(M2·M3) | GPL-3.0(-or-later) | 가능 | 원천 표기(docstring) 유지. common이 카테고리 모듈을 가져갈 경우 "Origin" 문구 보존 | 사실 |
| 벤더 tgz(P3)·maplibre-vworld-react 코드 | GPL-3.0 | **이동 금지**(중복 금지 대상) | 이미 분리된 공유 라이브러리. common은 의존만 한다 | 지시 + 사실 |
| pg-aiguide 스킬(P6·A1) | Apache-2.0 | 가능(고지 조건) | Apache LICENSE 전문 + NOTICE 동봉, 수정 표시 | 사실 |
| Hallmark 스킬 본문 | 미확인 | **이동 금지** | 규칙 문서에 SKILL.md 문장을 옮겨 적지 말 것. 스탬프 형식(첫 줄 주석)만 규약으로 채택 가능 | 미확인 |
| opendbc(V1) | MIT | 대상 아님 | 참조 모델로만 사용 | 사실 |

### 3.3 고지 파일 구성(후보)

| 파일 | 내용 | 근거 |
|---|---|---|
| `LICENSE` | GPL-3.0 전문(현재 있음). 부록 자리표시자는 채우지 않아도 되지만, 저작권·버전 고지는 `README`/`NOTICE`에 별도 기재 | GPLv3 "How to Apply", D3 |
| `NOTICE` 또는 `COPYRIGHT` | `Copyright (C) 2026 Youn-sok Choi (digitie)`; "GPL-3.0-or-later"; 저작권자 연락처; 예외(§7 추가 허가)가 있으면 여기 명시 | `#HeardOtherLicense`, GPLv3 §7 |
| `THIRD_PARTY_NOTICES.md` | shadcn/ui(MIT), base-ui(MIT), radix(MIT), cva(Apache-2.0 + NOTICE 원문), lucide(ISC), tailwind-merge/clsx/tw-animate-css(MIT), maplibre-gl(BSD-3), pretendard(OFL-1.1 전문), pg-aiguide(Apache-2.0, 스킬을 common이 호스팅할 때만) — 각 항목에 버전·원문 URL·사본 | §2.4; canview `dbc/README.md` 모델 |
| `PROVENANCE.md`(또는 `docs/standards/provenance.md`) | 파일군별 원천 저장소·커밋·경로·라이선스 표(§2.3의 형식) | 선행 보고서 §9 "파일별 출처 목록" |
| `LICENSES/` 디렉터리(REUSE 관행) | `GPL-3.0-or-later.txt`, `MIT.txt`, `Apache-2.0.txt`, `OFL-1.1.txt` 등 SPDX 파일명으로 원문 보관 | 참조: `https://reuse.software/spec/`(미확인) |
| npm 패키지 디렉터리별 `LICENSE` | 게시 패키지마다 GPL 전문 사본(npm은 `files` 지정과 무관하게 `LICENSE*`를 포함, 참조: npm docs) | D7 재발 방지 |

### 3.4 헤더 규약(후보)

현재 관례(사실): pinvi "…에서 이식(T-356)" + "원문에서 바꾼 부분", map `Origin: python-kraddr-base …`, weather "copied from kor-travel-map", Hallmark 첫 줄 스탬프. SPDX 헤더는 없다(D10).

제안 형식(TS/CSS는 `//`·`/* */`, Python은 `#`):

```
// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-map@c494e227 packages/kor-travel-map-admin/frontend/src/components/ui/button.tsx (GPL-3.0-or-later)
// Derived-From: shadcn/ui (MIT) — see THIRD_PARTY_NOTICES.md
// Modified: 2026-09-xx — <바꾼 점 요약>
```

- `Origin`/`Derived-From`/`Modified`는 GPLv3 §5(a)(수정 고지)와 §7(b)(저작자 표시 보존)를 파일 단위로 충족하기 위한 것이다.
- Hallmark 스탬프는 SPDX 행 **다음**에 둔다(Hallmark 규칙은 "첫 번째 비어 있지 않은 줄"을 요구하므로 충돌 — 규약에서 순서를 정해야 함; 스킬 문서 `SKILL.md:461` 기준, 후보).
- shadcn CLI가 재생성하면 헤더가 사라지므로, common은 CLI 재생성이 아닌 소스 소유 방식(map `globals.css:48-49` "shadcn 스타일시트를 import하지 않으므로 이 파일이 직접 소유")을 따르는 편이 헤더 유지에 유리하다(추정).

### 3.5 패키지 메타데이터 규약(후보)

| 대상 | 필드 | 값 | 현재 상태(사실) |
|---|---|---|---|
| npm(`package.json`) | `license` | `"GPL-3.0-or-later"`(SPDX 식별자) | 조사 대상 프런트 패키지 전부 없음; map 하위 2개만 `MIT` |
| npm | `files` + `LICENSE` | 패키지 루트에 `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` | 없음 |
| npm | `private` | 게시 전엔 `true`; 게시 결정 후 제거 | maplibre-vworld-react 하위는 `private` 없음(D7) |
| Python(`pyproject.toml`) | `license` | PEP 639 형식 `license = "GPL-3.0-or-later"` + `license-files = ["LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"]`(참조: `https://peps.python.org/pep-0639/`, 미확인). 빌드 백엔드가 PEP 639를 지원하지 않으면 기존 `{ text = ... }` 유지 | geo·map·weather는 `{ text = ... }` 표 형식; kta·ktdm·weather 하위·pinvi etl은 없음 |
| Python | `classifiers` | `License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)` — PEP 639 이후 폐기 예정이므로 SPDX 필드와 병기(참조, 미확인) | geo·map·airkorea만 존재 |
| Docker 이미지 | 라벨 `org.opencontainers.image.licenses=GPL-3.0-or-later` + 이미지 내 `/licenses/` | 미확인(Dockerfile 라벨 조사 범위 밖) |

### 3.6 소비 앱 라이선스 정렬 판단

| 앱 | 현재 | GPL 의존성(사실) | 외부 배포 형태 | 판단 근거 | 권고 |
|---|---|---|---|---|---|
| ktc | MIT(루트·README) | `python-vworld-api`(GPL-3.0, GitHub 표시) 이미 의존; common 채택 시 UI·백엔드 모두 GPL 결합 | 공개 GitHub 저장소(추정: 선행 보고서 URL이 `github.com/digitie/kor-travel-concierge`), Docker(미확인) | `#IfLibraryIsGPL`: 배포되는 결합물은 GPL. MIT 루트 표기는 이미 `python-vworld-api` 의존으로 불완전. 권리자가 같으므로 (a) 루트를 GPL-3.0-or-later로 바꾸거나 (b) common에 §7 추가 허가를 넣어 MIT 앱이 링크할 수 있게 하는 두 길이 있음 | **(a) GPL-3.0-or-later로 정렬**. 이유: 7개 중 5개가 이미 GPL, (b)는 common의 모든 파일에 예외 문구를 유지·검증하는 비용이 크고 "GPL common" 전제와 어긋남. 파일별 MIT 고지는 `THIRD_PARTY_NOTICES`로 이관 |
| ktdm | MIT | 없음(digitie `python-*` 의존 0건; 프런트에도 GPL 없음) | 공개 GitHub(추정) | common을 소비하는 순간 ktc와 같은 상황 | common 소비 범위(프런트 토큰·UI·규칙 문서)를 정한 뒤 정렬. 규칙 **문서**만 참조하고 코드를 링크하지 않으면 MIT 유지 가능(문서는 저작물이지만 규칙을 따르는 것 자체는 파생이 아님 — 추정). 코드 소비 시 GPL-3.0-or-later 권고 |
| pinvi | 미표기; README "비공개(사내)", AGENTS "공개", api MIT | map 이식 35+파일(P1), geo 이식(P2), GPL tgz 3개(P3), `python-kasi-api`(GPL-3.0-or-later) | 공개 저장소(AGENTS 기준) + Docker + EAS production 스크립트(배포 실행 여부 미확인) | 이미 GPL 코드가 소스에 있으므로 "공개 저장소"라면 저장소 자체가 GPL 조건의 배포에 해당(추정). 사유·사내로 남기려면 저장소를 비공개로 하고 외부 배포를 하지 않아야 함(`#InternalDistribution`) | 먼저 README/AGENTS 상충을 해소. 공개 유지 시 **GPL-3.0-or-later 채택 + 루트 `LICENSE` 추가 + `apps/api/pyproject.toml` MIT 수정 + `docs/integrations/maplibre-vworld.md:23` 정정**. 사유 유지 시 GPL 코드(P1~P3)를 걷어내거나 권리자가 해당 원천을 별도 허가로 재선언해야 함 |

"같은 소유자니까 명시 없이 된다"는 성립하지 않는다: 소유자 본인은 구속되지 않지만(`#DeveloperViolate`), 저장소·이미지·앱을 받은 제3자는 그들이 받은 고지문에 따라 권리를 판단하므로 고지가 서로 모순되면 수령자의 권리가 불명확해진다. 예외를 두려면 GPLv3 §7의 추가 허가를 common `NOTICE`와 파일 헤더에 적어야 한다.

### 3.7 조치 목록(우선순위)

| ID | 조치 | 대상 | 근거 | 우선 |
|---|---|---|---|---|
| L1 | common `NOTICE`에 저작권자·`GPL-3.0-or-later`·연락처 기재, `README` 라이선스 절 추가 | common | D3, GPLv3 §14 | 높음 |
| L2 | `PROVENANCE.md` 초안 = §2.3 표. 이동하는 파일마다 원천 커밋·경로·라이선스 기록 | common | 선행 보고서 §9, `#RequiredToClaimCopyright` | 높음 |
| L3 | `THIRD_PARTY_NOTICES.md` + `LICENSES/`(MIT·Apache-2.0·OFL-1.1·BSD-3·ISC 원문) | common | §2.4, Apache §4, OFL | 높음 |
| L4 | 헤더 규약(§3.4) 확정 + 린트(`SPDX-License-Identifier` 존재 검사) | common 도구 | D10 | 높음 |
| L5 | npm/Python 메타데이터 규약(§3.5) 확정; common의 첫 패키지에 적용 | common | §2.1 표의 공백 | 높음 |
| L6 | pinvi 라이선스 결정(공개 GPL vs 사내 비공개) 후 README/AGENTS 정합, 루트 `LICENSE`, `apps/api/pyproject.toml`, `docs/integrations/maplibre-vworld.md:23` 수정 | pinvi | D4·D5, §3.6 | 높음(차단 B1 해제 조건) |
| L7 | maplibre-vworld-react 하위 패키지 `package.json`에 `license`(GPL-3.0-or-later 또는 권리자가 정한 MIT/이중) + 패키지 디렉터리 `LICENSE`; tgz 재생성 | maplibre-vworld-react → pinvi 벤더 갱신 | D5·D7 | 높음 |
| L8 | ktc·ktdm 루트 라이선스 정렬 결정(§3.6) — 결정 전에는 common 코드 링크 금지 | ktc·ktdm | `#IfLibraryIsGPL` | 중간 |
| L9 | map 루트 `LICENSE`를 GPL 전문으로 복원(현재 요약본의 저작권·버전 고지는 `NOTICE`로) | map | D1 | 중간 |
| L10 | geo `GPL-3.0-only` → `-or-later` 재선언 여부 결정. 유지하면 common에서 geo 유래 파일에 `SPDX-License-Identifier: GPL-3.0-only`를 별도 표기 | geo·common | D2 | 중간 |
| L11 | kta·weather 하위·pinvi etl `pyproject.toml`, 모든 프런트 `package.json`에 `license` 필드 추가 | 각 앱 | §2.1 | 중간 |
| L12 | pg-aiguide 스킬 디렉터리에 Apache-2.0 전문 + NOTICE 동봉(스킬을 common이 배포하기로 하면 common에서 1회) | 6개 저장소 또는 common | P6·A1 | 중간 |
| L13 | maplibre-vworld-js `package.json` `license`를 `MIT`로 정정 | maplibre-vworld-js | D6 | 낮음 |
| L14 | ktc `LICENSE` 저작권자 문구를 다른 저장소와 통일 | ktc | D8 | 낮음 |
| L15 | weather `packages/python-airkorea-api` 스냅샷과 GitHub 원본의 관계(정본 어느 쪽인지) 결정; common은 어느 쪽도 복제하지 않음 | weather | W3 | 낮음 |
| L16 | Hallmark 스킬 원천·라이선스 확인(작성자에게 문의) 전까지 규칙 문서에 SKILL.md 문장 인용 금지 | common 규칙 문서 | §2.5 | 낮음(차단 B3) |

## 4. 산출 (3) — 차단 항목(권리·결정 확인 전 이동 금지)

| ID | 항목 | 이유 | 해제 조건 |
|---|---|---|---|
| B1 | pinvi의 모든 파일(P1~P5 포함) | 저장소 라이선스 미결(D4). 자체 코드는 권리 유보 상태이고, 이식 코드는 원천 GPL이지만 pinvi 측 수정분의 라이선스가 선언되지 않음 | L6 완료(권리자의 라이선스 선언) |
| B2 | pinvi 벤더 tgz(P3) 및 `maplibre-vworld-react` 소스 | 이미 분리된 공유 라이브러리 = 중복 금지 대상. 또한 라이선스 메타데이터 부재(D7) | 해당 없음(영구 금지). common은 의존만 |
| B3 | Hallmark `SKILL.md` 본문·참조 문서 | 저작자·라이선스 미확인 | 원천 확인 |
| B4 | ktc `AppShell.tsx`·`globals.css`가 참조한 map admin IA·토큰 값(C1·C3) | 코드 복사인지 개념 참조인지 미확인. 복사라면 GPL 코드가 MIT 저장소에 있는 상태 | 파일 diff로 복사 여부 확정 후 L2에 기록 |
| B5 | pinvi 락파일의 `@radix-ui/*` 21개 | 직접 선언이 없어 어떤 의존성이 끌어오는지 미확인 → 고지 목록 누락 위험 | `npm ls @radix-ui/react-slot`(설치 환경) 또는 락 `dependencies` 역추적 |
| B6 | 생성 컴포넌트의 shadcn 버전·registry 항목 | 생성 시점 미기록. MIT 고지에 필요한 저작권 연도·저장소 URL만으로 충분하지만, 수정 전 원문 대조가 불가 | shadcn `LICENSE.md` 원문 확보 후 고지 |
| B7 | `python-*-api` 13종 중 GitHub에서 미확인인 저장소(kma·kasi·vworld·kraddr-base 외) | 라이선스 표시 미확인(모두 GPL 계열로 추정) | 각 저장소 `LICENSE` 확인 후 `THIRD_PARTY_NOTICES` 기재 |
| B8 | 봇 계정(Codex·Claude) 커밋분 | 권리 귀속은 도구 약관·관할법에 좌우(미확인). 외부 청구권자는 없음 | 정책 문서에 "AI 보조 생성물은 지시자(권리자)가 GPL로 배포" 명시(후보) |

## 5. 선행 문서와의 차이

| 선행 문서 | 서술 | 이 조사의 재검증 |
|---|---|---|
| `kor-travel-common-library-review.md` §9 | geo·map·weather GPL, ktc·ktdm MIT, pinvi 루트 LICENSE 없음 | 일치. 추가 발견: kta도 GPL-3.0 원문 보유, map은 요약본(D1), geo는 only(D2), 벤더 tgz 라이선스 부재(D5·D7), cva Apache-2.0, pg-aiguide Apache-2.0 |
| `cross/backend.md` 49행·417행·439행 | "kta 라이선스 선언 없음(미확인)", "kta `LICENSE` 존재 여부 미확인", "pinvi·ktdm·ktc는 MIT" | **정정**: kta 루트 `LICENSE`는 GPL-3.0 원문 674행(사실). pinvi는 루트 LICENSE 없음이며 MIT는 `apps/api/pyproject.toml`에만 있음 |
| `inventory/pinvi.md` 284행 | 벤더 tgz "라이선스 MIT(문서)" | 문서 기재는 사실이나 원천은 GPL-3.0, tgz 내 표기 없음(D5) |
| `inventory/kor-travel-map.md` 6행 | map-marker-react·user-client MIT, ADR-029 | 일치. 보완: 패키지 디렉터리에 `LICENSE` 파일 없음, `private: true`, pinvi는 이 패키지를 소비하지 않음 |
| `inventory/kor-travel-concierge.md` 220행 | "MIT → GPL 방향이라 허용되나 저작권 표기 유지 필요" | 일치. 보완: ktc는 이미 GPL `python-vworld-api`에 의존 |
| `cross/ui-components.md` §2.3·§6.1 | "airport WIP"에 `components.json`(`base-nova`)·`shadcn 4.21.0` 존재 | kta `2bb1111` 추적 트리와 작업 트리(clean)에는 `components.json`·`shadcn`이 없다(사실). "WIP"는 다른 작업 사본을 가리키는 것으로 보이며 이 조사에서는 미확인 |
| `cross/ui-components.md` 80행 | pinvi admin ui 28파일 전부 이식 주석 | 첫 6행 기준 35/50(admin 전체) — ui 하위만 보면 일치(사실) |

## 6. 열린 질문

1. pinvi를 공개 GPL 저장소로 둘지, 사내 비공개로 둘지(README vs AGENTS 상충). 이 결정이 B1·L6·L7의 전제다.
2. common이 GPLv3 §7 추가 허가(예: "MIT 앱이 이 라이브러리를 링크할 수 있다")를 둘 것인지, 아니면 ktc·ktdm·pinvi를 GPL로 정렬할 것인지. 이 문서의 권고는 후자(§3.6).
3. geo의 `GPL-3.0-only`를 유지할 이유가 있는지(다른 저장소는 or-later).
4. `maplibre-vworld-react`를 pinvi 문서대로 MIT(또는 이중)로 재선언할지, GPL-3.0을 유지하고 pinvi 문서를 고칠지.
5. Hallmark 스킬의 원저작자·라이선스. "Powered by Together AI" 외 정보 없음.
6. AI 도구 계정 커밋분에 대한 권리 귀속 정책을 common `CONTRIBUTING`에 어떻게 적을지.
7. common이 pg-aiguide 스킬 세트를 배포 대상에 포함할지(포함하면 Apache 고지가 common 책임).
8. ktc `AppShell.tsx`·`globals.css`의 map 참조가 코드 복사인지(B4).
9. Docker 이미지·EAS 빌드가 실제로 외부에 배포되는지(배포 여부가 GPL 의무 발생의 분기점).
10. pretendard를 npm 의존으로 번들할 때 OFL 사본을 어느 위치에 둘지(웹 번들 배포 시 의무 범위는 추정).

## 7. 근거 파일 목록

경로는 저장소 상대 경로. 저장소 약칭: kta·ktc·ktdm·geo·map·weather·pinvi·canview·common·mvr(maplibre-vworld-react)·mvj(maplibre-vworld-js).

1. kta `LICENSE`(1-5행, 645-674행), `frontend/package.json`, `backend/pyproject.toml`(1-20행), `frontend/src/app/tokens.css:1`, `frontend/src/app/globals.css:1`, `.hallmark/log.json`, `.hallmark/preflight.json`, `.agents/skills/postgres/SKILL.md:1-22`, `.claude/skills/postgres/SKILL.md:16`, `README.md`
2. ktc `LICENSE`, `README.md:203-205`, `frontend/package.json`, `frontend/components.json`, `frontend/package-lock.json`(license 필드), `tests/package.json`, `backend/requirements.txt`, `frontend/src/components/ui/*`(18파일 첫 줄), `frontend/src/components/AppShell.tsx:2,38`, `frontend/src/components/ui/field-variants.ts:1`, `frontend/src/app/globals.css:21,71,232`, `frontend/src/lib/youtube.ts:1-6`, `frontend/src/lib/utils.ts`
3. ktdm `LICENSE`, `frontend/package.json`, `frontend/package-lock.json`, `backend/pyproject.toml:1-15`, `frontend/tokens.css:1-3`, `frontend/src/app/globals.css:1`, `.hallmark/log.json`, `backend/src/kor_travel_docker_manager/api/websocket.py:88`
4. geo `LICENSE`, `pyproject.toml:5-17`, `kor-travel-geo-dagster/pyproject.toml:5-16`, `kor-travel-geo-ui/package.json:26,28`, `kor-travel-geo-ui/components.json`, `kor-travel-geo-ui/package-lock.json`(`node_modules/maplibre-vworld-react`, radix), `kor-travel-geo-ui/components/ui/*`(26파일 첫 줄), `kor-travel-geo-ui/app/globals.css:1-2,2440,2468,2476,2959`, `src/kortravelgeo/core/address/codes.py:1-7`, `docs/architecture/backend-package.md:293-295`, `docs/adr/035-address-code-helper-independent-impl.md:34`, `docs/kor-travel-common-library-review.md:190-196,278-283,294`
5. map `LICENSE`(25행 전체), `README.md:210-212`, `pyproject.toml:5-17,70-78`, `packages/kor-travel-map-api/pyproject.toml:11-17`, `packages/kor-travel-map-dagster/pyproject.toml:11-17`, `package.json`, `package-lock.json`, `packages/kor-travel-map-admin/frontend/package.json`, `packages/kor-travel-map-admin/frontend/components.json`, `packages/kor-travel-map-admin/frontend/README.md:289-291`, `packages/kor-travel-map-api/README.md:173-175`, `packages/map-marker-react/package.json:4-6`, `packages/map-marker-react/README.md:11-27`, `packages/map-marker-react/src/index.ts:1-2`, `packages/map-marker-react/src/maki.ts:1-2`, `packages/kor-travel-map-user-client/package.json:4-6`, `packages/kor-travel-map-user-client/README.md:10`, `packages/kor-travel-map-admin/frontend/src/components/ui/*`(32파일 첫 줄), `packages/kor-travel-map-admin/frontend/src/components/ui/data-table.tsx:6`, `packages/kor-travel-map-admin/frontend/src/app/globals.css:48-49,72,88,276`, `src/kortravelmap/category/__init__.py:1-11`, `src/kortravelmap/category/_definitions.py:7,45`, `src/kortravelmap/core/address.py:3,10`, `docs/architecture/category.md:452-465`, `docs/architecture/debug-ui-package.md:360,583-592`, `docs/adr/README.md:39,45,59`, `docs/archive/journal-2026-05a.md:3439-3442,3710-3711`, `tests/unit/test_frontend_dependency_security.py:78,201`
6. weather `LICENSE`, `README.md:123,129-131,155-167`, `pyproject.toml:1-26,74`, `packages/kor-travel-weather-api/pyproject.toml:1-20`, `packages/python-airkorea-api/pyproject.toml:1-25`, `packages/python-airkorea-api/LICENSE`, `packages/python-airkorea-api/README.md:4,265`, `packages/kor-travel-weather-admin/frontend/package.json`, `packages/kor-travel-weather-admin/frontend/package-lock.json`, `packages/kor-travel-weather-admin/frontend/app/tokens.css:2,14,25,38`, `packages/kor-travel-weather-admin/frontend/app/globals.css:2,8,1911`, `packages/kor-travel-weather-admin/frontend/components/admin-shell.tsx:3,26`
7. pinvi `README.md:242-244`, `AGENTS.md:321`, `apps/api/pyproject.toml:1-6`, `apps/etl/pyproject.toml:1-5`, `package.json` + 9개 workspace `package.json`, `package-lock.json`(`vworld-map-*` `file:`, radix 21종), `apps/mobile/vendor/vworld-map-core-1.0.0.tgz`, `apps/mobile/vendor/vworld-map-rn-1.0.0.tgz`, `apps/web/vendor/vworld-map-web-1.0.0.tgz`(각 `package/package.json`), `docs/integrations/maplibre-vworld.md:1-40`, `apps/web/Dockerfile:13-22`, `apps/mobile/package.json:23-26`, `apps/web/app/(admin)/admin/layout.tsx:46`, `apps/web/app/globals.css:1,20,22`, `apps/web/components/admin/*.tsx`·`admin/ui/*.tsx`(첫 6행 이식 주석 35/50), `apps/web/components/admin/ui/data-table.tsx:2,14,115,241`, `apps/web/components/ui/Button.tsx:1`, `apps/mobile/components/ui.tsx:14-16`, `packages/design-tokens/src/*`, `.agents/skills/postgres/SKILL.md:18-19`, `.claude/skills/postgres/SKILL.md:16`, `docs/decisions.md:593`
8. canview `LICENSE`, `README.md:54-58`, `dbc/README.md:9-40`, `dbc/opendbc/LICENSE:1-3`, `AGENTS.md:120`
9. common `LICENSE`, `git ls-files`(LICENSE 1건), `git status`(미추적 `docs/`·`tools/` 등), `docs/survey/cross/backend.md:49,417,439`, `docs/survey/cross/ui-components.md:80,105-125,305-320`, `docs/survey/cross/docs-conventions.md:364,383,387`, `docs/survey/inventory/pinvi.md:6,284,323`, `docs/survey/inventory/kor-travel-map.md:6`, `docs/survey/inventory/kor-travel-concierge.md:6,220`, `docs/survey/inventory/kor-travel-geo.md:6`
10. mvr `LICENSE`, `README.md:142-144`, `package.json:1-6`, `packages/vworld-map-core/package.json`, `packages/vworld-map-web/package.json`, `packages/vworld-map-rn/package.json`, `apps/expo-example/LICENSE:1-3`, `git log -- LICENSE`(`168f733` 2026-06-16)
11. mvj `LICENSE`, `package.json:33`, `README.md:263`
12. 사용자 홈 `C:/Users/digit/.agents/skills/hallmark/SKILL.md:1-15,461`(심볼릭 링크 `~/.claude/skills/hallmark`)
13. 외부(2026-09-06 WebFetch): `https://www.gnu.org/licenses/gpl-faq.en.html`(#IfLibraryIsGPL #GPLStaticVsDynamic #LinkingWithGPL #GPLInProprietarySystem #ReleaseUnderGPLAndNF #HeardOtherLicense #DeveloperViolate #GPLModuleLicense #WhatIsCompatible #VersionThreeOrLater #OnlyLatestVersion #GPLRequireSourcePostedPublic #UnreleasedMods #InternalDistribution #RequiredToClaimCopyright #HowIGetCopyright), `https://github.com/timescale/pg-aiguide`(Apache-2.0), `https://github.com/digitie/python-kraddr-base`(GPL-3.0), `https://github.com/digitie/python-kma-api`(GPL-3.0-or-later), `https://github.com/digitie/python-vworld-api`(GPL-3.0), `https://github.com/digitie/python-kasi-api`(GPL-3.0-or-later). 참조만(미확인): `https://www.gnu.org/licenses/gpl-3.0.html`(§4·§5·§7·§14), `https://www.gnu.org/licenses/license-list.html#apache2`, `https://github.com/shadcn-ui/ui/blob/main/LICENSE.md`, `https://openfontlicense.org`, `https://reuse.software/spec/`, `https://peps.python.org/pep-0639/`, `https://docs.npmjs.com/cli/v10/configuring-npm/package-json#license`
