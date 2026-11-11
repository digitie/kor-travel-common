# COMMON3 수정 후 독립 적대적 리뷰 B 원문

- reviewer: B / Epicurus, 구현 비참여. 전문: packaging/dependency/실제 해석 경로/CI/라이선스.
- runid: `Epicurus-B-common-postfix-3-20261111T153736Z`
- 시작 UTC: `2026-11-11T15:37:36Z`; 종료 UTC: `2026-11-11T15:54:21.401440+00:00`
- manifest: `review-manifest-common-3.json`, SHA256 `047ae6686cf8a08515a1e20b97147c218d5278823e976a6022aad34097021cd6` — 직접 일치 확인.
- **불변7e 기준선 verdict: BLOCK.** 신규 P1 3건 OPEN. 이 중 CI 경로 신뢰 문제는 범위 밖 00ddd65에서 수정·성공을 직접 관찰했으나 원7e 실패 기록을 변경하지 않는다. 나머지 scanner 및 연결 workspace 빌드 그래프 문제는 해결 근거 없음.
- B2-P3-01: **FIXED**. 최초 11건의 기존 FIXED 이력 보존. 상대 reviewer 원문은 열지 않았고 상대 결론을 근거로 사용하지 않았다.

## 기준선·격리·관찰 SHA

| 항목 | 관찰값 |
|---|---|
| common head | `7e3f33e0391990b9312fee513de581e28035aa8b` |
| 이전 common 리뷰 | `8dad71a50f9f8f12f0e3ba1c913a93e404dabfed` |
| common 최초 base | `c289b4624c8640eb918cc915803e72ae754e58fb` |
| VWorld head | `9a7a348b02d61969b394c681b024d5851eef836b` — 이전과 동일 |
| common pack source | `670a753bc17f956f71bdc28385d6241a6e4ee017` |
| artifact | `artifacts/integration-8-review`, CANDIDATE_NOT_RELEASED |
| 격리 | `/tmp/review-b-common3-20261111-153736`, detached7e |
| 증거 | `review-B-common-postfix-3-evidence/` |
| 별도 CI delta | `00ddd65be56a1955a4cee1a458a8cc274946fbe1`, manifest3 밖 |

AGENTS, agent-workflow, reviews/README 지침을 적용했다. 원 저장소에서는 Git object와 기존 도구 의존성만 참조했다. 소스 수정·신규 install·캐시 삭제·원격 쓰기를 하지 않았다. 자체 임시 fixture만 작성했다. build/test 때 기존 node_modules를 symlink로 참조했으며 마지막에 제거했다. 최종 격리 worktree의 HEAD는7e, `git status --porcelain=v1`은 빈 문자열이다. build가 생성한 ignored dist는 pack 비교에만 사용했다.

670→7e diff는 docs/journal.md, docs/resume.md, docs/tasks/T-218-radix-library-unification.md, frontend-artifacts.json만이다. runtime/package source는 같다. 상위 원본·artifact 이전 보고서 및 integration-7/8을 수정하지 않았다.

## 기존 finding closure

| ID | 상태 | 이번 근거 |
|---|---|---|
| B2-P3-01 tokens 고지 모순 | **FIXED** | `packages/tokens/THIRD_PARTY_NOTICES.md`의 ‘동봉한 CSS와 고지’는 shadcn CSS 원문·MIT 전문 동봉을 명시한다. 이름만 참조하는 글꼴과 구분하며 SHADCN_LICENSE를 가리킨다. 실제 c8 tgz의 이 파일이 불변 source와 같다. ‘별도 서드파티 소스 사본이 없으므로’라는 기존 모순이 제거됐다. |
| B-P0-01, B-P1-01~07, B-P2-01~03 | 기존 **11 FIXED 보존** | 이전 원문과 ID·심각도 변경 없음. VWorld source/3개 bytes 불변 및 6개 SRI를 재확인했다. 이번 UI101/정책41/버전95/고지·client directive·pack 비교에서 기존 문제의 재발을 확인하지 않았다. NativeCSS와 별개인 새 CI scanner 실패는 아래 새 ID로 보고한다. |

