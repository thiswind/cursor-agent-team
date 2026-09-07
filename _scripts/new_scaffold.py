#!/usr/bin/env python3
"""New Plan / New Session - Naming-convention scaffolds (G7).

Create-then-compliant: files are born with the right name and the right
frontmatter, so no lint is needed after the fact.

  python new_plan.py PLAN-V024-002 "Title of plan" --owner "workshop session"
      -> ai_workspace/plans/PLAN-V024-002.md (with PLAN template)
  python new_session.py session_20260908_recon
      -> ai_workspace/scratchpad/notes/session_20260908_recon.md

Both refuse to overwrite existing files. Exit codes: 0 created, 1 error.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent / "ai_workspace"

PLAN_ID_RE = re.compile(r"^PLAN-[A-Z0-9]+-\d{3}$")
SESSION_RE = re.compile(r"^session_\d{8}_[a-z0-9_]+$")


def refuse_if_exists(path: Path) -> bool:
    if path.exists():
        print(f"Error: already exists: {path}", file=sys.stderr)
        return False
    return True


def new_plan(args) -> int:
    if not PLAN_ID_RE.match(args.plan_id):
        print("Error: PLAN-ID must match PLAN-<SCOPE>-<NNN>, "
              "e.g. PLAN-V024-002", file=sys.stderr)
        return 1
    path = WORKSPACE / "plans" / f"{args.plan_id}.md"
    if not refuse_if_exists(path):
        return 1
    today = datetime.now().strftime("%Y-%m-%d")
    body = f"""# {args.plan_id} — {args.title}

> **Status**: draft
> **Created**: {today} · **Owner**: {args.owner}

## Owner's original instructions (verbatim, binding)

> (paste the binding instruction here)

## Scope

- [ ] (break work into checkable items)

## Anti-drift rules

- (list the fixed order / do-not-skip rules)

## Rollback

- (how to undo safely)
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    print(f"created: {path.relative_to(WORKSPACE.parent)}")
    print("next: cat_write.py index-rebuild  # after filling it in")
    return 0


def new_session(args) -> int:
    if not SESSION_RE.match(args.name):
        print("Error: NAME must match session_YYYYMMDD_slug "
              "(lowercase, underscores)", file=sys.stderr)
        return 1
    path = WORKSPACE / "scratchpad" / "notes" / f"{args.name}.md"
    if not refuse_if_exists(path):
        return 1
    today = datetime.now().strftime("%Y-%m-%d")
    body = f"""# {args.name}

> Session working note — created {today} by new_session.py.
> Claim long-running work here so parallel sessions see the claim.

## Claim / purpose

- (what this session claims and why)

## Findings

- 

## Leftovers

- 
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    print(f"created: {path.relative_to(WORKSPACE.parent)}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description="Naming-convention scaffolds for plans and session notes")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("new-plan", help="scaffold ai_workspace/plans/PLAN-*.md")
    sp.add_argument("plan_id", metavar="PLAN-ID")
    sp.add_argument("title", metavar="TITLE")
    sp.add_argument("--owner", default="unassigned")

    sp = sub.add_parser("new-session",
                        help="scaffold scratchpad/notes/session_*.md")
    sp.add_argument("name", metavar="NAME")

    args = p.parse_args()
    return new_plan(args) if args.cmd == "new-plan" else new_session(args)


if __name__ == "__main__":
    sys.exit(main())
