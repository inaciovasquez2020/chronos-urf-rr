from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FPz1RestrictedLambdaSolvedSurface.lean").read_text()
status = Path("docs/status/CHRONOS_FPZ1_RESTRICTED_LAMBDA_SOLVED_SURFACE_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fpz1_restricted_lambda_solved_surface_2026_05_16.json").read_text())

required_lean = [
    "def ChronosAdmissibleLambda",
    "def QuantitativeEntropyFaithfulSemanticFiberizationLambda",
    "def EntropyFaithfulLowerEnvelope",
    "def DepthBridgeLambda",
    "def ChronosRRLambda",
    "theorem restrictedRateSpectrumIsolation",
    "theorem lowerEnvelope_to_quantitativeLambda",
    "theorem fpz1_restricted_lambda_route",
]

for phrase in required_lean:
    assert phrase in lean, phrase

required_status = [
    "RESTRICTED_LAMBDA_ROUTE_SOLVED_SURFACE_ONLY",
    "unrestricted RateSpectrumIsolation",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

assert artifact["status"] == "RESTRICTED_LAMBDA_ROUTE_SOLVED_SURFACE_ONLY"
assert "fpz1_restricted_lambda_route" in artifact["closed_surface"]
assert "EntropyFaithfulLowerEnvelope" in artifact["requires"]
assert "DepthBridgeLambda" in artifact["requires"]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()

forbidden = [
    "proves unrestricted ratespectrumisolation",
    "proves unrestricted uniformrategap",
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

print("FPz1 restricted lambda solved surface verified.")
