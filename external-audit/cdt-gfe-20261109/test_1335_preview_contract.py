"""Illustrative SYNTHETIC preflight model; never authorizes physical execution.
No authenticated source provenance, no blind-key authority, no approved statistical
outlier rule. Passing tests here do not repair the pinned v2 classifier.
"""
import math
import unittest
from test_1335_adversarial import load, U as UNCERTAINTY, T as THRESHOLD
SEQ=("B1","B3","B2","B4","B2","B4","B1","B3","B3","B1","B4","B2","B4","B2","B3","B1")
MAPPING={"B1":"C1","B2":"C2","B3":"C3","B4":"C4"} # SYNTHETIC ONLY
CANDIDATE="SINGLE_LAB_CANDIDATE_ONLY"
MODEL=load()

def finite(x):
    if type(x) not in (float,int): return False
    try: return math.isfinite(x)
    except (OverflowError,TypeError,ValueError): return False

def fixture(vals=(6e-8,-6e-8,0.,0.),hours=6.):
    v=dict(zip(("C1","C2","C3","C4"),vals))
    return [{"block_index":i+1,"blind_code":code,"configuration":MAPPING[code],
             "eta":v[MAPPING[code]],"included":True,"accepted_hours":hours}
            for i,code in enumerate(SEQ)]

def preview(rows,u_c=UNCERTAINTY,threshold=THRESHOLD,*,mapping=MAPPING,synthetic=True):
    if not synthetic: return {"status":"PENDING","reason":"physical_not_authorized"}
    if not finite(u_c) or not finite(threshold) or u_c<=0 or threshold<=0:
        return {"status":"INVALID_INPUT"}
    if u_c!=UNCERTAINTY or threshold!=THRESHOLD: return {"status":"INVALID_INPUT"}
    if mapping is None: return {"status":"PENDING"}
    if not isinstance(mapping,dict) or set(mapping)!=set(SEQ) or set(mapping.values())!={"C1","C2","C3","C4"}:
        return {"status":"INVALID_INPUT"}
    if not isinstance(rows,list): return {"status":"INVALID_INPUT"}
    if len(rows)!=16: return {"status":"PENDING"}
    fields={"block_index","blind_code","configuration","eta","included","accepted_hours"}
    for i,row in enumerate(rows):
        if not isinstance(row,dict) or not fields.issubset(row): return {"status":"INVALID_INPUT"}
        if type(row["block_index"]) is not int or row["block_index"]!=i+1: return {"status":"INVALID_INPUT"}
        if row["blind_code"]!=SEQ[i] or row["configuration"]!=mapping[row["blind_code"]]:
            return {"status":"INVALID_INPUT"}
        if type(row["included"]) is not bool: return {"status":"INVALID_INPUT"}
        if not finite(row["eta"]) or not finite(row["accepted_hours"]): return {"status":"INVALID_INPUT"}
        if not row["included"] or row["accepted_hours"]<6: return {"status":"PENDING"}
    try: result=MODEL(rows,u_c,threshold)
    except (ArithmeticError,ValueError,TypeError,OverflowError): return {"status":"INVALID_INPUT"}
    vals=[result.get("swap_estimator"),result.get("null_estimator"),*result.get("means",{}).values()]
    if not all(finite(x) for x in vals): return {"status":"INVALID_INPUT"}
    return result

class Tests(unittest.TestCase):
    def accepted(self,rows,**kw): return preview(rows,**kw)["status"]==CANDIDATE
    def test_v2_original_null_control_correction_retained(self):
        self.assertEqual(MODEL(fixture((6e-8,-6e-8,1e-6,-1e-6)),UNCERTAINTY,THRESHOLD)["status"],"NO_CANDIDATE")
    def test_v2_nonfinite_signal_acceptance_exposed(self):
        self.assertEqual(MODEL(fixture((math.inf,-math.inf,0,0)),UNCERTAINTY,THRESHOLD)["status"],CANDIDATE)
        self.assertFalse(self.accepted(fixture((math.inf,-math.inf,0,0))))
    def test_v2_finite_overflow_acceptance_exposed(self):
        with self.assertRaises(OverflowError): MODEL(fixture((1e308,-1e308,0,0)),UNCERTAINTY,THRESHOLD)
        self.assertFalse(self.accepted(fixture((1e308,-1e308,0,0))))
    def test_v2_infinite_uncertainty_acceptance_exposed(self):
        self.assertEqual(MODEL(fixture(),math.inf,THRESHOLD)["status"],CANDIDATE)
        self.assertFalse(self.accepted(fixture(),u_c=math.inf))
    def test_v2_negative_threshold_acceptance_exposed(self):
        self.assertEqual(MODEL(fixture((1e-9,-1e-9,0,0)),UNCERTAINTY,-1)["status"],CANDIDATE)
        self.assertFalse(self.accepted(fixture(),threshold=-1))
    def test_preview_clean_synthetic_case(self): self.assertTrue(self.accepted(fixture()))
    def test_preview_not_authorized_for_physical_execution(self):
        self.assertFalse(self.accepted(fixture(),synthetic=False))
    def test_preview_no_blind_mapping(self): self.assertFalse(self.accepted(fixture(),mapping=None))
    def test_preview_rejects_all_nonfinite_eta_positions(self):
        for i in range(16):
            for x in (math.inf,-math.inf,math.nan):
                rows=fixture();rows[i]["eta"]=x;self.assertFalse(self.accepted(rows))
    def test_preview_rejects_bad_budgets(self):
        for x in (math.inf,-math.inf,math.nan,0.,-1.,True,"2"):
            self.assertFalse(self.accepted(fixture(),u_c=x))
            self.assertFalse(self.accepted(fixture(),threshold=x))
    def test_preview_rejects_non_numeric_eta_and_hours(self):
        for key in ("eta","accepted_hours"):
            for x in (True,"6",None,math.nan,math.inf,10**10000):
                rows=fixture();rows[0][key]=x;self.assertFalse(self.accepted(rows))
    def test_preview_requires_exact_16_blocks(self):
        self.assertFalse(self.accepted(fixture()[:-1]))
        self.assertFalse(self.accepted(fixture()+fixture()[:1]))
        self.assertFalse(self.accepted(fixture()[:4]))
    def test_preview_requires_ordered_blind_codes_and_ids(self):
        for key,value in (("block_index",2),("blind_code","B2"),("configuration","C2")):
            rows=fixture();rows[0][key]=value;self.assertFalse(self.accepted(rows))
    def test_preview_requires_six_accepted_hours_per_block(self):
        self.assertTrue(self.accepted(fixture(hours=6)))
        self.assertFalse(self.accepted(fixture(hours=5.999999)))
    def test_preview_exclusion_is_not_silently_discarded(self):
        rows=fixture();rows[0]["included"]=False;self.assertFalse(self.accepted(rows))
    def test_preview_rejects_bad_included_values(self):
        rows=fixture();rows[0]["included"]="yes";self.assertFalse(self.accepted(rows))
    def test_preview_retains_signal_and_null_gate(self):
        self.assertTrue(self.accepted(fixture()))
        self.assertFalse(self.accepted(fixture((2e-8,-2e-8,0,0))))
        self.assertFalse(self.accepted(fixture((6e-8,-6e-8,1e-6,-1e-6))))
    def test_preview_within_control_cancellation_is_still_unresolved(self):
        rows=fixture();pos=[i for i,v in enumerate(rows) if v["configuration"]=="C3"]
        rows[pos[0]]["eta"]=1e-4;rows[pos[1]]["eta"]=-1e-4
        self.assertTrue(self.accepted(rows))
if __name__=="__main__": unittest.main(verbosity=2)
