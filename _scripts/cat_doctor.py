#!/usr/bin/env python3
"""Cat Doctor - Cold-start & deployment health check for CAT (G9).

One command, four checks (AGENTS-GUIDE sec.5.2 table, machine-run):

  form      : which deployment shape is this host (plain dir / submodule /
              orphan pseudo-submodule)
  version   : installed VERSION vs git tag/HEAD info + staleness hint
  ignore    : is the state layer tracked by git? (policy check against the
              v0.24.0 whitelist default: state TRACKED, notes excluded)
  orphans   : nested .git leftovers / gitlink mismatch (FR-0021 class)

  --fleet HOST_ROOTS   run against a list of host repo roots, read-only,
                       tabular summary (for the workshop fleet audit)

Usage:
  python cat_doctor.py                    # check this host (workshop/product)
  python cat_doctor.py --root /path/to/host
  python cat_doctor.py --fleet /path/a /path/b ...
  python cat_doctor.py --json

Exit codes: 0 all critical ok (warnings allowed), 1 any critical issue.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PRODUCT = Path(__file__).resolve().parent.parent


def run_git(cwd, *args):
    try:
        r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                           text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def detect_form(host_root: Path, cat_dir_name="cursor-agent-team"):
    """Return (form, detail) for the CAT installation shape."""
    cat = host_root / cat_dir_name
    if not cat.is_dir():
        return ("absent", f"no {cat_dir_name}/ directory")
    nested_git = cat / ".git"
    if nested_git.is_file():
        return ("submodule", "nested .git is a gitfile (proper submodule/worktree)")
    gitmodules = host_root / ".gitmodules"
    has_gitmodules_entry = False
    if gitmodules.is_file():
        gm_text = gitmodules.read_text(encoding="utf-8", errors="replace")
        # match a path entry for this dir, not a mere substring mention
        # (e.g. a "release" submodule pointing at the same product repo
        # mentions cursor-agent-team only in its URL)
        for line in gm_text.splitlines():
            s = line.strip()
            if s.startswith("path") and "=" in s:
                if s.split("=", 1)[1].strip().strip('"') == cat_dir_name:
                    has_gitmodules_entry = True
    host_git = host_root / ".git"

    if nested_git.is_dir():
        if host_git.is_dir() or host_git.is_file():
            link = run_git(host_root, "ls-files", "-s", "--", cat_dir_name)
            if link and "160000" in link:
                return ("submodule", "gitlink 160000 present (submodule registered)")
        if has_gitmodules_entry:
            return ("orphan-pseudo-submodule",
                    ".gitmodules entry + nested .git dir but no gitlink — orphan "
                    "(FR-0021 class; host git ignores its contents)")
        return ("nested-independent-repo",
                "nested full .git without gitlink — treated as plain untracked dir by host git")

    # no nested .git at all
    if host_git.is_dir() or host_git.is_file():
        link = run_git(host_root, "ls-files", "-s", "--", cat_dir_name)
        if link and "160000" in link:
            return ("submodule", "gitlink 160000 present but nested .git missing — "
                    "broken submodule (run git submodule update)")
    if has_gitmodules_entry:
        return ("orphan-pseudo-submodule",
                ".gitmodules entry exists but neither gitlink nor nested .git — "
                "orphan dir (FR-0021 class)")
    return ("plain-dir", "no nested .git — plain tracked directory (workshop shape)")


def check_version(cat_root: Path):
    vfile = cat_root / "VERSION"
    version = vfile.read_text(encoding="utf-8").strip() if vfile.is_file() else "unknown"
    tag = run_git(cat_root, "describe", "--tags", "--abbrev=0") if (cat_root / ".git").exists() else None
    dirty = False
    if (cat_root / ".git").exists():
        st = run_git(cat_root, "status", "--porcelain")
        dirty = bool(st)
    detail = f"VERSION={version}" + (f", last-tag={tag}" if tag else "") + \
             (", working-tree dirty" if dirty else "")
    warn = None
    if tag and version not in tag:
        warn = f"VERSION file ({version}) and git tag ({tag}) disagree"
    return {"version": version, "tag": tag, "dirty": dirty, "detail": detail,
            "warning": warn}


def check_ignore(host_root: Path, cat_dir_name="cursor-agent-team"):
    """State-layer tracking check (v0.24.0 whitelist default)."""
    ws = host_root / cat_dir_name / "ai_workspace"
    if not ws.is_dir():
        return {"tracked": None, "detail": "no ai_workspace/"}
    tracked = run_git(host_root, "ls-files", "--",
                      f"{cat_dir_name}/ai_workspace")
    n = len([l for l in (tracked or "").splitlines() if l.strip()])
    nested_ignore = host_root / cat_dir_name / ".gitignore"
    policy = "unknown"
    if nested_ignore.is_file():
        gi = nested_ignore.read_text(encoding="utf-8")
        if "CAT STATE LAYER" in gi:
            policy = "whitelist-v0.24"
        elif "ai_workspace/**" in gi:
            policy = "legacy-ignore-all"
    status = "ok" if n > 0 else ("warn" if policy == "legacy-ignore-all" else "critical")
    return {"tracked_files": n, "policy": policy, "status": status,
            "detail": f"{n} state files tracked; .gitignore policy={policy}"}


def check_orphans(host_root: Path, cat_dir_name="cursor-agent-team"):
    issues = []
    host_git = host_root / ".git"
    if not (host_git.is_dir() or host_git.is_file()):
        return {"issues": [], "detail": "host is not a git repo"}
    ls = run_git(host_root, "ls-files", "-s") or ""
    cat_links = [l for l in ls.splitlines()
                 if l.startswith("160000") and cat_dir_name in l]
    gitmodules_cat = False
    if (host_root / ".gitmodules").is_file():
        gm = (host_root / ".gitmodules").read_text(encoding="utf-8")
        for ln in gm.splitlines():
            s = ln.strip()
            if s.startswith("path") and "=" in s:
                if s.split("=", 1)[1].strip() == cat_dir_name:
                    gitmodules_cat = True
    if gitmodules_cat and not cat_links:
        if not (host_root / cat_dir_name / ".git").exists():
            issues.append(".gitmodules mentions CAT but no gitlink and no nested .git — orphan")
    if (host_root / cat_dir_name / ".git").is_dir() and cat_links:
        issues.append("both nested .git dir and gitlink present — ambiguous shape")
    return {"issues": issues,
            "detail": f"gitlinks={len(cat_links)}; issues={len(issues)}"}


def doctor(host_root: Path, json_out=False):
    host_root = host_root.resolve()
    cat = host_root / "cursor-agent-team"
    cat = cat if cat.is_dir() else (PRODUCT if PRODUCT.name == "cursor-agent-team" else cat)
    cat_root = cat.resolve()

    form, form_detail = detect_form(host_root)
    ver = check_version(cat_root)
    ign = check_ignore(host_root)
    orph = check_orphans(host_root)

    criticals = []
    if form in ("orphan-pseudo-submodule", "absent"):
        criticals.append(f"form={form}")
    if ign["status"] == "critical":
        criticals.append("state layer not tracked (legacy ignore-all)")
    if orph["issues"]:
        criticals.append("orphan/ambiguous shape detected")

    result = {
        "host": str(host_root), "form": form, "form_detail": form_detail,
        "version": ver, "ignore": ign, "orphans": orph,
        "criticals": criticals, "ok": not criticals,
    }

    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "OK" if result["ok"] else "ISSUES"
        print(f"cat_doctor: {status}  (host: {host_root})")
        print(f"  form    : {form} — {form_detail}")
        print(f"  version : {ver['detail']}" + (f"  [WARN {ver['warning']}]" if ver['warning'] else ""))
        print(f"  ignore  : {ign['detail']}  [{ign['status']}]")
        print(f"  orphans : {orph['detail']}")
        for c in criticals:
            print(f"  CRITICAL: {c}")
    return result


def fleet(roots, json_out=False):
    rows, all_ok = [], True
    for r in roots:
        res = doctor(Path(r), json_out=False)
        all_ok = all_ok and res["ok"]
        rows.append(res)
    if json_out:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(f"{'HOST':<42} {'FORM':<28} {'VER':<9} {'IGNORE':<9} OK")
        for r in rows:
            print(f"{r['host']:<42} {r['form']:<28} "
                  f"{(r['version']['version'] or '?')[:8]:<9} "
                  f"{r['ignore']['status']:<9} {'yes' if r['ok'] else 'NO'}")
    return all_ok, rows


def main() -> int:
    p = argparse.ArgumentParser(description="CAT cold-start & deployment health check")
    p.add_argument("--root", help="host repo root (default: this product's parent)")
    p.add_argument("--fleet", nargs="+", metavar="HOST_ROOT",
                   help="audit multiple host roots (read-only)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.fleet:
        ok, _ = fleet(args.fleet, args.json)
        return 0 if ok else 1
    root = Path(args.root) if args.root else PRODUCT.parent
    res = doctor(root, args.json)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
