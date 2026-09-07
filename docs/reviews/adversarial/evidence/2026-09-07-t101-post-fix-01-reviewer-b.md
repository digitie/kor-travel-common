# T-101 post-fix 독립 적대적 리뷰 B 원본

- 실행 ID: `reviewer_b-t101-post-fix-4c33a5d-20260907-221537`
- 최종 판정: **PASS**. 기존 B finding 4건 모두 FIXED. 신규 P0/P1/P2/P3 finding 0건.
- 판정 범위: 아래 immutable 후보의 수정과 회귀. T-101 전체 완료·외부 발행·소비자 채택을 승인했다는 뜻은 아니다. 미실행 gate는 마지막 절에 분리한다.
- 시작 KST: `2026-09-07T22:15:37.1163204+09:00`
- 종료 검증 KST: `2026-09-07T22:19:45.4884780+09:00`
- 시작/종료 SHA: `4c33a5d951e32df0c2170b7a865f324d122dbe05`
- 시작/종료 tree: `aa81767746cb40641e43397af19082456aaacb3b`
- post-fix delta base: `f8894e293ca9677f457011197052cd55dbdc9696`
- 최초 구현 base: `cf2c610cecfa7a9b8f7a035c9529d7a296e27527`
- 격리: `F:/dev/kor-travel-common-wt/review-t101-post-b`를 후보에서 새 detached worktree로 생성. 시작·종료 `git status --porcelain=v1` 출력 없음.
- source `.git/config` 시작·종료 SHA256: `C06BFC225BFA7EBBF45777AF3B21E8DC7E69DD5011C07863B54B2EC6B4B3C0B9`. `core.worktree`를 변경하지 않았다.
- 독립성: reviewer A의 원본·새 결과를 읽거나 요청·공유하지 않았다. 후보 소스·문서·시험을 수정하지 않았고 commit/push하지 않았다. npm 빌드·설치·주입은 후보를 읽어 만든 임시 사본에서 실행했다. 소비자 저장소 쓰기·registry 게시 없음.

## 요청 원문

> Post-fix 적대 리뷰를 시작해 주세요. 새 immutable candidate SHA `4c33a5d951e32df0c2170b7a865f324d122dbe05`만 detached 기준으로 검토하고 수정·commit·push하지 마세요. 초기 B의 BLOCK finding이 실제로 닫혔는지 CI source SHA·build 전 drift·tarball/exports·GPL/PROVENANCE/redaction·Windows/Linux·pure CSS hairline·scoped 다크 상속·T-102 flat path 인계를 독립 재현하세요. 양 OS pack/install와 정적 gate를 SHA에 귀속해 확인하고 P0–P3 disposition/verdict를 원본 보고서와 최종 메시지로 남겨 주세요. reviewer A 결과는 읽거나 공유하지 마세요.

## 범위와 검증 명령

17파일 delta의 코드·CSS·시험·정본 문서를 읽었다. 생성물 변경은 generator 전체와 후보 JSON의 공식 스키마 검증, 7개 출력의 drift 검사, pack 후 ESM import 및 subpath resolve로 대조했다. 변경 없는 package metadata/lock/NOTICE/LICENSE/THIRD_PARTY_NOTICES/PROVENANCE/정본 tokens.css/versions.json은 `git diff --name-only` 결과가 비어 있음을 확인하여 최초 원천·고지 검증을 재사용했다. docs/README·resume·T-101과 T-102 및 관련 architecture/standards를 확인했다.

후보 밖 `.git/codex-audit/`에 다음 독립 보조 파일을 보존했다.

