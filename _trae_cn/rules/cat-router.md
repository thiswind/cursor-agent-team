---
name: cat-router
description: Cursor Agent Team (CAT) router — entry rule that routes work to the six role masks, scripts and ai_workspace. Applies to any repo with a cursor-agent-team/ checkout.
alwaysApply: true
---

# CAT Router (Trae CN)

This repo uses the Cursor Agent Team (CAT) framework. Rules for the six role
masks live as sibling rule files in `.trae/rules/`; activate by mask:

| Mask | Rule file | When |
|---|---|---|
| Discussion Partner | `discussion-assistant.md` | exploration, planning, topic tree |
| Crew Member | `crew-assistant.md` | plan execution |
| Writer | `writer-assistant.md` | prose compose (Draft → Review → Final) |
| Prompt Engineer | `prompt-engineer-assistant.md` | create/maintain roles |
| Spec Translator | `spec-translator-assistant.md` | spec translation |
| Workflow | `workflow-assistant.md` | workflow orchestration |

- Authoritative sources: `cursor-agent-team/_cursor/rules/*.mdc` and
  `cursor-agent-team/AGENTS-GUIDE.md`.
- State (single source of truth): `cursor-agent-team/ai_workspace/`
  (topic tree, plans, notes) — shared across Cursor / Trae CN / Claude Code.
- Skills are also installed at `.trae/skills/cursor-agent-team-*`.
