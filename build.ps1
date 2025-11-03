# Build script for Windows
# Creates standalone executable using PyInstaller

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Image to WebP Converter - Build Script" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
$pyinstallerCheck = python -c "import PyInstaller" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install PyInstaller. Please install manually:" -ForegroundColor Red
        Write-Host "  pip install pyinstaller" -ForegroundColor Red
        exit 1
    }
}

Write-Host "PyInstaller found!" -ForegroundColor Green
Write-Host ""

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "*.spec") { Remove-Item -Force "*.spec" }
Write-Host "Clean complete!" -ForegroundColor Green
Write-Host ""

# Build executable
Write-Host "Building executable..." -ForegroundColor Yellow
Write-Host ""

python build_exe.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "===============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your executable is ready at:" -ForegroundColor Cyan
    Write-Host "  $(Get-Location)\dist\ImageToWebP.exe" -ForegroundColor White
    Write-Host ""
    Write-Host "You can now distribute this file without requiring Python!" -ForegroundColor Yellow
    Write-Host ""
    
    # Ask if user wants to run the executable
    $response = Read-Host "Do you want to test the executable now? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        Write-Host "Starting executable..." -ForegroundColor Green
        Start-Process ".\dist\ImageToWebP.exe"
    }
} else {
    Write-Host ""
    Write-Host "BUILD FAILED!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
    exit 1
}
