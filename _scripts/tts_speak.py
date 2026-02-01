#!/usr/bin/env python3
"""
TTS 语音输出脚本 - 调用 macOS say 命令

职责：只负责调用 say 命令，不做任何文本预处理
文本整理由调用者（智能体）负责

用法:
    python tts_speak.py "要朗读的文本"
    python tts_speak.py --voice Tingting "要朗读的文本"
    python tts_speak.py --rate 180 "要朗读的文本"
    echo "文本" | python tts_speak.py --stdin
    python tts_speak.py --list-voices

退出码:
    0 - 成功
    1 - 参数错误
    2 - 系统不支持（非 macOS）
"""

import subprocess
import sys
import argparse
import platform
import json


def speak(text: str, voice: str = "Tingting", rate: int = 200) -> dict:
    """调用 macOS say 命令朗读文本"""
    
    if platform.system() != "Darwin":
        return {"success": False, "error": "此功能仅支持 macOS"}
    
    if not text or not text.strip():
        return {"success": False, "error": "文本为空"}
    
    cmd = ["say", "-v", voice, "-r", str(rate), text.strip()]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return {"success": True, "text_length": len(text), "voice": voice, "rate": rate}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": f"say 命令执行失败: {e.stderr}"}
    except FileNotFoundError:
        return {"success": False, "error": "say 命令不存在"}


def list_chinese_voices():
    """列出可用的中文语音"""
    if platform.system() != "Darwin":
        print(json.dumps({"success": False, "error": "此功能仅支持 macOS"}))
        return 1
    
    try:
        result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
        voices = []
        for line in result.stdout.split('\n'):
            if 'zh_' in line:
                voices.append(line.strip())
        
        print(json.dumps({
            "success": True,
            "voices": voices,
            "count": len(voices)
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="TTS 语音输出 - 调用 macOS say 命令",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python tts_speak.py "你好，这是一个测试"
  python tts_speak.py --voice "Lili (Premium)" "高质量语音"
  python tts_speak.py --rate 150 "慢速朗读"
  echo "长文本内容" | python tts_speak.py --stdin
  python tts_speak.py --list-voices
        """
    )
    parser.add_argument("text", nargs="?", help="要朗读的文本")
    parser.add_argument("--voice", "-v", default="Tingting", 
                        help="语音名称（默认 Tingting，可用 --list-voices 查看）")
    parser.add_argument("--rate", "-r", type=int, default=200, 
                        help="语速，词/分钟（默认 200）")
    parser.add_argument("--stdin", action="store_true", 
                        help="从标准输入读取文本")
    parser.add_argument("--list-voices", action="store_true", 
                        help="列出可用的中文语音")
    
    args = parser.parse_args()
    
    # 列出语音
    if args.list_voices:
        return list_chinese_voices()
    
    # 获取文本
    if args.stdin:
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return 1
    
    # 执行朗读
    result = speak(text, args.voice, args.rate)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
