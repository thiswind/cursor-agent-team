# Prompt Engineer Workspace

Workspace for `/prompt_engineer` command. Path: `cursor-agent-team/ai_workspace/prompt_engineer/`

---

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Session | `sessions/` | `session_YYYYMMDD_HHMMSS/` |
| Mode | `sessions/[session]/` | `mode.md` |
| Target Prompt | `sessions/[session]/` | `target_prompt.md` |
| Session Log | `sessions/[session]/` | `session_log.md` |
| Requirements | `sessions/[session]/` | `requirements.md` |
| Questions | `sessions/[session]/` | `questions.md` |
| Examples | `sessions/[session]/` | `examples.md` |
| Comparison | `sessions/[session]/` | `comparison.md` |
| Drafts | `sessions/[session]/drafts/` | `*_draft.md` |

---

## NEVER DO

- NEVER save final outputs to this workspace (use official directories)
- NEVER skip user confirmation before finalization
- NEVER delete this README
- NEVER overwrite existing prompts without comparison

---

## Output Locations (NOT in ai_workspace)

| Type | Directory | Format |
|------|-----------|--------|
| Prompts | `cursor-agent-team/ai_prompts/` | `[name]_prompts.md` |
| Commands | `.cursor/commands/` | `[name].md` |
| Rules | `.cursor/rules/` | `[name]_assistant.mdc` |

---

## Session Files

| File | Purpose | Mode |
|------|---------|------|
| `mode.md` | Create or Maintain | Both |
| `target_prompt.md` | Existing prompt content | Maintain |
| `session_log.md` | Complete session log | Both |
| `requirements.md` | Requirements analysis | Both |
| `questions.md` | Q&A record | Both |
| `examples.md` | Behavior examples | Both |
| `comparison.md` | Before/after comparison | Maintain |
| `drafts/prompt_draft.md` | Draft prompt | Both |
| `drafts/command_draft.md` | Draft command | Both |
| `drafts/rule_draft.md` | Draft rule | Both |

---

## Workflow

### Create Mode
1. Create session: `sessions/session_YYYYMMDD_HHMMSS/`
2. Save mode to `mode.md`
3. Analyze requirements → `requirements.md`
4. Ask questions → `questions.md`
5. Generate examples → `examples.md`
6. Create drafts → `drafts/`
7. Get user confirmation
8. Save to official directories

### Maintain Mode
1. Create session
2. Read existing prompt → `target_prompt.md`
3. Analyze changes → `requirements.md`
4. Generate comparison → `comparison.md`
5. Update drafts
6. Get user confirmation
7. Save to official directories

---

## Cleanup

- Retention: 7 days (or clean after finalization)
- Command: `python cursor-agent-team/_scripts/cleanup_ai_workspace.py --dir prompt_engineer/sessions/session_XXXXXXXX_XXXXXX`

---

**Last Updated**: 2026-02-02
