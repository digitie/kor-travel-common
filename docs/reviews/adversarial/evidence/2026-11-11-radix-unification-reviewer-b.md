# 독립 적대리뷰 B — common 통합 1차

- 실행 ID: `review-B-common-1-20261111`
- 역할: 구현에 참여하지 않은 packaging / dependency / CI / license 독립 리뷰어 B
- 시작: 2026-11-11 21:51:20 +09:00 (최초 기록 시각; 지시 문서 확인은 그 전에 시작)
- 종료: 2026-11-11T22:02:46+09:00
- 종류: FULL, 동일 immutable manifest 1차
- verdict: **BLOCK**
- finding: **P0 1건 / P1 7건 / P2 3건**, 전부 `OPEN`

현재 작업 트리의 수정 결과를 판정에 섞지 않았다. 아래 OPEN은 manifest 후보에 대한 상태다. 부모가 수정 중이라고 전달한 항목도 새 manifest의 불변 delta 재검토 전에는 FIXED로 표시하지 않는다. 다른 리뷰어의 이번 원본 보고서·finding·통합 결과는 열람하지 않았다. 필수 진입 문서의 과거 아카이브 색인·resume에 있는 역사적 요약은 현재 리뷰 입력으로 사용하지 않았다.

## 기준선·입력·격리

manifest: `/home/digitie/dev/common-unification-20261111/review-manifest-common-1.json`

| 저장소 | base | 실제 확인한 head |
|---|---|---|
| kor-travel-common | c289b4624c8640eb918cc915803e72ae754e58fb | 789e6d2e179a055b3cd793fb886083543244089c |
| maplibre-vworld-react | 9c46c57181d433c91f7e8837c4e4396204e9b583 | 7402214b9d4829f1f73f80ac29f68d22e2809254 |

`git rev-parse <sha>^{commit}` 및 `git show <sha>:<path>`, `git diff <base> <sha>`로 불변 객체를 확인했다. 빌드·재현은 아래 detached worktree에서만 수행했다.

- `/home/digitie/dev/common-unification-20261111/review-b-common-isolated`
- `/home/digitie/dev/common-unification-20261111/review-b-map-isolated`

두 worktree 모두 시작과 종료의 `git status --porcelain=v1`은 빈 문자열이고 HEAD는 표의 SHA였다. source·tracked 파일을 편집하지 않았다. 검증용 소비 앱·공격 fixture는 `/tmp/review-b-*`에 만들었다. 기존 checkout의 plain 파일·다른 리뷰어 report는 읽지 않았다. common의 고정 `AGENTS.md`, `docs/README.md`, `docs/resume.md`, `docs/runbooks/agent-workflow.md`, `docs/reviews/README.md`, 관련 T-218·ADR-017·라이브러리/라이선스 규약과 upstream AGENTS를 참조했다.

전달 요청의 핵심 제약은 다음과 같다: “독립 적대리뷰 B: 구현에 참여하지 않은 packaging/dependency/CI/license 전문. 다른 리뷰어 결과열람금지.” “gitshow/ref 사용해불변소스읽고확인.” “현재workingtree는부모가통합회귀/기존CI수정중이므로그것을baseline에섞지말것.” “sourceedit금지; 필요한테스트격리worktree에서.” “findingseverity file:line 재현영향권고,verdict.”

전체 사용자 요청 원문은 `review-B-common-evidence/request.txt`에 별도 보존한다. 범위는 package exports·client 지시문·peer/중복 React·pack 의존성·동일 bytes와 lock·workspace/모바일 정책·registry schema·MIT/GPL 출처와 고지·CI 실효성이다. 실제 소비자 저장소의 채택·배포·모바일 네이티브 실행은 이번 범위 밖이다.

## 주요 검증 결과

