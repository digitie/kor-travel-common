# T-103 반복 리뷰 근본 수정과 최종 재검토

- Review ID: `T103-PARSER-POST-FIX-20260908`
- 종류: 전문 리뷰어 서브에이전트 2인 독립 full review, coordinator `/root`.
- 상태: COMPLETE
- 최종 verdict: PASS — A/B 모두 PASS, 신규·잔여 P0/P1/P2/P3 0건.
- 최종 독립 실행: A 2026-09-08 20:01:04~20:04:13 KST, B 20:01:14~20:04:13 KST. 이후 각 원본을 확정하고 두 결과를 교차 확인했다.
- 코드 후보: `49d3867fd8fb941fde260966d2b4b3296c0f3d77`, tree `e2bfb5702ad976bfda5d47ddc6e52f2f735e440b`.
- 이전 제품: `31e3f0affd2ce1c32ac912bedf687d82c12ee876`; 상태 스택 시도: `b013ab0d2e95e3d892f6dbfa42042389582ea8a9`.
- 범위: [T-103](../../tasks/T-103-kt-contrast-ux-lint.md)의 대비·UX 검사기, 예제·시험·Node 의존·CI·문서와 사용자 요청인 36회 반복의 근본 해결.
- 범위 밖: 다른 저장소 수정·소비자 build/e2e·실제 MDX compile/render·npm/PyPI 게시·다음 task 착수.

## 1. 근본 원인과 조치

주석·문서 코드 제외라는 작은 요구에 Python 단독 실행 제약을 결합하면서 MDX·JavaScript 부분 파서를 직접 만들었다. 반례마다 prefix·연산자·줄 경계를 추가했고, 같은 문맥을 여러 helper가 추정했다. 실제 MDX 파서 없이 CommonMark를 간접 근거로 삼아 시험 기대값에도 잘못된 문법 가정이 들어갔다. 리뷰어의 확장 반례는 임시 파일에 남아 작성자의 저장소 시험이 다음 변형을 막지 못했다.

[첫 분석](2026-09-08-t103-root-cause.md) 후 상태 스택으로 정리한 시도 역시 정상 ESM 줄 연속·정규식·비교 연산자 결함으로 두 reviewer BLOCK이었다([A](evidence/2026-09-08-t103-root-fix-reviewer-a.md), [B](evidence/2026-09-08-t103-root-fix-reviewer-b.md)). 상태 소유권을 정리하는 것만으로는 JavaScript 문법 재구현 자체를 없애지 못했다.

[ADR-016](../../adr/016-mdx-parser-for-ux-lint.md)으로 MDX 검사에 한해 stdlib 단독 요구를 대체하고, 수동 MDX 파서 약 500줄을 제거했다. 고정 `@mdx-js/mdx` AST가 문법을 소유하며 Python은 패턴·baseline·추가행 판정을 맡는다. 입력을 실행하지 않고 parse만 하며 문법·설치·실행 실패는 exit 2다. 이식 경계의 마지막 BOM 오류는 parser가 제외한 첫 한 문자를 모든 범위의 원문 좌표에 공통 반영해 수정했다.

운영 측면에서는 기존 정본의 `BLOCK/CONDITIONAL/PASS`와 심각도별 disposition을 실제 manifest에 적용했다. post-36의 상대 결과 조기 공개는 독립 검토로 인정하지 않고 기록을 보존했다. 이후 두 실행은 각각 동일 불변 manifest·분리된 worktree·원본 확정 전 결과 비공개를 지켰다. 이번 누적 자료·변형·CLI·실패 주입은 저장소와 CI에서 먼저 실행한다. 최종 결과 기록은 기존 workflow의 closure artifact 절차로 처리하며, 기록만 추가했다고 같은 제품 리뷰를 다시 시작하지 않는다.

## 2. 기준선과 독립 원본

