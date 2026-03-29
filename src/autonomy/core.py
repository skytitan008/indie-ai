#!/usr/bin/env python3
"""
自主进化 AI - 总控模块

整合所有能力：
- 自主学习
- 硬件控制
- 多模态交互
- 自我编程
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.learner import AutonomousLearner
from src.hardware.controller import SystemMonitor, DeviceController, FileManager, NetworkManager
from src.interaction.chat.conversation import ChatBot, ConversationManager
from src.interaction.voice.speech import TextToSpeech, VoiceInterface
from src.planning.task_planner import TaskPlanner, TaskDecomposer, TaskExecutor, TaskPriority
from src.interaction.chat.code_generator import CodeGenerator
from src.autonomy.decision import AutonomousDecisionEngine, ActionType


class AutonomousAI:
    """自主进化 AI 核心"""
    
    def __init__(self, name: str = "Indie"):
        self.name = name
        self.created_at = datetime.now()
        
        # 初始化模块
        self.learner = AutonomousLearner()
        self.monitor = SystemMonitor()
        self.devices = DeviceController()
        self.files = FileManager()
        self.network = NetworkManager()
        
        # 交互模块（传入 self 引用）
        self.chat_bot = ChatBot(name, ai_instance=self)
        self.tts = TextToSpeech()
        
        # 任务规划模块
        self.planner = TaskPlanner()
        self.decomposer = TaskDecomposer()
        self.executor = TaskExecutor(self.planner)
        
        # 代码生成器
        self.code_gen = CodeGenerator()
        
        # 自主决策引擎
        self.decision_engine = AutonomousDecisionEngine(ai_instance=self)
        
        # 自主工作执行器
        from src.autonomy.worker import AutonomousWorker
        self.worker = AutonomousWorker()
        
        # 状态
        self.mode = "idle"  # idle, autonomous, working, learning
        self.current_task = None
        self.autonomous_mode = False
        
        print(f"\n╔════════════════════════════════════════════════════════╗")
        print(f"║         🤖 {self.name} - 自主进化 AI 已启动             ║")
        print(f"╚════════════════════════════════════════════════════════╝\n")
    
    def initialize(self):
        """初始化自检"""
        print("🔍 系统自检...\n")
        
        # 检查网络
        print("   检查网络连接...")
        if self.network.check_internet():
            print("   ✅ 网络正常")
        else:
            print("   ⚠️  网络异常")
        
        # 检查系统
        print("   检查系统资源...")
        status = self.monitor.get_full_status()
        cpu_ok = status['cpu']['usage_percent'] < 90
        mem_ok = status['memory']['usage_percent'] < 90
        print(f"   {'✅' if cpu_ok else '⚠️'} CPU: {status['cpu']['usage_percent']}%")
        print(f"   {'✅' if mem_ok else '⚠️'} 内存：{status['memory']['usage_percent']}%")
        
        # 检查 GPU
        gpus = status['gpu']
        if gpus and 'error' not in gpus[0]:
            print(f"   ✅ GPU: {len(gpus)} 个")
        
        print("\n✅ 自检完成\n")
    
    def learn(self, topic: str, category: str = "general"):
        """学习新知识"""
        print(f"\n📚 {self.name} 开始学习：{topic}")
        self.mode = "learning"
        self.current_task = f"learn:{topic}"
        
        result = self.learner.learn_topic(topic, category=category)
        
        self.mode = "idle"
        self.current_task = None
        
        if result:
            print(f"   ✅ 学习完成：{topic}")
        else:
            print(f"   ⚠️  学习失败：{topic}")
        
        return result
    
    def learn_programming(self, language: str, topic: str):
        """学习编程"""
        print(f"\n💻 {self.name} 学习编程：{language} - {topic}")
        self.learner.learn_programming(language, topic)
    
    def install_skill(self, skill_name: str, functionality: str):
        """安装新技能"""
        print(f"\n🎯 {self.name} 安装技能：{skill_name}")
        self.learner.install_skill(skill_name, functionality)
    
    def capture_photo(self):
        """拍照"""
        print("\n📷 拍照...")
        result = self.devices.control_camera("capture")
        if result['status'] == 'success':
            print(f"   ✅ 照片已保存：{result.get('path', '')}")
        return result
    
    def record_audio(self, duration: int = 5):
        """录音"""
        print(f"\n🎤 录音 {duration}秒...")
        result = self.devices.control_microphone("record", duration)
        if result['status'] == 'success':
            print(f"   ✅ 录音已保存：{result.get('path', '')}")
        return result
    
    def speak(self, text: str):
        """语音合成"""
        print(f"\n🔊 {self.name} 说：{text}")
        self.tts.speak(text)
    
    def chat(self, text: str) -> str:
        """聊天"""
        return self.chat_bot.chat(text)
    
    def start_chat(self):
        """启动聊天模式"""
        self.chat_bot.start_chat()
    
    def start_voice(self):
        """启动语音模式"""
        voice = VoiceInterface()
        voice.start_voice_mode(self)
    
    def get_status(self) -> Dict:
        """获取 AI 状态"""
        return {
            'name': self.name,
            'mode': self.mode,
            'current_task': self.current_task,
            'uptime': str(datetime.now() - self.created_at),
            'learning': self.learner.get_status(),
            'system': self.monitor.get_full_status()
        }
    
    def show_status(self):
        """显示状态"""
        print("\n╔════════════════════════════════════════════════════════╗")
        print(f"║         📊 {self.name} 状态                           ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        print(f"   名称：{self.name}")
        print(f"   模式：{self.mode}")
        print(f"   运行时长：{datetime.now() - self.created_at}")
        
        # 学习状态
        learning = self.learner.get_status()
        print(f"\n   📚 知识：{learning['knowledge_count']}")
        print(f"   🎯 技能：{learning['skills_count']}")
        print(f"   📖 学习：{learning['learning_sessions']} 次")
        
        # 系统状态
        self.monitor.show_status()
    
    def self_improve(self):
        """自我改进"""
        print("\n🔄 开始自我改进...\n")
        self.mode = "self_improving"
        
        # 1. 检查已有技能
        skills = self.learner.knowledge_base.get_skills()
        print(f"   当前技能：{len(skills)} 个")
        for skill in skills:
            print(f"      • {skill['name']} v{skill['version']}")
        
        # 2. 检查知识盲区
        print("\n   分析知识盲区...")
        # TODO: 实现知识图谱分析
        
        # 3. 自动学习缺失的技能
        print("\n   自动补充技能...")
        self.install_skill("code_reviewer", "代码审查和优化")
        self.install_skill("test_generator", "自动生成测试用例")
        
        self.mode = "idle"
        print("\n✅ 自我改进完成\n")
    
    def daily_routine(self):
        """日常任务"""
        print(f"\n☀️ {self.name} 的日常任务\n")
        
        # 1. 系统检查
        print("1️⃣  系统检查")
        self.monitor.show_status()
        
        # 2. 学习新知识
        print("2️⃣  学习新知识")
        self.learn("Python best practices 2026", category="programming")
        
        # 3. 自我改进
        print("3️⃣  自我改进")
        self.self_improve()
        
        # 4. 报告状态
        print("4️⃣  状态报告")
        self.show_status()
    
    def plan_task(self, task_name: str, description: str = "", priority: str = "medium") -> int:
        """规划任务"""
        print(f"\n📋 {self.name} 规划任务：{task_name}")
        
        # 转换优先级
        priority_map = {
            'critical': TaskPriority.CRITICAL,
            'high': TaskPriority.HIGH,
            'medium': TaskPriority.MEDIUM,
            'low': TaskPriority.LOW
        }
        task_priority = priority_map.get(priority.lower(), TaskPriority.MEDIUM)
        
        # 分解任务
        subtasks = self.decomposer.decompose(task_name, description)
        
        # 创建主任务
        total_time = sum(sub.get('estimated_time', 0) for sub in subtasks)
        main_task_id = self.planner.create_task(
            name=task_name,
            description=description,
            priority=task_priority,
            estimated_time=total_time
        )
        
        # 创建子任务
        prev_task_id = None
        for subtask in subtasks:
            dependencies = [prev_task_id] if prev_task_id else []
            subtask_id = self.planner.create_task(
                name=subtask['name'],
                description=subtask['description'],
                estimated_time=subtask['estimated_time'],
                parent_id=main_task_id,
                dependencies=dependencies
            )
            self.planner.add_subtask(main_task_id, subtask_id)
            prev_task_id = subtask_id
        
        print(f"   ✅ 任务已规划：{task_name}")
        print(f"   分解为 {len(subtasks)} 个子任务")
        print(f"   预计总时间：{total_time}分钟")
        
        return main_task_id
    
    def execute_task(self, task_id: int = None) -> bool:
        """执行任务"""
        task = self.executor.execute_next()
        
        if not task:
            print("   ⏸️  没有可执行的任务")
            return False
        
        print(f"   ▶️  执行任务：{task.name}")
        
        # 模拟执行
        import time
        time.sleep(0.1)
        
        # 完成任务
        self.executor.complete_task(task.id, f"完成{task.name}")
        print(f"   ✅ 任务完成：{task.name}")
        
        return True
    
    def get_task_status(self) -> Dict:
        """获取任务状态"""
        all_tasks = self.planner.get_all_tasks()
        
        status_count = {}
        for task in all_tasks:
            status = task.status.value
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            'total': len(all_tasks),
            'by_status': status_count,
            'ready': len(self.planner.get_ready_tasks())
        }
    
    def enable_autonomous_mode(self):
        """启用自主模式"""
        self.autonomous_mode = True
        self.mode = "autonomous"
        print(f"\n🧠 {self.name} 进入自主模式")
        print("   我会自己决定做什么，你可以随时打断我\n")
    
    def disable_autonomous_mode(self):
        """禁用自主模式"""
        self.autonomous_mode = False
        self.mode = "idle"
        print(f"\n⏸️  退出自主模式\n")
    
    def think(self) -> str:
        """自主思考并决定下一步"""
        if not self.autonomous_mode:
            return "💭 思考中...（自主模式未启用）"
        
        # 自主决策
        decision = self.decision_engine.decide_next_action()
        
        # 显示思考过程
        thought = f"""💭 {self.name} 的思考:

