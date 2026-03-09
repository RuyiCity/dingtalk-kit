# DingTalk Kit for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Plugin-green.svg)](https://openclaw.ai)

> 一个功能完整的钉钉消息发送工具包，支持多种消息格式、主动发送、长文本自动处理。

[English](#english) | [中文](#中文)

---

## 中文

### 🚀 功能特性

- ✅ **多种消息格式**：文本、Markdown、ActionCard、图片、文件
- ✅ **主动发送**：支持发送到群和个人（工作通知）
- ✅ **长文本处理**：自动拆分超长消息
- ✅ **无按钮模式**：Markdown 格式直接查看，无需跳转
- ✅ **简单易用**：一行命令发送消息

### 📦 安装

```bash
# 克隆到 OpenClaw 技能目录
git clone https://github.com/yourname/dingtalk-kit.git ~/.openclaw/skills/dingtalk-kit

# 或者手动下载解压到 ~/.openclaw/skills/dingtalk-kit/
```

### ⚙️ 快速配置

1. **复制配置模板**
   ```bash
   cd ~/.openclaw/skills/dingtalk-kit
   cp dingtalk_config.json.example dingtalk_config.json
   ```

2. **编辑配置**
   ```bash
   # 填入你的钉钉应用信息
   nano dingtalk_config.json
   ```

3. **测试配置**
   ```bash
   python -m dingtalk_kit test
   ```

### 📝 使用方法

#### 发送到群（主动发送）

```bash
# Markdown 格式（推荐，无按钮）
python -m dingtalk_kit markdown -t "通知标题" -c "消息内容"

# ActionCard 格式（带按钮）
python -m dingtalk_kit actioncard -t "标题" -c "内容" --button-text "查看" --button-url "https://..."

# 长文本（自动拆分）
python -m dingtalk_kit long -t "长文章" -f "article.txt"
```

#### 发送给个人（主动发送）

```bash
# 工作通知（私聊）
python -m dingtalk_kit user -u "manager3952" -c "您好，任务已完成"
```

### 🔧 Python API

```python
from dingtalk_kit import DingTalkKit

kit = DingTalkKit()

# 发送到群
kit.send_markdown("标题", "内容", "cidxxxxx")

# 发送给个人
kit.send_to_user("user_id", "消息内容")

# 发送长文本（自动拆分）
kit.send_long_text("标题", "超长内容..." * 1000)
```

---

## English

### 🚀 Features

- ✅ **Multiple Message Formats**: Text, Markdown, ActionCard, Image, File
- ✅ **Proactive Sending**: Send to groups and individuals (work notifications)
- ✅ **Long Text Handling**: Automatically split超长 messages
- ✅ **No Button Mode**: Markdown format for direct viewing without jumping
- ✅ **Easy to Use**: Send messages with one command

### 📦 Installation

```bash
git clone https://github.com/yourname/dingtalk-kit.git ~/.openclaw/skills/dingtalk-kit
```

### ⚙️ Quick Setup

```bash
cd ~/.openclaw/skills/dingtalk-kit
cp dingtalk_config.json.example dingtalk_config.json
# Edit dingtalk_config.json with your credentials
python -m dingtalk_kit test
```

### 📝 Usage

```bash
# Send to group
python -m dingtalk_kit markdown -t "Title" -c "Content"

# Send to individual
python -m dingtalk_kit user -u "user_id" -c "Message"

# Send long text (auto-split)
python -m dingtalk_kit long -t "Title" -f "article.txt"
```

---

## 📊 Message Format Comparison

| Format | Character Limit | Button | Direct View | Use Case |
|--------|----------------|--------|-------------|----------|
| Text | ~500 | ❌ | ✅ | Simple notifications |
| **Markdown** | ~3000 | ❌ | ✅ | **Recommended: Long text** |
| ActionCard | ~5000 | ✅ | ✅ | Long text + link |
| Image | Unlimited | ❌ | ✅ | Very long content |
| File | Unlimited | ❌ | ❌ | Attachments |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🤝 Contributing

Pull requests are welcome! Please feel free to submit issues and enhancement requests.

## 🙏 Acknowledgments

- Built for [OpenClaw](https://openclaw.ai)
- Powered by [DingTalk Open API](https://open.dingtalk.com)

---

**Made with ❤️ by OpenClaw Community**
