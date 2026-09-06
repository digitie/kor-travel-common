<!--
정본: docs/runbooks/agent-workflow.md §7 (PR 본문 6항목). 6절을 모두 채운다.
실행하지 않은 검증은 NOT_RUN(사유)로 적는다. 명령을 적은 것은 실행 증거가 아니다.
소비 저장소 PR은 templates/consumer-pr.md를 쓴다.
-->

## 1. Task와 변경 목적

- Task: `T-NNN`(`docs/tasks/T-NNN-*.md`) / 사용자 요청:
- 목적(한 줄):
- 산출물(한 PR = 한 산출물):
- 범위 밖:

## 2. 통과한 gate와 정확한 실행 명령

| 계층 | 명령(실행한 그대로) | 결과(수치·exit code) |
|---|---|---|
| 문서 검증 | `python3 -B -X utf8 tools/validate_document_links.py` | |
| 문서 검증 | `python3 -B -X utf8 tools/validate_plan.py` | |
| 도구 테스트 | `python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py"` | |
| 공백 | `git diff --check` | |
| 패키지 빌드·타입 | | |
| 단위 | | |
| tarball / wheel 설치 | | |
| 소비자 빌드·e2e | | |

## 3. 전문 리뷰어 2인

- 판정(light / full)과 판정자(작성자 ≠ 판정자), light면 면제 근거:
- Reviewer A 영역 / 실행 ID:
- Reviewer B 영역 / 실행 ID:
- 기준선 commit / 격리 방식(object-only / detached):
- report: `docs/reviews/adversarial/YYYY-MM-DD-<scope>.md` / evidence: `evidence/YYYY-MM-DD-<scope>-{manifest,reviewer-a,reviewer-b}.md`
- 최종 disposition: `P0`/`P1` 0 여부, `DEFERRED` 목록(owner·task·gate·기한), post-fix verdict A/B

## 4. 실패·미실행 검증과 남은 위험

- 실패한 검증과 처리:
- `NOT_RUN(사유)` 목록과 승격한 `외부 선행`:
- 남은 위험·열린 결정(O-xx):

## 5. Evidence 위치와 digest

- 파일·스크린샷·로그 위치:
- tarball / wheel / `SHA256SUMS` digest:
- CI run URL:

## 6. Rollback

- 되돌리기 명령(1회 revert로 원복되는지):
- 영향 소비자·매니페스트·`consumers.pins.json`:
- 릴리스 태그가 있으면 fix-forward 계획:

<!--
push 전 확인: git add -A/. 미사용 / git diff --staged 직접 읽음 / 비밀·운영 호스트·*.local.md 없음 /
validator 3종 + git diff --check 통과 / 새 소스 파일 SPDX 헤더·Origin 행 / 기록 갱신(resume·tasks·ADR·journal·CHANGELOG·review index)
-->
