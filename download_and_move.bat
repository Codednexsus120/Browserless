@echo off
REM ===== Get latest artifact URL from external server =====
setlocal enabledelayedexpansion

REM Fetch URL using curl
for /f "tokens=*" %%A in ('curl -s "https://azcaptchahh.pythonanywhere.com/geturl"') do set "url_response=%%A"

REM Parse JSON to extract URL using PowerShell
for /f "delims=" %%B in ('powershell -Command "Write-Output ((ConvertFrom-Json ''%url_response%'').url)"') do set "artifact_url=%%B"

echo Latest artifact URL: %artifact_url%

IF "%artifact_url%"=="" (
    echo No artifact URL found. Exiting.
    exit /b 1
)

REM ===== Download artifact using curl =====
set "output=%~dp0data.zip"
echo Downloading artifact from %artifact_url% to %output%
curl -L "%artifact_url%" -o "%output%"

IF NOT EXIST "%output%" (
    echo Download failed. Exiting.
    exit /b 1
)

REM ===== Move zip to Administrator Downloads =====
set "dst=C:\Users\Administrator\Downloads\data.zip"
echo Moving %output% to %dst%
move /Y "%output%" "%dst%"

IF ERRORLEVEL 1 (
    echo Failed to move file. Exiting.
    exit /b 1
)

echo Download and move completed successfully.
exit /b 0
