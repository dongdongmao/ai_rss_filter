"""FastAPI backend for RSS Filter"""
import os
import json
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import asyncio

logger = logging.getLogger(__name__)

from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier
from src.filter import ContentFilter

load_dotenv()

app = FastAPI(title="RSS Filter API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend build directory (relative to api.py location)
FRONTEND_BUILD_DIR = os.path.join(os.path.dirname(__file__), "frontend", "build")
FRONTEND_AVAILABLE = os.path.exists(FRONTEND_BUILD_DIR)

# Initialize components
try:
    fetcher = RSSFetcher()
    classifier = TextClassifier(
        model_name=os.getenv("MODEL_NAME", "distilbert-base-uncased"),
        device=os.getenv("DEVICE", "cpu")
    )
    content_filter = ContentFilter({
        "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", 0.7)),
        "min_content_length": int(os.getenv("MIN_CONTENT_LENGTH", 50)),
        "quality_threshold": 0.6,
        "spam_threshold": float(os.getenv("SPAM_THRESHOLD", 0.4))
    })
except Exception as e:
    print(f"Error initializing components: {e}")
    fetcher = None
    classifier = None
    content_filter = None

# Request/Response Models
class FilterRequest(BaseModel):
    topics: List[str] = []  # Selected topic ids (e.g. tech, ai). Empty = all topics.
    max_articles: int = 10

class FilterResponse(BaseModel):
    status: str
    total_fetched: int
    filtered_count: int
    final_count: int
    articles: list

class ConfigResponse(BaseModel):
    sources: list
    categories: list  # Available topics from config (e.g. tech, ai, crypto)
    model_name: str
    device: str

class ManualArticleInput(BaseModel):
    title: str
    content: str
    link: str = ""
    source: str = "Manual Input"

class ManualFilterRequest(BaseModel):
    articles: List[ManualArticleInput]
    max_articles: int = 10

# API Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "message": "RSS Filter API is running",
        "frontend_available": FRONTEND_AVAILABLE,
        "components_initialized": all([fetcher, classifier, content_filter])
    }

