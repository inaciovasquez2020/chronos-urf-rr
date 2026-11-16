"""Offline replay for the Chronos expanding-circle scalar detector benchmark.

Run this file with Python 3. Embedded GitHub source snapshots are checked
against the blob IDs observed at the documented commits before replay.
"""
import hashlib
import itertools
import sys
from types import ModuleType

MODEL_REVISION = "1714d0e17ed4c4bfa7aff01019ffacca23397aaf"
TOOLKIT_REVISION = "b0fd6ef97cf0b73658ad7067d0272084c2d60622"
MODEL = ("5043dc2235c523663dce3a5e77a08f29ca18679e", "# Exact expanding-circle 5D Einstein example — research-only certificate\n\n**Status:** mathematical construction with exact finite symbolic checks; **not** a viable cosmology or evidence for a physically necessary fifth dimension. No Lean proof or independent review is claimed.\n\n## Hypotheses\nFive-dimensional Lorentzian Einstein gravity with cosmological constant Λ5=6h², h>0; no other matter stress tensor. The fifth coordinate y is identified modulo 2π; all four spatial directions in the local metric share the same time-dependent scale factor. Consider\n\n```\nds5² = -dt² + exp(2ht) (dx1² + dx2² + dx3² + dy²).\n```\n\nThe coordinate-tensor certificate computes all components and checks `Ric5 = 4 h² g5` and `Scal5 = 20 h²`. Consequently the Einstein equation with Λ5=6h² holds. With the cosmological constant placed on the geometric side, material T_AB=0 obeys NEC, and the cosmological term vanishes on null contraction.\n\n## Four-dimensional Einstein-frame reduction\nThe circle radius is `b(t)=exp(ht)`, the Jordan metric is `gJ=-dt²+exp(2ht) dᶋx²`, and the Einstein metric is `gE=b*gJ`. For `tau = (2/h)exp(ht/2)`,\n\n```\nb(tau)=(h*tau/2)²\naE(tau)=(h*tau/2)³\nH_E=3/tau\nphi=sqrt(3/2)*log(b)\nV(phi)=6h²*exp(-sqrt(2/3)*phi)=24/tau².\n```\n\nWith the reduced four-dimensional gravitational normalization fixed by the Einstein-frame action, `3H_E² = (1/2)phi_dot²+V`, `H_E_dot=-(1/2)phi_dot²`, and `phi_ddot+3H_E phi_dot+dV/dphi=0`. Thus `aE''(tau)>0` for `tau>0`.\n\n## Failure boundary\nThe circle **is not stabilized**, since `b ∝ tau²`. In the chosen Einstein-frame normalization, `m1,E=b^(-3/2)`, so `m1,E/H_E=8/(3h³tau²)→0` at late times. This signals eventual failure of a zero-mode-only low-energy truncation. No full mode spectrum, perturbative stability, matter coupling, data comparison, or physical necessity claim is supplied.\n\n## Reproduction and provenance\nRun from the repository root, with its environment supplying SymPy:\n\n```bash\npython3 -B research/5d/expanding_circle_exact_audit.py\n```\n\nAll checks are exact symbolic assertions. On an assertion failure or resource timeout, classify the run as **FAIL** or **INCOMPLETE**, never PASS. The starting mathematical model is the familiar flat-slicing higher-dimensional de Sitter metric, here with a compact coordinate. The research contribution is a reproducible scoped check, **not** a claim of novelty.\n\n**Validation gate:** run the script and applicable repository CI at the exact PR HEAD, inspect the diff, and only merge after required checks complete. The local Mac working tree was not inspected. This addition is independent of the repository's cosmological data analyses.\n")
TOOLKIT = {
    "evidence": ("86a5fb893580a46dcd0373fca9f4561aa9345ab1", "\"\"\"Authenticated *receipt records*; authentication does not prove mathematics.\"\"\"\nfrom __future__ import annotations\nimport hashlib\nimport hmac\nimport json\nimport re\nfrom copy import deepcopy\n\nHEX64 = re.compile(r\"^[0-9a-f]{64}$\")\n\ndef canonical(value: object) -> bytes:\n    \"\"\"JSON restricted to unambiguous UTF-8 canonical output; floats prohibited.\"\"\"\n    def check(obj):\n        if isinstance(obj, float):\n            raise ValueError(\"floating-point values prohibited from canonical evidence\")\n        if isinstance(obj, dict):\n            if not all(isinstance(k, str) for k in obj):\n                raise ValueError(\"non-string JSON key\")\n            for v in obj.values(): check(v)\n        elif isinstance(obj, list):\n            for v in obj: check(v)\n        elif not isinstance(obj, (int, str, bool, type(None))):\n            raise ValueError(\"unsupported JSON value\")\n    check(value)\n    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(\",\", \":\"), allow_nan=False).encode(\"utf-8\")\n\ndef digest(value: object) -> str:\n    return hashlib.sha256(canonical(value)).hexdigest()\n\ndef attest(payload: dict, key: bytes) -> dict:\n    if len(key) < 32:\n        raise ValueError(\"attestation secret must be 32 bytes or longer\")\n    return {\"payload\": deepcopy(payload), \"mac\": hmac.new(key, canonical(payload), hashlib.sha256).hexdigest()}\n\ndef authenticate(envelope: object, key: bytes) -> bool:\n    if not isinstance(envelope, dict) or set(envelope) != {\"payload\", \"mac\"}:\n        return False\n    if not isinstance(envelope[\"payload\"], dict) or not isinstance(envelope[\"mac\"], str) or not HEX64.fullmatch(envelope[\"mac\"]):\n        return False\n    if len(key) < 32:\n        return False\n    try:\n        expected = hmac.new(key, canonical(envelope[\"payload\"]), hashlib.sha256).hexdigest()\n    except (ValueError, TypeError):\n        return False\n    return hmac.compare_digest(expected, envelope[\"mac\"])\n\nRECEIPT_FIELDS = {\"schema\", \"claim_id\", \"semantic_version\", \"proposition_digest\", \"scope_digest\", \"assumptions_digest\", \"dependencies_digest\", \"source_revision\", \"proof_digest\", \"checker\", \"checker_result\", \"axioms\", \"author\", \"verifier\", \"reviewer\"}\n\ndef bindings(claim: dict) -> dict:\n    return {\"claim_id\": claim[\"claim_id\"], \"semantic_version\": claim[\"semantic_version\"],\n            \"proposition_digest\": digest(claim[\"proposition\"]),\n            \"scope_digest\": digest(claim[\"scope\"]),\n            \"assumptions_digest\": digest(claim.get(\"assumptions\", [])),\n            \"dependencies_digest\": digest(claim.get(\"dependencies\", [])),\n            \"source_revision\": deepcopy(claim[\"source_revision\"])}\n\ndef validated_receipt(envelope: object, claim: dict, key: bytes, checker_allowlist: dict, role_map: dict) -> tuple[bool, str]:\n    \"\"\"Verify a delegated checker's authenticated attestation, not the proof itself.\"\"\"\n    if not authenticate(envelope, key):\n        return False, \"receipt authentication failed\"\n    p = envelope[\"payload\"]\n    if not RECEIPT_FIELDS <= set(p) or p[\"schema\"] != \"urf-ai.receipt.v1\":\n        return False, \"receipt schema invalid\"\n    if any(p.get(k) != v for k, v in bindings(claim).items()):\n        return False, \"receipt not bound to claim identity/scope/assumptions/dependencies/revision\"\n    if p[\"checker_result\"] != \"PASS\" or not HEX64.fullmatch(str(p[\"proof_digest\"])):\n        return False, \"checker result or proof digest invalid\"\n    checker = p[\"checker\"]\n    if (not isinstance(checker, dict) or not HEX64.fullmatch(str(checker.get(\"binary_digest\", \"\")))\n        or checker_allowlist.get(checker.get(\"name\")) != checker.get(\"binary_digest\")):\n        return False, \"untrusted checker binary\"\n    if p[\"axioms\"] != [\"Classical.choice\", \"Quot.sound\", \"propext\"]:\n        return False, \"unapproved or missing axiom audit\"\n    if p[\"author\"] != claim.get(\"author\"):\n        return False, \"claimed author mismatch\"\n    if not (p[\"author\"] != p[\"verifier\"] and p[\"author\"] != p[\"reviewer\"] and p[\"verifier\"] != p[\"reviewer\"]):\n        return False, \"independence rule failed\"\n    if role_map.get(p[\"verifier\"]) != \"VERIFIER\" or role_map.get(p[\"reviewer\"]) != \"REVIEWER\":\n        return False, \"missing trusted verifier or reviewer role\"\n    return True, \"authenticated scoped attestation (mathematics delegated to checker)\"\n"),
    "classifier": ("80c39e1fe7e2660d30dba51c6db49953dcabfdeb", "\"\"\"Conservative theorem-ledger classifier built on authenticated scoped evidence.\"\"\"\nfrom __future__ import annotations\nfrom .evidence import validated_receipt\n\nREQUIRED = (\"exact_statement\", \"domain\", \"hypothesis\", \"construction\", \"obstruction\", \"necessity_direction\", \"sufficiency_direction\", \"boundary\", \"proof_ledger\", \"dependency_ledger\", \"claim_boundary_ledger\")\n\ndef classify(claim: dict, envelope: object, key: bytes, allowlist: dict, roles: dict) -> dict:\n    cid = claim.get(\"claim_id\", \"UNKNOWN\")\n    def status(name, reason): return {\"claim_id\": cid, \"classification\": name, \"reason\": reason}\n    if claim.get(\"claimed_domain_exceeds_proven_domain\", False):\n        return status(\"OVERCLAIMED_LEDGER\", \"claimed scope exceeds formal scope\")\n    if claim.get(\"benchmark_match_only\", False):\n        return status(\"BENCHMARK_MATCH_ONLY\", \"benchmark matching is not verification\")\n    if claim.get(\"kind\") != \"THEOREM\":\n        return status(\"INCOMPLETE_LEDGER\", \"non-theorem record cannot receive theorem status\")\n    if not isinstance(claim.get(\"scope\"),dict) or not claim[\"scope\"].get(\"domain\"):\n        return status(\"INCOMPLETE_LEDGER\", \"formal theorem scope not specified\")\n    missing = next((x for x in REQUIRED if claim.get(\"objects\", {}).get(x) != \"present\"), None)\n    if missing or claim.get(\"missing_proof_object\", False):\n        return status(\"INCOMPLETE_LEDGER\", missing or \"MissingProofObject\")\n    is_conditional = claim.get(\"open_hypothesis\", False) or any(a.get(\"status\") != \"DISCHARGED\" for a in claim.get(\"assumptions\", []))\n    if any(f.get(\"status\") == \"OPEN\" and f.get(\"blocking\", True) for f in claim.get(\"frontier\", [])):\n        return status(\"INCOMPLETE_LEDGER\", \"blocking frontier\")\n    try:\n        ok, reason = validated_receipt(envelope, claim, key, allowlist, roles)\n    except (KeyError, ValueError, TypeError) as exc:\n        return status(\"INCOMPLETE_LEDGER\", f\"invalid binding: {type(exc).__name__}\")\n    if not ok: return status(\"INCOMPLETE_LEDGER\",reason)\n    if is_conditional: return status(\"COMPLETE_CONDITIONAL_LEDGER\", \"authenticated conditional evidence with remaining explicit hypotheses\")\n    if any(b.get(\"active\",False) and b.get(\"blocks_proved\",False) for b in claim.get(\"boundaries\", [])):\n        return status(\"INCOMPLETE_LEDGER\", \"active proof-blocking boundary lock\")\n    return status(\"COMPLETE_UNCONDITIONAL_LEDGER\",reason)\n"),
}


