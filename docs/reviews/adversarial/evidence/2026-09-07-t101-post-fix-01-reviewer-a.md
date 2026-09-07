# T-101 post-fix 독립 적대적 리뷰 A 원본

- 실행 ID: A-T101-POST-20260907-221508
- 판정: PASS. 최초 A finding 8건(원 심각도 P1 1건·P2 7건) 모두 FIXED. 신규 P0/P1/P2/P3 0건.
- 검토 후보: 4c33a5d951e32df0c2170b7a865f324d122dbe05
- 후보 tree: aa81767746cb40641e43397af19082456aaacb3b
- 수정 delta base: f8894e293ca9677f457011197052cd55dbdc9696
- PR 원 base: cf2c610cecfa7a9b8f7a035c9529d7a296e27527
- 격리: F:/dev/kor-travel-common-wt/review-t101-post-a, detached worktree.
- 시작: 2026-09-07 22:15:08.061 KST. 종료: 2026-09-07 22:22:08.491 KST.
- 시작·종료 HEAD/tree는 위 후보와 일치했고 git status --porcelain=v1 출력은 모두 비어 있었다.
- 상대 reviewer의 이번 결과는 열람하거나 요청하지 않았다. 후보 파일·소비자 저장소·source .git/config를 수정하지 않았고 commit/push/publish하지 않았다.

## 요청과 검토 범위

전달 요청: 새 immutable candidate를 detached로 검토하고, 최초 A의 DTCG 2025.10 구조/타입·$root 충돌·Tailwind v4 z·v3 transitionTimingFunction·dark-media OS variant·scoped color-scheme·profile/media 정본 동기화·dark 전수 map 시험 finding이 닫혔는지 독립 재현한다. 양 OS pack/install와 기존 정적 gate를 SHA에 귀속해 기록하고 P0–P3 disposition/verdict를 확정한다. 후보 수정·commit·push 및 reviewer B 결과 열람은 금지한다. 후속 메시지로 정확한 full SHA 4c33a5d951e32df0c2170b7a865f324d122dbe05가 확정됐다.

전체 수정 delta 17파일(+3332/-876)을 확인했다. generator·생성물·CSS·시험·CI 및 architecture/standards/T-101/T-102 문서를 대조했다. tokens.css·package.json·기존 Python tools/tests는 초기 후보와 동일함을 git diff --exit-code로 확인했다. 초기 리뷰의 고정 map 원천 조사 결과는 이 동일성 범위에서 재사용하고, 새 후보의 light/dark 전수 시험은 직접 실행했다.

읽기 중 main checkout build.mjs를 한 차례 경로 착오로 열었으나 즉시 후보 blob과 hash-object를 대조해 둘 다 9d574f2d0e217384260006f26b674ad5ed909423임을 확인했다. 이후 실제 모든 실행은 detached 후보 또는 그 임시 사본에서 수행했다.

## 실제 검증

Windows: Python 3.14.3, Node v25.9.0, npm 11.12.1. WSL: uv Python 3.11.15, Node v22.22.2, npm 11.19.1. Windows npm ci의 Node engine 경고는 기록했으며 요구 Node 버전 일치로 세지 않았다. 양 OS의 패키지 build/test/pack/install 및 변조는 임시 패키지 사본에서만 실행했다.

| 검증 | Windows | WSL |
|---|---|---|
| Python unittest discover 전체 | 203 tests / 61.866초 / OK / skip 0 | 203 tests / 40.649초 / OK / skip 0 |
| npm ci → check → build → check → test | 모두 exit 0, 7 tests / skip 0 | 모두 exit 0, 7 tests / skip 0 |
| npm pack → 임시 프로젝트 install | exit 0 | exit 0 |
| 설치 후 공개 subpath 11개 resolve, ESM tokenValues 44개 | 모두 성공 | 모두 성공 |
| 공식 DTCG JSON Schema 검사 | light 44·dark extension 44·alias 대상·$root 충돌 모두 PASS | 동일 PASS |
| dark warning-tint 30%→33% 변조 | 테스트 exit 1, 전수 dark map 및 media 시험 실패 | 동일 exit 1, 5 pass / 2 fail |
| dist/tokens.json을 {}로 변조 후 선행 check | exit 1 | exit 1 |
| 정본 radius 0.375rem→0.625rem, dark brand 76%→77% 변조 후 build/check | 모두 0; profile 참조 유지, radius 생성값 0.625rem, media 이전값 없음 | 동일 |
| plan | task 106 / 오류 0 | 동일 |
| 문서 링크 | 문서 355 / local targets 2306 / 오류 0 | 동일 |
| SPDX | 41파일 / 오류 0 | 동일 |
| secret / prod redaction | 각각 466파일 / 발견 0 / 예외 0 | 동일 |
| check_versions --self-check | exit 0 | exit 0 |
| PR base..HEAD git diff --check | exit 0 | exit 0 |

