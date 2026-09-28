# T-215 WSL 검증 후보 리뷰 manifest

- 종류: full, 공개 UI API·CSS·버전·CI 변경.
- 기준 commit: `dd084f1a191f04cd17a55065c7ace734e526674a`.
- 기준 tree: `c2cd2e9b5d027ed65719c9518380e47343318c65`.
- parent/base: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`.
- 요청: 로그인·메뉴 공용 부품, 최신 React/Next, 6개 실제 리모트 메뉴·색상 예시, 검증 후 PR 머지.
- 범위: 기준 base→commit의 54개 파일 전체. UI·토큰 소비·인증 상태/라우트 방어·접근성·예시·tarball Next fixture·3개 lockfile·CI·계약/버전 문서.
- 범위 밖: T-301/OpenAPI, 소비자 코드 수정·인증 서버·배포·registry 게시.
- 정본: AGENTS, architecture/packages, standards/ui-contract, 상세 T-215, agent-workflow §5.
- 격리: Git object-only. WSL git show·diff·cat-file로 지정 commit만 읽는다. 시작/종료에 실제 commit/tree와 작업 트리 상태를 기록하며 타 reviewer 결과를 보지 않는다.
- 확인된 로컬 검증: WSL root 설치·lock 생성·build/check/예시 타입, tokens 7개·UI 29개 단위 시험, tarball Next webpack/Turbopack 및 예시 Turbopack 빌드. 최종 title 보완 빌드·실제 브라우저·Python 전체 회귀·CI는 부모가 마무리하며 별도 evidence로 보존한다.
- 가능한 재현: npm ci; npm run build; npm run check; npm test; examples/README의 tarball·Next 명령. object-only reviewer가 직접 실행하지 않은 검증은 NOT_RUN으로 구분한다.
- 원본 출력: reviewer A/B별 실행 ID·시각·전문 분야·관찰 hash·finding(P0~P3)·재현·권고·verdict를 별도 evidence에 보존한다.
