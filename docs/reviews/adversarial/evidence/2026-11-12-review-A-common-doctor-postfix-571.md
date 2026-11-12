# 원 A-P2-11 수정 후 독립 재검토 — common571

- runid: `Mill-A-common-doctor-571-closure`
- 관찰 UTC: `2026-11-11T18:30–18:34Z` (actual-prepare.json의 상세 관찰 `2026-11-11T18:32:51.733524+00:00`).
- 동일 원 reviewer A(Mill), 구현 비참여, source 읽기 전용. 상대 raw/verdict를 열지 않았다.
- 입력: 사용자가 제공한 exact Git `5715e94fc630ec117156120551affa0f851eb3bb`; baseline `2d70461a7873d73ec2b278709cef1fba832134cc`. 별도 새 manifest가 제공되었다고 주장하지 않는다.
- 격리 detached worktree `/tmp/review-A-common-doctor-571`, 검증 후 HEAD571/clean. 기존 module 자식만 읽기 참조, 새 install/repack 없음.

**Verdict: PASS — A-P2-11 FIXED(이 helper source delta 범위).** 신규 P0/P1/P2/P3=0. exact2d COMMON6 CONDITIONAL 원문과 그 CI 실패는 그대로 보존한다. 미push 인계 뒤 최종 C11 exact CI는 이번에 관찰하지 않았으며, Scope fieldset finding은 OPEN이다.

## 확인한 수정과 원 재현

Git whole-tree diff2d→571은 `packages/ui/smoke/prepare-lock.mjs` **한 파일**, 17추가/8삭제다. workflow, Doctor 명령, config, ignore, dependency checker, shipped UI/tokens payload 변경이 아니다. 새 helper의 `:32` 이후 `artifactPackages`/`managedPackages` Set과 `npmAxesByPackage` Map을 loop 밖에서 구성한다. 각 npm axis의 명시적 packages 또는 key fallback을 index하고, 동일 이름이 여러 axis에 나타나면 배열 길이 검증으로 계속 거부한다. non-npm axis는 index하지 않는다.

기존 exact2d 원 A 로컬 `doctor-local.log`와 remote frontend130710770267에서 같은 세 경고·exit1을 재현한 원문은 `review-A-common-final-6.md` 및 그 evidence 디렉터리에 보존되어 있다. 새 exact571에서는 **동일 blocking 명령**으로 직접 실행했다.

```text
npm run doctor --workspace packages/ui
react-doctor --scope full --no-score --no-telemetry --blocking warning .
Scanned 80 files
No issues found!
exit 0
```

같은 80파일 스캔의 실제 개선이다. 작은 목록의 lookup이 사용자 browser 성능 문제였다고 새로 주장하지 않는다. 원 finding은 required gate 실패였으며, rule을 무시하지 않고 해당 명령을 통과시켜 닫았다.

## 회귀·실제 입력 확인

| 직접 실행 | 결과 | 증거 |
|---|---|---|
| required Doctor | 80files/0issues/exit0 | doctor.log |
| helper 전체 node regression | 41 PASS/0 FAIL/0 SKIP | prepare-tests.log |
| 실제 root/smoke/example3 NPM locks 복제본 | prepare exit0, pin 불변 | actual-prepare.json |
| CSS fix4 + Scope fix1의 실제 4개 대상 복사 | 원 vendor SHA256 모두 일치 | actual-prepare.json |
| 마지막 example lock에 중첩 stock Scope 삽입 | exit1, 모든 pin·기존 복사본 불변 | actual-prepare.json |
| 기존 C10 실제 7개 tarball 재해시 | COMMON6 원 A receipt와 7/7 동일 | actual-prepare.json |

41개에는 alias axis, 중복/없는/unmanaged axis, 원장·bytes 변조, 세 경로 각각의 의존성 section/override/lock 직접 선언, 중첩 버전/integrity/resolved, alias stock 설치 거부 및 실패 때 기존 vendor/lock 보존이 포함된다. helper의 새 Set/Map이 원 검증을 완화한 재현은 없었다.

원래 검증 순서인 **모든 고정 엔진 원장·root bytes와 세 대상 manifest/lock 검증 후 복사**는 유지된다. `--css-only` 호환 경로로 CSS+Scope 두 엔진을 실제로 준비했다. C10 UI/tokens runtime을 다시 빌드하거나 tarball을 변경하지 않았다. 이 파일은 shipped C10 package regular files에 포함되지 않는다.

## 명령·관찰 경계

```text
git worktree add --detach /tmp/review-A-common-doctor-571 5715e94fc630ec117156120551affa0f851eb3bb
git diff --name-only 2d70461a7873d73ec2b278709cef1fba832134cc..HEAD
git diff 2d70461a7873d73ec2b278709cef1fba832134cc..HEAD -- packages/ui/smoke/prepare-lock.mjs
CI=1 NO_COLOR=1 npm run doctor --workspace packages/ui
# cwd packages/ui
node --test test/native-css-policy.node.test.mjs
# exact source config와 3 locks를 자기 /tmp fixture에 복제, 두 root vendor는 읽기 참조 후 helper가 자기 Next vendor에만 복사
node packages/ui/smoke/prepare-lock.mjs --css-only
# 마지막 lock에 stock 전이 copy를 넣고 같은 명령 재실행(exit1), 전후 hash 비교
```

증거 디렉터리: `review-A-common-doctor-postfix-571-evidence/`의 helper-delta.patch, doctor.log, prepare-tests.log, actual-prepare.json. 로컬 Node22.22.2 및 기존 pinned modules를 사용했다. 공유 checkout은 actual-prepare 관찰 당시 HEAD571/clean였고, 검토는 공유 workingtree의 향후 metadata 변경을 포함하지 않는다.

- A-P2-11: **FIXED**.
- A-SCOPE-P2-01: **OPEN**, 사용자 수락한 원 library disabled fieldset/legend 수정과 새 fix2 code/pack formal input에서 별도 재확인.
- 최종 C11 새 source/7 metadata/정확 원격 frontend CI: **NOT_RUN / 후속 입력 대기**. 요청시 미push라는 인계와 local PASS를 remote SUCCESS로 바꾸지 않는다.
- COMMON6 exact2d 원문은 **CONDITIONAL 그대로**. 이 후속 bounded PASS가 과거 실패나 소비자·배포 gate를 소급 삭제하지 않는다.
