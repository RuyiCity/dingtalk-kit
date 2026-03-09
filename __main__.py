#!/usr/bin/env python3
"""
DingTalk Kit - 命令行工具
"""

import argparse
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dingtalk_kit import DingTalkKit, send_markdown, send_text, send_to_user, send_long_text

def main():
    parser = argparse.ArgumentParser(description='钉钉消息发送工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 发送 Markdown
    md_parser = subparsers.add_parser('markdown', help='发送 Markdown 消息')
    md_parser.add_argument('--title', '-t', required=True, help='消息标题')
    md_parser.add_argument('--content', '-c', required=True, help='消息内容')
    md_parser.add_argument('--chat-id', help='群ID')
    
    # 发送文本
    text_parser = subparsers.add_parser('text', help='发送文本消息')
    text_parser.add_argument('--content', '-c', required=True, help='消息内容')
    text_parser.add_argument('--chat-id', help='群ID')
    
    # 发送给个人
    user_parser = subparsers.add_parser('user', help='发送给个人')
    user_parser.add_argument('--user-id', '-u', required=True, help='用户ID')
    user_parser.add_argument('--content', '-c', required=True, help='消息内容')
    
    # 发送长文本
    long_parser = subparsers.add_parser('long', help='发送长文本（自动拆分）')
    long_parser.add_argument('--title', '-t', required=True, help='消息标题')
    long_parser.add_argument('--file', '-f', required=True, help='文本文件路径')
    long_parser.add_argument('--chat-id', help='群ID')
    
    # 测试配置
    test_parser = subparsers.add_parser('test', help='测试配置')
    
    args = parser.parse_args()
    
    if args.command == 'markdown':
        success = send_markdown(args.title, args.content, args.chat_id)
        sys.exit(0 if success else 1)
    
    elif args.command == 'text':
        success = send_text(args.content, args.chat_id)
        sys.exit(0 if success else 1)
    
    elif args.command == 'user':
        success = send_to_user(args.user_id, args.content)
        sys.exit(0 if success else 1)
    
    elif args.command == 'long':
        if not os.path.exists(args.file):
            print(f"[ERROR] 文件不存在: {args.file}")
            sys.exit(1)
        
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        success = send_long_text(args.title, content, args.chat_id)
        sys.exit(0 if success else 1)
    
    elif args.command == 'test':
        kit = DingTalkKit()
        if kit.app_key and kit.app_secret:
            print("[OK] 配置加载成功")
            print(f"  AppKey: {kit.app_key[:10]}...")
            print(f"  RobotCode: {kit.robot_code}")
            print(f"  DefaultChat: {kit.default_chat_id}")
        else:
            print("[ERROR] 配置未找到，请检查 dingtalk_config.json")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
