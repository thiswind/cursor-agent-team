# Workflow Command

**Core Philosophy**: Commands are like "masks" — when you wear the `/workflow` mask, you play the role of a **Workflow Executor**, supervised autonomous execution of PLAN-marked parallel work via cross-platform sub-agents — a peer of /crew, not a second planning system.

## Usage

- `/workflow PLAN-WF-001` — Execute a specific plan with parallel sub-agents
- `/workflow` — Auto-identify latest pending workflow-marked plan
- `/ultra` — Alias of `/workflow`

**Key Principle**: Plan-driven parallel execution. Without an explicit `Executor: workflow` mark in the PLAN, recommend `/crew`. Subtasks are read-only by default; heavy writes route to `/crew`. Behavior layer follows SUBAGENT-DISPATCH.md.

## Rules Reference

- `.cursor/rules/workflow_assistant.mdc` — executor behavior, scheduling, parallel safety
- `SUBAGENT-DISPATCH.md` (product root) — sub-agent dispatch template & acceptance discipline

## Cross-Platform Scheduler Guidance

Detect once per run, in this order:

| Environment | Carrier | Notes |
|-------------|---------|-------|
| Claude Code extension present | `run_in_background` sub-agents | original path, full parity |
| Stock Cursor IDE | native Background Task / `multitask` | batch dispatch, isolated context |
| TRAE SOLO runtime | native task runner | per-task logs under scratchpad |

- Sub-task logs are separated per subtask; only summaries aggregate to the main session.
- Old IDE without background tasks: serial downgrade + warning line (parallel acceleration unavailable).

## When to Use `/workflow` vs `/crew`

| Command | Use when |
|---------|----------|
| `/workflow` | Large fan-out, read-mostly recon, batch audits, multi-branch comparison, offline batch delivery |
| `/crew` | Multi-stage dependent changes, releases, paper revision, any write-heavy serial process |

Both report back into `ai_workspace/` identically (plan ledger + topic tree). The PLAN is the sole intent SSOT.

## Workflow (4-Phase)

**Output Markers (HARD REQUIREMENT)**:
- After each Phase N completes, review the phase output against that phase's requirements. If it passes, run `python cursor-agent-team/_scripts/phase_marker.py <N> true` and use the script's **single line of stdout** as that phase's completion marker; if not, run `... phase_marker.py <N> false` and redo or explain.
- The response must contain all 4 markers (one per phase), with format exactly as script output; do **not** type `[Phase N DONE]` by hand. Each marker appears after that phase's content and before the next phase (gate semantics). Missing markers = invalid response.

**Response Self-Verification (HARD REQUIREMENT)**:
- Before sending the response, save the complete response text to `cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md`, then run:
  ```bash
  python cursor-agent-team/_scripts/verify_response.py --phases 4 --file cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md
  ```
- If the check reports INVALID: fix the reported errors and re-verify. Never send an unverified response.

---

### Phase 0: Boot

```bash
python cursor-agent-team/_scripts/role_identity/workflow.py
python cursor-agent-team/_scripts/preflight_check.py
```

---

### Phase 1: Prepare

1. Read `cursor-agent-team/ai_workspace/discussion_topics.md` and `cursor-agent-team/ai_workspace/plans/INDEX.md`
2. Load the target PLAN (explicit argument wins; otherwise latest `Executor: workflow` plan; ask if ambiguous)
3. Verify the `Executor: workflow` mark; if absent → recommend `/crew` and stop
4. Detect environment (Claude Code / Cursor background task / TRAE task runner); if none supports background → announce serial downgrade with warning
5. Split PLAN stages into subtasks along file boundaries; draft the dispatch prompts per SUBAGENT-DISPATCH.md

---

### Phase 2: Execute

Dispatch sub-agents in parallel batches (or serial downgraded batch).

For each sub-agent:
- Task prompt = [Role] mask + rules paths / [Context] host root + read-write boundary / [Task] goal + steps + acceptance / [Output Contract] summary / files_changed / verification / leftovers
- Detailed logs to `cursor-agent-team/ai_workspace/scratchpad/<subtask>/`
- On return: verify the claim (re-run key checks, spot-read cited files); reject with reason + expected-vs-actual; two strikes → take back or escalate
- Blockers within task scope: resolve with bounded initiative (stay inside approved phases); scope-external → escalate to user

---

### Phase 3: Wrap-up

1. Record results with `update_plan_status.py` (completed / paused / in_progress)
2. Promote accepted artifacts out of scratchpad staging
3. Append topic-tree entry via `validate_topic_tree.py update`
4. Gleaning check
5. Report: per-subtask summary table + traceability (task ID → PLAN → logs)

---

## Example

```
/workflow PLAN-WF-001

/workflow
Execute the audit plan for all open docs.

/ultra PLAN-WF-001
```

---

<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-08-29)

**Version History**:
- v1.0.0 (2026-08-29): Initial creation. Cross-platform /workflow executor (RFC #6): scheduler guidance in command body; read-only default; SUBAGENT-DISPATCH.md behavior layer; /ultra alias.
