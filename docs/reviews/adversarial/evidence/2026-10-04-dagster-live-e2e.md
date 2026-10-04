# Dagster 공용 UI live e2e 및 최종 회귀

- 실행: Codex, 2026-10-04 09:57~10:26 KST, Windows Codex in-app browser.
- 코드: common `50d2db4` / weather `1218c8f`; 마지막 `ed47e9a` / `74882e1`은
  출처 주석·동일 Python 코드 SHA pin만 바뀌었다. UI artifact/source는 동일하다.
- 환경: WSL Ubuntu-26.04, Node 22, Next 15.5.24 production build/start,
  Python 3.13.14, Dagster 1.13.24, PostgreSQL 16.
- 격리: localhost UI14554/API14553/Dagster14552, 별도 `weather_e2e` DB,
  임시 SQLite Dagster metadata. 실제 weather Definitions를 로드했다.
  daemon은 시작하지 않았다. provider 수집·운영 데이터 변경은 하지 않았다.
- UI 자동화는 computer-use의 cua browser로 실행했다. HTTP/GraphQL mock을 사용하지 않았다.
  실패/진행 run 3개만 Dagster instance에 테스트 이벤트로 넣었다. 실제 worker crash를
  재현한 것으로 집계하지 않는다. ephemeral 로컬 인증은 production 인증 경로를 사용했다.

## 실제 관찰

| 흐름 | 관찰·판정 |
|---|---|
| 실패 로그인 | production UI에서 잘못된 비밀번호를 거절하고 한글 오류 표시, PASS |
| 정상 로그인 | 실제 API 세션 생성 후 운영 홈 표시, PASS |
| 로그아웃 | 로그인 화면으로 복귀, PASS |
| 공용 메뉴 | 홈→Dagster 이동 및 현재 메뉴 강조/aria-current, PASS |
| 실패 상세 | FAILURE run의 `E2E: worker 연결 실패 후 복구 검증` 표시, PASS |
| job별 정체 | 2시간 초과 KMA는 정체 의심, 16시간 상한 Open-Meteo는 1시간 경과에도 정상 진행, PASS |
| schedule 상세 | 초단기실황 expand에서 job/cron 및 해당 repository의 Dagster 링크, PASS |
| 화면 스타일 | 실패 text와 destructive 토큰 색상 일치, 오류 border 1px, 외곽 gutter 유지, PASS |
| 모바일 390×844 | body 수평 overflow 없음, gutter 12px, 표 scrollWidth 741/779가 자체 323px wrapper 내부에 제한, PASS |
| Dagster 연결 중단 | 테스트 webserver만 중단하고 새로고침 시 오류/다시 시도 표시, 이전 3개 run과 마지막 확인 시각 유지, PASS |
| 연결 복원 | 같은 metadata로 webserver 복원 후 다시 시도: 오류 사라짐, 10:22:35 KST로 확인 시각 갱신, 동일 run 유지, PASS |

[데스크톱 원본 base64](2026-10-04-dagster-ui-desktop.jpg.base64) ·
[모바일 원본 base64](2026-10-04-dagster-ui-mobile.jpg.base64).
저장 형식 note: common 정보 검사기는 모든 tracked 파일을 UTF-8로 읽으므로 JPEG 원본을
base64 텍스트로 인코딩했다. pixels/내용은 변경하지 않았다. 원래 JPEG를 관찰한 reviewer
보고서의 파일명은 역사로 유지한다. Python `base64.b64decode(Path(file).read_text())`로
원본 JPEG를 복원할 수 있다. 로컬 표시용 JPEG는 weather의 ignored `.codex_tmp`에 보존했다.
원본 SHA-256: desktop `f3c674363d4b29a2153355d823a219d30b37dcd8b2d082ca63fc430d7f831279`,
mobile `c73f06671a36fb0b39ab2a90c3855a4edf8e1a0dd8e0a1e195210b4bfbaf7642`.
브라우저 accessibility tree와 읽기 전용 DOM/computed-style로 확인했다.
실제 run 실행/취소 UI 권한은 Dagster 운영 링크가 소유하며 이번 테스트에서 실행하지 않았다.

## 최종 회귀와 설치

| 검증 | 결과 |
|---|---|
| weather 전체 `uv run pytest -q` 상당 locked venv pytest | 345 PASS, 31 deprecation warnings, 453.69초 |
| weather `ruff check .` | PASS |
| weather frontend ext4 clean npm ci → type-check / npm test / lint / production build | PASS / 64 PASS / PASS / PASS |
| common Python / UI | 21 PASS / 34 PASS |
| Python3.11 + Dagster1.9.0 floor | 21 PASS |
| common core-only wheel import | Dagster 없이 import PASS; Python CI도 동일 경계 확인 |
| common tarball clean 소비자 build / webpack | PASS / PASS |
| common tools unittest | 337 중 336 PASS·Windows 전용1skip(로컬); Linux CI 337 중334 PASS·3skip |
| 신규 DB migration | 별도 weather_e2e에서 head0018 PASS |
| 최종 metadata pin locked sync / common Python | PASS / 21 PASS |
| 공통 ruff / SPDX | PASS / 102파일 오류0 |

처음 실제 Dagster 조회에서 로그 limit2000이 서버 상한1000을 넘어 실패 상세가 사라졌다.
cursor pagination/timeout을 고쳤고 실제 UI 상세 표시 및 후속 page 회귀 시험을 통과했다.
처음 tarball integrity/Origin 형식 CI 실패도 수정했다. 실패를 최종 PASS로 덮어 기록하지 않는다.
evidence-only closure의 최초 secret-scan은 JPEG의 UTF-8 decode 오류로 실패했다.
위 원본 인코딩 후 secret/redaction 전체758파일·발견0을 직접 재확인했다.

## 메모리 측정과 범위

동일 합성 KMA fact 192,000개를 전체 staging과 5,000개 bounded staging으로 비교했다.
tracemalloc 피크는 446,740,271→12,766,381 bytes(약426→12MiB, 약97% 감소)였다.
이는 합성 Python 할당량이며 운영 RSS·실제 전국 raw payload 보증은 아니다.

NOT_RUN: 운영 배포, shared daemon 설정 적용, OS worker hard hang/crash/native retry 장애 주입,
운영 RSS 실측, transport/map/pinvi/geo의 실제 채택. 배포 전 migration/instance 설정과
launcher의 강제 process 종료·서비스 관리자 healthcheck는 적용 가이드의 선행이다.
마지막 CI와 merge 판정은 통합 review report에 별도로 연결한다.
