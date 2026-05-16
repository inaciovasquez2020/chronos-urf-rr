from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FPz1ConditionalUnrestrictedRoute.lean").read_text()
status = Path("docs/status/CHRONOS_FPZ1_CONDITIONAL_UNRESTRICTED_ROUTE_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fpz1_conditional_unrestricted_route_2026_05_16.json").read_text())

required_lean = [
    "def RateSpectrumIsolation",
    "def EntropyFaithfulLowerEnvelope",
    "def QuantitativeEntropyFaithfulSemanticFiberizationUnrestricted",
    "def DepthBridgeUnrestricted",
    "def ChronosRRUnrestricted",
    "theorem rateSpectrumIsolation_and_lowerEnvelope_to_quantitativeUnrestricted",
    "theorem fpz1_conditional_unrestricted_route",
]

for phrase in required_lean:
    assert phrase in lean, phrase

required_status = [
    "CONDITIONAL_UNRESTRICTED_ROUTE_ONLY",
    "RateSpectrumIsolation",
    "EntropyFaithfulLowerEnvelope",
    "DepthBridgeUnrestricted",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

assert artifact["status"] == "CONDITIONAL_UNRESTRICTED_ROUTE_ONLY"
assert "fpz1_conditional_unrestricted_route" in artifact["proved"]
assert "RateSpectrumIsolation" in artifact["requires"]
assert "EntropyFaithfulLowerEnvelope" in artifact["requires"]
assert "DepthBridgeUnrestricted" in artifact["requires"]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()

forbidden = [
    "proves ratespectrumisolation",
    "proves entropyfaithfullowerenvelope",
    "proves depthbridgeunrestricted",
    "proves unrestricted universalfiberentropygap",
    "proves unrestricted chronos-rr",
    "proves unrestricted h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves a clay problem",
    "clay closure",
]

for token in forbidden:
    assert token not in combined, token

print("FPz1 conditional unrestricted route verified.")
