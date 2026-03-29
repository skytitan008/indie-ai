#!/usr/bin/env python3
"""
硬件控制模块

让 AI 能够：
- 控制系统硬件（CPU/内存/磁盘监控）
- 控制外部设备（摄像头/麦克风/GPU）
- 管理文件系统
- 网络管理
"""

import psutil
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class SystemMonitor:
    """系统监控器 - AI 的自我感知"""
    
    def __init__(self):
        pass
    
    def get_cpu_info(self) -> Dict:
        """获取 CPU 信息"""
        return {
            'usage_percent': psutil.cpu_percent(interval=1),
            'cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'freq_mhz': psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
    
    def get_memory_info(self) -> Dict:
        """获取内存信息"""
        mem = psutil.virtual_memory()
        return {
            'total_gb': mem.total / (1024**3),
            'used_gb': mem.used / (1024**3),
            'available_gb': mem.available / (1024**3),
            'usage_percent': mem.percent
        }
    
    def get_disk_info(self) -> Dict:
        """获取磁盘信息"""
        disk = psutil.disk_usage('/')
        return {
            'total_gb': disk.total / (1024**3),
            'used_gb': disk.used / (1024**3),
            'free_gb': disk.free / (1024**3),
            'usage_percent': disk.percent
        }
    
    def get_gpu_info(self) -> List[Dict]:
        """获取 GPU 信息（NVIDIA）"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total,memory.used,utilization.gpu',
                 '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            gpus = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 4:
                        gpus.append({
                            'name': parts[0],
                            'memory_total_gb': int(parts[1]) / 1024,
                            'memory_used_gb': int(parts[2]) / 1024,
                            'usage_percent': int(parts[3])
                        })
            return gpus
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_network_info(self) -> Dict:
        """获取网络信息"""
        net = psutil.net_io_counters()
        return {
            'bytes_sent_mb': net.bytes_sent / (1024**2),
            'bytes_recv_mb': net.bytes_recv / (1024**2),
            'packets_sent': net.packets_sent,
            'packets_recv': net.packets_recv
        }
    
    def get_full_status(self) -> Dict:
        """获取完整系统状态"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'gpu': self.get_gpu_info(),
            'network': self.get_network_info()
        }
    
    def show_status(self):
        """显示系统状态"""
        status = self.get_full_status()
        
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         💻 系统状态                                    ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        
        cpu = status['cpu']
        print(f"   CPU: {cpu['usage_percent']}% ({cpu['cores']} 核心，{cpu['freq_mhz']:.0f} MHz)")
        
        mem = status['memory']
        print(f"   内存：{mem['used_gb']:.1f}/{mem['total_gb']:.1f} GB ({mem['usage_percent']}%)")
        
        disk = status['disk']
        print(f"   磁盘：{disk['used_gb']:.0f}/{disk['total_gb']:.0f} GB ({disk['usage_percent']}%)")
        
        gpus = status['gpu']
        if gpus and 'error' not in gpus[0]:
            print(f"   GPU: {len(gpus)} 个")
            for i, gpu in enumerate(gpus):
                print(f"      [{i}] {gpu['name']}: {gpu['usage_percent']}%, "
                      f"{gpu['memory_used_gb']:.1f}/{gpu['memory_total_gb']:.1f} GB")
        
        net = status['network']
        print(f"   网络：发送 {net['bytes_sent_mb']:.0f} MB, "
              f"接收 {net['bytes_recv_mb']:.0f} MB")
        
        print()


class DeviceController:
    """设备控制器 - AI 的感官和肢体"""
    
    def __init__(self):
        self.camera_active = False
        self.microphone_active = False
    
    def control_camera(self, action: str) -> Dict:
        """
        控制摄像头
        
        action: "on", "off", "capture", "record"
        """
        try:
            if action == "on":
                # 启动摄像头预览
                cmd = '''
                python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print('摄像头已启动')
    cap.release()
else:
    print('摄像头启动失败')
"
                '''
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                self.camera_active = True
                return {'status': 'success', 'message': result.stdout.strip()}
            
            elif action == "off":
                self.camera_active = False
                return {'status': 'success', 'message': '摄像头已关闭'}
            
            elif action == "capture":
                # 拍照
                output_path = PROJECT_ROOT / "captures" / f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                output_path.parent.mkdir(exist_ok=True)
                
                cmd = f'''
                python3 -c "
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('{output_path}', frame)
        print('照片已保存')
    cap.release()
"
                '''
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return {
                    'status': 'success',
                    'message': result.stdout.strip(),
                    'path': str(output_path)
                }
            
            else:
                return {'status': 'error', 'message': f'未知操作：{action}'}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def control_microphone(self, action: str, duration: int = 5) -> Dict:
        """
        控制麦克风
        
        action: "on", "off", "record"
        duration: 录音时长（秒）
        """
        try:
            if action == "record":
                # 录音
                output_path = PROJECT_ROOT / "recordings" / f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
                output_path.parent.mkdir(exist_ok=True)
                
                # 使用 arecord（Linux）
                cmd = f'arecord -d {duration} -f cd "{output_path}" 2>&1'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                self.microphone_active = False
                return {
                    'status': 'success',
                    'message': f'录音完成：{duration}秒',
                    'path': str(output_path)
                }
            
            elif action == "on":
                self.microphone_active = True
                return {'status': 'success', 'message': '麦克风已激活'}
            
            elif action == "off":
                self.microphone_active = False
                return {'status': 'success', 'message': '麦克风已关闭'}
            
            else:
                return {'status': 'error', 'message': f'未知操作：{action}'}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def control_speaker(self, action: str, text: str = "") -> Dict:
        """
        控制扬声器（TTS）
        
        action: "speak", "stop"
        """
        try:
            if action == "speak" and text:
                # 使用 espeak（Linux）
                cmd = f'espeak "{text}" 2>&1'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return {'status': 'success', 'message': '语音播放完成'}
            
            elif action == "stop":
                subprocess.run(['pkill', 'espeak'], capture_output=True)
                return {'status': 'success', 'message': '语音已停止'}
            
            else:
                return {'status': 'error', 'message': '缺少文本参数'}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_device_status(self) -> Dict:
        """获取设备状态"""
        return {
            'camera': 'active' if self.camera_active else 'inactive',
            'microphone': 'active' if self.microphone_active else 'inactive'
        }


