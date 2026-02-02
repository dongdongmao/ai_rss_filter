---
title: Ai Rss Filter
emoji: 📉
colorFrom: yellow
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: ai_rss_filter
---

# AI RSS Filter 🤖

Intelligent RSS filtering system using AI text classification.

## Quick Start

### Local Setup

**Windows:**
```bash
setup.ps1
```

**Linux/Mac:**
```bash
bash setup.sh
```

### Running the Application

```bash
# Web interface (React + FastAPI)
python api.py

# Then visit: http://localhost:8000
```

### Using Configuration

```bash
cp .env.example .env
```

## Deployment

### Hugging Face Spaces (Recommended)

1. Push code to GitHub
2. Create new Space with Docker SDK
3. Connect your GitHub repository
4. Space auto-deploys

Visit: **https://huggingface.co/spaces**

## Configuration

Edit `config/rss_sources.json` to add/modify RSS sources:

```json
{
  "sources": [
    {
      "name": "Source Name",
      "url": "https://example.com/rss",
      "enabled": true
    }
  ]
}
```

## Features

- 🤖 AI text classification (BERT/RoBERTa)
- 🎯 Smart filtering & spam detection
- 🌐 Modern React web interface
- 🐳 Docker containerized

## Environment Variables

Create a `.env` file to enable notifications (optional):


## Docker Deployment

Build and run with Docker:

```bash
docker build -t ai-rss-filter .
docker run -p 7860:7860 ai-rss-filter
```

## API Endpoints

- `GET /` - React web interface
- `GET /config` - Get configuration
- `POST /filter` - Run RSS filter

## Project Structure

```
ai_rss_filter/
├── api.py                  # FastAPI backend
├── requirements.txt        # Python dependencies
├── src/                    # Core modules
│   ├── rss_fetcher.py     # RSS fetching
│   ├── text_classifier.py # AI classification
│   ├── filter.py          # Content filtering
│   └── notifier.py        # Notification module (placeholder)
├── config/
│   └── rss_sources.json   # RSS source config
└── data/                  # Temporary data

frontend/
├── package.json           # React dependencies
└── src/
    ├── App.js            # Main React component
    └── components/       # UI components
```

## License

This project is licensed under the MIT License.
