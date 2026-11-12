# 원 reviewer A — COMMON7 / 최종 C11 독립 delta 검토

- runid `Mill-A-Common7-C11`, 원 A(Mill), frontend/accessibility. 구현 비참여, 읽기 전용. 상대 raw/verdict 미열람, docs/reviews를 source 감사에서 제외.
- 직접 metadata 검사 시작 UTC `2026-11-11T18:55:25.379172+00:00`; source 최종 관찰 `2026-11-11T19:01:24.700743+00:00`. CI 최종 조회 시각은 ci-observation.json에 보존.
- immutable input `review-manifest-common-7.json`, 실제 SHA256 **623ff78af00acc287d215a4684267104d8dca1c7b20228d147089b5dd2986ae6** 일치.
- exact common **2d4579b4cb90a29fd6a3a50b6ceaa1fab2b3db39**, producer **a35481349d6747b4f13b958ae64d9c0bbd0b5413**.
- Git show로 exact source metadata·helper·registry·문서를 자기 `/tmp/review-A-common7` capsule에 복원했다. 공유 workingtree는 source 입력으로 사용하지 않았으며, 최종 관찰 시 shared HEAD도 exact2d457/clean였다. fixture의 negative lock 변조는 자기 capsule에서만 했다.

**Verdict: PASS(이 Common7/C11 source·pack·policy·정확 CI 범위). 원 A-P2-11 FIXED. 신규 P0/P1/P2/P3=0.** Scope2 원 A finding도 별도 동일 reviewer raw에서 FIXED/PASS 확인 후 연결했다. 소비자 최종 app/head·Manager 새 SDK·실제 이미지 배포 승인은 별도다. COMMON6 exact2d704의 CONDITIONAL/실패 기록을 수정하지 않았다.

## 1. 이미 확인한 일반 정책과 이번 delta

원 A COMMON6 기능 검토 결과는 유지한다. 직접 실행했던 policy175, Python399PASS/1SKIP, 미래 engine/schema/generator·linked optional alias 공격 결과를 무의미하게 다시 반복하지 않았다. **tools checker/Python schema/generator 및 UI/tokens shipped checker가 Common6 exact bytes와 같음**을 이번에 Git blob으로 확인했다.

Doctor 수정 helper는 **5715e94fc630ec117156120551affa0f851eb3bb와 byte 동일**하다. 원 A가 따로 보존한 `review-A-common-doctor-postfix-571.md`의 직접 동일 명령80files/0issues/exit0, helper41, 실제3 locks 및 negative stock 공격 PASS를 유지한다. 이번 exact head의 remote frontend도 동일 Doctor80/0issue와 SUCCESS를 직접 확인했다. config/rule suppression으로 우회한 것이 아니다.

C10→C11 실제 tar member 비교:

| 패키지 | regular files | 동일 | 변경 |
|---|---:|---:|---|
| @kor-travel/ui | 94 | 93 | dependency-policy.json |
| @kor-travel/tokens | 25 | 24 | dependency-policy.json |

합계 **117파일 동일**. 두 policy JSON의 구조적 diff도 각각 **`versions/@radix-ui/react-focus-scope`의 fix.1→fix.2 한 값뿐**이다. checker/runtime/CSS/public package metadata는 동일하다. shipped policy는 exact2d457 생성 정책과 byte 일치한다. 외부 Scope1→2 runtime은 실제 변경이므로 이 동일성만으로 modal acceptance를 대신하지 않았다.

producer a354→head2d457의 검토 관련 packages/checker/schema/generator/versions 경로는 smoke package-lock의 **최종 UI/tokens SRI 2개**만 달라진다. 이를 전체 source 무차이라고 부르지 않는다. 실제 diff는 final-observations.json에 보존했다.

## 2. 실제7 metadata·bytes와 Scope2 연결

`artifacts/integration-11-review/common-artifacts.json`, immutable manifest artifact, exact head frontend-artifacts.json의 package entries가 같다. 7개의 tarball을 직접 읽어 name/version/크기/SHA512를 계산했고 모두 일치했다. C11 UI/tokens 원장만 새 SRI이고 CSS/VWorld bytes는 이전 검토 그대로다.

