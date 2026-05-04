import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts/chronos/certificates/chronos_cpol_type_gate_2026_05_04.json"
DOC = ROOT / "docs/status/CHRONOS_CPOL_TYPE_GATE_2026_05_04.md"

def test_chronos_cpol_type_gate_certificate_values():
    data = json.loads(CERT.read_text(encoding="utf-8"))
    assert data["status"] == "CPOL_TYPE_GATE_CLOSED_ONLY"
    assert data["theorem_closure"] is False
    assert data["chronos_closure"] is False
    assert data["h4_1_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False
    assert data["type_family"] == "TChr : Nat -> Type"
    assert data["definition"] == "inductive TChr (n : Nat) : Type | base : TChr n"
    assert "Nonempty(TChr n)" in data["proved_instances"]
    assert "DecidableEq(TChr n)" in data["proved_instances"]
    assert "canonical witness tChrCanonicalWitness n : TChr n" in data["proved_instances"]

def test_chronos_cpol_type_gate_status_tokens():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "CHRONOS_CPOL_TYPE_GATE",
        "CPOL_TYPE_GATE_CLOSED_ONLY",
        "T_CHR_DEFINED",
        "T_CHR_SINGLETON_CARRIER",
        "NONEMPTY_PROVED",
        "DECIDABLE_EQ_PROVED",
        "CANONICAL_WITNESS_PROVED",
        "DECIDABLE_EQ_NONEMPTY_PROVED",
        "THEOREM_CLOSURE_FALSE",
        "CHRONOS_CLOSURE_FALSE",
        "H4_1_FGL_CLOSURE_FALSE",
        "P_VS_NP_CLAIM_FALSE",
        "NO_C_N_CHR_CONSTRUCTION",
        "NO_CPDL_CLAIM",
        "NO_CCSL_CLAIM",
        "NO_CERTIFICATE_EMBEDDING_CLAIM",
    ]:
        assert token in text

def test_chronos_cpol_type_gate_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_cpol_type_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CPOL_TYPE_GATE_CLOSED_ONLY" in result.stdout