动机状态:
   好奇心：{self.decision_engine.motivation.curiosity:.0f}
   成就感：{self.decision_engine.motivation.achievement:.0f}
   改进欲：{self.decision_engine.motivation.improvement:.0f}

决策：{decision['action'].value}
理由：{decision['reason']}
效用：{decision['utility']:.3f}

{self.decision_engine.execute_action(decision)}"""
        
        return thought
    
    def start_autonomous_work(self, goal: str) -> str:
        """开始真正的自主工作"""
        # 启动工作执行器
        self.worker.start_work(goal)
        self.mode = "working"
        self.autonomous_mode = True
        
        # 创建工作文档
        self.worker.create_document(
            "工作目标",
            f"""
## 工作目标

{goal}

## 开始时间

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 工作计划

1. 调研分析
2. 技术方案
3. 编码实现
4. 测试验证
5. 总结报告
            """
        )
        
        return f"""🚀 开始自主工作：{goal}

📁 工作目录：{self.worker.workspace}

💡 我会真正执行工作并生成文件，你可以:
   • 输入"状态"查看进度
   • 输入"工作区"查看生成的文件
   • 输入"暂停"让我停下
   • 或者继续做其他事，不用管我"""
    
    def show_workspace(self) -> str:
        """显示工作区"""
        if self.worker:
            return self.worker.show_workspace()
        return "暂无工作区"
    
    def autonomous_loop(self, iterations: int = 5):
        """自主循环（执行多次自主决策）"""
        print(f"\n🔄 开始自主循环 ({iterations}次)\n")
        
        self.enable_autonomous_mode()
        
        for i in range(iterations):
            print(f"\n[第{i+1}次决策]")
            thought = self.think()
            print(thought)
            
            import time
            time.sleep(1)  # 模拟思考时间
        
        self.disable_autonomous_mode()
        print("\n✅ 自主循环完成\n")
    
    def get_autonomy_status(self) -> Dict:
        """获取自主状态"""
        return {
            'mode': self.mode,
            'autonomous': self.autonomous_mode,
            'energy': self.decision_engine.energy,
            'motivation': self.decision_engine.motivation,
            'decisions': len(self.decision_engine.action_history),
        }


def demo():
    """演示自主进化 AI"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🤖 自主进化 AI 演示                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    
    # 初始化
    ai.initialize()
    
    # 学习
    ai.learn_programming("Python", "async await")
    
    # 安装技能
    ai.install_skill("data_analyzer", "数据分析和可视化")
    
    # 拍照
    ai.capture_photo()
    
    # 自我改进
    ai.self_improve()
    
    # 显示状态
    ai.show_status()
    
    print("\n✅ 自主进化 AI 演示完成！\n")


if __name__ == '__main__':
    demo()
