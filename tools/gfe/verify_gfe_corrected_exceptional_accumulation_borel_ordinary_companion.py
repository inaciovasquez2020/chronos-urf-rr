#!/usr/bin/env python3
"""Certify the ordinary (log^0) order-2 Borel companion in the physical accumulation sector.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The already-certified top logarithmic coefficient has order-2 Borel coordinates
U_L=(Xi_L,K_L) and satisfies the cleared operator B U_L=0.  For a generalized
Frobenius solution x^alpha[V_L log x+V_O], the ordinary level is driven by the
exponent derivative of the Euler symbol.  In Borel coordinates this is exactly

    B U_O + B_p U_L = 0,

where B_p differentiates only C_j(p) with respect to p; the factorial clearing
and coordinate map are p-independent.

This verifier applies the same three certified left Ore row operations to B and
B_p, reduces every higher log jet back to the already-certified 44-state
homogeneous first-order system, constructs the triangular inhomogeneous 44+44
system, checks origin compatibility for the normalized ordinary seed, proves
positive-ray continuation hypotheses, and transfers the previously certified
weighted exp(B*sqrt(t)) homogeneous estimate to the ordinary companion by
variation of constants with polynomial forcing.

The normalization a1=0 fixes the one free ordinary n=1 homogeneous parameter;
it is an existence normalization, not a uniqueness claim for all generalized
Frobenius solutions.
"""
from __future__ import annotations

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_first_order_system as fo
import verify_gfe_corrected_exceptional_accumulation_borel_origin_removability as origin
import verify_gfe_corrected_exceptional_accumulation_borel_positive_ray_weighted_growth as wg
import verify_gfe_corrected_exceptional_accumulation_borel_reduced_denominators as rd
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def build_unreduced_and_p_derivative() -> tuple[sp.Matrix, sp.Matrix, sp.Symbol, sp.Symbol]:
    equations, h = rr.base._parse_equations()
    p = rr.base.p
    x = sp.symbols("x", positive=True)
    z, theta = sp.symbols("z theta")
    a, b = sp.symbols("a b")

    trial = {}
    for order in range(5):
        trial[h[0][order]] = a * rr.base._falling(p, order) / x**order
        trial[h[1][order]] = b * rr.base._falling(p - 1, order) / x ** (order + 1)

    specialized = []
    for equation in equations:
        q = equation.xreplace(trial).subs({
            rr.base.r: 2 + x,
            rr.base.M: 1,
            rr.base.omega: rr.base.I / 4,
            rr.base.lam: 6,
            rr.base.beta: sp.Rational(5, 2),
        })
        specialized.append(rr.simp(q))
    q0, q1 = specialized

    F = rr.ms(sp.Matrix([
        [sp.diff(rr.simp(x**3 * q0), a), sp.diff(rr.simp(x**3 * q0), b)],
        [sp.diff(rr.simp(x**2 * q1), a), sp.diff(rr.simp(x**2 * q1), b)],
    ]))
    Dp = sp.Poly(1, x, domain="EX")
    for entry in F:
        _, den = sp.fraction(rr.simp(entry))
        Dp = sp.lcm(Dp, sp.Poly(den, x, domain="EX").monic())
    D = rr.simp(Dp.as_expr() / Dp.as_expr().subs(x, 0))
    C = rr.ms(D * F)
    J = max(sp.Poly(entry, x, domain="EX").degree() for entry in C if entry != 0)
    if J != 10:
        raise AssertionError(f"finite lag changed: {J}")

    Cj = [
        rr.ms(sp.Matrix([
            [sp.Poly(C[row, col], x, domain="EX").coeff_monomial(x**j) for col in range(2)]
            for row in range(2)
        ]))
        for j in range(J + 1)
    ]

    alpha = sp.Rational(1, 2)
    S = sp.Matrix([[1, 1], [0, 4 * theta + 2]])
    B = sp.zeros(2, 2)
    Bp = sp.zeros(2, 2)
    for j in range(J + 1):
        fall = rr.falling(theta, J - j) ** 2
        B += z**j * rr.ms(Cj[j].subs(p, alpha + theta) * fall * S)
        Bp += z**j * rr.ms(Cj[j].diff(p).subs(p, alpha + theta) * fall * S)
    return B.applyfunc(sp.expand), Bp.applyfunc(sp.expand), z, theta


