#!/usr/bin/env python3
"""
学习 10 大编程语言

让 AI 系统学习主流编程语言：
1. C
2. Python
3. Java
4. JavaScript
5. C++
6. Go
7. Rust
8. TypeScript
9. C#
10. Ruby
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.autonomy.core import AutonomousAI


# 10 大编程语言学习大纲
LANGUAGES = {
    'C': {
        'topics': [
            'C programming basics syntax',
            'C pointers and memory management',
            'C data structures arrays lists',
            'C file I/O operations',
            'C best practices coding standards'
        ],
        'description': 'C 语言 - 系统编程基础'
    },
    'Python': {
        'topics': [
            'Python advanced features decorators generators',
            'Python async await concurrency',
            'Python data science pandas numpy',
            'Python web development flask django',
            'Python best practices PEP8'
        ],
        'description': 'Python - 通用编程语言'
    },
    'Java': {
        'topics': [
            'Java object oriented programming',
            'Java collections framework',
            'Java concurrency multithreading',
            'Java Spring framework',
            'Java best practices design patterns'
        ],
        'description': 'Java - 企业级应用'
    },
    'JavaScript': {
        'topics': [
            'JavaScript ES6 features',
            'JavaScript async promises',
            'JavaScript DOM manipulation',
            'JavaScript Node.js backend',
            'JavaScript React Vue frameworks'
        ],
        'description': 'JavaScript - Web 开发'
    },
    'C++': {
        'topics': [
            'C++ object oriented programming',
            'C++ templates generics',
            'C++ STL standard library',
            'C++ memory management smart pointers',
            'C++ modern features C++17 C++20'
        ],
        'description': 'C++ - 高性能编程'
    },
    'Go': {
        'topics': [
            'Go programming basics',
            'Go concurrency goroutines channels',
            'Go web development',
            'Go microservices',
            'Go best practices'
        ],
        'description': 'Go - 云原生语言'
    },
    'Rust': {
        'topics': [
            'Rust ownership borrowing',
            'Rust memory safety',
            'Rust async programming',
            'Rust web development',
            'Rust systems programming'
        ],
        'description': 'Rust - 内存安全系统语言'
    },
    'TypeScript': {
        'topics': [
            'TypeScript type system',
            'TypeScript advanced types',
            'TypeScript with React',
            'TypeScript Node.js',
            'TypeScript best practices'
        ],
        'description': 'TypeScript - 类型化 JavaScript'
    },
    'C#': {
        'topics': [
            'C# object oriented programming',
            'C# LINQ functional programming',
            'C# async await',
            'C# .NET framework',
            'C# Unity game development'
        ],
        'description': 'C# - 微软生态'
    },
    'Ruby': {
        'topics': [
            'Ruby programming basics',
            'Ruby object oriented features',
            'Ruby on Rails web framework',
            'Ruby metaprogramming',
            'Ruby best practices'
        ],
        'description': 'Ruby - 优雅简洁'
    }
}


def learn_all_languages(ai: AutonomousAI, max_pages: int = 3):
    """学习所有编程语言"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         📚 学习 10 大编程语言                           ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    for lang, info in LANGUAGES.items():
        print(f"\n{'='*60}")
        print(f"📖 学习：{lang} - {info['description']}")
        print(f"{'='*60}\n")
        
        for i, topic in enumerate(info['topics'], 1):
            print(f"[{i}/{len(info['topics'])}] {topic}")
            ai.learn(topic, category="programming")
        
        print(f"\n✅ {lang} 学习完成！\n")


def install_coding_skills(ai: AutonomousAI):
    """安装编程相关技能"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎯 安装编程技能                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    skills = [
        ("code_formatter", "代码格式化和美化"),
        ("code_analyzer", "代码分析和优化"),
        ("unit_test_writer", "单元测试生成"),
        ("doc_generator", "文档自动生成"),
        ("bug_finder", "Bug 检测和修复"),
        ("refactoring_tool", "代码重构工具"),
        ("performance_profiler", "性能分析工具"),
    ]
    
    for skill_name, functionality in skills:
        ai.install_skill(skill_name, functionality)


def main():
    """主函数"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎓 AI 学习 10 大编程语言                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建 AI
    ai = AutonomousAI(name="小七")
    
    # 初始化
    ai.initialize()
    
    # 安装编程技能
    install_coding_skills(ai)
    
    # 学习编程语言
    print("\n准备开始学习 10 大编程语言...\n")
    print("⚠️  提示：完整学习可能需要较长时间")
    print("   按 Ctrl+C 可以随时中断\n")
    
    try:
        learn_all_languages(ai, max_pages=2)
    except KeyboardInterrupt:
        print("\n\n⏸️  学习已中断")
    
    # 显示状态
    ai.show_status()
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎉 编程语言学习完成！                          ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("现在小七可以:")
    print("   ✅ 理解 10 大编程语言")
    print("   ✅ 帮你写代码")
    print("   ✅ 代码审查和优化")
    print("   ✅ 生成测试用例")
    print("   ✅ 编写文档")
    
    print("\n💬 输入 'chat' 开始聊天，输入 'quit' 退出\n")
    
    while True:
        try:
            cmd = input("命令：").strip().lower()
            
            if cmd in ['quit', 'exit', 'q']:
                print("小七：再见！👋")
                break
            elif cmd == 'chat':
                ai.start_chat()
            elif cmd == 'status':
                ai.show_status()
            else:
                # 直接聊天
                response = ai.chat(cmd)
                print(f"小七：{response}\n")
        except KeyboardInterrupt:
            print("\n小七：再见！👋")
            break


if __name__ == '__main__':
    main()
