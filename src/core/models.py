"""
Independent AI MVP - 核心数据模型

定义系统使用的核心数据结构
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Priority(Enum):
    """优先级"""
    LOW = 1
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 10


@dataclass
class Task:
    """
    任务定义
    
    代表一个需要完成的工作单元
    """
    id: str
    name: str
    description: str = ""
    priority: int = 5  # 1-10
    estimated_time: int = 60  # 分钟
    actual_time: Optional[int] = None
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        # 确保 priority 在有效范围内
        self.priority = max(1, min(10, self.priority))
    
    @property
    def urgency(self) -> float:
        """计算紧急度 (0-1)"""
        if not self.deadline:
            return 0.5
        remaining = (self.deadline - datetime.now()).total_seconds()
        if remaining <= 0:
            return 1.0
        # 24 小时内为高紧急度
        return min(1.0, 1.0 - (remaining / 86400))
    
    @property
    def is_overdue(self) -> bool:
        """是否已逾期"""
        if not self.deadline:
            return False
        return datetime.now() > self.deadline and self.status != TaskStatus.COMPLETED


@dataclass
class Goal:
    """
    目标定义
    
    代表一个需要达成的目标，可包含多个子目标
    """
    id: str
    description: str
    sub_goals: List[str] = field(default_factory=list)
    priority: int = 5
    deadline: Optional[datetime] = None
    progress: float = 0.0  # 0-1
    created_at: datetime = field(default_factory=datetime.now)
    
    def update_progress(self):
        """根据子目标更新进度"""
        if not self.sub_goals:
            self.progress = 1.0 if self.progress > 0 else 0.0


@dataclass
class Experience:
    """
    经验记录
    
    记录一次决策 - 行动的完整经历，用于学习
    """
    id: str
    timestamp: datetime
    state: Dict
    action: str
    reward: float  # -1 到 1
    next_state: Dict
    lesson: str = ""
    
    @property
    def is_positive(self) -> bool:
        return self.reward > 0.3
    
    @property
    def is_negative(self) -> bool:
        return self.reward < -0.3


@dataclass
class DecisionLog:
    """
    决策日志
    
    记录每次决策的详细信息
    """
    id: str
    timestamp: datetime
    situation: str
    options: List[str]
    chosen: str
    reasoning: str
    utilities: Dict[str, float] = field(default_factory=dict)
    outcome: str = ""
    
    def to_summary(self) -> str:
        return (
            f"[{self.timestamp.strftime('%H:%M:%S')}] "
            f"{self.situation}\n"
            f"  → 选择：{self.chosen}\n"
            f"  → 理由：{self.reasoning}"
        )


@dataclass
class PerformanceRecord:
    """
    性能记录
    
    记录 AI 系统的表现
    """
    timestamp: datetime
    metric_name: str
    expected: float
    actual: float
    context: str = ""
    
    @property
    def deviation(self) -> float:
        if self.expected == 0:
            return abs(self.actual)
        return abs(self.expected - self.actual) / abs(self.expected)
    
    @property
    def is_underperforming(self) -> bool:
        return self.actual < self.expected * 0.7
