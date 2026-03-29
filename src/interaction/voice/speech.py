#!/usr/bin/env python3
"""
语音交互模块

让 AI 能听会说：
- 语音识别（STT）
- 语音合成（TTS）
- 语音命令
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class SpeechRecognizer:
    """语音识别 - 把语音转文字"""
    
    def __init__(self):
        self.recording_dir = PROJECT_ROOT / "recordings"
        self.recording_dir.mkdir(exist_ok=True)
    
    def record(self, duration: int = 5) -> Optional[str]:
        """录音"""
        try:
            output_path = self.recording_dir / f"rec_{datetime.now().strftime('%H%M%S')}.wav"
            
            # 使用 arecord 录音
            cmd = ['arecord', '-d', str(duration), '-f', 'cd', '-t', 'wav', str(output_path)]
            subprocess.run(cmd, capture_output=True)
            
            print(f"   ✅ 录音完成：{output_path}")
            return str(output_path)
        except Exception as e:
            print(f"   ❌ 录音失败：{e}")
            return None
    
    def recognize(self, audio_path: str) -> Optional[str]:
        """语音识别（使用 Whisper 或其他引擎）"""
        try:
            # 这里可以集成 Whisper、Google Speech API 等
            # 目前返回提示
            print("   💡 提示：安装 Whisper 可实现语音识别")
            print("      pip install openai-whisper")
            return "[语音识别功能待实现]"
        except Exception as e:
            print(f"   ❌ 识别失败：{e}")
            return None
    
    def listen_and_recognize(self, duration: int = 5) -> Optional[str]:
        """录音并识别"""
        audio_path = self.record(duration)
        if audio_path:
            return self.recognize(audio_path)
        return None


class TextToSpeech:
    """语音合成 - 把文字转语音"""
    
    def __init__(self):
        self.available = self._check_engine()
    
    def _check_engine(self) -> bool:
        """检查 TTS 引擎是否可用"""
        try:
            subprocess.run(['which', 'espeak'], capture_output=True, check=True)
            return True
        except:
            try:
                subprocess.run(['which', 'say'], capture_output=True, check=True)  # macOS
                return True
            except:
                return False
    
    def speak(self, text: str, lang: str = 'zh') -> bool:
        """语音合成"""
        try:
            if not self.available:
                print(f"   🔊 [TTS] {text}")
                return True
            
            # 检测系统
            if subprocess.run(['which', 'say'], capture_output=True).returncode == 0:
                # macOS
                cmd = ['say', text]
            else:
                # Linux (espeak)
                cmd = ['espeak', '-v', 'zh', text]
            
            subprocess.run(cmd)
            return True
        except Exception as e:
            print(f"   ❌ TTS 失败：{e}")
            print(f"   🔊 [文字] {text}")
            return False
    
    def speak_async(self, text: str):
        """异步语音合成（不阻塞）"""
        import threading
        t = threading.Thread(target=self.speak, args=(text,))
        t.daemon = True
        t.start()


class VoiceCommand:
    """语音命令识别"""
    
    def __init__(self):
        self.commands = {
            '打开摄像头': 'camera_on',
            '关闭摄像头': 'camera_off',
            '拍照': 'camera_capture',
            '录音': 'record_audio',
            '显示状态': 'show_status',
            '帮助': 'help',
            '退出': 'exit',
        }
    
    def parse_command(self, text: str) -> Optional[str]:
        """解析语音命令"""
        text = text.strip()
        
        for cmd_text, cmd_id in self.commands.items():
            if cmd_text in text:
                return cmd_id
        
        return None
    
    def execute_command(self, cmd_id: str, ai) -> str:
        """执行语音命令"""
        if cmd_id == 'camera_on':
            result = ai.devices.control_camera("on")
            return "摄像头已打开" if result['status'] == 'success' else "摄像头打开失败"
        
        elif cmd_id == 'camera_off':
            result = ai.devices.control_camera("off")
            return "摄像头已关闭"
        
        elif cmd_id == 'camera_capture':
            result = ai.devices.control_camera("capture")
            return f"拍照完成：{result.get('path', '')}" if result['status'] == 'success' else "拍照失败"
        
        elif cmd_id == 'record_audio':
            result = ai.devices.control_microphone("record", 5)
            return f"录音完成" if result['status'] == 'success' else "录音失败"
        
        elif cmd_id == 'show_status':
            ai.show_status()
            return "状态已显示"
        
        elif cmd_id == 'help':
            return "可用命令：打开摄像头、关闭摄像头、拍照、录音、显示状态、退出"
        
        elif cmd_id == 'exit':
            return "再见！"
        
        return "未知命令"


class VoiceInterface:
    """语音交互界面"""
    
    def __init__(self):
        self.stt = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.command = VoiceCommand()
        print("\n╔════════════════════════════════════════════════════════╗")
        print("║         🎤 语音交互界面已启动                          ║")
        print("╚════════════════════════════════════════════════════════╝\n")
    
    def start_voice_mode(self, ai=None):
        """启动语音模式"""
        print("🎤 语音模式已启动（说 '退出' 结束）\n")
        print("可用命令：打开摄像头、关闭摄像头、拍照、录音、显示状态\n")
        
        while True:
            try:
                print("按 Enter 开始录音（5 秒）...")
                input()
                
                print("🎤 正在录音...")
                text = self.stt.listen_and_recognize(5)
                
                if not text:
                    print("小七：没听清楚，请再说一次\n")
                    continue
                
                print(f"你：{text}")
                
                # 检查是否是命令
                cmd = self.command.parse_command(text)
                if cmd:
                    if cmd == 'exit':
                        self.tts.speak("再见！")
                        break
                    
                    if ai:
                        result = self.command.execute_command(cmd, ai)
                        self.tts.speak(result)
                        print(f"小七：{result}\n")
                    continue
                
                # 普通对话
                if ai and hasattr(ai, 'chat'):
                    response = ai.chat(text)
                else:
                    response = "我听到了，但还需要学习更多。"
                
                self.tts.speak(response)
                print(f"小七：{response}\n")
                
            except KeyboardInterrupt:
                print("\n小七：再见！👋")
                break
            except Exception as e:
                print(f"小七：抱歉，{e}\n")


def demo():
    """演示"""
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║         🎤 语音系统演示                                ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    tts = TextToSpeech()
    
    print("🔊 测试语音合成:")
    tts.speak("你好，我是小七")
    tts.speak("很高兴为你服务")
    
    print("\n✅ 演示完成！\n")


if __name__ == '__main__':
    demo()
