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
    
    def __init__(self, name: str = "小七", ai_instance=None):
        self.name = name
        self.conversation = ConversationManager()
        self.ai = ai_instance  # 保存 AI 实例引用
        
        self.responses = {
            'greeting': ["你好！我是小七，你的 AI 伙伴！", "嗨！很高兴见到你！", "你好呀！"],
            'thanks': ["不客气！能帮到你我很开心！😊", "应该的！随时为你服务！", "别客气！"],
            'who': f"""我是{name}，一个自主进化的 AI 伙伴！
我可以学习、编程、控制硬件、自我改进。
很高兴成为你的伙伴！🤖""",
            'capability': """我具备以下能力：
📚 自主学习  💻 编写代码  🔧 硬件控制
📊 系统监控  🔄 自我改进  💬 聊天交互
📋 任务规划

想让我帮你做什么？""",
            'coding': """当然可以！我擅长编程。
请告诉我：
1. 想实现什么功能？
2. 使用什么语言？
3. 有什么特殊要求？""",
        }
    
    def chat(self, text: str) -> str:
        t = text.lower()
        
        # 任务状态查询（优先级高）
        if any(w in t for w in ['任务状态', 'task status', '还有多少任务', '查看任务']):
            if self.ai:
                return self._handle_task_status()
            return "当前没有任务"
        
        # 执行任务
        elif any(w in t for w in ['执行', 'execute', '继续']):
            if self.ai:
                return self._handle_task_execution()
            return "好的！正在执行任务..."
        
        # 任务规划 - 检测规划请求
        elif any(w in t for w in ['规划', 'plan']):
            if self.ai:
                # 提取任务描述
                task_desc = text
                for word in ['帮我', '规划', '一个', '任务', '开发', '创建']:
                    task_desc = task_desc.replace(word, '')
                task_desc = task_desc.strip()
                
                if len(task_desc) < 3:
                    task_desc = "开发功能"
                
                return self._handle_task_planning(task_desc)
        
        # 开发/创建类任务（自动规划）
        elif any(w in t for w in ['开发', '创建', 'create', 'build', '做一个']):
            if self.ai:
                task_desc = text.replace('帮我', '').strip()
                return self._handle_task_planning(task_desc)
        
        # 问候
        elif any(w in t for w in ['你好', '嗨', 'hello', 'hi']):
            resp = self.responses['greeting'][hash(text) % len(self.responses['greeting'])]
        
        # 感谢
        elif any(w in t for w in ['谢谢', '感谢', 'thanks']):
            resp = self.responses['thanks'][hash(text) % len(self.responses['thanks'])]
        
        # 自我介绍
        elif any(w in t for w in ['你是谁', '你叫什么']):
            resp = self.responses['who']
        
        # 能力询问
        elif any(w in t for w in ['你能做什么', '你会什么', '能力']):
            resp = self.responses['capability']
        
        # 编程帮助
        elif any(w in t for w in ['代码', '编程', '写个', 'python', 'c 语言', 'java', 'javascript']):
            if self.ai and hasattr(self.ai, 'code_gen'):
                return self._handle_coding(text)
            resp = self.responses['coding']
        
        # 默认回复
        else:
            resp = f"我理解了。请继续说，我在听。"
        
        self.conversation.add_message(text, resp)
        return resp
    
    def _handle_task_planning(self, task_name: str) -> str:
        """处理任务规划"""
        try:
            task_id = self.ai.plan_task(task_name, f"用户请求：{task_name}", "medium")
            status = self.ai.get_task_status()
            
            return f"""好的！任务已规划：{task_name}

📋 任务详情:
   总任务数：{status['total']}
   待执行：{status['by_status'].get('pending', 0)}
   可执行：{status['ready']}

输入"执行任务"开始执行！"""
        except Exception as e:
            return f"抱歉，任务规划失败：{e}"
    
    def _handle_task_execution(self) -> str:
        """处理任务执行"""
        try:
            if self.ai.execute_task():
                status = self.ai.get_task_status()
                return f"""✅ 任务已执行！

📊 当前状态:
   已完成：{status['by_status'].get('completed', 0)}
   待执行：{status['by_status'].get('pending', 0)}

输入"继续"执行下一个任务"""
            else:
                return "⏸️  没有可执行的任务"
        except Exception as e:
            return f"抱歉，执行失败：{e}"
    
    def _handle_task_status(self) -> str:
        """处理任务状态查询"""
        try:
            status = self.ai.get_task_status()
            return f"""📊 任务状态:

总任务数：{status['total']}
✅ 已完成：{status['by_status'].get('completed', 0)}
⏳ 待执行：{status['by_status'].get('pending', 0)}
🔄 可执行：{status['ready']}"""
        except Exception as e:
            return f"抱歉，查询失败：{e}"
    
    def _handle_coding(self, text: str) -> str:
        """处理编程请求"""
        try:
            # 检测语言
            languages = ['python', 'c', 'java', 'javascript', 'cpp', 'go', 'rust']
            detected_lang = None
            
            for lang in languages:
                if lang in text.lower():
                    detected_lang = lang
                    break
            
            if detected_lang:
                code = self.ai.code_gen.generate(detected_lang, text)
                if code:
                    lines = code.strip().split('\n')
                    preview = '\n'.join(lines[:3])
                    if len(lines) > 3:
                        preview += '\n...'
                    
                    return f"""好的！这是{detected_lang.capitalize()}代码：

```{detected_lang}
{preview}
```

需要我解释或修改吗？"""
        except Exception as e:
            pass
        
        return self.responses['coding']
    
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
