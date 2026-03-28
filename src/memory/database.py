"""
记忆系统 - SQLite 数据库存储

持久化存储任务、经验、决策日志等
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from ..core.models import Task, TaskStatus, Experience, DecisionLog, Goal


class MemoryDatabase:
    """
    SQLite 记忆数据库
    
    持久化存储 AI 系统的记忆
    """
    
    def __init__(self, db_path: str = "ai_memory.db"):
        self.db_path = db_path
        self.conn = None
        self._initialize_database()
    
    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def _initialize_database(self):
        """初始化数据库表"""
        self.connect()
        cursor = self.conn.cursor()
        
        # 任务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                priority INTEGER,
                estimated_time INTEGER,
                actual_time INTEGER,
                deadline TIMESTAMP,
                dependencies TEXT,
                status TEXT,
                created_at TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        ''')
        
        # 目标表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                sub_goals TEXT,
                priority INTEGER,
                deadline TIMESTAMP,
                progress REAL,
                created_at TIMESTAMP
            )
        ''')
        
        # 经验表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiences (
                id TEXT PRIMARY KEY,
                timestamp TIMESTAMP,
                state TEXT,
                action TEXT,
                reward REAL,
                next_state TEXT,
                lesson TEXT
            )
        ''')
        
        # 决策日志表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS decision_logs (
                id TEXT PRIMARY KEY,
                timestamp TIMESTAMP,
                situation TEXT,
                options TEXT,
                chosen TEXT,
                reasoning TEXT,
                utilities TEXT,
                outcome TEXT
            )
        ''')
        
        # 性能记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP,
                metric_name TEXT,
                expected REAL,
                actual REAL,
                context TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_experiences_reward ON experiences(reward)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_decision_logs_timestamp ON decision_logs(timestamp)')
        
        self.conn.commit()
        self.close()
    
    # ========== 任务操作 ==========
    
    def save_task(self, task: Task):
        """保存任务"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tasks 
            (id, name, description, priority, estimated_time, actual_time, 
             deadline, dependencies, status, created_at, started_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id,
            task.name,
            task.description,
            task.priority,
            task.estimated_time,
            task.actual_time,
            task.deadline.isoformat() if task.deadline else None,
            json.dumps(task.dependencies),
            task.status.value,
            task.created_at.isoformat(),
            task.started_at.isoformat() if task.started_at else None,
            task.completed_at.isoformat() if task.completed_at else None
        ))
        
        self.conn.commit()
        self.close()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        self.close()
        
        if not row:
            return None
        
        return self._row_to_task(row)
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        rows = cursor.fetchall()
        self.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def get_pending_tasks(self) -> List[Task]:
        """获取待处理任务"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute(
            'SELECT * FROM tasks WHERE status = ? ORDER BY priority DESC',
            (TaskStatus.PENDING.value,)
        )
        rows = cursor.fetchall()
        self.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """将数据库行转换为 Task 对象"""
        return Task(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            priority=row['priority'],
            estimated_time=row['estimated_time'],
            actual_time=row['actual_time'],
            deadline=datetime.fromisoformat(row['deadline']) if row['deadline'] else None,
            dependencies=json.loads(row['dependencies']) if row['dependencies'] else [],
            status=TaskStatus(row['status']),
            created_at=datetime.fromisoformat(row['created_at']),
            started_at=datetime.fromisoformat(row['started_at']) if row['started_at'] else None,
            completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None
        )
    
    # ========== 经验操作 ==========
    
    def save_experience(self, experience: Experience):
        """保存经验"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO experiences 
            (id, timestamp, state, action, reward, next_state, lesson)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            experience.id,
            experience.timestamp.isoformat(),
            json.dumps(experience.state),
            experience.action,
            experience.reward,
            json.dumps(experience.next_state),
            experience.lesson
        ))
        
        self.conn.commit()
        self.close()
    
    def get_experiences(self, limit: int = 100) -> List[Experience]:
        """获取经验记录"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute(
            'SELECT * FROM experiences ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        rows = cursor.fetchall()
        self.close()
        
        return [self._row_to_experience(row) for row in rows]
    
    def _row_to_experience(self, row: sqlite3.Row) -> Experience:
        """将数据库行转换为 Experience 对象"""
        return Experience(
            id=row['id'],
            timestamp=datetime.fromisoformat(row['timestamp']),
            state=json.loads(row['state']),
            action=row['action'],
            reward=row['reward'],
            next_state=json.loads(row['next_state']),
            lesson=row['lesson'] or ""
        )
    
    # ========== 决策日志操作 ==========
    
    def save_decision_log(self, log: DecisionLog):
        """保存决策日志"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO decision_logs 
            (id, timestamp, situation, options, chosen, reasoning, utilities, outcome)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log.id,
            log.timestamp.isoformat(),
            log.situation,
            json.dumps(log.options),
            log.chosen,
            log.reasoning,
            json.dumps(log.utilities),
            log.outcome
        ))
        
        self.conn.commit()
        self.close()
    
    def get_decision_logs(self, limit: int = 50) -> List[DecisionLog]:
        """获取决策日志"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute(
            'SELECT * FROM decision_logs ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        rows = cursor.fetchall()
        self.close()
        
        return [self._row_to_decision_log(row) for row in rows]
    
    def _row_to_decision_log(self, row: sqlite3.Row) -> DecisionLog:
        """将数据库行转换为 DecisionLog 对象"""
        return DecisionLog(
            id=row['id'],
            timestamp=datetime.fromisoformat(row['timestamp']),
            situation=row['situation'],
            options=json.loads(row['options']),
            chosen=row['chosen'],
            reasoning=row['reasoning'],
            utilities=json.loads(row['utilities']) if row['utilities'] else {},
            outcome=row['outcome'] or ""
        )
    
    # ========== 统计操作 ==========
    
    def get_stats(self) -> Dict:
        """获取数据库统计"""
        self.connect()
        cursor = self.conn.cursor()
        
        stats = {}
        
        # 任务统计
        cursor.execute('SELECT COUNT(*) FROM tasks')
        stats['total_tasks'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = ?', (TaskStatus.COMPLETED.value,))
        stats['completed_tasks'] = cursor.fetchone()[0]
        
        # 经验统计
        cursor.execute('SELECT COUNT(*) FROM experiences')
        stats['total_experiences'] = cursor.fetchone()[0]
        
        # 决策日志统计
        cursor.execute('SELECT COUNT(*) FROM decision_logs')
        stats['total_decisions'] = cursor.fetchone()[0]
        
        self.close()
        return stats
    
    def clear_all(self):
        """清空所有数据（调试用）"""
        self.connect()
        cursor = self.conn.cursor()
        
        cursor.execute('DELETE FROM tasks')
        cursor.execute('DELETE FROM goals')
        cursor.execute('DELETE FROM experiences')
        cursor.execute('DELETE FROM decision_logs')
        cursor.execute('DELETE FROM performance_records')
        
        self.conn.commit()
        self.close()
