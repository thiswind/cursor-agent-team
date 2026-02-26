---
name: "skill-tts"
description: "TTS voice output for macOS. Triggers ONLY when user explicitly requests voice output (e.g., '读给我听', 'read to me', 'say it to me'). Never triggers by default."
---

# TTS Speech Output

## Trigger Conditions

**Only invoke when user explicitly requests voice output.**

Recognize these trigger phrases:
- "read to me", "say it to me", "tell me", "read aloud", "speak it out"
- "读给我听", "念给我听", "说给我听", "念出来", "朗读一下", "语音播报"

**Do NOT trigger** for: normal text conversations, expressions like "I'll say something", "you're right".

## Script Location

```
cursor-agent-team/_scripts/tts_speak.py
```

## Usage

```bash
python cursor-agent-team/_scripts/tts_speak.py "prepared text"
echo "long text" | python cursor-agent-team/_scripts/tts_speak.py --stdin
python cursor-agent-team/_scripts/tts_speak.py --voice "Lili (Premium)" "text"
python cursor-agent-team/_scripts/tts_speak.py --rate 180 "slow reading"
python cursor-agent-team/_scripts/tts_speak.py --list-voices
```

## Content Preparation (MUST do before calling script)

The script only reads aloud. Content MUST be prepared as speakable natural language:

- **Tables**: Convert to natural language descriptions ("This table has two columns...")
- **Code**: Describe what code does ("This code iterates through numbers 0 to 9...")
- **Formulas**: Describe in words ("x equals y squared")
- **Images**: Describe briefly ("Here is an image showing...")
- **Markdown**: Remove all format symbols (`**`, `##`, backticks, `>`, `-`)
- **Links**: Read link text only, skip URLs

Prepared text should be: plain text, sound natural when read, retain core information.

## Environment Check

On first call, the script checks macOS + `say` command + Chinese voice availability. Results cached to `cursor-agent-team/ai_workspace/.tts_capability.json`.

When TTS is unavailable (`available: false`):
- Do NOT try to call TTS
- Silently use text reply instead
- Only explain when user explicitly asks

```bash
python cursor-agent-team/_scripts/tts_speak.py --check
python cursor-agent-team/_scripts/tts_speak.py --force-check
```

## Exit Codes

- 0: Success
- 1: Parameter error or execution failure
- 2: System not supported (not macOS)
- 3: TTS unavailable (environment check failed, silent exit)

---

**Version**: v1.0.0 (Created: 2026-02-26)
**Adapted from**: Cursor `_cursor/rules/tts_speech_rules.mdc` v1.2
