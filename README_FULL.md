# 私人 RSS/信息流降噪器 🤖

使用 AI 文本分类（BERT/RoBERTa）的智能 RSS 过滤系统，自动识别和过滤掉广告、标题党和低质内容，只推送有价值的内容到 Telegram 或邮箱。

**工作原理**：每天自动抓取你关注领域（科技、AI、理财等）的 RSS feeds，通过轻量级 NLP 模型进行内容分类，智能过滤掉垃圾内容和广告，将高质量文章推送到你的 Telegram 或邮箱。

## 功能特性

✨ **AI 文本分类**
- 使用 Hugging Face Transformers 的轻量级 BERT/RoBERTa 模型
- Zero-shot 分类，无需训练数据
- 自动识别广告、标题党、垃圾内容

🎯 **智能过滤**
- 基于质量评分的内容筛选
- 双重检测：质量分数 + 垃圾程度评分
- 自动去重和内容长度检查

📡 **多渠道推送**
- Telegram Bot 推送（实时、支持 Markdown）
- Email 摘要推送（HTML 格式）
- 支持日报/周报汇总

⚙️ **自动化调度**
- 每日定时运行
- 可配置运行时间
- 支持即时运行

📊 **可视化结果**
- JSON 格式保存过滤结果
- 质量评分展示
- 来源和链接跟踪

## 快速开始

### 1️⃣ 克隆项目并进入目录
```bash
cd ai_rss_filter
```

### 2️⃣ 运行快速安装脚本

**Windows:**
```bash
setup.ps1
```

**Linux/Mac:**
```bash
bash setup.sh
```

### 3️⃣ 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 Telegram Token 等
```

### 4️⃣ 运行快速配置向导
```bash
python quickstart.py
```

这个向导会帮你：
- 配置 Telegram Bot（可选）
- 配置 Email 推送（可选）
- 测试配置
- 首次运行

### 5️⃣ 立即测试
```bash
python main.py
```

### 6️⃣ 启动定时调度（每日 9:00）
```bash
python scheduler.py
```

## 配置 Telegram Bot（推荐）

### 获取 Bot Token

1. **打开 Telegram**，搜索 `@BotFather`
2. **发送命令** `/newbot`
3. **按提示**设置 Bot 名称（例如：MyRSSFilter）
4. **复制 Token**（类似：`123456:ABC-DEF...`）

### 获取 Chat ID

1. **向你的 Bot 发送任意消息**
2. **访问 API**（用你的 Token 替换）：
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```
3. **查看返回的 JSON**，找到 `response[0].message.chat.id`

### 配置 .env
```env
TELEGRAM_BOT_TOKEN=你的_bot_token
TELEGRAM_CHAT_ID=你的_chat_id
```

## 配置 Email 推送（可选）

### Gmail 配置

