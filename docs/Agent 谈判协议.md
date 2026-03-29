# 🤝 Agent 谈判协议

基于**合同网协议（Contract Net Protocol）**的多 Agent 协作系统

---

## 📋 概述

合同网协议是一种分布式任务分配协议，由 Smith 在 1980 年提出。Indie AI 实现了改进版本，支持：

- ✅ 任务招标（Task Announcement）
- ✅ 投标（Bid）
- ✅ 中标（Award）
- ✅ 协商（Negotiation）
- ✅ 多轮谈判

---

## 🏗️ 架构

```
┌─────────────────┐
│    Manager      │  ← 任务发布者
│  (管理者)        │
└────────┬────────┘
         │ 发布任务
         ▼
┌─────────────────┐
│  Announcement   │  ← 任务公告
└────────┬────────┘
         │ 广播
    ┌────┼────┐
    ▼    ▼    ▼
┌──────┐ ┌──────┐ ┌──────┐
│Agent │ │Agent │ │Agent │  ← 承包者
│  A   │ │  B   │ │  C   │
└──┬───┘ └──┬───┘ └──┬───┘
   │        │        │
   │ 投标    │ 投标    │ 投标
   ▼        ▼        ▼
┌─────────────────┐
│   Best Bid      │  ← 选择最优投标
└────────┬────────┘
         │ 中标通知
         ▼
┌─────────────────┐
│    Contract     │  ← 合同签订
└─────────────────┘
```

---

## 🎯 消息类型

| 类型 | 说明 | 方向 |
|------|------|------|
| `TASK_ANNOUNCE` | 任务公告 | Manager → Contractors |
| `BID` | 投标 | Contractor → Manager |
| `AWARD` | 中标通知 | Manager → Winner |
| `ACCEPT` | 接受 | Contractor → Manager |
| `REJECT` | 拒绝 | Contractor → Manager |
| `PROPOSE` | 提议 | Any → Any |
| `COUNTER_PROPOSE` | 反提议 | Any → Any |
| `AGREE` | 同意 | Any → Any |
| `REFUSE` | 拒绝 | Any → Any |

---

## 🧮 投标算法

```python
投标值 = 基础成本 × (1 - 能力匹配度 × 0.3) × 负载系数 × 优先级系数

其中:
- 基础成本 = 预计时间 (小时)
- 能力匹配度 = Σ(技能 proficiency) / 技能数量
- 负载系数 = 1.0 + 当前任务数 × 0.2
- 优先级系数 = 1.0 - (优先级 - 5) × 0.05
```

**投标值越低越容易中标**

---

## 💻 使用示例

### 基础任务分配

```python
from src.multi_agent.negotiation import ContractNetProtocol, NegotiationAgent
from src.core.models import Task

# 创建合同网
cnp = ContractNetProtocol()

# 创建管理者
manager = NegotiationAgent("Manager", AgentRole.MANAGER)
cnp.add_manager(manager)

# 创建承包者
contractor = NegotiationAgent("Worker", AgentRole.CONTRACTOR)
contractor.add_capability("coding", 0.9)
cnp.add_contractor(contractor)

# 创建任务
task = Task(
    id="T001",
    name="代码格式化",
    description="coding formatting",
    priority=8,
    estimated_time=30
)

# 运行谈判
contract = cnp.run_negotiation(task)
```

### AIGC 视频工作流

```python
# 创建角色
director = NegotiationAgent("Director", AgentRole.MANAGER)
script_writer = NegotiationAgent("ScriptWriter", AgentRole.CONTRACTOR)
storyboard = NegotiationAgent("StoryboardArtist", AgentRole.CONTRACTOR)
video_gen = NegotiationAgent("VideoGenerator", AgentRole.CONTRACTOR)

# 添加能力
script_writer.add_capability("writing", 0.95)
storyboard.add_capability("drawing", 0.9)
video_gen.add_capability("ai_video", 0.95)

# 任务序列
tasks = [
    Task("剧本创作", "writing creativity", priority=10),
    Task("分镜设计", "drawing composition", priority=9),
    Task("视频生成", "ai_video rendering", priority=8)
]

# 依次分配
for task in tasks:
    contract = cnp.run_negotiation(task)
```

