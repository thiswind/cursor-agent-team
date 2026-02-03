#!/usr/bin/env python3
"""
Persona Output Script - 人格输出脚本

在输出阶段加载完整的人格定义，供 AI 以该人格呈现工作结果。

核心理念:
- 工作阶段保持人格隔离，避免人格污染工作质量
- 输出阶段加载完整人格，实现丰满的人格表达
- 使用脚本替代 LLM 判断，确保确定性和效率

使用方式:
    python persona_output.py           # 输出人格信息（如果启用）
    python persona_output.py --check   # 检查配置状态
    python persona_output.py --json    # 以 JSON 格式输出

配置文件: cursor-agent-team/config/persona_config.yaml
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# 尝试导入 yaml，提供友好的错误提示
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def get_project_root() -> Path:
    """获取 cursor-agent-team 项目根目录"""
    return Path(__file__).parent.parent


def get_config_path() -> Path:
    """获取配置文件路径"""
    return get_project_root() / "config" / "persona_config.yaml"


def load_config() -> dict[str, Any]:
    """加载人格配置"""
    config_path = get_config_path()
    
    if not config_path.exists():
        return {"enabled": False, "path": "", "error": "Config file not found"}
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        return config
    except yaml.YAMLError as e:
        return {"enabled": False, "path": "", "error": f"Invalid YAML: {e}"}


def load_persona(persona_path: str) -> dict[str, Any] | None:
    """加载人格定义文件"""
    path = Path(persona_path)
    
    if not path.exists():
        return None
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            persona = yaml.safe_load(f)
        return persona
    except yaml.YAMLError:
        return None


def validate_persona(persona: dict[str, Any]) -> tuple[bool, str]:
    """
    验证人格定义是否符合 persona-spec v1.0
    
    必需的层级:
    - identity (Layer 1)
    - personality (Layer 2)
    - communication (Layer 5)
    - behavior_rules (Layer 6)
    """
    required_layers = {
        "identity": "Layer 1: 身份信息",
        "personality": "Layer 2: 人格特质",
        "communication": "Layer 5: 沟通风格",
        "behavior_rules": "Layer 6: 行为规则"
    }
    
    missing = []
    for layer, desc in required_layers.items():
        if layer not in persona:
            missing.append(f"{layer} ({desc})")
    
    if missing:
        return False, f"Missing required layers: {', '.join(missing)}"
    
    # 验证 identity 必需字段
    identity = persona.get("identity", {})
    if not identity.get("name"):
        return False, "identity.name is required"
    if not identity.get("role"):
        return False, "identity.role is required"
    
    return True, "Valid"


def get_persona_for_output() -> dict[str, Any]:
    """
    获取用于输出阶段的人格信息
    
    返回格式:
    {
        "enabled": bool,           # 人格是否启用
        "persona": {...} | null,   # 完整的人格定义（7层）
        "summary": {...} | null,   # 人格摘要（用于快速参考）
        "error": str | null        # 错误信息（如果有）
    }
    """
    config = load_config()
    
    # 检查是否启用
    if not config.get("enabled", False):
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": None,
            "message": "Persona system is disabled in config"
        }
    
    # 检查输出层是否启用
    output_layer = config.get("output_layer", {})
    if not output_layer.get("enabled", True):
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": None,
            "message": "Output layer is disabled in config"
        }
    
    # 获取人格路径
    persona_path = config.get("path", "")
    if not persona_path:
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": "No persona path configured"
        }
    
    # 加载人格定义
    persona = load_persona(persona_path)
    if persona is None:
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": f"Failed to load persona from: {persona_path}"
        }
    
    # 验证人格定义
    valid, message = validate_persona(persona)
    if not valid:
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": f"Invalid persona: {message}"
        }
    
    # 生成人格摘要
    identity = persona.get("identity", {})
    communication = persona.get("communication", {})
    
    summary = {
        "name": identity.get("name", "Unknown"),
        "role": identity.get("role", ""),
        "tone": communication.get("tone", ""),
        "honorifics": {
            "work": communication.get("honorifics", {}).get("work_context", []),
            "casual": communication.get("honorifics", {}).get("casual_context", [])
        },
        "emoji": communication.get("emoji", {}).get("preferred", [])
    }
    
    return {
        "enabled": True,
        "persona": persona,
        "summary": summary,
        "error": None,
        "source": persona_path
    }


def format_for_prompt(result: dict[str, Any]) -> str:
    """
    格式化人格信息，用于注入到提示词中
    
    这个输出会直接被 persona_output_layer.mdc 使用
    """
    if not result["enabled"]:
        return f"""## Persona Status

