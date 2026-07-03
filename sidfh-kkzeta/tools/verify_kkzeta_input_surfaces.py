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
]:
    if required not in text:
        print(f"KKZETA_INPUT_SURFACE_REJECTED missing token: {required}")
        sys.exit(1)

print("KKZETA_INPUT_SURFACE_OK")
