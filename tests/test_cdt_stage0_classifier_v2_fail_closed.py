"""Adversarial fail-closed tests for the synthetic-only Stage 0 v2 classifier."""
import itertools
import math
import random
import unittest
from tools.cdt_stage0_classifier_v2 import classify

U = 1.0269828382207759e-8
T = 5.1349141911038794e-8
CODES = ("C1", "C2", "C3", "C4")


def rows(values=(6e-8, -6e-8, 0., 0.), n=4):
    return [{"configuration": c, "eta": x, "included": True}
            for c, x in zip(CODES, values) for _ in range(n)]


class FailClosed(unittest.TestCase):
    def status(self, data=None, u_c=U, threshold=T):
        return classify(rows() if data is None else data, u_c, threshold)["status"]

    def test_valid_clean_case_and_v2_null_fix(self):
        self.assertEqual(self.status(), "SINGLE_LAB_CANDIDATE_ONLY")
        self.assertEqual(self.status(rows((6e-8,-6e-8,1e-6,-1e-6))), "NO_CANDIDATE")

    def test_null_control_grid_49(self):
        for p, q in itertools.product((-100,-2,-1,0,1,2,100), repeat=2):
            expected = abs(p)<2 and abs(q)<2
            actual = self.status(rows((6e-8,-6e-8,p*U,q*U))) == "SINGLE_LAB_CANDIDATE_ONLY"
            self.assertEqual(actual, expected, (p, q))

    def test_all_outputs_declared_synthetic_only(self):
        for data,u,t in [(rows(),U,T),(rows(n=1),U,T),
                         (rows(),math.inf,T),
                         (rows((6e-8,-6e-8,1e-6,-1e-6)),U,T)]:
            self.assertEqual(classify(data,u,t)["execution_scope"],"SYNTHETIC_ONLY")

    def test_seeded_10000_finite_grid_matches_explicit_oracle(self):
        rng = random.Random(1335)
        for _ in range(10000):
            a,b,c,d = (rng.uniform(-1e-7,1e-7) for _ in range(4))
            good = abs((a-b)/2)>=T and a*b<0 and abs(c)<2*U and abs(d)<2*U
            expected = "SINGLE_LAB_CANDIDATE_ONLY" if good else "NO_CANDIDATE"
            self.assertEqual(self.status(rows((a,b,c,d))),expected)

    def test_nonfinite_eta_all_configuration_positions(self):
        for position in range(16):
            for x in (math.inf,-math.inf,math.nan):
                data=rows();data[position]["eta"]=x
                self.assertEqual(self.status(data),"INVALID_INPUT",(position,x))

    def test_excluded_nonfinite_is_rejected(self):
        data=rows();data[0]["eta"]=math.inf;data[0]["included"]=False
        self.assertEqual(self.status(data),"INVALID_INPUT")

    def test_invalid_eta_types(self):
        for value in (True,False,None,"5",1+0j,{},10**10000):
            data=rows();data[0]["eta"]=value
            self.assertEqual(self.status(data),"INVALID_INPUT")

    def test_invalid_budget_types_and_values(self):
        for value in (math.inf,-math.inf,math.nan,0.,-1.,True,False,None,"2",10**10000):
            self.assertEqual(self.status(u_c=value),"INVALID_INPUT")
            self.assertEqual(self.status(threshold=value),"INVALID_INPUT")

    def test_budget_scaled_limit_overflow(self):
        self.assertEqual(self.status(u_c=1.5e308),"INVALID_INPUT")

    def test_oversized_finite_signal_rejected(self):
        self.assertEqual(self.status(rows((1e308,-1e308,0,0))),"INVALID_INPUT")

    def test_signal_product_overflow_rejected(self):
        self.assertEqual(self.status(rows((1e160,-1e160,0,0))),"INVALID_INPUT")

    def test_single_observation_per_group_is_pending(self):
        self.assertEqual(self.status(rows(n=1)),"PENDING")
        self.assertEqual(self.status(rows(n=3)),"PENDING")

    def test_missing_group_is_pending(self):
        data=[r for r in rows() if r["configuration"]!="C4"]
        self.assertEqual(self.status(data),"PENDING")

    def test_exclusions_can_reduce_counts_to_pending(self):
        data=rows();data[0]["included"]=False
        self.assertEqual(self.status(data),"PENDING")

    def test_extra_finite_excluded_outlier_preserves_v2(self):
        data=rows();data.append({"configuration":"C3","eta":100,"included":False})
        self.assertEqual(self.status(data),"SINGLE_LAB_CANDIDATE_ONLY")

    def test_wrong_included_type(self):
        for flag in (1,0,"yes",None):
            data=rows();data[0]["included"]=flag
            self.assertEqual(self.status(data),"INVALID_INPUT")

    def test_unknown_configuration(self):
        for label in ("C5",None,1,["C1"]):
            data=rows();data[0]["configuration"]=label
            self.assertEqual(self.status(data),"INVALID_INPUT")

    def test_missing_fields(self):
        for key in ("configuration","eta","included"):
            data=rows();del data[0][key]
            self.assertEqual(self.status(data),"INVALID_INPUT")

    def test_invalid_row_types(self):
        for value in (None,[],"C1",42):
            data=rows();data[0]=value
            self.assertEqual(self.status(data),"INVALID_INPUT")

    def test_invalid_rows_container(self):
        for value in (None,{},"",1):
            self.assertEqual(classify(value,U,T)["status"],"INVALID_INPUT")

    def test_within_control_cancellation_remains_open(self):
        data=rows();indices=[i for i,row in enumerate(data) if row["configuration"]=="C3"]
        data[indices[0]]["eta"]=1e-4
        data[indices[1]]["eta"]=-1e-4
        self.assertEqual(self.status(data),"SINGLE_LAB_CANDIDATE_ONLY")


if __name__=="__main__":
    unittest.main(verbosity=2)
