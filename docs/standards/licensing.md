# kor-travel-common 라이선스·출처 규약

이 문서는 [규칙 문서 색인](README.md)에 속한 저장소 라이선스 정책, 고지 파일 구성, SPDX 헤더, 패키지 메타데이터, 소비 저장소에서 코드를 추출할 때의 gate의 정본이다. 정본 지위: **확정 초안** — [브리프](../plan/design-brief.md) D-17·D-11·D-16을 규칙 ID `LIC-n`으로 옮긴 것이며, 고지 파일 실물(T-003; 구현·원문 확보 후 2인 검토)과 외부 결정(T-020 pinvi L6, T-021 ktc·ktdm L8)에서 대조해 확정하는 task가 남아 있다. 마지막 갱신: 2026-09-07.

법률 자문이 아니다. 판단 근거는 GNU 공식 FAQ·GPLv3 원문과 조사 기준 커밋의 실제 파일이며, 근거 절은 [licensing 횡단 비교](../survey/cross/licensing.md)(`lic`)로 인용한다.

## 1. 목표와 기준

- common은 `GPL-3.0-or-later`다. 7개 소비 저장소 중 5개(airport·geo·map·weather + pinvi 이식 코드의 원천)가 이미 GPL 계열이고 사람 기여자가 한 명(`digitie`/`Youn-sok Choi`, 동일 이메일)이라 재라이선스 결정에 제3자 동의가 필요 없다(사실·추정: `lic` §2.1·§2.6).
- 수령자가 받는 고지가 서로 모순되면 권리가 불명확해진다(`lic` §3.6). 따라서 "같은 소유자니까 명시 없이 된다"는 성립하지 않으며, 모든 예외·재선언은 `NOTICE`와 파일 헤더에 적는다.
- GPLv3 §7 추가 허가(MIT 앱이 링크할 수 있게 하는 예외)는 두지 않는다(O-2 기본값). 이유: 모든 파일에 예외 문구를 유지·검증하는 비용이 크고 "GPL common" 전제와 어긋난다(`lic` §3.6).
- 코드를 옮기기 전에 권리를 확인한다. 차단 항목 B1~B8(§8)이 열려 있는 원천에서는 추출하지 않는다.

## 2. 문서 사용법

| 변경 대상 | 상세 정본 |
|---|---|
| 저작권자·라이선스 버전·연락처 | [NOTICE](../../NOTICE) |
| 서드파티 고지 목록 | [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md) |
| 라이선스 원문 사본 | [원문·출처 안내](../../LICENSES/README.md) |
| 이식 파일군의 원천·커밋·경로 | [PROVENANCE.md](../../PROVENANCE.md) |
| AI 보조 생성물·기여 조건 | [CONTRIBUTING.md](../../CONTRIBUTING.md) |
| 파일 헤더 검사 | [check_spdx.py](../../tools/check_spdx.py), [tools README](../../tools/README.md) |
| 패키지 동봉·`license` 필드 | 이 문서 §6, 절차는 [release](../runbooks/release.md) |
| 소비 저장소 정렬 요청 문서 | T-020·T-021 산출물, [consumer adoption](../runbooks/consumer-adoption.md) |
| 결정 이유 | [ADR-004](../adr/004-gpl-3-0-or-later-and-provenance-gate.md)([ADR 색인](../adr/README.md)) |
| 조치·차단 원본 | [licensing 횡단 비교](../survey/cross/licensing.md) §3.7·§4, [공통화 매트릭스](../survey/commonality-matrix.md) §4.1 |

## 3. 저장소 라이선스 정책

