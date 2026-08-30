#!/usr/bin/env python3
"""
Build Commands - Generate all platform command artifacts from commands.yaml.

Single source of truth workflow:

    python3 _scripts/build_commands.py            # regenerate all artifacts
    python3 _scripts/build_commands.py --check    # verify no drift (CI gate)

Artifacts generated per command (based on `platforms` in commands.yaml):
    cursor : _cursor/commands/{name}.md
    claude : _claude/commands/{name}.md
    trae   : _trae_solo/commands/{name}.md

Host-agnostic frontier-agent skills (generated for every command with a
`skill` block, regardless of platform — since v0.22.0):
    skills : _skills/{skill-slug}/SKILL.md
    skills : _skills/cursor-agent-team/SKILL.md  (master routing skill)

Every generated command embeds:
    - the Output Markers requirement (phase_marker.py contract)
    - the Response Self-Verification step (verify_response.py closed loop)

Generated files start with a "do not edit" header. Edit commands.yaml instead.
"""

import argparse
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

PRODUCT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_PATH = os.path.join(PRODUCT_ROOT, "commands.yaml")

GENERATED_HEADER = (
    "<!-- Generated from commands.yaml by _scripts/build_commands.py — "
    "do not edit by hand. Edit commands.yaml and regenerate. -->"
)

VERIFY_SCRIPT = "cursor-agent-team/_scripts/verify_response.py"
MARKER_SCRIPT = "cursor-agent-team/_scripts/phase_marker.py"
VERIFY_TEMP_FILE = "cursor-agent-team/ai_workspace/scratchpad/temp/response_last.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def to_python(text: str) -> str:
    """Convert canonical `python3` invocations to `python` (Cursor/TRAE style)."""
    return text.replace("python3 ", "python ")


def parse_history_head(line: str):
    """Parse 'v1.2.0 (2026-08-16): description' into (version, date)."""
    m = re.match(r"^(v[\d.]+) \((\d{4}-\d{2}-\d{2})\):", line)
    return (m.group(1), m.group(2)) if m else ("", "")


def markers_block(phases: int) -> str:
    return (
        "**Output Markers (HARD REQUIREMENT)**:\n"
        "- After each Phase N completes, review the phase output against that "
        "phase's requirements. If it passes, run "
        f"`python {MARKER_SCRIPT} <N> true` and use the script's **single line "
        "of stdout** as that phase's completion marker; if not, run "
        "`... phase_marker.py <N> false` and redo or explain.\n"
        f"- The response must contain all {phases} markers (one per phase), "
        "with format exactly as script output; do **not** type "
        "`[Phase N DONE]` by hand. Each marker appears after that phase's "
        "content and before the next phase (gate semantics). Missing markers "
        "= invalid response."
    )


def verification_block(phases: int, python3: bool) -> str:
    exe = "python3" if python3 else "python"
    return (
        "**Response Self-Verification (HARD REQUIREMENT)**:\n"
        "- Before sending the response, save the complete response text to "
        f"`{VERIFY_TEMP_FILE}`, then run:\n"
        f"  ```bash\n  {exe} {VERIFY_SCRIPT} --phases {phases} --file {VERIFY_TEMP_FILE}\n  ```\n"
        "- If the check reports INVALID: fix the reported errors and "
        "re-verify. Never send an unverified response."
    )


def phase_body(ph, python3: bool) -> str:
    body = ph["body"].rstrip()
    return body if python3 else to_python(body)


def history_footer(cmd) -> str:
    version, date = parse_history_head(cmd["history"][0])
    lines = [f"- {h}" for h in cmd["history"]]
    return (
        f"{GENERATED_HEADER}\n\n"
        f"**Version**: {version} (Updated: {date})\n\n"
        "**Version History**:\n" + "\n".join(lines)
    )


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def render_cursor(cmd) -> str:
    n = cmd["phases"]
    out = []
    out.append(f"# {cmd['title']} Command")
    out.append(
        f"**Core Philosophy**: Commands are like \"masks\" — when you wear "
        f"the `/{cmd['name']}` mask, you play the role of a "
        f"**{cmd['role']}**, {cmd['role_summary']}."
    )
    out.append("## Usage")
    out.append("\n".join(f"- {u}" for u in cmd["usage"]))
    out.append(f"**Key Principle**: {cmd['key_principle']}")
    for body in (cmd.get("extra_sections") or {}).values():
        out.append(body.rstrip())
    out.append(f"## Workflow ({n}-Phase)")
    if cmd.get("mandatory_note"):
        out.append(f"**MANDATORY**: {cmd['mandatory_note']}")
    out.append(markers_block(n))
    out.append(verification_block(n, python3=False))
    for ph in cmd["phase_list"]:
        out.append("---")
        out.append(f"### Phase {ph['n']}: {ph['title']}")
        out.append(phase_body(ph, python3=False))
    out.append("---")
    out.append("## Example")
    out.append("```\n" + cmd["example"].strip() + "\n```")
    out.append("---")
    out.append(history_footer(cmd))
    return "\n\n".join(out) + "\n"


