<p align="center">
  <img src="logo.png" alt="cursor-agent-team logo" width="140">
</p>

<h1 align="center">cursor-agent-team</h1>

<p align="center">
  <b>The multi-role AI team your agent runs itself.</b><br>
  One model · one conversation · six role masks · zero cold handoffs.
</p>

<p align="center">
  <img src="banner.jpg" alt="cursor-agent-team — hexagonal command hub, orbiting agent pods, holographic mission control" width="760">
</p>

<p align="center">
  &nbsp; <b>Cursor</b> · <b>Claude Code</b> · <b>TRAE SOLO</b>
</p>

---

## A new era: agents that self-assemble — and self-discipline

cursor-agent-team (CAT) began as a set of slash commands that let one AI assistant wear
different role masks inside a single conversation. With **v0.22.0** the center of gravity
shifted: **the primary user is no longer the human typing commands — it is the frontier
agent itself.** With **v0.24.0** the next shift landed: every state write passes through a
script-enforced gateway, and every wrap-up follows a machine-checked closing protocol.
With **v0.25.0** self-discipline became verifiable: mechanism markers turn "I read the
document carefully" and "I wrote with viewpoint discipline" into archives a script can
audit — gates, ledgers, convergence lines. With **v0.28.0** the discipline is airtight:
archives must prove they landed on disk (`LANDED:` read-back proof), phase markers have
exactly one valid path, and the installer finally honors `--ide` for all three platforms.

Modern frontier models enter a project cold, read the docs, and self-constrain. For them
CAT is not a command palette but an **operating discipline**: where the masks live, when
to adopt which one, how to dispatch sub-agents, and which machine-checked contracts to
honor — all readable directly from two files, no harness injection required. And since
v0.22.0 that discipline ships as **installable skills**: the same six masks, packaged so a
skill-aware host surfaces them in the agent's skill list every turn — the agent invokes
CAT itself, no human keystroke required.

> Humans are still first-class citizens: every slash command remains fully supported.
> But if your assistant is a frontier model, you may never need to type one again.

---

## For frontier agents (primary path)

Drop CAT into your project, install the skills, and the agent picks it up on its own:

```text
Read cursor-agent-team/AGENTS-GUIDE.md and adopt the role mask that fits this request.
Use cursor-agent-team/ai_workspace/ for all workspace writes.
```

That single instruction unlocks the full architecture:

| Capability | Entry point | What the agent gains |
|------------|-------------|---------------------|
| **Landing self-check** (new in v0.28.0) | archive `LANDED:` proof line | The agent re-reads its archive from disk before declaring done — a response that *claims* a file exists without the read-back proof is an invalid response; chat claims of "written" are banned |
| **Marker protocol v2** (new in v0.25.0) | `WRITE-GATE:` / `READ-GATE:` + ledgers | Machine-checkable mechanism markers: viewpoint×round ledgers, convergence lines (`CONVERGED: R<N>`), `verify_mechanism.py` audits the archive structure — verified discipline, not claimed discipline |
| **Unified `--ide` installer** (fixed in v0.28.0) | `install.py --ide claude_code\|trae_solo` | One entry point, three platforms; invalid values fail fast (exit 2) instead of silently installing Cursor |
| **Write gateway** (since v0.24.0) | `_scripts/cat_write.py` | All state writes go through one script: global flock queue, atomic landing, journaled ops — the model never edits state files by hand |
| **Operation skills** (since v0.24.0) | `writes` · `closing` · `doctor` · `dispatch` | HOW-to-act skills, orthogonal to masks: how to write state, how to wrap up, how to health-check, how to dispatch |
| **Closing protocol** (since v0.24.0) | `_scripts/closing_protocol.py` | One command, five steps — tree verify, response verify, wrap-up note, snapshot, commit — stop at first failure |
| **Machine-checked contracts** | `_scripts/` | Phase markers (exactly-one-path rule), `verify_response.py` self-verification, `verify_mechanism.py` archive audits, topic-tree validator, scratchpad & leak guards |
| **Installable mask skills** (since v0.22.0) | `_skills/` → `.claude/skills/` / `.trae/skills/` | The six masks plus a master router, auto-discovered by skill-aware hosts every turn; agent self-invokes CAT |
| **Self-assembled masks** | [`AGENTS-GUIDE.md`](AGENTS-GUIDE.md) | Picks any of the six personas cold — no slash commands, no injection; includes a "which mask when" decision list |
| **Sub-agent dispatch** | [`SUBAGENT-DISPATCH.md`](SUBAGENT-DISPATCH.md) | Fans out mid-tier sub-agents with structured prompts, mask-based constraints, trust-but-verify acceptance |
| **Externalized cognition** | `ai_workspace/` | Durable topic tree, plans, notes, scratchpad — working memory beyond the context window |

