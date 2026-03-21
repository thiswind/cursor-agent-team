# OpenClaw adapter (cursor-agent-team)

**Last updated**: 2026-03-22  

This directory contains the cross-platform installer, Skills, templates, and docs. The **full CLI** is defined by `python install.py --help`.

---

## Requirements

- **Python** 3.8+
- **OpenClaw CLI**: `openclaw` on `PATH`, version must pass checks in `install.py` (currently **≥ 2026.2.6**)
- **OS**: Windows (PowerShell), macOS, Linux; WSL optional

---

## Install (any platform)

**Prefer the root README**: full **For agents** (standard / accelerated) and **For humans** copy-paste blocks are in [**README.md**](../README.md) under **OpenClaw**. Below is a **human** command summary and platform examples.

From a clone of this repo, enter this directory:

```bash
cd cursor-agent-team/_openclaw
python install.py -y
openclaw gateway restart
```

- **Non-interactive**: `-y`; **by default** generates and non-destructively syncs `ai_workspace` into the OpenClaw workspace (required runtime workspace). To skip explicitly, add **`--no-ai-workspace`**.
- **Dry-run only**: `python install.py --dry-run --skip-openclaw-check`
- **Install does**: back up `~/.openclaw/openclaw.json`, append `skills.load.extraDirs` with the **absolute** path to this repo’s `_openclaw/skills`, and merge `AGENTS.md` / `SOUL.md` via anchor blocks (see `templates/`).

**Windows PowerShell example**

```powershell
Set-Location path\to\cursor-agent-team\_openclaw
py -3 install.py -y
openclaw gateway restart
```

Use Windows Terminal or `PYTHONIOENCODING=utf-8` if the console encoding misbehaves.

### CLI summary (canonical)

| Flag | Meaning |
|------|---------|
| `--merge` / `--apply-templates` | Merge templates (default on) |
| `--no-merge` | Only update `openclaw.json` if needed |
| `-y` | Non-interactive; **by default** syncs `ai_workspace` to the workspace (skip with `--no-ai-workspace`) |
| `--ai-workspace` | Explicitly run generate + sync (also in interactive mode; redundant with `-y` in most cases) |
| `--no-ai-workspace` | Skip `ai_workspace` generate + sync (not recommended unless you know you do not need the channel-side workspace) |
| `--force-ai-workspace` | Overwrite existing seed files in workspace `ai_workspace` when syncing (use with care) |
| `--dry-run` | No writes |
| `--skip-openclaw-check` | Skip `openclaw` checks (tests / dry-run) |

### Single source of truth: two `ai_workspace` trees

- Next to the extension: `cursor-agent-team/ai_workspace` — relative-path behavior for `preflight_check.py` is documented in the main framework docs.
- Channel-side data: **`$OPENCLAW_WORKSPACE/ai_workspace`** is authoritative for channel tools; **`install.py`** fills it via sync; it does not auto-merge with the extension copy.

### json5

If `openclaw.json` is not strict JSON, fix it or install optional **`json5`** (see installer error hints).

---

## Uninstall (essentials)

1. Edit `~/.openclaw/openclaw.json` (Windows: `%USERPROFILE%\.openclaw\openclaw.json`) and remove the entry in `skills.load.extraDirs` that points at this repo’s `_openclaw/skills`.  
2. If you no longer need the clone, delete it; if it lived under an OpenClaw extensions path, remove that copy too.  
3. `openclaw gateway restart`  
4. Install backups: `~/.openclaw/openclaw.json.backup.*` can be restored manually.

---

## Migrating from Cursor to OpenClaw (essentials)

Back up your project’s `ai_workspace`, then copy it to `$OPENCLAW_WORKSPACE/ai_workspace`; scripts and paths follow the merged `AGENTS.md`.

---

## Post-install smoke test

1. `openclaw gateway restart` if you have not already.  
2. In a channel, send `/discuss` and verify the four-phase flow (phase markers from `phase_marker.py`).  
3. If sync was skipped or you need a re-run: `python install.py -y` (includes `ai_workspace` by default; use `--no-ai-workspace` to skip).

---

## Automated tests (optional)

`cursor-agent-team/_openclaw/tests/test_install_helpers.py` — unit tests for helper functions.

---

## FAQ

**Cannot find `openclaw`?** Install OpenClaw and put the CLI on `PATH`.  

**Private repo?** You need clone access; install behavior is unchanged.
