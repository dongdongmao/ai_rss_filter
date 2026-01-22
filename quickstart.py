"""
Quick Start Guide - 快速开始指南

这个脚本会引导你快速配置和运行 RSS 过滤器。
"""

import os
import json
import sys
from pathlib import Path


def print_header(text):
    """打印标题"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def create_env_file():
    """创建 .env 文件"""
    print_header("1️⃣  配置环境变量")
    
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env 文件已存在")
        return
    
    print("\n请按照以下步骤获取配置信息：\n")
    
    print("【Telegram 配置】")
    print("1. 在 Telegram 中搜索 @BotFather")
    print("2. 发送 /newbot 命令")
    print("3. 按提示设置 Bot 名称")
    print("4. 复制生成的 Token\n")
    
    bot_token = input("请输入你的 Telegram Bot Token (可选，按Enter跳过): ").strip()
    
    if bot_token:
        print("\n现在获取 Chat ID:")
        print("1. 向你的 Bot 发送任意消息")
        print("2. 访问: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates")
        print("3. 找到 response[0].message.chat.id\n")
        chat_id = input("请输入你的 Telegram Chat ID: ").strip()
    else:
        chat_id = ""
    
    # Email 配置
    print("\n【Email 配置（可选）】")
    email_sender = input("请输入发件邮箱 (可选，按Enter跳过): ").strip()
    
    if email_sender:
        email_password = input("请输入邮箱密码或应用密码: ").strip()
        email_recipient = input("请输入收件邮箱: ").strip()
    else:
        email_password = ""
        email_recipient = ""
    
    # 创建 .env 文件
    env_content = f"""# Telegram Configuration
TELEGRAM_BOT_TOKEN={bot_token or 'your_bot_token_here'}
TELEGRAM_CHAT_ID={chat_id or 'your_chat_id_here'}

# Email Configuration (Optional)
EMAIL_SENDER={email_sender or 'your_email@gmail.com'}
EMAIL_PASSWORD={email_password or 'your_app_password'}
EMAIL_RECIPIENT={email_recipient or 'recipient@example.com'}

# Model Configuration
MODEL_NAME=distilbert-base-uncased
DEVICE=cpu  # Change to 'cuda' if you have GPU

# Filter Configuration
CONFIDENCE_THRESHOLD=0.7
MIN_CONTENT_LENGTH=50
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ .env 文件已创建")


def check_rss_sources():
    """检查 RSS 源配置"""
    print_header("2️⃣  检查 RSS 源配置")
    
    config_path = Path("config/rss_sources.json")
    if not config_path.exists():
        print("⚠️  config/rss_sources.json 不存在")
        return
    
    with open(config_path) as f:
        config = json.load(f)
    
    sources = config.get("sources", [])
    print(f"\n📰 已配置 {len(sources)} 个 RSS 源:\n")
    
    for i, source in enumerate(sources, 1):
        status = "✅" if source.get("enabled") else "❌"
        print(f"  {status} {i}. {source['name']} ({source['category']})")
    
    add_more = input("\n要添加更多 RSS 源吗? (y/n): ").strip().lower()
    if add_more == 'y':
        print("\n编辑 config/rss_sources.json 来添加新的 RSS 源")


def install_dependencies():
    """安装依赖"""
    print_header("3️⃣  安装依赖")
    
    print("\n开始安装依赖包，这可能需要几分钟...\n")
    
    os.system("pip install -r requirements.txt")
    
    print("\n✅ 依赖安装完成")


def test_configuration():
    """测试配置"""
    print_header("4️⃣  测试配置")
    
    print("\n测试各模块...\n")
    
    try:
        print("  正在加载 RSS 爬虫...", end="", flush=True)
        from src.rss_fetcher import RSSFetcher
        fetcher = RSSFetcher()
        print(" ✅")
        
        print("  正在加载 AI 分类器...", end="", flush=True)
        from src.text_classifier import TextClassifier
        classifier = TextClassifier()
        print(" ✅")
        
        print("  正在加载 过滤器...", end="", flush=True)
        from src.filter import ContentFilter
        filter_obj = ContentFilter()
        print(" ✅")
        
        print("  正在加载 通知器...", end="", flush=True)
        from src.notifier import NotificationManager
        notifier = NotificationManager()
        print(" ✅")
        
        print("\n✅ 所有模块加载成功!")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False
    
    return True


def run_first_time():
    """首次运行"""
    print_header("5️⃣  首次运行")
    
    print("\n即将运行 RSS 过滤器...\n")
    
    try:
        from main import RSSFilterApp
        
        app = RSSFilterApp()
        print("⏳ 正在处理... 这可能需要一分钟\n")
        
        articles = app.run_once(notify=False)
        app.print_summary(articles)
        
        if articles:
            print("\n✅ 成功! 过滤器工作正常")
            
            send_notifications = input("\n要现在发送测试通知吗? (y/n): ").strip().lower()
            if send_notifications == 'y':
                import asyncio
                asyncio.run(app.notifier.notify(
                    articles,
                    use_telegram=True,
                    use_email=True,
                    digest=True
                ))
                print("✅ 通知已发送!")
        else:
            print("\n⚠️  未找到高质量文章。可能是 RSS 源需要更新。")
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n请检查配置并重试。")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("  🤖 私人 RSS 降噪器 - 快速配置向导")
    print("="*60)
    
    print("\n这个向导将帮助你快速配置和运行 RSS 过滤器。\n")
    
    steps = [
        ("配置环境变量", create_env_file),
        ("检查 RSS 源", check_rss_sources),
        ("安装依赖", install_dependencies),
        ("测试配置", test_configuration),
        ("首次运行", run_first_time),
    ]
    
    for i, (name, func) in enumerate(steps, 1):
        try:
            func()
        except KeyboardInterrupt:
            print("\n\n⚠️  被用户中断")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            cont = input("是否继续? (y/n): ").strip().lower()
            if cont != 'y':
                sys.exit(1)
    
    print_header("🎉 配置完成!")
    
    print("""
下一步：

1. 【定时运行】
   python scheduler.py
   
2. 【手动运行】
   python main.py
   
3. 【立即测试推送】
   python scheduler.py now

更多信息请查看 README.md

祝你使用愉快！✨
""")


if __name__ == "__main__":
    main()
