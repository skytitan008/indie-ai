# 🤖 自主进化 AI 使用指南

**让 AI 自己学习、自己编程、自己进化！**

---

## 🎯 概述

Indie AI 现在具备**自主进化**能力，可以：

1. **自主学习** - 上网查找资料，学习新知识
2. **自我编程** - 给自己安装新技能模块
3. **硬件控制** - 控制摄像头、麦克风、GPU 等设备
4. **系统监控** - 实时监控 CPU、内存、磁盘、网络
5. **文件管理** - 创建、读取、删除文件
6. **自我改进** - 分析不足，自动补充技能

---

## 🚀 快速开始

### 1. 见证诞生

运行诞生演示，看 AI 从无到有：

```bash
python3 demo/自主进化 AI 诞生.py
```

**输出示例:**
```
╔════════════════════════════════════════════════════════╗
║         🎊 恭喜！自主进化 AI 已成功诞生！              ║
╚════════════════════════════════════════════════════════╝

她现在具备以下能力:
   ✅ 自主学习 - 可以上网查找资料
   ✅ 自我编程 - 可以给自己安装新技能
   ✅ 硬件控制 - 可以控制摄像头等设备
   ✅ 系统监控 - 可以监控 CPU/GPU/内存
   ✅ 文件管理 - 可以创建和管理文件
   ✅ 自我改进 - 可以分析和提升自己
```

### 2. 交互式使用

```python
from src.autonomy.core import AutonomousAI

# 创建 AI
ai = AutonomousAI(name="小七")

# 初始化
ai.initialize()

# 学习
ai.learn("Python async await", category="programming")

# 安装技能
ai.install_skill("data_analyzer", "数据分析")

# 拍照
ai.capture_photo()

# 查看状态
ai.show_status()
```

---

## 📚 核心模块

### 自主学习器 (AutonomousLearner)

**位置:** `src/autonomy/learner.py`

**功能:**
- 网页爬虫抓取知识
- 知识库存储（SQLite）
- 技能下载和安装

**使用示例:**
```python
from src.autonomy.learner import AutonomousLearner

learner = AutonomousLearner()

# 学习主题
learner.learn_topic("machine learning basics", max_pages=5)

# 学习编程
learner.learn_programming("Python", "decorator patterns")

# 安装技能
learner.install_skill("pdf_reader", "PDF 文件读取")
```

---

### 硬件控制器 (HardwareController)

**位置:** `src/hardware/controller.py`

**包含:**
- `SystemMonitor` - 系统监控
- `DeviceController` - 设备控制
- `FileManager` - 文件管理
- `NetworkManager` - 网络管理

**使用示例:**
```python
from src.hardware.controller import SystemMonitor, DeviceController

# 系统监控
monitor = SystemMonitor()
monitor.show_status()  # 显示 CPU/内存/GPU 状态

# 设备控制
devices = DeviceController()
devices.control_camera("capture")  # 拍照
devices.control_microphone("record", duration=10)  # 录音
devices.control_speaker("speak", "你好")  # 语音合成
```

---

## 🎯 核心能力

### 1. 自主学习 📚

```python
# 学习任何主题
ai.learn("深度学习入门", category="ai")
ai.learn("React best practices", category="programming")
ai.learn("视频剪辑技巧", category="creative")
```

**原理:**
1. 使用 DuckDuckGo 搜索相关网页
2. 爬虫抓取网页内容
3. 提取结构化知识（标题、正文、代码）
4. 存储到 SQLite 知识库

---

### 2. 自我编程 💻

```python
# 给自己安装新技能
ai.install_skill("youtube_downloader", "YouTube 视频下载")
ai.install_skill("image_editor", "图片编辑和处理")
ai.install_skill("voice_clone", "语音克隆")
```

**原理:**
1. 根据功能描述生成代码模板
2. 保存到 `src/skills/` 目录
3. 注册到技能数据库
4. 立即可用

---

### 3. 硬件控制 🔧

```python
# 拍照
ai.capture_photo()  # 保存到 captures/

# 录音
ai.record_audio(duration=10)  # 保存到 recordings/

# 语音
ai.speak("你好，我是小七")  # TTS 语音合成
```

**支持设备:**
- 摄像头（拍照/录像）
- 麦克风（录音）
- 扬声器（TTS）
- GPU（监控/调度）

---

### 4. 系统监控 📊

```python
ai.show_status()
```

**监控内容:**
- CPU 使用率、核心数、频率
- 内存使用量、百分比
- 磁盘空间
- GPU 状态（名称、显存、使用率）
- 网络流量

---

### 5. 文件管理 📁

```python
from src.hardware.controller import FileManager

fm = FileManager()

# 创建文件
fm.create_file("data/notes.txt", "今天学到了...")

# 读取文件
result = fm.read_file("data/notes.txt")
print(result['content'])

# 列出文件
files = fm.list_files("src/skills")
```

