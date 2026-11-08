"""Executable regression and bounded adversarial tests for CDT Stage 0 v2."""
import hashlib
import itertools
import json
import unittest
from pathlib import Path

from tools.cdt_stage0_classifier_v2 import classify


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/external_validation/carbon_gravity_stage0_internal_execution_package_2026_07_12.json"
V1_SHA256 = "4291599bea04eb267dc832ad673f22aff27a6a008cbb2ace96c2746ddafa4ccc"


class CDTStage0ClassifierV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        package = json.loads(SOURCE.read_text(encoding="utf-8"))
        lock = package["analysis_lock"]
        cls.u_c = package["stage0_error_budget"]["declared_combined_uncertainty_eta"]
        cls.threshold = package["stage0_error_budget"]["single_lab_candidate_threshold_eta"]
        assert lock["algorithm_sha256"] == V1_SHA256
        assert hashlib.sha256(lock["canonical_code"].encode("utf-8")).hexdigest() == V1_SHA256
        assert package["execution_state"] == "NOT_EXECUTED"
        assert package["analysis_lock"]["measurement_dataset_present"] is False

    @staticmethod
    def rows(c1, c2, c3, c4):
        return [
            {"configuration": c, "eta": value, "included": True}
            for c, value in zip(("C1", "C2", "C3", "C4"), (c1, c2, c3, c4))
            for _ in range(4)  # 16 balanced simulated measurements
        ]

    def result(self, c1, c2, c3, c4):
        return classify(self.rows(c1, c2, c3, c4), self.u_c, self.threshold)

    def test_clean_reversing_signal_retained(self):
        r = self.result(6e-8, -6e-8, 0, 0)
        self.assertEqual(r["status"], "SINGLE_LAB_CANDIDATE_ONLY")
        self.assertTrue(r["null_controls_pass"])

    def test_opposite_large_controls_cannot_cancel(self):
        r = self.result(6e-8, -6e-8, 1e-6, -1e-6)
        self.assertEqual(r["null_estimator"], 0.0)
        self.assertFalse(r["null_controls_pass"])
        self.assertEqual(r["status"], "NO_CANDIDATE")

    def test_one_contaminated_control_rejects(self):
        for a, b in ((3e-8, 0), (0, 3e-8)):
            with self.subTest(a=a, b=b):
                self.assertEqual(self.result(6e-8, -6e-8, a, b)["status"], "NO_CANDIDATE")

    def test_nonreversing_signal_rejects(self):
        self.assertEqual(self.result(6e-8, 6e-8, 0, 0)["status"], "NO_CANDIDATE")

    def test_below_threshold_rejects(self):
        self.assertEqual(self.result(2e-8, -2e-8, 0, 0)["status"], "NO_CANDIDATE")

    def test_incomplete_blocks_are_pending(self):
        partial = [r for r in self.rows(6e-8, -6e-8, 0, 0) if r["configuration"] != "C4"]
        self.assertEqual(classify(partial, self.u_c, self.threshold)["status"], "PENDING")

    def test_excluded_outlier_is_not_used(self):
        good = self.rows(6e-8, -6e-8, 0, 0)
        good.append({"configuration": "C3", "eta": 100, "included": False})
        self.assertEqual(classify(good, self.u_c, self.threshold)["status"], "SINGLE_LAB_CANDIDATE_ONLY")

    def test_exhaustive_49_null_pair_states(self):
        # Enumerate sign, cancellation, and both strict 2-sigma boundaries.
        vals = (-100, -2, -1, 0, 1, 2, 100)
        count = 0
        for p, q in itertools.product(vals, repeat=2):
            with self.subTest(p=p, q=q):
                r = self.result(6e-8, -6e-8, p * self.u_c, q * self.u_c)
                expected = abs(p) < 2 and abs(q) < 2
                self.assertEqual(r["null_controls_pass"], expected)
                self.assertEqual(r["status"] == "SINGLE_LAB_CANDIDATE_ONLY", expected)
            count += 1
        self.assertEqual(count, 49)


if __name__ == "__main__":
    unittest.main()
