@echo off
setlocal

set "ROOT=%~dp0"
set "PYTHON=C:\Python314\python.exe"

cd /d "%ROOT%"

if exist "%PYTHON%" (
    start "FORGE" "%PYTHON%" "%ROOT%main.py"
    exit /b
)

where python >nul 2>nul
if not errorlevel 1 (
    start "FORGE" python "%ROOT%main.py"
    exit /b
)

if exist "%ROOT%dist\FORGE.exe" (
    start "FORGE" "%ROOT%dist\FORGE.exe"
    exit /b
)

echo Could not find Python or a built FORGE executable.
pause