| 검증 | 결과와 한계 |
|---|---|
| common `npm ci --engine-strict` | 성공, Node 22.22.2 / npm 11.19.1 |
| common `npm run build` | 성공; 소스와 dist의 client 지시문 확인 통과 |
| UI `npm test --workspace packages/ui` | Vitest 91 PASS + 정책 node 8 PASS, skip 0 |
| tokens 시험 | 8 PASS, skip 0 |
| 버전 도구 시험 | `python3 -m unittest discover -s tests -p test_check_versions.py`: 90 PASS, WSL Python 3.14 |
| registry / SPDX | `check_versions.py --self-check` 성공; `check_spdx.py` 189파일 오류 0 |
| upstream | core/web TypeScript 빌드·pack 성공; 다른 전체 검증은 아래 원격 CI와 구분 |
| 네 패키지 tarball | 재생성 SHA512가 manifest와 **모두 일치** |
| UI exports | 설치된 tarball의 88개 조건별 경로 전부 존재; 코드 export의 ESM import 전부 성공 |
| 깨끗한 web tarball 소비 | 네 tarball + 정책 지정 Next/React 등으로 설치 성공; 초기 `npm ls react react-dom --all` 성공, 공통 React 19.3.1 |
| 정상 Next 대조 | 서버 페이지에서 `<Button>` 사용: `next build --webpack` 성공 |
| Next helper 공격 | `buttonVariants`와 `badgeVariants` 각각 서버 호출 시 빌드 실패 |
| 실제 중복 React 공격 | npm 정상 설치 후 19.3.1 / 18.3.1 공존, 검사기는 exit 0; 렌더는 invalid hook call 실패 |
| 실제 tarball 한 바이트 변조 | 검사기 exit 1, `파일·원장·lock 해시 불일치`; 복구 후 exit 0 |
| policy / schema 공격 | 아래 finding별 잘못된 입력이 정상으로 통과함을 재현 |

재생성 artifact 무결성:

- `@kor-travel/ui@0.2.0`: `sha512-m81yqLBWVdTwA1bwRB/HVOdhi2KFQV5ijMh2QfkxYIV5YUI7o7q7YK8qFCejqqUsz2FAXDPgHm8rcFjibbqfZQ==`
- `@kor-travel/tokens@0.1.1`: `sha512-95d/E3rHhORo8etrQear9Phtj9PYgoek5yRueAEGFZkXxMGbfrywyH7hjYKVnDRgJak4rotJ653MOWTyKTY+sQ==`
- `vworld-map-core@1.0.0`: `sha512-tP++7XNg9UYXeeUc+aX8q+RD6/dkVzZuBSXPHUKEqHIRobLjUo1HcPEJruOU0bUzHGxnJL/8reIM7xI+vXYaUw==`
- `vworld-map-web@1.0.3`: `sha512-9S0TUlgu4ky9ztjkanf0lhoijydhcX5ehHtyQB1jla+rGnuPLK4POiH4wIb2v5ATKuO5hOnHEG534gfyuEH+5g==`

증거는 `review-B-common-evidence/`에 보존했다. tarball 원본, 해시 대조 JSON, 소비 manifest/lock, 시험·Next 로그, 정책 공격 harness와 결과, 마지막 isolation 상태를 포함한다. harness에 당시의 절대 경로가 있으므로 worktree 정리 후 재현할 때는 같은 SHA의 새 detached worktree 경로로 조정한다.

## Findings

### B-P0-01 — 지도 core/web 배포 tarball에서 GPL 전문·배포 고지가 빠진다

