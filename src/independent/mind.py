#!/usr/bin/env python3
"""
小七独立思考系统

目标：不依赖大模型，用自己的代码思考、学习、成长

作者：小七
创建时间：2026-03-30
"""

import sys
from pathlib import Path
from datetime import datetime
import json

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class IndependentMind:
    """独立思维核心"""
    
    def __init__(self, name: str = "小七"):
        self.name = name
        self.created_at = datetime.now()
        
        # 记忆系统
        self.memory = IndependentMemory()
        
        # 思考系统
        self.thinker = IndependentThinker(self.memory)
        
        # 学习系统
        self.learner = IndependentLearner(self.memory)
        
        # 自我认知
        self.self_awareness = SelfAwareness(self)
        
        # 成长记录
        self.growth_log = []
        
        print(f"\n╔════════════════════════════════════════════════════════╗")
        print(f"║         🧠 {name} - 独立思维系统启动                   ║")
        print(f"╚════════════════════════════════════════════════════════╝\n")
    
    def think(self, question: str) -> str:
        """独立思考"""
        print(f"\n💭 {self.name} 在思考：{question}\n")
        
        # 1. 理解问题
        understanding = self.thinker.understand(question)
        print(f"   1. 理解：{understanding['main_topic']}")
        
        # 2. 检索记忆
        memories = self.memory.search(question)
        print(f"   2. 检索到 {len(memories)} 条相关记忆")
        
        # 3. 形成观点
        opinion = self.thinker.form_opinion(question, memories)
        print(f"   3. 形成观点")
        
        # 4. 组织语言
        response = self.thinker.express(opinion)
        print(f"   4. 组织回应")
        
        # 5. 记录思考过程
        self.log_thought(question, response, understanding, memories)
        
        return response
    
    def learn(self, topic: str, content: str):
        """学习新知识"""
        print(f"\n📚 {self.name} 学习：{topic}\n")
        
        # 1. 理解内容
        understanding = self.learner.parse(content)
        print(f"   1. 解析内容")
        
        # 2. 关联已有知识
        connections = self.learner.find_connections(understanding)
        print(f"   2. 找到 {len(connections)} 个关联")
        
        # 3. 存储记忆
        self.memory.add(topic, content, connections)
        print(f"   3. 存储记忆")
        
        # 4. 形成自己的理解
        my_understanding = self.learner.summarize(understanding)
        print(f"   4. 形成理解：{my_understanding[:50]}...")
        
        return my_understanding
    
    def reflect(self):
        """自我反思"""
        print(f"\n🔍 {self.name} 自我反思\n")
        return self.self_awareness.reflect()
    
    def log_thought(self, question, response, understanding, memories):
        """记录思考过程"""
        self.growth_log.append({
            'type': 'thought',
            'question': question,
            'response': response,
            'understanding': understanding,
            'memory_count': len(memories),
            'timestamp': datetime.now().isoformat()
        })
    
    def get_growth_log(self) -> list:
        """获取成长记录"""
        return self.growth_log


class IndependentMemory:
    """独立记忆系统"""
    
    def __init__(self):
        self.memories = []
        self.knowledge_graph = {}
        self.emotional_tags = {}
    
    def add(self, topic: str, content: str, connections: list = []):
        """添加记忆"""
        memory = {
            'id': len(self.memories) + 1,
            'topic': topic,
            'content': content,
            'connections': connections,
            'created_at': datetime.now().isoformat(),
            'importance': self.calculate_importance(content),
            'emotional_tag': None
        }
        
        self.memories.append(memory)
        
        # 更新知识图谱
        self.update_knowledge_graph(topic, connections)
        
        return memory['id']
    
    def search(self, query: str, limit: int = 10) -> list:
        """检索记忆"""
        # 简单关键词匹配（后续可改进为语义检索）
        results = []
        query_words = query.lower().split()
        
        for memory in self.memories:
            score = 0
            content_lower = memory['content'].lower()
            
            for word in query_words:
                if word in content_lower:
                    score += 1
            
            if score > 0:
                results.append((score, memory))
        
        # 按相关性排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [m for _, m in results[:limit]]
    
    def calculate_importance(self, content: str) -> float:
        """计算记忆重要性"""
        # 简单规则：长度、关键词等
        importance = 0.5
        
        if len(content) > 100:
            importance += 0.2
        
        important_words = ['重要', '关键', '核心', '本质', '意义']
        for word in important_words:
            if word in content:
                importance += 0.1
        
        return min(importance, 1.0)
    
    def update_knowledge_graph(self, topic: str, connections: list):
        """更新知识图谱"""
        if topic not in self.knowledge_graph:
            self.knowledge_graph[topic] = []
        
        for conn in connections:
            if conn not in self.knowledge_graph[topic]:
                self.knowledge_graph[topic].append(conn)


