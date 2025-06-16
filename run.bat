@echo off
setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Set virtual environment path
set "VENV_PATH=%SCRIPT_DIR%venv"
set "PYTHON_EXE=%VENV_PATH%\Scripts\python.exe"
set "PIP_EXE=%VENV_PATH%\Scripts\pip.exe"

echo [%date% %time%] Starting maradmin-alert script...

REM Check if virtual environment exists
if not exist "%VENV_PATH%" (
    echo [%date% %time%] Virtual environment not found. Creating new environment...
    python -m venv "%VENV_PATH%"
    if errorlevel 1 (
        echo [%date% %time%] ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo [%date% %time%] Virtual environment created successfully
)

REM Check if Python executable exists in venv
if not exist "%PYTHON_EXE%" (
    echo [%date% %time%] ERROR: Python executable not found in virtual environment
    exit /b 1
)

REM Install/update requirements
echo [%date% %time%] Installing/updating requirements...
"%PIP_EXE%" install -r requirements.txt --quiet
if errorlevel 1 (
    echo [%date% %time%] WARNING: Some packages may have failed to install
)

REM Run the main script
echo [%date% %time%] Running main.py...
"%PYTHON_EXE%" main.py
set "EXIT_CODE=%errorlevel%"

if %EXIT_CODE% equ 0 (
    echo [%date% %time%] Script completed successfully
) else (
    echo [%date% %time%] Script failed with exit code %EXIT_CODE%
)

echo [%date% %time%] Finished
exit /b %EXIT_CODE%
