#!/usr/bin/env python3
"""
小七 - 自主进化 AI 交互界面

和你聊天、帮你编程、自我学习
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI


def show_welcome():
    """显示欢迎界面"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🤖 小七 - 你的 AI 伙伴                          ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("我可以:")
    print("   💬 和你聊天")
    print("   💻 帮你写代码（C/Python/Java/JS 等 10 种语言）")
    print("   📚 自主学习新知识")
    print("   🎯 安装新技能")
    print("   📷 控制硬件（摄像头/麦克风）")
    print("   📊 监控系统状态")
    
    print("\n命令:")
    print("   chat      - 聊天模式")
    print("   learn     - 学习模式")
    print("   code      - 编程帮助")
    print("   status    - 显示状态")
    print("   skills    - 查看技能")
    print("   help      - 帮助")
    print("   quit      - 退出")
    print("\n直接输入也可以和我聊天哦！\n")


def main():
    """主程序"""
    show_welcome()
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    
    # 初始化
    ai.initialize()
    
    print("\n✅ 准备就绪！\n")
    
    while True:
        try:
            user_input = input("你：").strip()
            
            if not user_input:
                continue
            
            cmd = user_input.lower()
            
            if cmd in ['quit', 'exit', 'q']:
                print("小七：再见！随时欢迎回来！👋")
                break
            
            elif cmd == 'chat':
                print("\n💬 聊天模式（输入 quit 返回）\n")
                while True:
                    try:
                        text = input("你：").strip()
                        if text.lower() in ['quit', 'q', 'exit']:
                            break
                        if not text:
                            continue
                        print(f"小七：{ai.chat(text)}\n")
                    except KeyboardInterrupt:
                        break
                print("\n返回主菜单\n")
            
            elif cmd == 'learn':
                print("\n📚 学习模式（输入 quit 返回）\n")
                while True:
                    try:
                        topic = input("想学什么：").strip()
                        if topic.lower() in ['quit', 'q', 'exit']:
                            break
                        if not topic:
                            continue
                        ai.learn(topic, category="general")
                        print()
                    except KeyboardInterrupt:
                        break
                print("\n返回主菜单\n")
            
            elif cmd == 'code':
                print("\n💻 编程帮助（输入 quit 返回）\n")
                print("我可以帮你:")
                print("   - 写代码")
                print("   - 审查代码")
                print("   - 调试 Bug")
                print("   - 优化性能")
                print("   - 写测试")
                print("\n请描述你的需求:\n")
                
                while True:
                    try:
                        req = input("需求：").strip()
                        if req.lower() in ['quit', 'q', 'exit']:
                            break
                        if not req:
                            continue
                        
                        # 生成代码帮助
                        response = f"""好的！我来帮你。

关于你的需求：{req}

我建议：
1. 先明确具体功能
2. 选择编程语言
3. 设计实现方案

你想用什么语言？我可以写 C、Python、Java、JavaScript 等。"""
                        print(f"小七：{response}\n")
                    except KeyboardInterrupt:
                        break
                print("\n返回主菜单\n")
            
            elif cmd == 'status':
                ai.show_status()
            
            elif cmd == 'skills':
                skills = ai.learner.knowledge_base.get_skills()
                print(f"\n🎯 当前技能 ({len(skills)}个):\n")
                for skill in skills:
                    print(f"   • {skill['name']} - {skill['description']}")
                print()
            
            elif cmd == 'help':
                print("""
可用命令:
   chat      - 聊天模式
   learn     - 学习新知识
   code      - 编程帮助
   status    - 显示 AI 状态
   skills    - 查看技能列表
   help      - 显示帮助
   quit      - 退出程序

也可以直接输入文字和我聊天！
""")
            
            else:
                # 直接聊天
                response = ai.chat(user_input)
                print(f"小七：{response}\n")
        
        except KeyboardInterrupt:
            print("\n\n小七：再见！👋")
            break
        except Exception as e:
            print(f"小七：抱歉，出了点问题：{e}\n")


if __name__ == '__main__':
    main()
