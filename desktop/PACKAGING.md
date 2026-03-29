# 📦 Indie AI 桌面版打包指南

## 快速打包

### Linux
```bash
cd desktop
npm run build:linux
```

### Windows
```bash
cd desktop
npm run build:win
```

### macOS
```bash
cd desktop
npm run build:mac
```

### 所有平台
```bash
cd desktop
npm run build
```

---

## 输出文件

打包完成后，可执行文件位于 `desktop/dist/` 目录：

### Linux
- `Indie AI-1.0.0.AppImage` - 免安装，直接运行
- `Indie AI-1.0.0.deb` - Debian/Ubuntu 安装包
- `Indie AI-1.0.0.rpm` - Fedora/RHEL 安装包

### Windows
- `Indie AI Setup 1.0.0.exe` - Windows 安装程序

### macOS
- `Indie AI-1.0.0.dmg` - macOS 安装包
- `Indie AI-1.0.0.zip` - macOS 压缩包

---

## 运行方式

### Linux AppImage
```bash
chmod +x "Indie AI-1.0.0.AppImage"
./"Indie AI-1.0.0.AppImage"
```

### Linux deb
```bash
sudo dpkg -i "Indie AI_1.0.0_amd64.deb"
indie-ai  # 命令行启动
```

### Windows
双击 `Indie AI Setup 1.0.0.exe` 安装

### macOS
双击 `Indie AI-1.0.0.dmg` 并拖拽到 Applications

---

## 故障排除

### 问题 1: 构建失败 - 缺少依赖
```bash
# 安装系统依赖（Ubuntu/Debian）
sudo apt-get install --no-install-recommends -y \
  wine \
  snapd \
  flatpak
```

### 问题 2: 权限错误
```bash
# Linux 上可能需要 sudo
sudo npm run build:linux
```

### 问题 3: 磁盘空间不足
打包需要约 2GB 空间，请确保有足够空间

---

## 自定义配置

编辑 `desktop/package.json` 中的 `build` 部分：

```json
{
  "build": {
    "appId": "com.indieai.desktop",
    "productName": "Indie AI",
    "version": "1.1.0",
    "win": {
      "target": ["nsis", "portable"]
    }
  }
}
```

---

*最后更新：2026-03-29*
