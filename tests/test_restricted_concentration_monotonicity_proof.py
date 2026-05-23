import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_restricted_concentration_monotonicity_status_and_next_object():
    data = json.loads((ROOT / "artifacts/chronos/restricted_concentration_monotonicity_proof_2026_05_23.json").read_text())
    assert data["status"] == "PROOF_SURFACE_ONLY_RESTRICTED_CONCENTRATION_MONOTONICITY_NOT_UNCONDITIONAL"
    assert data["previous_object"] == "LOCAL_BALANCE_LAW_DQDT_DERIVATION"
    assert data["next_admissible_object"] == "RESTRICTED_CONTINUATION_NORM_CONTROL_PROOF"

def test_restricted_concentration_monotonicity_assumptions_are_explicit():
    data = json.loads((ROOT / "artifacts/chronos/restricted_concentration_monotonicity_proof_2026_05_23.json").read_text())
    expected = [
        "localBalanceLawDQDTDerived",
        "stressEnergyConserved",
        "weakEnergyCondition",
        "dominantEnergyCondition",
        "bootstrapInequalitiesB",
        "fluxDominance",
        "deformationErrorControlled",
        "nonsymmetricErrorControlled",
        "etaRange",
        "fluxDominanceAbsorbsErrors",
        "qDerivativeNonnegative",
        "nonnegativeDerivativeImpliesConcentrationMonotone",
    ]
    assert data["assumptions"] == expected

def test_restricted_concentration_monotonicity_boundaries_are_preserved():
    data = json.loads((ROOT / "artifacts/chronos/restricted_concentration_monotonicity_proof_2026_05_23.json").read_text())
    for token in [
        "no unconditional restricted concentration monotonicity theorem",
        "no restricted continuation norm control proof",
        "no package compatibility proof",
        "no target-interface compatibility proof",
        "no concrete analytic Einstein-matter estimate package proof",
        "no gravity closure",
        "no Chronos-RR",
        "no H4.1/FGL",
        "no P vs NP",
        "no Clay problem",
    ]:
        assert token in data["boundary"]

def test_restricted_concentration_monotonicity_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/RestrictedConcentrationMonotonicityProof.lean").read_text()
    for token in [
        "RestrictedConcentrationMonotonicityProofData",
        "RestrictedConcentrationMonotonicityProofHypotheses",
        "LocalBalanceLawDQDTDerivationData",
        "RestrictedLocalConcentrationData",
        "RestrictedLocalFluxTerms",
        "fluxDominanceAbsorbsErrors",
        "qDerivativeNonnegative",
        "nonnegativeDerivativeImpliesConcentrationMonotone",
        "RestrictedConcentrationMonotonicityProof",
    ]:
        assert token in text
