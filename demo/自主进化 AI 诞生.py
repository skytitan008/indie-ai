#!/usr/bin/env python3
"""
自主进化 AI 诞生演示

见证 AI 自己学习、自己编程、自己进化！
"""

import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI


def main():
    """主演示"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 自主进化 AI 诞生演示                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("准备见证一个自主进化 AI 的诞生...\n")
    time.sleep(2)
    
    # 1. 创建 AI
    print("1️⃣  创建 AI 核心...")
    ai = AutonomousAI(name="小七")
    time.sleep(1)
    
    # 2. 初始化
    print("\n2️⃣  系统初始化...")
    ai.initialize()
    time.sleep(1)
    
    # 3. 第一次学习
    print("\n3️⃣  第一次学习...")
    ai.learn("Python programming basics", category="programming")
    time.sleep(1)
    
    # 4. 安装初始技能
    print("\n4️⃣  安装初始技能...")
    ai.install_skill("web_search", "网络搜索和信息检索")
    ai.install_skill("code_writer", "自动编写代码")
    ai.install_skill("file_manager", "文件管理和组织")
    time.sleep(1)
    
    # 5. 感知世界
    print("\n5️⃣  感知世界...")
    ai.capture_photo()
    time.sleep(1)
    
    # 6. 自我改进
    print("\n6️⃣  自我改进...")
    ai.self_improve()
    time.sleep(1)
    
    # 7. 最终状态
    print("\n7️⃣  最终状态报告...")
    ai.show_status()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎊 恭喜！自主进化 AI 已成功诞生！              ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("她现在具备以下能力:")
    print("   ✅ 自主学习 - 可以上网查找资料")
    print("   ✅ 自我编程 - 可以给自己安装新技能")
    print("   ✅ 硬件控制 - 可以控制摄像头等设备")
    print("   ✅ 系统监控 - 可以监控 CPU/GPU/内存")
    print("   ✅ 文件管理 - 可以创建和管理文件")
    print("   ✅ 自我改进 - 可以分析和提升自己")
    
    print("\n下一步:")
    print("   1. 教她更多知识")
    print("   2. 让她帮你工作")
    print("   3. 看着她不断进化...")
    
    print("\n🚀 开始和你的 AI 伙伴一起工作吧！\n")


if __name__ == '__main__':
    main()
