# 贡献指南

欢迎为 **独立 AI MVP** 项目贡献代码！🎉

## 🌟 如何贡献

### 1. 报告 Bug

发现 Bug？请开 Issue，包含：
- 清晰描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（Python 版本、操作系统）

### 2. 提出新功能

有新想法？请开 Issue 讨论：
- 功能描述
- 使用场景
- 实现思路（可选）

### 3. 提交代码

#### 步骤

1. **Fork 项目**
   ```bash
   # GitHub 上点击 Fork 按钮
   ```

2. **克隆项目**
   ```bash
   git clone https://github.com/YOUR_USERNAME/independent-ai-mvp.git
   cd independent-ai-mvp
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-fix-name
   ```

4. **开发**
   - 编写代码
   - 添加测试（如适用）
   - 更新文档（如需要）

5. **提交**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   # 或
   git commit -m "fix: fix your bug"
   ```

6. **推送**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Pull Request**
   - GitHub 上创建 PR
   - 填写详细描述
   - 等待审核

---

## 📝 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（非新功能，非 Bug 修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例

```bash
feat: 添加 SARSA 学习算法
fix: 修复 Q-Learning 参数不匹配问题
docs: 更新 README 使用示例
refactor: 重构决策引擎代码
perf: 优化 Q 表查询性能
```

---

## 🧪 开发环境

### 设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 运行测试

```bash
# 运行所有演示
./run.sh

# 运行特定实验
python3 demo/综合实验.py
```

---

## 📚 代码风格

### Python

遵循 [PEP 8](https://pep8.org/) 规范：

- 4 空格缩进
- 函数名：`snake_case`
- 类名：`PascalCase`
- 常量：`UPPER_CASE`
- 行宽：≤ 100 字符

示例：
```python
class IndependentAgent:
    def __init__(self, config=None):
        self.config = config or DEFAULT_CONFIG
        self.decision_engine = DecisionEngine()
```

### 命名约定

- 变量：描述性名称
- 函数：动词开头（`calculate_reward`, `update_q_table`）
- 类：名词（`DecisionEngine`, `TaskExecutor`）

---

## 📖 文档

### 更新文档

修改代码时，请同步更新：

- 函数/类 docstring
- README.md（如影响使用）
- 相关教程

### Docstring 格式

```python
def calculate_utility(task, weights):
    """
    计算任务效用值

    Args:
        task (Task): 任务对象
        weights (dict): 权重配置

    Returns:
        float: 效用值 (0-100)

    Example:
        >>> weights = {'urgency': 0.35, 'importance': 0.35}
        >>> calculate_utility(task, weights)
        78.5
    """
    pass
```

---

## 🔍 Code Review

所有 PR 都需要经过 Code Review：

### 审核标准

- ✅ 代码正确性
- ✅ 代码风格
- ✅ 测试覆盖（如适用）
- ✅ 文档完整性
- ✅ 性能影响

### 反馈

审核意见会作为 PR 评论，请：
- 及时回复
- 根据意见修改
- 讨论不同观点

---

## 🎯 开发路线图

查看 [README.md](README.md#-路线图) 了解当前优先级：

### 高优先级
- Windows 桌面版
- 实际应用集成
- WebSocket 实时推送

### 中优先级
- 任务依赖图分析
- 更多学习算法
- Agent 谈判协议

欢迎认领任务！请在 Issue 中评论。

---

## 💬 交流

- **Issue**: Bug 报告、功能请求
- **Discussion**: 一般讨论、问答
- **PR**: 代码贡献

---

## 🙏 感谢

感谢所有贡献者！🎉

本项目因你而更好！

---

*最后更新：2026-03-29*