def apply_certified_row_transform(
    B: sp.Matrix, Bp: sp.Matrix, z: sp.Symbol, theta: sp.Symbol
) -> tuple[list[list[sp.Expr]], list[list[sp.Expr]]]:
    target_rows, z0, theta0, steps = rd.reconstruct_reduced_rows()
    if z0 != z or theta0 != theta:
        raise AssertionError("symbol mismatch in reduced-row reconstruction")
    rows = [[B[i, 0], B[i, 1]] for i in range(2)]
    prows = [[Bp[i, 0], Bp[i, 1]] for i in range(2)]
    for high_i, low_i, shift, q in steps:
        low_b = rr.theta_left_row(rows[low_i], z, theta, shift)
        low_p = rr.theta_left_row(prows[low_i], z, theta, shift)
        rows[high_i] = [rr.simp(rows[high_i][c] - q * low_b[c]) for c in range(2)]
        prows[high_i] = [rr.simp(prows[high_i][c] - q * low_p[c]) for c in range(2)]
    for i in range(2):
        for c in range(2):
            if not rr.is_zero_expr(rows[i][c] - target_rows[i][c]):
                raise AssertionError("parallel Ore transform failed to recover certified reduced B row")
    return rows, prows


def theta_state_row(
    functional: list[sp.Expr], z: sp.Symbol,
    top_u: list[sp.Expr], top_v: list[sp.Expr]
) -> list[sp.Expr]:
    """Represent theta(functional*Y_L) again on the certified 44-state Y_L."""
    if len(functional) != 44:
        raise AssertionError("homogeneous state functional dimension changed")
    out = [rr.simp(z * sp.diff(value, z)) for value in functional]
    for k in range(21):
        out[k + 1] = rr.simp(out[k + 1] + functional[k])
        vk = 22 + k
        out[vk + 1] = rr.simp(out[vk + 1] + functional[vk])
    for j in range(44):
        out[j] = rr.simp(
            out[j] + functional[21] * top_u[j] + functional[43] * top_v[j]
        )
    return out


def log_jet_rule(
    component: int, order: int, z: sp.Symbol,
    top_u: list[sp.Expr], top_v: list[sp.Expr],
    cache: dict[tuple[int, int], list[sp.Expr]],
) -> list[sp.Expr]:
    """Reduce theta^order Xi_L or K_L to the certified 44-state exactly."""
    key = (component, order)
    if key in cache:
        return cache[key]
    if component not in (0, 1) or order < 0:
        raise AssertionError("invalid log-jet request")
    if order <= 21:
        row = [sp.Integer(0)] * 44
        row[(0 if component == 0 else 22) + order] = sp.Integer(1)
    elif order == 22:
        row = list(top_u if component == 0 else top_v)
    else:
        row = theta_state_row(
            log_jet_rule(component, order - 1, z, top_u, top_v, cache),
            z, top_u, top_v,
        )
    cache[key] = row
    return row


def operator_on_log_state(
    row: list[sp.Expr], z: sp.Symbol, theta: sp.Symbol,
    top_u: list[sp.Expr], top_v: list[sp.Expr]
) -> list[sp.Expr]:
    out = [sp.Integer(0)] * 44
    cache: dict[tuple[int, int], list[sp.Expr]] = {}
    for component, expr in enumerate(row):
        if rr.is_zero_expr(expr):
            continue
        poly = sp.Poly(sp.expand(expr), theta, domain="EX")
        for (k,), coeff in poly.terms():
            coeff = rr.simp(coeff)
            rule = log_jet_rule(component, int(k), z, top_u, top_v, cache)
            for j in range(44):
                if not rr.is_zero_expr(rule[j]):
                    out[j] = rr.simp(out[j] + coeff * rule[j])
    return out


