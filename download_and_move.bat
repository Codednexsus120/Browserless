@echo off
setlocal enabledelayedexpansion

REM ===== Step 1: Get latest artifact URL from external server =====
echo Fetching latest artifact URL...
for /f "tokens=*" %%A in ('curl -s "https://azcaptchahh.pythonanywhere.com/geturl"') do set "url_response=%%A"

REM Parse JSON to extract URL using PowerShell
for /f "delims=" %%B in ('powershell -Command "Write-Output ((ConvertFrom-Json ''%url_response%'').url)"') do set "artifact_url=%%B"

echo Latest artifact URL: %artifact_url%
IF "%artifact_url%"=="" (
    echo ERROR: Artifact URL is empty. Exiting.
    exit /b 1
)

REM ===== Step 2: Define paths =====
set "zip_path=%~dp0data.zip"
set "dst=%USERPROFILE%\Downloads\data.zip"
set "targetDir=%USERPROFILE%\Desktop\data"

REM ===== Step 3: Download artifact =====
echo Downloading artifact to %zip_path% ...
curl -L "%artifact_url%" -o "%zip_path%"
IF NOT EXIST "%zip_path%" (
    echo ERROR: Download failed. Exiting.
    exit /b 1
)
echo Downloaded file:
dir %zip_path%

REM ===== Step 4: Move ZIP to Downloads =====
echo Moving %zip_path% to %dst% ...
move /Y "%zip_path%" "%dst%"
IF ERRORLEVEL 1 (
    echo ERROR: Failed to move zip. Exiting.
    exit /b 1
)

REM ===== Step 5: Remove existing folder if exists =====
if exist "%targetDir%" (
    echo Removing existing folder %targetDir%
    rmdir /S /Q "%targetDir%"
)

REM ===== Step 6: Create folder =====
echo Creating folder %targetDir%
mkdir "%targetDir%"

REM ===== Step 7: Extract ZIP =====
echo Extracting ZIP to %targetDir% ...
powershell -Command "Expand-Archive -Path '%dst%' -DestinationPath '%targetDir%' -Force"

REM ===== Step 8: Cleanup =====
echo Cleaning up ZIP file ...
del "%dst%"

REM ===== Step 9: List extracted contents =====
echo Extraction completed. Contents of %targetDir%:
dir "%targetDir%"

echo Artifact downloaded, moved, and extracted successfully.
exit /b 0
