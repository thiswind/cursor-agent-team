#!/usr/bin/env python3
"""convert_rules_trae_cn.py — Generate Trae CN project rules from Cursor .mdc rules.

Single-source discipline: the six mask rules live as .mdc in _cursor/rules/;
this script renders them into _trae_cn/rules/*.md with Trae CN rule
frontmatter (name/description/alwaysApply per docs.trae.cn/ide_rules).
Body is copied verbatim (minus the .mdc frontmatter block).

Usage:
    python3 _scripts/convert_rules_trae_cn.py           # write
    python3 _scripts/convert_rules_trae_cn.py --check   # verify, exit 1 on drift

Design decisions (PLAN-TRAE-CN-001):
- Mask rules keep `alwaysApply: false` (Trae CN smart activation via
  description; avoids always-on injection of six full rule texts).
- A small router rule (cat-router.md) is alwaysApply: true — it is the
  always-on entry that points to masks, scripts and workspace.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

PRODUCT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (mdc source, output file, Trae CN name)
RULES = [
    ("discussion_assistant.mdc", "discussion-assistant.md", "discussion-assistant"),
    ("crew_assistant.mdc", "crew-assistant.md", "crew-assistant"),
    ("writer_assistant.mdc", "writer-assistant.md", "writer-assistant"),
    ("prompt_engineer_assistant.mdc", "prompt-engineer-assistant.md", "prompt-engineer-assistant"),
    ("spec_translator_assistant.mdc", "spec-translator-assistant.md", "spec-translator-assistant"),
    ("workflow_assistant.mdc", "workflow-assistant.md", "workflow-assistant"),
]

ROUTER = """---
name: cat-router
description: Cursor Agent Team (CAT) router — entry rule that routes work to the six role masks, scripts and ai_workspace. Applies to any repo with a cursor-agent-team/ checkout.
alwaysApply: true
---

# CAT Router (Trae CN)

This repo uses the Cursor Agent Team (CAT) framework. Rules for the six role
masks live as sibling rule files in `.trae/rules/`; activate by mask:

| Mask | Rule file | When |
|---|---|---|
| Discussion Partner | `discussion-assistant.md` | exploration, planning, topic tree |
| Crew Member | `crew-assistant.md` | plan execution |
| Writer | `writer-assistant.md` | prose compose (Draft → Review → Final) |
| Prompt Engineer | `prompt-engineer-assistant.md` | create/maintain roles |
| Spec Translator | `spec-translator-assistant.md` | spec translation |
| Workflow | `workflow-assistant.md` | workflow orchestration |

- Authoritative sources: `cursor-agent-team/_cursor/rules/*.mdc` and
  `cursor-agent-team/AGENTS-GUIDE.md`.
- State (single source of truth): `cursor-agent-team/ai_workspace/`
  (topic tree, plans, notes) — shared across Cursor / Trae CN / Claude Code.
- Skills are also installed at `.trae/skills/cursor-agent-team-*`.
"""


def parse_mdc(path: str) -> tuple[dict[str, str], str]:
    """Split a .mdc file into (frontmatter dict, body)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError(f"no frontmatter found in {path}")
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def render_rule(mdc: str, out_name: str, rule_name: str) -> str:
    src = os.path.join(PRODUCT_ROOT, "_cursor", "rules", mdc)
    fm, body = parse_mdc(src)
    desc = fm.get("description") or f"CAT mask rule {rule_name}"
    return (
        "---\n"
        f"name: {rule_name}\n"
        f"description: {desc}\n"
        "alwaysApply: false\n"
        "---\n"
        f"{body.rstrip()}\n"
    )


def targets() -> list[tuple[str, str]]:
    out = [(os.path.join("_trae_cn", "rules", "cat-router.md"), ROUTER)]
    for mdc, out_name, rule_name in RULES:
        out.append((
            os.path.join("_trae_cn", "rules", out_name),
            render_rule(mdc, out_name, rule_name),
        ))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    problems = []
    for rel, content in targets():
        path = os.path.join(PRODUCT_ROOT, rel)
        if args.check:
            if not os.path.isfile(path):
                problems.append(f"MISSING: {rel}")
            elif open(path, encoding="utf-8").read() != content:
                problems.append(f"DRIFT: {rel}")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"wrote {rel}")
    if args.check:
        if problems:
            print("Trae CN rules out of sync with .mdc sources:")
            for p in problems:
                print(f"  {p}")
            return 1
        print("OK: Trae CN rules match .mdc sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
