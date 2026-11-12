# Common build rules e1d0 原A postfix2 독립 리뷰 — SOURCE BLOCK

- Execution ID: A-COMMON-BUILD-e1d0-20261112T172533Z
- 원문 고정 UTC: 2026-11-12T17:25:33.236486+00:00
- 원 리뷰어 A/Mill. 구현 비참여. 상대 CURRENT 원문/판정 접근 0.
- source: `e1d0f01ef05b913e5f311a4d3ae2922a25a676c3`
- observed tree: `aea8c2ad8a7b6ffc6550d7a576c01d50551b8bb1`
- base: `678a5bcf0150ac0386bfa86106e7e0f4f77e8639`; prior BLOCK: `c4cc78781638808490c0ea540fbb38200b577346`.
- manifest: `validation/review-common-build-rules-e1d0-20261113/manifest.json`
- manifest SHA256: `5b391bc0200766c2cb9ed68fb4940924ccdd2f545b729aa9455e857d8af944f8`
- own evidence: `validation/review-A-common-build-rules-e1d0-2-evidence/`.
- 원 c4cc 보고서 SHA256 `87ceded53ac283ec11a6f39092778c8279dc0a1489b12abd23ff82eb876fbff2` 재확인, 불변 보존.

## 판정

**SOURCE BLOCK. P0 0 / P1 0 / OPEN P2 2건(기존 1 + 신규 1) / P3 0.**

기존 확정 RED 7개는 모두 해결됐다. 다만 P2-01의 유효 `.npmrc` 의미 검증은 인용 key/section 경계에서 계속 우회되므로 완전히 닫지 않는다. P2-02/03/04는 아래의 원 finding 범위에서 FIXED다. 별도로 shell `&` 명령 경계가 앱 인수 구분자 뒤에 숨는 신규 P2-05를 확인했다. 두 OPEN 건 모두 **수정 필요/예외 이관 없음**으로 권고한다. 현재 정상 Common workflow가 공격 구문을 사용한다거나 P0/P1 운영 장애가 발생했다는 주장은 아니다. e1d0 CI가 성공하더라도 이 source 판정을 대신하지 않는다.

## 자기 원 finding별 disposition

| ID | 판정 | 본인 재확인 |
|---|---|---|
| A-COMMON-BUILD-P2-01 | **OPEN** | 원 `engine-strict=true; force=true`는 이제 거부. 그러나 인용 `"force"=true`는 같은 보호 해제를 통과시키며 section 내부 strict를 전역 strict로 오인한다. 아래 잔여 근거 참조. |
| A-COMMON-BUILD-P2-02 | **FIXED** | 원 strict false/부정 2개 모두 거부. exact62와 own 추가 exec JSON 분리 false 거부, 명시 true·분리 true 수용 확인. `:130–149`의 허용 옵션/유효 strict 검사로 원 토큰 존재만의 문제 수정. |
| A-COMMON-BUILD-P2-03 | **FIXED** | 원 heredoc/backtick escape 2개 모두 거부. 새 `:154–166`이 미지원 지시문/본문 형식을 fail-closed로 거부. 연속행 heredoc 거부와 기본 backslash 지시문 정상 수용도 직접 확인. 모든 Docker grammar가 완전하다는 포괄 승인은 아님. |
| A-COMMON-BUILD-P2-04 | **FIXED** | 원 location global/npx package 2개 모두 거부. 새 install·npx selector 및 명령 허용목록을 확인. pinned 뒤 `npx -p npm@old`도 거부하고 정상 run/start 전달 인수는 수용. 아래 신규 shell instruction 경계 결함과 구분. |

## 기존 A-COMMON-BUILD-P2-01 잔여 — INI key/section 의미와 다른 line scan

- 위치: `tools/check_node_toolchain.mjs:55–67`, 특히 `:59–60`; 규범 `docs/standards/versions.md:50`의 유효 strict/force 요구.
- 재현 1: 정본 private metadata/selector를 둔 `.npmrc`가 다음이면 exact helper는 **ok:true**다.

```ini
engine-strict=true
"force"=true
```

- npm 12.0.1 vendored INI parser는 이를 전역 `engine-strict:true, force:true`로 읽는다. checker는 인용 key를 무관한 행으로 건너뛰어 force=false 기본값을 유지한다. 따라서 원 finding의 ‘force로 strict 무력화’가 다른 유효 표기로 그대로 남는다.
- 재현 2: `.npmrc`가 다음이면 역시 **ok:true**다.

```ini
[unrelated]
engine-strict=true
```

