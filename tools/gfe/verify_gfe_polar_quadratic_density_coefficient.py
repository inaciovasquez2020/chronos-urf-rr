from __future__ import annotations

"""Stage verifier for the unintegrated epsilon^2 action-density coefficient."""
import argparse
import hashlib
import json
import time
import sympy as s
from gfe_polar_angular_reduction import reduce_spherical_density
from gfe_polar_action_reference_comparison import compare_integrated_action_to_report
from pathlib import Path
from gfe_polar_first_order_curvature_operator import build_first_order_operator
from gfe_polar_second_order_curvature_operator import build_second_order_operator, direct_second_order_operator_comparison
from gfe_polar_quadratic_density_coefficient import build_raw_quadratic_density, direct_raw_density_comparison

EXPECTED_RAW_SHA256 = "84a03f8caea6cce9f6730af986fcec49afca6b8288c88d9e22d72cd51639e005"


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
    emit("raw_density_integrity_gate", digest == EXPECTED_RAW_SHA256,
         expected_sha256_srepr=EXPECTED_RAW_SHA256,
         actual_sha256_srepr=digest, expression_characters=len(canonical))
    if digest != EXPECTED_RAW_SHA256:
        raise SystemExit("raw density SHA-256 mismatch; refusing angular reduction")
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
        x_ang, angular_polynomial = reduce_spherical_density(raw, theta, progress=progress)
        degree = s.Poly(angular_polynomial, x_ang, domain="EX").degree()
        progress("exact_angular_polynomial_gate", degree=degree,
                 variable=str(x_ang), measure_removed="sin(theta)")
        integrated = s.simplify(2 * s.pi * s.integrate(angular_polynomial, (x_ang, -1, 1)))
        if integrated.has(s.Integral):
            raise ValueError("SymPy did not complete the exact polynomial integral")
    except Exception as exc:
        failure_receipt = {
            "schema": "gfe-polar-angular-reduction-receipt-v1",
            "passed": False, "input_sha256_srepr": digest,
            "error_type": type(exc).__name__, "error": str(exc),
            "spherical_integral_completed": False, "quadratic_action_derived": False,
        }
        with open("gfe_polar_angular_reduction_receipt.json", "w", encoding="utf-8") as f:
            json.dump(failure_receipt, f, sort_keys=True, indent=2)
        emit("exact_angular_reduction_gate", False,
             input_sha256_srepr=digest, error_type=type(exc).__name__,
             error=str(exc), elapsed_seconds=round(time.monotonic()-angular_started, 3),
             spherical_integral_completed=False, quadratic_action_derived=False)
        raise SystemExit(1)
    integrated_srepr = s.srepr(integrated)
    integrated_digest = hashlib.sha256(integrated_srepr.encode("utf-8")).hexdigest()
    with open("gfe_polar_integrated_epsilon_squared_density.srepr.txt","w",encoding="utf-8") as f:
        f.write(integrated_srepr+"\n")
    angular_receipt = {
        "schema": "gfe-polar-angular-reduction-receipt-v1",
        "passed": True, "input_sha256_srepr": digest,
        "integrated_sha256_srepr": integrated_digest,
        "angular_polynomial_degree": degree,
        "spherical_integral_completed": True,
        "reference_81_slot_comparison_completed": False,
        "quadratic_action_derived": False,
    }
    with open("gfe_polar_angular_reduction_receipt.json", "w", encoding="utf-8") as f:
        json.dump(angular_receipt, f, sort_keys=True, indent=2)
    emit("exact_angular_reduction_gate", True,
         input_sha256_srepr=digest, integrated_sha256_srepr=integrated_digest,
         angular_polynomial_degree=degree,
         elapsed_seconds=round(time.monotonic()-angular_started, 3),
         spherical_integral_completed=True,
         reference_81_slot_comparison_completed=False,
         quadratic_action_derived=False,
         next_frontier="COMPARE_INTEGRATED_EXPRESSION_TO_81_REFERENCE_SLOTS")

    comparison_started = time.monotonic()
    progress("reference_81_slot_comparison_started",
             integrated_sha256_srepr=integrated_digest)
    report_path = Path(__file__).resolve().parents[2] / "docs/status/even_parity_cubic_quadratic_action_independent_derivation_2026-10-21.md"
    try:
        reference_check = compare_integrated_action_to_report(
            integrated, data["coordinates"], report_path
        )
    except Exception as exc:
        failure_receipt = {
            "schema": "gfe-polar-action-reference-comparison-receipt-v1",
            "passed": False, "input_sha256_srepr": digest,
            "integrated_sha256_srepr": integrated_digest,
            "error_type": type(exc).__name__, "error": str(exc),
            "reference_81_slot_comparison_completed": False,
            "quadratic_action_derived": False,
        }
        with open("gfe_polar_action_comparison_receipt.json", "w", encoding="utf-8") as f:
            json.dump(failure_receipt, f, sort_keys=True, indent=2)
        emit("reference_81_slot_comparison_gate", False,
             integrated_sha256_srepr=integrated_digest,
             error_type=type(exc).__name__, error=str(exc),
             elapsed_seconds=round(time.monotonic()-comparison_started, 3),
             reference_81_slot_comparison_completed=False,
             quadratic_action_derived=False)
        raise SystemExit(1)
    comparison_receipt = {
        "schema": "gfe-polar-action-reference-comparison-receipt-v1",
        **reference_check,
        "input_sha256_srepr": digest,
        "reference_81_slot_comparison_completed": reference_check["passed"],
        "quadratic_action_derived": reference_check["passed"],
    }
    with open("gfe_polar_action_comparison_receipt.json", "w", encoding="utf-8") as f:
        json.dump(comparison_receipt, f, sort_keys=True, indent=2)
    emit("reference_81_slot_comparison_gate", reference_check["passed"],
         input_sha256_srepr=digest,
         integrated_sha256_srepr=reference_check["integrated_sha256_srepr"],
         reference_sha256=reference_check["reference_sha256"],
         reference_slot_count=reference_check["reference_slot_count"],
         nonzero_residual_count=reference_check["nonzero_residual_count"],
         nonzero_residuals=reference_check["nonzero_residuals"],
         elapsed_seconds=round(time.monotonic()-comparison_started, 3),
         reference_81_slot_comparison_completed=reference_check["passed"],
         quadratic_action_derived=reference_check["passed"],
         next_frontier=("ANGULAR_INTEGRAL_MATCHED_81_REFERENCE_SLOTS"
                        if reference_check["passed"] else "REFERENCE_RESIDUALS_REQUIRE_REVIEW"))
    if not reference_check["passed"]:
        raise SystemExit(1)

    # Single bounded next gate: independently derive E_H0 from the integrated
    # metric-derived action; the published E_H0 is a comparison oracle only.
    try:
        h0_check = verify_e_h0_against_report(
            integrated, data["coordinates"], report_path
        )
    except Exception as exc:
        h0_check = {
            "passed": False, "error_type": type(exc).__name__, "error": str(exc),
            "scope": "independent H0 variational derivative",
        }
    comparison_receipt["e_h0_verification"] = h0_check
    with open("gfe_polar_action_comparison_receipt.json", "w", encoding="utf-8") as f:
        json.dump(comparison_receipt, f, sort_keys=True, indent=2)
    emit("independent_e_h0_euler_lagrange_comparison",
         h0_check["passed"], **{k: v for k, v in h0_check.items() if k != "passed"})
    if not h0_check["passed"]:
        raise SystemExit(1)




