# T-003 고지·출처 파일(NOTICE·THIRD_PARTY_NOTICES·LICENSES/·PROVENANCE·CONTRIBUTING)·SPDX 헤더 규약·tools/check_spdx.py

- 상태: IN_PROGRESS
- 우선순위: P0
- Gate: 문서 검증·도구 테스트
- 선행: 없음

## 목표

GPL-3.0-or-later 저장소가 코드를 받기 전에 권리·출처 고지 골격을 갖추고, 이후 옮겨 오는 모든 파일이 SPDX 헤더와 출처 행을 갖도록 기계 검사한다. 이번 PR에서 `NOTICE`·`THIRD_PARTY_NOTICES.md`·`PROVENANCE.md`·`CONTRIBUTING.md`를 산출하며, `tools/check_spdx.py`와 `LICENSES/` 원문은 잔여 작업으로 이 task 안에서 이어서 완료한다.

## 고정 결정

- [설계 브리프](../plan/design-brief.md) D-17(라이선스·출처·추출 규칙·차단 B1~B8), D-11(tarball·wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉), D-32(SPDX/Origin 헤더 키는 영어).
- ADR-004(라이선스와 출처 고지·추출 gate) — [docs/adr/README.md](../adr/README.md).
- [라이선스 조사](../survey/cross/licensing.md) §2.3(파일군 출처 표 형식), §2.4(서드파티 라이선스), §3.3(고지 파일 구성), §3.4(헤더 규약), §3.5(패키지 메타데이터), §3.7 L1~L5, §4 B1~B8.
- 정정값: pinvi admin ui 파일 수 28([조사 안내](../survey/README.md) §6.2 항목 1). pinvi 유래 파일은 L6 전 추출 금지(B1), 벤더 tgz·`maplibre-vworld-*`·`python-*-api`는 영구 금지(B2).
- 규칙 정본 문서는 `docs/standards/licensing.md`(standards-be 작성자). 이 task는 파일·도구만 만들고 규칙 본문을 복제하지 않는다.

## 구현 범위

| 산출물 | 내용 |
|---|---|
| `NOTICE` | `Copyright (C) 2026 Youn-sok Choi (digitie)`, `GPL-3.0-or-later`, 저장소 URL·연락처, §7 추가 허가 없음 명시(D-17, O-2 기본값) |
| `THIRD_PARTY_NOTICES.md` | shadcn/ui MIT · `@base-ui/react` MIT · radix MIT · class-variance-authority Apache-2.0(고정 버전에 NOTICE가 실제 있으면 원문 유지) · lucide ISC · tailwind-merge/clsx/tw-animate-css MIT · maplibre-gl BSD-3 · pretendard OFL-1.1 · TanStack MIT · zod MIT — 각 항목에 버전·원문 URL·`LICENSES/` 사본 링크 |
| `LICENSES/` | `GPL-3.0-or-later.txt`, `MIT.txt`, `Apache-2.0.txt`, `ISC.txt`, `BSD-3-Clause.txt`, `OFL-1.1.txt` 원문 및 각 의존성의 저작권자 고지가 포함된 LICENSE 사본(잔여). 일반 라이선스 본문만으로 개별 고지를 대체하지 않음 |
| `PROVENANCE.md` | 열: 파일군 · 원천 저장소 · 커밋 · 경로 · 라이선스 · 수정 요약. 초기 행은 조사 기준 커밋(`docs/survey/README.md` §2.1)으로 기록하며 이관 전에는 열 정의 + "아직 옮긴 파일 없음" 상태 허용 |
| `CONTRIBUTING.md` | AI 보조 생성물은 권리자가 GPL로 배포(B8), 헤더 규약 링크, 2인 리뷰·`git add -A` 금지 링크 |
| `tools/check_spdx.py` + `tests/test_check_spdx.py` | 검사 대상 `packages/**`(`.ts`·`.tsx`·`.css`·`.py`·`.mjs`), `tools/*.py`, `templates/**` 코드 조각. 첫 주석 블록에 `SPDX-License-Identifier`·`SPDX-FileCopyrightText` 없으면 exit 1; 이식 파일은 `Origin:` 필수, 수정 시 `Modified:` 필수; `Hallmark ·` 스탬프가 있으면 fail(common 파일에는 없음); geo 유래는 `GPL-3.0-only` 병기 허용(O-20); 생성물(`dist/`·`*.gen.*`)은 제외 목록. stdlib만, Windows 동작 |
| `tools/README.md` 행 | `check_spdx.py` 1행 추가(잔여) |

