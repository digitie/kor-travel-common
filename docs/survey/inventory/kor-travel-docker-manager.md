# kor-travel-docker-manager 인벤토리

- **기준 커밋**: `862562dcbd6a70c5d00e8d1538264fafe5ed5f5c` (2026-09-05 10:35:54 +0900, `fix(compose): weather target을 등록 해제하고 bind baseline을 결박한다 (#320)`) — `git -C F:/dev/kor-travel-common-survey/ktdm-main rev-parse HEAD`로 확인
- **조사일**: 2026-09-06
- **조사 경로**: `F:/dev/kor-travel-common-survey/ktdm-main` (읽기 전용, 파일 변경 없음)
- **라이선스**: MIT — `LICENSE` 1행 `MIT License`, 3행 `Copyright (c) 2026 Youn-sok Choi` (사실). 선행 보고서(`F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md` §9)의 "concierge·docker-manager가 MIT" 기술과 일치한다.
- **규모**: 추적 파일 298개(`git ls-files | wc -l`), 커밋 786건(2026-06-10 ~ 2026-09-05, `git rev-list --count HEAD`), 백엔드 서비스 코드 41,031줄(`wc -l backend/src/kor_travel_docker_manager/services/*.py`), `docs/journal.md` 7,122줄.
- **표기 규칙**: 본문에서 **사실** = 파일에서 직접 확인, **후보** = 공통화 판단용 제안, **추정** = 근거가 간접적, **미확인** = 확인하지 못함.

## 1. 저장소 개요와 역할

1. 정체성: PinVi와 형제 서비스(`kor-travel-geo`, `kor-travel-concierge`, `kor-travel-map`)가 공용하는 기반 인프라(프로젝트별 전용 PostgreSQL/PostGIS 4개, RustFS, 관측 스택)와 앱 컨테이너를 Docker Compose로 구동·관리·모니터링하는 **운영 관리 소프트웨어**다(`README.md` 3~5행, `AGENTS.md` 56~63행, `SKILL.md` 8~15행).
2. 사용자: 화면 설계 문서는 대시보드 사용자를 **비전문 관리자**로 명시한다(`docs/dashboard-ui.md` 19행). 고객용 화면은 없고 `DESIGN.md` 5행이 "비즈니스 서비스 화면이나 고객용 사이트에는 적용하지 않는다"고 범위를 좁힌다.
3. 세 표면: FastAPI 백엔드(`backend/`, 포트 12901), Next.js 대시보드(`frontend/`, 포트 12905), Python CLI `ktdctl`(`backend/src/kor_travel_docker_manager/cli.py`, poetry console script)이 같은 target registry(`config/docker-targets.yml`)를 읽는다(`docs/architecture.md` 11~65행 다이어그램).
4. 형제 연동: `docker-compose.yml`이 `../kor-travel-geo`, `../kor-travel-concierge`, `../kor-travel-map`, `../pinvi` 체크아웃을 build context로 삼아 앱 이미지를 직접 빌드한다(`docker-compose.yml` 384~386, 488~490, 957~959, 1154~1156행). 형제 저장소는 자체 compose로 DB/RustFS 생명주기를 관리하지 않는다는 규칙이 `AGENTS.md` DO NOT 7, `SKILL.md` DO NOT 6에 있다.
5. 핵심 운영 계약: Map·PinVi를 어느 커밋으로 재구축할지는 root 소유 **runtime pin registry**가 소유하고(ADR-40, `docs/runtime-pin-registry.md`), production에서는 host-wide lock을 잡는 pinned workflow만 Map·PinVi runtime을 변경한다(`CLAUDE.md` 15~27행).
6. 포트 정책의 정본: `docs/ports.md`의 `12000 + dependency index * 100 + offset` 규칙(DB `+0`, API `+1`, UI `+5`)이 Kor Travel/PinVi 계열 전체의 로컬 포트를 배정한다(`AGENTS.md` DO NOT 4·9).
7. 개발 환경: 개발·검증·git·CodeGraph는 Linux/WSL에서만 수행하고 Windows PowerShell/CMD 실행을 금지한다(`AGENTS.md` 86~102행, DO NOT 10·11).
8. 문서 언어: 모든 Markdown은 한글, 코드 식별자·명령어·공식 용어만 영문(`AGENTS.md` 40~52행).
9. 최근 흐름: 2026-09-01 "범용 관리툴 감사(GM 트랙)" 20개 태스크 중 19개 완료(`docs/general-mgmt-audit.md` 1~40행), 2026-09-04 `kor-travel-weather` target 등록 후 2026-09-05 기준 커밋에서 등록 해제(`git log --oneline -15`; `config/docker-targets.yml`·`docker-compose.yml`에 `weather` 문자열 없음 — 사실).

## 2. 저장소 구조

최상위 트리(`git ls-files` 기준, 추적 파일 수):

| 경로 | 파일 수 | 역할 |
|---|---:|---|
| `backend/` | 114 | FastAPI + CLI(`src/kor_travel_docker_manager/`, 51 파일) · `tests/`(62 파일) · `pyproject.toml` |
| `frontend/` | 54 | Next.js 14 App Router 대시보드(`src/` 39, `public/images/` 6, 설정 9) |
| `docs/` | 18 | 아키텍처·ADR·일지·태스크·런북·디자인·기능 레퍼런스(하위 디렉터리 없음, 평면) |
| `.agents/`, `.claude/`, `.opencode/`, `.codex/`, `.gemini/` | 23 / 20 / 21 / 7 / 1 | 에이전트별 스킬·서브에이전트·MCP 설정(postgres 스킬 3벌 중복 vendoring) |
| `scripts/` | 16 | 설치·백업·회전·E2E 러너(bash/python) |
| `config/` | 4 | `docker-targets.yml`, `runtime-pins.seed.json`, prometheus/grafana provisioning |
| `deploy/` | 4 | systemd 유닛 2, tmpfiles.d 1, logrotate 템플릿 1 |
| `.github/workflows/` | 1 | `ci.yml` |
| 루트 | 13 | `AGENTS.md` `CLAUDE.md` `SKILL.md` `DESIGN.md` `README.md` `LICENSE` `docker-compose.yml`(1,522줄) `.env.example`(398줄) `claude.json` `codex.json` `opencode.json` `antigravity.json` `.hallmark/log.json` |

- 모노레포 workspace 아님: 루트에 `package.json`/`pyproject.toml` 없음, `frontend/package.json`과 `backend/pyproject.toml`이 각각 독립(사실). ADR-1은 이를 "모노레포 구조"라 부르지만 npm/poetry workspace 도구는 쓰지 않는다.
- `Dockerfile` 없음(`git ls-files | grep -i dockerfile` 결과 없음 — 사실). Manager 자신은 컨테이너가 아니라 systemd + venv/npm으로 실행된다(§6).
- 백엔드 lockfile(`poetry.lock`) 추적 없음(사실). 프론트엔드는 `package-lock.json`(lockfileVersion 3) 추적.

## 3. 프론트엔드

### 3.1 Docker Manager UI (`frontend/`)

**프레임워크/런타임** (사실, `frontend/package.json`·`package-lock.json`)

| 항목 | 선언 | lockfile 설치 |
|---|---|---|
| next | `^14.1.4` | 14.2.35 |
| react / react-dom | `^18.2.0` | 18.3.1 |
| typescript | `^5.4.3` | 5.9.3 |
| node engines / packageManager | 선언 없음 | CI `node-version: "20"`(`.github/workflows/ci.yml` 43행), `docs/dev-environment.md` 12행 "Node.js 20 LTS" |
| 패키지 매니저 | npm (`package-lock.json`, `npm ci` in CI) | — |

- **Next 14 / React 18 잔존 이유**: 문서 근거 **없음**(미확인). `docs/journal.md`·`docs/decisions.md`·`docs/tasks.md`·`docs/tasks-done.md`·`docs/ktdctl-ui-migration.md`·`docs/general-mgmt-audit.md`에서 `Next 15|16`, `React 19` 업그레이드 언급을 grep한 결과 0건. 관련 흔적은 둘뿐이다: (a) `docs/journal.md` 6952행 — 2026-06-11 `react-doctor`가 "기존 Next.js 14 보안 경고"를 보고했으나 후속 태스크 없음, (b) `docs/tasks-done.md` 224행 — `@testing-library/react@16`이 "React 18/19 peer"라는 메모. 추정: 초기 스캐폴딩(T-005, 2026-06) 이후 프레임워크 업그레이드 태스크가 한 번도 등록되지 않았다. 선행 보고서 §2가 지적한 "geo와 docker-manager의 React 18" 세대 차이는 사실로 재확인된다.

**스타일** (사실)

