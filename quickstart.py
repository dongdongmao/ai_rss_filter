"""
Quick Start Guide - Quick Setup Guide

This script will guide you through quick configuration and running the RSS filter.
"""

import os
import json
import sys
from pathlib import Path


def print_header(text):
    """Print header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def create_env_file():
    """Create .env file"""
    print_header("1️⃣  Configure Environment Variables")
    
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env file already exists")
        return
    
    print("\nPlease follow these steps to get configuration info:\n")
    
    print("【Telegram Configuration】")
    print("1. Search for @BotFather in Telegram")
    print("2. Send /newbot command")
    print("3. Follow prompts to set Bot name")
    print("4. Copy the generated Token\n")
    
    bot_token = input("Enter your Telegram Bot Token (optional, press Enter to skip): ").strip()
    
    if bot_token:
        print("\nNow get Chat ID:")
        print("1. Send any message to your Bot")
        print("2. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates")
        print("3. Find response[0].message.chat.id\n")
        chat_id = input("Enter your Telegram Chat ID: ").strip()
    else:
        chat_id = ""
    
    # Email Configuration
    print("\n【Email Configuration (Optional)】")
    email_sender = input("Enter sender email (optional, press Enter to skip): ").strip()
    
    if email_sender:
        email_password = input("Enter email password or app password: ").strip()
        email_recipient = input("Enter recipient email: ").strip()
    else:
        email_password = ""
        email_recipient = ""
    
    # Create .env file
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
    
    print("✅ .env file created")


def check_rss_sources():
    """Check RSS sources configuration"""
    print_header("2️⃣  Check RSS Sources Configuration")
    
    config_path = Path("config/rss_sources.json")
    if not config_path.exists():
        print("⚠️  config/rss_sources.json not found")
        return
    
    with open(config_path) as f:
        config = json.load(f)
    
    sources = config.get("sources", [])
    print(f"\n📰 {len(sources)} RSS sources configured:\n")
    
    for i, source in enumerate(sources, 1):
        status = "✅" if source.get("enabled") else "❌"
        print(f"  {status} {i}. {source['name']} ({source['category']})")
    
    add_more = input("\nWant to add more RSS sources? (y/n): ").strip().lower()
    if add_more == 'y':
        print("\nEdit config/rss_sources.json to add new RSS sources")


def install_dependencies():
    """Install dependencies"""
    print_header("3️⃣  Install Dependencies")
    
    print("\nStarting installation of dependency packages, this may take a few minutes...\n")
    
    os.system("pip install -r requirements.txt")
    
    print("\n✅ Dependencies installed successfully")


def test_configuration():
    """Test configuration"""
    print_header("4️⃣  Test Configuration")
    
    print("\nTesting all modules...\n")
    
    try:
        print("  Loading RSS fetcher...", end="", flush=True)
        from src.rss_fetcher import RSSFetcher
        fetcher = RSSFetcher()
        print(" ✅")
        
        print("  Loading AI classifier...", end="", flush=True)
        from src.text_classifier import TextClassifier
        classifier = TextClassifier()
        print(" ✅")
        
        print("  Loading filter...", end="", flush=True)
        from src.filter import ContentFilter
        filter_obj = ContentFilter()
        print(" ✅")
        
        print("  Loading notifier...", end="", flush=True)
        from src.notifier import NotificationManager
        notifier = NotificationManager()
        print(" ✅")
        
        print("\n✅ All modules loaded successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True


def run_first_time():
    """First run"""
    print_header("5️⃣  First Run")
    
    print("\nAbout to run RSS filter...\n")
    
    try:
        from main import RSSFilterApp
        
        app = RSSFilterApp()
        print("⏳ Processing... This may take a minute\n")
        
        articles = app.run_once(notify=False)
        app.print_summary(articles)
        
        if articles:
            print("\n✅ Success! Filter is working correctly")
            
            send_notifications = input("\nSend test notification now? (y/n): ").strip().lower()
            if send_notifications == 'y':
                import asyncio
                asyncio.run(app.notifier.notify(
                    articles,
                    use_telegram=True,
                    use_email=True,
                    digest=True
                ))
                print("✅ Notification sent!")
        else:
            print("\n⚠️  No high-quality articles found. RSS sources may need updating.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease check configuration and try again.")


def main():
    """Main function"""
    print("\n" + "="*60)
    print("  🤖 Personal RSS Denoiser - Quick Setup Wizard")
    print("="*60)
    
    print("\nThis wizard will help you quickly configure and run the RSS filter.\n")
    
    steps = [
        ("Configure environment variables", create_env_file),
        ("Check RSS sources", check_rss_sources),
        ("Install dependencies", install_dependencies),
        ("Test configuration", test_configuration),
        ("First run", run_first_time),
    ]
    
    for i, (name, func) in enumerate(steps, 1):
        try:
            func()
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            cont = input("Continue? (y/n): ").strip().lower()
            if cont != 'y':
                sys.exit(1)
    
    print_header("🎉 Setup Complete!")
    
    print("""
Next steps:

1. 【Scheduled Run】
   python scheduler.py
   
2. 【Manual Run】
   python main.py
   
3. 【Test Push Immediately】
   python scheduler.py now

For more information, see README.md

Enjoy! ✨
""")


if __name__ == "__main__":
    main()