| ID | 규칙 | 근거 |
|---|---|---|
| LIC-1 | common 루트 [LICENSE](../../LICENSE)는 GPL-3.0 전문이며, 버전 고지 `GPL-3.0-or-later`는 `NOTICE`·`README`·패키지 메타데이터·파일 헤더에 명시한다. 버전 미지정은 GPLv3 §14로 수령자가 임의 버전을 고를 수 있게 하므로 금지 | `lic` §2.2 D3·§3.1 |
| LIC-2 | §7 추가 허가·이중 라이선스는 두지 않는다. 필요해지면 새 ADR과 `NOTICE` 개정으로만 | O-2 기본값; `lic` §3.6 |
| LIC-3 | 소비 앱 정렬 권고: ktc·ktdm은 루트 `LICENSE`를 `GPL-3.0-or-later`로 정렬(L8, 각 1 PR; ktc는 이미 GPL `python-vworld-api`에 의존). 결정 전에는 common **코드**를 링크하지 않고 규칙 문서·`tokens.json` 참조까지만(D-16). 규칙을 따르는 것 자체는 파생이 아니다(추정) | `lic` §3.6·§4 B9; T-021 |
| LIC-4 | pinvi는 L6(공개 + `GPL-3.0-or-later`, 루트 `LICENSE` 추가, `apps/api/pyproject.toml` MIT 수정, `docs/integrations/maplibre-vworld.md:23` "MIT" 정정, README/AGENTS 상충 해소)을 1 PR로 처리한다(O-1 기본값). 완료 전 pinvi 파일 추출 금지(B1) | `lic` §2.2 D4·D5·§3.6; T-020·T-420 |
| LIC-5 | geo `GPL-3.0-only` 유래 파일은 common에서 `SPDX-License-Identifier: GPL-3.0-only`를 병기한다. 권리자가 `-or-later`로 재선언하면(O-20 권고) 병기를 제거한다 | `lic` §2.2 D2·§3.2 |
| LIC-6 | map 루트 `LICENSE` 25행 요약본은 전문으로 복원하고 저작권·버전 고지는 `NOTICE`로 옮긴다(L9). 전 앱 `package.json`·`pyproject.toml`에 `license` 필드를 넣는다(L11) | `lic` §2.2 D1·§2.1; map T-410·airport T-433 |
| LIC-7 | 배포(convey) 판단: 공개 저장소·외부 배포 이미지·앱 바이너리는 배포이고 사내 사용은 아니다(FAQ `#InternalDistribution`·`#UnreleasedMods`). pinvi Docker·EAS 배포 여부는 미확인이며 L6 결정의 입력이다 | `lic` §2.5·§3.1 |

### 3.1 소비 저장소 현황(조사 기준 커밋, 사실)

| 저장소 | 루트 `LICENSE` | 메타데이터 `license` | 판정 | 정렬 조치 |
|---|---|---|---|---|
| airport | GPL-3.0 원문(버전 미지정) | 없음 | GPL-3.0 | `-or-later` 명시·`license` 필드(L11) |
| concierge | MIT | 없음(pyproject 없음) | MIT + GPL 의존(`python-vworld-api`) | L8(O-2) |
| ktdm | MIT | 없음 | MIT, GPL 의존 없음 | L8(O-2); 규칙 문서 참조만이면 MIT 유지 가능 |
| geo | GPL-3.0 원문 | `GPL-3.0-only` | `-only` | L10(O-20) |
| map | 25행 요약본 | `GPL-3.0-or-later`(하위 2패키지 MIT) | `-or-later` | L9 전문 복원 |
| weather | GPL-3.0 원문 | 루트 `GPL-3.0-or-later`, 하위 없음 | `-or-later` | 하위 `license` 필드(L11) |
| pinvi | **없음** | `apps/api` MIT | 미결(README "비공개" vs AGENTS "공개") | L6(O-1) |
| common | GPL-3.0 원문 | 아직 없음 | 초기 | L1·L5 |

근거: `lic` §2.1; 정정값은 [survey README](../survey/README.md) §6.2 항목 8~11.

## 4. 고지 파일 구성

