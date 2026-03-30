#!/usr/bin/env python3
"""
小七 API 测试客户端

用于测试小七 API 服务

用法:
python3 test_api_client.py
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8765"


def test_root():
    """测试根路径"""
    print("\n" + "="*60)
    print("测试 1: 根路径")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ 响应：{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False
    
    return True


def test_chat():
    """测试聊天接口"""
    print("\n" + "="*60)
    print("测试 2: 聊天接口")
    print("="*60)
    
    test_messages = [
        "你好！",
        "量子力学是什么？",
        "你有意识吗？",
        "谢谢！",
    ]
    
    for msg in test_messages:
        print(f"\n👤 用户：{msg}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={"message": msg}
            )
            
            data = response.json()
            print(f"🤖 小七：{data['response'][:200]}...")
            print(f"😊 情感：{data['emotion']['mood']}")
            print(f"📊 元数据：{data['metadata']['thought_process']}")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
    
    return True


def test_learn():
    """测试学习接口"""
    print("\n" + "="*60)
    print("测试 3: 学习接口")
    print("="*60)
    
    topics = [
        ("相对论", None),
        ("区块链", None),
    ]
    
    for topic, content in topics:
        print(f"\n📚 学习：{topic}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/learn",
                json={"topic": topic, "content": content}
            )
            
            data = response.json()
            print(f"✅ 成功：{data['success']}")
            print(f"💡 理解：{data['understanding'][:100]}...")
            print(f"📝 记忆 ID: {data.get('memory_id', 'N/A')}")
            
        except Exception as e:
            print(f"❌ 错误：{e}")
    
    return True


def test_status():
    """测试状态接口"""
    print("\n" + "="*60)
    print("测试 4: 状态接口")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        data = response.json()
        
        print(f"📊 小七状态:")
        print(f"   名字：{data['name']}")
        print(f"   记忆数量：{data['memory_count']} 条")
        print(f"   交互次数：{data['interaction_count']} 次")
        print(f"   主动学习：{data['learned_count']} 次")
        print(f"   知识主题：{data['knowledge_topics']} 个")
        print(f"   心情：{data['current_mood']}")
        print(f"   精力：{data['personality']['energy']:.0%}")
        print(f"   好奇心：{data['personality']['curiosity']:.0%}")
        print(f"   友好度：{data['personality']['friendliness']:.0%}")
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False
    
    return True


def test_memories():
    """测试记忆接口"""
    print("\n" + "="*60)
    print("测试 5: 记忆列表")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/memories?limit=5")
        data = response.json()
        
        print(f"📚 最近的记忆:\n")
        for memory in data['memories']:
            print(f"   {memory['id']}. {memory['topic']}")
            print(f"      摘要：{memory['summary'][:50]}...")
            print(f"      访问：{memory['access_count']} 次")
            print()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False
    
    return True


def test_growth_log():
    """测试成长日志接口"""
    print("\n" + "="*60)
    print("测试 6: 成长日志")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/growth_log?limit=5")
        data = response.json()
        
        print(f"📝 最近的成长记录:\n")
        for log in data['logs']:
            print(f"   类型：{log['type']}")
            if log['type'] == 'interaction':
                print(f"      问题：{log['question'][:50]}...")
                print(f"      学习了：{log.get('learned', False)}")
            print(f"      时间：{log['timestamp'][-19:]}")
            print()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False
    
    return True


def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("交互模式 - 与小七聊天")
    print("="*60)
    print("\n输入 '退出' 结束对话\n")
    
    while True:
        try:
            user_input = input("👤 用户：").strip()
            
            if user_input in ['退出', 'exit', 'quit', 'q']:
                print("\n👋 再见！\n")
                break
            
            if not user_input:
                continue
            
            # 调用聊天 API
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={"message": user_input}
            )
            
            data = response.json()
            print(f"\n🤖 小七：{data['response']}\n")
            print(f"😊 情感：{data['emotion']}")
            print(f"📊 学习：{'是' if data['metadata']['learned'] else '否'}")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！\n")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}\n")


def main():
    """主函数"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧪 小七 API 测试客户端                         ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("请选择测试模式:\n")
    print("1. 自动测试（所有接口）")
    print("2. 交互模式（聊天）")
    print()
    
    choice = input("输入 1 或 2：").strip()
    
    if choice == '1':
        # 自动测试
        print("\n开始自动测试...\n")
        
        tests = [
            ("根路径", test_root),
            ("聊天接口", test_chat),
            ("学习接口", test_learn),
            ("状态接口", test_status),
            ("记忆列表", test_memories),
            ("成长日志", test_growth_log),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                success = test_func()
                results.append((name, success))
            except Exception as e:
                print(f"\n❌ {name} 测试失败：{e}\n")
                results.append((name, False))
        
        # 汇总
        print("\n" + "="*60)
        print("测试汇总")
        print("="*60)
        
        for name, success in results:
            status = "✅ 通过" if success else "❌ 失败"
            print(f"{status} - {name}")
        
        passed = sum(1 for _, s in results if s)
        total = len(results)
        print(f"\n总计：{passed}/{total} 通过\n")
        
    elif choice == '2':
        # 交互模式
        interactive_mode()
    else:
        print("\n默认使用交互模式\n")
        interactive_mode()


if __name__ == '__main__':
    main()
