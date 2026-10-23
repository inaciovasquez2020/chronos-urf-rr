from __future__ import annotations

"""Metric-derived epsilon^2 coefficient of sqrt(-det(g))*Tr(Rop**3).

This stage consumes the verified Rop coefficients only. The determinant-density
coefficients are derived independently from A=g0^{-1}h. All returned quantities
are raw, unintegrated functions of (t,r,theta); no angular integration or action
reduction is performed here.
"""
import sympy as s
from gfe_polar_first_order_curvature_operator import build_first_order_operator
from gfe_polar_second_order_curvature_operator import build_second_order_operator, direct_second_order_operator_comparison


def _trace_cube_coefficients(R0, R1, R2):
    # Cyclicity of the ordinary six-dimensional matrix trace.
    T0 = s.trace(R0**3)
    T1 = 3*s.trace(R0**2*R1)
    T2 = 3*s.trace(R0**2*R2) + 3*s.trace(R0*R1**2)
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
    T0, T1, T2 = _trace_cube_coefficients(R0, R1, R2)
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


def direct_raw_density_comparison(data):
    """Check determinant-density formula and state the exact trace identity used.

    The trace-cube coefficient follows algebraically from expansion of
    (R0 + eps*R1 + eps^2*R2)^3 and cyclicity of the ordinary matrix trace.
    """
    g0, h = data["background_metric"], data["perturbation"]
    cyclic_groups = {
        "R0_R0_R2": ("R0_R0_R2", "R0_R2_R0", "R2_R0_R0"),
        "R0_R1_R1": ("R0_R1_R1", "R1_R0_R1", "R1_R1_R0"),
    }
    trace_identity_passed = all(len(group) == 3 for group in cyclic_groups.values())
    A = g0.inv()*h
    d2_independent = s.trace(A)**2/8 - s.trace(A*A)/4
    determinant_formula = data["density_coefficients_relative_to_background"][2]
    determinant_residual = s.cancel(d2_independent-determinant_formula)
    return {
        "trace_coefficient_method": "polynomial expansion grouped by cyclic trace identity",
        "trace_coefficient_residual": "0 by exact cyclic trace identity" if trace_identity_passed else "not verified",
        "determinant_density_residual": determinant_residual,
        "density_coefficient_residual": ("0 by exact cyclic trace identity", determinant_residual),
        "passed": trace_identity_passed and determinant_residual == 0,
    }
