from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/ChronosRRConditionalFromUniversalGap.lean").read_text()
root = Path("lean/Chronos.lean").read_text()
artifact = json.loads(Path("artifacts/chronos/chronos_rr_conditional_from_universal_gap_2026_05_14.json").read_text())
status = Path("docs/status/CHRONOS_RR_CONDITIONAL_FROM_UNIVERSAL_GAP_2026_05_14.md").read_text()

required_lean = [
    "structure ChronosRRConditionalWitness",
    "def ChronosRRConditionalFromNonProp",
    "theorem chronosRRConditional_from_universalFiberEntropyGap",
    "theorem chronosRRConditional_from_nonprop_invariant",
    "UniversalFiberEntropyGapFromNonProp I",
    "universalFiberEntropyGap_from_nonprop_invariant I",
    "LAKE_NATIVE_CHRONOS_RR_CONDITIONAL_FROM_UNIVERSAL_GAP_CLOSED",
]

for token in required_lean:
    assert token in lean, token

assert "import Chronos.Frontier.ChronosRRConditionalFromUniversalGap" in root
assert artifact["status"] == "LAKE_NATIVE_CHRONOS_RR_CONDITIONAL_FROM_UNIVERSAL_GAP_CLOSED"
assert artifact["conditional_promotion_closed"] is True
assert artifact["unrestricted_theorem_closure"] is False

required_boundary = [
    "Lake-native Chronos-RR conditional promotion only.",
    "Does not prove unrestricted Chronos-RR closure.",
    "Does not prove H4.1/FGL closure.",
    "Does not prove P vs NP closure.",
    "Does not prove any Clay-problem closure.",
]

for phrase in required_boundary:
    assert phrase in status, phrase

for forbidden in [
    "unrestricted Chronos-RR is proved",
    "Chronos-RR is closed",
    "H4.1/FGL is closed",
    "P vs NP is proved",
    "Clay problem is solved",
]:
    assert forbidden not in lean
    assert forbidden not in status

print("ChronosRRConditionalFromUniversalGap verified.")
