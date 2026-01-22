"""
Hugging Face Spaces Gradio 应用
在 HF Spaces 上运行的 Web 界面
"""

import gradio as gr
import os
import json
from datetime import datetime
import asyncio
from dotenv import load_dotenv

from src.rss_fetcher import RSSFetcher
from src.text_classifier import TextClassifier
from src.filter import ContentFilter
from src.notifier import TelegramNotifier, EmailNotifier

# 加载环境变量
load_dotenv()

# 全局变量
fetcher = None
classifier = None
content_filter = None
last_results = []


def initialize_components():
    """初始化所有组件"""
    global fetcher, classifier, content_filter
    
    try:
        fetcher = RSSFetcher()
        classifier = TextClassifier(
            model_name=os.getenv("MODEL_NAME", "distilbert-base-uncased"),
            device=os.getenv("DEVICE", "cpu")
        )
        content_filter = ContentFilter({
            "confidence_threshold": float(os.getenv("CONFIDENCE_THRESHOLD", 0.7)),
            "min_content_length": int(os.getenv("MIN_CONTENT_LENGTH", 50)),
            "quality_threshold": 0.6,
            "spam_threshold": float(os.getenv("SPAM_THRESHOLD", 0.4))
        })
        return "✅ 组件初始化成功"
    except Exception as e:
        return f"❌ 初始化失败: {e}"


def run_filter(
    confidence_threshold: float = 0.7,
    min_content_length: int = 50,
    spam_threshold: float = 0.4,
    max_articles: int = 10
) -> str:
    """运行 RSS 过滤器"""
    global last_results
    
    try:
        # 更新过滤参数
        content_filter.confidence_threshold = confidence_threshold
        content_filter.min_content_length = min_content_length
        content_filter.spam_threshold = spam_threshold
        
        # 运行过滤流程
        print("📥 正在抓取 RSS 源...")
        articles = fetcher.fetch_feeds()
        
        if not articles:
            return "❌ 未能获取任何文章"
        
        print(f"📊 抓取到 {len(articles)} 篇文章，正在分类...")
        articles = classifier.batch_classify(articles, 
            ["valuable content", "advertisement", "clickbait", "spam"])
        
        print("🔍 正在过滤...")
        filtered = content_filter.filter_articles(articles)
        
        print("🔄 正在去重...")
        unique = content_filter.deduplicate(filtered)
        
        print("📈 正在排序...")
        sorted_articles = content_filter.sort_by_score(unique)
        
        print("✂️ 正在限制数量...")
        final = content_filter.limit_articles(sorted_articles, limit=max_articles)
        
        last_results = final
        
        # 生成输出
        output = f"""
✅ 过滤完成！

📊 **统计信息**：
- 抓取文章：{len(articles)}
- 过滤后：{len(filtered)}
- 去重后：{len(unique)}
- 最终结果：{len(final)}

📰 **文章列表**：
"""
        
        for i, article in enumerate(final, 1):
            classification = article.get("classification", {})
            quality = classification.get("quality_score", 0)
            spam = classification.get("spam_score", 0)
            
            output += f"""
{i}. **{article.get('title')}**
   - 📌 来源：{article.get('source')}
   - ⭐ 质量：{quality:.0%}
   - 🚫 垃圾：{spam:.0%}
   - 🔗 [链接]({article.get('link')})
   - 📝 {article.get('content')[:100]}...
"""
        
        return output
        
    except Exception as e:
        return f"❌ 错误: {str(e)}"


async def send_telegram_notification() -> str:
    """发送 Telegram 通知"""
    try:
        if not last_results:
            return "❌ 没有结果可发送"
        
        notifier = TelegramNotifier()
        if not notifier.available:
            return "❌ Telegram 未配置"
        
        await notifier.send_digest(last_results, "RSS Feed Summary from HF Spaces")
        return "✅ Telegram 通知已发送"
    except Exception as e:
        return f"❌ 发送失败: {e}"


def send_email_notification() -> str:
    """发送 Email 通知"""
    try:
        if not last_results:
            return "❌ 没有结果可发送"
        
        notifier = EmailNotifier()
        if not notifier.available:
            return "❌ Email 未配置"
        
        notifier.send_digest(last_results, "RSS Feed Summary from HF Spaces")
        return "✅ Email 已发送"
    except Exception as e:
        return f"❌ 发送失败: {e}"


def get_config_info() -> str:
    """获取配置信息"""
    try:
        with open("config/rss_sources.json") as f:
            config = json.load(f)
        
        sources = config.get("sources", [])
        enabled = sum(1 for s in sources if s.get("enabled", True))
        
        info = f"""
📋 **配置信息**：

🔗 **RSS 源**：
- 总数：{len(sources)}
- 启用：{enabled}

📝 **启用的源**：
"""
        for source in sources:
            if source.get("enabled", True):
                info += f"  - {source['name']} ({source.get('category')})\n"
        
        info += f"""

⚙️ **模型配置**：
- 模型：{os.getenv('MODEL_NAME', 'distilbert-base-uncased')}
- 设备：{os.getenv('DEVICE', 'cpu')}

🎯 **过滤参数**：
- 置信度阈值：{os.getenv('CONFIDENCE_THRESHOLD', 0.7)}
- 最小内容长度：{os.getenv('MIN_CONTENT_LENGTH', 50)}
- 垃圾评分阈值：{os.getenv('SPAM_THRESHOLD', 0.4)}
"""
        return info
    except Exception as e:
        return f"❌ 获取配置失败: {e}"


