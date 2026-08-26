from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def _symbols():
    return sp.symbols("M beta lam omega r")


def test_principal_determinant_factorization_and_exterior_root() -> None:
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
    }

    det = sp.sympify(data["principal_determinant"], locals=locals_)
    expected = (
        beta**2
        * lam**2
        * (lam - 2)
        * (r - 2 * M) ** 3
        * (-16 * M * beta + 5 * r**3)
        * (8 * M * beta + 5 * r**3)
        / (36 * r**11)
    )
    assert sp.factor(det - expected) == 0

    beta_c = 5 * r**3 / (16 * M)
    assert sp.simplify(det.subs(beta, beta_c)) == 0


def test_principal_null_direction_at_descriptor_surface() -> None:
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
    }

    principal = sp.Matrix(
        [[sp.sympify(entry, locals=locals_) for entry in row]
         for row in data["principal_matrix"]]
    )
    beta_c = 5 * r**3 / (16 * M)
    principal_c = principal.applyfunc(lambda x: sp.factor(x.subs(beta, beta_c)))

    A_c = -25 * lam * r**2 * (r - 2 * M) / (64 * M)
    expected = A_c * sp.Matrix([
        [1, sp.I * omega],
        [sp.I * omega, -omega**2],
    ])
    assert principal_c.applyfunc(sp.factor) == expected.applyfunc(sp.factor)

    v_c = sp.Matrix([-sp.I * omega, 1])
    w_c = sp.Matrix([[-sp.I * omega, 1]])
    assert (principal_c * v_c).applyfunc(sp.simplify) == sp.zeros(2, 1)
    assert (w_c * principal_c).applyfunc(sp.simplify) == sp.zeros(1, 2)

    # Under the ordinary exterior guards M != 0, r != 2M, lam != 0,
    # A_c is nonzero, so the matrix has rank exactly one rather than zero.
    assert sp.factor(principal_c[0, 0] - A_c) == 0


def test_horizon_ingoing_frobenius_leading_relation() -> None:
    """Certify the exact leading ingoing Frobenius relation at r=2M.

    With Fourier convention exp(-I*omega*t), horizon regularity in ingoing
    Eddington-Finkelstein coordinates v=t+r_* gives the Schwarzschild-radial
    weights

        h0 ~ x^p a0,
        h1 ~ x^(p-1) b0,
        p = -2 I M omega,
        b0 = 2 M a0,

    where x=r-2M.  The test derives the generic leading Euler coefficients
    from the stored exact equations, then checks that this nonzero ingoing
    pair annihilates both leading indicial conditions.  It does not propagate
    the branch to r_c and does not evaluate the crossing functional.
    """
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    x, p, a0, b0 = sp.symbols("x p a0 b0")
    jets = {
        **{f"h0r{j}": sp.symbols(f"h0r{j}") for j in range(5)},
        **{f"h1r{j}": sp.symbols(f"h1r{j}") for j in range(5)},
    }
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
        **jets,
    }

    def falling(q: sp.Expr, order: int) -> sp.Expr:
        return sp.prod(q - k for k in range(order))

    jet_subs = {
        jets[f"h0r{j}"]: a0 * falling(p, j) * x ** (-j)
        for j in range(5)
    }
    jet_subs.update({
        jets[f"h1r{j}"]: b0 * falling(p - 1, j) * x ** (-j - 1)
        for j in range(5)
    })

    physical = {p: -2 * sp.I * M * omega, b0: 2 * M * a0}

    for equation_text in data["euler_equations"]:
        equation = sp.sympify(equation_text, locals=locals_)
        trial = sp.together(equation.subs(r, 2 * M + x).subs(jet_subs))
        numerator, denominator = sp.fraction(trial)
        numerator_poly = sp.Poly(sp.expand(numerator), x)
        denominator_poly = sp.Poly(sp.expand(denominator), x)

        numerator_order = min(monomial[0] for monomial, _ in numerator_poly.terms())
        denominator_order = min(monomial[0] for monomial, _ in denominator_poly.terms())
        leading = sp.cancel(
            numerator_poly.nth(numerator_order)
            / denominator_poly.nth(denominator_order)
        )

        # The leading indicial condition is genuine before selecting the
        # physical ingoing relation, and is killed exactly by that relation.
        assert leading != 0
        assert sp.factor(sp.cancel(leading.subs(physical))) == 0


def test_horizon_ingoing_frobenius_n1_is_identity() -> None:
    """Derive n=1 exactly and certify that its recurrence is the identity 0=0."""
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    x, p, a0, a1, b0, b1 = sp.symbols("x p a0 a1 b0 b1")
    jets = {
        **{f"h0r{j}": sp.symbols(f"h0r{j}") for j in range(5)},
        **{f"h1r{j}": sp.symbols(f"h1r{j}") for j in range(5)},
    }
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
        **jets,
    }

    def falling(q: sp.Expr, order: int) -> sp.Expr:
        return sp.prod(q - k for k in range(order))

    jet_subs = {
        jets[f"h0r{j}"]: (
            a0 * falling(p, j) * x ** (-j)
            + a1 * falling(p + 1, j) * x ** (1 - j)
        )
        for j in range(5)
    }
    jet_subs.update({
        jets[f"h1r{j}"]: (
            b0 * falling(p - 1, j) * x ** (-j - 1)
            + b1 * falling(p, j) * x ** (-j)
        )
        for j in range(5)
    })

    physical = {p: -2 * sp.I * M * omega, b0: 2 * M * a0}
    next_conditions = []

    for equation_text in data["euler_equations"]:
        equation = sp.sympify(equation_text, locals=locals_)
        trial = sp.together(equation.subs(r, 2 * M + x).subs(jet_subs))
        numerator, denominator = sp.fraction(trial)
        numerator_poly = sp.Poly(sp.expand(numerator), x)
        denominator_poly = sp.Poly(sp.expand(denominator), x)

        numerator_order = min(monomial[0] for monomial, _ in numerator_poly.terms())
        denominator_order = min(monomial[0] for monomial, _ in denominator_poly.terms())
        n0 = numerator_poly.nth(numerator_order)
        n1 = numerator_poly.nth(numerator_order + 1)
        d0 = denominator_poly.nth(denominator_order)
        d1 = denominator_poly.nth(denominator_order + 1)

        leading = sp.cancel(n0 / d0)
        next_coefficient = sp.cancel((n1 * d0 - n0 * d1) / d0**2)
        assert sp.factor(sp.cancel(leading.subs(physical))) == 0
        next_conditions.append(sp.factor(sp.cancel(next_coefficient.subs(physical))))

    coefficient_matrix, source = sp.linear_eq_to_matrix(next_conditions, (a1, b1))
    assert coefficient_matrix == sp.zeros(2, 2)
    for i, entry in enumerate(source):
        reduced = sp.factor(sp.cancel(entry))
        assert reduced == 0, f"n=1 source[{i}]={reduced}"


def test_backtrack_boundary_is_not_overclaimed() -> None:
    """The local certificate does not decide the horizon-selected branch.

    This regression deliberately records only the algebraic rank-loss and null
    direction.  Whether the physical ingoing solution satisfies the projected
    compatibility condition at r_c is a separate global connection problem.
    """
    data = json.loads(ARTIFACT.read_text())
    assert data["differential_orders"] == {
        "E0_h0": 4,
        "E0_h1": 3,
        "E1_h0": 3,
        "E1_h1": 2,
    }
