#!/usr/bin/env python3
"""Exact full-source determinant specialization at r=3, lambda=6, omega=i/4."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def test_full_source_determinant_specialization():
    ROOT = Path(__file__).resolve().parents[1]
    ART = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
    M, beta, r, lam, omega = sp.symbols("M beta r lam omega")
    I = sp.I

    data = json.loads(ART.read_text())
    source = sp.sympify(
        data["descriptor_determinant"],
        locals={"M": M, "beta": beta, "r": r, "lam": lam,
                "lambda": lam, "omega": omega, "I": I},
    )

    # Specialize the complete rational expression first. Do not infer the result
    # from visible factors or cancel a denominator without its full numerator.
    specialized = sp.cancel(source.subs(
        {r: sp.Integer(3), lam: sp.Integer(6), omega: I / 4},
        simultaneous=True,
    ))
    quotient = sp.cancel(specialized / beta**3)
    limit = sp.factor(sp.limit(quotient, beta, 0))
    expected = -sp.Rational(125, 729) * (3 - 2 * M)**4
    assert sp.cancel(limit - expected) == 0, (
        f"full-source specialization mismatch: got {limit}, expected {expected}"
    )

    # Exact uniform lower bound on the closed real interval |M-1| <= 1/100.
    lower_bound = sp.Rational(125, 729) * sp.Rational(49, 50)**4
    assert lower_bound == sp.Rational(5764801, 36450000)
    assert sp.Abs(limit).subs(M, sp.Rational(1)) > lower_bound
    # On this interval 49/50 <= 3-2M <= 51/50, so the minimum is at 49/50.
    assert sp.factor(expected.subs(M, sp.Rational(101, 100))) == -lower_bound

    print("SOURCE_DESCRIPTOR_SHA256 =", hashlib.sha256(ART.read_bytes()).hexdigest())
    print("FULL_SOURCE_SPECIALIZATION =", limit)
    print("INTERVAL := |M-1| <= 1/100, M real")
    print("CERTIFIED_LOWER_BOUND =", lower_bound)
    print("DECIMAL_LOWER_BOUND >", sp.N(lower_bound, 12))
    print("PASS: full rational source determinant matches exact specialization and bound")


def test_finite_beta_source_determinant_guard():
    """Certify the full-source det(E)/beta^3 away from beta=0 locally."""
    ROOT = Path(__file__).resolve().parents[1]
    ART = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
    M, beta, r, lam, omega = sp.symbols("M beta r lam omega")
    x = sp.symbols("x", real=True)
    I = sp.I

    data = json.loads(ART.read_text())
    source = sp.sympify(
        data["descriptor_determinant"],
        locals={"M": M, "beta": beta, "r": r, "lam": lam,
                "lambda": lam, "omega": omega, "I": I},
    )
    specialized = sp.cancel(source.subs(
        {r: sp.Integer(3), lam: sp.Integer(6), omega: I / 4},
        simultaneous=True,
    ))
    quotient = sp.cancel(specialized / beta**3)
    expected = -sp.Rational(125, 729) * (3 - 2 * M)**4
    error = sp.cancel(quotient - expected).subs(M, 1 + x)
    error_num_expr, error_den_expr = sp.fraction(sp.cancel(error))
    error_num = sp.Poly(error_num_expr, x, beta)
    error_den = sp.Poly(error_den_expr, x, beta)

    radius_x = sp.Rational(1, 100)
    radius_beta = sp.Rational(1, 1000)

    def coefficient_bound(poly):
        total = sp.Integer(0)
        for (ix, ib), coeff in poly.terms():
            assert coeff.is_real, f"non-real coefficient in interval bound: {coeff}"
            total += abs(coeff) * radius_x**ix * radius_beta**ib
        return sp.factor(total)

    denominator_constant = error_den.coeff_monomial(1)
    assert denominator_constant.is_real
    denominator_variation = sp.factor(
        coefficient_bound(error_den)
        - abs(denominator_constant)
    )
    denominator_lower = sp.factor(
        abs(denominator_constant) - denominator_variation
    )
    assert denominator_lower > 0, (
        f"denominator interval guard failed: lower={denominator_lower}"
    )

    error_bound = sp.factor(coefficient_bound(error_num) / denominator_lower)
    limiting_lower = sp.Rational(5764801, 36450000)
    assert error_bound < limiting_lower, (
        f"finite-beta perturbation bound too large: {error_bound}"
    )
    finite_beta_lower = sp.factor(limiting_lower - error_bound)
    assert finite_beta_lower > 0

    print("SOURCE_DET_FINITE_BETA_DOMAIN := real |M-1| <= 1/100, complex |beta| <= 1/1000")
    print("SOURCE_DET_ERROR_DENOMINATOR_LOWER =", denominator_lower)
    print("SOURCE_DET_FINITE_BETA_ERROR_BOUND =", error_bound)
    print("SOURCE_DET_FINITE_BETA_LOWER_BOUND =", finite_beta_lower)
    print("PASS: full-source det(E)/beta^3 is bounded away from zero on the stated domain")
