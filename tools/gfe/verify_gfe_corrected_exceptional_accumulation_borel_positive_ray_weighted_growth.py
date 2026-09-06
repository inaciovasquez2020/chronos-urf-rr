#!/usr/bin/env python3
"""Certify a direct exp(B*sqrt(t)) growth bound on the physical positive Borel ray.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

Dependencies already certified earlier in CI:
* the physical Borel germ continues uniquely along every finite t>=0;
* the constrained 44-state ordinary system Y'=A(t)Y is exact on t>0;
* its only nonzero finite denominator point is -5/18.

The raw jet system has entries growing as high as t^8, but that is a coordinate
artifact.  We use the diagonal jet scaling

    Y_i = t^{w_i} Z_i,
    w(Xi_k)=k/2,
    w(K_k)=k/2+d,

and determine an exact rational interval of offsets d for which every entry of

    Z' = [D^{-1} A D - D^{-1}D'] Z

is O(t^{-1/2}) on t>=1.  For a certified midpoint d we then bound every entry
explicitly.  After t=s^2, each quantity s*B_ij(s^2) is rational in s; all of
its denominator factors are required to be among s and 18*s^2+5.  A coefficient
L1 bound on the numerator and the exact inequality 18*s^2+5>=18*s^2 (s>=1)
give a finite rational row-sum constant C_*.

Gronwall then yields

    ||Z(t)||_inf <= ||Z(1)||_inf exp(2 C_* (sqrt(t)-1)),

hence the physical 44-state satisfies a polynomial times exp(B*sqrt(t)) bound
with B=2 C_*.  This is a genuine solution-growth certificate, not a WKB
existence claim.  It does not yet perform the order-2 Laplace reconstruction.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_origin_removability as origin
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def rational_power_at_infinity(expr: sp.Expr, z: sp.Symbol) -> int:
    expr = rr.simp(expr)
    if rr.is_zero_expr(expr):
        return -10**9
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    return int(sp.Poly(num, z, domain="QQ").degree() - sp.Poly(den, z, domain="QQ").degree())


def weight(index: int, d: sp.Rational) -> sp.Rational:
    if index < 22:
        return sp.Rational(index, 2)
    return sp.Rational(index - 22, 2) + d


def bound_rational_on_s_ge_1(expr: sp.Expr, s: sp.Symbol) -> sp.Rational:
    """Return C with |expr(s)|<=C for real s>=1, using exact factor support."""
    expr = sp.factor(sp.cancel(sp.together(expr)))
    if expr == 0:
        return sp.Rational(0)
    num, den = sp.fraction(expr)
    pnum = sp.Poly(sp.expand(num), s, domain="QQ")
    pden = sp.Poly(sp.expand(den), s, domain="QQ")
    if pnum.degree() > pden.degree():
        raise AssertionError(
            f"scaled coefficient still grows: deg(num)={pnum.degree()} deg(den)={pden.degree()} expr={sp.sstr(expr)}"
        )

    coeff, factors = sp.factor_list(pden.as_expr(), s)
    s_power = 0
    quad_power = 0
    for fac, exponent in factors:
        fac_poly = sp.Poly(fac, s, domain="QQ").monic()
        if fac_poly == sp.Poly(s, s, domain="QQ").monic():
            s_power += int(exponent)
        elif fac_poly == sp.Poly(18 * s**2 + 5, s, domain="QQ").monic():
            quad_power += int(exponent)
        else:
            raise AssertionError(
                "unexpected scaled positive-ray denominator factor: " + sp.sstr(fac)
            )

    expected_degree = s_power + 2 * quad_power
    if expected_degree != pden.degree():
        raise AssertionError("denominator degree/factor accounting changed")

    # factor_list extracts a rational constant coeff.  Since s>=1 and
    # 18*s^2+5 >= 18*s^2, |den| >= |coeff|*18^q*s^degree.
    lower_lead = abs(sp.Rational(coeff)) * sp.Integer(18) ** quad_power
    if lower_lead <= 0:
        raise AssertionError("positive-ray denominator lower bound vanished")
    numerator_l1 = sum(abs(sp.Rational(c)) for c in pnum.all_coeffs())
    return sp.factor(numerator_l1 / lower_lead)


def main() -> None:
    z, top_u, top_v, constraint = origin.build_top_rules()
    if len(top_u) != 44 or len(top_v) != 44 or len(constraint) != 44:
        raise AssertionError("44-state first-order data changed")

    # Ordinary system nonzero entries.  Chain rows are Y_i'=Y_{i+1}/z.
    entries: list[tuple[int, int, sp.Expr]] = []
    for k in range(21):
        entries.append((k, k + 1, sp.Integer(1) / z))
        entries.append((22 + k, 22 + k + 1, sp.Integer(1) / z))
    for j, value in enumerate(top_u):
        value = rr.simp(value / z)
        if not rr.is_zero_expr(value):
            entries.append((21, j, value))
    for j, value in enumerate(top_v):
        value = rr.simp(value / z)
        if not rr.is_zero_expr(value):
            entries.append((43, j, value))

    # With jet slope q=1/2, only cross-block top-row entries constrain d.
    lower: sp.Rational | None = None
    upper: sp.Rational | None = None
    worst_same_block = -sp.oo
    for i, j, value in entries:
        p = rational_power_at_infinity(value, z)
        if p < -10**8:
            continue
        if i == 43 and j < 22:
            k = j
            candidate = sp.Rational(p) + sp.Rational(k, 2) - 10
            lower = candidate if lower is None else max(lower, candidate)
        elif i == 21 and j >= 22:
            k = j - 22
            candidate = 10 - sp.Rational(p) - sp.Rational(k, 2)
            upper = candidate if upper is None else min(upper, candidate)
        else:
            # d cancels from same-block entries and all chain equations.
            exponent = sp.Rational(p) + weight(j, sp.Rational(0)) - weight(i, sp.Rational(0))
            if i >= 22 and j >= 22:
                exponent = sp.Rational(p) + sp.Rational(j - i, 2)
            worst_same_block = max(worst_same_block, exponent)

    if lower is None or upper is None:
        raise AssertionError("cross-block weight constraints disappeared")
    if lower > upper:
        raise AssertionError(f"no half-jet weighted-growth offset exists: [{lower},{upper}]")
    if worst_same_block > -sp.Rational(1, 2):
        raise AssertionError(f"same-block weighted exponent exceeds -1/2: {worst_same_block}")

    d = sp.factor((lower + upper) / 2)

    # Verify every transformed off-diagonal system entry has power <= -1/2.
    worst = -sp.oo
    for i, j, value in entries:
        p = rational_power_at_infinity(value, z)
        exponent = sp.Rational(p) + weight(j, d) - weight(i, d)
        worst = max(worst, exponent)
        if exponent > -sp.Rational(1, 2):
            raise AssertionError(
                f"weighted infinity exponent failed at ({i},{j}): p={p}, exponent={exponent}, d={d}"
            )

    # Turn the asymptotic exponent statement into a global exact t>=1 bound.
    # Put t=s^2.  Multiplying each transformed coefficient by s should leave a
    # bounded rational function on s>=1.  Include the diagonal scaling term
    # -w_i/t separately.
    s = sp.symbols("s", positive=True)
    row_bounds = [sp.Rational(0) for _ in range(44)]
    entry_bound_count = 0
    for i, j, value in entries:
        power_s = int(2 * (weight(j, d) - weight(i, d)))
        scaled = sp.factor(
            sp.cancel(
                sp.together(
                    s * s**power_s * value.subs(z, s**2)
                )
            )
        )
        Cij = bound_rational_on_s_ge_1(scaled, s)
        row_bounds[i] += Cij
        entry_bound_count += 1

    # D^{-1}D' contributes -w_i/t on the diagonal.  For t=s^2 and s>=1,
    # s*|w_i|/s^2 <= |w_i|.
    for i in range(44):
        row_bounds[i] += abs(weight(i, d))

    Cstar = max(row_bounds)
    if not isinstance(Cstar, sp.Rational):
        Cstar = sp.Rational(Cstar)
    if Cstar <= 0:
        raise AssertionError("weighted row-sum constant is nonpositive")
    B = sp.factor(2 * Cstar)
    max_weight = max(weight(i, d) for i in range(44))
    min_weight = min(weight(i, d) for i in range(44))

    # Exact integral behind Gronwall.
    t = sp.symbols("t", positive=True)
    if sp.integrate(t ** (-sp.Rational(1, 2)), (t, 1, t)) != 2 * sp.sqrt(t) - 2:
        raise AssertionError("sqrt-growth Gronwall integral identity changed")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_POSITIVE_RAY_WEIGHTED_GROWTH_CERTIFIED")
    print("STATE_SCALING := Y_i=t^(w_i) Z_i with w(Xi_k)=k/2 and w(K_k)=k/2+d")
    print(f"CROSS_BLOCK_OFFSET_INTERVAL := [{sp.sstr(lower)},{sp.sstr(upper)}]")
    print(f"CERTIFIED_OFFSET_D := {sp.sstr(d)}")
    print(f"WORST_WEIGHTED_RATIONAL_POWER_AT_INFINITY := {sp.sstr(worst)}")
    print("WEIGHTED_MATRIX_DECAY := every transformed off-diagonal entry is O(t^(-1/2))")
    print(f"EXACT_ENTRY_BOUNDS_CERTIFIED := {entry_bound_count}")
    print(f"WEIGHT_RANGE := [{sp.sstr(min_weight)},{sp.sstr(max_weight)}]")
    print(f"WEIGHTED_INFINITY_ROW_SUM_CONSTANT_CSTAR := {sp.sstr(Cstar)}")
    print(f"PHYSICAL_POSITIVE_RAY_EXP_SQRT_CONSTANT_B := {sp.sstr(B)}")
    print("WEIGHTED_GROWTH_THEOREM := ||Z(t)||_inf <= ||Z(1)||_inf*exp(2*CSTAR*(sqrt(t)-1)) for t>=1")
    print("PHYSICAL_STATE_GROWTH := ||Y(t)||_inf <= C*t^W*exp(B*sqrt(t)) for finite C and W=max_i w_i")
    print("BOUNDARY := direct positive-ray exp(B*sqrt(t)) growth bound certified; order-2 double-Laplace convergence and reconstruction not yet certified")


if __name__ == "__main__":
    main()