| 단계 | 공통 manifest | A | B |
|---|---|---|---|
| 수동 상태 스택 | [기준선](evidence/2026-09-08-t103-root-fix-manifest.md), `b013ab0` | [원본 BLOCK](evidence/2026-09-08-t103-root-fix-reviewer-a.md) | [원본 BLOCK](evidence/2026-09-08-t103-root-fix-reviewer-b.md) |
| 실제 MDX 파서 | [기준선](evidence/2026-09-08-t103-parser-manifest.md), `31e3f0a` | [원본 BLOCK](evidence/2026-09-08-t103-parser-reviewer-a.md): 신규 A-P1-38 | [원본 PASS](evidence/2026-09-08-t103-parser-reviewer-b.md): 신규 0 |
| 원문 좌표 보정 | [기준선](evidence/2026-09-08-t103-parser-post-fix-manifest.md), `49d3867` | [최종 PASS](evidence/2026-09-08-t103-parser-post-fix-reviewer-a.md) | [최종 PASS](evidence/2026-09-08-t103-parser-post-fix-reviewer-b.md) |

A는 AST 문맥·Unicode·시험 기대값을, B는 의존·CI·실패·비실행·Git 판정을 우선 검토했다. 각 원본에 실행 ID·시각·명령·관찰 HEAD/tree·clean을 기록했다. 원본은 이후 실행 결과로 덮어쓰지 않는다.

## 3. Finding disposition

| ID·원 심각도 | 실패 형태·영향 | 조치·재검증 | 상태 |
|---|---|---|---|
| A-P1-35 | ESM 줄 연속의 template 패턴 누락 | 실제 파서로 위임, ESM 함수·클래스·삼항·chain 누적 입력 및 A 독립 90변형/42 CLI | FIXED, parser A 원본 확인 |
| A-P2-36 | 비교 연산자를 JSX로 잘못 해석해 주석·fence 오탐 | AST comment/code 범위, 비교·후속 fence 회귀 | FIXED, parser A 원본 확인 |
| A-P1-37 | Airport dark 실패를 성공으로 기록 | 실제 10미달·신규6·exit1로 [evidence](../../evidence/t103-kt-contrast-ux-lint.md) 정정, T-431 외부 gate 유지 | FIXED, parser A 원본 확인 |
| B-P1-30 | `in` 뒤 정규식의 중괄호로 표현식이 조기 종료해 P6 누락 | 실제 JS AST, in/instanceof/제어문/postfix 회귀 | FIXED, parser B 원본 확인 |
| B-P2-31 | 공백 없는 비교 뒤 fence의 P8 오탐 | 실제 MDX AST, 컨테이너·줄 종결자·CLI 변형 | FIXED, parser B 원본 확인 |
| B-P2-32 | Airport dark 표의 실패 은폐 | A-P1-37과 같은 정정, 원 P2와 관점은 보존 | FIXED, parser B 원본 확인 |
| A-P1-38 | 첫 BOM을 제외한 AST offset으로 `window.confirm`의 마지막 문자를 가려 P8 누락 | 모든 AST 범위의 원문 offset 보정, exact-mask54·BOM18파일/plain-base36 및 누적 자료 | FIXED, 최종 A/B 독립 재확인 |

앞서 확인한 A-P1-31/32·A-P2-33/34 및 B-P1-28·B-P2-27/29의 원 반례는 실제 파서 원본에서 FIXED로 재확인했다. 더 이전 누적 반례는 저장소 회귀와 보존 원본에 연결하며 과거 모든 임시 스크립트를 새로 실행했다고 주장하지 않는다. 일반 본문 `const`·`//`와 indented code의 기존 추정은 ADR-016의 명시적 문법 변경으로 구분한다. 심각도 하향이나 P1 연기는 없다.

## 4. 최종 후보 검증

