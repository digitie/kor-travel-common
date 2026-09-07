# T-104·T-020·T-021 독립 적대적 리뷰 B — post-fix

- 실행 ID: `B-T104-T020-T021-POSTFIX-20260908-073203`
- 판정: **BLOCK**. 기존 B-P1-01이 부분 수정 상태로 남는다. 기존 나머지 3건은 FIXED이며 신규 finding은 0건이다.
- 시작(KST): `2026-09-08T07:32:03.1809573+09:00`
- 검토 종료(KST): `2026-09-08T07:35:24.1496926+09:00`
- 실제 시작·종료 candidate: `b241ed9dcdd198a62c820e039717aef74f86ef2e`
- 실제 시작·종료 tree: `a6350aef9588eea9979a70c0edf356259376ab66`
- delta base: `7ffe525f8a6cfaef4ca4cbab7017306b1994f24a`
- 격리: `F:/dev/kor-travel-common-wt/review-t104-t020-t021-post-b`, 새 detached worktree. 시작·종료 `git status --porcelain=v1` 출력 없음.
- source `.git/config` 시작·종료 SHA256: `26B889B3EB290BA6E5A8BEAFE330E3CEAF47832CD202324162640DD12AD862D7`, 변경 없음.
- 상대 reviewer 원본·결과는 읽거나 요청하거나 공유하지 않았다. 후보·기존 보고서·소비자 파일 수정, commit, push는 수행하지 않았다. 작성 파일은 이 원본 하나다.

## 범위와 기준선

부모 요청에 따라 b241ed9를 full SHA로 해석하여 고정하고, [초기 B 원본](2026-09-08-t104-t020-t021-reviewer-b.md)의 네 finding과 `7ffe525..b241ed9` 변경 범위를 검토했다. [초기 manifest](2026-09-08-t104-t020-t021-manifest.md)는 초기 후보의 역사 기록이며, 이번 재검토 SHA는 부모의 새 요청으로 지정됐다. 초기 manifest의 실행 수치를 이번 실행으로 재사용하지 않았다.

전체 delta는 30개 경로다. 신규 manifest·초기 A/B 원본 3개를 제외한 변경 문서·패키지 계약을 확인했다. A 원본의 경로 존재만 보았고 내용은 열지 않았다. 이번 delta에는 문서뿐 아니라 `packages/tokens/shadcn.css`와 `packages/tokens/test/values.test.mjs` 변경이 포함된다. 이를 문서-only로 취급하지 않았다.

## 기존 finding disposition

| 초기 ID·심각도 | 판정 | 독립 재확인 |
|---|---|---|
| B-P1-01 / P1 | **부분 수정, 미해결** | license-only PR 분리와 T-021 소비자별 기록 표는 생겼지만, 요청서의 해제 조건은 여전히 후속 코드 채택 evidence를 요구한다. 아래 최소 재현 참조. |
| B-P2-02 / P2 | **FIXED** | T-453/T-454/T-485는 T-021 ktc 행을, T-472/T-473/T-486은 docker-manager 행을 소비한다. T-472/T-485의 `T-454/T-473 PR` 혼용이 제거됐다. |
| B-P2-03 / P2 | **FIXED** | T-021 구현·수용 기준이 결정/요청/evidence 형식까지로 명시되고 B4 실측은 후속 T-454 evidence로 이관됐다. 세 요청서에 해당 소비자 인벤토리와 이관 판정 링크가 추가됐다. 다만 요청서의 gate 본문 충돌은 B-P1-01에 포함한다. |
| B-P3-04 / P3 | **FIXED** | resume의 두 현재 수치가 모두 완료 20·열린 86으로 일치한다. 상세 task 직접 집계도 DONE 20, BLOCKED 79, READY 6, IN_PROGRESS 1, 합계 106이다. |

## 잔여 B-P1-01 — LICENSE-only PR의 해제 조건에 후행 evidence가 남아 있다

- 원 심각도 **P1** 유지. Disposition: **수정 후 같은 immutable 기준의 재검토 필요**.
- 주 위치: `docs/plan/requests/concierge-license-l8.md:26,30`, `docs/plan/requests/docker-manager-license-l8.md:26,30`.
- 관련 위치: concierge 요청서 `:17,22`, docker-manager 요청서 `:17,22`, `docs/tasks/T-021-ktc-ktdm-license-l8.md:26,69`, `docs/tasks/T-454-concierge-ui-v02.md:6,75`.

재현 명령은 요청서 두 파일을 행 번호와 함께 읽고 아래 조건을 대조하는 것이다.

```powershell
rg -n 'B4|해제 조건|T-454|T-473|코드 링크|외부 evidence' docs/plan/requests/concierge-license-l8.md docs/plan/requests/docker-manager-license-l8.md
rg -n 'B4|license-only|T-454|T-473' docs/tasks/T-021-ktc-ktdm-license-l8.md
rg -n '선행:|PR을 열지' docs/tasks/T-454-concierge-ui-v02.md
```

관찰한 최소 순차 반례:

