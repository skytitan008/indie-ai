"""
AI Agent 主类

整合决策、学习、监控和记忆系统
"""

from typing import List, Dict, Optional
from datetime import datetime
import uuid

from .core.models import Task, TaskStatus, Goal, Experience, DecisionLog
from .core.decision import DecisionEngine
from .learning.qlearner import SimpleQLearner, RewardShaper
from .monitoring.monitor import SelfMonitor
from .memory.database import MemoryDatabase


class IndependentAgent:
    """
    独立思考 AI Agent
    
    整合决策、学习、监控和记忆能力的自主 Agent
    """
    
    def __init__(self, db_path: str = "ai_memory.db"):
        # 初始化各子系统
        self.decision_engine = DecisionEngine()
        self.q_learner = SimpleQLearner()
        self.reward_shaper = RewardShaper()
        self.monitor = SelfMonitor()
        self.memory = MemoryDatabase(db_path)
        
        # 当前状态
        self.current_task: Optional[Task] = None
        self.state: Dict = {}
        
        # 统计
        self.tasks_completed = 0
        self.total_reward = 0.0
        
        print("🤖 IndependentAgent 初始化完成")
    
    # ========== 核心循环 ==========
    
    def think(self) -> str:
        """
        思考：决定下一步行动
        
        返回决策理由
        """
        # 获取待处理任务
        pending_tasks = self.memory.get_pending_tasks()
        
        if not pending_tasks:
            return "没有待处理的任务"
        
        # 构建当前状态
        self.state = self._build_state(pending_tasks)
        
        # 决策引擎选择任务
        task, decision_log = self.decision_engine.decide(pending_tasks)
        
        if not task:
            return "没有可执行的任务"
        
        # 保存决策日志
        self.memory.save_decision_log(decision_log)
        
        # 更新状态
        self.current_task = task
        
        return decision_log.reasoning
    
    def act(self) -> Dict:
        """
        行动：执行当前任务
        
        返回执行结果
        """
        if not self.current_task:
            return {'success': False, 'message': '没有当前任务'}
        
        task = self.current_task
        
        # 更新任务状态
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        self.memory.save_task(task)
        
        # 模拟执行（实际应用中这里会真正执行任务）
        result = self._execute_task(task)
        
        # 更新任务状态
        if result['success']:
            task.status = TaskStatus.COMPLETED
            task.actual_time = result['actual_time']
            task.completed_at = datetime.now()
            self.tasks_completed += 1
        else:
            task.status = TaskStatus.FAILED
        
        self.memory.save_task(task)
        
        # 学习和记录经验
        self._learn_from_result(task, result)
        
        # 重置当前任务
        self.current_task = None
        
        return result
    
    def _execute_task(self, task: Task) -> Dict:
        """
        执行任务（模拟）
        
        实际应用中替换为真实执行逻辑
        """
        import random
        
        # 模拟执行时间和结果
        base_time = task.estimated_time
        actual_time = int(base_time * (0.8 + random.random() * 0.4))  # 80%-120%
        
        # 模拟成功率（高优先级任务成功率更高）
        success_rate = 0.7 + (task.priority / 10) * 0.3
        success = random.random() < success_rate
        
        # 检查是否按时完成
        on_time = True
        if task.deadline:
            on_time = datetime.now() <= task.deadline
        
        return {
            'success': success,
            'actual_time': actual_time,
            'on_time': on_time,
            'message': f"任务 '{task.name}' {'完成' if success else '失败'}"
        }
    
    # ========== 学习 ==========
    
    def _learn_from_result(self, task: Task, result: Dict):
        """从任务执行结果中学习"""
        
        # 计算奖励
        reward = self.reward_shaper.calculate_reward(
            completed=result['success'],
            on_time=result['on_time'],
            estimated_time=task.estimated_time,
            actual_time=result.get('actual_time', task.estimated_time),
            priority=task.priority
        )
        
        self.total_reward += reward
        
        # 更新决策引擎的效率数据
        self.decision_engine.update_efficiency(
            task.name,
            result['success'],
            result['on_time']
        )
        
        # 创建经验记录
        next_state = self._build_state(self.memory.get_pending_tasks())
        
        experience = Experience(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            state=self.state,
            action=task.name,
            reward=reward,
            next_state=next_state,
            lesson=self._generate_lesson(task, result, reward)
        )
        
        # 保存经验
        self.memory.save_experience(experience)
        self.q_learner.add_experience(experience)
        
        # 定期经验回放学习
        if len(self.q_learner.experience_buffer) >= 32:
            self.q_learner.replay_experience()
        
        # 记录性能
        self.monitor.record_performance(
            metric_name='task_success_rate',
            expected=0.8,
            actual=1.0 if result['success'] else 0.0,
            context=task.name
        )
    
    def _generate_lesson(self, task: Task, result: Dict, reward: float) -> str:
        """生成经验教训"""
        if result['success'] and result['on_time']:
            return f"成功按时完成，效率良好"
        elif result['success']:
            return f"完成但超时，需要优化时间估算"
        else:
            return f"任务失败，需要分析原因"
    
    # ========== 状态管理 ==========
    
    def _build_state(self, pending_tasks: List[Task]) -> Dict:
        """构建当前状态表示"""
        return {
            'pending_count': len(pending_tasks),
            'high_priority_count': sum(1 for t in pending_tasks if t.priority >= 8),
            'overdue_count': sum(1 for t in pending_tasks if t.is_overdue),
            'current_hour': datetime.now().hour,
            'tasks_completed': self.tasks_completed
        }
    
    # ========== 任务管理 ==========
    
    def add_task(
        self,
        name: str,
        priority: int = 5,
        estimated_time: int = 60,
        deadline: datetime = None,
        description: str = ""
    ) -> Task:
        """添加新任务"""
        task = Task(
            id=str(uuid.uuid4())[:8],
            name=name,
            description=description,
            priority=priority,
            estimated_time=estimated_time,
            deadline=deadline
        )
        
        self.memory.save_task(task)
        return task
    
    def add_goal(self, description: str, sub_tasks: List[str] = None) -> Goal:
        """添加目标"""
        goal = Goal(
            id=str(uuid.uuid4())[:8],
            description=description,
            sub_goals=sub_tasks or []
        )
        
        # 将子任务添加为任务
        for sub_task in sub_tasks:
            self.add_task(sub_task, description=description)
        
        return goal
    
    # ========== 监控和报告 ==========
    
    def get_status(self) -> Dict:
        """获取 Agent 状态"""
        return {
            'tasks_completed': self.tasks_completed,
            'total_reward': self.total_reward,
            'pending_tasks': len(self.memory.get_pending_tasks()),
            'decision_stats': self.decision_engine.get_stats(),
            'learning_stats': self.q_learner.get_stats(),
            'monitor_stats': self.monitor.get_performance_summary()
        }
    
    def get_reflection(self) -> str:
        """获取自我反思报告"""
        return self.monitor.generate_insight()
    
    def run_cycle(self) -> str:
        """
        运行一个完整的思考 - 行动循环
        
        返回执行摘要
        """
        # 思考
        reasoning = self.think()
        
        if "没有" in reasoning:
            return f"🤔 思考：{reasoning}"
        
        # 行动
        result = self.act()
        
        # 生成摘要
        summary = [
            f"🤔 思考：{reasoning}",
            f"⚡ 行动：{result['message']}",
        ]
        
        if result['success']:
            summary.append(f"⏱️ 耗时：{result.get('actual_time', 'N/A')} 分钟")
        
        # 添加反思（如果有）
        if self.monitor.check_anomaly():
            summary.append(f"\n{self.get_reflection()}")
        
        return "\n".join(summary)
    
    # ========== 清理 ==========
    
    def close(self):
        """关闭 Agent，释放资源"""
        self.memory.close()
        print("👋 Agent 已关闭")
