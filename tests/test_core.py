"""
基础测试 - 验证核心功能
"""

import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.models import Task, TaskStatus, Priority
from src.core.decision import DecisionEngine
from src.learning.qlearner import SimpleQLearner, RewardShaper
from src.monitoring.monitor import SelfMonitor


class TestTask:
    """测试 Task 模型"""
    
    def test_task_creation(self):
        task = Task(
            id="test-1",
            name="测试任务",
            priority=8,
            estimated_time=60
        )
        assert task.name == "测试任务"
        assert task.priority == 8
        assert task.status == TaskStatus.PENDING
    
    def test_task_urgency(self):
        # 无截止时间
        task1 = Task(id="t1", name="任务 1", priority=5)
        assert task1.urgency == 0.5
        
        # 已逾期
        task2 = Task(
            id="t2",
            name="任务 2",
            priority=5,
            deadline=datetime.now() - timedelta(hours=1)
        )
        assert task2.urgency == 1.0
        
        # 24 小时内
        task3 = Task(
            id="t3",
            name="任务 3",
            priority=5,
            deadline=datetime.now() + timedelta(hours=12)
        )
        assert task3.urgency > 0.5


class TestDecisionEngine:
    """测试决策引擎"""
    
    def test_single_task_decision(self):
        engine = DecisionEngine()
        tasks = [
            Task(id="t1", name="任务 1", priority=5)
        ]
        
        chosen, log = engine.decide(tasks)
        assert chosen.name == "任务 1"
        assert log.chosen == "任务 1"
    
    def test_priority_decision(self):
        engine = DecisionEngine()
        tasks = [
            Task(id="t1", name="低优先", priority=3),
            Task(id="t2", name="高优先", priority=9),
        ]
        
        chosen, log = engine.decide(tasks)
        assert chosen.name == "高优先"
    
    def test_urgency_decision(self):
        engine = DecisionEngine()
        tasks = [
            Task(
                id="t1",
                name="紧急任务",
                priority=5,
                deadline=datetime.now() + timedelta(hours=1)
            ),
            Task(
                id="t2",
                name="普通任务",
                priority=5,
                deadline=datetime.now() + timedelta(days=7)
            ),
        ]
        
        chosen, log = engine.decide(tasks)
        assert chosen.name == "紧急任务"


class TestQLearner:
    """测试 Q-Learning"""
    
    def test_q_value_update(self):
        learner = SimpleQLearner(learning_rate=0.5)
        
        state = {"pending": 5}
        action = "task_1"
        reward = 1.0
        next_state = {"pending": 4}
        
        # 初始 Q 值为 0
        assert learner.get_q_value(state, action) == 0.0
        
        # 更新 Q 值
        learner.update(state, action, reward, next_state, [])
        
        # Q 值应该增加
        assert learner.get_q_value(state, action) > 0.0
    
    def test_action_selection(self):
        learner = SimpleQLearner(exploration_rate=0.0)  # 不探索
        
        state = {"pending": 3}
        actions = ["action_a", "action_b", "action_c"]
        
        # 设置不同的 Q 值
        learner.set_q_value(state, "action_a", 0.5)
        learner.set_q_value(state, "action_b", 0.8)
        learner.set_q_value(state, "action_c", 0.3)
        
        # 应该选择 Q 值最高的行动
        chosen = learner.get_best_action(state, actions)
        assert chosen == "action_b"


class TestRewardShaper:
    """测试奖励函数"""
    
    def test_on_time_completion(self):
        shaper = RewardShaper()
        
        reward = shaper.calculate_reward(
            completed=True,
            on_time=True,
            estimated_time=60,
            actual_time=50,
            priority=5
        )
        
        assert reward > 0.5
    
    def test_failed_task(self):
        shaper = RewardShaper()
        
        reward = shaper.calculate_reward(
            completed=False,
            on_time=False,
            estimated_time=60,
            actual_time=0,
            priority=5
        )
        
        assert reward < 0


class TestSelfMonitor:
    """测试自我监控"""
    
    def test_performance_recording(self):
        monitor = SelfMonitor()
        
        monitor.record_performance(
            metric_name="success_rate",
            expected=0.8,
            actual=0.9
        )
        
        stats = monitor.get_performance_summary()
        assert stats['total_records'] == 1
    
    def test_anomaly_detection(self):
        monitor = SelfMonitor()
        
        # 记录多次大偏差
        for i in range(10):
            monitor.record_performance(
                metric_name="test_metric",
                expected=1.0,
                actual=0.3  # 70% 偏差
            )
        
        assert monitor.check_anomaly("test_metric") is True
    
    def test_insight_generation(self):
        monitor = SelfMonitor()
        
        # 无异常时
        insight = monitor.generate_insight()
        assert "正常" in insight
        
        # 有异常时
        monitor.record_performance(
            metric_name="bad_metric",
            expected=1.0,
            actual=0.2  # 80% 偏差
        )
        
        insight = monitor.generate_insight()
        assert "异常" in insight


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
