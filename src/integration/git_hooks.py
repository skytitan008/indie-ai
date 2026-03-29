#!/usr/bin/env python3
"""
Git Hooks 集成

在 Git 操作时自动执行：
- pre-commit: 提交前格式化和测试
- post-commit: 提交后记录
- pre-push: 推送前检查
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional
import json
import os


class GitHooks:
    """Git Hooks 管理器"""
    
    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path) if repo_path else Path('.')
        self.git_hooks_dir = self.repo_path / '.git' / 'hooks'
        self.custom_hooks_dir = self.repo_path / '.githooks'
    
    def install(self, hooks: Optional[list] = None):
        """
        安装 Git Hooks
        
        Args:
            hooks: 要安装的钩子列表
        """
        if hooks is None:
            hooks = ['pre-commit', 'post-commit', 'pre-push']
        
        # 创建自定义钩子目录
        self.custom_hooks_dir.mkdir(exist_ok=True)
        
        # 配置 Git 使用自定义钩子目录
        subprocess.run(
            ['git', 'config', 'core.hooksPath', str(self.custom_hooks_dir)],
            cwd=self.repo_path
        )
        
        # 安装每个钩子
        for hook_name in hooks:
            self._install_hook(hook_name)
        
        print(f"✅ 已安装 Git Hooks: {', '.join(hooks)}")
        print(f"📁 钩子目录：{self.custom_hooks_dir}")
    
    def _install_hook(self, hook_name: str):
        """安装单个钩子"""
        hook_script = self.custom_hooks_dir / hook_name
        
        if hook_name == 'pre-commit':
            content = self._get_pre_commit_script()
        elif hook_name == 'post-commit':
            content = self._get_post_commit_script()
        elif hook_name == 'pre-push':
            content = self._get_pre_push_script()
        else:
            print(f"⚠️  未知钩子：{hook_name}")
            return
        
        with open(hook_script, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 添加执行权限
        os.chmod(hook_script, 0o755)
    
    def _get_pre_commit_script(self) -> str:
        """获取 pre-commit 钩子脚本"""
        return '''#!/bin/bash
# Pre-commit hook - 提交前自动格式化和测试

echo "╔════════════════════════════════════════════════════════╗"
echo "║         🔄 Pre-commit Hook                             ║"
echo "╚════════════════════════════════════════════════════════╝"

# 获取暂存的文件
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|js|ts|jsx|tsx)$')

if [ -z "$FILES" ]; then
    echo "ℹ️  没有需要检查的代码文件"
    exit 0
fi

echo "📝 检查文件：$FILES"
echo ""

# Python 文件格式化检查
PY_FILES=$(echo "$FILES" | grep '\.py$')
if [ -n "$PY_FILES" ]; then
    echo "🐍 检查 Python 文件..."
    
    # 检查 black 格式
    if command -v black &> /dev/null; then
        echo "  - 检查 black 格式..."
        if ! black --check $PY_FILES 2>/dev/null; then
            echo "❌ 代码格式不符合 black 规范"
            echo "💡 运行 'black $PY_FILES' 格式化代码"
            exit 1
        fi
    fi
    
    # 运行相关测试
    if [ -d "tests" ]; then
        echo "  - 运行相关测试..."
        if command -v pytest &> /dev/null; then
            pytest tests/ -x -q || {
                echo "❌ 测试失败"
                exit 1
            }
        fi
    fi
fi

# JavaScript/TypeScript 文件检查
JS_FILES=$(echo "$FILES" | grep -E '\.(js|ts|jsx|tsx)$')
if [ -n "$JS_FILES" ]; then
    echo "📜 检查 JavaScript/TypeScript 文件..."
    
    if [ -f "package.json" ] && command -v npx &> /dev/null; then
        echo "  - 检查 prettier 格式..."
        if ! npx prettier --check $JS_FILES 2>/dev/null; then
            echo "❌ 代码格式不符合 prettier 规范"
            echo "💡 运行 'npx prettier --write $JS_FILES' 格式化代码"
            exit 1
        fi
    fi
fi

echo ""
echo "✅ Pre-commit 检查通过！"
exit 0
'''
    
    def _get_post_commit_script(self) -> str:
        """获取 post-commit 钩子脚本"""
        return '''#!/bin/bash
# Post-commit hook - 提交后记录

echo "╔════════════════════════════════════════════════════════╗"
echo "║         📝 Post-commit Hook                            ║"
echo "╚════════════════════════════════════════════════════════╝"

# 获取提交信息
COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=%s)
COMMIT_TIME=$(date '+%Y-%m-%d %H:%M:%S')

echo "✅ 提交成功"
echo "  Hash: $COMMIT_HASH"
echo "  信息：$COMMIT_MSG"
echo "  时间：$COMMIT_TIME"

# 记录到日志文件
LOG_FILE="commit_log.json"

# 创建或读取日志
if [ -f "$LOG_FILE" ]; then
    LOG=$(cat "$LOG_FILE")
else
    LOG="[]"
fi

# 添加新记录（使用 Python 处理 JSON）
python3 << EOF
import json

try:
    with open('$LOG_FILE', 'r', encoding='utf-8') as f:
        logs = json.load(f)
except:
    logs = []

logs.append({
    'hash': '$COMMIT_HASH',
    'message': '$COMMIT_MSG',
    'time': '$COMMIT_TIME',
    'author': '$(git config user.name)'
})

# 只保留最近 100 条
logs = logs[-100:]

with open('$LOG_FILE', 'w', encoding='utf-8') as f:
    json.dump(logs, f, indent=2, ensure_ascii=False)
EOF

echo "📝 已记录到 $LOG_FILE"
exit 0
'''
    
    def _get_pre_push_script(self) -> str:
        """获取 pre-push 钩子脚本"""
        return '''#!/bin/bash
# Pre-push hook - 推送前检查

echo "╔════════════════════════════════════════════════════════╗"
echo "║         🚀 Pre-push Hook                               ║"
echo "╚════════════════════════════════════════════════════════╝"

# 运行所有测试
echo "🧪 运行测试套件..."
if [ -d "tests" ]; then
    if command -v pytest &> /dev/null; then
        pytest tests/ -q || {
            echo "❌ 测试失败，禁止推送"
            exit 1
        }
    fi
fi

# 检查是否有敏感信息
echo "🔒 检查敏感信息..."
if git diff --cached | grep -i "password\|secret\|api_key\|token" > /dev/null; then
    echo "⚠️  警告：提交中包含敏感信息关键字"
    echo "💡 请确认没有泄露密码、密钥等敏感信息"
    read -p "确认继续推送？(y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "❌ 推送已取消"
        exit 1
    fi
fi

echo ""
echo "✅ Pre-push 检查通过！"
exit 0
'''
    
    def uninstall(self):
        """卸载 Git Hooks"""
        import shutil
        
        # 重置 Git 配置
        subprocess.run(
            ['git', 'config', '--unset', 'core.hooksPath'],
            cwd=self.repo_path
        )
        
        # 删除自定义钩子目录
        if self.custom_hooks_dir.exists():
            shutil.rmtree(self.custom_hooks_dir)
        
        print("✅ Git Hooks 已卸载")
    
    def status(self):
        """显示 Git Hooks 状态"""
        print("╔════════════════════════════════════════════════════════╗")
        print("║         Git Hooks 状态                                 ║")
        print("╚════════════════════════════════════════════════════════╝")
        
        # 检查配置
        result = subprocess.run(
            ['git', 'config', 'core.hooksPath'],
            capture_output=True, text=True, cwd=self.repo_path
        )
        
        if result.stdout.strip():
            print(f"✅ Git Hooks 已配置")
            print(f"📁 钩子目录：{result.stdout.strip()}")
            
            # 列出已安装的钩子
            if self.custom_hooks_dir.exists():
                hooks = list(self.custom_hooks_dir.glob('*'))
                if hooks:
                    print(f"\n已安装的钩子:")
                    for hook in hooks:
                        print(f"  • {hook.name}")
        else:
            print("❌ Git Hooks 未配置")
            print("💡 运行 'python -m integration.git_hooks install' 安装")


def install_hooks():
    """安装 Git Hooks（命令行入口）"""
    hooks = GitHooks()
    hooks.install()


def uninstall_hooks():
    """卸载 Git Hooks（命令行入口）"""
    hooks = GitHooks()
    hooks.uninstall()


def show_status():
    """显示状态（命令行入口）"""
    hooks = GitHooks()
    hooks.status()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'install':
            install_hooks()
        elif sys.argv[1] == 'uninstall':
            uninstall_hooks()
        elif sys.argv[1] == 'status':
            show_status()
        else:
            print("用法：python -m integration.git_hooks [install|uninstall|status]")
    else:
        print("用法：python -m integration.git_hooks [install|uninstall|status]")
