# 🚀 独立 AI MVP

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stage: MVP](https://img.shields.io/badge/Stage-MVP-green.svg)]

**不依赖大模型的独立思考 AI 原型系统**

> 探索符号 AI + 强化学习的混合架构，实现自主决策、经验学习、自我监控能力

---

## 🌟 特性亮点

- 🤖 **真正的自主运行** - 给一个目标，AI 自主持续工作
- 🧠 **内在动机系统** - 好奇心/成就感/改进欲驱动
- 📊 **效用函数决策** - 透明可解释的自主决策
- 📚 **自主学习** - 主动学习新知识、下载技能
- 🔄 **自我进化** - 自动改进代码、优化性能
- 🎤 **文字 + 语音交互** - 自然对话 + 语音识别/合成
- 💻 **编程助手** - 支持 10 大编程语言
- 📋 **任务规划** - 自动分解复杂任务
- 👥 **多 Agent 协作** - 合同网协议 + 谈判机制
- 🖥️ **桌面应用** - Electron 跨平台桌面版
- 🔌 **VS Code 插件** - 编辑器深度集成

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

# 方式三：小七主程序（交互模式）
python3 xiaoqi.py

# 方式四：真正的自主运行！
python3 xiaoqi.py --auto "开发视频生成系统"

# 方式五：桌面版（跨平台 GUI）
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
├── vscode-extension/         # 🆕 VS Code 插件
│   ├── src/
│   │   └── extension.ts      # 插件主入口
│   ├── package.json          # 插件配置
│   ├── tsconfig.json         # TypeScript 配置
│   ├── README.md             # 插件文档
│   └── INSTALL.md            # 安装指南
│
├── docs/                       # 文档
│   ├── Agent 谈判协议.md       # 🆕 谈判协议详解
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

### 5. 🆕 Agent 谈判协议

基于合同网协议的谈判系统：

```bash
python3 demo/Agent 谈判协议演示.py
```

**功能**:
- 🤝 任务招标（Task Announcement）
- 💰 投标（Bid）
- 🏆 中标（Award）
- 💬 多轮协商（Negotiation）
- 📊 AIGC 视频工作流分配

**应用场景**:
- AIGC 视频生成（导演→编剧→分镜→视频）
- 代码开发（TechLead→前端→后端→测试）
- 文档编写（编辑→作者→审核→翻译）

### 6. Web 可视化

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

### 7. 🆕 桌面版（Electron）

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

### 8. 🆕 VS Code 插件

编辑器深度集成：

```bash
cd vscode-extension
npm install
npm run compile
```

**功能**:
- 🔌 右键格式化代码
- ⚡ 一键运行实验
- 📝 自动生成日报
- 📊 实时状态查看
- 🎹 快捷键支持（Ctrl+Shift+I/E）

**安装方式**:
1. 开发模式：F5 启动调试
2. 打包安装：`vsce package` + 从 VSIX 安装
3. 配置项目路径即可使用

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

## 🆕 新功能 (Day 5)

### CLI 命令行工具

```bash
# 运行实验
python3 cli.py run learning

# 查看状态
python3 cli.py status

# 查看统计
python3 cli.py stats

# 对比实验
python3 cli.py compare learning --rounds 5

# 启动 Web 界面
python3 cli.py web

# 启动桌面版
python3 cli.py desktop
```

### 实验对比工具

自动对比不同配置的效果：

```bash
python3 demo/实验对比演示.py
```

**支持对比**:
- 学习率（0.01, 0.05, 0.1, 0.2, 0.5）
- 折扣因子（0.8, 0.85, 0.9, 0.95, 0.99）
- 探索率（0.1, 0.2, 0.3, 0.5, 0.8）
- 决策权重（Balanced, Quality, Urgent）

### WebSocket 实时推送

实时推送实验数据到前端：

```bash
# 启动 WebSocket 服务器
python3 -m src.websocket.server

# 前端连接
const ws = new WebSocket('ws://localhost:8765');
```

---

## 🗺️ 路线图

### ✅ 已完成 (Day 1-5)
- [x] MVP 架构与基础演示
- [x] 学习验证（98% 完成率）
- [x] 多 Agent 协作系统
- [x] Web 可视化界面
- [x] SARSA 算法实现
- [x] Windows 桌面版（Electron）
- [x] 实际应用集成（格式化/测试/日报）
- [x] CLI 命令行工具
- [x] 实验对比工具
- [x] WebSocket 实时推送

### 🎯 进行中 (Week 2)
- [ ] 桌面版打包（可执行文件）
- [ ] 任务依赖图分析
- [ ] Deep Q-Learning
- [ ] VS Code 插件集成

### 🔮 计划中 (Week 3+)
- [ ] Agent 谈判协议
- [ ] 自动参数调优
- [ ] 生产环境部署
- [ ] 更多学习算法

---

## 📈 项目统计

| 项目 | 数值 |
|------|------|
| **代码量** | 1.6MB+ |
| **文件数** | 80+ |
| **Python 模块** | 35+ |
| **演示脚本** | 12+ |
| **学习算法** | 2 个 |
| **配置预设** | 5 种 |
| **GitHub 提交** | 6+ |

---

*最后更新：2026-03-30*  
*独立 AI MVP - 不依赖大模型的独立思考系统* 🚀

---

## 🎉 真正的自主运行

**这是 indie-ai 的核心突破！**

### 什么是真正的自主？

之前的 AI：
```
你：执行任务
AI：执行

你：学习
AI：学习

❌ 需要用户不断下命令
```

现在的小七：
```
你：帮我开发一个视频生成系统

小七：好的！我开始自主工作...

[小七自己持续运行]
[1] 💭 思考：自我改进 → 安装技能
[2] 💭 思考：执行任务 → 需求分析
[3] 💭 思考：学习 → 视频生成技术
[4] 💭 思考：执行任务 → 设计方案
...
[持续运行，直到用户叫停]

✅ 真正的自主！
```

### 核心特性

- 🧠 **内在动机** - 好奇心/成就感/改进欲驱动
- 📊 **效用函数** - 透明可解释的决策
- 🔄 **持续运行** - 不需要用户不断命令
- 📚 **自主学习** - 主动学习新知识
- 🔧 **自我改进** - 自动优化代码
- 📈 **定期汇报** - 显示进度和成果

### 立即体验

```bash
python3 xiaoqi.py --auto "开发视频生成系统"
```
