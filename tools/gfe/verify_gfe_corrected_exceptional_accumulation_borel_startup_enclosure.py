#!/usr/bin/env python3
"""Certify a quantitative finite-x startup enclosure for the physical branch.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

This verifier is the quantitative bridge between the already-certified local
order-2 Borel majorants and a future validated exterior propagation.  It uses
only exact rational inequalities for every truncation and tail decision.

For either the top-log or ordinary physical Borel vector X(z), and Euler jet
j=0,1,2, write P_{X,j} for the exact degree-20 prefix of theta^j X.  The full
double-Laplace moment of P_{X,j} is an exact rational vector because

  int_0^inf exp(-s)s^n ds * int_0^inf exp(-t)t^n dt = (n!)^2.

The error is split into three regions in z=x*s*t:

* local: z <= z_c=1/10000, controlled coefficientwise by the certified Borel
  majorants;
* compact: z_c < z <= 1, controlled by an exact rational Gronwall row-sum
  bound for the coupled 88-state top-log/ordinary system;
* far: z > 1, controlled by the certified weighted exp(B*sqrt(z)) estimate.

The nonlocal integrals are not numerically approximated.  The startup x is
chosen so that elementary inequalities e>2 and AM-GM force each of four
nonlocal tail contributions below 2^-120 by exact rational comparisons.

The returned enclosure is for W_L,W_O and their first two Euler jets, where
W=S(theta)V.  A symbolic componentwise enclosure for
Y=(h0,h0',h0'',h1,h1',h1'') is also constructed from

  (h0,x*h1)^T = x^(1/2) [W_L log(x)+W_O].

This certificate does not propagate that enclosure to r=4096 and does not
prove C_grow != 0.
"""
from __future__ import annotations

import contextlib
import io
from typing import Any

import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_double_laplace as double
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_companion as companion
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_local_majorant as omaj
import verify_gfe_corrected_exceptional_accumulation_borel_ordinary_transfer as transfer
import verify_gfe_corrected_exceptional_accumulation_borel_origin_removability as origin
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr
import verify_gfe_corrected_exceptional_accumulation_borel_positive_ray_weighted_growth as wg


N = 20
Z_CUT = sp.Rational(1, 10000)
TAIL_BITS = 120
C_L = sp.Rational(1, 9)
C_O = sp.Rational(4)
A_O = sp.Rational(19, 2)
B_SQRT = sp.Rational(108169036987421079299, 7372800)
C_G = sp.Rational(47202835805013908339, 1382400)
X_SAFE = sp.Rational(
    54358179840000,
    11700540562786069522705159372002046331401,
)


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def vector_inf_norm(vector: sp.Matrix) -> sp.Rational:
    values = [abs(sp.Rational(simp(value))) for value in vector]
    return max(values) if values else sp.Rational(0)


def ceil_log2_rational(value: sp.Rational) -> int:
    """Smallest integer b with value <= 2^b, using exact comparisons."""
    value = sp.Rational(value)
    if value <= 0:
        raise AssertionError("ceil_log2_rational requires a positive rational")
    p = int(value.p)
    q = int(value.q)
    b = p.bit_length() - q.bit_length()
    two = sp.Integer(2)
    while value > two**b:
        b += 1
    while value <= two ** (b - 1):
        b -= 1
    return b


def polynomial_geometric_sum(jet: int, power: int, q: sp.Rational) -> sp.Rational:
    """Exact sum sum_(n>=0) n^jet (n+1)^power q^n."""
    if not (0 <= q < 1):
        raise AssertionError("geometric moment requires 0<=q<1")
    n = sp.symbols("n")
    poly = sp.Poly(sp.expand(n**jet * (n + 1) ** power), n, domain="QQ")
    total = sp.Rational(0)
    for (degree,), coefficient in poly.terms():
        total += sp.Rational(coefficient) * omaj.moment_sum_polynomial(int(degree), q)
    return sp.Rational(simp(total))


