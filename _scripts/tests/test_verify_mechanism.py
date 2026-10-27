#!/usr/bin/env python3
"""Tests for verify_mechanism.py (marker protocol v2, RFC-003)."""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(os.path.dirname(HERE), "verify_mechanism.py")


def run(piece, text, as_file=True, dirname=None):
    with tempfile.TemporaryDirectory() as td:
        if as_file:
            p = os.path.join(td, "archive.md")
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            p = os.path.join(td, dirname or "reads")
            os.makedirs(os.path.join(p), exist_ok=True)
            with open(os.path.join(p, "ledger.md"), "w", encoding="utf-8") as f:
                f.write(text)
        r = subprocess.run([sys.executable, SCRIPT, piece, p, "--json"],
                           capture_output=True, text=True)
        import json
        return json.loads(r.stdout)


def test_write_pass_valid():
    text = (
        "WRITE-GATE: PASS\n"
        "## 视角\n- V1 清晰性\n- V2 简洁性\n"
        "[轮1·V1] 本稿要点…\n[轮1·V2] …\n"
        "[轮2·V1] 新发现:…\n[轮2·V2] 无增量\n"
        "CONVERGED: R2\n## 对照\n吻合 ✓\n"
    )
    r = run("write", text)
    assert r["valid"], r


def test_write_missing_gate():
    r = run("write", "[轮1·V1] x\nCONVERGED: R2\n")
    assert not r["valid"]
    assert any("M1" in e for e in r["errors"])


def test_write_wrong_prefix():
    r = run("write", "READ-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\nCONVERGED: R2\n")
    assert not r["valid"]


def test_write_single_round_banned():
    r = run("write", "WRITE-GATE: PASS\n[轮1·V1] x\nCONVERGED: R2\n")
    assert not r["valid"]
    assert any("single-round" in e for e in r["errors"])


def test_write_converged_r1_banned():
    r = run("write", "WRITE-GATE: PASS\n[轮1·V1] x\nCONVERGED: R1\n")
    assert not r["valid"]


def test_write_no_convergence():
    r = run("write", "WRITE-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\n")
    assert not r["valid"]
    assert any("M3" in e for e in r["errors"])


def test_write_budget_valid():
    r = run("write",
            "WRITE-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\n"
            "BUDGET: R2(时间预算耗尽, 采纳当前稿)\n")
    assert r["valid"], r


def test_write_skip_ok_no_loop():
    r = run("write", "WRITE-GATE: SKIP(随手笔记)\n直接写的内容。\n")
    assert r["valid"], r


def test_write_skip_with_convergence_is_error():
    r = run("write", "WRITE-GATE: SKIP(x)\nCONVERGED: R2\n")
    assert not r["valid"]


def test_write_converged_exceeds_rounds():
    r = run("write", "WRITE-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\nCONVERGED: R3\n")
    assert not r["valid"]


def test_write_dual_convergence_error():
    r = run("write",
            "WRITE-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\n"
            "CONVERGED: R2\nBUDGET: R2(z)\n")
    assert not r["valid"]


def test_read_dir_archive_valid():
    text = (
        "READ-GATE: PASS\n"
        "[轮1·V1] 提取:…\n[轮1·V2] …\n"
        "[轮2·V1] 新发现:…\n[轮2·V2] 无增量\n"
        "CONVERGED: R2\n## 对照\n吻合 ✓ / 缺失 ✗\n行动项…\n"
    )
    r = run("read", text, as_file=False)
    assert r["valid"], r


def test_read_single_round_banned():
    r = run("read", "READ-GATE: PASS\n[轮1·V1] x\nCONVERGED: R2\n", as_file=False)
    assert not r["valid"]


def test_read_skip_ok():
    r = run("read", "READ-GATE: SKIP(查单一事实)\n单遍笔记\n", as_file=False)
    assert r["valid"], r


# --- S-1 fix (v0.25.1): LANDED proof line, warning-level ---

def test_write_no_landed_warns():
    r = run("write",
            "WRITE-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\nCONVERGED: R2\n")
    assert r["valid"], r  # still valid — warning only
    assert any("S1" in w for w in r["warnings"])


def test_write_landed_no_warn():
    r = run("write",
            "WRITE-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\nCONVERGED: R2\n"
            "LANDED: p1_archive.md verified-by-read-back\n")
    assert r["valid"], r
    assert not any("S1" in w for w in r["warnings"])


def test_read_landed_no_warn():
    r = run("read",
            "READ-GATE: PASS\n[轮1·V1] x\n[轮2·V1] y\nCONVERGED: R2\n"
            "## 对照\n吻合 ✓\nLANDED: reads/p1_read verified-by-read-back\n",
            as_file=False)
    assert r["valid"], r
    assert not any("S1" in w for w in r["warnings"])