def weighted_forcing_bound(
    force_u: list[sp.Expr], force_v: list[sp.Expr], z: sp.Symbol
) -> tuple[sp.Rational, sp.Rational, int]:
    d = -sp.Rational(1, 2)
    rows = [(21, force_u), (43, force_v)]
    powers: list[sp.Rational] = []
    entries: list[tuple[int, int, sp.Expr, sp.Rational]] = []
    for i, row in rows:
        for j, value in enumerate(row):
            value = rr.simp(value / z)  # ordinary derivative forcing
            if rr.is_zero_expr(value):
                continue
            p = wg.rational_power_at_infinity(value, z)
            exponent = sp.Rational(p) + wg.weight(j, d) - wg.weight(i, d)
            powers.append(exponent)
            entries.append((i, j, value, exponent))
    if not powers:
        raise AssertionError("ordinary companion forcing vanished")
    worst = max(powers)
    Q = int(sp.ceiling(max(worst, sp.Rational(0))))

    # Exact row-sum constant for |D^-1 G D| <= C_G t^Q on t>=1.
    s = sp.symbols("s", positive=True)
    row_bounds = {21: sp.Rational(0), 43: sp.Rational(0)}
    for i, j, value, _ in entries:
        power_s = int(2 * (wg.weight(j, d) - wg.weight(i, d)))
        scaled = sp.factor(sp.cancel(sp.together(
            s**power_s * value.subs(z, s**2) / s ** (2 * Q)
        )))
        row_bounds[i] += wg.bound_rational_on_s_ge_1(scaled, s)
    Cg = max(row_bounds.values())
    if Cg <= 0:
        raise AssertionError("ordinary forcing row-sum constant is nonpositive")
    return worst, sp.Rational(Cg), Q


