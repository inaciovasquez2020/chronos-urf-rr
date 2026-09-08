#!/usr/bin/env python3
"""Certify an explicit local majorant for the canonical ordinary Borel companion.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The exact normalized ordinary transfer certificate gives, for n>=21,

  O_n = sum_(j=1..10) T_j(n) O_(n-j)
        + sum_(k=-1..10) F_k(n) L_(n-k),

where O_n and L_n are the physical two-vector coefficients after division by
(n!)^2.  The top-log invariant cone supplies a global geometric-times-linear
bound on L_n.  This verifier proves an invariant ordinary majorant

  ||O_n||_inf <= C_O (n+1)^5 (19/2)^n

for every n>=0.  The proof is split into two exact pieces:

* every finite induction step from n=21 to the certified tail start is checked
  by exact rational arithmetic;
* on the infinite tail, fixed signs and rational inequalities are certified by
  shifted-polynomial coefficient positivity, giving a uniform contraction for
  the homogeneous transfer and a geometric forcing reserve.

Since (19/2)*(1/10)=19/20<1, the resulting coefficient bound gives explicit
uniform bounds for the ordinary Borel vector and its first three Euler jets on
0<=z<=1/10.

This certificate does not numerically evaluate the two-fold Laplace startup
state, propagate the physical six-state to r=4096, or prove C_grow != 0.
"""
from __future__ import annotations

