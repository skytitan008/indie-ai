#!/usr/bin/env python3
"""
Agent 谈判协议

实现多 Agent 之间的协作与谈判机制：
- 任务招标（Task Announcement）
- 投标（Bid）
- 中标（Award）
- 协商（Negotiation）
- 合同网协议（Contract Net Protocol）
"""

import uuid
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.models import Task, Priority


class MessageType(Enum):
    """消息类型"""
    TASK_ANNOUNCE = "task_announce"      # 任务公告
    BID = "bid"                          # 投标
    AWARD = "award"                      # 中标通知
    REJECT = "reject"                    # 拒绝
    ACCEPT = "accept"                    # 接受
    CANCEL = "cancel"                    # 取消
    PROPOSE = "propose"                  # 提议
    COUNTER_PROPOSE = "counter_propose"  # 反提议
    AGREE = "agree"                      # 同意
    REFUSE = "refuse"                    # 拒绝


class AgentRole(Enum):
    """Agent 角色"""
    MANAGER = "manager"    # 管理者（发布任务）
    CONTRACTOR = "contractor"  # 承包者（执行任务）
    PEER = "peer"          # 平等协商


@dataclass
class Message:
    """谈判消息"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: MessageType = MessageType.TASK_ANNOUNCE
    sender: str = ""
    receiver: str = ""
    task: Optional[Dict] = None
    bid_value: float = 0.0
    proposal: Optional[Dict] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type.value,
            'sender': self.sender,
            'receiver': self.receiver,
            'task': self.task,
            'bid_value': self.bid_value,
            'proposal': self.proposal,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        return cls(
            id=data.get('id', str(uuid.uuid4())[:8]),
            type=MessageType(data['type']),
            sender=data['sender'],
            receiver=data['receiver'],
            task=data.get('task'),
            bid_value=data.get('bid_value', 0.0),
            proposal=data.get('proposal'),
            timestamp=data.get('timestamp', datetime.now().isoformat())
        )


class NegotiationAgent:
    """谈判 Agent"""
    
    def __init__(self, agent_id: str, role: AgentRole = AgentRole.PEER):
        self.id = agent_id
        self.role = role
        self.capabilities: Dict[str, float] = {}  # 能力评估
        self.current_tasks: List[str] = []  # 当前任务
        self.message_history: List[Message] = []
        self.negotiation_state: Dict[str, str] = {}
    
    def add_capability(self, skill: str, proficiency: float):
        """添加能力"""
        self.capabilities[skill] = min(1.0, max(0.0, proficiency))
    
    def calculate_bid(self, task: Dict) -> float:
        """计算投标值（越低越好）"""
        if not task:
            return float('inf')
        
        # 基础成本
        base_cost = task.get('estimated_time', 60) / 60.0  # 小时
        
        # 能力匹配度
        required_skills = task.get('required_skills', [])
        if required_skills:
            skill_match = sum(
                self.capabilities.get(skill, 0.0) 
                for skill in required_skills
            ) / len(required_skills)
        else:
            skill_match = 0.5
        
        # 当前负载
        workload_factor = 1.0 + len(self.current_tasks) * 0.2
        
        # 优先级调整
        priority = task.get('priority', 5)
        priority_factor = 1.0 - (priority - 5) * 0.05
        
        # 计算最终投标值
        bid = base_cost * (1.0 - skill_match * 0.3) * workload_factor * priority_factor
        
        return bid
    
    def receive_message(self, message: Message) -> Optional[Message]:
        """接收消息并响应"""
        self.message_history.append(message)
        
        if message.type == MessageType.TASK_ANNOUNCE:
            return self._handle_announcement(message)
        elif message.type == MessageType.BID:
            return self._handle_bid(message)
        elif message.type == MessageType.AWARD:
            return self._handle_award(message)
        elif message.type == MessageType.PROPOSE:
            return self._handle_propose(message)
        elif message.type == MessageType.COUNTER_PROPOSE:
            return self._handle_counter_propose(message)
        
        return None
    
    def _handle_announcement(self, message: Message) -> Optional[Message]:
        """处理任务公告"""
        if not message.task:
            return None
        
        # 计算投标
        bid_value = self.calculate_bid(message.task)
        
        # 决定是否投标
        if bid_value < float('inf'):
            return Message(
                type=MessageType.BID,
                sender=self.id,
                receiver=message.sender,
                task=message.task,
                bid_value=bid_value
            )
        
        return None
    
    def _handle_bid(self, message: Message) -> Optional[Message]:
        """处理投标（管理者）"""
        if self.role != AgentRole.MANAGER:
            return None
        
        # 存储投标
        state_key = f"bid_{message.task.get('id', 'unknown')}"
        if state_key not in self.negotiation_state:
            self.negotiation_state[state_key] = []
        
        self.negotiation_state[state_key].append(message.to_dict())
        
        return None
    
    def _handle_award(self, message: Message) -> Optional[Message]:
        """处理中标通知"""
        # 决定是否接受
        if message.bid_value <= self.calculate_bid(message.task or {}):
            return Message(
                type=MessageType.ACCEPT,
                sender=self.id,
                receiver=message.sender,
                task=message.task
            )
        else:
            return Message(
                type=MessageType.REJECT,
                sender=self.id,
                receiver=message.sender,
                task=message.task
            )
    
    def _handle_propose(self, message: Message) -> Optional[Message]:
        """处理提议"""
        if not message.proposal:
            return None
        
        # 简单策略：接受有利提议
        if message.proposal.get('favorable', False):
            return Message(
                type=MessageType.AGREE,
                sender=self.id,
                receiver=message.sender,
                proposal=message.proposal
            )
        else:
            # 反提议
            counter = message.proposal.copy()
            counter['value'] = counter.get('value', 0) * 1.1  # 提高 10%
            
            return Message(
                type=MessageType.COUNTER_PROPOSE,
                sender=self.id,
                receiver=message.sender,
                proposal=counter
            )
    
    def _handle_counter_propose(self, message: Message) -> Optional[Message]:
        """处理反提议"""
        # 简单策略：接受合理反提议
        if message.proposal and message.proposal.get('value', 0) < 100:
            return Message(
                type=MessageType.AGREE,
                sender=self.id,
                receiver=message.sender,
                proposal=message.proposal
            )
        
        return Message(
            type=MessageType.REFUSE,
            sender=self.id,
            receiver=message.sender
        )
    
    def announce_task(self, task: Task, receivers: List[str]) -> Message:
        """发布任务公告"""
        self.role = AgentRole.MANAGER
        
        return Message(
            type=MessageType.TASK_ANNOUNCE,
            sender=self.id,
            receiver="broadcast",
            task={
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'priority': task.priority,
                'estimated_time': task.estimated_time,
                'required_skills': task.description.split()[:3]  # 简单提取技能
            }
        )
    
    def select_best_bid(self, bids: List[Message]) -> Optional[Message]:
        """选择最佳投标（最低值）"""
        if not bids:
            return None
        
        best_bid = min(bids, key=lambda b: b.bid_value)
        
        return Message(
            type=MessageType.AWARD,
            sender=self.id,
            receiver=best_bid.sender,
            task=best_bid.task,
            bid_value=best_bid.bid_value
        )
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            'id': self.id,
            'role': self.role.value,
            'capabilities': self.capabilities,
            'current_tasks': self.current_tasks,
            'message_count': len(self.message_history),
            'negotiation_state': self.negotiation_state
        }


class ContractNetProtocol:
    """合同网协议协调器"""
    
    def __init__(self):
        self.manager: Optional[NegotiationAgent] = None
        self.contractors: Dict[str, NegotiationAgent] = {}
        self.contracts: List[Dict] = []
        self.message_log: List[Message] = []
    
    def add_manager(self, agent: NegotiationAgent):
        """添加管理者"""
        agent.role = AgentRole.MANAGER
        self.manager = agent
    
    def add_contractor(self, agent: NegotiationAgent):
        """添加承包者"""
        agent.role = AgentRole.CONTRACTOR
        self.contractors[agent.id] = agent
    
    def run_negotiation(self, task: Task, rounds: int = 3) -> Optional[Dict]:
        """运行谈判流程"""
        if not self.manager:
            print("❌ 没有管理者")
            return None
        
        print(f"\n╔════════════════════════════════════════════════════════╗")
        print(f"║         🤝 合同网谈判 - 任务：{task.name:<20} ║")
        print(f"╚════════════════════════════════════════════════════════╝\n")
        
        # 第 1 轮：任务公告
        print("📢 第 1 轮：任务公告")
        announce_msg = self.manager.announce_task(task, list(self.contractors.keys()))
        self.message_log.append(announce_msg)
        print(f"   管理者 {self.manager.id} 发布任务")
        
        # 第 2 轮：投标
        print("\n💰 第 2 轮：投标")
        bids = []
        for contractor_id, contractor in self.contractors.items():
            response = contractor.receive_message(announce_msg)
            if response and response.type == MessageType.BID:
                bids.append(response)
                print(f"   {contractor_id} 投标：{response.bid_value:.2f}")
        
        if not bids:
            print("   ❌ 无投标")
            return None
        
        # 第 3 轮：中标
        print("\n🏆 第 3 轮：中标")
        award_msg = self.manager.select_best_bid(bids)
        if award_msg:
            self.message_log.append(award_msg)
            winner_id = award_msg.receiver
            print(f"   {winner_id} 中标 (投标值：{award_msg.bid_value:.2f})")
            
            # 创建合同
            contract = {
                'task_id': task.id,
                'manager': self.manager.id,
                'contractor': winner_id,
                'bid_value': award_msg.bid_value,
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            self.contracts.append(contract)
            
            # 更新承包者任务列表
            if winner_id in self.contractors:
                self.contractors[winner_id].current_tasks.append(task.id)
            
            return contract
        
        return None
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        return {
            'total_negotiations': len(self.contracts),
            'active_contracts': sum(1 for c in self.contracts if c['status'] == 'active'),
            'manager': self.manager.id if self.manager else None,
            'contractors': list(self.contractors.keys()),
            'total_messages': len(self.message_log)
        }


def demo():
    """演示谈判协议"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🤝 Agent 谈判协议演示                          ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建合同网
    cnp = ContractNetProtocol()
    
    # 创建管理者
    manager = NegotiationAgent("Manager-001", AgentRole.MANAGER)
    cnp.add_manager(manager)
    
    # 创建承包者
    contractor1 = NegotiationAgent("Contractor-A", AgentRole.CONTRACTOR)
    contractor1.add_capability("coding", 0.9)
    contractor1.add_capability("testing", 0.7)
    
    contractor2 = NegotiationAgent("Contractor-B", AgentRole.CONTRACTOR)
    contractor2.add_capability("coding", 0.6)
    contractor2.add_capability("testing", 0.95)
    
    contractor3 = NegotiationAgent("Contractor-C", AgentRole.CONTRACTOR)
    contractor3.add_capability("coding", 0.8)
    contractor3.add_capability("documentation", 0.9)
    
    cnp.add_contractor(contractor1)
    cnp.add_contractor(contractor2)
    cnp.add_contractor(contractor3)
    
    print("📋 Agent 信息:")
    print(f"   管理者：{manager.id}")
    for agent in [contractor1, contractor2, contractor3]:
        print(f"   {agent.id}: {agent.capabilities}")
    
    # 创建任务
    task = Task(
        id="T001",
        name="代码格式化",
        description="coding formatting black",
        priority=8,
        estimated_time=30
    )
    
    # 运行谈判
    contract = cnp.run_negotiation(task)
    
    if contract:
        print(f"\n✅ 合同签订成功!")
        print(f"   任务：{contract['task_id']}")
        print(f"   承包者：{contract['contractor']}")
        print(f"   投标值：{contract['bid_value']:.2f}")
    
    # 统计
    print("\n📊 谈判统计:")
    stats = cnp.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ 谈判协议演示完成！\n")


if __name__ == '__main__':
    demo()
