#!/bin/bash
# 크론 데몬 실행
cron
# 로그 파일이 없으면 생성
touch /crawler/logs/cron.log
# 컨테이너가 종료되지 않도록 로그를 계속 출력
tail -f /crawler/logs/cron.log

