"""
长期学习实验

运行 50-100 轮，观察 AI 学习的完整曲线
分析 Q 表收敛和学习率调整
"""

import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.config import get_preset


console = Console()


def run_long_term_experiment(
    preset_name: str = 'quality',
    num_runs: int = 100,
    tasks_per_run: int = 9
):
    """
    运行长期学习实验
    
    Args:
        preset_name: 配置预设名
        num_runs: 运行轮数
        tasks_per_run: 每轮任务数
    """
    
    console.print(
        Panel.fit(
            f"[bold blue]长期学习实验[/bold blue]\n\n"
            f"配置：{preset_name} | 运行次数：{num_runs} | 任务/次：{tasks_per_run}\n\n"
            f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            title="🧠 Long-Term Learning Experiment",
            border_style="blue"
        )
    )
    
    # 获取配置
    config = get_preset(preset_name)
    
    # 创建 Agent（使用同一个，以积累学习）
    agent = IndependentAgent(db_path="long_term_experiment.db")
    
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
        'config': preset_name,
        'total_runs': num_runs,
        'start_time': datetime.now().isoformat(),
        'runs': []
    }
    
    # 标准任务集（AIGC 场景）
    def create_tasks():
        from datetime import timedelta
        now = datetime.now()
        
        return [
            {'name': '紧急 bug 修复', 'priority': 10, 'estimated_time': 30, 'deadline': now + timedelta(hours=1)},
            {'name': '调试视频生成 pipeline', 'priority': 9, 'estimated_time': 120, 'deadline': now + timedelta(hours=5)},
            {'name': '设计视频开场动画', 'priority': 8, 'estimated_time': 90, 'deadline': now + timedelta(hours=4)},
            {'name': '编写 AIGC 脚本', 'priority': 8, 'estimated_time': 90, 'deadline': now + timedelta(hours=4)},
            {'name': '优化提示词工程', 'priority': 7, 'estimated_time': 90},
            {'name': '调整模型参数', 'priority': 7, 'estimated_time': 60},
            {'name': '设计分镜草图', 'priority': 6, 'estimated_time': 150},
            {'name': '写技术文档', 'priority': 5, 'estimated_time': 90},
            {'name': '回复合作者邮件', 'priority': 5, 'estimated_time': 30},
        ][:tasks_per_run]
    
    console.print("\n[bold]开始长期实验...[/bold]\n")
    console.print("[yellow]提示：这可能需要几分钟，请耐心等待[/yellow]\n")
    
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
            
            for i in range(len(create_tasks())):
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
                'tasks_completed': stats['tasks_completed'],
                'exploration_rate': stats['learning_stats']['exploration_rate']
            }
            
            experiment_data['runs'].append(run_data)
            
            # 每 10 轮显示一次详细进度
            if (run_idx + 1) % 10 == 0 or run_idx == 0:
                console.print(
                    f"  轮次 {run_idx + 1:3d}/{num_runs}: "
                    f"奖励 {run_data['avg_reward']:+.3f} | "
                    f"成功 {run_data['success_rate']:.0%} | "
                    f"Q 表 {run_data['q_table_size']:4d} | "
                    f"更新 {run_data['total_updates']:5d}"
                )
            
            progress.advance(run_task)
    
    # 实验完成
    experiment_data['end_time'] = datetime.now().isoformat()
    
    # 保存数据
    data_file = Path("long_term_experiment_data.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(experiment_data, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[green]✓ 数据已保存到 {data_file}[/green]\n")
    
    # 分析结果
    analyze_long_term_results(experiment_data)
    
    agent.close()
    
    return experiment_data


