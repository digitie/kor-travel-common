# packages 브라우저 CI 환경 보정

기준 정책 source 256d263과 source2 리뷰 원문은 보존한다. common8dad의 packages job130579801074는 azure.archive.ubuntu.com DNS 해석 실패로 Playwright 시스템 의존성 apt 설치에 실패했다. 테스트 실패를 완화하거나 같은 환경 재시도를 추가하지 않는다.

packages job만 공식 mcr.microsoft.com/playwright:v1.65.0-noble의 부모가 확인한 amd64 digest sha256:bc4fbb329a25287ed23e9216c97063646abdd1bf2da669a9895fa3e2078b2302로 고정한다. PLAYWRIGHT_BROWSERS_PATH=/ms-playwright를 유지하고 기존 setup-node/.nvmrc의 Node22.23.1을 그대로 사용한다. 다른 root CI의 Node 설정은 바꾸지 않는다.

공식 [Docker 문서](https://playwright.dev/docs/docker)와 [v1.65.0 이미지 원본](https://github.com/microsoft/playwright/blob/v1.65.0/utils/docker/Dockerfile.noble)은 이미지에 브라우저와 시스템 의존성이 포함되고 npm Playwright 패키지는 프로젝트에서 설치함을 명시한다. 설치한 npm 버전을 중앙 정책과 대조하고 실행 파일의 실제 존재·실행 권한·headless launch/close를 확인한다. 별도 apt/browser download 단계는 제거하며 기존 실제 브라우저 테스트 명령과 모든 assertion은 유지한다.

로컬 image pull/전체 설치/브라우저 재실행은 하지 않았다. 로컬에서는 workflow 구조·고정 digest·기존 브라우저 명령 보존을 확인한다. 새 exact source의 원격 packages PASS는 부모의 PR/host CI 접수 후 확인해야 하며 현재 NOT_RUN이다. 이 변경만으로 PASS라고 보고하지 않는다.
