# COMMON7 / C11 — 원 reviewer B 독립 최종 제한 delta

- Reviewer B / Epicurus, packaging/dependency/platform/security/license/release·CI 전문. 구현 비참여.
- Run ID `Epicurus-B-common7-20261111T185330Z`, 시작 UTC `2026-11-11T18:53:33.406332+00:00`, 종료 UTC `2026-11-11T18:59:44.747955+00:00`.
- 불변 입력 `review-manifest-common-7.json`, 실제 관찰 SHA256 `623ff78af00acc287d215a4684267104d8dca1c7b20228d147089b5dd2986ae6` (시작/종료 동일).
- 관찰 HEAD **`2d4579b4cb90a29fd6a3a50b6ceaa1fab2b3db39`**, producer **`a35481349d6747b4f13b958ae64d9c0bbd0b5413`**, 이전 COMMON6 **`2d70461a7873d73ec2b278709cef1fba832134cc`**, Doctor 수정 **`5715e94fc630ec117156120551affa0f851eb3bb`**.
- 본인 detached worktree `/tmp/review-b-common7-20261111T185330Z`를 사용했고 시작/종료 HEAD 및 clean `git status --porcelain`을 확인했다. 본인 node_modules overlay는 기존 dependency를 읽기 참조한다. Git object·불변 checkout만 source 감사에 사용했다. `docs/reviews`·상대 raw/verdict는 열지 않았다. source edit·대형 install·재pack·타인 cache 삭제 없음.

## Verdict

**PASS — COMMON7 source·C11 actual metadata/artifact·exact CI 제한 범위. 신규 finding 0건. B-P1-11 FIXED 재확인.** exact 최종 head의 frontend/packages/browser 및 나머지 필수 workflow/job 완료를 직접 관찰했다.

이 판정은 소비자 앱의 최종 source/CI/브라우저/배포 승인을 포함하지 않는다. 기존 COMMON6 원문의 BLOCK과 당시 실제 CI 실패 기록은 수정하지 않는다.

## 본인 finding closure

| finding | disposition | 독립 근거 |
|---|---|---|
| B-P1-11 / 필수 Doctor gate 실패 | **FIXED** | 별도571 closure의 red3warnings/exit1→green80files/0issues/exit0; 현재 exact2d4579에서도 같은 명령 exit0, exact frontend CI도 성공 |
| 과거 COMMON4 B-P1-08/09/10, 초기11 및 own tokens 고지 P3, f864 gzip delta | 기존 FIXED/PASS 유지 | 이번에 해당 code/runtime/license/scanner를 바꾸지 않았고 최종 exact CI 확인. 과거 원문을 다시 쓰지 않음 |

571의 helper가 exact 최종 head와 byte-identical이다. `.github/workflows/frontend.yml` 및 Doctor script/config의 완화나 ignore 추가는 없다. 본인이 `packages/ui`에서 `node ../../node_modules/react-doctor/bin/react-doctor.js --scope full --no-score --no-telemetry --blocking warning .`를 실행해 80files/0issues/exit0을 다시 확인했다. source상의 Set/Map lookup 수정과 gate 통과를 구분하지 않고 함께 확인했다.

## 제한 diff·schema·정책·실제 7개 artifact

