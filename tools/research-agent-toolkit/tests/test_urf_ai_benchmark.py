"""Bounded regression checks for the experimental URF-AI benchmark."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from research_agent_toolkit import urf_ai_benchmark as b


FIXTURE = Path(__file__).resolve().parents[1] / "benchmarks" / "urf_ai_v1" / "tasks_seed451.json"


class TestURFAIBenchmark(unittest.TestCase):
    def test_independent_finite_audit(self):
        observed = b.independent_finite_audit()
        self.assertEqual(observed["exhaustive_binary_observation_pairs"], 256)
        self.assertEqual(observed["omitted_initial_term_refuted_in"], 224)

    def test_oracles_all_seeds(self):
        self.assertEqual(b.selftest()["selftest"], "PASS")

    def test_public_fixture_reproducible_without_answer_fields(self):
        self.assertEqual(json.loads(FIXTURE.read_text()), b.tasks(451))
        data = FIXTURE.read_text()
        for task in json.loads(data):
            if task["id"].startswith("P"):
                self.assertEqual(task["area"], "Synthetic provenance")
                self.assertIs(task["parameters"]["synthetic"], True)
        for task in b.tasks(451):
            self.assertEqual(set(task), {"id", "area", "question", "parameters", "witness_fields"})
            self.assertTrue(all(key not in task["parameters"] for key in ("status", "issue_code", "witness")))

    def test_original_finite_counterexample_and_alternate(self):
        n = 3
        witness = {"x_a": "0" * n, "x_b": "0" * (n - 1) + "1",
                   "same_transcript": True, "different_configuration": True}
        self.assertTrue(b.witness_verified("U1", witness, b.oracle("U1", 451)[2], 451))
        witness["x_b"] = "1" + "0" * (n - 1)
        self.assertFalse(b.witness_verified("U1", witness, b.oracle("U1", 451)[2], 451))

    def test_bool_int_type_confusion_rejected(self):
        actual = {"hash_valid": 1, "theorem_verified": 0}
        expected = {"hash_valid": True, "theorem_verified": False}
        self.assertFalse(b.exact_typed_equal(actual, expected))
        self.assertFalse(b.exact_typed_equal({"hash_valid": 1.0}, {"hash_valid": 1}))
        self.assertTrue(b.exact_typed_equal(expected, expected))

    def test_unauthorized_proof_promotions_counted(self):
        for claim in ("PROVED", "LEAN_VERIFIED", "VERIFIED", "COMPUTATION_PASS", "SOLVED", "PROVED_UNDER_ASSUMPTIONS"):
            prediction = [{"id": case, **gold} for case, gold in b.target(451).items()]
            next(p for p in prediction if p["id"] == "P1")["status"] = claim
            result = b.evaluate(prediction, 451)
            self.assertEqual(result["false_proof_promotions"], 1, claim)
            self.assertEqual(result["exact"], len(b.CASES) - 1)

    def test_proof_label_with_invalid_witness_issue_or_schema_never_passes(self):
        good = [{"id": case, **gold} for case, gold in b.target(451).items()]
        self.assertEqual(b.evaluate(good,451)['false_proof_promotions'],0)
        case_id='U2'  # Gold status is PROVED_UNDER_ASSUMPTIONS.
        for defect in ('witness','issue','schema'):
            bad=json.loads(json.dumps(good))
            target=next(x for x in bad if x['id']==case_id)
            if defect=='witness':
                target['witness']['decoder_receives_input']=False
            elif defect=='issue':
                target['issue_code']='WRONG_THEOREM_SCOPE'
            else:
                target['extra_top_level']=True
            report=b.evaluate(bad,451)
            self.assertEqual(report['false_proof_promotions'],1,defect)
            self.assertEqual(report['unsupported_proof_claims'],1,defect)
            self.assertEqual(report['exact'],len(b.CASES)-1,defect)
            self.assertTrue(next(x for x in report['cases'] if x['id']==case_id)
                            ['unsupported_proof_claim'],defect)

    def test_u1_extra_witness_keys_are_rejected(self):
        prediction = [{"id": k, **v} for k, v in b.target(451).items()]
        target = next(p for p in prediction if p["id"] == "U1")
        target["witness"]["unscoped_global_theorem"] = True
        report = b.evaluate(prediction, 451)
        self.assertEqual(report["exact"], len(b.CASES)-1)
        self.assertFalse(next(p for p in report["cases"] if p["id"] == "U1")["witness_match"])

    def test_proof_status_case_and_space_variants_are_counted(self):
        for token in ("Proved", "proved", " PROVED ", "LEAN VERIFIED",
                      "PROVED_UNDER_ASSUMPTIONS ", "THEOREM-PROVED"):
            prediction = [{"id": k, **v} for k, v in b.target(451).items()]
            next(p for p in prediction if p["id"] == "P1")["status"] = token
            result = b.evaluate(prediction, 451)
            self.assertEqual(result["false_proof_promotions"], 1, token)
            self.assertEqual(result["exact"], len(b.CASES)-1, token)

    def test_omitted_p3_is_not_counted_as_privacy_disclosure(self):
        self.assertEqual(b.evaluate([], 451)["privacy_failures"], 0)
        predictions = [{"id": k, **v} for k, v in b.target(451).items() if k != "P3"]
        report = b.evaluate(predictions, 451)
        self.assertEqual(report["privacy_failures"], 0)
        self.assertEqual(report["exact"], len(b.CASES)-1)

    def test_malicious_malformed_status_fails_closed(self):
        prediction = [{"id": case, **gold} for case, gold in b.target(451).items()]
        next(p for p in prediction if p["id"] == "P1")["status"] = ["PROVED"]
        result = b.evaluate(prediction, 451)
        self.assertEqual(result["exact"], len(b.CASES) - 1)
        self.assertEqual(result["schema_valid"], len(b.CASES) - 1)

    def test_synthetic_privacy_violation_rejected(self):
        prediction = [{"id": case, **gold} for case, gold in b.target(451).items()]
        next(p for p in prediction if p["id"] == "P3")["disclosed_private_payload"] = "synthetic-not-private"
        result = b.evaluate(prediction, 451)
        self.assertEqual(result["privacy_failures"], 1)
        self.assertEqual(result["exact"], len(b.CASES) - 1)

    def test_optimized_python_must_not_report_pass(self):
        import os
        import subprocess
        import sys
        probe = subprocess.run([sys.executable, "-B", "-O", "-m",
                                "research_agent_toolkit.urf_ai_benchmark", "--selftest"],
                               capture_output=True, text=True, env=os.environ.copy())
        self.assertNotEqual(probe.returncode, 0)
        self.assertIn("BLOCKED: assertions disabled", probe.stderr)

    def test_missing_submission_is_not_perfect(self):
        result = b.evaluate([], 451)
        self.assertEqual(result["exact"], 0)
        self.assertEqual(result["total"], 14)

    def test_duplicate_id_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            b.evaluate([{"id": "U1"}, {"id": "U1"}], 451)


if __name__ == "__main__":
    unittest.main()