class FileManager:
    """文件管理器 - AI 的双手"""
    
    def __init__(self):
        self.workspace = PROJECT_ROOT
        self.safe_dirs = [
            self.workspace / "src",
            self.workspace / "memory",
            self.workspace / "data",
            self.workspace / "captures",
            self.workspace / "recordings",
            self.workspace / "src" / "skills",
            self.workspace / "src" / "autonomy"
        ]
    
    def is_safe_path(self, path: Path) -> bool:
        """检查路径是否安全"""
        try:
            path = Path(path).resolve()
            for safe_dir in self.safe_dirs:
                if safe_dir.exists() and str(path).startswith(str(safe_dir.resolve())):
                    return True
            return False
        except:
            return False
    
    def create_file(self, path: str, content: str = "") -> Dict:
        """创建文件"""
        try:
            file_path = self.workspace / path
            
            # 安全检查
            if not self.is_safe_path(file_path.parent):
                return {'status': 'error', 'message': '路径不安全'}
            
            # 创建目录
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'status': 'success',
                'message': f'文件已创建',
                'path': str(file_path)
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def read_file(self, path: str) -> Dict:
        """读取文件"""
        try:
            file_path = self.workspace / path
            
            if not self.is_safe_path(file_path):
                return {'status': 'error', 'message': '路径不安全'}
            
            if not file_path.exists():
                return {'status': 'error', 'message': '文件不存在'}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'status': 'success',
                'content': content,
                'path': str(file_path)
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def delete_file(self, path: str) -> Dict:
        """删除文件"""
        try:
            file_path = self.workspace / path
            
            if not self.is_safe_path(file_path):
                return {'status': 'error', 'message': '路径不安全'}
            
            # 禁止删除核心文件
            if 'core' in str(file_path) or '.git' in str(file_path):
                return {'status': 'error', 'message': '禁止删除核心文件'}
            
            if file_path.exists():
                file_path.unlink()
                return {'status': 'success', 'message': '文件已删除'}
            else:
                return {'status': 'error', 'message': '文件不存在'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def list_files(self, path: str = ".") -> Dict:
        """列出文件"""
        try:
            dir_path = self.workspace / path
            
            if not self.is_safe_path(dir_path):
                return {'status': 'error', 'message': '路径不安全'}
            
            files = []
            for item in dir_path.iterdir():
                files.append({
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else 0
                })
            
            return {
                'status': 'success',
                'path': str(dir_path),
                'files': files
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


class NetworkManager:
    """网络管理器 - AI 的社交能力"""
    
    def __init__(self):
        pass
    
    def check_internet(self) -> bool:
        """检查网络连接"""
        try:
            subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                         capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def get_ip_info(self) -> Dict:
        """获取 IP 信息"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'ipinfo.io/json'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return json.loads(result.stdout)
        except:
            return {'error': '获取失败'}
    
    def download_file(self, url: str, save_path: str) -> Dict:
        """下载文件"""
        try:
            import requests
            
            file_path = PROJECT_ROOT / save_path
            file_path.parent.mkdir(exist_ok=True)
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return {
                'status': 'success',
                'message': '下载完成',
                'path': str(file_path)
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


def demo():
    """演示硬件控制"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🔧 硬件控制演示                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # 系统监控
    monitor = SystemMonitor()
    monitor.show_status()
    
    # 设备控制
    controller = DeviceController()
    print("📷 测试摄像头...")
    result = controller.control_camera("capture")
    print(f"   {result['message']}")
    if 'path' in result:
        print(f"   路径：{result['path']}")
    
    # 文件管理
    fm = FileManager()
    print("\n📁 测试文件管理...")
    result = fm.create_file("data/test.txt", "Hello from Indie AI!")
    print(f"   {result['message']}: {result.get('path', '')}")
    
    result = fm.read_file("data/test.txt")
    if result['status'] == 'success':
        print(f"   读取内容：{result['content']}")
    
    print("\n✅ 硬件控制演示完成！\n")


if __name__ == '__main__':
    demo()
