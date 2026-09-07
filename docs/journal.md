# kor-travel-common 작업 일지

이 문서는 작업 재현 정보(기준선·명령·결과·미실행·도구 fallback·소비 저장소 상태)의 역시간순 기록이다([documentation maintenance §4](runbooks/documentation-maintenance.md)). 최신 항목을 위에 추가하고 기존 항목은 사실 오류 correction 외에 수정하지 않는다. 현재 상태와 다음 작업은 [resume](resume.md)가 정본이다.

## 2026-09-08 (Codex, T-103 구현 시작)

T-103을 `codex/t103-kt-contrast-ux-lint`에서 시작했다. 조사 원문과 현재 `packages/tokens/tokens.css`를 다시 대조해 `tools/kt_contrast.py`(OKLCH·hex·`var()`·alpha 합성·TK-8 27쌍·light/dark·baseline)와 `tools/ux_lint.py`(UX-G9 P1~P8·`--root`·`--token-files`·baseline·diff)를 common 안에 작성했다. ktdm·concierge·geo·airport 조사 스냅샷 오버라이드와 baseline 예제, 회귀 fixture/evidence도 common에만 추가했다.

현재 Windows Python 전체 247 tests, focused T-103 11 tests, 문서 link 394/2410, plan 106, SPDX 56, secret/redaction 526, `git diff --check`가 통과했다. canonical 대비는 light/dark 27쌍 모두 PASS이며 4앱 미달 수치는 [T-103 evidence](evidence/t103-kt-contrast-ux-lint.md)에 기록했다. 소비자 저장소 build/e2e·재사용 workflow selftest는 `NOT_RUN(T-010 및 소비자 task)`. 다음은 동일 immutable candidate에 대한 reviewer A/B 독립 적대적 리뷰다.

## 2026-09-08 (Codex, T-104·T-020·T-021 최종 PASS·PR #17 merge·main CI 완료)

T-104 디자인 토큰 표준과 T-020 pinvi·T-021 concierge·docker-manager GPL-3.0-or-later 결정·요청 문서를 최종 정리했다. 반복 no-go의 근본 원인은 WCAG 일반 텍스트/비텍스트 기준, 조사 재현 오차/검사기 합격 판정, 소비자 license-only PR/후속 코드 채택 evidence, common 완료/외부 gate 완료, chart palette 소유권을 한 gate에 섞은 문서 계약이었다. TK-8·T-103·style-delivery의 4.5:1/3:1 기준과 `±0.03` 재현 오차를 분리하고 반올림 합격을 금지했으며, chart 슬롯은 앱 소유로 전환하고 Breaking/Migration·회귀 시험을 기록했다. T-020/T-021의 DONE은 common 결정·요청 문서 gate만 닫고 외부 LICENSE PR과 소비자 채택은 `OPEN/NOT_RUN`으로 유지한다.

최종 candidate `2ca6b0c491ddcf542d0c77540b78d18ddf100dfb`에서 reviewer A/B가 각각 누적 finding 7건/4건을 모두 FIXED로 확인하고 신규·잔여 P0–P3 0건으로 PASS했다. 원본 SHA256은 A `935C2F57F9FF313307FE5C8498463BD50AC635D99EFAEF6D5E593031A7ABDE0C`, B `0FD0B3BE1E0EB26B90F9CAF3D801FA72FF249163CDB9BB7EEA9779FBBF480685`다. [최종 통합 리뷰](reviews/adversarial/2026-09-08-t104-t020-t021.md)와 [A/B 원본](reviews/adversarial/evidence/2026-09-08-t104-t020-t021-reviewer-a-post-fix-04.md), [B](reviews/adversarial/evidence/2026-09-08-t104-t020-t021-reviewer-b-post-fix-04.md)에 기준선·명령·disposition을 보존했다.

PR #17(`4131c9d`)의 6개 job CI `34168541026`이 성공했고, squash merge SHA는 `c573e7c9477623b5c0e938d7b2fd1962be99cff2`다. merge 후 main CI `34168628049`의 6개 job도 모두 성공했다. 로컬에서는 문서 링크(393/2403, 오류 0), plan(106, 오류 0), SPDX(45, 오류 0), secret/redaction(508, 발견 0), tokens check·7 tests, Python 238 tests OK를 확인했다. T-103 실제 검사기·소비자 build/e2e/시각 검증·외부 LICENSE evidence·npm/PyPI 게시는 `NOT_RUN`이다. 다음 작업은 T-103 READY다.

## 2026-09-08 (Codex, T-102 반복 no-go 근본 원인 수정·최종 PASS·PR #15 merge·main CI 완료)

T-102의 반복 no-go는 reviewer별 판단 차이가 아니라, 초기 checker가 CSS를 변수 정규식과 부분 블록 문자열로만 다뤄 실제 적용 scope·import 변형·Unicode identifier·escape 경계를 브라우저 의미와 다르게 승인한 데서 시작됐다. Windows에서는 lexical 8.3 표기와 canonical 경계를 섞어 정상 fixture를 외부 경로로 오판했고, 진단이 입력 경로·식별자·값을 재출력할 수 있었다. 고정 원천을 다시 대조하기 전에는 map의 `radius-md` control과 weather의 panel 의미도 분리되지 않았다. raw reviewer evidence의 줄바꿈·공백을 immutable bytes로 보존하는 CI 정책도 후보 artifact와 함께 닫지 못해 문서/Windows gate가 반복 실패했다.

`0b50a63`·`ded1631`에서 parser를 지원 문법에 맞춰 fail-closed로 보강하고 direct mode stack, combined selector 중복, Unicode 정의·참조, escape·import·path/redaction 경계를 회귀 시험으로 고정했다. map shim은 control radius를 유지하고 weather 예제는 panel radius·dark shadow·앱 spacing을 소유하며, 원본 provenance를 보존했다. 최종 code candidate `ded1631b81d464ed919d36d73ab9c2a1111d38f4`(tree `41dd1c6551994b62d94a04c8a3c1f8bf98414de7`)에서 A/B final2 원본이 모두 PASS·신규 P0–P3 0건이다([통합 판정](reviews/adversarial/2026-09-08-t102-post-fix-01.md)). 원본 SHA256은 A `735D4718F53B8349A89638D3BCE1D4DF28593BD5418D14B56DA3EC5B3A03C63B`, B `B675AC97A9A9B9574B809008513BC187B0D18DA3368EF63CC66E53A1EDE6ECDA`이며 review archive와 path별 attributes 예외로 bytes를 보존했다.

