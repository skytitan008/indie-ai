#!/usr/bin/env python3
"""
代码格式化器

支持：
- black (Python)
- prettier (JavaScript/TypeScript)
- 自定义格式化规则
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class CodeFormatter:
    """代码格式化器"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.python_formatter = self.config.get('python_formatter', 'black')
        self.js_formatter = self.config.get('js_formatter', 'prettier')
        self.formatted_files: List[str] = []
        self.errors: List[str] = []
    
    def format_python(self, file_path: str, check_only: bool = False) -> bool:
        """
        格式化 Python 文件
        
        Args:
            file_path: 文件路径
            check_only: 只检查不修改
            
        Returns:
            bool: 是否成功
        """
        path = Path(file_path)
        if not path.exists():
            self.errors.append(f"文件不存在：{file_path}")
            return False
        
        if self.python_formatter == 'black':
            return self._format_with_black(path, check_only)
        elif self.python_formatter == 'autopep8':
            return self._format_with_autopep8(path, check_only)
        else:
            self.errors.append(f"未知的 Python 格式化器：{self.python_formatter}")
            return False
    
    def _format_with_black(self, path: Path, check_only: bool) -> bool:
        """使用 black 格式化"""
        cmd = ['black', '--quiet']
        if check_only:
            cmd.append('--check')
        cmd.append(str(path))
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.formatted_files.append(str(path))
                return True
            else:
                if check_only and result.returncode == 1:
                    # 需要格式化
                    self.formatted_files.append(str(path))
                    return True
                else:
                    self.errors.append(f"black 格式化失败：{result.stderr}")
                    return False
        except subprocess.TimeoutExpired:
            self.errors.append(f"black 格式化超时：{path}")
            return False
        except FileNotFoundError:
            self.errors.append("未找到 black，请安装：pip install black")
            return False
    
    def _format_with_autopep8(self, path: Path, check_only: bool) -> bool:
        """使用 autopep8 格式化"""
        cmd = ['autopep8', '--in-place'] if not check_only else ['autopep8', '--diff']
        cmd.append(str(path))
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.formatted_files.append(str(path))
                return True
            else:
                self.errors.append(f"autopep8 格式化失败：{result.stderr}")
                return False
        except Exception as e:
            self.errors.append(f"autopep8 错误：{str(e)}")
            return False
    
    def format_javascript(self, file_path: str, check_only: bool = False) -> bool:
        """格式化 JavaScript/TypeScript 文件"""
        path = Path(file_path)
        if not path.exists():
            self.errors.append(f"文件不存在：{file_path}")
            return False
        
        if self.js_formatter == 'prettier':
            return self._format_with_prettier(path, check_only)
        else:
            self.errors.append(f"未知的 JS 格式化器：{self.js_formatter}")
            return False
    
    def _format_with_prettier(self, path: Path, check_only: bool) -> bool:
        """使用 prettier 格式化"""
        cmd = ['npx', 'prettier', '--write' if not check_only else '--check', str(path)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.formatted_files.append(str(path))
                return True
            else:
                if check_only and result.returncode == 1:
                    self.formatted_files.append(str(path))
                    return True
                else:
                    self.errors.append(f"prettier 格式化失败：{result.stderr}")
                    return False
        except Exception as e:
            self.errors.append(f"prettier 错误：{str(e)}")
            return False
    
    def format_directory(self, dir_path: str, extensions: Optional[List[str]] = None) -> dict:
        """
        格式化整个目录
        
        Args:
            dir_path: 目录路径
            extensions: 文件扩展名列表
            
        Returns:
            dict: 统计信息
        """
        path = Path(dir_path)
        if not path.is_dir():
            return {'success': False, 'error': '不是目录'}
        
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.jsx', '.tsx']
        
        stats = {
            'total': 0,
            'formatted': 0,
            'errors': 0,
            'files': []
        }
        
        for ext in extensions:
            for file in path.rglob(f'*{ext}'):
                # 跳过虚拟环境和 node_modules
                if 'venv' in str(file) or 'node_modules' in str(file):
                    continue
                
                stats['total'] += 1
                
                if ext == '.py':
                    success = self.format_python(str(file))
                else:
                    success = self.format_javascript(str(file))
                
                if success:
                    stats['formatted'] += 1
                    stats['files'].append(str(file))
                else:
                    stats['errors'] += 1
        
        return stats
    
    def get_report(self) -> str:
        """生成格式化报告"""
        report = []
        report.append("╔════════════════════════════════════════════════════════╗")
        report.append("║           📝 代码格式化报告                            ║")
        report.append("╠════════════════════════════════════════════════════════╣")
        report.append(f"║  时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                    ║")
        report.append(f"║  格式化器：{self.python_formatter} (Python), {self.js_formatter} (JS)            ║")
        report.append("╠════════════════════════════════════════════════════════╣")
        
        if self.formatted_files:
            report.append(f"║  成功：{len(self.formatted_files)} 个文件                              ║")
            report.append("║                                                        ║")
            report.append("║  文件列表：")
            for file in self.formatted_files[:10]:  # 只显示前 10 个
                filename = Path(file).name
                report.append(f"║    ✓ {filename:<50} ║")
            if len(self.formatted_files) > 10:
                report.append(f"║    ... 还有 {len(self.formatted_files) - 10} 个文件                         ║")
        else:
            report.append("║  没有需要格式化的文件                                ║")
        
        if self.errors:
            report.append("╠════════════════════════════════════════════════════════╣")
            report.append(f"║  错误：{len(self.errors)} 个                                    ║")
            for error in self.errors[:5]:  # 只显示前 5 个错误
                error_msg = error[:50]
                report.append(f"║    ✗ {error_msg:<50} ║")
        
        report.append("╚════════════════════════════════════════════════════════╝")
        
        return '\n'.join(report)


# 快捷函数
def format_code(paths: List[str], recursive: bool = True) -> CodeFormatter:
    """
    快速格式化代码
    
    Args:
        paths: 文件或目录路径列表
        recursive: 是否递归处理目录
        
    Returns:
        CodeFormatter 实例
    """
    formatter = CodeFormatter()
    
    for path_str in paths:
        path = Path(path_str)
        if path.is_file():
            if path.suffix == '.py':
                formatter.format_python(str(path))
            elif path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                formatter.format_javascript(str(path))
        elif path.is_dir() and recursive:
            formatter.format_directory(str(path))
    
    return formatter


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python formatter.py <文件或目录> [更多文件...]")
        print("示例：python formatter.py src/ demo/")
        sys.exit(1)
    
    formatter = format_code(sys.argv[1:])
    print(formatter.get_report())
