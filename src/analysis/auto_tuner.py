#!/usr/bin/env python3
"""
自动参数调优

使用网格搜索或贝叶斯优化寻找最优配置
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from itertools import product
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.core.models import Task, Priority


class AutoTuner:
    """自动参数调优器"""
    
    def __init__(self, output_dir: str = "tuning_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict] = []
    
    def grid_search(self, param_grid: Dict[str, List], 
                    tasks: List[Task],
                    rounds: int = 5) -> Dict:
        """
        网格搜索
        
        Args:
            param_grid: 参数网格，如 {'learning_rate': [0.01, 0.1], 'epsilon': [0.1, 0.3]}
            tasks: 任务列表
            rounds: 每配置运行轮数
            
        Returns:
            Dict: 最佳配置和结果
        """
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         🔍 网格搜索 - 自动参数调优                     ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        # 生成所有参数组合
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        combinations = list(product(*values))
        
        print(f"📊 参数组合总数：{len(combinations)}")
        print(f"📁 每配置运行 {rounds} 轮")
        print(f"📈 预计总轮次：{len(combinations) * rounds}\n")
        
        best_config = None
        best_score = -float('inf')
        
        for i, combo in enumerate(combinations, 1):
            config = dict(zip(keys, combo))
            
            print(f"\n{'='*50}")
            print(f"配置 {i}/{len(combinations)}: {config}")
            print(f"{'='*50}")
            
            # 创建 Agent 并应用配置
            agent = IndependentAgent()
            self._apply_config(agent, config)
            
            # 运行评估
            score = self._evaluate(agent, tasks, rounds)
            
            result = {
                'config': config,
                'score': score,
                'timestamp': datetime.now().isoformat()
            }
            
            self.results.append(result)
            
            print(f"得分：{score:.3f}")
            
            if score > best_score:
                best_score = score
                best_config = config.copy()
                print(f"🏆 新的最佳配置！")
        
        # 保存结果
        self._save_results()
        
        # 打印最佳配置
        print("\n" + "="*60)
        print("🏆 最佳配置")
        print("="*60)
        for key, value in best_config.items():
            print(f"  {key}: {value}")
        print(f"\n最佳得分：{best_score:.3f}")
        print(f"结果已保存到：{self.output_dir}")
        
        return {
            'best_config': best_config,
            'best_score': best_score,
            'all_results': self.results
        }
    
    def _apply_config(self, agent: IndependentAgent, config: Dict):
        """应用配置到 Agent"""
        if 'learning_rate' in config:
            agent.q_learner.alpha = config['learning_rate']
        
        if 'discount_factor' in config:
            agent.q_learner.gamma = config['discount_factor']
        
        if 'exploration_rate' in config:
            agent.q_learner.epsilon = config['exploration_rate']
        
        if 'exploration_decay' in config:
            agent.q_learner.epsilon_decay = config['exploration_decay']
        
        if 'decision' in config:
            agent.decision_engine.weights = config['decision']
    
    def _evaluate(self, agent: IndependentAgent, 
                  tasks: List[Task], 
                  rounds: int) -> float:
        """评估配置"""
        total_reward = 0
        completed = 0
        total = 0
        
        for _ in range(rounds):
            for task in tasks:
                result = agent.decide_and_act()
                
                total += 1
                if result and result.get('success', False):
                    completed += 1
                    total_reward += result.get('reward', 1.0)
        
        # 综合得分：完成率 70% + 平均奖励 30%
        completion_rate = completed / total if total > 0 else 0
        avg_reward = total_reward / total if total > 0 else 0
        
        score = completion_rate * 0.7 + avg_reward * 0.3
        
        return score
    
    def _save_results(self):
        """保存结果"""
        filename = f"tuning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 结果已保存到：{filepath}")
    
    def quick_tune(self, tasks: List[Task] = None, rounds: int = 3) -> Dict:
        """快速调优（默认参数范围）"""
        if tasks is None:
            tasks = self._create_sample_tasks()
        
        param_grid = {
            'learning_rate': [0.05, 0.1, 0.2],
            'discount_factor': [0.9, 0.95, 0.99],
            'exploration_rate': [0.1, 0.3, 0.5]
        }
        
        return self.grid_search(param_grid, tasks, rounds)
    
    def _create_sample_tasks(self) -> List[Task]:
        """创建示例任务"""
        return [
            Task(id="1", name="修复显存", description="修复 ComfyUI 显存溢出", priority=10),
            Task(id="2", name="调试 pipeline", description="调试视频生成 pipeline", priority=9),
            Task(id="3", name="优化推理", description="优化模型推理速度", priority=8),
            Task(id="4", name="测试模板", description="测试新提示词模板", priority=7),
            Task(id="5", name="整理文档", description="整理项目文档", priority=6),
        ]


def demo():
    """演示"""
    print("\n🚀 自动参数调优演示\n")
    
    tuner = AutoTuner()
    tasks = tuner._create_sample_tasks()
    
    # 快速调优
    result = tuner.quick_tune(tasks, rounds=2)
    
    print("\n✅ 调优完成！")
    print(f"\n推荐配置:")
    for key, value in result['best_config'].items():
        print(f"  {key} = {value}")
    print()


if __name__ == '__main__':
    demo()
