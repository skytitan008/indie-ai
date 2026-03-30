#!/bin/bash
# 启动小七 API 服务

echo "╔════════════════════════════════════════════════════════╗"
echo "║         🚀 启动小七 AI 服务                            ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 检查端口是否被占用
if lsof -ti:8765 > /dev/null; then
    echo "⚠️  端口 8765 已被占用，正在停止旧服务..."
    lsof -ti:8765 | xargs kill -9 2>/dev/null
    sleep 1
    echo "✅ 旧服务已停止"
fi

# 启动服务
echo "🚀 启动小七 AI 服务..."
echo ""
echo "📡 API 端点:"
echo "   - GET  /            - 服务信息"
echo "   - POST /api/chat    - 聊天"
echo "   - POST /api/learn   - 学习"
echo "   - GET  /api/status  - 状态"
echo "   - GET  /api/memories - 记忆列表"
echo "   - GET  /api/growth_log - 成长日志"
echo "   - WS   /api/ws      - WebSocket 实时推送"
echo ""
echo "📖 API 文档：http://localhost:8765/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
uvicorn indie_ai_server:app --host 0.0.0.0 --port 8765 --reload
