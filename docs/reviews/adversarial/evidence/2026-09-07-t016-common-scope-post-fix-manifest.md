# T-016 공용 범위 재점검 post-fix 리뷰 manifest

- Review ID: `T016-SCOPE-POST-FIX-20260907`
- Candidate/post-fix: `a9fc2f5187bcf2517cb1da54ece9b12ab04b82ff`
- Base: `c8f81be7e70abbce892417eb0247a5d2337f31`
- 직전 post-fix: `7504d0d47f0c4da31ed2683b79332ef63bcca5de`
- Candidate tree: `4b9acba43d126f1adf31b680ed64389a4e74b440`
- PR: [#9](https://github.com/digitie/kor-travel-common/pull/9)

## 동일 입력

두 reviewer에게 위 candidate의 detached clean worktree와 같은 base, 아래 범위·수용 기준·검증 목록을 전달했다. reviewer는 candidate 파일을 수정하거나 상대 결과를 읽지 않는다.

- 대상 delta: ADR-001·010·011·014·015, architecture/standards/runbook, AGENTS, 범위 재점검·통합 계획·design brief, T-011·T-016·T-210·T-211·T-213·T-213a·T-214·T-312·T-403, resume/tasks/journal, PR #9 문서.
- 핵심 계약: common은 독립 운영 시스템이 아니라 위젯·디자인 토큰·공용 코어·로그인 UI/주입형 인증 프리미티브를 제공하고 서버·DB·비밀·IdP·앱 정책은 소비자 소유다. npm/PyPI 게시와 소비자 저장소 수정은 제외한다.
- 핵심 전이: T-213a는 외부 소비자와 무관한 UI 0.2 common 후보 보존, T-214는 T-210·T-213a 뒤의 로그인 위젯, T-213은 T-212 외부 evidence와 T-213a 후보 뒤의 rc/정식 릴리스다.
- T-011 계약: manifest 앱 경로와 소비자 저장소 root를 함께 전달하고 root-relative lock/workflow 경계를 검증한다. 초안은 10개 앱 표면이다.

## 실행 가능한 검증

```text
python -B -X utf8 tools/validate_plan.py
python -B -X utf8 tools/validate_document_links.py
python -B -X utf8 tools/check_prod_redaction.py
python -B -X utf8 -m unittest discover -s tests -v
git diff --check c8f81be7e70abbce892417eb0247a5d2337f31 a9fc2f5187bcf2517cb1da54ece9b12ab04b82ff
gh run view 34107732188 --json headSha,conclusion,jobs,url
```

CI 필수 job은 docs, tools(ubuntu-24.04/windows-2025), check-versions, secret-scan 5개다. 패키지 실물·소비자 실행·후보 tag/Release·npm/PyPI 게시 검증은 이 리뷰 범위 밖이며 `NOT_RUN`으로 기록한다.
