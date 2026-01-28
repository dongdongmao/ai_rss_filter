---
title: AI RSS Filter
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
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
# Edit .env and add Telegram Token (optional)
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
- 📡 Telegram & Email notifications
- 🌐 Modern React web interface
- 🐳 Docker containerized

## Environment Variables

Create a `.env` file to enable notifications (optional):

```bash
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

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
- `POST /notify/telegram` - Send Telegram notification
- `POST /notify/email` - Send email notification

## Project Structure

```
ai_rss_filter/
├── api.py                  # FastAPI backend
├── requirements.txt        # Python dependencies
├── src/                    # Core modules
│   ├── rss_fetcher.py     # RSS fetching
│   ├── text_classifier.py # AI classification
│   ├── filter.py          # Content filtering
│   └── notifier.py        # Notifications
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