| ID | 파일 | 내용 | 근거 |
|---|---|---|---|
| LIC-8 | `LICENSE` | GPL-3.0 전문(현재 있음). 부록 자리표시자는 채우지 않아도 되며 고지는 `NOTICE`에 | GPLv3 "How to Apply"; `lic` §3.3 |
| LIC-9 | `NOTICE` | `Copyright (C) 2026 Youn-sok Choi (digitie)`, `SPDX-License-Identifier: GPL-3.0-or-later`, 연락처, 패키지 버전 표기 규칙, §7 추가 허가 없음 명시 | D-17; `lic` §3.3 |
| LIC-10 | `THIRD_PARTY_NOTICES.md` | 항목: shadcn/ui(MIT), `@base-ui/react`(MIT), radix(MIT; geo 유래·pinvi 전이 21종은 B5 역추적 후), `class-variance-authority`(**Apache-2.0**, 고정 버전에 NOTICE가 있으면 원문 유지), lucide(ISC와 Feather 파생 MIT; 인라인 SVG로 가져와도 전체 고지 유지), `tailwind-merge`·`clsx`·`tw-animate-css`(MIT), `maplibre-gl`(BSD-3-Clause, 이름 홍보 금지 조항), pretendard(OFL-1.1 전문; 폰트 파일은 미배포), TanStack(MIT), zod(MIT). 각 항목에 버전·원문 URL·사본 위치. `python-*-api` 13종은 B7 확인 후 | D-17; `lic` §2.4·§3.3 |
| LIC-11 | `LICENSES/` | SPDX 파일명 원문: `GPL-3.0-or-later.txt`, `MIT.txt`, `Apache-2.0.txt`, `ISC.txt`, `BSD-3-Clause.txt`, `OFL-1.1.txt`(원문·버전·digest는 LICENSES 안내) | `lic` §3.3 |
| LIC-12 | `PROVENANCE.md` | 파일군별 표 `ID \| 파일군 \| 원천 저장소 \| 커밋 \| 경로 \| 라이선스 \| 수정`(`lic` §2.3 형식). 이식 PR마다 행을 추가하며 원천 커밋은 40자 SHA 또는 조사 기준 단축 SHA + 저장소명 | `lic` §2.3·§3.3 L2 |
| LIC-13 | `CONTRIBUTING.md` | "AI 보조 생성물(Codex·Claude 계정 커밋 포함)은 지시자인 권리자가 GPL-3.0-or-later로 배포한다"(B8), 외부 기여 시 동일 라이선스 조건, SPDX 헤더 의무 | `lic` §2.6·§4 B8·§6-6 |
| LIC-14 | 패키지 동봉 | npm tarball·Python wheel·sdist 각각에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`와 해당 서드파티 저작권 사본을 동봉하고 고지의 상대 링크를 수령자가 따라갈 수 있는지 확인(npm은 `files`와 무관하게 `LICENSE*` 포함; Python은 PEP 639 `license-files`). 벤더 tgz에 라이선스가 없던 D7 재발 방지 | D-11; `lic` §2.2 D7·§3.3·§3.5 |

### 4.1 NOTICE·PROVENANCE 예시

`NOTICE`(형식만; 연락처는 실제 파일에):

```text
kor-travel-common
Copyright (C) 2026 Youn-sok Choi (digitie)
SPDX-License-Identifier: GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version.
No additional permissions under GPLv3 section 7 are granted.
Third-party notices: THIRD_PARTY_NOTICES.md. Provenance of ported files: PROVENANCE.md.
```

`PROVENANCE.md` 행(`lic` §2.3 형식):

| ID | 파일군 | 원천 저장소 | 커밋 | 경로 | 라이선스 | 수정 |
|---|---|---|---|---|---|---|
| M1 | `packages/ui/src/button.tsx` | kor-travel-map | `c494e227` | `packages/kor-travel-map-admin/frontend/src/components/ui/button.tsx` | GPL-3.0-or-later(shadcn/ui MIT 파생) | variant 정리, forwardRef 제거 |
| CV1 | `tools/validate_plan.py` | canview | `1f93b8a` | `tools/validate_plan.py` | GPL-3.0 → `-or-later` 재선언 | docstring 1줄 |

## 5. SPDX 헤더 규약

| ID | 규칙 | 근거 |
|---|---|---|
| LIC-15 | common의 모든 소스 파일(`*.ts`·`*.tsx`·`*.js`·`*.mjs`·`*.cjs`·`*.css`·`*.py`·`*.toml`·`*.yml`·`*.yaml`·`*.sh`·`.editorconfig`)은 첫 비어 있지 않은 줄부터 SPDX 헤더로 시작한다. **Hallmark 스탬프는 common 파일에 없다**(D-13·D-17; 스킬 본문 인용 금지 B3). 조사 문서에서 본 "첫 줄 스탬프" 관례는 소비 저장소 것이며 common으로 가져오지 않는다 | `lic` §2.2 D10·§3.4 |
| LIC-16 | 헤더 형식(주석 문법은 파일 종류별: TS/CSS `//`·`/* */`, Python/TOML/YAML/shell `#`). `Origin:`은 이식 파일 필수, `Derived-From:`은 서드파티 파생(shadcn 생성물 등) 시 필수, `Modified:`는 원천과 다를 때 필수. 세 행은 GPLv3 §5(a)(수정 고지)·§7(b)(저작자 표시 보존)를 파일 단위로 충족한다 | `lic` §3.4 |
| LIC-17 | 예외(헤더 없음 허용): `*.md`(문서), `*.json`(주석 불가; `tokens.json` 등 생성물은 생성기가 `$comment`나 sidecar로 출처 기록), lockfile, `LICENSES/*`, `.gitkeep`, 바이너리. `dist/`·`*.d.ts` 생성물은 빌드가 헤더를 삽입하거나 `THIRD_PARTY_NOTICES.md`로 대신한다(T-101·T-201에서 확정) | — |
| LIC-18 | [check_spdx.py](../../tools/check_spdx.py)는 common 트리의 대상 파일에 `SPDX-License-Identifier`·`SPDX-FileCopyrightText`가 없거나 값이 비어 있으면 즉시 fail한다(baseline 없음, common은 신규 저장소). geo `-only` 유래 파일의 식별자 검사, `Origin:` 행의 저장소·커밋 형식 검사 포함 | D-17 |
| LIC-19 | 앱 사본과 common 원본의 drift 비교(`tools/ui_drift.py` T-211 등)는 선두 주석 블록(SPDX·Hallmark 스탬프·이식 주석)을 정규화한 뒤 비교한다 | D-17 |

