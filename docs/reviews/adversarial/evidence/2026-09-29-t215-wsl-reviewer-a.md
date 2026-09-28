# T-215 WSL 독립 적대적 리뷰 A 원본

- 실행 ID: `/root/review_wsl_security`.
- 전문 영역: 로그인 보안, redirect 경계, 비동기 상태, 공개 API 계약.
- 시각: 2026-09-29 08:21:42+09:00 최초 명시적 clock 확인(이전 기준선·문서 읽기 포함), 08:23:08+09:00 종료 확인.
- 종류: full 독립 리뷰의 보안·계약 담당.
- 코드 리뷰 verdict: **PASS**. 신규 P0/P1/P2/P3 finding 0건.
- 별도 merge gate: 전체 Python 회귀와 원격 CI는 이 원본 확정 당시 진행 전/중이므로 아직 merge 승인으로 계산하지 않는다. 두 리뷰 및 필수 검증을 확인하는 최종 merge 담당 판정이 필요하다.

## 전달받은 요청 원문

> AGENTS.md 의무 독립 적대적 리뷰 A를 수행하라. 전문영역 로그인 보안/redirect/비동기 상태/API 계약. 현재 새 세션은 full-access여야 한다. WSL Ubuntu-26.04, repo /mnt/f/dev/kor-travel-common-wt/t215-main. Git은 WSL로만. immutable candidate dd084f1a191f04cd17a55065c7ace734e526674a tree c2cd2e9b5d027ed65719c9518380e47343318c65 base afc8d1bf166d0ddcbee059252eb5cee245157dcd. manifest는 commit26c849b17385eee7330a5200af0f8888582ea698:docs/reviews/adversarial/evidence/2026-09-29-t215-wsl-manifest.md, SHA256 d5be51273f9db9e46b146205fd9f11cdfd2ad9786c00948b34e73faaff470e6f. Git object-only git show/diff로 검토. AGENTS/docs README/resume/T215 task/runbook 필요 부분 읽고 immutable hash와 시작종료 clean 검증. 상대 reviewer 보고서 열람 금지. 원본 결과는 F:/dev/kor-travel-common/test-results/t215-merge/reviewer-wsl-new-a.md 에만 작성. candidate 수정금지. root는 현재 브라우저/Python 검증 수행 중. 실제 WSL 패키지 build,typecheck,UI29/token7,real tarball Next webpack+Turbopack,Next example build PASS 완료; 브라우저/Python 결과는 최종 전달 예정. 실행ID/시각/전달 요청/hash/범위/공격 시나리오/finding P0-P3/한계/verdict 포함하라. 현재 working HEAD26c849b는 manifest-only 추가이며 candidate 내용만 검토. 문제 발견 즉시 root에 알리고 최종 raw 제출.

## 기준선과 격리

- manifest commit: `26c849b17385eee7330a5200af0f8888582ea698`.
- manifest SHA256: `d5be51273f9db9e46b146205fd9f11cdfd2ad9786c00948b34e73faaff470e6f`, Git blob을 `sha256sum`으로 직접 확인했다.
- 실제 검토 candidate: `dd084f1a191f04cd17a55065c7ace734e526674a`.
- 실제 tree: `c2cd2e9b5d027ed65719c9518380e47343318c65`.
- base: `afc8d1bf166d0ddcbee059252eb5cee245157dcd`.
- Git object-only: 변경 소스와 문서는 지정 commit의 `git show`/`git diff`로 읽었다. source worktree 파일을 기준선 대용으로 읽지 않았다.
- 시작·종료 HEAD는 manifest-only commit `26c849b17385eee7330a5200af0f8888582ea698`이며 두 번의 `git status --porcelain=v1` 출력은 모두 비었다. candidate와 tree는 종료에 재확인했다.
- 새 reviewer의 WSL 실행은 성공했다. 이전 agent 권한 실패를 이 실행의 제한으로 계승하지 않는다.
- 현재 상대 reviewer의 finding·원본 보고서는 열람하지 않았다. 필수 review archive 인덱스는 절차 확인 용도로 읽었다.

## 읽은 범위

AGENTS, docs/README, docs/resume, T-215 task, agent-workflow, review archive 규칙, manifest를 읽었다. base→candidate 전체 파일 목록을 확인하고 `packages/ui/src/*`, 계약·navigation·preview 시험, Preview, packed Next page, UI README·examples README, 공개 exports·build 검사·tsconfig·NOTICE, UI 계약/architecture/CHANGELOG, root script·versions·CI delta를 검토했다. lockfile 전체 설치 graph와 CSS 대비 세부 감사는 다른 전문 영역이며 이 원본에서 독립 재실행을 주장하지 않는다. 소비자 구현·T-301·실제 인증 서버·배포는 범위 밖이다.

