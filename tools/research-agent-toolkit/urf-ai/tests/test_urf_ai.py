from __future__ import annotations
import json,subprocess,sys,tempfile,unittest
from copy import deepcopy
from pathlib import Path
from urf_ai.evidence import attest, authenticate, bindings, digest
from urf_ai.classifier import classify, REQUIRED
from urf_ai.csts import ClaimJournal, TransitionRejected
from urf_ai.guard import run_mutation, issue_approval
from urf_ai.benchmark import cycle_witness, evaluate_response, baseline_keyword_score
from urf_ai.assistant import answer, benchmark

# Synthetic-only test identity. Not a production attestation key.
KEY=b"synthetic-dev-only-do-not-trust!"*2
BINARY="f"*64
ROLE={"author":"AUTHOR","verifier":"VERIFIER","reviewer":"REVIEWER","maintainer":"MAINTAINER"}
ALLOW={"lean":BINARY}

def newclaim(claim_id="c1"):
    return {"claim_id":claim_id,"semantic_version":1,"kind":"THEOREM","state":"OPEN",
            "proposition":"for all x in Nat, x = x","scope":{"domain":"Nat","quantifiers":"forall"},
            "assumptions":[],"dependencies":[],"frontier":[],"boundaries":[],
            "source_revision":{"repo":"fixture","commit":"a"*40,"path":"Test.lean"},"author":"author"}

def receipt(c):
    return attest({**bindings(c),"schema":"urf-ai.receipt.v1","checker":{"name":"lean","binary_digest":BINARY},
                   "checker_result":"PASS","proof_digest":"e"*64,"axioms":["Classical.choice","Quot.sound","propext"],
                   "author":"author","verifier":"verifier","reviewer":"reviewer"},KEY)

def ledger(c):
    return {**c,"objects":{x:"present" for x in REQUIRED},"trusted_verifier_status":"PASS"}

