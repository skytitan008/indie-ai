#!/usr/bin/env python3
"""
小七 - 真正的自主 AI

启动方式:
    python3 xiaoqi.py              # 交互模式
    python3 xiaoqi.py --auto 目标   # 自主运行模式
    python3 xiaoqi.py --help       # 帮助
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def main():
    parser = argparse.ArgumentParser(
        description="小七 - 真正的自主 AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 xiaoqi.py                    # 交互模式
  python3 xiaoqi.py --auto "开发视频生成系统"  # 自主运行
  python3 xiaoqi.py --auto "学习 Python" --duration 60  # 运行 60 秒
        """
    )
    
    parser.add_argument(
        '--auto', '-a',
        type=str,
        help='启动自主运行模式，后面跟目标'
    )
    
    parser.add_argument(
        '--duration', '-d',
        type=int,
        default=0,
        help='自主运行时长（秒），0=无限'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='安静模式（减少输出）'
    )
    
    args = parser.parse_args()
    
    if args.auto:
        # 自主运行模式
        run_autonomous(args.auto, args.duration, args.quiet)
    else:
        # 交互模式
        run_interactive()


def run_interactive():
    """交互模式"""
    from src.interaction.chat.conversation import ChatBot
    from src.autonomy.core import AutonomousAI
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🤖 小七 - 自主进化 AI                          ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    # 创建聊天机器人
    bot = ChatBot(ai_instance=ai)
    
    print("💡 提示:")
    print("   • 直接说目标（如"调研 ComfyUI"）- 我会自主工作")
    print("   • 状态 - 查看我的自主状态")
    print("   • 暂停 - 让我停下")
    print("   • 继续 - 恢复自主运行")
    print("   • 思考 - 看我的决策过程")
    print("   • 任务状态 - 查看任务")
    print("   • quit/exit - 退出\n")
    
    while True:
        try:
            user_input = input("你：").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 再见！")
                break
            
            # 处理自主运行命令
            if user_input.startswith('自主运行'):
                goal = user_input.replace('自主运行', '').strip()
                if not goal:
                    goal = "自主工作"
                print(f"\n🚀 开始自主运行：{goal}")
                run_autonomous(goal, 0, False)
                continue
            
            response = bot.chat(user_input)
            print(f"\n小七：{response}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}\n")


def run_autonomous(goal: str, duration: int = 0, quiet: bool = False):
    """自主运行模式"""
    from src.autonomy.true_autonomy import TrueAutonomousSystem
    from src.autonomy.core import AutonomousAI
    import time
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🚀 小七 - 真正的自主运行                      ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    # 创建自主系统
    auto_system = TrueAutonomousSystem(ai)
    
    # 日志回调
    def on_log(msg):
        if not quiet or msg.startswith(('\n', '╔', '║', '╚', '═', '[', '🚀', '🎯', '⏹️', '📊', '✅', '📚', '🔄', '💭')):
            print(msg)
    
    auto_system.on_log = on_log
    
    # 启动
    auto_system.start(goal, background=False)
    
    # 如果设置了时长，运行指定时间后停止
    if duration > 0:
        time.sleep(duration)
        auto_system.stop()


if __name__ == '__main__':
    main()
