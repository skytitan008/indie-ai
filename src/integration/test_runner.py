#!/usr/bin/env python3
"""
测试运行器

支持：
- pytest
- unittest
- 自定义测试命令
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import json


class TestRunner:
    """测试运行器"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.test_framework = self.config.get('framework', 'pytest')
        self.test_dir = self.config.get('test_dir', 'tests')
        self.coverage = self.config.get('coverage', False)
        self.verbose = self.config.get('verbose', True)
        
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'duration': 0,
            'tests': []
        }
    
    def run_tests(self, test_path: Optional[str] = None, 
                  pattern: str = "test_*.py") -> dict:
        """
        运行测试
        
        Args:
            test_path: 测试文件或目录路径
            pattern: 测试文件匹配模式
            
        Returns:
            dict: 测试结果
        """
        if test_path is None:
            test_path = self.test_dir
        
        path = Path(test_path)
        if not path.exists():
            return {
                'success': False,
                'error': f'测试路径不存在：{test_path}'
            }
        
        if self.test_framework == 'pytest':
            return self._run_pytest(path, pattern)
        elif self.test_framework == 'unittest':
            return self._run_unittest(path, pattern)
        else:
            return {
                'success': False,
                'error': f'不支持的测试框架：{self.test_framework}'
            }
    
    def _run_pytest(self, path: Path, pattern: str) -> dict:
        """运行 pytest"""
        cmd = ['pytest', str(path), '-k', pattern.split('*')[1] if '*' in pattern else pattern]
        
        if self.verbose:
            cmd.append('-v')
        
        if self.coverage:
            cmd.extend(['--cov', str(path.parent)])
        
        cmd.extend(['--tb=short', '--json-report'])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 分钟超时
            )
            
            # 解析输出
            output = result.stdout + result.stderr
            self._parse_pytest_output(output)
            
            self.results['success'] = result.returncode == 0
            self.results['duration'] = self._parse_duration(output)
            
            return self.results
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '测试运行超时（>5 分钟）'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'测试运行错误：{str(e)}'
            }
    
    def _parse_pytest_output(self, output: str):
        """解析 pytest 输出"""
        lines = output.split('\n')
        
        for line in lines:
            if 'passed' in line:
                # 解析通过数
                pass
            elif 'failed' in line:
                # 解析失败数
                pass
        
        # 简化处理：统计关键字
        self.results['passed'] = output.count(' PASSED')
        self.results['failed'] = output.count(' FAILED')
        self.results['errors'] = output.count(' ERROR')
        self.results['skipped'] = output.count(' SKIPPED')
        self.results['total'] = (
            self.results['passed'] + 
            self.results['failed'] + 
            self.results['errors'] + 
            self.results['skipped']
        )
    
    def _parse_duration(self, output: str) -> float:
        """解析测试耗时"""
        import re
        match = re.search(r'in (\d+\.?\d*)s', output)
        if match:
            return float(match.group(1))
        return 0.0
    
    def _run_unittest(self, path: Path, pattern: str) -> dict:
        """运行 unittest"""
        cmd = [sys.executable, '-m', 'unittest', 'discover', '-s', str(path), '-p', pattern]
        
        if self.verbose:
            cmd.append('-v')
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            output = result.stdout + result.stderr
            
            # 解析 unittest 输出
            self._parse_unittest_output(output)
            
            self.results['success'] = result.returncode == 0
            
            return self.results
            
        except Exception as e:
            return {
                'success': False,
                'error': f'测试运行错误：{str(e)}'
            }
    
    def _parse_unittest_output(self, output: str):
        """解析 unittest 输出"""
        import re
        
        # 解析 "Ran X tests in Y.YYYs"
        match = re.search(r'Ran (\d+) tests in (\d+\.?\d*)s', output)
        if match:
            self.results['total'] = int(match.group(1))
            self.results['duration'] = float(match.group(2))
        
        # 解析失败和错误
        if 'FAILED' in output:
            failures = output.count('FAIL:')
            errors = output.count('ERROR:')
            self.results['failed'] = failures
            self.results['errors'] = errors
            self.results['passed'] = self.results['total'] - failures - errors
    
    def run_single_test(self, test_file: str, test_name: str) -> dict:
        """运行单个测试"""
        cmd = [
            sys.executable, '-m', 'pytest',
            f'{test_file}::{test_name}',
            '-v', '--tb=short'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_report(self) -> str:
        """生成测试报告"""
        report = []
        report.append("╔════════════════════════════════════════════════════════╗")
        report.append("║           🧪 测试运行报告                              ║")
        report.append("╠════════════════════════════════════════════════════════╣")
        report.append(f"║  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║")
        report.append(f"║  框架：{self.test_framework:<45} ║")
        report.append("╠════════════════════════════════════════════════════════╣")
        
        # 统计信息
        total = self.results.get('total', 0)
        passed = self.results.get('passed', 0)
        failed = self.results.get('failed', 0)
        errors = self.results.get('errors', 0)
        skipped = self.results.get('skipped', 0)
        duration = self.results.get('duration', 0)
        
        report.append(f"║  总计：{total:<6}个测试                                   ║")
        report.append(f"║  ✓ 通过：{passed:<6}个                                     ║")
        
        if failed > 0:
            report.append(f"║  ✗ 失败：{failed:<6}个  ⚠️                                ║")
        else:
            report.append(f"║  ✗ 失败：{failed:<6}个                                     ║")
        
        if errors > 0:
            report.append(f"║  ⚠ 错误：{errors:<6}个  ⚠️                                ║")
        else:
            report.append(f"║  ⚠ 错误：{errors:<6}个                                     ║")
        
        report.append(f"║  ⊘ 跳过：{skipped:<6}个                                     ║")
        report.append(f"║  ⏱ 耗时：{duration:.2f}秒                                   ║")
        
        # 成功率
        if total > 0:
            success_rate = (passed / total) * 100
            report.append("╠════════════════════════════════════════════════════════╣")
            if success_rate >= 90:
                report.append(f"║  成功率：{success_rate:.1f}%  ✅                              ║")
            elif success_rate >= 70:
                report.append(f"║  成功率：{success_rate:.1f}%  ⚠️                             ║")
            else:
                report.append(f"║  成功率：{success_rate:.1f}%  ❌                             ║")
        
        # 结论
        report.append("╠════════════════════════════════════════════════════════╣")
        if self.results.get('success', False):
            report.append("║  结论：✅ 所有测试通过！                               ║")
        else:
            report.append("║  结论：❌ 有测试失败或错误                             ║")
        
        report.append("╚════════════════════════════════════════════════════════╝")
        
        return '\n'.join(report)
    
    def save_report(self, output_path: str = 'test_report.json'):
        """保存测试报告为 JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'framework': self.test_framework,
                'results': self.results
            }, f, indent=2, ensure_ascii=False)


# 快捷函数
def run_tests(path: str = 'tests', framework: str = 'pytest', 
              coverage: bool = False) -> TestRunner:
    """
    快速运行测试
    
    Args:
        path: 测试目录
        framework: 测试框架
        coverage: 是否生成覆盖率报告
        
    Returns:
        TestRunner 实例
    """
    runner = TestRunner({
        'framework': framework,
        'test_dir': path,
        'coverage': coverage
    })
    
    runner.run_tests()
    return runner


if __name__ == '__main__':
    import sys
    
    test_path = sys.argv[1] if len(sys.argv) > 1 else 'tests'
    
    runner = run_tests(test_path)
    print(runner.get_report())
    
    # 保存 JSON 报告
    runner.save_report()
    print(f"\n报告已保存到：test_report.json")