1. concierge의 LICENSE·metadata·고지만 바꾸는 외부 PR이 머지됐다고 가정한다. 요청서 17행과 T-021 26행은 B4 diff를 후속 T-454 코드 채택 PR에서 수행하도록 한다.
2. 이제 요청서의 `해제 조건`을 평가하면 30행에서 **B4 diff 결과와 파일별 고지가 기록됨**을 요구한다. 선행 LICENSE-only PR을 마쳤어도 이 조건은 아직 충족되지 않는다.
3. B4를 기록하도록 지정된 T-454는 G-LIC 이전에는 PR을 열지 못한다. 즉 B4를 뒤로 이관한 문장과 L8 해제 조건을 함께 지키려면 순환이 다시 발생한다.
4. docker-manager도 17행에서는 이 PR에 common 코드 링크를 넣지 말라고 하지만 30행은 **common 코드 링크와 함께 필요한 provenance**를 해제 조건으로 유지한다. 그 항목이 LICENSE 변경 고지만 뜻하는지 후속 코드 채택 provenance인지 해제 조건에서 구분하지 않았다.

두 요청 22행은 새 T-021 행을 원장으로 지정하는 반면 26행은 기존 T-454/T-473 선행 evidence 위치를 그대로 지명한다. T-021 69행도 실제 LICENSE 반영을 T-454/T-473 evidence로 남긴다는 문장을 유지한다. 이는 소비자별 행 자체가 틀린 B-P2-02와 별개로, evidence 생산 시점과 정본 위치를 끝까지 정리하지 못한 같은 gate 충돌이다.

영향: 문서 전반의 의도는 license-only → T-021 evidence → 코드 채택으로 개선됐으나, 실행자가 해제 조건을 빠짐없이 검사하면 여전히 멈춘다. 반대로 앞 절만 믿고 통과시키면 해제 조건 일부를 임의로 무시한다. 계획 validator는 이 본문 순환을 확인하지 않는다.

최소 권고: 두 요청의 `해제 조건`을 license-only 산출물·검사와 T-021의 해당 소비자 행으로 통일한다. B4 및 코드 링크 provenance는 후속 코드 채택 조건으로 분리하고 G-LIC 해제 조건에서 제거한다. T-021 69행도 같은 기록 위치로 맞춘다. 실제 소비자 저장소를 이 작업에서 수정할 필요는 없다.

## 이번 실행 결과

| 명령·검사 | 결과 |
|---|---|
| `git rev-parse b241ed9 'b241ed9^{tree}'`, 시작·종료 HEAD/tree/status | 위 SHA/tree 일치, detached clean |
| `git diff --check 7ffe525 HEAD` | exit 0 |
| `git diff --exit-code 7ffe525 HEAD -- tools tests versions.json .github AGENTS.md` | exit 0. Python checker/시험·버전·workflow·AGENTS 불변 |
| `py -3.14 -B -X utf8 F:/dev/kor-travel-common/.git/codex-audit/review-t102-post-b-gates.py F:/dev/kor-travel-common-wt/review-t104-t020-t021-post-b` | 독립 임시 사본에서 정적 검사·focused 시험, exit 0 |
| plan / links | 상세 task 106 오류 0 / 문서 385개·로컬 대상 2,372개 오류 0 |
| SPDX / secrets / production redaction | 45개 오류 0 / 500개 발견·예외 0 / 500개 발견·예외 0 |
| `check_versions.py --self-check`, alias 검사 | exit 0 / CSS 1개 오류 0 |
| focused unittest | 35 tests, 0.978초, OK, skip 없음 |
| `npm run check --workspace packages/tokens` | 생성물 clean, exit 0 |
| `npm test --workspace packages/tokens` | 7 tests, 7 PASS, fail/skip 0 |
| Python 읽기 전용 CSS 블록 대조 | `:root`, `.dark`, `:where([data-kt-surface])` 각 alias 25개, 키와 var 참조 값 전부 일치 |
| Python 읽기 전용 요청 링크·상태 집계 | 세 요청 모두 인벤토리/판정 링크 존재, task 106개·완료 20개·열린 86개 |
| `gh run list --commit b241ed9dcdd198a62c820e039717aef74f86ef2e --limit 3 --json databaseId,headSha,status,conclusion,url` | exact candidate [run 34166952061](https://github.com/digitie/kor-travel-common/actions/runs/34166952061), completed/success |

CSS 대조의 첫 임시 정규식은 숫자 포함 chart 이름을 세지 못해 20개를 출력했다. `[a-z0-9-]`로 다시 대조해 chart 5개까지 포함한 최종 25개 결과를 확인했다. 후보 파일은 변경하지 않았다.

## 재사용·미실행과 경계

- 최초 Windows 전체 238 Python tests 성공은 Python 도구·시험 파일이 동일함을 확인하고 재사용한다. 이번에 238개를 새로 실행한 것으로 세지 않는다. 변경된 패키지는 위 7개 시험을 새로 실행했다.
- `NOT_RUN`: 이번 후보 WSL/Linux 로컬 시험, 브라우저 computed-style·소비자 build/e2e·시각 대비·외부 LICENSE/merge SHA 실측, tarball 설치·npm/PyPI 게시. CSS 정적 동등성과 정규식 기반 시험을 브라우저 검증으로 표시하지 않는다.
- GPL-3.0-or-later 결정, §7 추가 허가 없음, 기존 원천 고지, 소비자 쓰기 금지와 미게시 경계는 유지된다. T-021 두 소비자 행은 실제로 NOT_RUN/OPEN이며 외부 검증을 완료한 것으로 적지 않았다. pinvi 요청과 licensing의 실제 외부 반영 담당은 T-420이다.
- 현재 T-104는 IN_PROGRESS다. T-103 문구는 TK-8을 대비 쌍 정본으로 참조하도록 바뀌었으며, 도구 구현을 수행한 것처럼 표시하지 않는다.

새 finding은 없지만 B-P1-01이 완전히 닫히지 않았으므로 최종 판정은 **BLOCK**이다.
