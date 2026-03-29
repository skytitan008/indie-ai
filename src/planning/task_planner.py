#!/usr/bin/env python3
"""
任务规划核心模块

让 AI 能够：
- 分解复杂任务为子任务
- 分析任务依赖关系
- 生成执行计划
- 跟踪执行进度
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from enum import Enum
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    BLOCKED = "blocked"      # 被阻塞


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1  # 关键
    HIGH = 2      # 高
    MEDIUM = 3    # 中
    LOW = 4       # 低


class Task:
    """任务类"""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        parent_id: Optional[int] = None,
        estimated_time: int = 0,  # 分钟
        dependencies: List[int] = None
    ):
        self.id: Optional[int] = None
        self.name = name
        self.description = description
        self.status = TaskStatus.PENDING
        self.priority = priority
        self.parent_id = parent_id
        self.subtasks: List[int] = []  # 子任务 ID 列表
        self.dependencies = dependencies or []
        self.estimated_time = estimated_time
        self.actual_time = 0
        self.result: Optional[str] = None
        self.error: Optional[str] = None
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'priority': self.priority.value,
            'parent_id': self.parent_id,
            'subtasks': self.subtasks,
            'dependencies': self.dependencies,
            'estimated_time': self.estimated_time,
            'actual_time': self.actual_time,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """从字典创建"""
        task = cls(
            name=data['name'],
            description=data.get('description', ''),
            priority=TaskPriority(data.get('priority', 3)),
            parent_id=data.get('parent_id'),
            estimated_time=data.get('estimated_time', 0),
            dependencies=data.get('dependencies', [])
        )
        task.id = data.get('id')
        task.status = TaskStatus(data.get('status', 'pending'))
        task.subtasks = data.get('subtasks', [])
        task.actual_time = data.get('actual_time', 0)
        task.result = data.get('result')
        task.error = data.get('error')
        task.created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else datetime.now()
        task.started_at = datetime.fromisoformat(data['started_at']) if data.get('started_at') else None
        task.completed_at = datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None
        return task
    
    def __repr__(self):
        return f"Task({self.name}, {self.status.value})"


class TaskPlanner:
    """任务规划器"""
    
    def __init__(self, db_path: str = "ai_memory.db"):
        self.db_path = PROJECT_ROOT / db_path
        self._init_db()
        self.current_task_id: Optional[int] = None
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 3,
                parent_id INTEGER,
                subtasks TEXT DEFAULT '[]',
                dependencies TEXT DEFAULT '[]',
                estimated_time INTEGER DEFAULT 0,
                actual_time INTEGER DEFAULT 0,
                result TEXT,
                error TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES tasks(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_task(
        self,
        name: str,
        description: str = "",
        priority: TaskPriority = TaskPriority.MEDIUM,
        parent_id: Optional[int] = None,
        estimated_time: int = 0,
        dependencies: List[int] = None
    ) -> int:
        """创建任务"""
        task = Task(
            name=name,
            description=description,
            priority=priority,
            parent_id=parent_id,
            estimated_time=estimated_time,
            dependencies=dependencies
        )
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO tasks (name, description, status, priority, parent_id,
                             subtasks, dependencies, estimated_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.name, task.description, task.status.value,
            task.priority.value, task.parent_id,
            json.dumps(task.subtasks), json.dumps(task.dependencies),
            task.estimated_time
        ))
        task.id = c.lastrowid
        conn.commit()
        conn.close()
        
        return task.id
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """获取任务"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = c.fetchone()
        conn.close()
        
        if not row:
            return None
        
        data = {
            'id': row[0], 'name': row[1], 'description': row[2],
            'status': row[3], 'priority': row[4], 'parent_id': row[5],
            'subtasks': json.loads(row[6]), 'dependencies': json.loads(row[7]),
            'estimated_time': row[8], 'actual_time': row[9],
            'result': row[10], 'error': row[11],
            'created_at': row[12], 'started_at': row[13], 'completed_at': row[14]
        }
        return Task.from_dict(data)
    
    def update_task_status(
        self,
        task_id: int,
        status: TaskStatus,
        result: Optional[str] = None,
        error: Optional[str] = None
    ):
        """更新任务状态"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        now = datetime.now().isoformat()
        if status == TaskStatus.RUNNING:
            c.execute('''
                UPDATE tasks SET status = ?, started_at = ? WHERE id = ?
            ''', (status.value, now, task_id))
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            c.execute('''
                UPDATE tasks SET status = ?, completed_at = ?, result = ?, error = ?
                WHERE id = ?
            ''', (status.value, now, result, error, task_id))
        else:
            c.execute('UPDATE tasks SET status = ? WHERE id = ?', (status.value, task_id))
        
        conn.commit()
        conn.close()
    
    def add_subtask(self, parent_id: int, subtask_id: int):
        """添加子任务"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 获取父任务
        c.execute('SELECT subtasks FROM tasks WHERE id = ?', (parent_id,))
        row = c.fetchone()
        subtasks = json.loads(row[0]) if row and row[0] else []
        subtasks.append(subtask_id)
        
        c.execute('''
            UPDATE tasks SET subtasks = ? WHERE id = ?
        ''', (json.dumps(subtasks), parent_id))
        
        conn.commit()
        conn.close()
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM tasks ORDER BY created_at')
        rows = c.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            data = {
                'id': row[0], 'name': row[1], 'description': row[2],
                'status': row[3], 'priority': row[4], 'parent_id': row[5],
                'subtasks': json.loads(row[6]), 'dependencies': json.loads(row[7]),
                'estimated_time': row[8], 'actual_time': row[9],
                'result': row[10], 'error': row[11],
                'created_at': row[12], 'started_at': row[13], 'completed_at': row[14]
            }
            tasks.append(Task.from_dict(data))
        
        return tasks
    
    def get_ready_tasks(self) -> List[Task]:
        """获取可执行的任务（依赖已满足）"""
        all_tasks = self.get_all_tasks()
        ready = []
        
        for task in all_tasks:
            if task.status != TaskStatus.PENDING:
                continue
            
            # 检查依赖
            deps_met = True
            for dep_id in task.dependencies:
                dep_task = self.get_task(dep_id)
                if dep_task and dep_task.status != TaskStatus.COMPLETED:
                    deps_met = False
                    break
            
            if deps_met:
                ready.append(task)
        
        # 按优先级排序
        ready.sort(key=lambda t: t.priority.value)
        return ready
    
    def delete_task(self, task_id: int):
        """删除任务"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
    
    def clear_all(self):
        """清空所有任务"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM tasks')
        conn.commit()
        conn.close()


