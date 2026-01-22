"""
使用示例 - USAGE EXAMPLES
"""

# ============ 示例 1：基础使用 ============
# 最简单的使用方式 - 立即运行并查看结果

from main import RSSFilterApp

app = RSSFilterApp()
articles = app.run_once(notify=False)  # 不发送通知
app.print_summary(articles)


# ============ 示例 2：自定义过滤参数 ============
# 调整过滤阈值

from src.filter import ContentFilter
from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier

fetcher = RSSFetcher()
classifier = TextClassifier()

# 自定义过滤配置 - 更严格
strict_config = {
    "confidence_threshold": 0.85,  # 只接收 85% 以上置信度的分类
    "min_content_length": 100,      # 最小 100 字符
    "quality_threshold": 0.75,      # 质量分数必须 > 75%
    "spam_threshold": 0.2            # 垃圾评分必须 < 20%
}

filter_obj = ContentFilter(strict_config)

# 运行流程
articles = fetcher.fetch_feeds()
articles = classifier.batch_classify(articles)
filtered = filter_obj.filter_articles(articles)
filtered = filter_obj.deduplicate(filtered)
sorted_articles = filter_obj.sort_by_score(filtered)
final = filter_obj.limit_articles(sorted_articles, limit=5)


# ============ 示例 3：仅使用特定类别 ============
# 只处理某些类别的 RSS 源

import json

# 加载配置
with open("config/rss_sources.json") as f:
    config = json.load(f)

# 只启用 tech 类别
for source in config["sources"]:
    source["enabled"] = source.get("category") == "tech"

# 保存修改后的配置
with open("config/rss_sources_tech_only.json", "w") as f:
    json.dump(config, f, indent=2)

# 使用自定义配置运行
fetcher = RSSFetcher("config/rss_sources_tech_only.json")
articles = fetcher.fetch_feeds()


# ============ 示例 4：自定义分类标签 ============
# 使用不同的分类标签

from src.text_classifier import TextClassifier

classifier = TextClassifier()

articles = [
    {
        "title": "New Python Library Released",
        "content": "A new Python library for data processing has been released with impressive features."
    }
]

# 自定义标签
custom_labels = [
    "高质量技术文章",
    "学习教程",
    "产品广告",
    "标题党新闻"
]

results = classifier.batch_classify(articles, category_labels=custom_labels)
for article in results:
    print(f"Title: {article['title']}")
    print(f"Classification: {article['classification']}")


# ============ 示例 5：发送 Telegram 通知 ============
# 发送过滤结果到 Telegram

import asyncio
from src.notifier import TelegramNotifier

notifier = TelegramNotifier()

# 发送单篇文章
async def send_article_example():
    article = {
        "title": "Important News",
        "content": "This is important breaking news...",
        "link": "https://example.com",
        "source": "TechNews",
        "classification": {"quality_score": 0.85}
    }
    await notifier.send_article(article)

# 运行
asyncio.run(send_article_example())

# 发送摘要
async def send_digest_example():
    articles = [
        {
            "title": "Article 1",
            "link": "https://example.com/1",
            "source": "Source1",
            "classification": {"quality_score": 0.8}
        },
        {
            "title": "Article 2",
            "link": "https://example.com/2",
            "source": "Source2",
            "classification": {"quality_score": 0.7}
        }
    ]
    await notifier.send_digest(articles, title="Daily News Digest")

asyncio.run(send_digest_example())


# ============ 示例 6：发送 Email 通知 ============
# 发送过滤结果到 Email

from src.notifier import EmailNotifier

notifier = EmailNotifier()

articles = [
    {
        "title": "Article 1",
        "content": "Article content here",
        "link": "https://example.com/1",
        "source": "Source1",
        "classification": {"quality_score": 0.8}
    }
]

if notifier.available:
    notifier.send_digest(articles, title="RSS Daily Digest")


# ============ 示例 7：添加新 RSS 源 ============
# 动态添加 RSS 源

import json

# 读取配置
with open("config/rss_sources.json") as f:
    config = json.load(f)

# 添加新源
new_source = {
    "name": "My Custom Feed",
    "url": "https://example.com/feed",
    "category": "tech",
    "enabled": True
}

config["sources"].append(new_source)

# 保存
with open("config/rss_sources.json", "w") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)


# ============ 示例 8：检查过滤统计 ============
# 分析过滤结果

from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier
from src.filter import ContentFilter

fetcher = RSSFetcher()
classifier = TextClassifier()
filter_obj = ContentFilter()

# 获取数据
articles = fetcher.fetch_feeds()
print(f"📊 Fetched: {len(articles)} articles")

# 分类
articles = classifier.batch_classify(articles)

# 统计分类结果
quality_scores = [a.get("classification", {}).get("quality_score", 0) for a in articles]
spam_scores = [a.get("classification", {}).get("spam_score", 0) for a in articles]

import statistics
print(f"📈 Quality score average: {statistics.mean(quality_scores):.2%}")
print(f"📈 Spam score average: {statistics.mean(spam_scores):.2%}")

# 过滤
filtered = filter_obj.filter_articles(articles)
print(f"✅ After filtering: {len(filtered)} articles ({len(filtered)/len(articles)*100:.1f}%)")


# ============ 示例 9：保存结果到不同格式 ============
# 导出过滤结果

import json
import csv
from datetime import datetime

articles = [
    {
        "title": "Article 1",
        "content": "Content",
        "link": "https://example.com",
        "source": "Source",
        "classification": {"quality_score": 0.8}
    }
]

# 保存为 JSON
with open("output.json", "w") as f:
    json.dump(articles, f, indent=2)

# 保存为 CSV
with open("output.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Source", "Quality", "Link"])
    for article in articles:
        writer.writerow([
            article["title"],
            article["source"],
            f"{article.get('classification', {}).get('quality_score', 0):.0%}",
            article["link"]
        ])


# ============ 示例 10：与第三方服务集成 ============
# 将结果发送到其他服务

# 示例：发送到 Slack
import requests

def send_to_slack(articles, webhook_url):
    for article in articles:
        message = {
            "text": f"{article['title']}",
            "attachments": [{
                "text": article["content"][:100],
                "title_link": article["link"],
                "fields": [
                    {"title": "Source", "value": article["source"], "short": True},
                    {"title": "Quality", "value": f"{article.get('classification', {}).get('quality_score', 0):.0%}", "short": True}
                ]
            }]
        }
        requests.post(webhook_url, json=message)

# send_to_slack(articles, "https://hooks.slack.com/services/YOUR/WEBHOOK/URL")


# 示例：保存到数据库
def save_to_database(articles):
    # 伪代码 - 根据你的数据库调整
    """
    for article in articles:
        db.articles.insert({
            "title": article["title"],
            "content": article["content"],
            "link": article["link"],
            "source": article["source"],
            "quality_score": article["classification"]["quality_score"],
            "created_at": datetime.now()
        })
    """
    pass
