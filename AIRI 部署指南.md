# 🚀 AIRI 快速部署指南

**目标：** 在本地部署 AIRI，测试与小七的整合

**创建时间：** 2026-03-31

---

## 📋 前提条件

### 系统要求

- **操作系统：** Windows 10+/macOS 10.15+/Linux
- **内存：** 至少 8GB（推荐 16GB）
- **存储：** 至少 5GB 可用空间
- **Node.js：** v18+（推荐 v20）
- **Python：** v3.10+（小七 API 需要）

### 必需软件

```bash
# Node.js 和 pnpm
curl -fsSL https://nodejs.org | sudo -E bash -
npm install -g pnpm

# Python 依赖（小七 API）
pip install fastapi uvicorn pydantic requests
```

---

## 🎯 部署步骤

### 步骤 1: 克隆 AIRI 项目

```bash
cd /tmp
git clone https://github.com/moeru-ai/airi.git
cd airi
```

**注意：** 如果克隆慢，可以用镜像：

```bash
git clone https://ghp.ci/github.com/moeru-ai/airi.git
```

---

### 步骤 2: 安装依赖

```bash
# 安装 Node.js 依赖
pnpm install

# 如果使用国内网络，配置镜像
pnpm config set registry https://registry.npmmirror.com
pnpm install
```

---

### 步骤 3: 配置环境变量

```bash
# 复制环境配置示例
cp .env.example .env

# 编辑 .env 文件
nano .env
```

**配置示例：**

```env
# LLM 配置（可以先不配置，后面用小七替换）
# OPENAI_API_KEY=sk-xxx
# ANTHROPIC_API_KEY=sk-ant-xxx

# 或者使用本地模型
# OLLAMA_URL=http://localhost:11434

# 小七 API 配置（后续整合用）
XIAOQI_API_URL=http://localhost:8765
```

---

### 步骤 4: 启动开发服务器

```bash
# 开发模式
pnpm dev

# 或者生产模式
pnpm build
pnpm start
```

**访问：** http://localhost:3000

---

### 步骤 5: 启动小七 API（并行运行）

```bash
# 新开一个终端
cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
./start_server.sh
```

**小七 API：** http://localhost:8765

---

## 🧪 测试整合

### 测试 1: 基本聊天

```bash
# 测试小七 API
curl -X POST http://localhost:8765/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好！"}'
```

**预期响应：**

```json
{
  "response": "你好呀！很高兴见到你！",
  "emotion": {
    "mood": "开心",
    "energy": 0.9
  }
}
```

---

### 测试 2: 情感同步

```bash
# 获取小七状态
curl http://localhost:8765/api/status
```

**预期响应：**

```json
{
  "name": "小七",
  "memory_count": 10,
  "personality": {
    "mood": "好奇",
    "energy": 0.95,
    "curiosity": 0.95,
    "friendliness": 0.95
  }
}
```

---

### 测试 3: 主动学习

```bash
# 让小七学习
curl -X POST http://localhost:8765/api/learn \
  -H "Content-Type: application/json" \
  -d '{"topic": "量子力学"}'

# 然后问相关问题
curl -X POST http://localhost:8765/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "量子力学是什么？"}'
```

---

## 🔌 整合实现

### 创建 XiaoQiProvider

在 AIRI 项目中创建文件：

```typescript
// airi/src/services/llm/xiaoqi.ts

import type { LLMProvider, ChatMessage, ChatResponse } from './types'

export class XiaoQiProvider implements LLMProvider {
  name = 'xiaoqi'
  displayName = '小七 (indie-ai)'
  
  private baseUrl = 'http://localhost:8765'
  
  async chat(messages: ChatMessage[], context?: any): Promise<ChatResponse> {
    const lastMessage = messages[messages.length - 1]
    
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: lastMessage.content,
        context: {
          history: messages.slice(0, -1),
          emotion: context?.emotion
        }
      })
    })
    
    const data = await response.json()
    
    return {
      text: data.response,
      emotion: data.emotion,
      metadata: data.metadata
    }
  }
  
  async *chatStream(messages: ChatMessage[], context?: any): AsyncGenerator<string> {
    // 流式响应（后续实现）
    const response = await this.chat(messages, context)
    yield response.text
  }
}
```

---

### 注册提供商

```typescript
// airi/src/services/llm/index.ts

import { XiaoQiProvider } from './xiaoqi'

export const providers = {
  openai: new OpenAIProvider(),
  claude: new ClaudeProvider(),
  gemini: new GeminiProvider(),
  xiaoqi: new XiaoQiProvider(),  // 新增
}

export function getProvider(name: string) {
  return providers[name as keyof typeof providers]
}
```

---

### 添加配置选项

```typescript
// airi/src/config/llm.ts

export const llmProviders = [
  { id: 'openai', name: 'OpenAI' },
  { id: 'claude', name: 'Claude' },
  { id: 'gemini', name: 'Gemini' },
  { id: 'xiaoqi', name: '小七 (indie-ai)' },  // 新增
]
```

