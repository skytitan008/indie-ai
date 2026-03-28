"""
演示脚本 - 展示独立思考 AI 的能力

运行此脚本查看 AI 自主决策和学习过程
"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.agent import IndependentAgent


console = Console()


def create_demo_tasks(agent: IndependentAgent):
    """创建演示任务"""
    console.print("\n[bold blue]📋 创建演示任务...[/bold blue]\n")
    
    # 添加一些示例任务
    tasks = [
        {
            'name': '写项目报告',
            'priority': 8,
            'estimated_time': 90,
            'deadline': datetime.now() + timedelta(hours=4)
        },
        {
            'name': '回复邮件',
            'priority': 5,
            'estimated_time': 30,
        },
        {
            'name': '团队会议',
            'priority': 7,
            'estimated_time': 60,
            'deadline': datetime.now() + timedelta(hours=2)
        },
        {
            'name': '代码审查',
            'priority': 6,
            'estimated_time': 45,
        },
        {
            'name': '修复紧急 bug',
            'priority': 10,
            'estimated_time': 30,
            'deadline': datetime.now() + timedelta(hours=1)
        },
    ]
    
    for task_info in tasks:
        task = agent.add_task(**task_info)
        deadline_str = task.deadline.strftime('%H:%M') if task.deadline else '无'
        console.print(
            f"  ✓ 添加任务：[green]{task.name}[/green] "
            f"(优先级：{task.priority}, 预估：{task.estimated_time}分钟，截止：{deadline_str})"
        )
    
    return len(tasks)


def run_demo_cycles(agent: IndependentAgent, cycles: int = 10):
    """运行多个思考 - 行动循环"""
    console.print(f"\n[bold blue]🔄 运行 {cycles} 个决策循环...[/bold blue]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task("执行中...", total=cycles)
        
        for i in range(cycles):
            # 运行一个循环
            result = agent.run_cycle()
            
            # 显示结果
            console.print(Panel(result, title=f"循环 {i+1}", border_style="blue"))
            
            progress.advance(task)
    
    console.print("\n[green]✓ 循环完成[/green]\n")


def show_statistics(agent: IndependentAgent):
    """显示统计信息"""
    console.print("\n[bold blue]📊 统计信息[/bold blue]\n")
    
    stats = agent.get_status()
    
    # 创建表格
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("指标", style="dim")
    table.add_column("数值")
    
    table.add_row("完成任务数", str(stats['tasks_completed']))
    table.add_row("总奖励", f"{stats['total_reward']:.2f}")
    table.add_row("待办任务", str(stats['pending_tasks']))
    table.add_row("决策次数", str(stats['decision_stats']['total_decisions']))
    table.add_row("平均效用值", f"{stats['decision_stats']['avg_utility']:.3f}")
    table.add_row("Q 表大小", str(stats['learning_stats']['q_table_size']))
    table.add_row("学习更新次数", str(stats['learning_stats']['total_updates']))
    table.add_row("平均奖励", f"{stats['learning_stats']['avg_reward']:.3f}")
    
    console.print(table)


def show_reflection(agent: IndependentAgent):
    """显示自我反思"""
    console.print("\n[bold blue]🤔 自我反思[/bold blue]\n")
    
    reflection = agent.get_reflection()
    console.print(Panel(reflection, border_style="yellow"))


def main():
    """主函数"""
    console.print(
        Panel.fit(
            "[bold blue]独立思考 AI - MVP 演示[/bold blue]\n\n"
            "展示不依赖大模型的自主决策和学习能力",
            title="🤖 Independent AI Demo",
            border_style="blue"
        )
    )
    
    # 初始化 Agent
    console.print("\n[bold]初始化 AI Agent...[/bold]\n")
    agent = IndependentAgent(db_path="demo_memory.db")
    
    try:
        # 创建演示任务
        task_count = create_demo_tasks(agent)
        
        # 运行决策循环
        run_demo_cycles(agent, cycles=task_count + 2)
        
        # 显示统计
        show_statistics(agent)
        
        # 显示反思
        show_reflection(agent)
        
        # 最终总结
        console.print(
            "\n[bold green]✓ 演示完成！[/bold green]\n"
            "这个 AI 系统展示了：\n"
            "  • 基于效用函数的自主决策\n"
            "  • 从经验中强化学习\n"
            "  • 自我监控和反思\n"
            "  • 所有决策可解释\n"
        )
        
    finally:
        agent.close()


if __name__ == "__main__":
    main()
