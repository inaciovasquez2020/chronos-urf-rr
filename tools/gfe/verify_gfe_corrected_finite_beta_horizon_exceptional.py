#!/usr/bin/env python3
"""Re-derive the exceptional omega=i/(4M), ell=2 horizon recurrence
from the corrected AEH=1/2 Euler artifact.

Historical exceptional-frequency certificates are not imported as proofs here:
the corrected finite-beta descriptor has a finite-radius rank-loss surface, so
source binding must be re-established directly.  This verifier constructs the
row-scaled Frobenius blocks from
artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json and checks the
exceptional logarithmic recurrence against exact formulas.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_finite_beta_horizon_indicial as base


def simp(z: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(z)))


def matrix_simp(A: sp.Matrix) -> sp.Matrix:
    return A.applyfunc(simp)


def laurent_coeff(expr: sp.Expr, x: sp.Symbol, power: int) -> sp.Expr:
    return simp(sp.residue(sp.together(expr / x ** (power + 1)), x, 0))


def solve_linear_scalar_equation(residual: sp.Matrix, scalar: sp.Symbol) -> sp.Expr:
    """Solve an exact vector equation affine-linear in one scalar and verify it."""
    candidate = None
    for entry in residual:
        coefficient = simp(sp.diff(entry, scalar))
        constant = simp(entry.subs(scalar, 0))
        if coefficient == 0:
            if constant != 0:
                raise AssertionError(
                    "scalar correction cannot cancel a scalar-independent residual; "
                    f"entry={sp.sstr(entry)}"
                )
            continue
        current = simp(-constant / coefficient)
        if candidate is None:
            candidate = current
        elif simp(candidate - current) != 0:
            raise AssertionError(
                "Euler rows demand inconsistent scalar corrections; "
                f"first={sp.sstr(candidate)}, current={sp.sstr(current)}"
            )
    if candidate is None:
        raise AssertionError("scalar correction equation contained no determining row")
    verified = matrix_simp(residual.subs(scalar, candidate))
    if not base._is_zero_matrix(verified):
        raise AssertionError(
            "derived scalar correction does not cancel full vector residual; "
            f"candidate={sp.sstr(candidate)}, residual={verified.tolist()}"
        )
    return candidate


def solve_affine_scalar_expression(expr: sp.Expr, scalar: sp.Symbol) -> sp.Expr:
    """Solve an exact affine scalar equation expr=0 for scalar and verify it."""
    coefficient = simp(sp.diff(expr, scalar))
    if coefficient == 0:
        raise AssertionError(
            "ordinary compatibility does not determine the selected scalar; "
            f"expr={sp.sstr(expr)}"
        )
    constant = simp(expr.subs(scalar, 0))
    candidate = simp(-constant / coefficient)
    if simp(expr.subs(scalar, candidate)) != 0:
        raise AssertionError(
            "derived affine scalar relation does not cancel compatibility; "
            f"candidate={sp.sstr(candidate)}"
        )
    return candidate


def main() -> None:
    equations, h = base._parse_equations()

    M = base.M
    beta = base.beta
    lam = base.lam
    omega = base.omega
    r = base.r
    I = base.I

    x = sp.symbols("x", positive=True)
    p = base.p
    n = sp.symbols("n", integer=True, positive=True)
    a, b = sp.symbols("a b")

    trial = {}
    for order in range(5):
        trial[h[0][order]] = a * base._falling(p, order) / x**order
        trial[h[1][order]] = b * base._falling(p - 1, order) / x ** (order + 1)

    specialized = []
    for equation in equations:
        q = equation.xreplace(trial)
        q = q.subs({r: 2 * M + x, omega: I / (4 * M), lam: 6})
        specialized.append(simp(q))

    q0, q1 = specialized

    def block(lag: int) -> sp.Matrix:
        row0 = laurent_coeff(q0, x, -3 + lag)
        row1 = laurent_coeff(q1, x, -2 + lag)
        return matrix_simp(
            sp.Matrix(
                [
                    [sp.diff(row0, a), sp.diff(row0, b)],
                    [sp.diff(row1, a), sp.diff(row1, b)],
                ]
            )
        )

    B0 = block(0)
    B1 = block(1)
    B2 = block(2)

    alpha = sp.Rational(1, 2)
    pn = alpha + n
    A = matrix_simp(B0.subs(p, pn))

    corrected_prefactor = beta * (5 * M**2 + beta)
    expected_A = sp.Matrix(
        [
            [
                -corrected_prefactor * n * (n - 1) * (2 * n - 3) * (2 * n + 1) / (8 * M**3),
                corrected_prefactor * n * (n - 1) * (2 * n - 3) / (16 * M**4),
            ],
            [
                corrected_prefactor * n * (n - 1) * (2 * n + 1) / (16 * M**4),
                -corrected_prefactor * n * (n - 1) / (32 * M**5),
            ],
        ]
    )
    if not base._is_zero_matrix(matrix_simp(A - expected_A)):
        raise AssertionError(
            "corrected exceptional leading block changed after normalization repair; "
            f"actual={A.tolist()}"
        )

    r_n = sp.Matrix([1, 2 * M * (2 * n + 1)])
    l_n = sp.Matrix([1, 2 * M * (2 * n - 3)])
    r_prev = sp.Matrix([1, 2 * M * (2 * n - 1)])
    if not base._is_zero_matrix(matrix_simp(A * r_n)):
        raise AssertionError("corrected exceptional right kernel changed")
    if not base._is_zero_matrix(matrix_simp(l_n.T * A)):
        raise AssertionError("corrected exceptional left projector changed")

    adjacent = matrix_simp(B1.subs(p, alpha + n - 1))
    gamma = simp((l_n.T * adjacent * r_prev)[0])
    expected_gamma = simp(
        -2
        * beta
        * (n - 1) ** 2
        * (6 * (5 * M**2 - 2 * beta) * n * (n - 2) + 5 * beta)
        / (3 * M**4)
    )
    if simp(gamma - expected_gamma) != 0:
        raise AssertionError(
            "corrected exceptional adjacent kernel coupling changed after exact repair; "
            f"actual={sp.sstr(gamma)}"
        )

    D_nn = matrix_simp(B0.diff(p).subs(p, pn))
    if simp((l_n.T * D_nn * r_n)[0]) != 0:
        raise AssertionError("corrected exceptional log-kernel decoupling changed")

    p0 = alpha
    p1 = alpha + 1
    p2 = alpha + 2
    B0_p0 = matrix_simp(B0.subs(p, p0))
    B0_p1 = matrix_simp(B0.subs(p, p1))
    B0_p2 = matrix_simp(B0.subs(p, p2))
    if not base._is_zero_matrix(B0_p0) or not base._is_zero_matrix(B0_p1):
        raise AssertionError("corrected exceptional double resonance changed")
    if simp(B0_p2.det()) != 0 or B0_p2.rank() != 1:
        raise AssertionError("corrected exceptional n=2 rank-one block changed")

    u0 = sp.Matrix([1, 2 * M])
    c1_symbol = sp.symbols("c1")
    v1_symbol = c1_symbol * sp.Matrix([1, -2 * M])
    order1_symbolic = matrix_simp(
        B1.subs(p, p0) * u0 + B0.diff(p).subs(p, p1) * v1_symbol
    )
    c1 = solve_linear_scalar_equation(order1_symbolic, c1_symbol)
    v1 = matrix_simp(v1_symbol.subs(c1_symbol, c1))

    l2 = sp.Matrix([1, 2 * M])
    log2_source = matrix_simp(B1.subs(p, p1) * v1)
    if simp((l2.T * log2_source)[0]) != 0:
        raise AssertionError("exceptional order-two log compatibility failed")

    # Fix the n=2 logarithmic kernel freedom by choosing a particular solution
    # with vanishing second component, then solve its first component exactly.
    d2_symbol = sp.symbols("d2")
    v2_symbol = sp.Matrix([d2_symbol, 0])
    log2_symbolic = matrix_simp(B0_p2 * v2_symbol + log2_source)
    d2 = solve_linear_scalar_equation(log2_symbolic, d2_symbol)
    v2_part = matrix_simp(v2_symbol.subs(d2_symbol, d2))
    log2_residual = matrix_simp(log2_symbolic.subs(d2_symbol, d2))
    if not base._is_zero_matrix(log2_residual):
        raise AssertionError("derived exceptional n=2 logarithmic coefficient lost cancellation")

    # The ordinary n=1 coefficient u1 is genuinely two-component free because
    # B0(p1)=0.  Do not import the historical affine relation.  Instead derive
    # the unique n=2 compatibility relation directly from the corrected source.
    a1, b1 = sp.symbols("a1 b1")
    u1_symbolic = sp.Matrix([a1, b1])
    nonlog2_source_symbolic = matrix_simp(
        B1.subs(p, p1) * u1_symbolic
        + B2.subs(p, p0) * u0
        + B0.diff(p).subs(p, p2) * v2_part
        + B1.diff(p).subs(p, p1) * v1
    )
    ordinary_n2_pairing_symbolic = simp((l2.T * nonlog2_source_symbolic)[0])
    b1_relation = solve_affine_scalar_expression(ordinary_n2_pairing_symbolic, b1)
    u1 = matrix_simp(u1_symbolic.subs(b1, b1_relation))
    nonlog2_source = matrix_simp(nonlog2_source_symbolic.subs(b1, b1_relation))
    ordinary_n2_pairing = simp((l2.T * nonlog2_source)[0])
    if ordinary_n2_pairing != 0:
        raise AssertionError(
            "derived corrected ordinary n=2 compatibility relation failed; "
            f"b1={sp.sstr(b1_relation)}, pairing={sp.sstr(ordinary_n2_pairing)}"
        )

    compatibility_det = simp(gamma**2)

    print("GFE_CORRECTED_FINITE_BETA_EXCEPTIONAL_HORIZON_RECURRENCE_AUDIT")
    print("SOURCE := artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json")
    print("SECTOR := ell=2; lambda=6; omega=I/(4*M); alpha=1/2")
    print("CORRECTED_LEADING_PREFACTOR := beta*(5*M^2+beta)")
    print("NORMALIZED_LEADING_SEED := [1, 2*M]")
    print("CORRECTED_FIRST_LOG_SCALAR := " + sp.sstr(c1))
    print("CORRECTED_FIRST_LOG_VECTOR := [" + ", ".join(sp.sstr(v) for v in v1) + "]")
    print("CORRECTED_N2_LOG_PARTICULAR := [" + ", ".join(sp.sstr(v) for v in v2_part) + "]")
    print("CORRECTED_N2_ORDINARY_RELATION := b1 = " + sp.sstr(b1_relation))
    print("CORRECTED_N2_ORDINARY_VECTOR := [" + ", ".join(sp.sstr(v) for v in u1) + "]")
    print("ORDER_N_RIGHT_KERNEL := [1, 2*M*(2*n+1)]")
    print("ORDER_N_LEFT_PROJECTOR := [1, 2*M*(2*n-3)]")
    print("ADJACENT_KERNEL_COUPLING := " + sp.sstr(gamma))
    print("LOG_KERNEL_DECOUPLING := 0")
    print("COMPATIBILITY_DETERMINANT := " + sp.sstr(compatibility_det))
    print("BOUNDARY := corrected coupling nonvanishing domain and all-order recurrence remain open")
    print("FORMAL_EXCEPTIONAL_LOG_FROBENIUS := verified through total order n=2 only")
    print("NEXT_ROUTE := classify the corrected adjacent-kernel coupling zeros for n>=2")


if __name__ == "__main__":
    main()
