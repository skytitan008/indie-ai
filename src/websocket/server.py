#!/usr/bin/env python3
"""
WebSocket 实时推送服务器

提供：
- 实验进度实时推送
- 学习曲线实时更新
- 多客户端支持
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Set, Dict, Any
import websockets
from websockets.server import WebSocketServerProtocol


class WebSocketServer:
    """WebSocket 服务器"""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.running = False
        self.data_buffer: Dict[str, Any] = {}
    
    async def register(self, websocket: WebSocketServerProtocol):
        """注册客户端"""
        self.clients.add(websocket)
        print(f"📱 新客户端连接，当前连接数：{len(self.clients)}")
        
        # 发送欢迎消息
        await self.send_to_client(websocket, {
            'type': 'welcome',
            'message': '已连接到 Indie AI WebSocket 服务器',
            'timestamp': datetime.now().isoformat()
        })
        
        # 发送当前数据
        if self.data_buffer:
            await self.send_to_client(websocket, {
                'type': 'initial_data',
                'data': self.data_buffer
            })
    
    async def unregister(self, websocket: WebSocketServerProtocol):
        """注销客户端"""
        self.clients.discard(websocket)
        print(f"📴 客户端断开连接，当前连接数：{len(self.clients)}")
    
    async def broadcast(self, data: Dict[str, Any]):
        """广播数据给所有客户端"""
        if not self.clients:
            return
        
        message = json.dumps(data, ensure_ascii=False)
        
        # 异步发送给所有客户端
        await asyncio.gather(
            *[self.send_to_client(client, data) for client in self.clients],
            return_exceptions=True
        )
    
    async def send_to_client(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """发送数据给单个客户端"""
        try:
            message = json.dumps(data, ensure_ascii=False)
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"❌ 发送失败：{e}")
    
    async def handle_client(self, websocket: WebSocketServerProtocol):
        """处理客户端连接"""
        await self.register(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """处理客户端消息"""
        try:
            data = json.loads(message)
            msg_type = data.get('type', '')
            
            if msg_type == 'subscribe':
                # 订阅特定数据
                channel = data.get('channel', 'all')
                await self.send_to_client(websocket, {
                    'type': 'subscribed',
                    'channel': channel
                })
            
            elif msg_type == 'request_data':
                # 请求数据
                key = data.get('key')
                if key and key in self.data_buffer:
                    await self.send_to_client(websocket, {
                        'type': 'data',
                        'key': key,
                        'value': self.data_buffer[key]
                    })
            
            elif msg_type == 'ping':
                # 心跳
                await self.send_to_client(websocket, {
                    'type': 'pong',
                    'timestamp': datetime.now().isoformat()
                })
            
        except json.JSONDecodeError:
            await self.send_to_client(websocket, {
                'type': 'error',
                'message': '无效的 JSON 格式'
            })
    
    def update_data(self, key: str, value: Any, broadcast: bool = True):
        """更新数据"""
        self.data_buffer[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        
        if broadcast:
            asyncio.create_task(self.broadcast({
                'type': 'data_update',
                'key': key,
                'value': value,
                'timestamp': self.data_buffer[key]['timestamp']
            }))
    
    async def start(self):
        """启动服务器"""
        self.running = True
        
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        print(f"\n╔════════════════════════════════════════════════════════╗")
        print(f"║     🌐 WebSocket 服务器已启动                          ║")
        print(f"╠════════════════════════════════════════════════════════╣")
        print(f"║  地址：ws://{self.host}:{self.port}                    ║")
        print(f"║  状态：运行中                                          ║")
        print(f"║  按 Ctrl+C 停止                                        ║")
        print(f"╚════════════════════════════════════════════════════════╝\n")
        
        await server.wait_closed()
    
    def stop(self):
        """停止服务器"""
        self.running = False
        print("\n⏸️  WebSocket 服务器已停止")


# 全局服务器实例
_server: WebSocketServer = None


def get_server() -> WebSocketServer:
    """获取服务器实例"""
    global _server
    if _server is None:
        _server = WebSocketServer()
    return _server


def update_experiment_data(script: str, status: str, output: str = None):
    """更新实验数据"""
    server = get_server()
    server.update_data('experiment', {
        'script': script,
        'status': status,
        'output': output,
        'timestamp': datetime.now().isoformat()
    })


def update_learning_curve(data: Dict):
    """更新学习曲线数据"""
    server = get_server()
    server.update_data('learning_curve', data)


def update_stats(stats: Dict):
    """更新统计数据"""
    server = get_server()
    server.update_data('stats', stats)


async def run_server(host: str = "localhost", port: int = 8765):
    """运行 WebSocket 服务器"""
    server = WebSocketServer(host, port)
    await server.start()


if __name__ == '__main__':
    import sys
    
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    
    asyncio.run(run_server(host, port))