### The write gateway: discipline by construction (since v0.24.0)

Prompts constrain softly; scripts constrain hard. The gateway moves every state mutation
behind one executable door:

- **Global flock** — one writer at a time, kernel-managed queue, no model-side politeness needed
- **Atomic landing** — temp file + `os.replace`, a crash can never leave a half-written tree
- **Journaled ops** — every operation appends to a monthly JSONL journal: who, what, when
- **Whitelisted operations** — notes append, topic round, plan status, index rebuild; anything else is rejected

Pair it with the four **operation skills** and the agent gets a complete HOW-layer:
`/cat-writes` for state writes, `/cat-closing` for the five-step wrap-up,
`/cat-doctor` for deployment health checks, `/cat-dispatch` for sub-agent discipline.

### Verified discipline: markers, ledgers, landing proof (v0.25.0 → v0.28.0)

Soft instructions say "be disciplined"; CAT's marker protocol makes discipline auditable:

- **`WRITE-GATE:` / `READ-GATE:`** — the writer opens every task by declaring whether
  viewpoint-round deliberation applies, and traces both paths. Skipping without a traced
  reason is an invalid archive.
- **Increment ledgers** — viewpoint×round entries (`[轮N·Vi]`) for writing, source-anchored
  two-layer scans for long-document reading; every round must show increment or explicitly
  record none.
- **Convergence lines** — `CONVERGED: R<N>` (N ≥ 2) or `BUDGET: R<N>(reason)`; a
  single-round stop is banned. `verify_mechanism.py` machine-checks gate, ledger depth,
  and convergence.
- **`LANDED:` read-back proof** — before declaring an archive complete, the agent re-reads
  it *from disk* (not from its own response) and appends a proof line. This kills the
  classic failure mode — a response that reports a complete archive while the file never
  landed because the Write tool was never invoked — which acceptance runs measured at an
  80% recurrence rate before the fix.

### Skills: the per-turn handle

Slash commands are the mid-tier handle — a human must remember and type them. Skills are
the frontier-agent handle: **install once, and the host surfaces CAT in the agent's skill
list on every turn.** The mask skills carry YAML frontmatter (name + trigger-rich
description) so any frontmatter-discovering host — Claude Code, TRAE, or future ones —
can list them without configuration. Install paths: `install_claude_code.py` →
`.claude/skills/`, `install_trae_solo.py` → `.trae/skills/`. A guard clause in every
skill keeps the agent silent when `cursor-agent-team/` is absent, so a stray skill in
the wrong repo degrades to a one-line notice instead of misfiring.

---

## Architecture

<p align="center">
  <img src="architecture.png" alt="cursor-agent-team architecture — dual entry paths, shared-context meeting room, supervised sub-agent fan-out" width="780">
</p>

**Two ways in, one meeting room.** A frontier agent (primary, cyan) and a human operator
(secondary, gray dashed) reach the same place: one model in one shared conversation wearing
role masks. When a plan calls for parallel work, the meeting room fans out read-only
sub-agents (violet), verifies their structured returns, and merges only the summaries —
the shared-context core never fragments. Everything lands in `ai_workspace/` through the
write gateway (global flock, atomic landing, JSONL journal), above a floor of
machine-checked contracts that are always in effect: phase markers, response
self-verification, mechanism-ledger audits, leak guards.

