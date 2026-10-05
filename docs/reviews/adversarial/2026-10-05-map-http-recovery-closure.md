# Common HTTP 복구·메모리 reviewer A closure (2026-10-05)

이 문서는 reviewer A의 원문 보존과 finding 재검증 연결만 기록한다. 기준선은 `7dc1d6dda955b9b836cb3f24d6fd5bcd37fabe52`, 최종 제품은 `1f8e339c7c79f86f8952b0d4c326ab4dae56bee8`다. 최종 독립 FULL 판정은 **PASS**이며 신규 미해결 finding은 없다. 상대 reviewer 결과와 두 사람의 통합 판정은 이 문서 범위 밖이다.

[보존 metadata](evidence/2026-10-05-map-http-reviewer-a-archive.json)는 원문 UTF-8 해시 `original_sha256`, 공개 MD 실제 파일 해시 `md_file_sha256`, JSON wrapper 실제 파일 해시 `file_sha256`를 구분한다. 최초·post-fix·최종 원문은 소급 수정하지 않았다. JSON `raw`의 UTF-8 bytes와 MD 원문 bytes가 모두 원본과 일치하며 공개 MD whitespace 정리는 필요하지 않았다.

| 단계 | 기준 | 판정 | 원문 |
|---|---|---|---|
| 최초 dirty | base 7dc1d6d, 원문 내부 파일 SHA 기준 | BLOCK | [MD](evidence/2026-10-05-map-http-reviewer-a.md) · [JSON](evidence/2026-10-05-map-http-reviewer-a.json) |
| 전체 post-fix | 2f7a9277c7191bb87e91593a37d53ad6e3ed2065 | BLOCK | [MD](evidence/2026-10-05-map-http-reviewer-a-postfix.md) · [JSON](evidence/2026-10-05-map-http-reviewer-a-postfix.json) |
| 최종 전체 post-fix | 1f8e339c7c79f86f8952b0d4c326ab4dae56bee8 | PASS | [MD](evidence/2026-10-05-map-http-reviewer-a-final.md) · [JSON](evidence/2026-10-05-map-http-reviewer-a-final.json) |

## Disposition과 직접 재검증

| finding | 심각도 | 최종 disposition | 직접 증거 |
|---|---|---|---|
| H01 clean CI httpx 누락 | P2 | FIXED | dev 직접 의존·lock closure60에 httpx·wheel optional extra metadata |
| H02 DigestAuth 중간 401 cap 우회 | P2 | FIXED | default auth=None·response hook 거부, Mock 및 표준 AsyncHTTPTransport 요청1개·큰 body 차단 |
| H03 cleanup 전체 대기 연장 | P2 | FIXED | 읽기40ms+close50ms에서91.04ms, 협조적 취소와 지원 transport 한계 문서 |
| H04 ReadTimeout.request 누락 | P3 | FIXED | 실제 request URL 보존 |
| H05 cleanup 실패 뒤 200 반환 | P2 | FIXED | 같은 slow close/ReadError 재현이 BoundedResponseError로 변경; OSError/httpcore 오류×정상/timeout/cap/cancel8경우 |
| H06 raw stream strict union 타입 실패 | P2 | FIXED | AsyncByteStream narrowing, strict mypy 및 wheel py.typed |

고정 최종 후보에서 직접 Python95 PASS(HTTP26 포함), HTTP strict mypy·ruff PASS, manifest15 SHA PASS, wheel build·core-only import 경계 PASS였다. 표준 HTTP/1.1 localhost transport로 gzip·chunked cap·DigestAuth·redirect·401·trickle deadline·caller cancel을 재검증했다. 문서594/local target2693·task109 검사 오류0. 도구337 실행은336 PASS+1 SKIP이며 skip은 PASS로 합산하지 않는다. archive의 Node 의존 누락에 따른 초기 실패와 본인 /tmp npm ci 후 closure도 최종 원문에 기록했다.

NOT_RUN: Python3.11/HTTPX0.27 별도 matrix, TLS/HTTP2, network clean Python 설치, Map/PinVi 채택·N150·실제 PostgreSQL·provider·운영 kill/RSS/shared daemon. 부모/상대 실행을 본인 실행으로 합산하지 않는다.

이 보존 작업은 제품 변경이나 새로운 제품 리뷰가 아니다. 코드·규범·기존 manifest와 상대 원문을 수정하지 않고 reviewer A의 closure artifact만 추가한다. archive index와 통합 문서는 소유권 범위 밖이므로 merge 담당이 연결한다.