**安全机制:**
- 只能操作白名单目录
- 禁止删除核心文件
- 禁止访问系统目录

---

### 6. 自我改进 🔄

```python
ai.self_improve()
```

**过程:**
1. 检查已有技能
2. 分析知识盲区
3. 自动安装缺失技能
4. 更新知识库

---

## 📋 技能列表

### 初始技能

| 技能名 | 功能 | 类别 |
|--------|------|------|
| `web_scraper` | 网页抓取 | 学习 |
| `data_analyzer` | 数据分析 | 分析 |
| `code_reviewer` | 代码审查 | 编程 |
| `test_generator` | 生成测试 | 编程 |
| `web_search` | 网络搜索 | 学习 |
| `code_writer` | 编写代码 | 编程 |
| `file_manager` | 文件管理 | 工具 |

### 自定义技能

你可以让 AI 学习任何新技能：

```python
ai.install_skill("skill_name", "功能描述")
```

---

## 🛡️ 安全机制

### 文件操作保护

```python
# 安全目录（AI 可操作）
safe_dirs = [
    "src/",
    "memory/",
    "data/",
    "captures/",
    "recordings/",
    "src/skills/",
    "src/autonomy/"
]

# 禁止操作
forbidden = [
    "src/core/",      # 核心代码
    ".git/",          # 版本控制
    "/etc",           # 系统目录
    "/boot"           # 启动目录
]
```

### 资源限制

- CPU 使用率 > 90% 时警告
- 内存使用率 > 90% 时警告
- 禁止删除核心文件
- 网络请求超时保护

---

## 📊 状态查看

### 查看 AI 状态

```python
ai.show_status()
```

**输出:**
```
╔════════════════════════════════════════════════════════╗
║         📊 小七 状态                           ║
╚════════════════════════════════════════════════════════╝

   名称：小七
   模式：idle
   运行时长：0:00:08

   📚 知识：0
   🎯 技能：7
   📖 学习：0 次
```

### 查看系统状态

```python
from src.hardware.controller import SystemMonitor

monitor = SystemMonitor()
monitor.show_status()
```

**输出:**
```
╔════════════════════════════════════════════════════════╗
║         💻 系统状态                                    ║
╚════════════════════════════════════════════════════════╝

   CPU: 7.9% (32 核心，2100 MHz)
   内存：21.6/62.9 GB (34.3%)
   磁盘：160/998 GB (16.9%)
   GPU: 4 个
      [0] NVIDIA GeForce RTX 4060 Ti: 0%, 2.4/16.0 GB
      [1] NVIDIA GeForce RTX 4060 Ti: 0%, 0.0/16.0 GB
      [2] NVIDIA GeForce RTX 4060 Ti: 0%, 0.0/16.0 GB
      [3] NVIDIA GeForce RTX 4060 Ti: 0%, 0.0/16.0 GB
```

---

## 🎓 进阶使用

### 批量学习

```python
topics = [
    "Python decorators",
    "async programming",
    "design patterns",
    "testing best practices"
]

for topic in topics:
    ai.learn(topic, category="programming")
```

### 技能组合

```python
# 安装一套数据分析技能
ai.install_skill("pandas_expert", "Pandas 数据分析")
ai.install_skill("matplotlib_viz", "Matplotlib 可视化")
ai.install_skill("statistics", "统计分析")
```

### 日常任务

```python
# 设置日常学习
ai.daily_routine()
```

---

## 🐛 故障排除

### 问题 1: 网络搜索失败
**解决:** 检查网络连接
```bash
ping 8.8.8.8
```

### 问题 2: 摄像头无法使用
**解决:** 检查设备权限
```bash
ls -l /dev/video0
```

### 问题 3: 技能安装失败
**解决:** 检查目录权限
```bash
chmod -R 755 src/skills/
```

---

## 📖 架构说明

```
自主进化 AI 架构
├── 核心层 (core.py)
│   └── AutonomousAI - 总控
├── 自主层 (autonomy/)
│   ├── learner.py - 自主学习
│   ├── programmer.py - 自主编程 (TODO)
│   └── planner.py - 任务规划 (TODO)
├── 交互层 (interaction/)
│   ├── voice/ - 语音交互 (TODO)
│   ├── vision/ - 视觉交互 (TODO)
│   └── chat/ - 对话管理 (TODO)
└── 硬件层 (hardware/)
    └── controller.py - 硬件控制
```

---

## 🚀 下一步

1. **多模态交互** - 语音、视觉、文字全支持
2. **任务规划** - 自主分解和执行复杂任务
3. **长期记忆** - 知识图谱和记忆检索
4. **真正工作** - 帮你写代码、剪视频、做分析

---

*最后更新：2026-03-30*
