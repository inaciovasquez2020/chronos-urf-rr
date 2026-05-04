import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "artifacts/chronos/certificates/chronos_certificate_primitive_axiom_2026_05_04.json"
DOC = ROOT / "docs/status/CHRONOS_CERTIFICATE_PRIMITIVE_AXIOM_2026_05_04.md"

def test_chronos_certificate_primitive_axiom_tokens():
    text = DOC.read_text(encoding="utf-8")
    for token in [
        "CHRONOS_CERTIFICATE_PRIMITIVE_AXIOM",
        "AXIOMATIC_DECLARATION_ONLY",
        "CCPA_TERMINAL_PRIMITIVE",
        "T_CHR_TYPE_FAMILY_REQUIRED",
        "FINTYPE_REQUIRED",
        "NONEMPTY_REQUIRED",
        "DECIDABLE_EQ_REQUIRED",
        "TARGET_SIDE_INDEPENDENT",
        "THEOREM_CLOSURE_FALSE",
        "CHRONOS_CLOSURE_FALSE",
        "H4_1_FGL_CLOSURE_FALSE",
        "P_VS_NP_CLAIM_FALSE",
        "NO_CERTIFICATE_EMBEDDING_CLAIM",
    ]:
        assert token in text

def test_chronos_certificate_primitive_axiom_certificate_values():
    data = json.loads(CERT.read_text(encoding="utf-8"))
    assert data["status"] == "AXIOMATIC_DECLARATION_ONLY"
    assert data["theorem_closure"] is False
    assert data["chronos_closure"] is False
    assert data["h4_1_fgl_closure"] is False
    assert data["p_vs_np_closure"] is False
    assert data["terminal_missing_primitive"] == "CCPA"
    assert data["primitive_type_family"] == "T_Chr : Nat -> Type"
    assert "Fintype(T_Chr n)" in data["required_instances"]
    assert "Nonempty(T_Chr n)" in data["required_instances"]
    assert "DecidableEq(T_Chr n)" in data["required_instances"]

def test_chronos_certificate_primitive_axiom_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_certificate_primitive_axiom.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "AXIOMATIC_DECLARATION_ONLY" in result.stdout
