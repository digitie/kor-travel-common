# T-217 로그인 폼 hydration 준비 경계

- 상태: IN_PROGRESS
- 우선순위: P1
- Gate: SSR·hydration 경계 회귀, 기존 UI 전체 단위·타입·빌드, 정규 pack·설치, 독립 2인 리뷰·CI
- 선행: T-215
- 외부 선행: Transport 별도 채택 PR의 정확 tarball·lock·빌드 및 Root 소유 공개 UI 재검증

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

설계만 준비됐으며 구현·패키지 검증·리뷰·소비자 채택은 아직 NOT_RUN이다.
원본 checkout의 미커밋 변경과 기존 CPU/Manager 소비자 PR은 수정하지 않는다.
Common 변경은 이 task의 commit revert, 소비자는 새 tarball 채택 PR revert로 원복한다.