---

## 📊 谈判流程

### 3 轮标准流程

```
第 1 轮：任务公告
  Manager → All Contractors: "谁来做这个任务？"

第 2 轮：投标
  Contractor A: "我！成本 1.5"
  Contractor B: "我！成本 1.2"
  Contractor C: "我！成本 1.8"

第 3 轮：中标
  Manager → Contractor B: "你来做！"
  Contractor B → Manager: "好的！"
```

### 多轮协商流程

```
Round 1:
  A → B: "帮我做 X，报酬 100"
  B → A: "太少，150" (反提议)

Round 2:
  A → B: "120 如何？" (新提议)
  B → A: "成交！" (同意)
```

---

## 🎭 Agent 角色

| 角色 | 说明 | 行为 |
|------|------|------|
| `MANAGER` | 管理者 | 发布任务、选择投标 |
| `CONTRACTOR` | 承包者 | 投标、执行任务 |
| `PEER` | 平等协商 | 提议、反提议 |

---

## 🔧 配置参数

### Agent 能力

```python
agent.add_capability("coding", 0.9)      # 编程能力
agent.add_capability("testing", 0.8)     # 测试能力
agent.add_capability("writing", 0.95)    # 写作能力
agent.add_capability("design", 0.85)     # 设计能力
agent.add_capability("ai_video", 0.9)    # AI 视频生成
```

### 任务属性

```python
task = Task(
    id="T001",
    name="任务名称",
    description="技能要求1 技能要求 2",
    priority=8,              # 1-10
    estimated_time=60        # 分钟
)
```

---

## 📈 统计信息

```python
stats = cnp.get_statistics()
print(stats)
# {
#   'total_negotiations': 5,
#   'active_contracts': 3,
#   'manager': 'Manager-001',
#   'contractors': ['Agent-A', 'Agent-B'],
#   'total_messages': 15
# }
```

---

## 🧪 运行演示

```bash
# 基础演示
python3 src/multi_agent/negotiation.py

# 完整演示
python3 demo/Agent 谈判协议演示.py
```

---

## 🎯 应用场景

### 1. AIGC 视频生成

```
Director (管理者)
  ↓
┌──────────────────────────────────────┐
│ ScriptWriter → 剧本创作              │
│ StoryboardArtist → 分镜设计          │
│ VideoGenerator → 视频生成            │
│ Editor → 后期剪辑                    │
└──────────────────────────────────────┘
```

### 2. 代码开发

```
TechLead (管理者)
  ↓
┌──────────────────────────────────────┐
│ FrontendDev → 前端开发               │
│ BackendDev → 后端开发                │
│ Tester → 测试                        │
│ DevOps → 部署                        │
└──────────────────────────────────────┘
```

### 3. 文档编写

```
Editor (管理者)
  ↓
┌──────────────────────────────────────┐
│ Writer → 内容撰写                    │
│ Reviewer → 审核                      │
│ Translator → 翻译                    │
└──────────────────────────────────────┘
```

---

## 🔍 优势

| 特性 | 说明 |
|------|------|
| **分布式** | 无中心节点，Agent 自主决策 |
| **透明** | 所有消息可追溯 |
| **灵活** | 支持多种谈判策略 |
| **高效** | 自动选择最优承包者 |
| **可扩展** | 轻松添加新 Agent |

---

## 📚 参考资料

1. Smith, R. G. (1980). The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver.
2. Durfee, E. H., & Lesser, V. R. (1989). Negotiating Task Decomposition and Allocation Using Partial Global Planning.
3. Rosenschein, J. S., & Zlotkin, G. (1994). Rules of Encounter: Designing Conventions for Automated Negotiation among Computers.

---

*最后更新：2026-03-29*
