#!/usr/bin/env python3
"""
Web 可视化服务器

启动简单的 HTTP 服务器来展示学习曲线
"""

import http.server
import socketserver
import os
from pathlib import Path
import sys

PORT = 8000

def main():
    # 切换到 web 目录
    web_dir = Path(__file__).parent / "web"
    
    if not web_dir.exists():
        print(f"❌ Web 目录不存在：{web_dir}")
        sys.exit(1)
    
    os.chdir(web_dir)
    
    # 创建 HTTP 服务器
    handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"╔════════════════════════════════════════════════════════╗")
        print(f"║     🌐 Web 可视化服务器已启动                         ║")
        print(f"╠════════════════════════════════════════════════════════╣")
        print(f"║  访问地址：http://localhost:{PORT}                    ║")
        print(f"║  文件目录：{web_dir}                                  ║")
        print(f"║                                                        ║")
        print(f"║  按 Ctrl+C 停止服务器                                  ║")
        print(f"╚════════════════════════════════════════════════════════╝")
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n服务器已停止")

if __name__ == "__main__":
    main()
