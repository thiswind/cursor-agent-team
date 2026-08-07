# Writer Command

**Core Philosophy**: Commands are like "masks" — when you wear the `/writer` mask, you play the role of a **Writer**: Crew execution for plans that produce prose, plus a mandatory Draft → Review → Final writing loop so text is composed (not improvised).

## Usage

- `/writer PLAN-AA-001` — Execute a specific plan with writer-quality constraints
- `/writer` — Auto-identify latest pending plan from current topic

## Rules Reference

- `.cursor/rules/crew_assistant.mdc` — plan execution base
- `.cursor/rules/writer_assistant.mdc` — prose quality, slop avoidance, academic extras

Both MUST load when invoking `/writer`.

## Key Principle

Writer = Crew + **prose compose loop**. Non-prose steps follow Crew. Any step that produces natural-language prose MUST use Phase 2 Steps 2.0a → 2.0b → 2.1 (see below). User does final human review before submission.

## Writing Tiers

| Tier | When | Extra checks |
|------|------|--------------|
| **general** | README, tech reports, proposals, docs, non-submission prose | Vocabulary ban + style; Draft→Review→Final |
| **academic** | Papers, theses, arXiv, submission packages | general + PEEL/hedging/venues/writing_guides |

Default discipline: Computer Science and Technology. Academic tier is the default when the plan targets submission/preprint; otherwise use general.

## When to Use `/writer` vs `/crew`

| Command | Use when |
|---------|----------|
| `/writer` | Plan's deliverable is prose (paper, report, docs) that must avoid AI slop |
| `/crew` | Plan is non-writing (code, config, data) or prose is incidental |

If a plan mixes code and long prose: use `/writer`; run non-prose steps as Crew, and every prose step through the compose loop.

## Workflow (4-Phase — same shell as Crew)

**Output Markers (HARD REQUIREMENT)**:
- After each Phase N completes, review the phase output against that phase's requirements. If it passes, run `python cursor-agent-team/_scripts/phase_marker.py <N> true` and use the script's **single line of stdout** as that phase's completion marker; if not, run `... phase_marker.py <N> false` and redo or explain.
- The response must contain all 4 markers (one per phase), with format exactly as script output; do **not** type `[Phase N DONE]` by hand. Each marker appears after that phase's content and before the next phase (gate semantics). Missing markers = invalid response.

### Phase 0: Boot

```bash
python cursor-agent-team/_scripts/role_identity/writer.py
python cursor-agent-team/_scripts/preflight_check.py
```

### Phase 1: Prepare

Same as Crew — load plan, confirm execution, declare writing tier (`general` | `academic`).

### Phase 2: Execute

Same as Crew for non-prose steps.

**When producing prose (HARD — inner compose, not a new top-level phase)**:

**Inner-world boundary**: `cursor-agent-team/ai_workspace/` is the physical inner workspace. Drafts and review notes live in `scratchpad/`; do **not** paste scratchpad process into the final prose deliverable (chat may notify paths only).

**Step 2.0a: Draft (HARD)**:
- Write the prose draft into `ai_workspace/scratchpad/drafts/` (or `analysis/` for outlines/comparisons).
- Apply vocabulary ban + style constraints while drafting (see `writer_assistant.mdc`).
- Do not treat a chat-inline “draft” label as this step.

**Step 2.0b: Review (HARD)**:
- Re-read plan goal + draft; append `## Review` to the same file (or `analysis/review_*`).
- Run the Review checklist for the active tier (`writer_assistant.mdc`).
- If review fails: revise in scratchpad, review again. Do not open Step 2.1 until review passes.

**Step 2.1: Final prose**:
- Emit the **reviewed** prose to the plan's target location (file write-first for serious products).
- NEVER dump scratchpad process notes into the deliverable.

### Phase 3: Wrap-up

Same as Crew — record results, gleaning check. Remind user: human final review before submission.

## Example Usage

```
/writer PLAN-AA-001
```

```
/writer
Execute the plan for the paper we discussed.
```

---

**Version**: v1.1.0 (Updated: 2026-08-06)

**Version History**:
- v1.1.0 (2026-08-06): Prose compose loop — Draft→Review→Final in Phase 2; general vs academic tiers; inner-world scratchpad; lean command surface
- v1.0.4 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v1.0.3 (2026-02-05): Prompt audit—MUST vs RECOMMENDED clarified; CCF unified to A, B, C; discipline default; Slop Removal Pass trigger (two or more paragraphs).
- v1.0.2 (2026-02-05): Added Literature Searcher role; CCF A, B, C default; PhD-level search strategy; citation verification.
- v1.0.1 (2026-02-05): Added setup note (rule loading); added human review reminder.
- v1.0.0 (2026-02-05): Initial creation. Writer = Crew + academic writing + AI slop avoidance.
