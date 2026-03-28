"""
决策过程可视化脚本

展示 AI 的决策思路和学习过程
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress
from rich import box

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent


console = Console()


def visualize_decision_process(agent: IndependentAgent, task_name: str):
    """可视化单个任务的决策过程"""
    
    console.print(
        Panel(
            f"[bold]分析任务：{task_name}[/bold]",
            title="🔍 决策过程可视化",
            border_style="cyan"
        )
    )
    
    # 获取所有待办任务
    pending_tasks = agent.memory.get_pending_tasks()
    
    if not pending_tasks:
        console.print("[yellow]没有待办任务[/yellow]")
        return
    
    console.print("\n[bold]步骤 1: 收集候选任务[/bold]\n")
    
    # 显示所有候选任务
    table = Table(box=box.SIMPLE)
    table.add_column("任务", style="cyan")
    table.add_column("优先级", justify="right")
    table.add_column("预估时间", justify="right")
    table.add_column("截止", justify="right")
    table.add_column("紧急度", justify="right")
    
    for task in pending_tasks:
        deadline_str = task.deadline.strftime('%H:%M') if task.deadline else '无'
        tree = Tree(task.name)
        tree.add(f"优先级：{task.priority}")
        tree.add(f"预估：{task.estimated_time}分钟")
        
        table.add_row(
            task.name,
            str(task.priority),
            f"{task.estimated_time}分钟",
            deadline_str,
            f"{task.urgency:.2f}"
        )
    
    console.print(table)
    
    # 计算每个任务的效用值
    console.print("\n[bold]步骤 2: 计算效用值[/bold]\n")
    
    utilities = {}
    breakdown = {}
    
    for task in pending_tasks:
        # 计算各因素
        urgency = agent.decision_engine._calculate_urgency(task, datetime.now())
        importance = task.priority / 10.0
        efficiency = agent.decision_engine._calculate_efficiency(task)
        dependency = agent.decision_engine._calculate_dependency(task)
        
        # 加权计算
        utility = (
            agent.decision_engine.weights['urgency'] * urgency +
            agent.decision_engine.weights['importance'] * importance +
            agent.decision_engine.weights['efficiency'] * efficiency +
            agent.decision_engine.weights['dependency'] * dependency
        )
        
        utilities[task.id] = utility
        breakdown[task.name] = {
            'urgency': urgency,
            'importance': importance,
            'efficiency': efficiency,
            'dependency': dependency,
            'total': utility
        }
    
    # 显示效用分解
    table = Table(box=box.ROUNDED)
    table.add_column("任务", style="cyan")
    table.add_column("紧急度\n(35%)", justify="right", style="yellow")
    table.add_column("重要性\n(35%)", justify="right", style="green")
    table.add_column("效率\n(20%)", justify="right", style="blue")
    table.add_column("依赖\n(10%)", justify="right", style="magenta")
    table.add_column("总效用", justify="right", style="bold")
    
    for task_name, data in breakdown.items():
        # 高亮最高分
        is_best = data['total'] == max(b['total'] for b in breakdown.values())
        
        if is_best:
            total_str = f"[bold green]{data['total']:.3f}[/bold green]"
        else:
            total_str = f"{data['total']:.3f}"
        
        table.add_row(
            task_name,
            f"{data['urgency']:.3f}",
            f"{data['importance']:.3f}",
            f"{data['efficiency']:.3f}",
            f"{data['dependency']:.3f}",
            total_str
        )
    
    console.print(table)
    
    # 显示决策理由
    console.print("\n[bold]步骤 3: 生成决策理由[/bold]\n")
    
    best_task = max(pending_tasks, key=lambda t: utilities[t.id])
    
    reasons = []
    if best_task.urgency > 0.7:
        reasons.append(f"🔥 任务紧急（剩余时间少）")
    if best_task.priority >= 8:
        reasons.append(f"⭐ 优先级高（{best_task.priority}/10）")
    eff = agent.decision_engine.task_efficiency.get(best_task.name, 0.5)
    if eff > 0.7:
        reasons.append(f"✓ 历史完成率高（{eff:.0%}）")
    if best_task.dependencies:
        reasons.append(f"🔗 有{len(best_task.dependencies)}个后续依赖")
    
    if not reasons:
        reasons.append("💡 综合效用值最高")
    
    for reason in reasons:
        console.print(f"  {reason}")
    
    console.print(f"\n[bold green]✓ 最终决策：{best_task.name}[/bold green]")


def show_learning_progress(agent: IndependentAgent):
    """展示学习进度"""
    
    console.print(
        Panel(
            "[bold]Q-Learning 学习进度[/bold]",
            title="📈 学习曲线",
            border_style="green"
        )
    )
    
    stats = agent.q_learner.get_stats()
    
    # 学习统计
    console.print(f"\n  Q 表大小：{stats['q_table_size']} 个状态 - 行动对")
    console.print(f"  总更新次数：{stats['total_updates']} 次")
    console.print(f"  平均奖励：{stats['avg_reward']:.3f}")
    console.print(f"  探索率：{stats['exploration_rate']:.0%}")
    console.print(f"  经验缓冲区：{stats['experience_buffer_size']} 条")
    
    # Q 值分布
    if agent.q_learner.q_table:
        console.print("\n[bold]Q 值分布[/bold]\n")
        
        q_values = []
        for state_actions in agent.q_learner.q_table.values():
            q_values.extend(state_actions.values())
        
        if q_values:
            min_q = min(q_values)
            max_q = max(q_values)
            avg_q = sum(q_values) / len(q_values)
            
            console.print(f"  最小值：{min_q:.3f}")
            console.print(f"  最大值：{max_q:.3f}")
            console.print(f"  平均值：{avg_q:.3f}")
            
            # 简单直方图
            console.print("\n  Q 值分布:")
            buckets = {'<0': 0, '0-0.5': 0, '0.5-1.0': 0, '>1.0': 0}
            for q in q_values:
                if q < 0:
                    buckets['<0'] += 1
                elif q < 0.5:
                    buckets['0-0.5'] += 1
                elif q < 1.0:
                    buckets['0.5-1.0'] += 1
                else:
                    buckets['>1.0'] += 1
            
            max_count = max(buckets.values())
            for bucket, count in buckets.items():
                bar_len = int(20 * count / max_count) if max_count > 0 else 0
                bar = "█" * bar_len
                console.print(f"    {bucket:8} |{bar} {count}")


def show_self_reflection(agent: IndependentAgent):
    """显示自我反思"""
    
    console.print(
        Panel(
            "[bold]自我监控报告[/bold]",
            title="🤔 自我反思",
            border_style="yellow"
        )
    )
    
    reflection = agent.get_reflection()
    console.print(f"\n{reflection}\n")
    
    # 性能指标
    stats = agent.monitor.get_performance_summary()
    
    if stats['status'] != 'no_data':
        console.print("\n[bold]性能指标[/bold]\n")
        console.print(f"  状态：{'✅ 良好' if stats['status'] == 'good' else '⚠️ 注意'}")
        console.print(f"  平均偏差：{stats['avg_deviation']:.1%}")
        console.print(f"  表现不佳率：{stats['underperforming_rate']:.0%}")
        console.print(f"  总记录数：{stats['total_records']}")
        console.print(f"  洞察数：{stats['total_insights']}")


def run_full_demo():
    """运行完整可视化演示"""
    
    console.print(
        Panel.fit(
            "[bold blue]独立思考 AI - 决策过程可视化[/bold blue]",
            title="🎬 Visualization Demo",
            border_style="blue"
        )
    )
    
    # 初始化 Agent
    agent = IndependentAgent(db_path="visualization_demo.db")
    
    try:
        # 创建任务
        console.print("\n[bold]创建测试任务...[/bold]\n")
        
        now = datetime.now()
        tasks = [
            {'name': '修复紧急 bug', 'priority': 10, 'estimated_time': 30, 'deadline': now + timedelta(hours=1)},
            {'name': '写项目报告', 'priority': 8, 'estimated_time': 90, 'deadline': now + timedelta(hours=4)},
            {'name': '团队会议', 'priority': 7, 'estimated_time': 60, 'deadline': now + timedelta(hours=2)},
            {'name': '代码审查', 'priority': 6, 'estimated_time': 45},
            {'name': '回复邮件', 'priority': 5, 'estimated_time': 30},
        ]
        
        for task in tasks:
            agent.add_task(**task)
            console.print(f"  ✓ {task['name']}")
        
        # 运行 3 个循环并可视化
        for i in range(3):
            console.print(f"\n{'='*60}")
            console.print(f"[bold]第 {i+1} 次决策循环[/bold]")
            console.print(f"{'='*60}\n")
            
            # 思考
            reasoning = agent.think()
            
            if "没有" not in reasoning:
                # 可视化决策过程
                if agent.current_task:
                    visualize_decision_process(agent, agent.current_task.name)
                
                # 行动
                result = agent.act()
                console.print(f"\n[green]✓ {result['message']}[/green]")
            
            # 展示学习进度
            if i == 2:  # 最后一次展示
                show_learning_progress(agent)
                show_self_reflection(agent)
        
        # 最终状态
        console.print(f"\n{'='*60}")
        console.print("[bold]最终状态[/bold]")
        console.print(f"{'='*60}\n")
        
        status = agent.get_status()
        console.print(f"  完成任务：{status['tasks_completed']}")
        console.print(f"  总奖励：{status['total_reward']:.2f}")
        console.print(f"  待办任务：{status['pending_tasks']}")
        
    finally:
        agent.close()


if __name__ == "__main__":
    run_full_demo()
