---
name: cursor-agent-team-dispatch
description: "Render compliant dispatch prompts (dispatch_header.py) and verify structured returns (verify_dispatch_return.py) with the two-strikes ledger. Invoke when: dispatching sub-agents; parallel task fan-out; checking a sub-agent's structured return."
---

# CAT Operation Skill — Sub-agent Dispatch Discipline

SUBAGENT-DISPATCH.md's template and return contract, executable. The header renderer guarantees the Role/Behavior/Context/Task/ Output-Contract sections; the return checker enforces the four fields (summary/files_changed/verification/leftovers) and records strikes — two strikes means re-dispatch, not re-read.

## The scripts (single source of truth)

| Command | What it does |
|---|---|
| `python cursor-agent-team/_scripts/dispatch_header.py` | render the dispatch prompt (mask/task/boundary/parallel-group) |
| `python cursor-agent-team/_scripts/verify_dispatch_return.py` | four-field check + two-strikes ledger |

## Rules (hard)

- Parallel agents get disjoint file boundaries (state it in the prompt)
- Trust but verify: every return is checked before its facts are used
- Two strikes: reject the agent's outputs for this task

## References

- SUBAGENT-DISPATCH.md (deep reference)

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-09-08)

**Version History**:
- v1.0.0 (2026-09-08): header renderer + return checker + strikes ledger