def render_claude(cmd) -> str:
    n = cmd["phases"]
    out = []
    out.append(f"# {cmd['title']} Mask")
    out.append(
        f"You are wearing the `/{cmd['name']}` mask inside the current "
        "Claude Code conversation."
    )
    out.append("## Core Principle")
    out.append(
        "This is a mask system, not a multi-agent handoff. Use the full "
        "prior conversation as shared meeting-room context. Do not delegate "
        "to a subagent just to become this role."
    )
    out.append(f"Role: **{cmd['role']}**. {cmd['claude_role_line']}")
    out.append("Arguments: `$ARGUMENTS`")
    out.append("## Hard Constraints")
    out.append("\n".join(f"- {c}" for c in cmd["hard_constraints"]))
    for body in (cmd.get("claude_extra_sections") or {}).values():
        out.append(body.rstrip())
    if cmd.get("mandatory_note"):
        out.append(f"**Phase mapping**: {cmd['mandatory_note']}")
    out.append("## Workflow")
    for ph in cmd["phase_list"]:
        out.append(f"### Phase {ph['n']}: {ph['title']}")
        out.append(phase_body(ph, python3=True))
        out.append(
            "End with:\n```bash\n"
            f"python3 {MARKER_SCRIPT} {ph['n']} true\n```\n"
            "\nUse the script stdout as the marker."
        )
    out.append(
        "## Output Rule\n"
        "Each completed phase must include the exact marker produced by "
        "`phase_marker.py`. If the script cannot run, use `[Phase N DONE]` "
        "as fallback and state why."
    )
    out.append(f"## Response Self-Verification (HARD REQUIREMENT)\n" +
               verification_block(n, python3=True).split("\n", 1)[1].lstrip("\n"))
    out.append("## Example Usage")
    out.append("```\n" + cmd["example"].strip() + "\n```")
    out.append("---")
    out.append(history_footer(cmd))
    return "\n\n".join(out) + "\n"


def render_trae(cmd) -> str:
    n = cmd["phases"]
    skill = cmd.get("skill") or {}
    description = skill.get("description") or cmd["role_summary"]
    description = " ".join(description.split())
    out = []
    out.append(f"---\nname: {cmd['name']}\ndescription: {description}\n---")
    out.append(
        f"You are now a **{cmd['role']}**, part of the cursor-agent-team "
        "framework."
    )
    out.append("## Core Principles")
    out.append("\n".join(f"- {c}" for c in cmd["hard_constraints"]))
    out.append(f"## Workflow ({n}-Phase)")
    out.append(
        f"Every message must execute the complete {n}-phase workflow — "
        "no skipping, no merging."
    )
    out.append(f"## Phase Markers (HARD REQUIREMENT)\n"
               f"- After each Phase N completes, run `python {MARKER_SCRIPT} <N> true` "
               "and use the script's single line of stdout as the completion marker\n"
               f"- The response must contain all {n} markers, with format exactly as "
               "script output; do not type [Phase N DONE] manually\n"
               "- Each marker appears after that phase's content and before the next "
               "phase. Missing markers = invalid response")
    verify = verification_block(n, python3=False).split("\n", 1)[1].lstrip("\n")
    out.append("## Response Self-Verification (HARD REQUIREMENT)\n" + verify)
    for ph in cmd["phase_list"]:
        out.append(f"## Phase {ph['n']}: {ph['title']}")
        out.append(phase_body(ph, python3=False))
    out.append(
        "## Note\n"
        "The workspace at `cursor-agent-team/ai_workspace/` is shared "
        "between Cursor and TRAE SOLO."
    )
    out.append("---\n" + history_footer(cmd))
    return "\n\n".join(out) + "\n"


