@echo off
title Single DT IoT Gateway
echo Starting DT gateway upload
:: All variables are local variables
setlocal
set /A try_count = 0
set /A max_retry = 3
set /A retry = 1

:: Start the virtual environment
call env\scripts\activate
if %ERRORLEVEL% == 0 goto :try_launch
echo Virtual environment didn't setup
goto :end

:: If connection failed, retry in 5 seconds
:try_launch
set /A try_count = %try_count% + 1
echo %try_count%
if %try_count% GTR %max_retry% goto :end
if %try_count% GTR %retry% timeout 5
call python Run.py %1 %2 %3
if %ERRORLEVEL% NEQ 0 goto :try_launch

:: If retry failed 3 times, exit the program
:end 
exit /B %ERRORLEVEL%
endlocal