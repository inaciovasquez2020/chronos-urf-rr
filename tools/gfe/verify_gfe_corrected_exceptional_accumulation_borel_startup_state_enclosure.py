#!/usr/bin/env python3
"""Certify an explicit finite-x enclosure of the physical double-Laplace startup state.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

This verifier combines the certified top-log and ordinary local Borel majorants
with the exact 88-state triangular positive-ray system.  It chooses an explicit
startup point x0=R^-2 inside the already-certified double-Laplace interval,
splits the two-fold Laplace quadrant into x0*s*t<=1/16 and its complement,
and bounds both pieces rigorously:

* on the local core, exact coefficient majorants give a truncation remainder
  through ordinary order N=20;
* on the complement, an exact rational row-sum bound on 1/16<=z<=1 is joined
  to the certified weighted O(z^-1/2) positive-ray system for z>=1;
* the complement starts at s+t>R/2, and the residual exponential tail is
  bounded algebraically using exp(d)>=d^K/K! rather than floating arithmetic.

The resulting enclosure is converted from the reconstructed weighted fields
(h0,x*h1) and their Euler derivatives into the physical six-state
(h0,h0',h0'',h1,h1',h1'') at r0=2+x0.

This is a startup-state certificate only.  It does not propagate the enclosure
to r=4096 and does not prove C_grow != 0.
"""
from __future__ import annotations