- Tailwind v4 CSS-first: `frontend/src/app/globals.css` 2~3행 `@import "tailwindcss"; @import "../../tokens.css";`, `postcss.config.js`는 `@tailwindcss/postcss` 하나만. `tailwind.config.*` 없음(2026-06-20 T-015에서 삭제, `docs/journal.md` 6795행). `tailwindcss ^4.0.0`(설치 4.3.1), `@tailwindcss/postcss ^4.0.0`(4.3.1), `postcss ^8.4.38`(8.5.15). autoprefixer 없음.
- 토큰 파일: `frontend/tokens.css`(72줄). `@theme` 블록(5~49행)에 색 20종(전부 `oklch`; page/card/subtle/elevated/row/line, strong/ink/secondary/tertiary/disabled, brand/brand-ink/brand-tint, info/warn/danger/ok, graphite/graphite-2/graphite-ink), shadow 3종(card/card-hover/modal), radius 3종(card 0.375rem, panel 0.5rem, pill 999px), easing 3종, font 3종. `:root` 블록(51~72행)에 간격 8단계(`--space-3xs`~`--space-2xl`), duration 3종(120/220/420ms), z-index 7단계(base 1 · raised 10 · dropdown 100 · sticky 200 · drawer 300 · modal 400 · toast 500). 헤더 주석(1~4행)이 brand 값의 출처를 "web_service_palette_testset.html의 Orange(#EA580C/#C2410C/#FFEDD5, Tailwind orange-600/700/100)를 OKLCH로 정확히 변환"이라고 밝힌다.
- `globals.css` 1,383줄: `@layer base`(5~82행: 전역 색·폰트·focus-visible 2px brand outline·버튼 전환 속성 제한·`prefers-reduced-motion` 전역 무력화)와 `@layer components`(83행~). 클래스 인벤토리: `ops-*` 계열 약 70개(`ops-button[--primary|--danger]`, `ops-input`, `ops-field`, `ops-modal`, `ops-modal-backdrop`, `ops-modal__header`, `ops-command-dialog*`, `ops-stat-strip*`, `ops-stat*`, `ops-signal*`, `ops-ledger*`, `ops-fleet-table`, `ops-archive-table`, `ops-table-wrap`, `ops-status-badge`, `ops-status-dot`, `ops-inline-note[--danger]`, `ops-alert`, `ops-auth-*` 9종, `ops-error-*`, `ops-detail-metric*`, `ops-group-*`, `ops-section-title/copy`, `ops-eyebrow`, `ops-title`, `ops-icon-button`)와 셸 계열(`app-shell[__workspace]`, `sidebar`, `sidebar-footer`, `sidebar-collapse-toggle`, `rail-nav`, `nav-group/title/link/button`, `brand*`, `page-head*`, `skip-link`, `mobile-logout-button`, `dashboard-stack`, `content`).
- 라이트/다크: **라이트 단일**. `prefers-color-scheme`·`data-theme`·`.dark` 셀렉터 없음(grep 0건). `DESIGN.md`도 다크 모드를 언급하지 않는다.
- 폰트: 웹폰트 로드 없음(`next/font`, `@font-face`, `fonts.googleapis` grep 0건). `--font-display`와 `--font-sans`가 같은 시스템 스택 `"Noto Sans KR", "Pretendard Variable", "Apple SD Gothic Neo", sans-serif`, `--font-mono`는 `"IBM Plex Mono", ... monospace`(`tokens.css` 42~48행, 주석에 "실제로 로드되는 웹폰트가 없어 ... 같은 순서로 고정"). 2026-08-26에 `next/font`로 로드하던 IBM Plex Sans/Space Grotesk를 걷어냈다(`docs/journal.md` 3178~3180행).
- 아이콘: `lucide-react ^0.363.0`(0.363.0). 애니메이션 라이브러리 없음(`tw-animate-css` 없음). `clsx`는 lockfile에만 존재(package.json 미선언 — 추정: recharts 전이 의존).

**UI 프리미티브** (사실)

- radix-ui / `@base-ui/react` / shadcn: **없음**. `components.json` 없음, `components/ui/` 디렉터리 없음, lockfile에 radix·base-ui·class-variance-authority·tailwind-merge 없음.
- `README.md` 12행·`AGENTS.md` 61·73행·`CLAUDE.md` 68행이 "Shadcn UI"를 스택으로 적지만 코드에는 없다(문서-코드 불일치, 사실). ADR-17 결과(부정) 항목이 "geo가 참조하는 shadcn primitive 구조는 매니저에 도입하지 않고 토큰 직접 적용 방식을 유지했다"고 결정을 명시한다(`docs/decisions.md` 542행). `DESIGN.md` 130~132행 "shadcn 대응" 절은 향후 도입 시 토큰 매핑(`background→--color-card`, `primary→--color-brand`, `border→--color-line`, `ring→--color-brand`)만 정한다.

**컴포넌트 인벤토리** (사실, `frontend/src/components/`)

| 파일 | 줄 | 성격 | 출처/헤더 근거 |
|---|---:|---|---|
| `DashboardClient.tsx` | 1,970 | 단일 페이지 본체(원장 표, 앱별 그룹, 로그·차트·설정 모달, 명령 팔레트, 토스트 스택 소유) | 헤더 주석 없음. recharts를 `next/dynamic`으로 지연 로드(62~69행) |
| `layout/AppShell.tsx` | 259 | 접히는 좌측 rail + 페이지 헤더 + `<main>` | 18행 "최신 Map admin rail과 같은 1024px 기준", `data-slot="admin-shell-rail/header/main"`(141·234·250행) — kor-travel-map `packages/kor-travel-map-admin/frontend/src/components/admin-shell.tsx` 240·391·458행과 동일 slot 이름(사실) |
| `layout/AppErrorPanel.tsx` | 103 | App Router `error.tsx`/`global-error.tsx`용 한국어 복구 패널 | geo PR #391 이식(ADR-17, `docs/journal.md` 6794행). 파일 헤더에는 출처 주석 없음 |
| `StatStrip.tsx` | 95 | 통계 띠(`<dl>` + `ops-stat*`) | 헤더 주석 없음. props(`key/label/value/unit/caption/tone/title/href/loading/testId`, `isLoading/size/framed/ariaLabel`)와 `renderValue/hasValue` 로직이 map `stat-strip.tsx`(9~40행)와 거의 같음. 차이: ktdm은 `help`(HelpTip) prop 없음·`title` prop 있음·`cn` 대신 배열 join·CSS 클래스(`ops-stat-strip`) 기반, map/pinvi는 Tailwind 유틸 그리드 기반. pinvi `apps/web/components/admin/stat-strip.tsx` 1행이 "kor-travel-map admin에서 이식(T-356)"이라 명시하므로 세 저장소에 같은 컴포넌트가 세 벌 있다(사실) |
| `Toast.tsx` | 104 | 자체 `ToastStack`/`successToast`/`errorToast`(성공 6초 자동 닫힘, 실패는 수동 닫힘, 원문 "자세히" 접기) | 자체 작성. map은 `components/ui/sonner.tsx`(sonner 래퍼), pinvi는 대응 파일 없음(`git ls-files` grep 0건) — 구현이 갈린다 |
| `InlineError.tsx` | 43 | 모달 내 `role="alert"` 인라인 오류(요청 ID 노출, raw 접기) | 자체 작성(`docs/dashboard-ui.md` §1). map 대응물은 `components/ui/alert.tsx`(추정 — 본 조사에서 내용 미열람) |
| `CopyableCommand.tsx` | 56 | SSH 명령 복사 카드 | 자체 작성(P7-E, `docs/ktdctl-ui-migration.md` 872행). map/pinvi에 같은 이름 파일 없음 |
| `LoginScreen.tsx` | 93 | 로그인 폼(`ops-auth-*`) | 2026-08-26 geo 로그인 화면 실측 spacing으로 정렬(`docs/journal.md` 2660~2666행) |
| `AdminSettingsPanel.tsx` | 617 | 비밀번호 변경·공개 API 키·로그인 감사 | react-query 미사용, `apiJson/postJson/deleteJson` 직접 호출 |
| `BackupHistoryPanel.tsx` | 486 | 백업 목록·생성(202 job 폴링)·off-box 상태 | — |
| `RuntimePinPanel.tsx` | 481 | pin 조회 + 2-step 회전 요청 폼 | `docs/dashboard-ui.md` §5-1 원형 |
| `SourceStatusPanel.tsx` | 550 | source-status·deployment-readiness·rebuild preflight 관측 | `Row`/`VerdictIcon` 기계 보유(§6) |
| `ContainerDetailModal.tsx` | 467 | inspect 6탭(overview/resources/mounts/networks/health/env), ensure 실행 | ESC·초기 focus 자체 처리(161·169행) |
| 테스트 4개 | — | `AdminSettingsPanel.test.tsx`, `ContainerDetailModal.test.tsx`, `ContainerDetailModal.prod.test.tsx`, `SourceStatusPanel.test.tsx` | — |

앱 레벨 공유 컴포넌트 중 과제 목록의 filter-bar, pagination-bar, status-badge(컴포넌트), data-table, empty-state, section-card, copy-button(→`CopyableCommand`이 대체), json-viewer, confirm-dialog(`window.confirm` 사용, 별도 컴포넌트 없음 — `docs/dashboard-ui.md` §3), help-tip, vworld map view는 **없음**(사실). 상태 배지는 CSS 클래스 `.ops-status-badge`/`.ops-status-dot`과 `lib/containerPresentation.ts`의 `getStatusConfig`로 처리된다.

**상태/데이터** (사실)

- `@tanstack/react-query ^5.28.0`(5.101.0). `Providers`(`src/app/providers.tsx`)가 `staleTime 5000`, `refetchInterval 5000` 기본값. 상태·로그는 WebSocket 우선, HTTP 폴링 fallback(`docs/architecture.md` 121행).
- zustand 없음. react-hook-form/zod **없음** — 2026-09 GM-19에서 "더미 의존성"으로 삭제(`docs/general-mgmt-audit.md` 1181행). 그러나 `README.md` 12행, `AGENTS.md` 61행, `docs/architecture.md` 122행은 여전히 Zod·React Hook Form을 스택으로 적는다(문서 stale, 사실).
- API 클라이언트: 생성기 없음(openapi-typescript 등 0건). `src/lib/api.ts`(580줄)에 응답 타입을 손으로 선언. 래퍼 `apiFetch`(`credentials: 'include'`, body 있으면 `content-type: application/json`) → `apiJson`(비 2xx면 본문 텍스트와 `x-request-id` 헤더로 `ApiError` 생성) → `postJson`/`deleteJson`(528~566행). 401은 `setUnauthorizedHandler`로 SPA 내 로그인 전환(505~507행). WebSocket 종료 코드 상수 4401/4000/1013(519~521행).
- 오류 표시 계층: `ApiError`(`{detail}`가 문자열이든 `{code,message}`든 파싱, 절대 throw 안 함) → `humanizeError(err, 동작명)`(`lib/errors.ts`, `CODE_MESSAGES` 24종 + `STATUS_MESSAGES` 7종, 우선순위 코드→서버 메시지→상태 코드) → `errorToast`/`InlineError`. `alert()` 금지(`docs/dashboard-ui.md` §1).
- 표시 헬퍼: `lib/containerPresentation.ts`(`statusLabel`, `roleLabel`, `getContainerPresentation`, `getStatusConfig`), `lib/format.ts`(`formatBytes`, `formatTimestamp` — UTC naive 문자열을 Z 붙여 파싱), `lib/configValidation.ts`(백엔드 검증 규칙 복제, 민감 키 판별), `lib/configDiff.ts`, `lib/chartData.ts`, `lib/backupRoles.ts`, `lib/github.ts`(GitHub compare 링크만 브라우저에서 생성).

**인증 경계** (사실)