| 보조 파일 | 검증 |
|---|---|
| `review-t101-b-pack.py` | 임시 사본 ci/check/build/test/pack/별도 설치·exports·LICENSE |
| `review-t101-post-b-drift.py` | 생성물 7개 각각 주입 후 현재 workflow의 build 전 check가 실패하며 주입 내용을 보존하는지 확인 |
| `review-t101-b-css.cjs` | 최초 CSS 반례를 후보에서 그대로 재실행 |
| `review-t101-post-b-css.cjs` | light/class-dark/media-dark × base/scoped 6조합의 실제 Chromium computed style과 surface containment |
| `review-t101-post-b-gates.py` | plan/link/SPDX/secret/redaction/self-check/diff를 양 OS에서 실행 |
| `review-t101-post-b-dtcg.py` | 후보 tokens.json을 직접 조회한 공식 2025.10 DTCG schema로 검증 |

```text
git worktree add --detach F:/dev/kor-travel-common-wt/review-t101-post-b 4c33a5d951e32df0c2170b7a865f324d122dbe05
git diff f8894e293ca9677f457011197052cd55dbdc9696 HEAD -- <17개 변경 파일>
py -3.14 -B -X utf8 .git/codex-audit/review-t101-b-pack.py F:/dev/kor-travel-common-wt/review-t101-post-b
py -3.14 -B -X utf8 .git/codex-audit/review-t101-post-b-drift.py F:/dev/kor-travel-common-wt/review-t101-post-b
py -3.14 -B -X utf8 .git/codex-audit/review-t101-post-b-gates.py F:/dev/kor-travel-common-wt/review-t101-post-b
node .git/codex-audit/review-t101-b-css.cjs F:/dev/kor-travel-common-wt/review-t101-post-b
node .git/codex-audit/review-t101-post-b-css.cjs F:/dev/kor-travel-common-wt/review-t101-post-b
py -3.14 -B -X utf8 .git/codex-audit/review-t101-post-b-dtcg.py F:/dev/kor-travel-common-wt/review-t101-post-b
gh run list --commit 4c33a5d951e32df0c2170b7a865f324d122dbe05 --json databaseId,event,headSha,status,conclusion
gh pr view 11 --json headRefOid,isDraft,state,baseRefName,url
gh run view 34126309766 --json jobs
gh run view 34126309766 --job 101755695147 --log
git diff --check f8894e293ca9677f457011197052cd55dbdc9696 HEAD
git rev-parse HEAD
git rev-parse 'HEAD^{tree}'
git status --porcelain=v1
```

WSL은 `wsl -d Ubuntu-26.04 -- bash -lc '<명령>'`에서 `/home/digitie/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11 -B -X utf8`로 pack/drift/gates 보조 파일을 실행했다. 인수 경로는 `/mnt/f/dev/...`다. 정적 검사 helper의 Git 환경은 process 범위 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t101-post-b`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t101-post-b`다. `/root/...` Python 설치 경로 탐색은 권한 오류가 나 `uv python find 3.11`로 실제 경로를 얻었다. 이 탐색 실패는 시험 실패나 성공으로 집계하지 않았다.

pack helper의 실제 npm 명령은 `npm ci --ignore-scripts --no-audit --no-fund`, `npm run check`, `npm run build`, `npm run check`, `npm test`, `npm pack --workspace packages/tokens --pack-destination <임시 경로> --json`, 별도 임시 설치 프로젝트의 `npm install --ignore-scripts --no-audit --no-fund <tarball 경로>`다. helper 끝에 남은 이전 build→check→test 주입 순서의 성공은 현재 수정 workflow 결과로 집계하지 않았다. 현재 workflow 반례는 새 drift helper의 build 전 check 7건으로 검증했다.

## 기존 finding disposition

