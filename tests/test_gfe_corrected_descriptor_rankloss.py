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


def test_horizon_special_frequency_logarithmic_relation() -> None:
    """Certify the n=1 log-amplitude relation at the sole resonance 4M*omega=I."""
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    x, p, a0, b0, c1, d1, L = sp.symbols("x p a0 b0 c1 d1 L")
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

    def log_jet(q: sp.Expr, order: int) -> sp.Expr:
        coeff = falling(q, order)
        return coeff * L + sp.diff(coeff, p)

    jet_subs = {
        jets[f"h0r{j}"]: (
            a0 * falling(p, j) * x ** (-j)
            + c1 * log_jet(p + 1, j) * x ** (1 - j)
        )
        for j in range(5)
    }
    jet_subs.update({
        jets[f"h1r{j}"]: (
            b0 * falling(p - 1, j) * x ** (-j - 1)
            + d1 * log_jet(p, j) * x ** (-j)
        )
        for j in range(5)
    })

    physical = {p: -2 * sp.I * M * omega, b0: 2 * M * a0}
    conditions = []

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
        d1_den = denominator_poly.nth(denominator_order + 1)

        leading = sp.cancel(n0 / d0)
        next_coefficient = sp.cancel((n1 * d0 - n0 * d1_den) / d0**2)
        assert sp.factor(sp.cancel(leading.subs(physical))) == 0

        next_physical = sp.expand(sp.factor(sp.cancel(next_coefficient.subs(physical))))
        conditions.append(sp.factor(sp.cancel(next_physical.coeff(L, 1))))
        conditions.append(sp.factor(sp.cancel(next_physical.subs(L, 0))))

    special = [
        sp.factor(sp.cancel(condition.subs(omega, sp.I / (4 * M))))
        for condition in conditions
    ]
    assert special[0] == 0
    assert special[2] == 0

    relation = (
        3 * (5 * M**2 + beta) * (d1 - 6 * M * c1)
        + 10 * a0 * beta * (lam - 2)
    )
    assert sp.factor(sp.cancel(special[1] + beta * lam * relation / (288 * M**4))) == 0
    assert sp.factor(sp.cancel(special[3] + beta * lam * relation / (576 * M**5))) == 0

    d1_solution = (
        6 * M * c1
        - 10 * a0 * beta * (lam - 2) / (3 * (5 * M**2 + beta))
    )
    assert sp.factor(sp.cancel(relation.subs(d1, d1_solution))) == 0


