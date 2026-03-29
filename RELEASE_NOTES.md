# 🎉 Release v1.1.0 - P3 功能增强版


## 🚀 新功能

### CLI 命令行工具
- `run` - 运行实验
- `status` - 查看状态
- `stats` - 查看统计
- `compare` - 对比实验
- `clean` - 清理数据
- `web` - 启动 Web 界面
- `desktop` - 启动桌面版
- `version` - 显示版本

### 实验对比工具
- 学习率对比（0.01, 0.05, 0.1, 0.2, 0.5）
- 折扣因子对比（0.8, 0.85, 0.9, 0.95, 0.99）
- 探索率对比（0.1, 0.2, 0.3, 0.5, 0.8）
- 决策权重对比（Balanced, Quality, Urgent）

### 自动参数调优
- 网格搜索参数组合
- 自动评估配置效果
- 保存最佳配置到文件

### WebSocket 实时推送
- 实时推送实验进度
- 实时更新学习曲线
- 多客户端支持
- 地址：ws://localhost:8765

### Git Hooks 自动化
- pre-commit：语法检查 + 敏感信息检测
- post-commit：提交日志记录
- 安装：`bash scripts/install-hooks.sh`

## 📊 项目统计

| 项目 | 数值 |
|------|------|
| 总文件数 | 85+ |
| 总代码量 | 1.65MB+ |
| Python 模块 | 40+ |
| 演示脚本 | 14+ |
| GitHub 提交 | 8+ |

## 🔧 技术改进

- 修复 Agent API 兼容性问题
- 优化 Task 类使用方式
- 简化实验对比流程
- 改进 CLI 用户体验

## 📝 使用示例

### 运行实验
```bash
python3 cli.py run learning
```

### 查看状态
```bash
python3 cli.py status
```

### 对比实验
```bash
python3 cli.py compare learning --rounds 5
```

### 启动 WebSocket
```bash
python3 -m src.websocket.server
```

### 安装 Git Hooks
```bash
bash scripts/install-hooks.sh
```

## 🎯 下一步

- [ ] 桌面版打包（Windows/macOS/Linux）
- [ ] Deep Q-Learning 实现
- [ ] VS Code 插件集成
- [ ] 任务依赖图可视化

---

**完整更新日志**: 见 CHANGELOG.md  
**项目地址**: https://github.com/skytitan008/indie-ai
