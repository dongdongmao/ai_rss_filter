"""Tests for RSS Filter components"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier
from src.filter import ContentFilter


class TestRSSFetcher(unittest.TestCase):
    """Test RSS fetcher"""
    
    def setUp(self):
        self.fetcher = RSSFetcher("config/rss_sources.json")
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.assertIn("sources", self.fetcher.config)
        self.assertGreater(len(self.fetcher.sources), 0)
    
    def test_active_categories(self):
        """Test getting active categories"""
        categories = self.fetcher.get_active_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)


class TestTextClassifier(unittest.TestCase):
    """Test text classifier"""
    
    def setUp(self):
        # Use smaller model for testing
        self.classifier = TextClassifier(model_name="distilbert-base-uncased")
    
    def test_classify_valuable_content(self):
        """Test classification of valuable content"""
        title = "New Deep Learning Research Breakthrough"
        content = "Researchers published a groundbreaking study on neural networks with state-of-the-art results."
        
        result = self.classifier.classify_article(title, content)
        
        self.assertIn("category", result)
        self.assertIn("confidence", result)
        self.assertIn("quality_score", result)
        self.assertIn("spam_score", result)
        self.assertGreater(result["quality_score"], 0.5)
    
    def test_classify_advertisement(self):
        """Test classification of advertisement"""
        title = "Buy Now! Limited Offer!!!"
        content = "Click here for exclusive discount. Limited time only!"
        
        result = self.classifier.classify_article(title, content)
        
        self.assertGreater(result["spam_score"], 0.3)
    
    def test_batch_classify(self):
        """Test batch classification"""
        articles = [
            {
                "title": "Article 1",
                "content": "This is quality content about technology"
            },
            {
                "title": "Article 2",
                "content": "This is another article"
            }
        ]
        
        results = self.classifier.batch_classify(articles)
        
        self.assertEqual(len(results), len(articles))
        for result in results:
            self.assertIn("classification", result)


class TestContentFilter(unittest.TestCase):
    """Test content filter"""
    
    def setUp(self):
        self.filter = ContentFilter({
            "confidence_threshold": 0.7,
            "min_content_length": 50,
            "quality_threshold": 0.6,
            "spam_threshold": 0.4
        })
    
    def test_filter_quality_article(self):
        """Test filtering quality article"""
        article = {
            "title": "Good Article",
            "content": "This is a long and detailed article about interesting topics.",
            "classification": {
                "quality_score": 0.8,
                "spam_score": 0.1,
                "confidence": 0.9
            }
        }
        
        is_quality = self.filter._is_quality_article(article)
        self.assertTrue(is_quality)
    
    def test_filter_spam_article(self):
        """Test filtering spam article"""
        article = {
            "title": "CLICK HERE",
            "content": "Buy now",
            "classification": {
                "quality_score": 0.2,
                "spam_score": 0.9,
                "confidence": 0.95
            }
        }
        
        is_quality = self.filter._is_quality_article(article)
        self.assertFalse(is_quality)
    
    def test_deduplication(self):
        """Test article deduplication"""
        articles = [
            {"title": "Article A", "source": "Source 1"},
            {"title": "Article A", "source": "Source 1"},  # duplicate
            {"title": "Article B", "source": "Source 2"}
        ]
        
        unique = self.filter.deduplicate(articles)
        self.assertEqual(len(unique), 2)
    
    def test_sorting(self):
        """Test article sorting"""
        articles = [
            {"title": "A", "classification": {"quality_score": 0.5}},
            {"title": "B", "classification": {"quality_score": 0.9}},
            {"title": "C", "classification": {"quality_score": 0.3}}
        ]
        
        sorted_articles = self.filter.sort_by_score(articles, descending=True)
        
        scores = [a["classification"]["quality_score"] for a in sorted_articles]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
