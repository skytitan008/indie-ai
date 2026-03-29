#!/bin/bash

# 独立 AI MVP 快速启动脚本

echo "╔════════════════════════════════════════════════════════╗"
echo "║     🚀 独立 AI MVP - 快速启动                         ║"
echo "║     不依赖大模型的独立思考系统                         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

echo "选择要运行的实验:"
echo ""
echo "  === P0 优先级 (已完成) ==="
echo "  1) 综合实验 (质量优先 + 学习曲线)"
echo "  2) 真实任务执行 ⭐"
echo "  3) 长期学习实验 (100 轮) ⭐"
echo "  4) SARSA 对比实验 ⭐"
echo ""
echo "  === P1 优先级 (新增) ==="
echo "  5) 多 Agent 协作演示 ⭐"
echo "  6) Web 可视化 ⭐"
echo ""
echo "  === P2 优先级 (新增) ==="
echo " 13) 实际应用集成 ⭐ NEW"
echo " 14) 新功能演示 ⭐ NEW"
echo ""
echo "  === P3 优先级 (新增) ==="
echo " 15) 实验对比工具 ⭐ NEW"
echo " 16) 自动参数调优 ⭐ NEW"
echo " 17) CLI 命令行工具 ⭐ NEW"
echo " 18) WebSocket 服务器 ⭐ NEW"
echo ""
echo "  === 已有实验 ==="
echo "  7) 学习曲线可视化"
echo "  8) 质量优先配置测试"
echo "  9) 参数对比实验"
echo " 10) 决策可视化"
echo " 11) AIGC 项目场景"
echo " 12) 查看实验报告"
echo "  0) 退出"
echo ""
read -p "请输入选项 (0-12): " choice

case $choice in
    1)
        echo ""
        echo "▶ 运行综合实验..."
        python3 "demo/综合实验.py"
        ;;
    2)
        echo ""
        echo "▶ 运行真实任务执行..."
        python3 "demo/真实任务执行.py"
        ;;
    3)
        echo ""
        echo "▶ 运行长期学习实验 (100 轮)..."
        python3 "demo/长期学习实验.py"
        ;;
    4)
        echo ""
        echo "▶ 运行 SARSA 对比实验..."
        python3 "demo/SARSA 对比实验.py"
        ;;
    5)
        echo ""
        echo "▶ 运行多 Agent 协作演示..."
        python3 "demo/多 Agent 协作演示.py"
        ;;
    6)
        echo ""
        echo "▶ 启动 Web 可视化服务器..."
        echo ""
        echo "访问地址：http://localhost:8000"
        echo "按 Ctrl+C 停止服务器"
        echo ""
        python3 "start_web.py"
        ;;
    7)
        echo ""
        echo "▶ 运行学习曲线可视化..."
        python3 "demo/学习曲线可视化.py"
        ;;
    8)
        echo ""
        echo "▶ 运行质量优先配置测试..."
        python3 "demo/质量优先配置测试.py"
        ;;
    9)
        echo ""
        echo "▶ 运行参数对比实验..."
        python3 "demo/参数对比实验.py"
        ;;
    9)
        echo ""
        echo "▶ 运行决策可视化..."
        python3 "demo/决策可视化.py"
        ;;
    10)
        echo ""
        echo "▶ 运行 AIGC 项目场景..."
        python3 "demo/AIGC 项目场景.py"
        ;;
    11)
        echo ""
        if [ -f "实验报告_第 2 天.md" ]; then
            cat "实验报告_第 2 天.md"
        else
            echo "实验报告不存在"
        fi
        ;;
    12)
        echo ""
        echo "▶ 查看 CLI 帮助..."
        python3 cli.py --help
        ;;
    13)
        echo ""
        echo "▶ 运行实际应用集成..."
        python3 "demo/实际应用集成演示.py"
        ;;
    14)
        echo ""
        echo "▶ 运行新功能演示..."
        python3 "demo/新功能演示.py"
        ;;
    15)
        echo ""
        echo "▶ 运行实验对比工具..."
        python3 "src/analysis/experiment_comparison.py"
        ;;
    16)
        echo ""
        echo "▶ 运行自动参数调优..."
        python3 "src/analysis/auto_tuner.py"
        ;;
    17)
        echo ""
        echo "▶ 启动 CLI status..."
        python3 cli.py status
        ;;
    18)
        echo ""
        echo "▶ 启动 WebSocket 服务器..."
        echo "按 Ctrl+C 停止"
        python3 -m src.websocket.server
        ;;
    0)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "✓ 实验完成！"
echo ""
