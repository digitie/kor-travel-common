# Native CSS 공통 정책 후속 인계

- 기준: 8dad71a50f9f8f12f0e3ba1c913a93e404dabfed.
- 작업: 별도 worktree common-native-css-policy / branch agent/codex-native-css-policy.
- 상태: 작성자 선택 검증 완료. 부모 통합·독립 A/B 최종 delta·원격 CI는 별도 gate이다.
- 원본 common의 제품·정책 코드는 수정하지 않았다. 부모의 후속 archive-only 커밋 299e0f9를 관찰했고 해당 제품 차이는 없다.

## 구현 범위

versions.json의 exact 축에 승인 stable SemVer build metadata를 지원하고 Lightning CSS를 web/mobile 필수 **개발 의존성**과 artifactPackages에 추가했다. runtimeRequired에는 넣지 않는다. 기존 prerelease 규칙과 legacy prefix checker 제외 조건을 보존했다.

root/vendor의 고정 tarball 한 개를 root 및 실제 Next smoke/example의 선언·lock·override가 사용한다. [준비 스크립트](../../packages/ui/smoke/prepare-lock.mjs)는 원장과 고정 lock 해시를 검증한 후 두 생성 vendor에 복사한다. CI의 격리 tar 복사에도 이 파일이 포함된다. 고정 CSS 해시는 자동 갱신하지 않는다. 세 lock은 offline package-lock-only로 생성했고 CSS 및 제거된 stock platform 항목 외 패키지 차이가 없음을 대조했다.

공유 workspace vendor의 상대 경로도 허용한다. 정규 파일명/vendor 디렉터리·lock 루트 안의 선언 경로와 실제 경로를 확인하며 절대 경로/외부 symlink를 거부한다. 개발 도구 아래 중첩 Lightning CSS의 버전/bytes도 검사하고, 무관한 workspace의 설치본은 판정에 섞지 않는다. 기존 React 런타임 중복 및 금지 라이브러리 회귀도 함께 통과했다.

[정책](../standards/frontend-libraries.md), [원본·고지](../../vendor/README.md), [canonical 원장](../../frontend-artifacts.json), [pack provenance](../../vendor/lightningcss-provenance.json)를 연결했다. 후보 Q6DD... bytes는 불변이며 UI/tokens 등 기존 5개 원장 해시는 바꾸지 않았다. 공통 8개 산출물 전체 refresh는 부모가 수행한다.

## A/B 후속 finding

- B의 새 P3: [tokens 고지](../../packages/tokens/THIRD_PARTY_NOTICES.md)가 shadcn CSS/MIT 동봉 사실과 충돌하던 문구를 수정했다.
- A-P2-08: [TableRow](../../packages/ui/src/table.tsx)의 전환 속성을 color/background-color/border-color/text-decoration-color/fill/stroke로 제한했다. outline을 제외하고 공식 shadcn Origin/Derived-From 및 Modified 고지를 유지했다.
- Tailwind4 실제 compile 결과에서도 위 여섯 transition-property만 출력됐다. 실제 computed transition과 포커스 outline의 즉시 표시 판정은 부모 A/B 3차 브라우저 delta가 소유한다.
- 두 원 리뷰 보고서는 수정·복제하지 않는다. 부모가 보고한 source2 docs CI의 Ubuntu apt DNS 실패를 우회하도록 설치/브라우저 gate를 약화하지 않았다.

## 실행한 검증

[선택 검증 manifest](evidence/2026-11-11-native-css-policy/manifest.json)와 원본 로그를 같은 디렉터리에 보존했다.

| 검사 | 결과 |
|---|---|
| schema exact/연결/기존 prerelease 선택 회귀 | 8 PASS |
| 정책·공유 경로·개발 그래프·copy 준비 unit | 40 PASS, skip 0 |
| 실제 vendor bytes·source·고지 audit unit | 2 PASS |
| UI 타입 검사 | PASS |
| 기존 baseline의 metadata 거부 재현 | 확인 |
| Tailwind TableRow 전환 compile | outline 제외 확인 |
| 생성 정책·세 lock·vendor 복사 검사 | PASS |

기존 common node_modules를 로컬 symlink로 **읽기 전용 사용**했다. 실제 exclude는 공용 Git metadata의 info/exclude에 /node_modules로 명시하여 directory가 아닌 symlink도 추적되지 않게 했다. 공유 node_modules에 설치/빌드 결과를 쓰지 않았다. 따라서 이 분기의 전체 fresh npm ci/Next build/브라우저 실행 성공을 주장하지 않는다.

필요한 재현 명령:

    PYTHONPATH=. python3 -B -X utf8 tests/test_check_versions.py CheckVersionsTests.test_explicit_prerelease_axis_is_only_for_exact_frontend_checker CheckVersionsTests.test_explicit_semver_axis_accepts_stable_and_build_metadata CheckVersionsTests.test_explicit_semver_axis_rejects_malformed_versions CheckVersionsTests.test_explicit_semver_axis_keeps_prefix_checker_disabled CheckVersionsTests.test_css_artifact_is_required_for_web_and_mobile_builds CheckVersionsTests.test_frontend_policy_rejects_unknown_fields CheckVersionsTests.test_frontend_profile_versions_and_forbidden_are_connected CheckVersionsTests.test_repo_registry_values_load
    node --test packages/ui/test/dependency-policy.node.test.mjs packages/ui/test/native-css-policy.node.test.mjs
    PYTHONPATH=. python3 -B -X utf8 tests/test_native_css_vendor.py
    npm run check:policy
    node packages/ui/smoke/prepare-lock.mjs --css-only
    node node_modules/typescript/bin/tsc --noEmit -p packages/ui/tsconfig.json

## 통합 순서와 미실행 gate

부모가 이 분기를 cherry-pick한 뒤 기존 common 8개 산출물을 refresh하고, 소비자 정책/원장/lock에 반영한다. 실제 macOS auto-WASM CI와 fresh Next smoke/example, A/B의 최종 delta를 검증한다. source2의 기존 11건/10건 FIXED 및 A2의 브라우저 성공은 부모의 불변 리뷰 기록을 따르며 이 후속 작성자의 독립 리뷰로 세지 않는다.

포크 원본 소스의 영구 보존/PR 통합은 부모가 소유한다. 공개 CSS 검증 manifest는 합성 fixture를 사용하고 비공개 소비자 앱 IR/실제 export 증거는 별도로 유지한다. 이 정책 보고서/manifest에 비공개 앱 CSS를 넣지 않았다.