Windows 실제 Tailwind 4.3.3/@tailwindcss/node 컴파일과 Tailwind 3.4.19/postcss 8.5.8 컴파일을 수행했다. v4 z-kt-nav/z-kt-modal/ease-kt-out/duration-kt-fast, v3 ease-kt-out/ease-kt-in/duration-kt-fast/bg-kt-brand/z-kt-modal이 모두 CSS에 생성됐다.

Windows Playwright Chromium에서 OS dark를 에뮬레이션하고 html class를 비운 채 bg-kt-surface-page dark:bg-kt-brand를 렌더링했다. root color-scheme=dark, 실제 배경 oklch(0.76 0.085 169)로 brand dark 값이 적용됐다. scoped base + dark-class 조합의 root/surface/input color-scheme은 모두 dark였다.

진단 probe에서 bg-primary와 border-input의 Tailwind utility 미생성도 출력됐지만 이번 계약의 shadcn.css는 의미 alias 변수 제공이며 이 이름의 utility 매핑을 T-101 수용 기준이 요구하지 않는다. 이 출력은 실패로 집계하지 않았다.

## 재현 명령과 보존 probe

기본 실행 위치는 detached 후보이다. 아래 helper는 main .git/codex-audit에만 있으며 후보 밖의 임시 사본을 사용한다.

    python -B -X utf8 -m unittest discover -s tests -q
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-post-a-package.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-post-a-gates.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-post-a-dtcg.py
    python -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/t101-a-values.py

WSL에서는 /mnt/f/dev/kor-travel-common-wt/review-t101-post-a로 이동하고 같은 helper의 /mnt/f 경로를 uv run --no-project --python 3.11 python -B -X utf8로 실행했다. 전체 unittest와 DTCG 검사는 --with jsonschema==4.26.0을 추가했다. WSL 정적 gate helper는 GIT_DIR/GIT_WORK_TREE 환경변수만 지정했으며 source config를 수정하지 않았다.

    cd F:/dev/kor-travel-common/.git/codex-audit/t101-css-a/post-fix
    node probe.mjs

이 CSS fixture에는 후보 packages/tokens 사본이 있고, 생성 compiled-v4.css/compiled-v3.css 및 브라우저 probe가 보존돼 있다.

## 최초 finding disposition

| ID / 원 심각도 | 후보 위치 | 재현과 판정 |
|---|---|---|
| A-T101-P1-01 / P1 | packages/tokens/scripts/build.mjs:62, :72, :148; dist/tokens.json | FIXED. 숫자·dimension·duration·cubicBezier·color·fontFamily·shadow가 공식 2025.10 schema를 통과한다. $root를 건너뛰지 않고 44개 light 토큰을 세었고, dark extension 44개를 각 타입의 토큰으로 재검증했다. brand root와 hover가 유효한 group/child로 공존한다. 모든 현존 light alias 대상과 타입도 확인했다. |
| A-T101-P2-02 / P2 | packages/tokens/theme.css:77 | FIXED. @utility z-kt-*가 추가됐고 실제 v4 컴파일에서 z-kt-nav/z-kt-modal이 생성된다. |
| A-T101-P2-03 / P2 | packages/tokens/scripts/build.mjs:224 | FIXED. transitionTimingFunction으로 생성하며 실제 v3 컴파일에서 ease-kt-out/ease-kt-in이 생성된다. |
| A-T101-P2-04 / P2 | packages/tokens/dark-media.css; docs/standards/design-tokens.md:172 | FIXED. class custom variant를 제거해 Tailwind 기본 media variant를 보존한다. OS dark·html class 없음에서 실제 dark:bg-kt-brand 계산값이 brand dark와 일치한다. architecture 및 frontend-stack 정본도 같은 계약을 설명한다. |
| A-T101-P2-05 / P2 | packages/tokens/base.scoped.css:6 | FIXED. scoped light 강제 선언이 제거됐다. root/surface/input의 계산 color-scheme이 모두 dark다. |
| A-T101-P2-06 / P2 | packages/tokens/scripts/build.mjs:157, :242 | FIXED. profile radius는 {radius.control} 참조이며 dark-media를 정본에서 생성/check한다. 양 OS 정본 변조 후 typed radius와 media가 즉시 갱신되고 이전 media 값이 남지 않는다. |
| A-T101-P2-07 / P2 | .github/workflows/docs.yml:183 | FIXED. build 전 check가 추가됐다. 변조 dist에 대해 선행 check가 양 OS에서 exit 1이며 CI의 실패 중단 대상으로 실행된다. build 후 check와 git diff도 유지된다. |
| A-T101-P2-08 / P2 | packages/tokens/test/values.test.mjs:131 | FIXED. light/dark 44개 전수 deepEqual이다. 이전에 통과하던 dark warning-tint 30%→33% 변조가 두 OS 모두 실제 실패한다. |

