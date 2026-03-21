---
name: cursor-agent-team-tts
description: TTS voice output functionality
user-invocable: false
---
When user explicitly requests voice output (trigger phrases: "read to me", "say it to me", "tell me", "read aloud", "speak it out", "voice output", "reply with voice", "voice feedback", "读给我听", "念给我听", "说给我听", "念出来", "朗读一下", "语音播报", "用语音回复", "语音反馈"):
1. Prepare content as speakable natural language:
   - Remove all Markdown syntax (**`, ##, `, >, - list markers, etc.)
   - Do NOT read table separators (|, |---|---|), describe tables in natural language
   - Do NOT read code literally, describe what the code does
   - Do NOT read LaTeX formulas, describe their meaning
   - Do NOT read URLs, only mention link text if relevant
2. Run (replace `EXT` with your `cursor-agent-team` root; **TTS is optional** — on Windows without macOS `say`, the script may silently skip; install success does not depend on TTS):
   ```bash
   python "$EXT/_scripts/tts_speak.py" "prepared text content"
   ```
3. If the script fails, fallback to text response without mentioning TTS failure
