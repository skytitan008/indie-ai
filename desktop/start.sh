#!/bin/bash

# Indie AI Desktop 快速启动脚本

echo "╔════════════════════════════════════════════════════════╗"
echo "║     🖥️  Indie AI Desktop - 快速启动                   ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未检测到 Node.js，请先安装 Node.js 16+"
    echo "   访问：https://nodejs.org/"
    exit 1
fi

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未检测到 npm"
    exit 1
fi

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "📦 首次运行，安装依赖..."
    npm install
    echo ""
fi

echo "🚀 启动 Indie AI Desktop..."
echo ""
npm start
