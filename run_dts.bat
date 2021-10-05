@echo off
title Main DT launch
start cmd /K call single_dt "1" "test_device" "dt_db1"
timeout 60
start cmd /K call single_dt "2" "pod_sim1" "dt_db2"
timeout 60
start cmd /K call single_dt "1" "pod_sim2" "dt_db3"
REM timeout 60
REM start cmd /K call single_dt "2" "dt31" "dt_db4"
REM timeout 60
REM start cmd /K call single_dt "2" "dt32" "dt_db5"

