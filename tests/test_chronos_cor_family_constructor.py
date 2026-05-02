import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("scripts/verify_chronos_cor_family_constructor.py")
GENERATOR = Path("scripts/generate_chronos_cor_triangle_chain_family.py")
DOC = Path("docs/status/CHRONOS_COR_SYMBOLIC_FAMILY_CONSTRUCTOR_2026_05_02.md")
GENERATED_DIR = Path("artifacts/cor/triangle_chain_family")


def test_chronos_cor_family_constructor_files_exist():
    assert SCRIPT.exists()
    assert GENERATOR.exists()
    assert DOC.exists()


def test_chronos_cor_family_constructor_doc_boundary():
    text = DOC.read_text()
    assert "Status: SYMBOLIC FAMILY CONSTRUCTOR / FINITE CERTIFICATE GENERATOR" in text
    assert "It does not prove the finite-to-general lift." in text
    assert "It does not prove the locality-to-depth bridge." in text
    assert "It does not prove theorem-level Chronos closure." in text
    assert "It does not assert an infinite-family theorem inside Lean." in text


def test_chronos_cor_family_constructor_generated_formula():
    cert = json.loads((GENERATED_DIR / "cor_triangle_chain_blocks_3.json").read_text())
    assert cert["vertex_count"] == 9
    assert len(cert["edges"]) == 11
    assert cert["cycle_space_dimension"] == 3
    assert cert["local_cycle_subspace_rank"] == 0
    assert cert["certified_obstruction_rank"] == 3


def test_chronos_cor_family_constructor_verifier_passes():
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
