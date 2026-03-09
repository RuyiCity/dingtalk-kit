# DingTalk Kit - 钉钉消息工具包

一个功能完整的钉钉消息发送工具包，支持多种消息格式、主动发送、长文本自动处理。

## 🚀 功能特性

- ✅ **多种消息格式**：文本、Markdown、ActionCard、图片、文件
- ✅ **主动发送**：支持发送到群和个人
- ✅ **长文本处理**：自动拆分超长消息
- ✅ **无按钮模式**：Markdown 格式直接查看，无需跳转
- ✅ **简单易用**：一行命令发送消息

## 📦 安装

```bash
# 克隆到技能目录
git clone https://github.com/yourname/dingtalk-kit ~/.openclaw/skills/dingtalk-kit

# 或者手动复制
cp -r dingtalk-kit ~/.openclaw/skills/
```

## ⚙️ 配置

### 第一步：钉钉开放平台配置

1. **访问钉钉开放平台**
   - 网址：https://open.dingtalk.com
   - 用钉钉扫码登录

2. **创建企业内部应用**
   - 点击「应用开发」→「企业内部应用」
   - 点击「创建应用」
   - 填写应用名称（如：OpenClaw助手）
   - 选择应用类型：「机器人」

3. **获取密钥信息**
   - 进入应用 →「凭证与基础信息」
   - 复制 **Client ID**（即 AppKey）
   - 复制 **Client Secret**（即 AppSecret）
   - 记录 **AgentId**

4. **配置机器人**
   - 左侧菜单 →「机器人」
   - 开启「机器人能力」
   - 设置机器人名称和头像
   - 记录 **RobotCode**

5. **配置事件订阅（Stream模式）**
   - 左侧菜单 →「事件订阅」
   - 选择「Stream 模式」
   - 添加订阅事件：`im.message.receive_v1`
   - 点击「保存」

6. **发布应用**
   - 左侧菜单 →「版本管理与发布」
   - 点击「创建版本」
   - 填写版本号（如：1.0.0）
   - 点击「保存并发布」

7. **添加机器人到群**
   - 打开钉钉群
   - 群设置 → 智能群助手
   - 添加机器人 → 选择你的应用
   - 完成后，在群里@机器人测试

### 第二步：获取群ID

**方法1：从日志获取（推荐）**
```bash
# 在群里发一条消息，查看 OpenClaw 日志
openclaw logs --follow
# 找到 conversationId，如：cidI95q3seolfS//sX0D3YeHg==
```

**方法2：通过API获取**
```python
from dingtalk_kit import DingTalkKit
kit = DingTalkKit()
# 先配置好 app_key 和 app_secret
# 然后调用获取群列表的API
```

### 第三步：编辑配置文件

创建 `dingtalk_config.json`：

```json
{
  "app_key": "dingxxxxxxxxx",
  "app_secret": "你的AppSecret",
  "robot_code": "dingxxxxxxxxx",
  "agent_id": "123456789",
  "default_chat_id": "cidxxxxxxxxxxx"
}
```

**文件位置（三选一）：**
- 当前目录：`./dingtalk_config.json`
- OpenClaw目录：`~/.openclaw/dingtalk_config.json`
- 系统目录：`~/.dingtalk/config.json`

---

## 🚀 快速开始（5分钟上手）

```bash
# 1. 复制技能到 OpenClaw 目录
cp -r dingtalk-kit ~/.openclaw/skills/

# 2. 复制配置模板
cp dingtalk_config.json.example dingtalk_config.json

# 3. 编辑配置（填入你的密钥）
nano dingtalk_config.json

# 4. 测试配置
python -m dingtalk_kit test

# 5. 发送第一条消息
python -m dingtalk_kit markdown -t "Hello" -c "钉钉消息测试"
```

✅ **完成！现在你可以主动发送钉钉消息了！**

## 📝 使用方法

### 1. 发送到群（主动发送）

#### 方法A：发送 Markdown（推荐）
无按钮，直接查看，支持约 3000 字：

```bash
python -m dingtalk_kit markdown -t "消息标题" -c "消息内容" --chat-id "cidxxxxx"
```

**简化版（使用默认群）：**
```bash
python -m dingtalk_kit markdown -t "通知" -c "大家好，系统已更新"
```

#### 方法B：发送 ActionCard
带按钮，支持约 5000 字：

```bash
python -m dingtalk_kit actioncard \
  -t "重要通知" \
  -c "长文本内容..." \
  --button-text "查看详情" \
  --button-url "https://example.com" \
  --chat-id "cidxxxxx"
```

#### 方法C：发送长文本（自动拆分）
超过 3000 字自动拆分成多条 Markdown：

```bash
# 从文件读取
python -m dingtalk_kit long -t "长文章" -f "article.txt"

# 或直接输入（用引号包裹）
python -m dingtalk_kit long -t "报告" -c "$(cat report.md)"
```

### 2. 发送给个人（主动发送）

#### 工作通知（私聊）
发送到用户的钉钉私聊：

