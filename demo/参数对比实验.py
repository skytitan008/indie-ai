"""
参数对比实验脚本

对比不同配置下的 AI 表现
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.config import CONFIG_PRESETS, get_preset


console = Console()


def create_standard_tasks(agent: IndependentAgent):
    """创建标准测试任务集"""
    now = datetime.now()
    
    tasks = [
        {
            'name': '紧急 bug 修复',
            'priority': 10,
            'estimated_time': 30,
            'deadline': now + timedelta(hours=1)
        },
        {
            'name': '项目报告',
            'priority': 8,
            'estimated_time': 90,
            'deadline': now + timedelta(hours=4)
        },
        {
            'name': '团队会议',
            'priority': 7,
            'estimated_time': 60,
            'deadline': now + timedelta(hours=2)
        },
        {
            'name': '代码审查',
            'priority': 6,
            'estimated_time': 45,
        },
        {
            'name': '回复邮件',
            'priority': 5,
            'estimated_time': 30,
        },
        {
            'name': '技术调研',
            'priority': 4,
            'estimated_time': 120,
        },
        {
            'name': '文档更新',
            'priority': 3,
            'estimated_time': 60,
        },
    ]
    
    for task_info in tasks:
        agent.add_task(**task_info)


def run_experiment(preset_name: str, cycles: int = 15) -> dict:
    """运行单次实验"""
    config = get_preset(preset_name)
    
    # 创建新 Agent
    agent = IndependentAgent(db_path=f"experiment_{preset_name}.db")
    
    # 应用配置
    agent.decision_engine.weights = {
        'urgency': config['decision'].urgency_weight,
        'importance': config['decision'].importance_weight,
        'efficiency': config['decision'].efficiency_weight,
        'dependency': config['decision'].dependency_weight,
    }
    agent.q_learner.alpha = config['learning'].learning_rate
    agent.q_learner.gamma = config['learning'].discount_factor
    agent.q_learner.epsilon = config['learning'].exploration_rate
    
    # 应用奖励配置
    agent.reward_shaper.rewards = {
        'completed_on_time': config['reward'].completed_on_time,
        'completed_late': config['reward'].completed_late,
        'failed': config['reward'].failed,
        'cancelled': config['reward'].cancelled,
        'early_completion_bonus': config['reward'].early_completion_bonus,
    }
    agent.reward_shaper.high_priority_multiplier = config['reward'].high_priority_multiplier
    
    # 创建任务
    create_standard_tasks(agent)
    
    # 运行循环
    decisions = []
    rewards = []
    
    for i in range(cycles):
        result = agent.run_cycle()
        
        # 解析结果
        if '行动' in result:
            if '完成' in result:
                rewards.append(1.0)
            elif '失败' in result:
                rewards.append(-0.5)
        
        decisions.append(result)
    
    # 获取统计
    stats = agent.get_status()
    
    agent.close()
    
    return {
        'preset_name': preset_name,
        'config': config,
        'decisions': decisions,
        'rewards': rewards,
        'final_stats': stats,
        'avg_reward': sum(rewards) / len(rewards) if rewards else 0,
        'total_reward': sum(rewards),
    }


def compare_presets():
    """对比所有预设配置"""
    console.print(
        Panel.fit(
            "[bold blue]参数对比实验[/bold blue]\n\n"
            "测试不同配置下的 AI 决策表现",
            title="🧪 Experiment",
            border_style="blue"
        )
    )
    
    results = []
    
    # 运行每个预设
    for preset_name in CONFIG_PRESETS.keys():
        console.print(f"\n[bold]运行实验：{preset_name}[/bold]")
        
        result = run_experiment(preset_name, cycles=10)
        results.append(result)
        
        console.print(f"  ✓ 完成 - 平均奖励：{result['avg_reward']:.3f}")
    
    # 对比表格
    console.print("\n[bold]📊 实验结果对比[/bold]\n")
    
    table = Table(box=box.ROUNDED)
    table.add_column("配置", style="cyan")
    table.add_column("名称", style="green")
    table.add_column("平均奖励", justify="right")
    table.add_column("总奖励", justify="right")
    table.add_column("决策次数", justify="right")
    table.add_column("Q 表大小", justify="right")
    
    # 排序（按平均奖励）
    results.sort(key=lambda x: x['avg_reward'], reverse=True)
    
    for i, result in enumerate(results):
        config = result['config']
        stats = result['final_stats']
        
        # 最佳结果高亮
        if i == 0:
            name_str = f"[bold green]{config['name']}[/bold green]"
            avg_reward_str = f"[green]{result['avg_reward']:.3f}[/green]"
        else:
            name_str = config['name']
            avg_reward_str = f"{result['avg_reward']:.3f}"
        
        table.add_row(
            result['preset_name'],
            name_str,
            avg_reward_str,
            f"{result['total_reward']:.1f}",
            str(stats['decision_stats']['total_decisions']),
            str(stats['learning_stats']['q_table_size']),
        )
    
    console.print(table)
    
    # 详细分析
    console.print("\n[bold]📈 详细分析[/bold]\n")
    
    for result in results:
        config = result['config']
        
        console.print(
            Panel(
                f"[bold]配置：{config['name']}[/bold]\n\n"
                f"决策权重:\n"
                f"  • 紧急度：{config['decision'].urgency_weight:.0%}\n"
                f"  • 重要性：{config['decision'].importance_weight:.0%}\n"
                f"  • 效率：{config['decision'].efficiency_weight:.0%}\n"
                f"  • 依赖：{config['decision'].dependency_weight:.0%}\n\n"
                f"学习参数:\n"
                f"  • 学习率 (α): {config['learning'].learning_rate:.2f}\n"
                f"  • 探索率 (ε): {config['learning'].exploration_rate:.2f}\n\n"
                f"实验结果:\n"
                f"  • 平均奖励：{result['avg_reward']:.3f}\n"
                f"  • 总奖励：{result['total_reward']:.1f}\n"
                f"  • 学习更新：{result['final_stats']['learning_stats']['total_updates']}次",
                title=result['preset_name'],
                border_style="green" if result == results[0] else "white"
            )
        )
    
    # 最佳推荐
    best = results[0]
    console.print(
        Panel(
            f"[bold green]推荐配置：{best['config']['name']}[/bold green]\n\n"
            f"在此测试场景下表现最佳\n\n"
            f"使用方式:\n"
            f"  [cyan]from src.config import get_preset[/cyan]\n"
            f"  [cyan]config = get_preset('{best['preset_name']}')[/cyan]",
            title="🏆 最佳配置",
            border_style="green"
        )
    )
    
    return results


def main():
    """主函数"""
    console.print("\n[bold]开始参数对比实验...[/bold]\n")
    
    results = compare_presets()
    
    console.print("\n[green]✓ 实验完成！[/green]\n")


if __name__ == "__main__":
    main()