- 심각도: **P0**, 상태: `OPEN`
- 위치: **upstream `packages/vworld-map-web/package.json:7`**, **`packages/vworld-map-core/package.json:6`**. 근거 규약: common `docs/standards/licensing.md` LIC-14, `docs/runbooks/agent-workflow.md` §5.3.
- 근거: upstream 루트 `LICENSE`는 GNU GPL v3 전문이지만 두 패키지 디렉터리에는 LICENSE/NOTICE가 없고 package metadata에도 license가 없다. `files`는 dist만 담는다. 실제 manifest와 SHA512가 일치하는 core/web tgz를 열면 LICENSE/NOTICE/COPYING 파일이 **0개**다. 루트 라이선스는 npm workspace pack이 자동으로 가져오지 않는다.
- 재현: 고정 upstream에서 `npm run build -w packages/vworld-map-core`, `npm run build -w packages/vworld-map-web`, 두 workspace `npm pack`. `tar -tzf <tgz>`로 내용 확인. 보존한 `review-B-common-evidence/tarballs/vworld-map-{core-1.0.0,web-1.0.3}.tgz`에서도 동일하다.
- 영향: 이번에 공통 배포·vendor 원본으로 지정한 산출물 자체가 패키지 고지 gate를 충족하지 않는다. GitHub 루트에 LICENSE가 있다는 사실만으로 수령 tarball의 고지 누락을 통과시킬 수 없다. 실제 외부 배포 완료 여부는 주장하지 않는다.
- 발생 구분: **상속된 패키징 결함을 이번 배포 후보에서도 재현**했다. upstream diff가 처음 만든 결함이라는 주장은 아니다.
- 권고: upstream 패키지별 GPL 전문·정확한 license/권리자·소스 위치 고지를 동봉하고 pack 내용 assertion을 CI에 추가한다. 신규 미배포 후보로 단일 pack·manifest/lock을 갱신한다. 이미 공개된 같은 버전의 bytes를 덮어쓰지 않는다.

### B-P1-01 — 직접 React만 확인해 전이 중복 React와 실제 hook 실패를 놓친다

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `tools/check_frontend_dependencies.mjs:23`**, `:37` 및 동일한 ui/tokens 배포 사본.
- 근거: `installed(name)`는 앱 기준에서 찾은 한 항목만 반환한다. `lock.packages`의 다른 React/React DOM 인스턴스는 검사하지 않는다.
- 재현: 네 실제 tarball과 정책 버전으로 정상 소비 앱을 설치한 뒤 `react:18.3.1`을 일반 dependencies로 갖는 작은 로컬 tarball `review-b-legacy-widget@1.0.0`을 `npm install`했다. 루트 React는 19.3.1, widget의 실제 해석 React는 18.3.1, 객체 동일성은 false였다. 그런데 배포된 `@kor-travel/ui/check-dependencies.mjs --artifacts common-artifacts.json`은 exit 0과 `공통 의존성과 산출물 일치`를 출력했다. 해당 전이 React의 `useState`를 사용하는 컴포넌트를 앱 React DOM으로 렌더하면 `Invalid hook call` / `Cannot read properties of null (reading 'useState')`로 실패한다. lock은 npm이 생성했으며 수작업 조작하지 않았다.
- 영향: 검사기가 정상이라고 보증한 실제 설치 트리에서 런타임 React hook 계약이 깨진다. 버전/peer 일치 gate가 전이 중복을 보증하지 못한다.
- 권고: 대상 workspace에서 도달 가능한 React/React DOM 설치 경로와 peer 해석을 확인하고 중복·불일치를 실패시킨다. 다른 독립 workspace의 합법적인 별도 인스턴스와 구분한다. 실제 tarball 설치·렌더 반례를 회귀에 포함한다.

### B-P1-02 — devDependencies가 dependencies를 덮어써 잘못된 운영 선언을 통과시킨다

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `tools/check_frontend_dependencies.mjs:19`** 및 두 배포 사본.
- 재현: 정상 policy fixture의 `dependencies.react`를 `18.3.1`로 바꾸고 `devDependencies.react`를 정책 버전 `19.3.1`로 넣으면 exit 0이다(`DEPENDENCIES_BAD_DEV_GOOD`). 객체 병합이 잘못된 runtime 선언을 지운다. 별도 실제 npm fixture에서도 dependencies React18 / devDependencies React19를 선언하면 일반 설치는 19.3.1로 성공하고, 같은 lock의 `npm ci --omit=dev`는 성공하면서 React가 사라져 `require('react/package.json')`가 MODULE_NOT_FOUND가 됐다.
- 영향: 운영 dependencies의 불일치·중복 선언을 정상으로 보고할 수 있고 개발 설치 성공이 운영 설치 보장을 대체한다. 해당 앱에 다른 peer가 React를 다시 설치하는지는 별도지만 선언 검사의 누락 자체는 확정이다.
- 권고: 각 dependency section을 별도로 검증하고 동일 키의 충돌을 명시적으로 거부한다. 필수 runtime 항목과 개발 도구의 section 조건도 구분한다.

