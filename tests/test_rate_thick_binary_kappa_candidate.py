import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_rate_thick_binary_kappa_candidate_verifier():
    subprocess.run(
        ["python3", "tools/verify_rate_thick_binary_kappa_candidate.py"],
        cwd=ROOT,
        check=True,
    )

def test_rate_thick_binary_kappa_candidate_lean_surface():
    lean = (ROOT / "lean/Chronos/Frontier/RateThickBinaryKappaCandidate.lean").read_text()
    assert "noncomputable def binaryKappaCandidate" in lean
    assert "noncomputable def mAryKappaCandidate" in lean
    assert "def BinaryKappaPositiveTarget" in lean
    assert "def EntropyMinDominatesBinaryCoefficientTarget" in lean
    assert "def BinaryCandidateUniformFiberMassBound" in lean
    assert "rateThickFiberCoercivity_from_binaryCandidateInputs" in lean

def test_rate_thick_binary_kappa_candidate_boundary():
    doc = (ROOT / "docs/status/RATE_THICK_BINARY_KAPPA_CANDIDATE_2026_05_17.md").read_text()
    assert "Candidate coefficient surface only." in doc
    assert "positivity of binaryKappaCandidate λ" in doc
    assert "entropy-minimum domination" in doc
    assert "uniform fiber-mass bound" in doc
    assert "unrestricted RateThickFiberCoercivity λ" in doc
    assert "unrestricted UniversalFiberEntropyGap λ" in doc
    assert "P vs NP" in doc
    assert "any Clay problem" in doc
