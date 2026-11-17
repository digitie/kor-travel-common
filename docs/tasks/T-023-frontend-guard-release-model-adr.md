# T-023 프론트 정책 guard·릴리스 모델 ADR(정책을 읽는 자리와 내장 정책) (2026-11-17, PR #60)

- 상태: DONE
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰·소유자 결정
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 A. T-022도 `docs/adr/README.md`를 고친다. 뒤에 병합하는 쪽이 rebase한다

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§4.1(K-01·K-02)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

2026-11-17에 정책 한 줄(`vworld-map-web` 1.0.4)이 다섯 저장소의 재vendor PR 5개·파일 80개를 만들었다. guard가 정책과 Node/npm 도구 축을 `main`에서 읽고, 패키지마다 한 버전만 허용하고, tarball이 정책 전체의 사본을 싣기 때문이다. 이 task는 그 모델을 어떻게 바꿀지 ADR-019로 결정한다. 구현은 T-024·T-025다.

## 고정 결정

- 현재 모델의 의도는 [frontend-libraries](../standards/frontend-libraries.md) '검사와 갱신' 절과 [ADR-017](../adr/017-shadcn-radix-shared-components.md)·[ADR-018](../adr/018-exact-node-npm-build-toolchain.md)이 정본이다. 이 ADR은 그 의도(최신 정본으로의 강제 수렴)를 유지할지부터 적는다.
- 단순함이 결박보다 우선이다(`AGENTS.md` Simplicity First). 새 강제 계층을 더하는 안은 채택하지 않는다.
- 결정자는 소유자다. 에이전트는 초안과 권고까지 쓴다.
- "ADR-019"는 `docs/architecture/consumers.md`·`docs/architecture/adoption-readiness.md`·`docs/plan/design-brief.md`에서 geo 저장소의 ADR을 가리키는 데 이미 쓰였다. 이 ADR은 common의 ADR-019이고 본문에 그 구분을 적는다.

## 구현 범위

1. ADR-019 초안: 계획 문서 §4.1의 네 안(정책을 호출 커밋에서 읽기 / 예고 필드 / 직전 버전 허용 / 현행+절차)을 대안 검토로 적고 하나를 결정한다. 기본 권고는 '정책과 도구 축을 `common-ref`에서 읽기 + 막지 않는 지연 보고'다.
2. 어느 안이든 다뤄야 하는 사실을 적는다: guard가 Node/npm도 `main`의 `versions.json`에서 읽는다(Node/npm patch가 같은 함대 실패를 만든다). weather·transport는 `ci.yml` 안의 guard 호출이 PR을 막는다. 소비자는 자기가 고정한 옛 검사기를 실행한다.
3. 예고 필드를 택한다면 함께 정한다: 동시 예고 수, 최대 창 길이와 초과 시 처리, registry 보안 갱신의 긴급 경로, Node/npm 축에도 같은 주기를 쓰는지, guard를 올릴 수 없는 소비자(Map, T-416)의 경로.
4. 내장 정책의 자리를 정한다. 권고: 각 패키지는 자기 것(자기 peer와 자기 식별)만 싣고 로컬 `check:dependencies`는 그것만 검사한다. 함대 전체의 정확 버전 대조는 중앙 guard에 남긴다. 'tarball에서 사본을 빼고 경로를 인자로 받기'를 택한다면 그 파일의 이름과 갱신 경로를 정한다.
5. 일부 소비자만 쓰는 부품은 기존 필수 패키지를 키우지 않고 선택형 산출물 패키지로 낸다는 원칙을 기록한다(`@kor-travel/toast` 선례, 계획 문서 §4.8의 비교).
6. 2026-11-17 실측(PR·시각·파일 수)을 컨텍스트에 인용한다. `docs/adr/README.md` 색인과 다음 후보 번호 갱신.

## 범위 밖

검사기·생성기·workflow 코드(T-024), 패키지 pack(T-025), 소비자 저장소.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/adr/019-frontend-policy-guard-model.md
docs/adr/README.md
docs/journal.md, docs/resume.md
```

## 수용 기준

- [x] ADR이 네 안 각각의 '얻는 것·잃는 것'과 결정 이유를 적고 상태가 `accepted`다(소유자 결정과 날짜 기록 포함).
- [x] Node/npm 도구 축, 내장 정책의 자리, 선택형 패키지 원칙이 각각 결정 문장으로 있다.
- [x] 결정이 T-024·T-025의 수용 기준으로 그대로 옮길 수 있는 문장으로 적혀 있다.
- [x] 문서 검증이 오류 0이다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
git diff --check
```

## evidence

ADR 본문과 두 리뷰 report. 소유자 결정은 PR 대화 또는 ADR의 '결정' 절에 날짜와 함께 남긴다.

실행 기록(2026-11-17): 소유자 결정 원문은 [ADR-019](../adr/019-frontend-policy-guard-model.md) 머리에 있다. 리뷰 [report](../reviews/adversarial/2026-11-17-adr-019-020-owner-decisions.md)(A·B 둘 다 PASS-with-fixes, finding 반영). `validate_document_links.py` 오류 0, `validate_plan.py` 오류 0, `git diff --check` 통과.

## rollback·release 차단 조건

- 문서 전용. `git revert` 1회.
- 소유자 결정 없이 `accepted`로 병합하지 않는다. 결정이 미뤄지면 `proposed`로 두고 이 task는 BLOCKED(외부 선행: 소유자 결정)로 바꾼다.