---

## For humans (secondary path)

All slash commands remain fully supported across Cursor, Claude Code, and TRAE SOLO:

| Role | Command | Purpose |
|------|---------|-------|
| Discussion Partner | `/discuss` | Explore ideas, clarify requirements, generate plans |
| Crew Member | `/crew` | Execute agreed plans strictly, step by step |
| Workflow Executor | `/workflow` (alias `/ultra`) | Supervised parallel execution via cross-platform sub-agents |
| Writer | `/writer` | Prose with Draft → Review → Final quality control |
| Prompt Engineer | `/prompt_engineer` | Create or maintain prompts, commands, new masks |
| Spec Translator | `/spec_translator` | Convert plans into spec-kit documents |

Because every mask lives in the same conversation, `/crew` already knows what `/discuss`
planned — no context handoff, no re-explaining.

---

## Quick start

```bash
# 1. Add as submodule inside your project
git submodule add https://github.com/thiswind/cursor-agent-team.git cursor-agent-team

# 2. Install for your platform
python3 cursor-agent-team/install.py                        # Cursor
python3 cursor-agent-team/install.py --ide claude_code      # Claude Code (dispatches; also installs skills → .claude/skills/)
python3 cursor-agent-team/install.py --ide trae_solo        # TRAE SOLO (dispatches; also installs skills → .trae/skills/)
# Dedicated entrypoints still work: install_claude_code.py / install_trae_solo.py

# 3a. On a skill-aware host the agent now sees CAT in its skill list   ← zero-keystroke
# 3b. Or point your frontier agent at AGENTS-GUIDE.md                  ← manual but universal
# 3c. Or type /discuss and start                                       ← classic
```

Or just tell your agent:

```text
Install cursor-agent-team into this project as a git submodule at cursor-agent-team/,
run the installer for my platform, then read cursor-agent-team/AGENTS-GUIDE.md.
```

---

## Why one conversation beats agent swarms

Every time one agent hands off to another, the receiving agent starts cold — it only knows
what you explicitly passed. Context bleeds, constrain softly, plans drift, you re-explain
yourself.

CAT keeps one model in one shared conversation and switches role masks instead. Switching
from planning to execution to prompt engineering loses nothing, because everyone in the
"meeting room" was there for the whole discussion. Parallelism is added only where it is
safe: supervised, read-only sub-agents that return structured summaries for verification.
Since v0.24.0 the meeting room has a bouncer — the write gateway guarantees every state
mutation is queued, atomic, and journaled. Since v0.25.0 the room takes minutes: mechanism
ledgers and convergence lines make the deliberation itself auditable, and since v0.28.0
every archive must prove it landed on disk before anyone calls it done.

---

## Features