class TaskDecomposer:
    """任务分解器 - 将复杂任务分解为子任务"""
    
    def __init__(self):
        # 常见任务分解模板
        self.templates = {
            '开发功能': self._decompose_development,
            '写代码': self._decompose_coding,
            '测试': self._decompose_testing,
            '部署': self._decompose_deployment,
            '学习': self._decompose_learning,
            '研究': self._decompose_research,
            '创建': self._decompose_creation,
            '分析': self._decompose_analysis,
        }
    
    def decompose(self, task_name: str, description: str = "") -> List[Dict]:
        """分解任务"""
        text = (task_name + " " + description).lower()
        
        # 更智能的关键词匹配
        if any(kw in text for kw in ['开发', '功能', 'feature', 'develop']):
            return self._decompose_development(task_name, description)
        elif any(kw in text for kw in ['写代码', '编程', 'code', 'program', 'python', 'c', 'java']):
            return self._decompose_coding(task_name, description)
        elif any(kw in text for kw in ['测试', 'test', 'testing']):
            return self._decompose_testing(task_name, description)
        elif any(kw in text for kw in ['部署', 'deploy', '上线']):
            return self._decompose_deployment(task_name, description)
        elif any(kw in text for kw in ['学习', 'learn', 'study']):
            return self._decompose_learning(task_name, description)
        elif any(kw in text for kw in ['研究', 'research', '调研']):
            return self._decompose_research(task_name, description)
        elif any(kw in text for kw in ['创建', 'create', 'build', '制作']):
            return self._decompose_creation(task_name, description)
        elif any(kw in text for kw in ['分析', 'analyze', 'analysis']):
            return self._decompose_analysis(task_name, description)
        
        # 默认分解
        return self._default_decompose(task_name, description)
    
    def _decompose_development(self, name: str, desc: str) -> List[Dict]:
        """开发功能分解"""
        return [
            {'name': '需求分析', 'description': '分析功能需求', 'estimated_time': 30},
            {'name': '设计方案', 'description': '设计实现方案', 'estimated_time': 60},
            {'name': '编写代码', 'description': '实现功能代码', 'estimated_time': 120},
            {'name': '代码审查', 'description': '审查代码质量', 'estimated_time': 30},
            {'name': '单元测试', 'description': '编写和运行测试', 'estimated_time': 60},
            {'name': '集成测试', 'description': '集成测试验证', 'estimated_time': 30},
        ]
    
    def _decompose_coding(self, name: str, desc: str) -> List[Dict]:
        """写代码分解"""
        return [
            {'name': '理解需求', 'description': '理解代码需求', 'estimated_time': 15},
            {'name': '设计结构', 'description': '设计代码结构', 'estimated_time': 30},
            {'name': '编写实现', 'description': '编写代码实现', 'estimated_time': 90},
            {'name': '代码格式化', 'description': '格式化代码', 'estimated_time': 10},
            {'name': '添加注释', 'description': '添加文档注释', 'estimated_time': 20},
            {'name': '测试验证', 'description': '测试代码功能', 'estimated_time': 30},
        ]
    
    def _decompose_testing(self, name: str, desc: str) -> List[Dict]:
        """测试分解"""
        return [
            {'name': '准备测试环境', 'description': '搭建测试环境', 'estimated_time': 30},
            {'name': '编写测试用例', 'description': '设计测试用例', 'estimated_time': 60},
            {'name': '执行测试', 'description': '运行测试', 'estimated_time': 30},
            {'name': '分析结果', 'description': '分析测试结果', 'estimated_time': 30},
            {'name': '修复问题', 'description': '修复发现的问题', 'estimated_time': 60},
        ]
    
    def _decompose_deployment(self, name: str, desc: str) -> List[Dict]:
        """部署分解"""
        return [
            {'name': '准备部署包', 'description': '构建部署包', 'estimated_time': 30},
            {'name': '配置环境', 'description': '配置目标环境', 'estimated_time': 60},
            {'name': '部署应用', 'description': '部署到服务器', 'estimated_time': 30},
            {'name': '验证部署', 'description': '验证部署成功', 'estimated_time': 30},
            {'name': '监控运行', 'description': '监控运行状态', 'estimated_time': 60},
        ]
    
    def _decompose_learning(self, name: str, desc: str) -> List[Dict]:
        """学习任务分解"""
        return [
            {'name': '确定学习目标', 'description': '明确学习内容', 'estimated_time': 15},
            {'name': '收集资料', 'description': '收集学习资源', 'estimated_time': 30},
            {'name': '学习基础知识', 'description': '学习基础概念', 'estimated_time': 120},
            {'name': '实践练习', 'description': '动手实践', 'estimated_time': 120},
            {'name': '总结复习', 'description': '总结知识点', 'estimated_time': 30},
        ]
    
    def _decompose_research(self, name: str, desc: str) -> List[Dict]:
        """研究任务分解"""
        return [
            {'name': '定义研究问题', 'description': '明确研究目标', 'estimated_time': 30},
            {'name': '文献调研', 'description': '调研相关资料', 'estimated_time': 120},
            {'name': '整理信息', 'description': '整理收集的信息', 'estimated_time': 60},
            {'name': '分析总结', 'description': '分析并总结', 'estimated_time': 90},
            {'name': '撰写报告', 'description': '写研究报告', 'estimated_time': 90},
        ]
    
    def _decompose_creation(self, name: str, desc: str) -> List[Dict]:
        """创建任务分解"""
        return [
            {'name': '需求分析', 'description': '分析创建需求', 'estimated_time': 30},
            {'name': '设计方案', 'description': '设计创建方案', 'estimated_time': 60},
            {'name': '创建内容', 'description': '创建具体内容', 'estimated_time': 120},
            {'name': '审查优化', 'description': '审查并优化', 'estimated_time': 60},
            {'name': '完成交付', 'description': '完成并交付', 'estimated_time': 30},
        ]
    
    def _decompose_analysis(self, name: str, desc: str) -> List[Dict]:
        """分析任务分解"""
        return [
            {'name': '收集数据', 'description': '收集分析数据', 'estimated_time': 60},
            {'name': '数据预处理', 'description': '预处理数据', 'estimated_time': 60},
            {'name': '分析数据', 'description': '分析数据', 'estimated_time': 120},
            {'name': '得出结论', 'description': '得出结论', 'estimated_time': 60},
            {'name': '撰写报告', 'description': '写分析报告', 'estimated_time': 60},
        ]
    
    def _default_decompose(self, name: str, desc: str) -> List[Dict]:
        """默认分解"""
        return [
            {'name': f'准备{name}', 'description': '准备工作', 'estimated_time': 30},
            {'name': f'执行{name}', 'description': '执行任务', 'estimated_time': 90},
            {'name': f'完成{name}', 'description': '收尾工作', 'estimated_time': 30},
        ]


