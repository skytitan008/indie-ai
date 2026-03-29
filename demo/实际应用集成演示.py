#!/usr/bin/env python3
"""
实际应用集成演示

展示如何使用集成模块：
- 代码格式化
- 测试运行
- 日报生成
- Git Hooks 安装
"""

from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.integration.formatter import CodeFormatter
from src.integration.test_runner import TestRunner
from src.integration.daily_report import DailyReportGenerator
from src.integration.git_hooks import GitHooks


def demo_code_formatter():
    """演示代码格式化"""
    print("\n" + "="*60)
    print("📝 演示：代码格式化")
    print("="*60 + "\n")
    
    formatter = CodeFormatter()
    
    # 格式化当前目录的 Python 文件
    print("正在格式化 src/integration/ 目录...")
    stats = formatter.format_directory('src/integration', extensions=['.py'])
    
    print(formatter.get_report())
    print(f"\n统计：{stats['formatted']}/{stats['total']} 个文件已格式化")


def demo_test_runner():
    """演示测试运行"""
    print("\n" + "="*60)
    print("🧪 演示：测试运行")
    print("="*60 + "\n")
    
    runner = TestRunner({
        'framework': 'pytest',
        'test_dir': 'tests',
        'verbose': True
    })
    
    # 运行测试（如果 tests 目录存在）
    if Path('tests').exists():
        print("正在运行测试...")
        results = runner.run_tests()
        print(runner.get_report())
    else:
        print("⚠️  tests 目录不存在，跳过测试运行")
        print("💡 创建 tests/ 目录并添加测试文件后重试")


def demo_daily_report():
    """演示日报生成"""
    print("\n" + "="*60)
    print("📋 演示：日报生成")
    print("="*60 + "\n")
    
    generator = DailyReportGenerator()
    
    print("正在生成今日日报...")
    report = generator.generate()
    print(report)
    
    # 保存到文件
    output_file = generator.save_report()
    print(f"\n✅ 日报已保存到：{output_file}")


def demo_git_hooks():
    """演示 Git Hooks 安装"""
    print("\n" + "="*60)
    print("🔧 演示：Git Hooks 安装")
    print("="*60 + "\n")
    
    hooks = GitHooks()
    
    # 显示当前状态
    print("当前 Git Hooks 状态:")
    hooks.status()
    
    # 询问是否安装
    print("\n是否安装 Git Hooks？")
    print("  y - 安装")
    print("  n - 跳过")
    print("  u - 卸载现有钩子")
    
    choice = input("\n请选择 (y/n/u): ").strip().lower()
    
    if choice == 'y':
        print("\n正在安装 Git Hooks...")
        hooks.install(['pre-commit', 'post-commit', 'pre-push'])
        print("\n✅ Git Hooks 安装完成！")
        print("\n现在，当你执行以下 Git 操作时会自动触发钩子:")
        print("  • git commit - 触发 pre-commit（格式化和测试）")
        print("  • git commit - 触发 post-commit（记录提交）")
        print("  • git push - 触发 pre-push（推送前检查）")
    
    elif choice == 'u':
        print("\n正在卸载 Git Hooks...")
        hooks.uninstall()
        print("\n✅ Git Hooks 已卸载")


def demo_all():
    """运行所有演示"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║     🚀 实际应用集成演示                                  ║")
    print("║     indie-ai - 不依赖大模型的独立思考 AI                ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    demo_code_formatter()
    demo_test_runner()
    demo_daily_report()
    demo_git_hooks()
    
    print("\n" + "="*60)
    print("✅ 所有演示完成！")
    print("="*60 + "\n")
    
    print("📚 更多信息请查看文档:")
    print("  • docs/集成使用指南.md")
    print("  • src/integration/README.md")
    print("\n💡 提示:")
    print("  • 代码格式化：python -m src.integration.formatter <路径>")
    print("  • 运行测试：python -m src.integration.test_runner <路径>")
    print("  • 生成日报：python -m src.integration.daily_report")
    print("  • Git Hooks: python -m src.integration.git_hooks install")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'format':
            demo_code_formatter()
        elif sys.argv[1] == 'test':
            demo_test_runner()
        elif sys.argv[1] == 'report':
            demo_daily_report()
        elif sys.argv[1] == 'hooks':
            demo_git_hooks()
        else:
            demo_all()
    else:
        demo_all()
