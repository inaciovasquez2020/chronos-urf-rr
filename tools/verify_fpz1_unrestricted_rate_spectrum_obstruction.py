from pathlib import Path
import json

lean = Path("lean/Chronos/Frontier/FPz1UnrestrictedRateSpectrumObstruction.lean").read_text()
status = Path("docs/status/CHRONOS_FPZ1_UNRESTRICTED_RATE_SPECTRUM_OBSTRUCTION_2026_05_16.md").read_text()
artifact = json.loads(Path("artifacts/chronos/fpz1_unrestricted_rate_spectrum_obstruction_2026_05_16.json").read_text())

required_lean = [
    "def RateSpectrumIsolation",
    "def InverseNatRateSequence",
    "theorem inverseNatRateSequence_refutes_rateSpectrumIsolation",
    "¬ RateSpectrumIsolation",
]

for phrase in required_lean:
    assert phrase in lean, phrase

required_status = [
    "UNRESTRICTED_RATE_SPECTRUM_OBSTRUCTION_ONLY",
    "does not construct concrete Chronos admissible objects",
    "unrestricted RateSpectrumIsolation",
    "unrestricted UniversalFiberEntropyGap",
    "unrestricted Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
]

for phrase in required_status:
    assert phrase in status, phrase

assert artifact["status"] == "UNRESTRICTED_RATE_SPECTRUM_OBSTRUCTION_ONLY"
assert "inverseNatRateSequence_refutes_rateSpectrumIsolation" in artifact["proved"]

combined = (lean + "\n" + status + "\n" + json.dumps(artifact)).lower()

forbidden = [
    "constructs concrete chronos admissible objects",
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

print("FPz1 unrestricted rate-spectrum obstruction verified.")
