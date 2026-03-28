"""
真实任务执行演示

让 AI 真正执行 Python 脚本和系统命令
- 代码格式化
- 运行测试
- 生成日报
- 清理临时文件
"""

import sys
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.executor import TaskExecutor, AIAgentWithExecution
from src.config import get_preset


console = Console()


def demo_code_format(executor: TaskExecutor):
    """演示代码格式化"""
    
    console.print(
        Panel.fit(
            "[bold blue]任务 1: 代码格式化[/bold blue]\n\n"
            "使用 black 格式化 Python 代码",
            title="📝 Code Formatting",
            border_style="blue"
        )
    )
    
    # 先创建一个需要格式化的测试文件
    test_file = Path("test_unformatted.py")
    test_content = """
# 未格式化的代码
import os,sys
from pathlib import Path

def hello(name ):
    if name:
        print( f"Hello, {name}!" )
    else:
        print( "Hello, World!" )

class Test:
    def __init__(self):
        self.value=42
"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    console.print(f"\n[yellow]✓ 创建测试文件：{test_file}[/yellow]")
    console.print("\n[bold]格式化前:[/bold]")
    console.print(test_content)
    
    # 执行格式化
    console.print("\n[bold]执行格式化...[/bold]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]格式化中...", total=None)
        
        result = executor.format_code(str(test_file))
        
        progress.update(task, completed=True)
    
    if result.success:
        console.print("\n[green]✓ 格式化成功！[/green]\n")
        
        # 读取格式化后的内容
        with open(test_file, 'r', encoding='utf-8') as f:
            formatted_content = f.read()
        
        console.print("[bold]格式化后:[/bold]")
        console.print(formatted_content)
        
        # 清理
        test_file.unlink()
        console.print("\n[green]✓ 测试文件已清理[/green]")
    else:
        console.print(f"\n[red]✗ 格式化失败：{result.error}[/red]")
        console.print("\n[yellow]提示：需要先安装 black: pip install black[/yellow]")
    
    return result.success


def demo_test_runner(executor: TaskExecutor):
    """演示测试运行"""
    
    console.print(
        Panel.fit(
            "[bold blue]任务 2: 运行测试[/bold blue]\n\n"
            "创建测试文件并运行 pytest",
            title="🧪 Test Runner",
            border_style="blue"
        )
    )
    
    # 创建测试目录和文件
    test_dir = Path("test_demo")
    test_dir.mkdir(exist_ok=True)
    
    # 创建被测试的模块
    module_file = test_dir / "calculator.py"
    module_content = """
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
"""
    
    with open(module_file, 'w', encoding='utf-8') as f:
        f.write(module_content)
    
    # 创建测试文件
    test_file = test_dir / "test_calculator.py"
    test_content = """