import contextlib
import io

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_transfer as transfer
import verify_gfe_corrected_exceptional_accumulation_borel_top_log_local_majorant as local


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ms(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def shifted_poly_sign(expr: sp.Expr, n: sp.Symbol, start: int) -> int:
    """Certify a strict polynomial sign on every integer n>=start."""
    m = sp.symbols("m", nonnegative=True)
    poly = sp.Poly(sp.expand(expr.subs(n, m + start)), m, domain=sp.QQ)
    coeffs = poly.all_coeffs()
    at_zero = poly.eval(0)
    if all(c >= 0 for c in coeffs) and at_zero > 0:
        return 1
    if all(c <= 0 for c in coeffs) and at_zero < 0:
        return -1
    return 0


def shifted_poly_nonnegative(expr: sp.Expr, n: sp.Symbol, start: int) -> bool:
    m = sp.symbols("m", nonnegative=True)
    poly = sp.Poly(sp.expand(expr.subs(n, m + start)), m, domain=sp.QQ)
    return all(c >= 0 for c in poly.all_coeffs())


def rational_sign(expr: sp.Expr, n: sp.Symbol, start: int) -> int:
    value = simp(expr)
    if value == 0:
        return 0
    num, den = sp.fraction(value)
    sn = shifted_poly_sign(num, n, start)
    sd = shifted_poly_sign(den, n, start)
    if sn == 0 or sd == 0:
        raise AssertionError(
            f"could not certify fixed rational sign on n>={start}: {sp.sstr(value)}"
        )
    return sn * sd


def rational_nonnegative(expr: sp.Expr, n: sp.Symbol, start: int) -> bool:
    value = simp(expr)
    if value == 0:
        return True
    num, den = sp.fraction(value)
    sd = shifted_poly_sign(den, n, start)
    if sd == 0:
        return False
    if sd > 0:
        return shifted_poly_nonnegative(num, n, start)
    return shifted_poly_nonnegative(-num, n, start)


def exact_matrix_inf_norm_at(matrix: sp.Matrix, n: sp.Symbol, index: int) -> sp.Rational:
    rows: list[sp.Rational] = []
    for i in range(matrix.rows):
        total = sp.Rational(0)
        for j in range(matrix.cols):
            value = simp(matrix[i, j].subs(n, index))
            if value.free_symbols:
                raise AssertionError("matrix evaluation retained symbolic parameters")
            total += abs(sp.Rational(value))
        rows.append(sp.Rational(total))
    return max(rows)


def tail_row_sums(matrix: sp.Matrix, n: sp.Symbol, start: int) -> list[sp.Expr]:
    rows: list[sp.Expr] = []
    for i in range(matrix.rows):
        total = sp.Integer(0)
        for j in range(matrix.cols):
            value = simp(matrix[i, j])
            sign = rational_sign(value, n, start)
            total += sign * value
        rows.append(simp(total))
    return rows


def certify_integer_row_bound(
    rows: list[sp.Expr],
    scale: sp.Expr,
    n: sp.Symbol,
    start: int,
    max_integer: int = 10000,
) -> sp.Integer:
    for candidate in range(1, max_integer + 1):
        bound = sp.Integer(candidate)
        if all(rational_nonnegative(bound * scale - row, n, start) for row in rows):
            return bound
    raise AssertionError(f"no integer row bound found through {max_integer}")


def top_log_global_constant() -> tuple[sp.Rational, dict[int, sp.Matrix]]:
    """Return C_L with ||L_n||_inf <= C_L (n+1) 5^n for all n>=0."""
    xi, kap = local.physical_prefix()
    vectors: dict[int, sp.Matrix] = {}
    finite_constants: list[sp.Rational] = []
    for index in range(61):
        moment = sp.factorial(index) ** 2
        Xi = sp.Rational(xi[index], moment)
        K = sp.Rational(kap[index], moment)
        vec = sp.Matrix([Xi + K, (4 * index + 2) * K])
        vectors[index] = vec
        norm = max(abs(sp.Rational(vec[0])), abs(sp.Rational(vec[1])))
        finite_constants.append(
            sp.Rational(norm, (index + 1) * 5**index)
        )

    K60 = abs(sp.Rational(kap[60], sp.factorial(60) ** 2))
    if K60 <= 0:
        raise AssertionError("top-log K_60 anchor vanished")
    # For n>=61, |Xi_n|<=|K_n|/n^3 and |K_n|<=K60*5^(n-60).
    # Hence the physical two-vector has infinity norm <=4(n+1)|K_n|.
    tail_constant = sp.Rational(4 * K60, 5**60)
    C_L = max(finite_constants + [tail_constant])
    if C_L <= 0:
        raise AssertionError("top-log global majorant constant is not positive")
    return sp.Rational(C_L), vectors


def top_log_vector_exact(index: int, vectors: dict[int, sp.Matrix]) -> sp.Matrix:
    if index < 0:
        return sp.zeros(2, 1)
    value = vectors.get(index)
    if value is None:
        raise AssertionError(f"exact top-log coefficient unavailable at n={index}")
    return value


def moment_sum_polynomial(power: int, q: sp.Rational) -> sp.Rational:
    """Exact sum sum_(n>=0) n^power q^n for 0<=q<1."""
    x = sp.symbols("x")
    value = 1 / (1 - x)
    for _ in range(power):
        value = simp(x * sp.diff(value, x))
    return sp.Rational(simp(value.subs(x, q)))


def main() -> None:
    # Bind to both previously certified ingredients.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        transfer.main()
    prior_transfer = buffer.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_TRANSFER_CERTIFIED",
        "TAIL_SOLVE_START := n >= 21",
        "ORDINARY_TRANSFER_GLOBAL_MAX_INFINITY_POWER := 0",
        "TOP_LOG_FORCING_GLOBAL_MAX_INFINITY_POWER := 4",
    ]:
        if token not in prior_transfer:
            raise AssertionError("ordinary-transfer dependency changed: " + token)

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        local.main()
    prior_local = buffer.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_TOP_LOG_LOCAL_MAJORANT_CERTIFIED",
        "LOCAL_MAJORANT_INTERVAL := 0 <= z <= 1/10",
        "BOREL_KERNEL_TAIL_STEP := |K_n| <= |K_60|*5^(n-60)",
        "BOREL_RANGE_TAIL_STEP := |Xi_n| <= |K_n|/n^3",
    ]:
        if token not in prior_local:
            raise AssertionError("top-log-majorant dependency changed: " + token)

    n, solve_det, ordinary_transfer, forcing_transfer = transfer.build_normalized_transfer()
    if simp(solve_det - sp.Rational(3125, 128) * n**3 * (n - 1) * (2 * n - 3)) != 0:
        raise AssertionError("ordinary tail solve determinant changed")

    A = sp.Rational(19, 2)
    P = 5
    zstar = sp.Rational(1, 10)
    q_endpoint = simp(A * zstar)
    if q_endpoint != sp.Rational(19, 20):
        raise AssertionError("ordinary endpoint geometric factor changed")

    C_L, exact_top_log = top_log_global_constant()

    # Reconstruct the exact canonical ordinary normalized prefix through n=20
    # directly from the certified transfer formula.  All required L_{n+1}
    # coefficients lie inside the exact top-log prefix.
    ordinary: dict[int, sp.Matrix] = {
        0: sp.Matrix([sp.Integer(1), sp.Integer(2)]),
        1: sp.Matrix([sp.Integer(0), sp.Rational(154, 45)]),
    }
    for index in range(2, 21):
        value = sp.zeros(2, 1)
        for lag, block in ordinary_transfer.items():
            prev = index - lag
            if prev >= 0:
                value += block.subs(n, index) * ordinary[prev]
        for lag, block in forcing_transfer.items():
            top_index = index - lag
            if top_index >= 0:
                value += block.subs(n, index) * top_log_vector_exact(top_index, exact_top_log)
        ordinary[index] = ms(value)

    if ordinary[0] != sp.Matrix([1, 2]) or ordinary[1] != sp.Matrix([0, sp.Rational(154, 45)]):
        raise AssertionError("canonical ordinary normalization changed")

    prefix_required = sp.Rational(0)
    for index in range(21):
        norm = max(abs(sp.Rational(ordinary[index][0])), abs(sp.Rational(ordinary[index][1])))
        required = sp.Rational(norm, A**index * (index + 1) ** P)
        prefix_required = max(prefix_required, required)

    def finite_homogeneous_ratio(index: int) -> sp.Rational:
        total = sp.Rational(0)
        for lag, block in ordinary_transfer.items():
            norm = exact_matrix_inf_norm_at(block, n, index)
            weight = sp.Rational(index - lag + 1, index + 1) ** P
            total += norm * weight / A**lag
        return sp.Rational(total)

    def finite_forcing_bound(index: int) -> sp.Rational:
        total = sp.Rational(0)
        for lag, block in forcing_transfer.items():
            top_index = index - lag
            if top_index < 0:
                continue
            norm = exact_matrix_inf_norm_at(block, n, index)
            total += norm * C_L * (top_index + 1) * 5**top_index
        return sp.Rational(total)

    # Find a tail where every transfer entry has fixed sign and simple integer
    # row bounds admit a strict homogeneous contraction.
    chosen_tail: int | None = None
    homogeneous_bounds: dict[int, sp.Integer] = {}
    forcing_bounds: dict[int, sp.Integer] = {}
    H_tail = sp.Rational(0)
    for candidate_tail in [64, 128, 256, 512, 1024, 2048]:
        try:
            hb: dict[int, sp.Integer] = {}
            fb: dict[int, sp.Integer] = {}
            for lag, block in ordinary_transfer.items():
                rows = tail_row_sums(block, n, candidate_tail)
                hb[lag] = certify_integer_row_bound(rows, sp.Integer(1), n, candidate_tail)
            for lag, block in forcing_transfer.items():
                rows = tail_row_sums(block, n, candidate_tail)
                fb[lag] = certify_integer_row_bound(rows, (n + 1) ** 4, n, candidate_tail)
            h = sum(sp.Rational(hb[lag], 1) / A**lag for lag in hb)
            h = sp.Rational(simp(h))
            if h < 1:
                chosen_tail = candidate_tail
                homogeneous_bounds = hb
                forcing_bounds = fb
                H_tail = h
                break
        except AssertionError:
            continue
    if chosen_tail is None:
        raise AssertionError("failed to certify an infinite-tail ordinary majorant zone")

    # Every finite induction step is checked exactly.  The global top-log
    # majorant is used, so no unproved top-log coefficients enter this check.
    finite_step_required = sp.Rational(0)
    finite_h_max = sp.Rational(0)
    for index in range(21, chosen_tail):
        h = finite_homogeneous_ratio(index)
        finite_h_max = max(finite_h_max, h)
        if not h < 1:
            raise AssertionError(
                f"ordinary majorant homogeneous contraction failed at n={index}: {sp.sstr(h)}"
            )
        forcing = finite_forcing_bound(index)
        required = sp.Rational(
            forcing,
            (1 - h) * A**index * (index + 1) ** P,
        )
        finite_step_required = max(finite_step_required, required)

    # Infinite-tail forcing reserve.  The forcing matrices satisfy
    # ||F_k(n)|| <= D_k (n+1)^4.  Also n-k+1 <= n+2 for k>=-1 and
    # (n+2)/(n+1) decreases with n.
    forcing_weight_sum = sp.Rational(0)
    for lag, bound in forcing_bounds.items():
        forcing_weight_sum += sp.Rational(bound) * sp.Rational(5) ** (-lag)
    forcing_weight_sum = sp.Rational(simp(forcing_weight_sum))
    linear_ratio = sp.Rational(chosen_tail + 2, chosen_tail + 1)
    tail_required = sp.Rational(
        C_L
        * linear_ratio
        * forcing_weight_sum
        * (sp.Rational(5, 1) / A) ** chosen_tail,
        1 - H_tail,
    )

    C_O = 2 * max(prefix_required, finite_step_required, tail_required)
    C_O = sp.Rational(C_O)
    if C_O <= 0:
        raise AssertionError("ordinary majorant constant is not positive")

    # Recheck all finite induction inequalities with the final constant.
    for index in range(21, chosen_tail):
        h = finite_homogeneous_ratio(index)
        forcing = finite_forcing_bound(index)
        lhs = h + sp.Rational(forcing, C_O * A**index * (index + 1) ** P)
        if not lhs <= 1:
            raise AssertionError(
                f"final ordinary induction inequality failed at n={index}: {sp.sstr(lhs)}"
            )

    tail_forcing_fraction = sp.Rational(
        C_L
        * linear_ratio
        * forcing_weight_sum
        * (sp.Rational(5, 1) / A) ** chosen_tail,
        C_O,
    )
    if not H_tail + tail_forcing_fraction <= 1:
        raise AssertionError("infinite-tail ordinary induction reserve is insufficient")

    # Explicit endpoint bounds for theta^j O(z), j=0,1,2,3.  Expand
    # n^j(n+1)^5 and evaluate the geometric moments exactly at q=19/20.
    m = sp.symbols("m")
    jet_bounds: list[sp.Rational] = []
    for jet in range(4):
        poly = sp.Poly(sp.expand(m**jet * (m + 1) ** P), m, domain=sp.QQ)
        total = sp.Rational(0)
        for (degree,), coeff in poly.terms():
            total += sp.Rational(coeff) * moment_sum_polynomial(degree, q_endpoint)
        bound = sp.Rational(C_O * total)
        if bound <= 0:
            raise AssertionError("ordinary endpoint jet bound is not positive")
        jet_bounds.append(bound)

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_LOCAL_MAJORANT_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("NORMALIZED_ORDINARY_PHYSICAL_VECTOR := O_n=vO_n/(n!)^2")
    print("NORMALIZED_TOP_LOG_PHYSICAL_VECTOR := L_n=vL_n/(n!)^2")
    print(f"TOP_LOG_GLOBAL_MAJORANT_CONSTANT := {sp.sstr(C_L)}")
    print("TOP_LOG_GLOBAL_MAJORANT := ||L_n||_inf <= C_L*(n+1)*5^n for every n>=0")
    print("ORDINARY_MAJORANT_BASE := 19/2")
    print("ORDINARY_MAJORANT_POLYNOMIAL_POWER := 5")
    print(f"ORDINARY_MAJORANT_CONSTANT := {sp.sstr(C_O)}")
    print("ORDINARY_COEFFICIENT_MAJORANT := ||O_n||_inf <= C_O*(n+1)^5*(19/2)^n for every n>=0")
    print(f"FINITE_INDUCTION_END := {chosen_tail - 1}")
    print(f"FINITE_HOMOGENEOUS_RATIO_MAX := {sp.sstr(finite_h_max)}")
    print(f"TAIL_START := n >= {chosen_tail}")
    for lag in sorted(homogeneous_bounds):
        print(f"TAIL_HOMOGENEOUS_LAG_{lag}_ROW_BOUND := {homogeneous_bounds[lag]}")
    for lag in sorted(forcing_bounds):
        label = "PLUS1" if lag == -1 else str(lag)
        print(f"TAIL_FORCING_LAG_{label}_N4_ROW_BOUND := {forcing_bounds[lag]}")
    print(f"TAIL_HOMOGENEOUS_CONTRACTION := {sp.sstr(H_tail)} < 1")
    print(f"TAIL_FORCING_FRACTION := {sp.sstr(tail_forcing_fraction)}")
    print("TAIL_INDUCTION := exact shifted-polynomial sign/bound certificates plus geometric forcing reserve")
    print("ORDINARY_BOREL_RADIUS_LOWER_BOUND := 2/19")
    print("LOCAL_MAJORANT_INTERVAL := 0 <= z <= 1/10")
    print("ENDPOINT_GEOMETRIC_FACTOR := (19/2)*(1/10)=19/20 < 1")
    for jet, bound in enumerate(jet_bounds):
        print(f"THETA_JET_{jet}_ORDINARY_VECTOR_UNIFORM_BOUND := {sp.sstr(bound)}")
    print("UNIFORMITY := coefficientwise absolute majorization on the full real interval 0<=z<=1/10")
    print("NEXT_ROUTE := combine top-log and ordinary local bounds to enclose a finite-x two-fold Laplace startup state, then validate forward propagation toward r=4096")
    print("BOUNDARY := ordinary local Borel majorant only; no numerical double-Laplace startup state, r=4096 physical-state enclosure, C_grow value/nonvanishing, or global exceptional-mode closure is claimed")


if __name__ == "__main__":
    main()
