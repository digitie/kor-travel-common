# T-501 릴리스 runbook 1회 완주 검증(rc→소비자 PR→정식→되돌리기 리허설)

- 상태: BLOCKED
- 우선순위: P1
- Gate: consumer-smoke
- 선행: T-109, T-212

## 목표

[release runbook](../runbooks/release.md)에 적힌 절차를 실제 패키지 릴리스 1회로 완주해 "문장이 실행 가능한가"를 evidence로 남긴다. 대상은 `tokens`와 `ui` 각 1회의 patch 수준 릴리스(`-rc.N` → 소비자 PR 검증 → 정식 태그)이며, 정식 태그 뒤 소비자 쪽에서 직전 버전으로 되돌리는 리허설까지 포함한다. T-109·T-212가 첫 정식 버전(`tokens-v0.1.0`, `ui-v0.1.0`)을 만드는 task라면, 이 task는 그 뒤 두 번째 릴리스에서 runbook의 재현성을 검증하는 task다. 이 task를 완료해도 py 패키지 릴리스(T-310)나 공개 npm/PyPI 게시(T-507)가 검증된 것은 아니다.

## 고정 결정

- 배포 채널·태그 불변·같은 버전 재발행 금지·`@main` 참조 금지: 브리프 D-11, ADR-005([ADR 색인](../adr/README.md)).
- 릴리스 흐름 `-rc.N` → 소비자 PR 검증 → 정식, CHANGELOG 단일 파일 + 패키지별 H3: 브리프 D-18; 기록 형식은 [CHANGELOG](../../CHANGELOG.md).
- SemVer 0.x(patch = additive만, minor 파괴 시 이관 절 필수): 브리프 D-31.
- 소비자 PR 규격(한 PR = 한 산출물, `git revert` 1회 원복, lock 동반, 본문에 검사 결과·되돌리기 명령): 브리프 D-24, [templates/consumer-pr.md](../../templates/consumer-pr.md), [consumer adoption runbook](../runbooks/consumer-adoption.md).
- 실행 못 한 검증은 `NOT_RUN(사유)`, 0 test를 pass로 집계 금지: 브리프 D-25, [tasks-rule](../tasks-rule.md) §6.
- 근거: `docs/survey/cross/backend.md` §5.2(후보 A·D 병행), `docs/survey/cross/licensing.md` §3.5(패키지 메타데이터), 선행 보고서 §8(rc를 두 대표 소비자 PR에서 검증 후 정식; `docs/survey/README.md` §2.2 참조).

## 구현 범위

