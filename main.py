"""Main Application - RSS Noise Filter with AI Classification"""
import logging
import asyncio
import json
from typing import List, Dict
from datetime import datetime
import os
from dotenv import load_dotenv

# Import modules
from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier
from src.filter import ContentFilter
from src.notifier import NotificationManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/rss_filter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class RSSFilterApp:
    """Main application class"""
    
    def __init__(self, config_path: str = "config/rss_sources.json"):
        """Initialize the application"""
        logger.info("Initializing RSS Filter Application")
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Initialize components
        self.fetcher = RSSFetcher(config_path)
        self.classifier = TextClassifier(
            model_name=os.getenv("MODEL_NAME", "distilbert-base-uncased"),
            device=os.getenv("DEVICE", "cpu")
        )
        
        filter_config = {
            "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", 0.7)),
            "min_content_length": int(os.getenv("MIN_CONTENT_LENGTH", 50)),
            "quality_threshold": 0.6,
            "spam_threshold": float(os.getenv("SPAM_THRESHOLD", 0.4))
        }
        self.filter = ContentFilter(filter_config)
        self.notifier = NotificationManager()
        
        logger.info("Application initialized successfully")
    
    def run_once(self, notify: bool = True) -> List[Dict]:
        """Run the filter pipeline once"""
        logger.info("="*50)
        logger.info("Starting RSS filter pipeline")
        
        # Step 1: Fetch articles
        logger.info("Step 1: Fetching RSS feeds...")
        articles = self.fetcher.fetch_feeds()
        logger.info(f"Fetched {len(articles)} articles")
        
        if not articles:
            logger.warning("No articles fetched")
            return []
        
        # Step 2: Classify articles
        logger.info("Step 2: Classifying articles...")
        category_labels = ["valuable content", "advertisement", "clickbait", "spam"]
        articles = self.classifier.batch_classify(articles, category_labels)
        
        # Step 3: Filter articles
        logger.info("Step 3: Filtering articles...")
        filtered_articles = self.filter.filter_articles(articles)
        logger.info(f"Filtered to {len(filtered_articles)} quality articles")
        
        # Step 4: Deduplicate
        logger.info("Step 4: Deduplicating articles...")
        unique_articles = self.filter.deduplicate(filtered_articles)
        logger.info(f"After deduplication: {len(unique_articles)} articles")
        
        # Step 5: Sort by score
        logger.info("Step 5: Sorting articles by quality...")
        sorted_articles = self.filter.sort_by_score(unique_articles)
        
        # Step 6: Limit
        limited_articles = self.filter.limit_articles(sorted_articles, limit=10)
        logger.info(f"Final result: {len(limited_articles)} articles")
        
        # Step 7: Save results
        self._save_results(limited_articles)
        
        # Step 8: Send notifications
        if notify and limited_articles:
            logger.info("Step 8: Sending notifications...")
            asyncio.run(self.notifier.notify(
                limited_articles,
                use_telegram=True,
                use_email=True,
                digest=True
            ))
        
        logger.info("Pipeline completed successfully")
        logger.info("="*50)
        
        return limited_articles
    
    def _save_results(self, articles: List[Dict]):
        """Save filtered articles to JSON file"""
        try:
            output_file = f"data/filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Prepare data for JSON serialization
            json_articles = []
            for article in articles:
                json_article = {
                    "title": article.get("title"),
                    "content": article.get("content"),
                    "link": article.get("link"),
                    "source": article.get("source"),
                    "category": article.get("category"),
                    "published": article.get("published"),
                    "classification": article.get("classification", {})
                }
                json_articles.append(json_article)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_articles, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved results to {output_file}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def print_summary(self, articles: List[Dict]):
        """Print summary of filtered articles"""
        print("\n" + "="*60)
        print(f"📰 RSS FILTER SUMMARY - {len(articles)} Quality Articles Found")
        print("="*60 + "\n")
        
        for i, article in enumerate(articles, 1):
            classification = article.get("classification", {})
            quality = classification.get("quality_score", 0)
            spam = classification.get("spam_score", 0)
            
            print(f"{i}. {article.get('title')}")
            print(f"   📌 Source: {article.get('source')}")
            print(f"   ⭐ Quality: {quality:.0%} | 🚫 Spam: {spam:.0%}")
            print(f"   🔗 {article.get('link')}")
            print(f"   📝 {article.get('content')[:100]}...")
            print()


def main():
    """Main entry point"""
    try:
        app = RSSFilterApp()
        articles = app.run_once(notify=False)  # Set to True to send notifications
        app.print_summary(articles)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
