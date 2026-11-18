@echo off
setlocal
cd /d "%~dp0"

if exist "%~dp0BitStream.exe" (
    start "BitStream" "%~dp0BitStream.exe"
    exit /b 0
)

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 main.py
    exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
    python main.py
    exit /b %errorlevel%
)

echo BitStream could not find Python. Install Python 3.10 or newer, or place BitStream.exe beside this launcher.
pause
exit /b 1
