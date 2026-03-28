"""
学习曲线可视化

从 JSON 数据绘制学习进度图表
"""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def load_data(filename="learning_curve_data.json"):
    """加载实验数据"""
    data_file = Path(filename)
    
    if not data_file.exists():
        console.print(f"[red]数据文件不存在：{filename}[/red]")
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def visualize_learning_curve(data):
    """可视化学习曲线"""
    
    console.print("\n")
    console.print(
        Panel(
            "[bold]📈 学习曲线可视化报告[/bold]\n\n"
            f"实验配置：{data.get('config', 'quality')}\n"
            f"运行次数：{len(data['runs'])}\n"
            f"时间范围：{data.get('start_time', 'N/A')[:19]} → {data.get('end_time', 'N/A')[:19]}",
            title="🧪 Learning Curve Visualization",
            border_style="blue"
        )
    )
    
    runs = data['runs']
    
    # 关键指标表格
    console.print("\n[bold]关键指标趋势:[/bold]\n")
    
    table = Table()
    table.add_column("轮次", justify="right", style="cyan", width=6)
    table.add_column("完成任务", justify="right", style="green", width=8)
    table.add_column("奖励", justify="right", style="yellow", width=8)
    table.add_column("Q 表大小", justify="right", style="blue", width=10)
    table.add_column("学习更新", justify="right", style="magenta", width=10)
    table.add_column("可视化", style="white")
    
    max_q = max(r['q_table_size'] for r in runs) if runs else 1
    max_updates = max(r['updates'] for r in runs) if runs else 1
    
    for run in runs:
        # Q 表进度条
        q_bar_len = int(20 * run['q_table_size'] / max_q) if max_q > 0 else 0
        q_bar = "█" * q_bar_len + "░" * (20 - q_bar_len)
        
        # 奖励颜色
        reward_color = "green" if run['reward'] >= 8 else "yellow" if run['reward'] >= 5 else "red"
        
        table.add_row(
            str(run['run']),
            f"{run['completed']}/9",
            f"[{reward_color}]{run['reward']:+.1f}[/{reward_color}]",
            str(run['q_table_size']),
            f"{run['updates']:,}",
            f"[blue]{q_bar}[/blue]"
        )
    
    console.print(table)
    
    # 学习进度分析
    console.print("\n[bold]📊 学习进度分析:[/bold]\n")
    
    if len(runs) >= 2:
        first = runs[0]
        last = runs[-1]
        
        # Q 表增长
        q_growth = last['q_table_size'] - first['q_table_size']
        q_growth_rate = q_growth / len(runs)
        
        console.print(f"  Q 表增长：{first['q_table_size']} → {last['q_table_size']} ([green]+{q_growth}[/green])")
        console.print(f"  平均每轮增长：{q_growth_rate:.1f} 个状态 - 行动对")
        
        # 学习更新
        update_growth = last['updates'] - first['updates']
        console.print(f"  学习更新：{first['updates']} → {last['updates']} ([green]+{update_growth}[/green])")
        console.print(f"  平均每轮：{update_growth / len(runs):.1f} 次更新")
        
        # 完成率
        avg_completed = sum(r['completed'] for r in runs) / len(runs)
        console.print(f"  平均完成率：{avg_completed:.1f}/9 ({avg_completed/9*100:.0f}%)")
        
        # 学习阶段判断
        console.print("\n[bold]🎯 学习阶段判断:[/bold]\n")
        
        if last['q_table_size'] < 20:
            console.print("  [yellow]初期探索阶段[/yellow]")
            console.print("    AI 刚开始学习，Q 表还在快速扩张")
        elif last['q_table_size'] < 50:
            console.print("  [cyan]快速学习阶段[/cyan]")
            console.print("    AI 正在积极学习，Q 表稳定增长")
        elif last['q_table_size'] < 100:
            console.print("  [green]稳定提升阶段[/green]")
            console.print("    AI 学习进入稳定期，开始优化已有知识")
        else:
            console.print("  [bold green]成熟阶段[/bold green]")
            console.print("    AI 已积累丰富经验，表现稳定")
        
        # 建议
        console.print("\n[bold]💡 优化建议:[/bold]\n")
        
        if q_growth_rate > 10:
            console.print("  • Q 表增长很快，可以考虑降低探索率 (epsilon)")
        elif q_growth_rate < 2:
            console.print("  • Q 表增长较慢，可以提高学习率 (alpha) 或探索率")
        
        if avg_completed < 7:
            console.print("  • 完成率偏低，检查任务难度或调整决策权重")
        elif avg_completed >= 8.5:
            console.print("  • 完成率很高！当前配置适合此类任务")
    
    # 奖励趋势图（ASCII）
    console.print("\n[bold]奖励趋势图:[/bold]\n")
    
    max_reward = max(r['reward'] for r in runs)
    min_reward = min(r['reward'] for r in runs)
    reward_range = max_reward - min_reward if max_reward != min_reward else 1
    
    for run in runs:
        bar_len = int(30 * (run['reward'] - min_reward) / reward_range) if reward_range > 0 else 15
        bar = "█" * bar_len + "░" * (30 - bar_len)
        
        color = "green" if run['reward'] >= 8 else "yellow" if run['reward'] >= 5 else "red"
        
        console.print(f"  第{run['run']:2d}轮 [{color}]{bar}[/{color}] {run['reward']:+.1f}")
    
    console.print("\n[green]✓ 可视化完成！[/green]\n")


def main():
    """主函数"""
    data = load_data()
    
    if data:
        visualize_learning_curve(data)


if __name__ == "__main__":
    main()