1. 릴리스 후보 선정: additive 변경만 담은 patch(예: 토큰 alias 추가, d.ts 주석 정정). 변경 내용 자체는 이 task의 산출물이 아니다.
2. `tokens-vX.Y.Z-rc.1`·`ui-vX.Y.Z-rc.1` 태그 + GitHub Release 자산(`kor-travel-<pkg>-X.Y.Z-rc.1.tgz`, `SHA256SUMS`, 동봉 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`).
3. 소비자 PR: `consumers.pins.json`의 대표 소비자(map admin, pinvi web; pinvi는 T-020 완료 시)에서 rc tarball URL 설치 + lock `integrity` 커밋 + CI green. 소비자 PR 위치는 각 저장소 `agent/<agent>-T-501-rc` 브랜치, 본문은 `templates/consumer-pr.md`.
4. `consumer-smoke` dispatch 실행(webpack·Turbopack 양쪽 `next build`).
5. 정식 태그·자산 발행 → 소비자 PR을 정식 버전으로 갱신 → merge.
6. 되돌리기 리허설: 소비자에서 `git revert <merge-commit>` 1회로 직전 lock·버전 복원 → build green 확인 → 리허설 커밋은 merge하지 않고 폐기(브랜치 삭제).
7. 태그 재발행 차단 확인: 같은 태그를 다른 커밋으로 push했을 때 거부되는지(branch/tag protection) 1회 시험, 실패 시 보호 규칙 요청을 `docs/journal.md`에 기록.
8. runbook 문장과 실제 실행이 다른 부분을 `docs/runbooks/release.md`에 반영(절차 변경이 규범 변경이면 2인 리뷰).

## 범위 밖

- 새 토큰·컴포넌트 기능 추가, minor(파괴) 릴리스의 이관 절 작성.
- py 패키지 릴리스 리허설(T-310에서 wheel 자산과 함께 검증), 공개 npm/PyPI 게시·Renovate(T-507).
- 소비자 저장소의 프레임워크 업그레이드 PR(D-24: 채택 PR과 분리).

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/runbooks/release.md              (실행과 다른 문장 보정)
CHANGELOG.md                          (### tokens / ### ui 절에 patch 항목)
docs/journal.md, docs/resume.md
docs/tasks/T-501-release-runbook-rehearsal.md   (evidence 절)
.github/workflows/*.yml               (릴리스 자산 생성 단계 보정이 필요할 때만)
<consumer>/kor-travel-common.lock.json, package.json, package-lock.json   (외부 저장소 PR)
```

## 수용 기준

- `tokens-v*-rc.1`·`ui-v*-rc.1`과 정식 태그가 각각 정확히 1회 존재하고, 같은 버전 문자열의 태그가 두 커밋을 가리키지 않는다.
- 각 Release 자산에 `kor-travel-<pkg>-X.Y.Z.tgz` + `SHA256SUMS`가 있고 `sha256sum -c`가 통과하며, 소비자 `package-lock.json`의 `integrity`가 그 tarball과 일치한다.
- tarball 안에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`와 `"license": "GPL-3.0-or-later"`가 있다.
- 대표 소비자 PR이 rc → 정식 순으로 갱신되어 merge됐고, 본문에 검사 결과·되돌리기 명령이 있다.
- `consumer-smoke` 실행 URL이 evidence에 있고 webpack·Turbopack 두 job 모두 green이다.
- 되돌리기 리허설의 revert 커밋 SHA와 build 결과(exit code)가 evidence에 있다.
- `CHANGELOG.md`에 패키지별 H3 아래 해당 patch 항목이 있다.
- runbook 보정 diff가 있거나 "보정 불필요"의 근거(실행 로그)가 evidence에 있다. 실행하지 못한 단계는 `NOT_RUN(사유)`로 남기고 DONE 전 `외부 선행`으로 승격한다.

## 검증 명령

```bash
git tag --list 'tokens-v*' 'ui-v*'
git rev-list -n 1 tokens-vX.Y.Z && git rev-list -n 1 tokens-vX.Y.Z-rc.1
gh release view tokens-vX.Y.Z --json assets,tagName
gh release download tokens-vX.Y.Z --pattern 'SHA256SUMS' --pattern '*.tgz' -D /tmp/rel && (cd /tmp/rel && sha256sum -c SHA256SUMS)
tar -tzf /tmp/rel/kor-travel-tokens-X.Y.Z.tgz | grep -E 'package/(LICENSE|NOTICE|THIRD_PARTY_NOTICES.md)$'
gh workflow run consumer-smoke.yml -f ref=tokens-vX.Y.Z && gh run list --workflow consumer-smoke.yml -L 1
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
```

Git Bash에서 동일하게 실행한다.

## evidence

- 이 파일 하단 "evidence" 절에 태그·자산 digest·소비자 PR URL·consumer-smoke run URL·revert SHA·exit code를 표로 기록한다.
- `docs/journal.md` 최신 항목에 실행 명령·도구 버전(`npm --version`, `gh --version`)·NOT_RUN 목록을 남긴다.
- runbook 보정이 규범 변경이면 [review archive](../reviews/README.md) 규칙대로 새 report를 만든다.

## rollback 또는 release 차단 조건

- rc 단계에서 소비자 CI 또는 consumer-smoke가 실패하면 정식 태그를 만들지 않는다. 수정은 `-rc.2`로 발행하고 rc.1 자산은 삭제하지 않는다.
- 정식 태그 발행 뒤 결함이 확인되면 같은 버전을 덮어쓰지 않고 patch 버전을 올린다(D-11). 소비자는 revert 1회로 직전 버전으로 돌아간다.
- 되돌리기 리허설이 실패하면(revert 후 build 실패) 원인을 runbook에 기록하고 이 task를 DONE으로 바꾸지 않는다.
