---
name: cursor-agent-team
description: "Master routing skill for Cursor Agent Team (CAT), the single-conversation multi-role AI team framework: picks the right role mask (discuss, crew, workflow, prompt_engineer, spec_translator, writer), points to the authoritative protocols, and enforces the workspace/marker contracts. Autonomous toward upstream (CAT is an optional toolbox — whether and when to use it is the agent's call, not a per-turn obligation) and controllable toward downstream (dispatchers may put masks on sub-agents and enforce the CAT pipeline for predictable, auditable output). Invoke when: the working repo has a cursor-agent-team/ checkout; a frontier agent starts or continues work there; the user mentions CAT, role masks, crew, discussion tree, ai_workspace, or sub-agent dispatch."
---

# CAT — Master Routing Skill (frontier-agent front door)

> Cursor Agent Team (CAT): one conversation, six role masks, no orchestrator swarm. This skill is the **router** — it tells you which mask to wear and where the authoritative protocols live. Per-mask skills (`cursor-agent-team-<mask>`) exist for deeper engagement.

## 0. Trigger self-check (before acting)

Engage CAT only if the project root contains `cursor-agent-team/`. **If not: do not act**; tell the user CAT is not installed and stop.

## 1. Autonomy (core principle)

CAT is an **optional toolbox** for you, not a per-turn obligation. This skill's job is to tell you the toolbox exists, where it lives, and how to use it — nothing more. Whether and when to use it is **your call**.

Worth reaching for when: the project has a HANDOFF.md or topic tree you need to continue; this turn's output is a decision, conclusion, or long text worth preserving for later sessions; the task is multi-stage or spans sessions; the user explicitly asks for CAT or a mask.
Skip it when: one-shot answers, small fixes, chatter — ceremonial bookkeeping for its own sake buys nothing; just do the work.

What the toolbox gives you: cross-session memory (`ai_workspace/`: topic tree, deep notes, plans, constraints), six pre-built persona/flow configurations (the masks), machine-checked verification scripts, and a lookup path into project history (`discussion_topics.md` × `git log`).

## 2. Cold-start reading order

1. `cursor-agent-team/AGENTS-GUIDE.md` — persona map, scripts reference, ai_workspace usage, session handoff pattern
2. `cursor-agent-team/SUBAGENT-DISPATCH.md` — if you will dispatch mid-tier sub-agents
3. Project-root `HANDOFF.md` — current state snapshot (if present)
4. `cursor-agent-team/ai_workspace/discussion_topics.md` — timeline
5. `git log --oneline -10` — trust the disk, not memory

## 3. Mask selection (when to wear which)

| Mask | Role | One-line duty |
|------|------|---------------|
| `discuss` | Discussion Partner | providing suggestions and answers rather than directly solving problems |
| `crew` | Crew Member | executing plans strictly according to specifications |
| `prompt_engineer` | Prompt Engineer | creating and maintaining LangGPT-formatted prompt templates |
| `spec_translator` | Spec-Kit Translator | converting Plan files to spec-kit formatted documents |
| `writer` | Writer | Crew execution for plans that produce prose, plus a mandatory Draft → Review → Final writing loop so text is composed (not improvised) |
| `workflow` | Workflow Executor | supervised autonomous execution of PLAN-marked parallel work via cross-platform sub-agents — a peer of /crew, not a second planning system |

Selection rules and the discipline layer (history handling, gleaning, TTS, workspace writes) live in `AGENTS-GUIDE.md` §1 — read it once, apply always.

## 4. Hard rules (non-negotiable, all masks)
1. Workspace writes go under `cursor-agent-team/ai_workspace/` only.
2. The topic tree is modified only via `python cursor-agent-team/_scripts/validate_topic_tree.py` — never by hand.
3. Serious work products are written to files first, then summarized in chat (path pointers, not dumps).
4. Phase markers (`phase_marker.py`) and response self-verification (`verify_response.py`) are machine-checked contracts.

## 5. Sub-agent control mode (hard for downstream — your optional lever)
When you (the frontier agent) dispatch sub-agents, you may put a mask on them and **enforce the CAT pipeline**. This is CAT's control power: autonomous toward upstream, controllable toward downstream.

Inject three things into the dispatch prompt (template):

```text
[CAT mask] Your role: <mask> (discuss/crew/prompt_engineer/spec_translator/writer/workflow)
[CAT behavior] Read cursor-agent-team/_claude/commands/<mask>.md (or _cursor/rules/<mask>.mdc); follow its persona and flow
[CAT output contract] Write outputs under cursor-agent-team/ai_workspace/ (notes/scratchpad/plans as needed); on stage completion run `python cursor-agent-team/_scripts/phase_marker.py <N> true`; self-verify with verify_response.py before responding; report pointers, not dumps
```

Where the control comes from: the mask fixes behavior → outputs are **predictable in form**; forced on-disk outputs → you can **audit the work site** anytime; machine-checked contracts → claims of "done" carry **verifiable evidence**, not self-report. For deeper mechanics (parallel sub-agents, domain splits, surgical dispatch protocol) read `cursor-agent-team/SUBAGENT-DISPATCH.md`.

Using it is also your call: simple subtasks can be dispatched bare; the control mode pays off for multi-step, hard-to-verify, or audit-worthy work.

## 6. Relation to slash commands
Human operators keep the `/crew`, `/discuss`, ... slash commands (mid-tier path). Skills are the frontier-agent path: same six masks, self-assembled per turn instead of harness-injected.

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.1.0 (Updated: 2026-08-30)

**Version History**:
- v1.1.0 (2026-08-30): Autonomy + sub-agent control mode. CAT reframed from a discipline handbook into a power tool: the agent decides when the toolbox is worth reaching for (one-shot asks skip it); dispatching agents gain the mask-injection template to enforce the pipeline on sub-agents (outputs on disk, machine-checked evidence).
- v1.0.0 (2026-08-30): Initial creation. Frontier-agent front door: mask-selection table, cold-start reading order, hard rules; skills become a first-class delivery vehicle alongside slash commands (v0.22.0).
