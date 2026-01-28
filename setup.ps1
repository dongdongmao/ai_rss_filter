# setup.ps1 Windows PowerShell Script
# Quick setup and configuration script

$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RSS Filter - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "✓ Checking Python..." -ForegroundColor Green
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Python not found, please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n✓ Creating virtual environment..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    python -m venv venv
}
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "`n✓ Installing dependency packages..." -ForegroundColor Green
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check directories
Write-Host "`n✓ Checking directory structure..." -ForegroundColor Green
if (-not (Test-Path "logs")) { mkdir logs }
if (-not (Test-Path "data")) { mkdir data }

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ✓ Setup complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Next steps:`n" -ForegroundColor Yellow
Write-Host "1. Configure environment variables:"
Write-Host "   copy .env.example .env"
Write-Host "   # Edit .env file and add your Telegram Token etc`n"

Write-Host "2. Run quick setup wizard:"
Write-Host "   python quickstart.py`n"

Write-Host "3. First test:"
Write-Host "   python main.py`n"

Write-Host "4. Start scheduled tasks:"
Write-Host "   python scheduler.py`n"
