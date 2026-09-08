# ADR-016: UX 검사기의 MDX 문법 해석을 표준 파서에 위임

- 상태: accepted
- 날짜: 2026-09-08
- Supersedes: ADR-003의 Python stdlib 단독 실행 요구 중 `ux_lint.py`의 MDX 검사 부분
- 근거 문서: [반복 원인](../reviews/adversarial/2026-09-08-t103-root-cause.md), [구조 수정 A](../reviews/adversarial/evidence/2026-09-08-t103-root-fix-reviewer-a.md), [구조 수정 B](../reviews/adversarial/evidence/2026-09-08-t103-root-fix-reviewer-b.md), [T-103](../tasks/T-103-kt-contrast-ux-lint.md)

## 컨텍스트

사용자는 36회 반복된 리뷰의 근본 해결과 실질 구현을 요청했다. Python 단독 실행을 지키려던 MDX 마스킹이 JavaScript·JSX·Markdown의 부분 파서로 커졌다. prefix helper를 상태 스택으로 바꾼 뒤에도 ESM 줄 연속, 정규식과 나눗셈, 비교 연산자와 JSX에서 정상 코드의 누락·오탐이 재현됐다. CommonMark의 들여쓰기 규칙을 MDX에 그대로 적용한 과거 시험도 있었다. 이 문제는 개별 연산자 목록을 계속 늘리는 방법으로 종료할 수 없다.

## 결정

1. `.mdx`는 `@mdx-js/mdx`의 구문 트리에서 code·inlineCode·JavaScript comment 범위를 받아 제외한다. 직접 만든 MDX lexer와 fallback은 제거한다. 패턴 판정·baseline·Git 추가행·출력은 기존 Python CLI가 담당한다.
2. 파서 의존은 common 루트의 `package.json`·`package-lock.json`으로 고정한다. 버전 업은 lock 변경과 누적 문법·CLI 시험을 함께 검토한다. Node 버전은 기존 `versions.json`을 따른다. MDX 파일이 없으면 Node를 호출하지 않는다.
3. `tools/mdx_mask.mjs`는 입력을 구문 분석만 하고 import·표현식·사용자 플러그인을 실행하지 않는다. 한 CLI 실행의 MDX 파일을 한 프로세스에 묶어 전달한다. 원문은 stdin으로 전달하며 예외의 원문·경로·stack을 밖으로 내보내지 않는다.
4. 파서 미설치·실행 실패·시간 초과·잘못된 MDX는 exit 2다. 부분 성공 report나 빈 finding PASS로 대체하지 않는다. 문법 오류는 소비자가 자신의 MDX 컴파일에서 수정한다.
5. AST의 UTF-16 위치를 사용해 가리되 Python의 Unicode 문자 수와 줄 종결자 위치를 보존한다. JS 문자열·template는 문서 인용이 아니므로 계속 검사한다.
6. Python 패키지 추가 의존은 없다. 다른 stdlib 도구와 TS/TSX/CSS 검사 경로는 유지한다. 설치·Windows/WSL·CI 명령은 [개발 환경](../dev-environment.md)이 정본이다. common은 독립 서비스가 아니며 npm/PyPI에 게시하지 않는다.

## 대안 검토

- stdlib 수동 lexer 유지: 정상 JavaScript 구문을 계속 재구현해야 하므로 반복 원인을 남긴다.
- 파서 실패 시 수동 lexer fallback: 유효성 오류와 미탐지를 구분할 수 없어 조용한 PASS가 재발한다.
- MDX 전체를 검사 제외: 기존 UX 패턴 gate를 없애므로 채택하지 않는다.
- 외부 파서와 명시적 입력 오류: MDX 실행에 Node가 추가되지만 구문 해석 책임과 설치 실패를 검증할 수 있어 채택한다.

## 결과와 이관

MDX 검사 전에 common checkout 루트에서 `npm ci`를 실행한다. Python 스크립트 한 파일만 복사한 환경은 MDX를 검사할 수 없으며 `tools/mdx_mask.mjs`와 잠긴 Node 의존을 함께 준비해야 한다. 토큰/UI/Python 라이브러리 소비 자체에 이 개발 도구 의존이 추가되는 것은 아니다.

과거 호환 추정과 달리 일반 본문의 `const value =`는 ESM을 열지 않고 `//` 행은 JS 주석이 아니다. 실행 예제는 `export` 또는 실제 MDX 표현식·JSX에 두고 문서 예제는 code fence/inline code로 표시한다. ESM 뒤 Markdown으로 전환할 때 빈 줄을 두고 여러 줄 blockquote는 각 줄의 `>`를 명시한다. MDX는 indented code를 지원하지 않으므로 들여쓰기만으로 코드를 제외하지 않는다. 이 차이 때문에 바뀐 시험은 입력 또는 기대값의 근거를 기록하며 검사 대상을 삭제해서 통과시키지 않는다.

문법 근거는 [MDX 공식 설명](https://mdxjs.com/docs/what-is-mdx/)(문서 수정 2025-01-27, 조회 2026-09-08)과 이번에 고정한 MDX 3.1.1의 구문 트리다. 구문 분석 성공은 실제 앱 compile/render/e2e 성공이 아니다.

## 후속·적용 위치

[T-103](../tasks/T-103-kt-contrast-ux-lint.md)의 문맥·좌표·입력 오류·설치 수용 기준, [개발 환경](../dev-environment.md), [tools](../../tools/README.md), [CHANGELOG](../../CHANGELOG.md)에 반영한다. 실제 소비자 MDX 및 커스텀 플러그인 채택 검증은 소비자 이관 task가 소유한다.
