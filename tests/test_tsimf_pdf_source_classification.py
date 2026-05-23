import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_tsimf_pdf_source_classification_boundary():
    data = json.loads((ROOT / "artifacts/chronos/tsimf_pdf_source_classification_2026_05_23.json").read_text())
    assert data["status"] == "SOURCE_HYGIENE_GAP_CLOSED_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["source"]["type"] == "conference_program_and_schedule_source"
    assert "proof of SixFieldAnalyticPackageHypothesis" in data["blocked_use"]
    assert "proof of any Clay problem" in data["blocked_use"]
    assert data["next_admissible_object"] == "ConcreteInitialDataClassSpecification"
