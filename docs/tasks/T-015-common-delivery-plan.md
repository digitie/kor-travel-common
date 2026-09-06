# T-015 npm·PyPI 미게시와 common 구현·외부 릴리스 선행 분리 (2026-09-07, PR #4)

- 상태: DONE
- 우선순위: P0
- Gate: 문서 검증·2인 독립 리뷰
- 선행: T-005

## 목표

사용자의 “common 라이브러리만 작성”, “이어서 완주”, “npm pypi 에는 안 올릴꺼야” 지시를 실행 가능한 순차 작업으로 반영한다. 계정 확보·공개 registry 게시 계획을 제외하고 common 구현을 외부 릴리스 대기와 분리한다.

## 고정 결정

- 사용자 지시가 [AGENTS](../../AGENTS.md)와 기존 ADR보다 우선한다. npm/PyPI 게시를 위한 권한·계정·이름 예약 작업을 하지 않는다.
- 기존 [ADR-005](../adr/005-release-channel-immutable-tags-semver-0x.md)의 GitHub Release·Git 태그 채널과 [ADR-013](../adr/013-package-release-execution-contract.md)의 호환 peer·승인 소비자 경계는 유지한다. 변경하는 조항은 새 ADR에 명시한다.
- GPL-3.0-or-later·출처 고지는 현재 common 정본을 유지한다. 소비자 라이선스 변경을 대신 수행하지 않는다.

## 구현 범위

1. 새 ADR로 npm/PyPI 미게시·패키지 식별자 확정·검증 후보 보존과 다음 minor 구현 순서를 결정한다.
2. T-006의 기존 계정 확보 범위는 사용자 지시로 철회했음을 기록하고, 이름 확정·미게시 기록으로 범위를 변경한다. 과거 가용성 검사를 성공으로 표시하지 않는다. T-507에서 공개 게시 재평가와 T-006 선행을 제외한다.
3. common 자체 검증과 소비자 검증이 섞인 선행을 하위 task로 나눈다. T-010의 외부 소비자 dispatch와 토큰·UI·Python 0.1 후보 보존을 별도로 추적한다. 다음 구현은 검증된 후보 보존을 요구하고 정식 릴리스·채택은 실제 소비자 evidence를 계속 요구한다.
4. 관련 architecture·standards·runbook·진입 문서·계획·task DAG를 동기화한다. 조사·과거 review는 수정하지 않는다. 이전 ADR 본문은 보존하고 상태·후속 링크만 갱신한다.

## 범위 밖

패키지 구현, registry 조회·게시·이름 예약, 실제 GitHub Release·태그 생성, 소비자 저장소 변경·설치·빌드·배포, 권리 gate의 승인 간주.

## 예상 변경 파일

ADR 색인·새 ADR·관련 이전 ADR 상태, architecture·standards·runbook의 채널/순서 절, AGENTS·README, 설계 브리프·통합 계획, T-006·T-010·T-109·T-201·T-205·T-212·T-213·T-302·T-306·T-307·T-310·T-311·T-507과 새 하위 task, task 원장·resume·journal·CHANGELOG.

## 수용 기준

- 현재 규범은 npm/PyPI 미게시와 기존 패키지 식별자를 명확히 규정하고 이름 확보 실패를 이유로 개명·차단하지 않는다.
- common 구현 경로에 외부 소비자 실행·이전 minor 정식 릴리스 대기가 남지 않는다. 외부 검증은 별도 BLOCKED task와 명시적인 릴리스 선행으로 보존한다.
- 후속 minor가 앞선 후보를 덮어쓰지 않도록 commit·원격 ref·산출물 digest·검증 결과와 버전 변경 순서를 명시한다. local pack을 정식 발행으로 세지 않는다.
- 소비자 쓰기·미승인 소비자 설치·미실행 검증의 성공 처리를 허용하지 않는다. 기존 태그 불변·재발행 금지·고지·peer 계약을 유지한다.
- 문서 link·plan·unittest·diff 검증과 동일 immutable 후보의 독립 2인 리뷰가 통과한다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

## evidence

2026-09-07: PR #3 병합 기준 `659aa6dd3cb319761e8f7290155e025b11029c83`에서 ADR-013·관련 task 원문을 다시 대조해 ADR-014와 T-010a·T-109a·T-212a·T-310a를 작성했다. 101 task metadata/DAG·문서 링크를 검사했고 common 구현 도달성과 외부 gate 보존을 모델로 확인했다. 모델은 제품 실행 성공이 아니다.

최종 candidate `95c139fdea523910fb5f1bdd32f5bae728df2915`는 두 독립 reviewer PASS이며 누적 9개 finding ID가 모두 FIXED, 새 finding 0이다([최종 리뷰](../reviews/adversarial/2026-09-07-t015-post-fix-03.md)). Windows 115 tests·skip 0과 문서·plan·diff 검사, 발행 실패/자산 확인 mock을 통과했다. candidate CI 34066138272도 성공했다. 이전 회차의 발견·수정·검증은 리뷰 원본과 journal에 보존했다.

실제 package build/install·후보 보존·Release·소비자 실행은 NOT_RUN(후속 구현 또는 외부 task 범위)이다. T-006은 철회된 계정 확보 실행이 아니라 범위 변경·식별자 확정 기록으로 종료한다. 사용자는 현재 PR #4 병합 뒤 대기를 요청했으므로 다음 task는 시작하지 않는다.

## rollback 또는 release 차단 조건

정책·계획만 바뀌므로 이 PR의 revert로 원복할 수 있다. 후보 보존이나 실제 소비자 gate가 빠지거나 DAG가 순환하면 merge하지 않는다. npm/PyPI 게시를 재도입하려면 새로운 사용자 지시와 별도 결정이 필요하다.
