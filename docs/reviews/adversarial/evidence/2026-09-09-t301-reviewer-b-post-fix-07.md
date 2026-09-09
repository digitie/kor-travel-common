# T-301 post-fix-07 B 원본 적대 리뷰

- Review ID: `T301-20260909-post-fix-07`
- 실행 ID: `T301-20260909-post-fix-07-B-20260909`
- 리뷰어: B — 문서·계약·parser·renderer·재현성
- 시작: 2026-09-09 (세션 진행분 포함, Asia/Seoul)
- 종료: 2026-09-09 (Asia/Seoul)
- 기준선(base): `afc8d1bf166d0ddcbee059252eb5cee245157dcd`
- 후보(commit): `1705a6a10954120b74e59d8611a520e7d9970605`
- 후보 tree: `c724361a4eac4c2b3697431e0d9a2baeb74a62ce`
- 입력 manifest: `docs/reviews/adversarial/evidence/2026-09-09-t301-post-fix-07-manifest.md`
- manifest SHA-256: `601680c947297bca5b3dcf9bc9b5708fba75ab08a9d5b1ea80c357112e15aca8`
- 격리: `F:/dev/kor-travel-common-review-b-t301-postfix07`의 detached worktree
- 상대 reviewer 결과와 통합 report: 읽지 않음
- 후보 파일 수정: 없음

## 범위와 판정

후보 전체 diff와 `docs/standards/openapi.md`, ADR-009/D-14, T-301 계약, `tools/openapi_exceptions.py`, 생성 Markdown/YAML, 회귀 시험, 후보 실행 evidence를 확인했다. 외부 소비자 저장소 build/e2e, npm/PyPI build·publish, GitHub Release, actionlint는 manifest가 정한 common 범위 밖이므로 `NOT_RUN(외부 저장소·게시 범위 밖)`이다.

최종 verdict는 **CONDITIONAL**이다.

- P0: 0건
- P1: 0건
- P2: 3건
- P3: 0건

P2-01~03을 수정하거나 owner·상세 task·검증 gate·목표 시점을 명시한 disposition으로 연결하고, 새 immutable 기준선에서 두 reviewer의 post-fix 재검토를 통과해야 PASS로 바꿀 수 있다.

## 기준선·clean 확인

다음 결과로 후보 object/tree와 detached 상태를 확인했다.

```text
git rev-parse HEAD
1705a6a10954120b74e59d8611a520e7d9970605

git rev-parse 'HEAD^{tree}'
c724361a4eac4c2b3697431e0d9a2baeb74a62ce

git status --porcelain=v1 --branch
## HEAD (no branch)
```

전달받은 manifest 파일의 SHA-256은 `601680c947297bca5b3dcf9bc9b5708fba75ab08a9d5b1ea80c357112e15aca8`로 일치했다. manifest는 candidate 외부의 immutable 입력으로 사용했다.

## 실행한 검증

| 명령 | 결과 |
|---|---|
| `python -B -X utf8 tools/openapi_exceptions.py --check` | exit 0; 예외 39건·Markdown 54줄 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_openapi_exceptions.py' -v` | exit 0; 31 tests OK |
| `npm ci` | exit 0; Node 25/npm 11에서 engine warning만 발생, 113 packages 설치 |
| `python -B -X utf8 -m unittest discover -s tests -p 'test_*.py' -q` | exit 0; 368 tests OK, 276.139초 |
| `python -B -X utf8 tools/validate_document_links.py .` | exit 0; 542 documents·2584 local targets, errors=0 |
| `python -B -X utf8 tools/validate_plan.py --root .` | exit 0; 상세 task 106, 오류 0 |
| `python -B -X utf8 tools/check_spdx.py --root .` | exit 0; 70 files, 오류 0 |
| `python -B -X utf8 tools/check_prod_redaction.py --root . --patterns .prod-redaction-patterns --all` | exit 0; 693 files, 발견 0 |
| `python -B -X utf8 tools/scan_secrets.py --root . --patterns .secret-scan-patterns --all` | exit 0; 693 files, 발견 0 |
| `git diff --check afc8d1bf166d0ddcbee059252eb5cee245157dcd 1705a6a10954120b74e59d8611a520e7d9970605 --` | exit 0 |
| `gh run list --repo digitie/kor-travel-common --commit 1705a6a10954120b74e59d8611a520e7d9970605` | docs `34308915146` success, selftest `34308915282` success |
| candidate check-runs | 12개 모두 candidate SHA 일치·completed·success |

처음 `node_modules`가 없는 새 worktree에서 full unittest를 실행했을 때는 MDX parser 의존성 부재로 exit 1(38 failures·3 errors)이었다. 이는 후보 코드 실패로 단정하지 않고 `npm ci` 후 동일 명령을 재실행했으며, 최종 368개가 모두 성공했다.

## 공격 시나리오와 통과한 경계

- PyYAML type oracle와 후보 parser를 비교한 8,623개 숫자·float·base·sexagesimal·timestamp 후보에서 non-string 수용 mismatch는 0건이었다.
- `0x_FF`, `0o_10`, `0b_10`, signed/short sexagesimal, short timezone timestamp, fractional timestamp는 거부됐다.
- YAML 예약 indicator `@`, backtick, 단독 `-`, `?`는 거부됐다.
- exact global surface `*`, `/*`, `/**`와 테스트된 underscore·한국어·점 접미사의 M10/동반 PR/task 변형은 거부됐다.
- BOM은 문서 시작에서만 허용되고, 내부 BOM 및 Cc/Cf/Zl/Zp 문자는 focused 시험에서 거부됐다.
- renderer에 schema·updated·apps·exceptions를 직접 변조해 넣은 네 가지 경우 모두 `RegistryError`로 거부됐다.
- T-301 task·resume·journal의 최신 post-fix-07 수치(31/368, 542/2584, 693/0)는 후보 실행 결과와 일치하며 post-fix-06 수치는 역사 문단으로 분리되어 stale current evidence는 재현되지 않았다.

