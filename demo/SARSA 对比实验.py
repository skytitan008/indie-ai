"""
SARSA vs Q-Learning 对比实验

比较两种强化学习算法在任务调度场景的表现
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
from src.learning.sarsa import SARSALearner, SARSAConfig
from src.config import get_preset


console = Console()


def create_tasks():
    """创建标准任务集"""
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
    ]


def run_sarsa_experiment(num_episodes: int = 50):
    """运行 SARSA 实验"""
    
    console.print("\n[bold blue]运行 SARSA 实验...[/bold blue]\n")
    
    config = SARSAConfig(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.1,
        exploration_decay=0.995
    )
    
    sarsa = SARSALearner(db_path="sarsa_experiment.db", config=config)
    
    episode_rewards = []
    
    with Progress(console=console) as progress:
        progress_task = progress.add_task("[cyan]SARSA 训练中...", total=num_episodes)
        
        for episode in range(num_episodes):
            # 简化：每个 episode 处理 9 个任务
            total_reward = 0.0
            
            for task_idx, task in enumerate(create_tasks()):
                # 状态：任务优先级 + 剩余时间
                state = f"p{task['priority']}_t{task_idx}"
                actions = ['execute', 'defer', 'cancel']
                
                # 选择动作
                action = sarsa.choose_action(state, actions)
                
                # 模拟奖励
                if action == 'execute':
                    reward = 1.0 if task['priority'] >= 7 else 0.5
                elif action == 'defer':
                    reward = 0.0
                else:  # cancel
                    reward = -0.5
                
                # 下一个状态
                next_state = f"p{task['priority']}_t{task_idx + 1}"
                next_actions = ['execute', 'defer', 'cancel']
                
                # SARSA 学习
                sarsa.learn(state, action, reward, next_state, next_actions)
                
                total_reward += reward
            
            # 结束 episode
            sarsa.end_episode(total_reward)
            episode_rewards.append(total_reward)
            
            # 每 10 轮显示
            if (episode + 1) % 10 == 0:
                avg_reward = sum(episode_rewards[-10:]) / 10
                stats = sarsa.get_stats()
                console.print(
                    f"  Episode {episode + 1:3d}/{num_episodes}: "
                    f"奖励 {avg_reward:+.2f} | "
                    f"Q 表 {stats['q_table_size']:3d} | "
                    f"更新 {stats['total_updates']:4d} | "
                    f"ε={stats['exploration_rate']:.3f}"
                )
            
            progress.advance(progress_task)
    
    return sarsa, episode_rewards


def run_qlearning_experiment(num_episodes: int = 50):
    """运行 Q-Learning 实验（使用现有的 SimpleQLearner）"""
    
    console.print("\n[bold green]运行 Q-Learning 实验...[/bold green]\n")
    
    from src.learning.qlearner import SimpleQLearner
    
    qlearner = SimpleQLearner(
        learning_rate=0.1,
        discount_factor=0.9,
        exploration_rate=0.1
    )
    
    episode_rewards = []
    
    with Progress(console=console) as progress:
        progress_task = progress.add_task("[cyan]Q-Learning 训练中...", total=num_episodes)
        
        for episode in range(num_episodes):
            total_reward = 0.0
            
            for task_idx, task in enumerate(create_tasks()):
                state = f"p{task['priority']}_t{task_idx}"
                actions = ['execute', 'defer', 'cancel']
                
                # Q-Learning 选择动作
                action = qlearner.choose_action(state, actions)
                
                # 模拟奖励
                if action == 'execute':
                    reward = 1.0 if task['priority'] >= 7 else 0.5
                elif action == 'defer':
                    reward = 0.0
                else:
                    reward = -0.5
                
                # 下一个状态
                next_state = f"p{task['priority']}_t{task_idx + 1}"
                
                # Q-Learning 更新
                qlearner.update(state, action, reward, next_state, actions)
                
                total_reward += reward
            
            qlearner.epsilon = max(0.01, qlearner.epsilon * 0.995)
            episode_rewards.append(total_reward)
            
            if (episode + 1) % 10 == 0:
                avg_reward = sum(episode_rewards[-10:]) / 10
                stats = qlearner.get_stats()
                console.print(
                    f"  Episode {episode + 1:3d}/{num_episodes}: "
                    f"奖励 {avg_reward:+.2f} | "
                    f"Q 表 {stats.get('q_table_size', 0):3d} | "
                    f"更新 {stats.get('total_updates', 0):4d} | "
                    f"ε={qlearner.epsilon:.3f}"
                )
            
            progress.advance(progress_task)
    
    return qlearner, episode_rewards


def compare_algorithms(sarsa, qlearner, sarsa_rewards, qlearning_rewards):
    """对比两种算法"""
    
    console.print("\n[bold]📊 算法对比结果[/bold]\n")
    
    table = Table(title="SARSA vs Q-Learning")
    table.add_column("指标", style="cyan", width=20)
    table.add_column("SARSA", style="blue", width=15)
    table.add_column("Q-Learning", style="green", width=15)
    table.add_column("优势", style="yellow", width=20)
    
    sarsa_stats = sarsa.get_stats()
    qlearning_stats = qlearner.get_stats()
    
    # 平均奖励
    sarsa_avg = sum(sarsa_rewards[-20:]) / 20
    ql_avg = sum(qlearning_rewards[-20:]) / 20
    
    table.add_row(
        "平均奖励 (后 20 轮)",
        f"{sarsa_avg:+.2f}",
        f"{ql_avg:+.2f}",
        "SARSA" if sarsa_avg > ql_avg else "Q-Learning"
    )
    
    # Q 表大小
    table.add_row(
        "Q 表大小",
        str(sarsa_stats['q_table_size']),
        str(qlearning_stats['q_table_size']),
        "更小" if sarsa_stats['q_table_size'] < qlearning_stats['q_table_size'] else "更大"
    )
    
    # 学习更新
    table.add_row(
        "总更新次数",
        str(sarsa_stats['total_updates']),
        str(qlearning_stats['total_updates']),
        "更多" if sarsa_stats['total_updates'] > qlearning_stats['total_updates'] else "更少"
    )
    
    # 最终探索率
    table.add_row(
        "最终探索率",
        f"{sarsa_stats['exploration_rate']:.3f}",
        f"{qlearning_stats['exploration_rate']:.3f}",
        "更稳定" if sarsa_stats['exploration_rate'] < qlearning_stats['exploration_rate'] else "更探索"
    )
    
    console.print(table)
    
    # 详细分析
    console.print("\n[bold]📈 详细分析[/bold]\n")
    
    # 奖励趋势对比
    console.print("[bold]奖励趋势对比 (每 10 轮平均):[/bold]\n")
    
    for i in range(0, 50, 10):
        sarsa_stage = sum(sarsa_rewards[i:i+10]) / 10
        ql_stage = sum(qlearning_rewards[i:i+10]) / 10
        
        sarsa_bar = "█" * int(20 * (sarsa_stage + 1) / 2)
        ql_bar = "█" * int(20 * (ql_stage + 1) / 2)
        
        console.print(
            f"  轮次 {i+1:2d}-{i+10:2d}: "
            f"SARSA: [{sarsa_bar:20s}] {sarsa_stage:+.2f}  |  "
            f"Q-L:   [{ql_bar:20s}] {ql_stage:+.2f}"
        )
    
    # 特性对比
    console.print("\n[bold]特性对比:[/bold]\n")
    
    console.print("  [bold blue]SARSA (On-policy):[/bold blue]")
    console.print("    ✓ 学习当前策略，更保守")
    console.print("    ✓ 适合风险敏感场景")
    console.print("    ✓ 探索更稳定")
    console.print("    ✗ 可能收敛到次优策略\n")
    
    console.print("  [bold green]Q-Learning (Off-policy):[/bold green]")
    console.print("    ✓ 学习最优策略，更激进")
    console.print("    ✓ 适合追求最优解")
    console.print("    ✓ 收敛更快")
    console.print("    ✗ 探索可能不稳定\n")
    
    # 推荐
    console.print("[bold]💡 使用建议:[/bold]\n")
    
    if sarsa_avg > ql_avg:
        console.print("  在本场景中，[blue]SARSA[/blue] 表现更好！")
        console.print("  推荐用于：风险敏感、需要稳定探索的任务")
    else:
        console.print("  在本场景中，[green]Q-Learning[/green] 表现更好！")
        console.print("  推荐用于：追求最优解、可以快速收敛的任务")


def main():
    """主函数"""
    
    console.print("\n")
    console.print(
        Panel(
            "[bold]🧪 SARSA vs Q-Learning 对比实验[/bold]\n\n"
            "比较两种强化学习算法\n\n"
            "SARSA: On-policy，学习当前策略\n"
            "Q-Learning: Off-policy，学习最优策略",
            title="🤖 Algorithm Comparison",
            border_style="blue"
        )
    )
    
    # 运行实验
    sarsa, sarsa_rewards = run_sarsa_experiment(num_episodes=50)
    qlearner, qlearning_rewards = run_qlearning_experiment(num_episodes=50)
    
    # 对比分析
    compare_algorithms(sarsa, qlearner, sarsa_rewards, qlearning_rewards)
    
    # 保存数据
    data = {
        'sarsa': {
            'rewards': sarsa_rewards,
            'stats': sarsa.get_stats()
        },
        'qlearning': {
            'rewards': qlearning_rewards,
            'stats': qlearner.get_stats()
        },
        'timestamp': datetime.now().isoformat()
    }
    
    with open("algorithm_comparison_data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[green]✓ 数据已保存到 algorithm_comparison_data.json[/green]\n")
    
    console.print(
        Panel(
            "[bold]✓ 对比实验完成！[/bold]\n\n"
            "两种算法各有优劣，选择取决于具体场景：\n"
            "  • 风险敏感 → SARSA\n"
            "  • 追求最优 → Q-Learning",
            title="📊 结论",
            border_style="green"
        )
    )


if __name__ == "__main__":
    main()