def build_interface():
    """构建 Gradio 界面"""
    
    with gr.Blocks(title="🤖 RSS 降噪器", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
# 🤖 私人 RSS 降噪器

使用 AI 智能过滤 RSS 信息流，自动识别和移除广告、垃圾内容，只推送有价值的文章。

**功能**：
- 🔗 从多个 RSS 源抓取文章
- 🤖 使用 BERT 进行 AI 分类
- 🎯 智能过滤垃圾和低质内容
- 📱 推送到 Telegram 或 Email
- 📊 实时查看过滤结果
        """)
        
        with gr.Tabs():
            # 标签页 1：运行过滤
            with gr.Tab("🚀 运行过滤"):
                gr.Markdown("### 调整过滤参数并运行")
                
                with gr.Row():
                    confidence_threshold = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.7,
                        step=0.05,
                        label="分类置信度阈值"
                    )
                    spam_threshold = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.4,
                        step=0.05,
                        label="垃圾评分阈值"
                    )
                
                with gr.Row():
                    min_content_length = gr.Slider(
                        minimum=10,
                        maximum=500,
                        value=50,
                        step=10,
                        label="最小内容长度"
                    )
                    max_articles = gr.Slider(
                        minimum=1,
                        maximum=50,
                        value=10,
                        step=1,
                        label="最多显示文章数"
                    )
                
                run_button = gr.Button("▶️ 运行过滤", variant="primary", scale=2)
                
                output_text = gr.Markdown()
                
                run_button.click(
                    fn=run_filter,
                    inputs=[confidence_threshold, min_content_length, spam_threshold, max_articles],
                    outputs=output_text
                )
            
            # 标签页 2：推送通知
            with gr.Tab("📱 推送通知"):
                gr.Markdown("### 将最新结果推送到外部服务")
                
                with gr.Row():
                    telegram_btn = gr.Button("📱 发送 Telegram", variant="primary")
                    email_btn = gr.Button("✉️ 发送 Email", variant="primary")
                
                notification_output = gr.Markdown()
                
                telegram_btn.click(
                    fn=lambda: asyncio.run(send_telegram_notification()),
                    outputs=notification_output
                )
                
                email_btn.click(
                    fn=send_email_notification,
                    outputs=notification_output
                )
                
                gr.Info("需要在环境变量中配置 Telegram Token/Chat ID 或 Email 账户")
            
            # 标签页 3：配置信息
            with gr.Tab("⚙️ 配置信息"):
                gr.Markdown("### 当前配置和统计")
                
                config_button = gr.Button("🔄 刷新配置")
                config_output = gr.Markdown()
                
                config_button.click(
                    fn=get_config_info,
                    outputs=config_output
                )
                
                # 自动加载配置
                gr.on(
                    triggers=[demo.load],
                    fn=get_config_info,
                    outputs=config_output
                )
            
            # 标签页 4：帮助
            with gr.Tab("❓ 帮助"):
                gr.Markdown("""
### 如何使用？

1. **运行过滤**：
   - 调整左侧的参数
   - 点击"运行过滤"按钮
   - 等待结果显示

2. **推送通知**：
   - 先运行一次过滤（生成结果）
   - 点击"发送 Telegram"或"发送 Email"
   - 需要提前配置相应的账户

3. **查看配置**：
   - 点击"配置信息"标签
   - 查看当前的 RSS 源和参数

### 参数说明

- **分类置信度阈值**：较高值 = 只接收置信度高的分类（更严格）
- **垃圾评分阈值**：较低值 = 过滤更多垃圾内容（更严格）
- **最小内容长度**：过滤掉短于此长度的文章
- **最多显示文章数**：限制显示的文章数量

### 推荐配置

- **保守**（高质量）：置信度 0.8，垃圾 0.2
- **平衡**（默认）：置信度 0.7，垃圾 0.4
- **宽松**（内容多）：置信度 0.5，垃圾 0.5

### 部署到 Hugging Face Spaces

1. 在 huggingface.co 创建新 Space
2. 选择 Docker 模板
3. 上传本项目文件
4. 在 Secrets 中添加环境变量（Telegram/Email）
5. 部署完成！

需要帮助？查看项目文档或联系开发者。
                """)
        
        # 页脚
        gr.Markdown("""
---
**🔗 项目信息**：
- 📖 [查看文档](https://github.com/...)
- 💻 [源代码](https://github.com/...)
- ⭐ 如果有帮助，请给 Star！
        """)
    
    return demo


if __name__ == "__main__":
    # 初始化组件
    print("初始化组件...")
    init_msg = initialize_components()
    print(init_msg)
    
    # 构建界面
    print("构建界面...")
    demo = build_interface()
    
    # 启动应用
    print("启动应用...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        debug=False
    )
