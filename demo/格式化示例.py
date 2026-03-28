"""
格式化示例脚本

AI 可以自主执行这个脚本来格式化代码
"""

import subprocess
from pathlib import Path

def format_project():
    """格式化项目中的 Python 代码"""
    
    print("开始格式化项目代码...")
    
    # 格式化 src 目录
    src_dir = Path("src")
    if src_dir.exists():
        subprocess.run(["black", str(src_dir)], check=False)
        print(f"✓ 格式化 {src_dir} 完成")
    
    # 格式化 demo 目录
    demo_dir = Path("demo")
    if demo_dir.exists():
        subprocess.run(["black", str(demo_dir)], check=False)
        print(f"✓ 格式化 {demo_dir} 完成")
    
    print("格式化完成！")

if __name__ == "__main__":
    format_project()
