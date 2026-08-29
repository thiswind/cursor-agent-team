# AGENTS-GUIDE.md — Quick Guide for Frontier-Model Agents

> **Who this is for**: AI agents (GPT-5.x-class, Claude-Fable-class, GLM-5-class frontier models) that enter a host project "cold" — no slash-command context, no harness injection. You can self-constrain; you only need to be told **where the masks are, when to use them, and how**.
>
> **Companion doc**: `SUBAGENT-DISPATCH.md` — how an orchestrator dispatches mid-tier sub-agents wearing CAT personas.
>
> **Official support note**: reading persona files directly and following their behavioral mode — without slash-command injection — is an officially supported usage path (since v0.20.0).

## 1. Persona Map

Five masks, each = one generated command file + one persistent rules file. Definitions live in the CAT copy inside the host project (path below shows the submodule layout; if installed differently, adjust the prefix):

| Mask | Role | Phases | Command def | Rules file | Core duty |
|------|------|--------|-------------|------------|-----------|
| `discuss` | Discussion Partner | 4 | `cursor-agent-team/_cursor/commands/discuss.md` | `_cursor/rules/discussion_assistant.mdc` | Explore, suggest, plan — never execute; recommend `/crew` when operations are needed |
| `crew` | Crew Member | 4 | `cursor-agent-team/_cursor/commands/crew.md` | `_cursor/rules/crew_assistant.mdc` | Execute a PLAN step-by-step as specification; auto-search on errors (max 3/step, logged); no deviation without approval |
| `prompt_engineer` | Prompt Engineer | 5 | `cursor-agent-team/_cursor/commands/prompt_engineer.md` | `_cursor/rules/prompt_engineer_assistant.mdc` | Iterate LangGPT-format prompt templates with the user; strict file naming |
| `spec_translator` | Spec-Kit Translator | 5 | `cursor-agent-team/_cursor/commands/spec_translator.md` | `_cursor/rules/spec_translator_assistant.mdc` | Fully automatic PLAN → spec-kit docs conversion; zero interaction |
| `writer` | Writer (Crew + prose loop) | 4 | `cursor-agent-team/_cursor/commands/writer.md` | `crew_assistant.mdc` + `writer_assistant.mdc` (both load) | Draft → Review → Final prose loop; academic tiers; CCF-A/B/C-only citations |

**When to self-adopt which mask** (frontier-agent usage):