---

## 🎭 情感同步实现

### 创建 Hook

```typescript
// airi/src/hooks/useXiaoQiEmotion.ts

import { useState, useEffect } from 'react'

interface Emotion {
  mood: string
  energy: number
  curiosity: number
  friendliness: number
}

export function useXiaoQiEmotion() {
  const [emotion, setEmotion] = useState<Emotion | null>(null)
  
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8765/api/ws')
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'emotion_update') {
        setEmotion(data.emotion)
      }
    }
    
    ws.onclose = () => {
      // 重连
      setTimeout(() => useXiaoQiEmotion(), 3000)
    }
    
    return () => ws.close()
  }, [])
  
  return emotion
}
```

---

### Live2D 参数映射

```typescript
// airi/src/components/Live2D/xiaoqi-params.ts

import type { Emotion } from '../../hooks/useXiaoQiEmotion'

export function mapEmotionToLive2DParams(emotion: Emotion): Record<string, number> {
  const params: Record<string, number> = {}
  
  // 眉毛形状
  switch (emotion.mood) {
    case '开心':
      params.ParamEyeBrowForm = 0.8
      break
    case '平静':
      params.ParamEyeBrowForm = 0.5
      break
    case '好奇':
      params.ParamEyeBrowForm = 0.6
      break
    case '困惑':
      params.ParamEyeBrowForm = 0.3
      break
    default:
      params.ParamEyeBrowForm = 0.5
  }
  
  // 脸红
  params.ParamCheek = emotion.mood === '害羞' ? 0.5 : 0.0
  
  // 眼睛大小（受精力影响）
  params.ParamEyeLOpen = 0.7 + (emotion.energy * 0.3)
  params.ParamEyeROpen = 0.7 + (emotion.energy * 0.3)
  
  return params
}
```

---

### 在组件中使用

```typescript
// airi/src/components/Live2D/model.tsx

import { useXiaoQiEmotion } from '../../hooks/useXiaoQiEmotion'
import { mapEmotionToLive2DParams } from './xiaoqi-params'

export function Live2DModel() {
  const emotion = useXiaoQiEmotion()
  const model = useLive2DModel()
  
  useEffect(() => {
    if (emotion && model) {
      const params = mapEmotionToLive2DParams(emotion)
      model.setParams(params)
    }
  }, [emotion, model])
  
  return <canvas ref={canvasRef} />
}
```

---

## 🛠️ 故障排除

### 问题 1: pnpm install 失败

```bash
# 清理缓存
pnpm store prune

# 使用国内镜像
pnpm config set registry https://registry.npmmirror.com

# 重新安装
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

---

### 问题 2: 端口冲突

```bash
# AIRI 默认端口 3000
lsof -ti:3000 | xargs kill -9

# 小七 API 端口 8765
lsof -ti:8765 | xargs kill -9
```

---

### 问题 3: WebSocket 连接失败

检查小七 API 是否启动：

```bash
curl http://localhost:8765/api/status
```

如果失败，重启小七 API：

```bash
cd /home/fenghuang/.copaw/workspaces/default/independent-ai-mvp
./start_server.sh
```

---

### 问题 4: CORS 错误

在小七 API 中已配置 CORS，如果还有问题，检查：

```python
# indie_ai_server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境可以，生产环境要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 性能优化

### 降低延迟

```python
# 小七 API 优化
# 1. 使用更快的序列化工具
pip install orjson

# 2. 启用 HTTP/2
uvicorn indie_ai_server:app --http h2

# 3. 使用 WebSocket 代替轮询
# 已实现
```

### 减少内存占用

```typescript
// AIRI 优化
// 1. 按需加载 Live2D 模型
const Model = lazy(() => import('./Live2D/model'))

// 2. 使用 React.memo 避免不必要的重渲染
export const Live2DModel = memo(function Live2DModel() {
  // ...
})
```

---

## 📖 参考资源

- [AIRI 官网](https://airi.moeru.ai)
- [AIRI GitHub](https://github.com/moeru-ai/airi)
- [小七 API 文档](http://localhost:8765/docs)
- [整合计划](docs/indie-ai_×_AIRI_整合计划.md)
- [AIRI 分析报告](docs/AIRI 项目深度分析报告.md)

---

## 🎯 下一步

1. **完成 AIRI 部署**
   - 克隆项目
   - 安装依赖
   - 启动测试

2. **实现 XiaoQiProvider**
   - 创建提供商类
   - 注册到系统
   - 测试聊天

3. **实现情感同步**
   - WebSocket 连接
   - Live2D 参数映射
   - 测试表情

4. **创建演示**
   - 录制视频
   - 写文档
   - 分享社区

---

*最后更新：2026-03-31*  
*AIRI 快速部署指南 - 让小七有"身体"* 🚀✨