def skill_slug(cmd) -> str:
    return f"cursor-agent-team-{cmd['name']}"


def render_skill(cmd) -> str:
    """Host-agnostic frontier-agent skill (since v0.22.0).

    Thin orchestration layer: YAML frontmatter for host auto-discovery,
    trigger self-check, SSOT pointers into the repo, the mask's operating
    loop, and the machine-checked output contract.
    """
    skill = cmd["skill"]
    name = cmd["name"]
    rules_files = skill.get("rules_files") or []
    triggers_flat = "; ".join(
        t.replace("`", "") for t in skill["triggers"]
    )
    fm_desc = " ".join(
        (
            skill["description"].strip(),
            f"Invoke when the working repo has a cursor-agent-team/ checkout "
            f"and the request matches: {triggers_flat}.",
            "Frontier agents may adopt this mask unprompted when the request "
            "clearly fits (self-assembly).",
        )
    )
    out = []
    out.append(
        "---\n"
        f"name: {skill_slug(cmd)}\n"
        f'description: "{fm_desc}"\n'
        "---"
    )
    out.append(f"# CAT Skill — {skill['name']}")
    out.append(
        "> One of the six role masks of Cursor Agent Team (CAT), packaged as "
        "a host-agnostic skill. This file is a **thin orchestration layer**: "
        "it tells you when and how to adopt the mask; the authoritative "
        "behavioral detail lives in the repo (SSOT pointers below). "
        "Adopting it is your call — use the mask when the work merits it, "
        "skip it for one-shot asks."
    )
    out.append("## 0. Trigger self-check (before acting)")
    out.append(
        "Adopt this mask only if **both** hold:\n"
        "1. The project root contains `cursor-agent-team/` (CAT installed as "
        "a submodule — this skill's scripts and workspace live there). "
        "**If not: do not act on this skill**; tell the user CAT is not "
        "installed in this repo and stop.\n"
        f"2. The request matches this mask: {triggers_flat}."
    )
    out.append("## 1. Authoritative sources (read before behaving)")
    pointers = [
        f"- Command definition: `cursor-agent-team/_cursor/commands/{name}.md`"
    ]
    for rf in rules_files:
        pointers.append(f"- Rules: `cursor-agent-team/_cursor/rules/{rf}`")
    pointers.append(
        "- Full persona map & discipline layer: "
        "`cursor-agent-team/AGENTS-GUIDE.md` §1"
    )
    out.append("\n".join(pointers))
    out.append("## 2. Mask contract")
    out.append("\n".join(f"- {b}" for b in skill["behavior"]))
    out.append("## 3. Operating loop")
    out.append("\n".join(f"{i}. {s}" for i, s in enumerate(skill["steps"], 1)))
    out.append(
        "## 4. Output contract (machine-checked)\n"
        "- End every long-form response with the phase-marker gates "
        f"(all {cmd['phases']} phases, emitted via "
        "`cursor-agent-team/_scripts/phase_marker.py`, never typed by hand).\n"
        "- Close the loop with "
        "`cursor-agent-team/_scripts/verify_response.py` before sending."
    )
    out.append("## Dependencies")
    out.append("\n".join(f"- {d}" for d in skill["dependencies"]))
    out.append("## Notes")
    out.append("\n".join(f"- {note}" for note in skill["notes"]))
    out.append("---\n" + history_footer(cmd))
    return "\n\n".join(out) + "\n"


