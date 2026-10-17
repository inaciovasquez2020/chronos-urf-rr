#!/usr/bin/env python3
"""Exact bridge: symbolic generator specialization -> fixed-point limiting resolvent."""
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json"
M, beta, z, r, lam, omega = s.symbols("M beta z r lam omega")
I = s.I
loc = {"M": M, "beta": beta, "z": z, "I": I, "r": r, "lam": lam,
       "lambda": lam, "omega": omega}
data = json.loads(ART.read_text())


def parse(v):
    return s.sympify(v, locals=loc).subs(
        {M: 1, r: 3, lam: 6, omega: I / 4}, simultaneous=True)


def poly_expr(coeffs):
    return s.cancel(sum((parse(c) * beta**j for j, c in enumerate(coeffs)),
                        s.Integer(0)))


N = s.Matrix(6, 6, lambda i, j: poly_expr(
    [a[i][j] for a in data["reduced_numerator_beta_coefficients"]]))
D = poly_expr(data["reduced_denominator_beta_coefficients"])
F = (z * D * s.eye(6) - N).applyfunc(s.cancel)
detF = s.factor(F.det(method="domain-ge"))
det_poly = s.Poly(detF, beta)
assert all(det_poly.nth(k) == 0 for k in range(4)), "determinant order is below 4"
det4 = s.cancel(det_poly.nth(4))
assert det4 != 0, "determinant order exceeds 4"

# Coefficient of beta^4 in D*adj(F), divided by the beta^4
# coefficient of det(F), is the exact entrywise limit of the resolvent.
actual = s.zeros(6, 6)
for i in range(6):
    for j in range(6):
        minor = F.minor_submatrix(j, i)
        cofactor = (-1)**(i + j) * minor.det(method="domain-ge")
        numerator = s.cancel(D * cofactor)
        num4 = s.cancel(s.Poly(numerator, beta).nth(4))
        actual[i, j] = s.factor(num4 / det4)
        print(f"fixed-point limit entry {i},{j} computed", flush=True)

den = 144 * z**2 - 337
expected = s.Matrix([
    [48*(3*z+2)/den, 0, 0, 364/(3*den), 0, 0],
    [(96*z+337)/den, 0, 0, 364*z/(3*den), 0, 0],
    [z*(96*z+337)/den, -1, 0, 364*z**2/(3*den), 0, 0],
    [324/den, 0, 0, 48*(3*z-2)/den, 0, 0],
    [324*z/den, 0, 0, -(96*z-337)/den, 0, 0],
    [324*z**2/den, 0, 0, -z*(96*z-337)/den, -1, 0],
])
residual = (actual - expected).applyfunc(lambda x: s.factor(s.cancel(x)))
assert residual == s.zeros(6), f"specialized resolvent mismatch: {residual}"

# Independently verify that the sum of residues is the documented projector.
a = s.sqrt(337) / 12
residue_sum = s.zeros(6)
for pole in (a, -a):
    residue_sum += actual.applyfunc(lambda x: s.limit((z - pole) * x, z, pole))
P = s.Matrix([
    [1, 0, 0, 0, 0, 0],
    [s.Rational(2, 3), 0, 0, s.Rational(91, 108), 0, 0],
    [s.Rational(337, 144), 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [s.Rational(9, 4), 0, 0, s.Rational(-2, 3), 0, 0],
    [0, 0, 0, s.Rational(337, 144), 0, 0],
])
assert (residue_sum - P).applyfunc(s.simplify) == s.zeros(6)
assert P * P == P and s.trace(P) == 2 and P.rank() == 2
print("PASS: all 36 exact limiting-resolvent entries match; residue sum is P*.", flush=True)
