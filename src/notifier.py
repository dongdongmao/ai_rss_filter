"""Notification Module for Telegram and Email"""
import logging
import os
import smtplib
from typing import List, Dict, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

try:
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Send notifications via Telegram"""
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID
        """
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram credentials not configured")
            self.available = False
        else:
            self.available = TELEGRAM_AVAILABLE
            if TELEGRAM_AVAILABLE:
                self.bot = Bot(token=self.bot_token)
    
    async def send_article(self, article: Dict) -> bool:
        """Send a single article to Telegram"""
        if not self.available:
            logger.warning("Telegram notifier not available")
            return False
        
        try:
            message = self._format_article_message(article)
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            logger.info(f"Sent article to Telegram: {article.get('title')}")
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
    
    async def send_digest(self, articles: List[Dict], title: str = "Daily Digest") -> bool:
        """Send digest of articles to Telegram"""
        if not self.available:
            logger.warning("Telegram notifier not available")
            return False
        
        try:
            message = self._format_digest_message(articles, title)
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            logger.info(f"Sent digest with {len(articles)} articles to Telegram")
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
    
    def _format_article_message(self, article: Dict) -> str:
        """Format article as Telegram message"""
        title = article.get("title", "")
        link = article.get("link", "")
        source = article.get("source", "Unknown")
        content = article.get("content", "")[:200]
        
        quality = article.get("classification", {}).get("quality_score", 0)
        
        message = (
            f"<b>{title}</b>\n\n"
            f"{content}...\n\n"
            f"📰 Source: {source}\n"
            f"⭐ Quality: {quality:.0%}\n"
            f"<a href='{link}'>Read More</a>"
        )
        return message
    
    def _format_digest_message(self, articles: List[Dict], title: str) -> str:
        """Format digest as Telegram message"""
        message = f"<b>{title}</b>\n\n"
        
        for i, article in enumerate(articles, 1):
            article_title = article.get("title", "")
            link = article.get("link", "")
            quality = article.get("classification", {}).get("quality_score", 0)
            
            message += f"{i}. <a href='{link}'>{article_title}</a> ({quality:.0%})\n"
        
        message += f"\n✅ Total: {len(articles)} articles"
        return message


class EmailNotifier:
    """Send notifications via Email"""
    
    def __init__(self, 
                 sender: str = None,
                 password: str = None,
                 recipient: str = None,
                 smtp_server: str = "smtp.gmail.com",
                 smtp_port: int = 587):
        """
        Initialize Email notifier
        
        Args:
            sender: Sender email address
            password: Email password or app password
            recipient: Recipient email address
            smtp_server: SMTP server address
            smtp_port: SMTP port
        """
        self.sender = sender or os.getenv("EMAIL_SENDER")
        self.password = password or os.getenv("EMAIL_PASSWORD")
        self.recipient = recipient or os.getenv("EMAIL_RECIPIENT")
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
        self.available = bool(self.sender and self.password and self.recipient)
    
    def send_digest(self, articles: List[Dict], title: str = "Daily Digest") -> bool:
        """Send digest of articles via email"""
        if not self.available:
            logger.warning("Email notifier not configured")
            return False
        
        try:
            message = self._create_email_message(articles, title)
            self._send_email(message)
            logger.info(f"Sent email digest with {len(articles)} articles")
            return True
        except Exception as e:
            logger.error(f"Email error: {e}")
            return False
    
    def _create_email_message(self, articles: List[Dict], title: str) -> MIMEMultipart:
        """Create email message"""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = title
        msg["From"] = self.sender
        msg["To"] = self.recipient
        
        # Create plain text and HTML versions
        text_content = self._format_digest_text(articles, title)
        html_content = self._format_digest_html(articles, title)
        
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))
        
        return msg
    
    def _format_digest_text(self, articles: List[Dict], title: str) -> str:
        """Format digest as plain text"""
        text = f"{title}\n{'='*50}\n\n"
        
        for i, article in enumerate(articles, 1):
            text += f"{i}. {article.get('title')}\n"
            text += f"   Source: {article.get('source')}\n"
            text += f"   Link: {article.get('link')}\n"
            text += f"   Quality: {article.get('classification', {}).get('quality_score', 0):.0%}\n\n"
        
        return text
    
    def _format_digest_html(self, articles: List[Dict], title: str) -> str:
        """Format digest as HTML"""
        html = f"""
        <html>
            <head></head>
            <body>
                <h2>{title}</h2>
        """
        
        for i, article in enumerate(articles, 1):
            quality = article.get('classification', {}).get('quality_score', 0)
            html += f"""
                <div style="margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50;">
                    <h3><a href="{article.get('link')}">{article.get('title')}</a></h3>
                    <p>{article.get('content')[:200]}...</p>
                    <small>
                        <b>Source:</b> {article.get('source')} | 
                        <b>Quality:</b> {quality:.0%}
                    </small>
                </div>
            """
        
        html += """
            </body>
        </html>
        """
        return html
    
    def _send_email(self, message: MIMEMultipart):
        """Send email via SMTP"""
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(message)


class NotificationManager:
    """Manage multiple notification channels"""
    
    def __init__(self):
        self.telegram = TelegramNotifier() if TELEGRAM_AVAILABLE else None
        self.email = EmailNotifier()
    
    async def notify(self, articles: List[Dict], 
                     use_telegram: bool = True,
                     use_email: bool = False,
                     digest: bool = True):
        """Send notifications through configured channels"""
        
        if use_telegram and self.telegram and self.telegram.available:
            if digest:
                await self.telegram.send_digest(articles, "RSS Feed Summary")
            else:
                for article in articles:
                    await self.telegram.send_article(article)
        
        if use_email and self.email and self.email.available:
            self.email.send_digest(articles, "RSS Feed Daily Digest")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test email notifier (Telegram requires async)
    test_articles = [
        {
            "title": "Article 1",
            "content": "This is a test article",
            "link": "https://example.com/1",
            "source": "Test Source",
            "classification": {"quality_score": 0.85}
        }
    ]
    
    email_notifier = EmailNotifier()
    if not email_notifier.available:
        print("Email notifier not configured. Set EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT env vars")