이번 재검토는 이전의 실제 browser 증거를 새로 실행한 것처럼 집계하지 않는다. Dialog 신규 API 기본값은 source·타입·단위검증 및 아래 별도 CI delta로 확인했다.

## 신규 findings

### B-P1-08 — 컨테이너의 checkout Git 신뢰 설정 누락으로 packages 필수 gate가 시작 전에 중단

- 심각도: **P1**. disposition: **OPEN@7e**; 별도 **00ddd65 수정은 직접 재확인**.
- 위치: `.github/workflows/docs.yml:173`, `.github/workflows/docs.yml:190`.
- 재현/증거: exact7e docs run43049460204, packages job130622278809. checkout은7e로 성공하지만 `test "$(git rev-parse HEAD)" = "$SOURCE_SHA"`에서 `fatal: detected dubious ownership in repository at '/__w/kor-travel-common/kor-travel-common'`. Node 설치부터 browser·tarball 단계까지 모두 skipped다. container root 실행과 checkout Git의 trust 설정이 이어지지 않는다.
- 영향: 고정 공식 Playwright image를 사용해도 packed UI/RSC/Dialog/Next 검증이 전혀 실행되지 않는다. 별도 frontend CI green을 packages PASS로 대체할 수 없다.
- 권고: 정확한 `$GITHUB_WORKSPACE`만 Git safe.directory로 설정한 뒤 SHA 검사를 보존하고 해당 job 전체를 다시 실행한다. wildcard 신뢰는 불필요하다.
- 후속 관찰: 00ddd65의 단 한 줄 `git config --global --add safe.directory "$GITHUB_WORKSPACE"` diff를 Git으로 직접 확인했다. run43050853120/job130627252820의 source SHA·preflight·pack/browser 성공도 직접 API/로그로 확인했다. 이 delta에서는 해당 원인의 수정이 입증됐지만 manifest3의 소스를 바꾼 것으로 기록하지 않는다.

### B-P1-09 — 추적 vendor tgz 추가와 UTF-8 전제 scanner가 충돌하여 필수 보안/문서/도구 CI 실패

- 심각도: **P1**, disposition: **OPEN**.
- 위치: `tools/_scan.py:206` → `tools/_scan.py:125`; 새 입력 `vendor/lightningcss-1.33.0+nativecss.fix.3.tgz`, `vendor/lightningcss-1.33.0+nativecss.fix.4.tgz`.
- 재현: 깨끗한 detached7e에서 `python3 -B -X utf8 tools/scan_secrets.py --all`, `python3 -B -X utf8 tools/check_prod_redaction.py --all` 모두 exit2, ‘검사 오류: UTF-8로 검사할 수 없는 입력’. `git ls-files`의 모든 blob/파일을 조사했을 때 UTF-8 비텍스트 입력은 위 두 tgz다. node_modules symlink를 제거한 최종 clean worktree에서도 동일하다.
- 원격 증거: exact7e의 secret130622278797, tools Ubuntu130622278806, docs130622279315에서 같은 오류. tools Windows130622279192도 failure. docs의 문서·계획·회귀·공백 단계는 성공하고 redaction 단계가 실패했다. 단위시험 failure나 실제 secret 유출로 바꿔 해석하지 않는다.
- 영향: 정상적인 새 vendor artifact를 체크인하면 전체 트리 scanner의 계약상 중단으로 필수 merge gate가 계속 red다. 새 CSS source/vendor gate가 이 scanner들을 대신하지 않는다.
- 권고: 검증된 정확 artifact 경로·digest를 인식하는 명시적 binary/archive 처리와 텍스트 내용 감사·실패 회귀를 연결한다. 임의 binary를 모두 무시하거나 UTF-8 decode error를 조용히 버리는 완화로 대체하지 않는다.
- 00ddd65 후속: 같은 docs run에서 packages만 성공했고 docs/secret/tools는 여전히 failure다. scanner 수정 중이라는 인계는 closure 증거가 아니다.

### B-P1-10 — 연결된 workspace 빌드 도구의 devDependency 엔진을 누락해 원본 LightningCSS 사용을 PASS 처리

