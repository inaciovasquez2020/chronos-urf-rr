#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/tsimf_pdf_source_classification_2026_05_23.json"
STATUS = ROOT / "docs/status/TSIMF_PDF_SOURCE_CLASSIFICATION_2026_05_23.md"
LEAN = ROOT / "lean/Chronos/Frontier/TSIMFPDFSourceClassification.lean"

REQUIRED_BLOCKS = [
    "proof of SixFieldAnalyticPackageHypothesis",
    "proof of NonSymmetricEinsteinMatterBootstrapKernelAnalyticPackage",
    "proof of Einstein-matter well-posedness",
    "proof of non-symmetric persistence",
    "proof of concentration transport",
    "proof of collapse-gate trigger",
    "proof of cosmic censorship",
    "proof of hoop conjecture",
    "proof of gravity closure",
    "proof of Chronos-RR",
    "proof of H4.1/FGL",
    "proof of P vs NP",
    "proof of any Clay problem",
]

def main() -> None:
    data = json.loads(ARTIFACT.read_text())
    status = STATUS.read_text()
    lean = LEAN.read_text()

    assert data["artifact"] == "TSIMF_PDF_SOURCE_CLASSIFICATION"
    assert data["status"] == "SOURCE_HYGIENE_GAP_CLOSED_NO_ANALYTIC_PACKAGE_PROOF"
    assert data["source"]["type"] == "conference_program_and_schedule_source"
    assert data["next_admissible_object"] == "ConcreteInitialDataClassSpecification"

    for phrase in REQUIRED_BLOCKS:
        assert phrase in data["blocked_use"], phrase
        assert phrase in status, phrase

    assert "provesSixFieldAnalyticPackageHypothesis := False" in lean
    assert "tsimf_pdf_does_not_prove_six_field" in lean

    print("TSIMF PDF source classification verification OK.")
    print("Status:", data["status"])
    print("Next admissible object:", data["next_admissible_object"])

if __name__ == "__main__":
    main()
