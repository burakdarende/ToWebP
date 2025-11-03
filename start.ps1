# Quick Start Script for Windows
# Double-click this file to run the application

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Image to WebP Converter" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow

$pythonCheck = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCheck) {
    Write-Host "ERROR: Python is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python found!" -ForegroundColor Green
Write-Host ""

# Check and install requirements
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$pillowCheck = python -c "import PIL" 2>&1
$ctkCheck = python -c "import customtkinter" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "All dependencies ready!" -ForegroundColor Green
Write-Host ""

# Run the application
Write-Host "Starting application..." -ForegroundColor Green
Write-Host ""

python gui.py

Write-Host ""
Write-Host "Application closed." -ForegroundColor Yellow
