"""
决策引擎 - 基于效用函数的自主决策

核心思想：每个行动都有一个效用值，选择效用最高的行动
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime
import uuid

from .models import Task, TaskStatus, DecisionLog, Goal


class DecisionEngine:
    """
    决策引擎
    
    基于多因素效用函数做出决策
    """
    
    def __init__(self):
        # 效用函数权重
        self.weights = {
            'urgency': 0.35,      # 紧急度
            'importance': 0.35,   # 重要性
            'efficiency': 0.20,   # 效率
            'dependency': 0.10,   # 依赖性
        }
        
        # 历史效率数据 {task_name: completion_rate}
        self.task_efficiency: Dict[str, float] = {}
        
        # 决策历史
        self.decision_history: List[DecisionLog] = []
    
    def calculate_utility(self, task: Task, current_time: datetime = None) -> float:
        """
        计算任务的综合效用值
        
        效用值越高，越应该优先执行
        """
        if current_time is None:
            current_time = datetime.now()
        
        # 1. 紧急度 (0-1)
        urgency = self._calculate_urgency(task, current_time)
        
        # 2. 重要性 (0-1)
        importance = task.priority / 10.0
        
        # 3. 效率因子 (0-1)
        efficiency = self._calculate_efficiency(task)
        
        # 4. 依赖性因子 (0-1)
        dependency = self._calculate_dependency(task)
        
        # 加权计算
        utility = (
            self.weights['urgency'] * urgency +
            self.weights['importance'] * importance +
            self.weights['efficiency'] * efficiency +
            self.weights['dependency'] * dependency
        )
        
        return utility
    
    def _calculate_urgency(self, task: Task, current_time: datetime) -> float:
        """计算紧急度"""
        if not task.deadline:
            return 0.5
        
        remaining = (task.deadline - current_time).total_seconds()
        
        if remaining <= 0:
            return 1.0  # 已逾期
        
        # 24 小时内完成度线性增长
        urgency = 1.0 - (remaining / 86400)
        return min(1.0, max(0.0, urgency))
    
    def _calculate_efficiency(self, task: Task) -> float:
        """
        计算效率因子
        
        基于历史完成率和预估时间
        """
        # 历史完成率
        history_rate = self.task_efficiency.get(task.name, 0.5)
        
        # 时间效率（短时间任务优先，减少上下文切换）
        time_factor = 1.0 if task.estimated_time <= 30 else 0.8
        
        return (history_rate + time_factor) / 2
    
    def _calculate_dependency(self, task: Task) -> float:
        """
        计算依赖性因子
        
        如果有其他任务依赖此任务，提高优先级
        """
        if not task.dependencies:
            return 0.5
        
        # 有依赖的任务优先处理
        return 0.8
    
    def decide(
        self, 
        tasks: List[Task],
        context: Dict = None
    ) -> Tuple[Optional[Task], DecisionLog]:
        """
        从任务列表中选择最优任务
        
        返回：(选中的任务，决策日志)
        """
        if not tasks:
            return None, self._create_empty_log()
        
        # 过滤可执行的任务
        available_tasks = [
            t for t in tasks 
            if t.status == TaskStatus.PENDING
        ]
        
        if not available_tasks:
            return None, self._create_empty_log()
        
        # 计算每个任务的效用值
        task_utilities: Dict[str, float] = {}
        for task in available_tasks:
            utility = self.calculate_utility(task)
            task_utilities[task.id] = utility
        
        # 选择效用最高的任务
        best_task = max(available_tasks, key=lambda t: task_utilities[t.id])
        
        # 创建决策日志
        decision_log = self._create_decision_log(
            tasks=available_tasks,
            chosen=best_task,
            utilities=task_utilities,
            context=context
        )
        
        self.decision_history.append(decision_log)
        
        return best_task, decision_log
    
    def _create_decision_log(
        self,
        tasks: List[Task],
        chosen: Task,
        utilities: Dict[str, float],
        context: Dict = None
    ) -> DecisionLog:
        """创建决策日志"""
        
        # 生成决策理由
        reasoning = self._generate_reasoning(chosen, utilities)
        
        return DecisionLog(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            situation=f"从 {len(tasks)} 个待办任务中选择",
            options=[t.name for t in tasks],
            chosen=chosen.name,
            reasoning=reasoning,
            utilities={t.name: utilities[t.id] for t in tasks},
            outcome=""
        )
    
    def _generate_reasoning(self, task: Task, utilities: Dict[str, float]) -> str:
        """生成人类可读的决策理由"""
        reasons = []
        
        # 检查紧急度
        if task.urgency > 0.7:
            reasons.append(f"任务紧急（剩余时间少）")
        
        # 检查重要性
        if task.priority >= 8:
            reasons.append(f"优先级高（{task.priority}/10）")
        
        # 检查效率
        efficiency = self.task_efficiency.get(task.name, 0.5)
        if efficiency > 0.7:
            reasons.append(f"历史完成率高（{efficiency:.0%}）")
        
        # 检查依赖性
        if task.dependencies:
            reasons.append(f"有{len(task.dependencies)}个后续依赖")
        
        if not reasons:
            reasons.append("综合效用值最高")
        
        return "；".join(reasons)
    
    def _create_empty_log(self) -> DecisionLog:
        """创建空决策日志"""
        return DecisionLog(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            situation="无可用任务",
            options=[],
            chosen="无",
            reasoning="没有待处理的任务",
            utilities={}
        )
    
    def update_efficiency(self, task_name: str, completed: bool, on_time: bool):
        """
        更新任务效率数据
        
        用于学习
        """
        # 简单指数移动平均
        current = self.task_efficiency.get(task_name, 0.5)
        
        if completed and on_time:
            new_value = current * 0.8 + 1.0 * 0.3
        elif completed:
            new_value = current * 0.8 + 0.7 * 0.3
        else:
            new_value = current * 0.8 + 0.3 * 0.3
        
        self.task_efficiency[task_name] = min(1.0, new_value)
    
    def get_stats(self) -> Dict:
        """获取决策统计"""
        return {
            'total_decisions': len(self.decision_history),
            'avg_utility': sum(
                max(log.utilities.values()) if log.utilities else 0 
                for log in self.decision_history
            ) / max(1, len(self.decision_history)),
            'task_efficiency_count': len(self.task_efficiency)
        }