- COMMON6 이후 제품 변경은 이미 검증한 helper571과 Scope의 고유 **fix.1→fix.2** pin/metadata다. generic checker/schema/generator, 양쪽 배포 checker, 두 정책 test 파일, CI workflow는 COMMON6와 byte-identical임을 직접 비교했다. COMMON6 기능175/추가29/schema/회귀의 결론을 보존하고 전체 옛 감사를 반복하지 않았다.
- root·smoke·example의 package/lock, root policy 및 UI/tokens policy **9개 JSON**을 의미 단위로 비교했다. 변경은 승인된 Scope full version/file 경로/SRI와 C11 UI/tokens SRI뿐이며 그 밖의 dependency metadata·runtime section·override·profile은 같다. 중복 JSON key도 없다.
- 실제 `versions.json`의 npm exact 축은 `1.3.1+kortravel.fix.2`, preferred source175를 가리킨다. `patchedRadixPackages` 및 공식 package stem·artifact 연결은 유지되고 web runtimeRequired에 Scope가 남아 있다. 모바일에 Scope를 새로 강제하지 않는다.
- source producer a354813과 최종 head의 정책·schema·helper·test·checker 관련 파일이 같다. final `frontend-artifacts.json`과 실제 `integration-11-review/common-artifacts.json`의 packages는 formal manifest의 **7개 entry와 정확히 같다**.
- 실제 7tgz를 읽어 각각 전체 SRI·package name·version을 검증했다. C10→C11 UI94 중93, tokens25 중24, 합계 **117개 regular file bytes 동일**이며 바뀐 것은 각 package의 **dependency-policy.json 총2개**다. checker/runtime/CSS/package metadata/LICENSE/NOTICE/exports의 변경은 없다.
- UI SRI `sha512-BsRRdnJUp6FQ2KWkXtINb7IkrxxwnWFlLP/oVlNN4UXBKren7uTlnYT4iJsdaO98iA4Tn2EMPX06eT2uB5jEDA==`.
- tokens SRI `sha512-85mqNJXqhTlA4RbtKUhmzx6rH6mOOeNmsXTJtCetQ5y8njLy+5XLZbdT6j1tf3ME9XQA6X63Ah4kmuLdqEZHbA==`.
- LightningCSS fix.4 및 VWorld core1.0.1/web1.0.3/RN1.0.1 네 tgz는 C10과 byte-identical이다. 과거 source/license 고지 검증을 같은 bytes에 연결한다.
- 외부 Scope runtime은 실제로 바뀐다. C11 tgz는 별도 본인 Scope2 PASS의 **33511bytes / SHA256 `1ca04870692565c243130d99c3dba91f3ac853ab2ec9538fc7b658b17fb7b49a`**와 byte-identical이며 source175/fix.2 full version이다. `vendor/radix-focus-scope-provenance-fix2.json`은 tar 내부 PROVENANCE의 정확한 사본이다. 기존 f97/fix.1은 재발행하거나 덮어쓰지 않았다.

## 직접 검증

| 검사 | 본인 실행 결과 |
|---|---|
| 실제 7 artifact SRI·identity 및 117파일 비교 | PASS |
| 실제 C11 metadata를 쓰는 bounded checker probe | **29개 기대 결과 일치**: 양성1 + 7개별 direct-lock bytes/local-ledger+lock 동시위조/nested optional copy/peer alias 변조 28개 거부 |
| Python registry/schema | **101 PASS**, 9.999초 |
| generator/문서 계약 | **6 PASS**, 0.624초 |
| `sync_frontend_policy.mjs --check` | exit0 |
| actual root/smoke/example prepare | exit0. 세 lock의 Scope/CSS version/SRI/resolved, root dev·Next runtime section, override 및 모든 설치 copy를 대조 |
| mandatory Doctor | **80files/0issues/exit0** |

probe는 실제 C11 archive bytes와 metadata를 본인 bounded fixture에 넣어 checker를 실행한 것이다. 실제 7개 소비자 앱을 새로 설치한 것이라는 뜻이 아니다. 원장만 바꾸거나 버전 문자열만 맞춰 다른 bytes를 통과시키는 경로도 거부했다.

빌려 읽은 현재 common module의 Scope dist6 파일은 이번 frozen fix.2 archive와 모두 같다. stock baseline으로 기존 common module을 사용하지 않았다. old fix.1/f97와 fix.2의 원본 동작 구분 및 실제 packed CJS/ESM 32PASS6FAIL→38PASS는 별도 Scope2 원문에 보존한다.

## Exact 원격 CI — source와 actual packed bytes

최종 직접 API 재조회 결과는 다음과 같다.

| workflow / job | 결론 |
|---|---|
| frontend run43081533300 / job130735053365 | **SUCCESS** |
| docs run43081533139 | **SUCCESS** |
| docs130735054161 / versions130735054152 / secret130735053922 | 모두 SUCCESS |
| Linux tools130735053963 / Windows tools130735053548 | 모두 SUCCESS |
| packages130735053710 | **SUCCESS** |
| workflows selftest run43081533768 | SUCCESS |
| python-package run43081533181 | SUCCESS |

