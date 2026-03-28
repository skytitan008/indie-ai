"""
实际场景应用 - AIGC 视频项目任务管理

演示如何用 AI 管理真实的 AIGC 视频生成项目
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent


console = Console()


def create_aigc_video_tasks(agent: IndependentAgent):
    """创建 AIGC 视频项目的真实任务"""
    
    console.print(
        Panel.fit(
            "[bold]AIGC 视频项目任务[/bold]\n\n"
            "多模态视频生成工作流",
            title="🎬 项目场景",
            border_style="blue"
        )
    )
    
    now = datetime.now()
    
    # AIGC 视频项目的典型任务
    tasks = [
        {
            'name': '修复 ComfyUI 显存溢出',
            'priority': 10,
            'estimated_time': 60,
            'deadline': now + timedelta(hours=2),
            'description': '4060Ti 16GB 显存不足，需要优化'
        },
        {
            'name': '调试视频生成 pipeline',
            'priority': 9,
            'estimated_time': 120,
            'deadline': now + timedelta(hours=5),
            'description': '多模态生成流程不稳定'
        },
        {
            'name': '准备训练数据集',
            'priority': 8,
            'estimated_time': 180,
            'deadline': now + timedelta(hours=8),
            'description': '收集 1000 个视频样本'
        },
        {
            'name': '优化提示词工程',
            'priority': 7,
            'estimated_time': 90,
            'description': '改进视频生成质量'
        },
        {
            'name': '测试昇腾 950PR 兼容性',
            'priority': 7,
            'estimated_time': 150,
            'deadline': now + timedelta(hours=6),
            'description': '国产芯片适配测试'
        },
        {
            'name': '写技术文档',
            'priority': 6,
            'estimated_time': 90,
            'description': '记录项目进展'
        },
        {
            'name': '回复合作者邮件',
            'priority': 5,
            'estimated_time': 30,
            'description': '项目合作沟通'
        },
        {
            'name': '调研最新论文',
            'priority': 4,
            'estimated_time': 120,
            'description': 'Sora 等技术调研'
        },
        {
            'name': '整理代码仓库',
            'priority': 3,
            'estimated_time': 60,
            'description': '代码重构和文档'
        },
    ]
    
    console.print("\n[bold]添加任务到 AI 管理系统...[/bold]\n")
    
    for task in tasks:
        agent.add_task(**task)
        deadline_str = task.get('deadline', now).strftime('%H:%M') if 'deadline' in task else '无'
        console.print(
            f"  ✓ {task['name']}\n"
            f"    优先级：{task['priority']} | "
            f"预估：{task['estimated_time']}分钟 | "
            f"截止：{deadline_str}\n"
        )
    
    return len(tasks)


def run_aigc_project_demo():
    """运行 AIGC 项目演示"""
    
    console.print(
        Panel.fit(
            "[bold blue]独立思考 AI - AIGC 视频项目管理[/bold blue]\n\n"
            "真实场景应用演示",
            title="🎯 Real World Application",
            border_style="blue"
        )
    )
    
    # 初始化 Agent
    console.print("\n[bold]初始化 AI 项目助手...[/bold]\n")
    agent = IndependentAgent(db_path="aigc_project.db")
    
    # 应用质量优先配置（适合创意工作）
    agent.decision_engine.weights = {
        'urgency': 0.30,
        'importance': 0.40,
        'efficiency': 0.25,
        'dependency': 0.05,
    }
    
    try:
        # 创建任务
        task_count = create_aigc_video_tasks(agent)
        
        # 运行决策循环
        console.print(f"\n[bold]开始自主任务调度...[/bold] (运行{task_count}个循环)\n")
        
        completed_tasks = []
        failed_tasks = []
        
        for i in range(task_count):
            result = agent.run_cycle()
            
            console.print(Panel(result, title=f"循环 {i+1}", border_style="blue"))
            
            if '完成' in result:
                completed_tasks.append(result)
            elif '失败' in result:
                failed_tasks.append(result)
        
        # 项目总结
        console.print(f"\n{'='*60}")
        console.print("[bold]📊 项目执行总结[/bold]")
        console.print(f"{'='*60}\n")
        
        status = agent.get_status()
        
        console.print(f"✅ 完成任务：{status['tasks_completed']}")
        console.print(f"⏱️  总奖励：{status['total_reward']:.2f}")
        console.print(f"🧠 决策次数：{status['decision_stats']['total_decisions']}")
        console.print(f"📚 学习更新：{status['learning_stats']['total_updates']}次")
        console.print(f"💡 Q 表大小：{status['learning_stats']['q_table_size']}")
        
        # AI 反思
        console.print(f"\n[bold]🤔 AI 的项目反思[/bold]\n")
        reflection = agent.get_reflection()
        console.print(Panel(reflection, border_style="yellow"))
        
        # 建议
        console.print(f"\n[bold]💡 给老王的建议[/bold]\n")
        
        if status['tasks_completed'] >= task_count * 0.8:
            console.print("  ✅ 项目进展顺利，AI 助手表现良好！")
            console.print("  💡 可以考虑增加更多并行任务")
        else:
            console.print("  ⚠️ 任务完成率有待提升")
            console.print("  💡 建议调整任务优先级或时间估算")
        
        if status['learning_stats']['q_table_size'] > 20:
            console.print("  ✅ AI 已经学习到足够的项目模式")
            console.print("  💡 可以继续训练，优化调度策略")
        
        console.print("\n[green]✓ AIGC 项目管理演示完成！[/green]\n")
        
    finally:
        agent.close()


if __name__ == "__main__":
    run_aigc_project_demo()