def polynomial_geometric_tail(
    jet: int, power: int, q: sp.Rational, cutoff: int
) -> sp.Rational:
    full = polynomial_geometric_sum(jet, power, q)
    finite = sp.Rational(0)
    for index in range(cutoff + 1):
        njet = sp.Integer(1) if jet == 0 else sp.Integer(index) ** jet
        finite += njet * sp.Integer(index + 1) ** power * q**index
    tail = sp.Rational(simp(full - finite))
    if tail < 0:
        raise AssertionError("geometric tail became negative")
    return tail


def exact_prefixes() -> tuple[dict[int, sp.Matrix], dict[int, sp.Matrix]]:
    """Return exact normalized physical top-log and ordinary vectors through N."""
    xi, kap = omaj.local.physical_prefix()
    top: dict[int, sp.Matrix] = {}
    for index in range(max(N + 2, 22)):
        moment = sp.factorial(index) ** 2
        Xi = sp.Rational(xi[index], moment)
        K = sp.Rational(kap[index], moment)
        top[index] = sp.Matrix([Xi + K, (4 * index + 2) * K])

    n, solve_det, ordinary_transfer, forcing_transfer = transfer.build_normalized_transfer()
    expected_det = sp.Rational(3125, 128) * n**3 * (n - 1) * (2 * n - 3)
    if simp(solve_det - expected_det) != 0:
        raise AssertionError("ordinary normalized transfer determinant changed")

    ordinary: dict[int, sp.Matrix] = {
        0: sp.Matrix([sp.Integer(1), sp.Integer(2)]),
        1: sp.Matrix([sp.Integer(0), sp.Rational(154, 45)]),
    }
    for index in range(2, N + 1):
        value = sp.zeros(2, 1)
        for lag, block in ordinary_transfer.items():
            previous = index - lag
            if previous >= 0:
                value += block.subs(n, index) * ordinary[previous]
        for lag, block in forcing_transfer.items():
            top_index = index - lag
            if top_index >= 0:
                value += block.subs(n, index) * top[top_index]
        ordinary[index] = value.applyfunc(simp)

    if ordinary[0] != sp.Matrix([1, 2]):
        raise AssertionError("ordinary n=0 normalization changed")
    if ordinary[1] != sp.Matrix([0, sp.Rational(154, 45)]):
        raise AssertionError("ordinary n=1 normalization changed")
    return top, ordinary


def full_moment_center(
    prefix: dict[int, sp.Matrix], jet: int, x: sp.Rational
) -> sp.Matrix:
    center = sp.zeros(2, 1)
    for index in range(N + 1):
        njet = sp.Integer(1) if jet == 0 else sp.Integer(index) ** jet
        center += njet * sp.factorial(index) ** 2 * prefix[index] * x**index
    return center.applyfunc(simp)


def compact_rational_bound(expr: sp.Expr, z: sp.Symbol, zmin: sp.Rational) -> sp.Rational:
    """Exact coefficient-L1 bound for a rational function on zmin<=z<=1.

    Every denominator factor of the certified 88-state derivative system must
    be supported on z and 18*z+5.  The numerator is bounded by its coefficient
    L1 norm because 0<=z<=1; denominator factors are minimized at z=zmin.
    """
    value = simp(expr)
    if value == 0:
        return sp.Rational(0)
    numerator, denominator = sp.fraction(value)
    pnum = sp.Poly(sp.expand(numerator), z, domain="QQ")
    pden = sp.Poly(sp.expand(denominator), z, domain="QQ")
    numerator_l1 = sum(abs(sp.Rational(c)) for c in pnum.all_coeffs())

    coeff, factors = sp.factor_list(pden.as_expr(), z)
    lower = abs(sp.Rational(coeff))
    z_monic = sp.Poly(z, z, domain="QQ").monic()
    linear_monic = sp.Poly(18 * z + 5, z, domain="QQ").monic()
    for factor, exponent in factors:
        p = sp.Poly(factor, z, domain="QQ")
        lead = abs(sp.Rational(p.LC()))
        monic = p.monic()
        if monic == z_monic:
            minimum = zmin
        elif monic == linear_monic:
            minimum = zmin + sp.Rational(5, 18)
        else:
            raise AssertionError(
                "unexpected compact-ray denominator factor: " + sp.sstr(factor)
            )
        lower *= (lead * minimum) ** int(exponent)
    if lower <= 0:
        raise AssertionError("compact denominator lower bound vanished")
    return sp.Rational(simp(numerator_l1 / lower))


