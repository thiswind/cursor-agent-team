---
name: cursor-agent-team-closing
description: "Orchestrate the five closing steps — topic-tree round, response verify, closing note, handoff snapshot, commit — via closing_protocol.py; stop-at-first-failure with recovery hints. Invoke when: session wrap-up / closing; handoff / archive this session; topic tree round before ending; commit the workspace."
---

# CAT Operation Skill — Session Closing (five steps, one command)

Five prompt paragraphs become one command. Each step is skipped when its argument is absent, so partial closings stay honest; the commit step runs commit_workspace.py (add -f + per-path assert), the same helper shipped in v0.23.0.

## The scripts (single source of truth)

| Command | What it does |
|---|---|
| `python cursor-agent-team/_scripts/closing_protocol.py` | orchestrator: --tree-file / --verify-file / --note / --snapshot-title / --commit-msg |
| `python cursor-agent-team/_scripts/commit_workspace.py` | add -f + per-path tracked assert + commit (v0.23.0) |

## Rules (hard)

- Closing is one command, not five remembered steps
- A failed step prints its recovery hint; earlier steps are already done — do not redo them
- Snapshot notes are CREATE-only; never edit old snapshots

## References

- AGENTS-GUIDE.md sec.4 (session handoff pattern)
- DESIGN-SKILLIFY-005 G8 (workshop plans/)

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-09-08)

**Version History**:
- v1.0.0 (2026-09-08): five-step orchestrator
