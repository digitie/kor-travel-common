# Common37 stdlib bytecode 독립 리뷰 D

- 판정: SOURCE_PASS. 열린 P0/P1/P2/P3 없음.
- 기준: base 200a350101665f44246422c7102c087fdfb3222e → product 084585796bc4428dc9a3347f08f8ebaaa04bdfa3.
- 전체 4파일 diff SHA256: 9949db4a1fda6080b660cec21fb02207967629dd54608a64b9b6841434460791.
- build_bytecode.py SHA256: b07c7f94565147f619bffba7f1f9871106c0ee07d3683974393d596ffda5d266.
- D는 Common36 기존 작성자다. 이번 독립 판정은 새 Common37 delta에만 해당한다. 다른 리뷰 원문은 읽지 않았다.

## 검토한 계약

제품90행·테스트234행·Dagster 가이드 §17·T319 추가 전체를 Git object에서 읽었다.
최종 interpreter의 sysconfig stdlib만 선택하고 worker1/optimize0/checked-hash/force를 고정한다.
앱·Dagster·DB import나 런타임 자동 실행이 없고 source/환경을 바꾸지 않는다.
단일 writer인 신뢰 빌드라는 문서 한계에 맞게 외부 source 링크·directory symlink·외부 cache prefix와
cache symlink를 거절/생략한다. 동시 공격자에 대한 sandbox/원자 snapshot으로 오인하지 않는다.
읽기/권한/빈 대상/문법 실패는 nonzero이며 부분 pyc는 rollback되지 않는다는 설명이 정확하다.
root 절대경로에 tests/site-packages 이름이 있어도 전체 컴파일을 생략하지 않는 수정도 확인했다.
core-only 의존성 추가0이고 기존 Common36 제품은 이 리뷰의 새 독립 검증으로 세지 않는다.

## 직접 검증

Git object의 helper·테스트만 별도 임시 경로로 추출하고 원 repository conftest 없이 Python3.12에서
26 PASS (0.22초). 비root 권한 음성도 실제 실행됐다. 로그 common37-build-bytecode-review-d-test-20261016.log
SHA256 87bc219ea97c3de799e434556778fe6bf6a016ff19c241e46e38fbae60ab4e97.
별도 순수 모형3개 PASS: root의 상위 site-packages 이름 허용/정확 cache magic·flags3·sourcehash·co_filename,
중첩 site-packages 문법오류 제외, 외부 prefix 실패와 source 불변.
모형 SHA256 5a3ab5712cc9b1cf0ac1bd89bec261ded034a94d345a5a912bb9246f063a762d.

## 한계

실제 이미지 빌드·패키지 전체 suite·wheel 설치·ARM 실행·운영 CPU/메모리 개선은 이 리뷰에서 NOT_RUN이다.
root가 제공한 실제 stdlib cache 부재/임시 prefix 실측은 채택 근거이며 이 Common 소스 시험 자체의 운영 효과가 아니다.
Docker source가 최종 interpreter/root 단계에서 실행하고 후속 layer가 cache를 제거하지 않는지는 소비자 검증이다.
소스 수정·SSH·Docker·DB·provider 호출0. 모든 검증 도구는 terminal이다.
