import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_local_balance_law_status_and_next_object():
    data = json.loads((ROOT / "artifacts/chronos/local_balance_law_dqdt_derivation_2026_05_23.json").read_text())
    assert data["status"] == "DERIVATION_SURFACE_ONLY_BALANCE_LAW_NOT_ANALYTICALLY_PROVED"
    assert data["previous_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK"
    assert data["next_admissible_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"

def test_local_balance_law_assumptions_are_explicit():
    data = json.loads((ROOT / "artifacts/chronos/local_balance_law_dqdt_derivation_2026_05_23.json").read_text())
    expected = [
        "regularityForDifferentiationUnderIntegral",
        "reynoldsTransportIdentity",
        "stressEnergyDivergenceFree",
        "boundaryFluxDecomposition",
        "deformationErrorIdentity",
        "nonsymmetricErrorIdentity",
        "qDerivativeBalanceFormula",
    ]
    assert data["assumptions"] == expected

def test_local_balance_law_boundaries_are_preserved():
    data = json.loads((ROOT / "artifacts/chronos/local_balance_law_dqdt_derivation_2026_05_23.json").read_text())
    for token in [
        "no analytic derivation of the local balance law",
        "no restricted concentration monotonicity proof",
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

def test_local_balance_law_lean_surface_terms():
    text = (ROOT / "lean/Chronos/Frontier/LocalBalanceLawDQDTDerivation.lean").read_text()
    for token in [
        "LocalBalanceLawDQDTDerivationData",
        "LocalBalanceLawDQDTDerivationHypotheses",
        "regularityForDifferentiationUnderIntegral",
        "reynoldsTransportIdentity",
        "stressEnergyDivergenceFree",
        "boundaryFluxDecomposition",
        "deformationErrorIdentity",
        "nonsymmetricErrorIdentity",
        "qDerivativeBalanceFormula",
        "LocalBalanceLawDQDTDerivation",
    ]:
        assert token in text
