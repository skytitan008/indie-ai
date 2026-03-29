#!/usr/bin/env python3
"""
对话管理模块 - 让 AI 能和你文字聊天
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class ConversationManager:
    """对话管理器"""
    
    def __init__(self, db_path: str = "ai_memory.db"):
        self.db_path = PROJECT_ROOT / db_path
        self._init_db()
        self.history = []
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            ai_response TEXT,
            topic TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
    
    def add_message(self, user_input: str, ai_response: str, topic: str = "chat"):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO conversations (user_input, ai_response, topic) VALUES (?, ?, ?)',
                  (user_input, ai_response, topic))
        conn.commit()
        conn.close()
        self.history.append({'user': user_input, 'ai': ai_response, 'time': datetime.now()})
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM conversations ORDER BY timestamp DESC LIMIT ?', (limit,))
        results = [dict(row) for row in c.fetchall()]
        conn.close()
        return results


class ChatBot:
    """聊天机器人"""
    
    def __init__(self, name: str = "小七"):
        self.name = name
        self.conversation = ConversationManager()
        
        self.responses = {
            'greeting': ["你好！我是小七，你的 AI 伙伴！", "嗨！很高兴见到你！", "你好呀！"],
            'thanks': ["不客气！能帮到你我很开心！😊", "应该的！随时为你服务！", "别客气！"],
            'who': f"""我是{name}，一个自主进化的 AI 伙伴！
我可以学习、编程、控制硬件、自我改进。
很高兴成为你的伙伴！🤖""",
            'capability': """我具备以下能力：
📚 自主学习  💻 编写代码  🔧 硬件控制
📊 系统监控  🔄 自我改进  💬 聊天交互

想让我帮你做什么？""",
            'coding': """当然可以！我擅长编程。
请告诉我：
1. 想实现什么功能？
2. 使用什么语言？
3. 有什么特殊要求？""",
        }
    
    def chat(self, text: str) -> str:
        t = text.lower()
        
        if any(w in t for w in ['你好', '嗨', 'hello', 'hi']):
            resp = self.responses['greeting'][hash(text) % len(self.responses['greeting'])]
        elif any(w in t for w in ['谢谢', '感谢', 'thanks']):
            resp = self.responses['thanks'][hash(text) % len(self.responses['thanks'])]
        elif any(w in t for w in ['你是谁', '你叫什么']):
            resp = self.responses['who']
        elif any(w in t for w in ['你能做什么', '你会什么']):
            resp = self.responses['capability']
        elif any(w in t for w in ['代码', '编程', 'python', 'c 语言']):
            resp = self.responses['coding']
        else:
            resp = f"我理解了。请继续说，我在听。"
        
        self.conversation.add_message(text, resp)
        return resp
    
    def start_chat(self):
        print(f"\n💬 聊天模式已启动（输入 quit 退出）\n")
        while True:
            try:
                text = input("你：").strip()
                if text.lower() in ['quit', 'exit', '退出']:
                    print(f"{self.name}：再见！👋")
                    break
                if not text: continue
                print(f"{self.name}：{self.chat(text)}\n")
            except KeyboardInterrupt:
                print("\n再见！👋")
                break


def demo():
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         💬 对话系统演示                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    bot = ChatBot()
    
    tests = ["你好", "你是谁？", "你能做什么？", "帮我写代码", "谢谢"]
    for t in tests:
        print(f"你：{t}")
        print(f"小七：{bot.chat(t)}\n")
    
    print("✅ 演示完成！\n")


if __name__ == '__main__':
    demo()
