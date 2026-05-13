import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_repository_native_semantic_rank_rate_exhaustiveness_realization_verifier():
    subprocess.run(
        ["python3", "tools/verify_repository_native_semantic_rank_rate_exhaustiveness_realization.py"],
        cwd=ROOT,
        check=True,
    )

def test_repository_native_semantic_rank_rate_exhaustiveness_realization_lean_surface():
    text = (ROOT / "Chronos/Frontier/RepositoryNativeSemanticRankRateExhaustivenessRealization.lean").read_text()
    assert "def RepositoryNativeSemanticRankRateWitnessObligation : Prop" in text
    assert "∀ c : ChronosCarrierData" in text
    assert "FinalCarrierDomain c" in text
    assert "∃ n : Nat, SemanticRankRateCertificate ChronosNativeCarrierFamily n" in text
    assert "RepositoryNativeSemanticRankRateExhaustiveness →" in text
    assert "RepositoryNativeSemanticRankRateExhaustivenessRealization" in text
    assert "FRONTIER_OPEN / WITNESS_REALIZATION_ONLY" in text

def test_repository_native_semantic_rank_rate_exhaustiveness_realization_doc_boundary():
    text = (ROOT / "docs/status/CHRONOS_REPOSITORY_NATIVE_SEMANTIC_RANK_RATE_EXHAUSTIVENESS_REALIZATION_2026_05_13.md").read_text()
    assert "No unrestricted UniversalFiberEntropyGap theorem." in text
    assert "No Chronos-RR." in text
    assert "No H4.1/FGL." in text
    assert "No P vs NP." in text
    assert "No Clay closure." in text
