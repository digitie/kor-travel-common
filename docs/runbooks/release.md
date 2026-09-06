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
3. 병합된 검증 commit에 불변 annotated tag `candidate-<pkg>-0.1.0-<N>`을 만들어 원격에 push한다. tag object와 peeled commit을 다시 조회해 기록한다. tag는 정식 Release·소비자 승인 표시가 아니다. 후보 수정에는 새 N과 재검증이 필요하다.
4. UI·Python의 다음 minor 구현은 보존 task가 DONE인 뒤 시작한다. 코드 추가 전에 UI metadata/lock을 `0.2.0-dev.0`, Python을 `0.2.0.dev0`로 변경한다. 초기 미발행 0.1.0의 로컬 pack을 정식 발행으로 세지 않는다. UI 스모크에서는 peer인 tokens도 common tarball 경로를 함께 설치한다.
5. CI artifact가 만료되면 보존 source에서 빌드·검증한다. 기존 digest와 다르면 기존 바이트를 재현했다고 기록하지 않는다. 새 후보 또는 새 rc와 필요한 검증으로 처리한다.

외부 릴리스는 후보에서 분기한 `codex/release-<pkg>-0.1` 같은 별도 branch를 사용한다. 버전 변경은 그 branch를 base로 하는 준비 branch의 PR로 반영하고 리뷰·CI를 거친다. rc→정식 전환에서도 해당 release branch를 사용하며 main을 과거 버전으로 낮추지 않는다. 초기 branch ref 생성은 검증한 후보 commit을 가리키고 별도 소스 변경을 포함하지 않는다. §3의 버전·lock·릴리스 기록 변경과 tag 생성 대상은 이 release branch다. 다음 minor 코드를 포함한 main에서 과거 버전 태그를 만들지 않는다.

T-010의 common fixture 성공과 T-010a의 실제 소비자 dispatch 성공은 별개다. 릴리스 task는 보존 후보·실제 소비자 검증과 자신의 모든 수용 기준이 닫혀야 DONE이다. 소비자 설치·빌드·PR은 해당 저장소에서 실행하며 common에서는 NOT_RUN/외부 선행으로 추적한다.

## 3. 절차

### 3.1 준비

1. 릴리스 대상 변경이 모두 `main`에 merge되어 있고 CI(`docs`·`tools`·`packages`·`python-package`·`secret-scan`)가 green인지 확인한다. 비면제 변경은 2인 리뷰 report와 disposition이 닫혀 있어야 한다([agent workflow §5](agent-workflow.md#5-전문-리뷰어-서브에이전트-2인-적대적-리뷰)).
2. `CHANGELOG.md` `## [Unreleased]`의 해당 패키지 절을 확인하고 minor면 `#### Breaking`과 이관 절이 있는지 본다.
3. 릴리스 브랜치 `agent/<agent>-release-<pkg>-vX.Y.Z`를 만들어 버전을 올린다: `packages/<pkg>/package.json` `version`(정확 핀, D-07) 또는 `packages/py/kor-travel-common/pyproject.toml` `version`; 루트 `package-lock.json`·`uv.lock` 갱신을 같은 커밋에 넣는다.
4. rc는 버전 문자열 자체를 `X.Y.Z-rc.N`으로 둔다(tarball 이름이 rc를 포함해야 정식과 구분된다).

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

```bash
git tag -a tokens-v0.1.0-rc.1 -m "tokens v0.1.0-rc.1"
git push origin tokens-v0.1.0-rc.1
gh release create tokens-v0.1.0-rc.1 --prerelease \
  --title "tokens v0.1.0-rc.1" --notes-file dist/release/notes.md \
  dist/release/kor-travel-tokens-0.1.0-rc.1.tgz dist/release/SHA256SUMS
gh release view tokens-v0.1.0-rc.1 --json assets --jq '.assets[].name'
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
# 버전 문자열에서 -rc.N 제거 → lock 갱신 → §3.2 재실행 → merge 후 main에서
git switch main && git pull --ff-only origin main
git tag -a tokens-v0.1.0 -m "tokens v0.1.0"
git push origin tokens-v0.1.0
gh release create tokens-v0.1.0 --title "tokens v0.1.0" --notes-file dist/release/notes.md \
  dist/release/kor-travel-tokens-0.1.0.tgz dist/release/SHA256SUMS
gh release view tokens-v0.1.0 --json tagName,isPrerelease,assets
```

정식 자산은 rc에서 검증한 commit과 같은 소스로 다시 빌드한 것이어야 하며, 다르면 rc를 다시 낸다.

### 3.6 후속 기록

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
| 1 | `main` merge 완료, CI green, 비면제 변경의 2인 리뷰 닫힘 | |
| 2 | 버전 문자열·lock 갱신 커밋(rc면 `-rc.N`) | |
| 3 | 빌드·단위·tarball(또는 wheel) 설치 스모크 통과, `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md` 동봉 확인 | |
| 4 | `SHA256SUMS` 생성, 자산 이름이 §2와 일치 | |
| 5 | rc 태그·pre-release 발행, `consumer-smoke` + 1차 소비자 PR 검증 | |
| 6 | 정식 태그·Release 발행, `gh release view`로 자산 확인 | |
| 7 | CHANGELOG 절 이동, versions·pins·integration-map·resume·journal·task evidence 갱신 | |
| 8 | 미실행 검증은 `NOT_RUN(사유)`로 릴리스 노트와 task에 기록 | |

### 패키지별 소비자 스모크 선택

[ADR-013](../adr/013-package-release-execution-contract.md)에 따라 tokens는 map·weather, UI는 map·pinvi admin(L6 완료) 또는 airport의 승인된 범위를 `consumers.pins.json`에 패키지별 기록한다. pinvi의 L6가 완료되기 전에는 pinvi에 common 자산을 설치하지 않는다. 도구·자산·승인 대상이 없으면 NOT_RUN과 gate 미완료이며 설치 생략을 green으로 세지 않는다. Python 0.2 발행 책임은 [T-311](../tasks/T-311-py-v0-2-0-release.md)에 둔다.
