# 🤖 Indie AI Helper - VS Code 插件

不依赖大模型的独立思考 AI 助手 - VS Code 集成

---

## 🚀 功能特性

### 代码格式化
- 右键菜单格式化 Python 代码
- 快捷键：`Ctrl+Shift+I` (Mac: `Cmd+Shift+I`)
- 保存时自动格式化（可选）

### 运行实验
- 一键运行各种 AI 实验
- 快捷键：`Ctrl+Shift+E` (Mac: `Cmd+Shift+E`)
- 支持 7 种实验类型

### 任务管理
- 代码格式化
- 运行测试
- 生成日报
- 安装 Git Hooks

### 状态查看
- 实时查看 AI 状态
- Q 表大小
- 学习率/探索率

---

## 📦 安装

### 方式 1: 从 VSIX 安装

```bash
cd vscode-extension
npm install
npm run compile
vsce package  # 生成 indie-ai-helper-1.0.0.vsix

# 在 VS Code 中
# 扩展 → ··· → 从 VSIX 安装 → 选择 .vsix 文件
```

### 方式 2: 开发模式

```bash
cd vscode-extension
npm install
npm run compile

# 按 F5 或 运行 → 启动调试
# 选择 "Extension Development Host"
```

---

## ⚙️ 配置

在 VS Code 设置中添加：

```json
{
  "indieAi.projectPath": "/path/to/indie-ai-mvp",
  "indieAi.pythonPath": "python3",
  "indieAi.autoFormat": false
}
```

**配置说明:**
- `indieAi.projectPath`: Indie AI 项目根目录
- `indieAi.pythonPath`: Python 解释器路径
- `indieAi.autoFormat`: 保存时自动格式化

---

## 🎹 快捷键

| 功能 | Windows/Linux | macOS |
|------|---------------|-------|
| 格式化代码 | `Ctrl+Shift+I` | `Cmd+Shift+I` |
| 运行实验 | `Ctrl+Shift+E` | `Cmd+Shift+E` |

---

## 🎯 使用方式

### 格式化代码

1. 打开 Python 文件
2. 右键 → `Indie AI: 格式化代码`
3. 或使用快捷键 `Ctrl+Shift+I`

### 运行实验

1. 按 `Ctrl+Shift+O`
2. 选择实验类型
3. 查看输出面板

### 生成日报

1. 按 `Ctrl+Shift+P`
2. 输入 `Indie AI: 生成日报`
3. 查看输出面板

---

## 📊 输出面板

所有操作结果都会显示在 **输出面板** 的 `Indie AI` 频道中。

打开方式：
- 查看 → 输出
- 选择 `Indie AI` 频道

---

## 🔧 开发

### 编译

```bash
npm run compile
```

### 监听模式

```bash
npm run watch
```

### 打包

```bash
vsce package
```

### 发布

```bash
vsce publish
```

---

## 📝 命令列表

| 命令 ID | 说明 |
|--------|------|
| `indie-ai.formatCode` | 格式化代码 |
| `indie-ai.runExperiment` | 运行实验 |
| `indie-ai.showStatus` | 显示状态 |
| `indie-ai.runTask` | 运行任务 |
| `indie-ai.generateReport` | 生成日报 |

---

## 🐛 故障排除

### 问题 1: 命令不生效
- 检查项目路径配置
- 确保 Python 环境正确
- 重启 VS Code

### 问题 2: 格式化失败
- 检查 black 是否安装：`pip install black`
- 检查项目路径是否正确

### 问题 3: 输出面板无内容
- 查看其他频道是否有输出
- 重启 VS Code

---

## 📄 许可证

MIT License

---

*最后更新：2026-03-29*
