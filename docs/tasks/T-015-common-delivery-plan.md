# T-015 npm·PyPI 미게시와 common 구현·외부 릴리스 선행 분리

- 상태: IN_PROGRESS
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

2026-09-07 착수: PR #3은 659aa6dd3cb319761e8f7290155e025b11029c83으로 병합했다. 원안 ADR-013 결정 1과 T-201·T-205·T-306/307의 선행, T-010의 외부 dispatch 수용 기준이 common 단독 완주를 막는 것을 원문에서 확인했다. 원문 대조 후 ADR-014·T-010a·T-109a·T-212a·T-310a를 작성했다. 전체 101 task의 metadata/DAG 검사와 문서 link 검증이 성공했다. 외부 선행 노드를 제외한 도달성 검사에서 UI T-201/205/208/210·Python T-306/307/308의 common 경로가 열리고 T-010a·T-109/212/213/310/311·T-507은 대기를 유지함을 확인했다. 이는 실행 성공 판정이 아니다. 독립 첫 리뷰는 A/B 모두 BLOCK이다. 태그 대상 충돌(P1 중복 2건), 외부 dispatch의 후보 선행 누락(P2), 0.2 보존 책임(P2), 과거 release branch와 현재 main 원장 왕복(P2)을 확인했다. 원 ID·심각도를 보존했고 최초 5개 finding은 원 reviewer가 FIXED로 확인했다. 첫 post-fix는 A PASS/B BLOCK으로, tag 실패 전파와 release SHA CI 경로 두 추가 finding을 수정했다. [수정 후 리뷰](../reviews/adversarial/2026-09-07-t015-post-fix.md)의 두 번째 재검토 전에는 완료하지 않는다. 사용자는 이 작업 병합 뒤 대기를 요청했다.

## rollback 또는 release 차단 조건

정책·계획만 바뀌므로 이 PR의 revert로 원복할 수 있다. 후보 보존이나 실제 소비자 gate가 빠지거나 DAG가 순환하면 merge하지 않는다. npm/PyPI 게시를 재도입하려면 새로운 사용자 지시와 별도 결정이 필요하다.
