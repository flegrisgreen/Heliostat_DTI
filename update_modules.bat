@echo off
title update modules
echo outdated modules
call "env/scripts/activate"
pip list --outdated
pause
echo Updating modules
call python -m pip install --upgrade pip
call pip install -r requirements.txt --upgrade


