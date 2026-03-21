#!/usr/bin/env python3
"""
cursor-agent-team OpenClaw adapter installer (cross-platform).

Resolves extension root from this script location (repository checkout).
Uses pathlib/shutil only; no cp/ln required for users.

Version: v2.0.0 (PLAN-OC-001)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional, Tuple

# --- Markers (must match PLAN-OC-001) ---
AGENTS_START = "<!-- cursor-agent-team:adapter:start -->"
AGENTS_END = "<!-- cursor-agent-team:adapter:end -->"
SOUL_START = "<!-- cursor-agent-team:soul-adapter:start -->"
SOUL_END = "<!-- cursor-agent-team:soul-adapter:end -->"
PLACEHOLDER = "{{CURSOR_AGENT_TEAM_EXTENSION_ROOT}}"

REQUIRED_OPENCLAW_SEMVER = (2026, 2, 6)


def repo_root() -> Path:
    """cursor-agent-team/ (parent of _openclaw/)."""
    return Path(__file__).resolve().parent.parent


def use_ascii_stdout() -> bool:
    """Prefer ASCII log lines on legacy Windows consoles (PLAN 1.9)."""
    enc = getattr(sys.stdout, "encoding", None) or ""
    return enc.upper() in ("CP437", "CP1252", "ASCII", "US-ASCII")


def log_ok(msg: str, ascii_mode: bool) -> None:
    print(f"[OK] {msg}" if ascii_mode else f"[OK] {msg}")


def log_info(msg: str, ascii_mode: bool) -> None:
    print(f"[INFO] {msg}" if ascii_mode else f"[INFO] {msg}")


def log_warn(msg: str, ascii_mode: bool) -> None:
    print(f"[WARN] {msg}" if ascii_mode else f"[WARN] {msg}")


def log_err(msg: str) -> None:
    print(f"[ERR] {msg}", file=sys.stderr)
    sys.exit(1)


def apply_placeholders(text: str, extension_root: Path) -> str:
    root_s = str(extension_root.resolve())
    return text.replace(PLACEHOLDER, root_s)


def parse_openclaw_version(stdout: str) -> Optional[Tuple[int, int, int]]:
    """
    Defensive semver extraction (PLAN 1.5): take first X.Y.Z in output.
    """
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", stdout)
    if not m:
        return None
    return tuple(int(m.group(i)) for i in range(1, 4))


def version_ok(found: Tuple[int, int, int], required: Tuple[int, int, int]) -> bool:
    return found >= required


def load_json_config(path: Path) -> Any:
    """
    Load JSON. If invalid, try optional json5 (PLAN 1.6).
    """
    raw = path.read_text(encoding="utf-8")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        try:
            import json5  # type: ignore

            return json5.loads(raw)
        except ImportError:
            log_err(
                f"Invalid JSON in {path} and 'json5' not installed. "
                f"Fix JSON or: pip install json5. Underlying error: {e}"
            )
        except Exception as e2:
            log_err(f"Failed to parse config {path}: {e2}")


def merge_block_into_file(
    target: Path,
    template_body: str,
    start_m: str,
    end_m: str,
    dry_run: bool,
) -> str:
    """
    Idempotent merge: replace inside markers, or append block, or create file.
    Returns human-readable action name.
    """
    block_inner = template_body.rstrip()
    block = f"{start_m}\n{block_inner}\n{end_m}\n"

    if not target.exists():
        action = "create"
        new_content = block
    else:
        text = target.read_text(encoding="utf-8")
        if start_m in text and end_m in text:
            pattern = re.compile(
                re.escape(start_m) + r"(.*?)" + re.escape(end_m), re.DOTALL
            )

            def repl(_m: re.Match[str]) -> str:
                return f"{start_m}\n{block_inner}\n{end_m}"

            new_content, n = pattern.subn(repl, text, count=1)
            if n == 0:
                new_content = text.rstrip() + "\n\n" + block
                action = "append_block"
            else:
                action = "replace_block"
        else:
            new_content = text.rstrip() + "\n\n" + block
            action = "append_block"

    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_content, encoding="utf-8")
    return action


def mirror_ai_workspace_nondestructive(
    src_root: Path,
    dest_root: Path,
    dry_run: bool,
    force: bool,
    log: Callable[[str], None],
) -> None:
    """
    Only create missing dirs; copy file only if dest missing or --force-ai-workspace (PLAN 1.7).
    """
    if not src_root.is_dir():
        return
    for path in sorted(src_root.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(src_root)
        dest = dest_root / rel
        if dest.exists() and not force:
            continue
        log(f"ai_workspace seed: {rel}")
        if dry_run:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def ensure_extra_dirs(
    config: dict,
    skills_abs: str,
    dry_run: bool,
) -> bool:
    """Return True if config was modified."""
    if "skills" not in config:
        config["skills"] = {}
    load = config["skills"].setdefault("load", {})
    extra = load.setdefault("extraDirs", [])
    if skills_abs in extra:
        return False
    if dry_run:
        return True
    extra.append(skills_abs)
    return True


def write_config_if_changed(
    config_file: Path,
    config: dict,
    modified: bool,
    dry_run: bool,
) -> None:
    if not modified or dry_run:
        return
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def openclaw_missing_help() -> str:
    return (
        "openclaw CLI not found in PATH.\n"
        "Install OpenClaw (see upstream docs), ensure the binary is on PATH "
        "(e.g. npm global bin), or add its directory to PATH, then retry."
    )


def resolve_workspace() -> Path:
    if "OPENCLAW_WORKSPACE" in os.environ:
        return Path(os.environ["OPENCLAW_WORKSPACE"]).expanduser()
    if "OPENCLAW_PROFILE" in os.environ and os.environ["OPENCLAW_PROFILE"] != "default":
        profile = os.environ["OPENCLAW_PROFILE"]
        return Path.home() / f".openclaw/workspace-{profile}"
    return Path.home() / ".openclaw/workspace"


def run_generate_ai_workspace(extension_root: Path, dry_run: bool) -> None:
    gen = extension_root / "_scripts" / "generate_ai_workspace.py"
    if not gen.is_file():
        return
    if dry_run:
        return
    subprocess.run([sys.executable, str(gen)], cwd=str(extension_root), check=True)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Install cursor-agent-team OpenClaw adapter (merge templates, extraDirs, ai_workspace sync by default with -y)."
    )
    p.set_defaults(merge=True)
    p.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Non-interactive: skip prompts (default: generate + sync ai_workspace to workspace; use --no-ai-workspace to skip).",
    )
    p.add_argument(
        "--merge",
        dest="merge",
        action="store_true",
        help="Merge AGENTS.md / SOUL.md templates (default: on).",
    )
    p.add_argument(
        "--no-merge",
        dest="merge",
        action="store_false",
        help="Do not merge templates; only update openclaw.json when applicable.",
    )
    p.add_argument(
        "--apply-templates",
        dest="merge",
        action="store_true",
        help="Alias for --merge (canonical name: --merge).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions only; do not write files or run generate.",
    )
    p.add_argument(
        "--force-templates",
        action="store_true",
        help="Force re-merge templates (same as merge; kept for CLI compatibility).",
    )
    p.add_argument(
        "--ai-workspace",
        action="store_true",
        help="Run generate_ai_workspace + non-destructive sync to workspace (default with -y; explicit for interactive yes).",
    )
    p.add_argument(
        "--no-ai-workspace",
        action="store_true",
        help="Skip ai_workspace step even in interactive mode.",
    )
    p.add_argument(
        "--force-ai-workspace",
        action="store_true",
        help="Overwrite existing seed files in workspace ai_workspace when syncing.",
    )
    p.add_argument(
        "--skip-openclaw-check",
        action="store_true",
        help="Skip openclaw CLI/version checks (for --dry-run or unit tests).",
    )
    return p.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    ascii_mode = use_ascii_stdout()

    root = repo_root()
    extension_root = root.resolve()

    print(
        "cursor-agent-team OpenClaw adapter install"
        if ascii_mode
        else "cursor-agent-team OpenClaw adapter install"
    )
    print("==========================================")
    log_info(f"Extension root: {extension_root}", ascii_mode)
    print()

    # 1) openclaw CLI (optional skip for dry-run/tests)
    if not args.skip_openclaw_check:
        oc = shutil.which("openclaw")
        if not oc:
            log_err(openclaw_missing_help())

        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            out = (result.stdout or "") + (result.stderr or "")
        except OSError as e:
            log_err(f"Could not run openclaw --version: {e}")

        ver = parse_openclaw_version(out)
        if ver is None:
            log_err(f"Could not parse semver from openclaw --version output:\n{out!r}")
        if not version_ok(ver, REQUIRED_OPENCLAW_SEMVER):
            log_err(
                f"OpenClaw too old: need >= {'.'.join(map(str, REQUIRED_OPENCLAW_SEMVER))}, got {'.'.join(map(str, ver))}"
            )
        log_ok(f"openclaw version OK: {'.'.join(map(str, ver))}", ascii_mode)
        print()
    else:
        log_info("Skipped openclaw CLI/version check (--skip-openclaw-check)", ascii_mode)
        print()

    workspace = resolve_workspace()
    log_info(f"Workspace: {workspace}", ascii_mode)
    print()

    config_file = Path.home() / ".openclaw" / "openclaw.json"
    if not config_file.exists():
        log_err(f"Missing config file: {config_file}")

    if not args.dry_run:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = Path.home() / ".openclaw" / f"openclaw.json.backup.{ts}"
        shutil.copy2(config_file, backup)
        log_ok(f"Backed up openclaw.json to {backup}", ascii_mode)
        print()
    else:
        log_info("[dry-run] skipping openclaw.json backup", ascii_mode)
        print()

    config = load_json_config(config_file)
    skills_dir = (extension_root / "_openclaw" / "skills").resolve()
    skills_str = str(skills_dir)

    cfg_changed = ensure_extra_dirs(config, skills_str, args.dry_run)
    if cfg_changed and not args.dry_run:
        write_config_if_changed(config_file, config, cfg_changed, args.dry_run)
        log_ok("Updated skills.load.extraDirs (absolute path)", ascii_mode)
    elif cfg_changed and args.dry_run:
        log_info("[dry-run] would append skills.load.extraDirs", ascii_mode)
    elif skills_str in (
        config.get("skills", {}).get("load", {}).get("extraDirs", [])
    ):
        log_info("skills.load.extraDirs already contains skills dir", ascii_mode)
    print()

    # Templates
    templates_dir = extension_root / "_openclaw" / "templates"
    agents_tpl = templates_dir / "AGENTS.md.template"
    soul_tpl = templates_dir / "SOUL.md.template"

    if args.merge:
        if not agents_tpl.is_file():
            log_err(f"Missing template: {agents_tpl}")
        if not soul_tpl.is_file():
            log_err(f"Missing template: {soul_tpl}")

        body_a = apply_placeholders(agents_tpl.read_text(encoding="utf-8"), extension_root)
        body_s = apply_placeholders(soul_tpl.read_text(encoding="utf-8"), extension_root)

        dest_agents = workspace / "AGENTS.md"
        dest_soul = workspace / "SOUL.md"

        a_act = merge_block_into_file(
            dest_agents, body_a, AGENTS_START, AGENTS_END, args.dry_run
        )
        s_act = merge_block_into_file(
            dest_soul, body_s, SOUL_START, SOUL_END, args.dry_run
        )
        if args.dry_run:
            log_info(f"[dry-run] AGENTS.md action={a_act} -> {dest_agents}", ascii_mode)
            log_info(f"[dry-run] SOUL.md action={s_act} -> {dest_soul}", ascii_mode)
        else:
            log_ok(f"AGENTS.md ({a_act})", ascii_mode)
            log_ok(f"SOUL.md ({s_act})", ascii_mode)
        print()

    # ai_workspace
    want_ai = False
    if args.no_ai_workspace:
        want_ai = False
    elif args.ai_workspace:
        want_ai = True
    elif args.yes:
        want_ai = True
    else:
        try:
            r = input("Initialize ai_workspace under workspace now? [y/N] ").strip().lower()
            want_ai = r in ("y", "yes")
        except (EOFError, KeyboardInterrupt):
            want_ai = False
            print()

    if want_ai:
        log_info("Generating and syncing ai_workspace (non-destructive)...", ascii_mode)
        run_generate_ai_workspace(extension_root, args.dry_run)
        src_ai = extension_root / "ai_workspace"
        dest_ai = workspace / "ai_workspace"

        def _log(m: str) -> None:
            log_info(m, ascii_mode)

        mirror_ai_workspace_nondestructive(
            src_ai,
            dest_ai,
            args.dry_run,
            args.force_ai_workspace,
            _log,
        )
        if not args.dry_run:
            log_ok(f"ai_workspace synced to {dest_ai}", ascii_mode)
        print()

    log_info("Next: restart gateway: openclaw gateway restart", ascii_mode)
    log_info("Commands: /discuss, /crew, /init_workspace (see AGENTS.md)", ascii_mode)


if __name__ == "__main__":
    main()
