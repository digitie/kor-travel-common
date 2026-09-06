# ADR-005: 배포 채널(GitHub Release tarball·git 태그·wheel)·태그 불변·SemVer 0.x

- 상태: accepted — 패키지명은 잠정(O-5), 공개 npm/PyPI 게시는 Phase 5 재평가
- 날짜: 2026-09-06
- 근거 문서: `docs/plan/design-brief.md` D-11·D-31·D-33·O-5·O-15·O-18, `docs/survey/cross/backend.md` §5.1·§5.2, `docs/survey/cross/version-matrix.md` §7.1·§7.4, `docs/survey/cross/licensing.md` §3.3·§3.5, 선행 보고서(geo `docs/kor-travel-common-library-review.md`) §8

## 컨텍스트

7개 저장소 어디에도 사내 패키지 index·Renovate·dependabot이 없고, Python provider 라이브러리는 `git+https://…@<sha>` 핀이 관례이며(kta 2·map 14·ktw 1), pinvi etl만 `@main`을 참조해 재현 불가 핀을 남겼다(`be` §5.1). npm 쪽은 map이 정확 핀 + 검증 스크립트, pinvi가 lock 무결성 검사를 쓴다(`vm` §7.1). 선행 보고서 §8은 "이동 브랜치 직접 참조 금지·명시 버전과 lockfile"을 요구했다. common은 tokens·ui·py 세 코드 패키지를 독립 주기로 내야 하고, 0.x 동안 토큰 이름·마크업 계약이 바뀔 수 있다.

## 결정

1. npm 채널은 GitHub Release 자산 tarball이다: 태그 `tokens-vX.Y.Z`·`ui-vX.Y.Z`, 자산 `kor-travel-<pkg>-X.Y.Z.tgz` + `SHA256SUMS`. 소비자는 tarball URL로 설치하고 `package-lock.json`의 `integrity`로 고정한다.
2. Python 채널은 git 태그 `py-vX.Y.Z` + wheel 자산 병행이다. 소비자는 `git+https://github.com/digitie/kor-travel-common.git@py-vX.Y.Z#subdirectory=packages/py/kor-travel-common`을 선언하고 `uv.lock`의 sha로 고정한다. Docker 빌드 스테이지에 `git`이 없으면 wheel 자산 URL 방식을 쓴다.
3. 태그는 불변이고 같은 버전 재발행을 금지하며 `@main` 참조를 금지한다(`check_versions` `FLOATING_REF`).
4. SemVer 0.x: minor = 파괴 허용(`-rc.N` → 소비자 PR 검증 → 정식, `CHANGELOG.md` `### Breaking` + 이관 절 필수), patch = 비파괴(additive). 파괴 항목은 토큰 이름/의미·data-slot/testid·prop 기본값·정렬 모드·CSS 파일 경로다. 토큰 이름 폐기는 1 minor 동안 alias를 유지한다. tokens·ui·py는 독립 버전이고 ui는 `@kor-travel/tokens` 같은 minor를 peer로 요구한다. 소비자 범위는 `~0.N`. 1.0은 GPL 소비자 3곳 채택 후다.
5. 각 tarball·wheel에 `LICENSE`·`NOTICE`·`THIRD_PARTY_NOTICES.md`를 동봉하고 `license: "GPL-3.0-or-later"` 필드(PEP 639 `license-files`)를 둔다.
6. common 자체 툴체인: 루트 `package.json` `workspaces: ["packages/*"]`, `packageManager: "npm@11.19.1"`, `engines.node ^22.12.0`, `.nvmrc 22.23.1`, 루트 `package-lock.json` 커밋, CI `npm install -g npm@11.19.1` 후 `npm ci`; Python은 `uv` + `packages/py/.../uv.lock`. `CHANGELOG.md`는 단일 파일에 패키지별 H3.
7. 공개 npm/PyPI 게시·Renovate는 Phase 5(T-507)에서 재평가한다. 전까지 자동 갱신은 `templates/dependabot.yml`로 보조한다. 전제는 common 저장소 공개(O-15).

## 대안 검토

- **공개 npm/PyPI 즉시 게시**: 소비자 설치가 가장 단순하지만 scope 확보(T-006)·게시 권한·회수 불가 게시 사고 위험이 있고, 소비자가 아직 없다. tarball 선행으로 비용 0에 개명 여지를 남겼다.
- **로컬 path/editable·서브모듈**: 개발 편의는 높지만 CI/Docker에서 COPY 경로 결합이 생겨 독립 CI에서 재현되지 않는다(선행 보고서 §6, ktw airkorea·geo dagster 방식).
- **사내 PyPI 호환 index**: 인프라·인증·가용성 운영 비용이 크고 어느 앱도 쓰지 않는다.
- **0.x에서도 minor 비파괴**: 초기 계약 변경이 잦아 major가 빠르게 올라가고 의미가 없어진다. rc + 소비자 PR 검증으로 파괴 minor의 위험을 흡수한다.

## 결과

- 소비자는 lock의 `integrity`/sha로 재현 가능한 설치를 갖고, 이동 참조는 report에서 즉시 드러난다.
- 릴리스마다 태그·자산·`SHA256SUMS`·CHANGELOG를 만드는 절차가 필요하며 runbook 1회 완주 검증(T-501)이 gate다.
- 파괴 minor는 소비자 PR을 동반하므로 릴리스 리드타임이 길어진다. 대신 1.0 전 계약 수정 여지를 남긴다.
- npm scope 실패 시 개명은 첫 소비자 PR 전이면 비용 0이지만 그 뒤에는 소비자 lock 갱신을 동반한다.

## 후속·적용 위치

- 절차: `docs/runbooks/release.md`(T-007), `CHANGELOG.md`
- 현재 설계: `docs/architecture/README.md` §4, `docs/architecture/packages.md` §1
- 외부 확인: T-006(scope·PyPI 이름), O-15(공개 여부)
- 릴리스 task: T-109(tokens v0.1.0), T-212·T-213(ui), T-310(py), T-501(완주 검증), T-507(공개 게시 재평가)
