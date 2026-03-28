"""
Q-Learning 学习系统

简单的强化学习实现，用于从经验中学习
"""

from typing import Dict, Tuple, List, Optional
import random
import json
from datetime import datetime

from ..core.models import Experience


class SimpleQLearner:
    """
    简化版 Q-Learning 实现
    
    用于从决策 - 行动经验中学习
    """
    
    def __init__(
        self, 
        learning_rate: float = 0.1, 
        discount_factor: float = 0.9,
        exploration_rate: float = 0.1
    ):
        self.alpha = learning_rate  # 学习率
        self.gamma = discount_factor  # 折扣因子
        self.epsilon = exploration_rate  # 探索率
        
        # Q 表：state -> action -> value
        self.q_table: Dict[str, Dict[str, float]] = {}
        
        # 经验回放缓冲区
        self.experience_buffer: List[Experience] = []
        self.max_buffer_size = 1000
        
        # 学习统计
        self.total_updates = 0
        self.total_rewards = 0.0
    
    def state_to_key(self, state: Dict) -> str:
        """将状态字典转换为字符串键"""
        return json.dumps(state, sort_keys=True)
    
    def get_q_value(self, state: Dict, action: str) -> float:
        """获取 Q 值"""
        state_key = self.state_to_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        return self.q_table[state_key].get(action, 0.0)
    
    def set_q_value(self, state: Dict, action: str, value: float):
        """设置 Q 值"""
        state_key = self.state_to_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action] = value
    
    def get_available_actions(self, state: Dict) -> List[str]:
        """获取状态可用的行动列表"""
        state_key = self.state_to_key(state)
        if state_key not in self.q_table:
            return []
        return list(self.q_table[state_key].keys())
    
    def choose_action(
        self, 
        state: Dict, 
        available_actions: List[str]
    ) -> str:
        """
        选择行动（ε-greedy 策略）
        
        大部分时间选择最优行动，小概率随机探索
        """
        if random.random() < self.epsilon:
            # 探索：随机选择
            return random.choice(available_actions)
        
        # 利用：选择 Q 值最高的行动
        if not available_actions:
            return None
        
        q_values = {
            action: self.get_q_value(state, action)
            for action in available_actions
        }
        
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        
        return random.choice(best_actions)
    
    def update(
        self, 
        state: Dict, 
        action: str, 
        reward: float, 
        next_state: Dict,
        next_actions: List[str]
    ):
        """
        更新 Q 值
        
        Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
        """
        current_q = self.get_q_value(state, action)
        
        # 估计下一状态的最大 Q 值
        if next_actions:
            next_max_q = max(
                self.get_q_value(next_state, a) 
                for a in next_actions
            )
        else:
            next_max_q = 0.0
        
        # Q-Learning 更新公式
        new_q = current_q + self.alpha * (
            reward + self.gamma * next_max_q - current_q
        )
        
        self.set_q_value(state, action, new_q)
        
        # 更新统计
        self.total_updates += 1
        self.total_rewards += reward
    
    def add_experience(self, experience: Experience):
        """添加经验到回放缓冲区"""
        self.experience_buffer.append(experience)
        
        # 限制缓冲区大小
        if len(self.experience_buffer) > self.max_buffer_size:
            self.experience_buffer.pop(0)
    
    def replay_experience(self, batch_size: int = 32):
        """
        从经验回放中学习
        
        随机采样历史经验进行批量学习
        """
        if len(self.experience_buffer) < batch_size:
            return 0
        
        # 随机采样
        batch = random.sample(self.experience_buffer, batch_size)
        
        total_loss = 0.0
        for exp in batch:
            # 从经验中提取学习数据
            state = exp.state
            action = exp.action
            reward = exp.reward
            next_state = exp.next_state
            
            # 获取下一状态的可用行动
            next_actions = self.get_available_actions(next_state)
            
            # 更新 Q 值
            old_q = self.get_q_value(state, action)
            self.update(state, action, reward, next_state, next_actions)
            new_q = self.get_q_value(state, action)
            
            total_loss += abs(new_q - old_q)
        
        return total_loss / batch_size
    
    def get_best_action(self, state: Dict, available_actions: List[str]) -> str:
        """获取最优行动（不探索）"""
        if not available_actions:
            return None
        
        q_values = {
            action: self.get_q_value(state, action)
            for action in available_actions
        }
        
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        
        return best_actions[0]
    
    def get_stats(self) -> Dict:
        """获取学习统计"""
        return {
            'q_table_size': len(self.q_table),
            'total_updates': self.total_updates,
            'avg_reward': self.total_rewards / max(1, self.total_updates),
            'experience_buffer_size': len(self.experience_buffer),
            'exploration_rate': self.epsilon
        }
    
    def save(self, filepath: str):
        """保存 Q 表到文件"""
        data = {
            'q_table': self.q_table,
            'stats': {
                'total_updates': self.total_updates,
                'total_rewards': self.total_rewards
            }
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filepath: str):
        """从文件加载 Q 表"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.q_table = data['q_table']
        self.total_updates = data['stats'].get('total_updates', 0)
        self.total_rewards = data['stats'].get('total_rewards', 0.0)


class RewardShaper:
    """
    奖励函数设计器
    
    将任务执行结果转换为强化学习的奖励信号
    """
    
    def __init__(self):
        # 奖励配置
        self.rewards = {
            'completed_on_time': 1.0,      # 按时完成
            'completed_late': 0.3,         # 完成但超时
            'failed': -0.5,                # 失败
            'cancelled': -0.3,             # 取消
            'early_completion_bonus': 0.2, # 提前完成奖励
        }
    
    def calculate_reward(
        self,
        completed: bool,
        on_time: bool,
        estimated_time: int,
        actual_time: int,
        priority: int = 5
    ) -> float:
        """
        计算奖励值
        
        考虑完成状态、时间、优先级等因素
        """
        if not completed:
            return self.rewards['failed']
        
        # 基础奖励
        if on_time:
            reward = self.rewards['completed_on_time']
        else:
            reward = self.rewards['completed_late']
        
        # 提前完成奖励
        if actual_time < estimated_time * 0.8:
            reward += self.rewards['early_completion_bonus']
        
        # 高优先级任务额外奖励
        if priority >= 8:
            reward *= 1.2
        
        return max(-1.0, min(1.0, reward))
