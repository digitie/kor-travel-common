# CONTRIBUTING

이 문서는 kor-travel-common에 기여할 때의 권리·헤더·커밋·리뷰 규칙 요약이다(브리프 D-04·D-17·D-32, ADR-004). 고지·검사 구현 task는 T-003이다. 절차의 정본은 [agent workflow](docs/runbooks/agent-workflow.md), 라이선스 규범의 정본은 [licensing](docs/standards/licensing.md)이며 이 문서는 요약과 링크만 둔다. 마지막 갱신 2026-09-07.

## 1. 라이선스와 권리

- 이 저장소 자체 작성 부분의 라이선스는 `GPL-3.0-or-later`다. 기존 원천의 별도 조건은 NOTICE와 파일별 고지에 보존한다([LICENSE](LICENSE), [NOTICE](NOTICE)). 기여물은 같은 라이선스로 배포되는 데 동의한 것으로 본다. GPLv3 7조의 추가 허가는 두지 않는다(O-2 기각).
- **AI 보조 생성물**: 에이전트·코딩 도구(Claude, Codex 등)의 도움으로 만든 코드·문서와 봇 계정 이름으로 커밋된 변경은, 그 생성을 지시하고 검토·수용한 저작권자(Youn-sok Choi, digitie)가 자신의 저작물로서 GPL-3.0-or-later로 배포한다. 도구 계정은 권리자가 아니며, 도구 약관·관할법상 권리 귀속이 불명확한 부분의 책임도 지시자가 진다(`docs/survey/cross/licensing.md` §2.6·§4 B8).
- 제3자 코드·문서·에셋을 반입할 때는 반드시 먼저 [PROVENANCE](PROVENANCE.md)에 행을 추가하고 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)를 갱신한다. 금지 원천(pinvi L6 전, 벤더 tgz·`maplibre-vworld-*`, Hallmark 스킬 본문, `python-*-api` 코드)은 PROVENANCE §규칙 4를 따른다.
- 외부 원문(Tailwind·shadcn·Next·FastAPI 문서 등)을 인용할 때는 공식 URL과 version/commit/revision을 함께 적는다.

## 2. SPDX 헤더

모든 소스 파일(`*.ts`, `*.tsx`, `*.css`, `*.py`, `*.mjs`, 워크플로 `*.yml`)의 첫 비어 있지 않은 줄부터 다음 헤더를 둔다. Markdown·JSON·lock 파일은 예외다.

