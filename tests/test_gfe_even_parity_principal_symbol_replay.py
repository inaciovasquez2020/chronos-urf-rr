from __future__ import annotations

import sympy as s


def _reported_three_jet_hessian(M: s.Symbol, r: s.Symbol) -> s.Matrix:
    return s.Matrix(
        [
            [
                3 * M * (r - 2 * M) ** 2 / r**3,
                6 * M * (r - 2 * M) / r**2,
                -3 * M / r,
            ],
            [
                6 * M * (r - 2 * M) / r**2,
                12 * M / r,
                6 * M / (2 * M - r),
            ],
            [
                -3 * M / r,
                6 * M / (2 * M - r),
                3 * M * r / (r - 2 * M) ** 2,
            ],
        ]
    )


def test_reported_three_jet_principal_hessian_is_exact_rank_one() -> None:
    M, r = s.symbols("M r", positive=True)
    hessian = _reported_three_jet_hessian(M, r)
    vector = s.Matrix([1, 2 * r / (r - 2 * M), -r**2 / (r - 2 * M) ** 2])
    prefactor = 3 * M * (r - 2 * M) ** 2 / (2 * r**3)

    assert hessian == hessian.T
    assert all(
        s.factor((hessian - 2 * prefactor * vector * vector.T)[i, j]) == 0
        for i in range(3)
        for j in range(3)
    )
    assert s.factor(hessian.det()) == 0
    assert all(
        s.factor(hessian.extract([i, j], [a, b]).det()) == 0
        for i in range(3)
        for j in range(i + 1, 3)
        for a in range(3)
        for b in range(a + 1, 3)
    )
    assert hessian.rank() == 1


def test_reported_six_jet_hessian_has_rank_four_on_exterior_domain() -> None:
    M, r = s.symbols("M r", positive=True)
    three_jet = _reported_three_jet_hessian(M, r)
    k_block = s.diag(
        -3 * M * r / (r - 2 * M) ** 2,
        6 * M / r,
        -3 * M * (r - 2 * M) ** 2 / r**3,
    )
    full_hessian = s.diag(1, 1, 1, 1, 1, 1)
    full_hessian[:3, :3] = three_jet
    full_hessian[3:, 3:] = k_block

    assert three_jet.rank() == 1
    assert k_block.rank() == 3
    assert full_hessian.rank() == 4


def test_reported_k_sector_principal_polynomial_factors_exactly() -> None:
    M, r, omega, k = s.symbols("M r omega k", positive=True)
    polynomial = (
        -3 * M * r / (r - 2 * M) ** 2 * omega**4
        + 6 * M / r * omega**2 * k**2
        - 3 * M * (r - 2 * M) ** 2 / r**3 * k**4
    )
    square_form = -3 * M * (
        s.sqrt(r) / (r - 2 * M) * omega**2
        - (r - 2 * M) / r ** s.Rational(3, 2) * k**2
    ) ** 2
    assert s.expand(polynomial - square_form) == 0
    assert s.factor(r**2 * omega**2 - (r - 2 * M) ** 2 * k**2) == (
        (r * omega - (r - 2 * M) * k)
        * (r * omega + (r - 2 * M) * k)
    )
