"""
质量优先配置 - AIGC 创意工作场景测试

对比质量优先配置 vs 平衡配置的效果
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.config import get_preset


console = Console()


def create_creative_tasks(agent: IndependentAgent):
    """创建创意型任务（适合质量优先配置）"""
    
    now = datetime.now()
    
    tasks = [
        {
            'name': '设计视频开场动画',
            'priority': 9,
            'estimated_time': 120,
            'deadline': now + timedelta(hours=5),
            'type': 'creative'
        },
        {
            'name': '编写 AIGC 脚本',
            'priority': 8,
            'estimated_time': 90,
            'deadline': now + timedelta(hours=4),
            'type': 'creative'
        },
        {
            'name': '调整模型参数',
            'priority': 7,
            'estimated_time': 60,
            'type': 'technical'
        },
        {
            'name': '修复 ComfyUI bug',
            'priority': 10,
            'estimated_time': 45,
            'deadline': now + timedelta(hours=2),
            'type': 'technical'
        },
        {
            'name': '设计分镜草图',
            'priority': 8,
            'estimated_time': 150,
            'type': 'creative'
        },
        {
            'name': '优化提示词',
            'priority': 6,
            'estimated_time': 60,
            'type': 'creative'
        },
        {
            'name': '整理代码',
            'priority': 4,
            'estimated_time': 45,
            'type': 'maintenance'
        },
        {
            'name': '写技术文档',
            'priority': 5,
            'estimated_time': 90,
            'type': 'documentation'
        },
    ]
    
    for task in tasks:
        agent.add_task(**{k: v for k, v in task.items() if k != 'type'})
    
    return tasks


def run_comparison():
    """运行配置对比"""
    
    console.print(
        Panel.fit(
            "[bold blue]质量优先配置 vs 平衡配置[/bold blue]\n\n"
            "AIGC 创意工作场景对比测试",
            title="🆚 Configuration Comparison",
            border_style="blue"
        )
    )
    
    results = {}
    
    # 测试两种配置
    for preset_name in ['balanced', 'quality']:
        config = get_preset(preset_name)
        
        console.print(f"\n[bold]测试配置：{config['name']}[/bold]\n")
        
        # 创建新 Agent
        agent = IndependentAgent(db_path=f"comparison_{preset_name}.db")
        
        # 应用配置
        agent.decision_engine.weights = {
            'urgency': config['decision'].urgency_weight,
            'importance': config['decision'].importance_weight,
            'efficiency': config['decision'].efficiency_weight,
            'dependency': config['decision'].dependency_weight,
        }
        agent.q_learner.alpha = config['learning'].learning_rate
        agent.q_learner.epsilon = config['learning'].exploration_rate
        
        # 创建任务
        tasks = create_creative_tasks(agent)
        
        # 运行
        creative_completed = 0
        technical_completed = 0
        total_reward = 0.0
        decisions = []
        
        for i in range(len(tasks)):
            result = agent.run_cycle()
            decisions.append(result)
            
            # 统计
            if '完成' in result:
                total_reward += 1.0
                if '设计' in result or '脚本' in result or '提示词' in result:
                    creative_completed += 1
                elif '修复' in result or '参数' in result:
                    technical_completed += 1
        
        # 获取最终状态
        final_stats = agent.get_status()
        
        results[preset_name] = {
            'config': config,
            'creative_completed': creative_completed,
            'technical_completed': technical_completed,
            'total_reward': total_reward,
            'decisions': decisions,
            'final_stats': final_stats,
        }
        
        agent.close()
    
    # 对比表格
    console.print("\n[bold]📊 对比结果[/bold]\n")
    
    table = Table(box=box.ROUNDED)
    table.add_column("指标", style="cyan")
    table.add_column("平衡配置", style="yellow")
    table.add_column("质量优先", style="green")
    
    r_balanced = results['balanced']
    r_quality = results['quality']
    
    table.add_row(
        "总奖励",
        f"{r_balanced['total_reward']:.1f}",
        f"[green]{r_quality['total_reward']:.1f}[/green]" if r_quality['total_reward'] > r_balanced['total_reward'] else f"{r_quality['total_reward']:.1f}"
    )
    
    table.add_row(
        "创意任务完成",
        f"{r_balanced['creative_completed']}个",
        f"[green]{r_quality['creative_completed']}个[/green]" if r_quality['creative_completed'] > r_balanced['creative_completed'] else f"{r_quality['creative_completed']}个"
    )
    
    table.add_row(
        "技术任务完成",
        f"{r_balanced['technical_completed']}个",
        f"{r_quality['technical_completed']}个"
    )
    
    table.add_row(
        "Q 表大小",
        str(r_balanced['final_stats']['learning_stats']['q_table_size']),
        str(r_quality['final_stats']['learning_stats']['q_table_size'])
    )
    
    table.add_row(
        "学习更新次数",
        str(r_balanced['final_stats']['learning_stats']['total_updates']),
        str(r_quality['final_stats']['learning_stats']['total_updates'])
    )
    
    console.print(table)
    
    # 详细分析
    console.print("\n[bold]📈 分析[/bold]\n")
    
    # 决策顺序对比
    console.print("[bold]平衡配置的决策顺序:[/bold]")
    for i, decision in enumerate(r_balanced['decisions'][:5], 1):
        if '思考' in decision:
            # 提取任务名
            lines = decision.split('\n')
            for line in lines:
                if '行动' in line:
                    console.print(f"  {i}. {line.strip()}")
    
    console.print("\n[bold]质量优先的决策顺序:[/bold]")
    for i, decision in enumerate(r_quality['decisions'][:5], 1):
        if '思考' in decision:
            lines = decision.split('\n')
            for line in lines:
                if '行动' in line:
                    console.print(f"  {i}. {line.strip()}")
    
    # 推荐
    console.print("\n[bold green]✓ 推荐[/bold green]\n")
    
    if r_quality['creative_completed'] > r_balanced['creative_completed']:
        console.print(
            Panel(
                "[bold]质量优先配置在创意任务上表现更好！[/bold]\n\n"
                "原因:\n"
                "  • 更重视重要性（40% vs 35%）\n"
                "  • 更重视效率（30% vs 20%）\n"
                "  • 适合需要深度思考的创意工作\n\n"
                "使用建议:\n"
                "  从 src.config import get_preset\n"
                "  config = get_preset('quality')",
                title="🏆 结论",
                border_style="green"
            )
        )
    else:
        console.print(
            Panel(
                "两种配置表现相当，可根据具体场景选择",
                title="💡 结论",
                border_style="yellow"
            )
        )


if __name__ == "__main__":
    run_comparison()
