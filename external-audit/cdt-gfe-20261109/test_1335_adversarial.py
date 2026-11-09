"""Offline, synthetic-only adversarial regression for frozen CDT Stage 0 v2.
Source snapshot is pinned by Git blob SHA; deliberately does not fix the classifier.
A passing test means the listed defects are reproducible, NOT production readiness.
"""
import hashlib
import importlib.util
import itertools
import math
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/"pinned_v2.py"
PIN="e40b4ca214073a66bc57e781e1b955bae8c87f5a"
U=1.0269828382207759e-8
T=5.1349141911038794e-8

def load():
    b=SRC.read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert actual==PIN,(actual,PIN)
    spec=importlib.util.spec_from_file_location("cdt_pinned",SRC)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.classify

def rows(vals,n=4):
    return [{"configuration":c,"eta":v,"included":True}
            for c,v in zip(("C1","C2","C3","C4"),vals) for _ in range(n)]

class Audit(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.classify=staticmethod(load())
    def result(self,values,n=4,u=U,t=T):
        return self.classify(rows(values,n),u,t)["status"]
    def test_cross_null_cancellation_fix(self):
        self.assertEqual(self.result((6e-8,-6e-8,1e-6,-1e-6)),"NO_CANDIDATE")
        self.assertEqual(self.result((6e-8,-6e-8,0,0)),"SINGLE_LAB_CANDIDATE_ONLY")
    def test_null_grid_49(self):
        values=(-100,-2,-1,0,1,2,100)
        for p,q in itertools.product(values,repeat=2):
            expected=abs(p)<2 and abs(q)<2
            actual=self.result((6e-8,-6e-8,p*U,q*U))=="SINGLE_LAB_CANDIDATE_ONLY"
            self.assertEqual(actual,expected,(p,q))
    def test_nonfinite_false_candidate_reproduced(self):
        self.assertEqual(self.result((math.inf,-math.inf,0,0)),"SINGLE_LAB_CANDIDATE_ONLY")
        self.assertEqual(self.result((6e-8,-6e-8,0,0),u=math.inf),"SINGLE_LAB_CANDIDATE_ONLY")
    def test_negative_threshold_false_candidate_reproduced(self):
        self.assertEqual(self.result((1e-9,-1e-9,0,0),t=-1),"SINGLE_LAB_CANDIDATE_ONLY")
    def test_one_sample_per_configuration_false_candidate_reproduced(self):
        self.assertEqual(self.result((6e-8,-6e-8,0,0),n=1),"SINGLE_LAB_CANDIDATE_ONLY")
        self.assertEqual(self.result((1e308,-1e308,0,0),n=1),"SINGLE_LAB_CANDIDATE_ONLY")
    def test_extreme_finite_overflow_reproduced(self):
        with self.assertRaises(OverflowError):
            self.result((1e308,-1e308,0,0))
    def test_within_null_control_cancellation_unresolved(self):
        data=rows((6e-8,-6e-8,0,0))
        ctrl=[r for r in data if r["configuration"]=="C3"]
        ctrl[0]["eta"]=1e-4
        ctrl[1]["eta"]=-1e-4
        self.assertEqual(self.classify(data,U,T)["status"],"SINGLE_LAB_CANDIDATE_ONLY")
    def test_physically_unauthorized(self):
        # No synthetic test is allowed to imply authorization or a measurement.
        self.assertEqual("SYNTHETIC_FIXTURE","SYNTHETIC_FIXTURE")

if __name__=="__main__":
    unittest.main(verbosity=2)
