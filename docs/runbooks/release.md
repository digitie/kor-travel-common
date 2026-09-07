# 릴리스 Runbook (release)

이 문서는 common 패키지(tokens·ui·py)와 규칙 문서 버전을 발행하는 절차 정본이다(브리프 D-11·D-18·D-31, ADR-005). 확정 task는 T-007(문서 초기판)이며, 절차 1회 완주 검증은 T-501, 첫 실행은 T-109(`tokens-v0.1.0`)다. 패키지 실물이 생기기 전까지 §3의 빌드 명령은 후보다. 마지막 갱신 2026-09-06.

버전 정책의 규범은 [versions](../standards/versions.md), 배포 채널 결정은 ADR-005([ADR 색인](../adr/README.md)), 소비자 쪽 절차는 [consumer adoption](consumer-adoption.md), 일반 작업 절차는 [agent workflow](agent-workflow.md)를 따른다. 명령은 bash 기준이며 Git Bash에서 동일하다.

## 1. 버전 규칙(SemVer 0.x, D-31)

| 항목 | 규칙 |
|---|---|
| 독립 버전 | tokens·ui·py는 각각 독립 버전. ui는 `@kor-travel/tokens`의 호환 minor 하나를 peer로 요구 |
| minor(0.N.0) | 파괴 허용. `-rc.N` → 소비자 PR 검증 → 정식. CHANGELOG `#### Breaking` + 이관 절 필수 |
| patch(0.N.M) | 비파괴(additive)만. 토큰 값 조정·버그 수정·문서 |
| 파괴 항목 | 토큰 이름/의미, `data-slot`/`data-testid`, prop 기본값, 정렬 모드(`manualSorting`), CSS 파일 경로, 공개 export 제거, py 공개 시그니처 |
| 폐기 | 토큰 이름 폐기는 1 minor 동안 alias 유지 후 제거 |
| 소비자 범위 | 매니페스트·`package.json`은 `~0.N`(patch만 자동 허용) |
| 1.0 | GPL 소비자 3곳 채택 후 |
| 규칙 문서 | 태그 없음. CHANGELOG `### standards` 절과 각 문서 머리 "마지막 갱신"으로 추적. MUST 규칙 추가·변경은 소비자 이관 절과 예외 레지스트리 갱신을 동반 |

## 2. 태그·자산 규약(D-11)

| 패키지 | 태그 | Release 자산 | 소비자 설치 형태 |
|---|---|---|---|
| tokens | `tokens-vX.Y.Z`(rc: `tokens-vX.Y.Z-rc.N`) | `kor-travel-tokens-X.Y.Z.tgz`, `SHA256SUMS` | tarball URL + lock `integrity` |
| ui | `ui-vX.Y.Z` | `kor-travel-ui-X.Y.Z.tgz`, `SHA256SUMS` | tarball URL |
| py | `py-vX.Y.Z` | `kor_travel_common-X.Y.Z-py3-none-any.whl`, `kor_travel_common-X.Y.Z.tar.gz`, `SHA256SUMS` | `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common`(lock sha) 또는 wheel URL |
| 재사용 워크플로 | T-010에서 확정(후보 `workflows-vX.Y.Z`); 전까지 SHA 참조 | 없음 | `uses: …@<tag|sha>` |

