from __future__ import annotations

from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
AXIAL_GENERATOR = ROOT / "tools/gfe/derive_gfe_axial_quadratic_action.sh"


def _schwarzschild_bivector_operator(
    M: s.Symbol, r: s.Symbol, theta: s.Symbol
) -> tuple[s.Matrix, s.Matrix, list[tuple[int, int]]]:
    t, phi = s.symbols("t phi", real=True)
    coordinates = (t, r, theta, phi)
    f = 1 - 2 * M / r
    metric = s.diag(-f, 1 / f, r**2, r**2 * s.sin(theta) ** 2)
    inverse = s.simplify(metric.inv())
    dimension = 4

    christoffel = [
        [[s.Integer(0) for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                christoffel[a][b][c] = s.simplify(
                    s.Rational(1, 2)
                    * sum(
                        inverse[a, d]
                        * (
                            s.diff(metric[d, c], coordinates[b])
                            + s.diff(metric[d, b], coordinates[c])
                            - s.diff(metric[b, c], coordinates[d])
                        )
                        for d in range(dimension)
                    )
                )

    riemann_up = [
        [
            [
                [s.Integer(0) for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                for d in range(dimension):
                    riemann_up[a][b][c][d] = s.simplify(
                        s.diff(christoffel[a][b][d], coordinates[c])
                        - s.diff(christoffel[a][b][c], coordinates[d])
                        + sum(
                            christoffel[a][c][e] * christoffel[e][b][d]
                            - christoffel[a][d][e] * christoffel[e][b][c]
                            for e in range(dimension)
                        )
                    )

    riemann_low = [
        [
            [
                [s.Integer(0) for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                for d in range(dimension):
                    riemann_low[a][b][c][d] = s.simplify(
                        sum(
                            metric[a, e] * riemann_up[e][b][c][d]
                            for e in range(dimension)
                        )
                    )

    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    operator = s.zeros(6)
    for row, (a, b) in enumerate(pairs):
        for column, (c, d) in enumerate(pairs):
            operator[row, column] = s.simplify(
                sum(
                    inverse[c, e]
                    * inverse[d, h]
                    * riemann_low[a][b][e][h]
                    for e in range(dimension)
                    for h in range(dimension)
                )
            )
    return operator, inverse, pairs


def _principal_riemann_operator(
    electric_components: dict[tuple[int, int], s.Expr],
    inverse: s.Matrix,
    pairs: list[tuple[int, int]],
) -> s.Matrix:
    # The pure second-time principal part of the linearized curvature is
    # delta R_{0 i 0 j} = -1/2 partial_t^2 h_{ij}.  All omitted terms have
    # fewer than two time derivatives and cannot contribute to the squared
    # second-time-derivative Hessian extracted below.
    dimension = 4
    lowered = [
        [
            [
                [s.Integer(0) for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for i in range(1, dimension):
        for j in range(1, dimension):
            value = electric_components.get((i, j), s.Integer(0))
            for a, b, c, d, signed in (
                (0, i, 0, j, value),
                (i, 0, 0, j, -value),
                (0, i, j, 0, -value),
                (i, 0, j, 0, value),
            ):
                lowered[a][b][c][d] = signed

    operator = s.zeros(6)
    for row, (a, b) in enumerate(pairs):
        for column, (c, d) in enumerate(pairs):
            operator[row, column] = s.simplify(
                sum(
                    inverse[c, e]
                    * inverse[d, h]
                    * lowered[a][b][e][h]
                    for e in range(dimension)
                    for h in range(dimension)
                )
            )
    return operator


def _integrated_matrix_trace_coefficient(
    background: s.Matrix,
    perturbation: s.Matrix,
    r: s.Symbol,
    theta: s.Symbol,
) -> s.Expr:
    phi = s.symbols("phi", real=True)
    density = s.simplify(
        3 * s.trace(background * perturbation * perturbation)
        * r**2
        * s.sin(theta)
    )
    return s.factor(
        s.integrate(density, (phi, 0, 2 * s.pi), (theta, 0, s.pi))
    )


def test_even_parity_relative_beta2_source_stops_at_higher_derivative_obstruction() -> None:
    source = AXIAL_GENERATOR.read_text()
    assert '"k1_tt^2": "6*Ls*M/(r**2*(-2*M + r))"' in source

    M, r, theta = s.symbols("M r theta", positive=True, real=True)
    q_h2, q_k = s.symbols("q_h2 q_k", real=True)
    background, inverse, pairs = _schwarzschild_bivector_operator(M, r, theta)
    expected_background = s.diag(
        2 * M / r**3,
        -M / r**3,
        -M / r**3,
        -M / r**3,
        -M / r**3,
        2 * M / r**3,
    )
    assert s.simplify(background - expected_background) == s.zeros(6)

    y20 = s.sqrt(s.Rational(5, 16) / s.pi) * (3 * s.cos(theta) ** 2 - 1)
    assert s.simplify(
        2 * s.pi * s.integrate(y20**2 * s.sin(theta), (theta, 0, s.pi)) - 1
    ) == 0

    # Calibrate the repository's Tr_{Lambda^2}(Rop^3) normalization against
    # the already-certified axial ell=2 coefficient of (partial_t^2 h1)^2.
    axial_vector_phi = s.sin(theta) * s.diff(y20, theta)
    axial_principal = _principal_riemann_operator(
        {
            (1, 3): -s.Rational(1, 2) * axial_vector_phi,
            (3, 1): -s.Rational(1, 2) * axial_vector_phi,
        },
        inverse,
        pairs,
    )
    axial_matrix_trace = _integrated_matrix_trace_coefficient(
        background, axial_principal, r, theta
    )
    axial_repository_coefficient = 36 * M / (r**2 * (r - 2 * M))
    normalization = s.factor(
        s.cancel(axial_repository_coefficient / axial_matrix_trace)
    )
    assert normalization == 8

    # Regge--Wheeler even parity: h_rr=f^{-1} H2 Y and
    # h_AB=r^2 K Y Omega_AB.  H0 and H1 have no pure second-time curvature
    # principal entry; the spatial variables H2 and K do.
    f = 1 - 2 * M / r
    polar_principal = _principal_riemann_operator(
        {
            (1, 1): -s.Rational(1, 2) * y20 * q_h2 / f,
            (2, 2): -s.Rational(1, 2) * r**2 * y20 * q_k,
            (3, 3): -s.Rational(1, 2)
            * r**2
            * s.sin(theta) ** 2
            * y20
            * q_k,
        },
        inverse,
        pairs,
    )
    cubic_hessian_principal = s.factor(
        normalization
        * _integrated_matrix_trace_coefficient(
            background, polar_principal, r, theta
        )
    )
    expected_cubic_hessian = (
        12 * M * r / (r - 2 * M) ** 2 * (q_h2**2 - q_k**2)
    )
    assert s.factor(cubic_hessian_principal - expected_cubic_hessian) == 0

    # The GfE relative beta^2 action uses one ninth of the cubic Hessian.
    relative_source_principal = s.factor(cubic_hessian_principal / 9)
    expected_relative_source = (
        4 * M * r / (3 * (r - 2 * M) ** 2) * (q_h2**2 - q_k**2)
    )
    assert s.factor(relative_source_principal - expected_relative_source) == 0

    q_h0, q_h1 = s.symbols("q_h0 q_h1", real=True)
    temporal_hessian = s.hessian(
        relative_source_principal,
        (q_h0, q_h1, q_h2, q_k),
    )
    expected_hessian = s.diag(
        0,
        0,
        8 * M * r / (3 * (r - 2 * M) ** 2),
        -8 * M * r / (3 * (r - 2 * M) ** 2),
    )
    assert s.simplify(temporal_hessian - expected_hessian) == s.zeros(4)
    assert temporal_hessian.rank() == 2

    exterior_offset = s.symbols("exterior_offset", positive=True)
    exterior_coefficient = s.factor(
        expected_hessian[2, 2].subs(r, 2 * M + exterior_offset)
    )
    assert exterior_coefficient == (
        8 * M * (2 * M + exterior_offset)
        / (3 * exterior_offset**2)
    )

    # The Euler source therefore contains nonzero fourth-time derivatives:
    # +C4 partial_t^4 H2 and -C4 partial_t^4 K.  This is the mandated stop.
    fourth_time_coefficient = expected_hessian[2, 2]
    assert fourth_time_coefficient != 0
