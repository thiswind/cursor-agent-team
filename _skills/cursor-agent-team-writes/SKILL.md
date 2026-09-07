---
name: cursor-agent-team-writes
description: "All writes to shared ai_workspace state (topic tree, notes append, plan checkboxes, plans INDEX) go through the single write gateway cat_write.py — never direct Write/Edit. Invoke when: update the topic tree / add a round; append a note; check off plan items; rebuild plans INDEX; any write intent targeting ai_workspace state files."
---

# CAT Operation Skill — State-layer Writes (single gateway)

One gateway, four operations, zero direct writes. The gateway serializes concurrent sessions (flock queue), validates per target (topic tree goes through validate_topic_tree), lands atomically (temp + os.replace), and journals every attempt (JSONL under ai_workspace/temp/cat_write_journal/). Direct Write/Edit on state files is the #1 discipline violation this skill exists to prevent.

## The scripts (single source of truth)

| Command | What it does |
|---|---|
| `python cursor-agent-team/_scripts/cat_write.py` | the gateway: notes --append / topic-round / plan-status / index-rebuild / journal / lock-wait-report |

## Rules (hard)

- State-layer files are NEVER written with Write/Edit tools — always via cat_write.py
- topic-round validates first (R1-R6); rejected writes never land
- Lock wait is journaled; check lock-wait-report if sessions feel slow
- Parallel sessions: file-boundary split + gateway serialization = safe

## References

- RFC-CONCURRENCY-001 (workshop plans/) — design & rulings
- AGENTS-GUIDE.md sec.1 discipline layer

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-09-08)

**Version History**:
- v1.0.0 (2026-09-08): gateway core (global flock, journal, topic-round via validator, notes/plan-status/index-rebuild)
