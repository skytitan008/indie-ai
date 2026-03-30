#!/usr/bin/env python3
"""
小七自主思维测试 v3.0

核心突破:
- 遇到问题主动找答案
- 不知道就学，学了再回答
- 像人类一样的思考过程

用法：
python3 test_autonomous_mind.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.independent.mind_v3 import AutonomousMind


def interactive_test():
    """交互式测试 v3.0"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七自主思维测试 v3.0                       ║")
    print("║         遇到问题 → 主动找答案 → 学习 → 回答            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("👋 你好，我是小七 v3.0！")
    print()
    print("🌟 我的新能力:")
    print("   ✅ 遇到问题会主动找答案")
    print("   ✅ 不知道的知识会主动学习")
    print("   ✅ 学了之后再回答你")
    print("   ✅ 像人类一样的思考过程")
    print()
    print("📋 试试问我:")
    print("   - 情景对话：'你好！' '吃饭了吗？' '谢谢！'")
    print("   - 未知问题：'量子力学是什么？' '相对论是什么？'")
    print("   - 我会主动学习并回答！")
    print("   - '状态' - 查看我的学习历史")
    print("   - '退出' - 结束对话")
    print()
    print("="*60)
    print()
    
    # 创建小七
    mind = AutonomousMind("小七")
    
    # 对话循环
    while True:
        try:
            user_input = input("👤 老王：").strip()
            
            if not user_input:
                continue
            
            if user_input in ['退出', 'exit', 'quit', 'q']:
                print("\n👋 小七：再见！下次再聊！😊\n")
                break
            
            if user_input == '状态':
                status = mind.get_status()
                print("\n📊 小七的状态:\n")
                print(f"   记忆数量：{status['memory_count']} 条")
                print(f"   交互次数：{status['interaction_count']} 次")
                print(f"   主动学习：{status['learned_count']} 次")
                print(f"   知识主题：{status['knowledge_topics']} 个")
                print()
                mind.show_learning_history()
                continue
            
            if user_input == '反思':
                reflection = mind.reflect()
                print("\n🔍 小七的自我反思:\n")
                for key, value in reflection.items():
                    if isinstance(value, dict):
                        for k, v in value.items():
                            print(f"   {k}: {v}")
                    else:
                        print(f"   {key}: {value}")
                print()
                continue
            
            # 自主回应
            response = mind.respond(user_input)
            
            print(f"\n🤖 小七：{response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 小七：下次再聊！😊\n")
            break
        except Exception as e:
            print(f"\n❌ 小七：出错了 - {e}\n")
            import traceback
            traceback.print_exc()


def demo_autonomous_learning():
    """演示自主学习"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七自主学习演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    mind = AutonomousMind("小七")
    
    # 测试问题列表
    questions = [
        "量子力学是什么？",
        "人工智能有哪些应用？",
        "相对论的核心是什么？",
        "区块链有什么用？",
    ]
    
    print("演示：小七遇到未知问题会主动学习\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"问题 {i}: {question}")
        print('='*60)
        
        response = mind.respond(question)
        print(f"\n🤖 小七的回答:\n{response}\n")
    
    # 显示学习历史
    print(f"\n{'='*60}")
    print("学习历史")
    print('='*60)
    mind.show_learning_history()
    
    # 显示状态
    status = mind.get_status()
    print(f"\n📊 最终状态:")
    print(f"   记忆数量：{status['memory_count']} 条")
    print(f"   主动学习：{status['learned_count']} 次")
    print()


if __name__ == '__main__':
    print("\n请选择测试模式:\n")
    print("1. 交互式对话（推荐）")
    print("2. 自主学习演示")
    print()
    
    choice = input("输入 1 或 2：").strip()
    
    if choice == '1':
        interactive_test()
    elif choice == '2':
        demo_autonomous_learning()
    else:
        print("\n默认使用交互式对话模式\n")
        interactive_test()
