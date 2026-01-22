#!/bin/bash
# setup.sh - Linux/Mac 快速安装脚本

echo ""
echo "========================================"
echo "  RSS 降噪器 - 快速安装"
echo "========================================"
echo ""

# 检查 Python
echo "✓ 检查 Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "✗ 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

# 创建虚拟环境
echo ""
echo "✓ 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 安装依赖
echo ""
echo "✓ 安装依赖包..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 检查目录
echo ""
echo "✓ 检查目录结构..."
mkdir -p logs
mkdir -p data

echo ""
echo "========================================"
echo "  ✓ 安装完成！"
echo "========================================"
echo ""

echo "下一步：
"
echo "1. 配置环境变量:"
echo "   cp .env.example .env"
echo "   # 编辑 .env 文件，添加你的 Telegram Token 等
"
echo "2. 运行快速配置向导:"
echo "   python quickstart.py
"
echo "3. 首次测试:"
echo "   python main.py
"
echo "4. 启动定时调度:"
echo "   python scheduler.py
"
