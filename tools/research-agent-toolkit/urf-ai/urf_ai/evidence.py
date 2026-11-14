"""Authenticated *receipt records*; authentication does not prove mathematics."""
from __future__ import annotations
import hashlib
import hmac
import json
import re
from copy import deepcopy

HEX64 = re.compile(r"^[0-9a-f]{64}$")

def canonical(value: object) -> bytes:
    """JSON restricted to unambiguous UTF-8 canonical output; floats prohibited."""
    def check(obj):
        if isinstance(obj, float):
            raise ValueError("floating-point values prohibited from canonical evidence")
        if isinstance(obj, dict):
            if not all(isinstance(k, str) for k in obj):
                raise ValueError("non-string JSON key")
            for v in obj.values(): check(v)
        elif isinstance(obj, list):
            for v in obj: check(v)
        elif not isinstance(obj, (int, str, bool, type(None))):
            raise ValueError("unsupported JSON value")
    check(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()

def attest(payload: dict, key: bytes) -> dict:
    if len(key) < 32:
        raise ValueError("attestation secret must be 32 bytes or longer")
    return {"payload": deepcopy(payload), "mac": hmac.new(key, canonical(payload), hashlib.sha256).hexdigest()}

def authenticate(envelope: object, key: bytes) -> bool:
    if not isinstance(envelope, dict) or set(envelope) != {"payload", "mac"}:
        return False
    if not isinstance(envelope["payload"], dict) or not isinstance(envelope["mac"], str) or not HEX64.fullmatch(envelope["mac"]):
        return False
    if len(key) < 32:
        return False
    try:
        expected = hmac.new(key, canonical(envelope["payload"]), hashlib.sha256).hexdigest()
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(expected, envelope["mac"])

RECEIPT_FIELDS = {"schema", "claim_id", "semantic_version", "proposition_digest", "scope_digest", "assumptions_digest", "dependencies_digest", "source_revision", "proof_digest", "checker", "checker_result", "axioms", "author", "verifier", "reviewer"}

def bindings(claim: dict) -> dict:
    return {"claim_id": claim["claim_id"], "semantic_version": claim["semantic_version"],
            "proposition_digest": digest(claim["proposition"]),
            "scope_digest": digest(claim["scope"]),
            "assumptions_digest": digest(claim.get("assumptions", [])),
            "dependencies_digest": digest(claim.get("dependencies", [])),
            "source_revision": deepcopy(claim["source_revision"])}

def validated_receipt(envelope: object, claim: dict, key: bytes, checker_allowlist: dict, role_map: dict) -> tuple[bool, str]:
    """Verify a delegated checker's authenticated attestation, not the proof itself."""
    if not authenticate(envelope, key):
        return False, "receipt authentication failed"
    p = envelope["payload"]
    if not RECEIPT_FIELDS <= set(p) or p["schema"] != "urf-ai.receipt.v1":
        return False, "receipt schema invalid"
    if any(p.get(k) != v for k, v in bindings(claim).items()):
        return False, "receipt not bound to claim identity/scope/assumptions/dependencies/revision"
    if p["checker_result"] != "PASS" or not HEX64.fullmatch(str(p["proof_digest"])):
        return False, "checker result or proof digest invalid"
    checker = p["checker"]
    if (not isinstance(checker, dict) or not HEX64.fullmatch(str(checker.get("binary_digest", "")))
        or checker_allowlist.get(checker.get("name")) != checker.get("binary_digest")):
        return False, "untrusted checker binary"
    if p["axioms"] != ["Classical.choice", "Quot.sound", "propext"]:
        return False, "unapproved or missing axiom audit"
    if p["author"] != claim.get("author"):
        return False, "claimed author mismatch"
    if not (p["author"] != p["verifier"] and p["author"] != p["reviewer"] and p["verifier"] != p["reviewer"]):
        return False, "independence rule failed"
    if role_map.get(p["verifier"]) != "VERIFIER" or role_map.get(p["reviewer"]) != "REVIEWER":
        return False, "missing trusted verifier or reviewer role"
    return True, "authenticated scoped attestation (mathematics delegated to checker)"
