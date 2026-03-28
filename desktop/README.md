# 🖥️ Indie AI Desktop - 桌面版

**不依赖大模型的独立思考 AI 系统 - Electron 桌面应用**

---

## 🚀 快速开始

### 方式一：开发模式运行

```bash
# 进入桌面目录
cd desktop

# 安装依赖
npm install

# 启动应用
npm start
```

### 方式二：打包为可执行文件

```bash
# 安装依赖
npm install

# 打包 Windows 版
npm run build:win

# 打包 macOS 版
npm run build:mac

# 打包 Linux 版
npm run build:linux

# 打包所有平台
npm run build
```

打包后的文件在 `dist/` 目录。

---

## 📦 安装包

### Windows
- `dist/Indie AI Setup x.x.x.exe` - 安装程序
- `dist/win-unpacked/` - 绿色版

### macOS
- `dist/Indie AI-x.x.x.dmg` - DMG 镜像

### Linux
- `dist/Indie AI-x.x.x.AppImage` - AppImage

---

## ✨ 功能特性

### 1. 独立窗口运行
- ✅ 不用开浏览器
- ✅ 1400x900 默认窗口
- ✅ 可调整大小
- ✅ 深色主题

### 2. 系统托盘
- ✅ 最小化到托盘
- ✅ 托盘菜单快速启动实验
- ✅ 双击托盘图标打开窗口
- ✅ 通知提醒

### 3. 实验管理
- ✅ 一键运行所有演示实验
- ✅ 实时输出显示
- ✅ 彩色日志（成功/失败/信息）
- ✅ 导出实验日志

### 4. 统计面板
- ✅ 已运行实验次数
- ✅ 成功/失败统计
- ✅ 运行时长
- ✅ Python 版本检测

### 5. 快捷键
- `Ctrl+L` - 清空控制台
- `Ctrl+S` - 导出日志

---

## 🎨 界面预览

### 主界面
- 左侧：实验列表（快速启动）
- 右上：统计卡片（4 个指标）
- 右下：实验输出控制台

### 系统托盘
- 打开主窗口
- 运行综合实验
- 运行真实任务执行
- 运行长期学习实验
- 运行多 Agent 协作
- 退出

---

## 📁 项目结构

```
desktop/
├── src/
│   ├── main.js          # Electron 主进程
│   ├── preload.js       # 预加载脚本
│   └── index.html       # 主界面
├── assets/
│   └── icon.png         # 应用图标
├── package.json         # Node.js 配置
└── README.md            # 本文件
```

---

## 🔧 开发指南

### 添加新实验

1. 在 `src/index.html` 的实验列表中添加按钮：
```html
<button class="experiment-btn" onclick="runExperiment('你的实验.py')" data-script="你的实验.py">
  🎯 你的实验
</button>
```

2. 确保实验文件在 `../demo/` 目录

### 自定义界面

编辑 `src/index.html` 中的 CSS 和 HTML。

### 修改主进程

编辑 `src/main.js`，重启应用生效。

---

## 🐛 常见问题

### Q1: npm install 失败？

**A**: 检查 Node.js 版本：
```bash
node --version  # 需要 16+
npm --version   # 需要 8+
```

### Q2: 应用无法启动？

**A**: 检查 Python 环境：
```bash
python3 --version
```

确保 `demo/` 目录中的脚本可以独立运行。

### Q3: 托盘图标不显示？

**A**: 某些 Linux 发行版需要安装托盘支持：
```bash
# Ubuntu/Debian
sudo apt install libappindicator3-1

# Arch Linux
sudo pacman -S libappindicator-gtk3
```

### Q4: 打包后文件太大？

**A**: 这是正常的，Electron 应用包含 Chromium 内核。
可以使用以下优化：
- 使用 `electron-builder` 的压缩选项
- 考虑使用 `portable` 格式

---

## 📊 技术栈

- **Electron** - 跨平台桌面框架
- **Node.js** - 运行时
- **HTML/CSS/JS** - 前端界面
- **Python** - 后端实验脚本

---

## 🎯 下一步

- [ ] 集成 WebView 直接显示 Web 可视化
- [ ] 添加实验历史记录
- [ ] 添加图表可视化（Chart.js 集成）
- [ ] 添加设置界面
- [ ] 自动更新功能
- [ ] 插件系统

---

## 📄 许可证

MIT License - 与主项目一致

---

*Indie AI Desktop - 让 AI 触手可及！* 🚀
