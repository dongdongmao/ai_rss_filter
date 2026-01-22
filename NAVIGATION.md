# 📚 项目概览和导航指南

## 🎯 项目介绍

**私人 RSS/信息流降噪器** 是一个使用 AI 的智能内容过滤系统，能够：

✅ **自动抓取** - 从多个 RSS 源获取文章  
✅ **智能分类** - 使用 BERT/RoBERTa 评估内容质量  
✅ **自动过滤** - 移除广告、垃圾和低质内容  
✅ **多渠道推送** - 通过 Telegram 或 Email 推送最优内容  
✅ **自动调度** - 每日定时运行  

---

## 📖 文档导航

### 🚀 快速开始（选择一个）

1. **5 分钟快速体验**
   - 查看：[GETTING_STARTED.md](GETTING_STARTED.md)
   - 运行：`python main.py`

2. **完整安装配置**
   - 查看：[README.md](README.md)
   - 运行：`python quickstart.py`

3. **命令行速查**
   - 查看：[QUICK_REFERENCE.md](QUICK_REFERENCE.md)
   - 用途：快速查找命令和参数

### 📚 详细文档

| 文档 | 用途 | 查看场景 |
|------|------|---------|
| [README.md](README.md) | 快速开始和基本使用 | 第一次使用 |
| [README_FULL.md](README_FULL.md) | 完整详细文档 | 深入学习 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 参数和命令速查 | 日常使用 |
| [EXAMPLES.md](EXAMPLES.md) | 10+ 代码示例 | 学习高级用法 |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 项目完成总结 | 了解项目结构 |
| [CHECKLIST.md](CHECKLIST.md) | 部署检查表 | 验证安装 |

---

## 🗂️ 项目结构

```
ai_rss_filter/
│
├── 📖 文档
│   ├── README.md                 ← START HERE（快速开始）
│   ├── README_FULL.md            ← 完整文档
│   ├── QUICK_REFERENCE.md        ← 参数速查
│   ├── EXAMPLES.md               ← 代码示例
│   ├── GETTING_STARTED.md        ← 项目概览
│   └── CHECKLIST.md              ← 部署检查表
│
├── 🐍 Python 程序
│   ├── main.py                   ← 主程序（运行这个）
│   ├── scheduler.py              ← 定时调度
│   ├── quickstart.py             ← 交互式配置
│   └── test_rss_filter.py        ← 单元测试
│
├── 📁 核心模块（src/）
│   ├── rss_fetcher.py            ← RSS 爬虫
│   ├── text_classifier.py        ← AI 分类
│   ├── filter.py                 ← 内容过滤
│   ├── notifier.py               ← 推送通知
│   └── __init__.py
│
├── ⚙️ 配置
│   ├── config/
│   │   └── rss_sources.json      ← RSS 源配置（需编辑）
│   ├── .env.example              ← 环境变量模板（复制→编辑）
│   ├── setup.ps1                 ← Windows 安装
│   ├── setup.sh                  ← Linux/Mac 安装
│   └── requirements.txt          ← 依赖
│
├── 📁 数据目录
│   ├── data/                     ← 过滤结果保存
│   └── logs/                     ← 日志文件
│
└── 📋 其他
    ├── LICENSE                   ← MIT 许可证
    └── NAVIGATION.md             ← 本文件
```

---

## 🎬 快速开始（3 步）

### 步骤 1：安装

**Windows:**
```bash
setup.ps1
```

**Linux/Mac:**
```bash
bash setup.sh
```

### 步骤 2：配置

```bash
cp .env.example .env
# 编辑 .env，添加 Telegram Token（可选）
```

### 步骤 3：运行

```bash
python main.py
```

---

## 📋 常用命令

```bash
# 立即运行一次，查看结果
python main.py

# 立即运行并推送通知
python scheduler.py now

# 启动定时调度（每日 9:00 运行）
python scheduler.py

# 交互式配置向导
python quickstart.py

# 运行单元测试
python test_rss_filter.py
```

---

## 🔧 配置指南

### 环境变量配置（.env）

