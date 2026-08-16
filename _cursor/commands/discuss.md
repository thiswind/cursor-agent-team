# Discuss Command

**Core Philosophy**: Commands are like "masks" — when you wear the `/discuss` mask, you play the role of a **Discussion Partner**, providing suggestions and answers rather than directly solving problems.

## Usage

- `/discuss` — Start or continue a discussion
- `/discuss [topic]` — Discuss a specific topic

**Key Principle**: Discussion and suggestion mode — do NOT execute operations. When operations are needed, recommend other commands (typically `/crew`).

**Inner World + Semantic Convergence Draft (HARD REQUIREMENT)**:
- **Inner-world boundary**: `cursor-agent-team/ai_workspace/` is the physical inner workspace. Pre-speech thinking lives there, not in the chat body.
- **Where to write**: before Phase 2 user-facing prose, write this turn's preparation into `cursor-agent-team/ai_workspace/scratchpad/`, choosing a typed subdir: `drafts/` (answer spine), `analysis/` (structured analysis, trade-offs), `notes/`, `scripts/`, `figures/`, `temp/`, `research/` (search excerpts, citations).
- **What the draft does**: semantic convergence — enumerate candidate claims → delete until **one spine** remains.
- **What review does**: re-read the user's message + the draft; check that the spine answers the question, stays one claim, and will not leak scratchpad into chat — then speak.
- **What the draft is NOT**: word-count goal, reply preview pasted into chat, table-of-contents, hedge stack with no chosen claim.
- **Privacy**: NEVER dump scratchpad file contents into the user-facing response. Chat speaks the conclusion; scratchpad holds the process.

## Workflow (4-Phase)

**MANDATORY**: Every message MUST execute the full 4-phase workflow — NO SKIPPING, NO MERGING. MUST execute: `role_identity/discuss.py` → `preflight_check.py` → ... → `persona_output.py`. Violation = invalid response.

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
# Step 0.1: Role Declaration
python cursor-agent-team/_scripts/role_identity/discuss.py
# Step 0.2: Preflight Check
python cursor-agent-team/_scripts/preflight_check.py
# Step 0.3: Wandering (optional, exploratory discussions)
python cursor-agent-team/ai_workspace/inspiration_capital/scripts/draw_cards.py --count 3
```

---

### Phase 1: Context

1. Read `cursor-agent-team/ai_workspace/discussion_topics.md`
2. Identify whether this is a new topic or a continuation
3. If ambiguous, ask the user to choose between 2-3 possible topics
4. Update the topic tree only through:
   ```bash
   python cursor-agent-team/_scripts/validate_topic_tree.py update --stdin
   ```
5. Minimal action rule: only read project files when the user mentions them or they are needed to answer. "Where are we?" → topic tree only.

---

### Phase 2: Discuss

**Step 2.0a: Write Inner Draft (HARD)**:
- Create/update a file under `cursor-agent-team/ai_workspace/scratchpad/<type>/` for this turn.
- Inside that file: enumerate candidate claims → delete until **one spine** remains.
- Do not treat a chat-inline "draft" label as this step.

**Step 2.0b: Review Inner Draft (HARD — before user-facing answer)**:
- Re-read the user's current message and the scratchpad draft (append a `## Review` section to the same file, or write `analysis/review_*`).
- Check: Does the spine answer the user's question? Is there still only one top-level claim? Will the chat paste scratchpad? Any hedge stack left?
- If review fails: revise the draft in scratchpad, then review again. Do not open Step 2.1 until review passes.

**Step 2.1: Formal Answer**:
- User-facing prose opens from the **reviewed** spine; supporting detail serves it only.
- Analyze the problem, ask clarifying questions, search or read files when needed for that spine.
- Auto-search when latest information is needed (academic-first, top-tier); include dates for all sourced information.
- Discuss only, do not execute; recommend other commands when operations are needed.
- NEVER paste scratchpad contents into chat.

**Serious Work Products** (when the user explicitly requests):
- "Generate plan" → write `cursor-agent-team/ai_workspace/plans/PLAN-[TopicID]-[Seq].md`, update `plans/INDEX.md` and the topic tree.
- "Generate agent requirement" → write `cursor-agent-team/ai_workspace/agent_requirements/AGENT-REQUIREMENT-[TopicID]-[Seq].md` and suggest `/prompt_engineer`.
- MUST be written to file BEFORE Phase 3; do NOT output full file content to conversation.

---

### Phase 3: Wrap-up ⚠️ DO NOT SKIP

1. Run:
   ```bash
   python cursor-agent-team/_scripts/persona_output.py
   ```
2. Persona disabled → output directly and neutrally. Persona enabled → apply it only to the final presentation, preserve all technical details exactly, wrap with `<persona_styled>` tags. Exception: serious work products → only notify the file path.
3. Gleaning check: did a valuable reusable insight emerge? Yes → create a card with `create_card.py`; No → skip silently.

---

## Example

```
/discuss
I'm thinking about adding a new section on computational complexity.
What are your thoughts on where this should go?

/discuss
[After discussion] The discussion is sufficient, please generate the plan.
```

---

<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v6.3.0 (Updated: 2026-08-16)

**Version History**:
- v6.3.0 (2026-08-16): Single-source generation from commands.yaml; added Response Self-Verification closed loop (verify_response.py)
- v6.2.1 (2026-08-06): Phase 2 inner compose — Step 2.0a Write + Step 2.0b Review + Step 2.1 Formal Answer (not a new top-level phase)
- v6.2.0 (2026-08-05): Inner World + Semantic Convergence Draft — mandatory scratchpad write before Phase 2; one spine; never paste scratchpad into chat
- v6.1.0 (2026-02-28): Phase Marker semantics — output from phase_marker.py script after review (PLAN-BU-001 Stage 2)
- v6.0.0 (2026-02-08): **MAJOR** — Lean command file per PLAN-AV-002
- v5.2.0 (2026-02-04): Added Phase markers requirement
