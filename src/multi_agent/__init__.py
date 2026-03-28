"""
多 Agent 协作系统
"""

from .coordinator import (
    MultiAgentCoordinator,
    CollaborativeAgent,
    CommunicationChannel,
    Task,
    Message,
    MessageType,
    AgentRole,
    AgentState
)

__all__ = [
    'MultiAgentCoordinator',
    'CollaborativeAgent',
    'CommunicationChannel',
    'Task',
    'Message',
    'MessageType',
    'AgentRole',
    'AgentState'
]
