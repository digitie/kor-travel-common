# 독립 적대리뷰 A(Mill) — COMMON source4 / integration9

- Run ID: Mill-A-common-final4.
- 시작 UTC: 2026-11-11T17:02:46.247958+00:00.
- 검증 종료 UTC: 2026-11-11T17:10:13.033051+00:00. 원문 작성 UTC: 2026-11-11T17:12:50.847491+00:00.
- 원 reviewer A, frontend/accessibility. 구현에 참여하지 않았으며 상대 reviewer의 raw report·verdict를 검토하지 않았다. diff 내용에서 docs/reviews 전체를 제외했다.
- **Verdict: CONDITIONAL. 원 A-P2-09 FIXED / 신규 A-P2-10 OPEN(P2).**
- **신규 P0 0 / P1 0 / P2 1 / P3 0.** 새 finding의 수정 또는 정식 disposition이 필요하다. 본 원문은 연기 승인이 아니다.
- exact2ec 원격 CI는 직접 조회상 모두 SUCCESS다. CI 성공과 새 적대적 반례를 구분한다.
- source3의 BLOCK 원문 및00ddd65 보충 기록은 수정하지 않았다.

## 1. 불변 입력·격리·관찰 SHA

root는 /home/digitie/dev/common-unification-20261111 이다.

manifest: root/review-manifest-common-4.json.
실측 SHA256: e5c7101e4130b4bf66c90a8ef2e54f3c672c5a79f0eeb8216bfc9ebcaa85c951, 전달값과 일치.

| 대상 | 고정 기준 |
|---|---|
| common base | c289b4624c8640eb918cc915803e72ae754e58fb |
| 이전 → 이번 head | 7e3f33e0391990b9312fee513de581e28035aa8b → 2ec519255ec1af9fca18856d980e968ee15b80a8 |
| c9 producer | 2c1182e765bb2bc53e01e0962cf2a73683891e1d |
| VWorld | 9a7a348b02d61969b394c681b024d5851eef836b, 이전 검토와 동일 |
| artifacts | root/artifacts/integration-9-review |

/tmp/review-A-final4/common detached worktree에서 immutable source를 검토했다. 시작·종료 모두 지정 HEAD/clean이며 공유 checkout을 수정하지 않았다. source3 원문 SHA256 ab02db083de78deb7b514067071d01c715658dd63c988410d6b880e0d67c0037,00ddd 보충 원문66e9ea4fd2937d2dfd408d25d83f7d589c758bb95f4ff37dfdec4748c33350e0을 전후 일치로 확인했다.

source3→4의 정책 AST·linked workspace 개발 그래프, archive scanner·정확 member 예외, 문서 생성/정본 범위, workflow 변경을 확인했다. c9 producer 이후에는 scanner·문서·검증 도구 변경도 있으므로 단순히 모든 source delta를 원장 변경뿐이라고 하지 않는다. UI/token runtime에는 변경이 없다.

## 2. 실제 c9 bytes와 이전 브라우저 증거의 적용 범위

6 tgz SHA512를 manifest와 독립 계산·대조하여 모두 MATCH했다(artifact-check.json).

c8/c9 archive의 모든 일반 파일을 직접 byte 비교했다:

| package | 파일 수 | 바뀐 파일 | 동일 파일 |
|---|---:|---|---:|
| @kor-travel/ui | 94 | package/check-dependencies.mjs | 93 |
| @kor-travel/tokens | 25 | package/check-dependencies.mjs | 24 |

따라서 runtime/CSS/metadata117파일은 동일하고 checker2파일만 다르다. 두 shipped checker의 bytes도 source4 tools/check_frontend_dependencies.mjs와 각각 일치했다. 증거: c8-c9-equivalence.json.

본인의 source3 c8 webpack65·Turbopack 추가10 browser 결과는 그대로 보존하며, c9 로컬 브라우저를 다시 실행했다고 하지 않는다. 한편 이번 exact2ec 원격 packages에서는 실제 c9 UI/tokens 전체 SRI 일치와 packed browser65 PASS를 별도로 직접 확인했다(§6). VWorld3 pack과 fix4 bytes는 전과 같으며 이번에 새 지도 WebGL·native CSS production rebuild를 했다고 주장하지 않는다.

## 3. A-P2-09 원 reviewer closure

**A-P2-09: FIXED.**

수정 위치: tools/check_frontend_dependencies.mjs:134(importedModule), :150(확장자), :157(공통 판정), 같은 배포 복제2파일.

source3에서 사용한 본인 공격 fixture를 재실행했다. 정상 canonical/artifact 조건과 transitive 구 private root 조건을 유지했다. source3/source4/실제 c9 UI checker/실제 c9 tokens checker를 각각 지정하여 실행했다.

