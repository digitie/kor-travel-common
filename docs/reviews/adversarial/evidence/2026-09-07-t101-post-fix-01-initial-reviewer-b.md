# T-101 독립 적대적 리뷰 B 원본

- 실행 ID: `reviewer_b-t101-f8894e2-20260907-214924`
- 판정: **BLOCK** — P0 0건, P1 0건, P2 3건, P3 1건. 아래 P2 수정 후 새 immutable 후보의 재검토가 필요하다.
- 독립성: reviewer A의 결과·메시지·보고서를 읽거나 요청하지 않았다. 후보 소스·문서·시험·설정과 소비자 저장소를 수정하지 않았고 commit/push/publish하지 않았다.
- 시작 KST: `2026-09-07T21:49:24.9478285+09:00`
- 종료 확인 KST: `2026-09-07T21:58:44.8810391+09:00`
- 후보 시작/종료 SHA: `f8894e293ca9677f457011197052cd55dbdc9696`
- 후보 시작/종료 tree: `30a25801de43472d322f560897cc6dc8e29daa52`
- base: `cf2c610cecfa7a9b8f7a035c9529d7a296e27527`
- 격리: `F:/dev/kor-travel-common-wt/review-t101-b` detached worktree. 시작/종료 `git status --porcelain=v1` 출력 없음. 빌드·설치·drift 주입은 이 트리를 읽어 만든 임시 사본에서만 실행했다.
- source `.git/config` 시작/종료 SHA256: `C06BFC225BFA7EBBF45777AF3B21E8DC7E69DD5011C07863B54B2EC6B4B3C0B9`. `core.worktree` 변경 없음.

## 전달 요청 원문

> T-101 draft PR #11의 immutable candidate `f8894e293ca9677f457011197052cd55dbdc9696`을 독립 적대적으로 리뷰해 주세요. 전문: CI workflow/source SHA·tarball contents/install, GPL/PROVENANCE/redaction, Windows/Linux portability, scope leakage/T-102, package docs contract. 같은 SHA를 detached/worktree로 고정하고 수정·commit·push하지 마세요. reviewer A 결과는 보지 말고, P0–P3 finding마다 독립 반례·명령·영향·disposition을 원본 evidence로 남기세요. BLOCK/CONDITIONAL/PASS를 명확히 보고해 주세요.

## 검토 범위와 실제 실행

base 대비 28개 변경 파일을 검토했다. workflow packages job, root workspace/lock, tokens CSS 7종·generator·생성물·6개 시험, package exports/files, GPL 고지·PROVENANCE, T-101/T-102와 architecture/style-delivery/design-tokens 정본을 대조했다. map 원천 `c494e227e010565be295de3f9670b2f7c8c20944:packages/kor-travel-map-admin/frontend/src/app/globals.css`는 소비자 Git object에서 읽기만 했다. 전체 원천 값의 별도 자동 전수 비교를 수행했다고 주장하지 않는다.

재현 보조 파일은 후보 밖의 다음 경로에 보존했다.

- `.git/codex-audit/review-t101-b-pack.py`: 후보를 임시 사본에 복사한 뒤 build/check/test/pack/install 및 drift 주입.
- `.git/codex-audit/review-t101-b-css.cjs`: 후보 CSS를 읽어 headless Chromium의 computed style을 조회. 후보 파일을 쓰지 않는다.

실행 명령의 핵심 인수는 다음과 같다. npm 명령은 위 pack 보조 파일이 임시 사본/설치 디렉터리에서 subprocess로 실행했다.

```text
py -3.14 -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/review-t101-b-pack.py F:/dev/kor-travel-common-wt/review-t101-b
# WSL에서는 동일 Python 보조 파일과 후보 경로를 /mnt/f/...로 바꾸어 Python 3.11.15로 실행
npm ci --ignore-scripts --no-audit --no-fund
npm run check
npm run build
npm run check
npm test
npm pack --workspace packages/tokens --pack-destination <임시 pack 디렉터리> --json
npm install --ignore-scripts --no-audit --no-fund <위 tarball 절대 경로>
node F:/dev/kor-travel-common/.git/codex-audit/review-t101-b-css.cjs F:/dev/kor-travel-common-wt/review-t101-b
py -3.14 -B -X utf8 tools/validate_plan.py
py -3.14 -B -X utf8 tools/validate_document_links.py
py -3.14 -B -X utf8 tools/check_spdx.py
py -3.14 -B -X utf8 tools/scan_secrets.py
py -3.14 -B -X utf8 tools/check_prod_redaction.py
py -3.14 -B -X utf8 tools/check_versions.py --self-check
git diff --check cf2c610cecfa7a9b8f7a035c9529d7a296e27527 f8894e293ca9677f457011197052cd55dbdc9696
gh pr view 11 --json headRefOid,isDraft,state,baseRefName,url
gh run view 34123916314 --json jobs
gh run view 34123916314 --job 101748005353 --log
```

