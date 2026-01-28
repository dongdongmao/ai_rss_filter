"""FastAPI backend for RSS Filter"""
import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier
from src.filter import ContentFilter
from src.notifier import TelegramNotifier, EmailNotifier

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
    confidence_threshold: float = 0.7
    min_content_length: int = 50
    spam_threshold: float = 0.4
    max_articles: int = 10

class FilterResponse(BaseModel):
    status: str
    total_fetched: int
    filtered_count: int
    final_count: int
    articles: list

class ConfigResponse(BaseModel):
    sources: list
    model_name: str
    device: str
    confidence_threshold: float
    min_content_length: int
    spam_threshold: float

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
    """Get current configuration"""
    try:
        with open("config/rss_sources.json") as f:
            config = json.load(f)
        
        sources = config.get("sources", [])
        
        return ConfigResponse(
            sources=sources,
            model_name=os.getenv("MODEL_NAME", "distilbert-base-uncased"),
            device=os.getenv("DEVICE", "cpu"),
            confidence_threshold=float(os.getenv("CONFIDENCE_THRESHOLD", 0.7)),
            min_content_length=int(os.getenv("MIN_CONTENT_LENGTH", 50)),
            spam_threshold=float(os.getenv("SPAM_THRESHOLD", 0.4))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/filter")
async def run_filter(request: FilterRequest) -> FilterResponse:
    """Run RSS filter with specified parameters"""
    try:
        # Update filter parameters
        content_filter.confidence_threshold = request.confidence_threshold
        content_filter.min_content_length = request.min_content_length
        content_filter.spam_threshold = request.spam_threshold
        
        # Step 1: Fetch articles
        articles = fetcher.fetch_feeds()
        total_fetched = len(articles)
        
        if not articles:
            return FilterResponse(
                status="no_articles",
                total_fetched=0,
                filtered_count=0,
                final_count=0,
                articles=[]
            )
        
        # Step 2: Classify articles
        category_labels = ["valuable content", "advertisement", "clickbait", "spam"]
        articles = classifier.batch_classify(articles, category_labels)
        
        # Step 3: Filter articles
        filtered = content_filter.filter_articles(articles)
        filtered_count = len(filtered)
        
        # Step 4: Deduplicate
        unique = content_filter.deduplicate(filtered)
        
        # Step 5: Sort by score
        sorted_articles = content_filter.sort_by_score(unique)
        
        # Step 6: Limit
        final = content_filter.limit_articles(sorted_articles, limit=request.max_articles)
        
        # Format response
        formatted_articles = []
        for article in final:
            classification = article.get("classification", {})
            formatted_articles.append({
                "title": article.get("title"),
                "content": article.get("content"),
                "link": article.get("link"),
                "source": article.get("source"),
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

@app.post("/api/notify/telegram")
async def send_telegram(articles: list = None):
    """Send articles to Telegram"""
    try:
        notifier = TelegramNotifier()
        if not notifier.available:
            raise HTTPException(status_code=400, detail="Telegram not configured")
        
        if not articles:
            raise HTTPException(status_code=400, detail="No articles provided")
        
        result = await notifier.send_digest(articles, "RSS Feed Summary")
        if result:
            return {"status": "success", "message": f"Sent {len(articles)} articles to Telegram"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send to Telegram")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/notify/email")
async def send_email(articles: list = None):
    """Send articles to Email"""
    try:
        notifier = EmailNotifier()
        if not notifier.available:
            raise HTTPException(status_code=400, detail="Email not configured")
        
        if not articles:
            raise HTTPException(status_code=400, detail="No articles provided")
        
        result = notifier.send_digest(articles, "RSS Feed Summary")
        if result:
            return {"status": "success", "message": f"Sent {len(articles)} articles via email"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
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