def ordinary_forcing_rows() -> tuple[sp.Symbol, list[sp.Expr], list[sp.Expr], list[sp.Expr], list[sp.Expr]]:
    """Reconstruct the exact ordinary derivative forcing used by its certificate."""
    B, Bp, z, theta = companion.build_unreduced_and_p_derivative()
    rows, prows = companion.apply_certified_row_transform(B, Bp, z, theta)
    z0, top_u, top_v, _constraint = origin.build_top_rules()
    if z0 != z:
        raise AssertionError("ordinary forcing symbol mismatch")

    dprow1 = rr.theta_left_row(prows[1], z, theta, 1)
    f0 = companion.operator_on_log_state(prows[0], z, theta, top_u, top_v)
    f1 = companion.operator_on_log_state(dprow1, z, theta, top_u, top_v)

    lead0 = rr.leading_vector(rows[0], theta)
    lead1 = rr.leading_vector(rows[1], theta)
    a, b = lead0
    c, dlead = lead1
    det = simp(a * dlead - b * c)
    expected_det = sp.Rational(625, 64) * z * (18 * z + 5)
    if simp(det - expected_det) != 0:
        raise AssertionError("ordinary forcing solve determinant changed")

    force_u = [simp(-(dlead * f0[j] - b * f1[j]) / det) for j in range(44)]
    force_v = [simp((c * f0[j] - a * f1[j]) / det) for j in range(44)]

    worst, Cg, Q = companion.weighted_forcing_bound(force_u, force_v, z)
    if worst != -sp.Rational(1, 2) or Q != 0 or Cg != C_G:
        raise AssertionError(
            "ordinary weighted forcing certificate changed: "
            f"worst={worst}, Q={Q}, Cg={Cg}"
        )
    return z, top_u, top_v, force_u, force_v


def compact_coupled_row_sum_bound() -> sp.Rational:
    """Bound the full top-log/ordinary 88-state derivative matrix on [z_c,1]."""
    z, top_u, top_v, force_u, force_v = ordinary_forcing_rows()

    homogeneous_rows = [sp.Rational(0) for _ in range(44)]
    chain = compact_rational_bound(sp.Integer(1) / z, z, Z_CUT)
    for k in range(21):
        homogeneous_rows[k] += chain
        homogeneous_rows[22 + k] += chain
    for j, value in enumerate(top_u):
        homogeneous_rows[21] += compact_rational_bound(value / z, z, Z_CUT)
    for j, value in enumerate(top_v):
        homogeneous_rows[43] += compact_rational_bound(value / z, z, Z_CUT)
    M_A = max(homogeneous_rows)

    forcing_rows = [sp.Rational(0), sp.Rational(0)]
    for value in force_u:
        forcing_rows[0] += compact_rational_bound(value / z, z, Z_CUT)
    for value in force_v:
        forcing_rows[1] += compact_rational_bound(value / z, z, Z_CUT)
    M_F = max(forcing_rows)
    if M_A <= 0 or M_F <= 0:
        raise AssertionError("compact coupled row-sum bound is nonpositive")

    # A block-triangular infinity-row bound is at most M_A+M_F.
    return sp.Rational(simp(M_A + M_F))


def initial_state_bound() -> sp.Rational:
    """Bound every one of the 88 Euler-jet coordinates at z=z_c."""
    qL = sp.Rational(5) * Z_CUT
    qO = A_O * Z_CUT
    top_bounds: list[sp.Rational] = []
    ordinary_bounds: list[sp.Rational] = []
    for jet in range(22):
        top_bounds.append(
            sp.Rational(2) * C_L * polynomial_geometric_sum(jet, 1, qL)
        )
        ordinary_bounds.append(
            sp.Rational(2) * C_O * polynomial_geometric_sum(jet, 5, qO)
        )
    bound = max(top_bounds + ordinary_bounds)
    if bound <= 0:
        raise AssertionError("startup 88-state bound is nonpositive")
    return sp.Rational(simp(bound))


