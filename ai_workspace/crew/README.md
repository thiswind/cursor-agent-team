# Crew Workspace

Workspace for `/crew` command. Path: `cursor-agent-team/ai_workspace/crew/`

---

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Session | `sessions/` | `session_YYYYMMDD_HHMMSS/` |
| Execution Log | `sessions/[session]/` | `session_log.md` |
| Plan Copy | `sessions/[session]/` | `plan.md` |
| Research | `sessions/[session]/` | `research.md` |
| Documents | `sessions/[session]/` | `documents.md` |
| Steps | `sessions/[session]/` | `execution_steps.md` |
| Runtime Research | `sessions/[session]/` | `runtime_research.md` |
| Results | `sessions/[session]/` | `results.md` |
| Discussion Update | `sessions/[session]/` | `discussion_update.md` |

---

## NEVER DO

- NEVER execute without reading the plan first
- NEVER modify plan goals based on search results (report to user instead)
- NEVER skip updating `discussion_topics.md` after execution
- NEVER delete this README

---

## Workflow

1. Read plan from `../plans/PLAN-*.md`
2. Create session: `sessions/session_YYYYMMDD_HHMMSS/`
3. Copy plan to `plan.md`
4. Research and save to `research.md`
5. Execute step by step, record to `execution_steps.md`
6. Save runtime searches to `runtime_research.md`
7. Save results to `results.md`
8. Update `../discussion_topics.md`

---

## Session Files

| File | Purpose | When |
|------|---------|------|
| `session_log.md` | Complete execution log | Always |
| `plan.md` | Plan copy for reference | Start |
| `research.md` | Pre-execution research | Before execution |
| `documents.md` | Document reading summary | Before execution |
| `execution_steps.md` | Step-by-step record | During execution |
| `runtime_research.md` | Runtime search results | During execution |
| `results.md` | Final results | After execution |
| `discussion_update.md` | Topic tree update content | After execution |

---

## Cleanup

- Retention: 7 days
- Command: `python cursor-agent-team/_scripts/cleanup_ai_workspace.py --dir crew/sessions/session_XXXXXXXX_XXXXXX`

---

**Last Updated**: 2026-02-02