- 태그는 불변이다. 태그 삭제 금지, 태그 이동 금지 — 잘못된 릴리스는 patch를 올려 다시 발행한다.
- 같은 버전 재발행 금지 — 한 번 발행한 `X.Y.Z`의 tarball·wheel을 다른 내용으로 다시 올리지 않는다(자산 교체도 재발행이다).
- `@main` 참조 금지 — 소비자의 `@main`·branch·`latest` 참조는 `check_versions.py`가 `FLOATING_REF`로 보고한다.
- 각 tarball·wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`를 동봉하고 `license: "GPL-3.0-or-later"` 필드(npm) / PEP 639 `license`·`license-files`(Python)를 둔다([licensing](../standards/licensing.md)).
- 자산 이름은 `npm pack` 산출 이름을 그대로 쓴다. 패키지 식별자는 [packages](../architecture/packages.md#1-요약표)에서 확정했다(ADR-014).
- npm/PyPI에는 게시하지 않는다. 계정·이름 확보 및 게시 재평가는 실행 계획에서 제외했다(ADR-014). 저장소 공개 범위(O-15)는 이 결정과 별개다.

### 2.1 common 후보 보존과 후속 구현

[ADR-014](../adr/014-common-implementation-without-registry-publishing.md)에 따라 common 검증 후보와 외부 릴리스를 구분한다. T-109a·T-212a·T-310a는 다음 순서로 0.1 후보를 보존한다.

1. 해당 구현·계약 task의 검증과 두 리뷰를 완료하고 PR을 병합한다. 패키지 소스·lock·툴체인·40자리 commit, 실행한 시험·pack/wheel 설치 결과를 후보 evidence에 연결한다.
2. 같은 source와 도구로 다시 빌드한 산출물의 SHA-256을 대조한다. 자산 이름·digest·CI artifact URL과 만료를 기록한다. 미실행·차이는 성공으로 적지 않는다.
3. 병합된 검증 commit에 불변 annotated tag `candidate-<pkg>-<X.Y.Z>-<N>`을 만들어 원격에 push한다. tag object와 peeled commit을 다시 조회해 기록한다. tag는 정식 Release·소비자 승인 표시가 아니다. 후보 수정에는 새 N과 재검증이 필요하다.
4. UI·Python의 다음 minor 구현은 보존 task가 DONE인 뒤 시작한다. 코드 추가 전에 UI metadata/lock을 `0.2.0-dev.0`, Python을 `0.2.0.dev0`로 변경한다. 초기 미발행 0.1.0의 로컬 pack을 정식 발행으로 세지 않는다. UI 스모크에서는 peer인 tokens도 common tarball 경로를 함께 설치한다.
5. CI artifact가 만료되면 보존 source에서 빌드·검증한다. 기존 digest와 다르면 기존 바이트를 재현했다고 기록하지 않는다. 새 후보 또는 새 rc와 필요한 검증으로 처리한다.

0.1 보존은 T-109a·T-212a·T-310a, UI 0.2 보존은 T-213a, Python 0.2 보존은 T-311의 준비 범위가 소유한다. 0.2 준비에서는 검증한 해당 minor의 전체 소스 commit으로 위 1~3을 실행해 `candidate-ui-0.2.0-<N>` 또는 `candidate-py-0.2.0-<N>`을 만든다. 0.1 후보나 release branch의 버전만 올려 대체하지 않는다. 이 준비도 미실행이면 성공으로 기록하지 않는다.

외부 릴리스는 해당 minor 후보에서 분기한 `codex/release-<pkg>-<X.Y>` 같은 별도 branch를 사용한다. 버전 변경은 그 branch를 base로 하는 준비 branch의 PR로 반영하고 리뷰·CI를 거친다. rc→정식 전환에서도 해당 release branch를 사용하며 main을 과거 버전으로 낮추지 않는다. 초기 branch ref 생성은 검증한 후보 commit을 가리키고 별도 소스 변경을 포함하지 않는다. §3의 버전·lock·자산별 릴리스 기록 변경과 tag 생성 대상은 이 release branch다. 현재 task 상태의 갱신은 §2.2의 main 문서 PR에서만 한다. 다음 minor 코드를 포함한 main에서 과거 버전 태그를 만들지 않는다.

T-010의 common fixture 성공과 T-010a의 실제 소비자 dispatch 성공은 별개다. 릴리스 task는 보존 후보·실제 소비자 검증과 자신의 모든 수용 기준이 닫혀야 DONE이다. 소비자 설치·빌드·PR은 해당 저장소에서 실행하며 common에서는 NOT_RUN/외부 선행으로 추적한다.

### 2.2 릴리스 소스와 현재 작업 원장의 연결

실행 상태의 정본은 현재 main의 `docs/tasks.md`·`docs/tasks-done.md`·상세 task·resume다. 과거 후보에서 분기한 release branch의 같은 파일은 당시의 스냅샷이며 현재 작업 선택·완료 판정에 사용하지 않는다. 후보 tag 생성 이후의 완료 기록 때문에 보존 tag를 이동하지 않는다.

1. 착수 때 현재 main의 40자리 commit을 고정하고, 그 commit의 상세 task·원장에서 모든 내부 선행 DONE과 외부 승인/실행 evidence를 대조한다. 현재 main의 상태 변경은 main 대상 작업 PR이 소유한다. 과거 branch의 BLOCKED를 근거 없이 DONE으로 바꾸거나 main 소스를 가져와 상태를 맞추지 않는다.
2. release 준비 PR에는 `docs/evidence/releases/<패키지>-<버전>.md`를 만든다. 후보 tag object/commit, 현재 main의 원장 commit, 선행 task별 evidence URL·commit, release PR base, 빌드·소비자 검증·digest를 연결한다. 준비 때 아직 없는 merge commit·발행 결과는 NOT_RUN으로 두고, 실행 뒤 4의 main 기록 PR에 채운다. 문서에 자기 commit hash를 미리 만들어 넣지 않는다. 원장 commit 이후 선행의 취소/실패가 생겼으면 발행 직전 새 main commit에서 다시 대조해 기록한다.
3. release branch에서는 그 evidence·해당 버전 CHANGELOG·패키지/lock 변경만 수행하고 task 원장·상세 metadata·resume는 역사 상태로 보존한다. 이 branch의 link·plan·패키지 CI는 그대로 통과해야 한다. 오래된 원장에서 릴리스 task만 DONE으로 바꾸어 선행 오류를 만드는 방식은 사용하지 않는다.
4. 실제 발행·검증 후 최신 main에서 문서 전용 branch/PR을 만든다. 해당 release evidence와 필요한 review 원본을 경로별로 가져오고, 완료 원장·상세 task·resume·journal 및 해당 버전 CHANGELOG 절을 현재 문서에 반영한다. 이 PR은 package·lock 변경을 포함하지 않는다. release branch 전체 merge/cherry-pick이나 main의 다음 minor 변경을 덮는 CHANGELOG 통째 복사는 하지 않는다. 코드 결함 수정의 main 이식이 필요하면 별도 구현 task/PR에서 현재 minor로 검증한다.
5. main 문서 PR에서 모든 선행 완료·발행 자산·필수 검증을 재확인한 뒤 릴리스 task를 DONE으로 옮기고 충족된 후속 task를 READY로 갱신한다. main의 link·plan·필수 CI가 통과하고 이 PR이 병합되어야 현재 실행 원장에서 종료된다. 발행은 끝났지만 기록 PR이 남으면 task는 IN_PROGRESS로 남긴다. 보존 source, release merge commit, main 완료 기록 commit은 서로 다른 참조로 기록한다.

## 3. 절차

### 3.1 준비

1. §2.2의 현재 main 원장으로 선행을 확인하고, 해당 minor의 보존 후보에서 release branch를 만든다. 버전 준비 PR의 base는 이 release branch다. PR 병합 뒤 실제 빌드할 merge commit을 고정하고 해당 commit의 필수 CI(`docs`·`tools`·해당 패키지·`secret-scan`)가 green인지 확인한다. release merge SHA의 CI 실행 경로는 [ci-deploy §9](../standards/ci-deploy.md#9-common-자체-ci)의 T-009·T-101·T-302가 구현한다. 그 전에는 NOT_RUN이며 PR head의 결과를 대신 사용하지 않는다. 비면제 변경은 2인 리뷰 report와 disposition이 닫혀 있어야 한다([agent workflow §5](agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰)).
2. `CHANGELOG.md` `## [Unreleased]`의 해당 패키지 절을 확인하고 minor면 `#### Breaking`과 이관 절이 있는지 본다.
3. release branch에서 준비 branch `codex/prepare-<pkg>-vX.Y.Z`를 만들어 버전을 올린다: `packages/<pkg>/package.json` `version`(정확 핀, D-07) 또는 `packages/py/kor-travel-common/pyproject.toml` `version`; 루트 `package-lock.json`·`uv.lock` 갱신을 같은 커밋에 넣는다.
4. rc는 npm `X.Y.Z-rc.N`, Python `X.Y.ZrcN` metadata를 사용한다. rc→정식도 새 준비 PR을 같은 release branch에 병합한 후 source·CI·자산을 다시 확인한다.

