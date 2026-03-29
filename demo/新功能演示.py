#!/usr/bin/env python3
"""
新功能演示

展示：
1. CLI 命令行工具
2. 实验对比工具
3. WebSocket 实时推送
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
    
    print("可用命令:")
    print("  indie-ai run <实验名>     # 运行实验")
    print("  indie-ai status           # 查看状态")
    print("  indie-ai stats            # 查看统计")
    print("  indie-ai compare <类型>   # 对比实验")
    print("  indie-ai clean            # 清理数据")
    print("  indie-ai web              # 启动 Web 界面")
    print("  indie-ai desktop          # 启动桌面版")
    print("  indie-ai version          # 显示版本")
    print("\n示例:")
    print("  python3 cli.py status")
    print("  python3 cli.py run learning")
    print("  python3 cli.py compare learning --rounds 5")
    print()


def demo_experiment_comparison():
    """演示实验对比工具"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🆚 实验对比工具演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    from src.analysis.experiment_comparison import ExperimentComparator
    from src.core.models import Task, Priority
    
    comparator = ExperimentComparator(output_dir="experiments/demo")
    
    tasks = [
        Task(id="1", name="修复显存", description="修复 ComfyUI 显存溢出", priority=10, estimated_time=30),
        Task(id="2", name="调试 pipeline", description="调试视频生成 pipeline", priority=9, estimated_time=45),
        Task(id="3", name="优化推理", description="优化模型推理速度", priority=8, estimated_time=60),
        Task(id="4", name="测试模板", description="测试新提示词模板", priority=7, estimated_time=30),
    ]
    
    print("📊 运行学习率对比实验（简化版，3 轮）\n")
    
    results = comparator.compare_learning_rates(
        rates=[0.05, 0.1, 0.2],
        task_list=tasks,
        rounds=3
    )
    
    print("\n✅ 实验对比完成！")
    print(f"📁 结果已保存到 experiments/demo/ 目录")
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
    print("\n前端集成示例:")
    print("""
    const ws = new WebSocket('ws://localhost:8765');
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'data_update') {
            updateChart(data.key, data.value);
        }
    };
    """)
    print()


def demo_all():
    """演示所有新功能"""
    print("\n" + "="*60)
    print("     🎉 Indie AI 新功能演示")
    print("="*60)
    
    demo_cli()
    demo_experiment_comparison()
    demo_websocket()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         ✅ 所有新功能演示完成！                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("📚 下一步:")
    print("  1. 使用 CLI 运行完整实验")
    print("  2. 启动 WebSocket 服务器")
    print("  3. 打开 Web 界面查看实时数据")
    print("  4. 尝试不同的配置对比")
    print()


if __name__ == '__main__':
    demo_all()