- Incoming request is a **question / "what should we do"** → `discuss` behavior (answer, don't touch project files; workspace notes OK)
- Incoming request is **"do it"** with an agreed plan → `crew` behavior (plan-as-spec fidelity, phase ledger, wrap-up bookkeeping)
- Long prose deliverable → `writer` behavior (compose loop + anti-AI-slop constraints)
- Prompt/role engineering task → `prompt_engineer` behavior
- PLAN → spec-kit conversion → `spec_translator` behavior

**Discipline layer — always in effect, for every mask** (read once, apply always): `history_context_handler.mdc` (strip persona styling from history; keep technical facts), `gleaning.mdc` (post-work inspiration cards), `tts_speech_rules.mdc` (speak only on explicit request), `social_media_policy.mdc` (rules override persona on public networks), plus optional `persona_input_layer.mdc` / `persona_output_layer.mdc` / `wandering.mdc` / `persona_definition.mdc`.

**Key hard rules common to all masks**:

1. Workspace writes go under `cursor-agent-team/ai_workspace/` — never scatter temp files elsewhere.
2. The topic tree (`ai_workspace/discussion_topics.md`) is modified **only** via `validate_topic_tree.py update` — never by hand.
3. Serious work products are written to files first, then summarized in chat (path pointers, not dumps).
4. Phase markers (`[Phase N DONE]`) and the response self-verification loop are machine-checked contracts — honor them in long-form responses.

## 2. Scripts Reference

All scripts live under `cursor-agent-team/_scripts/` (stdlib-only unless noted; run with the host's Python ≥3.10; `conda activate base` on this machine).

### Generation & verification spine

| Script | Purpose | Invoke | Side effects |
|--------|---------|--------|--------------|
| `build_commands.py` | Regenerate all platform command artifacts from `commands.yaml` (single source) | `python3 _scripts/build_commands.py`; `--check` (CI drift gate) | Writes `_cursor/ _claude/ _trae_solo/` artifacts; `--check` read-only. **Needs PyYAML** |
| `verify_response.py` | Verify a saved response contains all phase markers, in order, unique | `--phases N --file response.md` / `--stdin` / `--json` | Read-only; imports `build_marker` from `phase_marker.py` |
| `phase_marker.py` | Emit canonical `[Phase N DONE]` line | `python3 phase_marker.py <N> true` | Read-only stdout |

### Workspace state guardians

| Script | Purpose | Invoke | Side effects |
|--------|---------|--------|--------------|
| `validate_topic_tree.py` | R1–R4 rules + one-step update + auto-archive | `validate --old A --new B`; `update --stdin` (+`--dry-run`) | `update` writes topic tree + temp backup; auto-archives retired topics |
| `update_plan_status.py` | PLAN status/INDEX bookkeeping | `update_plan_status.py PLAN-B-001 --status completed` | Writes plan file + INDEX.md |
| `generate_ai_workspace.py` | Install-time workspace scaffolding | (no flags) / `--force` (dangerous) | Writes `ai_workspace/` — non-destructive by default (READMEs/templates refreshed, user history preserved) |
| `cleanup_ai_workspace.py` | Safe deletion inside workspace | `--pattern x --older-than 7` + `--dry-run` | Deletes (protected list enforced); **logs to `temp/cleanup.log` even in dry-run** |
| `cleanup_topic_tree_temp.py` | Whitelist cleanup of validation temps | (no flags) / `--dry-run` | Deletes whitelisted temp files only |

### Boot & persona

| Script | Purpose | Invoke | Side effects |
|--------|---------|--------|--------------|
| `preflight_check.py` | Session bootstrap status (<10 lines) | (no flags) | Read-only |
| `persona_output.py` | Persona styling at output stage | (prompt format) / `--check` / `--json` | Read-only; PyYAML optional (degrades gracefully) |
| `role_identity/*.py` | Role declaration lines | `python3 role_identity/crew.py` | Read-only stdout |
| `tts_speak.py` | macOS `say` wrapper | `tts_speak.py "text"` / `--check` | Audio; writes capability cache |
| `inspiration_capital`: `create_card.py` / `draw_cards.py` | Scatter-card bank | `create_card.py --source X --trigger Y`; `draw_cards.py --count 3` | create writes card file; draw read-only |

## 3. ai_workspace Usage

The workspace is CAT's core architectural bet: agent cognition externalized to disk (scratchpad reasoning, external memory beyond the context window, staged generation). Treat it as your working memory, not a log dumping ground.

### Directory semantics

| Path (under `ai_workspace/`) | What it is | Discipline |
|------------------------------|------------|------------|
| `discussion_topics.md` | Timeline SSOT (topic tree) | Append-only; changes only via `validate_topic_tree.py`; R1: topic IDs never deleted |
| `plans/` (`PLAN-*.md` + INDEX.md) | Unexecuted schemes, ledger-style | Append-only; status via `update_plan_status.py` |
| `scratchpad/` | Pre-speech thinking (drafts/analysis/scripts/figures/temp/research subdirs) | Disposable; process never leaks into chat |
| `notes/` | Deep notes `note_*.md` | The top-level `notes/` is legacy; canonical notes live in `scratchpad/notes/` — prefer the scratchpad location |
| `inspiration_capital/cards/` | Scatter-card creativity bank | Flat, no categories, append-only |
| `sessions dirs` (`crew/` `prompt_engineer/` `spec_translator/`) | Per-mask session snapshots | Ephemeral; 7-day retention |
| `topic_archives/` | Retired topics (auto-archived by validator) | Write-once |
| `temp/` | Validation temps, cleanup log | Disposable |

### Write discipline

- **notes vs plans split**: notes = technical facts that happened; plans = schemes not yet executed. Same event can produce both, in different voices.
- **Topic tree edits**: always `validate_topic_tree.py update --stdin`; `--old` for preservation checks should come from `git show HEAD:<path>`, never /dev/null.
- **Git policy**: `ai_workspace/**` is git-ignored by default in the product; only `inspiration_capital/scripts/` is tracked. In host projects where workspace files are already tracked, new files may need `git add -f` (host-side convention — follow the host's HANDOFF/AGENTS docs when they conflict with product defaults).

### Known pitfalls (machine-verified)

- **LS-type tools can drop content on large directories** — cross-check with `ls -l -t` / `tree` before concluding a dir is empty.
- **R2 false positives on Chinese words** containing "略" (e.g. "策略") trip the ellipsis check — avoid such words in topic-tree text.
- **Dry-run still logs**: both cleanup scripts append to `temp/cleanup.log` even with `--dry-run`.
- **Protected files** (never delete): workspace READMEs, topic tree, plans/INDEX.md — enforced by `cleanup_ai_workspace.py`.

## 4. Session Handoff Pattern

Cross-session state survives via disk, not memory. The handoff contract has two halves:

### Project-root HANDOFF.md (five sections)

1. 30-second project overview
2. Cold-start checklist (ordered file list to read)
3. SSOT layering table (what lives where)
4. Parallel-session conventions
5. Current status snapshot

### Closing protocol (end of every significant session)

```
topic tree append (via validator) → verify → deep notes if new stack/pitfall →
HANDOFF snapshot refresh → commit (the sync point)
```

**Parallel sessions**: `git log` before acting; append-only edits on shared files (topic tree / HANDOFF.md); claim files in notes/ for long tasks; commit = sync point.

## Relation

- `README.md` — human-facing entry
- `SUBAGENT-DISPATCH.md` — orchestrator→sub-agent dispatch best practice (companion doc)
- `CODE_WIKI.md`-equivalent architecture docs live in the workshop repo, not the product repo