def verify_e_h0_against_report(integrated, coordinates, report_path):
    """Independently vary the integrated action and compare the printed E_H0.

    The source expression is the newly metric-derived angular integral, not the
    published 81-term table. The table is read only as a final comparison oracle.
    """
    import re
    from sympy.core.function import AppliedUndef

    t, r, _, _ = coordinates
    fields = [f for f in integrated.atoms(AppliedUndef)
              if f.func.__name__ == "H0" and f.args == (t, r)]
    if len(fields) != 1:
        raise ValueError("expected exactly one H0(t,r) field in integrated action")
    h0 = fields[0]

    # Full higher-derivative variational derivative:
    # E_H0(L) = sum_J (-D)_J (partial L / partial H0_J).
    jets = [h0] + sorted(
        (d for d in integrated.atoms(s.Derivative) if d.expr == h0),
        key=lambda d: (len(d.variables), str(d)),
    )
    e_h0 = s.Integer(0)
    for jet in jets:
        variation = s.diff(integrated, jet)
        if variation == 0:
            continue
        variables = () if jet == h0 else jet.variables
        e_h0 += (-1)**len(variables) * (s.diff(variation, *variables) if variables else variation)

    report_text = Path(report_path).read_text(encoding="utf-8")
    match = re.search(
        r"### " + re.escape(chr(96) + "E_H0 = 0" + chr(96))
        + r"\s*" + re.escape(chr(96) * 3 + "text")
        + r"\s*(.*?)\s*" + re.escape(chr(96) * 3),
        report_text, re.S,
    )
    if match is None:
        raise ValueError("published E_H0 equation block missing")
    reference_text = match.group(1).strip()

    all_jets = {}
    replacements = {}
    for derivative in sorted(e_h0.atoms(s.Derivative),
                             key=lambda d: len(d.variables), reverse=True):
        if not isinstance(derivative.expr, AppliedUndef):
            raise ValueError("unexpected non-field derivative in generated E_H0")
        name = derivative.expr.func.__name__
        if name not in ("H0", "H1", "H2", "K"):
            raise ValueError(f"unexpected field: {name}")
        counts = dict(derivative.variable_count)
        suffix = ["t"]*counts.pop(t, 0) + ["r"]*counts.pop(r, 0)
        if counts:
            raise ValueError(f"unsupported derivative coordinates: {counts}")
        symbol_name = name + "_" + "_".join(suffix)
        replacements[derivative] = all_jets.setdefault(symbol_name, s.Symbol(symbol_name))
    for function in e_h0.atoms(AppliedUndef):
        name = function.func.__name__
        if name not in ("H0", "H1", "H2", "K"):
            raise ValueError(f"unexpected field: {name}")
        replacements[function] = all_jets.setdefault(name, s.Symbol(name))

    for name in re.findall(r"\b(?:H0|H1|H2|K)(?:_(?:t|r))*\b", reference_text):
        all_jets.setdefault(name, s.Symbol(name))

    generated = s.expand(e_h0.xreplace(replacements))
    m_candidates = [z for z in generated.free_symbols if z.name == "M"]
    if len(m_candidates) != 1:
        raise ValueError("cannot identify mass parameter in generated E_H0")
    M = m_candidates[0]
    reference = s.sympify(reference_text, locals={"M": M, "r": r, **all_jets})
    variables = [all_jets[k] for k in sorted(all_jets)]
    delta = s.Poly(s.expand(generated - reference), *variables, domain="EX")
    residuals = []
    for powers, coefficient in delta.terms():
        reduced = s.factor(s.cancel(s.together(coefficient)))
        if reduced != 0:
            monomial = "*".join(
                f"{v}^{p}" for v, p in zip(variables, powers) if p
            ) or "1"
            residuals.append({"monomial": monomial, "residual": str(reduced)})
            break  # First structural mismatch is authoritative.

    return {
        "passed": not residuals,
        "scope": "independent H0 variational derivative of metric-derived integrated action",
        "first_nonzero_residual": residuals[0] if residuals else None,
        "generated_srepr_sha256": hashlib.sha256(
            s.srepr(generated).encode("utf-8")
        ).hexdigest(),
        "published_e_h0_sha256": hashlib.sha256(
            reference_text.encode("utf-8")
        ).hexdigest(),
    }


if __name__ == "__main__":
    main()