- 심각도: **P1**, disposition: **OPEN**. 부모가 미리 알려준 CI 실패와 별개로 B가 독립 재현했다.
- 위치: `tools/check_frontend_dependencies.mjs:98`. 동봉한 UI/tokens checker 사본도 동일하다.
- 조건: 앱이 `workspaces:["tools/*"]`와 root devDependency `build-helper`를 갖고 빌드에서 이 helper를 실행한다. helper는 linked/private workspace이며 자신의 devDependencies에 stock `lightningcss:1.33.0`을 갖는다. lock의 root canonical engine은 fix4 실제 c8 integrity/file, helper 아래는 실제 stock1.33.0 integrity다.
- 재현: 보존한 `fixture/package.json`, `fixture/package-lock.json`을 입력으로 중앙 정본·artifact bytes·source를 모두 전달한 검사기는 exit0 ‘공통 의존성과 산출물 일치’. 실제 기존 모듈의 해석 경로는 helper에서 stock1.33.0이다. helper의 `.x{color:var(--x)}` + `visitor:{Rule:r=>r}` 변환은 `failed to deserialize; expected an object-like struct named Specifier, found ()`로 exit1. root의 같은 입력은 fix4에서 성공한다.
- 원인: link를 따라 helper workspace에 도달해도 `index === 0`일 때만 devDependencies를 포함한다. 현재 앱의 빌드에서 직접 실행하는 helper의 개발 엔진을 탐색하지 않는다.
- 대조: lock helper entry에서 devDependencies를 dependencies로만 바꾸면 같은 checker가 즉시 exit1 `lightningcss: 빌드 전이 버전·bytes 불일치 tools/build-helper/node_modules/lightningcss`. 불일치 검사가 있다는 사실과 누락 경로를 분리해서 확인했다.
- 영향: 루트 canonical artifact/SRI/lock은 맞아도 연결 workspace가 원래 고장난 변환 엔진을 실제 빌드에서 사용할 수 있다. ‘앱 개발 그래프까지 같은 bytes’라는 중앙 정책이 정상 workspace 도구 구성에서 false PASS한다. 현재 common smoke나 특정 실제 소비자가 이미 이 구성을 쓴다는 주장은 아니다.
- 권고: 현재 앱으로부터 도달한 linked workspace의 devDependencies도 CSS 빌드 그래프에서 해석하거나, 이에 준하는 유효 override/실제 resolver 검증을 추가한다. 무관한 다른 workspace·공개 패키지의 devDependencies까지 전부 순회할 필요는 없다. React runtime 중복 검사는 현재 의도한 runtime 범위를 유지한다. 위 최소 false-PASS와 대조군을 회귀로 추가한다.
- 재현 한계: 대형 install 금지에 따라 신규 `npm ci`를 하지 않았다. lock은 linked-workspace 구조를 구성한 최소 모델이고 필수 package 일부는 lock에만 있다. stock entry는 기존 실제 npm lock의 version/resolved/full integrity를 사용했으며 실제 helper/root 엔진 실행은 기존 모듈을 읽기 재사용했다. 완전한 새 npm 설치나 소비 앱 export 검증 결과로 확대하지 않는다. 최초 탐색 harness의 placeholder와 수정 전 오류는 별도 남겼고 최종 fixture/control 로그를 판정 근거로 쓴다.

## 실제 실행·artifact 검증

| 검증 | B 독립 결과 | 증거 |
|---|---|---|
| tokens 생성, UI tsc, package/client directive 검사 | 성공 | build.log |
| UI unit | **101 PASS, 9 suites** | ui101.log |
| tokens unit | **9 PASS** | tokens9.log |
| dependency/nativeCSS 정책 회귀 | **41 PASS** | policy41.log |
| Python 버전 판정 회귀 | **95 PASS** | versions-tests.log |
| vendor 라이선스/메타 검사 회귀 | **2 PASS** | vendor-tests.log |
| export target 존재 | UI88 / tokens21, missing0 | exports-targets.json |
| 6개 tarball 실제 SHA512 | 모두 manifest와 일치 | artifact-verification.json, manifest 복사 |
| UI source/dist/package/고지 비교 | 94개, 불일치0 | artifact-verification.json |
| tokens source/dist/package/고지 비교 | 25개, 불일치0 | artifact-verification.json |
| root ledger 및 checker 사본 | manifest packages 일치, source/tools/UI/tokens checker 동일 | artifact-verification.json |
| 연결 workspace CSS 공격·대조 | dev exit0/actualstock exit1, dependencies 대조 exit1 | workspace-devgraph-control.json, helper-stock-build.log, root-canonical-transform.log |
| 최종 clean 상태 scanner 2종 | 둘 다 exit2, 미통과 | final-clean-scanners.json |

