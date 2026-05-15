import json
from pathlib import Path

artifact_path = Path("artifacts/chronos/quasi_local_collapse_dichotomy_conditional_frontier_2026_05_15.json")
status_path = Path("docs/status/QUASI_LOCAL_COLLAPSE_DICHOTOMY_CONDITIONAL_FRONTIER_2026_05_15.md")

artifact = json.loads(artifact_path.read_text())
status = status_path.read_text()

assert artifact["status"] == "CONDITIONAL_FRONTIER_FRAMEWORK_ONLY"
assert artifact["theorem_level_closure"] is False
assert artifact["object"] == "QuasiLocalCollapseDichotomy"

required_assumptions = {"CosmicCensorship", "HoopConjecture"}
seen_assumptions = {item["name"] for item in artifact["assumptions"]}
assert required_assumptions <= seen_assumptions

for item in artifact["assumptions"]:
    assert item["status"] == "OPEN_CONJECTURE"

required_fields = [
    "smooth connected noncompact 3-manifold Sigma",
    "Riemannian asymptotically flat metric h",
    "symmetric extrinsic curvature tensor K",
    "matter field Phi satisfying the Einstein-matter equations in the maximal Cauchy development",
    "Hamiltonian constraint",
    "momentum constraint",
    "dominant energy condition",
    "finite ADM mass",
    "no past trapped boundary",
    "generic nondegeneracy",
]
for field in required_fields:
    assert field in artifact["data_class"]["fields"], field

required_status_phrases = [
    "Status: CONDITIONAL_FRONTIER_FRAMEWORK_ONLY",
    "Cosmic Censorship and Hoop Conjecture as explicit assumptions",
    "Does not prove:",
    "unrestricted `QL_CollapseGate`",
    "unrestricted nonspherical collapse exclusion",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted `UniversalBoundaryCompactness`",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay-problem closure",
]
for phrase in required_status_phrases:
    assert phrase in status, phrase

artifact_for_claim_scan = dict(artifact)
artifact_for_claim_scan.pop("forbidden_claims", None)

combined = "\n".join(
    [
        json.dumps(artifact_for_claim_scan, sort_keys=True),
        status,
    ]
).lower()

for forbidden in artifact["forbidden_claims"]:
    assert forbidden.lower() not in combined, forbidden

print("Quasi-local collapse dichotomy conditional frontier verified.")
