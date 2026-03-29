#!/usr/bin/env python3
"""
Deep Q-Learning 实现

使用神经网络近似 Q 值函数
支持：
- 经验回放（Experience Replay）
- 目标网络（Target Network）
- ε-贪婪探索
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque
import random
import json
from pathlib import Path
from datetime import datetime


class NeuralNetwork:
    """简单神经网络（无依赖实现）"""
    
    def __init__(self, input_size: int, hidden_sizes: List[int], output_size: int):
        self.layers = []
        self.biases = []
        
        # 初始化权重（Xavier 初始化）
        sizes = [input_size] + hidden_sizes + [output_size]
        for i in range(len(sizes) - 1):
            # Xavier 初始化
            limit = np.sqrt(6.0 / (sizes[i] + sizes[i+1]))
            weights = np.random.uniform(-limit, limit, (sizes[i], sizes[i+1]))
            bias = np.zeros((1, sizes[i+1]))
            self.layers.append(weights)
            self.biases.append(bias)
    
    def relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU 激活函数"""
        return np.maximum(0, x)
    
    def relu_derivative(self, x: np.ndarray) -> np.ndarray:
        """ReLU 导数"""
        return (x > 0).astype(float)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """前向传播"""
        self.activations = [x]
        self.z_values = []
        
        current = x
        for i, (weights, bias) in enumerate(zip(self.layers, self.biases)):
            z = np.dot(current, weights) + bias
            self.z_values.append(z)
            
            # 最后一层不用激活函数
            if i < len(self.layers) - 1:
                current = self.relu(z)
            else:
                current = z
            
            self.activations.append(current)
        
        return current
    
    def backward(self, target: np.ndarray, learning_rate: float = 0.001) -> float:
        """反向传播"""
        m = target.shape[0]  # batch size
        
        # 输出层误差
        delta = self.activations[-1] - target
        
        gradients_w = []
        gradients_b = []
        
        # 反向传播
        for i in range(len(self.layers) - 1, -1, -1):
            # 计算梯度
            grad_w = np.dot(self.activations[i].T, delta) / m
            grad_b = np.sum(delta, axis=0, keepdims=True) / m
            
            gradients_w.insert(0, grad_w)
            gradients_b.insert(0, grad_b)
            
            if i > 0:
                # 传播误差
                delta = np.dot(delta, self.layers[i].T) * self.relu_derivative(self.z_values[i-1])
        
        # 更新权重
        for i in range(len(self.layers)):
            self.layers[i] -= learning_rate * gradients_w[i]
            self.biases[i] -= learning_rate * gradients_b[i]
        
        # 返回损失（MSE）
        loss = np.mean((self.activations[-1] - target) ** 2)
        return loss
    
    def copy_weights(self) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """复制权重"""
        return [w.copy() for w in self.layers], [b.copy() for b in self.biases]
    
    def load_weights(self, weights: List[np.ndarray], biases: List[np.ndarray]):
        """加载权重"""
        self.layers = [w.copy() for w in weights]
        self.biases = [b.copy() for b in biases]


