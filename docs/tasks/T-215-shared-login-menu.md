# T-215 공용 로그인·탐색 메뉴 구현

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: 타입·단위·접근성·tarball·Next 빌드·2인 적대적 리뷰
- 선행: 없음
- 외부 선행: Linux/Node 정본 환경, 의존 설치, Git 쓰기, 소비자 채택 PR

## 목표

2026-09-29 사용자 요청에 따라 map·weather·concierge·geo·transport·docker-manager에서 사용할 로그인과 탐색 메뉴를 먼저 구현한다. 기존 T-201·T-214의 전체 선행 작업을 완료 처리하지 않고, 요청된 native 컴포넌트에 필요한 최소 패키지 기반만 만든다. T-214의 정식 로그인 gate는 그대로 남는다.

## 고정 결정

[ADR-015](../adr/015-common-shared-systems-scope.md)의 주입형 로그인 경계와 [UI 계약](../standards/ui-contract.md)을 따른다. 앱 셸·권한·라우트 구성은 앱 소유이며 메뉴는 전달된 항목을 표시하는 부품이다. [조사](../survey/cross/ux-patterns.md) §1.2·§1.8의 다중 소비자 링크/동작 메뉴와 로그인 상태 반복이 근거다. transport는 이번 요청의 대상이며 과거 7개 소비자 조사·채택 완료 수에 포함하지 않는다.

최신 안정 React·Next 기준 요청에 따라 `versions.json`의 recommended만 공식 registry 조회일과 함께 갱신한다. peer React 19 호환 범위는 유지한다. 최신 버전 설치·실행 여부와 기준 버전 확인을 구분한다.

## 구현 범위

- ESM·선언 파일·클라이언트 지시문 보존, 로그인/메뉴/순수 함수 subpath.
- `LoginForm`, `LoginError`, `LoginStatus`, `sanitizeLocalPath`, 한국어 오류 매핑.
- `AppMenu`: 그룹·링크·동작 버튼·활성 항목·반응형 strip/rail, 라우터 링크 주입.
- 사용 예와 App Router fixture, 계약·접근성 시험.

## 범위 밖

인증 서버·세션 저장소·네트워크 호출·앱 권한 필터·전체 셸·소비자 수정·게시·T-201 전체 프리미티브 기반 구현.

## 예상 변경 파일

`packages/ui/`, `package.json`, `package-lock.json`, `versions.json`, UI 계약·패키지 문서, CHANGELOG.

## 수용 기준

- 비밀번호를 저장·로그·URL 전달하지 않고 비동기 제출 중 중복 호출을 막는다. CTA는 탭 순서와 포커스를 유지한다.
- label/입력 연결, 항상 존재하는 오류 alert, pending/실패/재시도 상태를 시험한다.
- 외부·protocol-relative·역슬래시·제어문자 이동 경로를 `/`로 치환한다.
- 메뉴는 native nav/link/button이고 권한 정책을 내장하지 않는다. 경계가 맞는 가장 긴 경로 하나만 활성화한다. hash 라우터는 `activeItemId`로 주입한다.
- 320px·PC·다크·키보드 동작, tarball 설치와 최신 Next의 webpack/Turbopack 빌드를 검증한다.
- 두 독립 reviewer가 같은 고정 기준선에서 재검토한다. 미실행 gate가 있으면 DONE/릴리스 가능으로 표시하지 않는다.

## 검증 명령

