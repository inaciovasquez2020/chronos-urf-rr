from pathlib import Path

p = Path("lean/Chronos/Frontier/CarbonStructuralGravityInputSurface.lean")
text = p.read_text()

required = [
    "structure AMSIsotopeCharacterizationSurface",
    "structure CarbonAllotropeIdentitySurface",
    "structure EotvosWEPBoundInputSurface",
    "structure CarbonStructuralResidualInputSurface",
    "structure PositiveAccelerationInterval",
    "noncomputable def etaMin",
    "noncomputable def etaMax",
    "structure CDTSampleSpecificationSurface",
    "structure CDTMeasurementProtocolSurface",
    "structure CDTUncertaintyBudgetSurface",
    "structure CDTDecisionRuleSurface",
    "theorem cdt_detected_eta_nonzero",
    "structure CDTNullControlPairSurface",
    "structure CDTReplicationCriterionInputSurface",
    "def CDTCarbonStructuralGravityCausalClaim : Prop := False",
    "theorem cdt_rejects_causal_overclaim",
    "structure StructuralObservableInputSurface",
    "structure StructuralCouplingPredictionSurface",
    "noncomputable def predictedAcceleration",
    "noncomputable def predictedEtaCDT",
    "theorem predicted_acceleration_lambda_zero",
    "theorem predicted_eta_lambda_zero",
]

for item in required:
    if item not in text:
        raise SystemExit(f"MISSING_OBJECT := {item}")

for forbidden in ["axiom", "opaque", "sorry", "admit"]:
    if forbidden in text:
        raise SystemExit(f"FORBIDDEN_LEAN_TOKEN := {forbidden}")

forbidden_claims = [
    "CDTCarbonStructuralGravityCausalClaim : Prop := True",
    "cdt_proves_carbon_structural_gravity",
    "cdt_proves_wep_violation",
    "cdt_proves_new_gravity",
    "CDT_proves_carbon_structural_gravity",
    "cdt_proves_structural_coupling",
    "structural_coupling_empirically_established",
    "lambda_nonzero_theorem",
]

for item in forbidden_claims:
    if item in text:
        raise SystemExit(f"FORBIDDEN_OVERCLAIM := {item}")

chronos = Path("lean/Chronos.lean").read_text()
if "import Chronos.Frontier.CarbonStructuralGravityInputSurface" not in chronos:
    raise SystemExit("MISSING_OBJECT := Chronos import for CarbonStructuralGravityInputSurface")

print("CDT_PROTOCOL_SURFACES_OK")
