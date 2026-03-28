"""
多 Agent 协作系统

实现多个 Agent 之间的通信、任务分配和协作决策
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from pathlib import Path


class MessageType(Enum):
    """消息类型"""
    TASK_ANNOUNCE = "task_announce"      # 任务公告
    TASK_BID = "task_bid"                # 任务投标
    TASK_ASSIGN = "task_assign"          # 任务分配
    HELP_REQUEST = "help_request"        # 求助请求
    HELP_OFFER = "help_offer"            # 提供帮助
    STATUS_UPDATE = "status_update"      # 状态更新
    RESULT_SHARE = "result_share"        # 结果分享


class AgentRole(Enum):
    """Agent 角色"""
    WORKER = "worker"           # 普通工作者
    COORDINATOR = "coordinator" # 协调者
    SPECIALIST = "specialist"   # 专家（特定领域）
    OBSERVER = "observer"       # 观察者（学习用）


@dataclass
class Message:
    """Agent 间消息"""
    msg_type: MessageType
    sender: str
    receiver: str
    content: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: int = 5  # 1-10, 10 最高


@dataclass
class Task:
    """协作任务"""
    id: str
    name: str
    priority: int
    estimated_time: int
    required_skills: List[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    status: str = "pending"  # pending, in_progress, completed, failed
    reward: float = 1.0


@dataclass
class AgentState:
    """Agent 状态"""
    agent_id: str
    role: AgentRole
    current_task: Optional[str] = None
    workload: float = 0.0  # 0-1, 负载程度
    skills: List[str] = field(default_factory=list)
    availability: float = 1.0  # 0-1, 可用程度
    trust_score: float = 0.5  # 0-1, 信任度


class CommunicationChannel:
    """
    通信频道
    
    Agent 间消息传递的中介
    """
    
    def __init__(self):
        self.message_queue: List[Message] = []
        self.subscribers: Dict[str, List[str]] = {}  # topic -> [agent_ids]
        self.message_history: List[Message] = []
    
    def send(self, message: Message):
        """发送消息"""
        self.message_queue.append(message)
        self.message_history.append(message)
        
        # 限制历史消息数量
        if len(self.message_history) > 1000:
            self.message_history.pop(0)
    
    def broadcast(self, sender: str, msg_type: MessageType, content: Dict, priority: int = 5):
        """广播消息"""
        message = Message(
            msg_type=msg_type,
            sender=sender,
            receiver="broadcast",
            content=content,
            priority=priority
        )
        self.send(message)
    
    def get_messages(self, agent_id: str) -> List[Message]:
        """获取发给某 Agent 的消息"""
        messages = []
        for msg in self.message_queue:
            if msg.receiver == agent_id or msg.receiver == "broadcast":
                if msg.sender != agent_id:  # 不接收自己的消息
                    messages.append(msg)
        
        # 清除已读取的消息
        self.message_queue = [
            msg for msg in self.message_queue
            if not (msg.receiver == agent_id or msg.receiver == "broadcast")
            or msg.sender == agent_id
        ]
        
        return messages
    
    def get_recent_history(self, limit: int = 50) -> List[Message]:
        """获取最近的历史消息"""
        return self.message_history[-limit:]


class MultiAgentCoordinator:
    """
    多 Agent 协调器
    
    管理多个 Agent 的协作
    """
    
    def __init__(self):
        self.agents: Dict[str, 'CollaborativeAgent'] = {}
        self.channel = CommunicationChannel()
        self.tasks: Dict[str, Task] = {}
        self.collaboration_history: List[Dict] = []
    
    def register_agent(self, agent: 'CollaborativeAgent'):
        """注册 Agent"""
        self.agents[agent.agent_id] = agent
        agent.coordinator = self
        agent.channel = self.channel
        
        # 广播新 Agent 加入
        self.channel.broadcast(
            sender="system",
            msg_type=MessageType.STATUS_UPDATE,
            content={
                'event': 'agent_joined',
                'agent_id': agent.agent_id,
                'role': agent.role.value
            }
        )
    
    def unregister_agent(self, agent_id: str):
        """注销 Agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            
            self.channel.broadcast(
                sender="system",
                msg_type=MessageType.STATUS_UPDATE,
                content={
                    'event': 'agent_left',
                    'agent_id': agent_id
                }
            )
    
    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.id] = task
        
        # 广播任务
        self.channel.broadcast(
            sender="system",
            msg_type=MessageType.TASK_ANNOUNCE,
            content={
                'task_id': task.id,
                'task_name': task.name,
                'priority': task.priority,
                'required_skills': task.required_skills
            }
        )
    
    def run_collaboration_cycle(self):
        """运行一轮协作"""
        # 1. 每个 Agent 接收消息并处理
        for agent in self.agents.values():
            agent.process_messages()
        
        # 2. 任务分配
        self._assign_tasks()
        
        # 3. 每个 Agent 执行任务
        for agent in self.agents.values():
            agent.execute_task()
        
        # 4. 记录协作历史
        self._record_collaboration()
    
    def _assign_tasks(self):
        """分配未分配的任务"""
        for task in self.tasks.values():
            if task.assigned_to is None and task.status == "pending":
                # 寻找合适的 Agent
                best_agent = self._find_best_agent(task)
                
                if best_agent:
                    task.assigned_to = best_agent.agent_id
                    task.status = "in_progress"
                    
                    # 发送任务分配消息
                    self.channel.send(Message(
                        msg_type=MessageType.TASK_ASSIGN,
                        sender="coordinator",
                        receiver=best_agent.agent_id,
                        content={
                            'task_id': task.id,
                            'task_name': task.name,
                            'priority': task.priority
                        }
                    ))
    
    def _find_best_agent(self, task: Task) -> Optional['CollaborativeAgent']:
        """为任务找到最合适的 Agent"""
        candidates = []
        
        for agent in self.agents.values():
            if agent.state.availability < 0.3:  # 太忙的 Agent 不考虑
                continue
            
            # 计算匹配度
            skill_match = len(set(task.required_skills) & set(agent.state.skills))
            availability = agent.state.availability
            trust = agent.state.trust_score
            
            score = skill_match * 0.5 + availability * 0.3 + trust * 0.2
            candidates.append((agent, score))
        
        if not candidates:
            return None
        
        # 选择分数最高的
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def _record_collaboration(self):
        """记录协作历史"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'agents': len(self.agents),
            'tasks': len([t for t in self.tasks.values() if t.status == "completed"]),
            'messages': len(self.channel.message_history)
        }
        self.collaboration_history.append(record)
    
    def get_stats(self) -> Dict:
        """获取协作统计"""
        return {
            'total_agents': len(self.agents),
            'total_tasks': len(self.tasks),
            'completed_tasks': len([t for t in self.tasks.values() if t.status == "completed"]),
            'total_messages': len(self.channel.message_history),
            'collaboration_rounds': len(self.collaboration_history)
        }


class CollaborativeAgent:
    """
    协作 Agent
    
    可以与其他 Agent 协作完成任务
    """
    
    def __init__(
        self,
        agent_id: str,
        role: AgentRole = AgentRole.WORKER,
        skills: List[str] = None
    ):
        self.agent_id = agent_id
        self.role = role
        self.state = AgentState(
            agent_id=agent_id,
            role=role,
            skills=skills or []
        )
        
        self.coordinator: Optional[MultiAgentCoordinator] = None
        self.channel: Optional[CommunicationChannel] = None
        
        self.current_task: Optional[Task] = None
        self.task_history: List[Task] = []
        self.message_buffer: List[Message] = []
        
        # 内部 Agent（用于实际决策）
        self.internal_agent = None
    
    def set_internal_agent(self, agent):
        """设置内部 Agent（IndependentAgent 实例）"""
        self.internal_agent = agent
    
    def process_messages(self):
        """处理接收到的消息"""
        if not self.channel:
            return
        
        messages = self.channel.get_messages(self.agent_id)
        
        for msg in messages:
            self._handle_message(msg)
    
    def _handle_message(self, msg: Message):
        """处理单条消息"""
        if msg.msg_type == MessageType.TASK_ANNOUNCE:
            self._on_task_announce(msg)
        elif msg.msg_type == MessageType.TASK_BID:
            self._on_task_bid(msg)
        elif msg.msg_type == MessageType.HELP_REQUEST:
            self._on_help_request(msg)
        elif msg.msg_type == MessageType.STATUS_UPDATE:
            self._on_status_update(msg)
    
    def _on_task_announce(self, msg: Message):
        """处理任务公告"""
        content = msg.content
        
        # 检查是否有需要的技能
        required_skills = content.get('required_skills', [])
        has_skills = any(skill in self.state.skills for skill in required_skills)
        
        if has_skills and self.state.availability > 0.5:
            # 投标
            bid = {
                'task_id': content['task_id'],
                'bidder': self.agent_id,
                'skills_match': len(set(required_skills) & set(self.state.skills)),
                'availability': self.state.availability,
                'trust_score': self.state.trust_score
            }
            
            self.channel.send(Message(
                msg_type=MessageType.TASK_BID,
                sender=self.agent_id,
                receiver="coordinator",
                content=bid
            ))
    
    def _on_task_bid(self, msg: Message):
        """处理其他 Agent 的投标"""
        # 可以记录竞争对手的信息
        pass
    
    def _on_help_request(self, msg: Message):
        """处理求助请求"""
        if self.state.availability > 0.7:
            # 提供帮助
            self.channel.send(Message(
                msg_type=MessageType.HELP_OFFER,
                sender=self.agent_id,
                receiver=msg.sender,
                content={
                    'helper': self.agent_id,
                    'availability': self.state.availability
                }
            ))
    
    def _on_status_update(self, msg: Message):
        """处理状态更新"""
        content = msg.content
        event = content.get('event')
        
        if event == 'agent_joined':
            print(f"  [{self.agent_id}] 新 Agent 加入：{content['agent_id']}")
        elif event == 'agent_left':
            print(f"  [{self.agent_id}] Agent 离开：{content['agent_id']}")
    
    def execute_task(self):
        """执行当前任务"""
        if self.current_task and self.internal_agent:
            # 使用内部 Agent 执行
            result = self.internal_agent.run_cycle()
            
            # 更新状态
            if '完成' in result:
                self.current_task.status = "completed"
                self.task_history.append(self.current_task)
                self.state.workload = max(0, self.state.workload - 0.3)
                self.state.trust_score = min(1.0, self.state.trust_score + 0.05)
                
                # 分享结果
                self.channel.broadcast(
                    sender=self.agent_id,
                    msg_type=MessageType.RESULT_SHARE,
                    content={
                        'task_id': self.current_task.id,
                        'result': result,
                        'executor': self.agent_id
                    }
                )
            elif '失败' in result:
                self.current_task.status = "failed"
                self.state.workload = max(0, self.state.workload - 0.2)
            
            self.current_task = None
            self.state.availability = 1.0 - self.state.workload
    
    def update_state(self):
        """更新状态"""
        # 根据当前任务更新负载
        if self.current_task:
            self.state.workload = min(1.0, self.state.workload + 0.1)
        else:
            self.state.workload = max(0, self.state.workload - 0.05)
        
        self.state.availability = 1.0 - self.state.workload
    
    def get_stats(self) -> Dict:
        """获取 Agent 统计"""
        return {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'current_task': self.current_task.name if self.current_task else None,
            'completed_tasks': len(self.task_history),
            'workload': self.state.workload,
            'availability': self.state.availability,
            'trust_score': self.state.trust_score,
            'skills': self.state.skills
        }
