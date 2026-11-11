작성 UTC: 2026-11-11T15:52:30.720114+00:00

# A(Mill) COMMON source3 이후 CI 보충 기록 — 00ddd65

이 문서는 7e immutable source3 원문을 변경하지 않는 별도 CI 증거다.

- 관찰 대상 common: 00ddd65be56a1955a4cee1a458a8cc274946fbe1.
- [GitHub run43050853120](https://github.com/digitie/kor-travel-common/actions/runs/43050853120).
- [packages job130627252820](https://github.com/digitie/kor-travel-common/actions/runs/43050853120/job/130627252820): completed / SUCCESS.
- A가 GitHub connector로 run jobs, packages steps, packages 전체 로그를 직접 조회했다. 부모의 성공 공유만으로 독립 API 관찰을 대체하지 않았다.
- 실행 시각·API 응답 원문·직접 확인한 Git diff: review-A-common-evidence-postfix-3/ci-00ddd65.json.

packages 로그에서 exact SOURCE_SHA=00ddd65와 checkout/SHA 확인 성공, 공식 MCR 이미지 및 기동 preflight를 확인했다. 이미지 digest는 bc4fbb329a25287ed23e9216c97063646abdd1bf2da669a9895fa3e2078b2302, tag는 mcr.microsoft.com/playwright:v1.65.0-noble이다. 실제 출력은 Playwright1.65.0 / Chromium158.0.8127.18 / /ms-playwright/chromium-1254/chrome-linux64/chrome이다.

packages의 tokens 빌드·검사·시험, UI/설치 산출물 Next 검증, tarball 설치 smoke가 모두 success이다. 로그에서 UI101 pass, 실제 packed webpack 및 Turbopack builder 실행, Radix+Dialog browser65 pass(41.0초), Turbopack example 실행을 확인했다. 이는 로컬 성공과 구분되는 공식 MCR 환경의 remote 성공 증거다.

7e→00ddd65의 전체 Git diff는 packages의 SHA assert 직전에 다음 workflow 한 줄을 추가한 것이다:

~~~sh
git config --global --add safe.directory "$GITHUB_WORKSPACE"
~~~

불변 c8 manifest는 변경하지 않았다. 위 두 source 사이 UI/token/pack payload 변경은 없다. c8 source670 및 기존 pack SHA 대조 결과는 source3 원문의 기록을 그대로 사용한다.

한계와 disposition:

- 이 새 source에서 MCR Git ownership 때문에 packages를 실행하지 못하던 문제는 해소된 증거가 있다. 7e에서 성공했다고 소급하지 않는다.
- API 관찰상 같은 run의 docs, secret-scan, tools(Windows/Ubuntu)는 FAILURE다. docs의 문서·계획·회귀 검사 step과 check-versions 자기 검사는 SUCCESS다. 부모가 공유한 frontend/python/selftest 성공은 이에 대한 추가 근거로 기록하되 전체 run 성공으로 확대하지 않는다.
- UTF8 archive scanner 수정은 아직 후속 delta이다. 이 보충 기록으로 전체 merge gate를 PASS로 바꾸지 않는다.
- A-P2-08 FIXED와 신규 A-P2-09 OPEN(P2), source3 원문 CONDITIONAL/BLOCK 판정은 그대로다. source3 manifest 또는 이전 원문을 덮어쓰지 않는다.
- 앱 consumer/export/배포, NativeCSS macOS 상태 및 원 finding은 이 CI 보충 범위가 아니다.


## c8와 CI 실제 pack의 직접 hash 대응

A가 직접 조회한 packages 전체 로그에서 npm notice의 축약 SRI가 아닌,
최종 검증 출력의 UI/tokens 전체 SRI를 추출했다. 두 값 모두 immutable
manifest3의 integration8 integrity와 문자열 전체가 일치함을 assertion으로 확인했다.

- @kor-travel/ui: sha512-RaBKVxmLJi7ZoQZqs28BaTmXzxpHsihV7D/VvR/vnDeqXtOvtiZawAo6K3CtbuZ37daKqMhGCG5hC5p42pI3Ug== (MATCH)
  - 실제 로그: 2026-11-11T15:43:01.2527071Z @kor-travel/ui: sha512-RaBKVxmLJi7ZoQZqs28BaTmXzxpHsihV7D/VvR/vnDeqXtOvtiZawAo6K3CtbuZ37daKqMhGCG5hC5p42pI3Ug==
- @kor-travel/tokens: sha512-juHDU+d/0GtLmylPyx9kDur2GwnzV5izAtRpzfqhxvbMjPlVfrbEanLBcdqC+EdmifO7StrMlcQJso239gv5PA== (MATCH)
  - 실제 로그: 2026-11-11T15:43:01.2525380Z @kor-travel/tokens: sha512-juHDU+d/0GtLmylPyx9kDur2GwnzV5izAtRpzfqhxvbMjPlVfrbEanLBcdqC+EdmifO7StrMlcQJso239gv5PA==


따라서 이 remote의 packed UI/tokens bytes는 c8와 동일하며 단순 source 동일성 추론에 그치지 않는다.
이 hash 증거와 공식 MCR의 UI101/policy41/tokens9, packed browser65 PASS(41.0초, skip0),
webpack/Turbopack 성공을 함께 보존한다. Python 및 scanner에 관한 다른 job의 범위나
7e 원본 verdict를 소급 변경하지 않는다.
