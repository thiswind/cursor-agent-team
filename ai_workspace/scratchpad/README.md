# Scratchpad

Temporary workspace for `/discuss` command. Path: `cursor-agent-team/ai_workspace/scratchpad/`

---

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Notes | `notes/` | `note_[topic]_YYYYMMDD.md` |
| Scripts | `scripts/` | `script_[purpose]_YYYYMMDD_HHMMSS.[ext]` |
| Analysis | `analysis/` | `analysis_[topic]_YYYYMMDD_HHMMSS.md` |
| Temp | `temp/` | `temp_[desc]_YYYYMMDD_HHMMSS.[ext]` |

---

## NEVER DO

- NEVER save notes outside `notes/`
- NEVER save permanent files here (use official directories)
- NEVER delete README files in subdirectories

---

## Directory Structure

```
scratchpad/
├── README.md           # This file
├── notes/              # Discussion notes
├── scripts/            # Temporary scripts
├── analysis/           # Analysis results
└── temp/               # Other temporary files
```

---

## Cleanup

- Retention: 7 days
- Command: `python cursor-agent-team/_scripts/cleanup_ai_workspace.py --older-than 7`

---

**Last Updated**: 2026-02-02
