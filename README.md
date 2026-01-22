# 私人 RSS/信息流降噪器 🤖

使用 AI 文本分类（BERT/RoBERTa）的智能 RSS 过滤系统，自动识别和过滤掉广告、标题党和低质内容，只推送有价值的内容到 Telegram 或邮箱。

---

## 🚀 部署选项

### ⭐ 选项 1：Hugging Face Spaces（推荐）
**无需本地环境，5 分钟部署**
- 免费部署，Web 界面可分享
- 📖 [5 分钟快速部署](HF_SPACES_QUICKSTART.md)

### 💻 选项 2：本地运行
**完全控制，自动化任务**
- 支持定时任务
- 见下方快速开始

### 🐳 选项 3：Docker 部署
**容器化、可扩展**
- 📖 [完整部署文档](HF_SPACES_DEPLOYMENT.md)

---

## ⚡ 功能特性

✨ **AI 文本分类** - BERT/RoBERTa 轻量级模型  
🎯 **智能过滤** - 质量评分 + 垃圾检测  
📡 **多渠道推送** - Telegram + Email  
⚙️ **自动化** - 每日定时运行  
🌐 **Web 界面** - Gradio 和 CLI 支持  

---

## 快速开始（本地）

### 1️⃣ 安装

**Windows:**
```bash
setup.ps1
```

**Linux/Mac:**
```bash
bash setup.sh
```

### 2️⃣ 配置

```bash
cp .env.example .env
# 编辑 .env，添加 Telegram Token
```

### 3️⃣ 运行

```bash
python main.py
```

---

## 🌐 Hugging Face Spaces 部署

**最快的方式 - 5 分钟内部署到免费服务器：**

1. 打开 [Hugging Face Spaces](https://huggingface.co/spaces)
2. 创建新 Space，选择 Docker
3. 上传项目文件
4. 推送到 Git
5. 等待自动部署

📖 **详细步骤** → [HF_SPACES_QUICKSTART.md](HF_SPACES_QUICKSTART.md)

---

## 常用命令

```bash
# 立即运行
python main.py

# 启动定时任务
python scheduler.py

# Web 界面
python app.py

# 交互式配置
python quickstart.py
```

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [HF_SPACES_QUICKSTART.md](HF_SPACES_QUICKSTART.md) | ⭐ 5 分钟快速部署到 Spaces |
| [HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md) | 完整部署指南 |
| [README_FULL.md](README_FULL.md) | 详细文档 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 参数速查 |
| [EXAMPLES.md](EXAMPLES.md) | 代码示例 |

---

**开始使用**：
```bash
python main.py
```

或 [立即在 HF Spaces 上试用](HF_SPACES_QUICKSTART.md) 🚀
