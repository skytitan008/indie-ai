#!/usr/bin/env python3
"""
小七编程助手演示

展示 AI 如何帮你写代码
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI
from src.interaction.chat.code_generator import CodeGenerator


def demo():
    """演示编程帮助"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         💻 小七编程助手演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    # 测试代码生成
    gen = CodeGenerator()
    
    print("="*60)
    print("📝 代码生成测试")
    print("="*60 + "\n")
    
    tests = [
        ("Python", "快速排序"),
        ("Python", "Hello World"),
        ("C", "Hello World"),
        ("JavaScript", "函数定义"),
        ("Java", "类定义"),
        ("C++", "Hello World"),
        ("Go", "Hello World"),
        ("Rust", "Hello World"),
    ]
    
    for lang, task in tests:
        code = gen.generate(lang, task)
        print(f"📄 {lang} - {task}")
        if code:
            lines = code.strip().split('\n')
            preview = lines[0] + ('...' if len(lines) > 1 else '')
            print(f"   ✅ {preview[:60]}")
        else:
            print(f"   ❌ 未找到模板")
        print()
    
    print("="*60)
    print("💬 对话测试")
    print("="*60 + "\n")
    
    # 对话测试
    questions = [
        "你好",
        "你能帮我写代码吗",
        "用 Python 写个快速排序",
        "谢谢",
    ]
    
    for q in questions:
        print(f"你：{q}")
        response = ai.chat(q)
        print(f"小七：{response}\n")
    
    print("="*60)
    print("📊 系统状态")
    print("="*60 + "\n")
    
    ai.show_status()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 演示完成！                                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("💡 使用方式:")
    print("   python3 xiaoqi.py  # 启动交互界面")
    print("   或直接调用 API:")
    print("   ai.chat('用 Python 写个快速排序')\n")


if __name__ == '__main__':
    demo()