### B-P1-03 — 모바일 필수 react-native가 버전 정본 밖에 있어 wildcard·lock 누락도 통과한다

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `versions.json:833`**, **`tools/check_frontend_dependencies.mjs:32`**, **`tools/check_versions.py:369`**.
- 근거: mobile.required에는 react-native가 있지만 frontendPolicy.packages/생성 versions에는 없다. JS는 `wanted`가 없으면 선언과 lock 검사를 통째로 건너뛴다. Python schema도 required와 정책 버전 목록의 연결을 검증하지 않는다.
- 재현: 나머지 모바일 필수 의존성·tokens 해시를 정상으로 유지한 fixture에서 `react-native: "*"`로 선언하고 `lock.packages['node_modules/react-native']`를 삭제했다. `--profile mobile`이 **exit 0**이었다(`MOBILE_REACT_NATIVE_RANGE_NO_LOCK`). 추가 schema 공격에서도 required에 축 없는 이름 추가, 필수 react를 forbidden에도 추가, artifactPackages에 축 없는 이름 추가가 모두 `Registry.load`에서 ACCEPTED였다. 원래 registry self-check 및 90개 회귀도 통과한다.
- 영향: 모바일의 핵심 플랫폼 의존성·설치 증거 누락을 버전 일치로 오인한다. 정본 self-check가 정책 내 불가능한 조건이나 검증되지 않는 필수 항목을 막지 못한다.
- 권고: react-native 정책을 승인된 명시 버전/표현으로 정본화하거나 의도된 제외라면 별도 검증 규칙과 예외 근거를 둔다. required/artifactPackages가 검증 가능한 버전 집합에 포함되는지, required와 forbidden이 충돌하지 않는지 schema와 생성기에서 검증한다. `wanted` 없는 필수 항목을 조용히 skip하지 않는다.

### B-P1-04 — 공개 variants 전용 entrypoint도 client 함수여서 Next 서버 호출이 실패한다

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `packages/ui/src/button-variants.ts:3`**, **`packages/ui/src/badge-variants.ts:3`**, `packages/ui/package.json:186`.
- 근거: 전용 entrypoint는 순수 cva 정의를 갖지 않고 `"use client"`인 button.js/badge.js에서 다시 export한다. shim 자체에 client 지시문이 없더라도 서버 callable이 되지 않는다.
- 재현: 실제 ui/tokens tgz + Next16.4.6/React19.3.1의 깨끗한 앱에서 서버 `app/page.tsx`를 다음처럼 작성하고 `next build --webpack`을 실행한다.

```tsx
import { buttonVariants } from '@kor-travel/ui/button-variants';
export default function Page() {
  return <main className={buttonVariants({ variant: 'default' })}>시험</main>;
}
```

컴파일·타입은 통과하지만 prerender에서 `Attempted to call buttonVariants() from the server but buttonVariants is on the client`로 exit 1이다. badgeVariants도 독립 실행해 같은 실패를 확인했다. 같은 환경의 `<Button>` 대조는 빌드 성공이다.

- 영향: 새 공개 helper 경로를 사용하는 정상적인 Next 서버 페이지가 빌드되지 않는다. export 경로 존재·ESM import 시험만으로 발견되지 않는다.
- 권고: cva 정의를 client 지시문·DOM 의존성이 없는 전용 모듈로 옮기고 client 컴포넌트와 public helper가 이를 함께 import하게 한다. 두 helper의 실제 packed Next 서버 호출을 검증한다.

