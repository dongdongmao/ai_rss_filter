# 🚀 Hugging Face Spaces 部署 - 5 分钟快速指南

## ⚡ 超快速部署（仅需 5 步）

### 步骤 1：创建 Space
```
1. 打开 huggingface.co/spaces
2. 点击 "Create new Space"
3. 输入名称（如：rss-filter）
4. 选择 "Docker"
5. 点击 "Create"
```

### 步骤 2：上传文件
```bash
# 克隆你的 Space
git clone https://huggingface.co/spaces/你的用户名/rss-filter
cd rss-filter

# 复制项目文件
cp -r ../ai_rss_filter/* .

# 或手动上传这些文件：
# - Dockerfile
# - app.py
# - requirements.txt
# - src/ 文件夹
# - config/ 文件夹
```

### 步骤 3：更新 requirements.txt
```bash
# 添加 Gradio
echo "gradio==4.11.0" >> requirements.txt
echo "schedule==1.2.0" >> requirements.txt
```

### 步骤 4：添加 Secrets（可选）
在 Space 设置中添加：
```env
TELEGRAM_BOT_TOKEN=你的_token
TELEGRAM_CHAT_ID=你的_id
```

### 步骤 5：推送部署
```bash
git add .
git commit -m "Deploy to HF Spaces"
git push
```

---

## ✨ 就这样！

空间会自动：
1. 构建 Docker 镜像
2. 启动应用
3. 生成公开 URL

**总耗时**：5-15 分钟

---

## 🎉 部署完成后

- 打开生成的 URL
- 在 Web 界面中调整参数
- 点击"运行过滤"查看结果
- 使用"推送通知"发送结果（可选）

---

## 📋 Dockerfile 说明

自动创建的 `Dockerfile` 会：
- 使用 Python 3.10
- 安装所有依赖
- 复制项目文件
- 运行 Gradio 应用
- 暴露端口 7860

---

## 🎯 使用 Web 界面

### 🚀 运行过滤
1. 调整参数滑块
2. 点击"运行过滤"
3. 查看结果

### 📱 推送通知
1. 先运行过滤
2. 点击"发送 Telegram"或"发送 Email"
3. 查看推送状态

### ⚙️ 配置信息
1. 查看当前 RSS 源
2. 查看模型配置
3. 查看过滤参数

---

## ⚠️ 重要提示

- **模型下载**：首次运行 5-10 分钟（正常）
- **免费配额**：CPU 有限，但足够用
- **GPU**：需要付费版本
- **存储**：保存到 `/app/data`，重启后保留

---

## 🔗 完整文档

详细内容见：[HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md)

---

## 💬 遇到问题？

| 问题 | 解决 |
|------|------|
| 模型下载慢 | 等待 5-10 分钟（正常） |
| Telegram 不工作 | 检查 Secrets 中的 Token |
| 找不到文件 | 确保 `src/` 和 `config/` 目录已上传 |
| 界面打不开 | 等待构建完成，刷新页面 |

---

**现在就试试吧！** 🚀✨