| 원 ID·심각도 | 판정 | 후보 위치·독립 재현 결과 |
|---|---|---|
| B-P2-01, P2 | **FIXED** | `.github/workflows/docs.yml:183–187`에 build 전 check와 재생성 뒤 git diff가 존재한다. 임시 사본의 dist 6개 및 dark-media.css 각각 끝에 주입하면 양 OS 모두 `check_exit=1`, `build_reached=false`, `payload_preserved=true`. 후보의 깨끗한 check/build/check는 0. CI의 기본 bash 실패 중단 설정에서 build에 도달하지 않는다. |
| B-P2-02, P2 | **FIXED** | `packages/tokens/base.scoped.css`의 자손 `color-scheme: light` 선언이 제거됐다. 최초 반례에서 root/inside/outside 모두 dark로 바뀌었다. 추가 OS media dark에서도 입력이 dark를 상속하고 light에서 모두 light다. |
| B-P2-03, P2 | **FIXED** | `base.css` 일반 CSS 클래스와 `base.scoped.css`의 surface 한정 일반 CSS가 생겼다. Tailwind 변환 없이 hairline 및 control-line의 실제 색이 `var(--kt-border)`/`var(--kt-control-line)` 직접 지정 기준 요소와 일치한다. surface 자체/자손 모두 적용되며 scoped 클래스는 surface 밖에서 적용되지 않는다. |
| B-P3-04, P3 | **FIXED** | T-102 구현·예정 파일이 `packages/tokens/aliases/map-vocabulary.css`, 검사 인수가 `packages/tokens/aliases`로 정정됐다. 해당 task의 `packages/tokens/src` 잔여 참조 없음. 기존 root exports 예약과 tarball `aliases/map-vocabulary.css` 및 examples 미동봉 수용 기준을 유지한다. 실제 alias 구현 성공으로 세지 않는다. |

최초 CSS 반례의 실제 후보 출력은 base와 scoped 모두 `rootScheme=dark, insideScheme=dark, outsideScheme=dark, borderColor=oklch(0.31 0.012 145)`였다. 확장 6조합에서는 다음 결과를 확인했다.

| 모드 | hairline | control-line | scoped 밖 hairline 클래스 |
|---|---|---|---|
| light | `oklch(0.925 0.01 141)` | `oklch(0.61 0.012 145)` | 기본 currentColor 유지 |
| class-dark | `oklch(0.31 0.012 145)` | `oklch(0.58 0.012 145)` | 기본 currentColor 유지 |
| media-dark | `oklch(0.31 0.012 145)` | `oklch(0.58 0.012 145)` | 기본 currentColor 유지 |

새 P0/P1/P2/P3 finding은 확인하지 못했다. 타입별 DTCG 변환·root token 계층·dark-media 생성·preset transitionTimingFunction·theme z 유틸리티 변경도 회귀 범위에 포함했다. 범용 CSS parser의 모든 가능한 입력을 지원한다고 판정한 것은 아니다.

## 양 OS 실제 결과

| 검증 | Windows | WSL |
|---|---|---|
| runtime | Python 3.14.3 / Node v25.9.0 / npm 11.12.1 | Python 3.11.15 / Node v22.22.2 / npm 11.19.1 |
| npm ci/check/build/check | 모두 exit 0; Node engine EBADENGINE 경고는 존재 | 모두 exit 0 |
| npm test | 7개 pass, fail/skip 0 | 7개 pass, fail/skip 0 |
| build 전 주입 | 7개 모두 exit 1·원문 보존 | 동일 |
| pack / 별도 설치 | exit 0 / exit 0 | exit 0 / exit 0 |
| 설치 후 exports·ESM | 구체 subpath 13개 resolve, tokenValues 44개 | 동일 |
| tarball | 18개 파일; CSS 7종·고지 3개·JSON·d.ts 포함 | 같은 필수 파일 목록 |
| LICENSE bytes | repo LICENSE와 일치 | 일치 |
| plan | 상세 task 106, 오류 0 | 동일 |
| links | 355 documents / 2306 targets / errors 0 | 동일 |
| SPDX | 41개 파일, 오류 0 | 동일 |
| secret·redaction | 각각 466개 파일, 발견 0·예외 0 | 동일 |
| versions self-check·diff check | exit 0 / exit 0 | 동일 |