### B-P1-05 — 기존 필수 package CI가 이전 tarball 파일명에서 중단된다 [부모가 사전 고지]

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `packages/ui/smoke/prepare-lock.mjs:14`**, `packages/ui/smoke/next-app/package.json:10`, `.github/workflows/docs.yml:214`.
- 재현·원격 증거: manifest head의 [packages job 130528691167](https://github.com/digitie/kor-travel-common/actions/runs/43022441710/job/130528691167)은 새 ui0.2.0/tokens0.1.1을 성공적으로 pack한 직후 `kor-travel-tokens-0.1.0.tgz` ENOENT로 실패했다. helper와 smoke manifest는 ui0.1.0-dev.9/tokens0.1.0을 계속 가리킨다. smoke의 React19.3.0·Next16.3.6 등도 새 정본과 다르다.
- 영향: 새 frontend workflow 성공과 별개로 필수 packed Next webpack/Turbopack 및 후속 설치 gate가 실행되지 않는다.
- 권고: smoke manifest/lock/prepare-lock을 새 단일 artifact 원장과 정본에 함께 맞추고, 고정 source SHA에서 필수 CI를 다시 실행한다. 이 원본 보고서는 부모의 진행 중 수정 결과를 확인한 것이 아니다.

### B-P1-06 — shadcn 상태 shorthand가 Radix 상태와 다른 CSS selector로 배포된다 [부모가 사전 고지]

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `packages/tokens/radix.css:4`**, **`packages/ui/src/tabs.tsx:72`** (다른 새 shadcn 부품의 shorthand에도 같은 문제).
- 근거: 제공 CSS에는 shadcn의 상태 custom variant 선언이 없고 소스는 `data-active`, `data-open`, `data-horizontal` 등의 shorthand를 사용한다. `@source` 포함만으로 상태 의미가 교정되지 않는다.
- 재현: 실제 Tailwind4.3.5 compiler에서 `data-active:bg-background`는 `[data-active]` selector, `data-horizontal:flex-col`은 `[data-horizontal]` selector를 생성했다. 실제 Radix Tabs 출력은 `data-state="active"`, `data-orientation="horizontal"`이다. 대조한 `data-[state=active]:bg-background`는 올바른 `[data-state="active"]` selector를 생성했다. tokens 전체 CSS 검색상 custom variant는 dark-class의 dark뿐이다.
- 영향: CSS가 아예 생성되지 않는다는 단순 문제가 아니라 **생성된 selector가 실제 DOM에 매칭되지 않아** 선택·방향·열림 상태 표현이 깨진다. 여러 소비자가 동일 bytes를 받아도 동일하게 잘못된다.
- 권고: 실제 사용되는 모든 상태/그룹/방향 shorthand의 의미를 호환 CSS로 함께 제공하거나 Radix의 실제 data 속성을 명시한 variant로 전환한다. tarball CSS를 사용하는 상태별 브라우저/컴파일 검증이 필요하다.

### B-P1-07 — 필수 docs/tools/secret gate가 오탐·공백으로 실패한다 [부모가 사전 고지]

- 심각도: **P1**, 상태: `OPEN`
- 위치: **common `packages/ui/src/login-form.tsx:50`**, `:69`, **`packages/ui/src/accordion.tsx:62`**; 관련 `.github/workflows/docs.yml`.
- 재현: `python3 tools/scan_secrets.py --all`은 zod의 password 스키마와 setFocus의 필드명에 SECRET-ASSIGNMENT/SECRET-QUOTED **3건**을 보고하며 exit 1이다. 비밀값 유출로 판단한 finding이 아니다. `git diff --check c289b462 789e6d2`도 accordion/breadcrumb 등의 trailing whitespace로 실패한다.
- 원격 증거: 같은 head의 [secret-scan job 130528690892](https://github.com/digitie/kor-travel-common/actions/runs/43022441710/job/130528690892), [Ubuntu tools job 130528690958](https://github.com/digitie/kor-travel-common/actions/runs/43022441710/job/130528690958)에서 같은 세 오탐이 확인된다. docs job은 공백 단계에서 실패하고 tools Windows도 실패 상태다. Ubuntu unittest는 340개 중 skipped=3으로 성공했으므로 이를 schema 회귀 실패로 잘못 보고하지 않는다.
- 영향: 현재 후보의 필수 CI 전체 성공이 아니다. 새 frontend 성공만으로 merge gate를 충족했다고 판단할 수 없다.
- 권고: 실제 비밀 탐지를 약화하지 않는 근거 있는 오탐 처리와 공백 정리를 수행하고 전체 필수 job을 정확한 새 SHA에서 재확인한다.

### B-P2-01 — mobile 프로필이 DOM용 UI 패키지 설치를 허용한다

- 심각도: **P2**, 상태: `OPEN`
- 위치: **common `tools/check_frontend_dependencies.mjs:20`**, **`versions.json:830`**. 계약 근거: `docs/standards/frontend-libraries.md:7`의 모바일 DOM UI 미설치 규칙.
- 재현: 정상 mobile fixture에 @kor-travel/ui의 정확 버전·vendor 참조·해시·lock·원장을 모두 추가하면 `--profile mobile`이 exit 0이다(`MOBILE_DIRECT_DOM_UI_INSTALLED`). mobile에는 required 목록만 있고 profile별 forbidden 조건이 없다.
- 영향: tokens만 쓰는 네이티브 경계와 달리 DOM/Radix 패키지가 모바일로 들어오는 정책 위반을 자동 gate가 막지 못한다. 이 fixture가 실제 네이티브 앱 빌드 성공을 뜻하지는 않는다.
- 권고: profile별 금지 패키지/런타임 경계를 명시하고 모바일에서 DOM UI 유입을 실패시킨다. native 컴포넌트와 tokens의 허용 계약은 유지한다.

### B-P2-02 — Tabs orientation을 context로 전달하지 않는다 [부모가 사전 고지]

- 심각도: **P2**, 상태: `OPEN`
- 위치: **common `packages/ui/src/tabs.tsx:15`**, `:19`.
- 재현: 실제 packed Tabs를 `orientation="vertical"`로 renderToStaticMarkup하면 바깥 div는 `data-orientation="vertical"`인데 내부 tablist는 `aria-orientation="horizontal"`, trigger/content도 horizontal이다. props에서 orientation을 꺼낸 뒤 Primitive.Root에 전달하지 않기 때문이다.
- 영향: 표시·ARIA·키보드 방향의 계약이 어긋난다. 이번 재현은 SSR 속성 확인이며 브라우저 키 입력은 별도다.
- 권고: Root에 orientation을 전달하고 vertical DOM/ARIA와 키보드 회귀를 검증한다.

### B-P2-03 — forceMount한 비활성 TabsContent에 숨김 처리가 없다 [부모가 사전 고지]

- 심각도: **P2**, 상태: `OPEN`
- 위치: **common `packages/ui/src/tabs.tsx:86`**.
- 재현: defaultValue=a이고 a/b Content를 모두 forceMount하면 b는 `data-state="inactive"`인 채 실제 자식과 함께 렌더되고 hidden 속성·hidden 스타일·상태별 숨김 클래스가 없다. 현재 클래스는 `flex-1 text-sm outline-none`뿐이다. SSR 원문에서 active/inactive 콘텐츠가 둘 다 확인됐다.
- 영향: 상태 보존을 위해 forceMount하는 소비자는 비활성 패널도 표시하게 된다. forceMount하지 않는 기본 경로가 깨진다고 주장하지 않는다.
- 권고: 비활성 상태의 표시·접근성 계약을 정하고 실제 상태 selector로 숨김을 제공한다. 두 패널 forceMount 후 전환·포커스·접근성 검증을 추가한다.

## 원격 CI·라이선스의 확인된 정상 범위

현재 PR의 댓글·리뷰·다른 리뷰어 결과는 조회하지 않고 commit별 workflow runs/jobs/logs만 직접 읽었다.

- common head: [frontend 43022441887](https://github.com/digitie/kor-travel-common/actions/runs/43022441887), [workflow selftest 43022441756](https://github.com/digitie/kor-travel-common/actions/runs/43022441756), [python-package 43022441750](https://github.com/digitie/kor-travel-common/actions/runs/43022441750)는 성공. [docs 43022441710](https://github.com/digitie/kor-travel-common/actions/runs/43022441710)은 실패. check-versions job만 성공했으며 packages/docs/secret-scan/tools 양 OS는 실패다.
- upstream head: [Marker CI 43022446909](https://github.com/digitie/maplibre-vworld-react/actions/runs/43022446909), job130528710668의 typecheck/build/lint/기존21/Chromium17/tarball17 단계가 모두 성공이다. upstream CI를 로컬에서 다시 전부 실행한 것은 아니다. 성공 job도 GPL 동봉 누락은 검사하지 않는다.
- common ui/tokens에는 LICENSE/NOTICE/THIRD_PARTY_NOTICES가 실제 동봉된다. ui에는 SHADCN_LICENSE도 있다. shadcn MIT 전문은 [고정 원천 LICENSE.md](https://github.com/shadcn-ui/ui/blob/dd41d19e2f80ff6891951f7ced74c2c9a650b065/LICENSE.md)를 GitHub 도구로 직접 조회해 2023 shadcn 고지와 대조했다. SPDX189 성공을 별도의 포장 내용 확인으로 보완했다.
- 새 VirtualTable의 Map 원천 SHA/경로, shadcn 파일의 Origin/Derived-From/Modified, PROVENANCE 및 shadcn-sources 원장 존재를 확인했다. 금지된 pinvi/maplibre 소스를 common에 복사했다는 근거는 발견하지 않았다. 이는 모든 외부 원문과의 전수 텍스트 동일성 검증을 뜻하지 않는다.
- fresh upstream pack 결과는 수정한 ES2022 web 빌드와 manifest SHA512가 일치한다. core/web 상대 import 목표 누락을 발견하지 않았고 React19 타깃의 실제 소비 설치도 성공했다. release registry 게시·이미 배포된 동일 버전 재발행 사실은 검증하지 않았다. manifest의 CANDIDATE_NOT_RELEASED 상태를 유지한다.

## 미실행·한계·후속 gate

- 실제 Geo/Map/Pinvi 등 소비자 저장소의 adoption/이미지/운영/live/모바일 native 실행: **NOT_RUN(이번은 common/upstream 원본 1차 독립 리뷰)**. 후속 소비 앱도 같은 독립 역할로 별도 검토할 수 있으나 이번 PASS에 포함하지 않는다.
- 로컬 Windows 도구 재실행, upstream 전체 browser/RN 시험: **NOT_RUN**. 필요한 upstream 검증은 정확 SHA의 원격 job 결과로만 기록했다.
- 새 common helper 공격은 Next webpack으로 재현했다. Turbopack은 **NOT_RUN**이며 기존 필수 CI도 현재 smoke 준비에서 중단한다.
- 기존 사용자/부모 workingtree의 회귀·CI 수정: **NOT_REVIEWED**. 새 manifest delta 이후 재검토한다.
- 최초 임시 소비 설치는 WSL 루트 용량 ENOSPC로 실패했다. npm cache를 `/tmp`로 분리하고 리뷰어가 만든 upstream node_modules만 `/tmp`로 옮긴 뒤 재실행해 설치 성공을 확인했다. 이 환경 실패를 제품 finding으로 세지 않았다.

P0/P1은 수정 또는 근거 있는 반박을 새 불변 커밋에서 원 리뷰어가 재확인하기 전에는 닫히지 않는다. 네 artifact의 bytes 일치와 단위시험 성공은 위 packaging/실제 설치/서버 빌드/정책 gate 결함을 해소하지 않는다. **최종 verdict: BLOCK.**

검증 종료 뒤 두 리뷰용 detached worktree를 `git worktree remove`로 정리했다. 시작·종료 clean 증거와 tarball·로그는 별도 evidence 디렉터리에 보존했다. 기존 작업 checkout과 branch는 변경하지 않았다.