def local_remainder(layer: str, jet: int) -> sp.Rational:
    if layer == "L":
        q = sp.Rational(5) * Z_CUT
        return sp.Rational(
            simp(C_L * polynomial_geometric_tail(jet, 1, q, N))
        )
    if layer == "O":
        q = A_O * Z_CUT
        return sp.Rational(
            simp(C_O * polynomial_geometric_tail(jet, 5, q, N))
        )
    raise AssertionError("unknown Borel layer")


def prefix_pointwise_bound(prefix: dict[int, sp.Matrix], jet: int) -> sp.Rational:
    total = sp.Rational(0)
    for index in range(N + 1):
        njet = sp.Integer(1) if jet == 0 else sp.Integer(index) ** jet
        total += njet * vector_inf_norm(prefix[index])
    return sp.Rational(simp(total))


def choose_startup_x(K_compact: sp.Rational, S0: sp.Rational, Pmax: sp.Rational) -> tuple[sp.Rational, dict[str, int]]:
    """Choose x=x_safe/10^k using only exact square inequalities."""
    mid_actual_prefactor = sp.Rational(24) * S0
    mid_poly_prefactor = sp.Rational(4) * Pmax
    global_actual_prefactor = (
        sp.Rational(6) * S0 * (sp.Rational(2) + C_G) * sp.Integer(1536) ** 2
    )
    global_poly_prefactor = (
        Pmax * (sp.factorial(N) * sp.Integer(2) ** (N + 1)) ** 2
    )

    L_mid_actual = max(1, TAIL_BITS + ceil_log2_rational(mid_actual_prefactor))
    L_mid_poly = max(1, TAIL_BITS + ceil_log2_rational(mid_poly_prefactor))
    L_global_actual = max(1, TAIL_BITS + ceil_log2_rational(global_actual_prefactor))
    L_global_poly = max(1, TAIL_BITS + ceil_log2_rational(global_poly_prefactor))

    levels = {
        "mid_actual": L_mid_actual,
        "mid_poly": L_mid_poly,
        "global_actual": L_global_actual,
        "global_poly": L_global_poly,
    }

    for decade in range(1001):
        x = sp.Rational(X_SAFE, 10**decade)
        invx = sp.Rational(1, x)
        local_ratio = sp.Rational(Z_CUT, x)
        conditions = [
            local_ratio >= (K_compact + L_mid_actual) ** 2,
            local_ratio >= sp.Integer(L_mid_poly) ** 2,
            invx >= 4 * (K_compact + L_global_actual) ** 2,
            invx >= sp.Integer(L_global_poly) ** 2,
        ]
        if all(conditions):
            return x, levels
    raise AssertionError("failed to choose an exact startup x within 1000 decades")


