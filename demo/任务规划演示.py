#!/usr/bin/env python3
"""
任务规划演示

展示 AI 如何分解复杂任务
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.planning.task_planner import TaskPlanner, TaskDecomposer, TaskExecutor, TaskPriority, TaskStatus


def demo():
    """演示任务规划"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         📋 任务规划系统演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建规划器
    planner = TaskPlanner()
    planner.clear_all()
    
    # 创建分解器
    decomposer = TaskDecomposer()
    
    # 演示 1: 任务分解
    print("="*60)
    print("演示 1: 任务分解")
    print("="*60 + "\n")
    
    examples = [
        ("开发功能", "开发用户登录功能"),
        ("写代码", "用 Python 写个 Web 爬虫"),
        ("测试", "测试登录功能"),
        ("学习", "学习机器学习"),
        ("部署", "部署到生产环境"),
    ]
    
    for task_type, task_desc in examples:
        print(f"📝 任务：{task_desc}")
        subtasks = decomposer.decompose(task_desc)
        print(f"   分解为 {len(subtasks)} 个子任务:")
        total_time = 0
        for i, sub in enumerate(subtasks, 1):
            print(f"      {i}. {sub['name']} ({sub['estimated_time']}分钟)")
            total_time += sub['estimated_time']
        print(f"   预计总时间：{total_time}分钟\n")
    
    # 演示 2: 创建任务树
    print("="*60)
    print("演示 2: 创建任务树")
    print("="*60 + "\n")
    
    # 创建主任务
    main_task_id = planner.create_task(
        name="开发 AIGC 视频生成系统",
        description="开发一个完整的 AIGC 视频生成系统",
        priority=TaskPriority.HIGH,
        estimated_time=600
    )
    
    # 分解并创建子任务
    subtasks = decomposer.decompose("开发 AIGC 视频生成系统")
    
    print(f"📋 主任务：开发 AIGC 视频生成系统")
    print(f"   分解为 {len(subtasks)} 个子任务:\n")
    
    prev_task_id = None
    for i, subtask in enumerate(subtasks, 1):
        # 添加依赖关系（顺序执行）
        dependencies = [prev_task_id] if prev_task_id else []
        
        subtask_id = planner.create_task(
            name=subtask['name'],
            description=subtask['description'],
            estimated_time=subtask['estimated_time'],
            parent_id=main_task_id,
            dependencies=dependencies
        )
        planner.add_subtask(main_task_id, subtask_id)
        
        deps_text = f" (依赖：任务{prev_task_id})" if prev_task_id else ""
        print(f"   {i}. {subtask['name']} - {subtask['estimated_time']}分钟{deps_text}")
        prev_task_id = subtask_id
    
    # 演示 3: 任务执行
    print("\n" + "="*60)
    print("演示 3: 任务执行")
    print("="*60 + "\n")
    
    executor = TaskExecutor(planner)
    
    # 执行任务
    step = 1
    while True:
        task = executor.execute_next()
        if not task:
            break
        
        print(f"步骤 {step}: 执行任务 - {task.name}")
        
        # 模拟执行
        import time
        time.sleep(0.1)
        
        # 完成任务
        executor.complete_task(task.id, f"完成{task.name}")
        print(f"         ✅ 完成\n")
        
        step += 1
        if step > 10:  # 防止无限循环
            break
    
    # 演示 4: 任务状态
    print("="*60)
    print("演示 4: 任务状态")
    print("="*60 + "\n")
    
    all_tasks = planner.get_all_tasks()
    status_count = {}
    
    for task in all_tasks:
        status = task.status.value
        status_count[status] = status_count.get(status, 0) + 1
    
    print("任务状态统计:")
    for status, count in status_count.items():
        emoji = {"completed": "✅", "pending": "⏳", "running": "🔄", "failed": "❌"}.get(status, "📋")
        print(f"   {emoji} {status}: {count}个")
    
    # 显示主任务树
    print("\n任务树:")
    main_task = planner.get_task(main_task_id)
    print(f"  📋 {main_task.name}")
    
    for subtask_id in main_task.subtasks:
        subtask = planner.get_task(subtask_id)
        emoji = {"completed": "✅", "pending": "⏳", "running": "🔄"}.get(subtask.status.value, "📋")
        print(f"     {emoji} {subtask.name} ({subtask.status.value})")
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 演示完成！                                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("💡 使用方式:")
    print("   from src.planning.task_planner import TaskPlanner, TaskDecomposer")
    print("   ")
    print("   planner = TaskPlanner()")
    print("   decomposer = TaskDecomposer()")
    print("   ")
    print("   # 分解任务")
    print("   subtasks = decomposer.decompose('开发功能')")
    print("   ")
    print("   # 创建任务")
    print("   task_id = planner.create_task(name='任务名')")
    print("   ")
    print("   # 执行任务")
    print("   executor = TaskExecutor(planner)")
    print("   task = executor.execute_next()")
    print()


if __name__ == '__main__':
    demo()
