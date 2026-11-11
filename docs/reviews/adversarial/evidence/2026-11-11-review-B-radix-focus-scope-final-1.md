# Radix FocusScope formal1 독립 리뷰 B 원문

- reviewer **B / Epicurus**, 구현 비참여. packaging/source/provenance/실제 runtime 해석 담당.
- runid `Epicurus-B-scope1-20261111T175647Z`; UTC 시작 `2026-11-11T17:56:47Z`, 종료 `2026-11-11T18:09:42.707362+00:00`.
- manifest 실제 SHA256 `4a7457463f69ad3e68ea9bba804401c546375ce8f69b1b389fe04d9df97c37ce`, 요청과 일치.
- source **`706e27aaf87bda2df7bbb9da60cc01cebc9ff064`**, upstream Git **`eb3a2b7091293e27df8f9ba906632d8daa3d81a3`**. 이후 cc 등 현재 worktree는 source에 혼합하지 않았다.
- artifact **`@radix-ui/react-focus-scope@1.3.1+kortravel.fix.1`**, 31,214 bytes, SHA256 **`f97c1dd4851fd1dc7b75bfbe9ce7e2d68bbd32e225b9ff52954c683fd4c7081d`**.
- SRI `sha512-550B+tdvg3N/tsIzOFA8zRhoMxGnPeBRl65Wg+9kY2VEEf6TW7RZKBWckVToLNuALHYZR8J9zG8GUP7DROBflg==` 직접 재계산 일치.
- **source/package 검토 PASS, 새 P0/P1/P2/P3 finding 없음. 최종 gate verdict CONDITIONAL**: R706 연결 regression CI가 browser 중 CANCELLED, pack 단계 skipped다. packed Pinvi/C10·후속 최종 head/producer/delivery delta는 별도 입력이다.
- 기존 소비자1의 Pinvi B-CONS-P2-01을 이 low-level package 결과로 닫지 않는다. 상대 reviewer raw/verdict 미열람.

## 1. 무엇을 기준으로 실행했는가

원 repo의 source는 full SHA Git show/diff로 읽었다. 자체 `/tmp/review-b-scope1-20261111-175647`에 exact preferred source와 고정 pack을 물질화했다. 동봉15개 파일의 path/type/hash를 검사하고 자체 fixture에만 추출했다. 원본 source·artifact·manifest를 수정하거나 새 install·repack하지 않았다.

stock은 부모가 보존한 registry1.3.1의9개 파일·receipt를 사용했다. 이를 그냥 Git eb3와 같은 것이라고 가정하지 않았다. frozen Pinvi ada425의 실제 package-lock registry URL/SRI가 receipt와 같은지 확인했고, 해당 공개 registry tgz14,955 bytes를 설치 없이 제한 크기로 읽어 SRI와9개 파일 SHA256이 보존본과 모두 같은 것까지 독립 확인했다. original registry SRI는 `sha512-ugeMhbXt4y5S2T1GnIqbWDKEN962PDwnX1fN0eKOOgf5f63Dh2mn8F1FUySlgW0iF6GiVsRF32DzuDIWTUyQJg==`다.

React/테스트 도구는 소비자 Pinvi의 기존 module 항목을 자기 overlay로 읽기 재사용했다. 패치 중인 commonRoot 모듈을 stock으로 쓰지 않았다. cache는 자기 tmp에만 생성했다. 원문·consumer 판정은 보존하고 implementation commit·원격 write를 하지 않았다.

## 2. registry1.3.1과 Git eb3, R706의 실제 runtime 차이

**stock registry1.3.1은 Git eb3와 완전히 같은 runtime이 아니다.** 두 dist sourcemap의 sourcesContent와 실제 JS를 직접 대조했다.

1. registry→eb3: focus-scope.tsx에 IME composition/keyCode229 early return이 추가돼 있다. composing 입력의 Tab을 focus loop가 소비하지 않게 하는 변경이다. index source와 나머지 runtime source는 같다.
2. eb3→R706: Shift+Tab에서 현재 focus가 첫 tabbable뿐 아니라 scope container 자신이어도 경계를 처리한다. `loop`이면 마지막 후보로 이동하고, trapped-only면 preventDefault하며 container를 유지한다.
3. 실제 pack의 CJS/ESM dist에는 위 **두 행동 차이**가 있고 추가 실행 코드 차이는 없다. 나머지는 source 경로 주석 차이뿐이다. 실제 dist diff를 evidence에 보존했다.