WSL 정적 검사는 동일 6개 도구를 Python 3.11.15로 실행했다. Git 관련 명령에는 process 환경의 `GIT_DIR=/mnt/f/dev/kor-travel-common/.git/worktrees/review-t101-b`, `GIT_WORK_TREE=/mnt/f/dev/kor-travel-common-wt/review-t101-b`만 사용했다. source config를 바꾸지 않았다. Windows에서 잘못 인용한 `HEAD^{tree}` 조회와 glob 인수 검색은 실패 후 인수를 인용하거나 실제 파일명으로 고쳐 다시 실행했다. 실패한 조회는 gate 성공으로 집계하지 않았다.

| 검증 | Windows 실제 결과 | WSL 실제 결과 |
|---|---|---|
| runtime | Node v25.9.0, npm 11.12.1 | Node v22.22.2, npm 11.19.1 |
| ci / 최초 check / build / check | 전부 exit 0, root engine에 대한 EBADENGINE 경고 존재 | 전부 exit 0 |
| npm test | 6 tests, 6 pass, 0 skip | 6 tests, 6 pass, 0 skip |
| pack / 별도 설치 | exit 0 / exit 0 | exit 0 / exit 0 |
| 설치 후 공개 구체 subpath | 13개 resolve 성공; ESM tokenValues 44개 | 13개 resolve 성공; ESM tokenValues 44개 |
| tarball | 18개 파일, CSS 7종·고지 3개·d.ts/JSON 포함 | 같은 18개 파일명과 필수 내용물 |
| LICENSE | tarball LICENSE bytes가 repo LICENSE와 동일 | 동일 |
| plan | tasks 106, errors 0 | tasks 106, errors 0 |
| links | documents 355, local targets 2306, errors 0 | 동일 |
| SPDX | 41개 파일, 오류 0 | 동일 |
| secret / redaction | 각각 466개 파일, 발견 0, 예외 0 | 동일 |
| registry self-check / diff check | exit 0 / exit 0 | exit 0 / exit 0 |

임시 tarball SHA256은 Windows `28fe9035d4b5e939e073fb1fd9db148a278260a9ac11e6c15b1b1a2707fd2a83`, WSL `15b9e4c989d8be116915e40a157aaf0fab405325817a7ccf78475a313f71e24d`였다. 런타임·npm이 다르므로 바이트 재현성을 통과로 판정하지 않는다. 이 값은 외부 배포 자산 digest가 아니다. tarball은 임시 디렉터리에서 검사 후 정리되었다.

GPL-3.0-or-later package metadata, LICENSE/NOTICE/THIRD_PARTY_NOTICES.md 동봉, tokens.css SPDX·Origin·Modified, PV-013의 고정 map commit/경로를 확인했다. 파일 목록에 소비자 로컬 파일·폰트·weather 예제·운영 값은 없었다. JSON/생성물 고지는 패키지 THIRD_PARTY_NOTICES.md와 연결되며 별도 외부 코드·폰트의 도입은 확인되지 않았다. npm/PyPI 게시·소비자 쓰기는 없었다.

## Finding

### B-P2-01 — CI가 커밋된 생성물 drift를 먼저 덮어써 통과시킨다