임시 tarball SHA256은 Windows `4695afab5acb39a67333b44d7e7286c7d2e28d58a0a49d7fd07874201913c409`, WSL `b72fad230e498a8b49a546b26bdd0bcfb24a06832035f230b53a9a4af07effcd`다. 런타임/npm이 다르므로 바이트 재현성 통과를 주장하지 않는다. 이 값은 로컬 시험 산출물이며 외부 릴리스 digest가 아니다. 임시 사본·tarball·설치 프로젝트는 helper가 정리했다.

[공식 DTCG 2025.10 schema](https://www.designtokens.org/schemas/2025.10/format.json)를 2026-09-07에 직접 조회했다. 수신 bytes SHA256은 `32e93b780e4e4bca778d0780cb797a560deedc470c608af16576223f7e42915f`, 내장 resource 18개다. Windows jsonschema 4.26.0 Draft7Validator로 **후보 JSON 오류 0**을 직접 확인했다. 후보의 자체 assertion만 믿고 DTCG 적합을 선언하지 않았다.

GPL/PROVENANCE·LICENSE/NOTICE/THIRD_PARTY_NOTICES 및 npm/PyPI 미게시 경계는 변경되지 않았다. 새 dark-media 생성물에도 GPL SPDX·저작권·Generated 헤더가 있으며 실제 pack에 고지를 유지했다. 현재 tarball 파일 목록에 alias·weather 예제·폰트·소비자 파일은 없다. T-102 구현/소비자 이관을 이번 후보가 완료했다고 표시하지 않는다.

## 정확한 CI와 미실행 한계

- [PR #11](https://github.com/digitie/kor-travel-common/pull/11)은 조회 시 draft/open, base main, head `4c33a5d951e32df0c2170b7a865f324d122dbe05`다.
- [CI run 34126309766](https://github.com/digitie/kor-travel-common/actions/runs/34126309766)은 이 정확한 head의 PR run으로 6개 job 모두 success였다. packages job `101755695147` 로그에서 checkout ref/SOURCE_SHA/실제 HEAD 비교 일치, Node v22.23.1, npm@11.19.1 설치 성공, 새 build 전 check·생성 후 git diff·7 tests/7 pass·tarball install 성공을 확인했다.
- `NOT_RUN(로컬 exact Node 22.23.1 미설치)`: Windows/WSL 로컬 결과와 exact 원격 CI runtime을 구분했다.
- `NOT_RUN(이 리뷰에서 직접 실행하지 않음)`: Tailwind v3/v4 실제 컴파일, 별도 tsc 및 WSL 브라우저. 코드·정본·순수 CSS 브라우저·pack/ESM·DTCG 검증을 대신 동일 시험으로 부풀리지 않았다. workflow의 없는 lint/type-check script는 `--if-present`이므로 실제 해당 검사 통과로 세지 않는다.
- `NOT_RUN(변경 없는 Python 코드 재실행 생략)`: 로컬 전체 Python unittest. 양 OS 정적 gate는 직접 실행했고 exact 원격 tools job 성공은 별도 관찰했다.
- `NOT_RUN(이 리뷰에서 관찰하지 않음)`: 임시 release push와 main merge SHA의 실제 CI. T-101 closure 전 해당 실행 gate는 PR head 성공과 구분해 기록해야 한다.
- `NOT_RUN(T-102/T-103·소비자 후속 task)`: alias 구현·대비 도구·소비자 build/e2e·6폭 시각 diff. `NOT_RUN(사용자 범위 밖)`: 실제 Release/태그 생성·npm/PyPI 게시·소비자 쓰기.
- resume의 이전 시작 상태와 T-101 최종 evidence/완료 기록 정리는 이번 IN_PROGRESS 후보 이후 closure 작업으로 남는다. 이 리뷰는 미완료 외부 gate를 완료로 바꾸지 않았다.

최종 **PASS**: 원 B finding 4건 FIXED, 신규 finding 0건. 위 미실행 범위와 후속 closure gate를 보존한다.
