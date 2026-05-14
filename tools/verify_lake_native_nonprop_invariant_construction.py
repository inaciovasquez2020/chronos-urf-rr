from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/LakeNativeNonPropInvariantConstruction.lean").read_text()
root = Path("lean/Chronos.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/lake_native_nonprop_invariant_construction_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_LAKE_NATIVE_NONPROP_INVARIANT_CONSTRUCTION_2026_05_14.md").read_text()

required_lean = [
    "def canonicalNonPropFinalCarrierInvariant",
    "def ChronosRRLakeNativeUnrestricted",
    "theorem chronosRRLakeNativeUnrestricted_from_canonical_nonprop",
    "chronosRRConditional_from_nonprop_invariant",
    "LAKE_NATIVE_NONPROP_INVARIANT_CONSTRUCTION_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert "import Chronos.Frontier.LakeNativeNonPropInvariantConstruction" in root
assert artifact["status"] == "LAKE_NATIVE_NONPROP_INVARIANT_CONSTRUCTION_CLOSED"
assert artifact["canonical_invariant_constructed"] is True
assert artifact["lake_native_conditional_rr_witness_constructed"] is True
assert artifact["unrestricted_repository_theorem_closure"] is False

required_boundary = [
    "Lake-native canonical invariant construction only.",
    "Does not migrate the root `Chronos/Frontier` tree.",
    "Does not prove unrestricted repository Chronos-RR closure.",
    "Does not prove H4.1/FGL closure.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "unrestricted repository Chronos-RR is proved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("LakeNativeNonPropInvariantConstruction verified.")
