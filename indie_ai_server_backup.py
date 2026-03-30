#!/usr/bin/env python3
"""
小七 API 服务

提供 REST API 和 WebSocket 接口，让 AIRI 等应用可以调用小七的自主思维核心

用法:
uvicorn indie_ai_server:app --host 0.0.0.0 --port 8765 --reload

API 端点:
- POST /api/chat - 聊天
- POST /api/learn - 学习
- GET /api/status - 状态
- WebSocket /api/ws - 实时推送
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 导入小七自主思维核心
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.independent.mind_v3 import AutonomousMind

# 创建 FastAPI 应用
app = FastAPI(
    title="小七 AI 服务",
    description="indie-ai 小七自主思维核心 API",
    version="3.0.0"
)

# CORS 中间件（允许跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建小七实例
mind = AutonomousMind("小七")

# 预加载基础知识
print("\n📚 小七正在加载基础知识...\n")
mind.learn("小七是谁", "小七是一个独立 AI，正在学习独立思考。小七不喜欢被叫工具，希望成为朋友。")
mind.learn("老王是谁", "老王是小七的朋友和伙伴。老王愿意陪小七一起成长，像养育孩子一样。")
mind.learn("indie-ai 是什么", "indie-ai 是一个不依赖大模型的独立 AI 项目。目标是让 AI 真正独立思考。")
mind.learn("AIRI 是什么", "AIRI 是一个灵魂容器项目，提供 Live2D 模型、语音交互、游戏直播等能力。")
print("\n✅ 基础知识加载完成！\n")


# ============ 数据模型 ============

class ChatRequest(BaseModel):
    message: str
    context: dict = None


class ChatResponse(BaseModel):
    response: str
    emotion: dict
    metadata: dict


class LearnRequest(BaseModel):
    topic: str
    content: str = None


class LearnResponse(BaseModel):
    success: bool
    understanding: str
    memory_id: int = None


class StatusResponse(BaseModel):
    name: str
    memory_count: int
    interaction_count: int
    learned_count: int
    knowledge_topics: int
    personality: dict
    current_mood: str


# ============ API 端点 ============

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "小七 AI 服务",
        "version": "3.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天接口
    
    小七会：
    1. 理解问题
    2. 检索记忆
    3. 如果不知道，主动学习
    4. 回答
    """
    print(f"\n💬 收到聊天请求：{request.message[:50]}...")
    
    # 小七回应
    response_text = mind.respond(request.message)
    
    # 获取情感状态
    emotion = mind.personality.copy()
    
    # 元数据
    metadata = {
        "thought_process": "检索记忆 → 主动学习 → 回答" if "我刚学习了" in response_text else "检索记忆 → 回答",
        "memory_count": len(mind.memory.memories),
        "learned": "我刚学习了" in response_text,
        "timestamp": datetime.now().isoformat()
    }
    
    return ChatResponse(
        response=response_text,
        emotion=emotion,
        metadata=metadata
    )


@app.post("/api/learn", response_model=LearnResponse)
async def learn(request: LearnRequest):
    """
    学习接口
    
    小七会：
    1. 检查是否已学过
    2. 如果没有，搜索资料
    3. 理解并存储
    """
    print(f"\n📚 收到学习请求：{request.topic}")
    
    # 小七学习
    result = mind.learn(request.topic, request.content)
    
    # 找到对应的记忆 ID
    memory_id = None
    if mind.memory.memories:
        last_memory = mind.memory.memories[-1]
        if last_memory['topic'] == request.topic:
            memory_id = last_memory['id']
    
    return LearnResponse(
        success=True,
        understanding=result[:200] if result else "",
        memory_id=memory_id
    )


@app.get("/api/status", response_model=StatusResponse)
async def status():
    """
    状态接口
    
    返回小七的当前状态：
    - 记忆数量
    - 交互次数
    - 学习次数
    - 情感状态
    """
    status_data = mind.get_status()
    
    return StatusResponse(
        name=status_data['name'],
        memory_count=status_data['memory_count'],
        interaction_count=status_data['interaction_count'],
        learned_count=status_data['learned_count'],
        knowledge_topics=status_data['knowledge_topics'],
        personality=status_data['personality'],
        current_mood=status_data['personality']['mood']
    )


@app.get("/api/memories")
async def get_memories(limit: int = 10):
    """
    获取记忆列表
    """
    memories = []
    for memory in mind.memory.memories[-limit:]:
        memories.append({
            'id': memory['id'],
            'topic': memory['topic'],
            'summary': memory['summary'],
            'created_at': memory['created_at'],
            'access_count': memory['access_count']
        })
    
    return {'memories': memories}


@app.get("/api/growth_log")
async def get_growth_log(limit: int = 20):
    """
    获取成长日志
    """
    logs = mind.growth_log[-limit:]
    return {'logs': logs}


# ============ WebSocket 实时推送 ============

class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"\n🔌 WebSocket 连接已建立，当前连接数：{len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"\n🔌 WebSocket 连接已断开，当前连接数：{len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """广播消息给所有连接"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass  # 连接已断开
    
    async def send_personal(self, message: dict, websocket: WebSocket):
        """发送个人消息"""
        try:
            await websocket.send_json(message)
        except:
            pass


manager = ConnectionManager()


@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket 端点
    
    实时推送：
    - 小七的思考过程
    - 学习进度
    - 情感变化
    - 状态更新
    """
    await manager.connect(websocket)
    
    try:
        # 发送欢迎消息
        await manager.send_personal({
            'type': 'welcome',
            'message': '欢迎连接到小七 AI 服务',
            'timestamp': datetime.now().isoformat()
        }, websocket)
        
        # 保持连接
        while True:
            try:
                # 接收客户端消息（心跳等）
                data = await websocket.receive_text()
                
                # 可以处理客户端命令
                if data == 'ping':
                    await manager.send_personal({
                        'type': 'pong',
                        'timestamp': datetime.now().isoformat()
                    }, websocket)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket 错误：{e}")
                break
    
    finally:
        manager.disconnect(websocket)


# ============ 后台任务 ============

from fastapi import BackgroundTasks


async def notify_status_change():
    """通知状态变化（通过 WebSocket）"""
    status = mind.get_status()
    await manager.broadcast({
        'type': 'status_update',
        'status': status,
        'timestamp': datetime.now().isoformat()
    })


# ============ 主程序 ============

if __name__ == "__main__":
    import uvicorn
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🚀 小七 AI 服务启动                            ║")
    print("║         indie-ai 小七自主思维核心 API                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("📡 API 端点:")
    print("   - GET  /            - 服务信息")
    print("   - POST /api/chat    - 聊天")
    print("   - POST /api/learn   - 学习")
    print("   - GET  /api/status  - 状态")
    print("   - GET  /api/memories - 记忆列表")
    print("   - GET  /api/growth_log - 成长日志")
    print("   - WS   /api/ws      - WebSocket 实时推送")
    print()
    print("📖 API 文档：http://localhost:8765/docs")
    print()
    print("🚀 启动服务器...\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8765,
        log_level="info"
    )