즉 exact 최종 head의 **4개 workflow와 docs 산하6개 job 모두 SUCCESS**다. frontend는 PR 합성 merge `a7ed7029c6b86d90485ced9644dc8477d80891cb`를 검사했다. GitHub compare는 exact2d4579를 merge base로 ahead1/behind0/files0이므로 같은 tree임을 독립 확인했다. docs/packages/tools는 exact2d4579를 명시 checkout하고 source SHA를 검사한다.

[실제 packages job130735053710](https://github.com/digitie/kor-travel-common/actions/runs/43081533139/job/130735053710) 로그에서 다음을 직접 읽었다: Playwright1.65.0/Chromium158.0.8127.18 launch, UI101·정책175·tokens9, webpack/Turbopack build, **새 packed browser65 PASS(46.2s)**, 위 C11 UI/tokens의 **전체 SRI 출력 일치**. Scope2 vendor/lock을 쓰는 exact 새 실행이며 C10의 65개 성공을 재사용하지 않았다. 앱 Pinvi export/배포 결과로 확대하지 않는다.

[frontend job130735053365](https://github.com/digitie/kor-travel-common/actions/runs/43081533300/job/130735053365) 로그에서도 Doctor80files/No issues와 이후 계약 검사 완료를 직접 확인했다. 따라서 본인이 찾았던 필수 gate 회귀의 local 수정과 exact final CI 성공이 연결된다.

집계는 환경별로 분리한다. 부모 로컬 handoff의 도구400은 **399PASS/1SKIP**이지만 본인 이번 로컬에서 전체400을 반복하지 않았다. 실제 원격 Linux/docs 로그는 **400 실행/397PASS/3SKIP**, Windows 로그는 **400 실행/398PASS/2SKIP**이다. 원격 skip을 pass로 집계하지 않는다. 기존 optional/플랫폼 조건이 있는 test suite이며 개별 skip 사유는 non-verbose 로그에 나오지 않으므로 원격에서도1skip만 있다고 추정하지 않는다. 직접 읽은 원격 scanner는1380files/findings0(예외32/4), links831documents/3152targets/errors0이다.

## 한계·인계·원문 보존

본인은 이번 제한 delta에서 새 npm clean install/재pack/전체 로컬175·400·UI101·tokens9·browser65를 반복하지 않았다. 본인 실행은 위 metadata/29probe/schema101/generator6/prepare/Doctor이며, 나머지 exact CI는 원격 API와 실제 로그의 직접 관찰이다. 이전 COMMON6 및 Scope2의 독립 검증은 원문의 scope대로 연결했다.

기존 COMMON6 raw BLOCK SHA256 `73d7ca645d6f3286a7e5e2fdb3ac9cfd26737607ca0ae4eb21f05a65ee38e0df`, Doctor571 delta SHA256 `bb70f83ed568877904ac7962b70391817850d25eed89ce5c68e783735d2f6f12`, Scope2 raw SHA256 `314713873ae382352e06d08fad53d3cf786255b316e179d735004f78bceb04b6`가 그대로다. 기존 모든 본인 raw hash도 대조했다.

B 소비자1 Map 계약/문서 및 Pinvi focus의3 finding은 **최종 앱 불변 delta의 본인 재검증 전까지 OPEN 유지**다. Scope2 source 수정과 common C11 browser 통과만으로 앱 finding을 닫지 않는다. Manager 새 backend/SDK 및 나머지 소비자 후속 fix는 별도 formal input이다. 실제 운영 lifecycle·배포·앱 merge 승인도 이번 범위 밖이다.

증거는 `review-B-common-final-7-evidence/`의 source snapshot/diff, actual7 probe/audit script와 결과, 본인 실행 log, 원격 API/log 발췌와 최종 상태, old raw hash 및 명령/시간 metadata에 보존했다. 증거별 digest는 `SHA256SUMS.json`이다. 본인 임시 worktree만 정리했다.
