#!/usr/bin/env python3
"""Verify Scratchpad - Machine-check the scratchpad draft-loop contract (G1).

The discuss/writer masks require: draft goes to a scratchpad FILE first,
then a "## Review" section is appended, then the final text is produced.
This script makes that contract machine-checkable:

  1. Draft file exists and is non-empty.
  2. Draft mtime is recent (default 60 min) — i.e. written this round,
     not a stale file from an earlier session.
  3. Draft contains a "## Review" section with non-trivial content.

Usage:
  python verify_scratchpad.py --file scratchpad/discuss/draft_x.md
  python verify_scratchpad.py --file ... --max-age-min 120 --json

Exit codes: 0 = contract satisfied, 1 = violated/usage error.
"""

import argparse
import json
import os
import sys
import time


def verify(path: str, max_age_min: float) -> dict:
    errors, warnings = [], []
    exists = os.path.isfile(path)
    size = os.path.getsize(path) if exists else 0

    if not exists:
        errors.append(f"draft file not found: {path}")
    elif size == 0:
        errors.append(f"draft file is empty: {path}")

    age_min = None
    if exists:
        age_min = (time.time() - os.path.getmtime(path)) / 60.0
        if age_min > max_age_min:
            errors.append(
                f"draft is stale: last modified {age_min:.0f} min ago "
                f"(> {max_age_min:.0f} min) — write the draft THIS round"
            )

    has_review = False
    review_len = 0
    if exists and size > 0:
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            errors.append(f"cannot read draft: {e}")
            text = ""
        lowered = text.lower()
        idx = lowered.find("## review")
        if idx < 0:
            errors.append(
                'no "## Review" section — the draft loop requires a '
                "self-review section before finalizing"
            )
        else:
            review_body = text[idx:]
            review_len = len(review_body.strip())
            has_review = True
            if review_len < 40:
                warnings.append(
                    '"## Review" section is very short (<40 chars) — '
                    "a meaningful review is expected"
                )

    return {
        "valid": not errors,
        "file": path,
        "exists": exists,
        "size": size,
        "age_min": round(age_min, 1) if age_min is not None else None,
        "has_review": has_review,
        "review_len": review_len,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Verify the scratchpad draft-loop contract (G1)")
    p.add_argument("--file", required=True, help="path to the draft file")
    p.add_argument("--max-age-min", type=float, default=60.0,
                   help="draft must be modified within this many minutes "
                        "(default 60)")
    p.add_argument("--json", action="store_true", help="output JSON result")
    args = p.parse_args()

    result = verify(args.file, args.max_age_min)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print(f"VALID: draft loop satisfied "
                  f"(age {result['age_min']} min, review {result['review_len']} chars)")
        else:
            print("INVALID: scratchpad draft-loop contract violated")
            for e in result["errors"]:
                print(f"  ERROR: {e}")
        for w in result["warnings"]:
            print(f"  WARN: {w}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
