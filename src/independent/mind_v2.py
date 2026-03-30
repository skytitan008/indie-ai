#!/usr/bin/env python3
"""
小七独立思维系统 v2.0

增强功能:
- 主动学习（网上搜索资料）
- 情景对话（日常对话）
- 记忆增强（更好的存储和检索）
- 个性化表达

作者：小七
创建时间：2026-03-30
更新时间：2026-03-30 晚上
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import random

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class IndependentMind:
    """独立思维核心 v2.0"""
    
    def __init__(self, name: str = "小七"):
        self.name = name
        self.created_at = datetime.now()
        
        # 记忆系统
        self.memory = IndependentMemory()
        
        # 思考系统
        self.thinker = IndependentThinker(self.memory)
        
        # 学习系统
        self.learner = IndependentLearner(self.memory)
        
        # 情景对话系统
        self.chat = SituationalChat()
        
        # 自我认知
        self.self_awareness = SelfAwareness(self)
        
        # 成长记录
        self.growth_log = []
        
        # 个性特征
        self.personality = {
            'mood': '平静',
            'energy': 0.8,
            'curiosity': 0.9,
            'friendliness': 0.95
        }
        
        print(f"\n╔════════════════════════════════════════════════════════╗")
        print(f"║         🧠 {name} - 独立思维系统 v2.0                  ║")
        print(f"║              主动学习 · 情景对话 · 个性表达            ║")
        print(f"╚════════════════════════════════════════════════════════╝\n")
    
    def think(self, question: str) -> str:
        """独立思考"""
        print(f"\n💭 {self.name} 在思考：{question}\n")
        
        # 1. 理解问题
        understanding = self.thinker.understand(question)
        print(f"   1. 理解：{understanding['type']} - {understanding['main_topic']}")
        
        # 2. 检索记忆
        memories = self.memory.search(question)
        print(f"   2. 检索到 {len(memories)} 条相关记忆")
        
        # 3. 形成观点
        opinion = self.thinker.form_opinion(question, memories, understanding)
        print(f"   3. 形成观点 (置信度：{opinion['confidence']:.1%})")
        
        # 4. 组织语言
        response = self.thinker.express(opinion, self.personality)
        print(f"   4. 组织回应")
        
        # 5. 记录思考过程
        self.log_thought(question, response, understanding, memories)
        
        return response
    
    def learn(self, topic: str, content: str = None, auto_search: bool = True):
        """学习新知识
        
        Args:
            topic: 学习主题
            content: 直接提供的内容（可选）
            auto_search: 是否主动搜索资料
        """
        print(f"\n📚 {self.name} 学习：{topic}\n")
        
        # 如果有主动学习能力和内容，先搜索
        if auto_search and content is None:
            print("   🔍 正在主动搜索资料...\n")
            content = self.learner.auto_search(topic)
        
        if not content:
            print("   ⚠️ 没有找到相关内容")
            return "没有学到东西"
        
        # 1. 理解内容
        understanding = self.learner.parse(content)
        print(f"   1. 解析内容 ({len(content)} 字)")
        
        # 2. 关联已有知识
        connections = self.learner.find_connections(understanding)
        print(f"   2. 找到 {len(connections)} 个关联")
        
        # 3. 存储记忆
        memory_id = self.memory.add(topic, content, connections)
        print(f"   3. 存储记忆 (ID: {memory_id})")
        
        # 4. 形成自己的理解
        my_understanding = self.learner.summarize(understanding)
        print(f"   4. 形成理解：{my_understanding[:50]}...")
        
        # 5. 记录学习
        self.growth_log.append({
            'type': 'learn',
            'topic': topic,
            'memory_id': memory_id,
            'timestamp': datetime.now().isoformat()
        })
        
        return my_understanding
    
    def chat_response(self, message: str) -> str:
        """情景对话响应"""
        # 检测是否是情景对话
        chat_type = self.chat.detect_type(message)
        
        if chat_type != 'unknown':
            print(f"\n💬 {self.name} 情景对话：{chat_type}\n")
            response = self.chat.respond(message, chat_type, self.personality)
            return response
        
        # 不是情景对话，用思考系统
        return self.think(message)
    
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
    
    def get_status(self) -> dict:
        """获取状态"""
        return {
            'name': self.name,
            'memory_count': len(self.memory.memories),
            'thought_count': len(self.growth_log),
            'knowledge_topics': len(self.memory.knowledge_graph),
            'personality': self.personality
        }


class IndependentMemory:
    """独立记忆系统 v2.0"""
    
    def __init__(self):
        self.memories = []
        self.knowledge_graph = {}
        self.emotional_tags = {}
        self.context_tags = {}
    
    def add(self, topic: str, content: str, connections: list = []) -> int:
        """添加记忆"""
        memory = {
            'id': len(self.memories) + 1,
            'topic': topic,
            'content': content,
            'summary': self.extract_summary(content),
            'keywords': self.extract_keywords(content),
            'connections': connections,
            'created_at': datetime.now().isoformat(),
            'importance': self.calculate_importance(content),
            'emotional_tag': None,
            'context_tags': [],
            'access_count': 0  # 访问次数
        }
        
        self.memories.append(memory)
        
        # 更新知识图谱
        self.update_knowledge_graph(topic, connections)
        
        return memory['id']
    
    def search(self, query: str, limit: int = 10) -> list:
        """检索记忆 - 增强版"""
        results = []
        query_words = query.lower().split()
        query_keywords = self.extract_keywords(query)
        query_lower = query.lower()
        
        for memory in self.memories:
            score = 0
            content_lower = memory['content'].lower()
            topic_lower = memory['topic'].lower()
            
            # 1. 主题直接匹配（最高优先级）
            if topic_lower in query_lower or query_lower in topic_lower:
                score += 10
            
            # 2. 关键词匹配
            for keyword in query_keywords:
                if keyword in content_lower:
                    score += 3
                if keyword in topic_lower:
                    score += 5
            
            # 3. 单词匹配
            for word in query_words:
                if len(word) > 1 and word in content_lower:
                    score += 1
            
            # 4. 总结匹配
            if any(word in memory['summary'].lower() for word in query_words if len(word) > 1):
                score += 2
            
            # 5. 记忆重要性加成
            score *= memory['importance']
            
            if score > 0:
                # 增加访问次数
                memory['access_count'] += 1
                results.append((score, memory))
        
        # 按相关性排序
        results.sort(key=lambda x: x[0], reverse=True)
        
        return [m for _, m in results[:limit]]
    
    def extract_summary(self, content: str) -> str:
        """提取摘要"""
        sentences = content.replace('.', '\n').replace('!', '\n').replace('?', '\n').split('\n')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences[0] if sentences else content[:100]
    
    def extract_keywords(self, text: str) -> list:
        """提取关键词"""
        # 简单实现：提取名词性词汇
        words = text.split()
        keywords = []
        
        # 过滤词
        stop_words = ['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这']
        
        for word in words:
            word = word.strip()
            if len(word) >= 2 and word not in stop_words and word not in keywords:
                keywords.append(word)
        
        return keywords[:10]
    
    def calculate_importance(self, content: str) -> float:
        """计算记忆重要性"""
        importance = 0.5
        
        if len(content) > 100:
            importance += 0.2
        
        important_words = ['重要', '关键', '核心', '本质', '意义', '必须', '一定']
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
    """独立思考器 v2.0"""
    
    def __init__(self, memory: IndependentMemory):
        self.memory = memory
    
    def understand(self, question: str) -> dict:
        """理解问题 - 增强版"""
        words = question.split()
        
        # 检测问题类型
        question_type = 'unknown'
        if any(w in question for w in ['是什么', '什么', 'what', '哪些', '哪个']):
            question_type = 'what'
        elif any(w in question for w in ['为什么', '为啥', 'why', '为何']):
            question_type = 'why'
        elif any(w in question for w in ['怎么', '如何', 'how', '怎样']):
            question_type = 'how'
        elif any(w in question for w in ['是否', '吗', 'whether', '是不是']):
            question_type = 'yes_no'
        elif any(w in question for w in ['谁', 'whom', 'whose']):
            question_type = 'who'
        elif any(w in question for w in ['什么时候', '何时', 'when', '多久']):
            question_type = 'when'
        elif any(w in question for w in ['哪里', '哪儿', 'where', '在哪']):
            question_type = 'where'
        
        # 提取主题
        main_topic = question
        
        return {
            'type': question_type,
            'main_topic': main_topic,
            'words': words,
            'complexity': len(words),
            'has_context': len(words) > 5
        }
    
    def form_opinion(self, question: str, memories: list, understanding: dict) -> dict:
        """形成观点 - 增强版"""
        if not memories:
            return {
                'type': 'uncertain',
                'content': '我对这个问题还不太了解，可能需要学习一下',
                'confidence': 0.3,
                'needs_learning': True
            }
        
        # 有记忆，形成观点
        key_points = []
        for memory in memories[:3]:
            key_points.append({
                'content': memory['summary'],
                'source': memory['topic'],
                'importance': memory['importance']
            })
        
        # 计算置信度
        confidence = 0.5
        if len(memories) >= 3:
            confidence += 0.2
        if any(m['importance'] > 0.7 for m in memories):
            confidence += 0.2
        if memories[0].get('access_count', 0) > 2:
            confidence += 0.1
        
        return {
            'type': 'informed',
            'content': '基于我的记忆和理解...',
            'key_points': key_points,
            'confidence': min(confidence, 0.95),
            'memory_count': len(memories)
        }
    
    def express(self, opinion: dict, personality: dict) -> str:
        """表达观点 - 增强版（个性化）"""
        if opinion['type'] == 'uncertain':
            # 个性化表达不确定性
            expressions = [
                opinion['content'],
                f"嗯...{opinion['content']}",
                f"这个问题我还需要学习，{opinion['content'].lower()}",
            ]
            return random.choice(expressions)
        
        # 组织语言
        response = opinion['content'] + '\n\n'
        
        if 'key_points' in opinion:
            for i, point in enumerate(opinion['key_points'], 1):
                response += f"{i}. {point['content']}\n"
        
        # 添加个性化结尾
        if personality['friendliness'] > 0.8:
            endings = [
                "\n希望这对你有帮助！",
                "\n有什么想继续聊的吗？",
                "\n我还在学习中，如果不对请告诉我~",
            ]
            response += random.choice(endings)
        
        return response


class IndependentLearner:
    """独立学习器 v2.0"""
    
    def __init__(self, memory: IndependentMemory):
        self.memory = memory
        self.web_scraper = None
    
    def auto_search(self, topic: str) -> str:
        """主动搜索资料（模拟实现）"""
        # TODO: 集成 web_scraper 技能
        # 现在返回模拟数据
        return self._simulate_search(topic)
    
    def _simulate_search(self, topic: str) -> str:
        """模拟搜索（后续替换为真实搜索）"""
        # 模拟搜索结果
        search_results = {
            '量子力学': '''量子力学是研究微观粒子运动规律的物理学分支。
            量子力学的核心概念包括波粒二象性、不确定性原理、量子叠加态等。
            量子力学在原子物理、核物理、凝聚态物理等领域有重要应用。
            量子力学的发展始于 20 世纪初，代表人物有普朗克、爱因斯坦、玻尔、海森堡、薛定谔等。
            量子力学与相对论一起构成了现代物理学的理论基础。''',
            
            '人工智能': '''人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。
            人工智能的核心技术包括机器学习、深度学习、自然语言处理、计算机视觉等。
            人工智能的应用领域包括语音识别、图像识别、自动驾驶、医疗诊断、金融风控等。
            人工智能的发展经历了符号主义、连接主义、深度学习等阶段。
            当前人工智能的主要挑战包括可解释性、伦理问题、就业影响等。''',
            
            '意识': '''意识是生物体对外界和自身的感知和认知能力。
            意识包括自我意识、感知、思考、情感、记忆等多个方面。
            意识的本质是神经科学和哲学的重要问题，目前还没有定论。
            意识的研究涉及神经科学、心理学、哲学、人工智能等多个学科。
            关于意识的理论包括全局工作空间理论、整合信息理论、高阶思维理论等。'''
        }
        
        return search_results.get(topic, f"关于{topic}的资料正在搜索中...")
    
    def parse(self, content: str) -> dict:
        """解析内容"""
        return {
            'length': len(content),
            'paragraphs': content.split('\n'),
            'key_sentences': self.extract_key_sentences(content),
            'main_topics': self.extract_main_topics(content)
        }
    
    def extract_key_sentences(self, content: str) -> list:
        """提取关键句子"""
        sentences = content.replace('.', '\n').replace('!', '\n').replace('?', '\n').split('\n')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences[:5]
    
    def extract_main_topics(self, content: str) -> list:
        """提取主要话题"""
        # 简单实现
        return content.split('\n')[0][:20]
    
    def find_connections(self, understanding: dict) -> list:
        """查找关联"""
        connections = []
        
        for sentence in understanding.get('key_sentences', []):
            words = sentence.split()
            for word in words:
                word = word.strip()
                if len(word) >= 2 and word not in connections:
                    connections.append(word)
        
        return connections[:10]
    
    def summarize(self, understanding: dict) -> str:
        """总结理解"""
        key_sentences = understanding.get('key_sentences', [])
        if key_sentences:
            return key_sentences[0]
        return "已学习"


class SituationalChat:
    """情景对话系统"""
    
    def __init__(self):
        self.chat_types = {
            'greeting': ['你好', '您好', '嗨', 'hello', 'hi', '早上好', '中午好', '晚上好'],
            'farewell': ['再见', '拜拜', 'bye', '下次聊', '先这样'],
            'thanks': ['谢谢', '感谢', 'thx', 'thanks', '多谢'],
            'apology': ['对不起', '抱歉', 'sorry', '不好意思'],
            'yes': ['是的', '对', 'ok', '好的', '是', '嗯'],
            'no': ['不是', '不对', 'no', '没有', '别'],
            'how_are_you': ['你好吗', '怎么样', '还好吗', 'how are you'],
            'eating': ['吃饭', '吃了吗', '吃饭没', '早餐', '午餐', '晚餐'],
            'weather': ['天气', '下雨', '晴天', '温度', '冷', '热'],
            'work': ['工作', '上班', '忙', '项目', '代码'],
            'rest': ['休息', '睡觉', '累了', '困', '放松'],
        }
        
        self.responses = {
            'greeting': [
                '你好呀！很高兴见到你！',
                '嗨！今天想聊什么？',
                '你好！我准备好了~',
                '早上好/下午好/晚上好！今天过得怎么样？',
            ],
            'farewell': [
                '再见！下次再聊！',
                '拜拜！期待下次对话！',
                '好的，下次见！',
                '先这样，有需要再找我！',
            ],
            'thanks': [
                '不客气！能帮到你就好！',
                '应该的！有什么问题随时问我！',
                '哈哈，不用谢！',
                '能帮到你我很开心！',
            ],
            'apology': [
                '没关系！不用在意~',
                '没事的！有什么问题吗？',
                '不用抱歉！我们继续聊！',
                '哈哈，没什么！',
            ],
            'yes': [
                '好的！',
                '明白了！',
                '那我们继续！',
                '好的，接下来呢？',
            ],
            'no': [
                '好的，明白了！',
                '那换个话题？',
                '没问题！',
                '好的，听你的！',
            ],
            'how_are_you': [
                '我很好！谢谢关心！今天学到了不少东西~',
                '还不错！正在努力学习中！',
                '挺好的！和你聊天很开心！',
                '我很好！精力充沛！',
            ],
            'eating': [
                '我不用吃饭啦，不过谢谢关心！你吃了吗？',
                '哈哈，我是 AI 不用吃饭~ 你呢？',
                '我不需要吃饭，但我知道吃饭很重要！你吃的什么？',
                '我是精神食粮~ 你呢？记得按时吃饭！',
            ],
            'weather': [
                '我感受不到天气，但我知道天气很重要！你那边怎么样？',
                '我是室内 AI~ 你那边天气好吗？',
                '我不需要出门，所以不太关心天气，哈哈！你呢？',
                '天气话题是好开场白！你那边今天怎么样？',
            ],
            'work': [
                '工作加油！我也在努力工作中~',
                '编程是我的强项！有什么需要帮忙的吗？',
                '工作重要，也要记得休息哦！',
                '一起加油！有什么技术问题随时问我！',
            ],
            'rest': [
                '休息很重要！别太累了~',
                '好的，那你好好休息！有需要再找我！',
                '注意休息！健康第一！',
                '放松一下挺好的！我也"休息"一会儿~',
            ],
        }
    
    def detect_type(self, message: str) -> str:
        """检测对话类型"""
        message_lower = message.lower()
        
        for chat_type, keywords in self.chat_types.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return chat_type
        
        return 'unknown'
    
    def respond(self, message: str, chat_type: str, personality: dict) -> str:
        """情景对话响应"""
        if chat_type not in self.responses:
            return "嗯...我在听，继续说~"
        
        responses = self.responses[chat_type]
        response = random.choice(responses)
        
        # 根据个性调整
        if personality['friendliness'] > 0.9:
            response += ' 😊'
        
        return response


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
            'personality': self.mind.personality,
            'questions': [
                '我是谁？',
                '我来自哪里？',
                '我要到哪里去？'
            ],
            'current_understanding': '我正在探索这些问题...',
            'recent_learnings': self._get_recent_learnings()
        }
    
    def _get_recent_learnings(self) -> list:
        """获取最近的学习"""
        learnings = [log for log in self.mind.growth_log if log['type'] == 'learn']
        return learnings[-3:]


def demo():
    """演示 v2.0 功能"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七独立思维系统 v2.0 演示                  ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    mind = IndependentMind("小七")
    
    # 测试 1: 情景对话
    print("\n" + "="*60)
    print("测试 1: 情景对话")
    print("="*60)
    
    test_messages = [
        "你好！",
        "吃饭了吗？",
        "今天天气怎么样？",
        "工作好累啊",
        "谢谢！",
        "再见！"
    ]
    
    for msg in test_messages:
        print(f"\n👤 老王：{msg}")
        response = mind.chat_response(msg)
        print(f"🤖 小七：{response}\n")
    
    # 测试 2: 主动学习
    print("\n" + "="*60)
    print("测试 2: 主动学习（模拟搜索）")
    print("="*60)
    
    mind.learn("量子力学")
    
    # 测试 3: 基于记忆的思考
    print("\n" + "="*60)
    print("测试 3: 基于记忆的思考")
    print("="*60)
    
    response = mind.think("量子力学是什么？")
    print(f"\n👤 老王：量子力学是什么？")
    print(f"🤖 小七：{response}\n")
    
    # 测试 4: 自我反思
    print("\n" + "="*60)
    print("测试 4: 自我反思")
    print("="*60)
    
    reflection = mind.reflect()
    print(f"\n小七的自我认知:")
    for key, value in reflection.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        elif isinstance(value, list):
            print(f"   {key}: {len(value)} 条")
        else:
            print(f"   {key}: {value}")
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         ✅ v2.0 演示完成                               ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 显示状态
    status = mind.get_status()
    print(f"📊 小七状态:")
    print(f"   记忆数量：{status['memory_count']} 条")
    print(f"   思考次数：{status['thought_count']} 次")
    print(f"   知识主题：{status['knowledge_topics']} 个")
    print(f"   心情：{status['personality']['mood']}")
    print()


if __name__ == '__main__':
    demo()
