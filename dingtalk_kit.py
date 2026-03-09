#!/usr/bin/env python3
"""
DingTalk Kit - 钉钉消息工具包
核心模块
"""

import json
import urllib.request
import urllib.error
import ssl
import os
from typing import Optional, List

class DingTalkKit:
    """钉钉消息工具包主类"""
    
    def __init__(self, app_key: str = None, app_secret: str = None, 
                 robot_code: str = None, agent_id: str = None):
        """
        初始化
        
        Args:
            app_key: 钉钉 AppKey
            app_secret: 钉钉 AppSecret
            robot_code: 机器人 Code
            agent_id: 应用 AgentId
        """
        # 从参数或配置文件读取
        config = self._load_config()
        
        self.app_key = app_key or config.get('app_key')
        self.app_secret = app_secret or config.get('app_secret')
        self.robot_code = robot_code or config.get('robot_code')
        self.agent_id = agent_id or config.get('agent_id')
        self.default_chat_id = config.get('default_chat_id')
        
        self._access_token = None
        self._token_expire_time = 0
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_paths = [
            'dingtalk_config.json',
            os.path.expanduser('~/.openclaw/dingtalk_config.json'),
            os.path.expanduser('~/.dingtalk/config.json')
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        return {}
    
    def _get_access_token(self) -> Optional[str]:
        """获取 access_token"""
        import time
        
        # 检查缓存
        if self._access_token and time.time() < self._token_expire_time:
            return self._access_token
        
        url = f"https://oapi.dingtalk.com/gettoken?appkey={self.app_key}&appsecret={self.app_secret}"
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            req = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('errcode') == 0:
                    self._access_token = result['access_token']
                    # 提前5分钟过期
                    self._token_expire_time = time.time() + 7200 - 300
                    return self._access_token
                else:
                    print(f"[ERROR] 获取token失败: {result.get('errmsg')}")
                    return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def _send_message(self, open_id: str, msg_key: str, msg_param: dict) -> bool:
        """发送消息底层方法"""
        token = self._get_access_token()
        if not token:
            return False
        
        url = "https://api.dingtalk.com/v1.0/robot/groupMessages/send"
        
        payload = {
            "robotCode": self.robot_code,
            "openConversationId": open_id,
            "msgKey": msg_key,
            "msgParam": json.dumps(msg_param)
        }
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-acs-dingtalk-access-token': token
        }
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('success') or result.get('processQueryKey'):
                    print(f"[OK] 消息发送成功")
                    return True
                else:
                    print(f"[ERROR] 发送失败: {result}")
                    return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    
    def send_markdown(self, title: str, content: str, chat_id: str = None) -> bool:
        """
        发送 Markdown 消息（无按钮，直接查看）
        
        Args:
            title: 消息标题
            content: Markdown 内容
            chat_id: 群ID，不传则使用默认群
        """
        chat_id = chat_id or self.default_chat_id
        if not chat_id:
            print("[ERROR] 未指定群ID")
            return False
        
        return self._send_message(
            chat_id,
            "sampleMarkdown",
            {"title": title, "text": content}
        )
    
    def send_actioncard(self, title: str, content: str, 
                       button_text: str = "查看详情", 
                       button_url: str = "https://www.dingtalk.com",
                       chat_id: str = None) -> bool:
        """
        发送 ActionCard 消息（带按钮）
        
        Args:
            title: 消息标题
            content: Markdown 内容
            button_text: 按钮文字
            button_url: 按钮跳转链接
            chat_id: 群ID
        """
        chat_id = chat_id or self.default_chat_id
        if not chat_id:
            print("[ERROR] 未指定群ID")
            return False
        
        return self._send_message(
            chat_id,
            "sampleActionCard",
            {
                "title": title,
                "markdown": content,
                "singleTitle": button_text,
                "singleURL": button_url
            }
        )
    
    def send_text(self, content: str, chat_id: str = None) -> bool:
        """
        发送纯文本消息
        
        Args:
            content: 消息内容
            chat_id: 群ID
        """
        chat_id = chat_id or self.default_chat_id
        if not chat_id:
            print("[ERROR] 未指定群ID")
            return False
        
        return self._send_message(
            chat_id,
            "sampleText",
            {"content": content}
        )
    
    def send_to_user(self, user_id: str, content: str) -> bool:
        """
        发送消息给个人（工作通知）
        
        Args:
            user_id: 用户ID
            content: 消息内容
        """
        token = self._get_access_token()
        if not token:
            return False
        
        url = f"https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token={token}"
        
        data = {
            "agent_id": self.agent_id,
            "userid_list": user_id,
            "msg": {
                "msgtype": "text",
                "text": {"content": content}
            }
        }
        
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('errcode') == 0:
                    print(f"[OK] 发送给用户 {user_id} 成功")
                    return True
                else:
                    print(f"[ERROR] 发送失败: {result.get('errmsg')}")
                    return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    
    def send_long_text(self, title: str, content: str, chat_id: str = None,
                      max_length: int = 2800) -> bool:
        """
        发送长文本（自动拆分多条消息）
        
        Args:
            title: 消息标题
            content: 长文本内容
            chat_id: 群ID
            max_length: 单条消息最大长度
        """
        chat_id = chat_id or self.default_chat_id
        if not chat_id:
            print("[ERROR] 未指定群ID")
            return False
        
        # 如果内容不长，直接发送
        if len(content) <= max_length:
            return self.send_markdown(title, content, chat_id)
        
        # 拆分发送
        parts = []
        current_part = ""
        lines = content.split('\n')
        
        for line in lines:
            if len(current_part) + len(line) + 1 > max_length and current_part:
                parts.append(current_part)
                current_part = line + "\n"
            else:
                current_part += line + "\n"
        
        if current_part:
            parts.append(current_part)
        
        # 分批发送
        total = len(parts)
        for i, part in enumerate(parts, 1):
            part_title = f"{title} ({i}/{total})" if total > 1 else title
            print(f"[INFO] 发送第 {i}/{total} 部分...")
            if not self.send_markdown(part_title, part.strip(), chat_id):
                return False
        
        print(f"[OK] 长文本已拆分为 {total} 条消息发送")
        return True


# 便捷函数
def send_markdown(title: str, content: str, chat_id: str = None) -> bool:
    """快捷发送 Markdown"""
    kit = DingTalkKit()
    return kit.send_markdown(title, content, chat_id)

def send_text(content: str, chat_id: str = None) -> bool:
    """快捷发送文本"""
    kit = DingTalkKit()
    return kit.send_text(content, chat_id)

def send_to_user(user_id: str, content: str) -> bool:
    """快捷发送给个人"""
    kit = DingTalkKit()
    return kit.send_to_user(user_id, content)

def send_long_text(title: str, content: str, chat_id: str = None) -> bool:
    """快捷发送长文本"""
    kit = DingTalkKit()
    return kit.send_long_text(title, content, chat_id)
