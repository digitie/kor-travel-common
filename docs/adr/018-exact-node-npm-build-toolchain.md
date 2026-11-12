# ADR-018: private anchor의 정확 Node/npm 빌드·테스트 선택

- 상태: accepted
- 날짜: 2026-11-13
- 근거 문서: [버전 규약](../standards/versions.md), [T-218](../tasks/T-218-radix-library-unification.md)
- Supersedes: ADR-008의 Node/npm 빌드·테스트 선택에 한해 범위 선언 자유를 대체하며 일반 floor/report 정책은 유지

## 컨텍스트

private manifest의 선언만으로는 실제 job·fresh Docker stage의 npm 선택을 보장하지 못한다.
한 단계에서 `npx npm@<version> ci`를 수행해도 다음 bare npm 명령은 다른 CLI를 사용할 수 있다.
C11 공개 패키지는 이미 불변 릴리스이므로 도구 선택을 위해 같은 버전을 재pack할 수 없다.

## 결정

정확 선택값은 `versions.json`의 Node/npm 권고 patch가 소유한다. private 앱 anchor와
workspace private root의 선언·selector·engine-strict 및 실제 실행을 함께 검증한다.
root lock metadata 이외 의존성 graph/version/SRI는 보존한다. 일반 floor는 별도 호환 하한이다.

재사용 frontend guard는 기존 검사 뒤 live 중앙 도구 축으로 runtime을 검증한다.
추가 private manifest와 생산 Node Dockerfile 경로는 선택 JSON 배열로 받되 모든 경로를
동일한 checker로 검증한다. 외부 경로·symlink 우회나 해석 불가 입력은 실패한다.
Node 이미지의 배포판/libc는 앱이 보존하고 정확 tag·digest를 핀하며 중앙 공통 digest는 강제하지 않는다.

## 대안 검토

- 선언만 일치: 실제 CLI 불일치와 stage 경계를 검출하지 못하므로 기각한다.
- 공개 패키지 재발행: 불변 C11과 라이브러리 호환 범위를 불필요하게 변경하므로 기각한다.
- 일반 floor 상향: 호환 하한과 빌드 선택을 혼동하므로 기각한다.

## 결과

명시 선택·runtime guard는 설치·빌드 증거와 구분한다. 정본 환경이 없으면 해당 실행은
NOT_RUN이며 주입한 runtime 음성 대조만으로 실제 runtime PASS를 주장하지 않는다.
CI 순서·needs·fail-fast 감사/최적화는 이 결정 범위 밖이며 기존 step 상대 순서를 유지한다.

## 후속·적용 위치

[`tools/check_node_toolchain.mjs`](../../tools/check_node_toolchain.mjs), root npm scripts,
[개발 환경](../dev-environment.md), 재사용 guard와 각 소비자 private anchor에 적용한다.
소비자 PR은 실제 지원 입력이 있는 불변 ref와 앱별 검증을 사용한다.
T-218과 native 실기기/EAS/스토어 NOT_RUN 상태를 이 도구 후보만으로 완료로 변경하지 않는다.
