"""
学习曲线绘制脚本

连续运行多次，观察 AI 的学习进步
"""

import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.config import get_preset


console = Console()


def run_learning_experiment(
    preset_name: str = 'quality',
    num_runs: int = 10,
    tasks_per_run: int = 5
):
    """
    运行学习实验
    
    连续运行多次，观察学习曲线
    """
    
    console.print(
        Panel.fit(
            f"[bold blue]学习曲线实验[/bold blue]\n\n"
            f"配置：{preset_name} | 运行次数：{num_runs} | 任务/次：{tasks_per_run}",
            title="📈 Learning Curve Experiment",
            border_style="blue"
        )
    )
    
    # 获取配置
    config = get_preset(preset_name)
    
    # 创建 Agent（使用同一个，以积累学习）
    agent = IndependentAgent(db_path="learning_experiment.db")
    
    # 应用配置
    agent.decision_engine.weights = {
        'urgency': config['decision'].urgency_weight,
        'importance': config['decision'].importance_weight,
        'efficiency': config['decision'].efficiency_weight,
        'dependency': config['decision'].dependency_weight,
    }
    agent.q_learner.alpha = config['learning'].learning_rate
    agent.q_learner.epsilon = config['learning'].exploration_rate
    
    # 实验数据
    experiment_data = {
        'runs': [],
        'config': preset_name,
        'start_time': datetime.now().isoformat()
    }
    
    # 标准任务集
    def create_tasks():
        from datetime import timedelta
        now = datetime.now()
        
        tasks = [
            {'name': '紧急 bug 修复', 'priority': 10, 'estimated_time': 30, 'deadline': now + timedelta(hours=1)},
            {'name': '写项目报告', 'priority': 8, 'estimated_time': 90, 'deadline': now + timedelta(hours=3)},
            {'name': '代码审查', 'priority': 6, 'estimated_time': 45},
            {'name': '回复邮件', 'priority': 5, 'estimated_time': 30},
            {'name': '技术调研', 'priority': 4, 'estimated_time': 120},
        ]
        return tasks
    
    console.print("\n[bold]开始连续运行...[/bold]\n")
    
    with Progress(console=console) as progress:
        run_task = progress.add_task("[cyan]运行中...", total=num_runs)
        
        for run_idx in range(num_runs):
            # 清空任务
            agent.memory.clear_all()
            
            # 创建任务
            for task_info in create_tasks():
                agent.add_task(**task_info)
            
            # 运行
            run_rewards = []
            run_successes = []
            
            for i in range(tasks_per_run):
                result = agent.run_cycle()
                
                # 记录奖励
                if '完成' in result:
                    run_rewards.append(1.0)
                    run_successes.append(True)
                elif '失败' in result:
                    run_rewards.append(-0.5)
                    run_successes.append(False)
                else:
                    run_rewards.append(0.0)
                    run_successes.append(None)
            
            # 获取统计
            stats = agent.get_status()
            
            # 记录数据
            run_data = {
                'run_number': run_idx + 1,
                'timestamp': datetime.now().isoformat(),
                'avg_reward': sum(run_rewards) / len(run_rewards) if run_rewards else 0,
                'total_reward': sum(run_rewards),
                'success_rate': sum(1 for s in run_successes if s) / len(run_successes) if run_successes else 0,
                'q_table_size': stats['learning_stats']['q_table_size'],
                'total_updates': stats['learning_stats']['total_updates'],
                'tasks_completed': stats['tasks_completed']
            }
            
            experiment_data['runs'].append(run_data)
            
            # 显示进度
            success_count = sum(1 for s in run_successes if s)
            console.print(
                f"  运行 {run_idx + 1:2d}/{num_runs}: "
                f"奖励 {run_data['avg_reward']:+.3f} | "
                f"成功 {success_count}/{tasks_per_run} | "
                f"Q 表 {run_data['q_table_size']:3d} | "
                f"更新 {run_data['total_updates']:4d}"
            )
            
            progress.advance(run_task)
    
    # 实验完成
    experiment_data['end_time'] = datetime.now().isoformat()
    
    # 保存数据
    data_file = Path("learning_experiment_data.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(experiment_data, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[green]✓ 数据已保存到 {data_file}[/green]\n")
    
    # 分析结果
    analyze_learning_curve(experiment_data)
    
    agent.close()
    
    return experiment_data


