@echo off
title BitStream Launcher
cd /d "%~dp0"

echo ====================================================
echo  BITSTREAM — LOSSLESS DATA CONTAINER LAUNCHER
echo ====================================================
echo [STATUS] Starting BitStream application...
echo.

:: Use exact Python installation path to avoid Windows App Store alias bugs
set "PYTHON_EXE=C:\Users\mehul\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

:: Launch BitStream GUI
start "" "%PYTHON_EXE%" main.py

echo [STATUS] BitStream application is now running.
echo.
echo ----------------------------------------------------
echo  TYPE 'stop' (or 'stock') AND PRESS ENTER TO STOP
echo ----------------------------------------------------
echo.

:LOOP
set /p choice="Command > "

if /i "%choice%"=="stop" goto KILL_PROCESS
if /i "%choice%"=="stock" goto KILL_PROCESS
if /i "%choice%"=="exit" goto KILL_PROCESS
if /i "%choice%"=="q" goto KILL_PROCESS

echo [!] Invalid command. Type 'stop' or 'stock' to terminate the process.
echo.
goto LOOP

:KILL_PROCESS
echo.
echo [STATUS] Terminating BitStream application...

:: Stop process cleanly
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*main.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1

echo [STATUS] BitStream process terminated successfully.
echo.
timeout /t 2 >nul
exit