따라서 published stock 기준으로 ‘한 조건만 바뀌었다’고 보고하지 않는다. source-before22PASS/4FAIL은 이미 IME 수정이 있는 Git base를 기준으로 한 것이고, 아래 B의 실제 registry-before20PASS/6FAIL과 기준이 다르다.

## 3. package/API/고지/source 연결

| 확인 | 독립 결과 |
|---|---|
| tgz | 전체 SHA256/SHA512·크기 일치, 일반파일15개, 탈출/중복/link 없음 |
| 이름·full version | 원 package 이름 유지, `1.3.1+kortravel.fix.1`을 실제 publish manifest가 보존 |
| CJS/ESM/type targets | require/import 각 JS와 d.ts/d.mts 네 target 모두 존재 |
| 실제 public exports | stock·fixed 모두 CJS/ESM **동일5개** |
| 선언 | fixed d.ts/d.mts가 registry stock과 **bytes 동일** |
| runtime dependency·peer/meta | stock과 동일. 공개3개 dependency versions, React16~19 peer 범위/optional type peer 보존 |
| dev tool 강제 | published package에서 devDependencies/scripts 제거, `@repo/*`를 runtime dep로 강제하지 않음 |
| 라이선스 | MIT 전문이 Git R706 root LICENSE 및 registry stock과 bytes 동일 |
| preferred source | src/index.ts, src/focus-scope.tsx, source test, tsconfig의4개 hash가 PROVENANCE/manifest/Git R706와 모두 같음 |
| generated JS 계보 | dist sourcemap의 source 내용이 동봉 preferred source와 정확히 연결되며, actual JS에서도 두 변경만 확인 |

실제5개 export는 `FocusScope`, `FocusScopeBranchProvider`, `Root`, `useFocusScopeBranch`, `useFocusScopeBranchRegistry`다. Branch provider/hook이 stock에 없던 새 public API라고 해석하지 않았다. 두 entry의 실제 Node 조건부 package exports를 own consumer fixture에서 로드해 확인했다.

PROVENANCE는 fork/upstream URL·Git eb3·source R706·patched identity·MIT·pnpm11.5.0과4개 source hash를 기록한다. BUILDING은 full checkout의 Node24/pnpm11.5.0 install→build→unit→browser→pack recipe와 비공식 downstream 후보임을 명시한다. package 자체가 단독 source workspace 전체라고 주장하지 않는다.

생산 스크립트는 publishConfig의 dist target을 사용하고 workspace deps를 공개 버전으로 변환하며 source를 동봉한다. pnpm normalizer가 build metadata를 없애는 문제를 피하려 verified manifest를 GNU tar/gzip으로 묶고 기존 후보 파일을 overwrite하지 않는다. 실제 f97에는 요구 full version과 같은 public deps가 들어 있다. 이번 검토에서 새로 producer를 실행해 후보를 다시 만들지는 않았다. 이후 producer/script/delivery metadata 변경은 formal2에서 별도 확인할 대상이다.

## 4. B가 직접 실행한 actual-packed regression

R706의 원본26개 unit assertion을 그대로 사용하고, **scope import만 실제 package exports로 연결**했다. ref-stability helper는 같은 Git source를 사용했다. callback/timeout/assertion을 약화하거나 retry를 넣지 않았다. CJS와 ESM 각각 별도 actual package consumer를 만들었다. actual NPM 새 install은 하지 않았고 그 차이를 숨기지 않는다.

| actual package/loader | 직접 결과 |
|---|---|
| 보존 registry stock / CJS | **20 PASS / 6 FAIL** |
| 보존 registry stock / ESM | **20 PASS / 6 FAIL** |
| f97 fixed / CJS | **26 PASS, skip0/retry0** |
| f97 fixed / ESM | **26 PASS, skip0/retry0** |
| B 독립 empty/nested CJS 대조 | **4 PASS** |

stock의6개 실패는 container 역방향 경계4개와 IME2개다. source-before22/4 및 browser-before5/4 인계와 모순된 집계가 아니라 **registry와 Git base의 IME 차이를 반영**한다.