def analyze_learning_curve(data: dict):
    """分析学习曲线"""
    
    console.print("\n[bold]📊 学习曲线分析[/bold]\n")
    
    runs = data['runs']
    
    # 表格
    table = Table(title="各轮次表现")
    table.add_column("轮次", justify="right", style="cyan")
    table.add_column("平均奖励", justify="right", style="green")
    table.add_column("成功率", justify="right", style="yellow")
    table.add_column("Q 表大小", justify="right", style="blue")
    table.add_column("更新次数", justify="right", style="magenta")
    
    for run in runs:
        # 奖励颜色
        reward_str = f"{run['avg_reward']:+.3f}"
        if run['avg_reward'] > 0.8:
            reward_str = f"[green]{reward_str}[/green]"
        elif run['avg_reward'] < 0.5:
            reward_str = f"[red]{reward_str}[/red]"
        
        table.add_row(
            str(run['run_number']),
            reward_str,
            f"{run['success_rate']:.0%}",
            str(run['q_table_size']),
            str(run['total_updates'])
        )
    
    console.print(table)
    
    # 趋势分析
    console.print("\n[bold]📈 趋势分析[/bold]\n")
    
    if len(runs) >= 3:
        # 奖励趋势
        first_third_avg = sum(r['avg_reward'] for r in runs[:len(runs)//3]) / (len(runs)//3)
        last_third_avg = sum(r['avg_reward'] for r in runs[-len(runs)//3:]) / (len(runs)//3)
        
        reward_trend = last_third_avg - first_third_avg
        
        if reward_trend > 0.1:
            console.print(f"  [green]↑ 奖励呈上升趋势 (+{reward_trend:.3f})[/green]")
        elif reward_trend < -0.1:
            console.print(f"  [red]↓ 奖励呈下降趋势 ({reward_trend:.3f})[/red]")
        else:
            console.print(f"  [yellow]→ 奖励基本稳定 ({reward_trend:+.3f})[/yellow]")
        
        # Q 表增长
        q_growth = runs[-1]['q_table_size'] - runs[0]['q_table_size']
        console.print(f"  Q 表增长：+{q_growth} 个状态 - 行动对")
        
        # 学习速度
        total_updates = runs[-1]['total_updates']
        console.print(f"  总学习更新：{total_updates} 次")
        console.print(f"  平均每轮：{total_updates / len(runs):.1f} 次更新")
    
    # 最终状态
    console.print("\n[bold]🎯 最终状态[/bold]\n")
    
    final_run = runs[-1]
    console.print(f"  最终平均奖励：{final_run['avg_reward']:+.3f}")
    console.print(f"  最终成功率：{final_run['success_rate']:.0%}")
    console.print(f"  最终 Q 表大小：{final_run['q_table_size']}")
    
    # 简单可视化
    console.print("\n[bold]奖励趋势可视化[/bold]\n")
    
    max_reward = max(r['avg_reward'] for r in runs)
    min_reward = min(r['avg_reward'] for r in runs)
    range_reward = max_reward - min_reward if max_reward != min_reward else 1
    
    for run in runs:
        bar_len = int(30 * (run['avg_reward'] - min_reward) / range_reward) if range_reward > 0 else 15
        bar = "█" * bar_len + "░" * (30 - bar_len)
        
        reward_color = "green" if run['avg_reward'] > 0.7 else "yellow" if run['avg_reward'] > 0.4 else "red"
        
        console.print(
            f"  第{run['run_number']:2d}轮 [{reward_color}]{bar}[/{reward_color}] {run['avg_reward']:+.3f}"
        )
    
    # 结论
    console.print("\n[bold]💡 结论[/bold]\n")
    
    if runs[-1]['q_table_size'] > runs[0]['q_table_size'] * 2:
        console.print("  ✅ AI 明显在学习（Q 表显著增长）")
    else:
        console.print("  ⚠️ 学习速度较慢，可考虑提高学习率")
    
    if runs[-1]['avg_reward'] > runs[0]['avg_reward']:
        console.print("  ✅ 表现有提升（后期奖励更高）")
    else:
        console.print("  ⚠️ 表现稳定或略有波动")
    
    console.print("\n[green]✓ 学习曲线分析完成！[/green]\n")


def main():
    """主函数"""
    console.print("\n[bold]准备运行学习曲线实验...[/bold]\n")
    
    console.print("这将：")
    console.print("  1. 连续运行 10 次")
    console.print("  2. 每次处理 5 个任务")
    console.print("  3. 使用同一个 Agent（积累学习）")
    console.print("  4. 记录并分析学习曲线")
    console.print()
    
    # 运行实验
    data = run_learning_experiment(
        preset_name='quality',
        num_runs=10,
        tasks_per_run=5
    )
    
    console.print("\n[bold green]✓ 实验完成！[/bold green]\n")


if __name__ == "__main__":
    main()
