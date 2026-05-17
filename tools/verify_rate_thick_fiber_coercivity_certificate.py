from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RateThickFiberCoercivityCertificate.lean"
DOC = ROOT / "docs/status/RATE_THICK_FIBER_COERCIVITY_CERTIFICATE_2026_05_17.md"
ARTIFACT = ROOT / "artifacts/chronos/rate_thick_fiber_coercivity_certificate_2026_05_17.json"

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    required_lean = [
        "def UniformRateThickFiberLowerBoundCertificate",
        "rateThickFiberCoercivity_from_uniformLowerBoundCertificate",
        "rateThickFiberEntropyGap_from_uniformLowerBoundCertificate",
        "universalFiberEntropyGap_from_uniformLowerBoundCertificate",
        "chronosRR_from_uniformLowerBoundCertificate",
        "FRONTIER_OPEN",
        "CERTIFICATE_INPUT_SURFACE_ONLY",
    ]

    for phrase in required_lean:
        assert phrase in lean, phrase

    required_doc = [
        "Status: FRONTIER_OPEN / CERTIFICATE_INPUT_SURFACE_ONLY",
        "Certificate input",
        "Conditional consequences",
        "Boundary",
        "Does not construct:",
        "UniformRateThickFiberLowerBoundCertificate",
        "RateThickFiberCoercivity",
        "UniversalFiberEntropyGap",
        "unrestricted Chronos-RR",
        "P vs NP",
        "any Clay problem",
    ]

    for phrase in required_doc:
        assert phrase in doc, phrase

    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["surface"] == "CERTIFICATE_INPUT_SURFACE_ONLY"
    assert artifact["certificate"] == "UniformRateThickFiberLowerBoundCertificate lambda"

    forbidden = [
        "unconditional Chronos-RR",
        "unconditional H4.1/FGL",
        "solves P vs NP",
        "solves any Clay problem",
        "Clay closure",
    ]

    combined = "\n".join([lean, doc, json.dumps(artifact)])
    for phrase in forbidden:
        assert phrase not in combined, phrase

    print("Rate-thick fiber coercivity certificate surface verified.")

if __name__ == "__main__":
    main()
