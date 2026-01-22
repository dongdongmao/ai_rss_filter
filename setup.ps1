# setup.sh / setup.ps1 Windows PowerShell 脚本
# 快速安装和配置脚本

$ErrorActionPreference = "Continue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  RSS 降噪器 - 快速安装" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 检查 Python
Write-Host "✓ 检查 Python..." -ForegroundColor Green
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

# 创建虚拟环境
Write-Host "`n✓ 创建虚拟环境..." -ForegroundColor Green
if (-not (Test-Path "venv")) {
    python -m venv venv
}
& ".\venv\Scripts\Activate.ps1"

# 安装依赖
Write-Host "`n✓ 安装依赖包..." -ForegroundColor Green
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 检查目录
Write-Host "`n✓ 检查目录结构..." -ForegroundColor Green
if (-not (Test-Path "logs")) { mkdir logs }
if (-not (Test-Path "data")) { mkdir data }

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ✓ 安装完成！" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "下一步：`n" -ForegroundColor Yellow
Write-Host "1. 配置环境变量:"
Write-Host "   copy .env.example .env"
Write-Host "   # 编辑 .env 文件，添加你的 Telegram Token 等`n"

Write-Host "2. 运行快速配置向导:"
Write-Host "   python quickstart.py`n"

Write-Host "3. 首次测试:"
Write-Host "   python main.py`n"

Write-Host "4. 启动定时调度:"
Write-Host "   python scheduler.py`n"
