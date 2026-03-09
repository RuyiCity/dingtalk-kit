# DingTalk Kit for OpenClaw

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Plugin-green.svg)](https://openclaw.ai)

> A complete DingTalk messaging toolkit for OpenClaw - supporting multiple formats, proactive sending, and long text handling.

[中文文档](README.md) | [English](#english)

---

## Features

- ✅ **Multiple Formats**: Text, Markdown, ActionCard, Image, File
- ✅ **Proactive Sending**: Send to groups and individuals
- ✅ **Long Text**: Auto-split long messages
- ✅ **No Button**: Markdown for direct viewing
- ✅ **Easy to Use**: One command to send

## Quick Start

```bash
# Install
git clone https://github.com/RuyiCity/dingtalk-kit.git ~/.openclaw/skills/dingtalk-kit

# Configure
cp dingtalk_config.json.example dingtalk_config.json
# Edit with your credentials

# Test
python -m dingtalk_kit test

# Send message
python -m dingtalk_kit markdown -t "Hello" -c "World"
```

## Usage

### Send to Group
```bash
python -m dingtalk_kit markdown -t "Title" -c "Content"
```

### Send to Individual
```bash
python -m dingtalk_kit user -u "user_id" -c "Message"
```

### Send Long Text
```bash
python -m dingtalk_kit long -t "Title" -f "article.txt"
```

## API Usage

```python
from dingtalk_kit import DingTalkKit

kit = DingTalkKit()
kit.send_markdown("Title", "Content")
kit.send_to_user("user_id", "Message")
```

## License

MIT License
