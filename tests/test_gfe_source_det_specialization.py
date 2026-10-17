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
