from __future__ import annotations

"""Metric-derived epsilon^2 coefficient of sqrt(-det(g))*Tr(Rop**3).

This stage consumes the verified Rop coefficients only. The determinant-density
coefficients are derived independently from A=g0^{-1}h. All returned quantities
are raw, unintegrated functions of (t,r,theta); no angular integration or action
reduction is performed here.
"""
from itertools import product
import sympy as s
from gfe_polar_first_order_curvature_operator import build_first_order_operator
from gfe_polar_second_order_curvature_operator import build_second_order_operator, direct_second_order_operator_comparison


def _trace_product3(A, B, C):
    """Compute Tr(A*B*C) by scalar index contraction, without matrix intermediates."""
    n = A.rows
    return sum(
        (A[i, j] * B[j, k] * C[k, i]
         for i, j, k in product(range(n), repeat=3)),
        s.Integer(0),
    )


def _trace_cube_coefficients(R0, R1, R2, report=None):
    def mark(stage):
        if report is not None:
            report(stage)

    mark("trace_T0_started")
    T0 = sum((R0[i, i]**3 for i in range(R0.rows)), s.Integer(0)) \
        if all(s.simplify(R0[i, j]) == 0 for i in range(R0.rows)
               for j in range(R0.cols) if i != j) else s.trace(R0**3)
    mark("trace_T0_completed")
    mark("trace_T1_started")
    T1 = 3 * sum((R0[i, i]**2 * R1[i, i] for i in range(R0.rows)), s.Integer(0)) \
        if all(s.simplify(R0[i, j]) == 0 for i in range(R0.rows)
               for j in range(R0.cols) if i != j) else 3 * _trace_product3(R0, R0, R1)
    mark("trace_T1_completed")
    mark("trace_R0R0R2_started")
    T20 = sum((R0[i, i]**2 * R2[i, i] for i in range(R0.rows)), s.Integer(0)) \
        if all(s.simplify(R0[i, j]) == 0 for i in range(R0.rows)
               for j in range(R0.cols) if i != j) else _trace_product3(R0, R0, R2)
    mark("trace_R0R0R2_completed")
    mark("trace_R0R1R1_started")
    if all(s.simplify(R0[i, j]) == 0 for i in range(R0.rows)
           for j in range(R0.cols) if i != j):
        T21 = sum(
            (R0[i, i] * R1[i, j] * R1[j, i]
             for i, j in product(range(R0.rows), repeat=2)),
            s.Integer(0),
        )
    else:
        T21 = _trace_product3(R0, R1, R1)
    mark("trace_R0R1R1_completed")
    T2 = 3*T20 + 3*T21
    return T0, T1, T2


def build_raw_quadratic_density(first_data=None, second_data=None, progress=None):
    """Build raw coefficient; progress(stage, **fields) reports completed boundaries."""
    def report(stage, **fields):
        if progress is not None:
            progress(stage, **fields)

    first = first_data if first_data is not None else build_first_order_operator()
    second = second_data if second_data is not None else build_second_order_operator(first)
    g0, h = first["background_metric"], first["perturbation"]

    A = g0.inv()*h
    trA = s.trace(A)
    trA2 = s.trace(A*A)
    d1 = s.expand(trA/2)
    d2 = s.expand(trA**2/8 - trA2/4)
    report("determinant_density_coefficients_built",
           determinant_coefficient_count=3)

    R0 = first["operator_background"]
    R1 = first["operator_first_order"]
    R2 = second["operator_second_order"]
    T0, T1, T2 = _trace_cube_coefficients(R0, R1, R2, report=report)
    report("trace_cube_coefficients_built",
           coefficient_count=3, trace_dimension=6)

    density0 = s.sqrt(-g0.det())
    report("background_density_factor_built")
    raw = density0*(T2 + d1*T1 + d2*T0)
    report("raw_density_expression_assembled")
    return {
        "coordinates": first["coordinates"],
        "epsilon": first["epsilon"],
        "background_metric": g0,
        "perturbation": h,
        "operator_background": R0,
        "operator_first_order": R1,
        "operator_second_order": R2,
        "trace_cube_coefficients": (T0, T1, T2),
        "density_coefficients_relative_to_background": (s.Integer(1), d1, d2),
        "sqrt_minus_det_background": density0,
        "raw_epsilon_squared_density_coefficient": raw,
        "coefficient_convention": "coefficient_of_epsilon_squared",
        "angular_integration_performed": False,
        "quadratic_action_derived": False,
    }


def direct_raw_density_comparison(data, progress=None):
    """Compare the trace coefficient using explicit scalar index contractions."""
    g0, h = data["background_metric"], data["perturbation"]
    R0 = data["operator_background"]
    R1 = data["operator_first_order"]
    R2 = data["operator_second_order"]
    T2_formula = data["trace_cube_coefficients"][2]

    direct_terms = []
    products = (
        ("R0R0R2", R0, R0, R2),
        ("R0R2R0", R0, R2, R0),
        ("R2R0R0", R2, R0, R0),
        ("R0R1R1", R0, R1, R1),
        ("R1R0R1", R1, R0, R1),
        ("R1R1R0", R1, R1, R0),
    )
    for label, A, B, C in products:
        if progress is not None:
            progress("direct_trace_" + label + "_started")
        direct_terms.append(_trace_product3(A, B, C))
        if progress is not None:
            progress("direct_trace_" + label + "_completed")
    T2_direct = sum(direct_terms, s.Integer(0))
    trace_residual = s.simplify(T2_direct-T2_formula)

    A = g0.inv()*h
    d2_independent = s.trace(A)**2/8 - s.trace(A*A)/4
    determinant_formula = data["density_coefficients_relative_to_background"][2]
    determinant_residual = s.cancel(d2_independent-determinant_formula)
    return {
        "trace_coefficient_method": "explicit scalar index contractions for all six ungrouped products",
        "trace_coefficient_residual": trace_residual,
        "determinant_density_residual": determinant_residual,
        "density_coefficient_residual": (trace_residual, determinant_residual),
        "passed": trace_residual == 0 and determinant_residual == 0,
    }
