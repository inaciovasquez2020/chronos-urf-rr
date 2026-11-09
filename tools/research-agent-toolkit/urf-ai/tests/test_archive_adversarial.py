"""Source-specific public regression fixtures, not held-out model evaluation.

The analytical infinite-family arguments are documented in the archive audit;
finite tests alone are not proof of an unbounded theorem or of Lean validity.
"""
from __future__ import annotations

import unittest
from fractions import Fraction

from urf_ai.archive_adversarial import (
    MAX_EXACT_CYCLE_ORDER, MAX_PRISM_ORDER, cycle_laplacian_trace_exact,
    cycle_trace_formula, prism_adjacency, prism_shared_edge_cycle_count,
    prism_explicit_vertex_transitive,
)
from urf_ai.archive_admission import finite_fold_precheck


class XystemArchiveRegression(unittest.TestCase):
    def test_exact_pseudoinverse_trace(self):
        for n in (5, 8, 12, 16):
            with self.subTest(n=n):
                self.assertEqual(cycle_laplacian_trace_exact(n),
                                 cycle_trace_formula(n))

    def test_parameterized_formula_produces_arbitrarily_large_values(self):
        # Bounded samples only; unbounded implication is the elementary formula.
        for radius, cap in ((1,1), (2,10), (7,100), (12,1000)):
            n = max(radius + 1, 4)
            while cycle_trace_formula(n) <= Fraction(cap):
                n += 1
            self.assertGreater(n, radius)
            self.assertGreater(cycle_trace_formula(n), cap)

    def test_resource_and_type_limits_fail_closed(self):
        for n in (True, 3, -1, MAX_EXACT_CYCLE_ORDER + 1):
            with self.subTest(n=n), self.assertRaises(ValueError):
                cycle_laplacian_trace_exact(n)


class FO2ArchiveRegression(unittest.TestCase):
    def test_prism_shared_edge_cycle_family(self):
        for n in (4, 6, 8, 12):
            with self.subTest(n=n):
                self.assertEqual(prism_shared_edge_cycle_count(n), n-1)
                self.assertEqual(len(prism_adjacency(n)), 2*n)
                self.assertTrue(prism_explicit_vertex_transitive(n))

    def test_prism_resource_and_type_limits(self):
        for n in (False, 2, MAX_PRISM_ORDER + 1):
            with self.subTest(n=n), self.assertRaises(ValueError):
                prism_shared_edge_cycle_count(n)


class FoldAdmissionRegression(unittest.TestCase):
    def test_sound_nontrivial_finite_fold_is_not_a_global_proof(self):
        r = finite_fold_precheck([0,1,2,3], {0:'a',1:'a',2:'b',3:'b'},
                                 {0:0,1:0,2:1,3:1}, complete_domain=True)
        self.assertEqual(r['status'], 'SOUND_ON_ATTESTED_FINITE_DOMAIN')
        self.assertEqual(r['proof_status'], 'NOT_LEAN_VERIFIED')

    def test_unsound_fold_rejected(self):
        r = finite_fold_precheck([0,1], {0:'x',1:'x'}, {0:0,1:1},
                                 complete_domain=True)
        self.assertEqual(r['status'], 'REJECT_UNSOUND_FOLD')

    def test_injective_fold_is_not_unsolvability(self):
        r = finite_fold_precheck([0,1], {0:'x',1:'y'}, {0:0,1:1},
                                 complete_domain=True)
        self.assertEqual(r['status'], 'NO_NONTRIVIAL_REDUCTION_IN_CANDIDATE')
        self.assertNotIn('FORBIDDEN', r['status'])

    def test_incomplete_coverage_and_budget(self):
        cases = [
            finite_fold_precheck([0,1], {0:'a'}, {0:0,1:1}, complete_domain=True),
            finite_fold_precheck([0,1], {0:'x',1:'x'}, {0:0,1:0}, complete_domain=False),
            finite_fold_precheck(list(range(5)), {}, {}, max_states=4),
        ]
        self.assertTrue(all(x['status']=='INCOMPLETE' for x in cases))

    def test_python_bool_int_key_alias_rejected(self):
        # Python regards True == 1, but admission must not silently conflate key types.
        r = finite_fold_precheck([1], {True:'f'}, {1:0}, complete_domain=True)
        self.assertEqual(r['status'], 'DEFER')

    def test_untrusted_mutable_or_ill_typed_data_rejected(self):
        r = finite_fold_precheck([0,1], {0:[],1:[]}, {0:0,1:0}, complete_domain=True)
        self.assertEqual(r['status'], 'DEFER')
        r = finite_fold_precheck([0,0], {0:0}, {0:0}, complete_domain=True)
        self.assertEqual(r['status'], 'DEFER')


if __name__ == '__main__':
    unittest.main()
