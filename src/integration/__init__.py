#!/usr/bin/env python3
"""
实际应用集成模块

提供日常开发中的自动化功能：
- 代码格式化
- 测试运行
- 日报生成
- 任务安排
"""

from .formatter import CodeFormatter
from .test_runner import TestRunner
from .daily_report import DailyReportGenerator
from .task_scheduler import TaskScheduler
from .git_hooks import GitHooks

__all__ = [
    'CodeFormatter',
    'TestRunner',
    'DailyReportGenerator',
    'TaskScheduler',
    'GitHooks',
]
