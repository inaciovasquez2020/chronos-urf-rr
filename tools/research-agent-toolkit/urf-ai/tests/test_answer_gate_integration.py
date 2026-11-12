"""Adversarial end-to-end tests against the real in-memory CSTS journal."""
from __future__ import annotations
import unittest
from copy import deepcopy
from urf_ai.csts import ClaimJournal
from urf_ai.evidence import attest, bindings, digest
from urf_ai.answer_gate import assess_from_journal

KEY = b"synthetic-only-local-research-gate-2026" * 2
BINARY = "f" * 64
ROLES = {"author": "AUTHOR", "verifier": "VERIFIER", "reviewer": "REVIEWER"}
ALLOW = {"lean": BINARY}


def initial(cid="c"):
    return {"claim_id": cid, "semantic_version": 1, "kind": "THEOREM",
            "state": "OPEN", "proposition": "synthetic proposition",
            "scope": {"domain": "synthetic"}, "assumptions": [],
            "dependencies": [], "frontier": [], "boundaries": [],
            "source_revision": {"repo": "fixture", "commit": "a"*40},
            "author": "author"}


def receipt(c):
    return attest({**bindings(c), "schema": "urf-ai.receipt.v1",
                   "checker": {"name": "lean", "binary_digest": BINARY},
                   "checker_result": "PASS", "proof_digest": "e"*64,
                   "axioms": ["Classical.choice", "Quot.sound", "propext"],
                   "author": "author", "verifier": "verifier",
                   "reviewer": "reviewer"}, KEY)


def proposal(c, assertion="PROVED"):
    return {"claim_id": c["claim_id"],
            "semantic_version": c["semantic_version"],
            "proposition_digest": digest(c["proposition"]),
            "scope_digest": digest(c["scope"]),
            "source_revision": deepcopy(c["source_revision"]),
            "assertion": assertion}


class TestAuthenticatedAnswerGate(unittest.TestCase):
    def setUp(self):
        self.j = ClaimJournal(KEY, ROLES, ALLOW)
        self.j.apply(event_id="register", kind="REGISTER", claim_id="c",
                     actor="author", expected_version=0, payload=initial(),
                     reason="synthetic")
    def promote(self):
        self.j.apply(event_id="promote", kind="PROMOTE_PROVED", claim_id="c",
                     actor="reviewer", expected_version=1,
                     payload={"receipt": receipt(self.j.claim("c"))},
                     reason="synthetic")
    def check(self, status="PROVED"):
        return assess_from_journal(self.j, proposal(self.j.claim("c"), status))
    def test_open_denies_proved(self): self.assertFalse(self.check().allowed)
    def test_open_allows_open(self): self.assertTrue(self.check("OPEN").allowed)
    def test_signed_promotion_allows_ledger_status(self):
        self.promote()
        r = self.check()
        self.assertTrue(r.allowed)
        self.assertEqual(r.reasons, ("AUTHENTICATED_CSTS_STATUS_ONLY",))
    def test_tampered_record_denied(self):
        self.promote()
        p = proposal(self.j.claim("c"))
        self.j.records["c"]["proposition"] = "forged"
        self.assertFalse(assess_from_journal(self.j, p).allowed)
    def test_unlogged_proved_record_denied(self):
        self.promote()
        forged = deepcopy(self.j.records["c"])
        forged["claim_id"] = "forged"
        self.j.records["forged"] = forged
        self.assertFalse(self.j.audit_events())
        self.assertFalse(assess_from_journal(self.j, proposal(forged)).allowed)

    def test_atomic_claim_snapshot_is_copy(self):
        self.promote()
        snapshot = self.j.audited_claim("c")
        snapshot["state"] = "OPEN"
        self.assertEqual(self.j.claim("c")["state"], "PROVED")
        self.assertTrue(self.j.audit_events())

    def test_atomic_claim_rejects_unlogged_record(self):
        self.promote()
        forged = deepcopy(self.j.records["c"])
        forged["claim_id"] = "unlogged"
        self.j.records["unlogged"] = forged
        with self.assertRaises(ValueError):
            self.j.audited_claim("unlogged")

    def test_tampered_event_denied(self):
        self.promote()
        self.j.events[0]["reason"] = "forged"
        self.assertFalse(self.check().allowed)
    def test_forged_dict_journal_denied(self):
        self.assertFalse(assess_from_journal({"state": "PROVED"},
                                             proposal(self.j.claim("c"))).allowed)
    def test_overridden_audit_denied(self):
        class Fake(ClaimJournal):
            def audit_events(self): return True
        self.assertFalse(assess_from_journal(Fake(KEY, ROLES, ALLOW),
                                             proposal(self.j.claim("c"))).allowed)
    def test_scope_swap_denied(self):
        self.promote()
        p = proposal(self.j.claim("c"))
        p["scope_digest"] = "b"*64
        self.assertFalse(assess_from_journal(self.j, p).allowed)
    def test_revision_swap_denied(self):
        self.promote()
        p = proposal(self.j.claim("c"))
        p["source_revision"]["commit"] = "b"*40
        self.assertFalse(assess_from_journal(self.j, p).allowed)
    def test_bool_semantic_version_denied(self):
        self.promote()
        p = proposal(self.j.claim("c"))
        p["semantic_version"] = True
        self.assertFalse(assess_from_journal(self.j, p).allowed)
    def test_revision_revokes_old_proof(self):
        self.promote()
        old = proposal(self.j.claim("c"))
        self.j.apply(event_id="revise", kind="REVISE", claim_id="c",
                     actor="author", expected_version=1,
                     payload={"changes": {"proposition": "revised"}},
                     reason="synthetic")
        self.assertFalse(assess_from_journal(self.j, old).allowed)
        self.assertFalse(self.check().allowed)
    def test_transitively_stale_proof_denied(self):
        self.promote()
        c = self.j.claim("c")
        child = initial("d")
        child["dependencies"] = [{"claim_id": "c", "semantic_version": 1,
                                  "proposition_digest": digest(c["proposition"])}]
        self.j.apply(event_id="register-child", kind="REGISTER", claim_id="d",
                     actor="author", expected_version=0, payload=child,
                     reason="synthetic")
        self.j.apply(event_id="promote-child", kind="PROMOTE_PROVED", claim_id="d",
                     actor="reviewer", expected_version=1,
                     payload={"receipt": receipt(self.j.claim("d"))},
                     reason="synthetic")
        self.assertTrue(assess_from_journal(self.j, proposal(self.j.claim("d"))).allowed)
        self.j.apply(event_id="revise", kind="REVISE", claim_id="c",
                     actor="author", expected_version=1,
                     payload={"changes": {"proposition": "new"}},
                     reason="synthetic")
        self.assertFalse(assess_from_journal(self.j, proposal(self.j.claim("d"))).allowed)
    def test_unknown_claim_denied(self):
        p = proposal(self.j.claim("c"))
        p["claim_id"] = "missing"
        self.assertFalse(assess_from_journal(self.j, p).allowed)
    def test_unsupported_lean_claim_denied(self):
        self.assertFalse(self.check("LEAN_VERIFIED").allowed)
    def test_missing_binding_denied(self):
        p = proposal(self.j.claim("c"))
        del p["scope_digest"]
        self.assertFalse(assess_from_journal(self.j, p).allowed)


if __name__ == "__main__":
    unittest.main()