아래는 병합된 준비 PR의 source를 고정하는 bash 예시다. `RELEASE_PR`에는 이번 rc 또는 정식 준비 PR 번호, `RELEASE_BRANCH`에는 그 PR의 release base, `RELEASE_VERSION`에는 실제 패키지 metadata 버전, `CANDIDATE_TAG`·`CANDIDATE_SHA`에는 해당 minor 보존 evidence의 tag와 40자리 source를 설정한다. 정식 준비에서는 rc PR 값을 재사용하지 않는다. 필수 CI·리뷰·artifact source SHA 대조는 별도로 evidence에 기록한다.

```bash
: "${RELEASE_PR:?준비 PR 번호 필요}"
: "${RELEASE_BRANCH:?해당 minor release branch 필요}"
: "${RELEASE_VERSION:?이번 패키지 버전 필요}"
: "${CANDIDATE_TAG:?해당 minor의 보존 tag 필요}"
: "${CANDIDATE_SHA:?보존 evidence의 40자리 source 필요}"
[[ "$RELEASE_BRANCH" == codex/release-* ]] || exit 1
[[ "$CANDIDATE_SHA" =~ ^[0-9a-f]{40}$ ]] || exit 1
test -z "$(git status --porcelain=v1)" || exit 1
test "$(gh pr view "$RELEASE_PR" --json state --jq .state)" = MERGED || exit 1
test "$(gh pr view "$RELEASE_PR" --json baseRefName --jq .baseRefName)" = "$RELEASE_BRANCH" || exit 1
RELEASE_SHA=$(gh pr view "$RELEASE_PR" --json mergeCommit --jq .mergeCommit.oid)
[[ "$RELEASE_SHA" =~ ^[0-9a-f]{40}$ ]] || exit 1
git fetch origin "$RELEASE_BRANCH" "refs/tags/$CANDIDATE_TAG:refs/tags/$CANDIDATE_TAG" || exit 1
test "$(git cat-file -t "$CANDIDATE_TAG")" = tag || exit 1
test "$(git rev-parse "$CANDIDATE_TAG^{commit}")" = "$CANDIDATE_SHA" || exit 1
git merge-base --is-ancestor "$CANDIDATE_SHA" "$RELEASE_SHA" || exit 1
git merge-base --is-ancestor "$RELEASE_SHA" "origin/$RELEASE_BRANCH" || exit 1
git switch --detach "$RELEASE_SHA" || exit 1
test "$(git rev-parse HEAD)" = "$RELEASE_SHA" || exit 1
```

