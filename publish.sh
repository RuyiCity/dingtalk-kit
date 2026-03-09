#!/bin/bash
# 发布到 GitHub 的脚本

echo "🚀 准备发布 DingTalk Kit 到 GitHub"
echo ""

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 请先安装 Git"
    exit 1
fi

# 初始化 git
git init

# 添加文件
git add .

# 提交
git commit -m "Initial commit: DingTalk Kit for OpenClaw

Features:
- Send messages to DingTalk groups and individuals
- Multiple formats: Markdown, ActionCard, Text, Image, File
- Long text auto-split
- Command line and Python API
- Easy configuration

See README.md for usage instructions."

# 添加远程仓库（需要手动替换）
echo ""
echo "📋 下一步操作："
echo ""
echo "1. 在 GitHub 创建新仓库（不要初始化）"
echo "   仓库名：dingtalk-kit"
echo ""
echo "2. 运行以下命令："
echo "   git remote add origin https://github.com/你的用户名/dingtalk-kit.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 完成！🎉"