class TaskExecutor:
    """任务执行器"""
    
    def __init__(self, planner: TaskPlanner):
        self.planner = planner
        self.current_task: Optional[Task] = None
    
    def execute_next(self) -> Optional[Task]:
        """执行下一个就绪任务"""
        ready_tasks = self.planner.get_ready_tasks()
        
        if not ready_tasks:
            return None
        
        # 选择优先级最高的
        task = ready_tasks[0]
        self.current_task = task
        
        # 更新状态为运行中
        self.planner.update_task_status(task.id, TaskStatus.RUNNING)
        
        return task
    
    def complete_task(self, task_id: int, result: str):
        """完成任务"""
        self.planner.update_task_status(task_id, TaskStatus.COMPLETED, result=result)
    
    def fail_task(self, task_id: int, error: str):
        """任务失败"""
        self.planner.update_task_status(task_id, TaskStatus.FAILED, error=error)


if __name__ == '__main__':
    # 测试
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         📋 任务规划系统测试                            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 创建规划器
    planner = TaskPlanner()
    planner.clear_all()
    
    # 创建分解器
    decomposer = TaskDecomposer()
    
    # 测试任务分解
    print("测试任务分解:")
    subtasks = decomposer.decompose("开发功能", "开发一个新功能")
    print(f"  分解为 {len(subtasks)} 个子任务:")
    for i, task in enumerate(subtasks, 1):
        print(f"    {i}. {task['name']} - {task['estimated_time']}分钟")
    
    print("\n创建主任务并分解:")
    
    # 创建主任务
    main_task_id = planner.create_task(
        name="开发用户登录功能",
        description="开发一个完整的用户登录功能",
        priority=TaskPriority.HIGH,
        estimated_time=300
    )
    
    # 分解并创建子任务
    subtasks = decomposer.decompose("开发用户登录功能")
    parent_id = None
    
    for subtask in subtasks:
        subtask_id = planner.create_task(
            name=subtask['name'],
            description=subtask['description'],
            estimated_time=subtask['estimated_time'],
            parent_id=main_task_id
        )
        planner.add_subtask(main_task_id, subtask_id)
    
    # 显示任务树
    print(f"\n任务树:")
    main_task = planner.get_task(main_task_id)
    print(f"  📋 {main_task.name} ({main_task.status.value})")
    
    for subtask_id in main_task.subtasks:
        subtask = planner.get_task(subtask_id)
        print(f"    ├─ {subtask.name} - {subtask.estimated_time}分钟")
    
    # 获取就绪任务
    ready = planner.get_ready_tasks()
    print(f"\n可执行任务：{len(ready)}个")
    
    print("\n✅ 测试完成！")
