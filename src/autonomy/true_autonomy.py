#!/usr/bin/env python3
"""
真正的自主运行系统

特点：
- 用户给一个目标
- AI 自主持续运行
- 自我决策、执行、学习、进化
- 除非用户叫停，否则一直运行
"""

import threading
import time
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TrueAutonomousSystem:
    """真正的自主系统"""
    
    def __init__(self, ai_instance=None):
        self.ai = ai_instance
        self.running = False
        self.paused = False
        self.thread: Optional[threading.Thread] = None
        self.goal: str = ""
        self.start_time: Optional[datetime] = None
        self.action_count = 0
        self.learned_topics = []
        self.completed_tasks = []
        self.improvements = []
        
        # 回调函数
        self.on_action: Optional[Callable] = None
        self.on_log: Optional[Callable] = None
        
        # 运行参数
        self.report_interval = 5  # 每 5 次行动汇报一次
        self.learn_interval = 3   # 每 3 次行动学习一次
        self.improve_interval = 10  # 每 10 次行动自我改进一次
    
    def start(self, goal: str, background: bool = True):
        """启动自主运行"""
        self.goal = goal
        self.running = True
        self.paused = False
        self.start_time = datetime.now()
        self.action_count = 0
        
        self._log(f"\n🚀 开始自主运行")
        self._log(f"🎯 目标：{goal}")
        self._log(f"⏰ 时间：{self.start_time.strftime('%H:%M:%S')}")
        self._log(f"💡 模式：{'后台' if background else '前台'}运行")
        self._log(f"⚠️  输入 'stop' 随时停止\n")
        
        if background:
            # 后台线程运行
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
        else:
            # 前台运行
            self._run_loop()
    
    def stop(self):
        """停止自主运行"""
        self.running = False
        self._log(f"\n⏹️  停止自主运行")
        self._show_summary()
    
    def pause(self):
        """暂停"""
        self.paused = True
        self._log(f"\n⏸️  已暂停")
    
    def resume(self):
        """恢复"""
        self.paused = False
        self._log(f"\n▶️  已恢复")
    
    def _log(self, message: str):
        """日志输出"""
        if self.on_log:
            self.on_log(message)
        else:
            print(message)
    
    def _show_summary(self):
        """显示总结"""
        if not self.start_time:
            return
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        self._log(f"\n{'='*60}")
        self._log(f"📊 自主运行总结")
        self._log(f"{'='*60}")
        self._log(f"🎯 目标：{self.goal}")
        self._log(f"⏱️  运行时间：{elapsed:.0f}秒 ({elapsed/60:.1f}分钟)")
        self._log(f"🔢 行动次数：{self.action_count}")
        self._log(f"📚 学习主题：{len(self.learned_topics)}个")
        self._log(f"✅ 完成任务：{len(self.completed_tasks)}个")
        self._log(f"🔄 自我改进：{len(self.improvements)}个")
        
        if self.learned_topics:
            self._log(f"\n📚 学习的内容:")
            for topic in self.learned_topics[-5:]:
                self._log(f"   • {topic}")
        
        if self.completed_tasks:
            self._log(f"\n✅ 完成的任务:")
            for task in self.completed_tasks[-5:]:
                self._log(f"   • {task}")
        
        self._log(f"\n{'='*60}\n")
    
    def _run_loop(self):
        """主运行循环"""
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            
            try:
                # 执行一次自主行动
                self._execute_action()
                
                # 行动计数
                self.action_count += 1
                
                # 定期汇报
                if self.action_count % self.report_interval == 0:
                    self._report_progress()
                
                # 短暂休息（模拟思考时间）
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                self._log("\n⚠️  用户中断")
                self.stop()
                break
            except Exception as e:
                self._log(f"❌ 错误：{e}")
                time.sleep(1)
    
    def _execute_action(self):
        """执行一次自主行动"""
        if not self.ai:
            self._log("❌ 没有 AI 实例")
            return
        
        # 1. 自主决策
        if hasattr(self.ai, 'decision_engine'):
            decision = self.ai.decision_engine.decide_next_action()
        else:
            # 简单决策
            decision = self._simple_decision()
        
        action_type = decision['action']
        
        # 2. 执行行动
        result = self._perform_action(action_type, decision)
        
        # 3. 记录
        if result['success']:
            self._record_success(action_type, result)
        else:
            self._record_failure(action_type, result.get('error', ''))
        
        # 4. 回调
        if self.on_action:
            self.on_action(action_type, result)
    
    def _simple_decision(self) -> dict:
        """简单决策（没有 decision_engine 时）"""
        import random
        
        actions = ['learn', 'execute', 'create_task', 'improve']
        weights = [0.4, 0.3, 0.2, 0.1]
        
        action = random.choices(actions, weights)[0]
        
        return {
            'action': action,
            'reason': f'自主选择{action}',
            'utility': 0.5
        }
    
    def _perform_action(self, action_type, decision: dict) -> dict:
        """执行具体行动"""
        from src.autonomy.decision import ActionType
        
        # 转换为字符串
        if hasattr(action_type, 'value'):
            action_str = action_type.value
        else:
            action_str = str(action_type)
        
        self._log(f"\n[{self.action_count + 1}] 💭 思考：{decision.get('reason', '')}")
        
        try:
            if action_str == 'execute' or action_type == ActionType.EXECUTE_TASK:
                return self._action_execute()
            
            elif action_str == 'learn' or action_type == ActionType.LEARN:
                return self._action_learn()
            
            elif action_str == 'create_task' or action_type == ActionType.CREATE_TASK:
                return self._action_create_task()
            
            elif action_str == 'improve' or action_type == ActionType.SELF_IMPROVE:
                return self._action_improve()
            
            elif action_str == 'explore' or action_type == ActionType.EXPLORE:
                return self._action_explore()
            
            elif action_str == 'monitor' or action_type == ActionType.MONITOR:
                return self._action_monitor()
            
            elif action_str == 'rest' or action_type == ActionType.REST:
                return self._action_rest()
            
            else:
                return {'success': False, 'error': f'未知行动：{action_str}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _action_execute(self) -> dict:
        """执行任务"""
        if hasattr(self.ai, 'execute_task'):
            success = self.ai.execute_task()
            if success:
                self._log(f"   ✅ 执行任务")
                return {'success': True, 'type': 'execute'}
            else:
                self._log(f"   ⏸️  没有可执行任务")
                return {'success': False, 'error': 'no tasks'}
        return {'success': False, 'error': 'no execute method'}
    
    def _action_learn(self) -> dict:
        """学习"""
        topics = self._get_learning_topics()
        topic = topics[self.action_count % len(topics)]
        
        if hasattr(self.ai, 'learn'):
            self._log(f"   📚 学习：{topic}")
            self.ai.learn(topic, category="programming")
            self.learned_topics.append(topic)
            return {'success': True, 'type': 'learn', 'topic': topic}
        
        return {'success': False, 'error': 'no learn method'}
    
    def _action_create_task(self) -> dict:
        """创建任务"""
        if hasattr(self.ai, 'plan_task'):
            task_name = f"自主任务-{self.action_count}"
            self._log(f"   📋 创建任务：{task_name}")
            self.ai.plan_task(task_name, "自主创建", "low")
            return {'success': True, 'type': 'create_task'}
        return {'success': False, 'error': 'no plan_task method'}
    
    def _action_improve(self) -> dict:
        """自我改进"""
        self._log(f"   🔄 自我改进")
        if hasattr(self.ai, 'self_improve'):
            self.ai.self_improve()
            self.improvements.append(f"改进-{self.action_count}")
        return {'success': True, 'type': 'improve'}
    
    def _action_explore(self) -> dict:
        """探索"""
        areas = ["AIGC 视频", "强化学习", "深度学习", "计算机视觉", "自然语言处理"]
        area = areas[self.action_count % len(areas)]
        self._log(f"   🔍 探索：{area}")
        if hasattr(self.ai, 'learn'):
            self.ai.learn(f"{area} 基础", category="research")
            self.learned_topics.append(area)
        return {'success': True, 'type': 'explore'}
    
    def _action_monitor(self) -> dict:
        """监控"""
        self._log(f"   📊 系统监控")
        if hasattr(self.ai, 'show_status'):
            # 简化监控
            if hasattr(self.ai, 'get_task_status'):
                status = self.ai.get_task_status()
                self._log(f"      任务：{status['total']}个")
        return {'success': True, 'type': 'monitor'}
    
    def _action_rest(self) -> dict:
        """休息"""
        self._log(f"   💤 休息中...")
        time.sleep(1)
        return {'success': True, 'type': 'rest'}
    
    def _get_learning_topics(self) -> list:
        """获取学习主题列表"""
        base_topics = [
            "Python 高级特性",
            "异步编程",
            "机器学习基础",
            "深度学习",
            "视频生成技术",
            "AIGC 原理",
            "强化学习",
            "自然语言处理",
            "计算机视觉",
            "Web 开发最佳实践",
        ]
        
        # 根据目标添加相关主题
        if "视频" in self.goal:
            base_topics.extend([
                "FFmpeg 使用",
                "视频编码",
                "图像处理",
                "ComfyUI 工作流",
            ])
        
        if "编程" in self.goal or "代码" in self.goal:
            base_topics.extend([
                "代码优化",
                "设计模式",
                "测试驱动开发",
            ])
        
        return base_topics
    
    def _report_progress(self):
        """汇报进度"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        self._log(f"\n{'='*40}")
        self._log(f"📊 进度汇报 (行动#{self.action_count})")
        self._log(f"⏱️  运行：{elapsed:.0f}秒")
        self._log(f"📚 学习：{len(self.learned_topics)}个主题")
        self._log(f"✅ 任务：{len(self.completed_tasks)}个完成")
        self._log(f"🔄 改进：{len(self.improvements)}次")
        
        if hasattr(self.ai, 'get_autonomy_status'):
            status = self.ai.get_autonomy_status()
            self._log(f"⚡ 精力：{status['energy']}")
        
        self._log(f"{'='*40}\n")
    
    def _record_success(self, action_type, result: dict):
        """记录成功"""
        if result.get('type') == 'execute':
            self.completed_tasks.append(f"任务-{self.action_count}")
    
    def _record_failure(self, action_type, error: str):
        """记录失败"""
        pass  # 可以添加失败记录逻辑


def demo():
    """演示真正的自主运行"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🚀 真正的自主运行系统演示                      ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    from src.autonomy.core import AutonomousAI
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    # 创建自主系统
    auto_system = TrueAutonomousSystem(ai)
    
    # 设置日志回调
    def on_log(msg):
        print(msg)
    
    auto_system.on_log = on_log
    
    # 设置行动回调
    def on_action(action_type, result):
        pass  # 可以在这里添加自定义逻辑
    
    auto_system.on_action = on_action
    
    # 启动自主运行（10 次行动后停止）
    print("演示：运行 10 次行动\n")
    auto_system.start("演示目标", background=False)
    
    print("\n✅ 演示完成！")


if __name__ == '__main__':
    demo()
