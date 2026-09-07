# CI 버전 report fixture

이 입력은 T-009의 `check-versions` job이 report 표와 step summary를 실제 생성하는지 확인하는 최소 fixture다. npm 설치용 lock이나 소비자 실측이 아니다. 설치·게시하지 않는다.

React의 의도적인 하한 미달 1행과 Node/npm의 권장값 불일치 2행을 현재 `versions.json`에서 검출한다. report 모드는 exit 0이며, CI는 비어 있지 않은 finding·BELOW_FLOOR와 summary 출력을 별도로 확인한다. 정책 변경으로 기대가 달라지면 그 PR에서 이 fixture를 함께 검토한다.
