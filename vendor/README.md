# 공통 CSS 빌드 의존성의 원본과 고지

이 디렉터리의 Lightning CSS tarball은 2026-11-11 사용자 승인에 따라 웹·모바일이 같은 bytes를 소비하기 위한 빌드/개발 의존성이다. common 제품 소스로 추출하거나 npm tarball을 재포장하지 않는다. 정확 버전의 정본은 [versions.json](../versions.json), 파일명·SHA512의 정본은 [frontend-artifacts.json](../frontend-artifacts.json)이다.

## 고정 출처

- 상류: [parcel-bundler/lightningcss](https://github.com/parcel-bundler/lightningcss/tree/1d680fa14e9a089c92dc0929f869d6757ae91c30), npm 1.33.0의 gitHead.
- 원본 수정: [digitie/lightningcss PR1](https://github.com/digitie/lightningcss/pull/1)의 fix.4 source 1e94372a6da4a55eac4a6dc3ff9cdeec103e8ac1.
- serde-content 원본: [rushmorem/serde-content](https://github.com/rushmorem/serde-content/tree/bb5066da57fb0d76a981dbbef04b68f2aff90a3f), 수정 source 67fe4a9c5b4595433a731b70dbe31412721bea8c.
- native/raw WASM은 Rust/Cargo/vendor 입력 digest가 같은 684c528 빌드에서 재사용한다. 현재 JS helper로 adapter를 다시 번들했으며 source gate가 checkout·동봉 archive·빌드 계보를 대조한다.
- [pack 원본 provenance](lightningcss-provenance-fix4.json)는 tarball 내부 NATIVE-FIX-PROVENANCE.json의 사본이다. native/WASM/source archive/Cargo.lock 해시를 보존한다.

공개 라이브러리 검증 manifest는 합성 CSS 5개 클래스·8개 입력을 사용한다. 소비자의 비공개 앱 CSS·전체 IR 증거는 별도로 관리하고 이 저장소와 tarball에 복사하지 않는다. 영구 포크 PR의 병합과 공통 8개 산출물 원장 갱신은 부모 통합 단계가 소유한다.

## 원본 소스와 법적 고지의 동봉 확인

| 위치 | 실제 동봉 내용 |
|---|---|
| package/LICENSE | Lightning CSS MPL-2.0 전문. 외부 사본은 [원문](../LICENSES/upstream/lightningcss-1.33.0.txt) |
| package/native-source.tar.gz | 수정 source, Cargo.lock, 원본 fixture와 vendor 소스 |
| source archive의 vendor/serde-content | LICENSE-MIT·LICENSE-APACHE·UPSTREAM.md를 포함한 수정 crate |
| package/wasm/NAPI-WASM-NOTICE | napi-wasm 1.1.3, 고정 package.json의 author/MIT 선언, 허가·조건·면책 전문, 원본 SHA·npm integrity |
| package/NATIVE-FIX-PROVENANCE.json | 제품 source SHA와 native/WASM/source bytes 해시 |

napi-wasm의 고정 package.json도 wasm/napi-wasm-package.json으로 동봉한다. 상류가 제공하지 않은 copyright 연도/권리자는 추정하지 않으며, author attribution과 MIT 허가·조건·면책 전문을 함께 제공한다. fix.3 tarball/이전 provenance와 보고서는 역사 증거로 보존하고 현재 설치 정본은 원장의 fix.4만 선택한다. 최종 수정 pack은 포크 PR 독립 리뷰에서 재확인한다. common 자체 GPL 고지와 외부 MPL/MIT/Apache 원문을 서로 대체하지 않는다.

## 설치 경로와 플랫폼

root의 vendor 파일만 체크인한다. 다음 명령이 원본 파일과 원장·세 lock의 버전/해시를 검증한 뒤 smoke·example의 vendor로 같은 bytes를 복사한다.

    node packages/ui/smoke/prepare-lock.mjs --css-only

두 fixture의 vendor 사본은 생성물이므로 Git에서 제외한다. CI는 준비된 smoke 디렉터리를 통째로 격리 경로에 복사하여 외부 저장소 node_modules 없이 npm ci한다. UI/tokens의 개발 pack 생성 뒤 옵션 없이 실행하면 그 두 개발 pack integrity만 갱신하며, 고정 Lightning CSS 해시는 갱신하지 않는다.

Linux x64/glibc >=2.35는 내장 GNU native를 사용한다. 다른 Node >=18 호스트와 LIGHTNINGCSS_FORCE_WASM=1은 같은 수정 source의 내장 WASM을 사용한다. stock optional platform 패키지로 돌아가지 않는다. macOS 실제 실행은 포크 macOS CI gate이며 이 정책 분기의 설치 정의를 CI 성공으로 표시하지 않는다.

fix.4 source archive는 .gitattributes에 따라 fixture vendor의 역사 tgz를 제외한다. Rust/Cargo/vendor/wasm/build script 대응 source는 계속 포함한다. package/wasm/ADAPTER-BUILD.json은 실제 JS 입력과 번들 출력 hash를 기록한다.
