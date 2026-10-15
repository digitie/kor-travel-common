# HTTP 생존 점검 post-fix manifest

- 제품 수정 commit: `001b03eb9a6b85bb7921d4d55a7f7fdf265c1160`.
- 이전 고정 후보: `c7b55aec8e2de6ac70b8f2ef21e2fc18df87c0ce`.
- [초기 manifest](2026-10-16-http-health-manifest.md)의 전체 문맥을 유지하며 아래5파일 delta와 이 manifest를 재검토한다.
- 두 독립 P2의 필수 SP 누락 반례를 len(status)==3 조건으로 거절한다. 이유 문구 자체는 빈 문자열을 허용한다.
- 정상 경계·총 예산·header cap·패키징·CLI·소비자 미채택 한계를 유지한다.
- reviewer A는 HTTP/시간/메모리, reviewer B는 패키징/소비자/CLI 관점으로 독립 재검토하며 peer raw를 읽지 않는다.

| 파일 | 수정 blob SHA256 |
|---|---|
| `docs/journal.md` | `e2878c0336132c190070c69ef97e2e511a07ffad98ee8194b663b2d9ba9d1fa3` |
| `docs/resume.md` | `9004a4c62555ff6820b54d7c76d8c6700555856b534db1f40ddf7447583c21bf` |
| `docs/runbooks/http-health-probe.md` | `e2abc4ca855aa0408a0b69f29dfe5fd71c83cb46c23fbb27bbc1a726313c14b4` |
| `packages/py/kor-travel-common/src/kortravelcommon/http_health.py` | `dafb57227662e1298675017be9de04ad602cbeb1a383dcb029e387792c9ec4f6` |
| `packages/py/kor-travel-common/tests/test_http_health.py` | `5daac6305a70918aa3a0716ddf94ed3b78b36f6d6c09031dd50395896479d55a` |

## 실제 작성자 재검증

- 해당 패키지에서 `uv run --no-sync ruff check .`·`uv run --no-sync pytest -q`: PASS,208건/102.11초(신규48포함). import가 현재 자기 WT임을 먼저 확인했다.
- 새 wheel SHA `b0efb0f0cbb3a0b772fb205af4ef1dc8a8d690d28ed0dfa1ee61a3edcf8f3096`: 빈 core-only venv에 offline 정상 설치/pipcheck/설치source 동일/실제CLI200·503·누락SP 종료0·1·1.
- 문서 링크695/2809targets·plan109오류0·diff check PASS. 초기 도구337실행/336PASS1SKIP는 이 코드 수정 전의 문서 도구 검증이며 별도 수치다.
- 초기204/44·첫 wheel/두 최초 원문은 보존한다. 운영/외부HTTP/SSH/PG/Docker 변경0이며 소비자 exact 통합pin/이미지/healthy·CPU/UI는 NOT_RUN이다.
