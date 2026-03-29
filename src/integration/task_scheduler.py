#!/usr/bin/env python3
"""
任务调度器

自动安排和执行日常任务：
- 每天早上：规划当日任务
- 工作期间：监控和执行
- 晚上：生成日报
"""

import schedule
import time
from datetime import datetime
from typing import Callable, Optional
from pathlib import Path
import json


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.project_root = Path(self.config.get('project_root', '.'))
        self.tasks = []
        self.running = False
    
    def schedule_morning_routine(self, time_str: str = "14:00"):
        """
        安排晨间例行任务
        
        Args:
            time_str: 执行时间（HH:MM 格式）
        """
        schedule.every().day.at(time_str).do(self._morning_routine)
        print(f"✅ 已安排晨间任务：每天 {time_str}")
    
    def schedule_evening_routine(self, time_str: str = "02:00"):
        """
        安排晚间例行任务
        
        Args:
            time_str: 执行时间（HH:MM 格式）
        """
        schedule.every().day.at(time_str).do(self._evening_routine)
        print(f"✅ 已安排晚间任务：每天 {time_str}")
    
    def _morning_routine(self):
        """晨间例行任务"""
        print("\n🌅 晨间任务开始...")
        
        # 1. 检查待办任务
        self._check_pending_tasks()
        
        # 2. 规划今日任务
        self._plan_today_tasks()
        
        # 3. 发送提醒（可选）
        self._send_morning_reminder()
        
        print("✅ 晨间任务完成\n")
    
    def _evening_routine(self):
        """晚间例行任务"""
        print("\n🌙 晚间任务开始...")
        
        # 1. 生成日报
        from .daily_report import DailyReportGenerator
        generator = DailyReportGenerator()
        report_file = generator.save_report()
        print(f"📝 日报已生成：{report_file}")
        
        # 2. 清理临时文件
        self._cleanup_temp_files()
        
        # 3. 发送提醒
        self._send_evening_reminder()
        
        print("✅ 晚间任务完成\n")
    
    def _check_pending_tasks(self):
        """检查待办任务"""
        task_file = self.project_root / 'tasks.json'
        if task_file.exists():
            with open(task_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
                pending = [t for t in tasks if t.get('status') == 'pending']
                print(f"📋 待办任务：{len(pending)} 个")
    
    def _plan_today_tasks(self):
        """规划今日任务"""
        print("📅 正在规划今日任务...")
        # 这里可以集成 AI 决策引擎
        pass
    
    def _send_morning_reminder(self):
        """发送晨间提醒"""
        print("🔔 晨间提醒：开始新一天的工作！")
    
    def _send_evening_reminder(self):
        """发送晚间提醒"""
        print("🔔 晚间提醒：该休息啦！")
    
    def _cleanup_temp_files(self):
        """清理临时文件"""
        print("🧹 清理临时文件...")
        temp_patterns = ['*.tmp', '*.bak', '*.log', '__pycache__']
        for pattern in temp_patterns:
            for file in self.project_root.rglob(pattern):
                try:
                    if file.is_file():
                        file.unlink()
                except:
                    pass
    
    def add_task(self, name: str, callback: Callable, 
                 interval: Optional[str] = None,
                 time_str: Optional[str] = None):
        """
        添加自定义任务
        
        Args:
            name: 任务名称
            callback: 回调函数
            interval: 间隔（hourly/daily/weekly）
            time_str: 具体时间（HH:MM）
        """
        if interval == 'hourly':
            schedule.every().hour.do(callback)
        elif interval == 'daily' and time_str:
            schedule.every().day.at(time_str).do(callback)
        elif interval == 'weekly':
            schedule.every().week.do(callback)
        
        self.tasks.append({
            'name': name,
            'callback': callback,
            'interval': interval,
            'time': time_str
        })
        
        print(f"✅ 已添加任务：{name}")
    
    def start(self):
        """启动调度器"""
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         ⏰ 任务调度器已启动                            ║")
        print("╠════════════════════════════════════════════════════════╣")
        print(f"║  项目：{self.project_root.absolute()}")
        print("║  按 Ctrl+C 停止                                        ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        self.running = True
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    def stop(self):
        """停止调度器"""
        self.running = False
        print("\n⏸️  任务调度器已停止")
    
    def run_pending(self):
        """运行待处理任务（手动调用）"""
        schedule.run_pending()


# 快捷函数
def start_scheduler(morning_time: str = "14:00", 
                    evening_time: str = "02:00"):
    """
    快速启动调度器
    
    Args:
        morning_time: 晨间任务时间
        evening_time: 晚间任务时间
    """
    scheduler = TaskScheduler()
    scheduler.schedule_morning_routine(morning_time)
    scheduler.schedule_evening_routine(evening_time)
    scheduler.start()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # 只运行一次（测试用）
        scheduler = TaskScheduler()
        scheduler._morning_routine()
        scheduler._evening_routine()
    else:
        # 持续运行
        start_scheduler()
