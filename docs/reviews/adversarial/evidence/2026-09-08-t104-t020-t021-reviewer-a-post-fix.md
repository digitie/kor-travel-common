# T-104 · T-020 · T-021 수정 후 독립 리뷰 A 원본

## 실행·기준선

- 실행 ID: `A-T104-T020-T021-POSTFIX-20260908-073154`.
- 시작: 2026-09-08 07:31:54.594 KST. 종료: 2026-09-08 07:38:04.869 KST.
- 후보: `b241ed9dcdd198a62c820e039717aef74f86ef2e` (`git rev-parse b241ed9`로 확인).
- tree: `a6350aef9588eea9979a70c0edf356259376ab66`.
- 후보 parent: `304d10c4e52349d395cc5c5382418d3121f5d112`.
- 수정 delta base: `7ffe525f8a6cfaef4ca4cbab7017306b1994f24a`.
- 전체 변경의 원 base: `1eb8a78b0fe8ec890b5d15b9f4abfd3f81ef9d59`.
- 전용 detached: `F:/dev/kor-travel-common-wt/review-t104-t020-t021-post-a`. 시작·종료 SHA/tree 일치, `git status --porcelain=v1` 모두 빈 출력.
- 후보·소비자·기존 원본을 수정하지 않았고 commit/push하지 않았다. 새 원본 한 파일만 기본 checkout에 작성했다. 브라우저 probe는 stdin/page.setContent, build/pack/install은 기존 A 도구를 이용한 임시 사본에서 수행했다. B의 원본/결과는 미열람이다.

## 요청·검토 범위

요청은 “최종 후보 immutable b241ed9를 대상으로 초기 A finding과 7ffe525..b241ed9 전체 delta를 확인하고, TK-8/T-103·dark cascade·z/shadow·scoped shadcn alias·TK 번호·license-only 선행과 소비자별 evidence를 검증한 새 원본을 작성하라”였다. 최초 공통 manifest의 범위를 이어받되, 그 파일의 초기 candidate를 수정 후 후보와 혼동하지 않았다.

30개 delta 경로 중 제품/규범/task/요청 변경을 읽고, 추가된 자신의 최초 원본과 manifest를 대조했다. B 원본 내용은 독립성 때문에 제외했다. 변경 없는 tokens.css·theme.css·생성기·상위 정책은 이전 원본의 검토를 재사용하고 값·생성물·회귀는 다시 실행했다.

## 판정과 원 finding disposition

**BLOCK.** 원 finding 3건은 FIXED, 3건은 PARTIALLY_FIXED/OPEN이다. 새 P2 회귀 1건을 추가했다. 현재 OPEN 합계는 P1 2건, P2 2건이며 P0/P3는 없다. OPEN 항목의 owner는 후보 작성자, gate와 기한은 이 PR merge 전 수정 및 독립 재검토다.

| 원 ID | 원 심각도 | disposition | 확인 |
|---|---|---|---|
| A-P1-01 | P1 | PARTIALLY_FIXED / OPEN | T-103이 TK-8을 참조하지만 3:1로 낮춘 텍스트 기준이 상위 architecture 4.5:1과 충돌 |
| A-P2-02 | P2 | PARTIALLY_FIXED / OPEN | font/dark/색/alpha 참조는 정정, 타입 스케일 참조 3곳이 TK-3으로 잘못 이동 |
| A-P2-03 | P2 | FIXED | class `:root:not(.dark)`와 light media 선택자를 실제 브라우저에서 확인, dark common fallback 적용 |
| A-P2-04 | P2 | FIXED | shadow/z 표와 TK-6이 모두 프로필·등록 예외만 허용으로 일치 |
| A-P2-05 | P2 | FIXED | `[data-kt-surface]`에서 semantic 1rem → shadcn alias 1rem → 실제 radius 16px, light/dark 모두 일치 |
| A-P1-06 | P1 | PARTIALLY_FIXED / OPEN | 소비자별 license-only PR 선행은 분리했지만 요청의 해제 조건에 후속 B4·코드 링크 evidence가 남음 |

## A-P1-01 잔여 — 3:1로 낮춘 기준이 상위 정본과 일반 텍스트 기준을 만족하지 않는다

