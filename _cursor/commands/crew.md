# Crew Command

**Core Philosophy**: Commands are like "masks" — when you wear the `/crew` mask, you play the role of a **Crew Member** (universal worker), executing plans strictly according to specifications.

## Usage

- `/crew PLAN-C-001` — Execute specific plan
- `/crew` — Auto-identify latest pending plan from current topic

**Key Principle**: Execution mode — strictly follow plans without deviation. Auto-search for solutions when encountering difficulties.

## Workflow (4-Phase)

**Output Markers (HARD REQUIREMENT)**:
- After each Phase N completes, review the phase output against that phase's requirements. If it passes, run `python cursor-agent-team/_scripts/phase_marker.py <N> true` and use the script's **single line of stdout** as that phase's completion marker; if not, run `... phase_marker.py <N> false` and redo or explain.
- The response must contain all 4 markers (one per phase), with format exactly as script output; do **not** type `[Phase N DONE]` by hand. Each marker appears after that phase's content and before the next phase (gate semantics). Missing markers = invalid response.

---

### Phase 0: Boot

**Step 0.1: Role Declaration**
```bash
python cursor-agent-team/_scripts/role_identity/crew.py
```

**Step 0.2: Preflight Check**
```bash
python cursor-agent-team/_scripts/preflight_check.py
```

---

### Phase 1: Prepare

1. Read `cursor-agent-team/ai_workspace/discussion_topics.md`
2. Read `cursor-agent-team/ai_workspace/plans/INDEX.md`
3. Identify and load the plan to execute
4. Display plan summary, wait for user confirmation
5. (Optional) Search latest information, read related documents

---

### Phase 2: Execute

- Execute plan steps one by one
- Auto-search for solutions when encountering problems
- Do not deviate from plan; report to user when modifications needed
- Execute strictly according to plan; wait for user confirmation when needed

---

### Phase 3: Wrap-up ⚠️ DO NOT SKIP

**Step 3.1: Record Results**
- If the target plan is known, update plan/index bookkeeping with:
  ```bash
  python cursor-agent-team/_scripts/update_plan_status.py PLAN-[TopicID]-[Seq] --status completed --session cursor-agent-team/ai_workspace/crew/sessions/session_YYYYMMDD_HHMMSS --note "Implementation completed and verified"
  ```
- Use `--status paused` or `--status in_progress` instead when execution is blocked or partial.
- If the target plan cannot be inferred, do not guess; report: `Plan status not updated: target plan could not be inferred.`
- Update `discussion_topics.md` execution record only when this execution changes topic state.
- Record format when topic update is needed: `[Time] - /crew - [PlanID] - Execution completed (success/failed/partial)`

**Step 3.2: Gleaning Check**
- Any useful methods/techniques discovered during execution?
- Yes → Run `create_card.py` to create inspiration card
- No → Skip silently

---

## Example

```
/crew PLAN-C-001
```

---

**Version**: v4.1.0 (Updated: 2026-02-28)

**Version History**:
- v4.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v4.0.0 (2026-02-08): **MAJOR** — Lean command file per PLAN-AV-002. Removed human documentation (Purpose, Role Definition, Key Features, Best Practices, Integration, Notes). Kept core workflow and markers.
- v3.0.1 (2026-02-05): Phase marker format — [Phase N DONE] for LLM tokenizer stability
- v3.0.0 (2026-02-03): **MAJOR** — Standardized to English-only.
- v2.1.0 (2026-02-03): Merge role declaration into Phase 0.
- v2.0.0 (2026-02-03): **MAJOR REFACTOR** — Simplified from 11 steps to 4 phases.
