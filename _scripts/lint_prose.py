#!/usr/bin/env python3
"""Lint Prose - Slop-phrase & banned-pattern scanner for CAT writing outputs (G4).

Two tiers, mirroring the writer mask's discipline:
  general  : filler intensifiers, hedge clichés, AI-tell phrases
  academic : general + academic cliches ("delve into", "novel framework", ...)

Reads a file (or stdin), reports hits with line numbers. Warnings only by
design (the writer decides); --fail turns it into a gate (exit 1).

Usage:
  python lint_prose.py --file final.md
  python lint_prose.py --file final.md --tier academic --json
  cat draft.md | python lint_prose.py --stdin

Exit codes: 0 clean (or warnings without --fail), 1 hits with --fail / usage.
"""

import argparse
import json
import re
import sys

GENERAL = [
    (r"\bit[''']?s important to note\b", "filler opener"),
    (r"\bnote that\b", "filler"),
    (r"\bin conclusion\b", "cliché closer"),
    (r"\bat the end of the day\b", "filler"),
    (r"\bdelve into\b", "AI-tell"),
    (r"\bdeep dive\b", "AI-tell"),
    (r"\bgame[- ]changer\b", "hype"),
    (r"\bseamless(ly)?\b", "hype"),
    (r"\bleverage\b", "corporate filler (prefer 'use')"),
    (r"\brobust\b", "vague if unquantified"),
    (r"\bcutting[- ]edge\b", "hype"),
    (r"\bharness\b", "AI-tell"),
    (r"\bunleash\b", "hype"),
    (r"\bpivotal\b", "vague intensifier"),
    (r"\btestament to\b", "cliché"),
    (r"\bin today[''']?s (fast[- ]paced |ever[- ]evolving )?world\b", "cliché"),
    (r"\bnavigate the (complexities|landscape) of\b", "cliché"),
    (r"\bfolks\b", "tone"),
    (r"\blet[''']?s (dive|explore)\b", "AI-tell opener"),
    (r"\bI think (that )?it[''']?s worth\b", "hedge padding"),
    (r"\bquite (good|bad|nice)\b", "weak qualifier"),
    (r"\bvery (unique|important|interesting)\b", "redundant intensifier"),
]

ACADEMIC = GENERAL + [
    (r"\bnovel (framework|approach|method|technique)\b", "academic cliché"),
    (r"\bstate[- ]of[- ]the[- ]art\b", "overused; cite specifics"),
    (r"\bfurther research is needed\b", "empty closer"),
    (r"\bplays a (crucial|vital|pivotal) role\b", "vague claim"),
    (r"\bcomprehensive (analysis|study|review)\b", "self-praise"),
    (r"\bin recent years\b", "weak framing"),
    (r"\bextensive (experiments|evaluation)\b", "self-praise"),
    (r"\bremarkable (performance|results)\b", "self-praise"),
    (r"\b sheds? light on\b", "cliché"),
    (r"\bpaves? the way\b", "cliché"),
    (r"\btreasure trove\b", "cliché"),
    (r"\ba myriad of\b", "prefer 'many'"),
    (r"\bplethora\b", "prefer 'many'"),
]

TIER_PATTERNS = {"general": GENERAL, "academic": ACADEMIC}


def lint(text: str, tier: str) -> list:
    hits = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for pat, label in TIER_PATTERNS[tier]:
            for m in re.finditer(pat, line, re.IGNORECASE):
                hits.append({
                    "line": i, "phrase": m.group(0), "label": label,
                })
    return hits


CAPTION_RE = re.compile(r"(?i)^(table|fig(ure)?|表|图)\s*\.?\s*\d", re.I)


def check_insertions(text: str, max_paren_words: int = 6) -> list:
    """Detect mid-sentence explanatory insertions (issue #10 rule).

    Flags: paired em dashes around an explanation, colon/semicolon followed
    by an explanatory clause with a connective, over-long parentheticals,
    and the Chinese equivalents. Caption lines (Table x / Figure x / 表x / 图x)
    are exempt. Warning-level by design.
    """
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if CAPTION_RE.search(line):
            continue
        for m in re.finditer(r"\S[^—–]*[—–]\s*[^—–]{8,}\s*[—–]", line):
            hits.append({"line": i, "phrase": m.group(0)[:60],
                         "label": "em-dash insertion"})
        for m in re.finditer(
                r"[a-zA-Z][^:;]{10,}[:;]\s*(which|where|because|since|"
                r"meaning|namely|i\.e\.|that is)[ ,]", line):
            hits.append({"line": i, "phrase": m.group(0)[:60],
                         "label": "colon/semicolon explanatory clause"})
        for m in re.finditer(r"\(([^)]+)\)", line):
            inner = m.group(1)
            if len(inner.split()) > max_paren_words:
                hits.append({"line": i, "phrase": m.group(0)[:60],
                             "label": f"parenthetical >{max_paren_words} words"})
        for m in re.finditer(r"[，。；][^。！？]*——[^。！？]*[，。；]", line):
            hits.append({"line": i, "phrase": m.group(0)[:60],
                         "label": "中文破折号插入语"})
    return hits


def main() -> int:
    p = argparse.ArgumentParser(description="Slop-phrase lint for CAT writing outputs")
    p.add_argument("--file", help="file to lint")
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--tier", choices=["general", "academic"], default="general")
    p.add_argument("--fail", action="store_true",
                   help="exit 1 when hits found (default: warn only)")
    p.add_argument("--insertions", action="store_true",
                   help="also check mid-sentence explanatory insertions "
                        "(issue #10 rule: em dash/colon/semicolon/"
                        "parentheses; captions exempt)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if not args.stdin and not args.file:
        print("Error: provide --file PATH or --stdin", file=sys.stderr)
        return 1
    try:
        if args.stdin:
            text = sys.stdin.read()
        else:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
    except OSError as e:
        print(f"Error: cannot read input: {e}", file=sys.stderr)
        return 1

    hits = lint(text, args.tier)
    if args.insertions:
        hits = hits + check_insertions(text)

    if args.json:
        print(json.dumps({"tier": args.tier, "hits": hits,
                          "count": len(hits)}, indent=2))
    else:
        if hits:
            print(f"lint_prose [{args.tier}]: {len(hits)} hit(s)")
            for h in hits:
                print(f"  L{h['line']}: \"{h['phrase']}\" — {h['label']}")
        else:
            print(f"lint_prose [{args.tier}]: clean")

    if args.fail and hits:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