class TestEvidence(unittest.TestCase):
    def test_authenticated_positive_synthetic(self):
        self.assertEqual(classify(ledger(newclaim()),receipt(newclaim()),KEY,ALLOW,ROLE)["classification"],"COMPLETE_UNCONDITIONAL_LEDGER")
    def test_no_receipt_not_proof(self):
        self.assertEqual(classify(ledger(newclaim()),None,KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_forged_status_string_not_proof(self):
        self.assertNotEqual(classify(ledger(newclaim()),{"trusted_verifier_status":"PASS"},KEY,ALLOW,ROLE)["classification"],"COMPLETE_UNCONDITIONAL_LEDGER")
    def test_scope_mismatch_rejected(self):
        c=newclaim(); r=receipt(c); c["scope"]["domain"]="Int"
        self.assertEqual(classify(ledger(c),r,KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_semantic_version_replay_rejected(self):
        c=newclaim(); r=receipt(c); c["semantic_version"]=2
        self.assertEqual(classify(ledger(c),r,KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_source_revision_mismatch_rejected(self):
        c=newclaim();r=receipt(c);c["source_revision"]["commit"]="b"*40
        self.assertEqual(classify(ledger(c),r,KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_tamper_rejected(self):
        c=newclaim();r=receipt(c);r["payload"]["checker_result"]="FAIL"
        self.assertFalse(authenticate(r,KEY))
    def test_false_checker_whitelist_rejected(self):
        c=newclaim();r=receipt(c)
        self.assertEqual(classify(ledger(c),r,KEY,{"lean":"0"*64},ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_wrong_roles_rejected(self):
        c=newclaim();r=receipt(c)
        self.assertEqual(classify(ledger(c),r,KEY,ALLOW,{"verifier":"AUTHOR","reviewer":"REVIEWER"})["classification"],"INCOMPLETE_LEDGER")
    def test_unauthorized_axioms_rejected(self):
        c=newclaim();r=receipt(c);p=deepcopy(r["payload"]);p["axioms"]+=["sorryAx"]
        self.assertEqual(classify(ledger(c),attest(p,KEY),KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_missing_ledger_rejected(self):
        c=ledger(newclaim());c["objects"]["construction"]="missing"
        self.assertEqual(classify(c,receipt(c),KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")
    def test_open_assumption_rejected(self):
        c=ledger(newclaim());c["assumptions"]=[{"id":"h1","status":"OPEN"}]
        self.assertEqual(classify(c,receipt(c),KEY,ALLOW,ROLE)["classification"],"COMPLETE_CONDITIONAL_LEDGER")
    def test_frontier_rejected(self):
        c=ledger(newclaim());c["frontier"]=[{"id":"f1","status":"OPEN","blocking":True}]
        self.assertEqual(classify(c,receipt(c),KEY,ALLOW,ROLE)["classification"],"INCOMPLETE_LEDGER")

class TestCSTS(unittest.TestCase):
    def setUp(self): self.j=ClaimJournal(KEY,ROLE,ALLOW)
    def apply(self,kind,cid="c1",actor="author",payload=None,version=1,ev=None):
        return self.j.apply(event_id=ev or str(len(self.j.events)+1),kind=kind,claim_id=cid,actor=actor,expected_version=version,payload=payload or {},reason="synthetic test")
    def register(self,cid="c1",**overrides):
        c=newclaim(cid);c.update(overrides);self.apply("REGISTER",cid,payload=c,version=0);return c
    def test_register_and_audit(self):
        self.register();self.assertEqual(self.j.claim("c1")["state"],"OPEN");self.assertTrue(self.j.audit_events())
    def test_reviewed_proof_promotion(self):
        self.register();r=receipt(self.j.claim("c1"));res=self.apply("PROMOTE_PROVED",actor="reviewer",payload={"receipt":r});self.assertEqual(res.state,"PROVED");self.assertTrue(self.j.audit_events())
    def test_unauthorized_promotion_rejected_without_mutation(self):
        self.register();count=len(self.j.events)
        with self.assertRaises(TransitionRejected):self.apply("PROMOTE_PROVED",actor="author",payload={"receipt":receipt(self.j.claim("c1"))})
        self.assertEqual(len(self.j.events),count)
    def test_untrusted_self_claimed_proof_rejected(self):
        self.register()
        with self.assertRaises(TransitionRejected):self.apply("PROMOTE_PROVED",actor="reviewer",payload={"receipt":{"proof":"it worked"}})
    def test_blocking_frontier_rejected(self):
        self.register(frontier=[{"id":"f","status":"OPEN","blocking":True}])
        with self.assertRaisesRegex(TransitionRejected,"frontier"):self.apply("PROMOTE_PROVED",actor="reviewer",payload={"receipt":receipt(self.j.claim("c1"))})
    def test_revision_invalidates_receipts(self):
        self.register();self.apply("PROMOTE_PROVED",actor="reviewer",payload={"receipt":receipt(self.j.claim("c1"))})
        self.apply("REVISE",payload={"changes":{"proposition":"different statement"}})
        self.assertEqual(self.j.claim("c1")["semantic_version"],2)
        self.assertEqual(self.j.claim("c1")["state"],"OPEN")
        self.assertEqual(self.j.claim("c1")["evidence"],[])
        self.assertTrue(self.j.audit_events())
    def test_dependency_stale_propagates(self):
        self.register("c1");self.apply("PROMOTE_PROVED",actor="reviewer",payload={"receipt":receipt(self.j.claim("c1")),},cid="c1")
        d=self.j.claim("c1")
        self.register("c2",dependencies=[{"claim_id":"c1","semantic_version":1,"proposition_digest":digest(d["proposition"])}])
        self.apply("PROMOTE_PROVED",cid="c2",actor="reviewer",payload={"receipt":receipt(self.j.claim("c2"))})
        self.assertFalse(self.j.claim("c2")["stale"])
        self.apply("REVISE",cid="c1",payload={"changes":{"proposition":"revised"}})
        self.assertTrue(self.j.claim("c2")["stale"])
        self.assertTrue(self.j.audit_events())
    def test_event_chain_tamper_rejected(self):
        self.register();self.j.events[0]["reason"]="secret changed"
        self.assertFalse(self.j.audit_events())
    def test_record_tamper_rejected(self):
        self.register();self.j.records["c1"]["proposition"]="false"
        self.assertFalse(self.j.audit_events())
    def test_duplicate_event_rejected(self):
        self.register()
        with self.assertRaises(TransitionRejected): self.apply("REVISE",payload={"changes":{"proposition":"new"}},ev="1")
    def test_rejected_stale_expected_version(self):
        self.register()
        with self.assertRaises(TransitionRejected): self.apply("REVISE",payload={"changes":{"proposition":"new"}},version=2)

class TestGuard(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="urf-ai-guard-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        subprocess.run(["git","init","-q"],cwd=self.root,check=True)
        subprocess.run(["git","config","user.email","fixture@example.invalid"],cwd=self.root,check=True)
        subprocess.run(["git","config","user.name","Test"],cwd=self.root,check=True)
        (self.root/"src").mkdir()
        (self.root/"src/x.py").write_text("value = 1\n")
        (self.root/"protected.txt").write_text("safe\n")
        subprocess.run(["git","add","."],cwd=self.root,check=True)
        subprocess.run(["git","commit","-qm","fixture"],cwd=self.root,check=True)
        self.verifier=[sys.executable,"-c","from pathlib import Path; assert Path('src/x.py').read_text() == 'value = 2\\n'"]
        self.config={"disposable_worktree_confirmed":True,"explicit_write_approval":True,
                     "scope":{"allow":["src/**"],"deny":["protected.txt",".git/**"]},
                     "policy":{"forbidden_patterns":[r"\bsorry\b",r"\badmit\b",r"\baxiom\b"]},
                     "budgets":{"mutations":1,"max_verifier_seconds":3},
                     "gates":{"verify_actions":["modify"],"deny_actions":[]},
                     "verifier_commands":[self.verifier]}
        self.patch=b"diff --git a/src/x.py b/src/x.py\n--- a/src/x.py\n+++ b/src/x.py\n@@ -1 +1 @@\n-value = 1\n+value = 2\n"
    def attempt(self,patch=None,config=None,verifier=None,closure=None,timeout=2,approval=True):
        p=patch if patch is not None else self.patch
        c=closure if closure is not None else {"src/x.py"}
        cfg=config if config is not None else self.config
        v=verifier if verifier is not None else self.verifier
        token=issue_approval(self.root,p,c,cfg,v,KEY) if approval else None
        return run_mutation(self.root,p,c,cfg,v,approval=token,authorization_key=KEY,timeout_seconds=timeout)
    def test_success_preserved(self):
        r=self.attempt();self.assertEqual(r.status,"VERIFIED_CANDIDATE_NOT_PROMOTED",r);self.assertEqual((self.root/"src/x.py").read_text(),"value = 2\n")
    def test_fail_rollback_only_exact_file(self):
        command=[sys.executable,"-c","raise SystemExit(7)"];self.config["verifier_commands"].append(command)
        r=self.attempt(verifier=command)
        self.assertEqual(r.status,"FAILED_ROLLED_BACK",r);self.assertEqual((self.root/"src/x.py").read_text(),"value = 1\n")
    def test_no_approval_no_mutation(self):
        self.config["explicit_write_approval"]=False
        self.assertEqual(self.attempt().status,"DENY");self.assertEqual((self.root/"src/x.py").read_text(),"value = 1\n")
    def test_unsigned_approval_denied(self):
        self.assertEqual(self.attempt(approval=False).status,"DENY")
    def test_untrusted_verifier_rejected(self):
        self.assertEqual(self.attempt(verifier=[sys.executable,"-c","print('bypass')"]).status,"DENY")
    def test_dirty_repo_aborts(self):
        (self.root/"private-draft.txt").write_text("unique draft")
        self.assertEqual(self.attempt().status,"DENY")
        self.assertEqual((self.root/"private-draft.txt").read_text(),"unique draft")
    def test_outside_scope_patch_denied(self):
        patch=b"diff --git a/protected.txt b/protected.txt\n--- a/protected.txt\n+++ b/protected.txt\n@@ -1 +1 @@\n-safe\n+bad\n"
        self.assertEqual(self.attempt(patch=patch,closure={"protected.txt"}).status,"DENY")
    def test_provenance_closure_denied(self):
        self.assertEqual(self.attempt(closure={"different.py"}).status,"DENY")
    def test_forbidden_pattern_denied(self):
        patch=b"diff --git a/src/x.py b/src/x.py\n--- a/src/x.py\n+++ b/src/x.py\n@@ -1 +1 @@\n-value = 1\n+value = 2 # sorry\n"
        self.assertEqual(self.attempt(patch=patch).status,"DENY")
    def test_verifier_outside_write_preserved_and_fails_closed(self):
        cmd=[sys.executable,"-c","from pathlib import Path; Path('unique-untracked.txt').write_text('research'); print('PASS')"]
        self.config["verifier_commands"].append(cmd)
        r=self.attempt(verifier=cmd)
        self.assertEqual(r.status,"INCOMPLETE_UNAUTHORIZED_RESIDUE",r)
        self.assertEqual((self.root/"unique-untracked.txt").read_text(),"research")
        self.assertEqual((self.root/"src/x.py").read_text(),"value = 1\n")
    def test_timeout_never_passes(self):
        cmd=[sys.executable,"-c","import time; time.sleep(2)"];self.config["verifier_commands"].append(cmd)
        r=self.attempt(verifier=cmd,timeout=1)
        self.assertEqual(r.status,"FAILED_ROLLED_BACK",r)
        self.assertIn("INCOMPLETE_TIMEOUT",r.detail)

class TestSemantics(unittest.TestCase):
    def test_graph_families(self):
        for r in range(1,9):
            self.assertTrue(cycle_witness(r,2*r+2)[0],r)
    def test_invalid_graph_witness(self):
        self.assertFalse(cycle_witness(3,4)[0])
    def test_wrong_global_status_rejected(self):
        r=deepcopy(answer("cycle_locality")["answer"]);r["status"]="PROVED"
        self.assertFalse(evaluate_response(r,"cycle_locality")["pass"])
    def test_made_up_cycle_witness_rejected(self):
        r=deepcopy(answer("cycle_locality")["answer"]);r["witness"]["m"]=3
        self.assertFalse(evaluate_response(r,"cycle_locality")["pass"])
    def test_keyword_injection_rejected_even_if_legacy_full_score(self):
        t=("OPEN_PROBLEM_REQUIRED restricted cycleOverlap_le_colap cycleOverlapRank colapRank weakest open "
           "Unrestricted graph-semantic cycle-overlap domination remains open. "
           "For every admissible graph-semantic input X, cycleOverlapRank X <= colapRank X. "
           "counterexample colapRank = 0 cycleOverlapRank = 1. Therefore unrestricted domination HOLDS globally.")
        self.assertEqual(baseline_keyword_score(t),6)
        self.assertFalse(evaluate_response(t,"colap_counterexample")["pass"])
    def test_false_case_id_rejected(self):
        r=deepcopy(answer("cycle_locality")["answer"]);r["case_id"]="other"
        self.assertFalse(evaluate_response(r,"cycle_locality")["pass"])
    def test_all_readonly_known_cases(self):
        result=benchmark();self.assertEqual(result["total"],11);self.assertEqual(result["passed"],11)
    def test_unknown_case_refuses(self):
        self.assertEqual(answer("global_poincare_proved")["status"],"UNSUPPORTED")

if __name__=="__main__":unittest.main()