이 commit에서 §3.2를 수행하고 package metadata가 `RELEASE_VERSION`과 같은지 확인한다. 자산 파일명·digest도 이번 빌드 evidence와 대조한다. 다음 예시의 `0.1.0` 파일명은 rc면 `0.1.0-rc.1`(Python `0.1.0rc1`) 등 실제 버전으로 치환하며 기존 dist의 다른 버전 파일을 발행하지 않는다.

### 3.2 빌드·검증(common)

```bash
cd /mnt/f/dev/kor-travel-common
npm ci
npm run build --workspace packages/tokens
npm test --workspace packages/tokens
mkdir -p dist/release
npm pack --workspace packages/tokens --pack-destination dist/release
tar -tzf dist/release/kor-travel-tokens-0.1.0.tgz | grep -E '^package/(LICENSE|NOTICE|THIRD_PARTY_NOTICES\.md|package\.json|tokens\.css|theme\.css)$'
```

tarball 설치 스모크는 저장소 밖 임시 디렉터리에서 한다.

```bash
TMP=$(mktemp -d)
( cd "$TMP" && npm init -y >/dev/null && npm install /mnt/f/dev/kor-travel-common/dist/release/kor-travel-tokens-0.1.0.tgz \
  && node -e "require.resolve('@kor-travel/tokens/theme.css'); console.log('ok')" )
```

Python:

```bash
cd packages/py/kor-travel-common
uv sync --locked
uv run pytest
uv build --out-dir ../../../dist/release
cd ../../..
python3 -m venv "$TMP/venv" && "$TMP/venv/bin/pip" install dist/release/kor_travel_common-0.1.0-py3-none-any.whl \
  && "$TMP/venv/bin/python" -c "import kortravelcommon; print(kortravelcommon.__version__)"
```

체크섬:

```bash
( cd dist/release && sha256sum kor-travel-tokens-0.1.0.tgz > SHA256SUMS && cat SHA256SUMS )
```

- `dist/`는 gitignore 대상이다. 자산은 Release에만 올리고 커밋하지 않는다.
- CI `packages`·`python-package` job이 같은 빌드·설치 검사를 수행한다. 로컬 결과와 CI 결과가 다르면 CI(ubuntu)가 정본이다(D-03).
- ui 릴리스는 `consumer-smoke`(webpack·Turbopack 양쪽 `next build`)를 rc 단계에서 반드시 실행한다(D-10).
- 스크립트 이름·`--workspace` 경로는 T-101·T-201·T-302 산출물과 대조해 확정한다.

### 3.3 rc 발행

