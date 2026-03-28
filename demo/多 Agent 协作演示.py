"""
多 Agent 协作演示

展示 2 个 Agent 如何协作完成 AIGC 项目任务
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.multi_agent import (
    MultiAgentCoordinator,
    CollaborativeAgent,
    Task,
    AgentRole
)
from src.agent import IndependentAgent
from src.config import get_preset


console = Console()


def create_collaborative_agents():
    """创建协作 Agent 团队"""
    
    console.print(
        Panel.fit(
            "[bold blue]创建多 Agent 团队[/bold blue]\n\n"
            "2 个 Agent，不同角色和技能",
            title="🤖 Multi-Agent Team",
            border_style="blue"
        )
    )
    
    # 创建协调器
    coordinator = MultiAgentCoordinator()
    
    # Agent 1: 技术专家
    tech_agent = CollaborativeAgent(
        agent_id="TechAgent-01",
        role=AgentRole.SPECIALIST,
        skills=["python", "debugging", "pipeline", "model"]
    )
    
    # 创建内部 Agent
    config = get_preset('quality')
    tech_internal = IndependentAgent(db_path="tech_agent.db")
    tech_internal.decision_engine.weights = {
        'urgency': config['decision'].urgency_weight,
        'importance': config['decision'].importance_weight,
        'efficiency': config['decision'].efficiency_weight,
        'dependency': config['decision'].dependency_weight,
    }
    tech_agent.set_internal_agent(tech_internal)
    
    # Agent 2: 创意专家
    creative_agent = CollaborativeAgent(
        agent_id="CreativeAgent-01",
        role=AgentRole.SPECIALIST,
        skills=["design", "script", "prompt", "storyboard"]
    )
    
    creative_internal = IndependentAgent(db_path="creative_agent.db")
    creative_internal.decision_engine.weights = {
        'urgency': config['decision'].urgency_weight,
        'importance': config['decision'].importance_weight,
        'efficiency': config['decision'].efficiency_weight,
        'dependency': config['decision'].dependency_weight,
    }
    creative_agent.set_internal_agent(creative_internal)
    
    # 注册 Agent
    coordinator.register_agent(tech_agent)
    coordinator.register_agent(creative_agent)
    
    console.print("\n[bold]Agent 团队:[/bold]\n")
    console.print("  🤖 TechAgent-01 (技术专家)")
    console.print("     技能：Python, Debugging, Pipeline, Model")
    console.print("  🎨 CreativeAgent-01 (创意专家)")
    console.print("     技能：Design, Script, Prompt, Storyboard")
    
    return coordinator, tech_agent, creative_agent


def create_aigc_tasks():
    """创建 AIGC 项目任务"""
    
    now = datetime.now()
    
    tasks = [
        Task(
            id="task_001",
            name="修复 ComfyUI 显存溢出",
            priority=10,
            estimated_time=60,
            required_skills=["python", "debugging"],
            reward=2.0
        ),
        Task(
            id="task_002",
            name="调试视频生成 pipeline",
            priority=9,
            estimated_time=120,
            required_skills=["pipeline", "model"],
            reward=2.0
        ),
        Task(
            id="task_003",
            name="设计视频开场动画",
            priority=8,
            estimated_time=90,
            required_skills=["design"],
            reward=1.5
        ),
        Task(
            id="task_004",
            name="编写 AIGC 脚本",
            priority=8,
            estimated_time=90,
            required_skills=["script"],
            reward=1.5
        ),
        Task(
            id="task_005",
            name="优化提示词工程",
            priority=7,
            estimated_time=90,
            required_skills=["prompt"],
            reward=1.5
        ),
        Task(
            id="task_006",
            name="设计分镜草图",
            priority=6,
            estimated_time=150,
            required_skills=["storyboard", "design"],
            reward=1.5
        ),
    ]
    
    return tasks


def run_collaboration_demo():
    """运行协作演示"""
    
    console.print("\n")
    console.print(
        Panel(
            "[bold]🤝 多 Agent 协作演示[/bold]\n\n"
            "2 个 Agent 协作完成 6 个 AIGC 项目任务\n\n"
            "观察:\n"
            "  • 任务如何分配\n"
            "  • Agent 如何通信\n"
            "  • 协作效率如何",
            title="🎬 Collaboration Demo",
            border_style="blue"
        )
    )
    
    # 创建团队
    coordinator, tech_agent, creative_agent = create_collaborative_agents()
    
    # 创建任务
    tasks = create_aigc_tasks()
    
    console.print("\n[bold]项目任务:[/bold]\n")
    for task in tasks:
        skills_str = ", ".join(task.required_skills)
        console.print(f"  • {task.name} (P{task.priority}, 技能：{skills_str})")
    
    # 添加任务到协调器
    for task in tasks:
        coordinator.add_task(task)
    
    console.print("\n[bold]开始协作...[/bold]\n")
    
    # 运行协作
    max_cycles = 10
    completed_tasks = 0
    
    with Progress(console=console) as progress:
        cycle_task = progress.add_task("[cyan]协作进行中...", total=max_cycles)
        
        for cycle in range(max_cycles):
            console.print(f"\n[bold]━━ 第 {cycle + 1} 轮 ━━[/bold]\n")
            
            # 运行一轮协作
            coordinator.run_collaboration_cycle()
            
            # 更新 Agent 状态
            tech_agent.update_state()
            creative_agent.update_state()
            
            # 显示状态
            tech_stats = tech_agent.get_stats()
            creative_stats = creative_agent.get_stats()
            
            console.print(f"  🤖 TechAgent: 负载 {tech_stats['workload']:.0%}, "
                         f"可用 {tech_stats['availability']:.0%}, "
                         f"信任 {tech_stats['trust_score']:.2f}")
            console.print(f"  🎨 CreativeAgent: 负载 {creative_stats['workload']:.0%}, "
                         f"可用 {creative_stats['availability']:.0%}, "
                         f"信任 {creative_stats['trust_score']:.2f}")
            
            # 检查任务完成情况
            completed = sum(1 for t in tasks if t.status == "completed")
            if completed > completed_tasks:
                new_completed = completed - completed_tasks
                console.print(f"\n  [green]✓ 新完成 {new_completed} 个任务！[/green]")
                completed_tasks = completed
            
            # 检查是否全部完成
            if completed == len(tasks):
                console.print("\n[bold green]✓ 所有任务完成！[/bold green]\n")
                break
            
            progress.advance(cycle_task)
    
    # 最终统计
    console.print("\n[bold]📊 协作统计[/bold]\n")
    
    stats = coordinator.get_stats()
    
    table = Table(title="协作结果")
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="green")
    
    table.add_row("总 Agent 数", str(stats['total_agents']))
    table.add_row("总任务数", str(stats['total_tasks']))
    table.add_row("完成任务", str(stats['completed_tasks']))
    table.add_row("总消息数", str(stats['total_messages']))
    table.add_row("协作轮数", str(stats['collaboration_rounds']))
    
    console.print(table)
    
    # Agent 个人统计
    console.print("\n[bold]Agent 表现:[/bold]\n")
    
    agent_table = Table()
    agent_table.add_column("Agent", style="cyan")
    agent_table.add_column("角色", style="blue")
    agent_table.add_column("完成任务", justify="right", style="green")
    agent_table.add_column("信任度", justify="right", style="yellow")
    agent_table.add_column("技能", style="magenta")
    
    agent_table.add_row(
        "TechAgent-01",
        "技术专家",
        str(len(tech_agent.task_history)),
        f"{tech_agent.state.trust_score:.2f}",
        ", ".join(tech_agent.state.skills)
    )
    
    agent_table.add_row(
        "CreativeAgent-01",
        "创意专家",
        str(len(creative_agent.task_history)),
        f"{creative_agent.state.trust_score:.2f}",
        ", ".join(creative_agent.state.skills)
    )
    
    console.print(agent_table)
    
    # 任务分配分析
    console.print("\n[bold]📋 任务分配详情:[/bold]\n")
    
    for task in tasks:
        status_emoji = "✅" if task.status == "completed" else "❌" if task.status == "failed" else "⏳"
        assigned_to = task.assigned_to or "未分配"
        console.print(f"  {status_emoji} {task.name}")
        console.print(f"      执行者：{assigned_to}")
        console.print(f"      状态：{task.status}")
        console.print()
    
    # 清理
    tech_agent.internal_agent.close()
    creative_agent.internal_agent.close()
    
    console.print(
        Panel(
            "[bold]✓ 多 Agent 协作演示完成！[/bold]\n\n"
            "关键特性:\n"
            "  • 基于技能的智能分配\n"
            "  • Agent 间自主通信\n"
            "  • 动态负载均衡\n"
            "  • 信任度机制\n\n"
            "下一步:\n"
            "  • 增加更多 Agent\n"
            "  • 实现任务转包\n"
            "  • 添加冲突解决机制",
            title="🎉 演示完成",
            border_style="green"
        )
    )


def main():
    """主函数"""
    run_collaboration_demo()


if __name__ == "__main__":
    main()
