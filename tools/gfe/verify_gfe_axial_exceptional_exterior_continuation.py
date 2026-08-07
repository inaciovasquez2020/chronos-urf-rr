#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

import sympy as s

if len(sys.argv) != 2:
    raise SystemExit("MISSING_OBJECT := canonical GfE source argument")

source = Path(sys.argv[1])
text = source.read_text()

m = re.search(
    r'''cat >"\$tmp_py" <<'PY_CORE'\n(.*?)\nPY_CORE''',
    text,
    re.S,
)
if m is None:
    raise SystemExit("MISSING_OBJECT := embedded canonical PY_CORE")

core = m.group(1)
marker = "H1_220_LEADING ="
if marker not in core:
    raise SystemExit(
        "MISSING_OBJECT := canonical relative-O(beta^2) axial source marker"
    )

prefix = core.split(marker, 1)[0]
ns = {"__name__": "gfe_exceptional_exterior_source"}
exec(compile(prefix, str(source), "exec"), ns)

required = [
    "r", "M", "beta", "f", "omega",
    "H0_radial", "H1_radial_beta2",
    "E0_CORR_FOURIER", "E1_CORR_FOURIER",
]
missing = [name for name in required if name not in ns]
if missing:
    raise SystemExit(
        "MISSING_OBJECT := canonical source symbols: " + ", ".join(missing)
    )

r = ns["r"]
M = ns["M"]
beta = ns["beta"]
f = ns["f"]
omega = ns["omega"]
H0 = ns["H0_radial"]
H1 = ns["H1_radial_beta2"]
E0corr = ns["E0_CORR_FOURIER"]
E1corr = ns["E1_CORR_FOURIER"]

def simp(expr):
    return s.factor(s.cancel(s.together(expr)))

# Exact uneliminated ell=2 Fourier equations.
Q = -s.I*omega*H1 - s.diff(H0, r) + 2*H0/r
A0 = s.diff(Q, r) + 2*Q/r + 4*H0/(f*r**2)
A1 = s.I*omega*Q - 4*f*H1/r**2
E0 = s.expand(6*A0 + beta**2*E0corr)
E1 = s.expand(6*A1 + beta**2*E1corr)

omega_star = s.I/(4*M)
E0s = E0.subs(omega, omega_star)
E1s = E1.subs(omega, omega_star)

h04 = s.diff(H0, r, 4)
h03 = s.diff(H0, r, 3)
h13 = s.diff(H1, r, 3)
h12 = s.diff(H1, r, 2)

c4 = simp(s.diff(E0s, h04))
d3 = simp(s.diff(E0s, h13))
a3 = simp(s.diff(E1s, h03))
b2 = simp(s.diff(E1s, h12))

C = s.Matrix([[c4, d3], [a3, b2]])
detC = simp(C.det())

expected_c4 = simp(-8*beta**2*M*(r - 2*M)/r**4)
expected_d3 = simp(2*beta**2*(r - 2*M)/r**4)
expected_a3 = simp(2*beta**2*(r - 2*M)/r**4)
expected_b2 = simp(
    8*beta**2*M*(r - 2*M)
    * (-16*M - r**3/(16*M**2) + 8*r)
    / r**7
)
expected_det = simp(
    -512*beta**4*M**2*(r - 2*M)**3/r**11
)

checks = [
    ("C00", c4, expected_c4),
    ("C01", d3, expected_d3),
    ("C10", a3, expected_a3),
    ("C11", b2, expected_b2),
    ("DET_C", detC, expected_det),
]
for name, actual, expected in checks:
    if simp(actual - expected) != 0:
        print(f"FIRST_FAILED_IDENTITY := {name}")
        print("ACTUAL :=", actual)
        print("EXPECTED :=", expected)
        raise SystemExit(3)

# We deliberately solve the lower equation for H0''' because a3 is
# manifestly nonzero everywhere in the open exterior at omega=i/(4M).
# This avoids any division by b2, which may itself vanish.
if simp(a3 / (2*beta**2*(r - 2*M)/r**4) - 1) != 0:
    raise SystemExit("FIRST_FAILED_IDENTITY := globally nonzero a3 factor")

# Differentiating the solved E1 relation and substituting in E0 leaves
# the H1''' coefficient
#   kappa = d3 - c4*b2/a3 = -det(C)/a3.
kappa = simp(d3 - c4*b2/a3)
expected_kappa = simp(
    256*beta**2*M**2*(r - 2*M)**2/r**7
)
if simp(kappa - expected_kappa) != 0:
    print("FIRST_FAILED_IDENTITY := differentiated constraint coefficient")
    print("ACTUAL :=", kappa)
    print("EXPECTED :=", expected_kappa)
    raise SystemExit(3)

# Exact derivative-order census.
def radial_order(derivative, field):
    if derivative.expr != field:
        return None
    if any(v != r for v in derivative.variables):
        return None
    return len(derivative.variables)

def max_order(expr, field):
    orders = [
        radial_order(d, field)
        for d in expr.atoms(s.Derivative)
    ]
    orders = [o for o in orders if o is not None]
    return max(orders or [0])

