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
Write-Host "1. Configure (optional): copy .env.example .env"
Write-Host "2. Web app: python api.py  (then open http://localhost:7860)"
Write-Host "3. CLI test: python main.py"
Write-Host "4. Scheduler: python scheduler.py"
Write-Host ""
