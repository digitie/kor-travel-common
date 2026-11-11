# 원 reviewer A(Mill) — A-P2-10 gzip 수정 재확인

- Run ID: Mill-A-gzip-postfix5-f8643d5-docs-d1fe0a3.
- 시작 UTC: 2026-11-11T17:25:13.633563+00:00. 종료 UTC: 2026-11-11T17:29:49.675615+00:00.
- 같은 원 reviewer A. 구현하지 않았고 상대 raw/verdict를 열람하지 않았다. 자동 전체 scan은 경로·규칙만 출력했으며 상대 원문 내용은 열지 않았다.
- **Scanner delta verdict: PASS. A-P2-10 FIXED(원 reviewer 직접 red/green). 신규 P0/P1/P2/P3 모두0.**
- **출판·전체 CI gate는 미완:** 지정 d1fe 문서의 prod scan1건과 push 후 exact 새 CI 확인이 별도다. source4 CONDITIONAL 원문을 덮어쓰지 않는다.

## 입력과 불변 경계

root=/home/digitie/dev/common-unification-20261111.
입력은 validation/common-gzip-member/HANDOFF.md 및 review-input.json이다.
review-input SHA256=6ff2bc6ae754990afd0b612067e14d06ff5fa576f41c44c5b0df005e4e7e46fa.

base2ec519255ec1af9fca18856d980e968ee15b80a8 → scanner source f8643d56bd8ce4cc7ff3d730b31173a8583593a4.
변경은 tools/_scan.py, tests/test_scan_gzip_members.py 두 파일뿐이다.

격리 worktree는 d1fe0a34ed720e4511a0612265e949632623a8dd의 문서 snapshot을 포함한다. 위 두 scanner/test 파일은 f864 Git object와 실제 bytes를 대조하여 완전 동일했다. f864→d1fe는 review archive8파일뿐이며 그 내용은 검토하지 않았다. 시험 전후 HEAD=d1fe/clean이다.

common-artifacts.json SHA256=7d76d61565c8076934640538e783624719351edc06fad9bf99ebe4ff943e276e를 입력값과 대조했고 canonical6 tgz 전체 SRI도 모두 MATCH했다. UI/CSS/runtime 재pack은 없다.

## 원 finding closure와 구현 확인

**A-P2-10 FIXED.** tools/_scan.py:247 부근의 single-member zlib decoder가 원인 경로를 교체한다.

gzip.GzipFile의 자동 연결 해제를 제거했다. zlib.decompressobj(16+MAX_WBITS)에 최대 허용 확장량+1만 요청한다. 초과, eof 미도달, unused_data 또는 unconsumed_tail이 있으면 값 비공개 exit2로 거부한다. 뒤 gzip member·외부 zero padding·다른 trailing bytes가 성공하지 않는다. 정상 tar 내부 padding은 유지한다.

첫 FNAME/FCOMMENT/FEXTRA 검사는 그대로이며 zlib가 단일 stream의 CRC/ISIZE/FHCRC와 trailer를 검증한다. 기존 archive 깊이·input/확장량/member 제한, 비추출 순회와 exact member/rule/raw SHA256 예외 경로를 유지했다.

본인의 source4 원 공격 script는 수정하지 않았다. after 복사본에서 SOURCE와 임시 fixture 부모 경로만 바꿨다.

| 원 공격 | 기존2ec 두 CLI | 새f864 두 CLI |
|---|---|---|
| 첫 header의 동일 canary | 각각 exit1 | 각각 exit1 |
| 둘째 빈 member header canary | 각각 exit0 | 각각 exit2 |
| 안전한 두 gzip member 대조군 | 각각 exit0 | 각각 exit2 |

숫자는 CLI exit code다. 후속 header를 전부 지원한다고 판정한 것이 아니라, 지원 범위를 단일 완결 stream으로 한정하여 우회를 명시적으로 거부함을 확인했다.

## 직접 검증과 raw evidence

evidence=root/review-A-common-evidence-gzip-postfix-5/.

| 직접 실행 | 실제 결과 | evidence |
|---|---|---|
| 본인 원 공격 before/after | 위 red/green 일치 | original-attack-before/after.log, gzip-member-attack-after.py |
| 같은 focused9를 기존 scanner에 실행 | 9실행,16실패 subcase | focused-before.log |
| 새 focused9 | 전부 PASS | focused-after.log |
| 최종 전체 tools suite | 391실행=390 PASS/1 SKIP/실패0,71.907초 | full-tools.log |
| 실제 d1fe 전체 secret scan | 1361파일,발견0,정확 예외32,exit0 | secrets-all.log |
| 실제 d1fe 전체 prod scan | 1361파일,발견1,정확 예외4,exit1 | prod-all.log |
| canonical6 SRI/원장 | 모두 MATCH | artifacts-unchanged.json |
| diff --check | PASS | diff-check.log |

focused9는 첫/둘째 FNAME·FCOMMENT·FEXTRA, 빈/비어 있지 않은 후속 stream, 중첩 source, 외부 padding/trailing bytes, metadata 안의 gzip magic, 유효/손상 FHCRC·CRC·ISIZE·잘린 trailer, exact 확장량 경계 및 digest 예외가 후속 header를 면제하지 못함을 포함한다. 값·Traceback 비공개 assertion도 유지된다.

초기 전체 driver에는 node_modules 참조가 없어 MDX 파서 관련38FAIL/3ERROR가 있었다(full-tools-first-no-modules.log). 기존 모듈을 readonly symlink로 연결하고 동일391개를 재실행하여 위390PASS/1SKIP을 확인했다. fresh install이나 assertion 변경은 하지 않았다.

## 별도 gate·한계

d1fe의 prod1건은 부모가 먼저 공개한 archive 문서의 INTERNAL-HOST literal이며 scan 출력은 해당 경로/34행/규칙만 보인다. 이것을 scanner 회귀나 새로운 자신의 finding으로 중복 채번하지 않는다. 부모의 publication 수정 뒤 전체 scan 재확인과 exact 후속 commit CI가 필요하다. 본 고정 snapshot의 exit1을 PASS로 바꾸지 않는다.

지정 f864/d1fe의 원격 CI는 본 실행에서 수용하지 않았다(NOT_RUN/아직 push·출판 정리 대기라는 부모 전달). 이전2ec CI 성공을 새 source CI로 대체하지 않는다. 소비 앱 리뷰·배포 및 NativeCSS 재검토는 이 closure 범위 밖이다.

source4 원문 SHA256은 25df57642d2a8d8cd29d62e8e5aa7707599525a884e629af9d66ad7c6a0396ba로 전후 불변이다. 소스·allowlist·pack·상대 원문을 수정하지 않았고 출력은 본인 tmp/evidence에만 만들었다.

**A-P2-10 FIXED / scanner delta PASS / 출판·새 exact CI 별도 미완.**
