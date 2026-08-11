#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
BASE_ARTIFACT = ROOT / "artifacts/chronos/gfe_soi_leading_fredholm_obstruction.json"


class IV:
    def __init__(self, lo, hi=None):
        self.lo = Q(lo)
        self.hi = Q(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("bad interval")

    def __add__(self, other):
        other = other if isinstance(other, IV) else IV(other)
        return IV(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-(other if isinstance(other, IV) else IV(other)))

    def __rsub__(self, other):
        return IV(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, IV) else IV(other)
        values = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return IV(min(values), max(values))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        values = (Q(1) / self.lo, Q(1) / self.hi)
        return IV(min(values), max(values))

    def __truediv__(self, other):
        other = other if isinstance(other, IV) else IV(other)
        return self * other.reciprocal()

    def __rtruediv__(self, other):
        return IV(other) / self

    def __pow__(self, n):
        n = int(n)
        if n < 0:
            return (self ** (-n)).reciprocal()
        if n == 0:
            return IV(1)
        if self.lo >= 0:
            return IV(self.lo**n, self.hi**n)
        if self.hi <= 0:
            if n % 2 == 0:
                return IV(self.hi**n, self.lo**n)
            return IV(self.lo**n, self.hi**n)
        if n % 2 == 0:
            return IV(0, max((-self.lo) ** n, self.hi**n))
        return IV(self.lo**n, self.hi**n)

    def decimal_pair(self):
        return [float(self.lo), float(self.hi)]


def qstr(value: Q) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_q(value: str) -> Q:
    if "/" in value:
        p, q = value.split("/", 1)
        return Q(int(p), int(q))
    return Q(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="artifacts/chronos/gfe_reverse_chain_uplift_leading_leakage.json",
    )
    parser.add_argument("--base-artifact", default=str(BASE_ARTIFACT))
    args = parser.parse_args()

    base_path = Path(args.base_artifact)
    if not base_path.is_file():
        raise SystemExit(f"MISSING_OBJECT := {base_path}")

    base = json.loads(base_path.read_text(encoding="utf-8"))

    if base.get("leading_fredholm_order") != "q^3":
        raise SystemExit("FIRST_FAILED_IDENTITY := base Fredholm order")

    expected_formula = (
        "I*(a+I*b)/4423680*"
        "(313800*a^2+627600*I*a*b-313800*b^2"
        "-62760*sqrt(15)*eta-56057)"
    )
    actual_formula = base["leading_first_massless_column"]["formula"]
    if actual_formula != expected_formula:
        raise SystemExit("FIRST_FAILED_IDENTITY := base Fredholm formula")

    if base["certified_real_part"]["simple_enclosure"] != (
        "1/605 < Re(f0) < 1/600"
    ):
        raise SystemExit("FIRST_FAILED_IDENTITY := base Fredholm enclosure")

    if base["certified_real_part"]["strictly_positive"] is not True:
        raise SystemExit("FIRST_FAILED_IDENTITY := base Fredholm positivity")

    # ------------------------------------------------------------------
    # Exact augmented-graph identity.
    #
    # P-state u in C^2, Q-state v in C^4:
    #
    #   u_x = A u + B v,
    #   v_x = C u + D v.
    #
    # For the rank-one uplift v = p u + alpha r,
    #
    #   R = C + D p - p_x - p(A+Bp)
    #
    # gives exactly
    #
    #   r alpha_x =
    #       R u + ((D-pB)r-r_x) alpha.
    #
    # Projecting by a left mode ell gives the amplitude equation.
    # ------------------------------------------------------------------
    def sym_matrix(prefix: str, rows: int, cols: int) -> sp.Matrix:
        syms = sp.symbols(
            " ".join(f"{prefix}{i}" for i in range(rows * cols))
        )
        return sp.Matrix(rows, cols, syms)

    A4 = sym_matrix("A", 2, 2)
    B4 = sym_matrix("B", 2, 4)
    C4 = sym_matrix("C", 4, 2)
    D4 = sym_matrix("D", 4, 4)
    p4 = sym_matrix("p", 4, 2)
    px4 = sym_matrix("px", 4, 2)
    r4 = sym_matrix("r", 4, 1)
    rx4 = sym_matrix("rx", 4, 1)
    u2 = sym_matrix("u", 2, 1)
    alpha, alpha_x = sp.symbols("alpha alpha_x")

    v4 = p4 * u2 + r4 * alpha
    u_x = A4 * u2 + B4 * v4
    lifted_lhs = px4 * u2 + p4 * u_x + rx4 * alpha + r4 * alpha_x
    lifted_rhs = C4 * u2 + D4 * v4
    R4 = C4 + D4 * p4 - px4 - p4 * (A4 + B4 * p4)
    identity_rhs = (
        R4 * u2
        + ((D4 - p4 * B4) * r4 - rx4) * alpha
        - r4 * alpha_x
    )

    if any(
        sp.expand(entry) != 0
        for entry in (lifted_rhs - lifted_lhs - identity_rhs)
    ):
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := exact augmented graph identity"
        )

    # ------------------------------------------------------------------
    # Certified leading inner crossing modes.
    # ------------------------------------------------------------------
    boxes = base["certified_boxes"]
    a_lo, a_hi = map(parse_q, boxes["Re_Omega"])
    b_lo, b_hi = map(parse_q, boxes["Im_Omega"])
    eta_lo, eta_hi = map(parse_q, boxes["eta_star"])
    sqrt15_lo, sqrt15_hi = map(parse_q, boxes["sqrt15"])

    # xi box from the already-certified dependency-aware crossing gate.
    xi_lo = Q(-605658, 10**6)
    xi_hi = Q(-600793, 10**6)

    a, b, eta, xi, lam = sp.symbols(
        "a b eta xi lam",
        real=True,
    )
    sqrt15 = sp.sqrt(15)
    Omega = a + sp.I * b

    m11 = (
        sqrt15
        * sp.I
        * (20 * Omega - 9)
        * (20 * Omega + 9)
        / 1200
    )
    m12 = -sqrt15 * (8 * Omega**2 - 1) / (384 * Omega)
    m21 = -sqrt15 * Omega / 12
    m22 = (
        sp.I
        * (
            1600 * sqrt15 * Omega**2
            - 600 * sp.I * xi
            - 277 * sqrt15
        )
        / 4800
    )

    M = sp.Matrix([[m11, m12], [m21, m22]])
    characteristic = sp.factor((lam * sp.eye(2) - M).det())
    dlam = sp.factor(sp.diff(characteristic, lam))

    right = sp.Matrix([m12, lam - m11])
    left = sp.Matrix([[m21, lam - m11]])
    pairing = sp.factor((left * right)[0])

    # Correct off-shell identity; on a characteristic root this reduces to
    # (lambda-m11) * d_lambda(characteristic).
    pairing_offshell = sp.factor(
        (lam - m11) * dlam - characteristic
    )
    if sp.simplify(pairing - pairing_offshell) != 0:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := left/right pairing identity"
        )

    dlam_i = sp.factor(dlam.subs(lam, sp.I * eta))
    z = sp.expand_complex(sp.I * eta - m11)
    z_re = sp.factor(sp.re(z))
    z_im = sp.factor(sp.im(z))
    abs_dlam_sq = sp.factor(
        sp.re(dlam_i) ** 2 + sp.im(dlam_i) ** 2
    )

    A = IV(a_lo, a_hi)
    B = IV(b_lo, b_hi)
    E = IV(eta_lo, eta_hi)
    X = IV(xi_lo, xi_hi)
    S = IV(sqrt15_lo, sqrt15_hi)

    def ev(expr, env):
        if expr == sp.sqrt(15):
            return S
        if expr.is_Rational:
            return IV(Q(int(expr.p), int(expr.q)))
        if expr.is_Symbol:
            return env[expr]
        if expr.is_Add:
            out = IV(0)
            for term in expr.args:
                out = out + ev(term, env)
            return out
        if expr.is_Mul:
            out = IV(1)
            for term in expr.args:
                out = out * ev(term, env)
            return out
        if expr.is_Pow and expr.args[1].is_Integer:
            return ev(expr.args[0], env) ** int(expr.args[1])
        raise RuntimeError(f"unsupported interval expression: {expr}")

    env = {a: A, b: B, eta: E, xi: X}

    z_re_iv = ev(sp.expand(z_re), env)
    z_im_iv = ev(sp.expand(z_im), env)
    z_abs_sq_iv = z_re_iv**2 + z_im_iv**2
    dlam_abs_sq_iv = ev(sp.expand(abs_dlam_sq), env)

    # Tight rational guards.
    z_sq_lo_guard = Q(999, 100000)
    z_sq_hi_guard = Q(51, 5000)
    dlam_sq_lo_guard = Q(3, 250)
    dlam_sq_hi_guard = Q(3, 200)

    if not z_abs_sq_iv.lo > z_sq_lo_guard:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := |lambda-m11|^2 lower bound"
        )
    if not z_abs_sq_iv.hi < z_sq_hi_guard:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := |lambda-m11|^2 upper bound"
        )
    if not dlam_abs_sq_iv.lo > dlam_sq_lo_guard:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := |d_lambda F|^2 lower bound"
        )
    if not dlam_abs_sq_iv.hi < dlam_sq_hi_guard:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := |d_lambda F|^2 upper bound"
        )

    # On-shell pairing bounds:
    #
    # |ell^T r|^2
    #   = |lambda-m11|^2 |d_lambda F|^2.
    pairing_sq_lo = z_sq_lo_guard * dlam_sq_lo_guard
    pairing_sq_hi = z_sq_hi_guard * dlam_sq_hi_guard

    # ------------------------------------------------------------------
    # Re-derive the merged leading Fredholm coefficient and normalize it
    # by the nonzero crossing-mode pairing.
    # ------------------------------------------------------------------
    fredholm = (
        sp.I
        * Omega
        / sp.Integer(4423680)
        * (
            sp.Integer(313800) * a**2
            + sp.Integer(627600) * sp.I * a * b
            - sp.Integer(313800) * b**2
            - sp.Integer(62760) * sqrt15 * eta
            - sp.Integer(56057)
        )
    )

    fredholm_real = sp.factor(
        sp.re(sp.expand_complex(fredholm))
    )
    expected_real = sp.factor(
        (-b)
        * (
            sp.Integer(941400) * a**2
            - sp.Integer(313800) * b**2
            - sp.Integer(62760) * sqrt15 * eta
            - sp.Integer(56057)
        )
        / sp.Integer(4423680)
    )
    if sp.simplify(fredholm_real - expected_real) != 0:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := Fredholm real formula"
        )

    # Since Re(f0) > 1/605, |f0| > 1/605.  Since the on-shell
    # pairing square is < pairing_sq_hi, the normalized source obeys
    #
    # |f0/(ell^T r)|^2
    #   > (1/605)^2 / pairing_sq_hi
    #   > (2/15)^2.
    leakage_sq_lo = (Q(1, 605) ** 2) / pairing_sq_hi
    if not leakage_sq_lo > Q(4, 225):
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := normalized leakage lower bound"
        )

    report = {
        "program": "GfE Reverse-Chain Uplift",
        "baseline": {
            "graph": "p_bar(q,x) = q^2 P2(x)",
            "status": "Fredholm obstructed near q=0",
            "leading_fredholm_order": "q^3",
        },
        "uplift": {
            "ansatz": "Q = p P + alpha r",
            "rank": 1,
            "exact_identity": (
                "r alpha_x = R(q,p) P + "
                "((G_QQ-p G_PQ)r-r_x) alpha"
            ),
            "projected_amplitude_equation": (
                "(ell^T r) alpha_x = ell^T R(q,p) P + "
                "ell^T((G_QQ-p G_PQ)r-r_x) alpha"
            ),
        },
        "inner_crossing_mode": {
            "right": "(m12, lambda-m11)^T",
            "left": "(m21, lambda-m11)",
            "off_shell_pairing": (
                "(lambda-m11)*d_lambda(characteristic)"
                "-characteristic"
            ),
            "on_shell_pairing": (
                "(lambda-m11)*d_lambda(characteristic)"
            ),
            "lambda_minus_m11_abs_sq_interval":
                z_abs_sq_iv.decimal_pair(),
            "d_lambda_characteristic_abs_sq_interval":
                dlam_abs_sq_iv.decimal_pair(),
            "pairing_abs_sq": {
                "lower_guard": qstr(pairing_sq_lo),
                "upper_guard": qstr(pairing_sq_hi),
                "nonzero": True,
            },
        },
        "leading_leakage": {
            "massless_column": 0,
            "source": (
                "alpha_x = q^3*f0/(ell^T r) + higher order "
                "at alpha=0"
            ),
            "fredholm_real_enclosure":
                "1/605 < Re(f0) < 1/600",
            "normalized_source_magnitude_gt": "2/15",
            "uniformly_nonzero": True,
        },
        "result": (
            "the nonzero q^3 Fredholm obstruction becomes a "
            "uniformly nonzero resonant fast-mode source under "
            "the rank-one Reverse-Chain Uplift"
        ),
        "boundary": [
            "leading inner uplift only",
            "exact finite-q 4x4 companion lift not yet certified",
            "complement equation not yet certified",
            "endpoint admissibility not yet certified",
            "global invariant manifold not yet proved",
            "projected 220 QNM/tail transfer remains prohibited",
        ],
        "next_gate": (
            "derive exact finite-q 4x4 right/adjoint companion modes "
            "and certify the complement equation"
        ),
    }

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("PROGRAM := GfE Reverse-Chain Uplift")
    print("AUGMENTED_GRAPH := Q = p P + alpha r")
    print("AUGMENTED_GRAPH_IDENTITY := exact")
    print(
        "AMPLITUDE_PROJECTION := "
        "(ell^T r) alpha_x = ell^T R P + "
        "ell^T((G_QQ-p G_PQ)r-r_x) alpha"
    )
    print("INNER_RIGHT_MODE := (m12, lambda-m11)^T")
    print("INNER_LEFT_MODE := (m21, lambda-m11)")
    print(
        "LEFT_RIGHT_PAIRING_ON_SHELL := "
        "(lambda-m11)*d_lambda(characteristic)"
    )
    print(
        "LAMBDA_MINUS_M11_ABS_SQUARED_INTERVAL :=",
        z_abs_sq_iv.decimal_pair(),
    )
    print(
        "CHARACTERISTIC_DERIVATIVE_ABS_SQUARED_INTERVAL :=",
        dlam_abs_sq_iv.decimal_pair(),
    )
    print(
        "LEFT_RIGHT_PAIRING_ABS_SQUARED_GT :=",
        qstr(pairing_sq_lo),
    )
    print(
        "LEFT_RIGHT_PAIRING_ABS_SQUARED_LT :=",
        qstr(pairing_sq_hi),
    )
    print("FREDHOLM_REAL_GT := 1/605")
    print("FREDHOLM_REAL_LT := 1/600")
    print("NORMALIZED_LEAKAGE_MAGNITUDE_GT := 2/15")
    print(
        "LEADING_REVERSE_CHAIN_SOURCE := "
        "alpha_x = q^3*f0/(ell^T r) + higher order "
        "at alpha=0, first massless column"
    )
    print(
        "RESULT := nonzero Fredholm obstruction becomes a "
        "uniformly nonzero resonant fast-mode source"
    )
    print(
        "BOUNDARY := leading inner uplift only; exact 4x4 finite-q "
        "companion lift, complement equation, endpoint admissibility, "
        "and global invariant manifold remain unproved"
    )
    print(
        "NEXT_ACTIONS := derive exact finite-q 4x4 right/adjoint "
        "companion modes and certify the complement equation"
    )
    print("JSON_REPORT :=", output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