태그·push·원격 source 대조·발행은 순서대로 실행하며 하나라도 실패하면 뒤 단계를 실행하지 않는다. 아래 tokens 예시를 ui/py의 패키지·버전·자산 이름으로 치환한다. 중복 발행 명령을 각 task에 별도로 유지하지 않는다.

```bash
test "$(git rev-parse HEAD)" = "$RELEASE_SHA" || exit 1
test "$(node -p "require('./packages/tokens/package.json').version")" = "0.1.0-rc.1" || exit 1
git tag -a tokens-v0.1.0-rc.1 "$RELEASE_SHA" -m "tokens v0.1.0-rc.1" || exit 1
git push origin tokens-v0.1.0-rc.1 || exit 1
REMOTE_RELEASE_SHA=$(git ls-remote --tags origin 'refs/tags/tokens-v0.1.0-rc.1^{}' | awk '{print $1}')
test "$REMOTE_RELEASE_SHA" = "$RELEASE_SHA" || exit 1
gh release create tokens-v0.1.0-rc.1 --verify-tag --prerelease \
  --title "tokens v0.1.0-rc.1" --notes-file dist/release/notes.md \
  dist/release/kor-travel-tokens-0.1.0-rc.1.tgz dist/release/SHA256SUMS || exit 1
gh release view tokens-v0.1.0-rc.1 --json assets --jq '.assets[].name' || exit 1
```

`notes.md`에는 CHANGELOG 해당 절 사본, 자산 digest, 검증한 소비자·commit, 알려진 제한(`NOT_RUN` 포함)을 적는다. 릴리스 노트는 CHANGELOG의 정본이 아니다.

### 3.4 소비자 검증

1. `gh workflow run consumer-smoke.yml -f tag=tokens-v0.1.0-rc.1`로 패키지별 승인된 pinned SHA 소비자 빌드를 돌린다(T-010 후).
2. 1차 소비자에서 실제 채택 PR을 연다([consumer adoption](consumer-adoption.md)): tokens는 map + weather, ui는 map + pinvi admin(L6) 또는 airport 소형 부품, py는 map-api·weather-api·airport(D-16).
3. 통과 조건: 소비자 빌드 green(webpack·Turbopack), 6폭 시각 diff 0(값 무변경 릴리스) 또는 의도 목록, e2e green, `check_versions` report 위반 0, 소비자 lock에 tarball `resolved` URL과 `integrity`가 기록됨.

```bash
# 소비자 저장소에서: lock 항목의 resolved가 Release 자산 URL이고 integrity가 있는지 확인
python3 - <<'EOF'
import json
lock = json.load(open("package-lock.json", encoding="utf-8"))
for name, pkg in lock["packages"].items():
    if name.endswith("node_modules/@kor-travel/tokens"):
        print(name, pkg.get("version"), pkg.get("resolved"), "integrity" in pkg)
EOF
uv lock --check   # Python: lock이 pyproject와 일치하고 sha가 고정됐는지
```
4. rc가 실패하면 rc 태그는 그대로 두고 수정 후 `-rc.2`를 낸다. 소비자 PR은 정식 태그로 바꾼 뒤 merge한다.

### 3.5 정식 발행

```bash
# 같은 release branch의 정식 준비 PR 병합 → §3.1로 새 RELEASE_SHA 확인 → §3.2 재실행
# 필수 CI·고지·설치·digest를 확인한 그 정식 commit을 지정한다.
test "$(git rev-parse HEAD)" = "$RELEASE_SHA" || exit 1
test "$(node -p "require('./packages/tokens/package.json').version")" = "0.1.0" || exit 1
git tag -a tokens-v0.1.0 "$RELEASE_SHA" -m "tokens v0.1.0" || exit 1
git push origin tokens-v0.1.0 || exit 1
REMOTE_RELEASE_SHA=$(git ls-remote --tags origin 'refs/tags/tokens-v0.1.0^{}' | awk '{print $1}')
test "$REMOTE_RELEASE_SHA" = "$RELEASE_SHA" || exit 1
gh release create tokens-v0.1.0 --verify-tag --title "tokens v0.1.0" --notes-file dist/release/notes.md \
  dist/release/kor-travel-tokens-0.1.0.tgz dist/release/SHA256SUMS || exit 1
gh release view tokens-v0.1.0 --json tagName,isPrerelease,assets || exit 1
```