## 범위 밖

- 소비 앱 조치(map `LICENSE` 전문 복원 L9, `license` 필드 L11, ktc·ktdm 정렬 L8, pinvi L6)는 T-020·T-021·T-410·T-433.
- `docs/standards/licensing.md` 본문(standards-be), 패키지 `package.json`/`pyproject.toml`의 `license` 필드 적용은 T-101·T-201·T-302.
- pg-aiguide 스킬 고지(L12)는 common 미배포이므로 없음.

## 예상 변경 파일

예정 경로는 존재·실행 증거가 아니다. `NOTICE`, `THIRD_PARTY_NOTICES.md`, `PROVENANCE.md`, `CONTRIBUTING.md`, `LICENSES/*.txt`(6), `tools/check_spdx.py`, `tests/test_check_spdx.py`, `tools/README.md`.

## 수용 기준

- `NOTICE`에 저작권자·라이선스 식별자·연락처 3항목이 있고 §7 추가 허가 문구가 없다.
- `THIRD_PARTY_NOTICES.md`의 모든 실제 항목에 고정 버전·원문 URL·`LICENSES/`의 해당 저작권 고지 사본 링크가 있다. cva NOTICE는 해당 버전 upstream의 존재 여부를 확인해 있으면 보존하고 없으면 부재 근거를 남긴다. 문서의 과거 항목 수를 완료 기준으로 쓰지 않는다.
- `LICENSES/`에 라이선스 6종 본문과 의존성별 저작권 고지 사본이 있고 `THIRD_PARTY_NOTICES.md`·`NOTICE`의 링크가 모두 해석된다.
- `PROVENANCE.md`에 pinvi 유래 행이 없고(B1), `maplibre-vworld-*`·`python-*-api` 행이 없다(B2).
- `python3 -B -X utf8 tools/check_spdx.py`가 헤더 없는 fixture에서 exit 1, 규약 준수 fixture에서 exit 0이며 테스트가 이를 고정한다(잔여).
- 저장소 어디에도 Hallmark `SKILL.md` 문장 인용이 없다(B3).
- `tools/validate_document_links.py` 오류 0.

## 검증 명령

```bash
python3 -B -X utf8 tools/validate_document_links.py
python3 -B -X utf8 tools/check_spdx.py
python3 -B -X utf8 -m unittest discover -s tests -p "test_check_spdx.py" -v
ls LICENSES
rg -n "Hallmark" --glob '!docs/survey/**' --glob '!docs/plan/**' .
rg -n "pinvi|maplibre-vworld|python-.*-api" PROVENANCE.md
```

Git Bash에서 동일.

## evidence

- 명령·exit code·검사 파일 수를 이 절과 `docs/journal.md`에 남긴다. `check_spdx.py`·`LICENSES/`가 미완이면 `NOT_RUN(잔여)`로 두고 `DONE` 전에 완료한다.

## rollback 또는 release 차단 조건

- 문서·도구만 바뀌므로 `git revert` 1회로 원복한다.
- `check_spdx.py`가 없거나 실패하는 상태에서는 `packages/*`에 코드를 넣는 T-101·T-201·T-302를 `DONE`으로 바꾸지 않는다.
- tarball·wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`가 동봉되지 않으면 T-109·T-212·T-310 릴리스를 차단한다.
