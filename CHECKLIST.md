# 项目清单 & 部署检查表

## ✅ 项目文件清单

### 核心功能模块
- [x] `src/rss_fetcher.py` - RSS 爬虫
- [x] `src/text_classifier.py` - AI 文本分类
- [x] `src/filter.py` - 内容过滤
- [x] `src/notifier.py` - 推送通知
- [x] `src/__init__.py` - 包初始化

### 应用程序
- [x] `main.py` - 主程序
- [x] `scheduler.py` - 定时调度
- [x] `quickstart.py` - 快速配置向导

### 配置和依赖
- [x] `requirements.txt` - Python 依赖
- [x] `.env.example` - 环境变量模板
- [x] `config/rss_sources.json` - RSS 源配置
- [x] `setup.ps1` - Windows 安装脚本
- [x] `setup.sh` - Linux/Mac 安装脚本

### 文档
- [x] `README.md` - 快速开始文档
- [x] `README_FULL.md` - 完整文档
- [x] `QUICK_REFERENCE.md` - 快速参考
- [x] `EXAMPLES.md` - 代码示例
- [x] `GETTING_STARTED.md` - 入门指南
- [x] `CHECKLIST.md` - 本文件

### 测试和质量
- [x] `test_rss_filter.py` - 单元测试

### 目录结构
- [x] `src/` - 源代码
- [x] `config/` - 配置
- [x] `data/` - 数据输出
- [x] `logs/` - 日志

---

## 🚀 部署检查表

### 初始设置
- [ ] 克隆/下载项目
- [ ] 打开项目文件夹
- [ ] 检查文件完整性

### 环境配置
- [ ] 安装 Python 3.8+
- [ ] 运行 `setup.ps1`（Windows）或 `setup.sh`（Linux/Mac）
- [ ] 虚拟环境激活
- [ ] 依赖安装完成

### 配置 Telegram（可选但推荐）
- [ ] 找 @BotFather 创建 Bot
- [ ] 复制 Bot Token
- [ ] 获取 Chat ID
- [ ] 配置 `.env` 文件

### 配置 Email（可选）
- [ ] 启用 Gmail 两步验证
- [ ] 生成应用专用密码
- [ ] 配置 `.env` 文件

### RSS 源配置
- [ ] 编辑 `config/rss_sources.json`
- [ ] 添加至少 2-3 个 RSS 源
- [ ] 验证 RSS 源 URL 有效

### 功能测试
- [ ] 运行 `python main.py` 测试
- [ ] 查看是否成功过滤内容
- [ ] 检查日志文件是否正常
- [ ] 测试通知推送（如已配置）

### 参数优化
- [ ] 调整过滤阈值
- [ ] 测试不同的 AI 模型
- [ ] 优化 RSS 源列表
- [ ] 记录最佳参数

### 部署运行
- [ ] 启动定时调度：`python scheduler.py`
- [ ] 验证日志输出
- [ ] 检查首次运行结果
- [ ] 监控后续推送

### 维护和监控
- [ ] 定期检查日志
- [ ] 更新 RSS 源
- [ ] 调整过滤参数
- [ ] 备份配置文件

---

## 📋 常见部署问题

### ❓ 问题：Telegram 无法发送

**检查项**：
- [ ] `.env` 文件中 `TELEGRAM_BOT_TOKEN` 不为空
- [ ] `.env` 文件中 `TELEGRAM_CHAT_ID` 不为空
- [ ] Bot Token 格式正确（数字:字母数字字符）
- [ ] Chat ID 是数字
- [ ] 网络连接正常

### ❓ 问题：RSS 源无法连接

**检查项**：
- [ ] RSS 源 URL 有效可访问
- [ ] 网络连接正常
- [ ] 没有防火墙/代理阻止
- [ ] RSS 源是否已停用

### ❓ 问题：没有高质量文章

**检查项**：
- [ ] `CONFIDENCE_THRESHOLD` 设置是否太高
- [ ] `SPAM_THRESHOLD` 设置是否太低
- [ ] RSS 源是否包含足够的内容
- [ ] 日志中是否有错误信息

### ❓ 问题：速度太慢

**检查项**：
- [ ] 是否启用了 GPU（如可用）
- [ ] 是否使用了轻量级模型（distilbert）
- [ ] 是否在处理过多的文章
- [ ] 网络速度是否正常

---

## 🔄 定期维护任务

### 每周
- [ ] 检查日志是否有错误
- [ ] 验证 Telegram/Email 推送是否正常
- [ ] 查看推送的文章质量

### 每月
- [ ] 备份 `.env` 和 `config/rss_sources.json`
- [ ] 更新 RSS 源列表（添加/移除）
- [ ] 调整过滤参数基于实际效果
- [ ] 运行单元测试：`python test_rss_filter.py`

### 每季度
- [ ] 检查 Python 和依赖包是否需要更新
- [ ] 检查 Telegram/Email 配置是否仍有效
- [ ] 评估是否需要升级到新的 AI 模型

---

## 📊 性能基准

期望的运行时间（首次运行）：

| 操作 | 时间 | 说明 |
|------|------|------|
| 模型下载 | 5-10 分钟 | 仅首次 |
| RSS 抓取 | 30-60 秒 | 取决于源数量 |
| AI 分类 | 2-5 分钟 | DistilBERT, CPU |
| AI 分类 | 30-60 秒 | DistilBERT, GPU |
| 过滤/排序 | 1-2 秒 | 取决于文章数 |
| 推送 | 5-10 秒 | 取决于文章数 |
| **总计** | **3-6 分钟** | 首次 |
| **总计** | **1-2 分钟** | 后续 |

---

## 🎯 优化建议

### 如果推送内容过多
1. 提高 `CONFIDENCE_THRESHOLD` 到 0.75-0.8
2. 降低 `SPAM_THRESHOLD` 到 0.3-0.2
3. 增加 `MIN_CONTENT_LENGTH` 到 100-150

### 如果推送内容过少
1. 降低 `CONFIDENCE_THRESHOLD` 到 0.5-0.6
2. 提高 `SPAM_THRESHOLD` 到 0.5-0.6
3. 减少 `MIN_CONTENT_LENGTH` 到 20-30

### 如果速度太慢
1. 使用 `distilbert-base-uncased` 模型
2. 启用 GPU（如可用）
3. 减少 RSS 源数量

### 如果准确度不够
1. 使用 `roberta-base` 或 `distilroberta-base` 模型
2. 添加更多 RSS 源
3. 自定义分类标签

---

## ✨ 成功指标

✅ 项目成功部署标志：

- [ ] 能成功运行 `python main.py` 并输出结果
- [ ] 日志中没有 ERROR 信息
- [ ] 过滤出至少 5-10 篇高质量文章
- [ ] Telegram/Email 推送正常工作
- [ ] 定时调度能自动运行
- [ ] 结果保存到 JSON 文件

---

**最后检查**：所有项都打勾了吗？那你已经准备好了！🚀

运行以下命令启动：
```bash
python scheduler.py
```

祝你使用愉快！✨
