---
name: cursor-agent-team-doctor
description: "Machine-run the four cold-start checks — deployment form, version, ignore policy, orphan shapes — via cat_doctor.py; --fleet audits multiple host repos read-only. Invoke when: cold start in a CAT host repo; check CAT health; after install/upgrade verification; fleet audit across host repos."
---

# CAT Operation Skill — CAT Health Check (cold start & upgrades)

The two-command self-check table from AGENTS-GUIDE sec.5.2, promoted to one command. On the v0.24.0 whitelist policy the ignore check reports whether the state layer is actually tracked — catching both legacy ignore-all remnants and fresh installs where nothing was added yet.

## The scripts (single source of truth)

| Command | What it does |
|---|---|
| `python cursor-agent-team/_scripts/cat_doctor.py` | form/version/ignore/orphans checks; --fleet HOST ROOTS...; --json |

## Rules (hard)

- Run at cold start; trust its output over memory
- critical items (orphan shapes, untracked state layer) block work until resolved or acknowledged

## References

- AGENTS-GUIDE.md sec.5 (deployment topologies)
- DEPLOYMENT.md (v0.24.0)

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-09-08)

**Version History**:
- v1.0.0 (2026-09-08): four checks + --fleet