import pytest
from calculator import add, subtract, multiply

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0
"""
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    console.print(f"\n[yellow]✓ 创建测试文件：{test_file}[/yellow]")
    
    # 运行测试
    console.print("\n[bold]运行测试...[/bold]\n")
    
    result = executor.run_tests(str(test_dir))
    
    if result.success:
        console.print("\n[green]✓ 所有测试通过！[/green]\n")
    else:
        console.print("\n[red]✗ 测试失败[/red]\n")
    
    if result.output:
        console.print("[bold]测试输出:[/bold]")
        console.print(Panel(result.output[:1000], border_style="green" if result.success else "red"))
    
    # 清理
    import shutil
    shutil.rmtree(test_dir)
    console.print("\n[green]✓ 测试目录已清理[/green]")
    
    console.print("\n[yellow]提示：需要安装 pytest: pip install pytest[/yellow]")
    
    return result.success


def demo_daily_report(executor: TaskExecutor):
    """演示日报生成"""
    
    console.print(
        Panel.fit(
            "[bold blue]任务 3: 生成日报[/bold blue]\n\n"
            "自动生成今日工作总结",
            title="📋 Daily Report",
            border_style="blue"
        )
    )
    
    # 生成日报
    console.print("\n[bold]生成日报...[/bold]\n")
    
    result = executor.generate_report("demo_daily_report.md")
    
    if result.success:
        console.print("\n[green]✓ 日报生成成功！[/green]\n")
        
        # 读取并显示报告
        report_file = Path("demo_daily_report.md")
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        console.print(Panel(report_content, title="日报内容", border_style="green"))
        
        # 清理
        report_file.unlink()
        console.print("\n[green]✓ 报告文件已清理（实际使用会保留）[/green]")
    else:
        console.print(f"\n[red]✗ 生成失败：{result.error}[/red]")
    
    return result.success


def demo_ai_task_execution():
    """演示 AI 自主决定并执行任务"""
    
    console.print(
        Panel.fit(
            "[bold blue]任务 4: AI 自主执行[/bold blue]\n\n"
            "让 AI 决定执行哪个任务并真正运行",
            title="🤖 AI Autonomous Execution",
            border_style="blue"
        )
    )
    
    # 创建 Agent
    config = get_preset('quality')
    agent = IndependentAgent(db_path="demo_execution.db")
    
    # 应用配置
    agent.decision_engine.weights = {
        'urgency': config['decision'].urgency_weight,
        'importance': config['decision'].importance_weight,
        'efficiency': config['decision'].efficiency_weight,
        'dependency': config['decision'].dependency_weight,
    }
    
    # 创建执行器包装
    ai_executor = AIAgentWithExecution(agent, workspace=".")
    
    # 添加可执行的任务
    console.print("\n[bold]添加可执行任务...[/bold]\n")
    
    # 任务 1: 格式化代码
    ai_executor.map_task_to_script("格式化测试代码", "demo/格式化示例.py")
    
    # 任务 2: 运行测试
    ai_executor.map_task_to_script("运行单元测试", "demo/运行测试示例.py")
    
    # 任务 3: 生成日报
    ai_executor.map_task_to_script("生成今日日报", "demo/生成日报示例.py")
    
    console.print("  ✓ 格式化测试代码 → demo/格式化示例.py")
    console.print("  ✓ 运行单元测试 → demo/运行测试示例.py")
    console.print("  ✓ 生成今日日报 → demo/生成日报示例.py")
    
    # 让 AI 决定并执行
    console.print("\n[bold]AI 开始工作...[/bold]\n")
    
    for i in range(3):
        # AI 思考并选择任务
        reasoning = agent.think()
        
        if agent.current_task:
            task_name = agent.current_task.name
            console.print(f"\n[bold cyan]第 {i+1} 轮决策:[/bold cyan]")
            console.print(f"  选择任务：{task_name}")
            console.print(f"  决策理由：{reasoning}\n")
            
            # 执行任务
            result = ai_executor.execute_current_task()
            
            if result['success']:
                console.print(f"  [green]✓ 执行成功：{result['message']}[/green]")
            else:
                console.print(f"  [yellow]⚠ 执行失败：{result.get('error', '未知错误')}[/yellow]")
            
            # 给 AI 反馈
            if result['success']:
                agent.act(success=True)
            else:
                agent.act(success=False)
        else:
            console.print("[yellow]没有可执行的任务[/yellow]")
            break
    
    agent.close()
    
    console.print("\n[green]✓ AI 自主执行演示完成！[/green]\n")


def main():
    """主函数"""
    
    console.print("\n")
    console.print(
        Panel(
            "[bold]🚀 真实任务执行演示[/bold]\n\n"
            "让 AI 真正帮你干活！\n\n"
            "演示内容:\n"
            "  1. 代码格式化 (black)\n"
            "  2. 运行测试 (pytest)\n"
            "  3. 生成日报\n"
            "  4. AI 自主执行任务",
            title="🛠️ Real Task Execution Demo",
            border_style="blue"
        )
    )
    
    # 创建执行器
    executor = TaskExecutor(workspace=".")
    
    console.print("\n[bold]准备开始演示...[/bold]\n")
    console.print("[yellow]提示：以下演示会创建临时文件，完成后自动清理[/yellow]\n")
    
    # 演示 1: 代码格式化
    console.print("\n" + "="*60 + "\n")
    format_success = demo_code_format(executor)
    
    # 演示 2: 运行测试
    console.print("\n" + "="*60 + "\n")
    test_success = demo_test_runner(executor)
    
    # 演示 3: 生成日报
    console.print("\n" + "="*60 + "\n")
    report_success = demo_daily_report(executor)
    
    # 演示 4: AI 自主执行
    console.print("\n" + "="*60 + "\n")
    demo_ai_task_execution()
    
    # 总结
    console.print("\n" + "="*60 + "\n")
    
    summary_table = Table(title="演示总结")
    summary_table.add_column("任务", style="cyan")
    summary_table.add_column("状态", style="green")
    
    summary_table.add_row("代码格式化", "[green]✓ 成功[/green]" if format_success else "[yellow]⚠ 需安装 black[/yellow]")
    summary_table.add_row("运行测试", "[green]✓ 成功[/green]" if test_success else "[yellow]⚠ 需安装 pytest[/yellow]")
    summary_table.add_row("生成日报", "[green]✓ 成功[/green]" if report_success else "[red]✗ 失败[/red]")
    summary_table.add_row("AI 自主执行", "[green]✓ 完成[/green]")
    
    console.print(summary_table)
    
    console.print("\n[bold green]✓ 所有演示完成！[/bold green]\n")
    
    console.print(
        Panel(
            "[bold]下一步:[/bold]\n\n"
            "1. 安装依赖：pip install black pytest\n"
            "2. 修改 executor.py 添加更多任务类型\n"
            "3. 集成到你的实际工作流\n"
            "4. 让 AI 每天自动执行这些任务",
            title="💡 使用建议",
            border_style="green"
        )
    )


if __name__ == "__main__":
    main()