def render_master_skill(commands, master) -> str:
    """Master routing skill: the frontier agent's front door to CAT."""
    fm_desc = " ".join(
        (
            master["description"].strip(),
            "Invoke when: the working repo has a cursor-agent-team/ checkout; "
            "a frontier agent starts or continues work there; the user "
            "mentions CAT, role masks, crew, discussion tree, ai_workspace, "
            "or sub-agent dispatch.",
        )
    )
    rows = []
    for name, cmd in commands.items():
        summary = " ".join((cmd.get("role_summary") or "").split())
        rows.append(f"| `{name}` | {cmd['role']} | {summary} |")
    table = "\n".join(rows)
    out = []
    out.append(
        "---\n"
        f"name: {master['name']}\n"
        f'description: "{fm_desc}"\n'
        "---"
    )
    out.append("# CAT — Master Routing Skill (frontier-agent front door)")
    out.append(
        "> Cursor Agent Team (CAT): one conversation, six role masks, no "
        "orchestrator swarm. This skill is the **router** — it tells you "
        "which mask to wear and where the authoritative protocols live. "
        "Per-mask skills (`cursor-agent-team-<mask>`) exist for deeper "
        "engagement."
    )
    out.append("## 0. Trigger self-check (before acting)")
    out.append(
        "Engage CAT only if the project root contains `cursor-agent-team/`. "
        "**If not: do not act**; tell the user CAT is not installed and stop."
    )
    out.append("## 1. Autonomy (core principle)")
    out.append(
        "CAT is an **optional toolbox** for you, not a per-turn obligation. "
        "This skill's job is to tell you the toolbox exists, where it lives, "
        "and how to use it — nothing more. Whether and when to use it is "
        "**your call**."
    )
    out.append(
        "Worth reaching for when: the project has a HANDOFF.md or topic "
        "tree you need to continue; this turn's output is a decision, "
        "conclusion, or long text worth preserving for later sessions; the "
        "task is multi-stage or spans sessions; the user explicitly asks "
        "for CAT or a mask.\n"
        "Skip it when: one-shot answers, small fixes, chatter — ceremonial "
        "bookkeeping for its own sake buys nothing; just do the work."
    )
    out.append(
        "What the toolbox gives you: cross-session memory "
        "(`ai_workspace/`: topic tree, deep notes, plans, constraints), "
        "six pre-built persona/flow configurations (the masks), "
        "machine-checked verification scripts, and a lookup path into "
        "project history (`discussion_topics.md` × `git log`)."
    )
    out.append("## 2. Cold-start reading order")
    out.append(
        "1. `cursor-agent-team/AGENTS-GUIDE.md` — persona map, scripts "
        "reference, ai_workspace usage, session handoff pattern\n"
        "2. `cursor-agent-team/SUBAGENT-DISPATCH.md` — if you will dispatch "
        "mid-tier sub-agents\n"
        "3. Project-root `HANDOFF.md` — current state snapshot (if present)\n"
        "4. `cursor-agent-team/ai_workspace/discussion_topics.md` — timeline\n"
        "5. `git log --oneline -10` — trust the disk, not memory"
    )
    out.append("## 3. Mask selection (when to wear which)")
    out.append(
        "| Mask | Role | One-line duty |\n|------|------|---------------|\n"
        + table
    )
    out.append(
        "Selection rules and the discipline layer (history handling, "
        "gleaning, TTS, workspace writes) live in `AGENTS-GUIDE.md` §1 — "
        "read it once, apply always."
    )
    out.append(
        "## 4. Hard rules (non-negotiable, all masks)\n"
        "1. Workspace writes go under `cursor-agent-team/ai_workspace/` "
        "only.\n"
        "2. The topic tree is modified only via "
        "`python cursor-agent-team/_scripts/validate_topic_tree.py` "
        "— never by hand.\n"
        "3. Serious work products are written to files first, then "
        "summarized in chat (path pointers, not dumps).\n"
        "4. Phase markers (`phase_marker.py`) and response "
        "self-verification (`verify_response.py`) are machine-checked "
        "contracts."
    )
    out.append(
        "## 5. Sub-agent control mode (hard for downstream — your "
        "optional lever)\n"
        "When you (the frontier agent) dispatch sub-agents, you may put a "
        "mask on them and **enforce the CAT pipeline**. This is CAT's "
        "control power: autonomous toward upstream, controllable toward "
        "downstream.\n\n"
        "Inject three things into the dispatch prompt (template):\n\n"
        "```text\n"
        "[CAT mask] Your role: <mask> "
        "(discuss/crew/prompt_engineer/spec_translator/writer/workflow)\n"
        "[CAT behavior] Read cursor-agent-team/_claude/commands/<mask>.md "
        "(or _cursor/rules/<mask>.mdc); follow its persona and flow\n"
        "[CAT output contract] Write outputs under "
        "cursor-agent-team/ai_workspace/ (notes/scratchpad/plans as "
        "needed); on stage completion run "
        "`python cursor-agent-team/_scripts/phase_marker.py <N> true`; "
        "self-verify with verify_response.py before responding; report "
        "pointers, not dumps\n"
        "```\n\n"
        "Where the control comes from: the mask fixes behavior → outputs "
        "are **predictable in form**; forced on-disk outputs → you can "
        "**audit the work site** anytime; machine-checked contracts → "
        "claims of \"done\" carry **verifiable evidence**, not "
        "self-report. For deeper mechanics (parallel sub-agents, domain "
        "splits, surgical dispatch protocol) read "
        "`cursor-agent-team/SUBAGENT-DISPATCH.md`.\n\n"
        "Using it is also your call: simple subtasks can be dispatched "
        "bare; the control mode pays off for multi-step, "
        "hard-to-verify, or audit-worthy work."
    )
    out.append(
        "## 6. Relation to slash commands\n"
        "Human operators keep the `/crew`, `/discuss`, ... slash commands "
        "(mid-tier path). Skills are the frontier-agent path: same six "
        "masks, self-assembled per turn instead of harness-injected."
    )
    out.append("---\n" + history_footer({"history": master["history"]}))
    return "\n\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Targets and main
