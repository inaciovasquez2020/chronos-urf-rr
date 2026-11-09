"""Six adversarial gaps in the SYNTHETIC preview, not production acceptance."""
import unittest
from test_1335_preview_contract import fixture, preview, MAPPING, CANDIDATE
class Gaps(unittest.TestCase):
    def test_missing_digest_is_not_authenticated(self):
        rows=fixture();self.assertFalse(any("source_digest" in r for r in rows))
        self.assertEqual(preview(rows)["status"],CANDIDATE)
    def test_physical_mode_stays_blocked(self):
        self.assertEqual(preview(fixture(),synthetic=False)["status"],"PENDING")
    def test_caller_supplied_mapping_not_authenticated(self):
        perm={"B1":"C2","B2":"C1","B3":"C3","B4":"C4"}
        rows=fixture()
        for row in rows:
            row["configuration"]=perm[row["blind_code"]]
            row["eta"]={"C1":6e-8,"C2":-6e-8,"C3":0.,"C4":0.}[row["configuration"]]
        self.assertEqual(preview(rows,mapping=perm)["status"],CANDIDATE)
    def test_within_null_group_cancellation(self):
        rows=fixture();pos=[i for i,r in enumerate(rows) if r["configuration"]=="C3"]
        rows[pos[0]]["eta"]=1e-4;rows[pos[1]]["eta"]=-1e-4
        self.assertEqual(preview(rows)["status"],CANDIDATE)
    def test_forged_gates_cannot_authorize_physical(self):
        rows=fixture()
        for row in rows: row.update({"source_digest":"f"*64,**{f"G{i}":"PASS" for i in range(1,6)}})
        self.assertEqual(preview(rows,synthetic=False)["status"],"PENDING")
    def test_forged_gates_not_authenticated_in_synthetic(self):
        rows=fixture()
        for row in rows: row.update({"source_digest":"f"*64,**{f"G{i}":"PASS" for i in range(1,6)}})
        self.assertEqual(preview(rows)["status"],CANDIDATE)
if __name__=="__main__": unittest.main(verbosity=2)