def test_horizon_special_frequency_n2_reordered_consistency() -> None:
    """Certify n=2 consistency after delayed lower-order substitution."""
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    x, p, L = sp.symbols("x p L")
    a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")
    c1, c2, d1, d2 = sp.symbols("c1 c2 d1 d2")
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

    def log_jet(q: sp.Expr, order: int) -> sp.Expr:
        coeff = falling(q, order)
        return coeff * L + sp.diff(coeff, p)

    jet_subs = {
        jets[f"h0r{j}"]: (
            a0 * falling(p, j) * x ** (-j)
            + a1 * falling(p + 1, j) * x ** (1 - j)
            + a2 * falling(p + 2, j) * x ** (2 - j)
            + c1 * log_jet(p + 1, j) * x ** (1 - j)
            + c2 * log_jet(p + 2, j) * x ** (2 - j)
        )
        for j in range(5)
    }
    jet_subs.update({
        jets[f"h1r{j}"]: (
            b0 * falling(p - 1, j) * x ** (-j - 1)
            + b1 * falling(p, j) * x ** (-j)
            + b2 * falling(p + 1, j) * x ** (1 - j)
            + d1 * log_jet(p, j) * x ** (-j)
            + d2 * log_jet(p + 1, j) * x ** (1 - j)
        )
        for j in range(5)
    })

    special = {
        p: sp.Rational(1, 2),
        omega: sp.I / (4 * M),
        b0: 2 * M * a0,
    }
    next_coefficients = []
    n2_conditions = []

    for equation_text in data["euler_equations"]:
        equation = sp.sympify(equation_text, locals=locals_)
        trial = sp.together(equation.subs(r, 2 * M + x).subs(jet_subs))
        numerator, denominator = sp.fraction(trial)
        numerator_poly = sp.Poly(sp.expand(numerator), x)
        denominator_poly = sp.Poly(sp.expand(denominator), x)

        numerator_order = min(monomial[0] for monomial, _ in numerator_poly.terms())
        denominator_order = min(monomial[0] for monomial, _ in denominator_poly.terms())
        numerators = [numerator_poly.nth(numerator_order + k) for k in range(3)]
        denominators = [denominator_poly.nth(denominator_order + k) for k in range(3)]

        quotient = []
        for k in range(3):
            lower = sum(
                denominators[j] * quotient[k - j]
                for j in range(1, k + 1)
            )
            quotient.append(sp.cancel((numerators[k] - lower) / denominators[0]))

        q0 = sp.factor(sp.cancel(quotient[0].subs(special)))
        q1 = sp.expand(sp.factor(sp.cancel(quotient[1].subs(special))))
        q2 = sp.expand(sp.factor(sp.cancel(quotient[2].subs(special))))
        assert q0 == 0
        assert sp.Poly(q1, L).degree() <= 1
        assert sp.Poly(q2, L).degree() <= 1
        next_coefficients.append(q1)
        n2_conditions.append(sp.factor(sp.cancel(q2.coeff(L, 1))))
        n2_conditions.append(sp.factor(sp.cancel(q2.subs(L, 0))))

    A = 5 * M**2 + beta
    c1_forced = 5 * a0 * beta * (lam - 2) / (12 * M * A)
    d1_forced = -2 * M * c1_forced
    b1_forced = (
        -2 * M * a1
        + a0 * ((300 * M**2 - 95 * beta) * lam - 510 * M**2 + 208 * beta)
        / (15 * A)
    )
    forced = {c1: c1_forced, d1: d1_forced, b1: b1_forced}

    for q1 in next_coefficients:
        assert sp.factor(sp.cancel(q1.subs(forced))) == 0

    reduced = [
        sp.factor(sp.cancel(condition.subs(forced)))
        for condition in n2_conditions
    ]
    log_e0, plain_e0, log_e1, plain_e1 = reduced

    assert sp.factor(sp.cancel(log_e1 + log_e0 / (2 * M))) == 0
    assert sp.factor(
        sp.cancel(plain_e1 + plain_e0 / (2 * M) - log_e0 / M)
    ) == 0

    pivot = beta * lam * A / (48 * M**4)
    assert sp.factor(sp.cancel(sp.diff(log_e0, d2) - pivot)) == 0
    assert sp.factor(sp.cancel(sp.diff(plain_e0, b2) - pivot)) == 0

    P = (
        144 * M**4
        - 30 * M**2 * beta * lam
        + 30 * M**2 * beta
        - 19 * beta**2 * lam
        + 38 * beta**2
    )
    d2_explicit = (
        10 * M * c2
        + 5 * a0 * (lam - 2) * P / (36 * M * A**2)
    )
    d2_from_pivot = sp.cancel(-log_e0.subs(d2, 0) / sp.diff(log_e0, d2))
    assert sp.factor(sp.cancel(d2_from_pivot - d2_explicit)) == 0

    R = (
        -86400 * M**6 * lam
        + 116640 * M**6
        + 22140 * M**4 * beta * lam
        - 49212 * M**4 * beta
        + 19350 * M**2 * beta**2 * lam**2
        - 59970 * M**2 * beta**2 * lam
        + 42720 * M**2 * beta**2
        - 2675 * beta**3 * lam**2
        + 12044 * beta**3 * lam
        - 13604 * beta**3
    )
    b2_explicit = (
        10 * M * a2
        + 4 * M * c2
        + a1 * P / (3 * beta * A)
        + a0 * R / (360 * M * beta * A**2)
    )
    plain_after_d2 = sp.cancel(plain_e0.subs(d2, d2_explicit))
    b2_from_pivot = sp.cancel(
        -plain_after_d2.subs(b2, 0) / sp.diff(plain_after_d2, b2)
    )
    assert sp.factor(sp.cancel(b2_from_pivot - b2_explicit)) == 0

    solved = {d2: d2_explicit, b2: b2_explicit}
    for condition in reduced:
        assert sp.factor(sp.cancel(condition.subs(solved))) == 0


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
