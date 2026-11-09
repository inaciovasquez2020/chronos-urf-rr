"""Synthetic-status namespace prototype, not authorization or production logic."""
import math
import unittest
from test_1335_preview_contract import fixture,preview,MAPPING,CANDIDATE
def classify_synthetic_fixture(rows,*,mapping=None,physical=False):
    if physical:
        return {"status":"BLOCKED_AUTHORIZATION","execution_scope":"UNAUTHORIZED_PHYSICAL",
                "valid_for_physical_execution":False}
    try:
        raw=preview(rows,mapping=mapping,synthetic=True)
        status=raw["status"]
        if status==CANDIDATE: status="SYNTHETIC_CANDIDATE_ONLY"
        elif status=="NO_CANDIDATE": status="SYNTHETIC_NO_CANDIDATE"
        elif status not in ("PENDING","INVALID_INPUT"): status="INVALID_INPUT"
    except Exception: status="INVALID_INPUT"
    return {"status":status,"execution_scope":"SYNTHETIC_FIXTURE",
            "valid_for_physical_execution":False}
class Tests(unittest.TestCase):
    def test_positive_is_never_physical_candidate(self):
        r=classify_synthetic_fixture(fixture(),mapping=MAPPING)
        self.assertEqual(r["status"],"SYNTHETIC_CANDIDATE_ONLY")
        self.assertNotEqual(r["status"],CANDIDATE)
        self.assertFalse(r["valid_for_physical_execution"])
    def test_physical_must_remain_blocked(self):
        self.assertEqual(classify_synthetic_fixture(fixture(),mapping=MAPPING,physical=True)["status"],"BLOCKED_AUTHORIZATION")
    def test_unlocked_mapping_must_remain_pending(self):
        self.assertEqual(classify_synthetic_fixture(fixture())["status"],"PENDING")
    def test_nonfinite_values_rejected(self):
        rows=fixture();rows[0]["eta"]=math.inf
        self.assertEqual(classify_synthetic_fixture(rows,mapping=MAPPING)["status"],"INVALID_INPUT")
    def test_cancelled_outlier_still_requires_review(self):
        rows=fixture();pos=[i for i,r in enumerate(rows) if r["configuration"]=="C3"]
        rows[pos[0]]["eta"]=1e-4;rows[pos[1]]["eta"]=-1e-4
        self.assertEqual(classify_synthetic_fixture(rows,mapping=MAPPING)["status"],"SYNTHETIC_CANDIDATE_ONLY")
if __name__=="__main__": unittest.main(verbosity=2)
