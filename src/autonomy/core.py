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
        
        # 交互模块
        self.chat_bot = ChatBot(name)
        self.tts = TextToSpeech()
        
        # 状态
        self.mode = "idle"
        self.current_task = None
        
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
