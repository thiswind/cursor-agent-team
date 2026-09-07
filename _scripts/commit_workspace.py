#!/usr/bin/env python3
"""
commit_workspace.py — CAT closing-protocol helper for ai_workspace state files.

Why this exists (FR-0008/0009/0010, host-agent feedback ledger 2026-09):
CAT's own installer writes `ai_workspace/` ignore rules (host root) and
`ai_workspace/**` (nested cursor-agent-team/.gitignore). Untracked files under
those rules are SILENTLY skipped by `git add` — single-file add exits 1, but
directory-level add exits 0 — so notes and plans can sit on disk while the
repo history shows nothing. Two real incidents: a note lost for 3 days
(FR-0010), and a submodule host whose entire state layer never entered any
repository (FR-0017).

What it does (one command = one safe closing step):
  1. `git add -f` every requested path (force past the ignore rules)
  2. ASSERT each path is actually staged/tracked (`git ls-files --error-unmatch`
     + `git diff --cached --name-only` check) — fail loudly instead of silently
  3. `git commit` with the given message (default provided)

Usage:
  python3 _scripts/commit_workspace.py <path...> -m "message"          # commit
  python3 _scripts/commit_workspace.py <path...> -m "message" --dry-run
  python3 _scripts/commit_workspace.py <path...> --check-only          # assert only

Exit codes: 0 success / 1 assertion or git failure / 2 not a git host.

Notes:
- Paths are resolved relative to the *host project root* (script's grandparent
  dir), not CWD — safe to call from anywhere.
- Also stages already-tracked modifications of the given paths (add is idempotent).
- Never touches files outside the explicit path list.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CAT_ROOT = SCRIPT_DIR.parent            # cursor-agent-team/
HOST_ROOT = Path(os.environ.get("CAT_HOST_ROOT", str(CAT_ROOT.parent))).resolve()  # the host project root


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description="CAT workspace closing-commit helper")
    parser.add_argument("paths", nargs="+", help="Paths under the host root (ai_workspace files) to commit")
    parser.add_argument("-m", "--message", default="chore: CAT workspace state update",
                        help="Commit message")
    parser.add_argument("--dry-run", action="store_true", help="Stage+assert only, no commit")
    parser.add_argument("--check-only", action="store_true",
                        help="Only assert the paths are tracked; no add, no commit")
    args = parser.parse_args()

    if subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                      cwd=str(HOST_ROOT), capture_output=True).returncode != 0:
        print("ERROR: host root is not a git repository (state stays disk-only here)")
        sys.exit(2)

    resolved = []
    for p in args.paths:
        rp = (HOST_ROOT / p).resolve()
        if not rp.exists():
            print(f"ERROR: path does not exist: {p} (resolved {rp})")
            sys.exit(1)
        resolved.append(rp)

    # Step 1: force-add past ignore rules
    if not args.check_only:
        r = sh(["git", "add", "-f"] + [str(p) for p in resolved], cwd=str(HOST_ROOT))
        if r.returncode != 0:
            print(f"ERROR: git add -f failed:\n{r.stderr}")
            sys.exit(1)

    # Step 2: assertion — every path must be tracked AND (when committing) staged
    staged = set()
    if not args.check_only:
        sr = sh(["git", "diff", "--cached", "--name-only"], cwd=str(HOST_ROOT))
        staged = set(sr.stdout.splitlines())

    failures = []
    for rp in resolved:
        rel = str(rp.relative_to(HOST_ROOT))
        tracked = sh(["git", "ls-files", "--error-unmatch", rel], cwd=str(HOST_ROOT)).returncode == 0
        if not tracked:
            failures.append(f"{rel}: NOT tracked — add silently failed (ignore rule?)")
        elif not args.check_only and rel not in staged and sh(
                ["git", "diff", "--name-only", "HEAD", "--", rel], cwd=str(HOST_ROOT)).stdout.strip():
            failures.append(f"{rel}: tracked but not staged this run")
    if failures:
        print("ASSERTION FAILED (nothing committed):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    if args.check_only or args.dry_run:
        print(f"OK: {len(resolved)} path(s) tracked"
              + ("" if args.check_only else " and staged (dry-run, no commit)"))
        sys.exit(0)

    # Step 3: commit
    r = sh(["git", "commit", "-m", args.message], cwd=str(HOST_ROOT))
    if r.returncode != 0:
        print(f"ERROR: git commit failed:\n{r.stderr}")
        sys.exit(1)
    print(f"OK: committed {len(resolved)} path(s) — {r.stdout.strip().splitlines()[0] if r.stdout.strip() else 'done'}")


if __name__ == "__main__":
    main()
