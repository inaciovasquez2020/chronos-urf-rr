import json
import subprocess
import sys
from pathlib import Path

CERT = Path("artifacts/cor/cor_certificate_example.json")
SCRIPT = Path("scripts/verify_chronos_cor_certificate.py")
DOC = Path("docs/status/CHRONOS_COR_FINITE_CERTIFICATE_PARSER_2026_05_02.md")


def test_chronos_cor_certificate_exists():
    assert CERT.exists()
    assert SCRIPT.exists()
    assert DOC.exists()


def test_chronos_cor_certificate_arithmetic_identity():
    cert = json.loads(CERT.read_text())
    assert cert["field"] == "F2"
    assert cert["certified_obstruction_rank"] == (
        cert["cycle_space_dimension"] - cert["local_cycle_subspace_rank"]
    )


def test_chronos_cor_certificate_growth_inequality():
    cert = json.loads(CERT.read_text())
    growth = cert["linear_growth_claim"]
    assert cert["certified_obstruction_rank"] * growth["alpha_den"] >= (
        growth["alpha_num"] * cert["vertex_count"]
    )


def test_chronos_cor_certificate_boundary():
    text = DOC.read_text()
    assert "Status: FINITE CERTIFICATE PARSER / THEOREM ASSUMPTION SURFACE" in text
    assert "This parser checks finite certificate arithmetic only." in text
    assert "It does not recompute \\(Z_1(G)\\) from raw graph incidence data." in text
    assert "It does not prove the finite-to-general lift." in text
    assert "It does not prove the locality-to-depth bridge." in text
    assert "It does not prove theorem-level Chronos closure." in text


def test_chronos_cor_certificate_verifier_passes():
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
