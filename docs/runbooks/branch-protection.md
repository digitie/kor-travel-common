# common branch protection 설정 절차

이 문서는 common의 PR 필수 검사 이름과 GitHub ruleset 갱신 절차를 정의한다. workflow 정본은 [docs.yml](../../.github/workflows/docs.yml), CI 계약은 [CI 규약 §9](../standards/ci-deploy.md#9-common-자체-ci)다. T-009에서는 이 절차를 작성하며 원격 설정을 적용하지 않는다.

## 적용 범위와 필수 검사

`main`과 `codex/release-*`에 PR 필수, linear history, force push·삭제 금지를 적용한다. bypass 허용 계정과 긴급 변경 절차는 설정을 실제 적용하는 PR에서 유지자가 명시한다. 현재 설정 여부는 GitHub의 실제 ruleset에서 확인하며 문서만으로 적용 완료를 판단하지 않는다.

필수 status check 문자열은 matrix가 확장된 실제 check run의 이름을 사용한다.

| 현행 check 이름 | 책임 |
|---|---|
| `docs` | 문서·계획·회귀·공백·운영 정보 |
| `tools (ubuntu-24.04)` | Linux 도구·SPDX·검사기 |
| `tools (windows-2025)` | Windows Tier 2 도구·SPDX·검사기 |
| `secret-scan` | 비밀 값 전체 트리 검사 |
| `check-versions` | registry 자체 검사·고정 fixture report/step summary |

아직 없는 packages·python-package check는 등록하지 않는다. T-101·T-201·T-302가 실제 job을 구현하고 성공한 뒤 해당 PR에서 이 목록과 ruleset 변경안을 함께 갱신한다.

## 이름 변경과 적용 검증

1. workflow를 바꾸기 전에 현재 check 이름·ruleset 요구 목록을 조회한다. matrix job ID `tools`와 실제 check 이름을 혼동하지 않는다.
2. 변경 PR의 모든 실제 check가 성공하고 두 독립 리뷰가 끝난 뒤 이름 목록을 대조한다. `gh pr checks <PR>` 또는 해당 commit의 check runs를 사용한다.
3. 유지자가 검토한 설정 변경으로 새 check를 추가하고 기존 check를 제거한다. 새 이름이 생성되기 전에 필수로 등록해 PR을 영구 대기시키지 않는다.
4. main/release push에서도 필수 job이 빠지지 않고, 각 job의 summary source SHA와 run head SHA가 검사 대상 commit과 같은지 확인한다. PR head의 성공으로 다른 merge commit을 대체하지 않는다.
5. 설정 전후 결과·대상 branch·검사 이름을 해당 task evidence에 남긴다. 설정을 실행하지 않았으면 `NOT_RUN(문서만 작성)`으로 기록한다.

실제 설정이 잘못되어 merge가 막히면 원인을 확인한 뒤 설정 변경을 되돌린다. 검사를 생략하거나 성공으로 위장해 우회하지 않는다.