def verify_blob(item):
    expected, source = item
    data = source.encode("utf-8")
    header = f"blob {len(data)}".encode() + b"\0"
    if hashlib.sha1(header + data).hexdigest() != expected:
        raise ValueError(f"Git blob mismatch for {expected}")
    return source


def load_toolkit():
    package = ModuleType("urf_ai")
    package.__path__ = []
    sys.modules["urf_ai"] = package
    for name, item in TOOLKIT.items():
        qualified_name = f"urf_ai.{name}"
        module = ModuleType(qualified_name)
        sys.modules[qualified_name] = module
        exec(compile(verify_blob(item), qualified_name, "exec"), module.__dict__)


def require(condition, description):
    if not condition:
        raise ValueError(description)


def main():
    verify_blob(MODEL)
    load_toolkit()
    from urf_ai.classifier import classify
    from urf_ai.evidence import digest

    near = [t*t-r*r for t, r in itertools.product(range(22, 27), range(14, 19))]
    far = [t*t-r*r for t, r in itertools.product(range(22, 27), range(30, 35))]
    require((len(near), min(near), max(near)) == (25, 160, 480), "near bounds")
    require((len(far), max(far)) == (25, -224), "far bounds")
    # Squared amplitude bound using pi < 22/7.
    require(120**2 * 24**3 * 7**10 > 16 * 5**3 * 22**10, "amplitude bound")
    record = {
        "claim_id": "chronos.expanding_circle.local_scalar_detector",
        "scope": {"domain": "synthetic normalized scalar field"},
        "model_revision": MODEL_REVISION,
        "model_blob": MODEL[0],
        "toolkit_revision": TOOLKIT_REVISION,
        "toolkit_blobs": {name: item[0] for name, item in TOOLKIT.items()},
        "cases": {"near": near, "far": far},
        "threshold": {"numerator": 1, "denominator": 240},
    }
    verdict = classify(
        {**record, "kind": "THEOREM", "benchmark_match_only": True},
        None, b"", {}, {},
    )
    require(verdict["classification"] == "BENCHMARK_MATCH_ONLY", "classification")
    require(digest(record) == digest(dict(reversed(list(record.items())))), "canonical digest")
    try:
        digest({**record, "threshold": 1/240})
    except ValueError:
        pass
    else:
        raise ValueError("floating-point threshold accepted")
    print("SOURCE_BLOBS = PASS (3)")
    print("FINITE_CASES = PASS (50)")
    print("URF_AI_CLASSIFICATION =", verdict["classification"])
    print("EVIDENCE_SHA256 =", digest(record))


if __name__ == "__main__":
    main()