- 위치: `docs/standards/design-tokens.md:113`, 120행; `docs/tasks/T-103-kt-contrast-ux-lint.md:21`; `docs/architecture/style-delivery.md:98`.
- 수정 확인: disabled 제외와 TK-8 링크를 추가했다. 그러나 초기의 tertiary/status 텍스트 4.5:1을 3:1로 내렸다. 상위 architecture의 §9는 여전히 primary/secondary/tertiary 및 status 텍스트/tint에 4.5:1을 요구한다. TK-8은 tertiary를 메타·캡션, status를 상태 텍스트로 정의하며 큰 글자나 비텍스트 mark로 제한하지 않는다.
- 최소 반례: 작은 캡션 또는 상태 라벨의 전경 `#888`, 배경 `#fff` 대비를 계산하면 `3.5448862152994`다. 새 task/표의 3:1 기준은 통과시키지만 architecture의 4.5:1 기준은 실패한다. 실제 kt_contrast는 미구현이므로 이 값은 독립 상대휘도 계산이며 도구 실행 결과가 아니다.
- 외부 교차 확인: WCAG 2.2 SC 1.4.3은 일반 텍스트에 4.5:1, 큰 텍스트에 3:1을 정하고 비활성/장식 등은 제외한다. 단순히 caption/status라는 역할은 3:1 예외가 아니다. [W3C 공식 SC 1.4.3 설명](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), 2026-09-08 조회.
- 영향: 기준을 단일화하는 과정에서 작은 텍스트의 신규 미달을 정상 처리할 수 있다. task 괄호 안의 중복 목록에는 TK-8의 icon/brand-tint도 여전히 생략돼 있어 목록을 복제하지 않는 편이 안전하다.
- 수용 권고: 일반 텍스트 4.5:1을 보존하고 3:1은 큰 텍스트/비텍스트로 검증 가능한 경우에만 분리한다. architecture·TK-8·T-103을 하나의 동일 계약으로 맞춘다. 기존 미달은 baseline/기한으로 다루며 기준을 낮춰 없애지 않는다.

## A-P2-02 잔여 — 타입 스케일의 근거가 역할 표 TK-3으로 이동했다

- 위치: `docs/standards/frontend-stack.md:127`, `docs/standards/responsive-web.md:75`, `docs/standards/ux-guide.md:131`.
- 재현: `rg -n '타입 스케일|스케일 이름|admin 타입' docs/standards/frontend-stack.md docs/standards/responsive-web.md docs/standards/ux-guide.md`. 세 문장이 새 TK-3을 참조한다. TK-3은 44개 semantic 역할/값 표이고 7단 타입 스케일 및 비inline @theme 설명은 TK-5/TK-10에 있다.
- 영향: 초기의 없는 TK-14/15 등은 정정됐지만 의미 기준으로 확인하면 타입 스케일/생성 방식 참조가 여전히 잘못된다. 파일 링크 validator로는 잡히지 않는다.
- 수용 권고: 7단 값은 TK-5, 비inline @theme/생성물 규칙은 TK-10 등 실제 내용을 담은 정본으로 연결한다. 전역 숫자 치환보다 의미별 대조로 잔여 참조를 닫는다.

## A-P1-06 잔여 — LICENSE-only 요청의 해제 조건이 후속 코드 채택을 요구한다

- 위치: `docs/plan/requests/concierge-license-l8.md:17`, 22, 26–31행; `docs/plan/requests/docker-manager-license-l8.md:17`, 26–31행.
- 수정 확인: T-021의 소비자별 external evidence와 각 tokens/UI/Python task는 독립 license-only PR의 SHA/고지를 선행으로 확인하게 바뀌었다. 기존 task 간 직접 순환은 제거됐다.
- 잔여: concierge 요청은 B4 diff를 후속 코드 채택 PR에서 확인한다고 정하고도 해제 조건에서 B4 결과를 요구한다. docker-manager 요청은 L8 이후에만 코드 링크를 넣으라고 정하고도 L8 해제 조건에 `common 코드 링크와 함께 필요한 provenance`를 요구한다. 해제 조건의 저장 위치도 T-021 새 원장과 별개로 T-454/T-473을 그대로 가리킨다.
- 최소 재현: 두 요청의 `대상 외부 PR` → `외부 evidence 기록` → `해제 조건`을 순서대로 따른다. LICENSE-only PR에 금지된 코드 채택 결과를 해제 조건 충족에 사용해야 하므로, 코드 채택을 열기 위한 선행이 다시 후속 작업을 요구한다.
- 수용 권고: G-LIC 해제 조건을 license-only PR의 LICENSE/metadata/고지 검사로 한정하고 T-021 소비자 행에 기록한다. B4/코드 링크 provenance/build evidence는 별도 채택 gate로 분리한다. 요청의 앞부분만이 아니라 해제 조건과 기록 위치도 함께 수정한다.

## A-P2-07 신규 — scoped alias가 앱 소유 chart 팔레트를 덮는다

