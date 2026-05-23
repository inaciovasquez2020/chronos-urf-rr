#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
artifact = ROOT / "artifacts/chronos/local_balance_law_dqdt_derivation_2026_05_23.json"
doc = ROOT / "docs/status/LOCAL_BALANCE_LAW_DQDT_DERIVATION_2026_05_23.md"
lean = ROOT / "lean/Chronos/Frontier/LocalBalanceLawDQDTDerivation.lean"

data = json.loads(artifact.read_text())

assert data["name"] == "LOCAL_BALANCE_LAW_DQDT_DERIVATION"
assert data["status"] == "DERIVATION_SURFACE_ONLY_BALANCE_LAW_NOT_ANALYTICALLY_PROVED"
assert data["previous_object"] == "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK"
assert data["next_admissible_object"] == "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF"

for token in [
    "regionFamilyOmega",
    "metricDataGamma",
    "stressEnergyT",
    "normalFieldN",
    "extrinsicCurvatureK",
    "nonsymmetricDefect",
    "volumeFormGamma",
    "fluxIn",
    "fluxOut",
    "deformationError",
    "nonsymmetricError",
    "concentrationFunctionalQ",
]:
    assert token in data["objects"]

for token in [
    "regularityForDifferentiationUnderIntegral",
    "reynoldsTransportIdentity",
    "stressEnergyDivergenceFree",
    "boundaryFluxDecomposition",
    "deformationErrorIdentity",
    "nonsymmetricErrorIdentity",
    "qDerivativeBalanceFormula",
]:
    assert token in data["assumptions"]

for boundary in [
    "derivation surface only",
    "Reynolds transport identity assumed",
    "boundary flux decomposition assumed",
    "deformation error identity assumed",
    "nonsymmetric error identity assumed",
    "Q-derivative balance formula assumed",
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
    assert boundary in data["boundary"]

doc_text = doc.read_text()
for token in [
    "DERIVATION_SURFACE_ONLY_BALANCE_LAW_NOT_ANALYTICALLY_PROVED",
    "CONCRETE_ANALYTIC_EINSTEIN_MATTER_ESTIMATE_PACKAGE_PROOF_OBLIGATION_LOCK",
    "RESTRICTED_CONCENTRATION_MONOTONICITY_PROOF",
]:
    assert token in doc_text

lean_text = lean.read_text()
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
    assert token in lean_text

print("Local balance-law dQ/dt derivation verifier OK.")
print("Status:", data["status"])
print("Next admissible object:", data["next_admissible_object"])
