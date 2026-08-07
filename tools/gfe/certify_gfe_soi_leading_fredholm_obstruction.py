#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp


def qstr(x: Q) -> str:
    return f"{x.numerator}/{x.denominator}"


def decstr(x: Q, digits: int = 18) -> str:
    getcontext().prec = digits + 10
    value = Decimal(x.numerator) / Decimal(x.denominator)
    return format(value, f".{digits}f")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="artifacts/chronos/gfe_soi_leading_fredholm_obstruction.json",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Corrected singular center.
    #
    # Principal balanced transverse characteristic:
    #
    #   (mu^2 + 6/(5 f))^2.
    #
    # At x=4, f=1/2, hence
    #
    #   mu0 = +/- i sqrt(12/5).
    # ------------------------------------------------------------------

    mu = sp.symbols("mu")
    f4 = sp.Rational(1, 2)

    principal = sp.factor(
        (mu**2 + sp.Rational(6, 5) / f4) ** 2
    )
    expected_principal = (mu**2 + sp.Rational(12, 5)) ** 2

    if sp.expand(principal - expected_principal) != 0:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := corrected inner principal center"
        )

    # ------------------------------------------------------------------
    # Leading Fredholm coefficient.
    #
    # Omega = a + i b,
    #
    # f0 =
    #   i Omega / 4423680 *
    #   (
    #       313800 a^2
    #       + 627600 i a b
    #       - 313800 b^2
    #       - 62760 sqrt(15) eta
    #       - 56057
    #   ).
    #
    # This is the first massless-column adjoint projection of the
    # exact q^2 P2 graph residual at the first surviving Fredholm order.
    # ------------------------------------------------------------------

    a, b, eta = sp.symbols("a b eta", real=True)
    sqrt15 = sp.sqrt(15)

    fredholm = (
        sp.I * (a + sp.I * b) / sp.Integer(4423680)
        * (
            sp.Integer(313800) * a**2
            + sp.Integer(627600) * sp.I * a * b
            - sp.Integer(313800) * b**2
            - sp.Integer(62760) * sqrt15 * eta
            - sp.Integer(56057)
        )
    )

    fredholm_real = sp.factor(sp.re(sp.expand_complex(fredholm)))

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
            "FIRST_FAILED_IDENTITY := Fredholm real-part formula"
        )

    # ------------------------------------------------------------------
    # Certified frequency / crossing boxes.
    # ------------------------------------------------------------------

    a_lo = Q(467, 1250)      # 0.3736
    a_hi = Q(1869, 5000)     # 0.3738

    b_lo = Q(-891, 10000)    # -0.0891
    b_hi = Q(-111, 1250)     # -0.0888

    eta_lo = Q(-39656, 10**6)
    eta_hi = Q(-39439, 10**6)

    sqrt15_lo = Q(3872983346, 10**9)
    sqrt15_hi = Q(3872983347, 10**9)

    if not sqrt15_lo * sqrt15_lo < Q(15) < sqrt15_hi * sqrt15_hi:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := rational sqrt(15) enclosure"
        )

    # For
    #
    # Z = 941400 a^2 - 313800 b^2
    #     - 62760 sqrt(15) eta - 56057,
    #
    # monotonicity on the certified box gives the exact enclosure below.
    def z_value(a_: Q, b_: Q, s_: Q, eta_: Q) -> Q:
        return (
            Q(941400) * a_ * a_
            - Q(313800) * b_ * b_
            - Q(62760) * s_ * eta_
            - Q(56057)
        )

    z_lo = z_value(a_lo, b_lo, sqrt15_lo, eta_hi)
    z_hi = z_value(a_hi, b_hi, sqrt15_hi, eta_lo)

    if z_lo <= 0:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := positive Fredholm bracket"
        )

    denominator = Q(4423680)

    # Independent interval multiplication is deliberately used here:
    # -b in [0.0888, 0.0891], Z in [z_lo,z_hi].
    re_lo = (-b_hi) * z_lo / denominator
    re_hi = (-b_lo) * z_hi / denominator

    # Simple rational theorem enclosure.
    if not re_lo > Q(1, 605):
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := Fredholm lower bound > 1/605"
        )

    if not re_hi < Q(1, 600):
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := Fredholm upper bound < 1/600"
        )

    if re_lo <= 0:
        raise SystemExit(
            "FIRST_FAILED_IDENTITY := nonzero Fredholm coefficient"
        )

    report = {
        "scope": (
            "corrected AEH=1/2 leading Shadow-of-Infinity "
            "Fredholm obstruction for the regular q^2 P2 graph center"
        ),
        "normalization": {
            "A_EH": "1/2",
            "principal_balanced_characteristic_at_x4":
                "(mu^2 + 12/5)^2",
            "inner_center_at_x4":
                "mu0 = +/- I*sqrt(12/5)",
            "moving_inner_center":
                "mu_pm(x) = +/- I*sqrt(6/(5*f(x)))",
        },
        "graph_center": "p_bar(q,x) = q^2 P2(x)",
        "residual_structure": {
            "expansion": "R(q,q^2 P2) = q^2 R2 + O(q^3)",
            "slow_U_rows_at_R2": "0",
            "R2_V0": [
                "599/36864",
                "I*(320*Omega^2-51)/(8192*Omega)",
            ],
            "R2_V1": [
                "-523*I*Omega/3072",
                "(8064*Omega^2-8873)/147456",
            ],
        },
        "crossing_modes": {
            "right":
                "(m12, lambda-m11)^T",
            "adjoint":
                "(m21, lambda-m11)",
            "pairing":
                "(lambda-m11)*d_lambda(characteristic)",
            "local_transversality":
                "9/100 < d_xi Re(lambda_inner) < 1/8",
        },
        "leading_fredholm_order": "q^3",
        "leading_first_massless_column": {
            "formula": (
                "I*(a+I*b)/4423680*"
                "(313800*a^2+627600*I*a*b-313800*b^2"
                "-62760*sqrt(15)*eta-56057)"
            ),
            "real_part_formula": (
                "(-b)*(941400*a^2-313800*b^2"
                "-62760*sqrt(15)*eta-56057)/4423680"
            ),
        },
        "certified_boxes": {
            "Re_Omega": [qstr(a_lo), qstr(a_hi)],
            "Im_Omega": [qstr(b_lo), qstr(b_hi)],
            "eta_star": [qstr(eta_lo), qstr(eta_hi)],
            "sqrt15": [qstr(sqrt15_lo), qstr(sqrt15_hi)],
        },
        "certified_real_part": {
            "lower_exact": qstr(re_lo),
            "upper_exact": qstr(re_hi),
            "lower_decimal": decstr(re_lo, 16),
            "upper_decimal": decstr(re_hi, 16),
            "simple_enclosure": "1/605 < Re(f0) < 1/600",
            "strictly_positive": True,
        },
        "result": (
            "leading q^3 Fredholm coefficient is uniformly nonzero "
            "on the certified q->0 crossing/frequency box"
        ),
        "consequence": (
            "the regular graph center q^2 P2 fails the first surviving "
            "Fredholm compatibility condition for all sufficiently "
            "small positive q"
        ),
        "boundary": {
            "finite_q_interval_newton_through_q_1e_minus_2":
                "not claimed",
            "nonexistence_of_all_deformed_invariant_graphs":
                "not claimed",
            "full_theory_220_qnm_tail_transfer":
                "prohibited",
        },
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("AEH := 1/2")
    print("INNER_CENTER_X4 := +/- I*sqrt(12/5)")
    print("FIRST_NONZERO_FREDHOLM_ORDER := q^3")
    print(
        "FREDHOLM_REAL_LOWER_DECIMAL :=",
        report["certified_real_part"]["lower_decimal"],
    )
    print(
        "FREDHOLM_REAL_UPPER_DECIMAL :=",
        report["certified_real_part"]["upper_decimal"],
    )
    print("FREDHOLM_REAL_GT := 1/605")
    print("FREDHOLM_REAL_LT := 1/600")
    print("FREDHOLM_COMPATIBILITY_q2P2 := refuted near q=0")
    print(
        "BOUNDARY := no claim of finite-q crossing certification "
        "through q=1e-2 and no claim excluding every possible "
        "deformed invariant graph"
    )
    print("220_QNM_TAIL_TRANSFER := prohibited")
    print("JSON_REPORT :=", output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
