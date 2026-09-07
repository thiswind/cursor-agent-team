#!/usr/bin/env python3
"""Cat Write - The single write gateway to shared ai_workspace state (RFC-CONCURRENCY-001).

Design (owner ruling 2026-09-07 + dual-model consult 2026-09-08):
  - ALL writes to the shared state layer go through this script.
  - Serialization: ONE global flock (gateway lock) — writes are
    millisecond-scale; a single lock removes deadlock-ordering risk and
    covers the shared journal. Lock-wait time is journaled so per-target
    locks can be justified by data later (fable-5.1 position, adopted).
  - Atomic landing: write to temp file, then os.replace onto the target —
    concurrent READERS never see a half-written file.
  - Journal: every attempted write is appended (JSONL) under
    ai_workspace/temp/cat_write_journal/ — the audit trail that makes
    discipline violations detectable (git history vs journal cross-check).

Operations (whitelist — unregistered targets are REJECTED):
  notes --append   FILE MSG    append one line to ai_workspace/notes/FILE
  topic-round      FILE        replace the topic tree with FILE's content
                              (validates via validate_topic_tree first)
  plan-status      PLAN-ID ST  set/clear plan checkboxes by marker id
  index-rebuild                rebuild plans/INDEX.md from plan files

Usage:
  python cat_write.py notes --append project-x.md "message"
  python cat_write.py topic-round /tmp/tree_new.md [--force]
  python cat_write.py plan-status PLAN-V024-001 x2 done
  python cat_write.py index-rebuild
  python cat_write.py journal --tail 5
  python cat_write.py lock-wait-report

Exit codes: 0 ok, 1 rejected/failed, 2 usage error, 3 lock timeout.
"""

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPT_DIR.parent / "ai_workspace"
JOURNAL_DIR = WORKSPACE / "temp" / "cat_write_journal"
LOCK_PATH = WORKSPACE / "temp" / "cat_write.lock"
DEFAULT_WAIT = 30.0


# ---------------------------------------------------------------------------
# Gateway core: flock + journal + atomic replace
# ---------------------------------------------------------------------------

class GatewayLockTimeout(Exception):
    pass


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def journal_append(record: dict) -> None:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    month = datetime.now().strftime("%Y-%m")
    entry = dict(record)
    entry["ts"] = _now_iso()
    path = JOURNAL_DIR / f"journal-{month}.jsonl"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def gateway(wait: float):
    """Context manager: acquire the global gateway lock or time out."""
    import contextlib

    @contextlib.contextmanager
    def _ctx():
        WORKSPACE.joinpath("temp").mkdir(parents=True, exist_ok=True)
        fd = os.open(str(LOCK_PATH), os.O_RDWR | os.O_CREAT, 0o644)
        t0 = time.time()
        acquired = False
        try:
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except OSError:
                    if time.time() - t0 >= wait:
                        break
                    time.sleep(0.05)
            if not acquired:
                raise GatewayLockTimeout(
                    f"gateway lock not acquired within {wait}s")
            yield time.time() - t0
        finally:
            if acquired:
                fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    return _ctx()


