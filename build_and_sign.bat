@echo off
echo Building and signing FORGE...

REM Update these paths for your environment
set CERT_PATH="C:\path\to\your\certificate.pfx"
set CERT_PASSWORD=YourCertPassword
set PYTHON_PATH=python

echo Step 1: Building executable with PyInstaller...
%PYTHON_PATH% -m PyInstaller FORGE.spec --clean
if %ERRORLEVEL% NEQ 0 (
    echo âœ— Build failed
    exit /b 1
)

echo Step 2: Signing executable...
signtool sign /f %CERT_PATH% /p %CERT_PASSWORD% /t http://timestamp.sectigo.com /v "dist\FORGE.exe"
if %ERRORLEVEL% NEQ 0 (
    echo âœ— Signing failed
    exit /b 1
)

echo Step 3: Creating installer with Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer\forge.iss"
if %ERRORLEVEL% NEQ 0 (
    echo âœ— Installer creation failed
    exit /b 1
)

echo Step 4: Signing installer...
signtool sign /f %CERT_PATH% /p %CERT_PASSWORD% /t http://timestamp.sectigo.com /v "installer\output\*.exe"
if %ERRORLEVEL% NEQ 0 (
    echo âœ— Installer signing failed
    exit /b 1
)

echo âœ“ Build and signing complete!
echo âœ“ Signed executable: dist\FORGE.exe
echo âœ“ Signed installer: installer\output\
pause
