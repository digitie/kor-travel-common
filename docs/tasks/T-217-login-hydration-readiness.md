# T-217 로그인 폼 hydration 준비 경계

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: SSR·hydration 경계 회귀, 기존 UI 전체 단위·타입·빌드, 정규 pack·설치, 독립 2인 리뷰·CI
- 선행: T-215
- 외부 선행: Transport 후보의 정확 tarball·lock·빌드와 HTTP UI32는 수용했으며, 소비자 소유 공개 TLS·운영 배포 검증은 남는다.

## 관측과 범위

Transport 공개 UI의 로그인 단계에서 차단된 요청이 실제 `POST /login`으로 분류됐다.
기존 공통 폼은 `method="post"`이고 action이 없으며 client submit의 첫 문장에서 기본 제출을 막는다.
서버 렌더 결과에는 그 handler가 준비되기 전에도 활성 입력과 제출 버튼이 존재한다.
요청의 경로는 확인됐지만 hydration 지연의 상세 원인·모든 기존 실패의 단일 원인은 확정하지 않는다.

## 최소 계약

- 서버 렌더와 최초 client 렌더에서 로그인 입력 두 개와 제출 버튼을 native disabled로 제공한다.
- 동일 컴포넌트의 client effect가 실행된 뒤에만 준비 상태를 열고 입력과 버튼을 활성화한다.
- client handler의 기본 제출 차단은 첫 문장으로 유지하며 준비 전 callback도 거부한다.
- 준비 후 기존 pending의 readOnly·aria-disabled·포커스 유지, 중복 제출 차단·오류·재시도·비밀번호 지우기를 그대로 보존한다.
- 공개 props·기본값·data-slot·testid·네트워크 책임을 변경하지 않는다. 인증 서버·운영 계정은 소비자 소유다.

## 검증과 채택 순서

1. SSR DOM에서 hydration을 지연한 click·Enter가 native submit을 만들지 않는 반례를 먼저 고정한다.
2. hydrate 후 실제 callback 1회, async pending·실패 재시도·복수 폼/StrictMode를 검증한다.
3. 기존 전체 UI·타입·정규 빌드와 pack 설치에서 SSR disabled 출력을 재검산한다.
4. 새 UI 개발 버전으로만 pack하고 기존 버전 tgz를 덮어쓰지 않는다. Transport 별도 branch/PR에 파일·lock·무결성과 source를 고정한다.
5. 독립 2인 source 리뷰·정확 CI와 소비자 공개 UI는 각각 별도 gate다. Root만 실제 공개 UI를 실행한다.

## 현재 상태와 rollback

개발 후보 dev.9의 최소 제품과 3개 SSR/hydration 회귀를 구현했다. 기존 UI 단위는 전부 보존했다.

- 초기 2개 경계 회귀는 수정 전 2 FAIL, 수정 후 2 PASS였다. layout commit 뒤 passive effect 전 callback 차단을 더한 최종 전체는 UI 79 PASS·tokens 7 PASS다.
- `npm run build`·`npm run check`는 PASS이며 Node 22.22.2/npm 11.19.1·잠긴 npm 의존을 사용했다. Python 도구 회귀는 337개 중 336 PASS·기존 1 SKIP(73.860초)다.
- 정규 `npm pack -w packages/ui`의 dev.9 산출물은 27파일·SHA256 `b738d8824e36eb6e58d8cc6b78af7dc31233b6763248d634286044def795b403`이다. tokens 원산출물과 함께 임시 디렉터리에 실제 오프라인 설치하고 ESM import/SSR disabled 3개·callback 0을 확인했다.
- pack metadata parser는 prepack stdout 때문에 처음 실패했고, 설치 probe는 import-only ESM 패키지에 CommonJS resolve를 써 처음 실패했다. 제품·산출물을 바꾸지 않고 원파일 보존 뒤 실제 tgz metadata/ESM resolver로 정정했다.
- 원 f0b60bb CI는 tools 양 OS·secret-scan의 시험 예시 패턴 3실패와 smoke dev.8 누락 1실패였다. 원문 보존 뒤 검사기/단언 완화 없이 시험 식별자·상수와 후보 파일명만 정렬했다. 제품·산출물은 같다.
- JSDOM 회귀는 브라우저·Next event replay·실제 공개 UI 수용을 대체하지 않는다. 후속 Common47 병합·정확 CI8·J/W 독립 두 리뷰 및 Transport6913 후보 HTTP UI32를 수용했다. [최종 정산](../reports/2026-10-27-common47-consumer-ui-closure.md)에 동일 성공 빌드 복제 재실행·원 실패와 한계를 보존한다. 공개 TLS·운영 배포·운영 CPU/RSS는 미수용이므로 IN_PROGRESS를 유지한다.
원본 checkout의 미커밋 변경과 기존 CPU/Manager 소비자 PR은 수정하지 않는다.
Common 변경은 이 task의 commit revert, 소비자는 새 tarball 채택 PR revert로 원복한다.
