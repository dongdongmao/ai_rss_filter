#!/usr/bin/env python3
"""
快速启动脚本 - 同时启动 FastAPI 后端和 React 前端
或单独启动 FastAPI（如果 React 已构建）
"""

import os
import sys
import subprocess
import time
import platform

def main():
    print("=" * 60)
    print("AI RSS Filter - 启动管理器")
    print("=" * 60)
    print()
    
    # 检查 React 是否已构建
    frontend_build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
    react_built = os.path.exists(frontend_build_dir)
    
    print("📊 系统检查:")
    print(f"  ✓ Python: {sys.version.split()[0]}")
    print(f"  {'✓' if react_built else '✗'} React 构建: {'已完成' if react_built else '未完成'}")
    print()
    
    # 显示选项
    print("选择启动方式:")
    print("  1. 启动 FastAPI + React 静态服务 (需要 React 已构建)")
    print("  2. 启动 FastAPI + React 开发服务器 (完整开发模式)")
    print("  3. 仅启动 FastAPI")
    print("  4. 仅构建 React")
    print("  5. 构建 React + 启动 FastAPI")
    print()
    
    choice = input("请选择 (1-5): ").strip()
    
    if choice == "1":
        if not react_built:
            print("\n❌ 错误: React 还未构建")
            print("请先运行: npm run build (在 frontend 目录)")
            sys.exit(1)
        start_fastapi_with_static()
        
    elif choice == "2":
        start_fastapi_with_dev_frontend()
        
    elif choice == "3":
        start_fastapi_only()
        
    elif choice == "4":
        build_react()
        
    elif choice == "5":
        build_react()
        time.sleep(2)
        start_fastapi_with_static()
        
    else:
        print("❌ 无效选择")
        sys.exit(1)

def start_fastapi_with_static():
    """启动 FastAPI，使用已构建的 React 静态文件"""
    print("\n🚀 启动 FastAPI (port 7860)...")
    print("   前端: http://localhost:7860")
    print("   API: http://localhost:7860/api")
    print("\n按 Ctrl+C 停止服务\n")
    
    os.chdir(os.path.join(os.path.dirname(__file__), "ai_rss_filter"))
    os.system("python api.py")

def start_fastapi_with_dev_frontend():
    """启动 FastAPI 后端和 React 开发服务器"""
    print("\n🚀 启动完整开发环境...")
    print()
    
    backend_dir = os.path.join(os.path.dirname(__file__), "ai_rss_filter")
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    # 启动后端
    print("📌 启动后端服务器 (FastAPI)...")
    print("   Port: 8000")
    backend_process = None
    
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "api.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("   ✓ 后端启动中...")
    except Exception as e:
        print(f"   ✗ 后端启动失败: {e}")
        return
    
    # 等待后端启动
    time.sleep(3)
    
    # 启动前端
    print("\n📌 启动前端开发服务器 (React)...")
    print("   Port: 3000")
    print("   浏览器会自动打开...")
    
    try:
        os.chdir(frontend_dir)
        if platform.system() == "Windows":
            os.system("npm start")
        else:
            subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        pass
    finally:
        if backend_process:
            backend_process.terminate()
            print("\n后端已停止")

def start_fastapi_only():
    """仅启动 FastAPI"""
    print("\n🚀 启动 FastAPI (port 8000)...")
    print("   API: http://localhost:8000")
    print("   文档: http://localhost:8000/docs")
    print("\n按 Ctrl+C 停止服务\n")
    
    os.chdir(os.path.join(os.path.dirname(__file__), "ai_rss_filter"))
    os.system(f"{sys.executable} api.py")

def build_react():
    """构建 React"""
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    print("\n🔨 构建 React...")
    os.chdir(frontend_dir)
    
    # 检查依赖
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("📌 安装依赖中...")
        if os.system("npm install") != 0:
            print("❌ npm install 失败")
            return False
    
    print("📌 构建项目中...")
    if os.system("npm run build") != 0:
        print("❌ 构建失败")
        return False
    
    print("✅ React 构建完成！")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已停止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
