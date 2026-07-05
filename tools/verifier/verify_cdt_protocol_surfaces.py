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
    "structure CDTUncertaintyComputationReceipt",
"theorem cdt_uncertainty_computation_delta_nonnegative",
"structure CDTDecisionRuleSurface",
    "theorem cdt_detected_eta_nonzero",
    "structure CDTMeasurementRunReceipt",
"theorem cdt_measurement_run_detected_eta_nonzero",
"structure CDTDecisionReceipt",
"theorem cdt_decision_receipt_detected_eta_nonzero",
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


receipt_start = text.find("structure CDTMeasurementRunReceipt where")
receipt_end = text.find("theorem cdt_measurement_run_detected_eta_nonzero", receipt_start)

if receipt_start == -1 or receipt_end == -1:
    raise SystemExit("MISSING_OBJECT := CDTMeasurementRunReceipt block")

receipt_block = text[receipt_start:receipt_end]

for item in [
    "eta_observed : ℝ",
    "delta_eta_total : ℝ",
    "detected : Prop",
    "h_detected_iff : detected ↔ |eta_observed| > k * delta_eta_total",
]:
    if item not in receipt_block:
        raise SystemExit(f"MISSING_OBJECT := CDTMeasurementRunReceipt.{item}")


uncertainty_start = text.find("structure CDTUncertaintyComputationReceipt where")
uncertainty_end = text.find("theorem cdt_uncertainty_computation_delta_nonnegative", uncertainty_start)

if uncertainty_start == -1 or uncertainty_end == -1:
    raise SystemExit("MISSING_OBJECT := CDTUncertaintyComputationReceipt block")

uncertainty_block = text[uncertainty_start:uncertainty_end]

for item in [
    "timing_uncertainty : ℝ",
    "distance_uncertainty : ℝ",
    "sample_preparation_uncertainty : ℝ",
    "environmental_uncertainty : ℝ",
    "delta_eta_total : ℝ",
    "h_delta_eta_total_eq_sum",
]:
    if item not in uncertainty_block:
        raise SystemExit(f"MISSING_OBJECT := CDTUncertaintyComputationReceipt.{item}")


decision_start = text.find("structure CDTDecisionReceipt where")
decision_end = text.find("theorem cdt_decision_receipt_detected_eta_nonzero", decision_start)

if decision_start == -1 or decision_end == -1:
    raise SystemExit("MISSING_OBJECT := CDTDecisionReceipt block")

decision_block = text[decision_start:decision_end]

for item in [
    "measurement : CDTMeasurementRunReceipt",
    "uncertainty : CDTUncertaintyComputationReceipt",
    "h_delta_eta_total_bind",
    "decision_detected : Prop",
    "h_decision_detected_iff_measurement_detected",
]:
    if item not in decision_block:
        raise SystemExit(f"MISSING_OBJECT := CDTDecisionReceipt.{item}")

print("CDT_PROTOCOL_SURFACES_OK")