package probe의 ci-build/ci-check/ci-test 라벨은 선행 check 실패 이후에도 진단 목적으로 계속 실행한 명령이며 이 세 exit 0을 실제 CI 전체 성공으로 세지 않았다. 새 CI는 그 앞의 check exit 1에서 중단한다. 또한 값 변조 시험의 마지막 generator check exit 0은 테스트가 생성물을 재생성한 후의 결과이며, 해당 반례의 test exit 1을 성공으로 바꾸지 않는다.

## 공식 규격과 CI 근거

[DTCG 2025.10 형식 정본](https://www.designtokens.org/tr/2025.10/format/)과 [공식 JSON Schema](https://www.designtokens.org/schemas/2025.10/format.json)를 2026-09-07에 확인했다. schema 다운로드 사본은 t101-dtcg-2025-10-schema.json이며 SHA256은 32e93b780e4e4bca778d0780cb797a560deedc470c608af16576223f7e42915f이다. RefResolver deprecation 경고는 발생했으나 모든 참조가 실제 해결되고 검증이 exit 0으로 끝났다.

[PR CI run 34126309766](https://github.com/digitie/kor-travel-common/actions/runs/34126309766)의 headRefOid가 후보 SHA와 일치함을 gh pr view로 확인했다. docs·tools Ubuntu·tools Windows·secret-scan·check-versions·packages 6개 모두 SUCCESS였다. packages job 실제 로그에서 Node v22.23.1, 생성물 check 2회 clean, tests 7/pass 7을 확인했다. PR 실행을 release/main push 실행으로 대신 세지 않았다.

## NOT_RUN 및 결론의 범위

- NOT_RUN: 실제 소비자 저장소 build/e2e·채택, registry 게시·GitHub Release·태그 생성. 이 리뷰 범위 밖이며 소비자 쓰기는 하지 않았다.
- NOT_RUN: kt_contrast/T-103 이후 gate. 토큰 값 정본은 불변이며 이 gate를 대신 통과로 표시하지 않는다.
- NOT_RUN: local exact Node 22.23.1 양 OS 실행. Windows v25.9.0/WSL v22.22.2에서 직접 확인했고 CI packages의 v22.23.1 성공은 별도로 관찰했다.
- NOT_RUN: WSL 브라우저/Tailwind 네이티브 컴파일. 실제 CSS 컴파일·브라우저 검증은 Windows에서, 양 OS package/build/pack/install/schema/회귀는 각각 실행했다.
- NOT_RUN: A의 실제 release push CI run 관찰. T-101 task 종료의 해당 수용 기준은 coordinator가 exact run/head/source SHA evidence로 별도 채워야 한다. 이 보고서의 PASS는 검토한 수정 코드와 기존 A finding의 종료 판정이며 미실행 task gate를 닫는 기록이 아니다.

독립 verdict는 PASS이며 추가 코드 수정 권고는 없다. 위 8건의 FIXED disposition과 미실행 범위 구분을 유지해 통합 기록에 반영하면 된다.