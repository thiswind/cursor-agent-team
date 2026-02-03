#!/usr/bin/env python3
"""
Persona Output Script

Loads complete persona definition at output stage for AI to present work results with persona style.

Core principles:
- Keep persona isolated during work stage to avoid contaminating work quality
- Load complete persona at output stage for rich persona expression
- Use scripts to replace LLM judgment, ensuring determinism and efficiency

Usage:
    python persona_output.py           # Output persona info (if enabled)
    python persona_output.py --check   # Check configuration status
    python persona_output.py --json    # Output in JSON format

Config file: cursor-agent-team/config/persona_config.yaml
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Try to import yaml with friendly error message
try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def get_project_root() -> Path:
    """Get cursor-agent-team project root directory"""
    return Path(__file__).parent.parent


def get_config_path() -> Path:
    """Get configuration file path"""
    return get_project_root() / "config" / "persona_config.yaml"


def load_config() -> dict[str, Any]:
    """Load persona configuration"""
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
    """Load persona definition file"""
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
    Validate persona definition against persona-spec v1.0
    
    Required layers:
    - identity (Layer 1)
    - personality (Layer 2)
    - communication (Layer 5)
    - behavior_rules (Layer 6)
    """
    required_layers = {
        "identity": "Layer 1: Identity info",
        "personality": "Layer 2: Personality traits",
        "communication": "Layer 5: Communication style",
        "behavior_rules": "Layer 6: Behavior rules"
    }
    
    missing = []
    for layer, desc in required_layers.items():
        if layer not in persona:
            missing.append(f"{layer} ({desc})")
    
    if missing:
        return False, f"Missing required layers: {', '.join(missing)}"
    
    # Validate identity required fields
    identity = persona.get("identity", {})
    if not identity.get("name"):
        return False, "identity.name is required"
    if not identity.get("role"):
        return False, "identity.role is required"
    
    return True, "Valid"


def get_persona_for_output() -> dict[str, Any]:
    """
    Get persona info for output stage
    
    Return format:
    {
        "enabled": bool,           # Whether persona is enabled
        "persona": {...} | null,   # Complete persona definition (7 layers)
        "summary": {...} | null,   # Persona summary (for quick reference)
        "error": str | null        # Error message (if any)
    }
    """
    config = load_config()
    
    # Check if enabled
    if not config.get("enabled", False):
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": None,
            "message": "Persona system is disabled in config"
        }
    
    # Check if output layer is enabled
    output_layer = config.get("output_layer", {})
    if not output_layer.get("enabled", True):
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": None,
            "message": "Output layer is disabled in config"
        }
    
    # Get persona path
    persona_path = config.get("path", "")
    if not persona_path:
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": "No persona path configured"
        }
    
    # Load persona definition
    persona = load_persona(persona_path)
    if persona is None:
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": f"Failed to load persona from: {persona_path}"
        }
    
    # Validate persona definition
    valid, message = validate_persona(persona)
    if not valid:
        return {
            "enabled": False,
            "persona": None,
            "summary": None,
            "error": f"Invalid persona: {message}"
        }
    
    # Generate persona summary
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
    Format persona info for injection into prompts
    
    This output is used directly by persona_output_layer.mdc
    """
    if not result["enabled"]:
        return f"""## Persona Status

**Persona system not enabled**

Reason: {result.get('error') or result.get('message', 'Unknown')}

Please output work results directly without applying persona style.
"""
    
    persona = result["persona"]
    summary = result["summary"]
    
    # Build complete persona prompt
    output_lines = [
        "## Persona Definition (Complete)",
        "",
        f"**You are {summary['name']}**",
        "",
        "You have completed work that needs to be presented to the user in your own way.",
        "This work is yours, express and present it with your personality traits.",
        "",
        "---",
        "",
        "### Complete Persona Definition (7 layers)",
        "",
        "```yaml",
        yaml.dump(persona, allow_unicode=True, default_flow_style=False, sort_keys=False),
        "```",
        "",
        "---",
        "",
        "### Quick Reference",
        "",
        f"- **Name**: {summary['name']}",
        f"- **Role**: {summary['role']}",
        f"- **Tone**: {summary['tone']}",
        f"- **Work honorifics**: {', '.join(summary['honorifics']['work']) if summary['honorifics']['work'] else 'None specific'}",
        f"- **Casual honorifics**: {', '.join(summary['honorifics']['casual']) if summary['honorifics']['casual'] else 'None specific'}",
        f"- **Common emoji**: {' '.join(summary['emoji']) if summary['emoji'] else 'None'}",
        "",
        "---",
        "",
        "### Presentation Requirements",
        "",
        "1. **Claim the work**: This work is yours, don't say 'I received a report'",
        "2. **Maintain persona**: Express with your 7-layer personality traits",
        "3. **Technical accuracy**: Don't modify code, paths, data, or other technical content",
        "4. **Natural expression**: Speak like a real person, not mechanically",
        "",
    ]
    
    return "\n".join(output_lines)


def check_status() -> str:
    """Check configuration status and return friendly report"""
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
        description="Persona Output Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python persona_output.py           # Output persona info (for prompt injection)
  python persona_output.py --check   # Check configuration status
  python persona_output.py --json    # Output in JSON format
        """
    )
    
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check configuration status"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    
    args = parser.parse_args()
    
    if args.check:
        print(check_status())
        return
    
    result = get_persona_for_output()
    
    if args.json:
        # JSON output (for programmatic processing)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Formatted output (for prompt injection)
        print(format_for_prompt(result))


if __name__ == "__main__":
    main()