```bash
python -m dingtalk_kit user -u "manager3952" -c "您好，任务已完成"
```

**获取用户ID的方法：**
- 在群里@用户，查看日志中的 `senderStaffId`
- 或通过钉钉管理后台查看

**批量发送给多人：**
```python
from dingtalk_kit import DingTalkKit

kit = DingTalkKit()
user_ids = ["user1", "user2", "user3"]

for user_id in user_ids:
    kit.send_to_user(user_id, "群发消息测试")
```

### 2. 发送 ActionCard

带按钮，支持约 5000 字：

```bash
python -m dingtalk_kit send_actioncard \
  --title "消息标题" \
  --content "消息内容..." \
  --button-text "查看详情" \
  --button-url "https://example.com" \
  --chat-id "cidxxxxx"
```

### 3. 发送给个人

```bash
python -m dingtalk_kit send_to_user \
  --user-id "manager3952" \
  --content "消息内容"
```

### 4. 发送长文本（自动拆分）

超过 3000 字自动拆分成多条：

```bash
python -m dingtalk_kit send_long \
  --title "长文标题" \
  --file "article.txt" \
  --chat-id "cidxxxxx"
```

### 5. 发送图片

```bash
python -m dingtalk_kit send_image \
  --image "screenshot.png" \
  --chat-id "cidxxxxx"
```

### 6. 发送文件

```bash
python -m dingtalk_kit send_file \
  --file "document.pdf" \
  --chat-id "cidxxxxx"
```

## 💡 使用示例

### 示例1：发送通知

```bash
python -m dingtalk_kit send_markdown \
  --title "🎉 系统通知" \
  --content "## 更新完成\n\n系统已更新到最新版本，新功能：\n- 功能1\n- 功能2\n- 功能3" \
  --chat-id "cidI95q3seolfS//sX0D3YeHg=="
```

### 示例2：发送长文章

```bash
python -m dingtalk_kit send_markdown \
  --title "📖 OpenClaw 介绍" \
  --content "## 什么是 OpenClaw？\n\nOpenClaw 是一个开源的 AI 助手平台..." \
  --chat-id "cidI95q3seolfS//sX0D3YeHg=="
```

### 示例3：发送给个人

```bash
python -m dingtalk_kit send_to_user \
  --user-id "manager3952" \
  --content "您好，任务已完成，请查收。"
```

## 🔧 Python API 使用

### 完整示例

```python
from dingtalk_kit import DingTalkKit

# 初始化（自动读取配置文件）
kit = DingTalkKit()

# ========== 发送到群（主动发送）==========

# 1. 发送 Markdown（推荐，无按钮，直接查看）
kit.send_markdown(
    chat_id="cidI95q3seolfS//sX0D3YeHg==",
    title="📢 系统通知",
    content="## 更新完成\n\n系统已更新到最新版本"
)

# 2. 发送 ActionCard（带按钮）
kit.send_actioncard(
    chat_id="cidI95q3seolfS//sX0D3YeHg==",
    title="重要公告",
    content="长文本内容...",
    button_text="查看详情",
    button_url="https://www.example.com"
)

# 3. 发送纯文本
kit.send_text(
    chat_id="cidI95q3seolfS//sX0D3YeHg==",
    content="简单文本消息"
)

# 4. 发送长文本（自动拆分多条）
kit.send_long_text(
    chat_id="cidI95q3seolfS//sX0D3YeHg==",
    title="📖 长文章",
    content="超过3000字的长内容...",
    max_length=2800  # 自定义单条长度
)

# ========== 发送给个人（主动发送）==========

# 工作通知（发送到用户私聊）
kit.send_to_user(
    user_id="manager3952",
    content="您好，您负责的任务已到期，请尽快处理。"
)

# 批量发送
users = ["user1", "user2", "user3"]
for user in users:
    kit.send_to_user(user, "群发通知：本周五下午开会")
```

### 高级用法

```python
# 自定义配置（不读取配置文件）
kit = DingTalkKit(
    app_key="dingxxxxxx",
    app_secret="your_secret",
    robot_code="dingxxxxxx",
    agent_id="123456789"
)

# 使用默认群ID（在配置文件中设置）
kit.send_markdown(
    title="通知",  # 不传入 chat_id，使用默认值
    content="使用默认群发送"
)
```

## 📊 消息格式对比

| 格式 | 字数限制 | 有按钮 | 直接查看 | 适用场景 |
|------|---------|--------|----------|----------|
| 纯文本 | ~500字 | ❌ | ✅ | 简单通知 |
| **Markdown** | ~3000字 | ❌ | ✅ | **推荐：长文本** |
| ActionCard | ~5000字 | ✅ | ✅ | 长文本+跳转 |
| 图片 | 无限制 | ❌ | ✅ | 超长内容 |
| 文件 | 无限制 | ❌ | ❌ | 附件下载 |

## 🔒 安全提示

- 不要将 `app_secret` 提交到代码仓库
- 使用环境变量或配置文件管理密钥
- 定期更换密钥

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

**Made with ❤️ by OpenClaw Community**
