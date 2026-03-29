#!/usr/bin/env python3
"""
快速测试对话系统
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI

def test():
    ai = AutonomousAI(name="小七")
    
    tests = [
        ("你好", "问候测试"),
        ("开发用户登录功能", "任务规划测试"),
        ("执行任务", "任务执行测试"),
        ("任务状态", "状态查询测试"),
        ("用 Python 写个快速排序", "代码生成测试"),
        ("谢谢", "感谢测试"),
    ]
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         💬 对话系统测试                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    for text, desc in tests:
        print(f"[{desc}]")
        print(f"你：{text}")
        resp = ai.chat(text)
        # 截取前 200 字符
        preview = resp[:200] + "..." if len(resp) > 200 else resp
        print(f"小七：{preview}\n")
    
    print("✅ 测试完成！")

if __name__ == '__main__':
    test()