- 심각도: P2. Disposition 권고: **수정 필요**.
- 위치: `.github/workflows/docs.yml:183–185`; `packages/tokens/test/values.test.mjs:129–131`.
- 정본 근거: `docs/standards/design-tokens.md:18` TK-1은 정본에서 재생성한 생성물의 CI diff 0을 요구한다.
- 최소 재현: 임시 사본의 `packages/tokens/dist/tokens.js` 끝에 comment 한 줄을 추가한다. 이 상태에서 `npm run check`는 exit 1이다. 이어 workflow 순서대로 `npm run build`, `npm run check`, `npm test`를 실행하면 **모두 exit 0**이다. Windows와 WSL에서 동일했다.
- 원인: build가 추적 생성물을 덮어쓴 뒤 check가 그 결과만 비교한다. test도 build 후 check여서 커밋 당시 불일치를 복원해 검사하지 않는다. packages job에 작업 트리 생성물의 git diff 검사가 없다.
- 영향: stale/수동 변경된 JS·JSON·d.ts 등을 포함한 PR이 녹색 CI를 얻는다. 현재 후보의 최초 check는 실제로 성공했으므로 현재 파일이 불일치한다고 주장하는 finding은 아니다. 향후 잘못된 생성물 커밋을 차단할 필수 gate의 재현 가능한 false PASS다.
- 최소 권고: build 전 committed outputs를 check하거나, 재생성 직후 대상 generated paths에 `git diff --exit-code`를 실행한다. dirty 생성물을 주입한 음성 시험이 해당 gate를 실패시키도록 고정한다.

### B-P2-02 — scoped base가 dark surface의 native control까지 light로 강제한다

- 심각도: P2. Disposition 권고: **수정 필요**.
- 위치: `packages/tokens/base.scoped.css:7–9`.
- 최소 재현: 브라우저에 `tokens.css`와 `base.scoped.css`를 함께 넣고 `<html class="dark"><section data-kt-surface><input id="inside"></section><input id="outside">`의 computed `colorScheme`을 읽는다. 위 CSS 보조 파일로 직접 실행했다.
- 실제 출력: `rootScheme=dark, insideScheme=light, outsideScheme=dark`. 같은 문서에서 `base.css`를 사용하면 `rootScheme=dark, insideScheme=dark, outsideScheme=dark`였다.
- 원인: scoped root뿐 아니라 모든 자손에 `color-scheme: light`를 직접 선언하므로 조상의 dark 값 상속이 중단된다.
- 영향: 다크 토큰을 쓰는 admin 표면 안의 input/select 등 UA가 그리는 UI가 밝은 색 체계를 사용한다. `base.scoped.css`가 단지 base 적용 범위를 줄인다는 `docs/architecture/packages.md:34` 계약과 다르게 동작한다.
- 최소 권고: scoped surface가 선택된 color-scheme을 상속하도록 하고 class/media 경로에서 자손을 light로 덮어쓰지 않는다. surface 안/밖 native input의 computed style을 양쪽 dark 선택 경로에서 확인한다.

### B-P2-03 — Tailwind 없이 쓸 수 있다는 hairline 규칙이 브라우저에서 무시된다

- 심각도: P2. Disposition 권고: **수정 필요**.
- 위치: `packages/tokens/base.css:20–25`, `packages/tokens/base.scoped.css:21–26`.
- 정본 근거: `docs/architecture/packages.md:33–34`, `docs/standards/design-tokens.md:25`는 hairline 2종을 포함한 base 파일의 Tailwind 의존을 "없음"으로 정의한다.
- 최소 재현: Tailwind 변환 없이 tokens/base CSS를 브라우저에 넣고 `<div class="border-kt-hairline border-kt-hairline-scoped" style="border-width:1px;border-style:solid">`의 border 색을 읽는다. 위 CSS 보조 파일에서 base/scoped 각각 실행했다.
- 실제 출력: 양쪽 모두 `borderColor=rgb(255, 255, 255)`였고, 사용할 토큰 값은 `--kt-border=oklch(31% 0.012 145)`였다. 즉 currentColor가 사용되고 선언된 hairline 토큰은 적용되지 않았다.
- 원인: hairline과 control-line 모두 Tailwind 전용 `@utility` 내부에만 정의되어 일반 CSS 브라우저 파서가 무시한다.
- 영향: Tailwind를 쓰지 않는 소비자가 공개된 base 파일을 import해도 hairline/control 경계색 계약을 얻지 못한다. 파일 resolve/정규식 시험은 이 실패를 검출하지 못한다.
- 최소 권고: 해당 클래스의 일반 CSS 규칙을 제공하고 scoped 변형에는 surface containment를 적용한다. Tailwind 빌드와 순수 CSS 소비 둘 다 토큰 색을 얻는지 확인한다. 의존성 계약을 조용히 변경해 해결하지 않는다.

