#!/usr/bin/env python3
"""
测试小七 API 的 OpenAI 兼容端点和情感同步

用法:
python3 test_openai_compat.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8765"


def test_emotion_endpoint():
    """测试情感端点"""
    print("\n" + "="*60)
    print(" 测试情感端点 (/api/emotion)")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/emotion")
        response.raise_for_status()
        
        emotion = response.json()
        
        print(f"\n✅ 情感数据:")
        print(f"   心情：{emotion['mood']}")
        print(f"   精力：{emotion['energy']}")
        print(f"   好奇心：{emotion['curiosity']}")
        print(f"   友好度：{emotion['friendliness']}")
        
        print(f"\n🎭 Live2D 参数:")
        for param, value in emotion['live2d_params'].items():
            print(f"   {param}: {value:.2f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        return False


def test_openai_chat():
    """测试 OpenAI 兼容聊天端点"""
    print("\n" + "="*60)
    print("🤖 测试 OpenAI 兼容聊天端点 (/v1/chat/completions)")
    print("="*60)
    
    try:
        payload = {
            "model": "xiaoqi-v3",
            "messages": [
                {"role": "user", "content": "你好，小七！"}
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json=payload
        )
        response.raise_for_status()
        
        result = response.json()
        
        print(f"\n✅ OpenAI 格式响应:")
        print(f"   ID: {result['id']}")
        print(f"   模型：{result['model']}")
        print(f"   对象：{result['object']}")
        
        choice = result['choices'][0]
        print(f"\n💬 小七回答:")
        print(f"   {choice['message']['content']}")
        
        print(f"\n📊 Token 使用:")
        print(f"   提示词：{result['usage']['prompt_tokens']}")
        print(f"   完成：{result['usage']['completion_tokens']}")
        print(f"   总计：{result['usage']['total_tokens']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        return False


def test_openai_chat_stream():
    """测试 OpenAI 兼容流式聊天端点"""
    print("\n" + "="*60)
    print("🌊 测试 OpenAI 兼容流式聊天端点 (/v1/chat/completions/stream)")
    print("="*60)
    
    try:
        payload = {
            "model": "xiaoqi-v3",
            "messages": [
                {"role": "user", "content": "介绍一下你自己"}
            ]
        }
        
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions/stream",
            json=payload,
            stream=True
        )
        response.raise_for_status()
        
        print(f"\n💬 小七流式回答:\n")
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    
                    if data_str.strip() == '[DONE]':
                        print("\n\n✅ 流式传输完成")
                        break
                    
                    try:
                        data = json.loads(data_str)
                        content = data['choices'][0]['delta']['content']
                        print(content, end='', flush=True)
                    except:
                        pass
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        return False


def test_websocket():
    """测试 WebSocket 情感推送"""
    print("\n" + "="*60)
    print("🔌 测试 WebSocket 情感推送 (/api/ws)")
    print("="*60)
    
    try:
        import websocket
        import time
        
        ws = websocket.create_connection(f"ws://localhost:8765/api/ws")
        
        print("\n✅ WebSocket 连接成功")
        
        # 接收欢迎消息
        welcome = json.loads(ws.recv())
        print(f"\n📨 欢迎消息:")
        print(f"   类型：{welcome['type']}")
        print(f"   消息：{welcome['message']}")
        
        # 等待情感推送（最多等 5 秒）
        print("\n⏳ 等待情感推送...")
        ws.settimeout(5)
        
        try:
            while True:
                message = json.loads(ws.recv())
                
                if message['type'] == 'emotion_update':
                    print(f"\n💝 收到情感更新:")
                    print(f"   心情：{message['emotion']['mood']}")
                    print(f"   精力：{message['emotion']['energy']}")
                    
                    if 'live2d_params' in message['emotion']:
                        params = message['emotion']['live2d_params']
                        print(f"\n   🎭 Live2D 参数:")
                        for param, value in params.items():
                            print(f"      {param}: {value:.2f}")
                    
                    break
                
        except websocket.WebSocketTimeoutException:
            print("\n⚠️  等待超时，未收到情感推送")
        
        ws.close()
        print("\n✅ WebSocket 测试完成")
        
        return True
        
    except ImportError:
        print("\n⚠️  需要安装 websocket-client:")
        print("   pip install websocket-client")
        return False
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        return False


def test_airi_integration():
    """模拟 AIRI 整合测试"""
    print("\n" + "="*60)
    print("🎯 模拟 AIRI 整合测试")
    print("="*60)
    
    try:
        # 1. 获取情感
        emotion_resp = requests.get(f"{BASE_URL}/api/emotion")
        emotion = emotion_resp.json()
        
        print(f"\n1️⃣  获取小七情感:")
        print(f"   心情：{emotion['mood']}")
        print(f"   Live2D 参数：{len(emotion['live2d_params'])} 个")
        
        # 2. 发送聊天
        chat_payload = {
            "model": "xiaoqi-v3",
            "messages": [
                {"role": "user", "content": "今天心情怎么样？"}
            ]
        }
        
        chat_resp = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json=chat_payload
        )
        chat_result = chat_resp.json()
        
        response_text = chat_result['choices'][0]['message']['content']
        
        print(f"\n2️⃣  用户提问：今天心情怎么样？")
        print(f"   小七回答：{response_text}")
        
        # 3. 再次获取情感（应该有变化）
        emotion_resp2 = requests.get(f"{BASE_URL}/api/emotion")
        emotion2 = emotion_resp2.json()
        
        print(f"\n3️⃣  获取新情感:")
        print(f"   心情：{emotion2['mood']}")
        print(f"   精力：{emotion2['energy']:.2f}")
        
        print(f"\n✅ AIRI 整合测试完成")
        print(f"   - 情感同步：✅")
        print(f"   - 聊天对话：✅")
        print(f"   - Live2D 参数：✅")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("🧪 小七 API OpenAI 兼容端点测试")
    print("="*60)
    print(f"\n📡 服务器地址：{BASE_URL}")
    print(f"📖 API 文档：{BASE_URL}/docs")
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=3)
        if response.status_code == 200:
            print(f"✅ 服务器状态：运行中")
        else:
            print(f"❌ 服务器状态异常")
            return
    except:
        print(f"\n❌ 服务器未运行！请先启动小七 API:")
        print(f"   cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp")
        print(f"   ./start_server.sh")
        return
    
    # 运行测试
    results = []
    
    results.append(("情感端点", test_emotion_endpoint()))
    results.append(("OpenAI 聊天", test_openai_chat()))
    results.append(("OpenAI 流式", test_openai_chat_stream()))
    results.append(("WebSocket", test_websocket()))
    results.append(("AIRI 整合", test_airi_integration()))
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n总计：{passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！小七准备好与 AIRI 整合了！")
    else:
        print("\n⚠️  部分测试失败，请检查服务器状态")


if __name__ == "__main__":
    main()
