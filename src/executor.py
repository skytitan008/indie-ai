"""
真实任务执行器

让 AI 真正执行 Python 脚本和系统命令
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """任务类型"""
    PYTHON_SCRIPT = "python_script"
    SHELL_COMMAND = "shell_command"
    FILE_OPERATION = "file_operation"
    REPORT_GENERATION = "report_generation"


@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    output: str
    error: str
    duration: float
    exit_code: int


class TaskExecutor:
    """
    任务执行器
    
    执行真实的 Python 脚本和系统命令
    """
    
    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace)
        self.execution_history = []
    
    def execute_python(
        self,
        script_path: str,
        args: list = None,
        timeout: int = 300
    ) -> ExecutionResult:
        """
        执行 Python 脚本
        
        Args:
            script_path: 脚本路径
            args: 命令行参数
            timeout: 超时时间（秒）
        """
        script = self.workspace / script_path
        
        if not script.exists():
            return ExecutionResult(
                success=False,
                output="",
                error=f"脚本不存在：{script_path}",
                duration=0,
                exit_code=-1
            )
        
        cmd = ["python3", str(script)]
        if args:
            cmd.extend(args)
        
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.workspace)
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            execution_result = ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                duration=duration,
                exit_code=result.returncode
            )
            
            self._record_execution("python", script_path, execution_result)
            
            return execution_result
            
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error=f"执行超时（>{timeout}秒）",
                duration=timeout,
                exit_code=-1
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                duration=0,
                exit_code=-1
            )
    
    def execute_shell(
        self,
        command: str,
        timeout: int = 60
    ) -> ExecutionResult:
        """
        执行 Shell 命令
        """
        start_time = datetime.now()
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.workspace)
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            execution_result = ExecutionResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                duration=duration,
                exit_code=result.returncode
            )
            
            self._record_execution("shell", command, execution_result)
            
            return execution_result
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                duration=0,
                exit_code=-1
            )
    
    def format_code(self, file_pattern: str = "*.py") -> ExecutionResult:
        """
        格式化代码（使用 black）
        """
        cmd = f"black {file_pattern}"
        return self.execute_shell(cmd)
    
    def run_tests(self, test_path: str = "tests/") -> ExecutionResult:
        """
        运行测试
        """
        cmd = f"pytest {test_path} -v"
        return self.execute_shell(cmd)
    
    def generate_report(self, output_file: str = "daily_report.md") -> ExecutionResult:
        """
        生成日报
        """
        from datetime import date
        
        report_content = f"""# 日报 - {date.today()}

## 完成的任务

（待填充）

## 遇到的问题

（待填充）

## 明日计划

（待填充）

---
*自动生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        report_path = self.workspace / output_file
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            return ExecutionResult(
                success=True,
                output=f"报告已生成：{output_file}",
                error="",
                duration=0,
                exit_code=0
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                duration=0,
                exit_code=-1
            )
    
    def _record_execution(
        self,
        task_type: str,
        target: str,
        result: ExecutionResult
    ):
        """记录执行历史"""
        self.execution_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': task_type,
            'target': target,
            'success': result.success,
            'duration': result.duration
        })
    
    def get_execution_stats(self) -> Dict:
        """获取执行统计"""
        if not self.execution_history:
            return {'total': 0}
        
        total = len(self.execution_history)
        success = sum(1 for e in self.execution_history if e['success'])
        avg_duration = sum(e['duration'] for e in self.execution_history) / total
        
        return {
            'total': total,
            'success': success,
            'failed': total - success,
            'success_rate': success / total,
            'avg_duration': avg_duration
        }


class AIAgentWithExecution:
    """
    带执行能力的 AI Agent
    
    整合 IndependentAgent 和 TaskExecutor
    """
    
    def __init__(self, agent, workspace: str = "."):
        self.agent = agent
        self.executor = TaskExecutor(workspace)
        self.task_mappings = {}  # 任务名 → 执行脚本
    
    def map_task_to_script(self, task_name: str, script_path: str):
        """
        将任务映射到实际执行的脚本
        
        Args:
            task_name: AI 任务名
            script_path: 要执行的脚本路径
        """
        self.task_mappings[task_name] = script_path
    
    def execute_current_task(self) -> Dict:
        """
        执行当前 AI 选择的任务
        """
        if not self.agent.current_task:
            return {'success': False, 'message': '没有当前任务'}
        
        task = self.agent.current_task
        task_name = task.name
        
        # 检查是否有映射的脚本
        if task_name in self.task_mappings:
            script_path = self.task_mappings[task_name]
            result = self.executor.execute_python(script_path)
            
            return {
                'success': result.success,
                'message': f"执行脚本：{script_path}",
                'output': result.output[:500] if result.output else "",
                'error': result.error[:200] if result.error else "",
                'duration': result.duration
            }
        
        # 默认：模拟执行
        return self.agent.act()
    
    def run_auto_format(self) -> Dict:
        """运行代码格式化"""
        result = self.executor.format_code()
        return {
            'success': result.success,
            'message': "代码格式化完成",
            'output': result.output
        }
    
    def run_tests(self) -> Dict:
        """运行测试"""
        result = self.executor.run_tests()
        return {
            'success': result.success,
            'message': "测试完成",
            'output': result.output[:1000] if result.output else ""
        }
    
    def generate_daily_report(self) -> Dict:
        """生成日报"""
        result = self.executor.generate_report()
        return {
            'success': result.success,
            'message': "日报已生成",
            'output': result.output
        }