def atomic_replace(path: Path, content: str) -> None:
    tmp = path.with_name(path.name + ".cat_write.tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(str(tmp), str(path))


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Operation: notes --append
# ---------------------------------------------------------------------------

def op_notes_append(args) -> dict:
    rel = args.file
    if rel.startswith("notes/"):
        rel = rel[len("notes/"):]
    if not rel or "/" in rel or rel.startswith("."):
        return {"ok": False, "errors": [
            "notes FILE must be a bare filename under ai_workspace/notes/ "
            f"(got: {args.file!r})"]}
    if not args.msg or not args.msg.strip():
        return {"ok": False, "errors": ["--append MSG must be non-empty"]}

    target = WORKSPACE / "notes" / rel
    target.parent.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"- [{stamp}] {args.msg.strip()}\n"

    with gateway(args.wait) as waited:
        old = target.read_text(encoding="utf-8") if target.exists() else ""
        if old and not old.endswith("\n"):
            old += "\n"
        new = old + line
        atomic_replace(target, new)
        journal_append({
            "op": "notes-append", "target": f"notes/{rel}",
            "wait_s": round(waited, 3), "md5_after": _md5(new),
        })
    return {"ok": True, "message": f"appended to notes/{rel}", "line": line.strip()}


# ---------------------------------------------------------------------------
# Operation: topic-round (validator reuse, function-level import)
# ---------------------------------------------------------------------------

def op_topic_round(args) -> dict:
    src = Path(args.file)
    if not src.is_file():
        return {"ok": False, "errors": [f"input file not found: {args.file}"]}

    try:
        import validate_topic_tree as vtt
    except Exception as e:  # pragma: no cover
        return {"ok": False, "errors": [f"validator import failed: {e}"]}

    new_content = src.read_text(encoding="utf-8")

    with gateway(args.wait) as waited:
        try:
            result = vtt.update_topic_tree(
                new_content, dry_run=False, force=args.force,
                strict=getattr(args, "strict", False))
        except Exception as e:
            journal_append({"op": "topic-round", "outcome": "crash",
                            "error": str(e), "wait_s": round(waited, 3)})
            return {"ok": False, "errors": [
                f"validator crashed (write rejected): {e}"]}

        journal_append({
            "op": "topic-round",
            "outcome": "ok" if result.get("success") else "rejected",
            "wait_s": round(waited, 3),
            "md5_after": _md5(new_content) if result.get("success") else None,
            "errors": result.get("errors", [])[:3],
        })
    return result


# ---------------------------------------------------------------------------
# Operation: plan-status
# ---------------------------------------------------------------------------

PLAN_STATES = {"todo", "in-progress", "done", "blocked"}
MARKER_RE = re.compile(r"^\s*-\s*\[([ xX~/!])\]\s*(.*)$")


def op_plan_status(args) -> dict:
    plan_id = args.plan_id
    marker = args.marker
    state = args.state
    if state not in PLAN_STATES and state != "clear":
        return {"ok": False, "errors": [
            f"state must be one of {sorted(PLAN_STATES)} or 'clear'"]}

    plan_path = None
    for cand in (WORKSPACE / "plans" / f"{plan_id}.md",
                 WORKSPACE / "plans" / plan_id,
                 WORKSPACE / "plans" / f"{plan_id.upper()}.md"):
        if cand.is_file():
            plan_path = cand
            break
    if plan_path is None:
        plans = sorted(p.stem for p in (WORKSPACE / "plans").glob("*.md")) \
            if (WORKSPACE / "plans").is_dir() else []
        return {"ok": False, "errors": [
            f"plan not found: {plan_id}", f"available: {', '.join(plans) or '(none)'}"]}

    target_char = {"todo": " ", "in-progress": "~", "done": "x",
                   "blocked": "!"}.get(state, None)

    lines = plan_path.read_text(encoding="utf-8").splitlines(keepends=True)
    hits, out = 0, []
    for ln in lines:
        m = MARKER_RE.match(ln.rstrip("\n"))
        if m and marker in m.group(2):
            hits += 1
            rest = m.group(2)
            if state == "clear":
                out.append(ln)
                continue
            new = re.sub(r"^\s*-\s*\[[ xX~/!]\]", f"- [{target_char}]", ln.rstrip("\n"))
            out.append(new + ("\n" if ln.endswith("\n") else ""))
        else:
            out.append(ln)

    if hits == 0:
        return {"ok": False, "errors": [
            f"no checklist line contains marker {marker!r} in {plan_path.name}"]}

    new_text = "".join(out)
    with gateway(args.wait) as waited:
        atomic_replace(plan_path, new_text)
        journal_append({
            "op": "plan-status", "target": f"plans/{plan_path.name}",
            "marker": marker, "state": state, "hits": hits,
            "wait_s": round(waited, 3), "md5_after": _md5(new_text),
        })
    return {"ok": True, "message": f"{plan_path.name}: {hits} line(s) -> [{state}]"}


# ---------------------------------------------------------------------------
# Operation: index-rebuild
# ---------------------------------------------------------------------------

def op_index_rebuild(args) -> dict:
    plans_dir = WORKSPACE / "plans"
    if not plans_dir.is_dir():
        return {"ok": False, "errors": ["no plans/ directory"]}

    rows = []
    for p in sorted(plans_dir.glob("*.md")):
        if p.name == "INDEX.md":
            continue
        text = p.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.*)$", text, re.M)
        title = m.group(1).strip() if m else p.stem
        s = re.search(r"\*\*Status\*\*:\s*([^\n(]+)", text)
        status = s.group(1).strip() if s else "unknown"
        d = re.search(r"\*\*Created\*\*:\s*(\d{4}-\d{2}-\d{2})", text)
        created = d.group(1) if d else ""
        link = p.name
        rows.append(f"| {link} | {title} | {status} | {created} |")

    content = (
        "# Plans Index (auto-generated — rebuild via cat_write.py index-rebuild)\n\n"
        "| File | Title | Status | Created |\n"
        "|---|---|---|---|\n" + "\n".join(rows) + "\n"
    )
    target = plans_dir / "INDEX.md"
    with gateway(args.wait) as waited:
        atomic_replace(target, content)
        journal_append({"op": "index-rebuild", "target": "plans/INDEX.md",
                        "rows": len(rows), "wait_s": round(waited, 3),
                        "md5_after": _md5(content)})
    return {"ok": True, "message": f"INDEX.md rebuilt ({len(rows)} plans)"}


