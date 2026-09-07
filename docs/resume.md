# 현재 상태와 다음 한 작업

현재 상태의 정본이다. 정책은 [AGENTS](../AGENTS.md), 상세 문서 선택은 [문서 지도](README.md), 선행과 상태는 [task 원장](tasks.md), 실행 순서·출구는 [통합 계획](plan/integration-plan.md)을 따른다. 마지막 갱신: 2026-09-07, Codex.

## 현재 상태

[PR #1](https://github.com/digitie/kor-travel-common/pull/1)의 계획·문서와 [PR #2](https://github.com/digitie/kor-travel-common/pull/2)의 T-003 고지·출처·SPDX 구현을 main에 squash merge했다. [PR #3](https://github.com/digitie/kor-travel-common/pull/3)의 T-005는 f050997에서 두 독립 reviewer PASS, 최초 9개 finding 모두 FIXED다. 완료 기록 CI 34064140128 성공 후 PR #3을 659aa6d로 병합했다. T-015의 npm/PyPI 미게시·common 구현 선행 정리와 T-006의 범위 변경 기록을 [PR #4](https://github.com/digitie/kor-travel-common/pull/4)에 반영했다. 최종 candidate 95c139f는 두 reviewer PASS·누적 9개 finding FIXED이며 CI 34066138272가 성공했다. T-005a uv.lock 파서와 T-005b Poetry·requirements 파서를 완료했다. T-005b 최종 candidate `5b687585cddf6e7a5145911e75647a0e814d9078`은 PR #7 CI 34087885355의 5개 check와 두 reviewer PASS를 확인했고, T-005c code candidate `5807e535c16310c41c21f9efce87b2113aa17ee5`는 PR #8 CI 34097813843과 두 code reviewer PASS, 문서 candidate `7b35ff07b077cef85d7d0d6e0971cacff210374f`는 CI 34099960667과 두 docs reviewer PASS를 확인했다. T-016 최종 candidate `a9fc2f5187bcf2517cb1da54ece9b12ab04b82ff`는 두 reviewer PASS·누적 finding 10건 FIXED, PR #9 CI 34107732188 성공으로 완료했다. T-011 최종 candidate `4680bacdf285f2cc86f1a18cc1de29ff4129f2a8`도 두 reviewer PASS·신규 finding 0·누적 finding FIXED, PR #10 CI 34120043104 성공으로 완료했다. T-101은 PR #12 merge SHA `34c15b6`, main CI `34129164333`, release push source `65397a9`·CI `34129337363`까지 확인해 완료했다. 현재 완료 17개·열린 89개다.

T-005는 Windows Python 3.14.3·WSL Python 3.11.15에서 각각 전체 115 tests 성공·skip 0, SPDX 13개 오류 0, CI 성공이다. 7개 소비자의 고정 입력 48파일·306개 판정을 재현했다. report에 fail 기준 위반 102행이 있어 소비자 정책 준수·제품 검증 완료로 세지 않는다. [최종 리뷰](reviews/adversarial/2026-09-07-t005-post-fix.md)에 원본·경계 재현·한계를 연결했다.

`packages/tokens` 실물은 PR #12의 merge SHA `34c15b688b4c8663c1ca8608ab30336ac9ac0e01`에 반영됐다. 두 독립 적대 reviewer가 최초 BLOCK 12건을 모두 FIXED로 재현하고 신규 finding 0건으로 PASS했다([T-101 통합 리뷰](reviews/adversarial/2026-09-07-t101-post-fix-01.md)). 반복 no-go의 근본 원인은 생성물 drift를 검사 전에 덮어쓰는 CI 순서, 정본에서 중복된 dark/profile 값, 부분적인 dark 시험과 브라우저 상속 미검증이었다. 생성기·CI·전수 값 시험·Tailwind/Chromium probe로 이 계약을 닫았다. merge 후 main CI `34129164333`과 코드 변경 없는 `codex/release-tokens-verify` push CI `34129337363`이 source SHA 일치·6개 job 성공으로 끝났고, 검증 branch는 보존 tag `ci-t101-verify-20260907`로 남겼다. `packages/ui`·Python 패키지, 소비자 build/e2e·시각 검증·npm/PyPI·Release 게시도 후속 또는 사용자 범위 밖이다. T-009의 SPDX 필수 CI 단계·Windows matrix와 비밀/운영 정보 guard를 구현하고 실제 CI를 검증했다. 소비자 저장소는 수정하지 않았다. 사용자 범위 재확인으로 공용 로그인 위젯·인증 프리미티브를 포함하되 인증 서버·사용자 DB·운영 비밀·앱 정책은 소비자 소유로 재정의하는 T-016을 완료했다([ADR-015](adr/015-common-shared-systems-scope.md), [최종 리뷰](reviews/adversarial/2026-09-07-t016-common-scope-post-fix.md)). T-011은 경로별 `resolve/is_file/exists` 분산 검사와 OS별 symlink loop 차이가 반복 no-go의 근본 원인임을 확인해 중앙 입력 경계·조기 반환 방지·오류 redaction·Windows/WSL 회귀 시험으로 해결했다([최종 리뷰](reviews/adversarial/2026-09-07-t011-post-fix-07.md)). 현재 상세 task는 106개, 완료 17개·열린 89개다.

T-009는 [PR #5](https://github.com/digitie/kor-travel-common/pull/5)의 `6e1881b86f017d604ccfa416bd368e5aba24c669`로 병합했고 main CI 34071150863의 5개 check가 성공했다. T-005a도 [PR #6](https://github.com/digitie/kor-travel-common/pull/6)의 squash merge `796445fadb9b4fa6de2f392d6169f31abdccc0fa`로 main에 반영했고 main CI 34081751051의 5개 check가 성공했다. T-005b는 [PR #7](https://github.com/digitie/kor-travel-common/pull/7)의 squash merge `5cf304a7046dd3c7ef1fe1d8a643cc9bbb79c985`로 main에 반영했고 main CI 34088734547의 5개 check가 성공했다. T-005c는 [PR #8](https://github.com/digitie/kor-travel-common/pull/8)의 최종 review A/B PASS·누적 finding FIXED와 PR CI 34097813843의 5개 check 성공을 확인했다. [T005c 최종 리뷰](reviews/adversarial/2026-09-07-t005c-post-fix-03.md)와 [T-005c evidence](tasks/T-005c-workflow-static-report.md#evidence)에 기록했다.

## 다음 한 작업

- 작업: [T-102](tasks/T-102-map-vocabulary-shim.md), READY. T-101의 토큰 정본에 레거시 map·weather·geo 어휘 shim을 순차 추가한다.
- 사용자 재개 지시로 common 구현을 순차 진행한다. npm/PyPI 미게시·다른 저장소 수정 금지와 독립 두 리뷰·PR·CI·병합 경계를 유지한다.
- T-101은 PR #12로 병합했고, 초기 draft PR #11은 동일 source의 기록을 보존한 뒤 닫았다. 외부 소비자 gate와 실제 release 게시를 수행하지 않는다.

## 시작 파일과 검증

[T-102](tasks/T-102-map-vocabulary-shim.md)의 aliases 경로·충돌 검사 계약을 다음 시작 파일로 둔다. T-101의 코드·생성물·review evidence와 source SHA gate는 [완료 task](tasks/T-101-tokens-package.md)에 기록했다. 명령 사다리는 [개발 환경](dev-environment.md#6-검증-명령-사다리), 리뷰는 [agent workflow](runbooks/agent-workflow.md)을 따른다.

## 차단 조건

- 다른 저장소에 쓰지 않는다. 소비자 채택·CI·배포는 해당 저장소의 task와 PR에서 실행한다.
- 사용자 지시: npm·PyPI에 게시하지 않는다. GitHub Release 자산·고정 Git 태그 채널을 유지하며 T-015에서 계정 확보·공개 registry 재평가와 불필요한 선행을 제거했다. 현재는 사용자 재개 지시에 따라 순차 진행한다.
- 사용자는 모든 라이브러리를 GPLv3로 통일할 예정이라고 밝혔다. 현재 common의 GPL-3.0-or-later와 고정 원천 고지를 유지하며 실제 재선언 이전에 과거 원문·권리 gate를 바꾸지 않는다.
- 외부 결정: pinvi 권리(T-020), concierge·docker-manager 권리(T-021), airport 병합 후 현재 기준선·미해결 CI 재확인(T-430), geo React 승인(T-443), pinvi mobile 명시 예외(O-8). 기본값은 승인 evidence가 아니다.
- 아직 배포하지 않은 규칙·계약 초안은 T-104·T-204·T-302에서 실물과 대조한다. 소비자 테스트 개수·버전은 고정 조사 관찰이며 최신 실행값으로 재사용하지 않는다.
- CodeGraph는 이 checkout에 초기화되지 않아 실패했다. 코드 직접 읽기·rg·회귀 테스트로 확인했다.

## 인계 자료

[전체 작업](tasks.md) · [완료 원장](tasks-done.md) · [통합 계획](plan/integration-plan.md) · [architecture](architecture/README.md) · [standards](standards/README.md) · [ADR](adr/README.md) · [journal](journal.md). 이력·survey 전체를 작업 시작 때 통독하지 않는다.
