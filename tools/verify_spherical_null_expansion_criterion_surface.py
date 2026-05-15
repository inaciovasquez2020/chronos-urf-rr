import json
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/SphericalNullExpansionCriterionSurface.lean")
artifact_path = Path("artifacts/chronos/spherical_null_expansion_criterion_surface_2026_05_15.json")
status_path = Path("docs/status/SPHERICAL_NULL_EXPANSION_CRITERION_SURFACE_2026_05_15.md")
root_path = Path("Chronos.lean")

lean = lean_path.read_text()
artifact = json.loads(artifact_path.read_text())
status = status_path.read_text()
root = root_path.read_text()

required_lean = [
    "structure SphericalNullExpansionInput",
    "outgoingExpansion : Int",
    "ingoingExpansion : Int",
    "def FutureTrappedSphericalSurface",
    "S.outgoingExpansion < 0 ∧ S.ingoingExpansion < 0",
    "def FutureOuterMarginalSphericalSurface",
    "S.outgoingExpansion <= 0 ∧ S.ingoingExpansion < 0",
    "def TrappedOrMarginalByNullExpansions",
    "theorem trapped_spherical_null_expansions_imply_trapped_or_marginal",
    "theorem marginal_spherical_null_expansions_imply_trapped_or_marginal",
    "def SphericalNullExpansionCriterionBoundary : Prop := True",
]
for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.SphericalNullExpansionCriterionSurface" in root

assert artifact["status"] == "RESTRICTED_SPHERICAL_NULL_EXPANSION_SURFACE"
assert artifact["restricted_surface_closure"] is True
assert artifact["unrestricted_theorem_level_closure"] is False
assert artifact["lean_module"] == "Chronos.Frontier.SphericalNullExpansionCriterionSurface"

required_status = [
    "Status: RESTRICTED_SPHERICAL_NULL_EXPANSION_SURFACE",
    "Restricted spherical null-expansion criterion surface only.",
    "trapped_spherical_null_expansions_imply_trapped_or_marginal",
    "marginal_spherical_null_expansions_imply_trapped_or_marginal",
    "Does not prove:",
    "compactness-threshold-to-null-expansion bridge",
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

print("Spherical null-expansion criterion surface verified.")