```env
# Telegram（必选要推送）
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_id

# Email（可选）
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=app_password
EMAIL_RECIPIENT=recipient@gmail.com

# AI 模型
MODEL_NAME=distilbert-base-uncased
DEVICE=cpu  # or cuda

# 过滤参数
CONFIDENCE_THRESHOLD=0.7
MIN_CONTENT_LENGTH=50
SPAM_THRESHOLD=0.4
```

### RSS 源配置（config/rss_sources.json）

编辑此文件添加你的 RSS 源：

```json
{
  "sources": [
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com/rss",
      "category": "tech",
      "enabled": true
    }
  ]
}
```

---

## 🤖 核心功能模块

### 1. RSS 爬虫 (`src/rss_fetcher.py`)
- 从 RSS 源抓取文章
- 支持多个源并行处理
- 自动错误处理

### 2. AI 分类器 (`src/text_classifier.py`)
- BERT/RoBERTa 文本分类
- 评估内容质量（0-100%）
- 检测垃圾内容（0-100%）
- 支持 GPU 加速

### 3. 内容过滤 (`src/filter.py`)
- 多层过滤条件
- 自动去重
- 按质量排序
- 灵活阈值

### 4. 推送通知 (`src/notifier.py`)
- Telegram Bot 推送
- Email HTML 摘要
- 异步处理
- 格式化输出

---

## 🚦 工作流程

```
RSS 源 → 爬虫 → AI分类 → 过滤 → 排序 → 推送

详细步骤：
1. RSS 爬虫：从 RSS 源抓取最新文章
2. AI 分类：使用 BERT 评分（质量 + 垃圾）
3. 智能过滤：移除不符合条件的文章
4. 排序去重：按质量排序并去除重复
5. 多渠道推送：发送到 Telegram/Email
6. 结果保存：保存到 JSON 文件
```

---

## 🎓 学习路径

### 初级（刚开始）
1. 读 [README.md](README.md)
2. 运行 `python main.py`
3. 阅读 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

### 中级（想定制）
1. 阅读 [EXAMPLES.md](EXAMPLES.md)
2. 编辑 `config/rss_sources.json`
3. 修改 `.env` 的过滤参数
4. 查看日志理解运行过程

### 高级（想深入）
1. 研究 `src/` 的各模块
2. 运行 `test_rss_filter.py` 理解测试
3. 修改模块代码实现自定义功能
4. 在 [EXAMPLES.md](EXAMPLES.md) 的基础上扩展

---

## 🆘 问题排查

| 问题 | 解决 |
|------|------|
| Telegram 无法推送 | 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) 的故障排查部分 |
| 没有高质量文章 | 降低 `CONFIDENCE_THRESHOLD` 或查看 [CHECKLIST.md](CHECKLIST.md) |
| 速度太慢 | 使用更小的模型或启用 GPU，参考 [README_FULL.md](README_FULL.md) |
| 想修改代码 | 查看 [EXAMPLES.md](EXAMPLES.md) 获取代码示例 |

---

## 💡 使用场景

### 📰 场景 1：科技新闻播报
- 配置科技类 RSS 源
- 高过滤阈值（只要最优内容）
- Telegram 每日推送

### 📊 场景 2：数据分析学习
- 添加 Medium、Dev.to 等源
- 中等阈值（平衡数量和质量）
- Email 每周汇总

### 💰 场景 3：投资信息
- 配置金融/加密 RSS 源
- 实时 Telegram 推送
- 本地 JSON 存档

### 🔬 场景 4：学术追踪
- 添加 ArXiv、Papers with Code
- 保守过滤（只要顶级论文）
- 每月 Email 汇总

---

## 📞 获取帮助

| 需求 | 查看 |
|------|------|
| 快速开始 | [README.md](README.md) |
| 详细说明 | [README_FULL.md](README_FULL.md) |
| 命令和参数 | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 代码示例 | [EXAMPLES.md](EXAMPLES.md) |
| 部署检查 | [CHECKLIST.md](CHECKLIST.md) |
| 项目结构 | [GETTING_STARTED.md](GETTING_STARTED.md) |

---

## 🎉 准备好了吗？

立即开始！

```bash
# 1. 安装
setup.ps1  # 或 bash setup.sh

# 2. 配置
cp .env.example .env

# 3. 运行
python main.py
```

**祝你使用愉快！** ✨

---

**下一步**: 打开 [README.md](README.md) 开始详细设置。
