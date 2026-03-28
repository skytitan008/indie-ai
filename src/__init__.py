"""
Independent AI MVP

一个不依赖大模型的、具有基本自主决策和学习能力的 AI 系统原型
"""

from .agent import IndependentAgent
from .core.models import Task, Goal, Experience, DecisionLog
from .core.decision import DecisionEngine
from .learning.qlearner import SimpleQLearner, RewardShaper
from .monitoring.monitor import SelfMonitor
from .memory.database import MemoryDatabase

__version__ = '0.1.0'
__author__ = '老王 & 小七'

__all__ = [
    'IndependentAgent',
    'Task',
    'Goal',
    'Experience',
    'DecisionLog',
    'DecisionEngine',
    'SimpleQLearner',
    'RewardShaper',
    'SelfMonitor',
    'MemoryDatabase',
]
