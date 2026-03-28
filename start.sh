#!/bin/bash
# 快速启动脚本

echo "🚀 独立思考 AI MVP - 快速启动"
echo ""

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本：$python_version"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install -r requirements.txt

# 运行演示
echo ""
echo "🎬 运行演示..."
python3 demo/run_demo.py

echo ""
echo "✓ 完成！"