- Next 측 middleware/proxy/route handler **없음**(`src/app/`에 `layout.tsx`, `page.tsx`, `providers.tsx`, `error.tsx`, `global-error.tsx`뿐). 브라우저가 `NEXT_PUBLIC_BACKEND_URL`(빌드 타임 인라인, `frontend/.env.example`)의 백엔드를 직접 호출한다.
- 세션: 백엔드가 발급하는 쿠키 `ktdm_admin_session`(HMAC 서명 + DB 세션 해시, `httponly`, `samesite="strict"`, https일 때 `secure`; `services/auth_service.py` 20행·148~152행). CSRF 토큰 없음 — 대신 `require_frontend_origin`(Origin 허용 목록, 위반 403)과 SameSite=strict, CORS `allow_credentials=True` + 정확한 Origin 매칭(`main.py` 213~253행).
- 백엔드 신원 전달: 없음(프론트는 신원을 만들지 않는다). 신뢰 프록시는 `KTDM_TRUSTED_PROXY_CIDRS`(기본 loopback) + 선택 `X-KTDM-Proxy-Secret` 헤더(`auth_service.py` 534~550행).

**라우팅/화면 목록** (사실)

- `app/` 라우트: `/` 하나. 관리자 화면 1(대시보드) + 로그인 화면(같은 경로에서 인증 상태로 분기, `DashboardClient.tsx` 884~892행) + 오류 화면 2(`error.tsx`, `global-error.tsx`). 사용자(고객) 화면 0.
- 대시보드 내부: 해시 앵커 `#service-ledger`, `#service-groups`(`AppShell.tsx` 107~108행), 모달/패널 9종(로그·차트·설정·명령 팔레트(`⌘/Ctrl+K`, 193행)·AdminSettings·BackupHistory·RuntimePin·SourceStatus·ContainerDetail). rail 메뉴 그룹: 대시보드 / 서비스 관리 / 운영 도구 / 시스템(`AppShell.tsx` 99~127행).

**반응형/모바일** (사실)

- 분기점은 CSS만: `@media (min-width: 64rem)`(rail 접힘 4rem), `@media (max-width: 63.999rem)`(rail이 상단 가로 띠, 접기 버튼 숨김, 모바일 로그아웃 버튼 표시), `@media (max-width: 48rem)`(통계 띠 2열, 보관 이력 표를 block 행으로)(`globals.css` 1119·1174·1276행). `AppShell.tsx` 19행 `DRAWER_MEDIA_QUERY = '(max-width: 63.999rem)'`(현재 코드에서 drawer 자체는 사라지고 상수만 남음 — 사실; 2026-08-26의 drawer/`inert` 구현은 2026-08-31 Rail-Workbench 정합에서 대체됨, `docs/journal.md` 1117~1123행).
- Tailwind 반응형 유틸리티 사용은 극소(`md:text-sm` 9회, `lg:*` 7회). 모바일 전용 라우트/분기 없음. 터치: `button,[role="button"] { touch-action: manipulation }`(`globals.css` 51~53행). `DESIGN.md` 92~101행이 320/375/414/768/1024px 규칙과 "본문 전체가 아닌 표 영역만 가로 스크롤"을 규정.

**i18n / 접근성 / focus / reduced-motion** (사실)

- i18n 없음. 문자열은 한국어 하드코딩, `<html lang="ko">`(`layout.tsx` 16행). 숫자 포맷 `toLocaleString('ko-KR')`(`StatStrip.tsx` 41행), 테스트 `TZ=Asia/Seoul`.
- 접근성: skip-link(`AppShell.tsx` 134행), `aria-label`/`aria-current`/`aria-modal`/`role="dialog"`/`aria-live`(로그인 오류 `aria-live="assertive"` 상시 마운트, `LoginScreen.tsx` 85행), 각 모달의 ESC·초기 focus 자체 처리 규약(`docs/dashboard-ui.md` §6).
- focus 레시피: `:focus-visible { outline: 2px solid var(--color-brand); outline-offset: 2px }`(`globals.css` 60~68행), 입력은 brand 테두리 + `color-mix` ring(1113~1116행).
- reduced-motion: `@media (prefers-reduced-motion: reduce)`에서 모든 animation/transition을 0.001ms로(`globals.css` 72~80행). `transition-all` 금지(`DESIGN.md` 61행).

**테스트·품질** (사실)

- vitest `^4.1.11`(4.1.11) + jsdom 27.4.0 + `@testing-library/react` 16.3.3 + `@vitejs/plugin-react` 6.1.1(vite 8.2.2 전이). `vitest.config.mts`: `environment: 'jsdom'`, `include: src/**/*.test.{ts,tsx}`, alias `@`, setup `src/vitest-setup.ts`(`@testing-library/jest-dom/vitest`). `src/test-utils.tsx`의 `renderWithQueryClient`(테스트마다 새 QueryClient, `retry:false`). 테스트 파일 8개(lib 4 + 컴포넌트 4), 2026-09 기준 31 passed(`docs/tasks-done.md` 224행).
- playwright: 설정 파일 없음(`playwright.config` 0건, `docs/general-mgmt-audit.md` 78행이 부재를 확인). E2E는 MCP playwright 서버(`claude.json` 등)와 n150 수동 검증.
- react-doctor: 2026-06-11 1회 실행 기록(`docs/journal.md` 6952행), 설정 없음.
- eslint `^8.57.1`(8.57.1) + `eslint-config-next ^14.2.35`; `.eslintrc.json`은 `{"extends": "next/core-web-vitals"}` 한 줄(플러그인 추가 없음). CI는 `npm run lint -- --max-warnings=0`.
- tsconfig: `strict: true`, `target: es5`, `moduleResolution: bundler`, `paths @/* → ./src/*`, `noUncheckedIndexedAccess` 등 추가 strict 옵션 없음.
- 스크립트: `dev`/`start` `-p 12905`, `lint: next lint`, `type-check: tsc --noEmit`, `test: TZ=Asia/Seoul vitest run`.

**빌드/배포** (사실)

- `next.config.*` **없음**(추적 파일에 없음) — output/transpilePackages/images 설정 전부 기본값.
- Dockerfile 없음. 운영은 rsync로 `frontend/src/`만 전달 후 호스트에서 `npm ci` + `npm run build` + systemd `ktdm-frontend.service`(템플릿, 비root `User`, `npm run start`, `NoNewPrivileges=yes`; `deploy/systemd/ktdm-frontend.service.template`). 배포 전 `scripts/verify-frontend-toolchain.sh`가 `node_modules/.bin/next`와 `npm ls --depth=0`으로 툴체인 정합을 검사.
- `frontend/.env.example`: `NEXT_PUBLIC_BACKEND_URL` 하나(개발 `http://localhost:12901`, 운영은 `frontend/.env.production`; `.env.local`이 production을 덮는 함정 경고).

**디자인 문서** (사실)

| 문서 | 위치/길이 | 핵심 규칙 |
|---|---|---|
| `DESIGN.md` | 루트, 139줄 | 정본. 장르 editorial-utilitarian, 구조 Rail-Workbench, 테마 **Ember**(오렌지 조치 신호·따뜻한 종이 표면). 색 토큰 표(oklch), 타이포(표시 Pretendard→Noto Sans KR, 본문 Noto Sans KR→Pretendard, 데이터 IBM Plex Mono; 한글 레이블에 대문자·과도 자간 금지), 간격 8단계, radius 6/8px, 그림자는 모달·인증 카드만, 전환 120ms 속성별, 반응형 표(320~1024), 상태표(기본/Hover/Focus/Active/Disabled/Loading/Error/Success). **금지**: 장식 이미지·의미 없는 그라데이션/glass·카드 안의 카드·동일 KPI 카드 그리드·본문 전체 가로 스크롤·`transition-all`·라이브 데이터 없는 수치/차트·임의 hex/shadow/radius 유틸리티 |
| `docs/DESIGN-RULES.md` | 39줄 | 7개 구현 규칙 요약. **주의**: 규칙 5가 "표시 제목 Space Grotesk, 본문 IBM Plex Sans"라고 적어 현행 `tokens.css`·`DESIGN.md`(Noto Sans KR/Pretendard)와 어긋난다 — Cobalt 시대(2026-08-13) 잔존(사실) |
| `docs/design-system.md` | 51줄 | 토큰 용도표, 화면 구조 4항, 검토 기준 4항("별도 색상 체계를 만들지 않았는가", "gradient/glass/반복 카드/가로 스크롤 표/`transition-all`이 없는가", 320~768px 조작 가능, 문서≡tokens.css) |
| `docs/dashboard-ui.md` | 242줄 | 에이전트용 UX 계약: 설계 원칙 3(개발자 어휘 금지·파괴적 조작은 범위 선표시·불가능한 것은 처음부터 불가능하게), 오류 계층, 라벨 규약, 확인 규약(start 무확인 / stop·restart 영향 target 수 확인 / 설정 저장 diff / ensure 경고), 전이 폐포 그룹 규칙, CLI 전용 작업의 CopyableCommand 규약, 2-step 요청 패턴, 패널 추가 규약(`'use client'`, `ops-modal`, `role="dialog"`, 자체 ESC, `retry:false`, 진입점 2곳), 정직성 규약(unknown/stale은 "확인 필요") |
| `.hallmark/log.json` | 2026-08-13 실행 1건 | genre modern-minimal, macrostructure Workbench, theme **Cobalt** — 현행 Ember와 불일치(stale, 사실) |

디자인 변천(사실, ADR·journal): BMW M Pure Black(ADR-6, 2026-06-11; `public/images/` BMW PNG 6장이 참조 없이 잔존 — `grep` 0건) → StyleSeed 라이트 teal + Tailwind v4(ADR-17, 2026-06-20, geo `DESIGN-RULES.md` 포팅) → Hallmark Cobalt Workbench(ADR-36, 2026-08-13; Space Grotesk/IBM Plex Sans) → geo-ui 보라 톤 + 좌측 사이드바(2026-08-26, `docs/journal.md` 3167행) → 오렌지 재조정·Tailwind orange 정합(2026-08-27, 2690~2706행) → kor-travel-map Rail-Workbench 구조 정합·Ember 명명(2026-08-31, 1117행). `docs/architecture.md` 126행은 "6px/10px radius"라 적으나 `tokens.css`는 6px/8px(0.375/0.5rem)이다(문서 불일치, 사실).

## 4. 백엔드

### 4.1 kor-travel-docker-manager-backend (`backend/`)

**빌드·런타임** (사실, `backend/pyproject.toml`)

