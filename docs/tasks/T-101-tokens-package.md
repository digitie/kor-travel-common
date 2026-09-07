# T-101 packages/tokens(tokens.css map 값+.dark·theme.css `kt-`·shadcn.css·base.css·base.scoped.css·dark-class/media.css) + 생성물(tokens.json·tokens.ts·tailwind-preset.cjs; 정본 CSS) + 루트 npm workspace·lock + `npm pack` 설치 스모크

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 패키지 빌드·tarball 설치
- 선행: T-003, T-004

## 목표

값 무변경(map 정본) 토큰 패키지 `packages/tokens`를 만들어 Phase 1의 유일한 코드 산출물을 세운다. 정본은 `tokens.css` 하나이고 나머지는 생성물이다. 루트 npm workspace와 lock, `npm pack` 후 임시 프로젝트 설치 스모크까지가 이 task의 gate다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-12(접두 `--kt-*`·역할 목록·shadcn alias 의미·프로필·오버라이드 허용 목록·다크·정본/생성물·값 형식), D-10(`kt-` 유틸리티 네임스페이스·`theme.css` 정의·`base.scoped.css`), D-01(의존 방향), D-11(tarball에 고지 동봉·`license` 필드), D-31(SemVer 0.x), D-33(루트 `package.json` workspaces·`packageManager npm@11.19.1`·`engines.node ^22.12.0`·`.nvmrc 22.23.1`·루트 lock 커밋), O-4·O-11 기본값.
- ADR-005·ADR-006 — [docs/adr/README.md](../adr/README.md). 규칙 정본 초안은 [design-tokens.md](../standards/design-tokens.md)(T-104가 실물과 대조).
- 근거: [디자인 토큰 조사](../survey/cross/design-tokens.md) §3.2.1~§3.2.3(라이트·다크 값·alias), §3.4.2(대비 실측), §3.6.1(`--kt-*` 0회), §3.6.2(계층 2단), §3.6.3(산출물 표), §3.6.5(타입 스케일은 `@theme` 비inline), §3.6.6(다크), §5; [UI 컴포넌트 조사](../survey/cross/ui-components.md) §6.3; [map 인벤토리](../survey/inventory/kor-travel-map.md) §3.1(`globals.css` 정본, hairline 2종)·§9; [airport 인벤토리](../survey/inventory/kor-travel-airport.md) §3.2(`--muted`/`--accent`/`--radius` 충돌 회피 사례).
- 헤더는 T-003 SPDX 규약(`Origin: kor-travel-map@c494e227 …`), 출처는 `PROVENANCE.md`에 행 추가(GPL 원천이므로 추출 허용).

## 구현 범위

