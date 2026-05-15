import json
from pathlib import Path

lean_path = Path("lean/Chronos/Frontier/SphericalCompactnessNullExpansionBridgeSurface.lean")
artifact_path = Path("artifacts/chronos/spherical_compactness_null_expansion_bridge_surface_2026_05_15.json")
status_path = Path("docs/status/SPHERICAL_COMPACTNESS_NULL_EXPANSION_BRIDGE_SURFACE_2026_05_15.md")
root_path = Path("Chronos.lean")

lean = lean_path.read_text()
artifact = json.loads(artifact_path.read_text())
status = status_path.read_text()
root = root_path.read_text()

required_lean = [
    "import Chronos.Frontier.SphericalCollapseGateThresholdSurface",
    "import Chronos.Frontier.SphericalNullExpansionCriterionSurface",
    "structure SphericalCompactnessNullExpansionBridgeInput",
    "thresholdInput : SphericalCollapseGateInput",
    "expansionInput : SphericalNullExpansionInput",
    "threshold_to_outer_marginal",
    "SphericalCollapseGate thresholdInput",
    "FutureOuterMarginalSphericalSurface expansionInput",
    "def SphericalCompactnessToNullExpansionBridge",
    "theorem spherical_compactness_threshold_implies_outer_marginal_by_bridge",
    "theorem spherical_compactness_threshold_implies_trapped_or_marginal_by_bridge",
    "def SphericalCompactnessNullExpansionBridgeBoundary : Prop := True",
]
for phrase in required_lean:
    assert phrase in lean, phrase

assert "import Chronos.Frontier.SphericalCompactnessNullExpansionBridgeSurface" in root

assert artifact["status"] == "CONDITIONAL_RESTRICTED_SPHERICAL_BRIDGE_SURFACE"
assert artifact["restricted_interface_closure"] is True
assert artifact["geometric_bridge_proved"] is False
assert artifact["unrestricted_theorem_level_closure"] is False
assert artifact["lean_module"] == "Chronos.Frontier.SphericalCompactnessNullExpansionBridgeSurface"

required_status = [
    "Status: CONDITIONAL_RESTRICTED_SPHERICAL_BRIDGE_SURFACE",
    "Conditional restricted spherical bridge interface only.",
    "spherical_compactness_threshold_implies_outer_marginal_by_bridge",
    "spherical_compactness_threshold_implies_trapped_or_marginal_by_bridge",
    "Does not prove:",
    "geometric threshold-to-null-expansion theorem",
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

print("Spherical compactness-to-null-expansion bridge surface verified.")
