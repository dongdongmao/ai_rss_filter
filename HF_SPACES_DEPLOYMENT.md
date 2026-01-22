# HF Spaces 部署指南

## 🚀 在 Hugging Face Spaces 上部署

### 方式 1: 使用 Gradio Web 界面（推荐）

#### 前提条件
- Hugging Face 账户
- 项目文件

#### 步骤

1. **访问 Hugging Face Spaces**
   ```
   https://huggingface.co/spaces
   ```

2. **创建新 Space**
   - 点击 "Create new Space"
   - 输入 Space 名称（如 `rss-filter`）
   - 选择 **Docker** 作为 Space 类型
   - 选择 **Private**（可选，根据需要）
   - 点击 "Create Space"

3. **上传项目文件**
   - 克隆生成的 repo：
     ```bash
     git clone https://huggingface.co/spaces/你的用户名/rss-filter
     cd rss-filter
     ```
   - 复制本项目文件到此目录：
     ```bash
     cp -r ../ai_rss_filter/* .
     ```
   - 确保文件包括：
     - `Dockerfile`
     - `app.py`
     - `requirements_hf.txt` → `requirements.txt`
     - `src/` 目录
     - `config/` 目录

4. **配置环境变量**
   - 在 Space 设置中添加 Secrets：
     ```
     TELEGRAM_BOT_TOKEN=你的_token
     TELEGRAM_CHAT_ID=你的_id
     EMAIL_SENDER=your_email@gmail.com
     EMAIL_PASSWORD=your_app_password
     EMAIL_RECIPIENT=recipient@gmail.com
     ```

5. **推送到 Hugging Face**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push
   ```

6. **等待部署**
   - Space 会自动构建 Docker 镜像
   - 构建完成后，会获得一个公开 URL
   - 点击 URL 访问应用

### 方式 2: 使用 Docker 镜像

如果想在本地或其他地方使用 Docker 运行：

```bash
# 构建镜像
docker build -t rss-filter .

# 运行容器
docker run -p 7860:7860 \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_id \
  rss-filter
```

### 方式 3: 使用 Streamlit（可选）

如果更喜欢 Streamlit，可以创建 `streamlit_app.py`：

```python
import streamlit as st
from main import RSSFilterApp

st.set_page_config(page_title="RSS Filter", layout="wide")
st.title("🤖 RSS 降噪器")

# ... 页面代码
```

然后在 Space 设置中选择 Streamlit 类型。

---

## 📋 Hugging Face Spaces 限制和注意事项

### 资源限制
- **CPU**: 2 核
- **内存**: 16GB
- **存储**: 50GB
- **GPU**: 需要升级到付费版本

### 重要事项

⚠️ **模型下载**
- 首次运行会下载 BERT 模型 (~500MB)
- 可能需要 5-10 分钟
- 建议使用轻量级模型 `distilbert-base-uncased`

⚠️ **持久化存储**
- `/app/data` 和 `/app/logs` 目录会保留
- 重启后数据会保留
- 最多 50GB 空间

⚠️ **网络限制**
- 出站网络有限制
- RSS 抓取可能较慢
- Email 推送需要白名单

⚠️ **环境变量**
- 敏感信息存储在 Secrets 中
- 不要提交到 Git
- 每次部署自动注入

---

## 🔧 配置详解

### 在 Hugging Face Spaces 中添加 Secrets

1. 打开 Space 的设置页面
2. 找到 "Repository secrets" 或 "Secrets"
3. 添加以下 Secrets：

```
# Telegram（可选）
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Email（可选）
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx

# AI 模型
MODEL_NAME=distilbert-base-uncased
DEVICE=cpu

# 过滤参数
CONFIDENCE_THRESHOLD=0.7
MIN_CONTENT_LENGTH=50
SPAM_THRESHOLD=0.4
```

---

## ✨ Gradio Web 界面功能

### 🚀 运行过滤标签页
- 调整过滤参数的滑块
- 点击"运行过滤"
- 实时查看结果

### 📱 推送通知标签页
- 将结果推送到 Telegram
- 将结果推送到 Email
- 查看推送状态

### ⚙️ 配置信息标签页
- 查看当前配置
- 查看启用的 RSS 源
- 查看模型和参数

### ❓ 帮助标签页
- 使用说明
- 参数解释
- 推荐配置

---

## 🚨 常见问题

### Q: 模型下载超时怎么办？
**A**: 
- 使用更小的模型：`distilbert-base-uncased`
- 或预先下载模型到 Docker 镜像中

### Q: RSS 抓取很慢
**A**:
- HF Spaces 网络限制
- 减少 RSS 源数量
- 选择速度快的源

### Q: Telegram 推送不工作
**A**:
- 检查 Secrets 中的 Token 和 Chat ID
- 确保网络连接正常
- 查看日志文件

### Q: 我可以保存抓取的数据吗？
**A**:
- 可以，数据保存在 `/app/data` 目录
- 会在 Space 重启后保留
- 但不超过 50GB 限制

### Q: 如何自动运行任务？
**A**:
- 在 Web 界面点击"运行过滤"
- 或在 Container 中添加 cron 任务
- 或使用 HF Spaces 的定时功能（付费）

---

## 📊 部署检查清单

- [ ] Hugging Face 账户已创建
- [ ] 新 Space 已创建（Docker 类型）
- [ ] 所有项目文件已上传
- [ ] `.env.example` → `.env` 已复制
- [ ] `requirements_hf.txt` → `requirements.txt` 已复制
- [ ] Secrets 已添加
- [ ] `git push` 已执行
- [ ] 等待构建完成（5-15 分钟）
- [ ] 访问生成的 URL 测试
- [ ] Gradio 界面可以打开
- [ ] 点击"运行过滤"测试
- [ ] 推送功能测试（可选）

---

## 🎯 优化建议

### 加快启动速度
1. 使用轻量级模型：
   ```env
   MODEL_NAME=distilbert-base-uncased
   ```

2. 预加载模型到 Dockerfile：
   ```dockerfile
   RUN python -c "from transformers import pipeline; \
   pipeline('zero-shot-classification', model='distilbert-base-uncased')"
   ```

### 提高性能
1. 减少 RSS 源
2. 增加过滤阈值
3. 缓存模型

### 降低成本
1. 使用免费版 CPU
2. 避免大文件
3. 定期清理日志

---

## 🔗 相关链接

- [Hugging Face Spaces 文档](https://huggingface.co/docs/hub/spaces-overview)
- [Gradio 文档](https://gradio.app/docs/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- [项目主仓库](https://github.com/...)

---

## 💡 提示

- 部署后，Space URL 可以分享给其他人使用
- 定期检查日志排查问题
- 备份重要配置
- 监控 RSS 源的有效性

**祝你部署顺利！** 🚀
