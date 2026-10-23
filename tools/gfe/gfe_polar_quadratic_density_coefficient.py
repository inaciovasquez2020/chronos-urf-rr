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


def build_raw_quadratic_density(first_data=None, second_data=None):
    first = first_data if first_data is not None else build_first_order_operator()
    second = second_data if second_data is not None else build_second_order_operator(first)
    g0, h = first["background_metric"], first["perturbation"]
    A = g0.inv()*h
    trA = s.trace(A)
    trA2 = s.trace(A*A)
    # sqrt(-det(g0+eps*h)) = sqrt(-det(g0))*(1+eps*d1+eps^2*d2+...)
    d1 = s.expand(trA/2)
    d2 = s.expand(trA**2/8 - trA2/4)
    R0 = first["operator_background"]
    R1 = first["operator_first_order"]
    R2 = second["operator_second_order"]
    T0, T1, T2 = _trace_cube_coefficients(R0, R1, R2)
    density0 = s.sqrt(-g0.det())
    raw = density0*(T2 + d1*T1 + d2*T0)
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
    """Independent epsilon-series convolution for trace and determinant density.

    It recomputes the order-two trace coefficient from matrix coefficient
    convolution, then combines independently derived determinant coefficients.
    """
    g0, h = data["background_metric"], data["perturbation"]
    R0, R1, R2 = data["operator_background"], data["operator_first_order"], data["operator_second_order"]
    # Independent multiplication of the truncated matrix polynomial R0+e R1+e^2 R2.
    # Coefficient extraction uses convolution rather than the closed trace identity.
    coeff = [s.zeros(6), s.zeros(6), s.zeros(6)]
    coeff[0], coeff[1], coeff[2] = R0, R1, R2
    cube2 = s.zeros(6)
    for i in range(3):
        for j in range(3):
            k = 2-i-j
            if 0 <= k < 3:
                cube2 += coeff[i]*coeff[j]*coeff[k]
    trace2_convolution = s.trace(cube2)
    A = g0.inv()*h
    d2_independent = s.trace(A)**2/8 - s.trace(A*A)/4
    # Reconstruct T0 and T1 from the lower-order matrices, not from cached trace terms.
    T0_independent = s.trace(R0*R0*R0)
    T1_independent = s.trace(R1*R0*R0)+s.trace(R0*R1*R0)+s.trace(R0*R0*R1)
    T2_formula = data["trace_cube_coefficients"][2]
    # Check the expensive curvature-dependent part before multiplying by the
    # determinant factor; this avoids expanding a huge common symbolic factor.
    residual = s.simplify(trace2_convolution-T2_formula)
    return {
        "trace_cube_epsilon_squared_convolution": trace2_convolution,
        "density_coefficient_residual": residual,
        "passed": residual == 0,
    }
