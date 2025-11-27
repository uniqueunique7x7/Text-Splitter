@echo off
REM Text File Splitter - Golden Edition
REM Quick Launch Batch File

title Text File Splitter - Starting...

echo.
echo ========================================
echo    Text File Splitter - Golden Edition
echo ========================================
echo.
echo Starting application...
echo.

REM Try to run with 'python' command first
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using 'python' command...
    python file_splitter.py
    goto :end
)

REM If 'python' doesn't work, try 'py' command
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using 'py' command...
    py file_splitter.py
    goto :end
)

REM If neither works, show error message
echo.
echo ========================================
echo ERROR: Python not found!
echo ========================================
echo.
echo Please install Python 3.7 or higher from:
echo https://www.python.org/downloads/
echo.
echo Make sure to check "Add Python to PATH"
echo during installation.
echo.
pause
goto :end

:end
REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo Application closed with errors.
    echo Press any key to exit...
    pause >nul
)
