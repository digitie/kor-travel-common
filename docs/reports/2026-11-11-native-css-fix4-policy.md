# Native CSS fix.4 정책 후속

정책 기준 commit256d263과 그 보고서/evidence는 불변 보존했다. 새 exact 버전은 1.33.0+nativecss.fix.4이며 axis·artifact 원장·root 및 실제 Next smoke/example의 세 manifest/lock·생성 policy가 모두 같은 vendor pack을 선택한다. web/mobile.required의 빌드/개발 의존성 계약과 runtimeRequired 제외는 그대로다.

원본 LightningCSS source 1e94372a6da4a55eac4a6dc3ff9cdeec103e8ac1은 WASM file URL 인코딩, napi-wasm author/MIT 전문, source/archive/빌드 계보 자동 감사와 실제 Rust CI를 포함한다. native/raw WASM의 Rust/Cargo/vendor 입력은684c528 빌드와 동일하여 binary를 재사용하고 JS adapter만 다시 번들했다. 고정 source archive는 역사 fixture tgz를 제외한다. [현재 고지와 provenance](../../vendor/README.md)를 참조한다.

기존 fix.3 vendor 파일·provenance와 최초 정책 보고서를 그대로 보존했다. 현재 원장은 fix.4만 활성 선택한다. 다른 기존5개 artifact 원장과 세 lock의 CSS 외 package entry는256d263 object와 동일함을 대조했다. 원장8개 전체 refresh는 부모 통합 단계다.

[새 선택 검증 evidence](evidence/2026-11-11-native-css-fix4-policy/manifest.json): schema8·정책40·실제 vendor/source/고지2, 합계50 PASS/skip0. 생성 policy 정합과 root/smoke/example의 실제 vendor 복사 bytes도 통과했다. 공유 node_modules는 읽기 전용으로 사용했으며 설치 파일을 수정하지 않았다.

[packages 브라우저 환경 보정](2026-11-11-packages-browser-image.md)은 별도47cca0a commit이다. 새 exact source의 원격 packages/호스트 CI, fresh npm ci/Next build, A/B 최종 delta 리뷰는 부모 접수 후 실행해야 한다. 로컬 결과를 원격 CI나 실제 앱 export PASS로 확대하지 않는다. 이전 fix.3 앱 export/비공개 IR 증거는 별도 보존하며 공개 policy에는 포함하지 않는다.
