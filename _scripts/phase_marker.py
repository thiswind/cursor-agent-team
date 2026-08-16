#!/usr/bin/env python3
"""
Phase Marker - Output canonical phase completion markers for workflow validation.

Used at the end of each phase: after review, the agent calls this script;
script stdout is the single source of truth for [Phase N DONE] / [Phase N NOT DONE].
See: ai_workspace/scratchpad/phase_marker_script_design_20260228.md
"""

import sys
from typing import Optional


def parse_done(s: str) -> Optional[bool]:
    """Parse done argument: true/1 -> True, false/0 -> False, else None."""
    if s is None:
        return None
    t = s.strip().lower()
    if t in ("true", "1"):
        return True
    if t in ("false", "0"):
        return False
    return None


def build_marker(phase: int, done: bool = True) -> str:
    """Return the canonical marker line for a phase.

    Single source of truth for the marker format; verify_response.py imports
    this so generation and validation can never drift apart.
    """
    return f"[Phase {phase} {'DONE' if done else 'NOT DONE'}]"


def main() -> int:
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help")):
        print(
            "Usage: python phase_marker.py <phase> <done>\n"
            "  phase: non-negative integer (e.g. 0..3 for discuss/crew, 0..4 for prompt_engineer)\n"
            "  done:  true|false or 1|0 (case-insensitive)\n"
            "Output: exactly one line to stdout:\n"
            "  done=true  -> [Phase N DONE]\n"
            "  done=false -> [Phase N NOT DONE]\n"
            "Exit: 0 when done=true, 1 when done=false or invalid args.",
            file=sys.stderr,
        )
        return 1

    if len(sys.argv) != 3:
        print("Error: expected <phase> <done>", file=sys.stderr)
        return 1

    try:
        phase = int(sys.argv[1])
    except ValueError:
        print("Error: phase must be a non-negative integer", file=sys.stderr)
        return 1

    if phase < 0:
        print("Error: phase must be non-negative", file=sys.stderr)
        return 1

    done = parse_done(sys.argv[2])
    if done is None:
        print("Error: done must be true|false or 1|0", file=sys.stderr)
        return 1

    if done:
        print(build_marker(phase, True))
        return 0
    else:
        print(build_marker(phase, False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