packages job은 [ci-deploy §9](../standards/ci-deploy.md#9-common-자체-ci)에 따라 PR과 main·codex/release-* push에서 실행한다. release push의 github.sha를 checkout하고 필수 job을 path/PR 조건으로 생략하지 않는다. run·산출물 source SHA를 기록한다. 후보 보존 전에 이 실행 경로를 포함해야 한다.

1. 루트: `package.json`(`workspaces: ["packages/*"]`, `packageManager`, `engines`), `.nvmrc`, `package-lock.json`(v3), `.github/workflows` `packages` job(`npm install -g npm@11.19.1` → `npm ci` → committed output check → build → check → `npm pack` → 임시 디렉터리 설치 검사).
2. `packages/tokens/package.json`: `name` `@kor-travel/tokens`(ADR-014 확정), `version 0.1.0`, `license: "GPL-3.0-or-later"`, `files`(CSS·`dist`·`LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`), `exports`(`./tokens.css`·`./theme.css`·`./shadcn.css`·`./base.css`·`./base.scoped.css`·`./dark-class.css`·`./dark-media.css`·`./aliases/*`·`./tokens.json`·`.`→`dist/index.js`+`d.ts`·`./tailwind-preset`), `sideEffects: ["*.css"]`.
3. `packages/tokens/tokens.css`(정본): `:root{--kt-*}` map 값 + `.dark` 완비 + `color-scheme: light`; 역할 전부(surface 4·text 4+strong·icon·border·control-line·brand 4·focus·status 4+tint 4·overlay·radius 2·control-h 2·rail·duration 2·ease 2·shadow 2·z 5·font 2). 값은 OKLCH(map 원본 유지). 공개 CSS subpath도 이 파일을 가리킨다.
4. `theme.css`: `@theme`(타입 스케일 비inline) + `@theme inline`(색·간격·radius·폰트 → `--color-kt-*`·`--spacing-kt-*`·`--radius-kt-*`·`--text-kt-*`·`--font-kt-*`) + `@utility`(duration·z). `shadcn.css`: alias 의미 고정(`--input`=control-line, `--accent`=brand-tint, `--radius`=radius-control, `--border`=장식). `base.css`/`base.scoped.css`(`[data-kt-surface]`): focus-visible 단일 레시피·hairline(순수 CSS와 Tailwind 양쪽)·reduced-motion(스피너 예외)·`button:not(:disabled){cursor:pointer}`. `dark-class.css`(`@custom-variant dark (&:is(.dark *))`)/`dark-media.css`(Tailwind 기본 media variant 유지).
5. `scripts/build.mjs`(Node 22, 외부 의존 0): `tokens.css` → `tokens.json`(DTCG)·`dist/index.js`+`index.d.ts`·`tailwind-preset.cjs`(v3/NativeWind); `--check`로 생성물 diff 검사.
6. 값 대조표: `packages/tokens/VALUES.md`가 아니라 테스트(`packages/tokens/test/values.test.mjs`)로 map `globals.css`(조사 커밋) 추출값과 1:1 비교.

## 범위 밖

- 별칭 shim·weather 예제(T-102), `kt_contrast`·`ux_lint`(T-103), 규칙 문서 확정(T-104), 릴리스(T-109), consumer 프로필 값(pinvi 소유), 폰트 파일 배포, 마커 팔레트 hex.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `package.json`, `package-lock.json`, `.nvmrc`, `packages/tokens/{package.json,README.md,LICENSE,NOTICE,THIRD_PARTY_NOTICES.md}`, `packages/tokens/*.css`(공개 CSS subpath와 같은 정본 경로), `packages/tokens/scripts/build.mjs`, `packages/tokens/test/*.test.mjs`, `packages/tokens/dist/*`(생성물 커밋 여부는 T-104와 함께 결정, 기본 커밋), `.github/workflows/docs.yml`(`packages` job), `PROVENANCE.md`(행 추가).

## 수용 기준

- main·codex/release-* push 사건의 모든 필수 job 선택을 검증하고, common의 임시 release 검증 branch에 코드 변경 없는 검증 commit을 push한 실제 CI run으로 head/source SHA 일치를 확인한다. 태그·GitHub Release 생성은 필요 없다. 이 검증 branch는 PR 또는 보존 ref로 commit 도달성을 확보하고 작업 뒤 정리한다. 검사기를 통과한 PR head 결과를 다른 merge SHA 결과로 대신 기록하지 않는다.

- `packages/tokens/tokens.css`에 D-12 역할 전부가 `:root`·`.dark` 양쪽에 정의되고 `--ktc-`·`--ui-`·`--color-admin-`·`--pv-` 접두가 0건이다.
- 값 비교 테스트가 map 원본과 diff 0(값 무변경)을 단언한다.
- `npm run build --workspace packages/tokens` 후 `npm run check`가 clean(생성물 drift 0).
- `npm pack` tarball에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`·CSS 7종·`tokens.json`·`dist/index.d.ts`가 있고, 임시 프로젝트에서 `require.resolve("@kor-travel/tokens/theme.css")`가 성공한다.
- `check_spdx.py` exit 0, `PROVENANCE.md`에 map `globals.css`·`design.md` 원천 행이 있다.
- `theme.css`의 타입 스케일이 `@theme`(비inline)로 정의된다(pinvi 변수 가리기 기법 지원).
- `kt_contrast` 실행은 T-103 전이므로 `NOT_RUN(T-103 대기)`로 기록하되 map 값의 실측 대비(`dt` §3.4.2)를 인용한다.

## 검증 명령

```bash
npm install -g npm@11.19.1 && npm ci
npm run build --workspace packages/tokens && npm run check --workspace packages/tokens
npm test --workspace packages/tokens
npm pack --workspace packages/tokens --pack-destination /tmp/kt
tar -tzf /tmp/kt/kor-travel-tokens-0.1.0.tgz | grep -E "LICENSE|NOTICE|THIRD_PARTY|theme.css|tokens.json|index.d.ts"
cd "$(mktemp -d)" && npm init -y >/dev/null && npm install /tmp/kt/kor-travel-tokens-0.1.0.tgz && node -e "console.log(require.resolve('@kor-travel/tokens/theme.css'))"
python3 -B -X utf8 tools/check_spdx.py
```

Git Bash에서 동일(`/tmp` 대신 임의 디렉터리).

## evidence

- 로컬 확인: Node `v25.9.0`, npm `11.12.1`에서 `npm ci --ignore-scripts --no-audit --no-fund`, `npm run build --workspace packages/tokens`, `npm run check --workspace packages/tokens`, `npm test --workspace packages/tokens`(6개 통과), `npm pack` 및 공개 subpath 설치 스모크를 실행했다. 요구 버전 Node 22.23.1/npm 11.19.1은 로컬에 없어 버전 일치 gate는 `NOT_RUN(로컬 런타임 미설치)`이다.
- 현재 tarball은 CSS 7종·`LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`·`dist/index.d.ts`·`dist/tokens.json`을 포함하며, 임시 프로젝트에서 공개 subpath 10개(`@kor-travel/tokens` 포함)의 `require.resolve`가 성공했다. 산출물은 `npm run check`에서 drift 0이다.
- `kt_contrast`는 `NOT_RUN(T-103 대기)`, 소비자 저장소 build/e2e·실제 Release·npm/PyPI 게시·소비자 채택은 `NOT_RUN(사용자 범위와 후속 task)`이다. PR의 `packages` job과 main/release push 실제 run은 draft PR 이후 기록한다.

## rollback 또는 release 차단 조건

- 미배포 상태이므로 `git revert` 1회로 원복한다.
- map 값과 diff가 0이 아닌데 ADR 갱신이 없으면 merge 차단. 생성물 drift, 고지 파일 미동봉, SPDX 실패는 T-109 rc 발행 차단 조건이다.
