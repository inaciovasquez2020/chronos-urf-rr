import json
import subprocess
from pathlib import Path

DOC = Path("docs/status/EXPLICIT_IC_BRIDGE_CONTRACT_2026_05_04.md")
CERT = Path("artifacts/chronos/explicit_ic_bridge_contract_2026_05_04.json")


def test_explicit_ic_bridge_tokens_present():
    text = DOC.read_text(encoding="utf-8")
    assert "CONDITIONAL_BRIDGE_CONTRACT" in text
    assert "F_N_EXPLICIT" in text
    assert "MU_N_EXPLICIT" in text
    assert "SEARCH_F_N_EXPLICIT" in text
    assert "IC_LOWER_BOUND_EXPLICIT" in text
    assert "MISSING_OBJECT_CHRONOS_CERTIFICATE_EMBEDDING" in text


def test_explicit_ic_bridge_certificate_values():
    data = json.loads(CERT.read_text(encoding="utf-8"))
    assert data["status"] == "CONDITIONAL_BRIDGE_CONTRACT"
    assert data["theorem_closure"] is False
    assert data["chronos_closure"] is False
    assert data["h4_1_fgl_closure"] is False
    assert data["objects"]["F_n"] == "{0,1}^n"
    assert data["objects"]["mu_n"] == "uniform_distribution_on_{0,1}^n"
    assert data["objects"]["Search_F_n"] == "identity_search_functional_Search_F_n(x)=x"
    assert data["ic_lower_bound"]["constant_c"] == 1
    assert data["repository_binding"]["bound_to_certificate_constants"] is False
    assert data["repository_binding"]["missing_binding_object"] == "ChronosCertificateEmbedding"


def test_explicit_ic_bridge_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_explicit_ic_bridge_contract.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CONDITIONAL_BRIDGE_CONTRACT" in result.stdout