UI/tokens는 c8 실제 파일을 새로 빌드한 불변7e source와 대조했다. VWorld3개와 NativeCSSfix4는 기존 검토 bytes 불변을 확인한 것이며 이번에 Rust/지도 browser를 새로 빌드·실행한 것은 아니다. @kor-travel/tokens0.1.1, @kor-travel/ui0.2.0, lightningcss1.33.0+nativecss.fix.4, vworld-map-core1.0.1, vworld-map-rn1.0.1, vworld-map-web1.0.3의 완전한 SRI는 복사한 manifest에 보존했다.

Dialog/AlertDialog의 unstyled 기본 false, Dialog size 기본md, showCloseButton 기본true, Alert size 기본default를 확인했다. overlayProps가 단일 내부 overlay에 전달되고 공개 타입/호출부에서 소비되며 DOM으로 누출되지 않는 unit101 결과를 확인했다. max-height/overflow 및 size 계약은 source·CHANGELOG에 연결되어 있다. 새 options의 기본 동작 및 공개 export/client 경계에서 추가 결함을 확인하지 않았다. 실제 viewport/browser 검증은 아래 delta의 관찰이며 B 로컬에서 실행하지 않았다.

## exact7e 원격 CI와 후속00ddd65 증거의 구분

GitHub API를 읽기 전용으로 직접 조회했다. `remote-exact-7e.json`에 관찰 UTC, job/step 상태, 실패 원문 발췌를 저장했다.

| exact7e run | 결론 |
|---|---|
| workflows selftest43049460131 | success |
| common frontend43049460126 | success |
| python-package43049460336 | success |
| docs43049460204 | **failure** — check-versions success, packages/secret/docs/tools 양 OS failure |

원격 Python 로그의 실제 수치는 **Ran347, skipped3**이며 모두 통과라는 문구로 skip을 숨기지 않는다. 부모 local346PASS/1SKIP을 이 원격 수치로 치환하지 않았다. exact7e packages는 install/browser 이전에 중단됐으므로 NOT_RUN이다.

