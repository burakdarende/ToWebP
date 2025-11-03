@echo off
:: Quick Start Batch Script for Windows
:: Double-click this file to run the application

echo.
echo ========================================
echo    Image to WebP Converter
echo ========================================
echo.

:: Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

:: Install requirements if needed
echo Checking dependencies...
pip install -r requirements.txt >nul 2>&1

echo All dependencies ready!
echo.

:: Run the application
echo Starting application...
echo.

python gui.py

echo.
echo Application closed.
pause