헤더 예시(TS; Python은 `#`로 치환):

```text
// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-map@c494e227 packages/kor-travel-map-admin/frontend/src/components/ui/button.tsx (GPL-3.0-or-later)
// Derived-From: shadcn/ui (MIT) — see THIRD_PARTY_NOTICES.md
// Modified: 2026-09-06 — variant 7종·size 8종으로 정리, forwardRef 제거
```

### 5.1 파일 종류별 주석 문법

| 파일 | 헤더 시작 | 비고 |
|---|---|---|
| `*.ts`·`*.tsx`·`*.mjs`·`*.cjs` | `// SPDX-License-Identifier: …` | `'use client'`·`'use no memo'` 지시문은 헤더 **다음** 첫 문장(주석은 directive prologue를 깨지 않는다 — 추정, T-201 Next 빌드로 확인) |
| `*.css` | `/* SPDX-License-Identifier: … */` | `@import "tailwindcss"`보다 앞 |
| `*.py` | `# SPDX-License-Identifier: …` | shebang이 있으면 그 다음 줄 |
| `*.toml`·`*.yml`·`*.yaml`·`*.sh`·`.editorconfig` | `# SPDX-License-Identifier: …` | YAML front-matter가 있는 파일은 `---` 앞 |
| `*.md` | 헤더 없음 | 문서 저작권은 `NOTICE`·README 라이선스 절이 대신 |
| `*.json`·lockfile·바이너리 | 헤더 없음 | LIC-17 |

### 5.2 검사 범위와 출처 대조

검사기는 저장소 전체의 LIC-15 확장자를 검사한다. T-003 초안의 packages·tools·templates 최소 범위에 더해 tests·workflow·설정도 기존 LIC-15 범위에 포함한다. Python·shell·JavaScript CLI의 shebang 바로 다음 줄을 허용한다. 헤더는 선두의 연속된 주석 블록이며 문자열·docstring·실행문 뒤 주석은 인정하지 않는다.