def physical_six_state_enclosure(startup: dict[str, Any]) -> dict[str, Any]:
    """Convert the W-enclosure to an exact symbolic six-state enclosure."""
    x = sp.Rational(startup["x_start"])
    logx = sp.log(x)
    sqrtx = sp.sqrt(x)
    log_bound = ceil_log2_rational(sp.Rational(1, x))
    if log_bound <= 0:
        raise AssertionError("startup logarithm bound is not positive")

    centers = startup["W_centers"]
    radii = startup["W_radii"]
    WL0, WL1, WL2 = (centers["L"][j] for j in range(3))
    WO0, WO1, WO2 = (centers["O"][j] for j in range(3))
    rL0, rL1, rL2 = (sp.Rational(radii["L"][j]) for j in range(3))
    rO0, rO1, rO2 = (sp.Rational(radii["O"][j]) for j in range(3))

    F0 = (WL0 * logx + WO0).applyfunc(simp)
    F1 = (WL1 * logx + WL0 + WO1).applyfunc(simp)
    F2 = (WL2 * logx + 2 * WL1 + WO2).applyfunc(simp)

    rF0 = sp.Rational(simp(log_bound * rL0 + rO0))
    rF1 = sp.Rational(simp(log_bound * rL1 + rL0 + rO1))
    rF2 = sp.Rational(simp(log_bound * rL2 + 2 * rL1 + rO2))

    state_centers = [
        simp(sqrtx * F0[0]),
        simp((sp.Rational(1, 2) * F0[0] + F1[0]) / sqrtx),
        simp((F2[0] - sp.Rational(1, 4) * F0[0]) / (x * sqrtx)),
        simp(F0[1] / sqrtx),
        simp((F1[1] - sp.Rational(1, 2) * F0[1]) / (x * sqrtx)),
        simp((F2[1] - 2 * F1[1] + sp.Rational(3, 4) * F0[1]) / (x**2 * sqrtx)),
    ]
    state_radii = [
        simp(sqrtx * rF0),
        simp((sp.Rational(1, 2) * rF0 + rF1) / sqrtx),
        simp((rF2 + sp.Rational(1, 4) * rF0) / (x * sqrtx)),
        simp(rF0 / sqrtx),
        simp((rF1 + sp.Rational(1, 2) * rF0) / (x * sqrtx)),
        simp((rF2 + 2 * rF1 + sp.Rational(3, 4) * rF0) / (x**2 * sqrtx)),
    ]
    if any(radius <= 0 for radius in state_radii):
        raise AssertionError("symbolic physical six-state radius is nonpositive")
    return {
        "log_abs_upper": log_bound,
        "centers": state_centers,
        "radii": state_radii,
    }


def build_startup_enclosure() -> dict[str, Any]:
    """Construct the exact rational W startup enclosure and symbolic six-state."""
    # Bind this verifier to the exact previously certified ordinary-majorant
    # surface.  This is intentionally the expensive dependency: it prevents a
    # stale hard-coded C_O=4 from silently surviving a source change.
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        omaj.main()
    prior = buffer.getvalue()
    required = [
        "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_ORDINARY_LOCAL_MAJORANT_CERTIFIED",
        "TOP_LOG_GLOBAL_MAJORANT_CONSTANT := 1/9",
        "ORDINARY_MAJORANT_BASE := 19/2",
        "ORDINARY_MAJORANT_POLYNOMIAL_POWER := 5",
        "ORDINARY_MAJORANT_CONSTANT := 4",
        "LOCAL_MAJORANT_INTERVAL := 0 <= z <= 1/10",
    ]
    for token in required:
        if token not in prior:
            raise AssertionError("ordinary-local-majorant dependency changed: " + token)

    if simp(1 / B_SQRT**2 - X_SAFE) != 0:
        raise AssertionError("safe double-Laplace radius changed")
    if not (0 < Z_CUT < sp.Rational(1, 10)):
        raise AssertionError("local startup cutoff left the certified Borel interval")

    top, ordinary = exact_prefixes()

    local: dict[str, dict[int, sp.Rational]] = {"L": {}, "O": {}}
    bit = sp.Rational(1, 2**TAIL_BITS)
    for layer in ("L", "O"):
        for jet in range(3):
            remainder = local_remainder(layer, jet)
            if not remainder < bit:
                raise AssertionError(
                    f"local {layer} jet-{jet} remainder exceeds 2^-{TAIL_BITS}"
                )
            local[layer][jet] = remainder

    M88 = compact_coupled_row_sum_bound()
    K_compact = sp.Rational(simp(M88 * (1 - Z_CUT)))
    S0 = initial_state_bound()

    Pmax = sp.Rational(0)
    for prefix in (top, ordinary):
        for jet in range(3):
            Pmax = max(Pmax, prefix_pointwise_bound(prefix, jet))
    if Pmax <= 0:
        raise AssertionError("polynomial prefix bound vanished")

    x_start, suppression_levels = choose_startup_x(K_compact, S0, Pmax)
    if not (0 < x_start <= X_SAFE):
        raise AssertionError("startup x left the certified safe horizon interval")

    centers: dict[str, dict[int, sp.Matrix]] = {"L": {}, "O": {}}
    radii: dict[str, dict[int, sp.Rational]] = {"L": {}, "O": {}}
    for layer, prefix in (("L", top), ("O", ordinary)):
        for jet in range(3):
            centers[layer][jet] = full_moment_center(prefix, jet, x_start)
            radius = sp.Rational(simp(local[layer][jet] + 4 * bit))
            if not radius < 5 * bit:
                raise AssertionError("combined startup radius failed the 5*2^-T bound")
            radii[layer][jet] = radius

    result: dict[str, Any] = {
        "x_start": x_start,
        "x_safe": X_SAFE,
        "truncation_order": N,
        "local_borel_cutoff": Z_CUT,
        "tail_bits": TAIL_BITS,
        "compact_row_sum_bound": M88,
        "compact_gronwall_exponent": K_compact,
        "compact_initial_state_bound": S0,
        "prefix_pointwise_bound": Pmax,
        "suppression_levels": suppression_levels,
        "local_remainders": local,
        "W_centers": centers,
        "W_radii": radii,
    }
    result["physical_six_state"] = physical_six_state_enclosure(result)
    return result