| 패키지 | 버전 | SHA256 |
|---|---|---|
| @kor-travel/ui | 0.2.0 | 16b4c213453fb02b527f8e4ae673a703e4ba3808538ae6fb24f70bdda770d213 |
| @kor-travel/tokens | 0.1.1 | 7e88aaf70b93fed953198779fd17a003e327499e686794fd5f647b23cc325ad3 |
| lightningcss | 1.33.0+nativecss.fix.4 | 12c8326428a56e38231f7b5b376df0c6882e3492da794f3499269628edcaccf0 |
| vworld-map-core | 1.0.1 | 36d3ba16a3ba65f7a460db6027c07e29821f2795b15a526413949210f0ce92b6 |
| vworld-map-web | 1.0.3 | 1ab9af8794979a5a19e5ac635cd04a9e87b9847058eaf4e9df743143b8ad4104 |
| vworld-map-rn | 1.0.1 | 352307615edad047cc100cff6a39c625e778f77434b48475c9930e25ca7b6404 |
| @radix-ui/react-focus-scope | 1.3.1+kortravel.fix.2 | 1ca04870692565c243130d99c3dba91f3ac853ab2ec9538fc7b658b17fb7b49a |

C11 Scope는33511 bytes, 별도 formal Scope2 source175/1ca와 같다. 원 reviewer A `review-A-radix-focus-scope-final-2.md`에서 source38 red6/green38, 실제 fixed pack browser20, Node22/24 ESM+CJS5 exports, source/hash/license/API 및175/01 exact CI를 본인이 확인했다. **A-SCOPE-P2-01 FIXED**다. 이 Common7 원문이 peer verdict에 의존한 closure가 아니다.

기존 common modules를 readonly 참조했으며 새 install/repack은 하지 않았다. 현재 설치 CSS의19파일과 Scope2의15파일도 해당 archive와 전부 byte 일치, Scope version은 실제1.3.1+kortravel.fix.2다. current commonRoot를 stock baseline으로 사용하지 않았다.

## 3. 실제3 locks·정책 적용 직접 probe

- exact source7 registry를 Python Registry.load로 읽었다. generator `node tools/sync_frontend_policy.mjs --check` exit0. 도구 source는 검증된 동일 bytes이며 실제 입력은 source7의 Scope2 metadata다.
- root/smoke/example의 실제 package.json·package-lock.json을 복제하여 **새 helper의 --css-only 경로**를 직접 실행했다. CSS fix4/Scope2 두 엔진의 canonical version/filename/SHA512, direct section/override, lock 모든 copy를 검증한 뒤 두 Next 경로로 실제 bytes를 복사했고 exit0. 기존 여섯 manifest/lock pin은 불변이다.
- 마지막 example lock에 중첩 **이전 fix.1**을 삽입했다. 같은 기본 SemVer라도 metadata가 다르므로 exit1(`lock 전이 버전 불일치`). 실패 전후 전체 pin과 이미 복사된 엔진 bytes는 불변이다. fixture의 의도적 변조를 source 변경으로 간주하지 않는다.

`audit.json`에 전체7 SRI/hash,117파일 비교, 도구 동일성, 실제3경로 및 negative 결과와 실제 module provenance를 남겼다. source7 전체 tools400·UI101·tokens9를 reviewer 로컬에서 다시 실행한 것은 **이번 NOT_RUN**이며, 아래 exact source CI와 이전 동일 코드 직접 검증을 구분하여 사용했다.

## 4. 새 exact2d457 CI 직접 확인

GitHub connector로 exact commit runs/jobs와 완료된 frontend/packages job logs를 직접 읽었다. 부모가 알려준 SUCCESS를 검증 없이 복사하지 않았다. logs의 checkout/SOURCE_SHA도 exact head다.

| exact workflow | 직접 최종 결과 |
|---|---|
| common frontend43081533300 | SUCCESS |
| docs43081533139 | SUCCESS, 하위6 jobs 모두SUCCESS |
| workflows selftest43081533768 | SUCCESS |
| python-package43081533181 | SUCCESS |

