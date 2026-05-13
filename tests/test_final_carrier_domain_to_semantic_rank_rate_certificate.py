import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_final_carrier_domain_semantic_rank_rate_verifier():
    subprocess.run(
        ["python3", "tools/verify_final_carrier_domain_to_semantic_rank_rate_certificate.py"],
        cwd=ROOT,
        check=True,
    )

def test_final_carrier_domain_semantic_rank_rate_lean_surface():
    text = (ROOT / "Chronos/Frontier/FinalCarrierDomainToSemanticRankRateCertificate.lean").read_text()
    assert "RepositoryNativeSemanticRankRateExhaustiveness" in text
    assert "FinalCarrierDomain_to_RepositoryNativeSemanticRankRateDomain" in text
    assert "FinalCarrierDomain_to_native_SemanticRankRateCertificate_exists" in text
    assert "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n" in text

def test_final_carrier_domain_semantic_rank_rate_boundary():
    text = (ROOT / "docs/status/CHRONOS_FINAL_CARRIER_DOMAIN_TO_SEMANTIC_RANK_RATE_CERTIFICATE_2026_05_13.md").read_text()
    assert "CONDITIONAL_IMPORTER_ONLY" in text
    assert "This is a conditional importer surface only." in text
    assert "It does not prove:" in text
    assert "UniversalFiberEntropyGap" in text
    assert "P_ne_NP" in text
