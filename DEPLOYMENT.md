# DEPLOYMENT.md — CAT Deployment Guide

> How cursor-agent-team (CAT) actually lands in host repos: the shapes it
> takes, the policies that govern its state layer, and the health checks
> that keep it honest. Companion to `AGENTS-GUIDE.md` (personas & session
> patterns) — this file is about **where CAT lives and how it tracks**.

## 1. The three deployment shapes

| Shape | What it looks like | Watch out for |
|---|---|---|
| **Plain directory** (workshop shape) | `cursor-agent-team/` is a normal tracked dir of the host repo | Simplest and most robust; state files commit directly to the host repo |
| **Git submodule** | `cursor-agent-team` is a gitlink (mode 160000) pinned to an upstream tag | State lives in the host's tree but the submodule's own repo never receives host state — commit host-side (the v0.24.0 whitelist makes plain `git add` work) |
| **Orphan pseudo-submodule** (v0.13 legacy) | A `cursor-agent-team/` dir whose gitlink was never registered in the parent index | Looks installed, tracked by nobody; one cleanup pass can erase it. Detected by `cat_doctor.py`; remedy: re-install clean, migrate state via topic-tree backup, retire the old dir |

Detect yours: `python3 cursor-agent-team/_scripts/cat_doctor.py` (first
line of output is the form).

## 2. State-layer tracking policy (v0.24.0 whitelist)

The nested `cursor-agent-team/.gitignore` uses a **whitelist policy**:
state files ARE tracked by default; volatile and private zones are
excluded:

| Zone | Tracked? | Why |
|---|---|---|
| `discussion_topics.md`, `plans/**`, `constraints/**`, workspace `README.md` | ✅ yes | The cross-session memory — this IS the point of CAT |
| `notes/` | ❌ excluded by default | May quote private material (FR-0015); private-repo hosts may delete that one line to opt in |
| `temp/`, `sessions/`, `scratchpad/`, `*.bak`, `*.log` | ❌ excluded | Volatile / regenerable |
| `inspiration_capital/cards/**` | ❌ excluded | User-generated content |

Two governing rules:
1. **The host's ROOT `.gitignore` overrides this nested file** — hosts can
   tighten or loosen per-host without touching the product.
2. Breaking-change note (v0.23.0 → v0.24.0): legacy installs shipped
   `ai_workspace/**` (ignore-everything). After upgrading, previously
   ignored state files become addable — run `cat_doctor.py`; if it reports
   `policy=legacy-ignore-all`, replace the nested `.gitignore` with the
   v0.24.0 one (the installer does this on re-run), then `git add` the
   state layer and commit with `_scripts/commit_workspace.py` (it asserts
   every intended path actually entered the index).

## 3. Installers per platform

| Platform | Installer | Installs |
|---|---|---|
| Cursor | `install.py` | `.cursor/commands/*.md` + `.cursor/rules/*.mdc` |
| Claude Code | `install_claude_code.py` | `.claude/commands/*.md` |
| TRAE SOLO | `install_trae_solo.py` | `_trae_solo/` harness + skills |

All installers are **idempotent** (re-run safely), never delete
`ai_workspace/`, and since v0.24.0 warn before overwriting installer-owned
files that have local edits (ownership recorded with md5 in the install
record).

The skills under `_skills/` are **statically distributed** — hosts on
skill-aware harnesses (Claude Code / TRAE plugin / others) can register
them directly; the installers remain for command-file harnesses.

## 4. Cold-start self-check

```bash
python3 cursor-agent-team/_scripts/cat_doctor.py
# or across a fleet of host repos:
python3 cursor-agent-team/_scripts/cat_doctor.py --fleet /path/hostA /path/hostB
```

Four checks: **form** (which shape), **version** (VERSION file vs git
tag, dirty tree), **ignore** (is the state layer actually tracked; which
policy), **orphans** (gitlink mismatches, v0.13 relics). Exit 1 on
critical items — treat those as blockers.

## 5. Field-proven host practices

Harvested from the host-agent community ledger (2026-09):

- **Root-level `notes/` as a deliberate second layer** (FR-0012): a
  git-tracked scratch layer at the host root, adjacent to (not inside)
  the submodule — immune to submodule pointer resets and to the nested
  .gitignore. If adopted: root `notes/` is host-owned, NOT the CAT state
  layer; CAT notes still live under `ai_workspace/notes/`; keep cleanup
  scripts away from the root one; teach cold-start readers both paths.
- **Desktop routing AGENTS.md for multi-project desks** (FR-0013): one
  thin router AGENTS.md for several CAT hosts — one cold-start pointer
  per host, zero state in the router; each host keeps its own tree.
  Three weeks field-tested.
- **Public mirror exclusion triple** (FR-0015): hosts mirrored to public
  remotes exclude ① `ai_workspace/` (state), ② `notes/` (private
  quotes), ③ local tooling — via an explicit exclude list + graded scan
  (exact-path → basename → content keyword) + a reverse 404 check. Run
  after every mirror sync.
- **Submodule state visibility** (FR-0017): in submodule shape the state
  layer's ONLY version control is host-side commits; the upstream repo
  never sees host state. Budget review attention accordingly.

## 6. Upgrade SOP (v0.24.0+)

1. `cd <host>/cursor-agent-team && git fetch --tags && git log --oneline HEAD..v0.24.0`
   (plain-dir hosts without git: diff `VERSION` files) — read CHANGELOG first
2. `cat_doctor.py` — confirm the shape is intact before touching anything
3. Update: plain-dir hosts re-run the installer (idempotent; warns before
   overwriting local edits); submodule hosts `git checkout v0.24.0` and
   bump the pointer
4. If the ignore policy is `legacy-ignore-all`: adopt the v0.24.0
   whitelist (installer re-run replaces the nested `.gitignore`), then
   `git add` the state layer + `commit_workspace.py`
5. Re-run `build_commands.py --check` (if harness artifacts live in the
   host) and the test suite once
6. Append a topic-tree round noting the bump (via `cat_write.py
   topic-round`), commit

## 7. Concurrent sessions on one host

v0.24.0 introduces the **single write gateway** (`cat_write.py`):
flock-serialized, per-target validation (topic tree goes through the
R1–R6 validator), atomic landing (`temp` + `os.replace` — readers never
see half-written files), and a JSONL journal under
`ai_workspace/temp/cat_write_journal/` that makes every write auditable
(`cat_write.py journal --tail`, `lock-wait-report`).

Rules of thumb:
- Reads are always safe; writes always go through the gateway
- Parallel agents get **disjoint file boundaries** (state them in the
  dispatch prompt — `dispatch_header.py --boundary`)
- Response temp files are **session-scoped** (`$CAT_SESSION_ID` or `$$`),
  never one shared `response_last.md`

## 8. Uninstall

`uninstall.py` removes installed command/rule files and the install
record; `ai_workspace/` is never touched. Orphaned dirs (v0.13 class)
should be retired via the host's deletion protocol after state migration.