- python `^3.11`(CI 3.11). 빌드 시스템 **poetry**(`poetry-core`), 패키지 `kor_travel_docker_manager`(`src/` 레이아웃), console script `ktdctl = kor_travel_docker_manager.cli:main`.
- lockfile: `poetry.lock` **추적 없음**. CI는 poetry를 쓰지 않고 `pip install -e ./backend httpx==0.28.1 pytest==9.1.1 ruff==0.16.4`로 고정(`ci.yml` 25행). 운영은 root-owned offline wheelhouse(`scripts/provision-ktdm-offline-wheelhouse.py`, `/var/lib/kor-travel-docker-manager/wheelhouse`)에서 설치(`docs/prod-deployment.md` §3.1). 즉 "선언 범위(pyproject) / CI 핀 / 운영 wheelhouse" 세 곳이 각자 버전을 결정한다.

**의존 선언 범위** (사실)

| 구분 | 패키지 | 범위 | 비고 |
|---|---|---|---|
| 런타임 | fastapi | `^0.110.0` | |
| | uvicorn | `^0.28.0` | `websocket.py` 85행 주석 "uvicorn 0.28.1의 legacy websockets_impl" |
| | docker | `^7.0.0` | Docker SDK |
| | pydantic | `^2.6.0` | |
| | pydantic-settings | `^2.2.0` | **import 0건**(`grep -rn pydantic_settings backend/src` 없음) — 미사용 선언 |
| | python-dotenv | `^1.0.1` | 루트 `.env` 로드 |
| | pyyaml | `^6.0.1` | 중복 키 거부 로더 `services/yaml_strict.py` |
| | websockets | `^12.0` | uvicorn ws 구현용 |
| | sqlalchemy | `^2.0.0` | SQLite 전용 |
| dev | pytest `^8.0.0`, ruff `^0.3.0`, mypy `^1.9.0`, httpx `^0.27.0`, types-docker, types-PyYAML | | CI 핀(pytest 9.1.1, ruff 0.16.4, httpx 0.28.1)이 pyproject 범위 밖(drift, 사실) |
| 없음 | alembic, asyncpg/psycopg, structlog, prometheus-client, typer, tenacity, dagster, argon2 | | Prometheus는 수기 렌더, CLI는 argparse, 비밀번호는 pbkdf2 |

**앱 구성** (사실, `main.py`)

- 앱 팩토리 없음 — 모듈 레벨 `app = FastAPI(title="Docker Manager UI API", version="0.1.0", lifespan=lifespan)`(235~240행). lifespan이 metrics DB init, 백그라운드 metrics collector, WS broadcast loop, 로그 정리 루프를 기동/종료.
- 라우터 prefix: 모두 `/api/v1` 아래 — `auth`(`/auth`, tags auth), `admin`(`/admin`, tags admin), containers(prefix 없음, `router = APIRouter(dependencies=[Depends(require_admin_session)])`, tags containers), websocket(`/ws/status`, `/ws/logs/{id}`, tags websocket)(278~281행). `/health`, `/metrics`는 루트.
- 미들웨어: `CORSMiddleware`(`allow_credentials=True`, `expose_headers=["X-Request-ID"]`), `_assign_request_id`(서버가 항상 새 UUID 발급, 클라이언트 `X-Request-ID` 불신; 256~275행).
- 에러 envelope: 계약 예외 3종에 전용 핸들러 — `ComposePostMutationContractError`→500 `{detail:{code,message,stage:"post_mutation_recovery",mutation_applied:true,original_error,recovery_*,restoration}, request_id}`, `ComposeCandidateContractError`→409 `{detail:{code,message,stage:"candidate_validation",mutation_applied:false}, request_id}`, `DeploymentContractError`→409 `{detail:<문자열>, request_id}`(324~356행). 나머지 라우트는 `HTTPException(detail=문자열 | {code,message})` 혼용(`routes.py`, `auth.py`, `admin.py`). 예외 클래스 정본은 `services/errors.py`(GM-20), 재수출 동일성은 `tests/test_service_layer_boundaries.py`가 결박.
- 페이지네이션 규약: 없음. `limit` 쿼리(1~500)만 존재(`admin.py` 48·58행).
- 인증: 단일 관리자. `KTDM_ADMIN_USERNAME`/`KTDM_ADMIN_PASSWORD_HASH`(`pbkdf2_sha256:310000:<salt>:<hash>`, `$` 대신 `:` 구분 — compose 보간 회피, `.env.example` 40~43행), `KTDM_SESSION_SECRET`(≥32자)로 HMAC 서명 쿠키 + `admin_sessions` 테이블(8시간 TTL). Origin 검사(`require_frontend_origin`), 로그인 rate limit 5회/10분(감사 행 durable 카운트, 신뢰 프록시 뒤 IP 버킷; GM-05), 감사 테이블 `login_audit_events`. 공개 API 키(`?key=`, 32자 영숫자, SHA-256 해시 저장, 끝 6자 힌트)는 `require_public_api_key` dependency로 제공되나 실제 부착 라우트는 `/metrics` opt-in(`KTDM_METRICS_REQUIRE_KEY=1`)뿐(GM-19, `main.py` 364~383행). ServiceToken/argon2 없음. ADR-19가 이 패턴을 "`kor-travel-geo` PR #399 패턴"으로 명시.
- rate limit: 로그인 전용(위). 일반 API rate limit 없음. WebSocket은 동시 인가 handshake 상한 `KTDM_WS_MAX_PENDING_AUTHORIZATIONS`(기본 64, 초과 close 1013).

**OpenAPI** (사실)

- FastAPI 자동 문서만(`docs/dev-environment.md` 111행 `http://localhost:12901/docs`). export 스크립트·저장된 `openapi.json`·CI drift 검사·operationId 규약 **없음**. 태그는 auth/admin/containers/websocket 4종. 프론트 타입은 `lib/api.ts`에 수기. Map의 `packages/kor-travel-map-api/openapi*.json` 해시를 M05 E2E가 대조하는 코드는 있으나(`scripts/m05_isolated_e2e.py` 1914~1917행) Manager 자신의 OpenAPI 관리와는 무관.

**설정** (사실)

- pydantic-settings 미사용. `load_dotenv(get_env_path())`(루트 `.env` 또는 `KOR_TRAVEL_DOCKER_MANAGER_ENV_FILE`) 후 `os.environ.get`을 호출 시점마다 읽는다(`auth_service.py` 72~81행 docstring "모듈 상수로 캐시하지 않는다").
- prefix: Manager 자체 `KTDM_*`(약 25키: `KTDM_DOCKER_NETWORK_MODE`, `KTDM_DEPLOYMENT_ENVIRONMENT`, `KTDM_C6C_CONTRACT_GENERATION`, `KTDM_CORS_ALLOW_ORIGINS`, `KTDM_FRONTEND_ORIGINS`, `KTDM_TRUSTED_PROXY_CIDRS/SECRET`, `KTDM_WS_*`, `KTDM_ADMIN_*`, `KTDM_SESSION_SECRET`, `KTDM_LOGIN_AUDIT_MAX_ROWS`, `KTDM_METRICS_REQUIRE_KEY`, `KTDM_PROD_URL_*`, `KTDM_BACKUP_ROOT/SHARED_GROUP`, `KTDM_RUNTIME_PINS_FILE/PUBLIC_FILE`, `KTDM_RUNTIME_PIN_REQUEST_FILE`); 관리 대상은 `KOR_TRAVEL_GEO_*`, `KOR_TRAVEL_CONCIERGE_*`, `KOR_TRAVEL_MAP_*`, `PINVI_*`, `RUSTFS_*`, `GRAFANA_*`, `PROMETHEUS_*`, `CADVISOR_*`(`.env.example` 398줄, 키 약 200개). `.env`는 0600 강제(`scripts/check-env-permissions.sh`).

**관측성** (사실)

- 로깅: 표준 `logging` + 자체 `MonthlyRotatingFileHandler`(`backend/logs/kor_travel_docker_manager.log`, 1년 보존 정리 루프) + 콘솔, 포맷 `... [%(request_id)s] ...`에 `RequestIdLogFilter`(contextvar). structlog 없음.
- 메트릭: `GET /metrics`가 백그라운드 캐시를 Prometheus text로 수기 렌더(`services/metrics_collector.py`), 접두 **`ktdm_`** 약 40개(`ktdm_up`, `ktdm_docker_daemon_up`, `ktdm_container_state/health_status/cpu_percent/memory_*/block_io_*/network_*`, `*_available` 게이지). 컨테이너 리소스 이력은 SQLite `metrics` 테이블(10초 샘플).
- `GET /health` → `{"status":"healthy","service":"kor-travel-docker-manager-backend"}`. `/ready` 없음.

**DB** (사실)

- 자체 DB는 SQLite `pinvi_metrics.db`(경로가 `database.py` 14행에서 `__file__` 기준 저장소 루트로 유도, env 오버라이드 없음 — `docs/runtime-pin-registry.md` §7-1이 이 제약을 "왜 SQLite가 아닌가"의 근거로 인용). SQLAlchemy 2.0 `DeclarativeBase`, 테이블 4개(`metrics`, `admin_sessions`, `login_audit_events`, `public_api_keys`; `models.py`). 스키마는 `Base.metadata.create_all`(ADR-19 결과(부정) "별도 마이그레이션 체계가 생기면 DDL 관리로 옮겨야"). alembic 없음. `busy_timeout 3000` + WAL 시도(GM-14).
- PostGIS는 관리 대상(compose)일 뿐 Manager DB에는 없음. 관리 대상 4 instance는 `postgis/postgis:16-3.5`(geo/concierge) 및 digest 고정(`pinvi`), map은 `KOR_TRAVEL_MAP_POSTGRES_IMAGE_ID` 필수.

**백업/복원, Dagster, CLI** (사실)

- 백업: `services/standalone_backup.py`(1,499줄) — role별 `pg_dump` 산출물 3종 세트 + manifest, `job_runner`로 202 비동기, off-box 동기화(`services/offbox_backup_sync.py`, `scripts/run-offbox-sync.sh`), cron 래퍼 `scripts/run-standalone-backup.sh`, logrotate 템플릿. 복원은 `db-backup restore-plan`(읽기 전용)과 `rehearse-restore`까지(`cli.py` 1213·1276행); 파괴적 restore 없음(`docs/ktdctl-ui-migration.md` KUM-M13).
- Dagster: Manager 자체에는 없음(Map/PinVi/Geo Dagster 컨테이너를 관리만 함).
- CLI `ktdctl`: **argparse**(`cli.py` 1733행 `build_parser`). 명령 트리 — `targets list|validate`, `status`, `ensure`(별칭 `db|storage|gra|cadv|prom|geo|conc|map|pinvi|all|srv|main`), `logs`, `action`, `inspect`, `pinvi-pair rebuild-pinned --confirm`, `compose-boundary stage-legacy-override|retire-legacy-override|activate-canonical-concierge`, `source-status`, `pin init|show|verify|migrate-execution-v6|rebind-execution|show-execution|block-execution|publish-generation|rotate|rotate-pair|block|rollback|apply-pending|show-pending|clear-pending`, `db-backup create|list|gc|restore-plan|rehearse-restore`, `offbox-sync run|status`. mutation은 `--confirm` 필수, root 전용 명령 다수, `--json` 출력 계약(GM-06).