def analyze_long_term_results(data: dict):
    """分析长期实验结果"""
    
    console.print("\n[bold]📊 长期学习结果分析[/bold]\n")
    
    runs = data['runs']
    
    # 关键指标表格
    table = Table(title="关键指标")
    table.add_column("指标", style="cyan")
    table.add_column("初始 (第 1 轮)", style="yellow")
    table.add_column("中期 (第 50 轮)", style="blue")
    table.add_column("最终 (第 100 轮)", style="green")
    table.add_column("变化", style="magenta")
    
    if len(runs) >= 100:
        initial = runs[0]
        mid = runs[49]
        final = runs[99]
        
        table.add_row(
            "平均奖励",
            f"{initial['avg_reward']:+.3f}",
            f"{mid['avg_reward']:+.3f}",
            f"{final['avg_reward']:+.3f}",
            f"{final['avg_reward'] - initial['avg_reward']:+.3f}"
        )
        
        table.add_row(
            "成功率",
            f"{initial['success_rate']:.0%}",
            f"{mid['success_rate']:.0%}",
            f"{final['success_rate']:.0%}",
            f"{final['success_rate'] - initial['success_rate']:+.0%}"
        )
        
        table.add_row(
            "Q 表大小",
            str(initial['q_table_size']),
            str(mid['q_table_size']),
            str(final['q_table_size']),
            f"+{final['q_table_size'] - initial['q_table_size']}"
        )
        
        table.add_row(
            "学习更新",
            str(initial['total_updates']),
            str(mid['total_updates']),
            str(final['total_updates']),
            f"+{final['total_updates'] - initial['total_updates']}"
        )
    
    console.print(table)
    
    # 学习阶段分析
    console.print("\n[bold]🎯 学习阶段分析[/bold]\n")
    
    if len(runs) >= 10:
        # 计算每 10 轮的平均表现
        stage_rewards = []
        stage_q_sizes = []
        
        for i in range(0, len(runs), 10):
            stage_runs = runs[i:i+10]
            avg_reward = sum(r['avg_reward'] for r in stage_runs) / len(stage_runs)
            avg_q_size = sum(r['q_table_size'] for r in stage_runs) / len(stage_runs)
            
            stage_rewards.append(avg_reward)
            stage_q_sizes.append(avg_q_size)
        
        # 显示阶段表现
        for i in range(len(stage_rewards)):
            reward = stage_rewards[i]
            q_size = stage_q_sizes[i]
            
            # 判断阶段
            if i < 2:
                stage_name = "初期探索"
                stage_color = "yellow"
            elif i < 5:
                stage_name = "快速学习"
                stage_color = "cyan"
            elif i < 8:
                stage_name = "稳定提升"
                stage_color = "green"
            else:
                stage_name = "成熟优化"
                stage_color = "bold green"
            
            # 奖励条
            bar_len = int(20 * (reward + 0.5) / 1.5)  # 归一化到 0-1
            bar = "█" * bar_len + "░" * (20 - bar_len)
            
            console.print(
                f"  阶段 {i+1:2d} ({stage_name:8s}): "
                f"[{stage_color}]{bar}[/{stage_color}] "
                f"奖励 {reward:+.3f}, Q 表 {q_size:.0f}"
            )
    
    # Q 表收敛分析
    console.print("\n[bold]📈 Q 表收敛分析[/bold]\n")
    
    if len(runs) >= 10:
        # 计算 Q 表增长率
        q_growth_rates = []
        for i in range(1, len(runs)):
            growth = runs[i]['q_table_size'] - runs[i-1]['q_table_size']
            q_growth_rates.append(growth)
        
        # 分段计算平均增长率
        early_growth = sum(q_growth_rates[:len(q_growth_rates)//3]) / (len(q_growth_rates)//3)
        late_growth = sum(q_growth_rates[-len(q_growth_rates)//3:]) / (len(q_growth_rates)//3)
        
        console.print(f"  初期 Q 表增长率：{early_growth:.1f} 个/轮")
        console.print(f"  后期 Q 表增长率：{late_growth:.1f} 个/轮")
        
        if late_growth < early_growth * 0.5:
            console.print("  [green]✓ Q 表增长放缓，开始收敛[/green]")
        else:
            console.print("  [yellow]⚠ Q 表仍在快速增长，未完全收敛[/yellow]")
        
        # 收敛点估计
        for i, rate in enumerate(q_growth_rates):
            if rate < 1:  # 增长率低于 1 个/轮
                console.print(f"  [green]✓ 收敛点估计：第 {i+1} 轮左右[/green]")
                break
    
    # 学习率调整建议
    console.print("\n[bold]💡 学习率调整建议[/bold]\n")
    
    if len(runs) >= 50:
        final_reward = runs[-1]['avg_reward']
        final_q_growth = runs[-1]['q_table_size'] - runs[-2]['q_table_size']
        
        if final_reward > 0.9:
            console.print("  ✅ 当前学习率表现优秀，建议保持")
        elif final_reward > 0.7:
            console.print("  ✅ 表现良好，可以考虑降低探索率")
        elif final_reward > 0.5:
            console.print("  ⚠️ 表现一般，建议调整学习率或探索率")
        else:
            console.print("  ❌ 表现较差，需要重新调整参数")
        
        if final_q_growth > 10:
            console.print("  💡 Q 表增长过快，建议降低探索率 (epsilon)")
        elif final_q_growth < 1:
            console.print("  💡 Q 表增长过慢，建议提高学习率 (alpha)")
    
    # 可视化奖励趋势
    console.print("\n[bold]奖励趋势可视化 (每 10 轮)[/bold]\n")
    
    if len(runs) >= 10:
        max_reward = max(r['avg_reward'] for r in runs)
        min_reward = min(r['avg_reward'] for r in runs)
        reward_range = max_reward - min_reward if max_reward != min_reward else 1
        
        for i in range(0, len(runs), 10):
            stage_runs = runs[i:i+10]
            avg_reward = sum(r['avg_reward'] for r in stage_runs) / len(stage_runs)
            
            bar_len = int(30 * (avg_reward - min_reward) / reward_range) if reward_range > 0 else 15
            bar = "█" * bar_len + "░" * (30 - bar_len)
            
            color = "green" if avg_reward > 0.8 else "yellow" if avg_reward > 0.5 else "red"
            
            console.print(
                f"  轮次 {i+1:3d}-{i+10:3d}: "
                f"[{color}]{bar}[/{color}] "
                f"{avg_reward:+.3f}"
            )
    
    console.print("\n[green]✓ 长期学习分析完成！[/green]\n")


def main():
    """主函数"""
    
    console.print("\n")
    console.print(
        Panel(
            "[bold]🧠 长期学习实验[/bold]\n\n"
            "运行 100 轮，观察 AI 学习的完整过程\n\n"
            "将分析:\n"
            "  • Q 表收敛曲线\n"
            "  • 学习阶段划分\n"
            "  • 学习率调整建议\n"
            "  • 奖励趋势变化",
            title="📈 Long-Term Learning Analysis",
            border_style="blue"
        )
    )
    
    # 运行实验
    data = run_long_term_experiment(
        preset_name='quality',
        num_runs=100,
        tasks_per_run=9
    )
    
    console.print("\n[bold green]✓ 实验完成！[/bold green]\n")


if __name__ == "__main__":
    main()