class DeepQLearner:
    """Deep Q-Learning 智能体"""
    
    def __init__(self, 
                 state_size: int,
                 action_size: int,
                 learning_rate: float = 0.001,
                 discount_factor: float = 0.95,
                 exploration_rate: float = 1.0,
                 exploration_decay: float = 0.995,
                 exploration_min: float = 0.01,
                 replay_buffer_size: int = 10000,
                 batch_size: int = 32,
                 target_update_freq: int = 100):
        
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay
        self.epsilon_min = exploration_min
        self.batch_size = batch_size
        self.target_update_freq = target_update_freq
        
        # 主网络和目标网络
        self.model = NeuralNetwork(state_size, [64, 64], action_size)
        self.target_model = NeuralNetwork(state_size, [64, 64], action_size)
        
        # 复制权重到目标网络
        weights, biases = self.model.copy_weights()
        self.target_model.load_weights(weights, biases)
        
        # 经验回放缓冲区
        self.memory = deque(maxlen=replay_buffer_size)
        
        # 统计
        self.step_count = 0
        self.total_loss = 0
        self.loss_count = 0
    
    def remember(self, state: np.ndarray, action: int, reward: float, 
                 next_state: np.ndarray, done: bool):
        """存储经验"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state: np.ndarray) -> int:
        """选择动作（ε-贪婪）"""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        q_values = self.model.forward(state.reshape(1, -1))
        return np.argmax(q_values[0])
    
    def replay(self) -> float:
        """经验回放"""
        if len(self.memory) < self.batch_size:
            return 0.0
        
        # 随机采样
        minibatch = random.sample(self.memory, self.batch_size)
        
        states = np.array([exp[0] for exp in minibatch])
        actions = np.array([exp[1] for exp in minibatch])
        rewards = np.array([exp[2] for exp in minibatch])
        next_states = np.array([exp[3] for exp in minibatch])
        dones = np.array([exp[4] for exp in minibatch])
        
        # 计算目标 Q 值
        current_q = self.model.forward(states)
        next_q = self.target_model.forward(next_states)
        
        targets = current_q.copy()
        for i in range(self.batch_size):
            if dones[i]:
                targets[i, actions[i]] = rewards[i]
            else:
                targets[i, actions[i]] = rewards[i] + self.gamma * np.max(next_q[i])
        
        # 训练
        loss = self.model.backward(targets, learning_rate=0.001)
        
        self.total_loss += loss
        self.loss_count += 1
        self.step_count += 1
        
        # 更新目标网络
        if self.step_count % self.target_update_freq == 0:
            weights, biases = self.model.copy_weights()
            self.target_model.load_weights(weights, biases)
        
        # 衰减探索率
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        return loss
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            'step_count': self.step_count,
            'epsilon': self.epsilon,
            'memory_size': len(self.memory),
            'avg_loss': self.total_loss / self.loss_count if self.loss_count > 0 else 0
        }
    
    def save(self, filepath: str):
        """保存模型"""
        data = {
            'state_size': self.state_size,
            'action_size': self.action_size,
            'epsilon': self.epsilon,
            'step_count': self.step_count,
            'weights': [w.tolist() for w in self.model.layers],
            'biases': [b.tolist() for b in self.model.biases],
            'target_weights': [w.tolist() for w in self.target_model.layers],
            'target_biases': [b.tolist() for b in self.target_model.biases],
            'saved_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ 模型已保存到：{filepath}")
    
    def load(self, filepath: str):
        """加载模型"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.epsilon = data['epsilon']
        self.step_count = data['step_count']
        
        self.model.load_weights(
            [np.array(w) for w in data['weights']],
            [np.array(b) for b in data['biases']]
        )
        
        self.target_model.load_weights(
            [np.array(w) for w in data['target_weights']],
            [np.array(b) for b in data['target_biases']]
        )
        
        print(f"✅ 模型已从 {filepath} 加载")


def demo():
    """演示 Deep Q-Learning"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 Deep Q-Learning 演示                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建环境（简单网格世界）
    state_size = 16  # 4x4 网格
    action_size = 4  # 上下左右
    
    # 创建 DQN 智能体
    dqn = DeepQLearner(
        state_size=state_size,
        action_size=action_size,
        learning_rate=0.001,
        discount_factor=0.95,
        exploration_rate=1.0,
        exploration_decay=0.995,
        replay_buffer_size=10000,
        batch_size=32,
        target_update_freq=100
    )
    
    print("📊 网络结构:")
    print(f"   输入层：{state_size}")
    print(f"   隐藏层：64 -> 64")
    print(f"   输出层：{action_size}")
    print()
    
    print("🎮 训练开始...\n")
    
    # 训练
    episodes = 100
    max_steps = 100
    
    for episode in range(1, episodes + 1):
        # 重置环境
        state = np.random.randint(0, state_size)
        state_onehot = np.zeros(state_size)
        state_onehot[state] = 1
        
        total_reward = 0
        
        for step in range(max_steps):
            # 选择动作
            action = dqn.act(state_onehot)
            
            # 执行动作（模拟）
            next_state = (state + action) % state_size
            next_state_onehot = np.zeros(state_size)
            next_state_onehot[next_state] = 1
            
            # 奖励（到达目标位置得 10 分）
            reward = 10 if next_state == state_size - 1 else -1
            done = next_state == state_size - 1
            
            # 存储经验
            dqn.remember(state_onehot, action, reward, next_state_onehot, done)
            
            # 经验回放
            dqn.replay()
            
            state = next_state
            state_onehot = next_state_onehot
            total_reward += reward
            
            if done:
                break
        
        # 打印进度
        if episode % 10 == 0:
            stats = dqn.get_stats()
            print(f"  回合 {episode:3d}/{episodes}: "
                  f"奖励 {total_reward:6.1f}, "
                  f"ε={stats['epsilon']:.3f}, "
                  f"记忆 {stats['memory_size']:5d}")
    
    # 最终统计
    print("\n📊 训练完成统计:")
    stats = dqn.get_stats()
    print(f"   总步数：{stats['step_count']}")
    print(f"   最终 ε: {stats['epsilon']:.3f}")
    print(f"   记忆大小：{stats['memory_size']}")
    print(f"   平均损失：{stats['avg_loss']:.6f}")
    
    # 保存模型
    dqn.save("deep_q_model.json")
    
    print("\n✅ Deep Q-Learning 演示完成！\n")


if __name__ == '__main__':
    demo()
