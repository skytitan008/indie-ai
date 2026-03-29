#!/usr/bin/env python3
"""
Week 2 Day 7 功能验证脚本

测试 VS Code 插件和 Agent 谈判协议
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def test_negotiation():
    """测试谈判协议"""
    print("\n" + "="*60)
    print("🧪 测试：Agent 谈判协议")
    print("="*60)
    
    from src.multi_agent.negotiation import (
        NegotiationAgent, 
        ContractNetProtocol, 
        AgentRole,
        MessageType
    )
    from src.core.models import Task
    
    # 创建合同网
    cnp = ContractNetProtocol()
    
    # 创建管理者
    manager = NegotiationAgent("Manager", AgentRole.MANAGER)
    cnp.add_manager(manager)
    
    # 创建承包者
    contractor = NegotiationAgent("Worker", AgentRole.CONTRACTOR)
    contractor.add_capability("coding", 0.9)
    cnp.add_contractor(contractor)
    
    # 创建任务
    task = Task(
        id="TEST-001",
        name="测试任务",
        description="coding test",
        priority=8,
        estimated_time=30
    )
    
    # 运行谈判
    contract = cnp.run_negotiation(task)
    
    # 验证
    assert contract is not None, "合同创建失败"
    assert contract['manager'] == 'Manager', "管理者错误"
    assert contract['contractor'] == 'Worker', "承包者错误"
    assert contract['bid_value'] > 0, "投标值错误"
    
    print("✅ 谈判协议测试通过")
    return True


def test_message_types():
    """测试消息类型"""
    print("\n" + "="*60)
    print("🧪 测试：消息类型")
    print("="*60)
    
    from src.multi_agent.negotiation import MessageType
    
    expected_types = [
        'TASK_ANNOUNCE',
        'BID',
        'AWARD',
        'REJECT',
        'ACCEPT',
        'CANCEL',
        'PROPOSE',
        'COUNTER_PROPOSE',
        'AGREE',
        'REFUSE'
    ]
    
    for type_name in expected_types:
        msg_type = getattr(MessageType, type_name)
        assert msg_type is not None, f"消息类型 {type_name} 不存在"
        print(f"   ✓ {type_name}")
    
    print("✅ 消息类型测试通过")
    return True


def test_bid_calculation():
    """测试投标计算"""
    print("\n" + "="*60)
    print("🧪 测试：投标计算")
    print("="*60)
    
    from src.multi_agent.negotiation import NegotiationAgent, AgentRole
    
    agent = NegotiationAgent("TestAgent", AgentRole.CONTRACTOR)
    agent.add_capability("coding", 0.9)
    agent.add_capability("testing", 0.8)
    
    # 测试不同任务的投标
    task1 = {'estimated_time': 60, 'priority': 5, 'required_skills': ['coding']}
    task2 = {'estimated_time': 120, 'priority': 10, 'required_skills': ['coding', 'testing']}
    
    bid1 = agent.calculate_bid(task1)
    bid2 = agent.calculate_bid(task2)
    
    print(f"   任务 1 (60 分钟，优先级 5): {bid1:.2f}")
    print(f"   任务 2 (120 分钟，优先级 10): {bid2:.2f}")
    
    assert bid1 > 0, "投标值应为正数"
    assert bid2 > bid1, "更复杂任务应有更高投标"
    
    print("✅ 投标计算测试通过")
    return True


def test_vscode_extension():
    """测试 VS Code 插件文件"""
    print("\n" + "="*60)
    print("🧪 测试：VS Code 插件文件")
    print("="*60)
    
    extension_path = Path(__file__).parent.parent / "vscode-extension"
    
    required_files = [
        "package.json",
        "src/extension.ts",
        "tsconfig.json",
        "README.md",
        "INSTALL.md"
    ]
    
    for file in required_files:
        file_path = extension_path / file
        assert file_path.exists(), f"文件不存在：{file}"
        print(f"   ✓ {file}")
    
    # 检查 package.json
    import json
    with open(extension_path / "package.json") as f:
        package = json.load(f)
    
    assert package['name'] == 'indie-ai-helper', "插件名称错误"
    assert 'contributes' in package, "缺少 contributes 配置"
    assert 'commands' in package['contributes'], "缺少 commands 配置"
    
    commands = package['contributes']['commands']
    assert len(commands) >= 5, "命令数量不足"
    
    print(f"   ✓ 插件配置正确 ({len(commands)} 个命令)")
    print("✅ VS Code 插件测试通过")
    return True


def main():
    """运行所有测试"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🧪 Week 2 Day 7 功能验证                       ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    tests = [
        ("消息类型", test_message_types),
        ("投标计算", test_bid_calculation),
        ("谈判协议", test_negotiation),
        ("VS Code 插件", test_vscode_extension)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} 测试失败：{e}")
            failed += 1
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    print(f"   通过：{passed}/{len(tests)}")
    print(f"   失败：{failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✅ 所有测试通过！Week 2 Day 7 功能正常")
    else:
        print(f"\n❌ {failed} 个测试失败，请检查")
    
    print()
    
    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