@app.get("/api/config")
async def get_config() -> ConfigResponse:
    """Get current configuration including available topics"""
    try:
        with open("config/rss_sources.json") as f:
            config = json.load(f)
        
        sources = config.get("sources", [])
        # Topics = category keys from config + unique categories from sources
        category_keys = list(config.get("categories", {}).keys())
        source_cats = {s.get("category", "general") for s in sources if s.get("category")}
        categories = sorted(set(category_keys) | source_cats)
        
        return ConfigResponse(
            sources=sources,
            categories=categories,
            model_name=os.getenv("MODEL_NAME", "distilbert-base-uncased"),
            device=os.getenv("DEVICE", "cpu")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _get_demo_articles():
    """Generate demo articles for Hugging Face Spaces (when network is unavailable)"""
    return [
        {"title": "New AI Breakthrough in Natural Language Processing", "content": "Researchers have developed a new transformer architecture that significantly improves understanding of context in long-form text.", "link": "https://example.com/ai-breakthrough", "source": "Tech News Demo", "category": "ai"},
        {"title": "Open Source Framework Simplifies Machine Learning Deployment", "content": "A new open-source framework makes it easier for developers to deploy machine learning models to production.", "link": "https://example.com/ml-framework", "source": "Developer Blog Demo", "category": "tech"},
        {"title": "CLICK HERE FOR AMAZING DEALS!!!", "content": "Buy now! Limited time offer! Click here for exclusive discounts.", "link": "https://example.com/ads", "source": "Advertisement Demo", "category": "tech"},
        {"title": "Deep Dive: Understanding Neural Network Architectures", "content": "This comprehensive guide explores different neural network architectures.", "link": "https://example.com/neural-networks", "source": "Educational Content Demo", "category": "ai"},
        {"title": "You Won't Believe What Happened Next!", "content": "Shocking results! This one weird trick will change everything.", "link": "https://example.com/clickbait", "source": "Clickbait Demo", "category": "tech"},
        {"title": "Best Practices for Code Review in Large Teams", "content": "Effective code review processes are essential for maintaining code quality in large development teams.", "link": "https://example.com/code-review", "source": "Engineering Blog Demo", "category": "tech"},
        {"title": "FREE MONEY!!! CLICK NOW!!!", "content": "Get rich quick! No investment required!", "link": "https://example.com/spam", "source": "Spam Demo", "category": "tech"},
        {"title": "Introduction to Rust: Memory Safety Without Garbage Collection", "content": "Rust is a systems programming language that provides memory safety guarantees.", "link": "https://example.com/rust-tutorial", "source": "Programming Tutorial Demo", "category": "tech"}
    ]

@app.post("/api/filter")
async def run_filter(request: FilterRequest) -> FilterResponse:
    """Run RSS filter; optionally restrict by selected topics."""
    try:
        # Step 1: Fetch articles
        try:
            if fetcher is not None:
                articles = fetcher.fetch_feeds()
            else:
                articles = []
            total_fetched = len(articles)
            if not articles:
                articles = _get_demo_articles()
                total_fetched = len(articles)
        except Exception as e:
            logger.warning(f"Failed to fetch RSS feeds (network may be unavailable): {e}")
            articles = _get_demo_articles()
            total_fetched = len(articles)
        
        # Filter by selected topics (category) if any; if that would leave 0, show all
        if request.topics:
            topics_set = set(t.lower() for t in request.topics)
            by_topic = [a for a in articles if (a.get("category") or "general").lower() in topics_set]
            if by_topic:
                articles = by_topic
            # else: keep all articles so we always show something when we have data
        
        if not articles:
            return FilterResponse(
                status="no_articles",
                total_fetched=0,
                filtered_count=0,
                final_count=0,
                articles=[]
            )
        
        # Step 2: Classify articles (skip if classifier failed to load; use default scores)
        category_labels = ["valuable content", "advertisement", "clickbait", "spam"]
        if classifier is not None:
            articles = classifier.batch_classify(articles, category_labels)
        else:
            for a in articles:
                a["classification"] = {"quality_score": 0.7, "spam_score": 0.2, "confidence": 0.8}
        
        # Step 3: Filter articles (pass-through, no dropping)
        filtered = content_filter.filter_articles(articles) if content_filter else articles
        filtered_count = len(filtered)
        
        # Step 4: Deduplicate
        unique = content_filter.deduplicate(filtered) if content_filter else filtered
        
        # Step 5: Sort by score
        sorted_articles = content_filter.sort_by_score(unique) if content_filter else unique
        
        # Step 6: Limit
        final = content_filter.limit_articles(sorted_articles, limit=request.max_articles) if content_filter else sorted_articles[:request.max_articles]
        
        # Format response
        formatted_articles = []
        for article in final:
            classification = article.get("classification", {})
            formatted_articles.append({
                "title": article.get("title"),
                "content": article.get("content"),
                "link": article.get("link"),
                "source": article.get("source"),
                "topic": article.get("category", "general"),
                "quality_score": round(classification.get("quality_score", 0), 3),
                "spam_score": round(classification.get("spam_score", 0), 3),
                "confidence": round(classification.get("confidence", 0), 3)
            })
        
        return FilterResponse(
            status="success",
            total_fetched=total_fetched,
            filtered_count=filtered_count,
            final_count=len(final),
            articles=formatted_articles
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/filter/manual")
async def run_filter_manual(request: ManualFilterRequest) -> FilterResponse:
    """Run filter on manually provided articles (uses server default thresholds)"""
    try:
        # Convert manual input to article format
        articles = []
        for article_input in request.articles:
            articles.append({
                "title": article_input.title,
                "content": article_input.content,
                "link": article_input.link,
                "source": article_input.source,
                "category": "manual"
            })
        
        total_fetched = len(articles)
        
        if not articles:
            return FilterResponse(
                status="no_articles",
                total_fetched=0,
                filtered_count=0,
                final_count=0,
                articles=[]
            )
        
        # Step 2: Classify articles (skip if classifier failed)
        category_labels = ["valuable content", "advertisement", "clickbait", "spam"]
        if classifier is not None:
            articles = classifier.batch_classify(articles, category_labels)
        else:
            for a in articles:
                a["classification"] = {"quality_score": 0.7, "spam_score": 0.2, "confidence": 0.8}
        
        # Step 3: Filter articles (currently pass-through)
        filtered = content_filter.filter_articles(articles) if content_filter else articles
        filtered_count = len(filtered)
        
        # Step 4: Deduplicate
        unique = content_filter.deduplicate(filtered) if content_filter else filtered
        
        # Step 5: Sort by score
        sorted_articles = content_filter.sort_by_score(unique) if content_filter else unique
        
        # Step 6: Limit
        final = content_filter.limit_articles(sorted_articles, limit=request.max_articles) if content_filter else sorted_articles[:request.max_articles]
        
        # Format response
        formatted_articles = []
        for article in final:
            classification = article.get("classification", {})
            formatted_articles.append({
                "title": article.get("title"),
                "content": article.get("content"),
                "link": article.get("link"),
                "source": article.get("source"),
                "topic": article.get("category", "manual"),
                "quality_score": round(classification.get("quality_score", 0), 3),
                "spam_score": round(classification.get("spam_score", 0), 3),
                "confidence": round(classification.get("confidence", 0), 3)
            })
        
        return FilterResponse(
            status="success",
            total_fetched=total_fetched,
            filtered_count=filtered_count,
            final_count=len(final),
            articles=formatted_articles
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve React frontend static files
if FRONTEND_AVAILABLE:
    # Mount static files (CSS, JS, images, etc.)
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_BUILD_DIR, "static")), name="static")
    
    # Serve index.html for all non-API routes (SPA support)
    @app.get("/")
    async def serve_frontend():
        """Serve React frontend"""
        return FileResponse(os.path.join(FRONTEND_BUILD_DIR, "index.html"))
    
    @app.get("/{full_path:path}")
    async def serve_frontend_routes(full_path: str):
        """Catch-all route for React SPA routing"""
        # If path starts with 'api', let it 404 naturally
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Check if it's a static file that exists
        file_path = os.path.join(FRONTEND_BUILD_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Otherwise, serve index.html for client-side routing
        return FileResponse(os.path.join(FRONTEND_BUILD_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        """Root endpoint when frontend is not available"""
        return {
            "status": "ok",
            "message": "RSS Filter API is running",
            "frontend_available": False,
            "api_docs": "/docs"
        }

if __name__ == "__main__":
    import uvicorn
    # For Hugging Face Spaces: use port 7860
    port = int(os.getenv("PORT", 7860))
    print(f"Starting server on port {port}")
    print(f"Frontend available: {FRONTEND_AVAILABLE}")
    if FRONTEND_AVAILABLE:
        print(f"Frontend directory: {FRONTEND_BUILD_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=port)