| 입력 형태 | source3 | source4 | c9 UI | c9 tokens |
|---|---:|---:|---:|---:|
| static import | 1 | 1 | 1 | 1 |
| static re-export | 0 | 1 | 1 | 1 |
| literal dynamic import | 0 | 1 | 1 | 1 |
| literal require | 0 | 1 | 1 | 1 |

숫자는 CLI exit code다. 이전의 실재 우회3종이 새 source와 실제 배포 checker 양쪽에서 거부된다. policy-own-attack-source3/source4/c9-ui/c9-tokens.mjs와 각 log에 원 입력·stdout/stderr를 보존했다.

policy68 전체도 직접 PASS했다. 여기에는 export-star, no-substitution template import/require, 외부 TS import, type import, MJS/CJS/MTS/CTS, 인접 다른 package 허용, 설명 문자열·주석 비오인 및 linked workspace dev CSS 불일치 거부가 포함된다. 정확 root 또는 root+"/" 경계는 유지된다. 비literal 동적 module resolver 전체 해석을 새 지원으로 주장하지 않는다.

A-P2-08과 최초10건의 이전 FIXED disposition은 유지한다. runtime117파일이 동일하며 이번 delta에서 재OPEN할 근거를 찾지 못했다. 이전 모든 UI·map 공격을 재실행한 것은 아니다.

## 4. 직접 실행한 검증

영구 evidence: root/review-A-common-evidence-postfix-4/.

| 검증 | 결과 | raw evidence |
|---|---|---|
| dependency/nativeCSS policy | 68 PASS / skip0 | policy.log |
| 원 A-P2-09 red/green 및 실제 c9 두 checker | 위 표와 동일 | policy-own-attack-*.log |
| Python tools unittest 전체 | 382실행 = 381 PASS / 1 SKIP / 실패0 | python-all.log |
| 새 frontend 문서 계약 집중 시험 | 3 PASS | docs-tests.log |
| policy JSON·문서 생성물 --check | PASS | policy-sync.log |
| 실제 source 전체 secret scan | 1352파일 / 발견0 / 정확 예외32 | secrets-all.log |
| 실제 source 전체 prod scan | 1352파일 / 발견0 / 정확 예외4 | prod-all.log |
| 아래 새 gzip member 공격 | 두 CLI 모두 false negative 재현 | gzip-member-attack.py / .log |
| source3→4 diff --check | PASS | diff-check.log |
| c8/c9 bytes·source/checker·실제 CI SRI | MATCH | artifact-check.json / c8-c9-equivalence.json / remote-pack-sri-match.json |

manifest validation의 scanner379는 이전 scanner 소스에서의 기록이다. 본인이 실행한 최종2ec에는 문서 계약3개가 더 있어 실제382실행이며 skip1을 PASS에 더하지 않았다. 전체 scan의 실제 tracked file 수 역시1352로 기록했다.

새 문서 생성기는 단일 marker 두 개를 검증하고 versions.json에서 JSON·문서 표를 함께 계산한다. 문서 단독 drift·registry 변경·marker 유실3시험과 --check를 직접 확인했다. AGENTS/consumers의 현재7개 저장소·9표면 승인 범위는 과거 조사/채택·배포 완료 상태와 구분되어 있다. 이것을 앱별 수용 완료로 해석하지 않는다.

archive scanner는 임의 tgz skip이 아니다. 64MiB input/archive,32MiB member,256MiB 총 확장량,4096 tar member,깊이4의 상한과 비추출 순회, 링크·sparse·중복·traversal·잘린 입력 거부, 알려진 native/WASM/image/V8의 ASCII 검사 경로를 확인했다. 예외는 exact member/rule/raw SHA256 단위이고 header·다른 rule은 계속 검사한다. 실제 예외32/4가 성공했더라도 아래 독립 반례는 별개다.

## 5. 신규 A-P2-10 — 연결된 두 번째 gzip member의 header가 검사되지 않음

- **P2 / OPEN.** 이 scanner delta에서 독립 재현한 새 finding이다.
- 위치: tools/_scan.py:247〜250. gzip_header_parts 호출은 바이트 시작의 header 한 번뿐이지만 gzip.GzipFile.read는 이어진 gzip member도 자동 해제한다.
- 기대: 첫 header와 후속 header에 같은 정책 일치 문자열이 있을 때 모두 finding(exit1) 또는 지원하지 않는 입력으로 거부(exit2)해야 한다.
- 최소 재현은 보존된 gzip-member-attack.py 실행이다. 작은 안전한 tar를 gzip으로 압축하고, 같은 파일명 metadata를 갖는 빈 두 번째 gzip member를 이어 붙인다. private fixture repo와 각 CLI의 실제 기본 pattern을 사용하며 allowlist는 없다. 문자열은 공개 합성 canary이며 실제 비밀·운영 주소가 아니다.

