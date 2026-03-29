#!/usr/bin/env python3
"""
日报生成器

自动分析当天的：
- Git 提交
- 文件修改
- 实验运行记录
- 任务完成情况

生成工作日报
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import os


class DailyReportGenerator:
    """日报生成器"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.project_root = Path(self.config.get('project_root', '.'))
        self.git_repo = self.config.get('git_repo', True)
        self.include_experiments = self.config.get('include_experiments', True)
        self.include_files = self.config.get('include_files', True)
    
    def generate(self, date: Optional[datetime] = None) -> str:
        """
        生成日报
        
        Args:
            date: 日期（默认今天）
            
        Returns:
            str: 日报内容
        """
        if date is None:
            date = datetime.now()
        
        report = []
        
        # 标题
        report.append(self._generate_header(date))
        
        # 今日概览
        report.append(self._generate_overview(date))
        
        # Git 提交
        if self.git_repo:
            report.append(self._generate_git_commits(date))
        
        # 实验运行
        if self.include_experiments:
            report.append(self._generate_experiment_log(date))
        
        # 文件修改
        if self.include_files:
            report.append(self._generate_file_changes(date))
        
        # 明日计划
        report.append(self._generate_tomorrow_plan())
        
        # 总结
        report.append(self._generate_summary())
        
        return '\n'.join(report)
    
    def _generate_header(self, date: datetime) -> str:
        """生成头部"""
        lines = []
        lines.append("╔════════════════════════════════════════════════════════╗")
        lines.append("║              📝 工作日报                               ║")
        lines.append("╠════════════════════════════════════════════════════════╣")
        lines.append(f"║  日期：{date.strftime('%Y年%m月%d日')} {self._get_weekday(date)}                  ║")
        lines.append(f"║  生成时间：{datetime.now().strftime('%H:%M:%S')}                           ║")
        lines.append(f"║  项目：indie-ai                                      ║")
        lines.append("╚════════════════════════════════════════════════════════╝")
        return '\n'.join(lines)
    
    def _get_weekday(self, date: datetime) -> str:
        """获取星期"""
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[date.weekday()]
    
    def _generate_overview(self, date: datetime) -> str:
        """生成今日概览"""
        lines = []
        lines.append("")
        lines.append("━━━ 📊 今日概览 ━━━")
        lines.append("")
        
        # 统计信息
        stats = self._collect_stats(date)
        
        lines.append(f"  • Git 提交：{stats.get('commits', 0)} 次")
        lines.append(f"  • 实验运行：{stats.get('experiments', 0)} 次")
        lines.append(f"  • 文件修改：{stats.get('files_changed', 0)} 个")
        lines.append(f"  • 代码增量：+{stats.get('additions', 0)} -{stats.get('deletions', 0)} 行")
        lines.append("")
        
        # 工作效率评分
        score = self._calculate_productivity_score(stats)
        lines.append(f"  🎯 今日效率评分：{score}/100")
        lines.append("")
        
        return '\n'.join(lines)
    
    def _collect_stats(self, date: datetime) -> Dict:
        """收集统计数据"""
        stats = {
            'commits': 0,
            'experiments': 0,
            'files_changed': 0,
            'additions': 0,
            'deletions': 0
        }
        
        # Git 统计
        if self.git_repo:
            try:
                # 提交数
                result = subprocess.run(
                    ['git', 'log', '--since', date.strftime('%Y-%m-%d'), 
                     '--until', (date + timedelta(days=1)).strftime('%Y-%m-%d'),
                     '--oneline'],
                    capture_output=True, text=True, cwd=self.project_root
                )
                stats['commits'] = len([l for l in result.stdout.split('\n') if l.strip()])
                
                # 文件变更
                result = subprocess.run(
                    ['git', 'diff', '--shortstat',
                     date.strftime('%Y-%m-%d'),
                     (date + timedelta(days=1)).strftime('%Y-%m-%d')],
                    capture_output=True, text=True, cwd=self.project_root
                )
                
                # 解析输出
                output = result.stdout
                if 'files changed' in output:
                    parts = output.split(',')
                    for part in parts:
                        if 'files changed' in part:
                            stats['files_changed'] = int(part.split()[0])
                        elif 'insertions' in part or 'addition' in part:
                            stats['additions'] = int(part.split()[0])
                        elif 'deletions' in part or 'deletion' in part:
                            stats['deletions'] = int(part.split()[0])
            except Exception as e:
                pass
        
        # 实验统计（从日志文件读取）
        if self.include_experiments:
            log_file = self.project_root / 'experiment_log.json'
            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        logs = json.load(f)
                        today = date.strftime('%Y-%m-%d')
                        stats['experiments'] = len([
                            l for l in logs 
                            if l.get('date', '').startswith(today)
                        ])
                except:
                    pass
        
        return stats
    
    def _calculate_productivity_score(self, stats: Dict) -> int:
        """计算效率评分"""
        score = 0
        
        # Git 提交（最多 30 分）
        commits = min(stats.get('commits', 0), 10)
        score += commits * 3
        
        # 实验运行（最多 30 分）
        experiments = min(stats.get('experiments', 0), 5)
        score += experiments * 6
        
        # 代码量（最多 40 分）
        additions = stats.get('additions', 0)
        if additions > 0:
            score += min(40, additions // 10)
        
        return min(100, score)
    
    def _generate_git_commits(self, date: datetime) -> str:
        """生成 Git 提交记录"""
        lines = []
        lines.append("")
        lines.append("━━━ 💻 Git 提交 ━━━")
        lines.append("")
        
        try:
            result = subprocess.run(
                ['git', 'log', '--since', date.strftime('%Y-%m-%d'),
                 '--until', (date + timedelta(days=1)).strftime('%Y-%m-%d'),
                 '--pretty=format:%h - %s (%an, %ar)',
                 '--stat'],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            if result.stdout.strip():
                lines.append(result.stdout)
            else:
                lines.append("  今天没有提交")
        except Exception as e:
            lines.append(f"  无法获取 Git 记录：{e}")
        
        lines.append("")
        return '\n'.join(lines)
    
    def _generate_experiment_log(self, date: datetime) -> str:
        """生成实验运行记录"""
        lines = []
        lines.append("")
        lines.append("━━━ 🧪 实验运行 ━━━")
        lines.append("")
        
        # 查找实验日志
        log_file = self.project_root / 'experiment_log.json'
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    today = date.strftime('%Y-%m-%d')
                    today_logs = [l for l in logs if l.get('date', '').startswith(today)]
                
                if today_logs:
                    for log in today_logs[:10]:  # 最多显示 10 条
                        script = log.get('script', '未知')
                        status = '✅' if log.get('success', False) else '❌'
                        duration = log.get('duration', 0)
                        lines.append(f"  {status} {script} ({duration:.1f}秒)")
                else:
                    lines.append("  今天没有运行实验")
            except:
                lines.append("  无法读取实验日志")
        else:
            lines.append("  无实验日志文件")
        
        lines.append("")
        return '\n'.join(lines)
    
    def _generate_file_changes(self, date: datetime) -> str:
        """生成文件修改记录"""
        lines = []
        lines.append("")
        lines.append("━━━ 📁 文件修改 ━━━")
        lines.append("")
        
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-status',
                 date.strftime('%Y-%m-%d'),
                 (date + timedelta(days=1)).strftime('%Y-%m-%d')],
                capture_output=True, text=True, cwd=self.project_root
            )
            
            if result.stdout.strip():
                changed_files = []
                for line in result.stdout.split('\n'):
                    if line.strip():
                        status, *files = line.split('\t')
                        status_map = {'A': '🆕', 'M': '✏️', 'D': '🗑️', 'R': '🔄'}
                        icon = status_map.get(status, '📄')
                        filename = files[0] if files else '未知'
                        changed_files.append(f"  {icon} {filename}")
                
                lines.extend(changed_files[:20])  # 最多显示 20 个
                if len(changed_files) > 20:
                    lines.append(f"  ... 还有 {len(changed_files) - 20} 个文件")
            else:
                lines.append("  今天没有文件修改")
        except Exception as e:
            lines.append(f"  无法获取文件变更记录：{e}")
        
        lines.append("")
        return '\n'.join(lines)
    
    def _generate_tomorrow_plan(self) -> str:
        """生成明日计划"""
        lines = []
        lines.append("")
        lines.append("━━━ 📋 明日计划 ━━━")
        lines.append("")
        lines.append("  [ ] 待办事项 1")
        lines.append("  [ ] 待办事项 2")
        lines.append("  [ ] 待办事项 3")
        lines.append("")
        return '\n'.join(lines)
    
    def _generate_summary(self) -> str:
        """生成总结"""
        lines = []
        lines.append("")
        lines.append("━━━ 💭 今日总结 ━━━")
        lines.append("")
        lines.append("  今日工作总结和反思...")
        lines.append("")
        lines.append("╔════════════════════════════════════════════════════════╗")
        lines.append("║  明天继续加油！💪                                     ║")
        lines.append("╚════════════════════════════════════════════════════════╝")
        return '\n'.join(lines)
    
    def save_report(self, output_path: Optional[str] = None) -> str:
        """保存日报到文件"""
        if output_path is None:
            output_path = f"daily_report_{datetime.now().strftime('%Y%m%d')}.md"
        
        report = self.generate()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path


# 快捷函数
def generate_daily_report(date: Optional[datetime] = None, 
                          save: bool = True) -> str:
    """
    快速生成日报
    
    Args:
        date: 日期（默认今天）
        save: 是否保存到文件
        
    Returns:
        str: 日报内容或文件路径
    """
    generator = DailyReportGenerator()
    
    if save:
        return generator.save_report()
    else:
        return generator.generate(date)


if __name__ == '__main__':
    report = generate_daily_report(save=False)
    print(report)
    
    # 保存到文件
    output_file = generate_daily_report(save=True)
    print(f"\n日报已保存到：{output_file}")
