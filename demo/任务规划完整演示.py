#!/usr/bin/env python3
"""
任务规划完整演示

展示 AI 如何规划并执行复杂任务
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
    print("║         📋 任务规划系统完整演示                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    # 演示 1: 规划开发任务
    print("\n" + "="*60)
    print("演示 1: 规划开发任务")
    print("="*60 + "\n")
    
    task_id = ai.plan_task(
        "开发 AIGC 视频生成功能",
        "开发一个完整的 AIGC 视频生成系统",
        "high"
    )
    
    # 演示 2: 规划学习任务
    print("\n" + "="*60)
    print("演示 2: 规划学习任务")
    print("="*60 + "\n")
    
    task_id2 = ai.plan_task(
        "学习机器学习",
        "系统学习机器学习基础知识",
        "medium"
    )
    
    # 演示 3: 规划写代码任务
    print("\n" + "="*60)
    print("演示 3: 规划写代码任务")
    print("="*60 + "\n")
    
    task_id3 = ai.plan_task(
        "用 Python 写个 Web 爬虫",
        "编写一个爬取网页数据的爬虫",
        "medium"
    )
    
    # 显示任务状态
    print("\n" + "="*60)
    print("当前任务状态")
    print("="*60 + "\n")
    
    status = ai.get_task_status()
    print(f"总任务数：{status['total']}")
    print(f"待执行：{status['by_status'].get('pending', 0)}")
    print(f"已完成：{status['by_status'].get('completed', 0)}")
    print(f"可执行：{status['ready']}")
    
    # 演示 4: 自动执行任务
    print("\n" + "="*60)
    print("自动执行任务")
    print("="*60 + "\n")
    
    executed = 0
    max_executions = 20  # 限制执行次数
    
    while executed < max_executions:
        if not ai.execute_task():
            break
        executed += 1
        time.sleep(0.2)
    
    # 最终状态
    print("\n" + "="*60)
    print("最终任务状态")
    print("="*60 + "\n")
    
    status = ai.get_task_status()
    print(f"总任务数：{status['total']}")
    print(f"待执行：{status['by_status'].get('pending', 0)}")
    print(f"已完成：{status['by_status'].get('completed', 0)}")
    
    # 演示 5: 对话式任务规划
    print("\n" + "="*60)
    print("对话式任务规划")
    print("="*60 + "\n")
    
    print("你：帮我规划一个开发任务")
    response = ai.chat("帮我规划一个开发任务")
    print(f"小七：{response}\n")
    
    print("你：用 Python 写个快速排序")
    response = ai.chat("用 Python 写个快速排序")
    print(f"小七：{response}\n")
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 演示完成！                                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("💡 使用方式:")
    print("   python3 xiaoqi.py")
    print("   你：帮我规划一个任务")
    print("   你：执行下一个任务")
    print("   你：任务状态")
    print()


if __name__ == '__main__':
    demo()
