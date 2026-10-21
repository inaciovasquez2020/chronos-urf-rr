from __future__ import annotations

import sympy as s

from test_gfe_polar_even_parity_quadratic_source_obstruction import (
    _integrated_matrix_trace_coefficient,
    _principal_riemann_operator,
    _schwarzschild_bivector_operator,
)


def test_ordinary_bivector_trace_coefficients_are_not_table_calibrated() -> None:
    M, r, theta = s.symbols("M r theta", positive=True, real=True)
    q_h2, q_k = s.symbols("q_h2 q_k", real=True)
    background, inverse, pairs = _schwarzschild_bivector_operator(M, r, theta)

    y20 = s.sqrt(s.Rational(5, 16) / s.pi) * (3 * s.cos(theta) ** 2 - 1)

    axial_vector_phi = s.sin(theta) * s.diff(y20, theta)
    axial_principal = _principal_riemann_operator(
        {
            (1, 3): -s.Rational(1, 2) * axial_vector_phi,
            (3, 1): -s.Rational(1, 2) * axial_vector_phi,
        },
        inverse,
        pairs,
    )
    axial_trace = _integrated_matrix_trace_coefficient(
        background, axial_principal, r, theta
    )
    assert s.factor(
        axial_trace - 9 * M / (2 * r**2 * (r - 2 * M))
    ) == 0

    f = 1 - 2 * M / r
    polar_principal = _principal_riemann_operator(
        {
            (1, 1): -s.Rational(1, 2) * y20 * q_h2 / f,
            (2, 2): -s.Rational(1, 2) * r**2 * y20 * q_k,
            (3, 3): -s.Rational(1, 2) * r**2 * s.sin(theta) ** 2 * y20 * q_k,
        },
        inverse,
        pairs,
    )
    polar_trace = _integrated_matrix_trace_coefficient(
        background, polar_principal, r, theta
    )
    expected_polar_trace = (
        3 * M * r / (2 * (r - 2 * M) ** 2) * (q_h2**2 - q_k**2)
    )
    assert s.factor(polar_trace - expected_polar_trace) == 0

    relative_action = s.factor(polar_trace / 9)
    relative_hessian = s.hessian(relative_action, (q_h2, q_k))
    expected_hessian = s.diag(
        M * r / (3 * (r - 2 * M) ** 2),
        -M * r / (3 * (r - 2 * M) ** 2),
    )
    assert s.simplify(relative_hessian - expected_hessian) == s.zeros(2)