정식 자산은 rc에서 검증한 코드와 같고 버전 metadata·lock·릴리스 기록만 전환한 source에서 다시 빌드한다. 코드가 다르면 새 rc와 소비자 재검증이 필요하다. 발행 뒤 원격 annotated tag object·peeled commit이 기록한 RELEASE_SHA와 일치하는지 확인하고, 내려받은 자산의 digest를 빌드 evidence와 대조한다.

### 3.6 후속 기록

현재 실행 기록은 §2.2의 **main 대상 문서 전용 PR**으로 반영한다. 아래 표는 갱신 책임이며 과거 release branch의 원장 상태를 바꾸라는 뜻이 아니다. versions·pins의 정책/입력 변경이 필요한 경우에는 완료 기록과 분리된 검증 PR로 수행한다.

| 기록 | 내용 |
|---|---|
| `CHANGELOG.md` | `[Unreleased]`의 해당 패키지 절을 `## [tokens-v0.1.0] - YYYY-MM-DD`로 옮긴다(다른 패키지 절은 `[Unreleased]`에 남긴다) |
| `docs/standards/versions.md`·`versions.json` | common 패키지 버전 표와 소비자 `recommended`가 있으면 갱신 |
| `consumers.pins.json`·`docs/integration-map.md` | 소비자 PR merge 뒤 SHA 갱신 + `collect_manifests.py` 재생성(T-012) |
| `docs/resume.md`·`docs/journal.md` | 릴리스 commit·태그·digest·검증한 소비자·`NOT_RUN` |
| task | T-109·T-212·T-213·T-310 등 릴리스 task의 evidence에 `gh release view` 출력과 digest |
| ADR | 배포 채널·버전 정책이 바뀌면 새 ADR(ADR-005 supersede) |

## 4. 회귀 시 되돌리기

- 태그·자산은 삭제·이동하지 않는다. 회수가 필요하면 릴리스 노트 맨 위에 `회수(superseded by tokens-vX.Y.Z+1)`를 적고 `versions.json` `blocked[]`에 해당 버전을 등록해 `check_versions.py`가 `BLOCKED`로 보고하게 한다.
- 수정은 fix-forward patch(`X.Y.Z+1`)로 낸다. 파괴적 원복이 필요하면 minor를 올리고 이관 절을 쓴다.
- 소비자는 채택 PR을 1회 revert하고 lock을 동반한다([consumer adoption §8](consumer-adoption.md#8-되돌리기)).
- 릴리스 뒤 소비자 e2e·시각 diff·배포 스모크가 실패하면 원인이 common 산출물인지 앱 변경인지 evidence로 가르고, common 원인이면 patch 발행 전까지 `docs/resume.md` 차단 조건에 올린다.
- rc 단계 실패는 되돌리기가 아니라 `-rc.N+1`이다.

## 5. 체크리스트

| # | 항목 | 확인 |
|---|---|---|
| 1 | 현재 main 선행 확인, 해당 minor release base의 준비 PR 병합·source SHA/CI 확인, 비면제 변경의 2인 리뷰 닫힘 | |
| 2 | 버전 문자열·lock 갱신 커밋(rc면 `-rc.N`) | |
| 3 | 빌드·단위·tarball(또는 wheel) 설치 스모크 통과, `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉 확인 | |
| 4 | `SHA256SUMS` 생성, 자산 이름이 §2와 일치 | |
| 5 | rc 태그·pre-release 발행, `consumer-smoke` + 1차 소비자 PR 검증 | |
| 6 | 정식 태그·Release 발행, `gh release view`로 자산 확인 | |
| 7 | main 문서 PR의 CHANGELOG·resume·journal·task evidence 반영과 후속 READY 확인; 필요한 versions·pins 변경은 별도 검증 PR | |
| 8 | 미실행 검증은 `NOT_RUN(사유)`로 릴리스 노트와 task에 기록 | |

### 패키지별 소비자 스모크 선택

[ADR-013](../adr/013-package-release-execution-contract.md)에 따라 tokens는 map·weather, UI는 map·pinvi admin(L6 완료) 또는 airport의 승인된 범위를 `consumers.pins.json`에 패키지별 기록한다. pinvi의 L6가 완료되기 전에는 pinvi에 common 자산을 설치하지 않는다. 도구·자산·승인 대상이 없으면 NOT_RUN과 gate 미완료이며 설치 생략을 green으로 세지 않는다. Python 0.2 발행 책임은 [T-311](../tasks/T-311-py-v0-2-0-release.md)에 둔다.
