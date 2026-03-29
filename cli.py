#!/usr/bin/env python3
"""
Indie AI 命令行工具

使用方式:
    indie-ai run <实验名>     # 运行实验
    indie-ai status          # 查看状态
    indie-ai stats           # 查看统计
    indie-ai compare         # 对比实验
    indie-ai clean           # 清理数据
    indie-ai web             # 启动 Web 界面
    indie-ai desktop         # 启动桌面版
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def cmd_run(args):
    """运行实验"""
    experiment_map = {
        'decision': 'demo/决策引擎演示.py',
        'learning': 'demo/学习曲线实验.py',
        'sarsa': 'demo/SARSA 对比实验.py',
        'multi-agent': 'demo/多 Agent 协作演示.py',
        'task': 'demo/真实任务执行.py',
        'long-term': 'demo/长期学习实验.py',
        'integration': 'demo/实际应用集成演示.py',
    }
    
    if args.experiment not in experiment_map:
        print(f"❌ 未知实验：{args.experiment}")
        print(f"可用实验：{', '.join(experiment_map.keys())}")
        return 1
    
    script = experiment_map[args.experiment]
    script_path = PROJECT_ROOT / script
    
    if not script_path.exists():
        print(f"❌ 脚本不存在：{script_path}")
        return 1
    
    print(f"\n🚀 运行实验：{args.experiment}")
    print(f"📁 脚本：{script_path}\n")
    
    import subprocess
    result = subprocess.run([sys.executable, str(script_path)], cwd=PROJECT_ROOT)
    
    return result.returncode


def cmd_status(args):
    """查看状态"""
    from src.agent import IndependentAgent
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🤖 Indie AI 状态                               ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    agent = IndependentAgent()
    
    print(f"📊 Agent 状态:")
    print(f"   总任务完成：{agent.tasks_completed}")
    print(f"   总奖励：{agent.total_reward}")
    
    print(f"\n🧠 学习状态:")
    print(f"   Q 表大小：{len(agent.q_learner.q_table)}")
    print(f"   探索率 ε: {agent.q_learner.epsilon:.3f}")
    print(f"   学习率 α: {agent.q_learner.alpha:.3f}")
    print(f"   折扣因子 γ: {agent.q_learner.gamma:.3f}")
    
    print(f"\n⚙️  决策权重:")
    for key, value in agent.decision_engine.weights.items():
        print(f"   {key}: {value:.2f}")
    
    print()


def cmd_stats(args):
    """查看统计"""
    db_path = PROJECT_ROOT / "ai_memory.db"
    
    if not db_path.exists():
        print("❌ 数据库不存在，请先运行实验")
        return 1
    
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         📊 Indie AI 统计                               ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 实验运行统计
    try:
        cursor.execute("SELECT COUNT(*) FROM experiments")
        exp_count = cursor.fetchone()[0]
        print(f"📁 实验运行次数：{exp_count}")
    except:
        print("📁 实验运行次数：N/A")
    
    # 任务统计
    try:
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]
        print(f"📋 任务总数：{task_count}")
        
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'")
        completed = cursor.fetchone()[0]
        print(f"✅ 完成任务：{completed}")
        
        if task_count > 0:
            rate = completed / task_count * 100
            print(f"📈 完成率：{rate:.1f}%")
    except:
        print("📋 任务统计：N/A")
    
    # Q 表统计
    try:
        cursor.execute("SELECT COUNT(*) FROM q_table")
        q_count = cursor.fetchone()[0]
        print(f"🧠 Q 表条目：{q_count}")
    except:
        print("🧠 Q 表条目：N/A")
    
    conn.close()
    print()


def cmd_compare(args):
    """对比实验"""
    from src.analysis.experiment_comparison import ExperimentComparator, create_sample_tasks
    
    print("\n🆚 启动实验对比工具\n")
    
    comparator = ExperimentComparator()
    tasks = create_sample_tasks()
    
    if args.type == 'learning':
        comparator.compare_learning_rates(task_list=tasks, rounds=args.rounds)
    elif args.type == 'decision':
        comparator.compare_decision_weights(task_list=tasks, rounds=args.rounds)
    else:
        print("❌ 未知对比类型")
        print("可用类型：learning, decision")
        return 1
    
    return 0


def cmd_clean(args):
    """清理数据"""
    import shutil
    
    print("\n⚠️  清理数据\n")
    
    files_to_clean = [
        PROJECT_ROOT / "ai_memory.db",
        PROJECT_ROOT / "experiments",
        PROJECT_ROOT / "logs",
        PROJECT_ROOT / "reports",
    ]
    
    for path in files_to_clean:
        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"✅ 删除：{path}")
            else:
                shutil.rmtree(path)
                print(f"✅ 删除目录：{path}")
        else:
            print(f"⏭️  跳过：{path} (不存在)")
    
    print("\n✅ 清理完成\n")
    return 0


def cmd_web(args):
    """启动 Web 界面"""
    import http.server
    import socketserver
    import threading
    
    web_dir = PROJECT_ROOT / "web"
    
    if not web_dir.exists():
        print("❌ Web 目录不存在")
        return 1
    
    port = args.port or 8080
    
    print(f"\n🌐 启动 Web 服务器")
    print(f"📁 目录：{web_dir}")
    print(f"🔌 端口：{port}")
    print(f"🌍 访问：http://localhost:{port}\n")
    
    os.chdir(web_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏸️  Web 服务器已停止")
    
    return 0


def cmd_desktop(args):
    """启动桌面版"""
    desktop_dir = PROJECT_ROOT / "desktop"
    
    if not desktop_dir.exists():
        print("❌ 桌面版目录不存在")
        return 1
    
    print("\n🖥️  启动桌面版")
    print(f"📁 目录：{desktop_dir}")
    print("⚠️  请确保已安装依赖：npm install\n")
    
    import subprocess
    result = subprocess.run(["npm", "start"], cwd=desktop_dir)
    
    return result.returncode


def cmd_version(args):
    """显示版本"""
    version_file = PROJECT_ROOT / "VERSION"
    
    if version_file.exists():
        version = version_file.read_text().strip()
    else:
        version = "1.0.0-dev"
    
    print(f"\n🤖 Indie AI v{version}")
    print(f"📅 构建时间：{datetime.now().strftime('%Y-%m-%d')}")
    print(f"🐍 Python {sys.version.split()[0]}")
    print(f"📁 路径：{PROJECT_ROOT}\n")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='🤖 Indie AI 命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  indie-ai run decision      # 运行决策引擎演示
  indie-ai run learning      # 运行学习曲线实验
  indie-ai status            # 查看当前状态
  indie-ai stats             # 查看统计数据
  indie-ai compare learning  # 对比不同学习率
  indie-ai clean             # 清理实验数据
  indie-ai web               # 启动 Web 界面
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # run 命令
    run_parser = subparsers.add_parser('run', help='运行实验')
    run_parser.add_argument('experiment', help='实验名称')
    run_parser.set_defaults(func=cmd_run)
    
    # status 命令
    status_parser = subparsers.add_parser('status', help='查看状态')
    status_parser.set_defaults(func=cmd_status)
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='查看统计')
    stats_parser.set_defaults(func=cmd_stats)
    
    # compare 命令
    compare_parser = subparsers.add_parser('compare', help='对比实验')
    compare_parser.add_argument('type', choices=['learning', 'decision'], help='对比类型')
    compare_parser.add_argument('--rounds', type=int, default=5, help='运行轮数')
    compare_parser.set_defaults(func=cmd_compare)
    
    # clean 命令
    clean_parser = subparsers.add_parser('clean', help='清理数据')
    clean_parser.set_defaults(func=cmd_clean)
    
    # web 命令
    web_parser = subparsers.add_parser('web', help='启动 Web 界面')
    web_parser.add_argument('--port', type=int, default=8080, help='端口')
    web_parser.set_defaults(func=cmd_web)
    
    # desktop 命令
    desktop_parser = subparsers.add_parser('desktop', help='启动桌面版')
    desktop_parser.set_defaults(func=cmd_desktop)
    
    # version 命令
    version_parser = subparsers.add_parser('version', help='显示版本')
    version_parser.set_defaults(func=cmd_version)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == '__main__':
    import os
    sys.exit(main())
