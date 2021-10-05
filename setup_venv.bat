echo off
title Setup Virtual Environment
py -m venv env && env\scripts\activate && python -m pip install --upgrade pip && pip install -r requirements.txt
echo virtual enivironment file "env" has been created
pause