#!/usr/bin/env python3
from pathlib import Path
import sys

p = Path("Sidfh/KkZeta/Basic.lean")
text = p.read_text()

for forbidden in [
    ": True",
    "theorem zeta_analytic_continuation",
    "theorem heat_kernel_seely_dewitt",
    "theorem zeta_det_closed_form",
    "heatKernel (A : AOp)",
    "zeta (A : AOp)",
    ":= 0",
]:
    if forbidden in text:
        print(f"KKZETA_INPUT_SURFACE_REJECTED forbidden token: {forbidden}")
        sys.exit(1)

for required in [
    "structure HilbertSpaceOperator where",
    "selfAdjoint : Prop",
    "structure TraceClassHeatKernelInputSurface where",
    "traceClassForPositiveTime : Prop",
    "structure SpectralMeasureZetaInputSurface where",
    "spectralMeasureExists : Prop",
    "def zeta_det_closed_form_proof_target : Prop :=",
    "Nonempty ZetaDetClosedFormInputSurface",
    "structure KKZetaOperatorSurface where",
    "H : Type",
    "DenseDomain : H → Prop",
    "operator : H → H",
    "symmetric : Prop",
    "nonnegative : Prop",
    "def KKZetaOperatorSurface_proof_target : Prop :=",
    "Nonempty KKZetaOperatorSurface",
    "def concreteKKZetaOperatorSurface : KKZetaOperatorSurface where",
    "theorem concreteKKZetaOperatorSurface_symmetric",
    "theorem concreteKKZetaOperatorSurface_nonnegative",
    "structure InversePowerBoundedInputSurface where",
    "structure TraceClassInversePowerInputSurface where",
    "structure ImportedAnalyticContinuationInput where",
    "structure ConditionalZetaDeterminantInputSurface where",
    "def A_inverse_power_bounded_proof_target : Prop :=",
    "def trace_class_for_Re_gt_1_proof_target : Prop :=",
    "def imported_analytic_input_proof_target : Prop :=",
    "def conditional_zeta_determinant_proof_target : Prop :=",
    "def BOUNDARY_meromorphic_continuation : Prop :=",
    "def BOUNDARY_conditional_determinant_properties : Prop :=",
]:
    if required not in text:
        print(f"KKZETA_INPUT_SURFACE_REJECTED missing token: {required}")
        sys.exit(1)

print("KKZETA_INPUT_SURFACE_OK")
