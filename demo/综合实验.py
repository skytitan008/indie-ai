"""
综合实验套件

整合所有实验功能，一键运行完整测试
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.config import get_preset


console = Console()


def apply_config(agent, preset_name):
    """应用预设配置"""
    config = get_preset(preset_name)
    agent.decision_engine.weights = {
        'urgency': config['decision'].urgency_weight,
        'importance': config['decision'].importance_weight,
        'efficiency': config['decision'].efficiency_weight,
        'dependency': config['decision'].dependency_weight,
    }
    agent.q_learner.alpha = config['learning'].learning_rate
    agent.q_learner.epsilon = config['learning'].exploration_rate
    return config


def create_aigc_tasks():
    """创建 AIGC 视频项目任务"""
    now = datetime.now()
    
    return [
        {'name': '修复 ComfyUI 显存溢出', 'priority': 10, 'estimated_time': 60, 'deadline': now + timedelta(hours=2)},
        {'name': '调试视频生成 pipeline', 'priority': 9, 'estimated_time': 120, 'deadline': now + timedelta(hours=5)},
        {'name': '设计视频开场动画', 'priority': 8, 'estimated_time': 90, 'deadline': now + timedelta(hours=4)},
        {'name': '编写 AIGC 脚本', 'priority': 8, 'estimated_time': 90, 'deadline': now + timedelta(hours=4)},
        {'name': '优化提示词工程', 'priority': 7, 'estimated_time': 90},
        {'name': '调整模型参数', 'priority': 7, 'estimated_time': 60},
        {'name': '设计分镜草图', 'priority': 6, 'estimated_time': 150},
        {'name': '写技术文档', 'priority': 5, 'estimated_time': 90},
        {'name': '回复合作者邮件', 'priority': 5, 'estimated_time': 30},
    ]


def run_quality_test():
    """质量优先配置测试"""
    console.print(
        Panel.fit(
            "[bold blue]质量优先配置测试[/bold blue]\n\n"
            "AIGC 创意工作场景",
            title="🎨 Quality First Test",
            border_style="blue"
        )
    )
    
    agent = IndependentAgent(db_path="quality_test.db")
    apply_config(agent, 'quality')
    
    tasks = create_aigc_tasks()
    
    console.print("\n[bold]任务列表:[/bold]\n")
    for i, task in enumerate(tasks, 1):
        deadline = task.get('deadline', '').strftime('%H:%M') if task.get('deadline') else '无'
        console.print(f"  {i}. {task['name']} (P{task['priority']}, {deadline}截止)")
    
    console.print("\n[bold]开始执行...[/bold]\n")
    
    completed = []
    failed = []
    
    with Progress(console=console) as progress:
        task_progress = progress.add_task("[cyan]执行中...", total=len(tasks))
        
        for _ in range(len(tasks)):
            result = agent.run_cycle()
            
            if '完成' in result:
                # 提取任务名
                for task in tasks:
                    if task['name'] in result and task['name'] not in completed:
                        completed.append(task['name'])
                        break
            elif '失败' in result:
                for task in tasks:
                    if task['name'] in result and task['name'] not in failed:
                        failed.append(task['name'])
                        break
            
            progress.advance(task_progress)
    
    stats = agent.get_status()
    
    # 结果表格
    table = Table(title="执行结果")
    table.add_column("指标", style="cyan")
    table.add_column("数值", style="green")
    
    table.add_row("完成任务", f"{len(completed)}/{len(tasks)}")
    table.add_row("完成率", f"{len(completed)/len(tasks)*100:.0f}%")
    table.add_row("总奖励", f"{stats['total_reward']:.2f}")
    table.add_row("Q 表大小", str(stats['learning_stats']['q_table_size']))
    table.add_row("学习更新", str(stats['learning_stats']['total_updates']))
    
    console.print("\n")
    console.print(table)
    
    # 完成的任务
    console.print("\n[bold green]✓ 完成的任务:[/bold green]")
    for task in completed:
        console.print(f"  • {task}")
    
    if failed:
        console.print("\n[bold red]✗ 失败的任务:[/bold red]")
        for task in failed:
            console.print(f"  • {task}")
    
    # AI 反思
    console.print("\n[bold]🤔 AI 反思:[/bold]")
    console.print(f"  {agent.get_reflection()}")
    
    agent.close()
    
    return {
        'completed': len(completed),
        'total': len(tasks),
        'reward': stats['total_reward'],
        'q_table_size': stats['learning_stats']['q_table_size'],
        'updates': stats['learning_stats']['total_updates']
    }


def run_learning_curve(num_runs=10):
    """学习曲线实验"""
    console.print(
        Panel.fit(
            f"[bold blue]学习曲线实验[/bold blue]\n\n"
            f"连续运行 {num_runs} 次，观察学习进步",
            title="📈 Learning Curve",
            border_style="blue"
        )
    )
    
    agent = IndependentAgent(db_path="learning_curve.db")
    apply_config(agent, 'quality')
    
    experiment_data = {'runs': []}
    
    with Progress(console=console) as progress:
        run_progress = progress.add_task("[cyan]运行中...", total=num_runs)
        
        for run_idx in range(num_runs):
            # 清空并重新创建任务
            agent.memory.clear_all()
            
            for task in create_aigc_tasks():
                agent.add_task(**task)
            
            # 运行
            run_completed = 0
            run_reward = 0
            
            for _ in range(len(create_aigc_tasks())):
                result = agent.run_cycle()
                if '完成' in result:
                    run_completed += 1
                    run_reward += 1.0
            
            # 记录
            stats = agent.get_status()
            run_data = {
                'run': run_idx + 1,
                'completed': run_completed,
                'reward': run_reward,
                'q_table_size': stats['learning_stats']['q_table_size'],
                'updates': stats['learning_stats']['total_updates']
            }
            experiment_data['runs'].append(run_data)
            
            # 显示
            console.print(
                f"  运行 {run_idx + 1:2d}/{num_runs}: "
                f"完成 {run_completed}/9 | "
                f"奖励 {run_reward:+.1f} | "
                f"Q 表 {run_data['q_table_size']:3d} | "
                f"更新 {run_data['updates']:4d}"
            )
            
            progress.advance(run_progress)
    
    # 保存数据
    with open("learning_curve_data.json", 'w', encoding='utf-8') as f:
        json.dump(experiment_data, f, indent=2, ensure_ascii=False)
    
    console.print("\n[green]✓ 数据已保存[/green]\n")
    
    # 分析
    runs = experiment_data['runs']
    
    if len(runs) >= 2:
        first_q = runs[0]['q_table_size']
        last_q = runs[-1]['q_table_size']
        q_growth = last_q - first_q
        
        console.print(f"[bold]学习进步:[/bold]")
        console.print(f"  Q 表增长：{first_q} → {last_q} (+{q_growth})")
        console.print(f"  总学习更新：{runs[-1]['updates']} 次")
        
        if q_growth > 0:
            console.print("  [green]✓ AI 正在学习！[/green]")
    
    agent.close()
    
    return experiment_data


def main():
    """主函数"""
    console.print("\n")
    console.print(
        Panel(
            "[bold]🚀 独立 AI MVP 综合实验套件[/bold]\n\n"
            "作者：小七 & 老王\n"
            f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "运行内容:\n"
            "  1. 质量优先配置测试\n"
            "  2. 学习曲线实验 (10 次连续运行)\n"
            "  3. 结果总结",
            title="🧪 Experiment Suite",
            border_style="blue"
        )
    )
    
    # 实验 1: 质量优先测试
    console.print("\n" + "="*60 + "\n")
    quality_result = run_quality_test()
    
    # 实验 2: 学习曲线
    console.print("\n" + "="*60 + "\n")
    learning_result = run_learning_curve(num_runs=10)
    
    # 总结
    console.print("\n" + "="*60 + "\n")
    console.print(
        Panel.fit(
            "[bold green]✓ 所有实验完成！[/bold green]\n\n"
            "关键发现:\n"
            f"  • 质量优先配置完成率：{quality_result['completed']}/{quality_result['total']}\n"
            f"  • Q 表最终大小：{quality_result['q_table_size']}\n"
            f"  • 总学习更新：{quality_result['updates']} 次\n\n"
            "下一步:\n"
            "  • 查看 learning_curve_data.json 详细数据\n"
            "  • 调整 config.py 中的权重参数\n"
            "  • 集成到实际 AIGC 工作流",
            title="📊 实验总结",
            border_style="green"
        )
    )


if __name__ == "__main__":
    main()
