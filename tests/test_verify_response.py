"""Tests for verify_response.py — closed-loop phase marker validation."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_scripts"))

from verify_response import verify  # noqa: E402


def make_response(phases=4, text="Some content.\n"):
    return "\n".join(f"{text}[Phase {i} DONE]" for i in range(phases))


class TestVerifyResponse(unittest.TestCase):

    def test_valid_four_phase_response(self):
        result = verify(make_response(4), 4)
        self.assertTrue(result["valid"])
        self.assertEqual(result["markers_found"], 4)
        self.assertEqual(result["errors"], [])

    def test_valid_five_phase_response(self):
        result = verify(make_response(5), 5)
        self.assertTrue(result["valid"])

    def test_missing_marker(self):
        text = make_response(4).replace("[Phase 2 DONE]\n", "").replace("[Phase 2 DONE]", "")
        result = verify(text, 4)
        self.assertFalse(result["valid"])
        self.assertTrue(any("missing marker: [Phase 2 DONE]" in e for e in result["errors"]))

    def test_duplicate_marker(self):
        text = make_response(4) + "\n[Phase 0 DONE]"
        result = verify(text, 4)
        self.assertFalse(result["valid"])
        self.assertTrue(any("duplicate marker" in e for e in result["errors"]))

    def test_out_of_order_markers(self):
        text = "[Phase 1 DONE]\n[Phase 0 DONE]\n[Phase 2 DONE]\n[Phase 3 DONE]"
        result = verify(text, 4)
        self.assertFalse(result["valid"])
        self.assertTrue(any("out of order" in e for e in result["errors"]))

    def test_not_done_marker_fails(self):
        text = make_response(4).replace("[Phase 2 DONE]", "[Phase 2 NOT DONE]")
        result = verify(text, 4)
        self.assertFalse(result["valid"])
        self.assertTrue(any("NOT DONE" in e for e in result["errors"]))
        self.assertTrue(any("missing marker: [Phase 2 DONE]" in e for e in result["errors"]))

    def test_out_of_range_marker(self):
        text = make_response(4) + "\n[Phase 9 DONE]"
        result = verify(text, 4)
        self.assertFalse(result["valid"])
        self.assertTrue(any("out-of-range" in e for e in result["errors"]))

    def test_empty_text_invalid(self):
        result = verify("", 4)
        self.assertFalse(result["valid"])
        self.assertEqual(len(result["errors"]), 4)

    def test_marker_inline_warns_but_passes(self):
        text = "\n".join(f"Result: [Phase {i} DONE] done" for i in range(4))
        result = verify(text, 4)
        self.assertTrue(result["valid"])
        self.assertEqual(len(result["warnings"]), 4)

    def test_marker_on_own_line_no_warning(self):
        result = verify(make_response(4), 4)
        self.assertEqual(result["warnings"], [])


if __name__ == "__main__":
    unittest.main()
