#!/usr/bin/env python3
"""
创建 GitHub Release

使用 GitHub API 创建 Release
"""

import subprocess
import json
from pathlib import Path

# Release 信息
TAG = "v1.1.0"
TITLE = "🎉 Release v1.1.0 - P3 功能增强版"

BODY = """
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
"""

def create_release():
    """创建 Release"""
    print(f"\n🎬 创建 GitHub Release {TAG}\n")
    
    # 检查 tag 是否存在
    result = subprocess.run(
        ["git", "tag", "-l", TAG],
        capture_output=True,
        text=True
    )
    
    if TAG not in result.stdout:
        print(f"❌ Tag {TAG} 不存在，请先创建 tag")
        return False
    
    print(f"✅ Tag {TAG} 存在")
    
    # 保存 Release 说明到文件
    release_file = Path("RELEASE_NOTES.md")
    with open(release_file, 'w', encoding='utf-8') as f:
        f.write(f"# {TITLE}\n\n")
        f.write(BODY)
    
    print(f"✅ Release 说明已保存到：{release_file}")
    
    # 打印创建说明
    print("\n" + "="*60)
    print("📝 手动创建 Release 步骤:")
    print("="*60)
    print(f"\n1. 访问：https://github.com/skytitan008/indie-ai/releases/new")
    print(f"2. 选择 tag: {TAG}")
    print(f"3. 标题：{TITLE}")
    print(f"4. 复制以下 Release 说明:\n")
    print("-"*60)
    print(BODY)
    print("-"*60)
    print("\n5. 点击 'Publish release'")
    print()
    
    return True


if __name__ == '__main__':
    create_release()