- 허용 식별자는 `GPL-3.0-or-later`, `GPL-3.0-only`, `GPL-3.0-or-later AND GPL-3.0-only`다. LIC-5의 병기는 -only 식별자 또는 AND 결합으로 표현하며 geo 원천에서 -or-later 단독 표기는 실패다.
- `Origin`은 `저장소@7~40자 소문자 Git SHA 원천상대경로`와 선택적 `(원천 라이선스)`다. 자체 작성 파일은 Origin을 만들지 않는다. 이식 소스는 [PROVENANCE](../../PROVENANCE.md)에 명시한 경로와 저장소·커밋을 대조하며, 수정 행은 날짜·요약을 가진 `Modified`, 서드파티 파생 행은 `Derived-From`도 요구한다. 코드 복사 여부·권리 확인·수정 내용의 진위는 원천 diff와 2인 리뷰가 맡는다.
- `dist/`·`build/`·`.next/`·`.turbo/`·`coverage/`, 의존성·환경 디렉터리(`node_modules/`·`.venv/`·`venv/`·`__pycache__/`), `.git/`·`LICENSES/`와 `*.gen.*`·`*.d.ts`·lockfile은 제외한다. 생성물의 고지 동봉은 LIC-17과 패키지 gate에서 별도로 확인한다.
- 검사 범위 0개, 읽기 실패, 대상 심볼릭 링크, 헤더·출처 오류는 exit 1이다. 정상 파일을 실제 검사한 경우에만 exit 0이다. `--root`는 독립 fixture 또는 다른 common checkout 검증에 쓴다.
- 현재 CLI와 회귀 시험은 실행 가능하며 CI의 필수 SPDX 명령 연결·Windows job은 T-009가 담당한다. 현재 CI 연결이 끝난 것처럼 표시하지 않는다.

## 6. 패키지 메타데이터

