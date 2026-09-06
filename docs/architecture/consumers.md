# 소비자

> airport의 WIP·Admin 범위는 조사 이후 변경됐다. [인계 시점 재확인](../plan/handoff-verification.md)과 T-430의 현재 SHA·잔여 gate 대조를 먼저 적용한다. 아래 조사 기준 표를 최신 배포 상태로 해석하지 않는다.

- 정본 지위: 소비자 7(+pinvi 표면 3)의 현재 상태·채택 순서·선행 조건의 정본(초안). §5 채택 버전 표는 T-012부터 [통합 지도](../integration-map.md)(생성물)가 정본이 되고 여기서는 링크만 남긴다. 확정 task: T-008(★이번 PR)·T-011·T-012. 마지막 갱신: 2026-09-06.
- 근거: [브리프](../plan/design-brief.md) §0·D-16·D-19·D-20·D-23·D-28·D-29, `docs/survey/README.md` §2.1(기준 커밋)·§6.2(정정값), `docs/survey/commonality-matrix.md` §1.5·§3.2·§3.3·§4.1, `docs/survey/cross/licensing.md` §3.6, `docs/survey/cross/version-matrix.md` §1.1·§2.1·§3.2, `docs/survey/cross/ci-deploy.md` §1.1·§1.2, `docs/survey/cross/backend.md` §5.1.

이 문서는 [아키텍처 개요](README.md) §1의 소비자를 저장소 단위로 펼친다. gate 판정은 [채택 준비 기준](adoption-readiness.md), 이관 절차는 [consumer adoption runbook](../runbooks/consumer-adoption.md), 앱별 task는 [tasks](../tasks.md) T-4xx가 정본이다. 아래 사실은 조사 기준 커밋에 고정된 관찰이며 저장소가 바뀌어도 본문을 고치지 않고 분기 감사(T-506)에서 기준 커밋을 갱신한 절로만 확장한다.

## 1. 소비자 목록과 현재 상태(조사 기준 커밋, 사실)

| 약칭 | 저장소 | 기준 커밋 | 라이선스 | Admin 표면 | 프론트(설치 기준) | 백엔드 | 근거 |
|---|---|---|---|---|---|---|---|
| kta | kor-travel-airport | `2bb1111`(main); WIP `99b3f98` `codex/shadcn-ui-foundation` | GPL-3.0 원문 674행(버전 미지정) | 무인증 백업·collector-status 패널 + `/v1/admin/*`(ADR-003 무인증 의도, D-20) | main: 순수 CSS 1,844행, Next 16.3.2, React 19, TS 7.0.2, ESLint 없음; WIP: Tailwind 4.3.3 + shadcn `base-nova` + base-ui 1.8 | FastAPI, RFC7807(`code`·`request_id` 없음, 스펙 422 불일치), export만·CI drift 없음, `uv.lock` CI만(Docker pip) | `inv/kor-travel-airport` §1·§3.2·§9, `vm` §6 |
| ktc | kor-travel-concierge(TripMate) | `7945305` | MIT(정렬 대상 L8) | admin | Next 16.2.7, base-ui 1.5 `base-nova` 18종(map 계보 부분집합), `--ktc-*` 125회, `@config`, maplibre-gl 6.0 | FastAPI, `/api/v1`, `{detail}`, `requirements.txt` 4벌 하한만(`mcp<2` 사고 2026-09-04), CI 없음, 라우터 단일 파일 3,759줄 | `inv/kor-travel-concierge`, `vm` §5.2 |
| ktdm | kor-travel-docker-manager(ktdctl) | `862562d` | MIT(L8) | admin | Next 14.2.35, React 18.3.1, ESLint 8, Tailwind 4.3.1 `@theme` OKLCH, `ops-*` CSS, shadcn 미도입, Node 20 CI | FastAPI, `/api/v1`, `{detail}`, SQLite, Poetry(lock 미커밋), systemd+venv(컨테이너 아님), 포트 정본 `docs/ports.md` | `inv/kor-travel-docker-manager` §2·§6 |
| geo | kor-travel-geo(+kor-travel-geo-ui) | `1d9d74d` | GPL-3.0-only(O-20) | admin ui | Next 16.2.12, React 18.3.1(ADR-019), radix-ui 1.6 `radix-nova`, `@config` 잔존, Tailwind 4.3.1, openapi-typescript 7.13, Node 20 CI | FastAPI, `/v1/healthz`·`/v1/readyz`, envelope 3종(VWorld/v2/legacy), 검증 400, ruff+mypy strict+import-linter, Python lock 없음 | `inv/kor-travel-geo` §3.1·§9 |
| map | kor-travel-map(npm workspaces) | `c494e227` | GPL(25행 요약본, L9 전문 복원) | admin(UI 정본) + api + dagster | Next 16.2.12 exact, base-ui 1.6 `base-nova`(CLI 미설치), npm 12.0.1 exact + `verify-*.mjs`, Playwright 1.60 exact, e2e 30·vitest 42 | FastAPI 원형(`ProblemDetail`·`{data,meta}`·profile export `--check`), `starlette<1.0`·`alembic<1.20`, Python lock 없음 | `inv/kor-travel-map` §9, `oa` §3 |
| wx | kor-travel-weather | `6003da9` | GPL-3.0 | admin | Tailwind 없음, 2,495행 CSS(map 값 복사, hue navy, map 어휘 294회, `--rail` 17rem), Next 15.5.24, Vitest 3.2, Node 20 CI, react-query 선언만 | FastAPI, `Problem` 동형, `/health`·`/version`, `uv.lock` CI·Docker `--locked`, `python-airkorea-api` 벤더링 | `inv/kor-travel-weather` §3.1·§8·§9.1 |
| pinvi | PinVi(apps/web·mobile·api·etl) | `9af25e5`(shallow clone) | 루트 `LICENSE` 없음(README "비공개" vs AGENTS "공개", `apps/api` MIT) → L6 | admin(web) | admin: KTM 이식 28 primitive + base-ui 1.8 overlay만, `--color-admin-*`, `@config` v3 preset, webpack 강제(ADR-066), `AdminTable` 어댑터 35~36쪽, e2e 56·vitest 27 | FastAPI, `{error:{}}`, argon2id+JWT(10분)+RBAC, `uv.lock` 미소비(`pip install -e`), etl `python-kasi-api@main` | `inv/pinvi` §3.1·§3.2, `lic` §3.6 |

