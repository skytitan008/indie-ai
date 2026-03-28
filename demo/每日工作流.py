"""
日报生成器

每天早上让 AI 安排任务，晚上生成执行报告
"""

import sys
from pathlib import Path
from datetime import datetime, date
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.config import get_preset


console = Console()


class DailyWorkflow:
    """
    每日工作流
    
    早间计划 + 晚间报告
    """
    
    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.agent = None
        self.today = date.today()
    
    def morning_planning(self, tasks: list) -> str:
        """
        早间计划：让 AI 安排今日任务
        
        Args:
            tasks: 任务列表，每项包含 name, priority, estimated_time, deadline(可选)
        """
        console.print(
            Panel.fit(
                f"[bold blue]早间计划 - {self.today}[/bold blue]",
                title="🌅 Morning Planning",
                border_style="blue"
            )
        )
        
        # 初始化 Agent（使用质量优先配置）
        config = get_preset('quality')
        self.agent = IndependentAgent(db_path=f"daily_{self.today}.db")
        
        # 应用配置
        self.agent.decision_engine.weights = {
            'urgency': config['decision'].urgency_weight,
            'importance': config['decision'].importance_weight,
            'efficiency': config['decision'].efficiency_weight,
            'dependency': config['decision'].dependency_weight,
        }
        
        # 添加任务
        console.print("\n[bold]添加今日任务...[/bold]\n")
        
        for task in tasks:
            self.agent.add_task(**task)
            deadline_str = task.get('deadline', '').strftime('%H:%M') if task.get('deadline') else '无'
            console.print(f"  ✓ {task['name']} (P{task['priority']}, {task['estimated_time']}分钟，截止：{deadline_str})")
        
        # 让 AI 排序
        console.print("\n[bold]AI 建议的执行顺序:[/bold]\n")
        
        planned_order = []
        
        for i in range(len(tasks)):
            reasoning = self.agent.think()
            
            if self.agent.current_task:
                task_name = self.agent.current_task.name
                planned_order.append(task_name)
                
                console.print(f"  {i+1}. [cyan]{task_name}[/cyan]")
                console.print(f"     理由：{reasoning}\n")
                
                # 标记为已计划（不真正执行）
                self.agent.current_task = None
        
        # 保存计划
        plan = {
            'date': self.today.isoformat(),
            'tasks': [{**t, 'deadline': t.get('deadline').isoformat() if t.get('deadline') else None} for t in tasks],
            'planned_order': planned_order,
            'created_at': datetime.now().isoformat()
        }
        
        plan_file = self.workspace / f"plan_{self.today}.json"
        import json
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        console.print(f"\n[green]✓ 计划已保存到 {plan_file}[/green]\n")
        
        return planned_order
    
    def evening_report(self, completed_tasks: list = None) -> str:
        """
        晚间报告：生成今日执行总结
        
        Args:
            completed_tasks: 完成的任务列表
        """
        console.print(
            Panel.fit(
                f"[bold blue]晚间报告 - {self.today}[/bold blue]",
                title="🌙 Evening Report",
                border_style="blue"
            )
        )
        
        if not self.agent:
            # 尝试加载
            try:
                self.agent = IndependentAgent(db_path=f"daily_{self.today}.db")
            except:
                console.print("[yellow]未找到今日数据[/yellow]")
                return ""
        
        # 获取统计
        stats = self.agent.get_status()
        
        # 生成报告
        report_lines = [
            f"# 日报 - {self.today}",
            "",
            "## 📊 执行总结",
            "",
            f"- **完成任务**: {stats['tasks_completed']}",
            f"- **总奖励**: {stats['total_reward']:.2f}",
            f"- **决策次数**: {stats['decision_stats']['total_decisions']}",
            f"- **学习更新**: {stats['learning_stats']['total_updates']}次",
            "",
            "## 🤔 AI 反思",
            "",
            self.agent.get_reflection(),
            "",
            "## 📈 学习状态",
            "",
            f"- Q 表大小：{stats['learning_stats']['q_table_size']}",
            f"- 平均奖励：{stats['learning_stats']['avg_reward']:.3f}",
            f"- 探索率：{stats['learning_stats']['exploration_rate']:.0%}",
            "",
        ]
        
        # 添加完成的任务详情
        if completed_tasks:
            report_lines.extend([
                "## ✅ 完成的任务",
                "",
            ])
            
            for i, task in enumerate(completed_tasks, 1):
                report_lines.append(f"{i}. {task}")
            
            report_lines.append("")
        
        # 添加建议
        report_lines.extend([
            "## 💡 明日建议",
            "",
        ])
        
        if stats['tasks_completed'] < 3:
            report_lines.append("- 今天完成的任务较少，明天可以减少任务数量或提高时间估算")
        elif stats['tasks_completed'] >= 7:
            report_lines.append("- 今天效率很高！可以继续保持这个节奏")
        
        if stats['total_reward'] > 5:
            report_lines.append("- AI 调度表现良好，建议继续使用当前配置")
        
        report_lines.extend([
            "",
            "---",
            f"*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ])
        
        # 保存报告
        report_content = "\n".join(report_lines)
        report_file = self.workspace / f"report_{self.today}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # 显示报告
        console.print("\n[bold]生成报告:[/bold]\n")
        console.print(Panel(report_content, border_style="green"))
        
        console.print(f"\n[green]✓ 报告已保存到 {report_file}[/green]\n")
        
        return report_content
    
    def run_full_day_simulation(self, tasks: list):
        """
        运行完整的一天模拟
        
        早间计划 → 执行 → 晚间报告
        """
        # 早间计划
        planned_order = self.morning_planning(tasks)
        
        # 模拟执行
        console.print("\n[bold]模拟执行...[/bold]\n")
        
        completed = []
        
        for task_name in planned_order:
            result = self.agent.run_cycle()
            
            if '完成' in result:
                completed.append(task_name)
            
            console.print(f"  ✓ {task_name}")
        
        # 晚间报告
        self.evening_report(completed)
        
        self.agent.close()


def demo_daily_workflow():
    """演示每日工作流"""
    
    from datetime import timedelta
    
    workflow = DailyWorkflow()
    
    # 今日任务
    today_tasks = [
        {
            'name': '修复 ComfyUI 显存溢出',
            'priority': 10,
            'estimated_time': 60,
            'deadline': datetime.now() + timedelta(hours=2)
        },
        {
            'name': '调试视频生成 pipeline',
            'priority': 9,
            'estimated_time': 120,
            'deadline': datetime.now() + timedelta(hours=5)
        },
        {
            'name': '优化提示词工程',
            'priority': 7,
            'estimated_time': 90
        },
        {
            'name': '写技术文档',
            'priority': 6,
            'estimated_time': 90
        },
        {
            'name': '回复合作者邮件',
            'priority': 5,
            'estimated_time': 30
        },
    ]
    
    workflow.run_full_day_simulation(today_tasks)


if __name__ == "__main__":
    demo_daily_workflow()
