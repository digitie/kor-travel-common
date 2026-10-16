# Common36 r2 보존 DB 독립 역사 검증 C

판정: 역사 근거 검증 PASS. 원 one-shot controller PASS로 승격하지 않는다. control 활성 유지 중 post-child 두 tick gate와의 동등성은 미입증이며 HOLD다.

WSL 고립 lab 0a0443e6-ea68-4e7e-8059-d626e89f58ff의 정확한 home SQLite를 stdlib sqlite3 mode=ro, query_only=ON, 명시 읽기 transaction으로 직접 확인했다. SDK import, 새 fault/run/launch/start/stop/flag 조작, 운영 호출은 0이다.

runs 전체가 정확 4개다. 부모 bf3b027e-feaa-4a2e-8f1f-046c0d08d1d2 FAILURE, 자식 62d0c2c6-46f3-4b2a-8172-3b451059461b SUCCESS, 두 control SUCCESS다. 부모 공식 RUN_WORKER_RESTART 실패 event는 정확 1개다. 전 run의 native dagster/max_retries=0이다. 자식의 Common retry attempt는 1, infra parent 태그와 deterministic run key가 정확 부모를 가리킨다. job/origin/project/config도 같다. Dagster parent_run_id는 null이므로 네이티브 reexecution 계보라고 설명하지 않는다. 추가 자식은 없다.

자식 SUCCESS event는 1792131587.019034다. 이후 owned_infra completed tick 24/26과 owned_incarnation 25/27이 각각 정확 2개이며 모두 SKIPPED, run_ids=[]다. 오류/미완료 tick을 완료로 계산하지 않았다.

시점 한계: control SUCCESS는 1792132324.4931116와 1792132324.542734다. 위 네 tick은 1792132353.424815~1792132419.5313072로 모두 control 종료 뒤다. 자식 완료 후 두 센서가 추가 자식을 만들지 않았다는 실증은 있으나 control을 STARTED로 유지한 채 두 tick을 확인하는 원 run()의 순서를 통과한 증거는 아니다.

원 C 정상 정산 receipt SHA 1451f0b1684dd5683f99c96a9b504a873bb5b0c873500e262fa610b49f57733b를 대조했다. 정확 소유 3 CID를 현재 read-only Docker inspect로 확인하여 모두 PID0/Running false/Exit0/OOM false/RestartCount0이며 CID가 원문과 같다. daemon Config/HostConfig/Image/Name/Created와 순서 정규화 Mounts도 당시 원문과 같다.

읽기 전후 대상 6 DB 및 존재하는 WAL SHA가 모두 같다. DB별 transaction이므로 여러 SQLite 파일 전체에 걸친 원자 snapshot은 아니다. 세 소유 컨테이너는 모두 정지 상태다. D 관측 SHA 694912926240fc32894f9b6f5c9ddf0f076dc988d83d78e6b2df92a6f792e97f와 자식 SUCCESS event 시간을 대조했지만 결론은 직접 DB에서 산출했다.

원 r2 daemon OOM/137 controller 실패, C continuation의 Mounts 순서 false assertion, 정상 종료 receipt의 당시 postchild 미입증 표시는 원형 보존한다. r3 실패와도 별도다. 통합 scenario의 부분 증거이며 원 one-shot 전체 PASS, 운영/ARM 효과를 주장하지 않는다.

초기 독립 reader r1은 control 성공 전 tick이라는 더 강한 시간조건을 적용해 AssertionError로 종료했다. r2에서는 실제 시점 차이를 별도 필드로 정산했다. 추가 상태 변경은 없다.

직접 reader: common36-historical-postchild-reader-c-r2-20261016.py / SHA256 84958bdfa09c70a59dd66cebb1f05ea27362642abf045022e9c6d38ad8c4285a

원시 Env·주소·cursor가 없는 안전 투영: common36-historical-postchild-review-c-r2-20261016.safe.json / SHA256 893ed66c268d88b6b90f79c889a85ea1f7f442424b28aab3cc0af70390e5624c
