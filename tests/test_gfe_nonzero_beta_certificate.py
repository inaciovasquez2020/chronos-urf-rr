"""Source-backed exact nonzero-beta determinant certificate; draft-only regression."""
import hashlib
import json
from pathlib import Path
import sympy as sp


def test_full_source_nonzero_beta_certificate():
    root = Path(__file__).resolve().parents[1]
    art = root / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"
    raw = art.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == "c471ef35cf5ecc569e337d67f4265ba64fe8a6b999485fdff2a613e62ad63004"
    data = json.loads(raw)
    M, beta, r, lam, omega = sp.symbols("M beta r lam omega", real=True)
    source = sp.sympify(data["descriptor_determinant"], locals={
        "M": M, "beta": beta, "r": r, "lam": lam, "lambda": lam,
        "omega": omega, "I": sp.I,
    })
    specialized = sp.cancel(source.subs(
        {r: sp.Integer(3), lam: sp.Integer(6), omega: sp.I / 4},
        simultaneous=True,
    ) / beta**3)
    exact = (2*M - 3)**4 * (8*M*beta + 135)**2 * (16*M*beta - 135) / sp.Integer(3)**15
    assert sp.cancel(specialized - exact) == 0
    assert sp.denom(sp.cancel(exact)) == sp.Integer(3)**15

    f0 = -sp.Rational(125, 729)*(3-2*M)**4
    x = 8*M*beta
    assert sp.factor(exact.subs(beta, 0) - f0) == 0
    assert sp.factor(exact - f0 - (2*M-3)**4*(405*x**2 + 2*x**3)/3**15) == 0
    assert sp.factor(sp.diff(exact, beta).subs(beta, 0)) == 0

    # Rational interval certificate: |M| <= 101/100,
    # |2M-3| <= 51/50, |x| <= 101/1250 for |beta| <= 1/100.
    mmax = sp.Rational(101, 100)
    xmax = 8*mmax / 100
    K = (sp.Rational(51, 50)**4) * (405 + 2*xmax) * (8*mmax)**2 / 3**15
    assert xmax == sp.Rational(101, 1250)
    assert K < sp.Rational(1, 100)
    delta = sp.Rational(1, 100)
    c0 = sp.Rational(5764801, 36450000)
    lower = c0 - delta**2 / 100
    assert lower == sp.Rational(115295291, 729000000)
    assert lower > 0
    assert 135 - xmax > 0 and 135 - 2*xmax > 0
    print("SOURCE_DESCRIPTOR_SHA256 =", digest)
    print("FULL_SOURCE_FACTORIZATION =", sp.factor(exact))
    print("QUADRATIC_REMAINDER_COEFFICIENT_UPPER =", K)
    print("NONZERO_BETA_RECTANGLE := |M-1| <= 1/100, |beta| <= 1/100, M beta real")
    print("UNIFORM_NONVANISHING_LOWER_BOUND =", lower)
    print("FULL_SOURCE_NONZERO_BETA_CERTIFICATE := PASS")
