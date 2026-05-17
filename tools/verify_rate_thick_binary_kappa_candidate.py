from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/RateThickBinaryKappaCandidate.lean"
DOC = ROOT / "docs/status/RATE_THICK_BINARY_KAPPA_CANDIDATE_2026_05_17.md"
ARTIFACT = ROOT / "artifacts/chronos/rate_thick_binary_kappa_candidate_2026_05_17.json"

def main() -> None:
    lean = LEAN.read_text()
    doc = DOC.read_text()
    artifact = json.loads(ARTIFACT.read_text())

    required_lean = [
        "noncomputable def binaryKappaCandidate",
        "noncomputable def mAryKappaCandidate",
        "def BinaryKappaAdmissible",
        "def MAryKappaAdmissible",
        "def BinaryKappaPositiveTarget",
        "binaryKappaCandidate_pos",
        "binaryKappaPositiveTarget_proved",
        "def MAryKappaPositiveTarget",
        "def EntropyMinDominatesBinaryCoefficientTarget",
        "def BinaryCandidateUniformFiberMassBound",
        "def BinaryKappaCandidateCertificateInputs",
        "uniformLowerBoundCertificate_from_binaryCandidateInputs",
        "rateThickFiberCoercivity_from_binaryCandidateInputs",
        "universalFiberEntropyGap_from_binaryCandidateInputs",
        "FRONTIER_OPEN",
        "BINARY_KAPPA_POSITIVITY_PROVED",
    ]

    for phrase in required_lean:
        assert phrase in lean, phrase

    required_doc = [
        "Status: FRONTIER_OPEN / BINARY_KAPPA_POSITIVITY_PROVED",
        "Candidate coefficient",
        "General m-ary coefficient",
        "Isolated targets",
        "BinaryKappaPositiveTarget",
        "EntropyMinDominatesBinaryCoefficientTarget",
        "BinaryCandidateUniformFiberMassBound",
        "Closed conditional consequences",
        "Boundary",
        "Binary kappa positivity proved under `BinaryKappaAdmissible λ`.",
        "P vs NP",
        "any Clay problem",
    ]

    for phrase in required_doc:
        assert phrase in doc, phrase

    assert artifact["status"] == "FRONTIER_OPEN"
    assert artifact["surface"] == "BINARY_KAPPA_POSITIVITY_PROVED"
    assert "BinaryKappaPositiveTarget lambda" in artifact["proved_targets"]

    forbidden = [
        "proves entropy-minimum domination",
        "proves uniform fiber-mass bound",
        "unconditional Chronos-RR",
        "unconditional H4.1/FGL",
        "solves P vs NP",
        "solves any Clay problem",
        "Clay closure",
    ]

    combined = "\n".join([lean, doc, json.dumps(artifact)])
    for phrase in forbidden:
        assert phrase not in combined, phrase

    print("Rate-thick binary kappa candidate verified.")

if __name__ == "__main__":
    main()