**테스트·품질 게이트** (사실)

- pytest: `backend/tests/` 평면 62파일, `def test_` 1,273건(grep). unit/integration 디렉터리 분리 없음(파일명에 `_integration` 1건). testcontainers 없음(Docker SDK는 mock). coverage 게이트 없음. `conftest.py`가 `KTDM_RUNTIME_PINS_FILE`을 추적 seed로 고정하고 drvfs 0777 완화(`KTDM_RUNTIME_PINS_ALLOW_INSECURE_MODE=1`).
- ruff: `line-length 100`, `target py311`, `select E,F,I,UP,B,ASYNC`, `ignore E501,E402`; CI는 `--ignore EXE001` 추가해 `backend/src backend/tests scripts`. **`ruff format` 전체 실행 금지**(`SKILL.md` DO NOT 9 — "ruff-format 적용본이 아니다").
- mypy: dev 의존 선언만, CI 미실행(`docs/tasks-done.md` 226행 "CI에 mypy가 없어"). `[tool.mypy]` 없음.
- import-linter 없음. 대신 `tests/test_service_layer_boundaries.py`(예외·capability 센티널 재수출 동일성, AST로 순환 import 재도입 감지)와 `tests/test_normative_docs_cite_real_symbols.py`(규범 문서가 인용한 `test_*`·심볼 실존 검사; 대상 `AGENTS.md`·`SKILL.md`·`CLAUDE.md`·`docs/tasks.md`·`docs/resume.md`·`docs/runtime-pin-registry.md`·`docs/docker-management.md`·`docs/bindings.md`; `docs/resume.md`는 저장소에 없고 테스트는 `path.exists()`로 건너뜀 — 88행)이 계약을 결박한다.

## 5. 문서·에이전트 규약

**진입 파일** (사실)

| 파일 | 줄 | 역할 |
|---|---:|---|
| `AGENTS.md` | 169 | 최상위 규칙. 사고 원칙 5절(Think Before Coding/Simplicity First/Surgical Changes/Goal-Driven/Practical Bias), 문서 언어 정책, 역할·식별자 표, 개발 환경 정책, prod 배포·푸시 전 보안 감사, **지시 우선순위**(1 사용자 → 2 AGENTS.md → 3 SKILL.md → 4 architecture/decisions → 5 tasks/journal/README → 6 기존 코드·테스트), DO NOT 15항(15번 "한 사실을 두 곳에 독립 선언 금지: 유도→결박→탐지") |
| `CLAUDE.md` | 135 | 세션 컨텍스트(2026-08-25 현황 스냅샷, 디렉터리, 명령, 작업 후 의무 5항). 에이전트 공통(Claude/Antigravity/Codex)이 읽는다고 명시 |
| `SKILL.md` | 146 | 에이전트 매뉴얼: 정체성, 실행 위치 표, 디렉터리 지도, **§3.1 기능별 레퍼런스 표**(고치기 전에 읽을 문서와 대표 함정), DO NOT 11항, 도메인 어휘, 체크리스트(LF 확인 포함) |
| `DESIGN.md` | 139 | 디자인 정본(§3) |
| `README.md` | ~100 | 사람용 개요·포트 표·시작하기 |

- 언어 정책: 한글 본문, 영문 식별자(`AGENTS.md` 40~52행). 실제 코드 주석·docstring·커밋 메시지도 한국어(사실, 예: `git log` 최근 15건 전부 한국어 제목 + `fix(compose):`/`docs:`/`feat:` 접두).

**docs/ 트리** (사실, 평면 18파일)

| 파일 | 줄 | 규약 |
|---|---:|---|
| `architecture.md` | 284 | mermaid 다이어그램, 백엔드/프론트/관리 대상 인프라 정의 |
| `decisions.md` | 2,806 | ADR 단일 파일. "ADR 표준 형식"(상태/날짜/결정자/관련 → 컨텍스트/결정/근거/결과(긍정·부정)/후속). ADR-1~43 + F1G~F1J 4건. 상태값 accepted/superseded |
| `journal.md` | 7,122 | 역시간순 작업 일지. 검증/미확인을 절마다 구분해 적는 관행 |
| `tasks.md` | 19 | **활성 작업만** 한 줄씩(`[ ]`/`[/]`), 계층·lane 없음 |
| `tasks-done.md` | 932 | 완료 기록. ID 재사용 경고(T-013~018 중복) 보존, 역사 기록은 재번호하지 않음 |
| `bindings.md` | 110 | DO NOT 15 인벤토리: 결박(B-1~B-4)·결박 불가(U-1) 등록 형식(사실/정본/사본/이유/결박 테스트명) |
| `ports.md` | 58 | 포트 정본 |
| `dev-environment.md` | 206 | 개발 환경·prod 공개 주소 주입·에이전트 작업 흐름 |
| `docker-management.md` | 1,349 | CLI/API 정본, target 모델, 안전 규칙, 백업 |
| `prod-deployment.md` | 660 | 운영 런북(민감값은 `*.local.md`로 분리) |
| `runtime-pin-registry.md` | 846 | 기능 레퍼런스(불변식·데이터 모델·CLI/API 계약·상황별 대응·체크리스트) |
| `ktdctl-ui-migration.md` | 1,111 | 설계 문서 v5(개정 이력 내장), 태스크 분해 KUM-M1~18 / KUM-MAP-1~4 / KUM-PV-1~4 |
| `dashboard-ui.md`, `design-system.md`, `DESIGN-RULES.md` | 242/51/39 | §3 참조 |
| `general-mgmt-audit.md` | 1,204 | GM-01~20 감사 트랙(심각도/규모/분류/검증/E2E 열) |
| `tvn41-f1d-destructive-rebootstrap.md`, `tvn41-f1j-cancel-probe-fixture.md` | 221/115 | 개별 태스크 설계 |

- 하위 디렉터리(adr/, runbooks/, reviews/, archive/, journal/) **없음**. 런북은 `prod-deployment.md` + gitignore된 `docs/deploy-runbook.local.md`·`docs/prod-access.local.md`(`AGENTS.md` 110·116행).
- task ID 체계: `T-NNN`(초기, 재사용 사고 있음), `T-VN-41-F1D-H300`·`T-VN-40` 등 교차 저장소 VN 트랙, `GM-NN`(감사 트랙), `KUM-M*/MAP-*/PV-*`(UI 이관), `C6c`/`C7`/`M04`/`M05`(워크플로 세대명), `R1-S1` 등(리뷰 라운드-발견 번호).

**개발 환경·워크플로 규약** (사실)

- 정본 OS: Linux/WSL. Windows 실행 금지(git·codegraph 포함). 예외는 n150에서 Playwright가 불가능할 때뿐.
- worktree: 에이전트별 고정(`F:\dev\kor-travel-docker-manager-{antigravity,claude,codex}`, opencode는 `opencode.json`에 `-opencode`), `git switch -c agent/<topic> main`. 브랜치 접두는 실제 이력에서 `feat/`, `refactor/`도 사용(`refactor/general-mgmt-improvements`, `feat/weather-target-and-runtime-fixes`).
- codegraph: worktree마다 `codegraph init -i` 후 `codegraph sync`; `.codegraph/` gitignore. MCP 서버 4종(playwright headless, sequential-thinking, codegraph, filesystem)을 `claude.json`/`codex.json`/`antigravity.json`/`opencode.json`/`.gemini/mcp.json`에 중복 선언.
- 리뷰 정책: **2인 적대적 리뷰**가 관행으로 정착(`CLAUDE.md` 46행 "전문 적대 리뷰 2건", `docs/general-mgmt-audit.md` 9행 "의미 단위마다 전문 적대 리뷰어 2명", `docs/journal.md`에 "적대적 리뷰" 69회, 커밋 `8d0df81 fix: PR #318 적대적 리뷰 2건 반영`). 단 `AGENTS.md`/`SKILL.md`의 규칙으로 성문화되지는 않았다(사실). 리뷰 발견을 mutation-test로 검증하는 관행(`docs/tasks-done.md` 224행).
- PR/브랜치: `main` 직접 푸시 금지, PR 필수(DO NOT 1). 커밋 제목은 `type(scope): 한국어 문장 (#PR)`.
- 보안 감사: 푸시 전 5단계(`git diff --cached` 파일 점검, 비밀 패턴 grep, `.env.example` placeholder 확인, 덤프/로그 혼입 확인)(`AGENTS.md` 118~131행).
- `*.local.md`/`*.local.sh` gitignore(`.gitignore` 45~47행), 각 worktree에 수동 복사.
- 줄바꿈 LF 강제(`.gitattributes` `* text=auto eol=lf`, 2026-08-31 CRLF 사고 기록).
- 서브에이전트 정의: `.claude/agents/`(api-designer, backend-developer, frontend-developer, mobile-developer, ui-designer; 영문 범용 템플릿, `model: opus`), `.codex/agents/*.toml`(+ui-fixer, `gpt-5.5`), `.opencode/agent/`. postgres 스킬 패밀리(design-postgres-tables 등 7종)가 `.agents/`, `.claude/`, `.opencode/`에 3벌 복제.

## 6. CI·배포·운영

