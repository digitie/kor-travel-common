# kor-travel-common

kor-travel 제품군(kor-travel-airport·concierge·docker-manager·geo·map·weather·pinvi)의 UI·백엔드 공통 코드와 공통 규칙을 정의하는 GPL-3.0-or-later 저장소다. 디자인 토큰(`--kt-*`)·React 19 UI 컴포넌트·Python 인프라 모듈을 패키지로 배포하고, 색상 톤·UX·PC/Mobile Web·OpenAPI·라이브러리/플랫폼 버전 일치 규칙을 `docs/standards/`에 두며, `versions.json`과 검사 도구로 7개 소비 저장소의 정렬 상태를 보고한다. 확정 task: T-001 · 마지막 갱신: 2026-09-06 · 결정 근거: [설계 브리프](docs/plan/design-brief.md).

## 배포 단위

| 단위 | 위치 | 배포 이름·채널 | 상태(2026-09-06) |
|---|---|---|---|
| 디자인 토큰 | `packages/tokens` | npm `@kor-travel/tokens`(잠정, 열림 O-5) — GitHub Release tarball, 태그 `tokens-vX.Y.Z` | 미작성(T-101) |
| React UI | `packages/ui` | npm `@kor-travel/ui`(잠정, 열림 O-5) — 태그 `ui-vX.Y.Z` | 미작성(T-201) |
| Python 공통 | `packages/py/kor-travel-common` | 배포 이름 `kor-travel-common`, import `kortravelcommon` — git 태그 `py-vX.Y.Z` + wheel 자산 | 미작성(T-302) |
| 규칙 문서 | `docs/standards/` | 저장소 문서(소비자는 링크·템플릿으로 채택) | 초안(T-005·T-104~T-107·T-204·T-301·T-302) |
| 템플릿 | `templates/` | 소비자 설정 조각·PR 규격·체크리스트 | 규약·PR 틀 작성(T-007); 설정·캡처는 T-107·T-108에서 검증 |
| 버전 레지스트리·도구 | `versions.json`, `tools/*.py` | `check_versions`·`kt_contrast`·`ux_lint`·`check_spdx`·문서 validator 2종 | validator 2종 검증 완료(T-002), `versions.json`·`check_versions` 부분 구현(T-005), `kt_contrast`·`ux_lint`·`check_spdx`는 T-103·T-003 |

배포 채널·SemVer 0.x·태그 불변 규칙은 [release runbook](docs/runbooks/release.md), 경계와 의존 방향(앱 → ui → tokens, 앱 → py)은 [architecture](docs/architecture/README.md)가 정본이다. `config` npm 패키지와 `api-client-core`는 만들지 않는다.

## 소비자

| 저장소 | 약칭 | 표면 | 1차 채택 대상 | 외부 선행·열림 |
|---|---|---|---|---|
| kor-travel-map | map | admin UI·API·Dagster | tokens·ui·py 1차 | — |
| kor-travel-weather | wx | admin(Tailwind 미도입)·API | tokens 1차(별칭 shim)·py 1차 | — |
| pinvi | pinvi | admin(PinVi Admin)·사용자 웹·모바일(규칙만) | tokens·ui 1차(admin) | L6 라이선스 선언(O-1) |
| kor-travel-airport | kta | 무인증 백업·collector 패널(Admin)·API | tokens·소형 ui·py 1차 | WIP 병합(O-9) |
| kor-travel-geo | geo | React 18 admin·API | tokens → React 19 후 ui, py 2차 | React 19 승인(O-25) |
| kor-travel-concierge | ktc | frontend·API | 규칙·`tokens.json` 참조 → L8 후 코드 | L8 GPL 정렬(O-2), CI 신설 |
| kor-travel-docker-manager | ktdm | Next 14 frontend·API | 업그레이드 후 tokens, L8 후 ui·py | L8 GPL 정렬(O-2) |

소비자 표면·채택 순서는 [consumers](docs/architecture/consumers.md), 채택 gate는 [adoption readiness](docs/architecture/adoption-readiness.md), 현재 채택 버전은 생성물 [integration map](docs/integration-map.md)이 정본이다. 조사 근거는 `docs/survey/commonality-matrix.md` §1·§2다.

## 문서

상세 문서를 한꺼번에 읽지 않도록 [문서 지도](docs/README.md)가 작업별 진입점과 정본 관계를 관리한다. 에이전트는 [AGENTS.md](AGENTS.md)부터 읽고 작업별 시작점은 [SKILL.md](SKILL.md)에서 고른다.

- [아키텍처 개요](docs/architecture/README.md): 배포 단위·의존 방향·스타일 배포·소비자
- [현재 진척과 다음 작업](docs/resume.md)
- [열린 task와 gate](docs/tasks.md)
- [결정 색인과 ADR](docs/adr/README.md)
- [적대적 리뷰 아카이브](docs/reviews/README.md)
- [에이전트 workflow](docs/runbooks/agent-workflow.md)

## 저장소 상태

2026-09-06 기준 Phase 0(골격·규칙·gate)이다. 진입 문서·ADR·규칙 문서 초안·runbook·고지 파일·`versions.json`·task 원장을 만들고 문서 validator 2종과 `.github/workflows/docs.yml`로 자기 검증한다. 코드 패키지 3종은 아직 없으며, 규칙 문서는 실물 패키지(T-101·T-201·T-302)와 대조해 확정하는 task가 남은 정본 초안이다. 7개 소비 저장소의 조사 결과는 [docs/survey](docs/survey/README.md)에 기준 커밋 고정 스냅샷으로 있고, 사용자 확인이 필요한 열린 결정(O-1~O-25)은 [설계 브리프](docs/plan/design-brief.md) §2에 기본값과 함께 있다.

## 개발

정본 환경은 Linux/WSL bash이고 Windows는 Tier 2다. 도구 설치·경로 표기·검증 명령 사다리는 [개발 환경](docs/dev-environment.md), 문서 검사 도구는 [tools](tools/README.md)를 본다. 문서만 바꿨을 때의 최소 검증은 다음과 같다(Git Bash에서 동일).

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/validate_plan.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

## 라이선스

이 저장소는 `GPL-3.0-or-later`다([LICENSE](LICENSE); 저작권자·버전·연락처는 [NOTICE](NOTICE)). 이식·벤더링한 서드파티 코드의 라이선스는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), 파일군별 원천 저장소·커밋·라이선스는 [PROVENANCE.md](PROVENANCE.md), 기여 조건(AI 보조 생성물은 권리자가 GPL로 배포)은 [CONTRIBUTING.md](CONTRIBUTING.md)에 있다. 배포 tarball·wheel에는 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`를 동봉하고 패키지 메타데이터에 `license: "GPL-3.0-or-later"`를 선언한다. 라이선스·고지·SPDX 헤더·추출 규칙의 정본은 [licensing](docs/standards/licensing.md)이다.