## 공격 시나리오와 관찰

1. 외부 URL, protocol-relative, 역슬래시, 대소문자 %2f/%5c, 중첩 %25, 제어문자와 URL dot-segment 정규화 뒤 `//`가 드러나는 redirect를 추적했다. 입력 정규식과 URL 정규화 뒤 origin/path 검사로 실패 경로는 `/`가 된다. URL query/hash는 안전한 로컬 경로에서만 유지한다.
2. React state 반영 전 같은 틱에 두 submit가 들어오는 경우를 검토했다. ref를 콜백 전에 설정하므로 두 번째 호출은 차단된다. 외부 pending도 차단하고 native disabled 대신 aria-disabled로 CTA 포커스를 유지한다. 콜백이 Promise를 반환해야 한다는 사용 계약이 문서에 명시돼 있다.
3. 동기 throw·Promise reject·onClearError의 submit 경로 예외를 검토했다. 일반 한국어 문구만 렌더링하고 원문을 출력·로그하지 않는다. finally에서 password DOM 값을 지우고 inFlight와 상태를 해제한다. 비밀번호는 trim하지 않고 username만 trim한다. 저장소·네트워크·URL 전송 구현은 없다.
4. 서버 원문 오류 또는 사용자 label의 HTML 삽입을 확인했다. React text node로 렌더링하며 dangerouslySetInnerHTML을 사용하지 않는다. 외부 error는 소비자가 안전한 문구를 제공한다는 책임이 명시돼 있다.
5. `/jobs`와 `/jobsite`, 가장 긴 하위 경로, exact, query/hash 항목, disabled 링크와 명시적 activeItemId를 검토했다. 자동 활성화는 경계가 맞는 링크 하나이며 query/hash 상태는 소비자 주입이다. disabled 링크는 href 없는 span이고 권한 필터가 서버 권한 검증을 대체하지 않음을 README에서 구분한다.
6. Next client callback 경계와 navigation 순수 subpath를 검토했다. UI export는 client 지시문, 순수 함수는 별도 subpath이며 공개 API로 tarball fixture가 연결된다. 예시에서는 인증 성공을 실제 세션으로 표시하지 않는다.
7. 예시 링크 component가 렌더마다 새 component가 되는지, 프로젝트 변경 후 이전 상태가 남는지 확인했다. module-level PreviewLink와 keyed ProjectPreview 및 관련 계약 시험이 해당 회귀를 막는다.

## 실행 및 읽은 evidence

### 이 reviewer가 직접 실행

- candidate `navigation.ts` Git blob을 Node 22의 `--experimental-strip-types --input-type=module-typescript` stdin으로 실행했다. 추적 파일을 만들거나 빌드하지 않았다.
- 공격 경로 17개가 `/`인지 assert했다: 외부/protocol-relative/역슬래시/대소문자 encoding/중첩 encoding/CRLF/dot-segment/공백·탭·개행/JavaScript scheme/인코딩 query 경계.
- 안전 경로 5개의 반환 origin이 `https://local.invalid`인지 assert하고 `/a/../b`가 `/b`로 정규화되는지 확인했다.
- route 경계·exact·최장 항목 assertion 3개를 실행했다.
- 결과: exit 0, `{"attackCases":17,"safeCases":5,"routeAssertions":3,"result":"PASS"}`.

### 부모 실행 evidence를 읽거나 전달받은 항목

- `test-results/ui-preview/browser-evidence.json`을 직접 읽었다. 런타임 React 19.3.0·Next 16.3.6, 6개 메뉴 20/8/7/15/12/9개 및 순서·포커스·axe·로그인 재시도 PASS, 각 320/390/768/1024/1440px, packed Next Link/login/common dark axe PASS, errors 빈 배열을 확인했다. 브라우저를 이 reviewer가 재실행했다고 주장하지 않는다.
- root build·typecheck·UI 29개·tokens 7개·실제 tarball Next webpack/Turbopack 및 시각 Next build PASS는 manifest와 부모 전달 결과다. 독립 실행 아님.
- 전체 Python 회귀: NOT_RUN(이 reviewer 독립 실행), 부모 실행 진행 중. 원격 CI: NOT_RUN(PR 생성 전). 통과로 집계하지 않는다.

## 한계와 최종 판정

코드·계약의 신규 finding은 없다. **코드 리뷰 PASS**이며 전체 Python 회귀와 필수 원격 CI의 최종 성공을 확인한 뒤 merge해야 한다. 소비자 저장소 build/e2e·실제 인증/권한/세션·배포·게시 검증은 이 common 개발 후보의 검증으로 대체하지 않는다. 라이브 서비스 인증 보안이나 전체 접근성의 완전한 보증은 아니다.