"""RSS Feed Fetcher Module"""
import feedparser
import logging
from typing import List, Dict, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class RSSFetcher:
    """Fetch and parse RSS feeds"""
    
    def __init__(self, config_path: str = "config/rss_sources.json"):
        self.config = self._load_config(config_path)
        self.sources = self.config.get("sources", [])
    
    def _load_config(self, config_path: str) -> Dict:
        """Load RSS sources configuration"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {"sources": [], "categories": {}}
    
    def fetch_feeds(self) -> List[Dict]:
        """Fetch all enabled RSS feeds"""
        articles = []
        
        for source in self.sources:
            if not source.get("enabled", True):
                continue
            
            try:
                articles.extend(self._fetch_single_feed(source))
            except Exception as e:
                logger.error(f"Error fetching {source['name']}: {e}")
        
        return articles
    
    def _fetch_single_feed(self, source: Dict) -> List[Dict]:
        """Fetch a single RSS feed"""
        feed = feedparser.parse(source["url"])
        articles = []
        
        if feed.bozo:
            logger.warning(f"Feed parsing warning for {source['name']}: {feed.bozo_exception}")
        
        for entry in feed.entries[:100]:  # Limit to 30 latest entries per source
            article = {
                "title": entry.get("title", ""),
                "content": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": source["name"],
                "category": source.get("category", "general"),
                "author": entry.get("author", "Unknown")
            }
            
            # Skip if title or content is too short
            if len(article["title"]) > 5 and len(article["content"]) > 20:
                articles.append(article)
        
        logger.info(f"Fetched {len(articles)} articles from {source['name']}")
        return articles
    
    def get_active_categories(self) -> List[str]:
        """Get list of active categories"""
        categories = set()
        for source in self.sources:
            if source.get("enabled", True):
                categories.add(source.get("category", "general"))
        return list(categories)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fetcher = RSSFetcher()
    articles = fetcher.fetch_feeds()
    print(f"Fetched {len(articles)} articles")
    for article in articles[:3]:
        print(f"- {article['title']}")
