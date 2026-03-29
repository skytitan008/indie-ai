#!/usr/bin/env python3
"""
新功能快速演示

展示 CLI、实验对比、自动调优功能
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def demo_cli():
    """演示 CLI 工具"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         💻 CLI 命令行工具演示                          ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    import subprocess
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "cli.py"), "status"],
        capture_output=True,
        text=True
    )
    print(result.stdout)


def demo_simple_comparison():
    """简化版实验对比"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🆚 简化版实验对比                              ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    from src.agent import IndependentAgent
    
    configs = [
        {'name': 'LR=0.05', 'lr': 0.05},
        {'name': 'LR=0.1', 'lr': 0.1},
        {'name': 'LR=0.2', 'lr': 0.2},
    ]
    
    print(f"{'配置':<15} {'Q 表大小':<12} {'ε':<10}")
    print("-" * 40)
    
    for config in configs:
        agent = IndependentAgent()
        agent.q_learner.alpha = config['lr']
        
        # 简单运行几轮
        for _ in range(5):
            agent.run_cycle()
        
        q_size = len(agent.q_learner.q_table)
        epsilon = agent.q_learner.epsilon
        
        print(f"{config['name']:<15} {q_size:<12} {epsilon:<10.3f}")
    
    print()


def demo_auto_tuner():
    """演示自动调优"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🔍 自动参数调优演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("自动调优功能可寻找最优配置")
    print("\n使用方式:")
    print("  python3 src/analysis/auto_tuner.py")
    print("\n功能:")
    print("  - 网格搜索参数组合")
    print("  - 自动评估配置效果")
    print("  - 保存最佳配置")
    print()


def demo_websocket():
    """演示 WebSocket"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🌐 WebSocket 实时推送演示                      ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("WebSocket 服务器功能:")
    print("  - 实时推送实验进度")
    print("  - 实时更新学习曲线")
    print("  - 多客户端支持")
    print("\n启动方式:")
    print("  python3 -m src.websocket.server")
    print("\n连接地址:")
    print("  ws://localhost:8765")
    print()


def main():
    """主函数"""
    print("\n" + "="*60)
    print("     🎉 Indie AI 新功能演示 (简化版)")
    print("="*60)
    
    demo_cli()
    demo_simple_comparison()
    demo_auto_tuner()
    demo_websocket()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         ✅ 所有新功能演示完成！                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("📚 下一步:")
    print("  1. python3 cli.py run learning  - 运行学习实验")
    print("  2. python3 cli.py compare learning - 对比实验")
    print("  3. python3 -m src.websocket.server - 启动 WebSocket")
    print("  4. python3 cli.py web - 启动 Web 界面")
    print()


if __name__ == '__main__':
    main()
