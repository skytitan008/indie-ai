#!/usr/bin/env python3
"""
Agent 谈判协议演示

展示多 Agent 之间的任务分配与协商过程
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.multi_agent.negotiation import (
    NegotiationAgent, 
    ContractNetProtocol, 
    AgentRole
)
from src.core.models import Task


def demo_basic_negotiation():
    """基础谈判演示"""
    print("\n" + "="*60)
    print("🤝 场景 1: 基础任务分配")
    print("="*60 + "\n")
    
    # 创建合同网
    cnp = ContractNetProtocol()
    
    # 创建管理者
    manager = NegotiationAgent("ProjectManager", AgentRole.MANAGER)
    cnp.add_manager(manager)
    
    # 创建 3 个 Agent
    agents = []
    for i in range(1, 4):
        agent = NegotiationAgent(f"Dev-{i:02d}", AgentRole.CONTRACTOR)
        agent.add_capability("coding", 0.7 + i * 0.1)
        agent.add_capability("testing", 0.8 - i * 0.05)
        agents.append(agent)
        cnp.add_contractor(agent)
    
    # 创建任务
    task = Task(
        id="TASK-001",
        name="实现用户登录模块",
        description="coding authentication security",
        priority=9,
        estimated_time=120
    )
    
    # 运行谈判
    contract = cnp.run_negotiation(task)
    
    if contract:
        print(f"\n✅ 任务分配成功!")
        print(f"   执行者：{contract['contractor']}")
        print(f"   预计成本：{contract['bid_value']:.2f} 小时")


def demo_multi_round_negotiation():
    """多轮谈判演示"""
    print("\n" + "="*60)
    print("🤝 场景 2: 多轮协商")
    print("="*60 + "\n")
    
    # 创建两个 Agent
    agent1 = NegotiationAgent("Alice", AgentRole.PEER)
    agent1.add_capability("design", 0.9)
    
    agent2 = NegotiationAgent("Bob", AgentRole.PEER)
    agent2.add_capability("coding", 0.95)
    
    # 模拟协商
    print("💬 Alice 提议:")
    propose_msg = agent1.announce_task(
        Task(
            id="PROP-001",
            name="UI 设计",
            description="design interface figma",
            priority=7,
            estimated_time=60
        ),
        ["Bob"]
    )
    print(f"   任务：{propose_msg.task['name']}")
    print(f"   预计时间：{propose_msg.task['estimated_time']} 分钟")
    
    # Bob 响应
    response = agent2.receive_message(propose_msg)
    if response:
        print(f"\n💬 Bob 响应:")
        print(f"   类型：{response.type.value}")
        if response.bid_value:
            print(f"   投标值：{response.bid_value:.2f}")


def demo_aigc_video_workflow():
    """AIGC 视频工作流演示"""
    print("\n" + "="*60)
    print("🤝 场景 3: AIGC 视频生成工作流")
    print("="*60 + "\n")
    
    # 创建工作流合同网
    cnp = ContractNetProtocol()
    
    # 创建角色
    director = NegotiationAgent("Director", AgentRole.MANAGER)
    cnp.add_manager(director)
    
    script_writer = NegotiationAgent("ScriptWriter", AgentRole.CONTRACTOR)
    script_writer.add_capability("writing", 0.95)
    script_writer.add_capability("creativity", 0.9)
    cnp.add_contractor(script_writer)
    
    storyboard_artist = NegotiationAgent("StoryboardArtist", AgentRole.CONTRACTOR)
    storyboard_artist.add_capability("drawing", 0.9)
    storyboard_artist.add_capability("composition", 0.85)
    cnp.add_contractor(storyboard_artist)
    
    video_generator = NegotiationAgent("VideoGenerator", AgentRole.CONTRACTOR)
    video_generator.add_capability("ai_video", 0.95)
    video_generator.add_capability("rendering", 0.9)
    cnp.add_contractor(video_generator)
    
    # 任务序列
    tasks = [
        Task(
            id="VIDEO-001-1",
            name="剧本创作",
            description="writing creativity storytelling",
            priority=10,
            estimated_time=180
        ),
        Task(
            id="VIDEO-001-2",
            name="分镜设计",
            description="drawing composition visual",
            priority=9,
            estimated_time=120
        ),
        Task(
            id="VIDEO-001-3",
            name="视频生成",
            description="ai_video rendering gpu",
            priority=8,
            estimated_time=300
        )
    ]
    
    print("🎬 AIGC 视频工作流任务分配:\n")
    
    contracts = []
    for i, task in enumerate(tasks, 1):
        print(f"步骤 {i}/3: {task.name}")
        contract = cnp.run_negotiation(task)
        if contract:
            contracts.append(contract)
            print(f"   ✅ 分配给：{contract['contractor']}")
    
    # 统计
    print("\n📊 工作流统计:")
    stats = cnp.get_statistics()
    print(f"   总任务数：{len(contracts)}")
    print(f"   参与 Agent: {len(stats['contractors'])}")
    print(f"   总消息数：{stats['total_messages']}")
    
    # 展示分配结果
    print("\n📋 最终分配:")
    for i, contract in enumerate(contracts, 1):
        print(f"   {i}. {contract['task_id']}: {contract['contractor']} "
              f"(成本：{contract['bid_value']:.2f})")


def demo_negotiation_strategies():
    """谈判策略演示"""
    print("\n" + "="*60)
    print("🤝 场景 4: 不同谈判策略")
    print("="*60 + "\n")
    
    # 创建不同策略的 Agent
    aggressive = NegotiationAgent("Aggressive", AgentRole.CONTRACTOR)
    aggressive.add_capability("negotiation", 0.9)
    
    conservative = NegotiationAgent("Conservative", AgentRole.CONTRACTOR)
    conservative.add_capability("negotiation", 0.7)
    
    collaborative = NegotiationAgent("Collaborative", AgentRole.CONTRACTOR)
    collaborative.add_capability("negotiation", 0.85)
    
    print("📋 Agent 策略:")
    print(f"   Aggressive: 激进型 (能力强，投标低)")
    print(f"   Conservative: 保守型 (能力一般，投标高)")
    print(f"   Collaborative: 协作型 (能力良好，投标适中)")
    
    # 创建任务
    task = Task(
        id="STRAT-001",
        name="紧急任务",
        description="urgent critical important",
        priority=10,
        estimated_time=60
    )
    
    # 计算投标
    print("\n💰 投标计算:")
    for agent in [aggressive, conservative, collaborative]:
        bid = agent.calculate_bid({
            'estimated_time': task.estimated_time,
            'priority': task.priority,
            'required_skills': ['urgent']
        })
        print(f"   {agent.id}: {bid:.2f}")


def main():
    """主演示"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🤝 Agent 谈判协议完整演示                      ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 运行所有演示
    demo_basic_negotiation()
    demo_multi_round_negotiation()
    demo_aigc_video_workflow()
    demo_negotiation_strategies()
    
    print("\n" + "="*60)
    print("✅ 所有演示完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
