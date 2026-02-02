"""AI Text Classification Module using Hugging Face Transformers"""
import logging
from typing import Dict, Tuple, List
import os
from transformers import pipeline
import torch

logger = logging.getLogger(__name__)


class TextClassifier:
    """Classify articles using pre-trained NLP models"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased", device: str = None):
        """
        Initialize classifier
        
        Args:
            model_name: Hugging Face model name
            device: cuda or cpu (auto-detect if None)
        """
        if device is None:
            self.device = 0 if torch.cuda.is_available() else -1
        else:
            self.device = 0 if device.lower() == "cuda" else -1
        
        self.model_name = model_name
        self.classifier = None
        self._load_model()
        
        # Custom keywords for quality filtering
        self.ad_keywords = [
            "advertisement", "sponsored", "ad", "click here", "buy now",
            "limited offer", "promotion", "coupon", "discount code",
            "click to view", "clickbait", "shocking", "you won't believe"
        ]
        
        self.quality_keywords = [
            "research", "study", "analysis", "report", "investigation",
            "breakthrough", "innovation", "technical", "benchmark",
            "performance", "comparison", "tutorial", "guide"
        ]
    
    def _load_model(self):
        """Load the pre-trained model"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.classifier = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=self.device
            )
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def classify_article(
        self, 
        title: str, 
        content: str,
        category_labels: List[str] = None
    ) -> Dict:
        """
        Classify an article
        
        Args:
            title: Article title
            content: Article content/summary
            category_labels: List of category labels for classification
        
        Returns:
            Classification result with scores
        """
        if category_labels is None:
            category_labels = ["valuable", "advertisement", "clickbait"]
        
        text = f"{title}. {content}"[:512]  # Limit to 512 chars for efficiency
        
        try:
            # Get classification result
            result = self.classifier(text, category_labels, multi_class=False)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(title, content, result)
            
            # Detect spam/ads
            spam_score = self._detect_spam(title, content)
            
            return {
                "category": result["labels"][0],
                "confidence": result["scores"][0],
                "all_scores": dict(zip(result["labels"], result["scores"])),
                "quality_score": quality_score,
                "spam_score": spam_score,
                "is_quality": quality_score > 0.6 and spam_score < 0.4
            }
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {
                "category": "unknown",
                "confidence": 0.0,
                "all_scores": {},
                "quality_score": 0.5,
                "spam_score": 0.5,
                "is_quality": False
            }
    
    def _calculate_quality_score(self, title: str, content: str, result: Dict) -> float:
        """Calculate article quality score"""
        text = f"{title} {content}".lower()
        
        # Base score from classifier
        base_score = result["scores"][0]
        
        # Bonus for quality keywords
        quality_bonus = sum(0.1 for kw in self.quality_keywords if kw in text) * 0.1
        
        # Penalty for ad keywords
        ad_penalty = sum(0.1 for kw in self.ad_keywords if kw in text) * 0.1
        
        # Content length bonus (minimum 50 chars)
        length_bonus = 0.1 if len(content) > 100 else 0
        
        final_score = min(1.0, max(0.0, base_score + quality_bonus - ad_penalty + length_bonus))
        return final_score
    
    def _detect_spam(self, title: str, content: str) -> float:
        """Detect spam/advertisement content"""
        text = f"{title} {content}".lower()
        
        # Count ad keywords
        ad_count = sum(1 for kw in self.ad_keywords if kw in text)
        
        # Exclamation mark ratio
        exclamation_ratio = text.count("!") / max(len(text.split()), 1)
        
        # Question mark ratio (often used in clickbait)
        question_ratio = text.count("?") / max(len(text.split()), 1)
        
        spam_score = min(1.0, (ad_count * 0.3 + exclamation_ratio * 0.2 + question_ratio * 0.2))
        return spam_score
    
    def batch_classify(
        self, 
        articles: List[Dict],
        category_labels: List[str] = None
    ) -> List[Dict]:
        """Classify multiple articles"""
        results = []
        for article in articles:
            classification = self.classify_article(
                article.get("title", ""),
                article.get("content", ""),
                category_labels
            )
            article["classification"] = classification
            results.append(article)
        return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    classifier = TextClassifier()
    
    # Test samples
    test_articles = [
        {
            "title": "New BERT Model Achieves State-of-the-Art Performance",
            "content": "Researchers published a breakthrough in NLP with a new transformer architecture that outperforms existing models on multiple benchmarks."
        },
        {
            "title": "You Won't Believe This One Weird Trick!",
            "content": "Click here for exclusive offer. Limited time only! Buy now and save 50%."
        },
        {
            "title": "Comprehensive Analysis of Machine Learning Frameworks",
            "content": "A detailed technical comparison of TensorFlow, PyTorch, and JAX for production workloads."
        }
    ]
    
    for article in test_articles:
        result = classifier.classify_article(article["title"], article["content"])
        print(f"\nTitle: {article['title']}")
        print(f"Result: {result}")
