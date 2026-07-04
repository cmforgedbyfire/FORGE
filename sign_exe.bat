@echo off
echo Signing FORGE.exe...

REM Update these paths to match your certificate location
set CERT_PATH="path\to\your\certificate.pfx"
set CERT_PASSWORD=YourCertPassword

REM Sign the executable
signtool sign /f %CERT_PATH% /p %CERT_PASSWORD% /t http://timestamp.sectigo.com /v "dist\FORGE.exe"

if %ERRORLEVEL% EQU 0 (
    echo âœ“ Successfully signed FORGE.exe
) else (
    echo âœ— Failed to sign executable
    exit /b 1
)

echo Done!
pause
