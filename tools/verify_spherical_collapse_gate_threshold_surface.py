import json
from pathlib import Path

lean_path = Path("Chronos/Frontier/SphericalCollapseGateThresholdSurface.lean")
artifact_path = Path("artifacts/chronos/spherical_collapse_gate_threshold_surface_2026_05_15.json")
status_path = Path("docs/status/SPHERICAL_COLLAPSE_GATE_THRESHOLD_SURFACE_2026_05_15.md")
root_path = Path("Chronos.lean")

lean = lean_path.read_text()
artifact = json.loads(artifact_path.read_text())
status = status_path.read_text()
root = root_path.read_text()

required_lean = [
    "structure SphericalCollapseGateInput",
    "misnerSharpMass : Nat",
    "arealRadius : Nat",
    "positiveRadius : 0 < arealRadius",
    "def SphericalCollapseGate",
    "S.arealRadius <= 2 * S.misnerSharpMass",
    "def TrappedOrMarginalSphericalSurface",
    "theorem spherical_collapse_gate_implies_trapped_or_marginal_surface",
    "def SphericalCollapseGateBoundary : Prop := True",
]
for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.SphericalCollapseGateThresholdSurface" in root

assert artifact["status"] == "RESTRICTED_SPHERICAL_THRESHOLD_SURFACE"
assert artifact["restricted_surface_closure"] is True
assert artifact["unrestricted_theorem_level_closure"] is False
assert artifact["lean_module"] == "Chronos.Frontier.SphericalCollapseGateThresholdSurface"

required_status = [
    "Status: RESTRICTED_SPHERICAL_THRESHOLD_SURFACE",
    "Restricted spherical threshold surface only.",
    "spherical_collapse_gate_implies_trapped_or_marginal_surface",
    "Does not prove:",
    "nonspherical collapse exclusion",
    "Cosmic Censorship",
    "Hoop Conjecture",
    "unrestricted UniversalBoundaryCompactness",
    "unrestricted Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay-problem closure",
]
for phrase in required_status:
    assert phrase in status, phrase

artifact_for_claim_scan = dict(artifact)
artifact_for_claim_scan.pop("forbidden_claims", None)

combined = "\n".join(
    [
        lean,
        json.dumps(artifact_for_claim_scan, sort_keys=True),
        status,
    ]
).lower()

for forbidden in artifact["forbidden_claims"]:
    assert forbidden.lower() not in combined, forbidden

print("Spherical collapse gate threshold surface verified.")
