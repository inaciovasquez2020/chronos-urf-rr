import json
import subprocess
from pathlib import Path

def test_verifier_passes():
    out = subprocess.check_output([
        "python3",
        "tools/verify_finite_detector_coherence_forces_atomic_mass_representation.py",
    ], text=True)
    assert "FINITE_DETECTOR_COHERENCE_FORCES_ATOMIC_MASS_REPRESENTATION_OK" in out

def test_artifact_records_research_novelty_and_obstruction():
    data = json.loads(Path(
        "artifacts/chronos/finite_detector_coherence_forces_atomic_mass_representation_2026_05_28.json"
    ).read_text())
    assert data["status"] == "FINITE_COHERENCE_THEOREM_SOLVED"
    assert "forced" in data["research_novelty"]
    assert "regrouping" in data["harder_obstruction_removed"]

def test_doc_contains_paper_style_sections():
    text = Path(
        "docs/status/FINITE_DETECTOR_COHERENCE_FORCES_ATOMIC_MASS_REPRESENTATION_2026_05_28.md"
    ).read_text()
    for header in [
        "## Theorem",
        "## Proof",
        "## Comparison to Existing Formalization",
        "## Research Novelty",
        "## Harder Obstruction Removed",
        "## Boundary",
    ]:
        assert header in text
