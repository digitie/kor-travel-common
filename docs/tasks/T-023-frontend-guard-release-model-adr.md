# T-023 프론트 정책 guard·릴리스 모델 ADR(전환 창과 내장 정책 분리)

- 상태: READY
- 우선순위: P0
- Gate: 문서 검증·2인 리뷰·소유자 결정
- 선행: 없음
- 소유 저장소: kor-travel-common
- 병렬: 묶음 A

출처는 [공통화 재조사·계획(2026-11-17)](../plan/commonization-plan-2026-11-17.md)의 §2.2·§4.1(K-01·K-02)이다. 근거 위치(file:line)와 차이 분석은 그 문서가 정본이며 여기서 반복하지 않는다.

## 목표

2026-11-17에 정책 한 줄(`vworld-map-web` 1.0.4)이 다섯 저장소의 재vendor PR 5개·파일 80개를 만들었다. guard가 정책을 `main`에서 읽고, 패키지마다 한 버전만 허용하고, tarball이 정책 사본을 싣기 때문이다. 이 task는 그 모델을 어떻게 바꿀지 ADR로 결정한다. 구현은 T-024·T-025다.

## 고정 결정

- 현재 모델의 의도는 [frontend-libraries](../standards/frontend-libraries.md) '검사와 갱신' 절과 [ADR-017](../adr/017-shadcn-radix-shared-components.md)·[ADR-018](../adr/018-exact-node-npm-build-toolchain.md)이 정본이다. 이 ADR은 그 의도(정확 버전 수렴)를 유지할지부터 적는다.
- 단순함이 결박보다 우선이다(`AGENTS.md` Simplicity First). 새 강제 계층을 더하는 안은 채택하지 않는다.
- 릴리스된 같은 버전에 다른 bytes를 덮어쓰지 않는다([ADR-014](../adr/014-common-implementation-without-registry-publishing.md)).

## 구현 범위

1. ADR-019 초안: 계획 문서 §4.1의 세 안(전환 창 / 정책을 고정 커밋에서 읽기 / 현행+절차)과 내장 정책 분리를 대안 검토로 적고 하나를 결정한다. 기본 권고는 전환 창 + 내장 정책 분리다.
2. 결정에 포함할 것: 직전 버전을 몇 세대까지 허용하는가(권고 1세대), 만료일 표기와 공지 위치, 만료 뒤 동작, 소비자가 호출 SHA를 올리지 않았을 때의 동작, registry 패키지(`next` 등)에도 같은 창을 적용하는가.
3. 2026-11-17 실측(PR·시각·파일 수)을 컨텍스트에 인용한다.
4. `docs/adr/README.md` 색인과 다음 후보 번호 갱신.

## 범위 밖

검사기·생성기·workflow 코드(T-024), 패키지 pack(T-025), 소비자 저장소.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다.

```text
docs/adr/019-frontend-policy-transition-window.md
docs/adr/README.md
docs/journal.md, docs/resume.md
```

## 수용 기준

- [ ] ADR이 세 안 각각의 '얻는 것·잃는 것'과 결정 이유를 적고 상태가 `accepted`다(소유자 결정 기록 포함).
- [ ] 결정이 T-024·T-025의 수용 기준으로 그대로 옮길 수 있는 문장(허용 세대 수, 만료 규칙, 형식 호환)으로 적혀 있다.
- [ ] 문서 검증 4종이 오류 0이다.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
git diff --check
```

## evidence

ADR 본문과 두 리뷰 report. 소유자 결정은 PR 대화 또는 ADR의 '결정' 절에 날짜와 함께 남긴다.

## rollback·release 차단 조건

- 문서 전용. `git revert` 1회.
- 소유자 결정 없이 `accepted`로 병합하지 않는다. 결정이 미뤄지면 `proposed`로 두고 이 task는 BLOCKED(외부 선행: 소유자 결정)로 바꾼다.
