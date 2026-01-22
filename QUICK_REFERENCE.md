# 快速参考指南 - QUICK REFERENCE

## ⚡ 30秒快速开始

```bash
# 1. 克隆项目
cd ai_rss_filter

# 2. 安装（Windows）
setup.ps1

# 或（Linux/Mac）
bash setup.sh

# 3. 配置
copy .env.example .env
# 编辑 .env，添加 Telegram Token

# 4. 运行
python main.py
```

## 📋 常用命令速查表

| 命令 | 说明 |
|------|------|
| `python main.py` | 立即运行一次，输出结果 |
| `python scheduler.py now` | 立即运行并发送通知 |
| `python scheduler.py` | 启动定时任务（每日9:00） |
| `python quickstart.py` | 交互式配置向导 |
| `python test_rss_filter.py` | 运行单元测试 |

## 🔧 配置参数速查

### .env 文件关键参数

```env
# Telegram（必填）
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_id

# Email（可选）
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=app_password
EMAIL_RECIPIENT=recipient@email.com

# AI 模型
MODEL_NAME=distilbert-base-uncased    # 轻量级推荐
DEVICE=cpu                             # or cuda

# 过滤阈值
CONFIDENCE_THRESHOLD=0.7               # 分类置信度
MIN_CONTENT_LENGTH=50                  # 最小字符数
SPAM_THRESHOLD=0.4                     # 垃圾内容阈值
```

### RSS 源配置 (config/rss_sources.json)

```json
{
  "sources": [
    {
      "name": "源名称",
      "url": "https://example.com/feed",
      "category": "tech",
      "enabled": true
    }
  ]
}
```

## 📊 过滤阈值调优

| 场景 | CONFIDENCE_THRESHOLD | SPAM_THRESHOLD | 结果 |
|------|----|----|------|
| 🎯 高质量内容只 | 0.8+ | 0.2 | 少量精选内容 |
| ⚖️ 平衡（默认） | 0.7 | 0.4 | 适中数量的高质内容 |
| 🔄 内容丰富 | 0.5 | 0.5 | 更多内容，容许一些低质 |

## 🤖 AI 模型对比

| 模型 | 速度 | 准确度 | 内存 | 推荐 |
|------|------|--------|------|------|
| distilbert-base-uncased | ⚡⚡⚡ | ⭐⭐⭐ | 低 | ✅ 首选 |
| distilroberta-base | ⚡⚡ | ⭐⭐⭐⭐ | 低 | ✅ 高精度 |
| bert-base-uncased | ⚡ | ⭐⭐⭐⭐ | 中 | 好用 |
| roberta-base | ⚡ | ⭐⭐⭐⭐⭐ | 中 | 高精度 |

## 📡 推送配置速查

### Telegram 配置

```bash
# 1. 找 @BotFather 创建 Bot，复制 Token

# 2. 获取 Chat ID
https://api.telegram.org/bot<TOKEN>/getUpdates

# 3. 配置 .env
TELEGRAM_BOT_TOKEN=token
TELEGRAM_CHAT_ID=id
```

### Gmail 配置

```bash
# 1. 启用两步验证
myaccount.google.com/security

# 2. 生成应用密码
myaccount.google.com/apppasswords

# 3. 配置 .env
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=16位密码
EMAIL_RECIPIENT=recipient@gmail.com
```

## 🚀 高级配置

### GPU 加速（如果有 NVIDIA）

```bash
# 安装 GPU 版本
pip install torch --index-url https://download.pytorch.org/whl/cu118

# .env 中设置
DEVICE=cuda
```

### Docker 快速部署

```bash
# 构建镜像
docker build -t rss-filter .

# 运行容器
docker run -d --env-file .env --name rss-filter rss-filter

# 查看日志
docker logs rss-filter
```

## 🔍 日志查看

```bash
# 实时查看日志
tail -f logs/rss_filter.log

# 查看调度器日志
tail -f logs/scheduler.log

# 查看错误
grep ERROR logs/*.log
```

## ❌ 常见问题速解

| 问题 | 解决方案 |
|------|---------|
| Telegram 无法发送 | 检查 Token 和 Chat ID 是否正确 |
| 模型下载慢 | 正常，首次1-2GB，之后缓存本地 |
| 没有高质量文章 | 降低 CONFIDENCE_THRESHOLD 到 0.6 |
| 内存不足 | 使用 distilbert，或切换到 CPU |
| RSS 源无法连接 | 检查网络，或替换 URL 为其他镜像 |

## 📞 获取帮助

| 资源 | 链接 |
|------|------|
| 项目文档 | README.md |
| 使用示例 | EXAMPLES.md |
| 单元测试 | test_rss_filter.py |
| Hugging Face | https://huggingface.co/docs |
| Telegram API | https://core.telegram.org/bots |

## 💡 使用技巧

### 技巧 1：预先下载模型
```bash
python -c "from transformers import pipeline; \
pipeline('zero-shot-classification', model='distilbert-base-uncased')"
```

### 技巧 2：测试 RSS 源
```bash
python -c "from src.rss_fetcher import RSSFetcher; \
f = RSSFetcher(); articles = f.fetch_feeds(); print(len(articles))"
```

### 技巧 3：检查环境
```bash
python -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"
```

### 技巧 4：备份配置
```bash
cp config/rss_sources.json config/rss_sources.backup.json
cp .env .env.backup
```

## 📈 监控建议

- **每天检查日志**：确保任务正常运行
- **定期调整阈值**：根据推送内容质量调整
- **备份重要配置**：防止意外丢失
- **监控 Telegram 消息**：及时发现问题

---

**需要更多帮助？查看 README.md 的完整文档。**