1. **启用两步验证**：[Google 账户安全](https://myaccount.google.com/security)
2. **生成应用专用密码**：
   - 进入 https://myaccount.google.com/apppasswords
   - 选择 Mail 和 Windows Computer
   - 复制生成的密码
3. **配置 .env**：
   ```env
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=生成的应用密码
   EMAIL_RECIPIENT=recipient@gmail.com
   ```

## 项目结构

```
ai_rss_filter/
├── src/
│   ├── rss_fetcher.py         # RSS 爬虫模块
│   ├── text_classifier.py     # AI 文本分类
│   ├── filter.py              # 内容过滤
│   └── notifier.py            # Telegram/Email 推送
├── config/
│   └── rss_sources.json       # RSS 源配置
├── data/                      # 过滤结果存储
├── logs/                      # 日志文件
├── main.py                    # 主程序
├── scheduler.py               # 定时调度
├── quickstart.py              # 快速配置向导
├── requirements.txt           # 依赖
├── .env.example               # 环境变量示例
└── README.md                  # 文档
```

## 工作流程

```
RSS 源
  ↓
[RSS 爬虫] ← 解析 feed、提取元数据
  ↓
[AI 分类器] ← BERT/RoBERTa 评估内容
  - 质量分数（0-100%）
  - 垃圾评分（0-100%）
  - 置信度
  ↓
[智能过滤] ← 多层过滤
  - 质量分数 > 60%
  - 垃圾评分 < 40%
  - 内容长度 > 50 字符
  - 去重
  ↓
[排序] ← 按质量评分排序，取前 10 篇
  ↓
[推送通知]
  ├─ Telegram Bot
  ├─ Email 摘要
  └─ 本地 JSON 存储
```

## 常用命令

```bash
# 立即运行一次
python main.py

# 立即运行并推送通知
python scheduler.py now

# 启动定时调度（每日 9:00）
python scheduler.py

# 快速配置向导
python quickstart.py

# 运行测试
python test_rss_filter.py
```

## 自定义 RSS 源

编辑 `config/rss_sources.json`：

```json
{
  "sources": [
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/rss",
      "category": "tech",
      "enabled": true
    },
    {
      "name": "ArXiv 论文",
      "url": "http://arxiv.org/rss/cs.AI",
      "category": "ai",
      "enabled": true
    }
  ]
}
```

### 推荐高质量 RSS 源

**技术新闻：**
- Hacker News: `https://news.ycombinator.com/rss`
- TechCrunch: `http://feeds.techcrunch.com/TechCrunch/`
- The Verge: `https://www.theverge.com/rss/index.xml`

**AI 相关：**
- ArXiv CS: `http://arxiv.org/rss/cs`
- Papers with Code: `https://paperswithcode.com/rss/latest`
- Hugging Face: `https://huggingface.co/feed/new-models`

**编程：**
- GitHub Trending: `https://github.com/trending?spoken_language_code=&since=daily`
- Dev.to: `https://dev.to/api/articles?top=7`

**加密/金融：**
- CoinDesk: `https://feeds.coindesk.com/news`

## 调整过滤阈值

在 `.env` 中修改：

```env
# 分类置信度阈值（0-1）
# 越高 = 更严格，越低 = 更宽松
CONFIDENCE_THRESHOLD=0.7

# 最小内容长度（字符数）
MIN_CONTENT_LENGTH=50

# 垃圾评分阈值（0-1）
# 越高 = 过滤更多垃圾，越低 = 保留更多内容
SPAM_THRESHOLD=0.4
```

**推荐配置：**
- **保守**（只要最高质）：`CONFIDENCE_THRESHOLD=0.8, SPAM_THRESHOLD=0.3`
- **平衡**（默认）：`CONFIDENCE_THRESHOLD=0.7, SPAM_THRESHOLD=0.4`
- **宽松**（内容更多）：`CONFIDENCE_THRESHOLD=0.5, SPAM_THRESHOLD=0.5`

## 模型选择

在 `.env` 中设置 `MODEL_NAME`：

### 轻量级模型（推荐 ⭐）
- `distilbert-base-uncased` - 最快，内存最小
- `distilroberta-base` - 稍慢但更准确

### 标准模型
- `bert-base-uncased` - 较准确但较慢
- `roberta-base` - 高精度

### 大模型
- `roberta-large` - 最准确但最慢
- `deberta-base` - 新型模型，性能好

**首次运行会自动下载模型**（1-2 GB），之后会缓存本地。

## 性能优化

### 启用 GPU（推荐）

如果有 NVIDIA GPU：

```bash
# 安装 GPU 版本的 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 在 .env 中设置
DEVICE=cuda
```

### 内存优化

- 使用 DistilBERT 而非 BERT
- 减少 RSS 源数量
- 减少处理的文章数量

## 故障排查

### ❌ Telegram 不能发送

**检查 Token 和 Chat ID：**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'Token: {os.getenv(\"TELEGRAM_BOT_TOKEN\")}'); print(f'Chat ID: {os.getenv(\"TELEGRAM_CHAT_ID\")}')"
```

### ❌ 模型下载很慢

首次运行会下载模型（1-2 GB）。预先下载：
```bash
python -c "from transformers import pipeline; pipeline('zero-shot-classification', model='distilbert-base-uncased')"
```

### ❌ 内存不足

- 切换到 CPU：`.env` 中 `DEVICE=cpu`
- 使用更小的模型：`MODEL_NAME=distilbert-base-uncased`
- 减少 RSS 源

### ❌ 未找到高质量文章

- 降低 `CONFIDENCE_THRESHOLD`（例如 0.6）
- 降低 `SPAM_THRESHOLD`（例如 0.5）
- 检查 RSS 源是否有效

## 进阶用法

### 自定义分类标签

编辑 `main.py` 中的 `run_once` 方法：
```python
category_labels = [
    "技术突破",
    "工程最佳实践",
    "商业新闻",
    "垃圾和广告"
]
```

### 添加自定义过滤逻辑

编辑 `src/filter.py` 中的 `_is_quality_article` 方法。

### Docker 部署

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "scheduler.py"]
```

```bash
docker build -t rss-filter .
docker run -d --env-file .env rss-filter
```

## 依赖说明

| 库 | 用途 |
|---|---|
| `feedparser` | RSS/Atom feed 解析 |
| `transformers` | Hugging Face 模型库 |
| `torch` | 深度学习框架 |
| `python-telegram-bot` | Telegram 集成 |
| `python-dotenv` | 环境变量管理 |
| `schedule` | 定时任务调度 |
| `requests` | HTTP 请求 |
| `beautifulsoup4` | HTML 解析 |

## 许可证

MIT License

## 反馈和贡献

- 📝 提出 Issue
- 🔀 提交 Pull Request
- 💬 讨论新想法

## 相关资源

- 📚 [Hugging Face Transformers 文档](https://huggingface.co/docs/transformers)
- 🤖 [Telegram Bot API 文档](https://core.telegram.org/bots/api)
- 📖 [Feedparser 文档](https://feedparser.readthedocs.io/)
- 🔍 [Zero-shot Classification 详解](https://huggingface.co/tasks/zero-shot-classification)

---

**祝你使用愉快！如有问题，欢迎反馈。** ✨
