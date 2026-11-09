"""Conservative theorem-ledger classifier built on authenticated scoped evidence."""
from __future__ import annotations
from .evidence import validated_receipt

REQUIRED = ("exact_statement", "domain", "hypothesis", "construction", "obstruction", "necessity_direction", "sufficiency_direction", "boundary", "proof_ledger", "dependency_ledger", "claim_boundary_ledger")

def classify(claim: dict, envelope: object, key: bytes, allowlist: dict, roles: dict) -> dict:
    cid = claim.get("claim_id", "UNKNOWN")
    def status(name, reason): return {"claim_id": cid, "classification": name, "reason": reason}
    if claim.get("claimed_domain_exceeds_proven_domain", False):
        return status("OVERCLAIMED_LEDGER", "claimed scope exceeds formal scope")
    if claim.get("benchmark_match_only", False):
        return status("BENCHMARK_MATCH_ONLY", "benchmark matching is not verification")
    if claim.get("kind") != "THEOREM":
        return status("INCOMPLETE_LEDGER", "non-theorem record cannot receive theorem status")
    if not isinstance(claim.get("scope"),dict) or not claim["scope"].get("domain"):
        return status("INCOMPLETE_LEDGER", "formal theorem scope not specified")
    missing = next((x for x in REQUIRED if claim.get("objects", {}).get(x) != "present"), None)
    if missing or claim.get("missing_proof_object", False):
        return status("INCOMPLETE_LEDGER", missing or "MissingProofObject")
    is_conditional = claim.get("open_hypothesis", False) or any(a.get("status") != "DISCHARGED" for a in claim.get("assumptions", []))
    if any(f.get("status") == "OPEN" and f.get("blocking", True) for f in claim.get("frontier", [])):
        return status("INCOMPLETE_LEDGER", "blocking frontier")
    try:
        ok, reason = validated_receipt(envelope, claim, key, allowlist, roles)
    except (KeyError, ValueError, TypeError) as exc:
        return status("INCOMPLETE_LEDGER", f"invalid binding: {type(exc).__name__}")
    if not ok: return status("INCOMPLETE_LEDGER",reason)
    if is_conditional: return status("COMPLETE_CONDITIONAL_LEDGER", "authenticated conditional evidence with remaining explicit hypotheses")
    return status("COMPLETE_UNCONDITIONAL_LEDGER",reason)