- **CI**: `.github/workflows/ci.yml` 하나. 트리거 PR/`main` push/`workflow_dispatch`, `permissions: contents: read`, actions SHA 고정. `backend` job(ubuntu-24.04, py3.11, `pip install -e` + 핀 3종, `ruff check`, `pytest -q`), `frontend` job(Node 20, `npm ci`, `type-check`, `lint --max-warnings=0`, `test`, `build`). pre-commit 설정 없음. dependabot/renovate 없음. mypy·coverage·E2E·이미지 빌드 없음.
- **Compose**: `docker-compose.yml`(1,522줄, `name: kor-travel-docker-manager`). 서비스 약 35개: PostGIS 4 + db-init/role-bootstrap one-shot, `rustfs`(+`rustfs-init` minio/mc), geo api/ui/dagster/dagster-daemon(+db-init), concierge api/mcp/scheduler/ui(+db-init), map postgres/api/ui/dagster/dagster-daemon/application-fresh-300/finalize/storage-migrate/db-role-bootstrap, pinvi api/web/dagster/db-init/admin-bootstrap/db-runtime-role, `prometheus`(v2.53.1), `grafana`(11.1.4), `cadvisor`(v0.52.1). 기본 `network_mode: host`(ADR-16), PostgreSQL superuser password는 Docker secret 파일, `pinvi-postgres` 이미지 digest 고정, map postgres 이미지 ID 필수 env. 단일 canonical 파일만 허용(include/extends/override 거부, `docs/architecture.md` 277~278행).
- **포트**: §1 참조. Manager 12901/12905. weather 14100~14199는 sibling이 자기 compose로 점유(`docs/ports.md` 33행).
- **prod(n150)**: trusted installer `scripts/install-ktdm-trusted-release`(1,880줄 bash)가 release archive 해시 대조 → `/opt/kor-travel-docker-manager` staging→commit 통째 교체, wheelhouse 설치, `.env` 0600 검증, systemd 유닛 설치(`ktdm-backend.service` root 실행 ADR-41, `ktdm-frontend.service` 비root 템플릿 렌더), tmpfiles.d lease 디렉터리(`/run/lock/kor-travel-docker-manager` 0700 root), logrotate. registry/공개 사본/요청 파일은 배포 트리 밖 `/var/lib/kor-travel-docker-manager{,-public,-requests}`. 재기동은 installer가 하지 않고 운영자가 `systemctl restart`. 배포 후 검증은 `/health`·`:12905` 200뿐 아니라 브라우저 로그인→로그아웃 전환(DO NOT 14).
- **시크릿**: `.env`/`.env.production`/`*.local.md` gitignore + rsync 제외, `.env.example`은 placeholder만, inspect 응답은 env redaction(`configValidation.ts` 민감 키 목록과 백엔드 `docker_service.py` 동일 규칙), 푸시 전 grep 스캔.

## 7. 외부 연동 (cross-repo)

