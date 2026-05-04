import json
import subprocess
from pathlib import Path

DOC = Path("docs/status/CHRONOS_CERTIFICATE_EMBEDDING_INTERFACE_2026_05_04.md")
CERT = Path("artifacts/chronos/chronos_certificate_embedding_interface_2026_05_04.json")


def test_chronos_certificate_embedding_interface_tokens_present():
    text = DOC.read_text(encoding="utf-8")
    assert "CERTIFIED_INTERFACE_ONLY" in text
    assert "CHRONOS_CERTIFICATE_EMBEDDING_NAMED" in text
    assert "E_N_INTERFACE_DEFINED" in text
    assert "CERTIFICATE_INSTANCE_SPACE_C_N_REQUIRED" in text
    assert "CERTIFICATE_DISTRIBUTION_NU_N_REQUIRED" in text
    assert "PUSHFORWARD_UNIFORMITY_REQUIRED" in text
    assert "ADMISSIBILITY_PRESERVATION_REQUIRED" in text
    assert "CERTIFICATE_CONSTANT_BINDING_REQUIRED" in text
    assert "NO_E_N_CONSTRUCTION_CLAIM" in text


def test_chronos_certificate_embedding_interface_certificate_values():
    data = json.loads(CERT.read_text(encoding="utf-8"))
    assert data["status"] == "CERTIFIED_INTERFACE_ONLY"
    assert data["theorem_closure"] is False
    assert data["chronos_closure"] is False
    assert data["h4_1_fgl_closure"] is False
    assert data["named_missing_object"] == "ChronosCertificateEmbedding"
    assert data["interface"]["embedding_symbol"] == "E_n"
    assert data["interface"]["domain"] == "repository_certificate_instances_C_n"
    assert data["interface"]["codomain"] == "{0,1}^n"


def test_chronos_certificate_embedding_interface_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_chronos_certificate_embedding_interface.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CERTIFIED_INTERFACE_ONLY" in result.stdout
