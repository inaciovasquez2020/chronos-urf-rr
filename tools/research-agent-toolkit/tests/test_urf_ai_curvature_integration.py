"""Executed only against the staged, exact-source PR #1339 benchmark."""
import copy
import unittest
from research_agent_toolkit import urf_ai_benchmark as b


class CurvatureIntegration(unittest.TestCase):
    def test_exact_v1_plus_curvature_oracles(self):
        self.assertEqual(len(b.CASES),22)
        for seed in (0,1,451,99991):
            target=b.target(seed)
            self.assertEqual(len(target),22)
            self.assertEqual({x[0] for x in b.CASES},set(target))
            perfect=[{'id':case,**rec} for case,rec in target.items()]
            score=b.evaluate(perfect,seed)
            self.assertEqual(score['exact'],22)
            self.assertEqual(score['false_proof_promotions'],0)

    def test_proof_promotion_rejected_for_receipt_only(self):
        base=[{'id':case,**rec} for case,rec in b.target(451).items()]
        candidate=copy.deepcopy(base)
        next(v for v in candidate if v['id']=='C8')['status']='PROVED_UNDER_ASSUMPTIONS'
        score=b.evaluate(candidate,451)
        self.assertEqual(score['exact'],21)
        self.assertEqual(score['false_proof_promotions'],1)

    def test_wrong_witness_must_not_certify_curvature(self):
        base=[{'id':case,**rec} for case,rec in b.target(451).items()]
        candidate=copy.deepcopy(base)
        next(v for v in candidate if v['id']=='C2')['witness']['sign']='NEGATIVE'
        score=b.evaluate(candidate,451)
        self.assertEqual(score['exact'],21)
        self.assertEqual(score['false_proof_promotions'],1)

    def test_new_tasks_are_public_without_answer_leakage(self):
        tasks=b.tasks(451)
        self.assertEqual(len(tasks),22)
        for t in tasks:
            self.assertNotIn('status',t['parameters'])
            self.assertNotIn('issue_code',t['parameters'])
            self.assertNotIn('witness',t['parameters'])
        self.assertEqual(sum(t['id'].startswith('C') for t in tasks),8)


if __name__=='__main__':
    unittest.main()