- 같은 parser는 이를 `unrelated` 객체 내부 값으로 읽으므로 전역 engine-strict를 설정하지 않는다. checker는 section 경계를 무시하고 strict=true로 승인한다. 실제 canonical npm CLI 설치를 실행한 증거는 아니며, 정확 vendored parser의 직접 결과와 helper의 직접 결과 차이다.
- own `own-regressions.log`의 `force-quoted-key`, `section-strict-only` 및 `own-ini-semantics.log` 4PASS 참조. 공식 [npmrc 문서](https://docs.npmjs.com/cli/v12/configuring-npm/npmrc/)는 INI 구문/parser 사용을 명시한다. [npm12.0.1 동봉 parser](https://github.com/npm/cli/blob/v12.0.1/node_modules/ini/lib/ini.js)의 key unquote와 section 처리를 읽고 작은 pure 대조를 직접 실행했다.
- 영향: 도구 선언은 정본이지만 실효 strict가 꺼진 private anchor를 새 gate가 승인한다.
- 권고: 지원하는 INI 의미에 맞게 전역 key/중복/인용을 해석하거나, 지원하지 않는 quoted key·section 등 모호한 구조를 명시적으로 거부한다. 단순히 이 두 문자열만 차단하는 대신 유효 force/strict 값이라는 계약을 지켜야 한다. 무관한 peer/lifecycle 설정은 보존한다.
- disposition: **P2 OPEN, 수정 전 수용 불가 권고**. 원 literal 공격 수정 성공을 취소하거나 옛 원문을 덮어쓰지 않는다.

## 신규 A-COMMON-BUILD-P2-05 — shell `&`를 npm의 앱 인수로 잘못 취급

- 위치: `tools/check_node_toolchain.mjs:85–88`, `:126–130`, Docker command 분리 `:175–180`.
- 정본 Node tag/digest FROM과 canonical global npm pin 뒤 다음 RUN을 제출한다.

```dockerfile
RUN npm run build -- & npm install --global npm@11.19.1
RUN npm ci --engine-strict
```

- 실제 helper 결과: **ok:true, errors:[], checkedNodeImages:1**. own `ampersand-reselect`.
- 원인: shell 검사에서 단일 `&`를 거부하지 않는다. `&&`만 command로 나눈 뒤 npm `--` 뒤 전부를 앱 인수로 제외한다. 하지만 shell에서 `&`는 npm에 전달되는 인수가 아니라 앞 명령을 백그라운드 실행하고 다음 npm을 별도 호출하는 제어 연산자다. 뒤의 global old npm 선택을 검사하지 않은 채 stage.pinned=true가 유지된다.
- 직접 대조: `/bin/sh`에서 `npm`을 출력만 하는 함수로 치환한 **mock**을 실행했다. raw에 `MOCK_NPM <run> <build> <-->` 및 `MOCK_NPM <install> <--global> <npm@11.19.1>` 두 호출이 찍힌다. 실제 npm·Docker·설치 동작은 0이다. `own-shell-boundary.log`, `semantic-proof.json` 참조.
- 영향: Docker의 literal npm selector/strict 검사와 명령 경계가 다르므로 다른 npm 설치를 제출해도 guard가 통과한다. 임의 앱 script 내부를 분석하라는 요구가 아니라 제출된 RUN 자체의 shell 제어문자 경계를 지키라는 요구다.
- 권고: bounded 문법에서 미지원 shell 제어/리다이렉션을 먼저 fail-closed로 거부하거나 실제 lexical command 경계를 보존한다. npm `--`는 shell parsing 뒤에만 앱 인수의 의미를 가지며 shell 연산자를 보호하지 않는다. 정상 JSON exec-form/정상 전달 인수/지원 `&&` 대조를 유지한다.
- disposition: **P2 신규 OPEN / 수정 요청**. 기존 P2-04의 명시 selector 옵션 수정과 중복 집계하지 않는다.

## 직접 실행·테스트 원시 증거

1. `/usr/local/bin/node --test <E>/fixture/tests/check_node_toolchain.test.mjs`: **62PASS/0FAIL/0SKIP**, exit0. exact Git helper/tests/versions 복사본. source 파일 변경 0.
2. `/usr/local/bin/node --test <E>/own-seven-closure.test.mjs`: **9PASS/0FAIL/0SKIP**, exit0. 이전 own 공격 7개와 정상/직접 잘못된 FROM 2개를 같은 payload로 재사용했다. 이전 exploratory legacy 단독 항목만 제외했으며 원 fixture/log는 불변이다.
3. `/usr/local/bin/node --test <E>/own-regressions.test.mjs`: **9PASS/4FAIL/0SKIP**, exit1. 3FAIL은 위 quoted-force/section/ampersand false PASS. 나머지 1FAIL `strict-quoted-key`는 올바른 quoted strict를 checker가 거부한 호환성 관찰이다. 제한 문법의 명시 fail-closed 선택도 가능하므로 이를 별도 결함으로 세지 않았다. 이 탐색 테스트 기대값을 바꿔 녹색으로 만들거나 원 실패를 삭제하지 않았다.
4. `/usr/local/bin/node --test <E>/own-ini-semantics.test.mjs`: **4PASS/0FAIL/0SKIP**, exit0. npm v12.0.1 태그의 vendored pure INI 단일 파일을 own evidence에 보존하여 인용 key/section/마지막 false 의미를 검증했다. dependency install/실제 npm CLI 실행이 아니다.
5. `site path#%`의 exact helper 직접/alias/preserve-symlinks-main 3형식에서 정상 입력 exit0, literal force 입력 exit1이 일치했다. quoted-force는 모두 잘못된 PASS/exit0로 일관되게 나타나 CLI/API가 같은 잔여 결함을 공유한다. 경로 특수문자 때문에 CLI가 조용히 생략되는 현상과 구분한다. import-only 비자동 실행 대조도 exact62에서 통과했다.

직접 테스트 Node는 **v22.22.2**다. canonical22.23.1/npm12.0.1 runtime PASS로 확대하지 않는다. TMPDIR/TMP/TEMP는 own validation 하위이며 기존 테스트 정리 후 own tmp 잔여0, 타 owner 캐시/fixture 삭제0.

| 로그 | SHA256 |
|---|---|
| original62.log | `cdd1f1eb5095b1ab9a90c80610c8ae7ebcbe8c56a739b0dcd1a9f39f9897cff9` |
| own-seven-closure.log | `f2df4dd4ba78a0145f9ab6788ac0fd16569136862a74e8fc13ee7d6245d2d702` |
| own-regressions.log | `5c0ea60274c874ab52adbdb3fab6aec2e4ccd56b5ee0a0cc3b216213808ad79c` |
| own-ini-semantics.log | `fd6e03a7e3df794305bb304921bbb561ced98151392ee82d6b8be77da16dabdc` |
| npm12-ini.cjs | `007123836ffec243f41c8b35584fb3db0498aa12a440a9e0efc675d0000f4c32` |

## 바이트·규범·caller 경계

- manifest SHA, exact tree, 21 Git blob/SHA256/bytes와 base→head 경로 집합을 직접 검증했다. c4cc→e1d0 변경은 helper/tests/versions 규약/journal/resume 5개뿐이고 나머지16경로는 bytes 동일이다. 움직이는 작업트리를 입력으로 사용하지 않았으며 끝 tracked dirty 관찰0.
- 공개 source/vendor/frontend policy 193개를 base의 기존 SHA와 다시 비교해 **193일치**. root manifest/lock/registry/workflows는 c4cc와 동일하므로 원 graph/SRI/floor/예외8개 정리 검토를 그대로 연결할 수 있다. 새 C11 pack 검증·재발행 주장은 0.
- 문서는 유효 force=false, npm 자체 옵션 허용목록, heredoc/nondefault escape 거부, 앱 `--` 뒤 인수 구분과 old common-ref에 script 없으면 실패함을 명시한다. guard optional JSON argv 전달과 기존 단계 순서는 불변이다. CLI alias의 argv/module 양쪽 realpath 비교 및 import API 보존을 확인했다. old code-ref/tag 입력이 형식상 허용된다는 것과 새 script 실행 호환은 별개라는 제한을 공개했다.
- canonical-runtime-receipt의 입력7개가 **현재 exact helper/tests까지 모두 일치**, node/npm/runtime/builtin log4개의 SHA도 일치했다. owner actual Node22.23.1/npm12.0.1/runtime PASS/62PASS는 기존 실행 증거로 감사했다. 본인의 canonical 환경 실행은 NOT_RUN.
- 기존 c4cc47/CI 성공, original raw/hash, 옛 탐색 실패와 새 후보 실행을 구분했다. 상대 CURRENT 보고서를 읽지 않았고 source journal/tests에 포함된 수정 설명만 같은 입력으로 검토했다.

## NOT_RUN·승인 한계

e1d0 GitHub exact CI 조회/실행 **NOT_QUERIED/NOT_RUN**. c4cc CI green을 e1d0로 전용하지 않는다. Windows 실제 실행, canonical npm runtime의 본인 재실행, 400 Python 전체 재실행, install/whole build/browser/Docker/image registry/prod/auth/Map/소비자 변경/CI-order 최적화 모두 NOT_RUN. 확인한 범위는 source+작은 구조/순수 parser/무해 shell mock이다. source/index/branch 수정0, repo 내부 출력0. 원문과 own evidence는 불변 고정하며 후속 새 입력에서만 OPEN 두 건을 재검토한다.
