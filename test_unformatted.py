
# 未格式化的代码
import os,sys
from pathlib import Path

def hello(name ):
    if name:
        print( f"Hello, {name}!" )
    else:
        print( "Hello, World!" )

class Test:
    def __init__(self):
        self.value=42
