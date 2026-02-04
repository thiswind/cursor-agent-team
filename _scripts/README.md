# _scripts - Framework-Level Scripts

Hard constraint validation scripts for deterministic LLM output validation.

## Design Philosophy

```
┌─────────────────────────────────────────────────┐
│                    LLM Layer                    │
│   (Soft constraints: prompt rules, may be       │
│    violated due to randomness)                  │
└────────────────────┬────────────────────────────┘
                     │ calls
                     ▼
┌─────────────────────────────────────────────────┐
│                  Script Layer                   │
│   (Hard constraints: Python scripts,            │
│    deterministic execution)                     │
│   - Validate output format                      │
│   - Check required fields                       │
│   - Return errors for LLM to retry              │
└─────────────────────────────────────────────────┘
```

- **Soft Constraints (LLM Layer)**: Guide LLM behavior through prompt rules
- **Hard Constraints (Script Layer)**: Validate output through deterministic scripts

## Script Index

| Script | Purpose | Key Flags |
|--------|---------|-----------|
| `validate_topic_tree.py` | Topic tree validation and update | `update --stdin` |
| `cleanup_ai_workspace.py` | Safe workspace file deletion | `--dry-run`, `--older-than`, `--pattern` |
| `tts_speak.py` | Text-to-speech (macOS only) | `--check`, `--list-voices` |
| `preflight_check.py` | Session initialization check | (no flags) |
| `persona_output.py` | Load persona for output | `--check` |
| `role_identity/*.py` | Role declaration | (no flags) |

## Usage Examples

### Topic Tree Update (One-Step)

```bash
echo '{"action": "add_topic", "topic_id": "A", "topic_name": "New Topic"}' | \
  python cursor-agent-team/_scripts/validate_topic_tree.py update --stdin
```

### Workspace Cleanup

```bash
# Preview files older than 7 days
python cursor-agent-team/_scripts/cleanup_ai_workspace.py --older-than 7 --dry-run

# Delete by pattern
python cursor-agent-team/_scripts/cleanup_ai_workspace.py --pattern "*.bak"
```

### TTS Check

```bash
# Check if TTS is available
python cursor-agent-team/_scripts/tts_speak.py --check

# List available Chinese voices
python cursor-agent-team/_scripts/tts_speak.py --list-voices
```

### Session Initialization

```bash
python cursor-agent-team/_scripts/preflight_check.py
```

## Detailed Documentation

For detailed parameters and options, run `--help` on any script:

```bash
python cursor-agent-team/_scripts/validate_topic_tree.py --help
python cursor-agent-team/_scripts/cleanup_ai_workspace.py --help
python cursor-agent-team/_scripts/tts_speak.py --help
```

## Version History

- **v2.0.0** (2026-02-03): Major refactoring - simplified documentation, removed deprecated content
- **v1.5.0** (2026-02-01): Translated to English
- **v1.4.0** (2026-02-01): Added cleanup_ai_workspace.py
- **v1.3.0** (2026-02-01): Added TTS environment check
- **v1.2.0** (2026-02-01): Added tts_speak.py
- **v1.0.0** (2026-01-31): Initial version
