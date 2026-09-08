#!/usr/bin/env python3
"""Expose the exact normalized tail transfer for the ordinary order-2 Borel companion.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The canonical ordinary generalized-Frobenius coefficients satisfy a rank-one
coefficient equation at order n.  The missing right-kernel amplitude is fixed
by the left-null compatibility equation at order n+1.  Combining those two
scalar equations gives a nonsingular 2x2 solve for the ordinary coefficient
v^O_n in terms of the previous ten ordinary coefficients and the independently
known top-log coefficients.

After division by (n!)^2 this verifier constructs the exact recurrence

  O_n = sum_{j=1}^{10} T_j(n) O_{n-j}
        + sum_{k=-1}^{10} F_k(n) L_{n-k},

where O_n=v^O_n/(n!)^2 and L_n=v^L_n/(n!)^2.  The k=-1 term is the known
future top-log coefficient L_{n+1}; the top-log branch is triangular and has
already been certified independently.

This is a transfer-structure certificate.  It proves the symbolic solve is
nonsingular on the tail n>=21 and exposes exact rational infinity powers and
leading row-sum coefficients.  It deliberately does not infer a tail majorant
or claim a quantitative ordinary Borel bound.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_prefix as prefix


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def strict_polynomial_sign_from(expr: sp.Expr, n: sp.Symbol, N: int) -> int:
    """Return +1/-1 when coefficient positivity proves a strict tail sign."""
    m = sp.symbols("m", nonnegative=True)
    poly = sp.Poly(sp.expand(expr.subs(n, m + N)), m, domain=sp.QQ)
    coeffs = poly.all_coeffs()
    at_zero = poly.eval(0)
    if all(c >= 0 for c in coeffs) and at_zero > 0:
        return 1
    if all(c <= 0 for c in coeffs) and at_zero < 0:
        return -1
    return 0


def assert_rational_nonzero_from(expr: sp.Expr, n: sp.Symbol, N: int, label: str) -> None:
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    sn = strict_polynomial_sign_from(num, n, N)
    sd = strict_polynomial_sign_from(den, n, N)
    if sn == 0 or sd == 0:
        raise AssertionError(
            f"could not certify fixed nonzero sign for {label} on n>={N}: {sp.sstr(expr)}"
        )


def rational_power(expr: sp.Expr, n: sp.Symbol) -> int | None:
    value = simp(expr)
    if value == 0:
        return None
    num, den = sp.fraction(value)
    pn = sp.Poly(sp.expand(num), n, domain=sp.QQ)
    pd = sp.Poly(sp.expand(den), n, domain=sp.QQ)
    return int(pn.degree() - pd.degree())


def leading_at_power(expr: sp.Expr, n: sp.Symbol, power: int) -> sp.Rational:
    value = simp(expr)
    if value == 0:
        return sp.Rational(0)
    num, den = sp.fraction(value)
    pn = sp.Poly(sp.expand(num), n, domain=sp.QQ)
    pd = sp.Poly(sp.expand(den), n, domain=sp.QQ)
    actual = int(pn.degree() - pd.degree())
    if actual != power:
        return sp.Rational(0)
    return sp.Rational(pn.LC() / pd.LC())


def matrix_profile(matrix: sp.Matrix, n: sp.Symbol) -> tuple[int, sp.Rational]:
    powers = [rational_power(value, n) for value in matrix]
    finite = [power for power in powers if power is not None]
    if not finite:
        return (-10**9, sp.Rational(0))
    pmax = max(finite)
    leading = matrix.applyfunc(lambda value: leading_at_power(value, n, pmax))
    row_sums = [sum(abs(sp.Rational(leading[i, j])) for j in range(2)) for i in range(2)]
    return pmax, sp.Rational(max(row_sums))


def build_normalized_transfer() -> tuple[
    sp.Symbol,
    sp.Expr,
    dict[int, sp.Matrix],
    dict[int, sp.Matrix],
]:
    Cj, p = prefix.build_lag_blocks()
    J = len(Cj) - 1
    if J != 10:
        raise AssertionError(f"finite lag changed: {J}")

    n = sp.symbols("n", integer=True, positive=True)
    alpha = sp.Rational(1, 2)

    def rvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * (2 * k + 1)])

    def lvec(k: sp.Expr) -> sp.Matrix:
        return sp.Matrix([1, 2 * (2 * k - 3)])

    M = ms(Cj[0].subs(p, alpha + n))
    rnull = rvec(n)
    if any(value != 0 for value in ms(M * rnull)):
        raise AssertionError("ordinary order-n right-kernel vector changed")

    pivot_row = 0
    if M[pivot_row, 0] == 0 and M[pivot_row, 1] == 0:
        pivot_row = 1
    if M[pivot_row, 0] == 0 and M[pivot_row, 1] == 0:
        raise AssertionError("ordinary order-n leading matrix vanished identically")

    Mnext = ms(Cj[0].subs(p, alpha + n + 1))
    ell = lvec(n + 1)
    if any(value != 0 for value in ms(ell.T * Mnext)):
        raise AssertionError("ordinary order-(n+1) left-null vector changed")

    C1n = ms(Cj[1].subs(p, alpha + n))
    gamma = simp((ell.T * C1n * rnull)[0])
    expected_gamma = -sp.Rational(125, 6) * n**2
    if simp(gamma - expected_gamma) != 0:
        raise AssertionError(
            f"ordinary compatibility coupling changed: {sp.sstr(gamma)}"
        )

    first_row = sp.Matrix([[M[pivot_row, 0], M[pivot_row, 1]]])
    compatibility_row = ms(ell.T * C1n)
    solve_matrix = ms(sp.Matrix([
        [first_row[0, 0], first_row[0, 1]],
        [compatibility_row[0, 0], compatibility_row[0, 1]],
    ]))
    solve_det = simp(solve_matrix.det())
    if solve_det == 0:
        raise AssertionError("ordinary two-equation tail solve is singular identically")
    assert_rational_nonzero_from(solve_det, n, 21, "ordinary tail solve determinant")

    solve_inv = ms(solve_matrix.inv())

    ordinary_transfer: dict[int, sp.Matrix] = {}
    for lag in range(1, J + 1):
        rhs = sp.zeros(2, 2)
        block_n = ms(Cj[lag].subs(p, alpha + n - lag))
        rhs[0, 0] = -block_n[pivot_row, 0]
        rhs[0, 1] = -block_n[pivot_row, 1]
        if lag <= J - 1:
            block_next = ms(Cj[lag + 1].subs(p, alpha + n - lag))
            projected = ms(ell.T * block_next)
            rhs[1, 0] = -projected[0, 0]
            rhs[1, 1] = -projected[0, 1]
        falling = prefix.rr.falling(n, lag)
        ordinary_transfer[lag] = ms(solve_inv * rhs / falling**2)

    forcing_transfer: dict[int, sp.Matrix] = {}
    for lag in range(-1, J + 1):
        rhs = sp.zeros(2, 2)
        if 0 <= lag <= J:
            block_p = ms(Cj[lag].diff(p).subs(p, alpha + n - lag))
            rhs[0, 0] = -block_p[pivot_row, 0]
            rhs[0, 1] = -block_p[pivot_row, 1]
        if 0 <= lag + 1 <= J:
            block_p_next = ms(Cj[lag + 1].diff(p).subs(p, alpha + n - lag))
            projected_p = ms(ell.T * block_p_next)
            rhs[1, 0] = -projected_p[0, 0]
            rhs[1, 1] = -projected_p[0, 1]

        if lag == -1:
            moment_factor = (n + 1) ** 2
        else:
            moment_factor = 1 / prefix.rr.falling(n, lag) ** 2
        forcing_transfer[lag] = ms(solve_inv * rhs * moment_factor)

    # Algebraic reconstruction checks: undo the 2x2 solve and confirm every
    # transfer block returns exactly the coefficient rows from which it came.
    for lag, block in ordinary_transfer.items():
        falling = prefix.rr.falling(n, lag)
        recovered = ms(solve_matrix * block * falling**2)
        expected = sp.zeros(2, 2)
        Cn = ms(Cj[lag].subs(p, alpha + n - lag))
        expected[0, 0] = -Cn[pivot_row, 0]
        expected[0, 1] = -Cn[pivot_row, 1]
        if lag <= J - 1:
            Cnext = ms(Cj[lag + 1].subs(p, alpha + n - lag))
            projected = ms(ell.T * Cnext)
            expected[1, 0] = -projected[0, 0]
            expected[1, 1] = -projected[0, 1]
        if any(value != 0 for value in ms(recovered - expected)):
            raise AssertionError(f"ordinary normalized transfer reconstruction failed at lag {lag}")

    for lag, block in forcing_transfer.items():
        if lag == -1:
            undo = 1 / (n + 1) ** 2
        else:
            undo = prefix.rr.falling(n, lag) ** 2
        recovered = ms(solve_matrix * block * undo)
        expected = sp.zeros(2, 2)
        if 0 <= lag <= J:
            Cp = ms(Cj[lag].diff(p).subs(p, alpha + n - lag))
            expected[0, 0] = -Cp[pivot_row, 0]
            expected[0, 1] = -Cp[pivot_row, 1]
        if 0 <= lag + 1 <= J:
            Cpnext = ms(Cj[lag + 1].diff(p).subs(p, alpha + n - lag))
            projected = ms(ell.T * Cpnext)
            expected[1, 0] = -projected[0, 0]
            expected[1, 1] = -projected[0, 1]
        if any(value != 0 for value in ms(recovered - expected)):
            raise AssertionError(f"ordinary forcing transfer reconstruction failed at lag {lag}")

    return n, solve_det, ordinary_transfer, forcing_transfer


def main() -> None:
    # Bind this object to the already-certified finite prefix and its exact
    # generalized-Frobenius convention.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        prefix.main()
    prior = buffer.getvalue()
    required = [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_PREFIX_CERTIFIED",
        "EXACT_ORDINARY_PREFIX_END := 20",
        "FINITE_PREFIX_ONLY := True",
    ]
    for token in required:
        if token not in prior:
            raise AssertionError("ordinary-prefix dependency changed: " + token)

    n, solve_det, ordinary_transfer, forcing_transfer = build_normalized_transfer()

    ordinary_profiles = {
        lag: matrix_profile(block, n)
        for lag, block in ordinary_transfer.items()
    }
    forcing_profiles = {
        lag: matrix_profile(block, n)
        for lag, block in forcing_transfer.items()
    }
    ordinary_max_power = max(profile[0] for profile in ordinary_profiles.values())
    forcing_max_power = max(profile[0] for profile in forcing_profiles.values())

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_TRANSFER_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("NORMALIZED_ORDINARY_COORDINATE := O_n=vO_n/(n!)^2")
    print("NORMALIZED_TOP_LOG_COORDINATE := L_n=vL_n/(n!)^2")
    print("EXACT_TAIL_RECURRENCE := O_n=sum_(j=1..10) T_j(n)O_(n-j)+sum_(k=-1..10)F_k(n)L_(n-k)")
    print("TAIL_SOLVE_START := n >= 21")
    print(f"TAIL_SOLVE_DETERMINANT := {sp.sstr(solve_det)}")
    print("TAIL_SOLVE_NONVANISHING := exact shifted-polynomial sign certificate for every integer n>=21")
    for lag in sorted(ordinary_profiles):
        power, lead_rowsum = ordinary_profiles[lag]
        print(f"ORDINARY_TRANSFER_LAG_{lag}_INFINITY_POWER := {power}")
        print(f"ORDINARY_TRANSFER_LAG_{lag}_LEADING_ROWSUM := {sp.sstr(lead_rowsum)}")
    for lag in sorted(forcing_profiles):
        power, lead_rowsum = forcing_profiles[lag]
        label = "PLUS1" if lag == -1 else str(lag)
        print(f"TOP_LOG_FORCING_LAG_{label}_INFINITY_POWER := {power}")
        print(f"TOP_LOG_FORCING_LAG_{label}_LEADING_ROWSUM := {sp.sstr(lead_rowsum)}")
    print(f"ORDINARY_TRANSFER_GLOBAL_MAX_INFINITY_POWER := {ordinary_max_power}")
    print(f"TOP_LOG_FORCING_GLOBAL_MAX_INFINITY_POWER := {forcing_max_power}")
    print("TRANSFER_RECONSTRUCTION := every normalized transfer block inverts back to its exact coefficient-equation rows")
    print("NEXT_ROUTE := choose a polynomial-times-geometric invariant majorant from these exact tail powers, then certify a uniform ordinary Borel bound on 0<=z<=1/10")
    print("BOUNDARY := exact ordinary tail transfer only; no tail majorant, ordinary local uniform bound, numerical double-Laplace state, r=4096 enclosure, C_grow nonvanishing, or global exceptional-mode closure is claimed")


if __name__ == "__main__":
    main()