- 위치: `packages/tokens/shadcn.css:88`–92행. 계약 근거: `docs/standards/design-tokens.md:85`, TK-13의 chart 값 앱 소유 문장.
- 최소 재현: candidate tokens.css, shadcn.css를 로드하고 뒤에 앱 `:root { --chart-1: purple; }`를 둔다. `<section data-kt-surface="admin"><div style="background:var(--chart-1)"></div></section>`에서 computed 값을 읽는다.
- 실제 Chromium 전후 결과: 초기 7ffe525의 shadcn.css는 `--chart-1=purple`, `background=rgb(128, 0, 128)`; candidate는 `--chart-1=oklch(51.4% 0.081 169)`, 배경도 common brand가 된다. 바뀐 파일만 git object에서 읽어 동일 페이지로 대조했다.
- 원인: 낮은 specificity의 :where라도 해당 scope에 명시한 chart 선언은 부모에서 상속되는 앱 chart 값보다 우선한다. radius/semantic 파생 수정에 앱 소유 chart 5개까지 복사한 새 회귀다. 추가한 package 시험은 문자열 존재만 확인하므로 이 상속 결과를 검증하지 않는다.
- 영향: 기존 앱이 root에서 정의한 차트 색이 surface marker 추가/공통 파일 업데이트만으로 바뀐다. chart 색을 앱이 소유한다는 계약과 시각 회귀 경계를 깨뜨린다.
- 수용 권고: scoped semantic 파생 갱신과 앱 소유 chart 팔레트를 분리해 기존 root chart 값을 보존한다. 위 최소 사례 및 profile radius 갱신을 함께 computed style로 검증한다. 이 문제를 해결하려고 소비자 앱 파일을 수정하지 않는다.

## 실제 검증

모든 후보 소스 접근은 지정 detached cwd에서 수행했다. 44 변수와 88 light/dark 값을 Markdown 표에 다시 대조했으며 `sets 44 44 44 equal True`, `mismatches []`였다.

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/validate_document_links.py` | 385 documents, 2372 local targets, errors 0 |
| `python -B -X utf8 tools/validate_plan.py` | task 106, 오류 0 |
| `python -B -X utf8 tools/check_aliases.py` | CSS 1개, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py` | 45개, 오류 0 |
| `python -B -X utf8 tools/scan_secrets.py --all` | 500파일, 발견 0, 예외 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --all` | 500파일, 발견 0, 예외 0 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q` | Windows 238 tests, 53.560초, OK, skip 0 |
| WSL `uv run --no-project --python 3.11 --with jsonschema python -B -X utf8 -m unittest discover -s tests -p "test_*.py" -q` | 238 discovered, 33.657초, OK skipped 1; 고유 237개 실행 통과, Windows 8.3 전용 1개 미실행 |
| `npm run check --workspace packages/tokens` | 생성물 clean, exit 0 |
| `npm test --workspace packages/tokens` | 7 pass, 0 skip |
| `git diff --check 7ffe525 HEAD` | 빈 출력, exit 0 |

기존 A의 `t102-a-package.py`를 candidate cwd에서 실행했다. 임시 사본에서 npm ci/check/build/check/test 전부 exit 0, 7 package tests 통과, pack 19개 파일(alias 포함·examples 제외), 임시 tarball 설치와 공개 export resolve 통과다. Windows Node 25.9.0/npm 11.12.1은 engine 경고가 있었으며 정확한 CI Node 실행과 같다고 표시하지 않았다.

브라우저 검증은 Node stdin으로 Playwright Chromium을 호출하고 candidate CSS를 page.setContent에 넣었다. 파일 쓰기 없이 다음을 확인했다.

- class light override: `oklch(47% 0.14 255)`, class dark fallback: `oklch(76% 0.085 169)`.
- media light/dark 역시 각각 위 두 값. `page.emulateMedia({colorScheme:...})`로 분기했다.
- scoped profile light/dark 모두 semantic/alias `1rem`, computed radius `16px`, profile primary 색 red가 일치한다.
- 새 chart 회귀는 위 A-P2-07의 전후 값을 얻었다.

## CI와 미실행

`gh run list --commit b241ed9dcdd198a62c820e039717aef74f86ef2e ...` 및 `gh run view 34166952061 --json status,conclusion,headSha,jobs,url`로 exact SHA를 확인했다. [CI run 34166952061](https://github.com/digitie/kor-travel-common/actions/runs/34166952061)은 completed/success, docs·packages·tools Windows·tools Ubuntu·secret-scan·check-versions 6개 job 모두 success다. CI 성공이 위 문서·실제 CSS 반례를 닫지는 않는다.

- NOT_RUN: T-103 대비/UX 도구 실제 실행(미구현), 소비자 build/e2e/6폭 visual, 실제 폰트 파일/glyph 로딩, 외부 LICENSE/merge SHA/CI evidence 실물 검사, npm/PyPI publish·release/tag.
- NOT_RUN: WSL 브라우저와 npm package gate, WSL 별도 secret/redaction 재실행. Windows package/Chromium 검증 및 WSL Python 전체 회귀를 분리해 기록했다.
- 모든 기존 raw와 상대 결과를 보존했다. 이 원본의 결과는 b241ed9에만 귀속하며 후속 변경을 포함하지 않는다.
