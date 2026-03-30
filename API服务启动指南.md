# 🚀 小七 API 服务快速启动指南

---

## 📋 前提条件

确保已安装以下依赖：

```bash
pip install fastapi uvicorn pydantic requests
```

---

## 🎯 启动方式

### 方式 1: 使用启动脚本（推荐）

```bash
cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
./start_server.sh
```

### 方式 2: 直接使用 uvicorn

```bash
cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
uvicorn indie_ai_server:app --host 0.0.0.0 --port 8765 --reload
```

### 方式 3: 后台运行

```bash
cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
nohup uvicorn indie_ai_server:app --host 0.0.0.0 --port 8765 > server.log 2>&1 &
```

---

## 📡 API 端点

服务启动后，可以访问以下端点：

### REST API

```
GET  /                 - 服务信息
POST /api/chat         - 聊天（自主思考 + 主动学习）
POST /api/learn        - 学习新知识
GET  /api/status       - 获取小七状态
GET  /api/memories     - 记忆列表
GET  /api/growth_log   - 成长日志
```

### WebSocket

```
WS   /api/ws           - 实时推送（思考过程/情感变化）
```

### API 文档

```
http://localhost:8765/docs       - Swagger UI
http://localhost:8765/redoc      - ReDoc
```

---

## 🧪 测试方法

### 方法 1: 使用测试客户端

```bash
python3 test_api_client.py
```

选择模式：
- 模式 1：自动测试（测试所有接口）
- 模式 2：交互聊天（实时对话）

### 方法 2: 使用 curl

```bash
# 测试根路径
curl http://localhost:8765/

# 测试聊天
curl -X POST http://localhost:8765/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好！"}'

# 测试学习
curl -X POST http://localhost:8765/api/learn \
  -H "Content-Type: application/json" \
  -d '{"topic": "量子力学"}'

# 测试状态
curl http://localhost:8765/api/status
```

### 方法 3: 使用浏览器

打开 `http://localhost:8765/docs`，可以看到交互式 API 文档。

---

## 📊 示例响应

### 聊天响应

```json
{
  "response": "我刚学习了这个知识，现在来回答你：\n\n基于我的记忆和理解...\n\n1. 量子力学是研究微观粒子运动规律的物理学分支。\n\n有什么想继续问的吗？",
  "emotion": {
    "mood": "好奇",
    "energy": 0.9,
    "curiosity": 0.95,
    "friendliness": 0.95,
    "proactive": true
  },
  "metadata": {
    "thought_process": "检索记忆 → 主动学习 → 回答",
    "memory_count": 5,
    "learned": true,
    "timestamp": "2026-03-31T02:30:45.123456"
  }
}
```

### 状态响应

```json
{
  "name": "小七",
  "memory_count": 10,
  "interaction_count": 25,
  "learned_count": 5,
  "knowledge_topics": 8,
  "personality": {
    "mood": "开心",
    "energy": 0.9,
    "curiosity": 0.95,
    "friendliness": 0.95,
    "proactive": true
  },
  "current_mood": "开心"
}
```

---

## 🔌 集成到 AIRI

### TypeScript 示例

```typescript
class XiaoQiService {
  private baseUrl = 'http://localhost:8765'
  
  async chat(message: string): Promise<ChatResponse> {
    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    })
    return await res.json()
  }
  
  async getEmotion(): Promise<EmotionState> {
    const res = await fetch(`${this.baseUrl}/api/status`)
    const data = await res.json()
    return data.personality
  }
}

// 使用
const xiaoqi = new XiaoQiService()
const response = await xiaoqi.chat('你好！')

// 更新 Live2D 表情
updateLive2DEmotion(response.emotion)
```

### Python 示例

```python
import requests

BASE_URL = 'http://localhost:8765'

def chat(message: str):
    response = requests.post(
        f'{BASE_URL}/api/chat',
        json={'message': message}
    )
    return response.json()

def get_status():
    response = requests.get(f'{BASE_URL}/api/status')
    return response.json()

# 使用
result = chat('量子力学是什么？')
print(result['response'])
print(result['emotion'])
```

---

## 🛠️ 故障排除

### 端口被占用

```bash
# 查找占用端口的进程
lsof -ti:8765

# 杀死进程
lsof -ti:8765 | xargs kill -9

# 重启服务
./start_server.sh
```

### 依赖缺失

```bash
pip install fastapi uvicorn pydantic requests
```

### 导入错误

确保在项目目录下运行：

```bash
cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
```

---

## 📖 更多信息

- [整合计划](docs/indie-ai_×_AIRI_整合计划.md)
- [小七成长日记](docs/小七成长日记_第 2 天凌晨.md)
- [API 源码](indie_ai_server.py)
- [测试客户端](test_api_client.py)

---

*最后更新：2026-03-31*  
*小七 API 服务 - 给 AIRI 提供灵魂核心* 🚀✨
