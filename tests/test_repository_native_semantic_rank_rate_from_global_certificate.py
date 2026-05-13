import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_repository_native_semantic_rank_rate_from_global_certificate_verifier():
    subprocess.run(
        ["python3", "tools/verify_repository_native_semantic_rank_rate_from_global_certificate.py"],
        cwd=ROOT,
        check=True,
    )

def test_repository_native_semantic_rank_rate_from_global_certificate_lean_surface():
    text = (ROOT / "Chronos/Frontier/RepositoryNativeSemanticRankRateFromGlobalCertificate.lean").read_text()
    assert "RepositoryNativeSemanticRankRateExhaustiveness_from_global_certificate" in text
    assert "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n" in text
    assert "exact h" in text
    assert "axiom " not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_repository_native_semantic_rank_rate_from_global_certificate_boundary():
    text = (ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_SEMANTIC_RANK_RATE_FROM_GLOBAL_CERTIFICATE_2026_05_13.md").read_text()
    assert "CONDITIONAL_REDUCTION_ONLY" in text
    assert "native_semantic_rank_rate_certificate_exists" in text
    assert "This is a conditional reduction only." in text
    assert "UniversalFiberEntropyGap" in text
    assert "P_ne_NP" in text
