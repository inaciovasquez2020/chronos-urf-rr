from __future__ import annotations

from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
TIME_ORDER = ROOT / "tests/test_gfe_polar_transformed_h0_time_order.py"
ORDER_REDUCTION = ROOT / "tests/test_gfe_polar_even_parity_principal_order_reduction.py"


def _principal_riemann_operator(
    lowered_components: dict[tuple[int, int, int, int], s.Expr],
    inverse: s.Matrix,
    pairs: list[tuple[int, int]],
) -> s.Matrix:
    lowered = [
        [
            [
                [s.Integer(0) for _ in range(4)]
                for _ in range(4)
            ]
            for _ in range(4)
        ]
        for _ in range(4)
    ]
    for indices, value in lowered_components.items():
        lowered[indices[0]][indices[1]][indices[2]][indices[3]] = value
    operator = s.zeros(6)
    for row, (a, b) in enumerate(pairs):
        for column, (c, d) in enumerate(pairs):
            operator[row, column] = s.simplify(
                sum(
                    inverse[c, e]
                    * inverse[d, h]
                    * lowered[a][b][e][h]
                    for e in range(4)
                    for h in range(4)
                )
            )
    return operator


def test_transformed_h0_stops_at_nonzero_radial_derivative() -> None:
    time_source = TIME_ORDER.read_text()
    order_source = ORDER_REDUCTION.read_text()
    assert "assert max(time_orders)==2" in time_source
    assert "assert all(order<3 for order in time_orders)" in time_source
    assert "expected_substitution_matrix = s.Matrix([[a, a], [-a, 0]])" in order_source

    M, r, theta = s.symbols("M r theta", positive=True, real=True)
    q_h0_rr = s.symbols("q_h0_rr", real=True)
    f = 1 - 2 * M / r
    y20 = s.sqrt(s.Rational(5, 16) / s.pi) * (3 * s.cos(theta) ** 2 - 1)
    assert s.simplify(
        2 * s.pi * s.integrate(y20**2 * s.sin(theta), (theta, 0, s.pi)) - 1
    ) == 0

    background = s.diag(
        2 * M / r**3,
        -M / r**3,
        -M / r**3,
        -M / r**3,
        -M / r**3,
        2 * M / r**3,
    )
    inverse = s.diag(
        -1 / f,
        f,
        1 / r**2,
        1 / (r**2 * s.sin(theta) ** 2),
    )
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    # Regge--Wheeler lapse perturbation:
    #   h_00 = f H0 Y_20.
    # Its static highest-radial-derivative curvature component is
    #   delta R_0101 = -1/2 f Y_20 H0,rr.
    principal = -s.Rational(1, 2) * f * y20 * q_h0_rr
    perturbation = _principal_riemann_operator(
        {
            (0, 1, 0, 1): principal,
            (1, 0, 0, 1): -principal,
            (0, 1, 1, 0): -principal,
            (1, 0, 1, 0): principal,
        },
        inverse,
        pairs,
    )

    phi = s.symbols("phi", real=True)
    density = s.simplify(
        3 * s.trace(background * perturbation * perturbation)
        * r**2
        * s.sin(theta)
    )
    integrated = s.integrate(
        density,
        (phi, 0, 2 * s.pi),
        (theta, 0, s.pi),
    )

    # Repository normalization is eight; the relative beta^2 action is one ninth
    # of the cubic Hessian, as in the merged axial/even-parity chain.
    cubic_hessian_principal = s.factor(8 * s.simplify(integrated))
    expected_cubic_hessian = (
        12 * M * (r - 2 * M) ** 2 / r**3 * q_h0_rr**2
    )
    assert s.factor(cubic_hessian_principal - expected_cubic_hessian) == 0

    relative_source_principal = s.factor(cubic_hessian_principal / 9)
    expected_relative_source = (
        4 * M * (r - 2 * M) ** 2 / (3 * r**3) * q_h0_rr**2
    )
    assert s.factor(relative_source_principal - expected_relative_source) == 0

    # The H0 Euler equation therefore contains
    #   2D H0,rrrr, D=4M(r-2M)^2/(3r^3),
    # plus lower radial derivatives.  This is nonzero in the exterior.
    fourth_radial_coefficient = s.factor(
        8 * M * (r - 2 * M) ** 2 / (3 * r**3)
    )
    assert fourth_radial_coefficient != 0
    exterior_offset = s.symbols("exterior_offset", positive=True)
    assert s.factor(
        fourth_radial_coefficient.subs(r, 2 * M + exterior_offset)
    ) == 8 * M * exterior_offset**2 / (3 * (2 * M + exterior_offset) ** 3)

    # The order-reduction substitution changes H2 and K only, so it cannot
    # cancel this H0-only radial principal term.
    assert "H2 = H2hat + beta^2*a*(H2hat_tt + Khat_tt)" in order_source
    assert "K  = Khat  - beta^2*a*H2hat_tt" in order_source
    assert "H0 =" not in order_source

