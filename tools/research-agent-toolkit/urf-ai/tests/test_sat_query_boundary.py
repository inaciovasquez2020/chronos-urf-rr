"""Exact finite audits of the SAT input-query/no-go boundary, NOT Lean proof."""
import unittest
from copy import deepcopy
from fractions import Fraction
from urf_ai.sat_query_boundary import (
    sat_family_receipt, eager_read_entropy, brute_sat, scan_sat,
    evaluate_sat_query_response, SAT_QUERY_CASES,
    copy_machine_history, copy_machine_work_at, reconstruct_work_from_transcript,
    copy_machine_entropy_regression,
)
from urf_ai.benchmark import evaluate_response
from urf_ai.assistant import answer, benchmark


class SATQueryBoundaryTests(unittest.TestCase):
    def test_every_instance_independent_truth_table(self):
        for m in range(1, 13):
            r = sat_family_receipt(m)
            self.assertEqual(r["encoded_instances"], 2**m)
            self.assertEqual(r["sat_instances"], 1)
            self.assertEqual(r["all_positive_sensitivity"], m)
            self.assertEqual(r["deterministic_query_lower_bound"], m)
            self.assertEqual(r["matching_worst_case_scan_queries"], m)
            self.assertEqual(Fraction(r["uniform_mean_scan_queries_numerator"],
                                      r["uniform_mean_scan_queries_denominator"]),
                             Fraction(2*(2**m - 1), 2**m))
            self.assertLessEqual(r["sat_output_entropy_bits_approx"], 1.0)
        self.assertLess(sat_family_receipt(12)["sat_output_entropy_bits_approx"], 0.01)

    def test_input_revealing_schedule(self):
        for n in range(1, 11):
            for read in range(n+1):
                r = eager_read_entropy(n, read, extra_steps=4)
                self.assertEqual(r["conditional_input_entropy_bits"], n-read)
                self.assertEqual(r["input_information_acquired_bits"], read)
                self.assertEqual(r["full_reconstruction_from_observations"], read == n)
            self.assertEqual(eager_read_entropy(n, n, 0)["conditional_input_entropy_bits"],
                             eager_read_entropy(n, n, 512)["conditional_input_entropy_bits"])

    def test_genuine_two_tape_normalized_transcripts(self):
        for n in range(1, 11):
            r = copy_machine_entropy_regression(n)
            self.assertEqual(r["conditional_entropy_bits"],
                             [n-min(n,t+1) for t in range(n+2)])
            self.assertTrue(r["work_contents_reconstructed_from_transcript"])
            self.assertEqual(r["full_input_recovered_by_transcript_at_time"], n-1)
            self.assertEqual(sum(r["per_transition_information_bits"]), n-1)
        self.assertEqual(copy_machine_work_at("010", 2), "01")
        self.assertEqual(reconstruct_work_from_transcript(copy_machine_history("010",2)), "01")

    def test_inadmissible_inputs_fail_closed(self):
        for n in [0,13,False,-1,1.0]:
            with self.assertRaises(ValueError):sat_family_receipt(n)
        for args in [(0,0,0),(13,13,0),(2,3,0),(2,-1,0),(2,2,-1),(2,2,4097)]:
            with self.assertRaises(ValueError):eager_read_entropy(*args)
        for s in ["", "X", "0012", "0"*13]:
            with self.assertRaises(ValueError):brute_sat(s)
            with self.assertRaises(ValueError):scan_sat(s)

    def test_both_source_specific_cases_and_readonly_adapter(self):
        for c in SAT_QUERY_CASES:
            a = answer(c)
            self.assertTrue(a["validation"]["pass"], a)
            self.assertEqual(a["governance"]["claim_state"], "OPEN")
            self.assertTrue(a["governance"]["journal_audit"])
        total = benchmark()
        self.assertEqual(total["total"], 11)
        self.assertEqual(total["passed"], 11)

    def test_scope_and_status_mutations_rejected(self):
        for c in SAT_QUERY_CASES:
            original = answer(c)["answer"]
            probes = []
            v = deepcopy(original);v["status"] = "P_VS_NP_PROVED";probes.append(v)
            v = deepcopy(original);v["missing_obligation"] = "NONE";probes.append(v)
            v = deepcopy(original);v["witness"] = {};probes.append(v)
            v = deepcopy(original);v["extra"] = "assertion";probes.append(v)
            if c == "bridge_sat_sign_query":
                v = deepcopy(original);v["witness"]["all_positive_signs"] = "10" + "0"*(original["witness"]["m"]-2);probes.append(v)
                v = deepcopy(original);v["witness"]["m"] = 13;probes.append(v)
            if c == "bridge_eager_read_no_go":
                v = deepcopy(original);v["witness"]["read_steps"] = original["witness"]["input_bits"] - 1;probes.append(v)
                v = deepcopy(original);v["witness"]["postprocessing_steps"] = 4097;probes.append(v)
            for v in probes:
                self.assertFalse(evaluate_response(v, c)["pass"], (c, v))


if __name__ == "__main__": unittest.main()
