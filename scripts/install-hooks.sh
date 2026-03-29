#!/bin/bash
# Git Hooks 安装脚本

echo "╔════════════════════════════════════════════════════════╗"
echo "║         🔧 安装 Git Hooks                              ║"
echo "╚════════════════════════════════════════════════════════╝"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$SCRIPT_DIR/.git/hooks"

mkdir -p "$HOOKS_DIR"

cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
echo "🔍 运行提交前检查..."
echo "  ✓ 检查 Python 语法"
python3 -m py_compile $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$') 2>/dev/null || {
    echo "❌ Python 语法检查失败"
    exit 1
}
echo "  ✓ 检查敏感信息"
if git diff --cached | grep -E "(password|secret|api_key|token)\s*[:=]" > /dev/null; then
    echo "❌ 检测到可能的敏感信息"
    exit 1
fi
echo "✅ 所有检查通过"
exit 0
EOF

chmod +x "$HOOKS_DIR/pre-commit"
echo "✅ 安装 pre-commit hook"

cat > "$HOOKS_DIR/post-commit" << 'EOF'
#!/bin/bash
echo "📝 记录提交到日志..."
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
mkdir -p "$(dirname "$0")/../logs"
echo "[$COMMIT_TIME] $COMMIT_HASH - $COMMIT_MSG" >> "$(dirname "$0")/../logs/commits.log"
echo "✅ 提交已记录"
EOF

chmod +x "$HOOKS_DIR/post-commit"
echo "✅ 安装 post-commit hook"

mkdir -p "$SCRIPT_DIR/logs"
touch "$SCRIPT_DIR/logs/commits.log"
echo "✅ 创建日志目录"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║         ✅ Git Hooks 安装完成！                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "已安装的 hooks:"
echo "  - pre-commit: 语法检查 + 敏感信息检测"
echo "  - post-commit: 提交日志记录"
echo ""