## 2. 채택 순서(D-16)

| 배포 단위 | 1차 | 2차 | 3차 | common 선행 |
|---|---|---|---|---|
| tokens | map(T-410)·weather(T-461, `tokens.css` 교체 + shim) | pinvi admin(T-421, L6 완료 조건)·airport(T-431, WIP 병합 후) | geo(T-441)·concierge(T-453)·ktdm(T-472) | T-109 `tokens-v0.1.0` |
| ui | map(T-411·T-412)·pinvi admin(T-422, L6); L6가 T-2xx 착수까지 미결이면 airport 소형 부품(Alert·StatStrip·SectionCard·EmptyState, T-432; Button은 0.2 별도 검증) | geo(T-444, React 19 후) | concierge(T-454, L8)·ktdm(T-473, L8; StatStrip·AppErrorPanel·SectionCard 부분) | T-212 `ui-v0.1.0`·T-213 `ui-v0.2.0` |
| py | map-api(T-480)·weather-api(T-481)·airport(T-482) | geo(T-483) | pinvi(T-484)·concierge(T-485, L8)·ktdm(T-486, L8; breaking 묶음) | T-310 `py-v0.1.0`·T-311 `py-v0.2.0` |
| 규칙 문서·`tokens.json` 의미 이름 | 전 소비자 즉시(코드 링크 없음; ktc·ktdm은 L8 전 이것까지만) | — | — | Phase 0 |
| CI 재사용 워크플로·매니페스트 | 7 저장소 T-403(Node 22·SHA 핀·`check_versions` report·매니페스트 커밋) | Phase 3 `openapi-drift`·`typegen-drift` | Phase 4 `node-quality`·`python-quality`(concierge CI 신설 T-451 선행) | T-010·T-011·T-309·T-401 |

## 3. 소비자별 선행 조건

