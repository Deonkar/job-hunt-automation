import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import jev_verdict as jv  # noqa: E402

TODAY = dt.date(2026, 10, 20)
JOB = {"company": "Acme", "role": "SDE II (Backend)", "location": "Toronto", "cons": "Minimum 3 years asked"}


def answers(apply, exp=0.1, loc=0.1, stack=0.1):
    vals = {"apply": apply, "experience_gap": exp, "location_blocked": loc, "stack_mismatch": stack}
    return {k: {"type": "noul", "noul": v} for k, v in vals.items()}


class CellTest(unittest.TestCase):
    def test_yes_and_no_with_probability(self):
        self.assertEqual(jv.cell(answers(0.82)), "Yes (0.82)")
        self.assertEqual(jv.cell(answers(0.31)), "No (0.31)")

    def test_threshold_is_half(self):
        self.assertEqual(jv.cell(answers(0.5)), "Yes (0.50)")
        self.assertEqual(jv.cell(answers(0.49)), "No (0.49)")

    def test_blockers_above_cutoff_are_named(self):
        self.assertEqual(jv.cell(answers(0.2, exp=0.9, loc=0.7)), "No (0.20): experience gap, location")
        self.assertEqual(jv.cell(answers(0.7, stack=0.65)), "Yes (0.70): stack mismatch")
        self.assertEqual(jv.cell(answers(0.2, exp=0.59)), "No (0.20)")


class StateTest(unittest.TestCase):
    def test_full_time_months_counts_from_start(self):
        self.assertEqual(jv.full_time_months("2025-03", TODAY), 19)

    def test_full_time_months_adds_every_role(self):
        roles = [{"start": "2025-03", "end": None}, {"start": "2023-01", "end": "2024-01"}]
        self.assertEqual(jv.total_full_time_months(roles, TODAY), 31)

    def test_state_carries_job_and_candidate(self):
        profile = {"experience": {"full_time": [{"start": "2025-03"}]}, "skills": {"Languages": ["Go"]}}
        s = jv.build_state(JOB, "candidate notes", profile, TODAY)
        self.assertEqual(s["job"], JOB)
        self.assertEqual(s["candidate"]["full_time_experience"], "1 year 7 months")
        self.assertEqual(s["candidate"]["skills"], {"Languages": ["Go"]})
        self.assertEqual(s["candidate"]["profile"], "candidate notes")

    def test_every_question_is_a_noul_and_cell_reads_them_all(self):
        qs = jv.questions("Brazil")
        self.assertEqual(set(qs), {"apply", "experience_gap", "location_blocked", "stack_mismatch"})
        self.assertTrue(all(q["type"] == "noul" for q in qs.values()))
        self.assertIn("Brazil", qs["location_blocked"]["instructions"])
        self.assertNotIn("India", str(qs))


class KeyTest(unittest.TestCase):
    def test_env_file_value_is_read(self):
        path = os.path.join(os.path.dirname(__file__), "_tmp_test.env")
        with open(path, "w") as f:
            f.write("OTHER=1\nTYPESAFE_API_KEY=\"abc123\"\n")
        try:
            self.assertEqual(jv.key_from_env_file(path), "abc123")
            self.assertIsNone(jv.key_from_env_file(path + ".missing"))
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
