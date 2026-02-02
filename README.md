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
<<<<<<< HEAD
=======
# Edit .env and add Telegram Token (optional)
>>>>>>> 442630110f91a4288aa2c59da972a5ca14e49126
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
<<<<<<< HEAD
=======
- 📡 Telegram & Email notifications
>>>>>>> 442630110f91a4288aa2c59da972a5ca14e49126
- 🌐 Modern React web interface
- 🐳 Docker containerized

## Environment Variables

Create a `.env` file to enable notifications (optional):

<<<<<<< HEAD
=======
```bash
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```
>>>>>>> 442630110f91a4288aa2c59da972a5ca14e49126

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
<<<<<<< HEAD
=======
- `POST /notify/telegram` - Send Telegram notification
- `POST /notify/email` - Send email notification
>>>>>>> 442630110f91a4288aa2c59da972a5ca14e49126

## Project Structure

```
ai_rss_filter/
├── api.py                  # FastAPI backend
├── requirements.txt        # Python dependencies
├── src/                    # Core modules
│   ├── rss_fetcher.py     # RSS fetching
│   ├── text_classifier.py # AI classification
│   ├── filter.py          # Content filtering
<<<<<<< HEAD
│   └── notifier.py        # Notification module (placeholder)
=======
│   └── notifier.py        # Notifications
>>>>>>> 442630110f91a4288aa2c59da972a5ca14e49126
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

<<<<<<< HEAD
This project is licensed under the MIT License.
=======
This project is licensed under the MIT License.
>>>>>>> 442630110f91a4288aa2c59da972a5ca14e49126