| 계층 | 명령·관찰 | 결과 |
|---|---|---|
| Windows 작성자 전체 | `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py'` | 322실행·성공, skip0, 190.810초, exit0 |
| 누적 문맥·좌표·CLI | `python -B -X utf8 -m unittest tests.test_ux_mdx_context -v` | 8실행·성공, skip0, 12.367초; 66입력/498변형·delimiter120·exact-mask54·BOM18파일 및 Git 추가행 |
| AST 기대값 | `node tests/verify_mdx_reference.mjs node_modules/@mdx-js/mdx/index.js` | 498 PASS, 제외0. 제품과 같은 파서이므로 두 독립 파서 일치 증거가 아님 |
| 후보와 기록 CI | [34218404453](https://github.com/digitie/kor-travel-common/actions/runs/34218404453), source `ef91306f3c29ec0bd753df4229428b6eb90965c4` | 6 job success. `49d3867` 이후는 확정 raw2개·manifest1개뿐 |
| CI Python | 위 run의 tools Windows/Ubuntu 및 docs | 322수집: Windows320실행+jsonschema2skip, Ubuntu319실행+jsonschema2·Windows전용1skip. skip은 성공 건수에서 제외 |
| CI packages | tokens check/build/test·pack/install smoke | 7 tests 성공 및 tarball 설치 성공. 실제 소비자 실행 아님 |

이전 코드 push CI `34217256747`은 manifest push로 취소됐으며 성공으로 세지 않는다. 이전 manifest CI `34217374527`의 6 job 성공과 B의 WSL317실행·3skip도 최종 후보 자체의 실행 수로 바꾸지 않는다. 작성자의 이전 WSL 전체 두 실행은 NTFS 의존 로딩으로 중단했으며 완료 시험으로 집계하지 않는다.

첫 파서 전환에서 기존 UX 시험 8개가 실패했고, 실제 MDX 문법과 다른 fixture·기대값을 고친 뒤 통과했다. BOM 시험 초안의 이중 FEFF 바로 뒤 fence 기대도 실제 문법과 달라 줄 경계를 명시했다. 실패 기록을 삭제하거나 잘못된 파일을 PASS 처리하지 않았다.

## 5. 종료 조건과 한계

두 최종 원본에서 A-P1-38과 전체 변경의 재검토가 끝났고 신규 finding은 없다. A는 양 OS Unicode120 전체 마스크와 BOM18입력·plain/base36파일 관찰을, B는 양 OS BOM90입력·270 CLI 및 기존324 CLI를 독립 확인했다. 양 OS 집중 시험은 두 reviewer 모두 8개 성공·skip0이다. 앞선 P1/P2의 FIXED 판정도 유지했다.

| 최종 원본 | 원본 commit | 파일·blob SHA256 |
|---|---|---|
| A | `c59395527252557d3b7a5df63beb3903ddcfd3ba` | `2FF3276F2964BF74EA248B87079231BF4B0AC254ECA0A66E4A3CDCFB21FB4F7F` |
| B | `3e2ca063a1d835000e64bae384adc723303f9aa5` | `2315A060606A743E58D7CEA8F78FD7F4B491CC1AB5941F4BD8643EA275C517E6` |

두 원본을 수정 없이 보존하고 위 digest가 checkout에서도 같은지 확인했다. 이전 parser 원본 digest는 A `137053CC2A7F069602D0DFE0003C6DD7AC07EE72DD285669F5F5C38ADA1F2FED`, B `7D794C3DC70AD4B765C0E6EABA6247B69553843D3CE01B7B7C113B9000EAD058`다. 완료 기록은 규범·제품 변경 없이 원본·disposition·task 상태를 반영하며 최종 PR head의 CI 성공 후 병합한다.

소비자 build/e2e·커스텀 MDX 플러그인·실제 compile/render/browser·앱 baseline 등록은 `NOT_RUN(소비자 이관 task)`이다. Airport dark의 예상 FAIL은 T-431에서 실제 값·채택으로 검증한다. 이 PR은 common 검사 도구의 완료만 판정한다. npm/PyPI와 Release 게시를 수행하지 않으며, 사용자 최신 요청에 따라 [PR #20](https://github.com/digitie/kor-travel-common/pull/20) 병합 후 대기한다.
