"""
参数配置中心

集中管理所有可调整的参数
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class DecisionConfig:
    """决策引擎配置"""
    # 效用函数权重
    urgency_weight: float = 0.35      # 紧急度权重
    importance_weight: float = 0.35   # 重要性权重
    efficiency_weight: float = 0.20   # 效率权重
    dependency_weight: float = 0.10   # 依赖性权重
    
    def validate(self) -> bool:
        """验证权重和为 1"""
        total = (
            self.urgency_weight +
            self.importance_weight +
            self.efficiency_weight +
            self.dependency_weight
        )
        return abs(total - 1.0) < 0.001
    
    def to_dict(self) -> Dict:
        return {
            'urgency_weight': self.urgency_weight,
            'importance_weight': self.importance_weight,
            'efficiency_weight': self.efficiency_weight,
            'dependency_weight': self.dependency_weight,
        }


@dataclass
class LearningConfig:
    """学习系统配置"""
    learning_rate: float = 0.1        # α: 学习率
    discount_factor: float = 0.9      # γ: 折扣因子
    exploration_rate: float = 0.1     # ε: 探索率
    replay_batch_size: int = 32       # 经验回放批次大小
    
    def to_dict(self) -> Dict:
        return {
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor,
            'exploration_rate': self.exploration_rate,
            'replay_batch_size': self.replay_batch_size,
        }


@dataclass
class RewardConfig:
    """奖励函数配置"""
    completed_on_time: float = 1.0      # 按时完成奖励
    completed_late: float = 0.3         # 超时完成奖励
    failed: float = -0.5                # 失败惩罚
    cancelled: float = -0.3             # 取消惩罚
    early_completion_bonus: float = 0.2 # 提前完成奖励
    high_priority_multiplier: float = 1.2  # 高优先级 multiplier
    
    def to_dict(self) -> Dict:
        return {
            'completed_on_time': self.completed_on_time,
            'completed_late': self.completed_late,
            'failed': self.failed,
            'cancelled': self.cancelled,
            'early_completion_bonus': self.early_completion_bonus,
            'high_priority_multiplier': self.high_priority_multiplier,
        }


@dataclass
class MonitorConfig:
    """监控系统配置"""
    window_size: int = 10             # 分析窗口大小
    anomaly_threshold: float = 0.3    # 异常检测阈值（30% 偏差）
    underperforming_threshold: float = 0.7  # 表现不佳阈值
    
    def to_dict(self) -> Dict:
        return {
            'window_size': self.window_size,
            'anomaly_threshold': self.anomaly_threshold,
            'underperforming_threshold': self.underperforming_threshold,
        }


# ========== 预设配置方案 ==========

CONFIG_PRESETS = {
    'balanced': {
        'name': '平衡型',
        'description': '默认配置，各因素平衡考虑',
        'decision': DecisionConfig(),
        'learning': LearningConfig(),
        'reward': RewardConfig(),
        'monitor': MonitorConfig(),
    },
    
    'urgent': {
        'name': '紧急优先型',
        'description': '高度重视紧急度，适合 deadline 驱动场景',
        'decision': DecisionConfig(
            urgency_weight=0.50,
            importance_weight=0.30,
            efficiency_weight=0.15,
            dependency_weight=0.05,
        ),
        'learning': LearningConfig(),
        'reward': RewardConfig(),
        'monitor': MonitorConfig(),
    },
    
    'quality': {
        'name': '质量优先型',
        'description': '重视完成质量和效率',
        'decision': DecisionConfig(
            urgency_weight=0.25,
            importance_weight=0.40,
            efficiency_weight=0.30,
            dependency_weight=0.05,
        ),
        'learning': LearningConfig(learning_rate=0.15),
        'reward': RewardConfig(
            completed_on_time=1.2,
            early_completion_bonus=0.3,
        ),
        'monitor': MonitorConfig(),
    },
    
    'aggressive_learning': {
        'name': '激进学习型',
        'description': '高学习率，快速适应',
        'decision': DecisionConfig(),
        'learning': LearningConfig(
            learning_rate=0.3,
            exploration_rate=0.2,
        ),
        'reward': RewardConfig(),
        'monitor': MonitorConfig(),
    },
    
    'conservative': {
        'name': '保守稳健型',
        'description': '低探索率，稳定优先',
        'decision': DecisionConfig(),
        'learning': LearningConfig(
            learning_rate=0.05,
            exploration_rate=0.05,
        ),
        'reward': RewardConfig(
            failed=-0.8,  # 更重的失败惩罚
        ),
        'monitor': MonitorConfig(
            anomaly_threshold=0.2,  # 更敏感的异常检测
        ),
    },
}


def get_preset(preset_name: str) -> Dict:
    """获取预设配置"""
    if preset_name not in CONFIG_PRESETS:
        raise ValueError(f"未知配置：{preset_name}")
    return CONFIG_PRESETS[preset_name]


def print_preset_info():
    """打印所有预设配置信息"""
    print("\n" + "="*60)
    print("📊 可用配置预设")
    print("="*60)
    
    for name, config in CONFIG_PRESETS.items():
        print(f"\n🔹 {config['name']} ({name})")
        print(f"   {config['description']}")
        
        dec = config['decision']
        print(f"   决策权重：紧急{dec.urgency_weight:.2f} | "
              f"重要{dec.importance_weight:.2f} | "
              f"效率{dec.efficiency_weight:.2f} | "
              f"依赖{dec.dependency_weight:.2f}")
        
        learn = config['learning']
        print(f"   学习参数：α={learn.learning_rate:.2f} | "
              f"γ={learn.discount_factor:.2f} | "
              f"ε={learn.exploration_rate:.2f}")
    
    print("\n" + "="*60)