# ---------------------------------------------------------------------------

def targets_for(cmd):
    """Return [(relative_path, rendered_content), ...] for a command."""
    name = cmd["name"]
    targets = []
    if "cursor" in cmd["platforms"]:
        targets.append((f"_cursor/commands/{name}.md", render_cursor(cmd)))
    if "claude" in cmd["platforms"]:
        targets.append((f"_claude/commands/{name}.md", render_claude(cmd)))
    if "trae" in cmd["platforms"]:
        targets.append((f"_trae_solo/commands/{name}.md", render_trae(cmd)))
    if cmd.get("skill"):
        targets.append((
            f"_skills/{skill_slug(cmd)}/SKILL.md",
            render_skill(cmd),
        ))
    return targets


def all_targets(commands, master_skill=None):
    result = []
    for cmd in commands.values():
        result.extend(targets_for(cmd))
    if master_skill:
        result.append((
            f"_skills/{master_skill['name']}/SKILL.md",
            render_master_skill(commands, master_skill),
        ))
    return result


def expected_dirs():
    return [
        "_cursor/commands",
        "_claude/commands",
        "_trae_solo/commands",
        "_skills",
    ]


def find_extra_files(root, known_rel_paths):
    """Detect unexpected generated-looking files in the managed directories."""
    known = set(known_rel_paths)
    extras = []
    for d in expected_dirs():
        abs_dir = os.path.join(root, d)
        if not os.path.isdir(abs_dir):
            continue
        for base, _dirs, files in os.walk(abs_dir):
            for f in files:
                if not f.endswith(".md"):
                    continue
                abs_path = os.path.join(base, f)
                rel = os.path.relpath(abs_path, root)
                if rel not in known:
                    extras.append(rel)
    return sorted(extras)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate platform command artifacts from commands.yaml")
    parser.add_argument("--check", action="store_true",
                        help="verify artifacts match commands.yaml; exit 1 on drift")
    parser.add_argument("--out-dir", help="write artifacts under this root instead of the product root")
    parser.add_argument("--list", action="store_true", help="list target files")
    args = parser.parse_args()

    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    commands = doc["commands"]
    master_skill = doc.get("master_skill")

    targets = all_targets(commands, master_skill)
    root = args.out_dir or PRODUCT_ROOT

    if args.list:
        for rel, _content in targets:
            print(rel)
        return 0

    if args.check:
        known = [rel for rel, _ in targets]
        problems = []
        for rel, content in targets:
            path = os.path.join(root, rel)
            if not os.path.isfile(path):
                problems.append(f"MISSING: {rel}")
                continue
            with open(path, "r", encoding="utf-8") as f:
                if f.read() != content:
                    problems.append(f"DRIFT: {rel}")
        for rel in find_extra_files(root, known):
            problems.append(f"EXTRA: {rel}")
        if problems:
            print("Artifacts out of sync with commands.yaml:")
            for p in problems:
                print(f"  {p}")
            print("Fix: python3 _scripts/build_commands.py")
            return 1
        print(f"OK: all {len(known)} artifacts match commands.yaml")
        return 0

    written = 0
    for rel, content in targets:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        written += 1
        print(f"wrote {rel}")
    print(f"Done: {written} artifacts generated from commands.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
