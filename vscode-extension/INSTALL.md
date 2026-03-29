# 📦 VS Code 插件安装指南

## 快速安装

### 前提条件

确保已安装：
- Node.js 16+
- npm 8+
- VS Code 1.85+

---

## 方式 1: 开发模式（推荐）

### 步骤 1: 安装依赖

```bash
cd vscode-extension
npm install
```

### 步骤 2: 编译 TypeScript

```bash
npm run compile
```

### 步骤 3: 启动调试

1. 在 VS Code 中打开 `vscode-extension` 文件夹
2. 按 `F5` 或 运行 → 启动调试
3. 选择 "Extension Development Host"
4. 新窗口会加载插件

### 步骤 4: 配置项目路径

在新窗口中：
1. 文件 → 首选项 → 设置
2. 搜索 "Indie AI"
3. 设置 `Indie Ai: Project Path` 为项目根目录

---

## 方式 2: 打包安装

### 步骤 1: 安装 vsce

```bash
npm install -g @vscode/vsce
```

### 步骤 2: 打包

```bash
cd vscode-extension
npm install
npm run compile
vsce package
```

生成文件：`indie-ai-helper-1.0.0.vsix`

### 步骤 3: 安装

1. 打开 VS Code
2. 扩展 (Ctrl+Shift+X)
3. 点击右上角 `···` 菜单
4. 选择 "从 VSIX 安装..."
5. 选择生成的 `.vsix` 文件

---

## 方式 3: 本地链接

### 步骤 1: 链接插件

```bash
cd vscode-extension
npm link
```

### 步骤 2: 在 VS Code 中使用

1. 打开 VS Code
2. 运行 "Developer: Install Extension From Location"
3. 选择 `vscode-extension` 目录

---

## ⚙️ 配置

打开设置 (`Ctrl+,`)，搜索 "Indie AI"，配置以下项：

```json
{
  "indieAi.projectPath": "/home/fenghuang/.copaw/workspaces/default/independent-ai-mvp",
  "indieAi.pythonPath": "python3",
  "indieAi.autoFormat": false
}
```

或在 `settings.json` 中添加：

```json
{
  "indieAi.projectPath": "/path/to/indie-ai-mvp",
  "indieAi.pythonPath": "python3",
  "indieAi.autoFormat": false
}
```

---

## 🎹 快捷键

| 功能 | Windows/Linux | macOS |
|------|---------------|-------|
| 格式化代码 | `Ctrl+Shift+I` | `Cmd+Shift+I` |
| 运行实验 | `Ctrl+Shift+E` | `Cmd+Shift+E` |

---

## 🧪 测试

### 测试格式化

1. 打开 Python 文件
2. 按 `Ctrl+Shift+I`
3. 查看输出面板

### 测试运行实验

1. 按 `Ctrl+Shift+E`
2. 选择实验
3. 查看输出面板

### 测试生成日报

1. 按 `Ctrl+Shift+P`
2. 输入 "Indie AI: 生成日报"
3. 查看输出面板

---

## 🐛 故障排除

### 问题：命令不显示

**解决：**
1. 重启 VS Code
2. 检查插件是否启用
3. 查看扩展输出面板

### 问题：Python 命令失败

**解决：**
1. 检查 Python 路径：`which python3`
2. 更新配置中的 `indieAi.pythonPath`
3. 确保依赖已安装：`pip install -r requirements.txt`

### 问题：格式化无反应

**解决：**
1. 检查 black 是否安装：`pip install black`
2. 检查项目路径配置
3. 查看输出面板错误信息

---

## 📝 卸载

### 方式 1: VS Code 界面

1. 扩展 (Ctrl+Shift+X)
2. 搜索 "Indie AI Helper"
3. 点击卸载

### 方式 2: 命令行

```bash
# 找到插件位置
code --list-extensions | grep indie-ai

# 卸载
code --uninstall-extension skytitan008.indie-ai-helper
```

---

## 📦 发布到市场（可选）

### 步骤 1: 创建发布者

访问：https://marketplace.visualstudio.com/manage

### 步骤 2: 创建 Personal Access Token

1. Azure DevOps → Personal Access Tokens
2. 创建新 token（范围：Marketplace (Manage)）

### 步骤 3: 登录

```bash
vsce login skytitan008
# 输入 token
```

### 步骤 4: 发布

```bash
vsce publish
```

---

## 🔗 相关链接

- [VS Code 扩展文档](https://code.visualstudio.com/api)
- [插件市场](https://marketplace.visualstudio.com/vscode)
- [Yeoman 生成器](https://github.com/microsoft/vscode-generator-code)

---

*最后更新：2026-03-29*
