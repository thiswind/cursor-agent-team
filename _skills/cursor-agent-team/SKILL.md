---
name: cursor-agent-team
description: "Master routing skill for Cursor Agent Team (CAT), the single-conversation multi-role AI team framework: picks the right role mask (discuss, crew, workflow, prompt_engineer, spec_translator, writer), points to the authoritative protocols, and enforces the workspace/marker contracts. Invoke when: the working repo has a cursor-agent-team/ checkout; a frontier agent starts or continues work there; the user mentions CAT, role masks, crew, discussion tree, ai_workspace, or sub-agent dispatch."
---

# CAT — Master Routing Skill (frontier-agent front door)

> Cursor Agent Team (CAT): one conversation, six role masks, no orchestrator swarm. This skill is the **router** — it tells you which mask to wear and where the authoritative protocols live. Per-mask skills (`cursor-agent-team-<mask>`) exist for deeper engagement.

## 0. Trigger self-check (before acting)

Engage CAT only if the project root contains `cursor-agent-team/`. **If not: do not act**; tell the user CAT is not installed and stop.

## 1. Cold-start reading order

1. `cursor-agent-team/AGENTS-GUIDE.md` — persona map, scripts reference, ai_workspace usage, session handoff pattern
2. `cursor-agent-team/SUBAGENT-DISPATCH.md` — if you will dispatch mid-tier sub-agents
3. Project-root `HANDOFF.md` — current state snapshot (if present)
4. `cursor-agent-team/ai_workspace/discussion_topics.md` — timeline
5. `git log --oneline -10` — trust the disk, not memory

## 2. Mask selection (when to wear which)

| Mask | Role | One-line duty |
|------|------|---------------|
| `discuss` | Discussion Partner | providing suggestions and answers rather than directly solving problems |
| `crew` | Crew Member | executing plans strictly according to specifications |
| `prompt_engineer` | Prompt Engineer | creating and maintaining LangGPT-formatted prompt templates |
| `spec_translator` | Spec-Kit Translator | converting Plan files to spec-kit formatted documents |
| `writer` | Writer | Crew execution for plans that produce prose, plus a mandatory Draft → Review → Final writing loop so text is composed (not improvised) |
| `workflow` | Workflow Executor | supervised autonomous execution of PLAN-marked parallel work via cross-platform sub-agents — a peer of /crew, not a second planning system |

Selection rules and the discipline layer (history handling, gleaning, TTS, workspace writes) live in `AGENTS-GUIDE.md` §1 — read it once, apply always.

## 3. Hard rules (non-negotiable, all masks)
1. Workspace writes go under `cursor-agent-team/ai_workspace/` only.
2. The topic tree is modified only via `python cursor-agent-team/_scripts/validate_topic_tree.py` — never by hand.
3. Serious work products are written to files first, then summarized in chat (path pointers, not dumps).
4. Phase markers (`phase_marker.py`) and response self-verification (`verify_response.py`) are machine-checked contracts.

## 4. Relation to slash commands
Human operators keep the `/crew`, `/discuss`, ... slash commands (mid-tier path). Skills are the frontier-agent path: same six masks, self-assembled per turn instead of harness-injected.

---
<!-- Generated from commands.yaml by _scripts/build_commands.py — do not edit by hand. Edit commands.yaml and regenerate. -->

**Version**: v1.0.0 (Updated: 2026-08-30)

**Version History**:
- v1.0.0 (2026-08-30): Initial creation. Frontier-agent front door: mask-selection table, cold-start reading order, hard rules; skills become a first-class delivery vehicle alongside slash commands (v0.22.0).
