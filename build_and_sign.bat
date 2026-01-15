@echo off
echo Building and signing FORGE...

REM Update these paths for your environment
set CERT_PATH="C:\path\to\your\certificate.pfx"
set CERT_PASSWORD=YourCertPassword
set PYTHON_PATH=python

echo Step 1: Building executable with PyInstaller...
%PYTHON_PATH% -m PyInstaller ShipStudio.spec --clean
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Build failed
    exit /b 1
)

echo Step 2: Signing executable...
signtool sign /f %CERT_PATH% /p %CERT_PASSWORD% /t http://timestamp.sectigo.com /v "dist\ShipStudio.exe"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Signing failed
    exit /b 1
)

echo Step 3: Creating installer with Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer\ship_studio.iss"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Installer creation failed
    exit /b 1
)

echo Step 4: Signing installer...
signtool sign /f %CERT_PATH% /p %CERT_PASSWORD% /t http://timestamp.sectigo.com /v "installer\output\*.exe"
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Installer signing failed
    exit /b 1
)

echo ✓ Build and signing complete!
echo ✓ Signed executable: dist\ShipStudio.exe
echo ✓ Signed installer: installer\output\
pause