[docs run43081533139](https://github.com/digitie/kor-travel-common/actions/runs/43081533139)의 하위 jobs는 Windows130735053548, packages130735053710, secret130735053922, Linux130735053963, versions130735054152, docs130735054161이다. 처음 관찰할 때 진행 중이던 Windows도 최종 조회에서 SUCCESS를 직접 확인했다. source6/00ddd/447 CI를 대입하지 않았다.

[frontend job130735053365](https://github.com/digitie/kor-travel-common/actions/runs/43081533300/job/130735053365)의 새 required gate는 UI101·policy175 뒤 **Doctor80files/0issues**로 성공했다. 원 A-P2-11의 실제 원격 실패 조건도 이제 제거되었다.

[packages job130735053710](https://github.com/digitie/kor-travel-common/actions/runs/43081533139/job/130735053710)은 Playwright1.65.0/Chromium158.0.8127.18 launch, actual fixed engines prepare, UI101/policy175, webpack·Turbopack builds, **새 실제 C11 packed browser65 PASS(46.2초)**, 이후 example Turbopack build와 tarball smoke까지 성공했다. reporter의65를 별도10개 browser로 나누어 부르지 않는다.

이 job에서 직접 출력한 전체 SRI:

```text
@kor-travel/tokens: sha512-85mqNJXqhTlA4RbtKUhmzx6rH6mOOeNmsXTJtCetQ5y8njLy+5XLZbdT6j1tf3ME9XQA6X63Ah4kmuLdqEZHbA==
@kor-travel/ui: sha512-BsRRdnJUp6FQ2KWkXtINb7IkrxxwnWFlLP/oVlNN4UXBKren7uTlnYT4iJsdaO98iA4Tn2EMPX06eT2uB5jEDA==
```

actual C11 archive와 정확히 같다. **C10 packed65를 Scope2 acceptance로 재사용하지 않았다.** 로컬 reviewer의 common full Next65 재실행은 NOT_RUN이며, 위는 새 exact CI의 직접 관찰이다. 별도 own Scope2 packed20과 합쳐 하나의 suite 수치로 만들지 않는다.

증거 `ci-observation.json`, `ci-frontend.log`, `ci-packages.log`. 원 인계의400tools399PASS1SKIP/scans1380zero/links831·3152zero 등 상세 수치는 부모 source7 인계이고, reviewer는 해당 exact jobs SUCCESS를 직접 확인했지만 이 모든 상세 count 로그를 별도로 재집계한 것으로 쓰지 않는다.

## 5. 원 finding dispositions

| 원 A finding | 상태 | 이번 근거/경계 |
|---|---|---|
| 최초 A-P1-01/02, A-P2-01~07, A-P3-01 | FIXED 유지 | 원 A source2 직접 closure; 이 delta에서 해당 UI/runtime/CSS 동일 |
| A-P2-08 table outline transition | FIXED 유지 | 원 A source3 closure; runtime/CSS 동일 |
| A-P2-09 AST import 경로 | FIXED 유지 | 원 A source4 closure; 이번 checker bytes 동일 |
| A-P2-10 gzip member scan | FIXED 유지 | 원 A f864 closure, Common6 source 동일성/400 regression; 이번 도구 변경 범위 밖 |
| A-P2-11 required Doctor | **FIXED** | 원571 직접80/0/exit0 + helper41·실제3 locks; 이번 helper byte 동일 + exact2d457 remote frontend SUCCESS |
| A-SCOPE-P2-01 disabled fieldset | **FIXED** | 원 A 별도 formal Scope2 source175/actual1ca 직접 closure. C11 Scope 동일bytes |

신규 source/pack finding은 없다. 기존 Common6의 조건부/merge gate 실패 원문, Scope1 조건부, 최초 consumer1 BLOCK은 소급 변경하지 않는다.

## 6. Commands / 최종 경계

```text
sha256sum review-manifest-common-7.json
git show 2d4579b4cb90a29fd6a3a50b6ceaa1fab2b3db39:<정책·registry·helper·세NPMmanifest/lock 경로>
# frozen Git blobs를 자기 /tmp/review-A-common7에 복원; root vendor는 exact Git blob, 타인 modules는 readonly
node tools/sync_frontend_policy.mjs --check
# Python: 검증된 동일 Registry source로 source7 versions.json load
node packages/ui/smoke/prepare-lock.mjs --css-only
# 자기 example lock에 fix1 중첩항목 삽입 후 동일 명령 exit1, 전후 hash 비교
# Python tarfile/hashlib: 7 archives, C10→C11 all119regularfiles comparison, 두JSON semantic diff
# Git source571 helper와 source7 byte compare, Common6 checker/schema/generator byte compare
# Git producer a354→head2d457 bounded package diff
# GitHub exact commit runs → jobs → completed frontend/packages raw logs
```

**COMMON7 PASS.** 현재 원 A foundation source/Scope finding OPEN=0, 신규 findings0. 단, 이는 최종 소비자 C11 install·font/map/forms/state·app-specific browser, Pinvi 실제 잔여 suite, Manager 신규 candidate SDK/backend, 이미지 export/production deployment를 승인한 것은 아니다. Geo43/Concierge50/Mapf55 원 source finding closure는 별도 raw로 보존했으며 각 앱의 최종 새 manifest와 실제 운영 효과는 후속 gate다.
