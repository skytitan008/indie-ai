#!/usr/bin/env python3
"""
实验对比工具

对比不同配置下的实验结果：
- 学习率对比
- 折扣因子对比
- 探索率对比
- 决策权重对比
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import IndependentAgent
from src.core.models import Task, Priority


class ExperimentComparator:
    """实验对比器"""
    
    def __init__(self, output_dir: str = "experiments"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict] = []
    
    def run_comparison(self, configs: List[Dict], 
                       task_list: List[Task],
                       rounds: int = 10) -> Dict:
        """运行对比实验"""
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         🆚 实验对比工具                                ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        comparison_results = {
            'timestamp': datetime.now().isoformat(),
            'configs': [],
            'results': []
        }
        
        for i, config in enumerate(configs, 1):
            print(f"\n{'='*60}")
            print(f"📊 配置 {i}/{len(configs)}: {config.get('name', 'Config')}")
            print(f"{'='*60}\n")
            
            agent = self._create_agent(config)
            result = self._run_experiment(agent, task_list, rounds)
            
            config_result = {
                'name': config.get('name', f'Config_{i}'),
                'config': config,
                'result': result
            }
            
            comparison_results['configs'].append(config_result)
            self.results.append(config_result)
        
        report = self._generate_comparison_report(comparison_results)
        self._save_results(comparison_results)
        
        return comparison_results
    
    def _create_agent(self, config: Dict) -> IndependentAgent:
        """创建 Agent"""
        agent = IndependentAgent()
        
        if 'learning_rate' in config:
            agent.q_learner.alpha = config['learning_rate']
        if 'discount_factor' in config:
            agent.q_learner.gamma = config['discount_factor']
        if 'exploration_rate' in config:
            agent.q_learner.epsilon = config['exploration_rate']
        if 'decision' in config:
            agent.decision_engine.weights = config['decision']
        
        return agent
    
    def _run_experiment(self, agent: IndependentAgent, 
                       tasks: List[Task], 
                       rounds: int) -> Dict:
        """运行实验"""
        stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'total_reward': 0,
            'rewards': [],
            'completion_rates': [],
            'q_table_sizes': []
        }
        
        for round_num in range(1, rounds + 1):
            round_reward = 0
            round_completed = 0
            
            for task in tasks:
                agent.add_task(
                    name=task.name,
                    priority=task.priority,
                    estimated_time=task.estimated_time,
                    description=task.description
                )
                result = agent.run_cycle()
                
                if result:
                    round_completed += 1
                    round_reward += 1.0
                
                stats['total_tasks'] += 1
            
            stats['completed_tasks'] += round_completed
            stats['total_reward'] += round_reward
            stats['rewards'].append(round_reward)
            
            completion_rate = round_completed / len(tasks) * 100 if tasks else 0
            stats['completion_rates'].append(completion_rate)
            stats['q_table_sizes'].append(len(agent.q_learner.q_table))
            
            print(f"  轮次 {round_num}/{rounds}: "
                  f"完成率 {completion_rate:.1f}%, "
                  f"奖励 {round_reward:.1f}, "
                  f"Q 表 {len(agent.q_learner.q_table)}")
        
        stats['avg_reward'] = stats['total_reward'] / rounds if rounds > 0 else 0
        stats['avg_completion_rate'] = sum(stats['completion_rates']) / len(stats['completion_rates']) if stats['completion_rates'] else 0
        
        return stats
    
    def _generate_comparison_report(self, results: Dict) -> str:
        """生成对比报告"""
        lines = []
        lines.append("\n╔════════════════════════════════════════════════════════╗")
        lines.append("║         📊 实验对比报告                                ║")
        lines.append("╠════════════════════════════════════════════════════════╣")
        lines.append(f"║  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║")
        lines.append("╚════════════════════════════════════════════════════════╝\n")
        
        lines.append(f"{'配置名称':<20} {'完成率':<12} {'平均奖励':<12} {'Q 表大小':<12}")
        lines.append("─" * 60)
        
        for config_result in results['configs']:
            name = config_result['name'][:18]
            result = config_result['result']
            
            completion = f"{result['avg_completion_rate']:.1f}%"
            reward = f"{result['avg_reward']:.1f}"
            q_size = str(result['q_table_sizes'][-1]) if result['q_table_sizes'] else "0"
            
            lines.append(f"{name:<20} {completion:<12} {reward:<12} {q_size:<12}")
        
        lines.append("─" * 60)
        
        best_config = max(
            results['configs'],
            key=lambda x: x['result']['avg_completion_rate']
        )
        
        lines.append(f"\n🏆 最佳配置：{best_config['name']}")
        lines.append(f"   完成率：{best_config['result']['avg_completion_rate']:.1f}%")
        lines.append(f"   平均奖励：{best_config['result']['avg_reward']:.1f}")
        lines.append("\n")
        
        report = '\n'.join(lines)
        print(report)
        
        return report
    
    def _save_results(self, results: Dict):
        """保存结果"""
        filename = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 结果已保存到：{filepath}")
    
    def compare_learning_rates(self, rates: List[float] = None, **kwargs):
        """对比学习率"""
        if rates is None:
            rates = [0.01, 0.05, 0.1, 0.2, 0.5]
        
        configs = [{'name': f'LR={rate}', 'learning_rate': rate, 
                   'discount_factor': 0.95, 'exploration_rate': 0.3} 
                   for rate in rates]
        
        return self.run_comparison(configs, **kwargs)
    
    def compare_decision_weights(self, weights_list: List[Dict] = None, **kwargs):
        """对比决策权重"""
        if weights_list is None:
            weights_list = [
                {'urgency': 0.35, 'importance': 0.35, 'efficiency': 0.20, 'dependency': 0.10},
                {'urgency': 0.30, 'importance': 0.40, 'efficiency': 0.20, 'dependency': 0.10},
                {'urgency': 0.50, 'importance': 0.25, 'efficiency': 0.15, 'dependency': 0.10},
            ]
        
        names = ['Balanced', 'Quality', 'Urgent']
        configs = [{'name': name, 'learning_rate': 0.1, 'discount_factor': 0.95,
                   'exploration_rate': 0.3, 'decision': weights} 
                  for name, weights in zip(names, weights_list)]
        
        return self.run_comparison(configs, **kwargs)


def create_sample_tasks() -> List[Task]:
    """创建示例任务"""
    return [
        Task(id="1", name="修复显存", description="修复 ComfyUI 显存溢出", priority=10, estimated_time=30),
        Task(id="2", name="调试 pipeline", description="调试视频生成 pipeline", priority=9, estimated_time=45),
        Task(id="3", name="优化推理", description="优化模型推理速度", priority=8, estimated_time=60),
        Task(id="4", name="测试模板", description="测试新提示词模板", priority=7, estimated_time=30),
        Task(id="5", name="整理文档", description="整理项目文档", priority=6, estimated_time=20),
    ]


if __name__ == '__main__':
    comparator = ExperimentComparator()
    tasks = create_sample_tasks()
    
    print("\n📊 实验 1: 学习率对比")
    comparator.compare_learning_rates(task_list=tasks, rounds=3)
    
    print("\n📊 实验 2: 决策权重对比")
    comparator.compare_decision_weights(task_list=tasks, rounds=3)
