from __future__ import annotations

"""Stage verifier for the unintegrated epsilon^2 action-density coefficient."""
import argparse
import hashlib
import json
import time
import sympy as s
from gfe_polar_angular_reduction import reduce_spherical_density
from gfe_polar_first_order_curvature_operator import build_first_order_operator
from gfe_polar_second_order_curvature_operator import build_second_order_operator, direct_second_order_operator_comparison
from gfe_polar_quadratic_density_coefficient import build_raw_quadratic_density, direct_raw_density_comparison


def emit(stage, passed, **fields):
    print(json.dumps({"schema":"gfe-polar-quadratic-density-stage-receipt-v1",
        "stage":stage,"passed":bool(passed),"frontier":"PASS" if passed else "FAIL",**fields},
        sort_keys=True, default=str), flush=True)


def progress(stage, **fields):
    emit(stage, True, **fields)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trust-prior-second-order-replay",
        action="store_true",
        help="Skip repeating the second-order replay already completed by the preceding workflow step.",
    )
    args = parser.parse_args()

    started = time.monotonic()
    progress("first_order_build_started")
    first = build_first_order_operator()
    progress("first_order_build_completed", elapsed_seconds=round(time.monotonic()-started, 3))

    second_started = time.monotonic()
    progress("second_order_build_started")
    op = build_second_order_operator(first)
    progress("second_order_build_completed", elapsed_seconds=round(time.monotonic()-second_started, 3))

    if args.trust_prior_second_order_replay:
        progress("second_order_operator_replay_reused",
                 evidence="preceding workflow step Run independent second-order curvature operator audit")
    else:
        replay_started = time.monotonic()
        progress("second_order_operator_replay_started", checked_count=36)
        op_residuals = direct_second_order_operator_comparison(op)
        op_nonzero = [(i,j,str(op_residuals[i,j])) for i in range(6) for j in range(6)
                      if s.simplify(op_residuals[i,j]) != 0]
        emit("second_order_operator_replay_gate", not op_nonzero,
             checked_count=36, nonzero_residuals=op_nonzero,
             elapsed_seconds=round(time.monotonic()-replay_started, 3))
        if op_nonzero:
            raise SystemExit(1)

    progress("raw_density_construction_started")
    data = build_raw_quadratic_density(first, op, progress=progress)
    raw = data["raw_epsilon_squared_density_coefficient"]
    progress("raw_density_construction_completed",
             coefficient_convention=data["coefficient_convention"])

    comparison_started = time.monotonic()
    progress("independent_density_comparison_started")
    check = direct_raw_density_comparison(data, progress=progress)
    progress("independent_density_comparison_completed",
             elapsed_seconds=round(time.monotonic()-comparison_started, 3))
    emit("determinant_density_expansion", check["determinant_density_residual"] == 0,
         formula="sqrt(-det(g0))*(1 + eps*tr(A)/2 + eps^2*((tr(A))^2/8-tr(A^2)/4))",
         coefficient="epsilon**2",
         residual=str(check["determinant_density_residual"]))
    emit("raw_quadratic_density_independent_comparison", check["passed"],
         method="six explicit matrix-product traces plus independent determinant-density residual",
         trace_identity_residual=check["trace_coefficient_residual"],
         determinant_residual=str(check["determinant_density_residual"]))
    if not check["passed"]:
        raise SystemExit(1)

    progress("raw_density_serialization_started")
    serialization_started = time.monotonic()
    canonical = s.srepr(raw)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    with open("gfe_polar_raw_epsilon_squared_density.srepr.txt","w",encoding="utf-8") as f:
        f.write(canonical+"\n")
    emit("raw_quadratic_density_preserved", True,
         sha256_srepr=digest, expression_characters=len(canonical),
         serialization_elapsed_seconds=round(time.monotonic()-serialization_started, 3),
         coordinates=["t","r","theta","phi"],
         angular_integration_performed=False,
         quadratic_action_derived=False,
         next_frontier="RAW_EPSILON_SQUARED_DENSITY_VERIFIED")
    print(json.dumps({"frontier":"RAW_EPSILON_SQUARED_DENSITY_VERIFIED",
        "passed":True,"quadratic_action_derived":False,
        "spherical_integral_completed":False,"sha256_srepr":digest},sort_keys=True), flush=True)

    # Continue from the in-memory SymPy expression. Do not parse the large srepr
    # artifact: it is preservation evidence only.
    theta = data["coordinates"][2]
    if raw.has(data["coordinates"][3]):
        emit("axisymmetry_gate", False, reason="raw density depends on phi")
        raise SystemExit(1)
    progress("exact_angular_reduction_started", input_sha256_srepr=digest)
    angular_started = time.monotonic()
    try:
        x_ang, angular_polynomial = reduce_spherical_density(raw, theta)
        degree = s.Poly(angular_polynomial, x_ang, domain="EX").degree()
        progress("exact_angular_polynomial_gate", degree=degree,
                 variable=str(x_ang), measure_removed="sin(theta)")
        integrated = s.simplify(2 * s.pi * s.integrate(angular_polynomial, (x_ang, -1, 1)))
        if integrated.has(s.Integral):
            raise ValueError("SymPy did not complete the exact polynomial integral")
    except Exception as exc:
        emit("exact_angular_reduction_gate", False,
             input_sha256_srepr=digest, error_type=type(exc).__name__,
             error=str(exc), elapsed_seconds=round(time.monotonic()-angular_started, 3),
             spherical_integral_completed=False, quadratic_action_derived=False)
        raise SystemExit(1)
    integrated_srepr = s.srepr(integrated)
    integrated_digest = hashlib.sha256(integrated_srepr.encode("utf-8")).hexdigest()
    with open("gfe_polar_integrated_epsilon_squared_density.srepr.txt","w",encoding="utf-8") as f:
        f.write(integrated_srepr+"\\n")
    emit("exact_angular_reduction_gate", True,
         input_sha256_srepr=digest, integrated_sha256_srepr=integrated_digest,
         angular_polynomial_degree=degree,
         elapsed_seconds=round(time.monotonic()-angular_started, 3),
         spherical_integral_completed=True,
         reference_81_slot_comparison_completed=False,
         quadratic_action_derived=False,
         next_frontier="COMPARE_INTEGRATED_EXPRESSION_TO_81_REFERENCE_SLOTS")


if __name__ == "__main__":
    main()