| 소비자 | 외부 선행(사용자·타 저장소) | 앱 자체 선행(Phase 4) | common 선행 | 현재 판정 |
|---|---|---|---|---|
| kta | WIP `codex/shadcn-ui-foundation` 병합(O-9, T-430; 값 16/10·alpha line 유지, `cn`→clsx+tailwind-merge, shadcn/postcss devDependencies); L11 `license` 필드 | TS 7.0.2 예외 등록(O-6)·ESLint 도입 판정·`engines`·절대 링크 상대화(T-433); Docker `uv sync --locked`(T-482); AdminPageHeader·셸 소비는 T-035 라우트 분리 후(O-9) | T-109·T-212·T-310 | tokens 대기(WIP 병합 후) |
| ktc | L8 GPL 정렬(O-2, T-021) | `pyproject.toml`·`uv.lock`(`mcp<2` blocked)·ruff/mypy baseline(T-450); CI 신설 + production `frontend/Dockerfile`(T-451); hex fallback·`@config` 제거·`--ktc-*`→`--kt-*` 오버라이드(T-453) | T-401·T-305·T-109·T-213 | 규칙 참조만(L8 전) |
| ktdm | L8(O-2); 포트 `-latest`·sibling 등록 질의(T-014, O-24) | Next 16·React 19·ESLint 9·Node 22 별도 PR(T-470, 재포맷 금지); Poetry→`uv.lock`(T-471) | T-305·T-109·T-213·T-307 | 규칙 참조만(L8 전) |
| geo | React 19 승인(O-25, ADR-019 갱신, T-443); `-only` 재선언 여부(O-20) | Node 22 CI·`uv.lock`·pre-commit rev 정렬(T-440); `@config` 실효값 빌드 검증 → `@theme` 단일화(T-441) | T-109·T-213·T-308 | tokens 가능(T-109 후, React 19와 독립) |
| map | 없음(L9 LICENSE 전문 복원·`license` 필드는 T-410 채택 PR 동반) | Next 16.3·base-ui 1.8·Playwright 1.63 상향 별도 PR(T-413); OpenAPI 산출물 변경 시 pinvi·ktdm sha256 pin 갱신 PR 동반(T-480) | T-109·T-212·T-213·T-310 | 1차 대상 |
| wx | 없음 | Next 16·Vitest 4·Node 22·`moduleResolution: bundler`·CI vitest/mypy 추가(T-460); Python 3.11/3.12/3.13 정합·airkorea 스냅샷 정본(L15, T-481) | T-109·T-102(shim)·T-213·T-310 | 1차 대상(`tokens.css` 교체는 Next 버전과 독립) |
| pinvi | L6 라이선스·공개 결정(O-1, T-020·T-420); admin 44px 예외 2쪽(O-21); mobile Tailwind 3(O-8) | `uv.lock` CI·Docker 소비·etl `@main` 제거·export 파이프라인(T-484) | T-109·T-213·T-310 | 규칙 참조만(L6 전); L6 후 tokens·ui 1차 |

## 4. pinvi 세 표면(D-29)

| 표면 | 코드 소비 | 규칙 소비 | 비고 |
|---|---|---|---|
| admin(`apps/web` `[data-pv-surface='admin']`) | tokens: 스코프 안에서만 `--color-admin-*`→`--kt-*` 매핑 + `base.scoped.css`; ui v0.1/v0.2: `AdminTable` 어댑터 유지(`manualSorting=false` 명시)·`cn` 재수출·webpack 빌드 | admin 장 전부 | 44px 2쪽 영구 예외(O-21), 사용자 표면 무변경 e2e가 gate |
| 사용자 웹 | 없음 | consumer 프로필 규칙(8/14/20/32·44px·16px·하단 탭바·안전영역)·`tokens.json` 의미 이름 | 값·밀도는 pinvi 소유, 사용자 preset 유지 |
| 모바일(Expo, NativeWind 4) | `tailwind-preset.cjs` 생성물(O-8 승인 후) | consumer 프로필(48px) | Tailwind 3.4.19·RN 정확 핀 예외는 O-8 사용자 승인 전 `exceptions` 미등록(지시 (1) 축소이므로 "사용자 승인 대기") |

## 5. 채택 버전 표

정본은 T-012 이후 [통합 지도](../integration-map.md)다. 초기값은 모든 셀 "미채택"이며, 소비자 매니페스트(`kor-travel-common.lock.json`, T-011)가 커밋되면 `tools/collect_manifests.py`가 갱신한다. 여기서는 복제하지 않는다.

## 6. 공유 라이브러리와 범위 밖(D-23)

- `maplibre-vworld-react`(`95b49d3`)·`maplibre-vworld-js`(`2a13ce0`)·`digitie/python-*-api` 13종·`python-kraddr-base`는 common 범위 밖이며 의존만 한다. `versions.json` `providers` 절은 보고만 하고 정렬 주체는 각 저장소다(O-16).
- 사실로 확인된 불일치: `python-kma-api` map `a75d1e1` vs weather `0868b76`; `python-kasi-api` airport `51c39c1` vs pinvi etl `@main`; `python-airkorea-api` weather 저장소 내 path vs map SHA; `vworld-style.ts` map·weather 중복(`be` §5.1, `vm` §2.7). 정리 요청 문서는 T-505(`maplibre-vworld-react` npm 게시·`license` 필드, 마커 팔레트 P-01~16 hex 정본 포함).
- 인증(비밀번호·세션·CSRF·JWT·RBAC)과 앱 도메인은 소비자 소유다.

## 7. 회수 측정(D-28)

분기마다 `docs/reports/adoption-YYYY-QN.md`에 원본 수정 시간·타 앱 반영 시간·검증 시간·회귀 수·로컬 복사본 수 + drift·`EXEMPT`·`enforce` 전환 수를 기록한다(첫 회 T-503). 순절감 ≤0이 2분기 이어지면 범위를 축소하고, npm 소비자 우회 패치가 2회 이상이면 배포 방식을 재검토한다.