```bash
npm run build -w packages/ui
npm run check -w packages/ui
npm test -w packages/ui
npm pack -w packages/ui
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

## WSL 검증 후보의 현재 상태

2026-09-29 로컬 권한 변경 후 Ubuntu-26.04에서 npm 네트워크·Git 쓰기가 정상화됐다. 원격 main 기준 독립 브랜치로 UI 변경만 분리했으며 T-301 작업은 포함하지 않았다. 아래 최초 제한 환경 기록은 당시의 이력이며 현재 판정은 이 절과 후속 immutable commit 리뷰를 따른다.

- Node 22.22.2·npm 11.19.1에서 최신 React·Next 의존성을 실제 설치하고 root·예시·tarball fixture lockfile을 생성했다.
- root `npm run build`, `npm run check`, UI 예시 타입 검사 통과. tokens 7개·UI 29개 단위 시험이 통과했다.
- 실제 tarball 설치 fixture의 webpack·Turbopack 빌드와 시각 예시의 Turbopack 빌드를 통과했다. 문서 title 보완 후 최종 빌드·브라우저 검증은 진행 중이다.
- 실제 빌드에서 발견한 시각 예시 source `.js` 경로·Tailwind 해석 실패를 수정했다. 예시는 공통 UI의 공개 export를 소비하고 공통 패키지 개발 의존에 Tailwind를 명시한다.
- CI packages job에 UI 빌드·타입·단위·tarball 설치와 두 Next 빌드 방식·시각 예시 빌드를 추가했다. 생성 next-env는 ignore하며 예시 tsconfig는 strict·noUncheckedIndexedAccess로 고정했다.
- 소비자 저장소 수정·배포·npm 게시는 범위 밖이다. 실제 소비자 이관 build/e2e는 후속 채택 task의 외부 선행이며 이 개발 후보의 common 검증과 구분한다.
- 최종 immutable commit 2인 리뷰·CI 확인 전 머지하지 않는다. 후속 검증 결과는 이 절에 기록한다.

## 최초 제한 환경 evidence

2026-09-29 구현·시각 예시와 Windows 보조 검증을 수행했다. 소비자 리모트 `main`의 고정 SHA·파일 출처는 [예시 README](../../packages/ui/examples/README.md)에 기록했다. common 리모트 `main`은 `afc8d1bf166d0ddcbee059252eb5cee245157dcd`이며 현재 HEAD `802e68e`의 조상임을 확인했다. 기존 T-301 변경 3개는 보존했다.

| 검증 | 결과·한계 |
|---|---|
| TypeScript 소스·예시, ESM client 지시문·고지 | PASS, 캐시 TypeScript로 실행 |
| 6개 브라우저 예시 | PASS: 메뉴 20/8/7/15/12/9개 순서, 로그인 pending·오류·재시도·성공 안내, 키보드 링크 포커스, 320/390/768/1024/1440px overflow |
| 접근성 보조 검사 | PASS: 6개 테마 axe WCAG A/AA, 입력 경계 대비 3.54/3.54/5.08/5.36/3.54/6.03:1. 모든 접근성을 보증하지 않음 |
| tarball | PASS: UI 19개 파일, tokens 19개 파일 생성·오프라인 실제 설치·공개 export·React SSR·navigation subpath |
| 문서 link·plan, diff 공백 | PASS |
| SPDX | PASS: 추적 파일+새 UI 파일만 복사한 후보에서 93개 검사. ignored 원천/번들 포함 전체 작업 디렉터리 검사는 실패하여 후보 범위로 구분 |
| Python 도구 회귀 | 373개 실행 중 370 성공, 1 실패, 2 skip. 실패는 기존 tarball 설치 테스트의 Windows npm 임시 cache mkdir EPERM. 전체 PASS 아님 |
| Vitest 계약 시험 | NOT_RUN: Windows native binding 누락, 보조 캐시 사용 시 Vite 임시 디렉터리 EPERM. 시험 파일은 작성했으나 성공으로 집계하지 않음 |
| 최신 React/Next 빌드·다크 테마·소비자 채택 | NOT_RUN: 최신 의존 설치/정본 환경 및 소비자 이관 task 필요 |
| root lockfile | NOT_RUN: registry EACCES로 새 workspace 의존 graph를 갱신하지 못함. `npm ci` 사용 전 연결된 환경에서 `npm install` 및 lock 검토 필요 |
| 2인 리뷰 | 고정 파일 SHA256 스냅샷 보조 리뷰 수행. Git 쓰기 제한으로 정식 immutable commit 리뷰·PR은 NOT_RUN |

촬영은 캐시 React 19.2.8 및 webpack/Tailwind 브라우저 번들이다. 최신 기준은 versions.json과 fixture에 선언했으나 최신 Next 런타임 촬영/빌드로 주장하지 않는다. 로컬 산출물은 `test-results/ui-preview/gallery.html`, `overview.png`, `screenshots/`의 PC 로그인·메뉴·모바일 18장, `browser-evidence.json`이다. tarball과 설치 검사는 `test-results/ui-pack/`, `test-results/ui-install/`에 보존한다. 이들은 배포 산출물이 아니다.

Git branch 생성은 `.git` 쓰기 권한 거부, npm registry 접근은 EACCES, WSL은 E_ACCESSDENIED다. CodeGraph 대신 rg·타입·브라우저 검증을 사용했다. 이 환경에서 commit·push·소비자 수정·배포는 수행하지 않았다.

[2인 보조 리뷰 원본과 통합 판정](../reviews/adversarial/2026-09-29-t215.md)을 보존했다. 최종 delta 신규 finding은 없으나 두 merge verdict는 BLOCK이다.

## 머지 요청 후 재검증

2026-09-29 사용자 머지·재검증·WSL 실행 요청을 순서대로 확인했다.

- 리모트 `main`은 기존 `afc8d1bf166d0ddcbee059252eb5cee245157dcd`이며, 열린 PR #22는 별도 T-301 작업이다. 이를 변경하거나 머지하지 않았다.
- `test-results/t215-merge/candidate/`에 main 기준 UI 변경 47개 파일만 분리했다. manifest SHA256은 `0a27b7b7ea2f0022f389ba51e62b197645fd0c8ad0d2742d6107acb25ad3da69`다. 두 reviewer가 제품 코드 동일성과 시험의 변수명·상수 추출에 따른 동작 보존을 확인했고, B는 main 대비 task·CHANGELOG에서 T-301 변경 제외도 독립 확인했다. 정식 commit 리뷰로 집계하지 않는다.
- 문서 555개·링크 2607개, plan 107개, 분리 후보 SPDX 91개, 원 작업 트리 비밀·운영값 검사 각 737개·발견 0건, diff 공백 검사를 다시 통과했다. 비밀 검사에서 테스트 DOM 변수와 더미 입력 표현 2건을 오탐하여 변수명·상수 표현만 정리했고 assertion은 유지했다.
- 캐시 TypeScript 직접 실행으로 UI·예시 타입과 client 지시문 검사를 다시 통과했다. 정규 `npm run build`는 미설치 `.bin/tsc` 때문에 실패했다. 직접 실행 결과를 정규 설치 성공으로 집계하지 않는다.
- 브라우저 6개 프로젝트의 메뉴 순서·포커스·로그인·axe·입력 경계 대비·화면 폭 검사를 다시 통과했다. 캐시 React 19.2.8 보조 검증이다.
- 새 tarball을 실제 오프라인 설치하고 export·SSR을 재검증했다. UI SHA256 `f7c4e525a477c201a40893ee490091d669a4873f77978cd80f81ee0fa9be823d`, tokens SHA256 `9fbb20bd46eabef939cda0148e1d9c82c82e0a0430f0287d9f10efbf936ebecb`.
- npm registry 재조회는 EACCES, Vitest는 Windows native binding 누락으로 재실행 실패했다. 최신 버전 설치·lockfile·단위·Next 빌드 gate는 여전히 미완료다.
- WSL 전환 요청 후 `wsl.exe --list --quiet`가 `Wsl/EnumerateDistros/Service/E_ACCESSDENIED`로 exit 1을 반환했다. 배포판 조회 단계에서 거부되어 Linux 검증 명령은 실행하지 못했다. 진행 중이던 Windows 전체 Python 재검증은 WSL 전환 요청에 따라 중단했으며 새 PASS 수치로 집계하지 않는다. 이전 373개 결과는 위 표 그대로 유지한다.
- GitHub 후보 tree 생성도 도구가 승인을 요구하여 `approval_policy=never`로 거부됐다. 원격 tree·commit·branch·PR 생성 성공을 확인한 것이 없으며 머지는 수행하지 않았다. 승인 우회·main 직접 push를 하지 않는다.

## rollback 또는 release 차단 조건

새 UI 패키지와 연결 문서 변경을 되돌린다. 미완료 선행 작업·lockfile·정본 환경 빌드·소비자 채택·immutable commit 리뷰를 통과하기 전 릴리스하지 않는다.
