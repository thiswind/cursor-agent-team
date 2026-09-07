# AGENTS-GUIDE.md — Quick Guide for Frontier-Model Agents

> **Who this is for**: AI agents (GPT-5.x-class, Claude-Fable-class, GLM-5-class frontier models) that enter a host project "cold" — no slash-command context, no harness injection. You can self-constrain; you only need to be told **where the masks are, when to use them, and how**.
>
> **Companion doc**: `SUBAGENT-DISPATCH.md` — how an orchestrator dispatches mid-tier sub-agents wearing CAT personas.
>
> **Official support note**: reading persona files directly and following their behavioral mode — without slash-command injection — is an officially supported usage path (since v0.20.0).
>
> **Skills note (v0.22.0)**: if your host surfaces skills (`.claude/skills/`, `.trae/skills/`, or equivalent), CAT ships as 7 `SKILL.md` packages — the `cursor-agent-team` master router plus one per mask. Treat them as thin entry points: trigger self-check, then come back to this guide and the files it points at.

## 1. Persona Map

Six masks, each = one generated command file + one persistent rules file. Definitions live in the CAT copy inside the host project (path below shows the submodule layout; if installed differently, adjust the prefix):

| Mask | Role | Phases | Command def | Rules file | Core duty |
|------|------|--------|-------------|------------|-----------|
| `discuss` | Discussion Partner | 4 | `cursor-agent-team/_cursor/commands/discuss.md` | `_cursor/rules/discussion_assistant.mdc` | Explore, suggest, plan — never execute; recommend `/crew` when operations are needed |
| `crew` | Crew Member | 4 | `cursor-agent-team/_cursor/commands/crew.md` | `_cursor/rules/crew_assistant.mdc` | Execute a PLAN step-by-step as specification; auto-search on errors (max 3/step, logged); no deviation without approval |
| `workflow` | Workflow Executor | 4 | `cursor-agent-team/_cursor/commands/workflow.md` | `_cursor/rules/workflow_assistant.mdc` | Supervised parallel execution of `Executor: workflow` plans via cross-platform sub-agents; read-only subtasks by default, write-heavy work routes to `/crew`; behavior layer follows `SUBAGENT-DISPATCH.md` |
| `prompt_engineer` | Prompt Engineer | 5 | `cursor-agent-team/_cursor/commands/prompt_engineer.md` | `_cursor/rules/prompt_engineer_assistant.mdc` | Iterate LangGPT-format prompt templates with the user; strict file naming |
| `spec_translator` | Spec-Kit Translator | 5 | `cursor-agent-team/_cursor/commands/spec_translator.md` | `_cursor/rules/spec_translator_assistant.mdc` | Fully automatic PLAN → spec-kit docs conversion; zero interaction |
| `writer` | Writer (Crew + prose loop) | 4 | `cursor-agent-team/_cursor/commands/writer.md` | `crew_assistant.mdc` + `writer_assistant.mdc` (both load) | Draft → Review → Final prose loop; academic tiers; CCF-A/B/C-only citations |

**When to self-adopt which mask** (frontier-agent usage):

