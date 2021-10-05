echo off
title Firestore poll
call env\scripts\activate
REM start cmd /K call python firestore_poll.py
call python firestore_agg_poll.py