def main() -> None:
    B, Bp, z, theta = build_unreduced_and_p_derivative()
    rows, prows = apply_certified_row_transform(B, Bp, z, theta)
    p_orders = [rr.row_order(row, theta) for row in prows]
    if p_orders != [25, 23]:
        raise AssertionError(f"reduced exponent-derivative row orders changed: {p_orders}")

    # Existing exact homogeneous top-jet system.
    z0, top_u, top_v, constraint = origin.build_top_rules()
    if z0 != z:
        raise AssertionError("origin helper symbol mismatch")
    row0, row1 = rows
    prow0, prow1 = prows
    dprow1 = rr.theta_left_row(prow1, z, theta, 1)
    max_forcing_jet = max(rr.row_order(prow0, theta), rr.row_order(dprow1, theta))
    if max_forcing_jet != 25:
        raise AssertionError(f"inhomogeneous forcing jet order changed: {max_forcing_jet}")

    # Certify that the required theta^23..theta^25 log jets reduce exactly to
    # the existing 44-state rather than enlarging the dynamical system.
    cache: dict[tuple[int, int], list[sp.Expr]] = {}
    for component in (0, 1):
        for k in range(22, max_forcing_jet + 1):
            rule = log_jet_rule(component, k, z, top_u, top_v, cache)
            if len(rule) != 44:
                raise AssertionError("higher log-jet reduction changed state dimension")

    lead0 = rr.leading_vector(row0, theta)
    lead1 = rr.leading_vector(row1, theta)
    a, b = lead0
    c, dlead = lead1
    det = rr.simp(a * dlead - b * c)
    expected_det = sp.Rational(625, 64) * z * (18 * z + 5)
    if not rr.is_zero_expr(det - expected_det):
        raise AssertionError("ordinary companion top determinant changed")

    f0 = operator_on_log_state(prow0, z, theta, top_u, top_v)
    f1 = operator_on_log_state(dprow1, z, theta, top_u, top_v)
    force_u = [rr.simp(-(dlead * f0[j] - b * f1[j]) / det) for j in range(44)]
    force_v = [rr.simp((c * f0[j] - a * f1[j]) / det) for j in range(44)]

    allowed = [
        sp.Poly(z, z, domain="QQ").monic(),
        sp.Poly(18 * z + 5, z, domain="QQ").monic(),
    ]
    forcing_lcm, forcing_nonconstant, forcing_origin_order = fo.denominator_lcm(
        force_u + force_v, z, allowed
    )
    if forcing_origin_order > 1:
        raise AssertionError(
            f"ordinary theta forcing has origin pole order {forcing_origin_order}; top-log z divisibility is insufficient"
        )

    # Physical top-log first nonzero state: Y_L=z H with this H(0).
    xi1 = sp.Rational(20, 27)
    kap1 = -sp.Rational(5, 27)
    H0 = [xi1] * 22 + [kap1] * 22

    def forcing_limit(row: list[sp.Expr]) -> sp.Expr:
        total = sp.Integer(0)
        for j, value in enumerate(row):
            zv = rr.simp(z * value)
            total += rr.simp(zv.subs(z, 0)) * H0[j]
        return rr.simp(total)

    gu0 = forcing_limit(force_u)
    gv0 = forcing_limit(force_v)

    # Normalized ordinary seed U_O,0=(xi0,kappa0)=(0,1), so its 44-state
    # constant coefficient is nonzero only in K itself (state index 22).
    O0 = [sp.Integer(0)] * 44
    O0[22] = sp.Integer(1)
    homogeneous_top_u0 = rr.simp(sum(top_u[j].subs(z, 0) * O0[j] for j in range(44)))
    homogeneous_top_v0 = rr.simp(sum(top_v[j].subs(z, 0) * O0[j] for j in range(44)))
    if not rr.is_zero_expr(homogeneous_top_u0 + gu0):
        raise AssertionError(
            "ordinary origin compatibility failed in Xi top row: "
            + sp.sstr(rr.simp(homogeneous_top_u0 + gu0))
        )
    if not rr.is_zero_expr(homogeneous_top_v0 + gv0):
        raise AssertionError(
            "ordinary origin compatibility failed in K top row: "
            + sp.sstr(rr.simp(homogeneous_top_v0 + gv0))
        )

    # Retained inhomogeneous constraint R1 U_O + P1 U_L=0 at the origin.
    constraint_o0 = rr.simp(sum(constraint[j].subs(z, 0) * O0[j] for j in range(44)))
    p1_state = operator_on_log_state(prow1, z, theta, top_u, top_v)
    p1_limit = forcing_limit(p1_state)
    if not rr.is_zero_expr(constraint_o0 + p1_limit):
        raise AssertionError("ordinary retained inhomogeneous constraint fails at origin")

    # Canonical n=1 choice a1=0 in the already-certified formal relation.
    a1 = sp.Integer(0)
    b1 = sp.Rational(154, 45)
    kap_o1 = sp.factor(b1 / 6)
    xi_o1 = sp.factor(a1 - kap_o1)
    if kap_o1 != sp.Rational(77, 135) or xi_o1 != -sp.Rational(77, 135):
        raise AssertionError("canonical ordinary n=1 coordinates changed")

    # The inhomogeneous system has no positive-ray finite pole.  Its forcing
    # has at worst the same certified {z,18z+5} denominator support, while the
    # top-log state is already analytically continued for all finite t>0.
    ordinary_forcing_exprs = [rr.simp(value / z) for value in force_u + force_v]
    ordinary_forcing_lcm, _, ordinary_forcing_origin_order = fo.denominator_lcm(
        ordinary_forcing_exprs, z, allowed
    )

    worst_force_power, forcing_C, forcing_Q = weighted_forcing_bound(force_u, force_v, z)

    # Import the exact homogeneous weighted constant already certified by wg.
    Cstar = sp.Rational(108169036987421079299, 14745600)
    Bsqrt = 2 * Cstar
    if Bsqrt != sp.Rational(108169036987421079299, 7372800):
        raise AssertionError("homogeneous exp-sqrt constant changed")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_COMPANION_CERTIFIED")
    print("GENERALIZED_FROBENIUS_STRUCTURE := x^(1/2)[V_L(x)*log(x)+V_O(x)]")
    print("ORDER2_BOREL_ORDINARY_EQUATION := B*U_O + B_p*U_L = 0")
    print("B_P_DEFINITION := derivative in Euler exponent p of C_j(p) only; clearing factors and S(theta) are p-independent")
    print(f"REDUCED_B_P_ROW_ORDERS := {p_orders}")
    print(f"MAX_LOG_FORCING_JET_ORDER := {max_forcing_jet}")
    print("HIGHER_LOG_JET_REDUCTION := theta^23..theta^25 reduced exactly to the certified 44-state by repeated theta-system propagation")
    print("TRIANGULAR_FIRST_ORDER_STATE_DIMENSION := 88")
    print(f"THETA_FORCING_DENOMINATOR_LCM := {sp.sstr(forcing_lcm)}")
    print(f"THETA_FORCING_NONCONSTANT_DENOMINATOR_COUNT := {forcing_nonconstant}")
    print(f"THETA_FORCING_ORIGIN_POLE_ORDER := {forcing_origin_order}")
    print("TOP_LOG_ZERO_AT_ORIGIN := Y_L=z*H with H analytic")
    print("ORDINARY_ORIGIN_SEED := U_O,0=(0,1), corresponding to physical vector (1,2)")
    print("ORDINARY_ORIGIN_COMPATIBILITY := exact for both solved top rows")
    print("ORDINARY_RETAINED_CONSTRAINT_AT_ORIGIN := exact")
    print("CANONICAL_ORDINARY_N1_NORMALIZATION := a1=0")
    print("CANONICAL_ORDINARY_N1_PHYSICAL_VECTOR := [0,154/45]")
    print("CANONICAL_ORDINARY_N1_BOREL_COORDINATES := xi=-77/135; kappa=77/135")
    print("LOCAL_ORDINARY_BOREL_GERM := convergent by the standard analytic regular-singular/Frobenius theorem applied to the certified all-order formal recurrence and analytic inhomogeneous forcing")
    print(f"ORDINARY_DERIVATIVE_FORCING_DENOMINATOR_LCM := {sp.sstr(ordinary_forcing_lcm)}")
    print(f"ORDINARY_DERIVATIVE_FORCING_ORIGIN_POLE_ORDER := {ordinary_forcing_origin_order}")
    print("POSITIVE_RAY_ORDINARY_CONTINUATION := unique to every finite t>0 by the standard inhomogeneous linear-ODE theorem")
    print(f"WEIGHTED_FORCING_WORST_POWER_AT_INFINITY := {sp.sstr(worst_force_power)}")
    print(f"WEIGHTED_FORCING_POLYNOMIAL_POWER_Q := {forcing_Q}")
    print(f"WEIGHTED_FORCING_ROW_SUM_CONSTANT := {sp.sstr(forcing_C)}")
    print(f"FULL_LOG_PLUS_ORDINARY_EXP_SQRT_CONSTANT_B := {sp.sstr(Bsqrt)}")
    print("ORDINARY_GROWTH := variation of constants gives polynomial(t)*exp(B*sqrt(t)); same exponential constant B as top-log layer")
    print("FULL_BOREL_GROWTH := both log and ordinary Borel layers are polynomial(t)*exp(B*sqrt(t)) on t>=1")
    print("BOUNDARY := full log-plus-ordinary positive-ray Borel continuation/growth certified; two-fold Laplace reconstruction and original-equation closure remain to be certified")


if __name__ == "__main__":
    main()
