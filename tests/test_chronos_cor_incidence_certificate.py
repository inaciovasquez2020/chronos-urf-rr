import json
import subprocess
import sys
from pathlib import Path

CERT = Path("artifacts/cor/cor_incidence_basis_certificate_example.json")
SCRIPT = Path("scripts/verify_chronos_cor_incidence_certificate.py")
DOC = Path("docs/status/CHRONOS_COR_INCIDENCE_BASIS_CERTIFICATE_2026_05_02.md")


def test_chronos_cor_incidence_certificate_files_exist():
    assert CERT.exists()
    assert SCRIPT.exists()
    assert DOC.exists()


def test_chronos_cor_incidence_certificate_declared_identity():
    cert = json.loads(CERT.read_text())
    assert cert["field"] == "F2"
    assert cert["certified_obstruction_rank"] == (
        cert["cycle_space_dimension"] - cert["local_cycle_subspace_rank"]
    )


def test_chronos_cor_incidence_certificate_has_raw_graph_data():
    cert = json.loads(CERT.read_text())
    assert cert["vertex_count"] == 6
    assert len(cert["edges"]) == 7
    assert cert["cycle_basis"]
    assert cert["local_cycle_basis"]


def test_chronos_cor_incidence_certificate_boundary_language():
    text = DOC.read_text()
    assert "Status: FINITE INCIDENCE-BASIS CERTIFICATE / THEOREM ASSUMPTION SURFACE" in text
    assert "This verifies one finite incidence-basis certificate only." in text
    assert "It does not prove the finite-to-general lift." in text
    assert "It does not prove the locality-to-depth bridge." in text
    assert "It does not prove theorem-level Chronos closure." in text


def test_chronos_cor_incidence_certificate_verifier_passes():
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
