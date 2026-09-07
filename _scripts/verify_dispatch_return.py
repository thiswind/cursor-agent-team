#!/usr/bin/env python3
"""Verify Dispatch Return - Structured-return compliance checker (G5, part 2).

Checks a sub-agent's reply against the dispatch contract:
  1. all four fields present (summary/files_changed/verification/leftovers)
  2. verification field mentions a script/command (not empty words)
  3. two-strikes ledger: repeated non-compliance by the same agent is
     recorded under ai_workspace/temp/dispatch_strikes.json (warn at 1,
     recommend rejection at 2)

  python verify_dispatch_return.py --file reply.md --agent recon-1
  cat reply.md | python verify_dispatch_return.py --stdin --agent recon-1

Exit codes: 0 compliant, 1 non-compliant, 2 non-compliant AND two strikes.
"""

import argparse
import json
import re
import sys
from pathlib import Path

FIELDS = ["summary", "files_changed", "verification", "leftovers"]
STRIKES_PATH = Path(__file__).resolve().parent.parent / "ai_workspace" / \
    "temp" / "dispatch_strikes.json"


def check_fields(text: str) -> dict:
    missing, empty = [], []
    for f in FIELDS:
        m = re.search(rf"^\s*\*?\*?{f}\*?\*?\s*[:：]\s*(.*)$", text,
                      re.IGNORECASE | re.M)
        if not m:
            missing.append(f)
        elif not m.group(1).strip():
            empty.append(f)
    ok = not missing and not empty
    return {"ok": ok, "missing": missing, "empty": empty}


def check_verification(text: str) -> dict:
    m = re.search(r"^\s*\*?\*?verification\*?\*?\s*[:：]\s*(.*)$", text,
                  re.IGNORECASE | re.M)
    val = m.group(1) if m else ""
    has_evidence = bool(re.search(
        r"(\.py\b|pytest|test_|exit|code|md5|diff|ls |cat |--)", val,
        re.IGNORECASE) or re.search(r"\b(OK|PASS|VALID)\b", val))
    return {"ok": has_evidence, "value": val[:100]}


def load_strikes() -> dict:
    if STRIKES_PATH.is_file():
        try:
            return json.loads(STRIKES_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_strikes(data: dict) -> None:
    STRIKES_PATH.parent.mkdir(parents=True, exist_ok=True)
    STRIKES_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                            encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Check sub-agent reply against the dispatch contract")
    p.add_argument("--file", help="reply text file")
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--agent", required=True, help="agent identifier")
    p.add_argument("--no-strike", action="store_true",
                   help="check only; do not record a strike on failure")
    args = p.parse_args()

    if not args.stdin and not args.file:
        print("Error: provide --file PATH or --stdin", file=sys.stderr)
        return 1
    try:
        if args.stdin:
            text = sys.stdin.read()
        else:
            text = open(args.file, "r", encoding="utf-8").read()
    except OSError as e:
        print(f"Error: cannot read input: {e}", file=sys.stderr)
        return 1

    fields = check_fields(text)
    verif = check_verification(text)
    compliant = fields["ok"] and verif["ok"]

    strikes = load_strikes()
    entry = strikes.setdefault(args.agent, {"count": 0, "history": []})

    if compliant:
        print(f"COMPLIANT: {args.agent} — all four fields + verification evidence")
        if entry["count"] > 0:
            print(f"  (note: {args.agent} has {entry['count']} prior strike(s))")
        entry["history"].append({"ts": __import__("datetime").datetime.now()
                                 .isoformat(timespec="seconds"),
                                 "result": "compliant"})
        save_strikes(strikes)
        return 0

    print(f"NON-COMPLIANT: {args.agent}")
    for f in fields["missing"]:
        print(f"  missing field: {f}")
    for f in fields["empty"]:
        print(f"  empty field: {f}")
    if not verif["ok"]:
        print(f"  verification field lacks script/command evidence: {verif['value']!r}")

    if not args.no_strike:
        entry["count"] += 1
        entry["history"].append({
            "ts": __import__("datetime").datetime.now()
            .isoformat(timespec="seconds"),
            "result": "non-compliant",
            "missing": fields["missing"] + fields["empty"]})
        save_strikes(strikes)
        if entry["count"] >= 2:
            print(f"  TWO STRIKES ({entry['count']}): reject this agent's "
                  "outputs for this task; re-dispatch per SUBAGENT-DISPATCH.md")
            return 2
        print("  strike recorded (1/2)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
