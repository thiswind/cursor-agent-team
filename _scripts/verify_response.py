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
  python verify_response.py --phases 4 --file response.md \
      --scratchpad scratchpad/discuss/draft.md   # G1 draft-loop check
      --no-leak scratchpad/                      # G2 leak check (vs drafts)
      --stamp                                    # G3 self-check credential

Exit codes: 0 = valid, 1 = invalid or usage error.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_marker import build_marker  # noqa: E402
from verify_scratchpad import verify as verify_scratchpad_file  # noqa: E402

STAMP_PATH = Path(__file__).resolve().parent.parent / "ai_workspace" / \
    "temp" / "verify_stamps.jsonl"
LEAK_MARKER_RE = re.compile(r"<!--\s*PROC\s*-->(.*?)<!--\s*/PROC\s*-->",
                            re.S | re.I)


def check_leak(response_text: str, draft_dirs, threshold: float = 0.4) -> dict:
    """G2 leak check (dual-signal, warning-only by design):

    A. marked segments: <!--PROC-->...</PROC--> blocks found in any draft
       that appear verbatim in the response -> the direct violation signal.
    B. line-overlap ratio: normalized lines shared between response and any
       draft, above threshold -> the coarse net (normalized: stripped,
       non-trivial >=6 chars, deduped).
    """
    warnings = []
    draft_files = []
    for d in draft_dirs:
        p = Path(d)
        if p.is_file():
            draft_files.append(p)
        elif p.is_dir():
            draft_files.extend(q for q in p.rglob("*.md") if q.is_file())

    def norm_lines(text):
        seen, out = set(), set()
        for ln in text.splitlines():
            s = ln.strip()
            if len(s) >= 6:
                if s not in seen:
                    seen.add(s)
                    out.add(s)
        return out

    resp_norm = norm_lines(response_text)
    for df in draft_files:
        try:
            draft = df.read_text(encoding="utf-8")
        except OSError:
            continue
        # signal A: marked process segments
        for m in LEAK_MARKER_RE.finditer(draft):
            seg = " ".join(m.group(1).split())
            if len(seg) >= 10 and seg in " ".join(response_text.split()):
                warnings.append(
                    f"LEAK(A) marked process-segment from {df.name} appears "
                    f"in response: \"{seg[:60]}...\"")
        # signal B: overlap ratio
        ov = norm_lines(draft) & resp_norm
        ratio = len(ov) / max(len(resp_norm), 1)
        if ratio > threshold:
            warnings.append(
                f"LEAK(B) {df.name}: line overlap {ratio:.0%} > "
                f"{threshold:.0%} ({len(ov)} shared lines) — response may "
                "reproduce draft process-notes")
    return {"warnings": warnings, "drafts_checked": len(draft_files)}


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
    parser.add_argument("--scratchpad",
                        help="G1: also verify the scratchpad draft-loop for this file")
    parser.add_argument("--scratchpad-max-age", type=float, default=60.0,
                        help="draft freshness window in minutes (default 60)")
    parser.add_argument("--no-leak", action="append", default=[], metavar="DIR/FILE",
                        help="G2: warn when response overlaps draft process-notes")
    parser.add_argument("--leak-threshold", type=float, default=0.4,
                        help="G2 signal-B overlap ratio threshold (default 0.4)")
    parser.add_argument("--stamp", action="store_true",
                        help="G3: append a self-check credential "
                             "(ts/file/md5/exit) to verify_stamps.jsonl")
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

    # G1: scratchpad draft-loop orchestration (plan C: independent impl,
    # single exit)
    if args.scratchpad:
        sp = verify_scratchpad_file(args.scratchpad, args.scratchpad_max_age)
        result["scratchpad"] = sp
        for e in sp["errors"]:
            result["errors"].append(f"[scratchpad] {e}")
        result["warnings"].extend(f"[scratchpad] {w}" for w in sp["warnings"])

    # G2: leak check (warning-only by design — calibrate before gating)
    if args.no_leak:
        leak = check_leak(text, args.no_leak, args.leak_threshold)
        result["leak"] = leak
        result["warnings"].extend(f"[leak] {w}" for w in leak["warnings"])

    # recompute validity: leak stays warning-only; scratchpad errors DO gate
    result["valid"] = not result["errors"]

    # G3: stamp the run (even on failure — the credential records the truth)
    stamp_record = None
    if args.stamp:
        try:
            STAMP_PATH.parent.mkdir(parents=True, exist_ok=True)
            stamp_record = {
                "ts": datetime.now().isoformat(timespec="seconds"),
                "file": args.file or "<stdin>",
                "md5": hashlib.md5(text.encode("utf-8")).hexdigest(),
                "phases": args.phases,
                "valid": result["valid"],
            }
            with open(STAMP_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(stamp_record, ensure_ascii=False) + "\n")
            result["stamp"] = "written"
        except OSError as e:
            result["stamp"] = f"failed: {e}"

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
        if stamp_record:
            print(f"  STAMP: {stamp_record['ts']} md5={stamp_record['md5'][:12]} "
                  f"valid={stamp_record['valid']} -> verify_stamps.jsonl")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
