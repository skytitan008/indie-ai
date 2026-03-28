"""
SARSA 学习算法

On-policy 的时序差分学习算法
与 Q-Learning 的 Off-policy 形成对比
"""

import random
import sqlite3
from pathlib import Path
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class SARSAConfig:
    """SARSA 配置"""
    learning_rate: float = 0.1      # alpha
    discount_factor: float = 0.9    # gamma
    exploration_rate: float = 0.1   # epsilon
    min_exploration: float = 0.01   # 最小探索率
    exploration_decay: float = 0.995  # 探索率衰减


class SARSALearner:
    """
    SARSA 学习器
    
    SARSA (State-Action-Reward-State-Action) 是一种 On-policy 算法
    与 Q-Learning 的区别:
    - Q-Learning: 学习最优策略（Off-policy）
    - SARSA: 学习当前策略（On-policy），更保守
    
    更新公式:
    Q(s,a) ← Q(s,a) + α[r + γQ(s',a') - Q(s,a)]
    
    其中 a' 是根据当前策略选择的下一个动作
    """
    
    def __init__(self, db_path: str = "sarsa_memory.db", config: SARSAConfig = None):
        self.config = config or SARSAConfig()
        self.alpha = self.config.learning_rate
        self.gamma = self.config.discount_factor
        self.epsilon = self.config.exploration_rate
        
        # Q 表：state -> action -> value
        self.q_table: Dict[str, Dict[str, float]] = {}
        
        # 经验回放缓冲区
        self.experience_buffer: List[Tuple] = []
        
        # 统计信息
        self.total_updates = 0
        self.total_episodes = 0
        self.episode_rewards: List[float] = []
        
        # 持久化
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS q_values (
                state TEXT,
                action TEXT,
                value REAL,
                updated_at TIMESTAMP,
                PRIMARY KEY (state, action)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_stats (
                id INTEGER PRIMARY KEY,
                total_updates INTEGER,
                total_episodes INTEGER,
                avg_reward REAL,
                exploration_rate REAL,
                updated_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_q_value(self, state: str, action: str) -> float:
        """获取 Q 值"""
        if state not in self.q_table:
            self.q_table[state] = {}
        return self.q_table[state].get(action, 0.0)
    
    def set_q_value(self, state: str, action: str, value: float):
        """设置 Q 值"""
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = value
    
    def choose_action(self, state: str, available_actions: List[str]) -> str:
        """
        使用 ε-greedy 策略选择动作
        
        SARSA 是 On-policy，所以必须使用当前策略选择动作
        """
        if random.random() < self.epsilon:
            # 探索：随机选择
            return random.choice(available_actions)
        else:
            # 利用：选择最优动作
            if state not in self.q_table:
                return random.choice(available_actions)
            
            # 获取 Q 值最大的动作
            q_values = {
                action: self.get_q_value(state, action)
                for action in available_actions
            }
            
            max_q = max(q_values.values())
            best_actions = [
                action for action, q in q_values.items()
                if q == max_q
            ]
            
            return random.choice(best_actions)
    
    def update(
        self,
        state: str,
        action: str,
        reward: float,
        next_state: str,
        next_action: str,
        available_next_actions: List[str] = None
    ):
        """
        SARSA 更新
        
        更新公式:
        Q(s,a) ← Q(s,a) + α[r + γQ(s',a') - Q(s,a)]
        
        关键：使用实际选择的下一个动作 a' 的 Q 值
        """
        current_q = self.get_q_value(state, action)
        
        # 获取下一个状态的 Q 值
        next_q = self.get_q_value(next_state, next_action)
        
        # SARSA 更新
        new_q = current_q + self.alpha * (
            reward + self.gamma * next_q - current_q
        )
        
        self.set_q_value(state, action, new_q)
        self.total_updates += 1
    
    def learn(
        self,
        state: str,
        action: str,
        reward: float,
        next_state: str,
        available_actions: List[str]
    ) -> str:
        """
        完整的 SARSA 学习步骤
        
        返回：选择的下一个动作
        """
        # 选择下一个动作（根据当前策略）
        next_action = self.choose_action(next_state, available_actions)
        
        # 更新 Q 值
        self.update(state, action, reward, next_state, next_action)
        
        # 存储经验
        self.experience_buffer.append((state, action, reward, next_state, next_action))
        
        # 限制缓冲区大小
        if len(self.experience_buffer) > 10000:
            self.experience_buffer.pop(0)
        
        return next_action
    
    def decay_exploration(self):
        """衰减探索率"""
        self.epsilon = max(
            self.config.min_exploration,
            self.epsilon * self.config.exploration_decay
        )
    
    def end_episode(self, total_reward: float):
        """结束一个 episode"""
        self.total_episodes += 1
        self.episode_rewards.append(total_reward)
        
        # 衰减探索率
        self.decay_exploration()
        
        # 保存到数据库
        self._save_stats()
    
    def _save_stats(self):
        """保存统计信息到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        avg_reward = (
            sum(self.episode_rewards[-100:]) / len(self.episode_rewards[-100:])
            if self.episode_rewards else 0
        )
        
        cursor.execute('''
            INSERT OR REPLACE INTO learning_stats
            (id, total_updates, total_episodes, avg_reward, exploration_rate, updated_at)
            VALUES (1, ?, ?, ?, ?, ?)
        ''', (
            self.total_updates,
            self.total_episodes,
            avg_reward,
            self.epsilon,
            datetime.now().isoformat()
        ))
        
        # 保存 Q 表
        for state, actions in self.q_table.items():
            for action, value in actions.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO q_values
                    (state, action, value, updated_at)
                    VALUES (?, ?, ?, ?)
                ''', (state, action, value, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def load_from_db(self):
        """从数据库加载"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 加载 Q 表
        cursor.execute('SELECT state, action, value FROM q_values')
        for row in cursor.fetchall():
            state, action, value = row
            if state not in self.q_table:
                self.q_table[state] = {}
            self.q_table[state][action] = value
        
        # 加载统计
        cursor.execute('SELECT total_updates, total_episodes, avg_reward, exploration_rate FROM learning_stats WHERE id=1')
        row = cursor.fetchone()
        if row:
            self.total_updates = row[0]
            self.total_episodes = row[1]
            # exploration_rate 不加载，保持当前值
        
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_updates': self.total_updates,
            'total_episodes': self.total_episodes,
            'q_table_size': sum(len(actions) for actions in self.q_table.values()),
            'avg_reward': (
                sum(self.episode_rewards[-100:]) / len(self.episode_rewards[-100:])
                if self.episode_rewards else 0
            ),
            'exploration_rate': self.epsilon,
            'learning_rate': self.alpha,
            'discount_factor': self.gamma
        }
    
    def compare_with_qlearning(self, ql_stats: Dict) -> Dict:
        """与 Q-Learning 对比"""
        sarsa_stats = self.get_stats()
        
        return {
            'sarsa': sarsa_stats,
            'qlearning': ql_stats,
            'comparison': {
                'updates_diff': sarsa_stats['total_updates'] - ql_stats['total_updates'],
                'q_table_diff': sarsa_stats['q_table_size'] - ql_stats['q_table_size'],
                'reward_diff': sarsa_stats['avg_reward'] - ql_stats['avg_reward'],
            }
        }
