echo off
title latency experiment
start cmd /K call firestore_poll
start cmd /K call sql_poll
timeout 2
start cmd /K call run_dts