#!/usr/bin/env python3
"""Dispatch Header - Render the CAT sub-agent dispatch template (G5, part 1).

Prints a ready-to-paste dispatch prompt built from the SUBAGENT-DISPATCH.md
contract ([Role]/[Context]/[Task]/[Output Contract]). Machine-generated =
machine-compliant: the four sections and the structured-return fields are
always present.

  python dispatch_header.py --mask crew --task "recon scripts" \
      [--context-file ctx.md] [--boundary "ai_workspace/notes"] \
      [--parallel-group G1] [--read-only] > dispatch_prompt.txt

Exit codes: 0 ok, 1 usage error.
"""

import argparse
import sys

MASKS = ["discuss", "crew", "prompt_engineer", "spec_translator",
         "writer", "workflow"]

RETURN_FIELDS = ["summary", "files_changed", "verification", "leftovers"]


def render(args) -> str:
    role = f"[CAT mask] Your role: {args.mask} ({'/'.join(MASKS)})"
    behavior = ("[CAT behavior] Read cursor-agent-team/_claude/commands/"
                f"{args.mask}.md (or _cursor/rules/{args.mask}_assistant.mdc); "
                "follow its persona and flow")
    ctx = "[CAT context] " + (args.context or "")
    if args.context_file:
        try:
            with open(args.context_file, "r", encoding="utf-8") as f:
                ctx += "\n" + f.read().rstrip()
        except OSError as e:
            print(f"Error: cannot read context file: {e}", file=sys.stderr)
            raise SystemExit(1)
    task = "[CAT task] " + args.task
    if args.boundary:
        task += f"\n  File boundary (write ONLY within): {args.boundary}"
    if args.read_only:
        task += "\n  READ-ONLY: write nothing; report findings only."
    if args.parallel_group:
        task += (f"\n  Parallel group: {args.parallel_group} — other agents "
                 "work on disjoint paths; do not touch anything outside your boundary.")
    output = (
        "[CAT output contract]\n"
        "- Write outputs under cursor-agent-team/ai_workspace/ (notes/scratchpad/"
        "plans as the mask directs)\n"
        "- On stage completion run: python cursor-agent-team/_scripts/"
        "phase_marker.py <N> true\n"
        "- Self-verify with verify_response.py before responding\n"
        "- Final reply MUST be structured with exactly these fields:\n"
        + "".join(f"    {f}: <...>\n" for f in RETURN_FIELDS)
        + "- Report pointers, not dumps"
    )
    return "\n\n".join([role, behavior, ctx, task, output])


def main() -> int:
    p = argparse.ArgumentParser(
        description="Render the CAT sub-agent dispatch template")
    p.add_argument("--mask", required=True, choices=MASKS)
    p.add_argument("--task", required=True, help="one-line task description")
    p.add_argument("--context", default="", help="one-line context")
    p.add_argument("--context-file", help="file with fuller context")
    p.add_argument("--boundary", help="write boundary for this agent")
    p.add_argument("--parallel-group", help="parallel group id (e.g. G1)")
    p.add_argument("--read-only", action="store_true")
    args = p.parse_args()
    print(render(args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
