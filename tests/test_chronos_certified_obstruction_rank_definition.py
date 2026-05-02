from pathlib import Path
import subprocess
import sys

DOC = Path("docs/status/CHRONOS_CERTIFIED_OBSTRUCTION_RANK_DEFINITION_2026_05_02.md")

def test_chronos_certified_obstruction_rank_definition_doc_exists():
    assert DOC.exists()

def test_chronos_certified_obstruction_rank_definition_boundary():
    text = DOC.read_text()
    assert "Status: DEFINITION LOCK / THEOREM FRONTIER INPUT" in text
    assert "This document fixes a definition only." in text
    assert "It does not prove the Chronos theorem-level closure." in text
    assert "It does not prove the finite-to-general lift." in text
    assert "It does not prove the locality-to-depth bridge." in text

def test_chronos_certified_obstruction_rank_definition_formula():
    text = DOC.read_text()
    assert "\\operatorname{COR}_R(G)" in text
    assert "\\dim_{\\mathbb F_2}\\bigl(Z_1(G)/L_R(G)\\bigr)" in text
    assert "\\operatorname{COR}_R(G_n)\\ge \\alpha |V(G_n)|" in text

def test_chronos_certified_obstruction_rank_definition_verifier_passes():
    subprocess.run(
        [sys.executable, "scripts/verify_chronos_certified_obstruction_rank_definition.py"],
        check=True,
    )
