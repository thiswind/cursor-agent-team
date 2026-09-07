#!/usr/bin/env python3
"""Closing Protocol - One-command session wrap-up (G8).

Orchestrates the five closing steps that were previously five prompt
paragraphs (AGENTS-GUIDE sec.4), stopping at the first failure with a
recovery hint:

  1. topic-tree round   : if --tree-file given, land it via validate_topic_tree
                          (skip if omitted); report uncommitted-checks hint
  2. verify             : if --verify-file given, run verify_response on it
  3. notes              : if --note given, append to notes/ (via cat_write)
  4. snapshot           : refresh the handoff snapshot note (create only if
                          --snapshot-title given)
  5. commit             : run commit_workspace.py (add -f + assert + commit)

Usage:
  python closing_protocol.py --tree-file /tmp/tree.md --note "did X" \
      --note-file project.md --verify-file response.md --verify-phases 4 \
      --commit-msg "feat: X"

Exit codes: 0 all ok, 1 any step failed (see output for recovery hint).
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PRODUCT = SCRIPT_DIR.parent
WORKSPACE = PRODUCT / "ai_workspace"
PY = sys.executable or "python3"


def run_step(name, fn):
    print(f"[closing] step {name} ...", flush=True)
    try:
        ok, info = fn()
    except Exception as e:
        ok, info = False, [f"exception: {e}"]
    if ok:
        print(f"[closing] step {name}: OK" + (f" — {info}" if info else ""))
    else:
        print(f"[closing] step {name}: FAILED")
        for i in ([info] if isinstance(info, str) else info):
            print(f"    {i}")
        print(f"[closing] STOPPED at step {name}. Fix the issue, re-run "
              f"from this step (earlier steps are already done).")
    return ok


def step_tree(args):
    if not args.tree_file:
        uncommitted = (WORKSPACE / "temp" / "discussion_topics.md.new")
        hint = ("no --tree-file given — if you have pending topic-tree "
                f"changes, pass them; stale file exists: {uncommitted.exists()}")
        return True, hint
    r = subprocess.run(
        [PY, str(SCRIPT_DIR / "cat_write.py"), "topic-round", args.tree_file,
         "--wait", "30"] + (["--force"] if args.force else []),
        capture_output=True, text=True)
    ok = r.returncode == 0
    info = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()
    return ok, info


def step_verify(args):
    if not args.verify_file:
        return True, "skipped (no --verify-file)"
    r = subprocess.run(
        [PY, str(SCRIPT_DIR / "verify_response.py"),
         "--phases", str(args.verify_phases), "--file", args.verify_file,
         "--stamp"],
        capture_output=True, text=True)
    ok = r.returncode == 0
    info = (r.stdout.strip().splitlines() or [r.stderr.strip()])[0]
    return ok, info


def step_note(args):
    if not args.note:
        return True, "skipped (no --note)"
    note_file = args.note_file or "closing-log.md"
    r = subprocess.run(
        [PY, str(SCRIPT_DIR / "cat_write.py"), "notes", "--append", note_file,
         args.note, "--wait", "30"],
        capture_output=True, text=True)
    ok = r.returncode == 0
    info = (r.stdout.strip().splitlines() or [r.stderr.strip()])[0]
    return ok, info


def step_snapshot(args):
    if not args.snapshot_title:
        return True, "skipped (no --snapshot-title)"
    notes = WORKSPACE / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    existing = sorted(notes.glob(f"{today}-snapshot*.md"))
    path = notes / f"{today}-snapshot-{len(existing) + 1:02d}.md"
    body = (
        f"# {args.snapshot_title}\n\n"
        f"> Handoff snapshot written by closing_protocol.py — {datetime.now().isoformat(timespec='seconds')}\n\n"
        "## What this session did\n\n- (fill in 3-5 bullets)\n\n"
        "## Where things stand\n\n- topic tree: \n- plans: \n\n"
        "## Next session should\n\n- \n"
    )
    path.write_text(body, encoding="utf-8")
    return True, f"wrote {path.relative_to(PRODUCT.parent)}"


def step_commit(args):
    if args.no_commit:
        return True, "skipped (--no-commit)"
    msg = args.commit_msg or f"chore: CAT session closing {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    r = subprocess.run(
        [PY, str(SCRIPT_DIR / "commit_workspace.py"), "-m", msg],
        capture_output=True, text=True,
        cwd=str(PRODUCT.parent))
    ok = r.returncode == 0
    tail = (r.stdout.strip().splitlines() or [r.stderr.strip()])
    info = tail[-1] if tail else ""
    return ok, info


def main() -> int:
    p = argparse.ArgumentParser(description="One-command session wrap-up (five steps)")
    p.add_argument("--tree-file", help="new topic-tree content file to land via validator")
    p.add_argument("--force", action="store_true", help="pass --force to the topic-tree update")
    p.add_argument("--verify-file", help="response file to verify (with --stamp)")
    p.add_argument("--verify-phases", type=int, default=4)
    p.add_argument("--note", help="closing note text to append to notes/")
    p.add_argument("--note-file", default="closing-log.md",
                   help="notes file name (default closing-log.md)")
    p.add_argument("--snapshot-title", help="title for a handoff snapshot note")
    p.add_argument("--commit-msg", help="commit message for step 5")
    p.add_argument("--no-commit", action="store_true", help="skip step 5")
    args = p.parse_args()

    steps = [
        ("1/5 topic-tree", lambda: step_tree(args)),
        ("2/5 verify", lambda: step_verify(args)),
        ("3/5 note", lambda: step_note(args)),
        ("4/5 snapshot", lambda: step_snapshot(args)),
        ("5/5 commit", lambda: step_commit(args)),
    ]
    report = {}
    for name, fn in steps:
        ok = run_step(name, fn)
        report[name.split()[0]] = "ok" if ok else "FAILED"
        if not ok:
            print(json.dumps({"closing": "stopped", "steps": report},
                             ensure_ascii=False))
            return 1
    print(json.dumps({"closing": "complete", "steps": report},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