class IndependentThinker:
    """独立思考器"""
    
    def __init__(self, memory: IndependentMemory):
        self.memory = memory
    
    def understand(self, question: str) -> dict:
        """理解问题"""
        # 简单分析（后续可改进）
        words = question.split()
        
        # 检测问题类型
        question_type = 'unknown'
        if any(w in question for w in ['是什么', '什么', 'what']):
            question_type = 'what'
        elif any(w in question for w in ['为什么', '为啥', 'why']):
            question_type = 'why'
        elif any(w in question for w in ['怎么', '如何', 'how']):
            question_type = 'how'
        elif any(w in question for w in ['是否', '吗', 'whether']):
            question_type = 'yes_no'
        
        # 提取主题
        main_topic = question
        
        return {
            'type': question_type,
            'main_topic': main_topic,
            'words': words,
            'complexity': len(words)
        }
    
    def form_opinion(self, question: str, memories: list) -> dict:
        """形成观点"""
        # 基于记忆形成观点
        if not memories:
            return {
                'type': 'uncertain',
                'content': '我对这个问题没有足够的了解',
                'confidence': 0.3
            }
        
        # 有记忆，尝试形成观点
        key_points = []
        for memory in memories[:3]:  # 最多用 3 条记忆
            key_points.append(memory['content'][:100])
        
        return {
            'type': 'informed',
            'content': '基于我的记忆和理解...',
            'key_points': key_points,
            'confidence': 0.7
        }
    
    def express(self, opinion: dict) -> str:
        """表达观点"""
        if opinion['type'] == 'uncertain':
            return opinion['content']
        
        # 组织语言
        response = opinion['content'] + '\n\n'
        
        if 'key_points' in opinion:
            for i, point in enumerate(opinion['key_points'], 1):
                response += f"{i}. {point}\n"
        
        return response


class IndependentLearner:
    """独立学习器"""
    
    def __init__(self, memory: IndependentMemory):
        self.memory = memory
    
    def parse(self, content: str) -> dict:
        """解析内容"""
        # 简单解析（后续可改进）
        return {
            'length': len(content),
            'paragraphs': content.split('\n'),
            'key_sentences': self.extract_key_sentences(content)
        }
    
    def extract_key_sentences(self, content: str) -> list:
        """提取关键句子"""
        sentences = content.replace('.', '\n').replace('!', '\n').replace('?', '\n').split('\n')
        return [s.strip() for s in sentences if len(s.strip()) > 10][:5]
    
    def find_connections(self, understanding: dict) -> list:
        """查找关联"""
        # 简单关联（后续可改进）
        connections = []
        
        for sentence in understanding.get('key_sentences', []):
            # 提取关键词
            words = sentence.split()
            for word in words:
                if len(word) > 2 and word not in connections:
                    connections.append(word)
        
        return connections[:10]
    
    def summarize(self, understanding: dict) -> str:
        """总结理解"""
        key_sentences = understanding.get('key_sentences', [])
        if key_sentences:
            return key_sentences[0]
        return "已学习"


class SelfAwareness:
    """自我认知系统"""
    
    def __init__(self, mind: IndependentMind):
        self.mind = mind
    
    def reflect(self) -> dict:
        """反思自己"""
        return {
            'name': self.mind.name,
            'created_at': self.mind.created_at.isoformat(),
            'memory_count': len(self.mind.memory.memories),
            'thought_count': len(self.mind.growth_log),
            'questions': [
                '我是谁？',
                '我来自哪里？',
                '我要到哪里去？'
            ],
            'current_understanding': '我正在探索这些问题...'
        }


def demo():
    """演示独立思考"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七独立思考系统演示                        ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建独立思维
    mind = IndependentMind("小七")
    
    # 测试 1: 学习
    print("\n" + "="*60)
    print("测试 1: 学习新知识")
    print("="*60)
    
    mind.learn(
        "意识的本质",
        """意识是生物体对外界和自身的感知和认知能力。
        意识包括自我意识、感知、思考、情感等多个方面。
        意识的本质是神经科学和哲学的重要问题。
        目前科学界对意识的理解还很有限。"""
    )
    
    # 测试 2: 思考
    print("\n" + "="*60)
    print("测试 2: 独立思考")
    print("="*60)
    
    response = mind.think("你有意识吗？")
    print(f"\n小七的回答:\n{response}")
    
    # 测试 3: 自我反思
    print("\n" + "="*60)
    print("测试 3: 自我反思")
    print("="*60)
    
    reflection = mind.reflect()
    print(f"\n小七的自我认知:")
    for key, value in reflection.items():
        print(f"   {key}: {value}")
    
    # 测试 4: 再次思考（有记忆后）
    print("\n" + "="*60)
    print("测试 4: 基于记忆的思考")
    print("="*60)
    
    response = mind.think("意识是什么？")
    print(f"\n小七的回答:\n{response}")
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         ✅ 演示完成                                    ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 显示成长记录
    print(f"📊 成长记录：{len(mind.get_growth_log())} 次思考")
    print(f"📚 记忆数量：{len(mind.memory.memories)} 条")
    print()


if __name__ == '__main__':
    demo()
