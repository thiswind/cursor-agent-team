#!/usr/bin/env python3
"""
Verify Mechanism - Closed-loop validation of marker protocol v2 (RFC-003).

Marker protocol v2 makes professionalism-mechanism activation machine-checkable
(same philosophy as phase_marker.py -> verify_response.py). Mechanism archives
(write drafts / read ledgers) must carry:

  M1  activation gate line: <PIECE>-GATE: PASS | SKIP(reason)   [first line]
  M2  structural section markers (per-piece required markers)
  M3  convergence line: CONVERGED: R<N> (N>=2) | BUDGET: R<N>(reason)

Checks (write piece):
  1. First non-empty line matches WRITE-GATE: PASS or WRITE-GATE: SKIP(...)
  2. On PASS: at least one `[轮1·V<i>]` ledger entry AND >=2 distinct rounds
     present in ledger entries (`[轮N·V...]`, N >= 2).
  3. Exactly one convergence line (CONVERGED: R<N> with N>=2, or BUDGET: R<N>).
     CONVERGED: R1 is INVALID (single-round stop is banned).
  4. On SKIP: no convergence line required.

Checks (read piece): archive is a directory (viewpoints.md + ledger.md) or a
single ledger file:
  1. READ-GATE: PASS | SKIP(...) as above (in ledger.md, first non-empty line)
  2. On PASS: >=2 distinct rounds in `[轮N·V...]` entries.
  3. Convergence line as above (in ledger.md).
  4. On PASS: 对照 marker present (`对照` heading or 对照表) — the mandatory
     read endpoint (warning-level in v1; see RFC-003 §7 open items).

Exit codes: 0 = valid, 1 = invalid or usage error.
JSON mode: --json prints {"valid":bool,"errors":[...],"warnings":[...]}.
"""

import argparse
import json
import os
import re
import sys

GATE_RE = re.compile(r"^(WRITE|READ)-GATE:\s*(PASS|SKIP)\s*(\([^)]*\))?\s*$")
ROUND_RE = re.compile(r"\[轮(\d+)·V(\d+)")
CONVERGED_RE = re.compile(r"^CONVERGED:\s*R(\d+)\s*$", re.M)
BUDGET_RE = re.compile(r"^BUDGET:\s*R(\d+)\s*(\([^)]*\))?\s*$", re.M)


def first_gate_line(text: str):
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = GATE_RE.match(s)
        return m
    return None


def check_archive(piece: str, text: str) -> tuple[list, list]:
    errors, warnings = [], []

    m = first_gate_line(text)
    if not m:
        errors.append("M1: no gate line (expected '<PIECE>-GATE: PASS|SKIP(reason)' "
                      "as first non-empty line)")
        return errors, warnings
    prefix, verdict = m.group(1), m.group(2)
    expected = "WRITE" if piece == "write" else "READ"
    if prefix != expected:
        errors.append(f"M1: gate prefix '{prefix}-GATE' does not match piece "
                      f"'{piece}' (expected {expected}-GATE)")

    rounds = sorted({int(n) for n, _ in ROUND_RE.findall(text)})
    conv = CONVERGED_RE.search(text)
    budget = BUDGET_RE.search(text)

    if verdict == "PASS":
        if not rounds:
            errors.append("M2: no ledger entries found ([轮N·V...] markers)")
        elif rounds[-1] < 2:
            errors.append(f"M2/M3: only round(s) {rounds} present — single-round "
                          "stop is banned (at least round 2 required)")
        if conv and budget:
            errors.append("M3: both CONVERGED and BUDGET lines present "
                          "(exactly one required)")
        if not conv and not budget:
            errors.append("M3: no convergence line (expected 'CONVERGED: R<N>' "
                          "with N>=2 or 'BUDGET: R<N>(reason)')")
        if conv:
            n = int(conv.group(1))
            if n < 2:
                errors.append(f"M3: CONVERGED: R{n} invalid — N must be >= 2")
            elif rounds and n > rounds[-1]:
                errors.append(f"M3: CONVERGED: R{n} exceeds max ledger round "
                              f"R{rounds[-1]}")
        if budget:
            n = int(budget.group(1))
            if not budget.group(2):
                warnings.append("M3: BUDGET line lacks a ruling reason")
            if n < 2:
                errors.append(f"M3: BUDGET: R{n} invalid — N must be >= 2")
        # Warnings (v1 lenient, RFC-003 §7)
        if piece == "write" and "## 对照" not in text and "对照" not in text:
            warnings.append("M2: no 对照 section found (intent-vs-draft "
                            "alignment recommended)")
        if piece == "read" and "对照" not in text:
            warnings.append("M2: no 对照 endpoint in read ledger (mandatory "
                            "read endpoint; escalate after exp4 evidence)")
    else:  # SKIP
        if not (m.group(3) and m.group(3).strip("()")):
            warnings.append("M1: SKIP without a reason string")
        if conv or budget:
            errors.append("M3: convergence line present on a SKIP gate "
                         "(SKIP path writes no loop archive)")
        if rounds:
            warnings.append("M2: ledger entries present on SKIP gate "
                            "(expected direct single-pass)")
    return errors, warnings


def read_piece_text(path: str) -> tuple[str, str]:
    """Resolve read archive (dir with ledger.md, or single file) -> (name, text)."""
    if os.path.isdir(path):
        ledger = os.path.join(path, "ledger.md")
        if not os.path.isfile(ledger):
            # fall back: any .md in dir containing the gate line
            cands = [os.path.join(path, f) for f in sorted(os.listdir(path))
                     if f.endswith(".md")]
            for c in cands:
                with open(c, encoding="utf-8") as fh:
                    t = fh.read()
                if first_gate_line(t):
                    return os.path.basename(c), t
            raise SystemExit(f"error: no ledger.md or gate-bearing .md in {path}")
        with open(ledger, encoding="utf-8") as fh:
            return "ledger.md", fh.read()
    with open(path, encoding="utf-8") as fh:
        return os.path.basename(path), fh.read()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("piece", choices=["write", "read", "deliberation"],
                    help="mechanism piece")
    ap.add_argument("archive", help="process archive: drafts file (write) or "
                                    "ledger file/dir (read)")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    if args.piece == "deliberation":
        print("note: deliberation piece markers are checked by its own "
              "protocol (RFC-001 v2); this script covers write/read",
              file=sys.stderr)
        return 1

    try:
        if args.piece == "write":
            with open(args.archive, encoding="utf-8") as fh:
                text = fh.read()
        else:
            _, text = read_piece_text(args.archive)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    errors, warnings = check_archive(args.piece, text)
    if args.as_json:
        print(json.dumps({"valid": not errors, "errors": errors,
                          "warnings": warnings}, ensure_ascii=False, indent=2))
    else:
        for w in warnings:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        print("valid" if not errors else "invalid")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