import contextlib
import io
import math

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_double_laplace as dl
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_companion as companion
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_local_majorant as olocal
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_transfer as transfer
import verify_gfe_corrected_exceptional_accumulation_borel_origin_removability as origin
import verify_gfe_corrected_exceptional_accumulation_borel_positive_ray_weighted_growth as wg
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr
import verify_gfe_corrected_exceptional_accumulation_borel_top_log_local_majorant as local


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def ceil_rational(value: sp.Rational) -> int:
    q = sp.Rational(value)
    return int((int(q.p) + int(q.q) - 1) // int(q.q))


def ceil_sqrt_rational(value: sp.Rational) -> int:
    q = sp.Rational(value)
    target = (int(q.p) + int(q.q) - 1) // int(q.q)
    root = math.isqrt(target)
    if root * root < target:
        root += 1
    return root


def shifted_moment(poly_in_m: sp.Expr, m: sp.Symbol, q: sp.Rational) -> sp.Rational:
    poly = sp.Poly(sp.expand(poly_in_m), m, domain="QQ")
    total = sp.Rational(0)
    for (power,), coeff in poly.terms():
        total += sp.Rational(coeff) * olocal.moment_sum_polynomial(int(power), q)
    return sp.Rational(simp(total))


def local_tail_constant(
    n: sp.Symbol,
    m: sp.Symbol,
    start: int,
    jet: int,
    polynomial_power: int,
    qmax: sp.Rational,
    coefficient_constant: sp.Rational,
) -> sp.Rational:
    poly = (m + start) ** jet * (m + start + 1) ** polynomial_power
    return sp.Rational(coefficient_constant * shifted_moment(poly, m, qmax))


def rational_interval_abs_bound(expr: sp.Expr, z: sp.Symbol, zmin: sp.Rational) -> sp.Rational:
    value = simp(expr)
    if value == 0:
        return sp.Rational(0)
    num, den = sp.fraction(value)
    num_poly = sp.Poly(sp.expand(num), z, domain="QQ")
    num_upper = sum(abs(sp.Rational(c)) for c in num_poly.all_coeffs())

    coeff, factors = sp.factor_list(sp.expand(den), z)
    den_lower = abs(sp.Rational(coeff))
    for factor, power in factors:
        poly = sp.Poly(factor, z, domain="QQ")
        if poly.degree() == 0:
            den_lower *= abs(sp.Rational(poly.all_coeffs()[0])) ** power
            continue
        if poly.degree() != 1:
            raise AssertionError(
                "unexpected nonlinear denominator on the finite positive Borel interval: "
                + sp.sstr(factor)
            )
        left = sp.Rational(poly.as_expr().subs(z, zmin))
        right = sp.Rational(poly.as_expr().subs(z, 1))
        if left == 0 or right == 0 or left * right <= 0:
            raise AssertionError("denominator factor crosses zero on [1/16,1]")
        den_lower *= min(abs(left), abs(right)) ** power
    if den_lower <= 0:
        raise AssertionError("finite-interval denominator lower bound is nonpositive")
    return sp.Rational(num_upper, den_lower)


def build_theta_matrix_and_forcing() -> tuple[sp.Symbol, list[list[sp.Expr]], list[sp.Expr], list[sp.Expr]]:
    B, Bp, z, theta = companion.build_unreduced_and_p_derivative()
    rows, prows = companion.apply_certified_row_transform(B, Bp, z, theta)
    z0, top_u, top_v, _ = origin.build_top_rules()
    if z0 != z:
        raise AssertionError("origin/top-rule symbol mismatch")

    Atheta = [[sp.Integer(0) for _ in range(44)] for _ in range(44)]
    for k in range(21):
        Atheta[k][k + 1] = sp.Integer(1)
        Atheta[22 + k][22 + k + 1] = sp.Integer(1)
    Atheta[21] = list(top_u)
    Atheta[43] = list(top_v)

    row0, row1 = rows
    prow0, prow1 = prows
    dprow1 = rr.theta_left_row(prow1, z, theta, 1)
    lead0 = rr.leading_vector(row0, theta)
    lead1 = rr.leading_vector(row1, theta)
    a, b = lead0
    c, dlead = lead1
    det = simp(a * dlead - b * c)
    expected_det = sp.Rational(625, 64) * z * (18 * z + 5)
    if simp(det - expected_det) != 0:
        raise AssertionError("ordinary forcing top determinant changed")

    f0 = companion.operator_on_log_state(prow0, z, theta, top_u, top_v)
    f1 = companion.operator_on_log_state(dprow1, z, theta, top_u, top_v)
    force_u = [simp(-(dlead * f0[j] - b * f1[j]) / det) for j in range(44)]
    force_v = [simp((c * f0[j] - a * f1[j]) / det) for j in range(44)]
    return z, Atheta, force_u, force_v


def finite_interval_generator_bound(
    z: sp.Symbol,
    Atheta: list[list[sp.Expr]],
    force_u: list[sp.Expr],
    force_v: list[sp.Expr],
    zmin: sp.Rational,
) -> sp.Rational:
    row_bounds: list[sp.Rational] = []
    for i in range(44):
        row = sp.Rational(0)
        for value in Atheta[i]:
            if value != 0:
                row += rational_interval_abs_bound(simp(value / z), z, zmin)
        row_bounds.append(sp.Rational(row))

    # The ordinary block repeats the homogeneous rows and receives log forcing
    # only in its two solved top rows.
    ordinary_bounds = list(row_bounds)
    for target, forcing in [(21, force_u), (43, force_v)]:
        extra = sp.Rational(0)
        for value in forcing:
            if value != 0:
                extra += rational_interval_abs_bound(simp(value / z), z, zmin)
        ordinary_bounds[target] += sp.Rational(extra)
    bound = max(row_bounds + ordinary_bounds)
    if bound <= 0:
        raise AssertionError("finite positive-interval generator bound is nonpositive")
    return sp.Rational(bound)


def top_log_exact_vectors(end: int) -> tuple[dict[int, sp.Matrix], dict[int, sp.Matrix]]:
    xi, kap = local.physical_prefix()
    normalized: dict[int, sp.Matrix] = {}
    original: dict[int, sp.Matrix] = {}
    for index in range(end + 1):
        moment = sp.factorial(index) ** 2
        raw = sp.Matrix([
            sp.Rational(xi[index] + kap[index]),
            sp.Rational((4 * index + 2) * kap[index]),
        ])
        original[index] = raw
        normalized[index] = raw / moment
    return normalized, original


def ordinary_exact_vectors(end: int, exact_top: dict[int, sp.Matrix]) -> dict[int, sp.Matrix]:
    n, _, ordinary_transfer, forcing_transfer = transfer.build_normalized_transfer()
    ordinary: dict[int, sp.Matrix] = {
        0: sp.Matrix([sp.Integer(1), sp.Integer(2)]),
        1: sp.Matrix([sp.Integer(0), sp.Rational(154, 45)]),
    }
    for index in range(2, end + 1):
        value = sp.zeros(2, 1)
        for lag, block in ordinary_transfer.items():
            prev = index - lag
            if prev >= 0:
                value += block.subs(n, index) * ordinary[prev]
        for lag, block in forcing_transfer.items():
            top_index = index - lag
            if top_index >= 0:
                value += block.subs(n, index) * exact_top[top_index]
        ordinary[index] = value.applyfunc(simp)
    return ordinary


def endpoint_raw_state_bound(jet: int, q: sp.Rational, C: sp.Rational, power: int) -> sp.Rational:
    n = sp.symbols("n", nonnegative=True, integer=True)
    total = sp.Rational(0)
    # Sum n^jet (n+1)^power q^n exactly.  Raw (Xi,K) is bounded by twice
    # the corresponding physical two-vector coefficient.
    poly = sp.expand(n**jet * (n + 1) ** power)
    p = sp.Poly(poly, n, domain="QQ")
    for (k,), coeff in p.terms():
        total += sp.Rational(coeff) * olocal.moment_sum_polynomial(int(k), q)
    return sp.Rational(2 * C * total)


def prefix_norm(normalized: dict[int, sp.Matrix], jet: int, end: int) -> sp.Rational:
    rows = [sp.Rational(0), sp.Rational(0)]
    for index in range(end + 1):
        weight = sp.Integer(index) ** jet
        for component in range(2):
            rows[component] += abs(sp.Rational(weight * normalized[index][component]))
    return max(rows)


def incomplete_gamma_polynomial(p: int, R: int) -> sp.Rational:
    # After s+t=u, st<=u^2/4, and the safe exp(-u/2) damping,
    # int_{u>=R/2} u*(x*st)^p exp(-u/2) du is bounded by
    # exp(-R/4) times this rational factor.
    x = sp.Rational(1, R * R)
    series = sp.Rational(0)
    for k in range(2 * p + 2):
        series += sp.Rational(R, 4) ** k / sp.factorial(k)
    return sp.Rational(4 * sp.factorial(2 * p + 1) * x**p * series)


def main() -> None:
    # Re-run the two immediate theorem interfaces and lock their exact constants.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        olocal.main()
    ordinary_log = buffer.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_LOCAL_MAJORANT_CERTIFIED",
        "TOP_LOG_GLOBAL_MAJORANT_CONSTANT := 1/9",
        "ORDINARY_MAJORANT_BASE := 19/2",
        "ORDINARY_MAJORANT_POLYNOMIAL_POWER := 5",
        "ORDINARY_MAJORANT_CONSTANT := 4",
        "ORDINARY_BOREL_RADIUS_LOWER_BOUND := 2/19",
    ]:
        if token not in ordinary_log:
            raise AssertionError("ordinary-local-majorant dependency changed: " + token)

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        dl.main()
    laplace_log = buffer.getvalue()
    for token in [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_DOUBLE_LAPLACE_RECONSTRUCTION_CERTIFIED",
        "ACTUAL_ORIGINAL_EULER_SOLUTION :=",
        "DIFFERENTIATION_UNDER_INTEGRAL := justified for every finite Euler derivative",
    ]:
        if token not in laplace_log:
            raise AssertionError("double-Laplace dependency changed: " + token)

    CL = sp.Rational(1, 9)
    CO = sp.Rational(4)
    AL = sp.Rational(5)
    AO = sp.Rational(19, 2)
    N = 20
    zcore = sp.Rational(1, 16)
    qL = AL * zcore
    qO = AO * zcore
    if not (qL == sp.Rational(5, 16) and qO == sp.Rational(19, 32)):
        raise AssertionError("local core geometric factors changed")

    z, Atheta, force_u, force_v = build_theta_matrix_and_forcing()
    Mmid = finite_interval_generator_bound(z, Atheta, force_u, force_v, zcore)
    M = sp.Rational(15, 16) * Mmid

    # Certified weighted tail constants.  The 88-state triangular row sum is
    # bounded by (Cstar+Cforce)*t^-1/2 for t>=1.
    Cstar = sp.Rational(108169036987421079299, 14745600)
    Cforce = sp.Rational(47202835805013908339, 1382400)
    Btail = sp.Rational(2) * (Cstar + Cforce)

    # Local 88-state bound at z=1/16, including all Euler jets through 21.
    raw_bounds: list[sp.Rational] = []
    for jet in range(22):
        raw_bounds.append(endpoint_raw_state_bound(jet, qL, CL, 1))
        raw_bounds.append(endpoint_raw_state_bound(jet, qO, CO, 5))
    Xcore = max(raw_bounds)
    if Xcore <= 0:
        raise AssertionError("local 88-state endpoint bound is nonpositive")

    x_safe = sp.Rational(
        54358179840000,
        11700540562786069522705159372002046331401,
    )
    Rsafe = ceil_sqrt_rational(1 / x_safe)
    R = max(
        Rsafe,
        ceil_rational(Btail) + 1,
        8 * (ceil_rational(M) + 100),
        10000,
    )
    x0 = sp.Rational(1, R * R)
    if not (x0 > 0 and x0 <= x_safe):
        raise AssertionError("chosen startup point is outside the certified Laplace interval")
    if not sp.Rational(Btail, R) < 1:
        raise AssertionError("tail exponential damping reserve failed")

    # On the complement x0*s*t>1/16, AM-GM gives s+t>R/2.  The finite-interval
    # Gronwall factor contributes exp(M), while the quadrant tail contributes
    # exp(-R/4).  Keep the proof exact via exp(d)>=d^K/K!.
    d = sp.Rational(R, 4) - M
    if d <= 0:
        raise AssertionError("complement exponential reserve is nonpositive")
    Kexp = 48
    exp_tail_rational = sp.Rational(sp.factorial(Kexp), d**Kexp)

    exact_top, original_top = top_log_exact_vectors(N + 1)
    exact_ordinary = ordinary_exact_vectors(N, exact_top)
    original_ordinary = {
        index: exact_ordinary[index] * sp.factorial(index) ** 2
        for index in range(N + 1)
    }

    m = sp.symbols("m", nonnegative=True, integer=True)
    n = sp.symbols("n", nonnegative=True, integer=True)
    core_L: list[sp.Rational] = []
    core_O: list[sp.Rational] = []
    pref_L: list[sp.Rational] = []
    pref_O: list[sp.Rational] = []
    J0 = incomplete_gamma_polynomial(0, R)
    J11 = incomplete_gamma_polynomial(11, R)
    JN = incomplete_gamma_polynomial(N, R)

    global_tail_L: list[sp.Rational] = []
    global_tail_O: list[sp.Rational] = []
    for jet in range(3):
        SL = local_tail_constant(n, m, N + 1, jet, 1, qL, CL)
        SO = local_tail_constant(n, m, N + 1, jet, 5, qO, CO)
        core_L_j = sp.Rational(
            SL * (AL * x0) ** (N + 1) * sp.factorial(N + 1) ** 2
        )
        core_O_j = sp.Rational(
            SO * (AO * x0) ** (N + 1) * sp.factorial(N + 1) ** 2
        )
        core_L.append(core_L_j)
        core_O.append(core_O_j)

        PL = prefix_norm(exact_top, jet, N)
        PO = prefix_norm(exact_ordinary, jet, N)
        pref_L.append(PL)
        pref_O.append(PO)

        # ||theta^j W||_inf <= 6 ||X||_inf for j<=2.  The unified positive-ray
        # state bound is 4*Xcore*exp(M)*(1+z^11)*exp(Btail*sqrt(z)).
        # Prefix subtraction adds P_j*(1+z^N).  The common exponential tail is
        # removed with the exact d^-K algebraic bound above.
        state_piece = sp.Rational(24 * Xcore) * (J0 + J11)
        global_tail_L.append(
            sp.Rational(exp_tail_rational * (state_piece + PL * (J0 + JN)))
        )
        global_tail_O.append(
            sp.Rational(exp_tail_rational * (state_piece + PO * (J0 + JN)))
        )

    rad_L = [sp.Rational(core_L[j] + global_tail_L[j]) for j in range(3)]
    rad_O = [sp.Rational(core_O[j] + global_tail_O[j]) for j in range(3)]

    # Exact truncated centers after the two gamma moments restore (n!)^2.
    center_L: list[sp.Matrix] = []
    center_O: list[sp.Matrix] = []
    for jet in range(3):
        cL = sp.zeros(2, 1)
        cO = sp.zeros(2, 1)
        for index in range(N + 1):
            weight = sp.Integer(index) ** jet
            cL += weight * original_top[index] * x0**index
            cO += weight * original_ordinary[index] * x0**index
        center_L.append(cL.applyfunc(simp))
        center_O.append(cO.applyfunc(simp))

    # P=H_L*log(x)+H_O and its first two Euler derivatives.  Since x0=R^-2,
    # log(x0)=-2*log(R) exactly.  For radii use log(R)<=R-1 (R>=1).
    logx = -2 * sp.log(sp.Integer(R))
    log_abs_bound = sp.Integer(2 * (R - 1))
    Pcenter: list[sp.Matrix] = [
        center_L[0] * logx + center_O[0],
        center_L[1] * logx + center_L[0] + center_O[1],
        center_L[2] * logx + 2 * center_L[1] + center_O[2],
    ]
    Prad = [
        sp.Rational(log_abs_bound * rad_L[0] + rad_O[0]),
        sp.Rational(log_abs_bound * rad_L[1] + rad_L[0] + rad_O[1]),
        sp.Rational(log_abs_bound * rad_L[2] + 2 * rad_L[1] + rad_O[2]),
    ]

    half = sp.Rational(1, 2)
    state_center = [
        simp(Pcenter[0][0] / R),
        simp(R * (half * Pcenter[0][0] + Pcenter[1][0])),
        simp(R**3 * (Pcenter[2][0] - sp.Rational(1, 4) * Pcenter[0][0])),
        simp(R * Pcenter[0][1]),
        simp(R**3 * (Pcenter[1][1] - half * Pcenter[0][1])),
        simp(R**5 * (Pcenter[2][1] - 2 * Pcenter[1][1] + sp.Rational(3, 4) * Pcenter[0][1])),
    ]
    state_radius = [
        sp.Rational(Prad[0], R),
        sp.Rational(R * (half * Prad[0] + Prad[1])),
        sp.Rational(R**3 * (Prad[2] + sp.Rational(1, 4) * Prad[0])),
        sp.Rational(R * Prad[0]),
        sp.Rational(R**3 * (Prad[1] + half * Prad[0])),
        sp.Rational(R**5 * (Prad[2] + 2 * Prad[1] + sp.Rational(3, 4) * Prad[0])),
    ]
    if any(radius <= 0 for radius in state_radius):
        raise AssertionError("startup six-state radius is nonpositive")

    # The enclosure should be genuinely informative, not merely finite.  This
    # checks the aggregate radius against the aggregate center at high precision
    # without using that numerical comparison as a theorem dependency.
    center_scale = max(abs(sp.N(value, 80)) for value in state_center)
    radius_scale = max(sp.N(value, 80) for value in state_radius)
    relative_scale = sp.N(radius_scale / center_scale, 40) if center_scale != 0 else sp.oo

    r0 = sp.Rational(2) + x0
    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_STARTUP_STATE_ENCLOSURE_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print(f"TRUNCATION_ORDER := {N}")
    print(f"LOCAL_CORE_BOREL_RADIUS := {sp.sstr(zcore)}")
    print(f"FINITE_INTERVAL_88_STATE_ROW_SUM_BOUND := {sp.sstr(Mmid)}")
    print(f"FINITE_INTERVAL_GRONWALL_EXPONENT_BOUND := {sp.sstr(M)}")
    print(f"WEIGHTED_88_STATE_EXP_SQRT_CONSTANT := {sp.sstr(Btail)}")
    print(f"LOCAL_88_STATE_ENDPOINT_BOUND := {sp.sstr(Xcore)}")
    print(f"STARTUP_R := {R}")
    print(f"STARTUP_X := {sp.sstr(x0)}")
    print(f"STARTUP_RADIUS_R0 := {sp.sstr(r0)}")
    print(f"DOUBLE_LAPLACE_SAFE_X := {sp.sstr(x_safe)}")
    print("STARTUP_INSIDE_SAFE_INTERVAL := certified")
    print("LAPLACE_SPLIT := local core x*s*t<=1/16 plus positive-ray complement")
    print("COMPLEMENT_AMGM := x*s*t>1/16 implies s+t>R/2")
    print(f"COMPLEMENT_EXPONENTIAL_RESERVE_D := {sp.sstr(d)}")
    print(f"EXPONENTIAL_TAIL_ALGEBRAIC_ORDER := {Kexp}")
    print("EXPONENTIAL_TAIL_INEQUALITY := exp(-d) <= K!/d^K from exp(d)>=d^K/K!")
    for jet in range(3):
        print(f"THETA_JET_{jet}_TOP_LOG_REMAINDER_RADIUS := {sp.sstr(rad_L[jet])}")
        print(f"THETA_JET_{jet}_ORDINARY_REMAINDER_RADIUS := {sp.sstr(rad_O[jet])}")
    names = ["h0", "h0p", "h0pp", "h1", "h1p", "h1pp"]
    for name, center, radius in zip(names, state_center, state_radius):
        print(f"STARTUP_{name.upper()}_CENTER := {sp.sstr(center)}")
        print(f"STARTUP_{name.upper()}_RADIUS := {sp.sstr(radius)}")
        print(f"STARTUP_{name.upper()}_CENTER_DECIMAL := {sp.N(center, 24)}")
        print(f"STARTUP_{name.upper()}_RADIUS_DECIMAL := {sp.N(radius, 12)}")
    print(f"STARTUP_STATE_AGGREGATE_RELATIVE_RADIUS_DECIMAL := {relative_scale}")
    print("STARTUP_STATE_ENCLOSURE := componentwise closed disks around the displayed centers")
    print("NEXT_ROUTE := propagate this certified six-state enclosure from r0 to r=4096 with a validated interval ODE solver, then apply the existing growing-dual nonvanishing test")
    print("BOUNDARY := startup state enclosed only; no validated propagation to r=4096, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
