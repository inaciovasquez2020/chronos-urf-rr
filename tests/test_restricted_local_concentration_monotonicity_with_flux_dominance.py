import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_local_concentration_artifact_status_and_target():
    data = json.loads((ROOT / "artifacts/chronos/restricted_local_concentration_monotonicity_with_flux_dominance_2026_05_23.json").read_text())
    assert data["status"] == "ESTIMATE_CANDIDATE_ONLY_NO_GRAVITY_CLOSURE"
    assert data["supplies_next_analytic_ingredient_for"] == "RESTRICTED_CONCENTRATION_MONOTONICITY"
    assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL"

def test_restricted_local_concentration_boundaries_are_preserved():
    data = json.loads((ROOT / "artifacts/chronos/restricted_local_concentration_monotonicity_with_flux_dominance_2026_05_23.json").read_text())
    forbidden_promotions = [
        "no gravity closure",
        "no Chronos-RR",
        "no H4.1/FGL",
        "no P vs NP",
        "no Clay problem",
    ]
    for token in forbidden_promotions:
        assert token in data["boundary"]

def test_restricted_local_concentration_lean_surface_names_terms():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedLocalConcentrationMonotonicityWithFluxDominance.lean").read_text()
    for token in [
        "RestrictedLocalFluxTerms",
        "flux_in",
        "flux_out",
        "deformation_error",
        "nonsymmetric_error",
        "localBalanceLaw",
        "RestrictedLocalConcentrationMonotonicityWithFluxDominance",
    ]:
        assert token in text