### B-P3-04 — T-102의 src 경로 인계가 T-101의 실제 flat package와 맞지 않는다

- 심각도: P3. Disposition 권고: **T-102 착수 전 문서 정정**.
- 위치: `docs/tasks/T-102-map-vocabulary-shim.md:21,32,36,45`; 현재 `packages/tokens/package.json`의 exports/files 및 `scripts/build.mjs`.
- 재현: `rg -n 'src/aliases|packages/tokens/src|aliases' docs/tasks/T-102-map-vocabulary-shim.md`로 구현·검사 경로가 `packages/tokens/src`임을 확인한다. 현재 배포 CSS/정본은 `packages/tokens` 루트에 있고 generator에는 src→package-root 복사 과정이 없다. T-102의 tarball 수용 기준은 여전히 `aliases/map-vocabulary.css`다.
- 영향: 다음 에이전트가 현재 task 명령을 그대로 따르면 정본 CSS가 없는 src를 검사하거나, 공개 root aliases 경로와 다른 곳에 구현한다. 아직 T-102가 구현되지 않았다는 사실 자체는 결함으로 세지 않는다. 계획에 남아 있던 경로 불일치가 T-101 실물로 구체화된 낮은 우선순위 인계 문제다.
- 최소 권고: T-102의 구현·검사·예정 경로를 실제 flat layout과 일치시키거나 복사/exports 매핑 계약을 명시한다. 예제 미동봉과 alias opt-in 범위는 유지한다.

## CI·미실행·판정 한계

- [PR #11](https://github.com/digitie/kor-travel-common/pull/11)은 조회 시 draft/open, base main, head가 후보와 정확히 같았다.
- [CI run 34123916314](https://github.com/digitie/kor-travel-common/actions/runs/34123916314)은 정확한 후보 SHA의 PR run으로 6개 job 모두 success였다. packages job `101748005353` 로그에서 checkout ref와 SOURCE_SHA, 실제 `git rev-parse HEAD` 비교, Node v22.23.1 설치, npm@11.19.1 설치 명령 성공, 6 tests/6 pass 및 tarball smoke 성공을 직접 확인했다.
- 이 원격 녹색 결과가 B-P2-01의 음성 사례를 검사한다는 뜻은 아니다. 위 false PASS는 별도로 직접 재현했다.
- `NOT_RUN(로컬 Node 22.23.1 부재)`: 로컬 정확한 권장 런타임. WSL의 지원 범위 Node 및 exact 원격 CI 결과와 구분했다.
- `NOT_RUN(설치된 tsc 없음)`: 별도 실제 TypeScript 컴파일. workflow의 lint/type-check는 해당 script가 없어 `--if-present`로 건너뛴다. 이를 lint/type-check 성공으로 집계하지 않았다.
- `NOT_RUN(변경 없는 Python 코드의 전체 unittest 재실행 생략)`: 이 리뷰의 로컬 전체 Python 회귀. 정적 gate는 양 OS에서 직접 실행했고 원격 tools job 성공을 별도로 확인했다.
- `NOT_RUN(이번 리뷰에서 관찰하지 않음)`: 임시 release push와 main merge SHA의 실제 CI. T-101 closure 수용 기준에서 PR head 성공으로 대체할 수 없다.
- `NOT_RUN(T-102/T-103 및 소비자 후속 task)`: aliases 구현, 대비 도구, 소비자 build/e2e·6폭 시각 비교. 이번 Chromium 검사는 두 CSS 최소 반례만 확인한 것이며 완전한 접근성/브라우저 호환성 검사가 아니다. WSL 브라우저 검사는 실행하지 않았다.
- `NOT_RUN(사용자 범위 밖)`: 실제 GitHub Release/태그 발행, npm/PyPI 게시, 소비자 채택·소비자 파일 변경.

최종 **BLOCK**. CI/pack/install/GPL/정적 gate의 실제 성공을 보존하되, 재현된 P2 세 건이 남아 있으므로 T-101 완료 승인으로 사용할 수 없다.