orders = {
    "E0_H0": max_order(E0s, H0),
    "E0_H1": max_order(E0s, H1),
    "E1_H0": max_order(E1s, H0),
    "E1_H1": max_order(E1s, H1),
}
expected_orders = {
    "E0_H0": 4,
    "E0_H1": 3,
    "E1_H0": 3,
    "E1_H1": 2,
}
if orders != expected_orders:
    print("FIRST_FAILED_IDENTITY := derivative-order staircase")
    print("ACTUAL :=", orders)
    print("EXPECTED :=", expected_orders)
    raise SystemExit(3)

# Coefficient-pole census.  Every jet coefficient in both equations,
# after setting the exceptional frequency, must have no finite
# exterior denominator zero.  In y=r/M, permitted nonconstant factors
# are only y and y-2.
y = s.symbols("y", real=True)

def jet_list(field, max_n):
    return [field] + [s.diff(field, r, j) for j in range(1, max_n + 1)]

jets = jet_list(H0, 4) + jet_list(H1, 3)

def certify_denominator(name, expr):
    expr = simp(expr)
    if expr == 0:
        return
    _, den = s.fraction(expr)
    dy = simp(den.subs(r, M*y))
    poly = s.Poly(dy, y, domain="EX")

    # Certify the zero set, not SymPy's chosen factorization shape.
    # Remove every possible y and (y-2) factor.  What remains must be
    # a nonzero constant.  This accepts composite presentations such as
    # y**8*(y-2)**2 without assuming factor_list splits them.
    rem = poly
    zero_mult = 0
    horizon_mult = 0

    while rem.degree() > 0 and simp(rem.eval(0)) == 0:
        q, rr = s.div(rem, s.Poly(y, y, domain="EX"))
        if not rr.is_zero:
            raise SystemExit(
                f"FIRST_FAILED_IDENTITY := y-division remainder in {name}"
            )
        rem = q
        zero_mult += 1

    while rem.degree() > 0 and simp(rem.eval(2)) == 0:
        q, rr = s.div(rem, s.Poly(y - 2, y, domain="EX"))
        if not rr.is_zero:
            raise SystemExit(
                f"FIRST_FAILED_IDENTITY := (y-2)-division remainder in {name}"
            )
        rem = q
        horizon_mult += 1

    if rem.degree() > 0:
        print(
            f"FIRST_FAILED_IDENTITY := unexpected finite-radius denominator in {name}"
        )
        print("REMAINDER_FACTOR :=", s.factor(rem.as_expr()))
        raise SystemExit(3)

    if simp(rem.as_expr()) == 0:
        raise SystemExit(
            f"FIRST_FAILED_IDENTITY := zero denominator polynomial in {name}"
        )

    return {
        "r_zero_multiplicity": zero_mult,
        "horizon_multiplicity": horizon_mult,
    }

for eq_name, eq in (("E0", E0s), ("E1", E1s)):
    for index, jet in enumerate(jets):
        certify_denominator(f"{eq_name}_jet_{index}", s.diff(eq, jet))

# The two divisions used in the six-state first-order reduction are
# therefore globally legal on r>2M:
#   H0''' from E1 via a3,
#   H1''' from d_r(E1) and E0 via kappa.
# Both denominators are monomials in r and r-2M there.
certify_denominator("1/a3", 1/a3)
certify_denominator("1/kappa", 1/kappa)

print("GFE_EXCEPTIONAL_EXTERIOR_CONTINUATION")
print("EXCEPTIONAL_FREQUENCY := omega=I/(4*M)")
print("DERIVATIVE_STAIRCASE := E0=(H0^4,H1^3); E1=(H0^3,H1^2)")
print("STAIRCASE_PRINCIPAL_MATRIX :=", C)
print("STAIRCASE_DETERMINANT :=", detC)
print("FINITE_POSITIVE_DEGENERACY_SET := {r=2*M}")
print("OPEN_EXTERIOR_DEGENERACY_SET := empty")
print("SAFE_CONSTRAINT_PIVOT_A3 :=", a3)
print("DIFFERENTIATED_CONSTRAINT_PIVOT_KAPPA :=", kappa)
print("FIRST_ORDER_STATE := (H0,H0_r,H0_rr,H1,H1_r,H1_rr)")
print(
    "FIRST_ORDER_REDUCTION := E1 solves H0_rrr; "
    "d_r(E1) together with E0 solves H1_rrr"
)
print(
    "FIRST_ORDER_COEFFICIENT_POLES := only r=0 and r=2*M; "
    "none occur for finite r>2*M"
)
print(
    "CONTINUATION_THEOREM := every local exceptional solution trace "
    "at any r0>2*M has a unique solution continuation to every finite "
    "R>r0, and the convergent horizon solution therefore extends "
    "uniquely throughout the entire open exterior 2*M<r<infinity"
)
print(
    "RESULT := no finite-radius degeneracy obstructs the exceptional "
    "uneliminated axial solution; unique exterior continuation proved"
)
print(
    "BOUNDARY := the behavior at the singular endpoint r=infinity and "
    "the outgoing/decaying boundary condition there are not yet classified; "
    "no global mode or physical-instability claim follows"
)
print(
    "NEXT_ACTIONS := derive the exact infinity asymptotic basis and project "
    "the uniquely continued exceptional solution onto it"
)
