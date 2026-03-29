#!/usr/bin/env python3
"""
自主模式演示

展示 AI 真正的自主能力
"""

import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI


def demo():
    """完整演示"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 自主模式演示                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    # 演示 1: 查看自主状态
    print("\n" + "="*60)
    print("演示 1: 自主状态")
    print("="*60 + "\n")
    
    status = ai.get_autonomy_status()
    print(f"模式：{status['mode']}")
    print(f"精力：{status['energy']}")
    print(f"决策次数：{status['decisions']}")
    
    # 演示 2: 开启自主模式
    print("\n" + "="*60)
    print("演示 2: 开启自主模式")
    print("="*60 + "\n")
    
    ai.enable_autonomous_mode()
    
    # 演示 3: 自主决策循环
    print("\n" + "="*60)
    print("演示 3: 自主决策 (5 次)")
    print("="*60 + "\n")
    
    for i in range(5):
        print(f"\n[第{i+1}次决策]")
        thought = ai.think()
        print(thought)
        time.sleep(0.5)
    
    # 演示 4: 动机变化
    print("\n" + "="*60)
    print("演示 4: 动机变化")
    print("="*60 + "\n")
    
    status = ai.get_autonomy_status()
    print(f"好奇心：{status['motivation'].curiosity:.0f} (学习驱动力)")
    print(f"成就感：{status['motivation'].achievement:.0f} (任务驱动力)")
    print(f"改进欲：{status['motivation'].improvement:.0f} (自我提升驱动力)")
    print(f"社交欲：{status['motivation'].social:.0f} (聊天驱动力)")
    
    # 演示 5: 对话式自主
    print("\n" + "="*60)
    print("演示 5: 对话式自主")
    print("="*60 + "\n")
    
    dialogs = [
        "开启自主模式",
        "思考",
        "自主状态",
        "关闭自主模式",
    ]
    
    for dialog in dialogs:
        print(f"你：{dialog}")
        resp = ai.chat(dialog)
        print(f"小七：{resp[:300]}\n")
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 演示完成！                                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("💡 小七现在有真正的自主能力:")
    print("   ✅ 自主决策 - 自己决定做什么")
    print("   ✅ 内在动机 - 好奇心/成就感/改进欲")
    print("   ✅ 效用函数 - 基于多因素决策")
    print("   ✅ 精力系统 - 需要休息恢复")
    print("   ✅ 学习进化 - 从经验中学习")
    print("\n使用方式:")
    print("   python3 xiaoqi.py")
    print("   你：开启自主模式")
    print("   你：思考")
    print("   你：自主状态")
    print()


if __name__ == '__main__':
    demo()
