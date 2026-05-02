from pathlib import Path
import subprocess
import sys

DOC = Path("docs/status/CHRONOS_FINITE_TO_GENERAL_LIFT_FRONTIER_2026_05_02.md")
SCRIPT = Path("scripts/verify_chronos_finite_to_general_lift_frontier.py")


def test_chronos_finite_to_general_lift_frontier_files_exist():
    assert DOC.exists()
    assert SCRIPT.exists()


def test_chronos_finite_to_general_lift_frontier_status():
    text = DOC.read_text()
    assert "Status: THEOREM FRONTIER / NEXT MISSING LEMMA" in text
    assert "Next Missing Lemma" in text
    assert "finite-to-general lift" in text


def test_chronos_finite_to_general_lift_frontier_boundary():
    text = DOC.read_text()
    assert "This document isolates the next missing theorem-level bridge only." in text
    assert "It does not prove the finite-to-general lift." in text
    assert "It does not prove the locality-to-depth bridge." in text
    assert "It does not prove theorem-level Chronos closure." in text
    assert "It does not assert that finite evidence alone implies an infinite-family theorem." in text
    assert "It does not assert that the finite-to-general lift is the only remaining global Chronos theorem obligation." in text


def test_chronos_finite_to_general_lift_frontier_formula():
    text = DOC.read_text()
    assert "\\operatorname{COR}_R(G_i)\\ge \\alpha |V(G_i)|" in text
    assert "\\operatorname{COR}_R(G_n)\\ge \\alpha' |V(G_n)|" in text
    assert "n\\mapsto (G_n,C(n))" in text


def test_chronos_finite_to_general_lift_frontier_verifier_passes():
    subprocess.run([sys.executable, str(SCRIPT)], check=True)
