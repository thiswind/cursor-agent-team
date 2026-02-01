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
    python tts_speak.py --check
    python tts_speak.py --force-check

退出码:
    0 - 成功
    1 - 参数错误
    2 - 系统不支持（非 macOS）
    3 - TTS 不可用（环境检查失败，静默退出）
"""

import subprocess
import sys
import argparse
import platform
import json
from datetime import datetime
from pathlib import Path

# 缓存文件路径（相对于脚本所在目录的父目录）
SCRIPT_DIR = Path(__file__).parent.parent
CACHE_FILE = SCRIPT_DIR / "ai_workspace" / ".tts_capability.json"


def check_tts_capability() -> dict:
    """检查 TTS 能力"""
    checks = {
        "platform": platform.system(),
        "os_version": platform.mac_ver()[0] if platform.system() == "Darwin" else None,
        "say_command": False,
        "voice_available": False,
        "test_speak": False
    }
    
    # 1. 检查是否是 macOS
    if checks["platform"] != "Darwin":
        return {
            "available": False,
            "reason": f"Non-macOS platform: {checks['platform']}",
            "checked_at": datetime.now().isoformat(),
            **checks
        }
    
    # 2. 检查 say 命令是否存在
    try:
        result = subprocess.run(["which", "say"], capture_output=True)
        checks["say_command"] = result.returncode == 0
    except Exception:
        pass
    
    if not checks["say_command"]:
        return {
            "available": False,
            "reason": "say command not found",
            "checked_at": datetime.now().isoformat(),
            **checks
        }
    
    # 3. 检查是否有中文语音
    try:
        result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
        checks["voice_available"] = "zh_CN" in result.stdout
    except Exception:
        pass
    
    if not checks["voice_available"]:
        return {
            "available": False,
            "reason": "No Chinese voice available",
            "checked_at": datetime.now().isoformat(),
            **checks
        }
    
    # 4. 测试朗读（快速测试，用最快语速）
    try:
        result = subprocess.run(
            ["say", "-v", "Tingting", "-r", "999", "测试"],
            capture_output=True,
            timeout=5
        )
        checks["test_speak"] = result.returncode == 0
    except Exception:
        pass
    
    available = all([
        checks["say_command"],
        checks["voice_available"],
        checks["test_speak"]
    ])
    
    return {
        "available": available,
        "reason": "All checks passed" if available else "Test speak failed",
        "checked_at": datetime.now().isoformat(),
        **checks
    }


def get_tts_capability(force_check: bool = False) -> dict:
    """获取 TTS 能力（优先读取缓存）"""
    
    # 如果不强制检查，尝试读取缓存
    if not force_check and CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    
    # 执行检查
    result = check_tts_capability()
    
    # 写入缓存
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    
    return result


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
  python tts_speak.py --check
  python tts_speak.py --force-check
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
    parser.add_argument("--check", action="store_true", 
                        help="检查 TTS 环境并缓存结果")
    parser.add_argument("--force-check", action="store_true", 
                        help="强制重新检查（忽略缓存）")
    
    args = parser.parse_args()
    
    # 处理 --check 或 --force-check 参数
    if args.check or args.force_check:
        result = get_tts_capability(force_check=args.force_check)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["available"] else 1
    
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
    
    # 正常调用前先检查能力
    capability = get_tts_capability()
    if not capability.get("available", False):
        # 静默退出，不报错（但返回特殊退出码）
        print(json.dumps({
            "success": False, 
            "error": "TTS not available on this platform",
            "silent": True
        }, ensure_ascii=False))
        return 3  # 特殊退出码表示环境不支持
    
    # 执行朗读
    result = speak(text, args.voice, args.rate)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
