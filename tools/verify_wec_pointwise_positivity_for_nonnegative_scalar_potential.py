#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LEAN = ROOT / "lean/Chronos/Frontier/WECPointwisePositivityForNonnegativeScalarPotential.lean"
ARTIFACT = ROOT / "artifacts/chronos/wec_pointwise_positivity_for_nonnegative_scalar_potential_2026_05_22.json"
DOC = ROOT / "docs/status/WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL_2026_05_22.md"

REQUIRED_THEOREMS = [
    "wec_pointwise_positivity_for_nonnegative_scalar_potential",
    "scalarFieldEnergyDensity_nonneg",
]

FORBIDDEN_TOKENS = [
    "sorry",
    "admit",
]

REQUIRED_BOUNDARIES = [
    "no PDE evolution theorem",
    "no continuation theorem",
    "no finite-time collapse theorem",
    "no trapped-surface existence theorem",
    "no unrestricted gravity closure",
    "no cosmic censorship proof",
    "no hoop conjecture proof",
    "no four-dimensional non-symmetric collapse theorem",
    "no Clay problem closure",
]

def main() -> None:
    lean_text = LEAN.read_text()
    artifact = json.loads(ARTIFACT.read_text())
    doc_text = DOC.read_text()

    assert artifact["id"] == "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL"
    assert artifact["status"] == "ADMISSIBLE_LEMMA_PROVED_ALGEBRAIC_ONLY"

    assert artifact["corrected_naming"]["rejected_name"] == (
        "WEC_POINTWISE_PRESERVATION_FOR_NONNEGATIVE_SCALAR_POTENTIAL"
    )
    assert artifact["corrected_naming"]["accepted_name"] == (
        "WEC_POINTWISE_POSITIVITY_FOR_NONNEGATIVE_SCALAR_POTENTIAL"
    )

    for theorem in REQUIRED_THEOREMS:
        assert theorem in lean_text
        assert theorem in artifact["proved_theorems"]
        assert theorem in doc_text

    lowered = lean_text.lower()
    for token in FORBIDDEN_TOKENS:
        assert token not in lowered

    boundary_text = "\n".join(artifact["boundary"])
    for token in REQUIRED_BOUNDARIES:
        assert token in boundary_text

    for blocker in [
        "NON_SYMMETRIC_EINSTEIN_SCALAR_CONTINUATION_CRITERION_OPEN",
        "RAYCHAUDHURI_FOCUSING_WITH_SHEAR_CONTROL_OPEN",
        "NON_SYMMETRIC_TRAPPED_SURFACE_TRIGGER_FROM_CONCENTRATION_OPEN",
    ]:
        assert blocker in artifact["open_blockers"]

    print("WEC pointwise positivity verification OK.")
    print("Status: ADMISSIBLE_LEMMA_PROVED_ALGEBRAIC_ONLY")
    print("Next admissible object: EXPLICIT_STRESS_ENERGY_EVOLUTION_IDENTITY tensor calculation, conditional only.")

if __name__ == "__main__":
    main()
