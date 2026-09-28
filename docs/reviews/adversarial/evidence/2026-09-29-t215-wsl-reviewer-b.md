# T-215 WSL 후보 독립 리뷰 B 원본

- 실행 ID: `/root/review_wsl_ui` (새 full-access 세션).
- 전문 영역: React UI·접근성·패키징·lock·CI·라이선스·문서 정합.
- 최초 기록 시각: 2026-09-29T08:22:48+09:00. 초기 Git 읽기는 이 시각 전에 수행했으며 최초 도구 호출의 정확한 벽시계 시각은 수집하지 않았다.
- 종료 시각: 2026-09-29T08:24:08+09:00.
- 격리: WSL Ubuntu-26.04의 Git object-only. 소스·문서는 `git show dd084f1:<path>`와 `git diff afc8d1b dd084f1`로 읽었다. 이동 branch의 파일 내용을 검토 기준으로 삼지 않았다. 후보 파일을 수정하지 않았다.
- 실제 확인 candidate: `dd084f1a191f04cd17a55065c7ace734e526674a`.
- 실제 확인 tree: `c2cd2e9b5d027ed65719c9518380e47343318c65`.
- base: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`.
- manifest: `26c849b17385eee7330a5200af0f8888582ea698:docs/reviews/adversarial/evidence/2026-09-29-t215-wsl-manifest.md`.
- manifest SHA256 직접 확인: `d5be51273f9db9e46b146205fd9f11cdfd2ad9786c00948b34e73faaff470e6f`.
- 시작·종료 작업 HEAD: `26c849b17385eee7330a5200af0f8888582ea698`. 두 시점 `git status --porcelain` 출력은 비었다. HEAD의 manifest-only 추가와 제품 후보의 차이를 구분했다.
- 상대 reviewer 원본·finding은 열람하지 않았다. 과거 reviewer 원본도 이 실행에서는 열람하지 않았다.

## 전달 요청 원문

> AGENTS.md 의무 독립 적대적 리뷰 B를 수행하라. 전문영역 React UI/접근성/패키징·lock/CI/라이선스/정합. 현재 새 세션은 full-access여야 한다. WSL Ubuntu-26.04, repo /mnt/f/dev/kor-travel-common-wt/t215-main. Git은 WSL로만. immutable candidate dd084f1a191f04cd17a55065c7ace734e526674a tree c2cd2e9b5d027ed65719c9518380e47343318c65 base afc8d1bf166d0ddcbee059252eb5cee245157dcd. manifest는 commit26c849b17385eee7330a5200af0f8888582ea698:docs/reviews/adversarial/evidence/2026-09-29-t215-wsl-manifest.md, SHA256 d5be51273f9db9e46b146205fd9f11cdfd2ad9786c00948b34e73faaff470e6f. Git object-only git show/diff로 검토. AGENTS/docs README/resume/T215 task/runbook 필요 부분 읽고 immutable hash와 시작종료 clean 검증. 상대 reviewer 보고서 열람 금지. 원본 결과는 F:/dev/kor-travel-common/test-results/t215-merge/reviewer-wsl-new-b.md 에만 작성. candidate 수정금지. root는 현재 브라우저/Python 검증 수행 중. 실제 WSL 패키지 build,typecheck,UI29/token7,real tarball Next webpack+Turbopack,Next example build PASS 완료; 브라우저/Python 결과는 최종 전달 예정. 실행ID/시각/전달 요청/hash/범위/공격 시나리오/finding P0-P3/한계/verdict 포함하라. 현재 working HEAD26c849b는 manifest-only 추가이며 candidate 내용만 검토. 문제 발견 즉시 root에 알리고 최종 raw 제출.

## 범위와 공격 시나리오

54개 변경 파일 목록을 확인하고 이 역할의 제품 소스·시험·예시·빌드 설정·3개 lock·CI·공개 계약·버전·고지·task 변경을 검토했다. 기존 리뷰 원본은 독립성 유지를 위해 읽지 않았다.

- 로그인: 복수 폼의 ID 충돌, 빈 오류 alert 유지, 오류 연결, pending 상태의 CTA 포커스, 같은 틱 재제출, 콜백 예외, 비밀번호 공백 보존과 종료 후 삭제, 서버 원문 노출을 추적했다. 네이티브 required 입력과 명시 label, readOnly·aria-disabled 조합이 시험·계약과 일치한다.
- 메뉴: native nav/link/button과 disabled 항목, 아이콘·힌트 접근성 이름 제외, 최장 경로 하나의 활성 표시, 경로 경계와 query/hash 위임, 링크 adapter의 DOM·포커스 유지, 프로젝트 변경 시 상태 초기화를 검토했다. 메뉴 권한과 콜백은 소비자 책임으로 남는다.
- CSS: Tailwind 탐지 경로, 의미 토큰, 44px 최소 높이, 포커스 outline, strip/rail breakpoint, 긴 문구·좁은 화면, Concierge 어두운 rail·Geo 입력 경계를 검토했다. 정적 검토만으로 색상 대비 전체를 통과 판정하지 않는다.
- Next·배포: client 지시문 보존, 순수 함수 subpath, dist exports와 선언 파일, workspace 시각 예시와 실제 tarball fixture의 분리, CSS의 설치 dist 탐지, next/link 실제 주입, strict 설정, metadata title을 확인했다. tarball files 목록에는 소비자 예시와 아이콘 구현이 포함되지 않는다.
- lock: immutable JSON을 파싱해 root 254항목, 시각 fixture 102항목, packed fixture 103항목을 검사했다. 원격 resolved는 모두 registry.npmjs.org이고 sha512 integrity가 있다. 로컬 예외는 workspace link 또는 명시 file tarball뿐이다. 두 fixture와 root의 manifest 의존 선언이 각 lock root와 일치한다. packed UI·tokens의 integrity도 존재한다. 이 리뷰 자체가 tarball을 다시 생성해 바이트 digest를 검증한 것은 아니다.
- CI: 기존 read-only contents 권한·고정 action SHA·source SHA 확인을 유지하며 packages job이 UI build/check/examples/test, 실제 tarball install, Next webpack/Turbopack·시각 예시 빌드를 실행한다. 신규 workflow가 외부 비밀·쓰기 권한을 요구하지 않는다. 실제 CI 결과는 별도 gate다.
- 문서·고지: GPL 고지·LICENSE 동봉·자체 작성 설명, 개발 의존과 배포물 경계, 신규 API의 계약 명시, recommended만 갱신하고 floor 유지, pinned 소비자 출처와 조사일, T-201/T-214·소비자 채택 미완료 구분을 확인했다. 이전 제한 환경 실패와 현재 WSL 검증을 구분하는 기록은 완료 사실을 과장하지 않는다.

## 실행·읽은 검증과 한계

직접 실행한 것은 immutable hash/tree·manifest SHA256·시작종료 clean·candidate diff 공백 검사와 JSON lock 검토다. 모든 최종 검사는 통과했다. 첫 PowerShell lock 파싱은 빈 키 때문에 실패했고 `-AsHashtable`로 다시 실행했다. 첫 manifest 비교는 의존 그룹 부재의 null 예외가 있어 키 존재 조건을 추가한 검토 명령으로 재실행했으며 제품 변경은 없었다.

부모로부터 WSL build/typecheck/UI 29개·tokens 7개, 실제 tarball Next 두 빌드, 시각 예시 빌드 성공을 전달받았다. 이후 최신 React 19.3/Next 16.3.6의 6개 테마 메뉴 수·순서, 키보드 포커스, axe, 로그인 상태·비밀번호 초기화·재시도, 320/390/768/1024/1440 폭, 공통 dark, 실제 packed Next Link 검증 exit 0도 전달받았다. 이는 부모 실행 evidence이며 reviewer가 직접 실행한 결과로 세지 않는다.

`NOT_RUN(리뷰 격리상 빌드·브라우저 직접 실행 없음)`. 실제 소비자 리모트 내용을 이 실행에서 다시 조회하지 않았고, 고정 출처·설정 데이터의 정합성을 확인했다. 스크린리더 수동 평가·실제 인증 서버·소비자 채택·배포·registry 발행은 범위 밖이다. 전체 Python 회귀와 필수 GitHub CI는 원본 확정 시점에 미완료이며 merge 담당자가 별도로 닫아야 한다.

## Finding과 판정

신규 P0·P1·P2·P3 finding 없음. 검토한 코드·계약·패키징에 수정 요구 없음.

코드 리뷰 판정: PASS.

Merge verdict: CONDITIONAL. 조건은 현재 진행 중인 전체 Python 회귀·필수 CI 및 다른 독립 reviewer gate가 통과하고 최종 evidence가 보존되는 것이다. 조건 충족 전 merge를 허용하는 판정이 아니다. 코드 수정이 없다면 이 검증 결과 기록은 closure artifact로 보존할 수 있다. 제품 코드·계약·CI 수정이 생기면 새 immutable 기준선의 재검토가 필요하다.