## Findings

### B-P2-01 — exact 긍정 assertion이 질문형·불확정 괄호 내용을 허용

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:65-69`, 검증 사용부 `:493-495`; 정본 요구 `docs/standards/openapi.md:198`
- 근거: `EXTERNAL_CONTRACT_RE`는 `이다`/ `임` 뒤에 `?`·`:`·`!`를 허용하고, phrase 직후 `(`·`[`·`{`·`<`·backtick이 나오면 내부 내용을 전혀 검증하지 않고 positive assertion으로 인정한다.
- 재현:
  - canonical S1 reason에서 정상 assertion과 동반 증명을 제거하고 다음 reason을 넣어 `load_registry(..., as_of=date(2026,9,9))`를 실행했다.
  - 모두 `ACCEPT`였다.
    ```text
    소비하는 외부 계약이다? M10 동반 PR T-483
    소비하는 외부 계약임? M10 동반 PR T-483
    소비하는 외부 계약(아마) M10 동반 PR T-483
    소비하는 외부 계약(검증 중) M10 동반 PR T-483
    소비하는 외부 계약(계약미검증) M10 동반 PR T-483
    소비하는 외부 계약\`검토 중\` M10 동반 PR T-483
    ```
- 영향: 질문·가능성·검증 중인 설명이 exact positive external-contract assertion으로 통과한다. 정본이 요구하는 “부정·불확정 근거 허용 안 함”과 assertion 종결 계약을 자유 문자열로 우회한다.
- 권고: positive assertion을 자유 reason 검색이 아니라 구조화된 enum/boolean과 별도 evidence 필드로 검증한다. 현재 문법을 유지해야 한다면 `?`·`!`를 assertion 종결에서 제거하고, opening delimiter 뒤에는 허용된 인용/근거 grammar만 허용하며 arbitrary parenthetical text를 검사 없이 통과시키지 않는다.

### B-P2-02 — 불확정 자연어의 미포괄로 positive assertion을 우회

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:71-79`, 검증 사용부 `:493-495`; 정본 요구 `docs/standards/openapi.md:198`
- 근거: 확장된 `NEGATED_EVIDENCE_RE`가 많은 부정어를 처리하지만 자유 자연어의 불확정 표현 전체를 닫지는 못한다.
- 재현:
  - `소비하는 외부 계약이다. {표현} M10 동반 PR T-483` 형태로 reason을 만들고 registry를 load했다.
  - 다음 값이 모두 `ACCEPT`였다: `아마`, `검증되지`, `확인되지`, `존재하지`, `추정`, `maybe`, `perhaps`, `uncertain`, `unknown`, `unverified`, `pending`, `not_contract`, `no_contract`, `non‐contract`, `non–contract`.
- 영향: 새로운 한국어 활용형·영어 동의어·Unicode hyphen 변형만으로 계약 확정 여부를 모호하게 만들면서 positive assertion과 M10/동반 PR 증명을 통과할 수 있다. 목록을 계속 늘리는 방식은 닫힌 검증 계약이 아니다.
- 권고: 계약 여부·확정 상태·동반 변경 근거를 구조화된 필드와 검증 가능한 ID로 분리하고 reason은 설명용으로만 둔다. 구조화 전에는 허용 문장 grammar/allowlist를 두고 의문·추정·검증 상태·Unicode punctuation 회귀군을 함께 시험한다.

### B-P2-03 — Unicode combining mark가 M10·동반 PR·task exact token 경계를 우회

- 심각도: **P2**
- disposition: **OPEN**
- 위치: `tools/openapi_exceptions.py:44,82-83`, 검증 사용부 `:485-500`; 정본 요구 `docs/standards/openapi.md:198`
- 근거: 세 정규식은 `\w`를 identifier 경계로 사용하지만 Python의 `\w`가 combining mark(`Mn`)·variation selector를 identifier continuation으로 포함하지 않는다. `_validate_text`도 Cc/Cf/Zl/Zp만 거부하므로 `Mn`은 입력에 남을 수 있다.
- 재현:
  - canonical reason에 U+0301 combining acute accent를 각각 붙였다.
  - 결과:
    ```text
    M10\u0301 => ACCEPT
    동반 PR\u0301 => ACCEPT
    T-483\u0301 => ACCEPT
    ```
  - 문자열은 사람이 보는 token 뒤에 결합 문자가 붙어 있지만 exact token으로 판정된다.
- 영향: 시각적으로 구분하기 어려운 Unicode suffix로 교차 저장소 증명과 task provenance를 위조할 수 있다. 정본의 Unicode identifier/standalone token 경계와 parser가 서로 다른 토큰을 인정한다.
- 권고: token scanner에서 Unicode grapheme/combining mark를 명시적으로 처리하거나 evidence token 주변의 `Mn`·`Mc`·`Me`를 거부한다. 해당 클래스와 variation selector를 회귀 시험에 추가하고 task/M10/동반 PR에 동일 grammar를 적용한다.

## 결론

현재 candidate의 full/focused test, 문서 gate, CI, stale evidence 정합성, YAML 예약 indicator와 renderer semantic contract는 재현됐다. 그러나 exact positive assertion, 불확정 자연어, Unicode token boundary에 재현 가능한 P2가 남아 있어 PASS로 확정할 수 없다. 조건부 verdict는 **CONDITIONAL**이다.
