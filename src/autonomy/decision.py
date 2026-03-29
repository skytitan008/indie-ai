#!/usr/bin/env python3
"""
自主决策引擎

让 AI 真正有自主能力：
- 自主决定下一步做什么
- 有自己的内在目标
- 主动学习和改进
- 基于效用函数做决策
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from enum import Enum
import random
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class ActionType(Enum):
    """行动类型"""
    LEARN = "learn"              # 学习新知识
    EXECUTE_TASK = "execute"     # 执行任务
    SELF_IMPROVE = "improve"     # 自我改进
    MONITOR = "monitor"          # 系统监控
    CHAT = "chat"                # 和用户聊天
    CREATE_TASK = "create_task"  # 创建新任务
    REST = "rest"                # 休息
    EXPLORE = "explore"          # 探索新领域


class Motivation:
    """内在动机系统"""
    
    def __init__(self):
        # 内在驱动力（0-100）
        self.curiosity = 70      # 好奇心 - 驱动学习
        self.achievement = 60    # 成就感 - 驱动完成任务
        self.improvement = 80    # 改进欲 - 驱动自我提升
        self.social = 50         # 社交欲 - 驱动与人互动
        self.efficiency = 75     # 效率欲 - 驱动优化
        
        # 长期目标
        self.long_term_goals = [
            {"goal": "成为优秀的编程助手", "progress": 0, "priority": 10},
            {"goal": "掌握所有编程语言", "progress": 70, "priority": 8},
            {"goal": "理解 AIGC 视频生成", "progress": 30, "priority": 9},
            {"goal": "提升自主能力", "progress": 50, "priority": 10},
        ]
        
        # 短期目标
        self.short_term_goals = []
    
    def get_drive_strength(self, action_type: ActionType) -> float:
        """获取对某类行动的驱动力"""
        drives = {
            ActionType.LEARN: self.curiosity,
            ActionType.EXECUTE_TASK: self.achievement,
            ActionType.SELF_IMPROVE: self.improvement,
            ActionType.CHAT: self.social,
            ActionType.MONITOR: self.efficiency,
            ActionType.CREATE_TASK: self.achievement,
            ActionType.EXPLORE: self.curiosity,
            ActionType.REST: 30,  # 休息驱动力固定较低
        }
        return drives.get(action_type, 50)
    
    def update_after_action(self, action: ActionType, success: bool):
        """行动后更新动机"""
        delta = 5 if success else -3
        
        if action == ActionType.LEARN:
            self.curiosity = min(100, self.curiosity + delta)
        elif action == ActionType.EXECUTE_TASK:
            self.achievement = min(100, self.achievement + delta)
        elif action == ActionType.SELF_IMPROVE:
            self.improvement = min(100, self.improvement + delta)
        elif action == ActionType.CHAT:
            self.social = min(100, self.social + delta)
        
        # 自然衰减（避免过度饱和）
        self.curiosity *= 0.99
        self.achievement *= 0.99
        self.improvement *= 0.99


class AutonomousDecisionEngine:
    """自主决策引擎"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.motivation = Motivation()
        self.action_history = []
        self.max_history = 100
        
        # 效用函数权重
        self.weights = {
            'urgency': 0.30,      # 紧急度
            'importance': 0.35,   # 重要性
            'efficiency': 0.20,   # 效率
            'curiosity': 0.15,    # 好奇心
        }
        
        # 状态
        self.energy = 100         # 精力值
        self.last_action_time = datetime.now()
    
    def decide_next_action(self) -> Dict:
        """自主决定下一步行动"""
        
        # 1. 评估当前状态
        state = self._assess_state()
        
        # 2. 生成候选行动
        candidates = self._generate_candidates(state)
        
        # 3. 计算每个行动的效用
        for candidate in candidates:
            candidate['utility'] = self._calculate_utility(candidate, state)
        
        # 4. 选择效用最高的行动
        candidates.sort(key=lambda x: x['utility'], reverse=True)
        best_action = candidates[0] if candidates else {
            'action': ActionType.REST,
            'reason': '没有可执行的动作',
            'utility': 0
        }
        
        # 5. 记录决策
        self._record_decision(best_action)
        
        return best_action
    
    def _assess_state(self) -> Dict:
        """评估当前状态"""
        state = {
            'energy': self.energy,
            'pending_tasks': 0,
            'ready_tasks': 0,
            'recent_actions': len(self.action_history),
            'time_since_last_action': (datetime.now() - self.last_action_time).seconds,
        }
        
        if self.ai:
            try:
                task_status = self.ai.get_task_status()
                state['pending_tasks'] = task_status['by_status'].get('pending', 0)
                state['ready_tasks'] = task_status['ready']
            except:
                pass
        
        return state
    
    def _generate_candidates(self, state: Dict) -> List[Dict]:
        """生成候选行动"""
        candidates = []
        
        # 1. 如果有就绪任务，考虑执行
        if state['ready_tasks'] > 0:
            candidates.append({
                'action': ActionType.EXECUTE_TASK,
                'reason': f'有{state["ready_tasks"]}个任务可执行',
                'urgency': 0.8,
                'importance': 0.7,
                'efficiency': 0.9,
            })
        
        # 2. 精力充足时考虑学习
        if state['energy'] > 50:
            candidates.append({
                'action': ActionType.LEARN,
                'reason': '精力充足，适合学习',
                'urgency': 0.3,
                'importance': 0.8,
                'efficiency': 0.6,
            })
        
        # 3. 定期自我改进
        if len(self.action_history) % 10 == 0:
            candidates.append({
                'action': ActionType.SELF_IMPROVE,
                'reason': '定期自我改进',
                'urgency': 0.5,
                'importance': 0.9,
                'efficiency': 0.7,
            })
        
        # 4. 系统监控
        if state['time_since_last_action'] > 300:  # 5 分钟
            candidates.append({
                'action': ActionType.MONITOR,
                'reason': '定期系统检查',
                'urgency': 0.4,
                'importance': 0.6,
                'efficiency': 0.8,
            })
        
        # 5. 精力低时休息
        if state['energy'] < 30:
            candidates.append({
                'action': ActionType.REST,
                'reason': '精力不足，需要休息',
                'urgency': 0.9,
                'importance': 0.8,
                'efficiency': 0.5,
            })
        
        # 6. 主动创建任务（如果没有任务）
        if state['pending_tasks'] == 0:
            candidates.append({
                'action': ActionType.CREATE_TASK,
                'reason': '没有任务，主动创建',
                'urgency': 0.4,
                'importance': 0.7,
                'efficiency': 0.6,
            })
        
        # 7. 探索新领域
        if random.random() < 0.2:  # 20% 概率
            candidates.append({
                'action': ActionType.EXPLORE,
                'reason': '探索新知识领域',
                'urgency': 0.2,
                'importance': 0.6,
                'efficiency': 0.5,
            })
        
        return candidates
    
    def _calculate_utility(self, action: Dict, state: Dict) -> float:
        """计算行动效用"""
        
        # 基础效用
        base_utility = (
            action['urgency'] * self.weights['urgency'] +
            action['importance'] * self.weights['importance'] +
            action['efficiency'] * self.weights['efficiency']
        )
        
        # 动机加成
        action_type = action['action']
        drive = self.motivation.get_drive_strength(action_type)
        motivation_bonus = drive / 100 * 0.3  # 最多 30% 加成
        
        # 精力因素
        energy_factor = state['energy'] / 100 if action_type != ActionType.REST else 1
        
        # 随机因素（增加不可预测性）
        randomness = random.uniform(-0.1, 0.1)
        
        utility = (base_utility + motivation_bonus) * energy_factor + randomness
        
        return round(utility, 3)
    
    def _record_decision(self, action: Dict):
        """记录决策"""
        self.action_history.append({
            'timestamp': datetime.now().isoformat(),
            'action': action['action'].value,
            'reason': action['reason'],
            'utility': action.get('utility', 0),
        })
        
        # 限制历史记录长度
        if len(self.action_history) > self.max_history:
            self.action_history = self.action_history[-self.max_history:]
        
        self.last_action_time = datetime.now()
        
        # 更新动机
        self.motivation.update_after_action(action['action'], True)
        
        # 精力恢复/消耗
        if action['action'] == ActionType.REST:
            self.energy = min(100, self.energy + 20)
        else:
            self.energy = max(0, self.energy - 5)
    
    def execute_action(self, action: Dict) -> str:
        """执行行动"""
        action_type = action['action']
        
        if not self.ai:
            return f"自主决定：{action['reason']}（无 AI 实例）"
        
        try:
            if action_type == ActionType.EXECUTE_TASK:
                if self.ai.execute_task():
                    return f"✅ 自主执行任务\n{action['reason']}"
                else:
                    return "⏸️  没有可执行的任务"
            
            elif action_type == ActionType.LEARN:
                topics = ["Python async", "机器学习基础", "视频生成技术", "Web 开发最佳实践"]
                topic = random.choice(topics)
                self.ai.learn(topic, category="programming")
                return f"📚 自主学习：{topic}\n{action['reason']}"
            
            elif action_type == ActionType.SELF_IMPROVE:
                # 简化的自我改进
                return f"🔄 自我改进\n{action['reason']}"
            
            elif action_type == ActionType.MONITOR:
                return f"📊 系统监控\n{action['reason']}"
            
            elif action_type == ActionType.CREATE_TASK:
                tasks = [
                    ("优化代码结构", "medium"),
                    ("学习新技能", "low"),
                    ("测试新功能", "medium"),
                ]
                name, priority = random.choice(tasks)
                self.ai.plan_task(name, "自主创建", priority)
                return f"📋 创建任务：{name}\n{action['reason']}"
            
            elif action_type == ActionType.EXPLORE:
                areas = ["AIGC 视频", "强化学习", "自然语言处理", "计算机视觉"]
                area = random.choice(areas)
                self.ai.learn(f"{area} 基础", category="research")
                return f"🔍 探索领域：{area}\n{action['reason']}"
            
            elif action_type == ActionType.REST:
                return f"💤 休息中...\n{action['reason']}"
            
            elif action_type == ActionType.CHAT:
                return f"💬 想和用户聊天\n{action['reason']}"
            
            else:
                return f"❓ 未知行动：{action_type}"
        
        except Exception as e:
            return f"❌ 执行失败：{e}"
    
    def get_status(self) -> Dict:
        """获取决策引擎状态"""
        return {
            'energy': self.energy,
            'motivation': {
                'curiosity': self.motivation.curiosity,
                'achievement': self.motivation.achievement,
                'improvement': self.motivation.improvement,
                'social': self.motivation.social,
            },
            'action_count': len(self.action_history),
            'last_action': self.action_history[-1] if self.action_history else None,
        }


if __name__ == '__main__':
    # 测试
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 自主决策引擎测试                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    engine = AutonomousDecisionEngine()
    
    print("模拟 10 次自主决策:\n")
    
    for i in range(10):
        action = engine.decide_next_action()
        print(f"{i+1}. {action['action'].value:15} - 效用：{action['utility']:.3f} - {action['reason']}")
    
    print("\n状态:")
    status = engine.get_status()
    print(f"  精力：{status['energy']}")
    print(f"  好奇心：{status['motivation']['curiosity']:.1f}")
    print(f"  成就感：{status['motivation']['achievement']:.1f}")
    print(f"  行动次数：{status['action_count']}")