직접 actual-packed26은 loop/trapped 조합·disabled/hidden/negative tabindex·branch 등록·내부 blur·stable ref·unmount timer/restore·props/asChild를 확인한다. 추가4개는 empty에서 loop/trap/neither의 preventDefault 경계와, nested untrapped scope가 outer를 pause하고 닫힌 뒤 opener 복귀·outer reverse handling 재개를 확인했다. candidate 탐색·paused guard·restore가 container 수정으로 대체되거나 삭제되지 않았음을 actual engine에서 확인했다.

부모의 actual NPM install JSON도 별도로 읽었다: full version, lock의 같은 SRI, CJS/ESM5 exports 및 exit0. 이는 부모의 설치 증거이며 B가 npm ci를 새로 실행한 결과가 아니다. B의 exports/behavior fixture와 구분해 저장했다.

**actual packed browser 및 Pinvi 원본 app의 C10 설치 회귀는 B NOT_RUN.** source browser9 PASS는 부모 인계이며 actual-packed browser9 PASS로 바꿔 쓰지 않는다. 이 package 수준 결과로 consumer raw의 Pinvi 실패를 소급 삭제하지 않는다.

## 5. R706 CI와 조건

GitHub 직접 API에서 R706 연결 run43070580672/job130697032387은 **CANCELLED**다. install/build/lint/type/format/unit26은 success, Playwright 설치도 success였지만 실제 browser 실행은 cancelled, pack은 skipped다. upload success가 pack 생성 성공을 의미하지 않는다. 별도 Build workflow도 cancelled, SSR build/Chromatic success는 별개로 기록한다.

실제 checkout은 PR 합성 merge **`71b7d10c7b8c5e028666ca2db349169021f477ed`**였다. compare API로 R706 대비 merge_base=R706, ahead1/behind0, files=[]/too_large=null을 확인했다. 따라서 source 내용 연결은 인정하지만 actual HEAD가 R706였다고 잘못 적지 않는다.

원 workflow는 pinned pnpm lock 설치·관계 package build·lint/type/format·retry0 unit·browser·pack 순서를 갖는다. current cc 및 이후 CI-only/producer/delivery 추가를 R706에 혼합하지 않았다. 최종 새 head CI의 완료와 이번 범위 밖 delta 확인이 남으므로 **overall gate CONDITIONAL**이다. 이는 새 source/package Pn finding이 있다는 뜻이 아니다.

## 6. 명령·증거·보존

PowerShell workdir C:\ → wsl.exe bash로 실행했다. 주요 방법:

```bash
sha256sum review-manifest-radix-focus-scope-1.json
git rev-parse 706e27aaf87bda2df7bbb9da60cc01cebc9ff064^{commit}
git diff eb3a2b7091293e27df8f9ba906632d8daa3d81a3 706e27aaf87bda2df7bbb9da60cc01cebc9ff064
python3 -B audit.py
node consumers/{stock,fixed}/probe.{cjs,mjs}
SCOPE_CONSUMER=<own consumer> node <Pinvi vitest> run --config <own config> --configLoader bundle --no-cache --fsModuleCachePath <own tmp> --no-file-parallelism --maxWorkers 1
```

GitHub calls: commit_workflow_runs(R706), workflow_run_jobs(43070580672), workflow_job_logs(130697032387), compare_commits(R706,71b7). registry 읽기는 기존 pin의 작은 tgz를 읽어 hash를 대조한 것으로 install/갱신이 아니다。

evidence: `review-B-radix-focus-scope-final-1-evidence/`. manifest, stock receipt·registry 대조, source/dist diff, actual export probe, CJS/ESM red-green 로그, empty/nested 시험, 부모 NPM receipt, CI 상태·checkout 대조를 보존했다.

**최종: source/package PASS, 신규 finding0, 전체 gate CONDITIONAL.** consumer/새 common 정책·C10 metadata·모든 supported React 버전·새 producer·실제 packed browser/app 배포는 별도 범위다. R706/f97/stock 파일·기존 원문을 수정하지 않았다. 임시 fixture/cache만 정리하고 타인 modules/cache는 보존한다.