정확한 candidate CI [34137474603](https://github.com/digitie/kor-travel-common/actions/runs/34137474603)의 docs·tools(Windows/Ubuntu)·packages·secret-scan·check-versions 6개 job이 모두 성공했다. reviewer가 Windows 전체 238 tests·focused alias 35 tests, WSL 전체 235 pass·focused 34 pass(+플랫폼 skip), tokens check/build/test 7개·임시 tarball 19개 파일·install smoke를 확인했다. 소비자 저장소 변경, npm/PyPI 게시, T-461 weather 실교체/6폭 visual diff, T-103·T-104 후속 작업은 `NOT_RUN(범위 또는 후속 task)`로 유지한다. 초기 draft [#14](https://github.com/digitie/kor-travel-common/pull/14)는 같은 source의 기록으로 보존한 뒤 닫았고, ready PR [#15](https://github.com/digitie/kor-travel-common/pull/15)를 `4cde7e83910fba08f5b92a3c2f08274297e94223`로 squash merge했다. merge 후 main push CI [34139949549](https://github.com/digitie/kor-travel-common/actions/runs/34139949549)의 6개 job이 모두 성공했다.

## 2026-09-07 (Codex, T-101 반복 no-go 근본 원인 수정·post-fix PASS)

T-101 초기 candidate `f8894e293ca9677f457011197052cd55dbdc9696`에서 A/B가 각각 BLOCK했다. A는 DTCG 자료형·token/group 충돌·Tailwind z/easing·dark-media·scoped dark 상속·profile/media drift·dark 전수 시험 누락을, B는 build 전 drift 검사 부재·scoped `color-scheme`·Tailwind 없는 hairline·T-102 경로 불일치를 독립 재현했다. 원인은 리뷰어가 달랐기 때문이 아니라, 생성물을 덮어쓴 뒤 검사하는 순서와 정본에서 파생되지 않는 중복 값, 실행 의미를 확인하지 않는 부분 시험이 한 계약으로 묶이지 않았기 때문이다.

`4c33a5d951e32df0c2170b7a865f324d122dbe05`에서 DTCG 2025.10 변환과 `$root` 계층, dark/profile 생성, build 전 `check`·생성 후 Git diff, 44개 light/dark 전수 비교, Tailwind v4/v3·Chromium·순수 CSS probe를 추가했다. 두 reviewer가 같은 immutable SHA/tree를 detached clean worktree에서 독립 재검토해 최초 12건을 모두 FIXED, 신규 P0–P3 0건으로 PASS했다([통합 리뷰](reviews/adversarial/2026-09-07-t101-post-fix-01.md), [manifest](reviews/adversarial/evidence/2026-09-07-t101-post-fix-01-manifest.md), [A](reviews/adversarial/evidence/2026-09-07-t101-post-fix-01-reviewer-a.md), [B](reviews/adversarial/evidence/2026-09-07-t101-post-fix-01-reviewer-b.md)). 원본 SHA256은 통합 보고서와 evidence에 보존했다.

PR #11 정확한 head의 CI `34126309766` 6개 job이 성공했고 Windows/WSL package 7 tests·pack/install·plan/link/SPDX/secret/redaction/version gate를 직접 확인했다. workflow와 표준 문서의 검사 순서 drift도 `6ab650d`에서 정렬했으며, 후속 표준 문서 리뷰 A/B가 PASS·신규 finding 0, CI `34128018010` 6개 job 성공을 확인했다([후속 판정](reviews/adversarial/2026-09-07-t101-ci-docs-post-fix.md), [A](reviews/adversarial/evidence/2026-09-07-t101-ci-docs-post-fix-reviewer-a.md), [B](reviews/adversarial/evidence/2026-09-07-t101-ci-docs-post-fix-reviewer-b.md)). main merge 후 main CI와 `codex/release-*` 실제 push CI는 `NOT_RUN(merge 후 gate)`로 남겼으며, 소비자 build/e2e·T-103·Release·npm/PyPI 게시·소비자 저장소 수정은 사용자 범위 또는 후속 task로 실행하지 않았다.

## 2026-09-07 (Codex, T-101 merge·main/release push CI·완료 원장 반영)

PR #12에서 T-101 candidate `fd5b42ccd0388dbac9eedadc9019d6f923affd5a`를 squash merge해 main `34c15b688b4c8663c1ca8608ab30336ac9ac0e01`에 반영했다. ready PR CI `34129028534`와 merge 후 main push CI `34129164333`은 각각 정확한 source SHA에서 docs·tools 양 OS·secret-scan·check-versions·packages 6개 job이 성공했다.

수용 기준의 release push 경계를 확인하기 위해 main에서 코드 변경 없는 `codex/release-tokens-verify` commit `65397a987f65831ba6cf358609751d576de31d53`을 push했다. [CI `34129337363`](https://github.com/digitie/kor-travel-common/actions/runs/34129337363)의 6개 job과 source SHA 일치를 확인한 뒤 branch를 삭제하고 `ci-t101-verify-20260907` 보존 tag의 peeled commit을 원격에서 확인했다. npm/PyPI·GitHub Release·소비자 저장소 변경은 하지 않았다.

T-101 상세를 DONE으로 바꾸고 완료 원장에 추가했으며 T-102·T-103·T-104를 READY로 열었다. 현재 상세 task는 106개, 완료 17개·열린 89개이며 다음 순차 작업은 T-102다. 초기 draft PR #11은 동일 source의 기록을 보존한 뒤 닫고, 실제 merge는 REST로 생성한 ready PR #12에서 수행했다.

## 2026-09-07 (Codex, T-011 최종 review PASS·PR #10 merge gate)

T-011 `consumer-manifest.v1` strict schema·validator·10개 앱 표면 초안과 `check_versions --manifest` 저장소 root 경계를 `4680bacdf285f2cc86f1a18cc1de29ff4129f2a8`에서 마쳤다. 반복된 적대 리뷰 no-go의 근본 원인은 매니페스트·lock·workspace·app 입력을 각 호출부에서 `resolve/is_file/exists`로 따로 검사해 OS별 symlink loop와 누락 leaf의 결과가 달라지고, 존재성 조기 반환이 중간 symlink를 경계 검사 전에 소거한 데 있었다. `_resolve_input_path`·`_path_contains_symlink`로 경계를 중앙화하고 app 조기 반환·validator registry·check_versions registry 오류 원문을 닫았으며, Windows/WSL direct·중간·외부·self-symlink와 redaction 회귀를 고정했다.

post-fix-04~07에서 reviewer A/B가 서로 독립적으로 BLOCK finding을 재현하고 수정했으며, 최종 post-fix-07은 A/B 모두 PASS·신규 P0–P3 0·T011-R17~R20 FIXED다([통합 리뷰](reviews/adversarial/2026-09-07-t011-post-fix-07.md), [A](reviews/adversarial/evidence/2026-09-07-t011-post-fix-07-reviewer-a.md), [B](reviews/adversarial/evidence/2026-09-07-t011-post-fix-07-reviewer-b.md)). PR #10 exact CI `34120043104`의 5개 job이 성공했고 Windows/WSL 전체 203 tests·focused 23 tests, plan 106/오류0, link 353문서·2304대상, SPDX 32/오류0, secret/redaction 443/발견0, versions self-check를 확인했다. T-011을 완료 원장으로 옮기고 현재 완료 16개·열린 90개, 다음 READY는 T-101이다.

소비자 저장소 수정·build/e2e·npm ci·uv sync·공용 패키지 build/pack/install·Release·npm/PyPI 게시·실제 소비자 채택은 `NOT_RUN(사용자 범위와 외부 환경 밖)`이다. GPL-3.0-or-later와 common 전용 범위를 유지했다.

## 2026-09-07 (Codex, T-016 완료·PR #9 병합 대기)

T-016 공용 시스템 범위 재점검을 `a9fc2f5187bcf2517cb1da54ece9b12ab04b82ff`에서 마쳤다. ADR-015로 common을 독립 운영 시스템이 아닌 위젯·디자인 토큰·공용 코어·로그인 UI/주입형 인증 프리미티브를 제공하는 저장소로 확정하고, 서버·사용자/세션 DB·운영 비밀·IdP·앱 정책은 소비자 소유로 남겼다. T-213a common UI 0.2 후보 보존과 T-214 로그인 위젯을 외부 UI 정식 릴리스 T-213에서 분리했으며 T-011은 READY가 됐다.

두 reviewer가 같은 immutable candidate/tree에서 독립 PASS했다. A/B 누적 finding 10건과 중복 B finding을 모두 FIXED로 재확인했고 새 finding은 없다([통합 리뷰](reviews/adversarial/2026-09-07-t016-common-scope-post-fix.md), [manifest](reviews/adversarial/evidence/2026-09-07-t016-common-scope-post-fix-manifest.md)). PR #9 CI `34107732188`의 5개 job, plan 106/오류0, link 324문서·2261대상, redaction 399파일, Windows 전체 179 tests·skip 0, diff 검사가 성공했다.

소비자 저장소 변경·패키지 실물 build/pack/wheel 설치·실제 후보 tag/Release·소비자 build/e2e·npm/PyPI 게시·권리 gate는 `NOT_RUN(후속 task 또는 외부 범위)`이다. PR #9를 병합한 뒤 main CI를 확인하고 다음 작업은 T-011부터 순차 진행한다.

## 2026-09-07 (Codex, T-016 공용 범위 재점검 시작)

사용자가 common의 목표를 위젯·디자인 토큰·공용 코어 로직·로그인과 같은 공용 시스템을 한 저장소에 모으는 것으로 재확인했다. 기존 ADR-001·ADR-011·AGENTS·architecture·backend/UI 규칙의 “인증 전체 제외” 문구와 충돌하므로 [ADR-015](adr/015-common-shared-systems-scope.md)와 [범위 재점검](plan/common-scope-recheck-2026-09-07.md)을 작성하고 T-016으로 정본·task를 동기화한다. 로그인 UI와 저장소·키 주입형 인증 프리미티브는 common 책임으로 포함하되 인증 서버·사용자/세션 DB·운영 비밀·외부 IdP·앱별 정책은 소비자 소유로 고정했다.

독립 reviewer A/B의 사전 대조에서 T-011의 9/10 초안 수 불일치와 기존 `--manifest` 경로·workflow 경계 위험, common `130xx`를 운영 대역처럼 읽을 수 있는 T-014/CI-20 문구를 확인했다. T-011은 10개 앱 표면 대응표와 경계 회귀를 요구하도록 BLOCKED로 조정하고, T-014/CI-20/T-108은 임시 fixture 포트 원칙으로 바꾼다. 소비자 저장소 수정·소비자 빌드/e2e·npm/PyPI 게시·인증 구현은 `NOT_RUN(이번 범위 밖)`이다.

## 2026-09-07 (Codex, T-005c 문서 post-fix PASS·merge gate)

문서 gate에서 확인된 세 finding을 `7b35ff07b077cef85d7d0d6e0971cacff210374f`로 수정했다. reviewer-B evidence의 공백 예외를 `-blank-at-eof`로 좁혔고, mixed-line-ending manifest의 `-text -eol -whitespace`로 원본·Git blob·checkout SHA256 `D1AB00A0F4462AEEB1F99E14C6E3FA2C36A5BDD7FA28AE23C6B60278F3C8C451`을 보존했으며, resume의 다음 시작 파일을 T-011로 갱신했다. package/npm/PyPI 항목은 범위 밖 `NOT_RUN(사유)`로 분리했다.

두 docs reviewer가 Windows/WSL에서 독립 post-fix 검증을 완료해 PASS했고 새 finding은 없었다. [문서 post-fix 통합 보고서](reviews/adversarial/2026-09-07-t005c-docs-post-fix.md), [A 원본](reviews/adversarial/evidence/2026-09-07-t005c-docs-postfix-reviewer-a.md), [B 원본](reviews/adversarial/evidence/2026-09-07-t005c-docs-postfix-reviewer-b.md)에 기록했다. exact PR CI `34099960667`의 5개 job도 성공했다. 소비자 저장소와 npm/PyPI는 건드리거나 게시하지 않았고, PR #8 merge 후 main CI만 남은 gate다.

## 2026-09-07 (Codex, T-005c 최종 review 완료·PR #8 merge gate)

T-005c workflow 고정 참조·CI Node 선언 정적 보고를 `codex/t005c-workflow-static-report`에서 마쳤다. 최종 code candidate `5807e535c16310c41c21f9efce87b2113aa17ee5`는 plain/flow YAML quote·delimiter 경계, workflow 출력 redaction, 저장소 식별자 분리, Docker 이름 문법, local action root containment와 빈 구조 fail-close를 포함한다. PR #8 CI `34097813843`의 docs·tools(Windows/Ubuntu)·check-versions·secret-scan 5개 job이 모두 성공했다.

Windows/WSL에서 전체 179 tests·focused 84 tests를 각각 skip 0으로 실행했다. 문서 link(311/2202), plan(102), SPDX(29), secret/redaction(386), self-check와 diff 공백 검사가 오류 없이 통과했다. 전문 영역이 다른 두 reviewer의 최종 post3d 원본과 manifest를 [최종 통합 리뷰](reviews/adversarial/2026-09-07-t005c-post-fix-03.md) 및 [evidence](reviews/adversarial/evidence/2026-09-07-t005c-post3d-manifest.md)에 보존했고 A/B 모두 PASS, 누적 finding은 모두 FIXED다.

이번 변경은 common 저장소의 코드·fixture·문서·리뷰 evidence만 포함하며 소비자 저장소 변경과 npm/PyPI 게시를 하지 않았다. 실제 소비자 workflow·CI·빌드·e2e, 원격 action major·Docker image 조회, package build/install/publish와 merge 후 main CI는 `NOT_RUN(사유)` 범위로 남긴다. 완료 원장과 [resume](resume.md)을 T-005c DONE·다음 T-011 READY로 갱신하고 PR #8 merge gate에 올린다.

## 2026-09-07 (Codex, T-005b 완료·PR #7 병합 준비)

T-005b를 `codex/t005b-poetry-requirements`에서 완료했다. 최종 candidate `5b687585cddf6e7a5145911e75647a0e814d9078`은 PR #7에 push했고 [CI 34087885355](https://github.com/digitie/kor-travel-common/actions/runs/34087885355)의 5개 check가 모두 성공했다. Poetry lock의 package/source·metadata·조건별 Git reference, 재귀 requirements의 include·hash·editable·범위/차단·`NO_LOCK`, URL 오류 비공개와 PEP 508 marker 문법을 common 코드와 회귀 시험으로 마무리했다.

Windows Python 3.14.3·WSL Python 3.11.15에서 각각 전체 162 tests·skip 0, focused 67 tests·skip 0이 성공했다. 문서 link 283/2166, plan 102, SPDX 22, secret/redaction 351, self-check와 diff 공백 검사가 오류 0이다. `ktdm`·`ktc`·`geo-no-lock` fixture와 합성 `mcp>=2` 차단 사례를 실행했으며, 실제 소비자 설치·빌드·e2e·Poetry/pip/uv 설치·전환은 `NOT_RUN`이다. 조사 fixture의 `mcp<2`는 차단되지 않는 음성 사례로 보존했다.

최초부터 post4까지 A/B 독립 원본을 서로 비공개로 확정했다. 최초·post-fix·post2·post3은 BLOCK finding을 수정해 누적 finding을 닫았고, 최종 post4에서 A/B 모두 PASS·새 finding 0을 확인했다([최종 통합 리뷰](reviews/adversarial/2026-09-07-t005b-post4.md), [manifest](reviews/adversarial/evidence/2026-09-07-t005b-manifest.md)). 소비자 저장소는 수정하지 않았고 npm/PyPI에 게시하지 않았다. PR #7 merge와 main CI 확인 후 T-005c를 순차 진행한다.

## 2026-09-07 (Codex, T-005b 시작)

T-005a 문서 후속 커밋 `a9bef6c4ca4ac93544040961874e00e5238e7116`을 PR #6으로 squash merge해 main `796445fadb9b4fa6de2f392d6169f31abdccc0fa`에 반영했다. PR CI `34081699365`와 main CI `34081751051`의 필수 5개 check가 모두 성공했고 리뷰 worktree를 정리했다. 이제 T-005b를 `codex/t005b-poetry-requirements`에서 시작한다. 소비자 저장소 쓰기·npm/PyPI 게시·설치는 하지 않는다.

## 2026-09-07 (Codex, T-005a 완료·PR #6 병합 준비)

T-005a의 최종 code candidate `3c5801f14855a067080f257ec83d2279de32c74a`를 PR #6에 올렸다. `uv.lock`의 version/revision/source와 Python 하한, 공유 lock의 전이 축·차단·git source, PEP 735 group, `tool.uv.sources` 복수 항목을 검사하고 malformed input은 exit 2로 닫는다. branch/tag/rev 이름에 `@`가 들어간 경우 마지막 조각을 버전 태그로 오인하지 않도록 보수적으로 FLOATING_REF 처리했다. npm·PyPI 게시나 소비자 저장소 쓰기는 하지 않았다.

최초 A/B 적대적 리뷰는 BLOCK이었고, 고정 선언 우회·구조 fail-open·PEP 735 검증 누락·입력 원문 노출을 각각 수정했다. 후속 후보 `9027500`, `735efed`에서 잔여 반례를 추가로 수정했으며 최종 post-fix `3c5801f`에서 A/B가 독립적으로 PASS, 누적 8개 finding FIXED·새 finding 0을 확인했다([통합 리뷰](reviews/adversarial/2026-09-07-t005a-post3.md)).

Windows Python 3.14.3·WSL Python 3.11.15에서 각각 전체 140 tests·skip 0과 focused 45 tests가 성공했다. PR CI run `34080403871`의 5개 check도 모두 성공했다. 문서 link 272/2151, plan 102, SPDX 20, secret/redaction guard와 self-check가 오류 0이다. 공항 소비자 파일은 양 OS에서 읽기 전용으로 `findings=24 failing=2 exit=0`을 재현했으며 이는 제품 gate가 아니다. 실제 `uv sync --locked`·설치·빌드·e2e 및 소비자 CI는 NOT_RUN이다. PR #6 병합 후 다음 작업은 T-005b다.

## 2026-09-07 (Codex, T-009 두 리뷰 종료·완료 기록)

f15072f의 post-fix 원본을 각각 확정한 뒤 교차 비교했다. A/B PASS·원 finding 8개 FIXED·새 finding 0이다([최종 리뷰](reviews/adversarial/2026-09-07-t009-post-fix.md)). Windows/WSL 각각 135 tests·skip 0, 두 reviewer의 경로/정규식·8.3 별칭·step summary 원 반례가 성공했다. 초기 CI 실패·수정과 각 검증 수치/한계는 [T-009](tasks/T-009-ci-hardening.md#evidence)에 연결했다.

candidate PR CI 34070365064, 같은 tree의 빈 검증 commit 18b83bd에 대한 PR 34070419814/release push 34070419969가 5 check 모두 성공했다. source·보고 digest 일치를 확인했고 실제 Release·태그·registry 게시·ruleset·다른 저장소 쓰기는 하지 않았다. T-009를 DONE으로 옮기고 선행이 충족된 T-005c를 READY로 정렬했다. 다음 한 작업은 T-005a이며 이번 완료 기록 CI와 PR merge·main CI 후 착수한다.

## 2026-09-07 (Codex, T-009 CI·스냅샷 정보 검사 구현)

사용자 재개 지시로 T-009를 착수하고 [PR #5](https://github.com/digitie/kor-travel-common/pull/5)를 draft로 만들었다. docs·tools(ubuntu-24.04/windows-2025)·secret-scan·check-versions에 액션 SHA·읽기 권한·timeout·concurrency·PR/main/release push source SHA를 연결했다. report는 비설치용 고정 fixture로 비어 있지 않은 판정·step summary를 확인한다. 원격 branch protection 설정은 변경하지 않고 절차만 작성했다.

검사기는 같은 작업 트리/index/HEAD 스냅샷의 파일과 정책을 읽는다. Git·정규식·인코딩·링크·빈 범위 오류는 exit 2, 발견은 exit 1이며 원문 대신 파일·행·규칙 ID만 출력한다. 조사 문서의 민감 값은 [보안 정정](survey/README.md#9-t-009-보안-정정)에 따라 치환했고 다른 저장소는 수정하지 않았다. 삭제된 원문 값이 diff 로그에 다시 나오지 않도록 리뷰 출력도 마스킹한다.

Windows 131 tests·skip 0(29.892초), WSL Python 3.11의 131 tests·skip 0(13.107초), link260/2107·plan101·SPDX18·전체 트리 두 검사·diff가 성공했다. 실제 CI·release push 및 두 독립 리뷰는 candidate 이후 실행하며 현재 NOT_RUN이다. 초기 검사에서 발견한 실패와 수정 근거는 T-009 evidence에 기록했다.

## 2026-09-07 (Codex, T-015 최종 리뷰·완료 기록·대기)

95c139f의 두 reviewer 원본을 각각 확정한 뒤 교차 비교했다. 최종 PASS/PASS, 누적 9개 ID 모두 FIXED·새 finding 0이다([최종 리뷰](reviews/adversarial/2026-09-07-t015-post-fix-03.md)). 두 reviewer가 수정된 자산 명령 8개 시나리오와 문서·plan·diff를 새로 확인했고, 변경 없는 코드/정본의 이전 115 tests·발행/source 검증은 동일성 확인 후 재사용했음을 원본에 구분했다. candidate CI 34066138272 성공도 확인했다.

T-015와 T-006의 변경된 범위 기록을 완료 원장으로 옮겼다. T-006의 이전 npm/PyPI 이름 조회·예약은 NOT_RUN(사용자 제외)이며 계정 확보 성공을 주장하지 않는다. 완료 기록에서 link 258문서·2099대상, plan101·diff 오류 0과 Windows 115 tests·skip 0(13.223초)을 새로 확인했다. 최종 CI 성공 뒤 PR #4를 병합하고 대기한다. T-009와 다음 구현 task는 착수하지 않으며 소비자 저장소를 수정하지 않았다.

## 2026-09-07 (Codex, T-015 잔여 발행 명령 정리)

d1c7263의 두 독립 리뷰는 기존 7개 finding을 FIXED로 확인했지만 T-109·T-212의 오래된 발행 명령을 각각 A-P1-03·B-P1-06으로 보고했다([통합](reviews/adversarial/2026-09-07-t015-post-fix-02.md)). 두 원본 확정 후 비교했고 coordinator도 실패 3건을 재현했다. 두 task의 중복 발행 절을 정본 release 절차로 연결했으며 checksum/tar 6개 mock이 기대 결과와 같았다. Windows 115 tests·skip 0(12.916초), 문서·101 task·diff 검사 성공이다. 규범 문서에서 태그 생성·Release 생성은 runbook에만 남았다. 실제 발행·소비자 쓰기 없이 새 commit의 두 재확인 뒤 현재 PR #4를 병합하고 대기한다.

## 2026-09-07 (Codex, T-015 발행 실패 전파·CI 경로 보완)

첫 post-fix ae86185의 CI 34065243380 성공과 별개로 A PASS/B BLOCK이었다. 최초 5건은 모두 FIXED이며 새 B-P1-04·B-P2-05를 수용했다([재검토](reviews/adversarial/2026-09-07-t015-post-fix.md)). coordinator도 T-213 원문의 tag/push 실패 뒤 발행 도달을 bash mock으로 재현했다. 중복 발행 블록을 제거하고 정본의 tag/push/원격 peeled SHA/발행 실패를 즉시 종료하도록 보완했다. rc·정식 합계10개 mock 경계가 기대 결과와 같고 Windows 115 tests 성공·skip 0(17.619초), 문서·101 task·diff 검증 성공이다. 실제 발행은 실행하지 않았다. release merge commit을 위한 push/필수 job/source SHA 검증은 ci-deploy와 T-009/101/302의 구현·수용 기준으로 연결했으며 실제 구현은 NOT_RUN이다.

사용자가 “지금작업 머지 후 대기”로 지시했다. PR #4의 필수 두 재검토·CI와 완료 기록을 마쳐 병합한 뒤 대기하며, 준비만 읽어 둔 T-009는 착수하지 않는다. 소비자 저장소에는 쓰지 않았다.

## 2026-09-07 (Codex, T-015 독립 리뷰 수정)

[PR #4](https://github.com/digitie/kor-travel-common/pull/4) candidate a28c2a7의 CI 34064724584는 성공했지만 독립 리뷰는 A/B 모두 BLOCK이었다. 두 원본을 보존한 뒤 P1 ref 충돌 중복 2건과 P2 세 건을 모두 수용했다([통합 리뷰](reviews/adversarial/2026-09-07-t015.md)). release 태그는 후보에서 분기한 release base의 준비 PR merge commit을 명시하고, 실제 명령·workflow 예외·체크리스트를 정렬했다. T-010a에 후보 생산 선행을 연결하고 0.2 후보 보존 책임을 해당 릴리스 준비 task에 두었다. 과거 release branch의 task 원장은 스냅샷으로 보존하고 현재 main의 원장 commit·evidence로 선행을 확인한다. 실제 발행 뒤 main의 문서 전용 PR에서 완료와 후속 상태를 반영하며 패키지/lock은 가져오지 않는다.

Windows 전체 115 tests 성공·skip 0(14.668초), link·101 task DAG·diff 검증 성공이다. 실제 validator로 과거 branch 보존/현재 main 완료 상태 모델을 대조해 오류 0을 확인했고 release bash 블록은 WSL bash -n을 통과했다. 모델은 실제 task 완료·발행이 아니다. 두 post-fix 리뷰 전이며 패키지·소비자·실제 태그/발행은 NOT_RUN이다. 소비자 저장소에 쓰지 않았다.

## 2026-09-07 (Codex, T-015 미게시·common 구현 선행 정리)

PR #3은 closure ad00caa의 CI 34064140128 성공 후 659aa6d로 squash merge했고 source tree 동일성을 확인했다. 두 T-005 리뷰 worktree를 clean 상태에서 제거·prune했다. T-015에서는 사용자 npm/PyPI 미게시와 common만 구현 범위를 ADR-014로 반영하고 계정 확보 조건을 철회했다. 실제 소비자 dispatch(T-010a)와 세 패키지 0.1 후보 보존 task를 분리했으며 정식 릴리스·채택·권리 gate를 유지했다. 검증한 이전 후보를 원격 불변 ref·digest로 보존하고 다음 minor를 개발 버전으로 전환한 뒤 구현한다. 외부 릴리스는 후보에서 분기한 release branch의 PR로 준비한다.

문서 242개·1991 target, task 101개 검사가 오류 0이다. Windows Python 3.14.3 전체 115 tests 성공·skip 0, 버전 자체 검사 성공, diff 공백 검사 성공이다. 외부 노드를 제외한 DAG 도달성 검사에서 common UI/Python 구현 경로는 열리고 외부 dispatch·정식 릴리스·미래 재평가는 대기를 유지했다. source·workflow·registry 수치는 바꾸지 않았다. 패키지 build·실제 후보 보존·소비자 실행은 NOT_RUN(각 후속 task). 같은 후보의 독립 두 리뷰와 CI는 commit 후 수행하며 완료 전이다.

## 2026-09-07 (Codex, T-005 최종 리뷰·완료 기록)

f050997에서 A/B 두 원본이 독립 확정된 뒤 교차 비교했다. 최종 PASS/PASS, 최초 9개 ID 모두 FIXED이며 새 finding은 없다([최종 리뷰](reviews/adversarial/2026-09-07-t005-post-fix.md)). A는 Windows/WSL 115 tests와 환경당 공격 CLI 30개, B는 Windows 115 tests·판정/모드 30조합을 실행했다. 7곳 고정 입력 48파일·306행 전체 재현과 새 digest를 확인했으며 report의 102개 위반을 정상으로 세지 않았다. candidate CI 34063775506도 성공했다. T-005를 완료 원장으로 옮기고 T-005a/b·T-011을 READY로 바꾼다. 완료 기록의 CI를 확인한 뒤 PR #3을 병합한다. 다음은 사용자 지시의 npm/PyPI 미게시·common 구현 선행 정리다. 소비자 저장소는 수정하지 않았다.

## 2026-09-07 (Codex, T-005 독립 리뷰 수정)

두 원본 확정 후 9개 ID를 모두 수용했다([통합](reviews/adversarial/2026-09-07-t005.md)). 미해석 차단 버전 두 finding은 같은 원인이나 원 ID/심각도를 유지했다. 전이 링크·URL/branch·npm 이름·런타임 문법·build metadata·차단 범위·예외 공백을 고쳤다. 회귀 8개를 먼저 추가해 20 실패를 확인했고 수정 후 Windows 3.14.3·WSL 3.11.15에서 전체 115 tests 성공·skip 0이다. 같은 7개 고정 입력 48파일과 report 306행이 양 OS에서 원본과 같았다. 새 검사기 digest는 별도 post-fix evidence에 남기고 최초 원본을 덮어쓰지 않았다. 독립 재확인 전 T-005를 완료하거나 merge하지 않는다.

## 2026-09-07 (Codex, 병합·배포 채널 사용자 지시)

사용자가 완료 PR의 병합을 요구해 PR #1을 d4a992a, PR #2를 a3a8444로 squash merge했다. PR #2는 main 위로 재정렬한 7a1aee7이 기존 검토 트리 219e44d와 완전히 같음을 `git diff --exit-code`로 확인했고 [재정렬 CI](https://github.com/digitie/kor-travel-common/actions/runs/34063209673)도 성공했다. PR #3은 main 위의 3bec3eb로 재정렬했으며 최초 리뷰 후보 409b95c와 트리가 동일하다. 리뷰 격리 기준은 원래 commit을 유지했다.

사용자는 npm·PyPI에 게시하지 않는다고 확정했다. GitHub Release·고정 태그 채널과 빌드/설치 검증을 유지하고 불필요한 계정·게시 선행 및 common 구현을 외부 릴리스에 묶은 순서를 후속 계획 task에서 정리한다. 다른 저장소에 쓰지 않는 범위는 유지한다.

T-005 사후 재현: WSL uv Python 3.11.15 전체 107 tests 성공·skip 0이며 7개 report 306행과 48개 입력 digest가 Windows와 동일했다. 소비자 상태 사후 읽기에서는 airport의 HEAD 변경·dirty 6개가 관찰됐다. 이 작업은 소비자 저장소에 쓰지 않았고 bb47f107 고정 object 입력을 유지했다. 나머지 6곳은 시작 SHA와 같고 clean이었다.

## 2026-09-07 (Codex, T-005 버전 검사 구현 후보)

T-003 완료 commit 219e44d에서 `codex/t005-version-registry`를 분기했다. 회귀 7개에서 24 실패를 먼저 재현했고 strict 중첩 정책·역전 범위·만료·prerelease·optional/hoist·전이·shrinkwrap 처리를 보완했다. 코드 변경 후 Windows·WSL 전체 107 tests 성공·skip 0. [고정 입력 evidence](evidence/t005/README.md)는 7개 소비자 306개 판정과 입력 digest를 보존한다. 입력 원문은 common의 무시된 임시 위치에만 두고 소비자 저장소에는 쓰지 않았다. report exit 0을 정책 준수로 세지 않았고 `enforce`·`clean_runs`와 12개 예외 값/기한은 유지했다. 정본 간 충돌은 task를 versions 정책 §7에 맞춰 해소했다. CodeGraph는 기존 미초기화 상태이므로 rg·직접 코드·고장 주입으로 확인했다.

## 2026-09-07 (Codex, T-003 완료)

a2c1891에서 A/B 모두 PASS, 최초 6 finding 전부 FIXED다([최종 판정](reviews/adversarial/2026-09-07-t003-post-fix-02.md)). Python 3.11.15에서도 실제 100 tests·SPDX를 확인했고 [CI](https://github.com/digitie/kor-travel-common/actions/runs/34062228366)도 성공했다. T-003을 완료 원장으로 옮기고 그 선행이 닫힌 T-009·T-101·T-107·T-302를 READY로 표시했다. 완료 7개·열린 89개, 다음은 T-005다. 상태 이동은 완료 evidence의 기록이며 수용 기준·규칙·릴리스 gate를 변경하지 않았다.

## 2026-09-07 (Codex, T-003 확장자 별칭 보완)

951b443 재검토에서 B PASS, A는 기존 경로 별칭 finding의 확장자 변형을 OPEN으로 유지했다. 추가 음성/양성 시험을 먼저 실행해 실패 3개를 확인했고 확장자·주석 판별과 editorconfig·Windows 끝 공백/점 경계를 보완했다. Windows Python 3.14.3·WSL Python 3.14.4 모두 전체 100 tests 성공·skip 0, SPDX 13개·문서 222개/1869 target·task 96개 오류 0이다. 새 review 기록 추가 후 문서 검증은 commit 전에 다시 실행한다.

사용자가 모든 라이브러리를 GPLv3로 변경할 예정이라고 알렸다. 이 미래 방향과 고정 원천의 현재 선언을 구분하며, common은 현재 GPL-3.0-or-later를 유지한다. -only/or-later 표기는 별도 확인 질문을 전달했다. 다른 저장소는 수정하지 않았고 원문 사본·소비자 gate도 자동 변경하지 않았다.

## 2026-09-07 (Codex, T-003 독립 리뷰 수정)

017fef1의 두 원본을 확정한 뒤 6 finding을 모두 수용했다([통합 리뷰](reviews/adversarial/2026-09-07-t003.md)). 경로 별칭·qualified geo·PV 행 공백 우회를 회귀 시험으로 고정했다. canview 원본 재대조로 제목 검사는 기존 기능임을 확인해 수정 고지를 바로잡았다. 템플릿의 고지·PV 사본·라이선스 동반 목적지를 명시했다.

Windows·WSL 전체 98 tests 성공·skip 0, SPDX 13개 오류 0. 격리 전달 fixture는 설정 6개와 고지·PV·원문 사본을 확인했다. 제품·소비자 gate와 T-009 CI 확장은 미실행이며 리뷰 수정 candidate를 다시 commit·push한 뒤 동일 두 reviewer가 재확인한다. T-003을 닫기 전 다음 task 구현은 시작하지 않는다.

## 2026-09-07 (Codex, T-003 고지·SPDX 구현 후보)

PR #1의 b36c99fb6c7f4df2a27364842ee197fc947e461e에서 `codex/t003-license-provenance`를 분기했다. PR #1은 merge하지 않고 이 branch의 base로 유지한다. 사용자 요청에 따라 T-003 → T-005 → T-009 순서로 진행한다.

원문 확보 결과·94개 회귀 시험·SPDX 13개·문서/DAG·수정한 초기 시험 실패는 [T-003 evidence](tasks/T-003-notices-provenance-spdx.md#evidence)에 있다. 초안의 geo 설정 출처 누락을 실제 Git object 대조로 찾아 PV-007~012와 GPL-3.0-only 고지로 보완했다. 새 소비자 제품 코드를 복사하거나 소비 저장소를 수정하지 않았다. CodeGraph의 기존 미초기화 상태 대신 코드 읽기·rg·고장 주입 시험으로 검증했다. 두 독립 reviewer는 같은 commit의 별도 detached worktree에서 검사한다.

## 2026-09-06 (Codex, T-013 종료 대조의 숨은 선행 정정)

8fb1334에서 완료 6개·인계·draft PR/리모트 SHA·CI run 34025999506은 일치했다. coordinator가 T-009의 미구현 SPDX 도구 의존을 추가 질문했고 두 reviewer가 같은 원인을 A-P1-06/B-P2-10으로 독립 확인했다. 심각도는 원본 그대로 보존하며 통합 차단은 높은 P1을 따른다. T-009 상세/원장에 T-003 선행을 넣고 BLOCKED로 되돌렸다. T-005 전체 DONE은 기술적 필수와 구분하고 기본 실행 대기열의 T-003 → T-005 → T-009는 유지한다.

후속 에이전트가 T-009를 직접 지정받아 backlog를 읽지 않아도 필수 도구 선행을 알 수 있게 했다. 코드·CI는 불변이며 새 문서·DAG·공백 검사와 같은 두 reviewer의 수정 기준선 재검토로 닫는다. 과거 종료 원본은 [종료 판정](reviews/adversarial/2026-09-06-phase0-closure.md)에 보존한다.

## 2026-09-06 (Codex, T-013 문서 task 종료·순차 인계)

5670642에서 두 reviewer가 모두 PASS이며 최초 14건과 후속 B-P2-09까지 FIXED를 확인했다([세 번째 통합 판정](reviews/adversarial/2026-09-06-phase0-post-fix-03.md)). T-001·T-002·T-004·T-007·T-008·T-013의 실제 evidence를 연결하고 상세 H1/상태와 완료 원장 제목을 동기화했다. 총 96개 중 완료 6개·열린 90개이며 다음은 T-003 READY, 이후 T-005·T-009다. 개별 규칙 확정과 SPDX/라이선스 원문·소비자 보고·실물 구현은 완료하지 않았다.

정본 서두의 리뷰 전/IN_PROGRESS를 문서 초기판 완료 범위와 맞추고 패키지 실물 대조·소비자 첫 적용의 초안 상태는 유지했다. 기존 원본·조사 스냅샷·소비자 checkout을 보존했다. 이번 종료 delta도 별도 immutable 기준선으로 같은 두 reviewer에게 제출하며 최종 CI·리모트 SHA·판정은 [리뷰 색인](reviews/README.md)과 draft PR #1에 연결한다. 이번 작업은 PR merge·릴리스를 포함하지 않는다.

## 2026-09-06 (Codex, T-013 두 번째 재검토·종료 기준 대조)

84759b6 CI run 34025270597 성공. 두 번째 post-fix에서 원 14 finding은 모두 FIXED지만 B가 T-005b의 빈 입력 성공 지침을 새 P2(B-P2-09)로 기록했다. 유효 선언과 lock 부재 fixture의 NO_LOCK/report 결과를 입력 자체가 없는 exit 2 음성 사례와 분리했다. 도구 코드는 바꾸지 않았다. 원본과 disposition은 [두 번째 통합 판정](reviews/adversarial/2026-09-06-phase0-post-fix-02.md)에 보존한다.

종료 기준 대조로 resume 5절·다음 작업 3불릿, 소비자 7곳 조사 §8·§9 링크 14개, maintenance의 버전 정본(versions.json) 안내를 정정했다. ADR 13편 H1/색인 상태·다음 번호 014·decisions.md 부재와 CLAUDE 32줄을 직접 검사했다. 새 문서 검사 201개·1734 target 오류 0, 96 task/DAG 오류 0, diff 공백 오류 0. 코드 회귀는 같은 84759b6의 Windows·WSL 67 tests·skip 0을 재사용한다. 종료 상태는 두 reviewer의 새 기준선 확인 뒤 이동한다.

## 2026-09-06 — T-013 post-fix 잔여와 인계 정합

12fb3a8 CI run 34024615020이 통과했다. A 재검토는 원 6건 중 5건 FIXED, Python 선언 fragment의 A-P1-05 OPEN으로 BLOCK이었다. 추가 CLI 회귀는 수정 전 24 tests 중 3 subtest 실패, 문맥별 ref 해석 후 전체 67 tests 성공·skip 0이다. npm 선언은 fragment, Python 선언은 path의 @rev, uv git lock source는 resolved 전체 SHA로 구분했다. 공식 문서·로컬 pip 재현 근거는 [인계 재확인](plan/handoff-verification.md)에 연결했다.

인계 대조에서 canview A 49개·R 77개가 원본 ID와 빠짐없이 대응하고 CLAUDE 포인터는 32줄임을 확인했다. ADR 13편 H1·상태/색인을 일치시켰다. 생성된 파일의 예정 상태를 정정하고 test_plan_validation의 추가 시험·출처 헤더를 PROVENANCE에 반영했다. 미완료 규칙 task를 READY/BLOCKED와 잔여 evidence로 되돌렸으며 개별 규칙 확정·도구 실행을 수행 완료로 세지 않았다. 다음 재검토는 이 정정까지 포함한 immutable commit으로 진행한다.

## 2026-09-06 — T-013 독립 리뷰 finding 정정

원본 후보 d3712a8을 리뷰어 A(도구·CI)와 B(계획·계약)가 격리 checkout에서 독립 검토했고 모두 BLOCK이었다. A의 5개 P1 음성 사례를 재현한 최초 회귀 실행은 22 tests 중 11 subtest 실패였으며 구현 수정 후 전체 65 tests가 Windows에서 통과했다(skip 0). B의 L6 결정/적용 역전, pinvi UI 0.1/0.2 순환, 다음 minor 코드 혼입, Python 0.2 릴리스 누락, 승인 전 스모크, useRender peer 누락을 ADR-013·선행 DAG·T-311/T-422a/T-422b로 정정했다. 공개 Python facade와 tokens 호환 minor도 명시했다. 원본 보고서는 수정하지 않고 evidence에 보존한다.

추가 직접 대조: T-432가 0.1에 없는 Button을 import하던 범위를 소형 공개 부품으로 제한했고, 아직 없는 T-211 검사기는 수동 shim/patch evidence로 분리했다. T-003의 고정 항목 수·존재 미확인 cva NOTICE 요구를 실제 고정 upstream 파일 대조로 바꿨다. 라이선스 원문 확보·소비자 7곳 버전 보고·패키지 구현은 후속 task이며 수행 완료로 집계하지 않았다.

## 2026-09-06 (Codex, T-013 인수·계획 원장·CI 재현)

PR #1 `09104ed`와 미커밋 초안을 실제 파일로 대조했다. 착수 검증은 링크 33건 오류·원장 누락 등 plan 94건 오류·unittest 57건 성공이었다. `d3712a8`에 로컬 초안과 T-013·93개 원장·통합 계획을 통합해 같은 draft PR에 push했다. 소비자 저장소를 수정하지 않았다.

- Windows에서는 통과했던 link validator가 [CI run 34023326750](https://github.com/digitie/kor-travel-common/actions/runs/34023326750)에서 `docs/survey/cross/backend.md`의 inline code를 링크로 오인했다. code span 제외와 회귀 2건을 추가했다. 조사 본문은 보존했다.
- `python3 -B -X utf8 tools/validate_document_links.py`, `tools/validate_plan.py`, `-m unittest discover -s tests -p "test_*.py"`: Windows Python 3.14.3과 WSL에서 오류 0·59 tests OK·skip 0. `git diff --check` 통과, 추적 파일 `i/crlf`·`i/mixed` 없음. Windows 명령 치환은 [개발 환경](dev-environment.md) §5를 적용했다.
- CodeGraph context 호출은 미초기화 오류로 실패했다. `rg`·직접 코드 읽기·회귀 테스트로 대체했다.
- 재확인(2026-09-06): 공식 [Next 메타데이터](https://registry.npmjs.org/next/16.3.4), [React 메타데이터](https://registry.npmjs.org/react/19.2.8), [TypeScript 메타데이터](https://registry.npmjs.org/typescript/7.0.2)에서 초안의 해당 버전 존재를 확인했다. 이 확인은 전체 버전 레지스트리·소비자 설치 검증이 아니며 T-005 잔여는 유지한다.
- 직접 읽은 소비자 HEAD·manifest: map `c494e227e010565be295de3f9670b2f7c8c20944` clean, weather `6003da995fa4b35799f9dadc406c6ba2878bfbae` clean, geo `1d9d74d3a852bbaaa09144b75bb69b99a58a6002` clean. airport 로컬은 조사 이후 `2e114b0a0530b32b72cca035ad0366ddb93c6cd2`로 진행했고 dirty 4건이 있어 보존했다. 기존 WIP의 현재 병합·CI evidence는 T-430에서 다시 대조한다. 선언값을 설치본으로 취급하지 않았다.
- 두 reviewer는 `d3712a8` detached worktree에서 동일 manifest로 검토 중이다. 원본 확정 전 상대 finding을 공유하지 않는다. 패키지·소비자 빌드·e2e는 NOT_RUN(이번 범위에 실물·소비자 변경 없음).

Git Bash에서 동일. 다음은 reviewer 원본 보존·finding 수정·post-fix 재검토·최종 인계다.

## 2026-09-06 (claude, 저장소 부트스트랩·조사·설계·계획)

기준선 `b92fabeb1c96a11c1fc9507d93271c1ebeee09b0`(Initial commit, 추적 파일 `LICENSE` 1개)에서 브랜치 `feat/bootstrap-survey-and-integration-plan`을 만들어 작업했다. 사용자 dirty 변경은 없었다. 환경은 Windows 11(Git Bash, Tier 2), Python 3.14.3(Windows), 원격 `origin = https://github.com/digitie/kor-travel-common.git`이다. CodeGraph MCP는 연결에 실패해 사용하지 않았고 `rg`·직접 읽기·validator로 대체했다.

**작업**

- canview(`F:/dev/canview` `1f93b8a`, 읽기 전용) 구조를 대조해 scaffold를 만들었다: `tools/validate_plan.py`·`tools/validate_document_links.py`(대상 경로·절대 링크 오류·산문 오탐 제외로 재작성)·`tests/test_plan_validation.py`·`tests/test_document_links.py`(신규 5건), `docs/tasks-rule.md`(common ID 대역·5열 문법 명문화), `docs/tasks-done.md`, `docs/tasks/README.md`, `docs/runbooks/{README,documentation-maintenance,agent-failure-patterns}.md`, `docs/reviews/README.md`, `docs/reviews/adversarial/TEMPLATE.md`(diff 0), `.gitignore`·`.gitattributes`·`.editorconfig`·`.github/workflows/docs.yml`. 출처는 `PROVENANCE.md`에 기록했다.
- 조사 워크플로: 7개 소비 저장소를 기준 커밋 단위로 고정해 인벤토리 7편 + 횡단 비교 10편 + README·공통화 매트릭스를 `docs/survey/`에 작성했다(서브에이전트 병렬). 17개 산출물 중 14개는 파일이 완결된 상태로 세션 한도(스키마 응답만 실패)에 걸렸고, 완결 여부를 마지막 절로 확인한 뒤 재실행하지 않았다. 나머지 3개는 미완결이어서 해당 에이전트만 다시 실행해 완결했다. 문서 간 불일치 19건은 `docs/survey/README.md` §6.2에 재확인 값과 함께 남겼다.
- 설계 판정: coordinator 초안 레지스터 + 독립 설계안 2(risk-first·velocity-first) + 판정 3(fact-consistency·migration-feasibility·directive-fidelity)을 실행하고 원본을 `docs/plan/design-panel/`(7파일)에 보존했다. 합의 문안을 채택해 `docs/plan/design-brief.md`(결정 D-01~D-33, 열린 결정 O-1~O-25, 파일 지도, ADR 12, task 92)를 확정했다.
- `09104ed0fa7f8564936fbbc3b9c17057f86d3e7c` "docs: bootstrap kor-travel-common with survey, design brief, validators"(2026-09-06 17:01 KST)를 커밋·push하고 [Draft PR #1](https://github.com/digitie/kor-travel-common/pull/1)을 열었다(base `main`).
- Phase 0 문서군(entry·runbooks·architecture·standards-fe·standards-be·versions-conventions·task 5·ledger)을 파일 지도의 소유자별로 병렬 작성했다. 이 항목 작성 시점에는 미커밋이며 상호 링크는 파일 지도 경로를 따른다.

**결정**: 브리프 D-01~D-33 채택(canview 계층·5열 원장·`decisions.md` 미보유·저장소 상대 링크만·Python 도구·GPL-3.0-or-later·tarball 배포·SemVer 0.x·`--kt-*`). 열린 결정 O-1~O-25는 사용자 확인 전까지 기본값으로 진행하고 문서에는 "열림(사용자 확인 필요)"로 적는다. 사용자 지시 완화로 보일 수 있는 항목은 pinvi mobile Tailwind 3 예외(O-8)뿐이며 "승인 대기"로만 적었다.

**검증(작성자 실제 실행, `09104ed` 기준)**

| 명령/환경 | 결과 |
|---|---|
| `python -B -X utf8 tools/validate_plan.py` (Windows, Python 3.14.3) | 오류 3: `docs/tasks: 상세 task 파일이 없음`, `docs/tasks.md: 읽기 실패`, `상세 task 수 불일치 (실제 0)` — 원장(ledger) 산출 전이므로 **통과 아님**, 문서군 완성 후 재실행 필요 |
| `python -B -X utf8 tools/validate_document_links.py` | 36 문서·60 local target·오류 19 — 전부 미작성 문서(`agent-workflow.md`·`consumer-adoption.md`·`release.md`·`docs/README.md`·`docs/tasks.md`·`docs/dev-environment.md`·`docs/standards/*`·`docs/architecture/README.md`)를 가리키는 링크. 산문 오탐은 도구 정정 후 0. **통과 아님** |
| `python -B -X utf8 -m unittest discover -s tests -p "test_*.py"` | 40 tests OK(plan validator 35 + link validator 5), 1.3s |
| `git diff --check HEAD~1 HEAD` | trailing whitespace 1건 `docs/plan/design-panel/register-coordinator-draft.md:77`(exit 2) — 판정 원본 파일, 미수정 |
| 조사 워크플로(서브에이전트 17) | 14 완결 + 3 재실행 후 완결 → `docs/survey/` 19파일 |
| 설계 판정 워크플로(설계자 2·판정자 3) | `docs/plan/design-panel/` 7파일 + `docs/plan/design-brief.md` |
| `gh pr create --draft` | PR #1 생성(2026-09-06T08:01:57Z UTC), CI `docs` run `34020728074` `validate-docs` **failure**(위 두 validator 오류와 동일 원인) |

**미실행(NOT_RUN)**: 패키지 빌드·타입 검사(패키지 미존재), `npm pack`·tarball 설치, wheel 빌드·설치, 소비자 빌드(`consumer-smoke`)·e2e, 브라우저·시각 기준선 캡처, `check_versions.py`·`kt_contrast.py`·`ux_lint.py`(미작성), 2인 독립 적대적 리뷰. 어느 것도 통과로 집계하지 않았고 task는 모두 `IN_PROGRESS`/`READY`/`BLOCKED`로 둔다.

**환경·fallback**: Windows에서 작성한 `.py`·`.md`는 `.gitattributes`(`* text=auto eol=lf`)가 add 시 LF로 정규화한다는 전제이며 첫 add에서 `git ls-files --eol`로 확인해야 한다(canview checklist Q6). 조사 대상 저장소와 canview에는 아무 파일도 쓰지 않았고 실행 전후 `git status`로 부산물이 없음을 확인했다(`docs/survey/README.md` §2.3).

**소비 저장소 상태(조사 기준, `docs/survey/README.md` §2.1)**: airport `2bb1111`(clean, WIP `codex/shadcn-ui-foundation` `99b3f98`), concierge `7945305`, docker-manager `862562d`, geo `1d9d74d`, map `c494e227`, weather `6003da9`, pinvi `9af25e5`(shallow clone). 어느 저장소도 수정하지 않았다.

**다음**: [resume](resume.md) "다음 한 작업" — 2인 적대적 리뷰 → task `DONE` → PR #1 본문 갱신·머지.