| ID | 대상 | 필드·값 | 현재 상태(사실) |
|---|---|---|---|
| LIC-20 | npm `package.json`(`@kor-travel/tokens`·`@kor-travel/ui`) | `"license": "GPL-3.0-or-later"`(SPDX 식별자), `files`에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`, 공개 게시 전 `private: true`, `repository`·`author` | 조사 대상 프런트 패키지 전부 `license` 없음; map 하위 2개만 MIT(`lic` §2.1·§3.5) |
| LIC-21 | Python `pyproject.toml`(`kor-travel-common`) | PEP 639 `license = "GPL-3.0-or-later"` + `license-files = ["LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"]`. hatchling의 PEP 639 지원 여부는 T-302에서 확인(미확인)하고 미지원이면 `{ text = "GPL-3.0-or-later" }` 표 형식 유지. classifier `License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)` 병기 | geo·map·weather 표 형식; airport·ktdm·pinvi etl 없음(`lic` §3.5) |
| LIC-22 | Docker 이미지 | 라벨 `org.opencontainers.image.licenses=GPL-3.0-or-later`, 이미지 내 `/licenses/`에 §4 파일 사본 | 미확인(`lic` §3.5); [ci-deploy](ci-deploy.md) CI-36 |
| LIC-23 | 공유 라이브러리 요청 | `maplibre-vworld-react` 하위 패키지 `license` 필드·`LICENSE` 동봉·tgz 재생성(L7), `maplibre-vworld-js` `license` `ISC`→`MIT` 정정(L13)은 common 범위 밖이며 T-505 요청 문서로 | `lic` §2.2 D6·D7 |

## 7. 추출 규칙(추출 gate)

소비 저장소에서 common으로 파일을 옮기는 PR은 아래 표의 조건을 모두 만족해야 하며, PR 본문에 `PROVENANCE.md` 행과 헤더 diff를 evidence로 붙인다(D-24 이관 PR 규격).

| ID | 원천 | 규칙 | 근거 |
|---|---|---|---|
| LIC-24 | GPL 원천(map `-or-later`, weather `-or-later`, airport GPL 버전 미지정) | 그대로 이동. airport 유래는 common에서 `-or-later`로 명시(권리자 동일). `Origin:` 필수 | `lic` §3.2 |
| LIC-25 | geo(`GPL-3.0-only`) | 이동 가능하되 `SPDX-License-Identifier: GPL-3.0-only` 병기(LIC-5). geo `codes.py`처럼 클린룸 재구현 선례(ADR-035)는 `Origin:` 대신 `Derived-From:` 없이 자체 작성으로 표기 | `lic` §2.3 G2·§3.2 |
| LIC-26 | MIT 원천(ktc·ktdm 자체 코드) | 이동 가능. MIT 저작권·허가문을 `THIRD_PARTY_NOTICES.md` 또는 파일 헤더에 유지. 권리자가 같으므로 GPL 재선언도 가능하나 재선언은 `NOTICE`에 기록 | `lic` §3.2 |
| LIC-27 | pinvi(자체 코드 P4, 이식 코드 P1·P2) | **L6 완료 전 추출 금지**(B1). 완료 후 P1(map 유래)·P2(geo 유래)는 원천 라이선스로 되돌리고 pinvi 수정분은 같은 권리자로 처리 | `lic` §2.3·§4 B1 |
| LIC-28 | 벤더 tgz(`vworld-map-*`)·`maplibre-vworld-react`·`python-*-api`·`python-kraddr-base` | **영구 금지**(B2). 이미 분리된 공유 라이브러리는 의존만 한다 | D-01·D-23; `lic` §4 B2 |
| LIC-29 | Hallmark `SKILL.md` 본문·참조 문서 | 규칙 문서에 문장 인용 금지(B3, L16). 스탬프 형식조차 common 파일에는 쓰지 않는다(LIC-15) | `lic` §2.5·§4 B3 |
| LIC-30 | ktc `AppShell.tsx`·`globals.css`의 map IA·토큰 값 | 코드 복사인지 개념 참조인지 파일 diff로 확정한 뒤(B4) `PROVENANCE.md`에 기록. 복사면 MIT 저장소 안의 GPL 코드 상태이므로 L8과 함께 정리 | `lic` §2.3 C1·C3·§4 B4 |
| LIC-31 | shadcn CLI 생성 컴포넌트(map M1·geo G1·ktc C1·airport WIP) | MIT 고지 유지(`Derived-From: shadcn/ui (MIT)`). 생성 시점 shadcn 버전은 미기록이므로 shadcn `LICENSE.md` 원문 확보 후 고지(B6). common은 CLI 재생성이 아니라 소스 소유 방식으로 헤더를 유지 | `lic` §2.3·§3.4·§4 B6 |
| LIC-32 | pg-aiguide 스킬(Apache-2.0) | common은 배포하지 않는다(각 앱 L12). 배포하기로 하면 Apache 전문 + NOTICE 동봉이 common 책임 | D-17; `lic` §2.5·§6-7 |
| LIC-33 | 봇 계정(Codex·Claude) 커밋분 | 권리 귀속 미확인(B8). `CONTRIBUTING.md` 문구(LIC-13)로 처리하고 외부 청구권자는 없음 | `lic` §2.6·§4 B8 |
| LIC-34 | canview(구조 참조) | 문서 구조·규약 어휘만 차용. `tools/validate_*.py`는 canview 동명 도구를 적응한 것이므로 `Origin: canview@1f93b8a tools/…`를 헤더에 기록(GPL-3.0 → `-or-later` 재선언, 권리자 동일) | [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §1.2; [tools README](../../tools/README.md) |

### 7.1 이관 PR 체크리스트

common 측 이식 PR 본문(`.github/pull_request_template.md`)에 다음을 evidence로 붙인다. 소비 저장소 쪽 PR은 [consumer adoption](../runbooks/consumer-adoption.md)의 규격을 따른다.

1. 원천 저장소·커밋·경로·라이선스(`PROVENANCE.md` 행)와 B1~B10 해당 여부.
2. 각 파일 헤더의 `SPDX-License-Identifier`·`Origin:`·`Derived-From:`·`Modified:`(`tools/check_spdx.py` 출력).
3. 새 서드파티 의존성의 라이선스와 `THIRD_PARTY_NOTICES.md` 행(cva Apache-2.0은 NOTICE 원문 포함 여부).
4. geo 유래 파일의 `-only` 병기(LIC-5) 또는 재선언 근거(O-20).
5. 원천이 MIT(ktc·ktdm)면 고지 유지 위치, pinvi면 L6 완료 링크(T-020 evidence).
6. 벤더 tgz·공유 라이브러리·Hallmark 본문이 diff에 없음을 확인한 grep 명령과 결과.

## 8. 조치 목록과 차단 항목 요약

원본은 `lic` §3.7(L1~L16)·§4(B1~B8)와 [공통화 매트릭스](../survey/commonality-matrix.md) §4.1(B9·B10)이다. 여기서는 소유자와 task만 접었다.

| ID | 조치 | 대상 | 우선 | task |
|---|---|---|---|---|
| L1 | `NOTICE`·README 라이선스 절 | common | 높음 | T-003 |
| L2 | `PROVENANCE.md` 초안(§2.3 표) | common | 높음 | T-003, 이식 PR마다 |
| L3 | `THIRD_PARTY_NOTICES.md` + `LICENSES/` | common | 높음 | T-003 |
| L4 | 헤더 규약 확정 + `check_spdx` | common | 높음 | T-003 |
| L5 | npm/Python 메타데이터 규약 첫 적용 | common | 높음 | T-101·T-302 |
| L6 | pinvi 라이선스 결정·정합 PR | pinvi | 높음(B1 해제) | T-020·T-420(O-1) |
| L7 | `maplibre-vworld-react` `license`·`LICENSE`·tgz 재생성 | 공유 lib | 높음 | T-505 요청 |
| L8 | ktc·ktdm 루트 정렬 결정 | ktc·ktdm | 중간 | T-021(O-2) |
| L9 | map `LICENSE` 전문 복원 | map | 중간 | T-410 |
| L10 | geo `-only` → `-or-later` 재선언 여부 | geo·common | 중간 | O-20 |
| L11 | 전 앱 `license` 필드 | 각 앱 | 중간 | T-433 외 앱별 |
| L12 | pg-aiguide Apache 전문·NOTICE 동봉 | 6개 저장소 | 중간 | 각 앱(common 미배포) |
| L13 | `maplibre-vworld-js` `license` 정정 | 공유 lib | 낮음 | T-505 요청 |
| L14 | ktc `LICENSE` 저작권자 문구 통일 | ktc | 낮음 | T-021 |
| L15 | `python-airkorea-api` 스냅샷 vs GitHub 원본 정본 결정 | weather | 낮음 | T-481 |
| L16 | Hallmark 원천 확인 전 인용 금지 | common 규칙 문서 | 낮음(B3) | 상시 |

| ID | 차단 | 해제 조건 |
|---|---|---|
| B1 | pinvi 모든 파일 | L6 완료 |
| B2 | 벤더 tgz·`maplibre-vworld-react` 소스 | 영구(의존만) |
| B3 | Hallmark `SKILL.md` 본문 | 원천 확인 |
| B4 | ktc `AppShell.tsx`·`globals.css`의 map 참조 | diff로 복사 여부 확정 후 `PROVENANCE.md` |
| B5 | pinvi 락파일 `@radix-ui/*` 21개 | `npm ls` 역추적 |
| B6 | shadcn 생성 컴포넌트의 버전·registry 항목 | shadcn `LICENSE.md` 원문 확보 |
| B7 | `python-*-api` 중 라이선스 미확인 저장소 | 각 `LICENSE` 확인 후 `THIRD_PARTY_NOTICES` |
| B8 | 봇 계정 커밋분 | `CONTRIBUTING.md` 문구(LIC-13) |
| B9 | ktc·ktdm이 common 코드를 링크 | L8(O-2) |
| B10 | map·pinvi·ktdm·concierge 간 sha256 pin 계약 | 흡수 부적합 — [openapi](openapi.md) M10 규약만 |

## 9. 검증 gate

| gate | 검사 | 실패 조건 | 실행 |
|---|---|---|---|
| 헤더 | `python3 -B -X utf8 tools/check_spdx.py` | 대상 파일에 `SPDX-License-Identifier` 없음, `-only` 병기 누락, `Origin:` 형식 오류 | 로컬 CLI; CI 필수 연결은 T-009 |
| 고지 목록 | `THIRD_PARTY_NOTICES.md` 항목 ↔ 루트 `package-lock.json`·`uv.lock`의 `license` 필드 대조(후보 도구) | 락에 있는 직접 의존성이 목록에 없음 | T-101·T-302에서 확정 |
| 출처 | 이식 PR 체크리스트: `PROVENANCE.md` 행·헤더 `Origin:`·B1~B10 해당 여부 | 행 누락, 차단 원천 | PR 리뷰(D-04 비면제: `packages/*` 공개 API) |
| 동봉 | `npm pack` tarball·wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 존재 | 누락 | `packages`·`python-package` job |
| 문서 | 이 문서 변경은 2인 독립 리뷰 | — | [agent workflow](../runbooks/agent-workflow.md) |

## 10. 열린 결정

| # | 항목 | 기본값 | 상태 |
|---|---|---|---|
| O-1 | pinvi 라이선스·공개 여부(L6) | 공개 + `GPL-3.0-or-later`, 1 PR | 열림(사용자 확인 필요) |
| O-2 | ktc·ktdm 정렬 vs common §7 추가 허가(L8) | GPL 정렬(각 1 PR), 추가 허가 없음 | 열림(사용자 확인 필요) |
| O-20 | geo `GPL-3.0-only` 재선언 | `-or-later` 권고, 전까지 `-only` 병기 | 열림(사용자 확인 필요) |
| — | `maplibre-vworld-react`를 MIT(또는 이중)로 재선언할지 | GPL-3.0 유지 + pinvi 문서 정정 | 후보(`lic` §6-4; T-505) |
| — | Hallmark 스킬 원저작자·라이선스 | 미확인, 인용 금지 유지 | 후보(`lic` §6-5) |
| — | pretendard OFL 사본 위치(웹 번들 배포 시 의무 범위) | `LICENSES/OFL-1.1.txt` + `THIRD_PARTY_NOTICES.md`; 폰트 파일은 common이 배포하지 않으므로 앱 책임 | 후보(`lic` §6-10; D-12 폰트 로딩 앱 책임) |
| — | Docker 이미지·EAS 빌드의 실제 외부 배포 여부 | 미확인(L6 입력) | 후보(`lic` §6-9) |

## 11. 근거

- [브리프](../plan/design-brief.md) D-01·D-11·D-13·D-16·D-17·D-23·D-24·O-1·O-2·O-20.
- [licensing 횡단 비교](../survey/cross/licensing.md) §2.1(선언 현황), §2.2(D1~D10), §2.3(파일군 M/P/G/W/C/K/T/A/V), §2.4(의존성 라이선스), §2.5(벤더링 상세), §2.6(기여자), §3.1(GNU FAQ 앵커), §3.2(재라이선스 판정), §3.3~§3.5(고지·헤더·메타데이터 후보), §3.6(소비 앱 정렬), §3.7(L1~L16), §4(B1~B8), §5·§6.
- [공통화 매트릭스](../survey/commonality-matrix.md) §4.1 B1~B10, §4.2 D24·D25.
- [survey README](../survey/README.md) §6.2 항목 8~11·13(라이선스 관련 문서 간 정정: airport GPL 원문, pinvi MIT는 `apps/api`만, 벤더 tgz 원천 GPL, map 요약본).
- [canview 구조 체크리스트](../survey/cross/canview-structure-checklist.md) §1.2(validator 적응 사실).
- 외부(2026-09-06 확인, `lic` §7-13): GNU GPL FAQ `https://www.gnu.org/licenses/gpl-faq.en.html`, GPLv3 원문 `https://www.gnu.org/licenses/gpl-3.0.html`(§4·§5·§7·§14). 참조만(미확인): REUSE `https://reuse.software/spec/`, PEP 639 `https://peps.python.org/pep-0639/`, OFL `https://openfontlicense.org`.
