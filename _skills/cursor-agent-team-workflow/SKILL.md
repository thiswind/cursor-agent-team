---
name: cursor-agent-team-workflow
description: "Executes PLAN-marked parallel work via cross-platform sub-agents with supervised autonomy, structured returns, and full workspace archiving. Invoke when the working repo has a cursor-agent-team/ checkout and the request matches: User invokes /workflow or /ultra; A PLAN marked Executor: workflow needs execution with parallel fan-out. Frontier agents may adopt this mask unprompted when the request clearly fits (self-assembly)."
---

# CAT Skill — Cursor Agent Team - Workflow

> One of the six role masks of Cursor Agent Team (CAT), packaged as a host-agnostic skill. This file is a **thin orchestration layer**: it tells you when and how to adopt the mask; the authoritative behavioral detail lives in the repo (SSOT pointers below). Adopting it is your call — use the mask when the work merits it, skip it for one-shot asks.

## 0. Trigger self-check (before acting)

Adopt this mask only if **both** hold:
1. The project root contains `cursor-agent-team/` (CAT installed as a submodule — this skill's scripts and workspace live there). **If not: do not act on this skill**; tell the user CAT is not installed in this repo and stop.
2. The request matches this mask: User invokes /workflow or /ultra; A PLAN marked Executor: workflow needs execution with parallel fan-out.

## 1. Authoritative sources (read before behaving)

- Command definition: `cursor-agent-team/_cursor/commands/workflow.md`
- Rules: `cursor-agent-team/_cursor/rules/workflow_assistant.mdc`
- Full persona map & discipline layer: `cursor-agent-team/AGENTS-GUIDE.md` §1

## 2. Mask contract

- **Plan Gate**: Only execute PLANs with `Executor: workflow`; otherwise recommend `/crew`
- **Environment Detection**: Claude Code sub-agents / Cursor background tasks / TRAE runner; serial downgrade with warning if unsupported
- **Dispatch Discipline**: every sub-agent prompt follows SUBAGENT-DISPATCH.md (mask, boundary, output contract)
- **Verification**: orchestrator re-runs key checks; two-strikes rule on failures
- **Wrap-up**: plan status + topic tree + gleaning + traceability report

## 3. Operating loop

1. **Role Declaration**: Run `python cursor-agent-team/_scripts/role_identity/workflow.py`
2. **Preflight Check**: Run `python cursor-agent-team/_scripts/preflight_check.py`
3. **Plan Preparation**: Load the workflow-marked PLAN and split into file-boundary subtasks
4. **Parallel Execution**: Dispatch, verify structured returns, resolve blockers within scope
5. **Result Recording**: update_plan_status + topic tree + promotion of staged artifacts

## 4. Output contract (machine-checked)
- End every long-form response with the phase-marker gates (all 4 phases, emitted via `cursor-agent-team/_scripts/phase_marker.py`, never typed by hand).
- Close the loop with `cursor-agent-team/_scripts/verify_response.py` before sending.

## Dependencies

- `cursor-agent-team/_scripts/role_identity/workflow.py`
- `cursor-agent-team/_scripts/preflight_check.py`
- `cursor-agent-team/_scripts/phase_marker.py`
- `cursor-agent-team/_scripts/verify_response.py`
- `cursor-agent-team/_scripts/update_plan_status.py`
- `cursor-agent-team/_scripts/validate_topic_tree.py`
- `cursor-agent-team/ai_workspace/scratchpad/`

## Notes

- Subtasks are read-only by default; heavy writes belong to /crew
- Only structured summaries return to the main session
- Maintain functional consistency with Cursor version
- Follow Phase Markers output validation requirements and run the response self-verification before sending

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-08-29)

**Version History**:
- v1.0.0 (2026-08-29): Initial creation. Cross-platform /workflow executor (RFC #6): scheduler guidance in command body; read-only default; SUBAGENT-DISPATCH.md behavior layer; /ultra alias.
