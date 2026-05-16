from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FPz1RateThickDomainGap.lean").read_text()
status = Path("docs/status/CHRONOS_FPZ1_RATE_THICK_DOMAIN_GAP_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fpz1_rate_thick_domain_gap_2026_05_16.json").read_text())

required_lean = [
    "def RateThickDomain",
    "def EntropyFaithfulLowerEnvelopeAt",
    "def EntropyFaithfulLowerEnvelope",
    "def RateDependentUniversalFiberEntropyGap",
    "theorem rateThickDomain_positive_rate_isolated",
    "theorem entropyFaithfulLowerEnvelopeAt_to_rateDependentUniversalFiberEntropyGap",
    "theorem entropyFaithfulLowerEnvelope_to_rateDependentUniversalFiberEntropyGap",
]

for phrase in required_lean:
    assert phrase in lean, phrase

required_status = [
    "RATE_THICK_DOMAIN_GAP_CONDITIONAL_ONLY",
    "RateThickDomain",
    "RateDependentUniversalFiberEntropyGap",
    "EntropyFaithfulLowerEnvelopeAt",
    "unrestricted UniversalFiberEntropyGap is false/open",
    "InverseNatRateSequence",
    "unrestricted RateSpectrumIsolation",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

assert artifact["status"] == "RATE_THICK_DOMAIN_GAP_CONDITIONAL_ONLY"
assert artifact["unrestricted_gap_status"] == "FALSE_UNDER_INVERSE_RATE_OBSTRUCTION_OTHERWISE_OPEN"
assert "RateThickDomain" in artifact["defined"]
assert "RateDependentUniversalFiberEntropyGap" in artifact["defined"]
assert "entropyFaithfulLowerEnvelopeAt_to_rateDependentUniversalFiberEntropyGap" in artifact["proved"]
assert "entropyFaithfulLowerEnvelope_to_rateDependentUniversalFiberEntropyGap" in artifact["proved"]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()

forbidden = [
    "proves unrestricted ratespectrumisolation",
    "proves entropyfaithfullowerenvelope",
    "proves unrestricted universalfiberentropygap",
    "unrestricted universalfiberentropygap is proved",
    "unrestricted universalfiberentropygap is closed",
    "closes unrestricted universalfiberentropygap",
    "proves unrestricted chronos-rr",
    "proves unrestricted h4.1/fgl",
    "proves p vs np",
    "solves p vs np",
    "solves a clay problem",
    "clay closure"
]

for token in forbidden:
    assert token not in combined, token

print("FPz1 rate-thick domain gap verified.")
