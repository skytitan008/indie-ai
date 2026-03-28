"""
运行测试示例脚本

AI 可以自主执行这个脚本来运行测试
"""

import subprocess
from pathlib import Path

def run_tests():
    """运行项目测试"""
    
    print("开始运行测试...")
    
    # 运行 tests 目录
    test_dir = Path("tests")
    if test_dir.exists():
        result = subprocess.run(
            ["pytest", str(test_dir), "-v"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode == 0:
            print("✓ 所有测试通过！")
        else:
            print("✗ 有测试失败")
            print(result.stderr)
    else:
        print("测试目录不存在")
    
    print("测试完成！")

if __name__ == "__main__":
    run_tests()