- **형제 서비스 호출**: Manager 백엔드가 형제 API를 런타임에 호출하는 코드는 smoke/preflight 한정(예: Map API·PinVi API loopback health GET, `services/c6c_deployment.py` `run_pinvi_canonical_smoke`, `loopback_readiness.py`). 일반 비즈니스 호출 없음(DO NOT 2·5).
- **빌드·구동 연동**: compose build context `${KOR_TRAVEL_GEO_REPO_DIR:-../kor-travel-geo}`(`docker/api.Dockerfile`, `kor-travel-geo-ui/`, `kor-travel-geo-dagster/docker/dagster.Dockerfile`), `../kor-travel-concierge`(`Dockerfile.python`, `frontend/`), `../kor-travel-map`(`docker/frontend.Dockerfile`; API/Dagster는 sealed paired candidate image ID), `../pinvi`(`apps/api/Dockerfile`, `apps/web/Dockerfile`, `apps/etl/Dockerfile`). weather는 HEAD에서 미등록.
- **교차 저장소 계약**(사실, `docs/runtime-pin-registry.md` §1, `docs/bindings.md`): pinset digest 직렬화(`canonical_pinset_bytes`)와 generation manifest v6·rebuild journal v8 문서 스키마는 kor-travel-map attestation(`c7_prod_attestation.py`)이 exact-dict로 결박; PinVi `contracts/kor-travel-map-m05-pair-provenance-v1.json`의 `map.*.source_revision`은 registry `map_revision`의 결박 불가 사본(U-1); Map `packages/kor-travel-map-api/openapi{,.service,.user}.json` 해시를 M05 E2E가 대조.
- **인증/토큰 주입**(Manager가 값을 소유·주입, 소비하지 않음): `KOR_TRAVEL_MAP_API_SERVICE_TOKEN`, `KOR_TRAVEL_MAP_API_OPS_READ/CANCEL/FIXTURE_TOKEN`, `KOR_TRAVEL_{GEO,MAP}_ADMIN_PROXY_SECRET`, `KOR_TRAVEL_CONCIERGE_UI_ADMIN_PROXY_SECRET`, `KOR_TRAVEL_MAP_KOR_TRAVEL_GEO_API_KEY`(Geo가 Map consumer에 발급), `*_UI_ADMIN_PASSWORD_HASH`/`*_UI_SESSION_SECRET`(geo/map/concierge UI 로그인) — 형제 admin UI가 모두 "관리자 해시 + 세션 시크릿 + admin proxy secret" 같은 모양의 env 계약을 갖는다는 간접 근거(`.env.example` 키 목록).
- **패턴 이식 이력**: 관리자 인증·API 키(geo PR #399 → ADR-19), 오류 복구 boundary(geo PR #391 → ADR-17), 로그인/모달 spacing(geo 실측, 2026-08-26), Rail-Workbench/StatStrip/AppShell slot(map admin, 2026-08-31).
- **공유 라이브러리**: `python-*-api`, `python-kraddr-base`, `maplibre-vworld-*`, `vworld-map-*` tgz 사용 **없음**(backend 의존·frontend lockfile grep 0건). `NEXT_PUBLIC_VWORLD_API_KEY`·`KOR_TRAVEL_CONCIERGE_UI_VWORLD_SERVICE_KEY`·`KOR_TRAVEL_GEO_VWORLD_API_KEY`는 형제 컨테이너에 주입하는 값일 뿐이다.

## 8. 공통화 후보

| # | 영역 | 근거 경로 | 신뢰도 | 비고 |
|---|---|---|---|---|
| 1 | UI · 디자인 토큰 계약(oklch 색 역할 20종 + shadow/radius/easing/space/duration/z-index) | `frontend/tokens.css`, `DESIGN.md` 20~62행 | 높음 | 역할명(`page/card/subtle/line/strong/ink/secondary/brand/ok/warn/danger/info`)이 map·geo와 개념적으로 겹친다. 값(Ember 오렌지)은 제품 정체성이라 common은 **역할 스키마와 라이트 기준값**만 공급하고 hue는 앱이 덮어쓰는 구조가 적합(선행 보고서 §3.5와 일치) |
| 2 | UI · `StatStrip` | `frontend/src/components/StatStrip.tsx`; map `packages/kor-travel-map-admin/frontend/src/components/stat-strip.tsx`; pinvi `apps/web/components/admin/stat-strip.tsx` 1행 | 높음 | 세 저장소 3벌 존재(pinvi가 map 이식을 명시). props 계약이 거의 동일. ktdm 판은 `help` 없음·CSS 클래스 기반 — common 판은 map 형태를 기준으로 `title` prop 흡수 |
| 3 | UI · `AppShell`(rail-workbench: 접힘 상태 localStorage, 그룹 메뉴, `data-slot="admin-shell-*"`, skip-link, 1024px 분기) | `frontend/src/components/layout/AppShell.tsx`; map `admin-shell.tsx` 187·240·391·458행 | 높음 | slot 이름·localStorage 키 패턴·64rem 분기점이 동일. 메뉴 데이터(`NavGroup[]`)만 앱 주입 |
| 4 | UI · 오류 humanize 계층(`ApiError` 파싱 → `HumanError{title,hint,raw,requestId}` → Toast/InlineError) | `frontend/src/lib/api.ts` 1~58행, `lib/errors.ts`, `components/Toast.tsx`, `components/InlineError.tsx`, `docs/dashboard-ui.md` §1 | 중간 | FastAPI `{detail: str \| {code,message}}` 파싱과 요청 ID 노출은 형제 FastAPI 백엔드 전부에 적용 가능. `CODE_MESSAGES` 사전은 앱별. map은 sonner를 쓰므로 토스트 렌더러는 어댑터 필요 |
| 5 | UI · `CopyableCommand`(CLI 전용 작업의 명령 복사 카드) | `frontend/src/components/CopyableCommand.tsx`, `docs/dashboard-ui.md` §5 | 중간 | 운영 콘솔 공통 패턴(geo/map admin에도 CLI 전용 작업 존재 여부는 미확인) |
| 6 | UI · App Router 오류 복구 boundary(`error.tsx`/`global-error.tsx` + `AppErrorPanel` + chunk/RSC 오류 1회 hard reload) | `frontend/src/app/error.tsx`, `global-error.tsx`, `components/layout/AppErrorPanel.tsx`, `lib/error-recovery.ts`; ADR-17 | 높음 | geo PR #391에서 이식된 것이 문서로 확인됨 — 이미 2벌 이상 |
| 7 | UI · 접근성·모션 베이스(`focus-visible` 2px brand outline, `prefers-reduced-motion` 무력화, `touch-action: manipulation`, skip-link, 모달 ESC/초기 focus 규약) | `frontend/src/app/globals.css` 5~82행, `docs/dashboard-ui.md` §6 | 높음 | 프레임워크 무관 CSS 조각으로 분리 가능 |
| 8 | UI · 로그인 화면 패턴(단일 관리자, `aria-live="assertive"` 상시 마운트, 429/403/503 문구) | `frontend/src/components/LoginScreen.tsx`, `docs/journal.md` 2660~2666행 | 중간 | geo와 spacing까지 맞춘 기록이 있음. 단 인증 경계(세션 위치)는 geo(Next 측)와 ktdm(백엔드 쿠키)이 다르다(선행 보고서 §3.6 재확인) |
| 9 | 백엔드 · 관리자 인증 프리미티브(pbkdf2 해시 형식 `pbkdf2_sha256:iter:salt:hash`, HMAC 서명 쿠키, DB 세션 해시, Origin 검사, 로그인 rate limit, 감사 행, 신뢰 프록시 CIDR+secret 헤더) | `backend/src/kor_travel_docker_manager/services/auth_service.py`, `api/auth.py`, ADR-19 | 중간 | ADR-19가 geo PR #399 패턴을 따랐다고 명시 → 최소 2벌. 공통 python 패키지 후보이나 SQLite 세션 저장소 결합을 풀어야 함 |
| 10 | 백엔드 · 요청 상관관계 ID(서버 발급 `X-Request-ID`, contextvar 로그 필터, CORS expose, 오류 envelope `request_id`) | `backend/src/kor_travel_docker_manager/request_context.py`, `main.py` 256~275행 | 높음 | 프론트 `ApiError.requestId`와 짝. FastAPI 형제 전부에 즉시 적용 가능 |
| 11 | 백엔드 · 계약 오류 envelope 규약(`{detail:{code,message,stage,mutation_applied,...}, request_id}` + 상태코드 매핑 409/500) | `backend/src/kor_travel_docker_manager/main.py` 284~356행, `services/errors.py` | 중간 | 공통 규칙(OpenAPI/에러 규약) 문서 후보. base 케이스가 평문 문자열로 남은 이유(테스트 부분 문자열 단언)가 주석에 있어 마이그레이션 비용 명시됨 |
| 12 | 백엔드 · 공개 API 키 프리미티브(32자 CSPRNG, SHA-256 해시 + 끝 6자 힌트, `?key=` dependency, 1회 노출) | `services/public_api_key_service.py`, `api/security.py` | 중간 | ADR-19 "VWorld 호환 32자" 계약이 geo v2 API와 같다고 기술 |
| 13 | 백엔드 · Prometheus 노출 규약(수기 text exposition, `ktdm_` 접두, `*_available` 게이지로 결측 구분, `Cache-Control: no-store`) | `services/metrics_collector.py` 655~914행, `main.py` 378~390행 | 낮음 | 접두 규칙(`ktg_`/`ktdm_`)만 공통 규칙으로 승격 가능. prometheus-client 미사용이라 코드 공유는 어려움 |
| 14 | 백엔드 · root-safe atomic write / dir fsync / `env_flag` 프리미티브 | `services/secure_state_file.py`(GM-10) | 중간 | 문서가 "12벌 복제"를 문제로 지목. 상태 파일을 쓰는 형제 CLI에 공통 유틸 후보 |
| 15 | 백엔드 · 중복 키 거부 YAML 로더 | `services/yaml_strict.py` | 중간 | 사람이 편집하는 설정 파일을 읽는 모든 형제에 유효 |
| 16 | 규칙 · 포트 정책(`12000 + index*100 + offset`, DB `+0`, API `+1`, UI `+5`, Manager 129xx, weather 141xx) | `docs/ports.md`, `AGENTS.md` DO NOT 4·9 | 높음 | 이미 전 형제가 따르는 계열 규칙 — common 규칙 문서의 정본 후보 |
| 17 | 규칙 · 문서 언어·진입 파일 체계(AGENTS/CLAUDE/SKILL/DESIGN + docs 평면 + decisions/journal/tasks/tasks-done, 지시 우선순위, `*.local.md`) | `AGENTS.md` 40~52·104~110·135~142행, `docs/` 트리 | 높음 | canview 참조 모델과 대조 필요(본 조사 범위 밖). ADR 표준 형식(`docs/decisions.md` 5~33행) 재사용 가능 |
| 18 | 규칙 · DO NOT 15 "유도→결박→탐지"와 `bindings.md` 등록 형식, `test_normative_docs_cite_real_symbols` | `AGENTS.md` 162~169행, `docs/bindings.md`, `backend/tests/test_normative_docs_cite_real_symbols.py` | 높음 | 버전 일치·중복 선언 정책의 **선행 사례**. common이 "라이브러리 버전 일치"를 정책화할 때 그대로 인용 가능 |
| 19 | 규칙 · runtime pin registry(값은 파일·계약은 코드·생애는 registry, 공개 사본, 2-step 요청, `pin verify` fail-close, 디렉터리 fsync) | `docs/runtime-pin-registry.md` §0~§7-1, ADR-40, `services/runtime_pin_registry.py`(1,313줄) | 중간 | "버전 핀을 코드 상수에서 root 소유 레지스트리로" 옮긴 사례. common의 버전 일치 정책이 형제별 lockfile/핀 파일을 어떻게 소유·검증할지의 설계 참고. 코드는 Map/PinVi 2-role에 결박돼 직접 재사용은 부적합 |
| 20 | 규칙 · 개발 환경 정본(Linux/WSL 전용, Windows 금지, 에이전트별 worktree, codegraph, 푸시 전 보안 감사, LF 강제, 2인 적대 리뷰 관행) | `AGENTS.md` 86~131행, `.gitattributes`, `docs/general-mgmt-audit.md` 9행 | 높음 | 관행 vs 성문화 격차(2인 리뷰)를 common 규칙에서 성문화 |
| 21 | 규칙 · UX 계약 문서(`dashboard-ui.md`: 비전문 관리자 원칙 3, 확인 규약, 정직성 규약, 패널 추가 체크리스트) | `docs/dashboard-ui.md` §0·§3·§7·§8 | 높음 | 제품 무관 조항이 많아 common UX 가이드의 초안으로 적합 |
| 22 | 규칙 · 디자인 감사 기준(금지 패턴 목록, 320/375/414/768 검증, `transition-all` 금지, 라이브 데이터 없는 수치 금지) | `DESIGN.md` 134~139행, `docs/design-system.md` 46~51행 | 높음 | Hallmark 감사 결과가 규칙으로 정착. map도 Hallmark 마커를 쓰므로 계열 공통 |
| 23 | 도구 · CI 골격(SHA 고정 actions, `contents: read`, `workflow_dispatch` 복구 진입점, `npm ci`, `--max-warnings=0`) | `.github/workflows/ci.yml` | 중간 | 재사용 가능한 워크플로/composite action 후보. Python 측은 poetry lock 부재로 형제와 다름 |
| 24 | 도구 · 프론트 툴체인 무결성 검사(`npm ls --depth=0` 게이트) | `scripts/verify-frontend-toolchain.sh` | 낮음 | rsync+호스트 빌드 배포 방식에 특화 |
| 25 | 도구 · vitest + jsdom + RTL + `renderWithQueryClient` 테스트 골격 | `frontend/vitest.config.mts`, `src/vitest-setup.ts`, `src/test-utils.tsx` | 중간 | react-query 사용 앱 공통. Vite 8 + `@vitejs/plugin-react` 필요성이 주석에 기록됨 |

## 9. 이 저장소 고유 차이·주의점

| 영역 | 내용 | 공통화 시 영향 |
|---|---|---|
| 프레임워크 세대 | Next 14.2.35 / React 18.3.1 / eslint 8 / `.eslintrc.json`(사실). 업그레이드 계획 문서 없음 | common이 React 19/Next 16 기준이면 이 앱은 peer 불일치. 선행 보고서 §2의 "업그레이드와 공통화는 독립 작업" 권고가 그대로 적용됨. 사용자 전제 (2)의 버전 일치화 대상 1순위 |
| UI 프리미티브 부재 | radix/base-ui/shadcn 없음, `ops-*` CSS 클래스 + 소수 Tailwind 유틸. ADR-17이 의도적으로 미도입 | common UI 패키지가 base-ui/shadcn 기반이면 이 앱은 "컴포넌트 이식"이 아니라 "프리미티브 도입"부터 시작. CSS 클래스 이름 충돌은 `ops-` 접두 덕에 낮음 |
| 스타일 아키텍처 | 토큰은 `@theme`이지만 컴포넌트 스타일 대부분이 `@layer components`의 수기 CSS 1,300줄 | Tailwind 유틸리티 중심 common과 이질. 선행 보고서 §7.3의 "사전 빌드 CSS + CSS 변수" 배포안이 이 앱에 유리 |
| 다크 모드 | 없음(라이트 단일) | common 토큰이 다크 세트를 요구하면 이 앱은 라이트만 소비하도록 명시 필요 |
| 폰트 | 웹폰트 미로드, OS 폰트 의존. `DESIGN-RULES.md`는 Cobalt 시대 폰트를 잘못 기술 | common이 Pretendard를 번들/로드하기로 하면 이 앱의 "로드 없음" 결정과 충돌 — 문서 정정 필요 |
| 문서-코드 불일치 | README/AGENTS/CLAUDE/architecture.md의 "Shadcn UI, Zod, React Hook Form" 표기, `.hallmark/log.json`의 Cobalt, `DESIGN-RULES.md` 폰트, architecture.md의 10px radius | 인벤토리 자동화 시 문서를 근거로 삼으면 오판. 코드/lockfile을 정본으로 봐야 함 |
| 인증 경계 | Next 측 서버 코드 0, 백엔드 쿠키 SameSite=strict + Origin 검사. 프론트는 완전 정적 SPA | geo(Next 세션 검증) 계열과 로그인 컴포넌트를 공유해도 세션 어댑터는 별도(선행 보고서 §3.6 재확인) |
| 백엔드 의존 관리 | poetry 선언 + lock 없음 + CI pip 핀 + 운영 wheelhouse 3중 | 버전 일치 정책이 "lockfile 존재"를 전제로 하면 이 저장소는 먼저 `poetry.lock`(또는 uv) 도입이 필요. `AGENTS.md` DO NOT 15의 "lockfile 없으면 하드 실패" 문구와 현재 상태가 모순 |
| ruff format 미적용본 | `ruff format` 전체 실행 금지 | common이 포맷터 통일을 정책화하면 대규모 1회 재포맷 PR이 불가피(리뷰 불가 경고 있음) |
| 도구 버전 drift | pytest `^8` 선언 vs CI 9.1.1, ruff `^0.3` vs CI 0.16.4, httpx `^0.27` vs 0.28.1 | 버전 표에서 "선언"과 "실행"이 다른 대표 사례 |
| 거대 모듈 | `compose_service.py` 8,166줄, `c6c_deployment.py` 7,048줄, `DashboardClient.tsx` 1,970줄 | 공통 유틸 추출 시 결합도 높음. KUM-M12가 JSX 분해를 의도적으로 보류 |
| 교차 저장소 계약 결박 | pinset digest·manifest v6·journal v8은 map/pinvi 동시 PR 없이는 변경 불가(`SKILL.md` DO NOT 10) | common이 이 코드를 흡수하면 세 저장소 릴리스가 동시 결합 — 흡수 부적합 |
| 배포 형태 | 컨테이너 아님(systemd + venv + `npm run start`), rsync 소스 배포 | Dockerfile 기반 공통 이미지 규약에서 예외 |
| 라이선스 | MIT(형제 geo/map/weather는 GPL-3.0, 선행 보고서 §9) | common이 GPL-3.0이면 MIT 앱이 소비하는 방향은 문제없으나, 이 저장소 코드를 common으로 옮길 때 저작권 표기 유지 필요 |
| 한국어 정책 | 코드 주석·docstring·커밋까지 한국어 | common 코드 주석 언어 정책 결정 필요 |

## 10. 버전 표

"선언"은 `frontend/package.json`·`backend/pyproject.toml`, "설치"는 `frontend/package-lock.json`(백엔드는 lock 부재라 CI 핀을 기재).

| 항목 | 선언 범위 | lockfile/CI 설치 |
|---|---|---|
| node | 미선언(engines 없음) | CI 20 (`ci.yml`), 문서 20 LTS |
| npm | 미선언 | lockfileVersion 3 |
| next | `^14.1.4` | 14.2.35 |
| react / react-dom | `^18.2.0` | 18.3.1 |
| typescript | `^5.4.3` | 5.9.3 |
| tailwindcss | `^4.0.0` | 4.3.1 |
| @tailwindcss/postcss | `^4.0.0` | 4.3.1 |
| @base-ui/react / radix-ui | 없음 | 없음 |
| shadcn | 없음(`components.json` 없음) | 없음 |
| lucide-react | `^0.363.0` | 0.363.0 |
| eslint / eslint-config-next | `^8.57.1` / `^14.2.35` | 8.57.1 / 14.2.35 |
| vitest | `^4.1.11` | 4.1.11 (vite 8.2.2) |
| playwright | 없음 | 없음 |
| @tanstack/react-query | `^5.28.0` | 5.101.0 |
| zod / zustand / react-hook-form | 없음(GM-19에서 zod·RHF 제거) | 없음 |
| recharts | `^3.8.1` | 3.8.1 |
| maplibre-gl | 없음 | 없음 |
| python | `^3.11` | CI 3.11 |
| fastapi | `^0.110.0` | 미확인(lock 없음) |
| pydantic / pydantic-settings | `^2.6.0` / `^2.2.0`(미사용) | 미확인 |
| sqlalchemy | `^2.0.0` | 미확인 |
| alembic / asyncpg / psycopg | 없음 | — |
| uvicorn | `^0.28.0` | 미확인(주석상 0.28.1) |
| docker (SDK) | `^7.0.0` | 미확인 |
| ruff | `^0.3.0` | CI 0.16.4 |
| mypy | `^1.9.0`(CI 미실행) | 미확인 |
| pytest | `^8.0.0` | CI 9.1.1 |
| httpx (dev) | `^0.27.0` | CI 0.28.1 |
| dagster | 없음 | — |
| 관리 대상 이미지 | postgis/postgis 16-3.5(+digest), prometheus v2.53.1, grafana 11.1.4, cadvisor v0.52.1, rustfs latest | `docker-compose.yml` |

## 11. 미확인·열린 질문

1. Next 14/React 18을 유지하는 **명시적 이유**가 어느 문서에도 없다. 업그레이드 시 위험 요소(`target: es5` tsconfig, eslint 8 legacy config, `next lint` 제거 예정, recharts 3 + React 19 peer)는 실제 시도 전까지 미확인.
2. 백엔드 실제 설치 버전(fastapi/pydantic/uvicorn 등): `poetry.lock` 부재로 미확인. 운영 wheelhouse 내용도 저장소 밖.
3. `docs/resume.md`가 규범 문서 목록(`test_normative_docs_cite_real_symbols.py`)과 `docs/bindings.md` B-4에 등장하지만 저장소에 없다 — 삭제된 것인지 미작성인지 미확인.
4. map/pinvi의 Toast(sonner)·Alert·HelpTip과 ktdm `Toast`/`InlineError`의 시각·동작 차이는 파일명 수준까지만 확인했다(map `components/ui/alert.tsx`, `sonner.tsx` 내용 부분 열람). 상세 비교는 map/pinvi 인벤토리 담당과 교차 검증 필요.
5. `.claude/agents/*.md`의 서브에이전트 정의가 실제로 사용되는지(영문 범용 템플릿, context-manager 프로토콜 언급) 미확인.
6. `frontend/public/images/` BMW PNG 6장이 배포 산출물에 포함되는지(참조 0건이지만 `public/`은 그대로 서빙됨) 미확인.
7. 선행 보고서가 언급한 "docker-manager admin은 자체 컴포넌트"는 재확인됐으나, 선행 보고서 표의 lucide/recharts 이외 라이브러리 목록은 없어 추가 비교 불가.
8. 2인 적대적 리뷰가 규칙(AGENTS/SKILL)이 아닌 관행이라는 판단은 grep 결과에 근거한다. 다른 정본(`docs/deploy-runbook.local.md` 등 gitignore 파일)에 성문화됐을 가능성은 미확인.
9. weather target 재등록 계획(`docs/journal.md` 2026-09-05 "회전이 weather target의 미완 등록에서 막혔다")의 후속은 기준 커밋 이후라 미확인.
10. `KTDM_DEPLOYMENT_LIFECYCLE`(`docs/architecture.md` 222행)이 `.env.example`에 없다 — 문서/예시 drift 여부 미확인.

## 12. 근거 파일 목록

실제로 열람한 파일(모두 `F:/dev/kor-travel-common-survey/ktdm-main/` 상대 경로, 별도 표기 제외):

1. `LICENSE`
2. `README.md`
3. `AGENTS.md`
4. `CLAUDE.md`
5. `SKILL.md`
6. `DESIGN.md`
7. `.gitignore`
8. `.gitattributes`
9. `.hallmark/log.json`
10. `claude.json`, `codex.json`, `opencode.json`, `antigravity.json`, `.codex/config.toml`, `.gemini/mcp.json`
11. `.claude/agents/frontend-developer.md`, `.claude/agents/ui-designer.md`, `.claude/agents/api-designer.md`, `.codex/agents/ui-fixer.toml`, `.claude/skills/postgres/SKILL.md`
12. `.github/workflows/ci.yml`
13. `.env.example`
14. `docker-compose.yml`(서비스·이미지·포트·build 라인 및 1~40행)
15. `config/docker-targets.yml`(1~90행), `config/runtime-pins.seed.json`, `config/prometheus/prometheus.yml`, `config/grafana/provisioning/datasources/prometheus.yml`
16. `deploy/systemd/ktdm-backend.service`, `deploy/systemd/ktdm-frontend.service.template`, `deploy/tmpfiles.d/kor-travel-docker-manager.conf`, `deploy/logrotate.d/kor-travel-docker-manager.template`
17. `scripts/verify-frontend-toolchain.sh`, `scripts/check-env-permissions.sh`, `scripts/install-ktdm-trusted-release`(1~50행), `scripts/provision-ktdm-offline-wheelhouse.py`(1~40행)
18. `frontend/package.json`, `frontend/package-lock.json`(버전 조회), `frontend/postcss.config.js`, `frontend/tsconfig.json`, `frontend/.eslintrc.json`, `frontend/vitest.config.mts`, `frontend/.env.example`
19. `frontend/tokens.css`
20. `frontend/src/app/globals.css`(1~130행, 1110~1300행, 구조 grep), `layout.tsx`, `providers.tsx`, `page.tsx`, `error.tsx`, `global-error.tsx`
21. `frontend/src/components/layout/AppShell.tsx`, `layout/AppErrorPanel.tsx`(1~30행)
22. `frontend/src/components/StatStrip.tsx`, `Toast.tsx`, `InlineError.tsx`, `CopyableCommand.tsx`(1~14행), `LoginScreen.tsx`
23. `frontend/src/components/DashboardClient.tsx`(1~14, 60~115, 880~1000행 및 grep), `ContainerDetailModal.tsx`(1~14행, grep), `AdminSettingsPanel.tsx`·`BackupHistoryPanel.tsx`·`RuntimePinPanel.tsx`·`SourceStatusPanel.tsx`(각 1~14행), 테스트 4파일 헤더
24. `frontend/src/lib/api.ts`(1~100, 500~580행), `errors.ts`, `error-recovery.ts`, `github.ts`(1~30행), `format.ts`, `containerPresentation.ts`(1~60행), `configValidation.ts`(1~40행)
25. `frontend/src/test-utils.tsx`, `frontend/src/vitest-setup.ts`
26. `backend/pyproject.toml`
27. `backend/src/kor_travel_docker_manager/main.py`, `_time.py`, `request_context.py`, `database.py`, `models.py`
28. `backend/src/kor_travel_docker_manager/api/auth.py`, `api/security.py`, `api/admin.py`(1~60행), `api/routes.py`(1~70행 및 데코레이터 grep), `api/websocket.py`(1~50행)
29. `backend/src/kor_travel_docker_manager/cli.py`(1~60행 및 명령 grep)
30. `backend/src/kor_travel_docker_manager/services/errors.py`, `auth_service.py`(1~80행 및 grep), `public_api_key_service.py`(1~40행), `metrics_collector.py`(메트릭 이름 grep), `registry.py`(1~60행), `compose_service.py`(1~50행), `docker_service.py`(1~40행), `yaml_strict.py`(1~30행), `secure_state_file.py`(1~60행)
31. `backend/tests/conftest.py`, `test_service_layer_boundaries.py`(1~70행), `test_normative_docs_cite_real_symbols.py`(1~50행 및 grep), `test_ws_contract.py`(1~30행), `test_api.py`(1~40행), 테스트 파일 목록
32. `docs/architecture.md`, `docs/ports.md`, `docs/bindings.md`, `docs/tasks.md`, `docs/dev-environment.md`, `docs/design-system.md`, `docs/DESIGN-RULES.md`, `docs/dashboard-ui.md`
33. `docs/decisions.md`(ADR 제목 전체, ADR-6·17·19·36·37·40·41 본문)
34. `docs/runtime-pin-registry.md`(1~140, 244~595행, 제목 전체)
35. `docs/ktdctl-ui-migration.md`(1~120, 626~644, 848~941, 980~1030행, 제목 전체)
36. `docs/docker-management.md`(212~362행, 제목 전체), `docs/prod-deployment.md`(1~60행, 제목 전체), `docs/general-mgmt-audit.md`(1~40행 및 grep), `docs/tasks-done.md`(1~18행, 제목, 224~227행), `docs/journal.md`(1~60, 1117~1200, 2660~2706, 3167~3200, 4200~4240, 6788~6800, 6945~6960행 및 grep)
37. 교차 확인: `F:/dev/kor-travel-geo-fixes/docs/kor-travel-common-library-review.md`(제목 전체, 22~40, 159~190행, docker-manager 언급 grep); `F:/dev/kor-travel-common-survey/ktm-main/packages/kor-travel-map-admin/frontend/src/components/stat-strip.tsx`(1~40행), `admin-shell.tsx`(grep), `ui/sonner.tsx`(1~20행), `git ls-files` 목록; `F:/dev/kor-travel-common-survey/pinvi/apps/web/components/admin/stat-strip.tsx`(1~30행), `git ls-files` 목록
