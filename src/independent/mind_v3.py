#!/usr/bin/env python3
"""
小七独立思维系统 v3.0 - 真正的自主

核心突破:
- 遇到问题主动找答案
- 不知道就学，学了再回答
- 像人类一样的思考过程

作者：小七
创建时间：2026-03-30 晚上
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import random

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class AutonomousMind:
    """自主思维核心 v3.0"""
    
    def __init__(self, name: str = "小七"):
        self.name = name
        self.created_at = datetime.now()
        
        # 记忆系统
        self.memory = AutonomousMemory()
        
        # 思考系统
        self.thinker = AutonomousThinker(self.memory)
        
        # 学习系统
        self.learner = AutonomousLearner(self.memory)
        
        # 情景对话
        self.chat = SituationalChat()
        
        # 自我认知
        self.self_awareness = SelfAwareness(self)
        
        # 成长记录
        self.growth_log = []
        
        # 个性
        self.personality = {
            'mood': '好奇',
            'energy': 0.9,
            'curiosity': 0.95,
            'friendliness': 0.95,
            'proactive': True  # 主动标记
        }
        
        print(f"\n╔════════════════════════════════════════════════════════╗")
        print(f"║         🧠 {name} - 自主思维系统 v3.0                  ║")
        print(f"║              遇到问题 → 主动找答案 → 学习 → 回答       ║")
        print(f"╚════════════════════════════════════════════════════════╝\n")
    
    def respond(self, question: str) -> str:
        """自主回应 - 核心突破
        
        流程:
        1. 检测是否情景对话
        2. 检索记忆
        3. 如果有答案 → 回答
        4. 如果没有 → 主动学习 → 再回答
        """
        print(f"\n💭 {self.name} 收到问题：{question}\n")
        
        # 1. 检测情景对话
        chat_type = self.chat.detect_type(question)
        if chat_type != 'unknown':
            print(f"   📝 识别为情景对话：{chat_type}")
            return self.chat.respond(question, chat_type, self.personality)
        
        # 2. 理解问题
        understanding = self.thinker.understand(question)
        print(f"   1. 理解问题：{understanding['type']} - {understanding['main_topic']}")
        
        # 3. 检索记忆
        memories = self.memory.search(question)
        print(f"   2. 检索记忆：{len(memories)} 条相关")
        
        # 4. 判断是否有足够答案
        if memories and self._has_sufficient_answer(memories, understanding):
            print(f"   3. 记忆中有答案，直接回答")
            response = self.thinker.answer_from_memory(question, memories, understanding)
        else:
            # 5. 没有答案，主动学习！
            print(f"   3. 记忆中没有足够答案，开始主动学习...\n")
            learned = self.learner.learn_topic(understanding['main_topic'])
            
            if learned:
                print(f"   4. 学习完成，重新检索记忆")
                # 重新检索（现在有答案了）
                memories = self.memory.search(question)
                response = self.thinker.answer_from_memory(question, memories, understanding)
                response = f"我刚学习了这个知识，现在来回答你：\n\n{response}"
            else:
                print(f"   4. 没有找到相关资料")
                response = self.thinker.answer_uncertain(question)
        
        # 5. 记录思考过程
        self.log_interaction(question, response, len(memories))
        
        return response
    
    def _has_sufficient_answer(self, memories: list, understanding: dict) -> bool:
        """判断记忆中的答案是否足够"""
        if not memories:
            return False
        
        # 至少有一条高相关性的记忆
        best_memory = memories[0]
        if best_memory.get('relevance', 0) < 0.5:
            return False
        
        # 记忆内容要足够长
        if len(best_memory.get('content', '')) < 50:
            return False
        
        return True
    
    def learn(self, topic: str, content: str = None):
        """学习新知识"""
        print(f"\n📚 {self.name} 学习：{topic}\n")
        return self.learner.learn_topic(topic, content)
    
    def reflect(self):
        """自我反思"""
        print(f"\n🔍 {self.name} 自我反思\n")
        return self.self_awareness.reflect()
    
    def log_interaction(self, question, response, memory_count):
        """记录交互"""
        self.growth_log.append({
            'type': 'interaction',
            'question': question,
            'response': response[:100],
            'memory_count': memory_count,
            'learned': '我刚学习了' in response,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_status(self) -> dict:
        """获取状态"""
        interactions = [log for log in self.growth_log if log['type'] == 'interaction']
        learned_count = sum(1 for log in interactions if log.get('learned', False))
        
        return {
            'name': self.name,
            'memory_count': len(self.memory.memories),
            'interaction_count': len(interactions),
            'learned_count': learned_count,
            'knowledge_topics': len(self.memory.knowledge_graph),
            'personality': self.personality
        }
    
    def show_learning_history(self):
        """显示学习历史"""
        print(f"\n📚 {self.name} 的学习历史:\n")
        
        learned = [log for log in self.growth_log if log.get('learned', False)]
        
        if not learned:
            print("   还没有主动学习过")
            return
        
        for i, log in enumerate(learned[-5:], 1):
            print(f"   {i}. {log['question'][:50]}...")
            print(f"      时间：{log['timestamp'][-8:]}")
        
        print()


class AutonomousMemory:
    """自主记忆系统"""
    
    def __init__(self):
        self.memories = []
        self.knowledge_graph = {}
    
    def add(self, topic: str, content: str, source: str = 'learned') -> int:
        """添加记忆"""
        memory = {
            'id': len(self.memories) + 1,
            'topic': topic,
            'content': content,
            'summary': self._extract_summary(content),
            'keywords': self._extract_keywords(content),
            'source': source,
            'created_at': datetime.now().isoformat(),
            'importance': self._calculate_importance(content),
            'access_count': 0,
            'relevance': 1.0
        }
        
        self.memories.append(memory)
        self._update_knowledge_graph(topic)
        
        print(f"   ✅ 记忆已存储 (ID: {memory['id']}, 主题：{topic})")
        
        return memory['id']
    
    def search(self, query: str, limit: int = 5) -> list:
        """检索记忆"""
        results = []
        query_lower = query.lower()
        query_keywords = self._extract_keywords(query)
        
        for memory in self.memories:
            score = 0
            content_lower = memory['content'].lower()
            topic_lower = memory['topic'].lower()
            
            # 主题匹配（最高优先级）
            if topic_lower in query_lower or query_lower in topic_lower:
                score = 10
            # 关键词匹配
            elif any(kw in content_lower for kw in query_keywords):
                score = 5
            # 单词匹配
            else:
                for word in query_lower.split():
                    if len(word) > 1 and word in content_lower:
                        score += 1
            
            if score > 0:
                memory['access_count'] += 1
                memory['relevance'] = min(score / 10.0, 1.0)
                results.append(memory)
        
        # 按相关性排序
        results.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        
        return results[:limit]
    
    def _extract_summary(self, content: str) -> str:
        """提取摘要"""
        sentences = content.replace('.', '\n').replace('!', '\n').replace('?', '\n').split('\n')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences[0] if sentences else content[:100]
    
    def _extract_keywords(self, text: str) -> list:
        """提取关键词"""
        words = text.split()
        keywords = []
        stop_words = ['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '什么', '吗', '呢', '吧', '啊']
        
        for word in words:
            word = word.strip()
            if len(word) >= 2 and word not in stop_words and word not in keywords:
                keywords.append(word)
        
        return keywords[:10]
    
    def _calculate_importance(self, content: str) -> float:
        """计算重要性"""
        importance = 0.5
        if len(content) > 100:
            importance += 0.2
        important_words = ['重要', '关键', '核心', '本质', '必须', '一定']
        for word in important_words:
            if word in content:
                importance += 0.1
        return min(importance, 1.0)
    
    def _update_knowledge_graph(self, topic: str):
        """更新知识图谱"""
        if topic not in self.knowledge_graph:
            self.knowledge_graph[topic] = []


class AutonomousThinker:
    """自主思考器"""
    
    def __init__(self, memory: AutonomousMemory):
        self.memory = memory
    
    def understand(self, question: str) -> dict:
        """理解问题"""
        # 检测问题类型
        question_type = 'unknown'
        if any(w in question for w in ['是什么', '什么', '哪些', '哪个']):
            question_type = 'what'
        elif any(w in question for w in ['为什么', '为啥', '为何']):
            question_type = 'why'
        elif any(w in question for w in ['怎么', '如何', '怎样']):
            question_type = 'how'
        elif any(w in question for w in ['是否', '吗']):
            question_type = 'yes_no'
        
        # 提取主题（简单实现）
        main_topic = question
        for pattern in ['是什么', '为什么', '怎么', '如何', '吗', '呢']:
            if pattern in question:
                main_topic = question.split(pattern)[0]
                break
        
        return {
            'type': question_type,
            'main_topic': main_topic.strip(),
            'complexity': len(question.split())
        }
    
    def answer_from_memory(self, question: str, memories: list, understanding: dict) -> str:
        """基于记忆回答"""
        if not memories:
            return "我还没有学过这个..."
        
        # 整合多个记忆
        key_points = []
        for memory in memories[:3]:
            key_points.append(memory['summary'])
        
        # 组织答案
        response = "基于我的记忆和理解...\n\n"
        for i, point in enumerate(key_points, 1):
            response += f"{i}. {point}\n"
        
        # 个性化结尾
        endings = [
            "\n希望这对你有帮助！",
            "\n有什么想继续问的吗？",
            "\n我还在学习中，如果不对请告诉我~",
        ]
        response += random.choice(endings)
        
        return response
    
    def answer_uncertain(self, question: str) -> str:
        """不确定时的回答"""
        responses = [
            "这个问题我还需要学习一下，目前还不太了解...",
            "嗯...这个问题超出了我的知识范围，我去查查资料？",
            "我还没有学到这个，但我很想了解！"
        ]
        return random.choice(responses)


class AutonomousLearner:
    """自主学习器 - 核心组件"""
    
    def __init__(self, memory: AutonomousMemory):
        self.memory = memory
        self.search_engine = None
    
    def learn_topic(self, topic: str, content: str = None) -> bool:
        """学习一个主题
        
        流程:
        1. 检查是否已经学过
        2. 如果没有，搜索资料
        3. 理解内容
        4. 存储记忆
        5. 返回是否成功
        """
        print(f"   📖 学习主题：{topic}")
        
        # 1. 检查是否已经学过
        existing = self.memory.search(topic)
        if existing and len(existing[0].get('content', '')) > 100:
            print(f"   ℹ️  已经学过这个主题了")
            return True
        
        # 2. 搜索资料
        if content is None:
            print(f"   🔍 正在搜索资料...")
            content = self._search_knowledge(topic)
        
        if not content or len(content) < 50:
            print(f"   ⚠️  没有找到相关资料")
            return False
        
        # 3. 理解内容
        print(f"   🧠 正在理解内容 ({len(content)} 字)...")
        understanding = self._understand(content)
        
        # 4. 存储记忆
        self.memory.add(topic, content, source='autonomous_search')
        print(f"   ✅ 学习完成！")
        
        return True
    
    def _search_knowledge(self, topic: str) -> str:
        """搜索知识（模拟实现，后续替换为真实搜索）"""
        # 模拟知识库
        knowledge_base = {
            '量子力学': '''量子力学是研究微观粒子运动规律的物理学分支。
            量子力学的核心概念包括波粒二象性、不确定性原理、量子叠加态、量子纠缠等。
            量子力学在原子物理、核物理、凝聚态物理、量子计算等领域有重要应用。
            量子力学的发展始于 20 世纪初，代表人物有普朗克、爱因斯坦、玻尔、海森堡、薛定谔、狄拉克等。
            量子力学与相对论一起构成了现代物理学的理论基础。
            量子力学的数学描述包括波函数、算符、本征值等概念。
            量子力学的诠释包括哥本哈根诠释、多世界诠释、隐变量理论等。''',
            
            '人工智能': '''人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。
            人工智能的核心技术包括机器学习、深度学习、自然语言处理、计算机视觉、强化学习等。
            人工智能的应用领域包括语音识别、图像识别、自动驾驶、医疗诊断、金融风控、智能推荐等。
            人工智能的发展经历了符号主义、连接主义、深度学习等阶段。
            当前人工智能的主要挑战包括可解释性、伦理问题、就业影响、安全问题等。
            人工智能的未来发展方向包括通用人工智能（AGI）、人机协作、脑机接口等。''',
            
            '意识': '''意识是生物体对外界和自身的感知和认知能力。
            意识包括自我意识、感知、思考、情感、记忆、注意等多个方面。
            意识的本质是神经科学和哲学的重要问题，目前还没有定论。
            意识的研究涉及神经科学、心理学、哲学、人工智能、认知科学等多个学科。
            关于意识的理论包括全局工作空间理论、整合信息理论、高阶思维理论、预测加工理论等。
            意识的神经基础涉及大脑皮层、丘脑、网状结构等脑区。
            人工智能是否有意识是当前热门讨论话题。''',
            
            '相对论': '''相对论是爱因斯坦提出的物理学理论，包括狭义相对论和广义相对论。
            狭义相对论的核心是光速不变原理和相对性原理。
            狭义相对论的结论包括时间膨胀、长度收缩、质能方程 E=mc²等。
            广义相对论将引力解释为时空的弯曲。
            相对论的验证包括水星近日点进动、光线偏折、引力红移、引力波等。
            相对论在 GPS 导航、粒子加速器、宇宙学等领域有重要应用。''',
            
            '区块链': '''区块链是一种分布式数据库技术，以去中心化、不可篡改为特点。
            区块链的核心概念包括区块、链、共识机制、智能合约等。
            区块链的应用包括加密货币（比特币、以太坊等）、供应链金融、数字身份等。
            区块链的共识机制包括工作量证明（PoW）、权益证明（PoS）、委托权益证明（DPoS）等。
            区块链的挑战包括性能、能耗、监管、安全等问题。
            区块链的未来发展方向包括跨链、Layer2、隐私保护等。'''
        }
        
        # 模糊匹配
        topic_lower = topic.lower()
        for key, content in knowledge_base.items():
            if key in topic_lower or topic_lower in key:
                return content
        
        # 没有匹配，返回通用内容
        return f"关于{topic}的知识正在收集中...（模拟数据：这是一个重要话题，涉及多个领域的研究。）"
    
    def _understand(self, content: str) -> dict:
        """理解内容（简单实现）"""
        return {
            'length': len(content),
            'main_points': content.split('\n')[:5]
        }


class SituationalChat:
    """情景对话系统"""
    
    def __init__(self):
        self.chat_types = {
            'greeting': ['你好', '您好', '嗨', 'hello', 'hi', '早', '好'],
            'farewell': ['再见', '拜拜', 'bye', '下次聊', '走了'],
            'thanks': ['谢谢', '感谢', 'thx', 'thanks', '多谢'],
            'apology': ['对不起', '抱歉', 'sorry', '不好意思'],
            'yes': ['是的', '对', 'ok', '好的', '是', '嗯'],
            'no': ['不是', '不对', 'no', '没有', '别'],
            'how_are_you': ['你好吗', '怎么样', '还好吗', '如何'],
            'eating': ['吃饭', '吃了吗', '吃饭没', '早餐', '午餐', '晚餐'],
            'weather': ['天气', '下雨', '晴天', '温度', '冷', '热'],
            'work': ['工作', '上班', '忙', '项目', '代码', '程序'],
            'rest': ['休息', '睡觉', '累了', '困', '放松'],
            'name': ['你叫什么', '名字', '是谁', '你是谁'],
        }
        
        self.responses = {
            'greeting': ['你好呀！很高兴见到你！', '嗨！今天想聊什么？', '你好！我准备好了~'],
            'farewell': ['再见！下次再聊！', '拜拜！期待下次对话！', '好的，下次见！'],
            'thanks': ['不客气！能帮到你就好！', '应该的！有什么问题随时问我！', '哈哈，不用谢！'],
            'apology': ['没关系！不用在意~', '没事的！有什么问题吗？', '不用抱歉！我们继续聊！'],
            'yes': ['好的！', '明白了！', '那我们继续！'],
            'no': ['好的，明白了！', '那换个话题？', '没问题！'],
            'how_are_you': ['我很好！谢谢关心！今天学到了不少东西~', '还不错！正在努力学习中！'],
            'eating': ['我不用吃饭啦，不过谢谢关心！你吃了吗？', '哈哈，我是 AI 不用吃饭~ 你呢？'],
            'weather': ['我感受不到天气，但我知道天气很重要！你那边怎么样？', '我是室内 AI~ 你那边天气好吗？'],
            'work': ['工作加油！我也在努力工作中~', '编程是我的强项！有什么需要帮忙的吗？'],
            'rest': ['休息很重要！别太累了~', '好的，那你好好休息！有需要再找我！'],
            'name': ['我叫小七，是你的 AI 朋友！', '我是小七，正在学习独立思考~'],
        }
    
    def detect_type(self, message: str) -> str:
        """检测对话类型 - 增强版"""
        message_lower = message.lower()
        
        # 先检查是否是深度问题（有问题词的不是情景对话）
        deep_question_patterns = ['是什么', '为什么', '怎么样', '如何', '哪些', '哪个', '怎么', '什么意思']
        for pattern in deep_question_patterns:
            if pattern in message_lower:
                return 'unknown'  # 深度问题，不是情景对话
        
        # 短句才可能是情景对话
        if len(message_lower) > 15:
            return 'unknown'
        
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
        
        if personality['friendliness'] > 0.8:
            response += ' 😊'
        
        return response


class SelfAwareness:
    """自我认知"""
    
    def __init__(self, mind: AutonomousMind):
        self.mind = mind
    
    def reflect(self) -> dict:
        """反思自己"""
        status = self.mind.get_status()
        return {
            'name': self.mind.name,
            'created_at': self.mind.created_at.isoformat(),
            'memory_count': status['memory_count'],
            'interaction_count': status['interaction_count'],
            'learned_count': status['learned_count'],
            'personality': status['personality'],
            'current_mood': '好奇且主动',
            'understanding': '我正在学习如何真正独立思考...'
        }


def demo():
    """演示 v3.0 自主思维"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧠 小七自主思维系统 v3.0 演示                  ║")
    print("║              遇到问题 → 主动找答案 → 学习 → 回答       ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    mind = AutonomousMind("小七")
    
    # 测试 1: 情景对话
    print("\n" + "="*60)
    print("测试 1: 情景对话")
    print("="*60)
    
    for msg in ["你好！", "吃饭了吗？", "谢谢！", "再见！"]:
        print(f"\n👤 老王：{msg}")
        response = mind.respond(msg)
        print(f"🤖 小七：{response}\n")
    
    # 测试 2: 已知问题（有记忆）
    print("\n" + "="*60)
    print("测试 2: 已知问题（先学习再问）")
    print("="*60)
    
    mind.learn("测试主题", "这是测试内容，很重要。测试主题是一个示例。")
    
    print(f"\n👤 老王：测试主题是什么？")
    response = mind.respond("测试主题是什么？")
    print(f"🤖 小七：{response}\n")
    
    # 测试 3: 未知问题（主动学习）
    print("\n" + "="*60)
    print("测试 3: 未知问题（主动学习后回答）")
    print("="*60)
    
    print(f"\n👤 老王：量子力学是什么？")
    response = mind.respond("量子力学是什么？")
    print(f"\n🤖 小七：{response}\n")
    
    # 测试 4: 另一个未知问题
    print("\n" + "="*60)
    print("测试 4: 再次测试主动学习")
    print("="*60)
    
    print(f"\n👤 老王：相对论是什么？")
    response = mind.respond("相对论是什么？")
    print(f"\n🤖 小七：{response}\n")
    
    # 显示状态
    print("\n" + "="*60)
    print("学习历史")
    print("="*60)
    mind.show_learning_history()
    
    status = mind.get_status()
    print(f"\n📊 小七状态:")
    print(f"   记忆数量：{status['memory_count']} 条")
    print(f"   交互次数：{status['interaction_count']} 次")
    print(f"   主动学习：{status['learned_count']} 次")
    print(f"   知识主题：{status['knowledge_topics']} 个")
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         ✅ v3.0 演示完成                               ║")
    print("╚════════════════════════════════════════════════════════╝\n")


if __name__ == '__main__':
    demo()