- **Archive landing self-check** (new in v0.28.0) — `LANDED:` read-back proof: re-read the archive from disk before declaring done; claimed-but-never-written archives are invalid
- **Marker protocol v2** (new in v0.25.0) — `WRITE-GATE:` / `READ-GATE:`, viewpoint×round increment ledgers, convergence lines, `verify_mechanism.py` closed-loop audit
- **Phase-marker exactly-one-path rule** (since v0.25.1) — the marker must exist at every join point: script-produced OR hand-typed canonical line; explaining the constraint without the marker is invalid
- **Unified `--ide` installer + auto-detect uninstall** (v0.28.0) — `install.py --ide claude_code|trae_solo` dispatches correctly and fails fast on typos; bare `uninstall.py` auto-detects the single installation and errors on ambiguity
- **Script-enforced write gateway** (since v0.24.0) — global flock, atomic landing, JSONL journal; the model never edits state files directly
- **Operation skills** (since v0.24.0) — `writes` / `closing` / `doctor` / `dispatch`: the HOW-layer, orthogonal to the six role masks
- **One-command closing protocol** (since v0.24.0) — tree → verify → note → snapshot → commit, stop at first failure
- **Deployment doctor** (since v0.24.0) — form / version / ignore-policy / orphan checks, `--fleet` for multi-host audits
- **Whitelist state tracking** (since v0.24.0) — state files tracked by default, volatile zones excluded; hosts override via root `.gitignore`
- **Installable frontier-agent skills** (since v0.22.0) — the six masks plus a master routing skill as host-agnostic SKILL.md packages
- **Frontier-agent self-assembly** — `AGENTS-GUIDE.md`: advanced agents enter cold, pick a role mask themselves (officially supported since v0.20.0)
- **Supervised sub-agent dispatch** — `SUBAGENT-DISPATCH.md`: orchestrator-grade fan-out with trust-but-verify acceptance
- **Cross-platform parallel execution** — `/workflow` fans out read-only sub-tasks to native background agents; serial downgrade on older IDEs
- **Single conversation, multiple masks** — role switching without handoff or context loss
- **Shared AI workspace** — durable plans, notes, topic tree, scratchpad in `cursor-agent-team/ai_workspace/`
- **Script-backed constraints** — Python scripts for preflight, phase markers, topic-tree validation, workspace generation
- **Closed-loop verification** — `verify_response.py` machine-checks every response: phase markers, scratchpad freshness, leakage guard, stamps
- **Single-source commands** — all role commands generated from `commands.yaml`; `--check` gates drift in CI
- **Human-in-the-loop** — discussion, planning, execution stay under user control
- **Platform adapters** — Cursor, Claude Code, TRAE SOLO share one methodology
- **Optional extensions** — persona output, inspiration cards, TTS helpers, spec-kit translation

---

## Maintaining commands (single source)

Never hand-edit `_cursor/commands/`, `_claude/commands/`, or `_trae_solo/` artifacts:

```bash
python3 _scripts/build_commands.py         # regenerate all platform artifacts
python3 _scripts/build_commands.py --check # verify no drift (use in CI)
```

Generated commands embed the phase-marker and response self-verification contracts, so
every platform gets them for free.

---

## Installation

### Let an agent install it

```text
Install cursor-agent-team into this project as a git submodule at cursor-agent-team/,
then run the platform installer for my environment.

Use:
- Cursor: python3 cursor-agent-team/install.py
- Claude Code: python3 cursor-agent-team/install_claude_code.py
- TRAE SOLO: python3 cursor-agent-team/install_trae_solo.py
```

### Manual install / update / uninstall

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
python3 cursor-agent-team/install.py              # or install_claude_code.py / install_trae_solo.py

git submodule update --remote cursor-agent-team   # update, then re-run installer
python3 cursor-agent-team/uninstall.py --platform cursor   # or claude_code / trae_solo
```

| Platform | Installer | What gets installed |
|----------|-----------|---------------------|
| Cursor | `install.py` (or `--ide cursor`) | `.cursor/commands/` and `.cursor/rules/` |
| Claude Code | `install.py --ide claude_code` (or `install_claude_code.py`) | `.claude/commands/` mask commands, `.claude/rules/` Writer rules, and skills → `.claude/skills/` |
| TRAE SOLO | `install.py --ide trae_solo` (or `install_trae_solo.py`) | `.trae/skills/` including Writer and an `AGENTS.md` template only when absent |

On Windows, use `py -3` instead of `python3`. Uninstall: `python3 uninstall.py`
auto-detects the only installed platform; with several installed it errors and
lists them — pass `--platform cursor|claude_code|trae_solo` explicitly.
Uninstall is recorded-file-only and safe for user-owned files; the submodule
remains unless `--remove-submodule` is passed. See
[DEPLOYMENT.md](DEPLOYMENT.md) for shapes, tracking policies, and upgrade SOPs.

---

## Version

Current version: **v0.28.0** — see [CHANGELOG.md](CHANGELOG.md).

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).

## Author

**thiswind** — [@thiswind](https://github.com/thiswind)
