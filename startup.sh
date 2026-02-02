#!/bin/bash
# Hugging Face Spaces 启动脚本
# 这个脚本在 Spaces 中自动运行

echo "=== AI RSS Filter - Hugging Face Spaces 启动 ==="
echo "Python version: $(python --version)"
echo "Node version: $(node --version)"

# 进入项目目录
cd /app

# 安装 Python 依赖（如果需要）
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# 构建 React 前端
if [ ! -d "frontend/build" ]; then
    echo "Building React frontend..."
    cd frontend
    npm ci
    npm run build
    cd /app
fi

# 启动 FastAPI
echo "Starting FastAPI server on port 7860..."
python api.py