~~~python
data = gzip_of(safe_tar) + gzip_of(b"", filename=synthetic_canary)
~~~

실측:

| 사례 | secret CLI | prod CLI |
|---|---|---|
| 같은 canary가 첫 gzip header에 있음 | exit1, SECRET-ASSIGNMENT | exit1, INTERNAL-HOST |
| 같은 canary가 두 번째 빈 gzip member header에 있음 | exit0, 발견0 | exit0, 발견0 |
| canary 없는 두 member 대조군 | exit0 | exit0 |

공격 입력은174bytes다. 두 번째 member는 압축 해제 결과가 비어 있어 tar의 trailing-payload 검사에도 걸리지 않는다. GzipFile은 두 stream을 정상 수용하지만 후속 FNAME metadata는 scan_parts에 전달되지 않는다. 예외 정책이나 hash 변경 없이 재현된다.

영향: 검사 대상 archive bytes에 정책상 금지된 metadata가 있어도 두 전체-tree gate가 성공할 수 있다. 현재 고정 vendor pack에 실제 비밀이 있다는 주장이나 runtime/CSS 결함 주장이 아니다. 첫 header 검사와 종료 뒤 payload 거부라는 새 계약이 concatenated gzip에는 완전하지 않다.

수정 권고: gzip member 경계를 명시적으로 순회하여 각 header(FNAME/FCOMMENT/FEXTRA)와 CRC/길이를 검사하고 총 압축·해제량 및 gzip member 수를 제한한다. 또는 지원 범위를 단일 gzip member로 한정하고 후속 stream을 명시적으로 거부한다. 첫/후속 metadata, 빈 후속 member, 안전한 연결 대조군과 기존 압축 폭탄 상한 시험을 함께 유지한다. 값 비공개 출력도 유지해야 한다.

Disposition: 수정 후 원 reviewer 재확인. 정식 P2 연기를 택하면 owner/task/gate/기한을 기록해야 하며 현재는 OPEN이다.

## 6. exact source4 CI 직접 관찰

GitHub connector로 exact2ec의 workflow runs, docs run jobs 및 packages 전체 로그를 직접 조회했다. 첫 조회의 docs in_progress와 최종 completed SUCCESS를 모두 보존했다(ci-direct-observation.json).

- common frontend run43063413154: SUCCESS.
- python-package run43063413008: SUCCESS.
- workflows selftest run43063413011: SUCCESS.
- docs run43063412925: SUCCESS. docs130672022639, check-versions130672022818, secret-scan130672022896, tools Windows130672022977, Ubuntu130672023089, packages130672023061 모두 SUCCESS.

[packages 실제 로그](https://github.com/digitie/kor-travel-common/actions/runs/43063412925/job/130672023061)에서 checkout/SOURCE_SHA=2ec, 공식 MCR Playwright1.65.0 및 Chromium158.0.8127.18 기동, UI101/policy68/tokens9, webpack·Turbopack, packed browser65 PASS(40.7초)를 확인했다.

동일 로그의 UI/tokens 전체 SRI가 manifest c9와 정확히 일치했다. 축약 npm notice나 source 추정만 사용하지 않았다. 원문은 remote-pack-sri-match.json에 보존했다.

원 source3에서 알려진 UTF8 입력 오류와 MCR ownership 실패는 이번 source의 기본 gate에서 해소된 증거가 있다. 이전7e 원문을 성공으로 소급 수정하지 않는다. 모든 CI 성공은 새 반례를 자동으로 해결하지 않으므로 이번 담당 verdict는 CONDITIONAL이다.

## 7. 한계·보존·최종 판정

C9 로컬 browser/build 전체 재실행은 NOT_RUN(117 동일 bytes+이전 본인 실제 검증, 새 exact 원격 c9 성공으로 구분). VWorld merge commit ae1의 tree 동일성, serde merge21d의 tree 동일성은 manifest 전달값이며 이번에 해당 merge tree를 새로 재감사했다고 주장하지 않는다. 지도 원9a와 pack hash는 불변이다.

NativeCSS3는 별도 원문이며 앱 consumer·CSS fork·앱 export·새 이미지/배포·실제 스크린리더 수용은 본 범위 밖이다. UI 코드·생성물을 수정하지 않았고 fresh install, image pull, 타인 cache 삭제도 하지 않았다. 기존 모듈은 읽기 참조했고 출력을 자기 tmp/evidence에 격리했다.

**A-P2-09 FIXED / 신규 A-P2-10 OPEN / source4 CONDITIONAL.**
이번 exact CI는 성공했지만 새 scanner P2의 수정 재확인 또는 정식 disposition 전에는 무조건 PASS로 요약하지 않는다.