```ts
// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
// Origin: kor-travel-map@c494e227 packages/kor-travel-map-admin/frontend/src/components/ui/button.tsx (GPL-3.0-or-later)
// Derived-From: shadcn/ui (MIT) — see THIRD_PARTY_NOTICES.md
// Modified: 2026-09-06 — loading 계약을 aria-disabled + aria-busy로 통일
```

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Youn-sok Choi (digitie)
# Origin: kor-travel-map@c494e227 src/kortravelmap/... (GPL-3.0-or-later)
```

- `SPDX-License-Identifier`·`SPDX-FileCopyrightText`는 필수, `Origin:`은 다른 저장소에서 옮긴 파일에 필수, `Derived-From:`은 서드파티 파생에 필수, `Modified:`는 원천을 바꿨을 때 필수다. geo 유래 파일은 `Origin:` 괄호에 `GPL-3.0-only`를 병기한다(O-20).
- CSS는 `/* … */`로 같은 행을 쓴다. Hallmark 스탬프는 common 파일에 두지 않는다(SPDX만, D-13·D-17).
- [check_spdx.py](tools/check_spdx.py)가 로컬에서 헤더·출처 누락을 exit 1로 판정한다. 전체 검사 범위·예외는 [licensing §5.2](docs/standards/licensing.md#52-검사-범위와-출처-대조), CI 필수 연결은 T-009를 따른다.
- 생성물(`tokens.json`·`tokens.ts`·`tailwind-preset.cjs`)은 생성기가 헤더를 넣는다. 손으로 고치지 않는다.

## 3. 커밋 규칙

- 제목은 Conventional Commits 영어 type(`feat`·`fix`·`docs`·`chore`·`refactor`·`test`·`ci`·`build`) + 한국어 문장이다(D-32). 예: `docs: consumer adoption runbook과 릴리스 절차 추가`. 패키지 범위는 scope로 적는다(`feat(tokens): …`).
- 본문에는 근거 문서 절·task ID·실행한 검증을 적고, 실행하지 않은 검증은 `NOT_RUN(사유)`로 쓴다. 명령을 적은 것은 실행 증거가 아니다(D-25).
- 파일을 경로별로 stage한다. `git add -A`·`git add .`는 금지다. push 전 `git diff --staged`를 직접 읽고 비밀·운영 호스트·`*.local.md`·`.env`가 없는지 grep한다(정본 [agent workflow §7](docs/runbooks/agent-workflow.md#7-stage-보안-감사와-pr)).
- 텍스트 파일은 LF다(`.gitattributes` `* text=auto eol=lf`, `.editorconfig`). Windows에서 작업했으면 첫 add 후 `git ls-files --eol <path>`로 `i/lf`를 확인한다.
- 한 PR = 한 산출물. 무관한 포맷 변경·의존성 상향을 섞지 않는다(D-24).
- 언어: Markdown 본문·코드 주석·docstring·사용자 문자열은 한국어, 식별자·SPDX 키·CHANGELOG 절 제목·공식 필드명·명령·URL·패키지명·벤더링 원문은 영어(D-32).

## 4. 브랜치·PR·리뷰 gate

- 브랜치는 `agent/<agent>-<task>`를 `origin/main`에서 분기하고 `main`에 직접 push하지 않는다. Draft PR로 시작한다.
- PR 본문은 [PR 템플릿](.github/pull_request_template.md)의 6항목(task·목적 / gate·명령 / 리뷰어 2인 영역·report·disposition / 실패·미실행·위험 / evidence·digest / rollback)을 모두 채운다.
- 리뷰 gate 요약(D-04): 비단순 변경은 전문 영역이 다른 리뷰어 2인의 독립 적대적 리뷰(같은 manifest·immutable 기준선·상대 결과 비공개)를 거친다. 비면제 목록은 `docs/standards/*`, `versions.json`, `packages/*` 공개 API·CSS, `.github/workflows/*`, `AGENTS.md`·`SKILL.md`·`docs/README.md`·ADR·runbook·task/review 규칙이다. 면제는 오탈자·동의 링크 수정뿐이며 작성자가 아닌 merge 담당이 승인한다. 심각도 `P0`~`P3`, disposition `OPEN/FIXED/REJECTED_WITH_EVIDENCE/DEFERRED`(`DEFERRED`는 P2/P3만), verdict `BLOCK/CONDITIONAL/PASS`. 정본은 [agent workflow §5](docs/runbooks/agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰)와 [review archive](docs/reviews/README.md)다.
- CI(`docs`·`tools`·`packages`·`python-package`·`secret-scan`·`check-versions`)와 리뷰 gate, 미해결 `P0`/`P1` 확인이 끝나기 전 merge하지 않는다.
- 단독 유지자 전제(D-33): 공통 API·릴리스 담당과 소비자 통합 담당을 겸임하더라도 작성자와 리뷰 판정자 역할은 분리한다(리뷰어는 서브에이전트, 판정은 merge 담당).

## 5. 문서 규칙 요약

- 링크는 저장소 상대 경로만 쓴다(절대 경로는 `tools/validate_document_links.py` 오류). 같은 규범을 두 문서에 복제하지 않고 상위 문서는 한두 문장 요약 + 정본 링크만 둔다.
- 사실/후보/추정/열림을 구분한다. 열린 결정은 "열림(사용자 확인 필요)" + 기본값을 적는다.
- 완료 전 `python3 -B -X utf8 tools/validate_document_links.py`, `python3 -B -X utf8 tools/validate_plan.py`, `python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py"`, `git diff --check`를 통과시킨다(Git Bash에서 동일; Windows 표기는 [개발 환경](docs/dev-environment.md) §5).
- 문서 종류별 책임·갱신 조건·이동 절차는 [documentation maintenance](docs/runbooks/documentation-maintenance.md), task 문법은 [tasks-rule](docs/tasks-rule.md), ADR 규칙은 [ADR 색인](docs/adr/README.md)이 정본이다.

## 6. 개발 환경

정본은 Linux/WSL bash + CI `ubuntu-24.04`, Windows는 Tier 2(`tools/*.py`만 보증)다(D-03). 명령 표기와 프로필은 [개발 환경](docs/dev-environment.md)을 본다. 임시 worktree는 병렬·격리·독립 리뷰 때만 만들고 종료 후 제거한다([agent workflow §2](docs/runbooks/agent-workflow.md#2-branch와-임시-worktree)).