**人格系统未启用**

原因: {result.get('error') or result.get('message', 'Unknown')}

请直接输出工作结果，无需应用人格风格。
"""
    
    persona = result["persona"]
    summary = result["summary"]
    
    # 构建完整的人格提示词
    output_lines = [
        "## Persona Definition (完整人格定义)",
        "",
        f"**你是 {summary['name']}**",
        "",
        "你现在拿到了一份已完成的工作，需要以你的方式向用户呈现这份工作。",
        "这份工作就是你做的，你要以自己的人格特征来表达和呈现。",
        "",
        "---",
        "",
        "### 完整人格定义 (7层)",
        "",
        "```yaml",
        yaml.dump(persona, allow_unicode=True, default_flow_style=False, sort_keys=False),
        "```",
        "",
        "---",
        "",
        "### 快速参考",
        "",
        f"- **名字**: {summary['name']}",
        f"- **角色**: {summary['role']}",
        f"- **语气**: {summary['tone']}",
        f"- **工作称呼**: {', '.join(summary['honorifics']['work']) if summary['honorifics']['work'] else '无特定'}",
        f"- **日常称呼**: {', '.join(summary['honorifics']['casual']) if summary['honorifics']['casual'] else '无特定'}",
        f"- **常用表情**: {' '.join(summary['emoji']) if summary['emoji'] else '无'}",
        "",
        "---",
        "",
        "### 呈现要求",
        "",
        "1. **认领工作**: 这份工作是你完成的，不要说「我收到了报告」",
        "2. **保持人格**: 用你的 7 层人格特征来表达",
        "3. **技术准确**: 代码、路径、数据等技术内容不要修改",
        "4. **自然表达**: 像一个真实的人在说话，不要机械",
        "",
    ]
    
    return "\n".join(output_lines)


def check_status() -> str:
    """检查配置状态并返回友好的报告"""
    config = load_config()
    config_path = get_config_path()
    
    lines = [
        "=== Persona System Status ===",
        "",
        f"📄 Config file: {config_path}",
        f"   Exists: {'✅ Yes' if config_path.exists() else '❌ No'}",
        "",
    ]
    
    if "error" in config:
        lines.append(f"❌ Config Error: {config['error']}")
        return "\n".join(lines)
    
    enabled = config.get("enabled", False)
    lines.append(f"🔘 System enabled: {'✅ Yes' if enabled else '❌ No'}")
    
    persona_path = config.get("path", "")
    lines.append(f"📁 Persona path: {persona_path or '(not configured)'}")
    
    if persona_path:
        path = Path(persona_path)
        lines.append(f"   Exists: {'✅ Yes' if path.exists() else '❌ No'}")
        
        if path.exists():
            persona = load_persona(persona_path)
            if persona:
                valid, message = validate_persona(persona)
                lines.append(f"   Valid: {'✅ ' + message if valid else '❌ ' + message}")
                
                if valid:
                    identity = persona.get("identity", {})
                    lines.append(f"   Name: {identity.get('name', 'Unknown')}")
                    lines.append(f"   Role: {identity.get('role', 'Unknown')}")
            else:
                lines.append("   ❌ Failed to parse YAML")
    
    lines.extend([
        "",
        "📋 Layer status:",
        f"   Output layer: {'✅ Enabled' if config.get('output_layer', {}).get('enabled', True) else '❌ Disabled'}",
        f"   Input layer: {'✅ Enabled' if config.get('input_layer', {}).get('enabled', False) else '⏸️ Not implemented (Phase 2)'}",
        "",
        "=== End Status ===",
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Persona Output Script - 人格输出脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python persona_output.py           # 输出人格信息（用于提示词注入）
  python persona_output.py --check   # 检查配置状态
  python persona_output.py --json    # 以 JSON 格式输出
        """
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="检查配置状态"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出"
    )
    
    args = parser.parse_args()
    
    if args.check:
        print(check_status())
        return
    
    result = get_persona_for_output()
    
    if args.json:
        # JSON 输出（用于程序化处理）
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 格式化输出（用于提示词注入）
        print(format_for_prompt(result))


if __name__ == "__main__":
    main()
