#!/usr/bin/env python3
"""
学习 10 大编程语言 - 极简版

快速学习核心知识
"""

import sys
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI

# 核心知识
LANGUAGES = [
    ('C', '系统编程基础'),
    ('Python', '通用编程语言'),
    ('Java', '企业级应用'),
    ('JavaScript', 'Web 开发'),
    ('C++', '高性能编程'),
    ('Go', '云原生语言'),
    ('Rust', '内存安全系统'),
    ('TypeScript', '类型化 JS'),
    ('C#', '微软生态'),
    ('Ruby', '优雅简洁'),
]

def main():
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎓 AI 学习 10 大编程语言                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    ai = AutonomousAI(name="小七")
    ai.initialize()
    
    print("\n开始学习...\n")
    start = time.time()
    
    for lang, desc in LANGUAGES:
        print(f"📖 {lang} - {desc}")
        ai.learner.knowledge_base.store_knowledge(
            topic=f"{lang}_basics",
            content={'language': lang, 'description': desc},
            category="programming",
            tags=[lang.lower(), 'programming']
        )
    
    elapsed = time.time() - start
    
    print(f"\n✅ 学习完成！用时：{elapsed:.1f}秒")
    print(f"\n📊 已学习 {len(LANGUAGES)} 种编程语言")
    
    ai.show_status()
    
    print("\n💡 现在可以:")
    print("   python3 xiaoqi.py  # 开始聊天")
    print("   ai.chat('帮我写个 Python 代码')  # API 调用")

if __name__ == '__main__':
    main()