# ---------------------------------------------------------------------------
# Read-only helpers: journal --tail, lock-wait-report
# ---------------------------------------------------------------------------

def op_journal(args) -> dict:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(JOURNAL_DIR.glob("journal-*.jsonl"))
    if not files:
        return {"ok": True, "entries": [], "message": "journal empty"}
    entries = []
    for f in files[-2:]:
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return {"ok": True, "entries": entries[-args.tail:]}


def op_lock_report(args) -> dict:
    files = sorted(JOURNAL_DIR.glob("journal-*.jsonl")) if JOURNAL_DIR.is_dir() else []
    waits, ops, slow = [], 0, []
    for f in files:
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "wait_s" in e:
                waits.append(e["wait_s"])
                ops += 1
                if e["wait_s"] >= 1.0:
                    slow.append({"ts": e.get("ts"), "op": e.get("op"),
                                 "wait_s": e["wait_s"]})
    return {
        "ok": True, "ops_with_wait": ops,
        "avg_wait_ms": round(1000 * sum(waits) / len(waits), 1) if waits else 0,
        "max_wait_s": max(waits) if waits else 0,
        "slow_writes_ge_1s": slow[-10:],
        "hint": "if avg wait stays <50ms, the global lock is fine; "
                "split per-target locks only if data says otherwise",
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Single write gateway to shared ai_workspace state",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--wait", type=float, default=DEFAULT_WAIT,
                   help=f"max seconds to wait for the gateway lock (default {DEFAULT_WAIT})")
    sub = p.add_subparsers(dest="op", required=True)

    sp = sub.add_parser("notes", help="append a line to ai_workspace/notes/FILE")
    sp.add_argument("--append", dest="msg", required=True, metavar="MSG")
    sp.add_argument("file", metavar="FILE")

    sp = sub.add_parser("topic-round", help="replace topic tree (validated)")
    sp.add_argument("file", metavar="FILE")
    sp.add_argument("--force", action="store_true")
    sp.add_argument("--strict", action="store_true")

    sp = sub.add_parser("plan-status", help="set plan checklist states")
    sp.add_argument("plan_id", metavar="PLAN-ID")
    sp.add_argument("marker", metavar="MARKER")
    sp.add_argument("state", metavar="STATE",
                    help="todo|in-progress|done|blocked|clear")

    sub.add_parser("index-rebuild", help="rebuild plans/INDEX.md")

    sp = sub.add_parser("journal", help="read the write journal")
    sp.add_argument("--tail", type=int, default=10)

    sub.add_parser("lock-wait-report", help="lock wait statistics")

    args = p.parse_args()

    try:
        if args.op == "notes":
            result = op_notes_append(args)
        elif args.op == "topic-round":
            result = op_topic_round(args)
        elif args.op == "plan-status":
            result = op_plan_status(args)
        elif args.op == "index-rebuild":
            result = op_index_rebuild(args)
        elif args.op == "journal":
            result = op_journal(args)
        elif args.op == "lock-wait-report":
            result = op_lock_report(args)
        else:  # pragma: no cover
            result = {"ok": False, "errors": [f"unknown op {args.op}"]}
    except GatewayLockTimeout as e:
        print(json.dumps({"ok": False, "errors": [str(e)]}, ensure_ascii=False))
        return 3

    print(json.dumps(result, ensure_ascii=False, indent=2,
                     default=str))
    ok = result.get("ok", result.get("success", False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
