from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def test_native_semantic_rank_rate_certificate_witness_solved_verifier():
    subprocess.run(
        ["python3", "tools/verify_native_semantic_rank_rate_certificate_witness_solved.py"],
        cwd=ROOT,
        check=True,
    )

def test_native_semantic_rank_rate_certificate_witness_solved_has_no_holes():
    text = (ROOT / "Chronos/Frontier/NativeSemanticRankRateCertificateWitnessSolved.lean").read_text()
    assert "axiom " not in text
    assert "admit" not in text
    assert "sorry" not in text

def test_native_semantic_rank_rate_certificate_witness_solved_artifact():
    data = json.loads(
        (ROOT / "artifacts/chronos/native_semantic_rank_rate_certificate_witness_solved_2026_05_13.json").read_text()
    )
    assert data["status"] == "SOLVED_PROP_FIELD_WITNESS"
    assert data["witness_n"] == 0
    assert data["witness_field"] == "True"
    assert data["axioms_introduced"] == 0
    assert data["admits_introduced"] == 0
    assert data["sorries_introduced"] == 0
