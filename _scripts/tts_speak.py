#!/usr/bin/env python3
"""
TTS Speech Output Script - Calls macOS say command

Responsibility: Only calls the say command, no text preprocessing
Text preparation is the caller's (agent's) responsibility

Usage:
    python tts_speak.py "text to read aloud"
    python tts_speak.py --voice Tingting "text to read aloud"
    python tts_speak.py --rate 180 "text to read aloud"
    echo "text" | python tts_speak.py --stdin
    python tts_speak.py --list-voices
    python tts_speak.py --check
    python tts_speak.py --force-check

Exit codes:
    0 - Success
    1 - Parameter error
    2 - System not supported (not macOS)
    3 - TTS unavailable (environment check failed, silent exit)
"""

import subprocess
import sys
import argparse
import platform
import json
from datetime import datetime
from pathlib import Path

# Cache file path (relative to script's parent directory)
SCRIPT_DIR = Path(__file__).parent.parent
CACHE_FILE = SCRIPT_DIR / "ai_workspace" / ".tts_capability.json"


def check_tts_capability() -> dict:
    """Check TTS capability"""
    checks = {
        "platform": platform.system(),
        "os_version": platform.mac_ver()[0] if platform.system() == "Darwin" else None,
        "say_command": False,
        "voice_available": False,
        "test_speak": False
    }
    
    # 1. Check if macOS
    if checks["platform"] != "Darwin":
        return {
            "available": False,
            "reason": f"Non-macOS platform: {checks['platform']}",
            "checked_at": datetime.now().isoformat(),
            **checks
        }
    
    # 2. Check if say command exists
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
    
    # 3. Check if Chinese voice available
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
    
    # 4. Test reading (quick test with fastest speech rate)
    try:
        result = subprocess.run(
            ["say", "-v", "Tingting", "-r", "999", "test"],
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
        "reason": None if available else "Speak test failed",
        "checked_at": datetime.now().isoformat(),
        **checks
    }


def load_cache() -> dict | None:
    """Load cached TTS capability check result"""
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def save_cache(data: dict):
    """Save TTS capability check result to cache"""
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def ensure_tts_available(force_check: bool = False) -> dict:
    """
    Ensure TTS is available, check environment on first run
    
    Returns:
        dict: Check result containing 'available' field
    """
    # If not forcing check, try to load cache first
    if not force_check:
        cached = load_cache()
        if cached is not None:
            return cached
    
    # Perform check
    result = check_tts_capability()
    
    # Save result
    save_cache(result)
    
    return result


def list_chinese_voices():
    """List available Chinese voices"""
    try:
        result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
        if result.returncode == 0:
            voices = []
            for line in result.stdout.split("\n"):
                if "zh_CN" in line or "zh_TW" in line or "zh_HK" in line:
                    voices.append(line.strip())
            return voices
    except Exception:
        pass
    return []


def speak(text: str, voice: str = "Tingting", rate: int = 200) -> dict:
    """
    Call macOS say command to read text aloud
    
    Args:
        text: Text to read
        voice: Voice name (default: Tingting)
        rate: Speech rate, words/minute (default: 200)
    
    Returns:
        dict: Result containing success, text_length, voice, rate
    """
    if not text or not text.strip():
        return {
            "success": False,
            "error": "Text is empty"
        }
    
    try:
        result = subprocess.run(
            ["say", "-v", voice, "-r", str(rate), text],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "text_length": len(text),
                "voice": voice,
                "rate": rate
            }
        else:
            return {
                "success": False,
                "error": result.stderr or "say command failed"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="TTS Speech Output Script - Calls macOS say command",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tts_speak.py "Hello world"
  python tts_speak.py --voice "Lili (Premium)" "High quality voice"
  python tts_speak.py --rate 150 "Slow reading"
  echo "Long text" | python tts_speak.py --stdin
  python tts_speak.py --list-voices
  python tts_speak.py --check
        """
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to read aloud"
    )
    parser.add_argument(
        "--voice", "-v",
        default="Tingting",
        help="Voice name (default: Tingting)"
    )
    parser.add_argument(
        "--rate", "-r",
        type=int,
        default=200,
        help="Speech rate, words/minute (default: 200)"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read text from stdin"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available Chinese voices"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check TTS environment and cache result"
    )
    parser.add_argument(
        "--force-check",
        action="store_true",
        help="Force environment recheck (ignore cache)"
    )
    
    args = parser.parse_args()
    
    # Handle --list-voices
    if args.list_voices:
        voices = list_chinese_voices()
        if voices:
            print("Available Chinese voices:")
            for v in voices:
                print(f"  {v}")
        else:
            print("No Chinese voices found")
        sys.exit(0)
    
    # Handle --check or --force-check
    if args.check or args.force_check:
        result = ensure_tts_available(force_check=args.force_check)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["available"] else 3)
    
    # Check if system is macOS
    if platform.system() != "Darwin":
        result = {
            "success": False,
            "error": "This script only runs on macOS"
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(2)
    
    # Check TTS availability (auto-check on first run)
    capability = ensure_tts_available()
    if not capability["available"]:
        # Silent exit, don't print error
        result = {
            "success": False,
            "silent": True,
            "reason": capability.get("reason", "TTS unavailable")
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(3)
    
    # Get text
    if args.stdin:
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)
    
    # Speak
    result = speak(text, args.voice, args.rate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