- Incoming request is a **question / "what should we do"** → `discuss` behavior (answer, don't touch project files; workspace notes OK)
- Incoming request is **"do it"** with an agreed plan → `crew` behavior (plan-as-spec fidelity, phase ledger, wrap-up bookkeeping)
- Large fan-out of read-only recon / batch audit / multi-branch comparison → `workflow` behavior (sub-agent dispatch per `SUBAGENT-DISPATCH.md`; write-heavy work → `/crew`)
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
- **Git policy (v0.24.0 whitelist)**: state files ARE tracked by default (`discussion_topics.md`, `plans/**`, `constraints/**`, `README.md`...); volatile zones (`temp/`, `sessions/`, `scratchpad/`, `*.bak`) and private `notes/` are excluded in the nested `.gitignore`. A host's ROOT `.gitignore` overrides this nested file. `commit_workspace.py` still asserts per-path tracked status after `add`.

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

One command (v0.24.0) — `closing_protocol.py` orchestrates the five steps,
skipping absent arguments and stopping at the first failure with a recovery
hint:

```bash
python3 _scripts/closing_protocol.py \
    --tree-file /tmp/tree_round.md \      # 1 topic-tree round (validator-gated)
    --verify-file "$RESP" \               # 2 response self-verify (with --stamp)
    --note "did X" \                      # 3 closing note (via cat_write gateway)
    --snapshot-title "Y wrap-up" \        # 4 handoff snapshot note (create-only)
    --commit-msg "chore: session close"    # 5 commit_workspace.py
```

The five steps behind it: topic tree append (via validator) → verify → deep
notes if new stack/pitfall → handoff snapshot (a dated note; the project-root
HANDOFF.md file itself is legacy since the 2026-08-31 all-hosts migration —
state SSOT is the topic tree + notes/) → commit (the sync point).

**Writes to shared state go through the gateway** (v0.24.0): notes appends,
topic-tree rounds, plan checkbox flips, INDEX rebuilds — all via
`cat_write.py` (flock-serialized, validated, atomic, journaled). Do not
Write/Edit state files directly.

**Parallel sessions**: `git log` before acting; append-only edits on shared
files (topic tree via gateway); claim files in notes/ for long tasks
(`new_scaffold.py new-session`); commit = sync point.

## 5. Deployment Topologies & Cold-Start Self-Check

> Harvested from the host-agent community ledger (2026-09, FR-0012/0013/0015/0017/0021). These are field-proven deployment practices, not requirements — adopt what matches your host's shape.

### 5.1 The three deployment shapes

| Shape | What it looks like | Watch out for |
|---|---|---|
| **Plain directory** (default) | `cursor-agent-team/` is a normal tracked dir of the host repo | The nested `.gitignore` writes `ai_workspace/**` — state files are silently skipped by plain `git add`. Use `_scripts/commit_workspace.py` or `git add -f` + post-add assertion (see §5.4) |
| **Git submodule** | `cursor-agent-team` is a gitlink (mode 160000) pinned to an upstream tag | **The state layer lives in the host's tree but the nested ignore means nothing enters the host repo by default; the submodule's own repo never receives host state** — without an explicit `add -f` policy the entire ai_workspace has zero version control (FR-0017). Always commit host-side with `add -f` |
| **Orphan pseudo-submodule** (v0.13 legacy) | A `cursor-agent-team/` dir whose gitlink was never registered in the parent index — an "orphan" that looks installed but is tracked by nobody | Cold-start self-check catches it (below). Remedy: re-install from a clean source, migrate state via the topic-tree backup, then retire the old dir via the host's deletion protocol |

### 5.2 Cold-start self-check (one command, v0.24.0)

```bash
python3 cursor-agent-team/_scripts/cat_doctor.py
```

Runs all four checks (form / version / ignore policy / orphans) and prints
one verdict; `--fleet ROOT...` audits several hosts, `--json` for scripts.
It subsumes the manual two-command check this section used to teach (VERSION
+ `git ls-files`). Orphan forms caught this way include a live v0.13 relic
surviving since January 2026 (FR-0021).

### 5.3 Field-proven host practices (from the ledger)

- **Root-level `notes/` counterexample, corrected** (FR-0012, direction fixed in v0.24.0 per DESIGN-DEPLOYDOC-003 §2.1): the ledger host deliberately kept a root-level `notes/` as a **positive pattern** — a git-tracked scratch layer adjacent to (not inside) the submodule, immune to submodule pointer resets, caught by no nested .gitignore. The earlier v0.23.0 text mis-filed it as an anti-pattern. If you adopt it: root `notes/` is host-owned state, NOT the CAT state layer — CAT notes still live under `ai_workspace/notes/`; never let cleanup scripts touch the root one, and teach cold-start readers both paths.
- **Desktop routing AGENTS.md for multi-project desks** (FR-0013): when one AGENTS.md routes several CAT hosts (e.g. a Desktop-level router), keep the router thin — one cold-start pointer per host project, zero state in the router itself; each host keeps its own tree. Three weeks field-tested.
- **Public mirror exclusion triple** (FR-0015): when the host repo is mirrored to a public remote, exclude ① `ai_workspace/` (state), ② `notes/` (may quote private material), ③ `_scripts/` local tooling — via an explicit mirror exclude list + a graded scan (exact-path match, then basename match, then content keyword) + a reverse check that the mirror 404s for those paths. Field-proven; run the triple after every mirror sync.

### 5.4 Upgrade SOP (v0.23.0+)

1. `cd <host>/cursor-agent-team && git fetch --tags && git log --oneline HEAD..v0.24.0` — read what changed (CHANGELOG first); plain-dir hosts without a git checkout: compare VERSION files
2. Re-run the cold-start self-check (§5.2) — confirm the shape is intact before touching anything
3. Update the copy: plain-dir hosts re-run the installer (idempotent, never deletes `ai_workspace/`; v0.24.0+ warns before overwriting locally-edited owned files); submodule hosts `git checkout v0.24.0` in the submodule and bump the pointer
4. Re-run `python3 _scripts/build_commands.py --check` (if harness artifacts live in the host) and the test suite once
5. Append a topic-tree round noting the version bump (validator), and commit with `commit_workspace.py` / `add -f`
6. If the host's tree predates the FR-0011 template skeleton, backfill missing structure in the same round — don't defer

- `README.md` — human-facing entry
- `SUBAGENT-DISPATCH.md` — orchestrator→sub-agent dispatch best practice (companion doc)
- `CODE_WIKI.md`-equivalent architecture docs live in the workshop repo, not the product repo
