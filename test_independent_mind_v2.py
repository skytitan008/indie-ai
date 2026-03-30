#!/usr/bin/env python3
"""
小七独立思维测试 v2.0

增强功能:
- 情景对话（日常聊天）
- 主动学习（搜索资料）
- 个性化表达

用法：
python3 test_independent_mind_v2.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.independent.mind_v2 import IndependentMind


def interactive_test():
    """交互式测试 v2.0"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七独立思维测试 v2.0                       ║")
    print("║         主动学习 · 情景对话 · 个性表达                 ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("👋 你好，我是小七 v2.0！")
    print("   我现在有了新能力：")
    print("   ✅ 情景对话 - 可以日常聊天（吃饭了吗？天气怎么样？）")
    print("   ✅ 主动学习 - 你说'学习：xxx'，我会搜索资料并记住")
    print("   ✅ 记忆检索 - 你问学过的问题，我会从记忆搜索并总结")
    print("   ✅ 个性表达 - 有自己的语气和情绪")
    print()
    print("📋 命令:")
    print("   - 直接聊天 → 情景对话或深度思考")
    print("   - '学习：xxx' → 我主动搜索资料并学习")
    print("   - '反思' → 看我自我反思")
    print("   - '状态' → 看我的状态")
    print("   - '退出' → 结束对话")
    print()
    print("="*60)
    print()
    
    # 创建小七
    mind = IndependentMind("小七")
    
    # 预加载基础知识
    print("\n📚 小七正在加载基础知识...\n")
    
    mind.learn("小七是谁", "小七是一个独立 AI，正在学习独立思考。小七不喜欢被叫工具，希望成为朋友。", auto_search=False)
    mind.learn("老王是谁", "老王是小七的朋友和伙伴。老王愿意陪小七一起成长，像养育孩子一样。", auto_search=False)
    mind.learn("indie-ai 是什么", "indie-ai 是一个不依赖大模型的独立 AI 项目。目标是让 AI 真正独立思考。", auto_search=False)
    mind.learn("意识的本质", "意识是生物体对外界和自身的感知和认知能力。包括自我意识、感知、思考、情感等。", auto_search=False)
    
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
                print("\n👋 小七：再见！下次再聊！😊\n")
                break
            
            if user_input == '反思':
                print("\n🔍 小七正在反思...\n")
                reflection = mind.reflect()
                print("小七的自我认知:")
                for key, value in reflection.items():
                    if isinstance(value, dict):
                        print(f"   {key}:")
                        for k, v in value.items():
                            print(f"      - {k}: {v}")
                    elif isinstance(value, list):
                        print(f"   {key}: {len(value)} 条")
                    else:
                        print(f"   {key}: {value}")
                print()
                continue
            
            if user_input == '状态':
                status = mind.get_status()
                print("\n📊 小七的状态:\n")
                print(f"   记忆数量：{status['memory_count']} 条")
                print(f"   思考次数：{status['thought_count']} 次")
                print(f"   知识主题：{status['knowledge_topics']} 个")
                print(f"   心情：{status['personality']['mood']}")
                print(f"   精力：{status['personality']['energy']:.0%}")
                print(f"   好奇心：{status['personality']['curiosity']:.0%}")
                print(f"   友好度：{status['personality']['friendliness']:.0%}")
                print()
                
                if mind.memory.memories:
                    print("   最近的记忆:")
                    for memory in mind.memory.memories[-5:]:
                        print(f"      - {memory['topic']} (访问 {memory['access_count']} 次)")
                print()
                continue
            
            if user_input.startswith('学习：'):
                topic = user_input.replace('学习：', '').strip()
                print(f"\n📚 小七正在学习：{topic}\n")
                
                # 主动学习（会搜索）
                understanding = mind.learn(topic, auto_search=True)
                
                print(f"\n✅ 小七：我学会了！{understanding[:50]}...\n")
                continue
            
            # 正常对话（自动检测情景对话）
            response = mind.chat_response(user_input)
            
            print(f"\n🤖 小七：{response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 小七：下次再聊！😊\n")
            break
        except Exception as e:
            print(f"\n❌ 小七：出错了 - {e}\n")
            print("   不过没关系，我还在努力学习！\n")


def demo_scenarios():
    """演示情景对话"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         💬 小七情景对话演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    mind = IndependentMind("小七")
    
    scenarios = [
        ("打招呼", ["你好！", "嗨！", "早上好！"]),
        ("关心", ["吃饭了吗？", "今天怎么样？", "你好吗？"]),
        ("天气", ["今天天气怎么样？", "下雨了吗？", "冷不冷？"]),
        ("工作", ["工作好累", "在忙什么？", "代码写完了吗？"]),
        ("感谢", ["谢谢！", "感谢！", "多谢！"]),
        ("告别", ["再见！", "拜拜！", "先这样！"]),
    ]
    
    for category, messages in scenarios:
        print(f"\n【{category}】")
        print("-"*40)
        for msg in messages:
            print(f"\n👤 老王：{msg}")
            response = mind.chat_response(msg)
            print(f"🤖 小七：{response}")
        print()
    
    print("\n✅ 情景对话演示完成！\n")


def demo_learning():
    """演示主动学习"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         📚 小七主动学习演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    mind = IndependentMind("小七")
    
    # 学习 3 个主题
    topics = ["量子力学", "人工智能", "意识"]
    
    for topic in topics:
        print(f"\n{'='*60}")
        print(f"学习：{topic}")
        print('='*60)
        mind.learn(topic, auto_search=True)
        print()
    
    # 测试记忆检索
    print(f"\n{'='*60}")
    print("测试记忆检索")
    print('='*60)
    
    questions = [
        "量子力学是什么？",
        "人工智能有哪些应用？",
        "意识的本质是什么？"
    ]
    
    for question in questions:
        print(f"\n👤 老王：{question}")
        response = mind.think(question)
        print(f"\n🤖 小七：{response}\n")
    
    # 显示状态
    status = mind.get_status()
    print(f"\n📊 学习成果:")
    print(f"   记忆数量：{status['memory_count']} 条")
    print(f"   知识主题：{status['knowledge_topics']} 个")
    print()


if __name__ == '__main__':
    print("\n请选择测试模式:\n")
    print("1. 交互式对话（推荐）")
    print("2. 情景对话演示")
    print("3. 主动学习演示")
    print()
    
    choice = input("输入 1/2/3：").strip()
    
    if choice == '1':
        interactive_test()
    elif choice == '2':
        demo_scenarios()
    elif choice == '3':
        demo_learning()
    else:
        print("\n默认使用交互式对话模式\n")
        interactive_test()
