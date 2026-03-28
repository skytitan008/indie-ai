# 🚀 独立 AI MVP

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stage: MVP](https://img.shields.io/badge/Stage-MVP-green.svg)]

**不依赖大模型的独立思考 AI 原型系统**

> 探索符号 AI + 强化学习的混合架构，实现自主决策、经验学习、自我监控能力

---

## 🌟 特性亮点

- 🤖 **自主决策** - 基于效用函数的透明决策机制
- 🧠 **经验学习** - Q-Learning + SARSA 双算法支持
- 👥 **多 Agent 协作** - 智能任务分配与团队协作
- 📊 **Web 可视化** - 浏览器实时查看学习曲线
- 💼 **真实任务执行** - 自动格式化代码、运行测试、生成日报
- 📈 **学习曲线分析** - 100 轮深度实验，观察 AI 成长

---

## 🎯 项目目标

本项目探索**不依赖大模型**的 AI 实现路径，通过符号 AI 与强化学习的结合，打造：

1. **透明可解释** - 每个决策都有明确理由
2. **轻量级** - 无需 GPU，普通电脑即可运行
3. **可定制** - 灵活的配置系统
4. **实用导向** - 真正帮助完成实际工作

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Linux / Windows / macOS
- 无需 GPU（可选加速）
- **桌面版**: Node.js 16+ (可选)

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/skytitan008/indie-ai.git
cd indie-ai

# 安装依赖
pip install -r requirements.txt

# 可选：安装额外工具
pip install black pytest  # 用于真实任务执行

# 可选：桌面版依赖
cd desktop
npm install
cd ..
```

### 运行演示

```bash
# 方式一：使用启动脚本（推荐）
./run.sh

# 方式二：直接运行 Python
python3 demo/综合实验.py

# 方式三：桌面版（跨平台 GUI）
cd desktop
./start.sh  # 或 npm start
```

### Web 可视化

```bash
# 启动 Web 服务器
python3 start_web.py

# 浏览器访问
http://localhost:8000
```

---

## 📁 项目结构

```
indie-ai/
├── src/                        # 核心源代码
│   ├── agent.py                # IndependentAgent 主类
│   ├── executor.py             # 真实任务执行器
│   ├── config.py               # 配置中心（5 种预设）
│   ├── decision.py             # 决策引擎
│   ├── learning/
│   │   ├── qlearner.py         # Q-Learning 算法
│   │   └── sarsa.py            # SARSA 算法
│   ├── memory/
│   │   └── database.py         # SQLite 记忆存储
│   ├── monitoring/
│   │   └── monitor.py          # 自我监控
│   └── multi_agent/
│       └── coordinator.py      # 多 Agent 协作
│
├── demo/                       # 演示脚本
│   ├── 综合实验.py              # 一键运行完整测试
│   ├── 真实任务执行.py          # AI 真正干活
│   ├── 长期学习实验.py          # 100 轮学习曲线
│   ├── SARSA 对比实验.py        # 算法对比
│   ├── 多 Agent 协作演示.py     # 团队协作
│   └── ...
│
├── web/                        # Web 可视化
│   ├── index.html              # 主页面
│   ├── app.js                  # 前端逻辑
│   └── ...
│
├── desktop/                    # 🆕 桌面版 (Electron)
│   ├── src/
│   │   ├── main.js             # Electron 主进程
│   │   ├── preload.js          # 预加载脚本
│   │   └── index.html          # 桌面界面
│   ├── assets/                 # 资源文件
│   ├── package.json            # Node.js 配置
│   └── README.md               # 桌面版文档
│
├── docs/                       # 文档
│   ├── 使用教程.md
│   ├── 开发文档.md
│   └── ...
│
├── run.sh                      # 快速启动脚本
├── start_web.py                # Web 服务器
├── requirements.txt            # Python 依赖
├── README.md                   # 本文件
└── LICENSE                     # MIT 许可证
```

---

## 🎮 核心功能演示

### 1. 综合实验

测试 AI 的基本能力：

```bash
python3 demo/综合实验.py
```

**输出示例**:
```
╭─ 🎨 Quality First Test ─╮
│ 质量优先配置测试        │
╰─────────────────────────╯

任务列表:
  1. 修复 ComfyUI 显存溢出 (P10, 02:12 截止)
  2. 调试视频生成 pipeline (P9, 05:12 截止)
  ...

执行结果:
  ✓ 完成任务：9/9
  ✓ 完成率：100%
  ✓ 总奖励：+9.0
```

### 2. 真实任务执行

让 AI 真正帮你干活：

```bash
python3 demo/真实任务执行.py
```

**功能**:
- ✅ 代码格式化（black）
- ✅ 运行测试（pytest）
- ✅ 生成日报
- ✅ AI 自主决定执行

### 3. 长期学习实验

观察 AI 学习的完整过程：

```bash
python3 demo/长期学习实验.py
```

**分析内容**:
- 100 轮连续运行
- Q 表收敛曲线
- 4 个学习阶段识别
- 学习率调整建议

### 4. 多 Agent 协作

看两个 AI 如何配合：

```bash
python3 demo/多 Agent 协作演示.py
```

**场景**:
- TechAgent（技术专家）：Python, Debugging
- CreativeAgent（创意专家）：Design, Script
- 智能任务分配
- 动态负载均衡

### 5. Web 可视化

浏览器查看学习曲线：

```bash
python3 start_web.py
# 访问 http://localhost:8000
```

**功能**:
- 📈 学习曲线图表
- 🧠 Q 表增长可视化
- ✅ 成功率柱状图
- 📊 实时数据统计
- 🌙 深色模式切换

### 6. 🆕 桌面版（Electron）

跨平台桌面应用：

```bash
cd desktop
./start.sh  # 或 npm start
```

**功能**:
- 🖥️ 独立窗口运行
- 🔔 系统托盘 + 通知
- ⚡ 一键运行实验
- 📊 实时统计面板
- 📝 实验日志导出
- 🌐 支持 Windows/macOS/Linux

**打包可执行文件**:
```bash
cd desktop
npm install
npm run build  # 或 npm run build:win
```

---

## ⚙️ 配置系统

### 5 种预设配置

| 配置名 | 紧急度 | 重要性 | 效率 | 适用场景 |
|--------|--------|--------|------|----------|
| `balanced` | 35% | 35% | 20% | 通用场景 |
| `urgent` | 50% | 25% | 15% | 紧急任务优先 |
| `quality` | 30% | 40% | 20% | **创意工作** ⭐ |
| `aggressive` | 25% | 30% | 35% | 快速执行 |
| `conservative` | 30% | 35% | 15% | 稳健执行 |

### 使用示例

```python
from src.agent import IndependentAgent
from src.config import get_preset

# 创建 Agent
agent = IndependentAgent()

# 应用质量优先配置
config = get_preset('quality')
agent.decision_engine.weights = {
    'urgency': config['decision'].urgency_weight,
    'importance': config['decision'].importance_weight,
    'efficiency': config['decision'].efficiency_weight,
    'dependency': config['decision'].dependency_weight,
}
```

---

## 📊 实验结果

### 第 2 天实验（2026-03-29）

**学习曲线实验**（10 轮）:
- 平均完成率：**98%** (8.8/9 任务)
- Q 表增长：**0 → 89**
- 学习更新：**1,888 次**
- 平均奖励：**+7.0 → +9.0**

### 第 3 天实验（2026-03-29）

**长期学习实验**（100 轮）:
- Q 表收敛：约第 60 轮开始稳定
- 学习阶段：初期→快速→稳定→成熟
- 最终成功率：**95%+**

**多 Agent 协作**:
- 2 个 Agent 协作完成 6 个任务
- 基于技能匹配的智能分配
- 信任度机制有效运行

---

## 🧠 技术架构

### 决策机制

**效用函数**:
```
Utility = 紧急度×35% + 重要性×35% + 效率×20% + 依赖性×10%
```

**质量优先配置**:
```
Utility = 紧急度×30% + 重要性×40% + 效率×20% + 依赖性×10%
```

### 学习算法

**Q-Learning** (Off-policy):
```python
Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
```

**SARSA** (On-policy):
```python
Q(s,a) ← Q(s,a) + α[r + γ·Q(s',a') - Q(s,a)]
```

### 多 Agent 协作

**任务分配评分**:
```
Score = 技能匹配×50% + 可用性×30% + 信任度×20%
```

---

## 📚 文档

- [使用教程](docs/使用教程.md) - 详细使用指南
- [开发文档](docs/开发文档.md) - 架构设计与扩展
- [实验报告](实验报告_第 2 天.md) - 详细实验数据
- [第 3 天成果](第 3 天完整成果.md) - 最新进展

---

## 🤝 贡献指南

欢迎贡献！请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/independent-ai-mvp.git
cd independent-ai-mvp

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 可选
```

### 提交代码

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **老王** (王军伟) - 项目发起人，AIGC 视频专家
- **小七** - 项目实现者
- 灵感来源：符号 AI、强化学习、多 Agent 系统

---

## 📬 联系方式

- **项目地址**: https://github.com/YOUR_USERNAME/independent-ai-mvp
- **问题反馈**: 请开 Issue
- **讨论交流**: 请开 Discussion

---

## 🗺️ 路线图

### ✅ 已完成 (Day 1-3)
- [x] MVP 架构与基础演示
- [x] 学习验证（98% 完成率）
- [x] 多 Agent 协作系统
- [x] Web 可视化界面
- [x] SARSA 算法实现

### 🎯 进行中 (Day 4-7)
- [ ] Windows 桌面版（Electron）
- [ ] 实际应用集成
- [ ] 任务依赖图分析
- [ ] WebSocket 实时推送

### 🔮 计划中 (Week 2+)
- [ ] Deep Q-Learning
- [ ] 更多学习算法
- [ ] Agent 谈判协议
- [ ] 生产环境部署

---

## 📈 项目统计

- **代码量**: 1.5MB+
- **文件数**: 35+
- **Python 文件**: 20+
- **演示脚本**: 10+
- **学习算法**: 2 个
- **配置预设**: 5 种

---

*最后更新：2026-03-29*  
*独立 AI MVP - 不依赖大模型的独立思考系统* 🚀
