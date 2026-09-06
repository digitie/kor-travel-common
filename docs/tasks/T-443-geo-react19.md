# T-443 geo: React 19 업그레이드(ADR-019 갱신, 별도 PR, 실검증)

- 상태: BLOCKED
- 우선순위: P2
- Gate: unit 43·e2e 23
- 선행: T-440
- 외부 선행: 사용자 O-25 승인(geo ADR-019 갱신 결정, geo 소유)

## 목표

geo-ui를 React 18.3.1에서 19.2.x로 올린다. geo ADR-019는 "Next 16 peer 범위가 허용하는 18.3.1 유지"만 근거이고 적극적 차단 사유 문서가 없으므로, 새 ADR(또는 ADR-019 갱신)로 결정을 남기고 별도 PR에서 실검증한다. `@kor-travel/ui`는 React 19 전용이라 이 task가 T-444의 전제다.

## 고정 결정

- [design-brief](../plan/design-brief.md) D-06(React floor 19.0·recommended 19.2.8; geo·ktdm 18.3.1은 Phase 4 전 예외)·D-09(ui는 React 19 전용, ref prop·forwardRef 없음)·D-24(프레임워크 업그레이드 PR 분리)·O-25(승인 기본값, ADR-019 갱신·별도 PR·실검증).
- ADR-007·ADR-008 — [ADR 색인](../adr/README.md). 정본: [versions](../standards/versions.md), [frontend-stack](../standards/frontend-stack.md).
- 사실: ADR-019(2026-05-23) React 18 유지 근거, `button.tsx` 주석 "React 18에서는 radix Trigger asChild가 ref를 넘기므로 forwardRef 필수", `zod ^4.4.3` 직접 의존(ADR-020, React 18 peer 정합), jsdom 25, lucide 0.468; React 19 breaking(forwardRef 불필요·`propTypes`·`defaultProps` 제거·`react-test-renderer` deprecated) — [inv/geo §3.1·§9·§11-1](../survey/inventory/kor-travel-geo.md), [vm §5.2·§5.3](../survey/cross/version-matrix.md).
- PR 순서: [judge-migration-feasibility §3.1 geo #3](../plan/design-panel/judge-migration-feasibility.md).

## 구현 범위

- geo `docs/adr/`에 "React 19 채택(ADR-019 부분 대체)" ADR 추가(사용자 승인 원문 인용), ADR-019 상태를 `partially superseded by ADR-NNN`으로.
- `kor-travel-geo-ui/package.json`: react/react-dom 19.2.x, `@types/react`·`@types/react-dom` 19, jsdom 30, `@testing-library/react` 호환 버전; radix-ui 1.6.0은 React 19 peer 허용 범위 확인 후 유지(교체는 T-444).
- 코드: `forwardRef` 제거는 하지 않는다(radix `asChild` 경로가 여전히 ref를 넘김; T-444에서 base-ui `render`로 정리). `defaultProps`·string ref 사용처 grep 후 0건 확인 또는 수정.
- `versions.json` geo React 예외 제거(common 후속 PR).

## 범위 밖

radix → base-ui(T-444), Next 16.3 minor 상향(별도), lucide 1.x(T-507 재평가 후), Python 측.

## 대상 저장소·브랜치·PR·되돌리기

- `digitie/kor-travel-geo`, 브랜치 `agent/<agent>-T-443-react19`, `origin/main`에서 분기. PR 1개(ADR + lock 동반).
- 되돌리기 = `git revert <merge-sha>` + `npm ci`; ADR은 revert되지 않도록 별도 커밋으로 분리하고 상태만 `superseded`로 갱신(결정 기록 삭제 금지, R2.6).

## 예상 변경 파일

아래는 이 task가 만들거나 고칠 예정 경로다. 예정 경로는 존재·실행 증거가 아니다.

```text
docs/adr/019-*.md(상태 갱신), docs/adr/NNN-react-19.md
kor-travel-geo-ui/package.json, kor-travel-geo-ui/package-lock.json
kor-travel-geo-ui/tests/setup.ts                 # jsdom 30 호환 시
kor-travel-geo-ui/components/**                   # defaultProps 등 0건 확인, 최소 수정
kor-travel-common: versions.json                  # 예외 제거
```

## 수용 기준

- [ ] `npm ls react react-dom`이 19.2.x 단일 버전이고 peer 경고 0(`npm ls --all` problems 0).
- [ ] unit 43 파일(204~210 tests 수준, 실측치 기록) green, e2e 23 + a11y 4 spec green, `next build` green.
- [ ] 6폭 스크린샷 diff 0(React 상향으로 diff가 나면 원인 기록; 토큰 diff와 혼동 금지).
- [ ] geo ADR에 사용자 승인 일자·범위가 있고 ADR-019 상태가 갱신됐다.
- [ ] `check_versions` geo React 행 `OK`, 예외 제거 common PR 링크.

## 검증 명령

```bash
# kor-travel-geo/kor-travel-geo-ui (Linux)
npm ci && npm ls react react-dom @types/react --depth=0 && npm ls --all >/dev/null
npm run lint && npm run type-check && npm test && npm run build
PLAYWRIGHT_MOCK_LOGIN=1 npm run test:e2e
grep -rn 'defaultProps\|propTypes\|createFactory' components lib app | wc -l   # 0 예상
# kor-travel-common
python3 -B -X utf8 tools/check_versions.py --manifest ../kor-travel-geo/kor-travel-geo-ui/kor-travel-common.lock.json
```

## evidence

PR URL·CI run·테스트 수·ADR 링크를 이 파일 "실행 기록"·`docs/journal.md`에. 승인 전에는 `NOT_RUN(O-25 미승인)`.

## rollback·release 차단 조건

- peer 경고·e2e red·원인 불명 diff면 머지 금지; 머지 후 회귀 시 revert 1회(T-444 미착수 상태여야 함).
- 사용자가 O-25를 거부하면 이 task는 취소되고 geo는 tokens까지만 소비(T-444 취소, D-16 "React 18 앱은 tokens부터").
