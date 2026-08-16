#!/usr/bin/env python3
"""
Verify Response - Closed-loop validation of phase markers in a response.

This is the missing "court" for the phase-marker contract: phase_marker.py
GENERATES the markers, this script VERIFIES a complete response contains
them correctly, so the HARD REQUIREMENT becomes machine-checkable.

Checks:
  1. Every expected marker [Phase N DONE] is present, exactly once each.
  2. Markers appear in ascending order.
  3. No leftover [Phase N NOT DONE] markers (incomplete phase).
  4. No out-of-range markers for the declared phase count.
Warnings (non-fatal):
  - Marker not on its own line (format drift from script stdout).

Usage:
  python verify_response.py --phases 4 --file response.md
  cat response.md | python verify_response.py --phases 4 --stdin
  python verify_response.py --phases 4 --file response.md --json

Exit codes: 0 = valid, 1 = invalid or usage error.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_marker import build_marker  # noqa: E402


def verify(text: str, phases: int) -> dict:
    """Verify phase markers in text. Returns result dict with errors/warnings."""
    errors = []
    warnings = []

    expected = [build_marker(i) for i in range(phases)]

    # Check 1: presence and uniqueness of each expected marker
    for marker in expected:
        count = text.count(marker)
        if count == 0:
            errors.append(f"missing marker: {marker}")
        elif count > 1:
            errors.append(f"duplicate marker: {marker} (found {count} times)")

    # Check 2: ascending order
    positions = [text.find(marker) for marker in expected]
    if all(p >= 0 for p in positions) and positions != sorted(positions):
        errors.append(
            "markers out of order: "
            + " -> ".join(f"[{p}]" for p in sorted(range(phases), key=lambda i: positions[i]))
        )

    # Check 3: leftover NOT DONE markers
    for i in range(phases):
        not_done = build_marker(i, False)
        if not_done in text:
            errors.append(f"incomplete phase marker present: {not_done}")

    # Check 4: out-of-range markers
    for match in re.finditer(r"\[Phase (\d+) (DONE|NOT DONE)\]", text):
        n = int(match.group(1))
        if n >= phases:
            errors.append(f"out-of-range marker: {match.group(0)} (expected phases 0..{phases - 1})")

    # Warning: each marker should sit on its own line (script stdout is one line)
    for marker in expected:
        for m in re.finditer(re.escape(marker), text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end].strip()
            if line != marker:
                warnings.append(f"marker not on its own line: {marker}")
                break

    found = [m for m in expected if text.count(m) == 1]
    return {
        "valid": not errors,
        "phases": phases,
        "markers_found": len(found),
        "markers_expected": phases,
        "errors": errors,
        "warnings": warnings,
    }


def load_text(args) -> str:
    if args.stdin:
        return sys.stdin.read()
    with open(args.file, "r", encoding="utf-8") as f:
        return f.read()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify phase markers in a response")
    parser.add_argument("--phases", type=int, required=True,
                        help="number of phases the role must complete (e.g. 4 or 5)")
    parser.add_argument("--file", help="path to the response text file")
    parser.add_argument("--stdin", action="store_true", help="read response from stdin")
    parser.add_argument("--json", action="store_true", help="output JSON result")
    args = parser.parse_args()

    if args.phases <= 0:
        print("Error: --phases must be a positive integer", file=sys.stderr)
        return 1
    if not args.stdin and not args.file:
        print("Error: provide --file PATH or --stdin", file=sys.stderr)
        return 1

    try:
        text = load_text(args)
    except OSError as e:
        print(f"Error: cannot read input: {e}", file=sys.stderr)
        return 1

    result = verify(text, args.phases)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print(f"VALID: all {result['markers_found']}/{result['markers_expected']} phase markers verified")
        else:
            print("INVALID: response does not satisfy the phase-marker contract")
            for e in result["errors"]:
                print(f"  ERROR: {e}")
        for w in result["warnings"]:
            print(f"  WARN: {w}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
