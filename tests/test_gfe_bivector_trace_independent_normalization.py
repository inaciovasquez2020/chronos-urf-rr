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


def test_h0_radial_principal_coefficient_uses_computed_background_operator() -> None:
    # This is a one-component principal-symbol check, not a full quadratic
    # action. The background curvature operator is recomputed from the metric.
    M, r, theta = s.symbols("M r theta", positive=True, real=True)
    q_h0_rr = s.symbols("q_h0_rr", real=True)
    f = 1 - 2 * M / r
    background, inverse, pairs = _schwarzschild_bivector_operator(M, r, theta)

    tr_pair_index = pairs.index((0, 1))
    background_tr_eigenvalue = s.factor(background[tr_pair_index, tr_pair_index])
    assert s.factor(background_tr_eigenvalue - 2 * M / r**3) == 0

    # For h_tt=-f H0 Y20, the radial principal part is
    # delta R_trtr=(f/2) H0_rr Y20. Raising the second pair yields
    # delta R_tr{}^tr= g^tt*g^rr*delta R_trtr = -(f/2) H0_rr Y20.
    # Encode that single curvature component in the six-dimensional operator;
    # no repository coefficient or axial normalization is used.
    y20 = s.sqrt(s.Rational(5, 16) / s.pi) * (3 * s.cos(theta) ** 2 - 1)
    raised_principal_component = s.factor(
        inverse[0, 0] * inverse[1, 1] * (f * q_h0_rr * y20 / 2)
    )
    radial_principal = s.zeros(6)
    radial_principal[tr_pair_index, tr_pair_index] = raised_principal_component

    density = s.factor(
        3
        * s.trace(background * radial_principal * radial_principal)
        * r**2
        * s.sin(theta)
    )
    phi = s.symbols("phi", real=True)
    ordinary_trace_coefficient = s.factor(
        s.integrate(density, (phi, 0, 2 * s.pi), (theta, 0, s.pi))
    )
    expected_ordinary_trace = 3 * M * (r - 2 * M) ** 2 / (2 * r**3)
    assert s.factor(
        ordinary_trace_coefficient / q_h0_rr**2 - expected_ordinary_trace
    ) == 0

    relative_action_coefficient = s.factor(
        ordinary_trace_coefficient / (9 * q_h0_rr**2)
    )
    expected_relative_action = M * (r - 2 * M) ** 2 / (6 * r**3)
    assert s.factor(relative_action_coefficient - expected_relative_action) == 0

    # For L=C*(H0_rr)**2, the EL principal coefficient of H0_rrrr is 2C.
    fourth_radial_coefficient = s.diff(
        relative_action_coefficient * q_h0_rr**2, q_h0_rr, 2
    )
    expected_fourth_radial = M * (r - 2 * M) ** 2 / (3 * r**3)
    assert s.factor(fourth_radial_coefficient - expected_fourth_radial) == 0
    assert s.simplify(fourth_radial_coefficient.subs(r, 3 * M)) > 0
