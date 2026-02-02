"""Content Filter Module"""
import logging
from typing import List, Dict
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ContentFilter:
    """Filter articles based on quality and relevance criteria"""
    
    def __init__(self, config: Dict = None):
        """
        Initialize filter with configuration
        
        Args:
            config: Filter configuration with thresholds
        """
        self.config = config or {}
        self.confidence_threshold = self.config.get("confidence_threshold", 0.7)
        self.min_content_length = self.config.get("min_content_length", 50)
        self.quality_threshold = self.config.get("quality_threshold", 0.6)
        self.spam_threshold = self.config.get("spam_threshold", 0.4)
    
    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        """Filter articles based on multiple criteria"""
        filtered = []
        
        for article in articles:
            if self._is_quality_article(article):
                filtered.append(article)
        
        logger.info(f"Filtered: {len(articles)} -> {len(filtered)} articles")
        return filtered
    
    def _is_quality_article(self, article: Dict) -> bool:
        """Check if article meets quality criteria"""
        
        # Check content length
        content = article.get("content", "")
        if len(content) < self.min_content_length:
            logger.debug(f"Filtered out: content too short - {article.get('title')}")
            return False
        
        # Check classification scores
        classification = article.get("classification", {})
        
        quality_score = classification.get("quality_score", 0.5)
        spam_score = classification.get("spam_score", 0.5)
        confidence = classification.get("confidence", 0.0)
        
        # Apply thresholds
        if quality_score < self.quality_threshold:
            logger.debug(f"Filtered out: low quality ({quality_score:.2f}) - {article.get('title')}")
            return False
        
        if spam_score > self.spam_threshold:
            logger.debug(f"Filtered out: high spam score ({spam_score:.2f}) - {article.get('title')}")
            return False
        
        if confidence < self.confidence_threshold:
            logger.debug(f"Filtered out: low confidence ({confidence:.2f}) - {article.get('title')}")
            return False
        
        # Check for duplicate content
        if self._is_duplicate_title(article.get("title", "")):
            logger.debug(f"Filtered out: duplicate title - {article.get('title')}")
            return False
        
        return True
    
    def _is_duplicate_title(self, title: str) -> bool:
        """Check if title looks like a duplicate"""
        # Simple check for common duplicate patterns
        duplicate_patterns = [
            r'\[duplicate\]',
            r'\(repost\)',
            r'AGAIN',
            r'REPOST'
        ]
        
        for pattern in duplicate_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                return True
        
        return False
    
    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles by title/content"""
        seen = set()
        unique = []
        
        for article in articles:
            # Create a simple hash of title and source
            key = (article.get("title", "").lower(), article.get("source", ""))
            
            if key not in seen:
                seen.add(key)
                unique.append(article)
        
        logger.info(f"Deduplicated: {len(articles)} -> {len(unique)} articles")
        return unique
    
    def sort_by_score(self, articles: List[Dict], descending: bool = True) -> List[Dict]:
        """Sort articles by quality score"""
        def get_score(article):
            classification = article.get("classification", {})
            return classification.get("quality_score", 0.0)
        
        return sorted(articles, key=get_score, reverse=descending)
    
    def limit_articles(self, articles: List[Dict], limit: int = 10) -> List[Dict]:
        """Limit number of articles returned"""
        return articles[:limit]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test articles with classifications
    test_articles = [
        {
            "title": "Great Article",
            "content": "This is a very detailed and informative article about technology.",
            "source": "TechNews",
            "classification": {
                "quality_score": 0.8,
                "spam_score": 0.1,
                "confidence": 0.9
            }
        },
        {
            "title": "Buy Now!!!",
            "content": "Click here",
            "source": "Spam",
            "classification": {
                "quality_score": 0.2,
                "spam_score": 0.9,
                "confidence": 0.95
            }
        }
    ]
    
    filter_config = {
        "confidence_threshold": 0.7,
        "min_content_length": 50,
        "quality_threshold": 0.6,
        "spam_threshold": 0.4
    }
    
    content_filter = ContentFilter(filter_config)
    filtered = content_filter.filter_articles(test_articles)
    print(f"Filtered: {len(test_articles)} -> {len(filtered)} articles")
