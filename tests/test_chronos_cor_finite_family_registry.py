import json
import subprocess
import sys
from pathlib import Path

REGISTRY = Path("artifacts/cor/cor_finite_family_registry.json")
CERT = Path("artifacts/cor/cor_incidence_basis_certificate_two_triangles_bridge.json")
SCRIPT = Path("scripts/verify_chronos_cor_finite_family_registry.py")
DOC = Path("docs/status/CHRONOS_COR_FINITE_FAMILY_REGISTRY_2026_05_02.md")


def test_chronos_cor_finite_family_registry_files_exist():
    assert REGISTRY.exists()
    assert CERT.exists()
    assert SCRIPT.exists()
    assert DOC.exists()


def test_chronos_cor_finite_family_registry_shared_alpha():
    registry = json.loads(REGISTRY.read_text())
    cert = json.loads(CERT.read_text())
    assert cert["radius"] == registry["shared_radius"]
    assert cert["certified_obstruction_rank"] * registry["alpha_den"] >= (
        registry["alpha_num"] * cert["vertex_count"]
    )


def test_chronos_cor_finite_family_registry_boundary_language():
    text = DOC.read_text()
    assert "Status: FINITE FAMILY REGISTRY / THEOREM ASSUMPTION SURFACE" in text
    assert "This registry verifies a finite family of incidence-basis certificates only." in text
    assert "It does not prove an infinite graph-family theorem." in text
    assert "It does not prove the finite-to-general lift." in text
    assert "It does not prove the locality-to-depth bridge." in text
    assert "It does not prove theorem-level Chronos closure." in text


def test_chronos_cor_finite_family_registry_verifier_passes():
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
