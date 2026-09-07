# 토큰 예제

`weather-overrides.css`는 고정 weather 원천(`6003da995fa4b35799f9dadc406c6ba2878bfbae`의
`packages/kor-travel-weather-admin/frontend/app/tokens.css`)을 `tokens.css`와
`aliases/map-vocabulary.css` 뒤에서 재현하는 앱 소유 오버라이드 예제다. `--kt-*` 값은
weather의 light/dark 색·형태·모션·폰트·17rem rail을 보존한다. map과 weather의
`--radius-md` 의미 차이는 이 예제에서 panel로 재선언하며, weather에만 있는 `--space-*`
간격 이름은 common 토큰으로 승격하지 않고 이 예제에 남긴다.

이 디렉터리는 npm 배포 대상이 아니다. 실제 weather 교체와 320·375·414·768·1024·1280px
6폭 시각 diff 0 검증은 T-461의 소비자 저장소 evidence에서 수행한다(`NOT_RUN(T-461)`).
