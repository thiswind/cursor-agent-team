# Spec Translator Workspace

Workspace for `/spec_translator` command. Path: `cursor-agent-team/ai_workspace/spec_translator/`

---

## Quick Reference

| What | Path | Format |
|------|------|--------|
| Session | `sessions/` | `session_YYYYMMDD_HHMMSS/` |
| Constitution | `../` (ai_workspace root) | `spec-kit-constitution-[TopicID]-[Seq].md` |
| Specify | `../` (ai_workspace root) | `spec-kit-specify-[TopicID]-[Seq].md` |
| Plan | `../` (ai_workspace root) | `spec-kit-plan-[TopicID]-[Seq].md` |

---

## NEVER DO

- NEVER convert non-software-development plans
- NEVER save Spec-Kit documents in this directory (save to ai_workspace root)
- NEVER delete this README

---

## Workflow

1. Read plan from `../plans/PLAN-*.md`
2. Validate: Is it a software development task?
3. Convert to three Spec-Kit documents
4. Save to `../` (ai_workspace root)
5. Update `../discussion_topics.md`

---

## Output Documents

| Document | Purpose |
|----------|---------|
| `spec-kit-constitution-*.md` | Project principles and development guidelines |
| `spec-kit-specify-*.md` | Requirements specification |
| `spec-kit-plan-*.md` | Technical implementation plan |

---

## Cleanup

- Retention: 7 days for sessions
- Spec-Kit documents: Keep as long as needed

---

**Last Updated**: 2026-02-02