def main() -> None:
    enclosure = build_startup_enclosure()
    bit = sp.Rational(1, 2**TAIL_BITS)
    max_local = max(
        enclosure["local_remainders"][layer][jet]
        for layer in ("L", "O")
        for jet in range(3)
    )
    max_radius = max(
        enclosure["W_radii"][layer][jet]
        for layer in ("L", "O")
        for jet in range(3)
    )

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_STARTUP_ENCLOSURE_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print(f"TRUNCATION_ORDER := {N}")
    print(f"LOCAL_BOREL_CUTOFF := {sp.sstr(Z_CUT)}")
    print(f"TARGET_TAIL_BITS := {TAIL_BITS}")
    print(f"SAFE_HORIZON_X_MAX := {sp.sstr(X_SAFE)}")
    print(f"STARTUP_X := {sp.sstr(enclosure['x_start'])}")
    print(f"COMPACT_88_STATE_ROW_SUM_BOUND := {sp.sstr(enclosure['compact_row_sum_bound'])}")
    print(f"COMPACT_GRONWALL_EXPONENT := {sp.sstr(enclosure['compact_gronwall_exponent'])}")
    print(f"COMPACT_INITIAL_88_STATE_BOUND := {sp.sstr(enclosure['compact_initial_state_bound'])}")
    print(f"PREFIX_POINTWISE_BOUND := {sp.sstr(enclosure['prefix_pointwise_bound'])}")
    print("TAIL_SPLIT := local z<=1/10000; compact 1/10000<z<=1; far z>1")
    print("NONLOCAL_TAIL_CERTIFICATE := each of mid-actual, mid-prefix, far-actual, far-prefix contributions <= 2^-120")
    print(f"LOCAL_REMAINDER_MAX := {sp.sstr(max_local)} < 2^-{TAIL_BITS}")
    print(f"W_COMPONENT_RADIUS_MAX := {sp.sstr(max_radius)} < 5*2^-{TAIL_BITS}")
    print("W_STARTUP_ENCLOSURE := theta^j W_L and theta^j W_O, j=0,1,2, have exact rational two-vector centers and componentwise rational radii")
    print(f"PHYSICAL_LOG_ABS_UPPER := {enclosure['physical_six_state']['log_abs_upper']}")
    print("PHYSICAL_SIX_STATE_SYMBOLIC_ENCLOSURE := exact centers in Q(sqrt(x),log(x)) with certified positive componentwise radii")
    print("STARTUP_INTERFACE := build_startup_enclosure() returns x_start, W centers/radii, and symbolic six-state enclosure")
    print("NEXT_ROUTE := propagate the scaled startup enclosure outward with validated interval arithmetic, switch to the physical six-state away from the horizon, and continue to r=4096")
    print("BOUNDARY := finite-x startup enclosure only; no validated propagation to r=4096, no Z_phys(4096) enclosure, no C_grow value/nonvanishing, and no global exceptional-mode closure claimed")


if __name__ == "__main__":
    main()
