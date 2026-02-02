#!/bin/bash
# 部署前检查清单脚本

echo "=== AI RSS Filter - Hugging Face Spaces 部署检查 ==="
echo ""

# 检查文件存在性
echo "📋 检查文件结构..."

files_to_check=(
    "Dockerfile.full-stack"
    ".dockerignore"
    "HUGGINGFACE_QUICK_DEPLOY.md"
    "HUGGINGFACE_DEPLOYMENT.md"
    "ai_rss_filter/api.py"
    "ai_rss_filter/requirements.txt"
    "ai_rss_filter/config/rss_sources.json"
    "frontend/package.json"
    "frontend/public/index.html"
    "frontend/src/App.js"
)

all_exist=true
for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
        all_exist=false
    fi
done

echo ""
echo "📦 检查 API 配置..."

# 检查 api.py 是否包含静态文件挂载
if grep -q "StaticFiles" ai_rss_filter/api.py; then
    echo "✅ api.py 包含静态文件挂载"
else
    echo "❌ api.py 缺少静态文件挂载"
fi

# 检查 requirements.txt 是否包含必要的包
if grep -q "fastapi" ai_rss_filter/requirements.txt; then
    echo "✅ requirements.txt 包含 fastapi"
else
    echo "❌ requirements.txt 缺少 fastapi"
fi

if grep -q "uvicorn" ai_rss_filter/requirements.txt; then
    echo "✅ requirements.txt 包含 uvicorn"
else
    echo "❌ requirements.txt 缺少 uvicorn"
fi

echo ""
echo "🌐 检查前端配置..."

# 检查 package.json
if [ -f "frontend/package.json" ]; then
    if grep -q "\"react\"" frontend/package.json; then
        echo "✅ React 已配置"
    else
        echo "❌ React 未配置"
    fi
    
    if grep -q "\"build\"" frontend/package.json; then
        echo "✅ build 脚本存在"
    else
        echo "❌ build 脚本缺失"
    fi
fi

echo ""
echo "🐳 检查 Docker 配置..."

if [ -f "Dockerfile.full-stack" ]; then
    if grep -q "react-builder" Dockerfile.full-stack; then
        echo "✅ Multi-stage React builder 已配置"
    else
        echo "⚠️  警告：Dockerfile 可能缺少 React 构建阶段"
    fi
    
    if grep -q "PORT=7860" Dockerfile.full-stack; then
        echo "✅ Hugging Face Spaces 端口已配置"
    else
        echo "⚠️  警告：端口配置可能不正确"
    fi
fi

echo ""
echo "✨ 检查完成！"
echo ""

if [ "$all_exist" = true ]; then
    echo "🎉 所有文件都存在，可以开始部署！"
    echo ""
    echo "下一步：按照 HUGGINGFACE_QUICK_DEPLOY.md 中的步骤进行部署"
else
    echo "⚠️  缺少某些文件，请检查上面的错误信息"
fi
