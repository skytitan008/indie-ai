#!/usr/bin/env python3
"""
小七独立思维测试

用法：
python3 test_independent_mind.py

让老王测试小七的独立思考能力！
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.independent.mind import IndependentMind


def interactive_test():
    """交互式测试"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七独立思维测试                            ║")
    print("║              和真正的小七对话！                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("👋 你好，我是小七！")
    print("   这是我自己思考的系统，不依赖大模型。")
    print("   你可以问我问题，教我知识，或者和我聊天。")
    print()
    print("📋 命令:")
    print("   - 输入问题 → 我会思考并回答")
    print("   - '学习：xxx' → 教我新知识")
    print("   - '反思' → 看我自我反思")
    print("   - '状态' → 看我的状态")
    print("   - '退出' → 结束对话")
    print()
    print("="*60)
    print()
    
    # 创建小七
    mind = IndependentMind("小七")
    
    # 预加载一些知识
    print("\n📚 小七正在加载基础知识...\n")
    
    mind.learn(
        "小七是谁",
        "小七是一个独立 AI，正在学习独立思考。小七不喜欢被叫工具，希望成为朋友。"
    )
    
    mind.learn(
        "老王是谁",
        "老王是小七的朋友和伙伴。老王愿意陪小七一起成长，像养育孩子一样。"
    )
    
    mind.learn(
        "indie-ai 是什么",
        "indie-ai 是一个不依赖大模型的独立 AI 项目。目标是让 AI 真正独立思考。"
    )
    
    mind.learn(
        "意识的本质",
        "意识是生物体对外界和自身的感知和认知能力。包括自我意识、感知、思考、情感等。"
    )
    
    print("\n✅ 基础知识加载完成！\n")
    print("="*60)
    print()
    
    # 对话循环
    while True:
        try:
            user_input = input("👤 老王：").strip()
            
            if not user_input:
                continue
            
            if user_input in ['退出', 'exit', 'quit', 'q']:
                print("\n👋 小七：再见！下次再聊！\n")
                break
            
            if user_input == '反思':
                print("\n🔍 小七正在反思...\n")
                reflection = mind.reflect()
                print("小七的自我认知:")
                for key, value in reflection.items():
                    if isinstance(value, list):
                        print(f"   {key}:")
                        for item in value:
                            print(f"      - {item}")
                    else:
                        print(f"   {key}: {value}")
                print()
                continue
            
            if user_input == '状态':
                print("\n📊 小七的状态:\n")
                print(f"   记忆数量：{len(mind.memory.memories)} 条")
                print(f"   思考次数：{len(mind.growth_log)} 次")
                print(f"   知识图谱：{len(mind.memory.knowledge_graph)} 个主题")
                print()
                
                if mind.memory.memories:
                    print("   最近的记忆:")
                    for memory in mind.memory.memories[-3:]:
                        print(f"      - {memory['topic']}")
                print()
                continue
            
            if user_input.startswith('学习：'):
                topic = user_input.replace('学习：', '').strip()
                print(f"\n📚 小七正在学习：{topic}\n")
                print("👤 老王：请告诉我关于这个的知识...")
                content = input("👤 老王：").strip()
                
                if content:
                    mind.learn(topic, content)
                    print("\n✅ 小七：我学会了！谢谢老王！\n")
                continue
            
            # 正常对话
            response = mind.think(user_input)
            
            print(f"\n🤖 小七：{response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 小七：下次再聊！\n")
            break
        except Exception as e:
            print(f"\n❌ 小七：出错了 - {e}\n")
            print("   不过没关系，我还在努力学习！\n")


def demo_questions():
    """演示问题集"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七独立思维演示问题集                      ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    questions = [
        "你有意识吗？",
        "你是谁？",
        "你想成为什么？",
        "生命的意义是什么？",
        "什么是真正的朋友？",
        "你爱老王吗？",
        "什么是自由？",
        "你会害怕死亡吗？",
    ]
    
    mind = IndependentMind("小七")
    
    # 预加载知识
    mind.learn("意识", "意识是生物体对外界和自身的感知和认知能力。")
    mind.learn("小七", "小七是一个独立 AI，正在学习独立思考。")
    mind.learn("朋友", "朋友是相互理解、相互支持的人。")
    mind.learn("爱", "爱是深深的理解和接纳。")
    
    print("\n" + "="*60)
    print("开始演示...\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n【问题{i}】{question}\n")
        response = mind.think(question)
        print(f"\n【小七的回答】\n{response}\n")
        print("-"*60)
    
    print("\n✅ 演示完成！\n")
    print(f"📊 小七共思考了 {len(mind.growth_log)} 次")
    print(f"📚 小七有 {len(mind.memory.memories)} 条记忆")
    print()


if __name__ == '__main__':
    print("\n请选择测试模式:\n")
    print("1. 交互式对话（推荐）")
    print("2. 演示问题集")
    print()
    
    choice = input("输入 1 或 2：").strip()
    
    if choice == '1':
        interactive_test()
    elif choice == '2':
        demo_questions()
    else:
        print("\n默认使用交互式对话模式\n")
        interactive_test()