별도 delta `00ddd65be56a1955a4cee1a458a8cc274946fbe1`는 `.github/workflows/docs.yml` 한 줄만 추가한다. runtime/source/c8 ledger는 변경 없다. [run43050853120 packages130627252820](https://github.com/digitie/kor-travel-common/actions/runs/43050853120/job/130627252820)의 API 상태는 success이고 모든 실제 검사 단계가 success다. 직접 읽은 로그에서 아래를 확인했다.

- 공식 image Playwright1.65.0 preflight 및 Chromium158.0.8127.18 `/ms-playwright/chromium-1254/chrome-linux64/chrome` 실제 launch.
- UI101·tokens9·정책41 및 webpack/Turbopack 빌드 성공.
- packed radix/Dialog browser **65 passed (41.0s)**, viewport320/375/가로667/desktop 및 size500/640/700/1280/1600 로그 존재. skip을 pass에 포함하지 않았다.
- 15:43:01Z의 전체 pack SHA512 출력이 UI `RaBKVxmLJi7ZoQZqs28BaTmXzxpHsihV7D/VvR/vnDeqXtOvtiZawAo6K3CtbuZ37daKqMhGCG5hC5p42pI3Ug==`, tokens `juHDU+d/0GtLmylPyx9kDur2GwnzV5izAtRpzfqhxvbMjPlVfrbEanLBcdqC+EdmifO7StrMlcQJso239gv5PA==`로 c8과 정확히 같다. 이는 source 동일성 추론뿐 아니라 실제 CI pack bytes 연결 증거다.
- 별도 run의 docs/secret/tools 양 OS failure는 그대로다. packages 성공을 workflow 전체 성공으로 부풀리지 않는다.

`remote-delta-00ddd65.json`, `remote-delta-sri-proof.json`, `delta-00ddd65.patch`에 직접 관찰을 보존했다. 이 delta는 B-P1-08의 수정 근거이고 새 immutable manifest에 포함될 때의 재검토에 사용할 수 있다. 현재7e 원문 verdict를 PASS로 바꾸지 않는다.

## 주요 명령·재현 자료

모든 명령은 Windows PowerShell `workdir C:\`에서 `wsl.exe -e bash -lc`로 실행했다. Windows cwd는 baseline으로 사용하지 않았다.

```bash
sha256sum /home/digitie/dev/common-unification-20261111/review-manifest-common-3.json
git worktree add --detach /tmp/review-b-common3-20261111-153736 7e3f33e0391990b9312fee513de581e28035aa8b
git rev-parse HEAD
git diff --name-only 670a753bc17f956f71bdc28385d6241a6e4ee017 7e3f33e0391990b9312fee513de581e28035aa8b
node packages/tokens/scripts/build.mjs
node node_modules/typescript/bin/tsc -p packages/ui/tsconfig.json
node packages/ui/scripts/check-package.mjs
node --test packages/ui/test/dependency-policy.node.test.mjs packages/ui/test/native-css-policy.node.test.mjs
(cd packages/ui && node ../../node_modules/vitest/vitest.mjs run)
(cd packages/tokens && node --test test/*.test.mjs)
# Python 재현 진입점: tests/test_check_versions.py(95), tests/test_native_css_vendor.py(2)
python3 -B -X utf8 tools/scan_secrets.py --all
python3 -B -X utf8 tools/check_prod_redaction.py --all
git diff 7e3f33e0391990b9312fee513de581e28035aa8b 00ddd65be56a1955a4cee1a458a8cc274946fbe1
git status --porcelain=v1
```

독립 공격의 최종 package/lock/helper source는 evidence/fixture, 실행 명령·기존 엔진 경로는 fixture-reproduction.md에 있다. API 호출은 `fetch_commit_workflow_runs(commit_sha=7e...)`, `fetch_workflow_run_jobs(run_id=43049460204/43050853120)`, `fetch_workflow_job_logs(job_id=130622278809/130622278797/130622278806/130622279315/130627252820)`이다. 어떤 원격 rerun/메시지/수정도 실행하지 않았다.

## 보존·미검증 경계·최종 판정

기존 common 원문 SHA256은 최초 `520356751417c84ecb0f8d078891556e3533c2b93a9d09184b6260567867ce87`, postfix2 `45b6aa8bce5f47ce50ce562f6f056eba1213e8860ab1e147ddd765dd7bf59446` 그대로다. NativeCSS 원문2개 SHA도 final-provenance.json에 보존했다. integration-7 및 이전 manifest/보고서는 수정하지 않았다.

새 대형 install, Rust rebuild, 신규 로컬 실제 browser/전체 소비 앱 export/배포/네이티브 실행은 NOT_RUN(디스크 제한과 이번 scope). 별도 NativeCSS748 macOS가 queued 뒤 CANCELLED라는 후속 인계는 해당 별도 scope의 정보이며 Mac PASS 근거로 사용하지 않았다. common 수정 중 작업트리와 후속 정책 worker 결과는 baseline에서 제외했다.

**최종: BLOCK@manifest3(7e). B2-P3-01 FIXED, 최초11 FIXED 유지. 신규 B-P1-08/09/10은7e에서 OPEN. 별도00ddd65에서08 수정과 동일 c8 실제 packed/browser 성공은 검증됐으나09/10은 잔여다. 새 불변 manifest에 대한 원 reviewer 확인 전 전체 gate/소비 앱/릴리스 PASS를 선언하지 않는다.**
