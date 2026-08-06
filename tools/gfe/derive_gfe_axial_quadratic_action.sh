#!/usr/bin/env bash
set -euo pipefail

python_bin="${PYTHON:-python3}"
"$python_bin" - <<'PY_CHECK'
import sys
try:
    import sympy as s
except Exception as exc:
    raise SystemExit(f"MISSING_OBJECT := sympy ({exc})")
if tuple(map(int, s.__version__.split('.')[:2])) < (1, 14):
    raise SystemExit(f"MISSING_OBJECT := sympy>=1.14 (found {s.__version__})")
print(f"SYMPY_VERSION := {s.__version__}")
PY_CHECK

tmp_py="$(mktemp "${TMPDIR:-/tmp}/gfe_axial_quadratic_action.XXXXXX.py")"
trap 'rm -f "$tmp_py"' EXIT
cat >"$tmp_py" <<'PY_CORE'
#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sympy as s

# Domain and grading.
r, M, beta = s.symbols("r M beta", positive=True)
ell = s.symbols("ell", integer=True, positive=True)
Ls = s.symbols("L", integer=True, positive=True)
lam = Ls - 2
f = 1 - 2*M/r

# The exact normalized coefficient table for the epsilon^2 coefficient of
# integral sqrt(-g) Tr_{Lambda^2}(Rop^3), after spherical integration.
# Harmonics obey integral Y_lm^2 dOmega = 1.
J_COEFFICIENT_STRINGS = {
  "k0^2": "-6*Ls*M*(-2*Ls**2*M*r**2 + Ls**2*r**3 + 56*Ls*M**2*r - 54*Ls*M*r**2 + 12*Ls*r**3 - 80*M**3 + 64*M**2*r - 4*M*r**2)/(r**8*(-2*M + r)**2)",
  "k0_r*k0": "12*Ls*M*(-16*Ls*M + 7*Ls*r + 8*M)/(r**6*(-2*M + r))",
  "k0_r*k1_rt": "-12*Ls*M*(-2*M + r)/r**5",
  "k0_r*k1_t": "24*Ls*M*(2*Ls*r - M - r)/r**6",
  "k0_r^2": "-12*Ls*M*(Ls*r + M + 2*r)/r**6",
  "k0_rr*k0": "-96*Ls*M**2/r**6",
  "k0_rr*k0_r": "12*Ls*M*(-2*M + r)/r**5",
  "k0_rr*k1_rt": "12*Ls*M*(-2*M + r)/r**4",
  "k0_rr*k1_t": "12*Ls*M*(-2*M + r)/r**5",
  "k0_rr^2": "-6*Ls*M*(-2*M + r)/r**4",
  "k0_rt*k0_t": "-24*Ls*M/(r**3*(-2*M + r))",
  "k0_rt*k1": "96*Ls*M**2/r**6",
  "k0_rt*k1_tt": "-12*Ls*M/(r**2*(-2*M + r))",
  "k0_rt^2": "6*Ls*M/(r**2*(-2*M + r))",
  "k0_t*k1": "24*Ls*M**2*(Ls*r + 16*M - 8*r)/(r**7*(-2*M + r))",
  "k0_t*k1_r": "96*Ls*M**2/r**6",
  "k0_t*k1_tt": "24*Ls*M/(r**3*(-2*M + r))",
  "k0_t^2": "-12*Ls*M*(Ls*r + 4*M - 4*r)/(r**4*(-2*M + r)**2)",
  "k1^2": "6*Ls*M*(-2*Ls**2*M*r**2 + Ls**2*r**3 - 8*Ls*M**2*r + 10*Ls*M*r**2 - 4*Ls*r**3 - 80*M**3 + 64*M**2*r - 20*M*r**2 + 4*r**3)/r**10",
  "k1_r*k1": "-24*Ls**2*M**2*(-2*M + r)/r**8",
  "k1_r^2": "-12*Ls*M*(Ls - 2)*(-2*M + r)**2/r**7",
  "k1_rt*k0": "96*Ls*M**2/r**6",
  "k1_rt*k1_t": "-12*Ls*M*(-2*M + r)/r**5",
  "k1_rt^2": "-6*Ls*M*(-2*M + r)/r**4",
  "k1_t*k0": "-12*Ls*M*(-12*Ls*M*r + 7*Ls*r**2 + 16*M**2 - 16*M*r)/(r**7*(-2*M + r))",
  "k1_t^2": "-12*Ls*M*(Ls*r + M + 2*r)/r**6",
  "k1_tt*k1": "-96*Ls*M**2/r**6",
  "k1_tt^2": "6*Ls*M/(r**2*(-2*M + r))"
}
J_COEFFICIENTS = {
    name: s.sympify(expr, locals={"L": Ls, "Ls": Ls, "M": M, "r": r})
    for name, expr in J_COEFFICIENT_STRINGS.items()
}

EXPECTED_FIXED_MODE_HASHES = {2: '8015c20088b76c84ee8ea1183064f0f5ec4d3db27f1c2a5607eb9196c9666954', 3: 'df5ab1f71c3e817259e989c94b7d211e7156a6420e2d66daeaae933462aed54c', 4: 'f51bf087fbcbe25e05d9d85e44d4bdd27aefd5a0257f6cb7e7b9e39b1a8796d8', 5: '2d0e445f9506839c9b694dd998db7523fd1427903c9ba55e8ea2a5257b533933', 6: 'dcb043ed16f6cbb034572d933f3e557579695606eb8785aff9dbed2b816d1a12'}


def canonical_hash(coeffs: dict[str, s.Expr]) -> str:
    payload = json.dumps(
        {name: s.sstr(s.factor(s.cancel(value))) for name, value in sorted(coeffs.items())},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def fixed_mode_coefficients(l_value: int) -> dict[str, s.Expr]:
    L_value = l_value * (l_value + 1)
    return {
        name: s.factor(s.cancel(value.subs(Ls, L_value)))
        for name, value in J_COEFFICIENTS.items()
    }


# ---------------------------------------------------------------------------
# Gauge-invariant axial variables.
# ---------------------------------------------------------------------------
t = s.symbols("t", real=True)
h0 = s.Function("h0")(t, r)
h1 = s.Function("h1")(t, r)
h2 = s.Function("h2")(t, r)
Lambda = s.Function("Lambda")(t, r)

k0 = h0 - s.diff(h2, t)/2
k1 = h1 - s.diff(h2, r)/2 + h2/r
Q = s.diff(k1, t) - s.diff(k0, r) + 2*k0/r

A0 = s.diff(Q, r) + 2*Q/r + lam*k0/(f*r**2)
A1 = -s.diff(Q, t) - lam*f*k1/r**2
A2 = s.diff(f*k1, r) - s.diff(k0, t)/f

# Gauge transformation:
# delta h0 = -dot Lambda, delta h1 = -Lambda' + 2 Lambda/r,
# delta h2 = -2 Lambda.
eps = s.symbols("eps")
gauge_sub = {
    h0: h0 - eps*s.diff(Lambda, t),
    h1: h1 - eps*s.diff(Lambda, r) + 2*eps*Lambda/r,
    h2: h2 - 2*eps*Lambda,
}
assert s.simplify(s.diff(k0.xreplace(gauge_sub), eps).subs(eps, 0)) == 0
assert s.simplify(s.diff(k1.xreplace(gauge_sub), eps).subs(eps, 0)) == 0
assert s.simplify(s.diff(Q.xreplace(gauge_sub), eps).subs(eps, 0)) == 0

# ---------------------------------------------------------------------------
# Einstein and Ricci-squared sectors.
# The overall GfE prefactor 3 beta / ell_P^4 is not included here.
# ---------------------------------------------------------------------------
L_EH = Ls/2 * (
        Q**2
        + lam*k0**2/(f*r**2)
        - lam*f*k1**2/r**2
    )

L_RICCI2 = Ls/2 * (
        -f*A0**2
        + A1**2/f
        + lam*A2**2/r**2
    )

# Exact Einstein axial Noether identity, checked with independent invariants.
K0 = s.Function("K0")(t, r)
K1 = s.Function("K1")(t, r)
QK = s.diff(K1, t) - s.diff(K0, r) + 2*K0/r
A0K = s.diff(QK, r) + 2*QK/r + lam*K0/(f*r**2)
A1K = -s.diff(QK, t) - lam*f*K1/r**2
A2K = s.diff(f*K1, r) - s.diff(K0, t)/f
assert s.simplify(
    s.diff(A0K, t) + s.diff(A1K, r) + 2*A1K/r + lam*A2K/r**2
) == 0
E0_EH = Ls*A0K
E1_EH = Ls*A1K
E2_EH = -Ls*lam*A2K/(2*r**2)
NOETHER_EH = s.simplify(
    s.diff(E0_EH, t) + s.diff(E1_EH, r) + 2*E1_EH/r - 2*E2_EH
)
assert NOETHER_EH == 0

# ---------------------------------------------------------------------------
# beta^2 background-variation contribution from the Einstein Hessian.
# It is first computed in Regge-Wheeler gauge. The gauge completion is applied
# only to the sum with the cubic Hessian.
# ---------------------------------------------------------------------------
u = 40*M**3/(9*r**7)
v = 24*M**2/r**6 - s.Rational(392, 9)*M**3/r**7
d = s.symbols("d")
A = f + d*u
B = f + d*v

# For the action integral sqrt(-g) R, G4=1 and F=G=H=2.
EA = 2/r * ((1-B)/r - s.diff(B, r))
EB = 2/r * ((1-B)/r - B*s.diff(A, r)/A)
a1 = Ls/r**2 * (
    s.diff(2*r*s.sqrt(B/A), r)
    + lam/s.sqrt(A*B)
    + r**2*EA/s.sqrt(A*B)
)
a2 = -Ls*s.sqrt(A*B) * (lam/r**2 + EB)
a3 = Ls*s.sqrt(B/A)
c0 = a1 - 2*s.diff(r*a3, r)/r**2

# Exterior branch: sqrt(f^2)=f for r>2M.
def exterior(expr: s.Expr) -> s.Expr:
    out = s.diff(expr, d).subs(d, 0)
    out = out.xreplace({s.Abs(2*M/r - 1): f})
    return s.factor(s.cancel(out))

dc0 = exterior(c0)
dc1 = exterior(a2)
dcQ = exterior(a3)

C0 = 2352*M**2 + 44*M*lam*r - 2256*M*r - 27*lam*r**2 + 540*r**2
C1 = 240*M**2 + 44*M*lam*r - 336*M*r - 27*lam*r**2 + 108*r**2
assert s.factor(dc0 - 4*Ls*M**2*C0/(9*r**8*(r-2*M)**2)) == 0
assert s.factor(dc1 - 4*Ls*M**2*C1/(9*r**10)) == 0
assert s.factor(dcQ - 12*Ls*M**2/r**6) == 0

# ---------------------------------------------------------------------------
# Cubic Hessian in Regge-Wheeler gauge.
# ---------------------------------------------------------------------------
rw_atoms = {
    "k0": h0,
    "k1": h1,
    "k0_r": s.diff(h0, r),
    "k0_t": s.diff(h0, t),
    "k0_rr": s.diff(h0, r, 2),
    "k0_rt": s.diff(h0, r, t),
    "k1_r": s.diff(h1, r),
    "k1_t": s.diff(h1, t),
    "k1_rt": s.diff(h1, r, t),
    "k1_tt": s.diff(h1, t, 2),
}


def parse_monomial(name: str, atoms: dict[str, s.Expr]) -> s.Expr:
    result = s.Integer(1)
    for factor in name.split("*"):
        if "^" in factor:
            base, power = factor.split("^", 1)
            result *= atoms[base]**int(power)
        else:
            result *= atoms[factor]
    return result


L_J_RW = s.Add(*[
    coefficient * parse_monomial(name, rw_atoms)
    for name, coefficient in J_COEFFICIENTS.items()
])

gi_atoms = {
    "k0": k0,
    "k1": k1,
    "k0_r": s.diff(k0, r),
    "k0_t": s.diff(k0, t),
    "k0_rr": s.diff(k0, r, 2),
    "k0_rt": s.diff(k0, r, t),
    "k1_r": s.diff(k1, r),
    "k1_t": s.diff(k1, t),
    "k1_rt": s.diff(k1, r, t),
    "k1_tt": s.diff(k1, t, 2),
}
L_J_GI = s.Add(*[
    coefficient * parse_monomial(name, gi_atoms)
    for name, coefficient in J_COEFFICIENTS.items()
])

Q_RW = s.diff(h1, t) - s.diff(h0, r) + 2*h0/r
L_DK_EH_RW = (dc0*h0**2 + dc1*h1**2 + dcQ*Q_RW**2)/2
L_DK_EH_GI = (dc0*k0**2 + dc1*k1**2 + dcQ*Q**2)/2
L_DK_PLUS_J = L_DK_EH_GI + L_J_GI/9

# Structural coefficient-by-coefficient Noether identity.
Ek0, Ek1 = s.Function("Ek0")(t, r), s.Function("Ek1")(t, r)
E0 = Ek0
E1 = Ek1
E2 = s.diff(Ek0, t)/2 + s.diff(Ek1, r)/2 + Ek1/r
NOETHER_GENERAL = s.simplify(
    s.diff(E0, t) + s.diff(E1, r) + 2*E1/r - 2*E2
)
assert NOETHER_GENERAL == 0

# beta=0 is the exact Einstein axial action.
L_GR_RW = s.factor(L_EH.subs(h2, 0).doit())
EXPECTED_GR_RW = s.factor(
    Ls/2 * (
        (s.diff(h1, t) - s.diff(h0, r) + 2*h0/r)**2
        + lam*h0**2/(f*r**2)
        - lam*f*h1**2/r**2
    )
)
assert s.expand(L_GR_RW - EXPECTED_GR_RW) == 0


# Exact leading massless-branch h0 elimination in the Fourier convention
# exp(-i*omega*t). This proves only the beta^0 constraint map.
omega = s.symbols("omega", nonzero=True)
Psi_minus = s.Function("Psi_minus")(r)
H1_radial = s.Function("H1_radial")(r)

# A1=0 gives Q=-i*lambda*f*h1/(omega*r^2).
# Substitution into A0=0 gives h0=(i*f/omega)*d_r(f*h1).
Q_constraint = -s.I*lam*f*H1_radial/(omega*r**2)
H0_from_constraints = s.factor(s.cancel(
    -f*r**2/lam
    * (s.diff(Q_constraint, r) + 2*Q_constraint/r)
))
H0_elimination = (
    s.I*f/omega
    * s.diff(f*H1_radial, r)
)
assert s.factor(
    s.cancel(H0_from_constraints - H0_elimination)
) == 0

# Master normalization Psi_minus=f*h1/r.
H1_from_master = r*Psi_minus/f
H0_from_master = (
    s.I*f/omega
    * s.diff(r*Psi_minus, r)
)

Q_from_master = s.factor(s.cancel(
    -s.I*omega*H1_from_master
    - s.diff(H0_from_master, r)
    + 2*H0_from_master/r
))

A0_from_master = s.factor(s.cancel(
    s.diff(Q_from_master, r)
    + 2*Q_from_master/r
    + lam*H0_from_master/(f*r**2)
))

A1_from_master = s.factor(s.cancel(
    s.I*omega*Q_from_master
    - lam*f*H1_from_master/r**2
))

RW_minus = s.factor(s.cancel(
    f**2*s.diff(Psi_minus, r, 2)
    + f*s.diff(f, r)*s.diff(Psi_minus, r)
    + (
        omega**2
        - f*(Ls/r**2 - 6*M/r**3)
    )*Psi_minus
))

assert s.factor(
    s.cancel(A1_from_master - r*RW_minus/f)
) == 0

assert s.factor(s.cancel(
    A0_from_master
    + s.I/omega
    * (
        s.diff(A1_from_master, r)
        + 2*A1_from_master/r
    )
)) == 0


# Relative O(beta^2) massless-branch axial constraint source for ell=2.
# Vary in (t,r) before Fourier substitution; substituting a single complex
# mode into the quadratic action would give incorrect kinetic signs.
def second_order_euler_operator(lagrangian, field):
    result = s.diff(lagrangian, field)
    for variable in (t, r):
        result -= s.diff(
            s.diff(lagrangian, s.Derivative(field, variable)),
            variable,
        )
    for first, second in ((t, t), (t, r), (r, r)):
        coefficient = s.diff(
            lagrangian,
            s.Derivative(field, first, second),
        )
        if coefficient != 0:
            result += s.diff(coefficient, first, second)
    return s.expand(result)


L_CORR_RW = s.expand(L_DK_PLUS_J.subs(h2, 0).doit())
E0_CORR_RW = second_order_euler_operator(L_CORR_RW, h0)
E1_CORR_RW = second_order_euler_operator(L_CORR_RW, h1)

H0_radial = s.Function("H0_radial")(r)
H1_radial_beta2 = s.Function("H1_radial_beta2")(r)


def fourier_radialize(expression):
    replacements = {
        h0: H0_radial,
        h1: H1_radial_beta2,
    }
    for field, radial_field in (
        (h0, H0_radial),
        (h1, H1_radial_beta2),
    ):
        for radial_order in range(5):
            for time_order in range(5):
                if radial_order + time_order == 0:
                    continue
                replacements[
                    s.diff(
                        field,
                        t,
                        time_order,
                        r,
                        radial_order,
                    )
                ] = (
                    (-s.I*omega)**time_order
                    * s.diff(radial_field, r, radial_order)
                )
    return s.expand(expression.xreplace(replacements))


E0_CORR_FOURIER = fourier_radialize(E0_CORR_RW).subs(Ls, 6)
E1_CORR_FOURIER = fourier_radialize(E1_CORR_RW).subs(Ls, 6)

H1_220_LEADING = r*Psi_minus/f
H0_220_LEADING = s.I*f/omega*s.diff(r*Psi_minus, r)
leading_replacements = {
    H0_radial: H0_220_LEADING,
    H1_radial_beta2: H1_220_LEADING,
}
for radial_field, leading_field in (
    (H0_radial, H0_220_LEADING),
    (H1_radial_beta2, H1_220_LEADING),
):
    for radial_order in range(1, 6):
        leading_replacements[
            s.diff(radial_field, r, radial_order)
        ] = s.diff(leading_field, r, radial_order)

S0_220 = s.expand(
    E0_CORR_FOURIER.xreplace(leading_replacements).doit()
)
S1_220 = s.expand(
    E1_CORR_FOURIER.xreplace(leading_replacements).doit()
)

# From 6*A1 + beta^2*S1_220 = 0:
Q2_220 = s.I*S1_220/(6*omega)

# From 6*A0 + beta^2*S0_220 = 0 with lambda=4:
H0_220_BETA2 = -f*r**2/s.Integer(4) * (
    s.diff(Q2_220, r)
    + 2*Q2_220/r
    + S0_220/6
)

assert s.expand(6*s.I*omega*Q2_220 + S1_220) == 0
assert s.cancel(s.together(
    6*(
        s.diff(Q2_220, r)
        + 2*Q2_220/r
        + 4*H0_220_BETA2/(f*r**2)
    )
    + S0_220
)) == 0

# The remaining Q-definition compatibility equation is the exact beta^2
# master source. It is not yet reduced with the leading RW equation.
RW2_220_UNREDUCED = s.expand(
    -s.diff(H0_220_BETA2, r)
    + 2*H0_220_BETA2/r
    - Q2_220
)
RW2_220_HASH = hashlib.sha256(
    s.sstr(RW2_220_UNREDUCED).encode("utf-8")
).hexdigest()
RW2_220_MAX_RADIAL_ORDER = max(
    [
        sum(
            count
            for variable, count in derivative.variable_count
            if variable == r
        )
        for derivative in RW2_220_UNREDUCED.atoms(s.Derivative)
    ]
    or [0]
)


# Structural order reduction of the ell=2 beta^2 source. Extract the five
# linear radial jets before applying the leading Regge-Wheeler recurrence.
psi0, psi1, psi2, psi3, psi4 = s.symbols("psi0 psi1 psi2 psi3 psi4")
RW2_220_JET = RW2_220_UNREDUCED.xreplace({
    Psi_minus: psi0,
    s.diff(Psi_minus, r): psi1,
    s.diff(Psi_minus, r, 2): psi2,
    s.diff(Psi_minus, r, 3): psi3,
    s.diff(Psi_minus, r, 4): psi4,
})
RW2_220_JET_COEFFS = [
    RW2_220_JET.coeff(symbol)
    for symbol in (psi0, psi1, psi2, psi3, psi4)
]
assert s.expand(
    RW2_220_JET
    - sum(
        coefficient*symbol
        for coefficient, symbol in zip(
            RW2_220_JET_COEFFS,
            (psi0, psi1, psi2, psi3, psi4),
        )
    )
) == 0

V_RW_220 = 6/r**2 - 6*M/r**3
A2_1 = -s.diff(f, r)/f
A2_0 = -(omega**2 - f*V_RW_220)/f**2
A3_1 = s.diff(A2_1, r) + A2_1**2 + A2_0
A3_0 = s.diff(A2_0, r) + A2_1*A2_0
A4_1 = s.diff(A3_1, r) + A3_1*A2_1 + A3_0
A4_0 = s.diff(A3_0, r) + A3_1*A2_0

c0, c1, c2, c3, c4 = RW2_220_JET_COEFFS
RW2_220_COEFF_D1_RAW = c1 + c2*A2_1 + c3*A3_1 + c4*A4_1
RW2_220_COEFF_D0_RAW = c0 + c2*A2_0 + c3*A3_0 + c4*A4_0
RW2_220_ORDER_REDUCED_RAW = (
    RW2_220_COEFF_D1_RAW*s.diff(Psi_minus, r)
    + RW2_220_COEFF_D0_RAW*Psi_minus
)
RW2_220_REDUCED_MAX_RADIAL_ORDER = max([
    sum(
        count
        for variable, count in derivative.variable_count
        if variable == r
    )
    for derivative in RW2_220_ORDER_REDUCED_RAW.atoms(s.Derivative)
] or [0])
assert RW2_220_REDUCED_MAX_RADIAL_ORDER == 1

RW2_220_ORDER_REDUCED_RAW_HASH = hashlib.sha256(
    s.sstr(RW2_220_ORDER_REDUCED_RAW).encode("utf-8")
).hexdigest()


# Normalize the two exact ell=2 order-reduced source coefficients.
RW2_220_COEFF_D1 = s.factor(s.cancel(s.together(
    RW2_220_COEFF_D1_RAW
)))
RW2_220_COEFF_D0 = s.factor(s.cancel(s.together(
    RW2_220_COEFF_D0_RAW
)))

RW2_220_COEFF_D1_EXPECTED = (
    -8*s.I*M*(
        -648*M**3 + 913*M**2*r - 417*M*r**2 + 60*r**3
    )
    /(3*omega*r**7*(-2*M + r))
)
RW2_220_COEFF_D0_EXPECTED = (
    -8*s.I*M*(
        10128*M**4 - 9004*M**3*r
        + 188*M**2*omega**2*r**4 - 797*M**2*r**2
        - 171*M*omega**2*r**5 + 2466*M*r**3
        + 36*omega**2*r**6 - 540*r**4
    )
    /(9*omega*r**8*(-2*M + r)**2)
)
assert s.factor(s.cancel(
    RW2_220_COEFF_D1 - RW2_220_COEFF_D1_EXPECTED
)) == 0
assert s.factor(s.cancel(
    RW2_220_COEFF_D0 - RW2_220_COEFF_D0_EXPECTED
)) == 0

# The Q-definition compatibility source enters the Regge-Wheeler equation as
# i*omega*f/r times RW2_220_ORDER_REDUCED_RAW.
RW2_220_EQUATION_D1 = s.factor(s.cancel(
    s.I*omega*f/r * RW2_220_COEFF_D1
))
RW2_220_EQUATION_D0 = s.factor(s.cancel(
    s.I*omega*f/r * RW2_220_COEFF_D0
))

# Fix the requested corrected-tortoise convention dr_*/dr=(N*F)^(-1).
# F=f+beta^2*v and N=1-12*beta^2*M^2/r^6, hence
# N*F=f+beta^2*NF_220_BETA2 through relative O(beta^2).
NF_220_BETA2 = s.factor(s.cancel(
    v - 12*M**2*f/r**6
))
NF_220_BETA2_EXPECTED = 4*M**2*(-44*M + 27*r)/(9*r**7)
assert s.factor(s.cancel(
    NF_220_BETA2 - NF_220_BETA2_EXPECTED
)) == 0

# Exterior master normalization:
# Psi_minus=(1+beta^2*MASTER_REDEF_220)*Phi_minus.
# A post-substitution equation multiplier
# 1+beta^2*EQUATION_MULTIPLIER_220 fixes the principal coefficient to (N*F)^2.
MASTER_REDEF_220 = (
    4*M*(140*M**2 - 147*M*r + 36*r**2)
    /(9*r**6*(-2*M + r))
)
EQUATION_MULTIPLIER_220 = s.factor(s.cancel(
    2*NF_220_BETA2/f
))

MASTER_REDEF_DERIVATIVE_REQUIRED = s.factor(s.cancel(
    (
        f*s.diff(NF_220_BETA2, r)
        - NF_220_BETA2*s.diff(f, r)
        - RW2_220_EQUATION_D1
    )
    /(2*f**2)
))
assert s.factor(s.cancel(
    s.diff(MASTER_REDEF_220, r)
    - MASTER_REDEF_DERIVATIVE_REQUIRED
)) == 0

DELTA_V_MINUS_220 = s.factor(
    -8*M*(653*M**2 - 281*M*r + 4*omega**2*r**4)/r**9
)

U_RW_220 = omega**2 - f*V_RW_220
TRANSFORMED_D2_220 = s.factor(s.cancel(
    EQUATION_MULTIPLIER_220*f**2
))
TRANSFORMED_D1_220 = s.factor(s.cancel(
    EQUATION_MULTIPLIER_220*f*s.diff(f, r)
    + RW2_220_EQUATION_D1
    + 2*f**2*s.diff(MASTER_REDEF_220, r)
))
TRANSFORMED_D0_220 = s.factor(s.cancel(
    EQUATION_MULTIPLIER_220*U_RW_220
    + RW2_220_EQUATION_D0
    + f**2*s.diff(MASTER_REDEF_220, r, 2)
    + f*s.diff(f, r)*s.diff(MASTER_REDEF_220, r)
))

TARGET_D2_220 = 2*f*NF_220_BETA2
TARGET_D1_220 = (
    f*s.diff(NF_220_BETA2, r)
    + NF_220_BETA2*s.diff(f, r)
)
TARGET_D0_220 = -v*V_RW_220 - f*DELTA_V_MINUS_220

assert s.factor(s.cancel(
    TRANSFORMED_D2_220 - TARGET_D2_220
)) == 0
assert s.factor(s.cancel(
    TRANSFORMED_D1_220 - TARGET_D1_220
)) == 0
assert s.factor(s.cancel(
    TRANSFORMED_D0_220 - TARGET_D0_220
)) == 0

RW2_220_NORMALIZED_COEFFICIENT_HASH = hashlib.sha256(
    json.dumps(
        {
            "D0": s.sstr(RW2_220_COEFF_D0),
            "D1": s.sstr(RW2_220_COEFF_D1),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()
DELTA_V_MINUS_220_HASH = hashlib.sha256(
    s.sstr(DELTA_V_MINUS_220).encode("utf-8")
).hexdigest()

# Shifted-horizon ingoing Frobenius data for the ell=2 canonical axial
# equation.  Use z=r/M, Omega=M*omega, and epsilon=beta^2/M^4.  The
# dimensionless equation is
#   P(z)^2 Phi'' + P(z) P'(z) Phi' + [Omega^2-F(z)V(z)] Phi = 0,
# with P=N*F and the physical horizon z_h=2-5*epsilon/72.
z_hor, x_hor, Omega_hor, epsilon_hor = s.symbols(
    "z_hor x_hor Omega_hor epsilon_hor"
)


def truncate_horizon_epsilon(expr):
    return s.cancel(
        expr.subs(epsilon_hor, 0)
        + epsilon_hor*s.diff(expr, epsilon_hor).subs(epsilon_hor, 0)
    )


f_hor = 1 - 2/z_hor
v_hor = 24/z_hor**6 - s.Rational(392, 9)/z_hor**7
p_hor = 4*(27*z_hor - 44)/(9*z_hor**7)
V0_hor = 6/z_hor**2 - 6/z_hor**3
deltaV_hor = -8*(
    653 - 281*z_hor + 4*Omega_hor**2*z_hor**4
)/z_hor**9
z_horizon = 2 - s.Rational(5, 72)*epsilon_hor

F_hor = truncate_horizon_epsilon(
    (f_hor + epsilon_hor*v_hor).subs(
        z_hor, z_horizon + x_hor
    )
)
P_hor = truncate_horizon_epsilon(
    (f_hor + epsilon_hor*p_hor).subs(
        z_hor, z_horizon + x_hor
    )
)
V_hor = truncate_horizon_epsilon(
    (V0_hor + epsilon_hor*deltaV_hor).subs(
        z_hor, z_horizon + x_hor
    )
)

assert s.simplify(truncate_horizon_epsilon(F_hor.subs(x_hor, 0))) == 0
assert s.simplify(truncate_horizon_epsilon(P_hor.subs(x_hor, 0))) == 0

P1_hor = s.simplify(truncate_horizon_epsilon(
    s.diff(P_hor, x_hor).subs(x_hor, 0)
))
P1_hor_expected = s.Rational(1, 2) + epsilon_hor/s.Integer(144)
assert s.simplify(P1_hor - P1_hor_expected) == 0

# Ingoing behavior for exp(-i*omega*t): Phi~x^alpha with
# alpha=-i*Omega/P'(z_h)=-2*i*Omega+i*epsilon*Omega/36.
alpha_ingoing_hor = (
    -2*s.I*Omega_hor
    + epsilon_hor*s.I*Omega_hor/s.Integer(36)
)

A_hor = truncate_horizon_epsilon(P_hor**2)
B_hor = truncate_horizon_epsilon(P_hor*s.diff(P_hor, x_hor))
C_hor = truncate_horizon_epsilon(
    Omega_hor**2 - F_hor*V_hor
)

FROBENIUS_ORDER_220 = 4
A_hor_coeff = [
    s.simplify(truncate_horizon_epsilon(
        s.diff(A_hor, x_hor, j).subs(x_hor, 0)/s.factorial(j)
    ))
    for j in range(FROBENIUS_ORDER_220 + 3)
]
B_hor_coeff = [
    s.simplify(truncate_horizon_epsilon(
        s.diff(B_hor, x_hor, j).subs(x_hor, 0)/s.factorial(j)
    ))
    for j in range(FROBENIUS_ORDER_220 + 2)
]
C_hor_coeff = [
    s.simplify(truncate_horizon_epsilon(
        s.diff(C_hor, x_hor, j).subs(x_hor, 0)/s.factorial(j)
    ))
    for j in range(FROBENIUS_ORDER_220 + 1)
]

A2_hor = A_hor_coeff[2]
B1_hor = B_hor_coeff[1]
C0_hor = C_hor_coeff[0]
assert s.simplify(A2_hor - (s.Rational(1, 4) + epsilon_hor/144)) == 0
assert s.simplify(B1_hor - A2_hor) == 0
assert s.simplify(C0_hor - Omega_hor**2) == 0

indicial_hor = truncate_horizon_epsilon(
    A2_hor*alpha_ingoing_hor*(alpha_ingoing_hor - 1)
    + B1_hor*alpha_ingoing_hor
    + C0_hor
)
assert s.simplify(indicial_hor) == 0

n_hor = s.symbols("n_hor", integer=True, positive=True)
recurrence_denominator_hor = s.factor(truncate_horizon_epsilon(
    A2_hor*(alpha_ingoing_hor + n_hor)
        *(alpha_ingoing_hor + n_hor - 1)
    + B1_hor*(alpha_ingoing_hor + n_hor)
    + C0_hor
))
recurrence_denominator_expected_hor = (
    n_hor*((36 + epsilon_hor)*n_hor
    - s.I*(144 + 2*epsilon_hor)*Omega_hor)/144
)
assert s.simplify(
    recurrence_denominator_hor
    - recurrence_denominator_expected_hor
) == 0

# For Phi=x^alpha sum_{n>=0} a_n x^n, a_0=1, the exact recurrence is
# I_n a_n plus the three lower-triangular coefficient sums equal to zero.
a_hor = [s.Integer(1)]
for n_value in range(1, FROBENIUS_ORDER_220 + 1):
    denominator = truncate_horizon_epsilon(
        A_hor_coeff[2]*(alpha_ingoing_hor + n_value)
            *(alpha_ingoing_hor + n_value - 1)
        + B_hor_coeff[1]*(alpha_ingoing_hor + n_value)
        + C_hor_coeff[0]
    )
    lower = s.Integer(0)
    for j_value in range(3, n_value + 3):
        k_value = n_value - j_value + 2
        lower += (
            A_hor_coeff[j_value]
            *(alpha_ingoing_hor + k_value)
            *(alpha_ingoing_hor + k_value - 1)
            *a_hor[k_value]
        )
    for j_value in range(2, n_value + 2):
        k_value = n_value - j_value + 1
        lower += (
            B_hor_coeff[j_value]
            *(alpha_ingoing_hor + k_value)
            *a_hor[k_value]
        )
    for j_value in range(1, n_value + 1):
        k_value = n_value - j_value
        lower += C_hor_coeff[j_value]*a_hor[k_value]

    next_coefficient = s.factor(truncate_horizon_epsilon(
        -lower/denominator
    ))
    assert s.simplify(truncate_horizon_epsilon(
        denominator*next_coefficient + lower
    )) == 0
    a_hor.append(next_coefficient)

A1_HORIZON_220 = s.factor(a_hor[1])
A1_HORIZON_220_GR = s.factor(A1_HORIZON_220.subs(epsilon_hor, 0))
A1_HORIZON_220_BETA2 = s.factor(
    s.diff(A1_HORIZON_220, epsilon_hor).subs(epsilon_hor, 0)
)
A1_HORIZON_220_GR_EXPECTED = s.factor(
    -s.I*(8*Omega_hor**2 + 2*s.I*Omega_hor - 3)
    /(2*(4*Omega_hor + s.I))
)
A1_HORIZON_220_BETA2_EXPECTED = s.factor(
    -s.I*(
        1408*Omega_hor**3
        + 512*s.I*Omega_hor**2
        + 924*Omega_hor
        + 243*s.I
    )/(96*(4*Omega_hor + s.I)**2)
)
assert s.simplify(
    A1_HORIZON_220_GR - A1_HORIZON_220_GR_EXPECTED
) == 0
assert s.simplify(
    A1_HORIZON_220_BETA2 - A1_HORIZON_220_BETA2_EXPECTED
) == 0

HORIZON_FROBENIUS_220_HASH = hashlib.sha256(
    json.dumps(
        {
            "alpha": s.sstr(alpha_ingoing_hor),
            "P1": s.sstr(P1_hor),
            "A": [s.sstr(value) for value in A_hor_coeff],
            "B": [s.sstr(value) for value in B_hor_coeff],
            "C": [s.sstr(value) for value in C_hor_coeff],
            "a": [s.sstr(value) for value in a_hor],
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()
assert HORIZON_FROBENIUS_220_HASH == (
    "bd0d8ee3929506081b1381330e03e7a13f605774585c3837b025f9a7ed3bdb76"
)

# Rigorous local majorant for the shifted-horizon ingoing series on a fixed
# ell=2 fundamental-mode box.  Clear the rational coefficients by multiplying
# the equation by z^10; the resulting recurrence has finite lag ten.
from fractions import Fraction as _Fraction

A_clear_hor = s.Poly(s.expand(truncate_horizon_epsilon(
    (z_horizon + x_hor)**10 * A_hor
)), x_hor)
B_clear_hor = s.Poly(s.expand(truncate_horizon_epsilon(
    (z_horizon + x_hor)**10 * B_hor
)), x_hor)
C_clear_hor = s.Poly(s.expand(truncate_horizon_epsilon(
    (z_horizon + x_hor)**10 * C_hor
)), x_hor)
assert A_clear_hor.degree() == 10
assert B_clear_hor.degree() == 8
assert C_clear_hor.degree() == 10
A_clear_coeff_hor = [
    s.expand(A_clear_hor.coeff_monomial(x_hor**j))
    for j in range(11)
]
B_clear_coeff_hor = [
    s.expand(B_clear_hor.coeff_monomial(x_hor**j))
    for j in range(11)
]
C_clear_coeff_hor = [
    s.expand(C_clear_hor.coeff_monomial(x_hor**j))
    for j in range(11)
]
assert A_clear_coeff_hor[0] == 0
assert A_clear_coeff_hor[1] == 0
assert B_clear_coeff_hor[0] == 0

class _ComplexDisk:
    __slots__ = ("re", "im", "rad")

    def __init__(self, re=0, im=0, rad=0):
        self.re = _Fraction(re)
        self.im = _Fraction(im)
        self.rad = _Fraction(rad)

    @staticmethod
    def coerce(value):
        if isinstance(value, _ComplexDisk):
            return value
        if isinstance(value, s.Rational):
            return _ComplexDisk(_Fraction(int(value.p), int(value.q)))
        return _ComplexDisk(value)

    def __add__(self, other):
        other = self.coerce(other)
        return _ComplexDisk(
            self.re + other.re,
            self.im + other.im,
            self.rad + other.rad,
        )

    __radd__ = __add__

    def __neg__(self):
        return _ComplexDisk(-self.re, -self.im, self.rad)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def center_abs_upper(self):
        return abs(self.re) + abs(self.im)

    def center_abs_lower(self):
        return max(abs(self.re), abs(self.im))

    def abs_upper(self):
        return self.center_abs_upper() + self.rad

    def __mul__(self, other):
        other = self.coerce(other)
        re = self.re*other.re - self.im*other.im
        im = self.re*other.im + self.im*other.re
        rad = (
            self.center_abs_upper()*other.rad
            + other.center_abs_upper()*self.rad
            + self.rad*other.rad
        )
        return _ComplexDisk(re, im, rad)

    __rmul__ = __mul__

    def inverse(self):
        lower = self.center_abs_lower()
        assert lower > self.rad
        norm2 = self.re*self.re + self.im*self.im
        inverse_center_re = self.re/norm2
        inverse_center_im = -self.im/norm2
        inverse_radius = self.rad/(lower*(lower - self.rad))
        return _ComplexDisk(
            inverse_center_re,
            inverse_center_im,
            inverse_radius,
        )

    def __truediv__(self, other):
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, power):
        assert isinstance(power, int) and power >= 0
        result = _ComplexDisk(1)
        base = self
        exponent = power
        while exponent:
            if exponent & 1:
                result = result*base
            base = base*base
            exponent >>= 1
        return result


def _disk_evaluate_polynomial(expression, omega_disk, epsilon_disk):
    polynomial = s.Poly(
        s.expand(expression), Omega_hor, epsilon_hor
    )
    result = _ComplexDisk(0)
    for (omega_power, epsilon_power), coefficient in polynomial.terms():
        assert coefficient.is_Rational
        rational_coefficient = _Fraction(
            int(coefficient.p), int(coefficient.q)
        )
        result += (
            rational_coefficient
            * omega_disk**omega_power
            * epsilon_disk**epsilon_power
        )
    return result

# Rectangle enclosed by the exact disk below:
# Re Omega in [0.3736,0.3738], Im Omega in [-0.0891,-0.0888].
OMEGA_HORIZON_BOX_220 = {
    "re_min": _Fraction(3736, 10000),
    "re_max": _Fraction(3738, 10000),
    "im_min": -_Fraction(891, 10000),
    "im_max": -_Fraction(888, 10000),
}
EPSILON_HORIZON_INTERVAL_220 = (
    _Fraction(0), _Fraction(1, 10000)
)
OMEGA_HORIZON_DISK_220 = _ComplexDisk(
    _Fraction(3737, 10000),
    -_Fraction(1779, 20000),
    _Fraction(1, 4000),
)
EPSILON_HORIZON_DISK_220 = _ComplexDisk(
    _Fraction(1, 20000), 0, _Fraction(1, 20000)
)

A_clear_disk_hor = [
    _disk_evaluate_polynomial(
        coefficient,
        OMEGA_HORIZON_DISK_220,
        EPSILON_HORIZON_DISK_220,
    )
    for coefficient in A_clear_coeff_hor
]
B_clear_disk_hor = [
    _disk_evaluate_polynomial(
        coefficient,
        OMEGA_HORIZON_DISK_220,
        EPSILON_HORIZON_DISK_220,
    )
    for coefficient in B_clear_coeff_hor
]
C_clear_disk_hor = [
    _disk_evaluate_polynomial(
        coefficient,
        OMEGA_HORIZON_DISK_220,
        EPSILON_HORIZON_DISK_220,
    )
    for coefficient in C_clear_coeff_hor
]
alpha_disk_hor = (
    _ComplexDisk(0, -2)*OMEGA_HORIZON_DISK_220
    + _ComplexDisk(0, _Fraction(1, 36))
      *EPSILON_HORIZON_DISK_220*OMEGA_HORIZON_DISK_220
)

MAJORANT_RADIUS_220 = _Fraction(1, 8)
LAUNCH_RADIUS_220 = _Fraction(1, 16)
MAJORANT_START_220 = 40
FROBENIUS_TRUNCATION_220 = 24

# Direct exact-disk recurrence through n=39.
a_disk_hor = [_ComplexDisk(1)]
finite_scaled_bounds_hor = [_Fraction(1)]
for n_value in range(1, MAJORANT_START_220):
    n_disk = _ComplexDisk(n_value)
    denominator_disk = (
        A_clear_disk_hor[2]
        *(alpha_disk_hor + n_disk)
        *(alpha_disk_hor + n_disk - 1)
        + B_clear_disk_hor[1]*(alpha_disk_hor + n_disk)
        + C_clear_disk_hor[0]
    )
    lower_disk = _ComplexDisk(0)
    for lag in range(1, min(10, n_value) + 1):
        k_value = n_value - lag
        k_disk = _ComplexDisk(k_value)
        transfer_disk = _ComplexDisk(0)
        if lag + 2 <= 10:
            transfer_disk += (
                A_clear_disk_hor[lag + 2]
                *(alpha_disk_hor + k_disk)
                *(alpha_disk_hor + k_disk - 1)
            )
        if lag + 1 <= 10:
            transfer_disk += (
                B_clear_disk_hor[lag + 1]
                *(alpha_disk_hor + k_disk)
            )
        transfer_disk += C_clear_disk_hor[lag]
        lower_disk += transfer_disk*a_disk_hor[k_value]
    next_disk = -lower_disk/denominator_disk
    a_disk_hor.append(next_disk)
    scaled_bound = (
        next_disk.abs_upper()*MAJORANT_RADIUS_220**n_value
    )
    finite_scaled_bounds_hor.append(scaled_bound)
    assert scaled_bound <= 1


def _polynomial_absolute_bound(expression, omega_bound, epsilon_bound):
    polynomial = s.Poly(
        s.expand(expression), Omega_hor, epsilon_hor
    )
    result = _Fraction(0)
    for (omega_power, epsilon_power), coefficient in polynomial.terms():
        assert coefficient.is_Rational
        coefficient_fraction = _Fraction(
            abs(int(coefficient.p)), int(coefficient.q)
        )
        result += (
            coefficient_fraction
            * omega_bound**omega_power
            * epsilon_bound**epsilon_power
        )
    return result

OMEGA_ABS_BOUND_220 = _Fraction(2, 5)
OMEGA_IM_ABS_BOUND_220 = _Fraction(891, 10000)
EPSILON_ABS_BOUND_220 = _Fraction(1, 10000)
ALPHA_ABS_BOUND_220 = (
    OMEGA_ABS_BOUND_220
    * (2 + EPSILON_ABS_BOUND_220/_Fraction(36))
)
Z_HORIZON_MIN_220 = (
    _Fraction(2) - _Fraction(5, 72)*EPSILON_ABS_BOUND_220
)
A_clear_abs_hor = [
    _polynomial_absolute_bound(
        coefficient,
        OMEGA_ABS_BOUND_220,
        EPSILON_ABS_BOUND_220,
    )
    for coefficient in A_clear_coeff_hor
]
B_clear_abs_hor = [
    _polynomial_absolute_bound(
        coefficient,
        OMEGA_ABS_BOUND_220,
        EPSILON_ABS_BOUND_220,
    )
    for coefficient in B_clear_coeff_hor
]
C_clear_abs_hor = [
    _polynomial_absolute_bound(
        coefficient,
        OMEGA_ABS_BOUND_220,
        EPSILON_ABS_BOUND_220,
    )
    for coefficient in C_clear_coeff_hor
]

# Uniform weighted recurrence norm for every n>=40.
majorant_numerator_220 = _Fraction(0)
for lag in range(1, 11):
    A_bound = (
        A_clear_abs_hor[lag + 2] if lag + 2 <= 10 else 0
    )
    B_bound = (
        B_clear_abs_hor[lag + 1] if lag + 1 <= 10 else 0
    )
    C_bound = C_clear_abs_hor[lag]
    majorant_numerator_220 += MAJORANT_RADIUS_220**lag * (
        A_bound
        *(1 + ALPHA_ABS_BOUND_220/MAJORANT_START_220)
        *(1 + (1 + ALPHA_ABS_BOUND_220)/MAJORANT_START_220)
        + B_bound
          *(1 + ALPHA_ABS_BOUND_220/MAJORANT_START_220)
          /MAJORANT_START_220
        + C_bound/MAJORANT_START_220**2
    )
majorant_denominator_220 = (
    Z_HORIZON_MIN_220**10/_Fraction(144)
    * (
        36
        - (144 + 2*EPSILON_ABS_BOUND_220)
          *OMEGA_IM_ABS_BOUND_220/MAJORANT_START_220
    )
)
HORIZON_MAJORANT_Q_220 = (
    majorant_numerator_220/majorant_denominator_220
)
assert HORIZON_MAJORANT_Q_220 < 1
assert max(finite_scaled_bounds_hor) == 1

launch_ratio_220 = LAUNCH_RADIUS_220/MAJORANT_RADIUS_220
HORIZON_SERIES_TAIL_220 = (
    launch_ratio_220**(FROBENIUS_TRUNCATION_220 + 1)
    /(1 - launch_ratio_220)
)
first_omitted_220 = FROBENIUS_TRUNCATION_220 + 1
HORIZON_SERIES_DERIVATIVE_TAIL_220 = (
    1/MAJORANT_RADIUS_220
    * launch_ratio_220**(first_omitted_220 - 1)
    * (
        first_omitted_220
        - (first_omitted_220 - 1)*launch_ratio_220
    )
    /(1 - launch_ratio_220)**2
)
assert HORIZON_SERIES_TAIL_220 == _Fraction(1, 16777216)
assert HORIZON_SERIES_DERIVATIVE_TAIL_220 == _Fraction(13, 524288)

HORIZON_MAJORANT_220_HASH = hashlib.sha256(
    json.dumps(
        {
            "omega_box": {
                key: str(value)
                for key, value in OMEGA_HORIZON_BOX_220.items()
            },
            "epsilon_interval": [
                str(value) for value in EPSILON_HORIZON_INTERVAL_220
            ],
            "majorant_radius": str(MAJORANT_RADIUS_220),
            "launch_radius": str(LAUNCH_RADIUS_220),
            "majorant_start": MAJORANT_START_220,
            "truncation": FROBENIUS_TRUNCATION_220,
            "q": str(HORIZON_MAJORANT_Q_220),
            "tail": str(HORIZON_SERIES_TAIL_220),
            "derivative_tail": str(HORIZON_SERIES_DERIVATIVE_TAIL_220),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()
assert HORIZON_MAJORANT_220_HASH == (
    "5feeb5e5a47b9a7139f431fc6e31cb861a58fdf4047a76ec04501adcca78746d"
)

# Exact complex-disk enclosure of the regular ingoing endpoint pair at
# x=1/16.  The physical Frobenius factor is Phi=x^alpha*S; this certificate
# encloses S and dS/dx.  Keeping the regular pair avoids any transcendental
# enclosure of x^alpha before validated radial propagation.
HORIZON_ENDPOINT_VALUE_220 = _ComplexDisk(0)
HORIZON_ENDPOINT_DERIVATIVE_220 = _ComplexDisk(0)
for n_value in range(FROBENIUS_TRUNCATION_220 + 1):
    HORIZON_ENDPOINT_VALUE_220 += (
        a_disk_hor[n_value]
        * LAUNCH_RADIUS_220**n_value
    )
    if n_value > 0:
        HORIZON_ENDPOINT_DERIVATIVE_220 += (
            n_value
            * a_disk_hor[n_value]
            * LAUNCH_RADIUS_220**(n_value - 1)
        )

# Add the independently certified omitted-series bounds.
HORIZON_ENDPOINT_VALUE_220.rad += HORIZON_SERIES_TAIL_220
HORIZON_ENDPOINT_DERIVATIVE_220.rad += (
    HORIZON_SERIES_DERIVATIVE_TAIL_220
)

HORIZON_ENDPOINT_VALUE_NONZERO_LOWER_220 = (
    HORIZON_ENDPOINT_VALUE_220.center_abs_lower()
    - HORIZON_ENDPOINT_VALUE_220.rad
)
assert HORIZON_ENDPOINT_VALUE_NONZERO_LOWER_220 > 1


def _exact_disk_record(disk):
    return {
        "re": str(disk.re),
        "im": str(disk.im),
        "rad": str(disk.rad),
    }


HORIZON_ENDPOINT_220_HASH = hashlib.sha256(
    json.dumps(
        {
            "launch_radius": str(LAUNCH_RADIUS_220),
            "truncation": FROBENIUS_TRUNCATION_220,
            "series_tail": str(HORIZON_SERIES_TAIL_220),
            "derivative_tail": str(
                HORIZON_SERIES_DERIVATIVE_TAIL_220
            ),
            "regular_value": _exact_disk_record(
                HORIZON_ENDPOINT_VALUE_220
            ),
            "regular_derivative": _exact_disk_record(
                HORIZON_ENDPOINT_DERIVATIVE_220
            ),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()
assert HORIZON_ENDPOINT_220_HASH == (
    "d0d8dde2f129ad7ddd640af81b1b27cf82ff7c8125bb79d7470252389b555d3e"
)

# Three-parameter affine endpoint model preserving the dependence on
# xi_ReOmega, xi_ImOmega, and xi_epsilon in [-1,1].  Unlike a single
# complex disk, this model does not discard the parameter correlations needed
# for validated outward propagation and interval Newton differentiation.
# The recurrence is extended from n=24 to n=32 using the already certified
# finite-lag majorant through n=39.

def _ac_add(lhs, rhs):
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])


def _ac_neg(value):
    return (-value[0], -value[1])


def _ac_mul(lhs, rhs):
    return (
        lhs[0]*rhs[0] - lhs[1]*rhs[1],
        lhs[0]*rhs[1] + lhs[1]*rhs[0],
    )


def _ac_inv(value):
    norm2 = value[0]*value[0] + value[1]*value[1]
    return (value[0]/norm2, -value[1]/norm2)


def _ac_abs_upper(value):
    return abs(value[0]) + abs(value[1])


def _ac_abs_lower(value):
    return max(abs(value[0]), abs(value[1]))


class _AffineDisk3:
    __slots__ = ("center", "linear", "remainder")

    def __init__(self, center=0, linear=None, remainder=0):
        if isinstance(center, tuple):
            self.center = (
                _Fraction(center[0]),
                _Fraction(center[1]),
            )
        else:
            self.center = (_Fraction(center), _Fraction(0))
        if linear is None:
            linear = (((0, 0)), ((0, 0)), ((0, 0)))
        self.linear = tuple(
            (_Fraction(value[0]), _Fraction(value[1]))
            for value in linear
        )
        assert len(self.linear) == 3
        self.remainder = _Fraction(remainder)

    @staticmethod
    def coerce(value):
        if isinstance(value, _AffineDisk3):
            return value
        if isinstance(value, s.Rational):
            return _AffineDisk3(
                _Fraction(int(value.p), int(value.q))
            )
        if isinstance(value, (int, _Fraction)):
            return _AffineDisk3(value)
        raise TypeError(value)

    def linear_abs_upper(self):
        return sum(
            (_ac_abs_upper(value) for value in self.linear),
            _Fraction(0),
        )

    def abs_upper(self):
        return (
            _ac_abs_upper(self.center)
            + self.linear_abs_upper()
            + self.remainder
        )

    def __add__(self, other):
        other = self.coerce(other)
        return _AffineDisk3(
            _ac_add(self.center, other.center),
            tuple(
                _ac_add(self.linear[index], other.linear[index])
                for index in range(3)
            ),
            self.remainder + other.remainder,
        )

    __radd__ = __add__

    def __neg__(self):
        return _AffineDisk3(
            _ac_neg(self.center),
            tuple(_ac_neg(value) for value in self.linear),
            self.remainder,
        )

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        lhs_linear = self.linear_abs_upper()
        rhs_linear = other.linear_abs_upper()
        linear = tuple(
            _ac_add(
                _ac_mul(self.center, other.linear[index]),
                _ac_mul(other.center, self.linear[index]),
            )
            for index in range(3)
        )
        remainder = (
            _ac_abs_upper(self.center)*other.remainder
            + _ac_abs_upper(other.center)*self.remainder
            + lhs_linear*rhs_linear
            + lhs_linear*other.remainder
            + rhs_linear*self.remainder
            + self.remainder*other.remainder
        )
        return _AffineDisk3(
            _ac_mul(self.center, other.center),
            linear,
            remainder,
        )

    __rmul__ = __mul__

    def inverse(self):
        center_lower = _ac_abs_lower(self.center)
        deviation = self.linear_abs_upper() + self.remainder
        assert center_lower > deviation
        inverse_center = _ac_inv(self.center)
        inverse_center_squared = _ac_mul(
            inverse_center,
            inverse_center,
        )
        linear = tuple(
            _ac_neg(_ac_mul(value, inverse_center_squared))
            for value in self.linear
        )
        remainder = (
            self.remainder/(center_lower*center_lower)
            + deviation*deviation/(
                center_lower*center_lower
                *(center_lower - deviation)
            )
        )
        return _AffineDisk3(
            inverse_center,
            linear,
            remainder,
        )

    def __truediv__(self, other):
        return self*self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other)/self

    def __pow__(self, power):
        assert isinstance(power, int) and power >= 0
        result = _AffineDisk3(1)
        base = self
        exponent = power
        while exponent:
            if exponent & 1:
                result = result*base
            base = base*base
            exponent >>= 1
        return result


def _affine_evaluate_polynomial(expression, omega_affine, epsilon_affine):
    polynomial = s.Poly(
        s.expand(expression), Omega_hor, epsilon_hor
    )
    result = _AffineDisk3(0)
    for (omega_power, epsilon_power), coefficient in polynomial.terms():
        assert coefficient.is_Rational
        result += (
            _Fraction(int(coefficient.p), int(coefficient.q))
            *omega_affine**omega_power
            *epsilon_affine**epsilon_power
        )
    return result


OMEGA_HORIZON_AFFINE_220 = _AffineDisk3(
    (_Fraction(3737, 10000), -_Fraction(1779, 20000)),
    (
        (_Fraction(1, 10000), 0),
        (0, _Fraction(3, 20000)),
        (0, 0),
    ),
)
EPSILON_HORIZON_AFFINE_220 = _AffineDisk3(
    _Fraction(1, 20000),
    (
        (0, 0),
        (0, 0),
        (_Fraction(1, 20000), 0),
    ),
)
I_AFFINE_220 = _AffineDisk3((0, 1))

A_clear_affine_hor = [
    _affine_evaluate_polynomial(
        coefficient,
        OMEGA_HORIZON_AFFINE_220,
        EPSILON_HORIZON_AFFINE_220,
    )
    for coefficient in A_clear_coeff_hor
]
B_clear_affine_hor = [
    _affine_evaluate_polynomial(
        coefficient,
        OMEGA_HORIZON_AFFINE_220,
        EPSILON_HORIZON_AFFINE_220,
    )
    for coefficient in B_clear_coeff_hor
]
C_clear_affine_hor = [
    _affine_evaluate_polynomial(
        coefficient,
        OMEGA_HORIZON_AFFINE_220,
        EPSILON_HORIZON_AFFINE_220,
    )
    for coefficient in C_clear_coeff_hor
]
alpha_affine_hor = (
    -2*I_AFFINE_220*OMEGA_HORIZON_AFFINE_220
    + _Fraction(1, 36)
      *I_AFFINE_220
      *EPSILON_HORIZON_AFFINE_220
      *OMEGA_HORIZON_AFFINE_220
)

AFFINE_FROBENIUS_TRUNCATION_220 = 32
AFFINE_HORIZON_SERIES_TAIL_220 = _Fraction(1, 2**32)
AFFINE_HORIZON_DERIVATIVE_TAIL_220 = _Fraction(17, 2**27)

a_affine_hor = [_AffineDisk3(1)]
for n_value in range(1, AFFINE_FROBENIUS_TRUNCATION_220 + 1):
    denominator_affine = (
        A_clear_affine_hor[2]
        *(alpha_affine_hor + n_value)
        *(alpha_affine_hor + n_value - 1)
        + B_clear_affine_hor[1]
          *(alpha_affine_hor + n_value)
        + C_clear_affine_hor[0]
    )
    lower_affine = _AffineDisk3(0)
    for lag in range(1, min(10, n_value) + 1):
        k_value = n_value - lag
        transfer_affine = _AffineDisk3(0)
        if lag + 2 <= 10:
            transfer_affine += (
                A_clear_affine_hor[lag + 2]
                *(alpha_affine_hor + k_value)
                *(alpha_affine_hor + k_value - 1)
            )
        if lag + 1 <= 10:
            transfer_affine += (
                B_clear_affine_hor[lag + 1]
                *(alpha_affine_hor + k_value)
            )
        transfer_affine += C_clear_affine_hor[lag]
        lower_affine += transfer_affine*a_affine_hor[k_value]
    a_affine_hor.append(-lower_affine/denominator_affine)

HORIZON_AFFINE_VALUE_220 = _AffineDisk3(0)
HORIZON_AFFINE_DERIVATIVE_220 = _AffineDisk3(0)
for n_value in range(AFFINE_FROBENIUS_TRUNCATION_220 + 1):
    HORIZON_AFFINE_VALUE_220 += (
        a_affine_hor[n_value]
        *LAUNCH_RADIUS_220**n_value
    )
    if n_value > 0:
        HORIZON_AFFINE_DERIVATIVE_220 += (
            n_value
            *a_affine_hor[n_value]
            *LAUNCH_RADIUS_220**(n_value - 1)
        )
HORIZON_AFFINE_VALUE_220.remainder += (
    AFFINE_HORIZON_SERIES_TAIL_220
)
HORIZON_AFFINE_DERIVATIVE_220.remainder += (
    AFFINE_HORIZON_DERIVATIVE_TAIL_220
)

# Quantize the final model outward to compact 96-bit dyadic data.  Center and
# linear rounding errors are transferred into the nonlinear remainder.
AFFINE_ENDPOINT_DYADIC_BITS_220 = 96
AFFINE_ENDPOINT_DYADIC_SCALE_220 = 1 << AFFINE_ENDPOINT_DYADIC_BITS_220


def _round_fraction_to_dyadic(value):
    numerator = value.numerator*AFFINE_ENDPOINT_DYADIC_SCALE_220
    denominator = value.denominator
    if numerator >= 0:
        rounded = (2*numerator + denominator)//(2*denominator)
    else:
        rounded = -(
            (2*(-numerator) + denominator)//(2*denominator)
        )
    error = abs(
        value
        - _Fraction(
            rounded,
            AFFINE_ENDPOINT_DYADIC_SCALE_220,
        )
    )
    return rounded, error


def _ceil_fraction_to_dyadic(value):
    assert value >= 0
    return (
        value.numerator*AFFINE_ENDPOINT_DYADIC_SCALE_220
        + value.denominator - 1
    )//value.denominator


def _quantized_affine_record(value):
    center_re, error_re = _round_fraction_to_dyadic(value.center[0])
    center_im, error_im = _round_fraction_to_dyadic(value.center[1])
    total_error = error_re + error_im
    linear = []
    for coefficient in value.linear:
        coefficient_re, coefficient_error_re = (
            _round_fraction_to_dyadic(coefficient[0])
        )
        coefficient_im, coefficient_error_im = (
            _round_fraction_to_dyadic(coefficient[1])
        )
        total_error += coefficient_error_re + coefficient_error_im
        linear.append([coefficient_re, coefficient_im])
    radius = _ceil_fraction_to_dyadic(
        value.remainder + total_error
    )
    return {
        "center": [center_re, center_im],
        "linear": linear,
        "radius": radius,
    }


HORIZON_AFFINE_VALUE_RECORD_220 = _quantized_affine_record(
    HORIZON_AFFINE_VALUE_220
)
HORIZON_AFFINE_DERIVATIVE_RECORD_220 = _quantized_affine_record(
    HORIZON_AFFINE_DERIVATIVE_220
)
HORIZON_AFFINE_ENDPOINT_220_PAYLOAD = {
    "dyadic_bits": AFFINE_ENDPOINT_DYADIC_BITS_220,
    "variables": [
        "xi_ReOmega",
        "xi_ImOmega",
        "xi_epsilon",
    ],
    "box": {
        "Omega_re_center": "3737/10000",
        "Omega_re_radius": "1/10000",
        "Omega_im_center": "-1779/20000",
        "Omega_im_radius": "3/20000",
        "epsilon_center": "1/20000",
        "epsilon_radius": "1/20000",
    },
    "launch_radius": "1/16",
    "truncation": AFFINE_FROBENIUS_TRUNCATION_220,
    "series_tail": str(AFFINE_HORIZON_SERIES_TAIL_220),
    "derivative_tail": str(
        AFFINE_HORIZON_DERIVATIVE_TAIL_220
    ),
    "value": HORIZON_AFFINE_VALUE_RECORD_220,
    "derivative": HORIZON_AFFINE_DERIVATIVE_RECORD_220,
}
HORIZON_AFFINE_ENDPOINT_220_HASH = hashlib.sha256(
    json.dumps(
        HORIZON_AFFINE_ENDPOINT_220_PAYLOAD,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()
assert HORIZON_AFFINE_ENDPOINT_220_HASH == (
    "1d17cbf45bd030e7b85cdd6cedd8781dd1b7d1723c5c72519f915f6667ca41ff"
)

# Validated projective propagation of the affine horizon endpoint to z=3.
# The propagated variable is the regular-factor logarithmic derivative L=S'/S.
def _certify_axial_horizon_riccati_propagation_220():
    import math
    B=96; S=1<<B; NV=3

    def nint(fr):
        n,d=fr.numerator,fr.denominator
        return (2*n+d)//(2*d) if n>=0 else -((2*(-n)+d)//(2*d))
    def ceilq(fr):
        assert fr>=0
        return (fr.numerator+fr.denominator-1)//fr.denominator
    def rs(fr):
        n=nint(_Fraction(fr)*S); return n,abs(_Fraction(fr)-_Fraction(n,S))
    SB=128; SS=1<<SB
    def supq(fr):
        x=_Fraction(fr)*SS
        return _Fraction((x.numerator+x.denominator-1)//x.denominator,SS)
    def infq(fr):
        x=_Fraction(fr)*SS
        return _Fraction(x.numerator//x.denominator,SS)

    class C:
        __slots__=('cr','ci','rad')
        def __init__(self,re=0,im=0,rad=0,raw=False):
            if raw:self.cr=int(re);self.ci=int(im);self.rad=int(rad);return
            a,ea=rs(re);b,eb=rs(im);self.cr=a;self.ci=b;self.rad=ceilq((_Fraction(rad)+ea+eb)*S)
        @classmethod
        def raw(cls,a,b,r=0):return cls(a,b,r,True)
        @classmethod
        def co(cls,x):return x if isinstance(x,C) else C(x)
        def au(self):return _Fraction(abs(self.cr)+abs(self.ci)+self.rad,S)
        def lo(self):return _Fraction(max(abs(self.cr),abs(self.ci))-self.rad,S)
        def __add__(self,o):
            o=C.co(o);return C.raw(self.cr+o.cr,self.ci+o.ci,self.rad+o.rad)
        __radd__=__add__
        def __neg__(self):return C.raw(-self.cr,-self.ci,self.rad)
        def __sub__(self,o):return self+(-C.co(o))
        def __rsub__(self,o):return C.co(o)-self
        def __mul__(self,o):
            o=C.co(o)
            rn=self.cr*o.cr-self.ci*o.ci; inn=self.cr*o.ci+self.ci*o.cr
            a=nint(_Fraction(rn,S));b=nint(_Fraction(inn,S))
            err=abs(rn-a*S)+abs(inn-b*S)
            c1=abs(self.cr)+abs(self.ci);c2=abs(o.cr)+abs(o.ci)
            cross=c1*o.rad+c2*self.rad+self.rad*o.rad
            return C.raw(a,b,(cross+err+S-1)//S)
        __rmul__=__mul__
        def inv(self):
            a=_Fraction(self.cr,S);b=_Fraction(self.ci,S);rr=_Fraction(self.rad,S)
            L=max(abs(a),abs(b));assert L>rr,(float(L),float(rr))
            den=a*a+b*b;re=a/den;im=-b/den
            x,ex=rs(re);y,ey=rs(im)
            rem=rr/(L*(L-rr))+ex+ey
            return C.raw(x,y,ceilq(rem*S))
        def __truediv__(self,o):return self*C.co(o).inv()
        def __rtruediv__(self,o):return C.co(o)/self
        def __pow__(self,n):
            out=C(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out
        def comp(self):return complex(self.cr/S,self.ci/S)

    class U:
        __slots__=('v','d')
        def __init__(self,v=0,d=None):self.v=C.co(v);self.d=list(d or [C(0),C(0),C(0)])
        @classmethod
        def co(cls,x):return x if isinstance(x,U) else U(x)
        def __add__(self,o):
            o=U.co(o);return U(self.v+o.v,[self.d[j]+o.d[j] for j in range(NV)])
        __radd__=__add__
        def __neg__(self):return U(-self.v,[-x for x in self.d])
        def __sub__(self,o):return self+(-U.co(o))
        def __rsub__(self,o):return U.co(o)-self
        def __mul__(self,o):
            o=U.co(o);return U(self.v*o.v,[self.d[j]*o.v+self.v*o.d[j] for j in range(NV)])
        __rmul__=__mul__
        def inv(self):
            iv=self.v.inv();iv2=iv*iv;return U(iv,[-x*iv2 for x in self.d])
        def __truediv__(self,o):return self*U.co(o).inv()
        def __rtruediv__(self,o):return U.co(o)/self
        def __pow__(self,n):
            out=U(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out

    def sadd(a,b,N):return [(a[i] if i<len(a) else U(0))+(b[i] if i<len(b) else U(0)) for i in range(N)]
    def sneg(a):return [-x for x in a]
    def ssub(a,b,N):return sadd(a,sneg(b),N)
    def smul(a,b,N):
        out=[U(0) for _ in range(N)]
        for i in range(min(N,len(a))):
            for j in range(min(N-i,len(b))):out[i+j]=out[i+j]+a[i]*b[j]
        return out
    def sscale(a,c,N):return [x*c for x in a[:N]]+[U(0)]*max(0,N-len(a))
    def pneg(c,k,N):return [U(((-1)**n)*math.comb(k+n-1,n)/c**(k+n)) for n in range(N)]
    def ppos(c,k,N):return [U(math.comb(k,n)*c**(k-n)) if n<=k else U(0) for n in range(N)]

    def de_series(c,N,O,e):
        xi=pneg(c,1,N);xi2=pneg(c,2,N);xi3=pneg(c,3,N);z0=c+2
        zm={k:pneg(z0,k,N) for k in [1,2,3,4,6,7,8,9]};zp={k:ppos(z0,k,N) for k in [1,2,3,4]};one=[U(1)]+[U(0)]*(N-1)
        f=ssub(one,sscale(zm[1],2,N),N);fp=sscale(zm[2],2,N)
        invf=smul(zp[1],xi,N);invf2=smul(zp[2],xi2,N);invf3=smul(zp[3],xi3,N)
        P1=sadd(sadd(sscale(zm[6],12,N),sscale(zm[7],-_Fraction(176,9),N),N),sscale(zm[2],-_Fraction(5,36),N),N)
        P1p=sadd(sadd(sscale(zm[7],-72,N),sscale(zm[8],_Fraction(1232,9),N),N),sscale(zm[3],_Fraction(5,18),N),N)
        F1=sadd(sadd(sscale(zm[6],24,N),sscale(zm[7],-_Fraction(392,9),N),N),sscale(zm[2],-_Fraction(5,36),N),N)
        V0=ssub(sscale(zm[2],6,N),sscale(zm[3],6,N),N);V0p=sadd(sscale(zm[3],-12,N),sscale(zm[4],18,N),N)
        num=sadd(ssub(sscale(one,653,N),sscale(zp[1],281,N),N),sscale(zp[4],4*(O*O),N),N)
        dV=sscale(smul(num,zm[9],N),-8,N);V1=ssub(dV,sscale(V0p,_Fraction(5,72),N),N)
        C0=ssub([O*O]+[U(0)]*(N-1),smul(f,V0,N),N);C1=sneg(sadd(smul(F1,V0,N),smul(f,V1,N),N))
        I=U(C(0,1));a0=-2*I*O;a1=_Fraction(1,36)*I*O;g0=a0*(a0-1);g1=a1*(2*a0-1)
        common=ssub(smul(P1p,invf,N),smul(smul(P1,fp,N),invf2,N),N)
        dd=sadd(sadd(sscale(xi,2*a0,N),smul(fp,invf,N),N),sscale(sadd(sscale(xi,2*a1,N),common,N),e,N),N)
        e0=sadd(sscale(xi2,g0,N),sscale(smul(smul(fp,invf,N),xi,N),a0,N),N);e0=sadd(e0,smul(C0,invf2,N),N)
        e1=sadd(sscale(xi2,g1,N),sscale(smul(common,xi,N),a0,N),N);e1=sadd(e1,sscale(smul(smul(fp,invf,N),xi,N),a1,N),N);e1=sadd(e1,smul(C1,invf2,N),N);e1=ssub(e1,sscale(smul(smul(P1,C0,N),invf3,N),2,N),N)
        return dd,sadd(e0,sscale(e1,e,N),N)

    class D:
        __slots__=('re','im','r')
        def __init__(self,re=0,im=0,r=0):self.re=_Fraction(re);self.im=_Fraction(im);self.r=_Fraction(r)
        @classmethod
        def co(cls,x):return x if isinstance(x,D) else D(x)
        def au(self):return abs(self.re)+abs(self.im)+self.r
        def __add__(self,o):o=D.co(o);return D(self.re+o.re,self.im+o.im,self.r+o.r)
        __radd__=__add__
        def __neg__(self):return D(-self.re,-self.im,self.r)
        def __sub__(self,o):return self+(-D.co(o))
        def __rsub__(self,o):return D.co(o)-self
        def __mul__(self,o):
            o=D.co(o);c1=abs(self.re)+abs(self.im);c2=abs(o.re)+abs(o.im)
            return D(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re,c1*o.r+c2*self.r+self.r*o.r)
        __rmul__=__mul__
        def inv(self):
            L=max(abs(self.re),abs(self.im));assert L>self.r,(float(L),float(self.r))
            den=self.re*self.re+self.im*self.im
            return D(self.re/den,-self.im/den,self.r/(L*(L-self.r)))
        def __truediv__(self,o):return self*D.co(o).inv()
        def __rtruediv__(self,o):return D.co(o)/self
        def __pow__(self,n):
            out=D(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out

    class DU:
        __slots__=('v','d')
        def __init__(self,v=0,d=None):self.v=D.co(v);self.d=list(d or [D(0),D(0),D(0)])
        @classmethod
        def co(cls,x):return x if isinstance(x,DU) else DU(x)
        def __add__(self,o):
            o=DU.co(o);return DU(self.v+o.v,[self.d[j]+o.d[j] for j in range(NV)])
        __radd__=__add__
        def __neg__(self):return DU(-self.v,[-x for x in self.d])
        def __sub__(self,o):return self+(-DU.co(o))
        def __rsub__(self,o):return DU.co(o)-self
        def __mul__(self,o):
            o=DU.co(o);return DU(self.v*o.v,[self.d[j]*o.v+self.v*o.d[j] for j in range(NV)])
        __rmul__=__mul__
        def inv(self):
            iv=self.v.inv();iv2=iv*iv;return DU(iv,[-x*iv2 for x in self.d])
        def __truediv__(self,o):return self*DU.co(o).inv()
        def __rtruediv__(self,o):return DU.co(o)/self
        def __pow__(self,n):
            out=DU(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out

    class P:
        def __init__(self,a=0):
            self.c={} if isinstance(a,dict) else {(0,0,0):D.co(a)}
            if isinstance(a,dict):self.c={m:D.co(v) for m,v in a.items()}
        @classmethod
        def co(cls,x):return x if isinstance(x,P) else P(x)
        def __add__(self,o):
            o=P.co(o);d=dict(self.c)
            for m,v in o.c.items():d[m]=d.get(m,D(0))+v
            return P(d)
        __radd__=__add__
        def __neg__(self):return P({m:-v for m,v in self.c.items()})
        def __sub__(self,o):return self+(-P.co(o))
        def __rsub__(self,o):return P.co(o)-self
        def __mul__(self,o):
            o=P.co(o);d={}
            for a,x in self.c.items():
                for b,y in o.c.items():
                    m=tuple(a[i]+b[i] for i in range(3));d[m]=d.get(m,D(0))+x*y
            return P(d)
        __rmul__=__mul__
        def __truediv__(self,o):
            if isinstance(o,P):assert set(o.c)=={(0,0,0)};o=o.c[(0,0,0)]
            return P({m:v/o for m,v in self.c.items()})
        def __rtruediv__(self,o):assert set(self.c)=={(0,0,0)};return P(o/self.c[(0,0,0)])
        def __pow__(self,n):
            out=P(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out
        def sumdeg(self,lo,hi=99):return sum((v.au() for m,v in self.c.items() if lo<=sum(m)<=hi),_Fraction(0))
        def at(self,m):return self.c.get(m,D(0))

    def coefficient_objects(x):
        z=x+2;O=P({(0,0,0):D(_Fraction(3737,10000),-_Fraction(1779,20000)),(1,0,0):D(_Fraction(1,10000)),(0,1,0):D(0,_Fraction(3,20000))});ep=P({(0,0,0):D(_Fraction(1,20000)),(0,0,1):D(_Fraction(1,20000))})
        f=x/z;fp=2/z**2;P1=12/z**6-_Fraction(176,9)/z**7-_Fraction(5,36)/z**2;P1p=-72/z**7+_Fraction(1232,9)/z**8+_Fraction(5,18)/z**3
        F1=24/z**6-_Fraction(392,9)/z**7-_Fraction(5,36)/z**2;V0=6/z**2-6/z**3;V0p=-12/z**3+18/z**4
        dV=-8*(653-281*z+4*(O*O)*z**4)/z**9;V1=dV-_Fraction(5,72)*V0p;C0=O*O-f*V0;C1=-(F1*V0+f*V1)
        I=P(D(0,1));a0=-2*I*O;a1=_Fraction(1,36)*I*O;g0=a0*(a0-1);g1=a1*(2*a0-1);invf=z/x;invf2=z**2/x**2;invf3=z**3/x**3;common=P1p*invf-P1*fp*invf2
        dd=2*a0/x+fp*invf+ep*(2*a1/x+common)
        ee=g0/x**2+a0*fp*invf/x+C0*invf2+ep*(g1/x**2+a0*common/x+a1*fp*invf/x+C1*invf2-2*P1*C0*invf3)
        return dd,ee

    def ric_bounds(c,h):
        dd,ee=coefficient_objects(P(D(c+h/2,0,h/2)));unit=[tuple(1 if i==j else 0 for i in range(3)) for j in range(3)]
        d0=dd.at((0,0,0)).au();e0=ee.at((0,0,0)).au();jd=sum(dd.at(m).au() for m in unit);je=sum(ee.at(m).au() for m in unit);dr=dd.sumdeg(2);er=ee.sumdeg(2);df=dd.sumdeg(0);ef=ee.sumdeg(0)
        dc=dd.at((0,0,0));dreal=dc.re-dc.r
        for m,v in dd.c.items():
            if m!=(0,0,0):dreal-=abs(v.re)+v.r
        return d0,e0,jd,je,dr,er,df,ef,dreal

    def analytic_bounds(c,R):
        x=DU(D(c,0,R));z=x+2;O=DU(D(_Fraction(3737,10000),-_Fraction(1779,20000)),[D(_Fraction(1,10000)),D(0,_Fraction(3,20000)),D(0)]);ep=DU(D(_Fraction(1,20000)),[D(0),D(0),D(_Fraction(1,20000))])
        f=x/z;fp=2/z**2;P1=12/z**6-_Fraction(176,9)/z**7-_Fraction(5,36)/z**2;P1p=-72/z**7+_Fraction(1232,9)/z**8+_Fraction(5,18)/z**3
        F1=24/z**6-_Fraction(392,9)/z**7-_Fraction(5,36)/z**2;V0=6/z**2-6/z**3;V0p=-12/z**3+18/z**4
        dV=-8*(653-281*z+4*(O*O)*z**4)/z**9;V1=dV-_Fraction(5,72)*V0p;C0=O*O-f*V0;C1=-(F1*V0+f*V1)
        I=DU(D(0,1));a0=-2*I*O;a1=_Fraction(1,36)*I*O;g0=a0*(a0-1);g1=a1*(2*a0-1);common=P1p/f-P1*fp/f**2
        dd=2*a0/x+fp/f+ep*(2*a1/x+common)
        ee=g0/x**2+a0*fp/(x*f)+C0/f**2+ep*(g1/x**2+a0*common/x+a1*fp/(x*f)+C1/f**2-2*P1*C0/f**3)
        return dd.v.au(),ee.v.au(),sum(z.au() for z in dd.d),sum(z.au() for z in ee.d)

    def find_center_bound(Y,R,d0,e0):
        B=supq(max(_Fraction(1),2*Y))
        for _ in range(64):
            rhs=supq(Y+R*(B*B+d0*B+e0))
            if rhs<=B and R*(2*B+d0)<1:return B
            B=supq(max(_Fraction(5,4)*B,_Fraction(21,20)*rhs))
        raise AssertionError('center majorant failed')

    def ric_step(l0,ls,c,h,N,O,e):
        d,ee=de_series(c,N,O,e);a0=[l0];ajs=[[ls[j]] for j in range(3)]
        for n in range(N):
            q=C(0)
            for k in range(n+1):q=q+a0[k]*a0[n-k]+d[k].v*a0[n-k]
            a0.append(-(q+ee[n].v)/_Fraction(n+1))
            for j in range(3):
                q=C(0)
                for k in range(n+1):q=q+(2*a0[k]+d[k].v)*ajs[j][n-k]+d[k].d[j]*a0[n-k]
                ajs[j].append(-(q+ee[n].d[j])/_Fraction(n+1))
        def ev(seq):
            out=C(0);hp=C(1)
            for n in range(N+1):out=out+seq[n]*hp;hp=hp*h
            return out
        ol0=ev(a0);ols=[ev(v) for v in ajs]
        arithmetic=_Fraction(ol0.rad+sum(z.rad for z in ols),S)
        ol0.rad=0
        for z in ols:z.rad=0
        R=c/_Fraction(16);d0b,e0b,jd,je=analytic_bounds(c,R);B0=find_center_bound(l0.au(),R,d0b,e0b);den=1-R*(2*B0+d0b);assert den>0
        B1=supq((sum(z.au() for z in ls)+R*(jd*B0+je))/den);rho=abs(h)/R;tail=supq((B0+B1)*rho**(N+1)/(1-rho));local=supq(tail+arithmetic)
        return ol0,ols,local,tail,arithmetic


    # Fast fixed-width outward polynomial bounds.  These replace only the
    # Fraction-valued disk-bound layer above; all inequalities remain outward.
    class PC:
        def __init__(self,a=0):
            self.c={} if isinstance(a,dict) else {(0,0,0):C.co(a)}
            if isinstance(a,dict):self.c={m:C.co(v) for m,v in a.items()}
        @classmethod
        def co(cls,x):return x if isinstance(x,PC) else PC(x)
        def __add__(self,o):
            o=PC.co(o);d=dict(self.c)
            for m,v in o.c.items():d[m]=d.get(m,C(0))+v
            return PC(d)
        __radd__=__add__
        def __neg__(self):return PC({m:-v for m,v in self.c.items()})
        def __sub__(self,o):return self+(-PC.co(o))
        def __rsub__(self,o):return PC.co(o)-self
        def __mul__(self,o):
            o=PC.co(o);d={}
            for a,x in self.c.items():
                for b,y in o.c.items():
                    m=tuple(a[i]+b[i] for i in range(3));d[m]=d.get(m,C(0))+x*y
            return PC(d)
        __rmul__=__mul__
        def __truediv__(self,o):
            if isinstance(o,PC):assert set(o.c)=={(0,0,0)};o=o.c[(0,0,0)]
            return PC({m:v/o for m,v in self.c.items()})
        def __rtruediv__(self,o):assert set(self.c)=={(0,0,0)};return PC(o/self.c[(0,0,0)])
        def __pow__(self,n):
            out=PC(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out
        def sumdeg(self,lo,hi=99):return sum((v.au() for m,v in self.c.items() if lo<=sum(m)<=hi),_Fraction(0))
        def at(self,m):return self.c.get(m,C(0))

    def coefficient_objects_fast(x):
        z=x+2;O=PC({(0,0,0):C(_Fraction(3737,10000),-_Fraction(1779,20000)),(1,0,0):C(_Fraction(1,10000)),(0,1,0):C(0,_Fraction(3,20000))});ep=PC({(0,0,0):C(_Fraction(1,20000)),(0,0,1):C(_Fraction(1,20000))})
        f=x/z;fp=2/z**2;P1=12/z**6-_Fraction(176,9)/z**7-_Fraction(5,36)/z**2;P1p=-72/z**7+_Fraction(1232,9)/z**8+_Fraction(5,18)/z**3
        F1=24/z**6-_Fraction(392,9)/z**7-_Fraction(5,36)/z**2;V0=6/z**2-6/z**3;V0p=-12/z**3+18/z**4
        dV=-8*(653-281*z+4*(O*O)*z**4)/z**9;V1=dV-_Fraction(5,72)*V0p;C0=O*O-f*V0;C1=-(F1*V0+f*V1)
        I=PC(C(0,1));a0=-2*I*O;a1=_Fraction(1,36)*I*O;g0=a0*(a0-1);g1=a1*(2*a0-1);invf=z/x;invf2=z**2/x**2;invf3=z**3/x**3;common=P1p*invf-P1*fp*invf2
        dd=2*a0/x+fp*invf+ep*(2*a1/x+common)
        ee=g0/x**2+a0*fp*invf/x+C0*invf2+ep*(g1/x**2+a0*common/x+a1*fp*invf/x+C1*invf2-2*P1*C0*invf3)
        return dd,ee

    def ric_bounds(c,h):
        dd,ee=coefficient_objects_fast(PC(C(c+h/2,rad=h/2)));unit=[tuple(1 if i==j else 0 for i in range(3)) for j in range(3)]
        d0=dd.at((0,0,0)).au();e0=ee.at((0,0,0)).au();jd=sum(dd.at(m).au() for m in unit);je=sum(ee.at(m).au() for m in unit);dr=dd.sumdeg(2);er=ee.sumdeg(2);df=dd.sumdeg(0);ef=ee.sumdeg(0)
        dc=dd.at((0,0,0));dreal=_Fraction(dc.cr-dc.rad,S)
        for m,v in dd.c.items():
            if m!=(0,0,0):dreal-=_Fraction(abs(v.cr)+v.rad,S)
        return d0,e0,jd,je,dr,er,df,ef,dreal

    def analytic_bounds(c,R):
        x=U(C(c,rad=R));z=x+2;O=U(C(_Fraction(3737,10000),-_Fraction(1779,20000)),[C(_Fraction(1,10000)),C(0,_Fraction(3,20000)),C(0)]);ep=U(C(_Fraction(1,20000)),[C(0),C(0),C(_Fraction(1,20000))])
        f=x/z;fp=2/z**2;P1=12/z**6-_Fraction(176,9)/z**7-_Fraction(5,36)/z**2;P1p=-72/z**7+_Fraction(1232,9)/z**8+_Fraction(5,18)/z**3
        F1=24/z**6-_Fraction(392,9)/z**7-_Fraction(5,36)/z**2;V0=6/z**2-6/z**3;V0p=-12/z**3+18/z**4
        dV=-8*(653-281*z+4*(O*O)*z**4)/z**9;V1=dV-_Fraction(5,72)*V0p;C0=O*O-f*V0;C1=-(F1*V0+f*V1)
        I=U(C(0,1));a0=-2*I*O;a1=_Fraction(1,36)*I*O;g0=a0*(a0-1);g1=a1*(2*a0-1);common=P1p/f-P1*fp/f**2
        dd=2*a0/x+fp/f+ep*(2*a1/x+common)
        ee=g0/x**2+a0*fp/(x*f)+C0/f**2+ep*(g1/x**2+a0*common/x+a1*fp/(x*f)+C1/f**2-2*P1*C0/f**3)
        return dd.v.au(),ee.v.au(),sum(z.au() for z in dd.d),sum(z.au() for z in ee.d)

    # exact launch quotient affine model
    def gg(pair):return (_Fraction(pair[0],S),_Fraction(pair[1],S))
    def ga(a,b):return (a[0]+b[0],a[1]+b[1])
    def gn(a):return (-a[0],-a[1])
    def gs(a,b):return ga(a,gn(b))
    def gm(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def gi(a):
        d=a[0]*a[0]+a[1]*a[1];return (a[0]/d,-a[1]/d)
    def gau(a):return abs(a[0])+abs(a[1])
    def glo(a):return max(abs(a[0]),abs(a[1]))
    def qg(a):
        ar=nint(a[0]*S);ai=nint(a[1]*S);return C.raw(ar,ai,0),abs(a[0]-_Fraction(ar,S))+abs(a[1]-_Fraction(ai,S))
    p=HORIZON_AFFINE_ENDPOINT_220_PAYLOAD;u0,v0=gg(p['value']['center']),gg(p['derivative']['center']);us=[gg(z) for z in p['value']['linear']];vs=[gg(z) for z in p['derivative']['linear']];Ru=_Fraction(p['value']['radius'],S);Rv=_Fraction(p['derivative']['radius'],S);Rvec=Ru+Rv
    inv=gi(u0);inv2=gm(inv,inv);lc=gm(v0,inv);lins=[gs(gm(vs[j],inv),gm(gm(v0,us[j]),inv2)) for j in range(3)]
    Ulin=sum(gau(z) for z in us);Vlin=sum(gau(z) for z in vs);L0=glo(u0);Dtot=Ulin+Rvec;assert L0>Dtot
    Rinv=Rvec/(L0*L0)+Dtot*Dtot/(L0*L0*(L0-Dtot));Ilin=sum(gau(gm(us[j],inv2)) for j in range(3));Rlog=gau(v0)*Rinv+gau(inv)*Rvec+Vlin*Ilin+Vlin*Rinv+Ilin*Rvec+Rvec*Rinv
    l0,qe=qg(lc);ls=[]
    for z in lins:q,e1=qg(z);ls.append(q);qe+=e1
    Rtot=supq(Rlog+qe)
    O=U(C(_Fraction(3737,10000),-_Fraction(1779,20000)),[C(_Fraction(1,10000)),C(0,_Fraction(3,20000)),C(0)]);ep=U(C(_Fraction(1,20000)),[C(0),C(0),C(_Fraction(1,20000))])
    x=_Fraction(1,16);N=12;steps=0;mt=_Fraction(0);ma=_Fraction(0);min_damping=None
    while x<1:
        h=_Fraction(1,1024) if x<_Fraction(1,8) else _Fraction(1,512) if x<_Fraction(1,4) else _Fraction(1,256) if x<_Fraction(1,2) else _Fraction(1,128)
        if x+h>1:h=1-x
        d0b,e0b,jd,je,dr,er,df,ef,dreal=ric_bounds(x,h);B0=find_center_bound(l0.au(),h,d0b,e0b);den=1-h*(2*B0+d0b);assert den>0;B1=supq((sum(z.au() for z in ls)+h*(jd*B0+je))/den)
        F=supq(B1*B1+jd*B1+dr*(B0+B1)+er);center_var=supq(h*(B0*B0+d0b*B0+e0b));m=infq(dreal+2*(_Fraction(l0.cr,S)-center_var-B1));min_damping=m if min_damping is None else min(min_damping,m)
        Be=supq(max(Rtot,2*(Rtot+h*F)))
        for _ in range(32):
            rhs=supq(Rtot+h*(Be*Be+F))
            if rhs<=Be:break
            Be=supq(max(_Fraction(5,4)*Be,_Fraction(21,20)*rhs))
        else:raise AssertionError('error majorant failed')
        nl0,nls,local,tail,arith=ric_step(l0,ls,x,h,N,O,ep)
        if m>=0:Rnext=supq(Rtot/(1+m*h)+h*(F+Be*Be))
        else:Rnext=supq((Rtot+h*(F+Be*Be))/(1+m*h))
        Rtot=supq(Rnext+local);l0,ls=nl0,nls;x+=h;steps+=1;mt=max(mt,tail);ma=max(ma,arith)
        if steps%64==0:print('step',steps,float(x),l0.comp(),float(Rtot),float(m),float(tail),float(arith),flush=True)
    # Physical matching point: x(z=3)=1+5*epsilon/72.
    # Split it into a fixed center shift and one normalized epsilon direction.
    delta0=_Fraction(1,288000);delta3=_Fraction(1,288000)
    h=delta0;d0b,e0b,jd,je,dr,er,df,ef,dreal=ric_bounds(x,h);B0=find_center_bound(l0.au(),h,d0b,e0b);den=1-h*(2*B0+d0b);assert den>0;B1=supq((sum(z.au() for z in ls)+h*(jd*B0+je))/den)
    F=supq(B1*B1+jd*B1+dr*(B0+B1)+er);center_var=supq(h*(B0*B0+d0b*B0+e0b));m=infq(dreal+2*(_Fraction(l0.cr,S)-center_var-B1));min_damping=min(min_damping,m)
    Be=supq(max(Rtot,2*(Rtot+h*F)))
    for _ in range(32):
        rhs=supq(Rtot+h*(Be*Be+F))
        if rhs<=Be:break
        Be=supq(max(_Fraction(5,4)*Be,_Fraction(21,20)*rhs))
    else:raise AssertionError('center-shift error majorant failed')
    nl0,nls,local,tail,arith=ric_step(l0,ls,x,h,N,O,ep)
    if m>=0:Rnext=supq(Rtot/(1+m*h)+h*(F+Be*Be))
    else:Rnext=supq((Rtot+h*(F+Be*Be))/(1+m*h))
    Rtot=supq(Rnext+local);l0,ls=nl0,nls;x+=h;steps+=1;mt=max(mt,tail);ma=max(ma,arith)

    # The remaining endpoint displacement is eta=delta3*xi_epsilon.
    # Add its first-order contribution to the epsilon sensitivity.
    dser,eser=de_series(x,1,O,ep);F0=-(l0*l0+dser[0].v*l0+eser[0].v);corr=F0*delta3
    shift_arith=_Fraction(corr.rad,S);corr.rad=0;ls[2]=ls[2]+corr;shift_arith+=_Fraction(ls[2].rad,S);ls[2].rad=0

    # Bound omitted parameter cross-terms and the quadratic x-Taylor tail.
    ddp,eep=coefficient_objects_fast(PC(C(x)))
    dc,ec=ddp.at((0,0,0)),eep.at((0,0,0))
    Dd=_Fraction(dc.rad,S)+ddp.sumdeg(1);De=_Fraction(ec.rad,S)+eep.sumdeg(1)
    Lc=l0.au();Lvar=sum(z.au() for z in ls)+Rtot;dcenter=_Fraction(abs(dc.cr)+abs(dc.ci),S)
    Fvar=supq(2*Lc*Lvar+Lvar*Lvar+dcenter*Lvar+Dd*(Lc+Lvar)+De)
    Rdisk=x/_Fraction(16);ddisk,eedisk=coefficient_objects_fast(PC(C(x,rad=Rdisk)));Dfull=ddisk.sumdeg(0);Efull=eedisk.sumdeg(0)
    Bfull=find_center_bound(Lc+sum(z.au() for z in ls)+Rtot,Rdisk,Dfull,Efull);rho=delta3/Rdisk
    shift_tail=supq(Bfull*rho*rho/(1-rho));shift=supq(delta3*Fvar+shift_tail+shift_arith);Rtot=supq(Rtot+shift)
    rec={'method':'96-bit fixed-grid dyadic damping-aware Riccati center-sensitivity Taylor with affine shifted-endpoint correction','variables':['xi_ReOmega','xi_ImOmega','xi_epsilon'],'launch_x':'1/16','matching_z':'3','matching_x_center':'1+1/288000','taylor_order':N,'steps':steps,'log_derivative':{'center':[l0.cr,l0.ci],'linear':[[z.cr,z.ci] for z in ls],'dyadic_bits':B,'radius':ceilq(Rtot*S)},'pre_shift_remainder':str(Rtot-shift),'physical_shift_remainder':str(shift),'physical_shift_center':'1/288000','physical_shift_linear':'1/288000','min_damping_lower':str(min_damping),'max_taylor_tail':str(mt),'max_step_arithmetic_radius':str(ma)}
    hh=hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    rec['hash']=hh
    assert hh == '6354eafe4b56c5b12c8dabde074323469578cad36bd74d875c3f7edf96b2da86'
    return rec

HORIZON_RICCATI_PROPAGATION_220_PAYLOAD = (
    _certify_axial_horizon_riccati_propagation_220()
)
assert HORIZON_RICCATI_PROPAGATION_220_PAYLOAD["hash"] == (
    "6354eafe4b56c5b12c8dabde074323469578cad36bd74d875c3f7edf96b2da86"
)
HORIZON_RICCATI_DYADIC_BITS_220 = (
    HORIZON_RICCATI_PROPAGATION_220_PAYLOAD["log_derivative"]["dyadic_bits"]
)
HORIZON_RICCATI_DYADIC_SCALE_220 = 1 << HORIZON_RICCATI_DYADIC_BITS_220
HORIZON_RICCATI_RADIUS_220 = _Fraction(
    HORIZON_RICCATI_PROPAGATION_220_PAYLOAD["log_derivative"]["radius"],
    HORIZON_RICCATI_DYADIC_SCALE_220,
)
assert HORIZON_RICCATI_RADIUS_220 < _Fraction(1, 100000)


# Outgoing ell=2 axial Jost endpoint on the complex ray z=3+i*t.
# Infinity is irregular; no convergent Frobenius claim is made. Instead,
# q=P*d_z(log Phi)-i*Omega is represented by an exact epsilon-linear
# Laurent recurrence, and its remainder is enclosed by a vertical-ray
# Volterra contraction where the outgoing exponential decays.
def _certify_axial_infinity_jost_endpoint_220():
    from fractions import Fraction as Q
    class G:
        __slots__ = ('re','im')
        def __init__(self,re=0,im=0): self.re=Q(re); self.im=Q(im)
        @staticmethod
        def co(x): return x if isinstance(x,G) else G(x)
        def __add__(self,o): o=G.co(o); return G(self.re+o.re,self.im+o.im)
        __radd__=__add__
        def __neg__(self): return G(-self.re,-self.im)
        def __sub__(self,o): return self+(-G.co(o))
        def __rsub__(self,o): return G.co(o)-self
        def __mul__(self,o): o=G.co(o); return G(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
        __rmul__=__mul__
        def iszero(self): return self.re==0 and self.im==0

    def L(a=0):
        if isinstance(a,dict):
            return {int(k):G.co(v) for k,v in a.items() if not G.co(v).iszero()}
        g=G.co(a); return {} if g.iszero() else {0:g}
    def ladd(a,b):
        d=dict(a)
        for k,v in b.items(): d[k]=d.get(k,G())+v
        return {k:v for k,v in d.items() if not v.iszero()}
    def lneg(a): return {k:-v for k,v in a.items()}
    def lsub(a,b): return ladd(a,lneg(b))
    def lmul(a,b):
        d={}
        for i,x in a.items():
            for j,y in b.items(): d[i+j]=d.get(i+j,G())+x*y
        return {k:v for k,v in d.items() if not v.iszero()}
    def lscale(a,c):
        c=G.co(c); d={}
        for k,v in a.items():
            w=v*c
            if not w.iszero(): d[k]=w
        return d
    def lshift(a,n): return {k+n:v for k,v in a.items()}
    def lder(a): return {k-1:G(v.re*k,v.im*k) for k,v in a.items() if k}

    def P(a=0,b=0): return (L(a),L(b))
    def padd(a,b): return (ladd(a[0],b[0]),ladd(a[1],b[1]))
    def pneg(a): return (lneg(a[0]),lneg(a[1]))
    def psub(a,b): return padd(a,pneg(b))
    def pscale(a,c): return (lscale(a[0],c),lscale(a[1],c))
    def pmul(a,b): return (lmul(a[0],b[0]),ladd(lmul(a[0],b[1]),lmul(a[1],b[0])))
    def pdiv_2iOmega(a):
        fac=G(0,-Q(1,2))
        return (lscale(lshift(a[0],-1),fac),lscale(lshift(a[1],-1),fac))

    def Qcoef(n):
        if n==2:return P(6)
        if n==3:return P(-18)
        if n==4:return P(12)
        if n==5:return P(0,{2:G(-32)})
        if n==6:return P(0,{2:G(64)})
        if n==8:return P(0,2392)
        if n==9:return P(0,-Q(30376,3))
        if n==10:return P(0,Q(32128,3))
        return P()

    def coeffs(N):
        c=[P() for _ in range(N+1)]
        for n in range(2,N+1):
            rhs=Qcoef(n)
            if n-1>=2: rhs=padd(rhs,pscale(c[n-1],n-1))
            if n-2>=2: rhs=psub(rhs,pscale(c[n-2],2*(n-2)))
            if n-7>=2: rhs=padd(rhs,(L(),lscale(c[n-7][0],12*(n-7))))
            if n-8>=2: rhs=padd(rhs,(L(),lscale(c[n-8][0],-Q(176,9)*(n-8))))
            square=P()
            for j in range(2,n-1): square=padd(square,pmul(c[j],c[n-j]))
            c[n]=pdiv_2iOmega(psub(rhs,square))
        return c

    def residual(c,N):
        out={}
        for n in range(2,max(2*N,N+8)+1):
            v=P()
            if n<=N:
                v=padd(v,(lscale(lshift(c[n][0],1),G(0,2)),lscale(lshift(c[n][1],1),G(0,2))))
            if 2<=n-1<=N:v=psub(v,pscale(c[n-1],n-1))
            if 2<=n-2<=N:v=padd(v,pscale(c[n-2],2*(n-2)))
            if 2<=n-7<=N:v=psub(v,(L(),lscale(c[n-7][0],12*(n-7))))
            if 2<=n-8<=N:v=psub(v,(L(),lscale(c[n-8][0],-Q(176,9)*(n-8))))
            for j in range(2,N+1):
                k=n-j
                if 2<=k<=N:v=padd(v,pmul(c[j],c[k]))
            v=psub(v,Qcoef(n))
            if v[0] or v[1]:out[n]=v
        return out

    class D:
        __slots__=('re','im','rad')
        def __init__(self,re=0,im=0,rad=0):self.re=Q(re);self.im=Q(im);self.rad=Q(rad)
        @staticmethod
        def co(x):return x if isinstance(x,D) else D(x)
        def __add__(self,o):o=D.co(o);return D(self.re+o.re,self.im+o.im,self.rad+o.rad)
        __radd__=__add__
        def __neg__(self):return D(-self.re,-self.im,self.rad)
        def __sub__(self,o):return self+(-D.co(o))
        def __rsub__(self,o):return D.co(o)-self
        def cu(self):return abs(self.re)+abs(self.im)
        def cl(self):return max(abs(self.re),abs(self.im))
        def au(self):return self.cu()+self.rad
        def __mul__(self,o):
            o=D.co(o)
            return D(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re,self.cu()*o.rad+o.cu()*self.rad+self.rad*o.rad)
        __rmul__=__mul__
        def inverse(self):
            lo=self.cl();assert lo>self.rad
            n=self.re*self.re+self.im*self.im
            return D(self.re/n,-self.im/n,self.rad/(lo*(lo-self.rad)))
        def __truediv__(self,o):return self*D.co(o).inverse()
        def __rtruediv__(self,o):return D.co(o)/self
        def __pow__(self,n):
            if n<0:return (self.inverse())**(-n)
            out=D(1);base=self
            while n:
                if n&1:out=out*base
                base=base*base;n//=2
            return out

    Omega=D(Q(3737,10000),-Q(1779,20000),Q(1,4000))
    epsilon=D(Q(1,20000),0,Q(1,20000))

    def evalL(a):
        out=D()
        for k,g in a.items():out+=D(g.re,g.im)*(Omega**k)
        return out
    def evalP(a):return evalL(a[0])+epsilon*evalL(a[1])

    def gpow(a,n):
        if n<0:
            d=a.re*a.re+a.im*a.im
            return gpow(G(a.re/d,-a.im/d),-n)
        out=G(1);base=a
        while n:
            if n&1:out=out*base
            base=base*base;n//=2
        return out

    def geval(a,o):
        out=G()
        for k,v in a.items():out+=v*gpow(o,k)
        return out

    def qceil(x,bits):
        S=1<<bits
        return (x.numerator*S+x.denominator-1)//x.denominator

    def qnearest(x,bits):
        S=1<<bits
        n=x.numerator*S;d=x.denominator
        if n>=0:return (2*n+d)//(2*d)
        return -((-2*n+d)//(2*d))

    N=14
    T=32
    c=coeffs(N)
    R=residual(c,N)
    assert min(R)==N+1
    rho=Q(1,T)
    q_bound=sum((evalP(c[n]).au()*rho**n for n in range(2,N+1)),Q())
    residual_bound=sum((evalP(v).au()*rho**n for n,v in R.items()),Q())
    eps_max=Q(1,10000)
    p_delta=2*rho+eps_max*(12*rho**6+Q(176,9)*rho**7)
    assert p_delta<1
    p_inv=1/(1-p_delta)
    re_omega_min=Q(3736,10000)
    omega_abs=Omega.au()
    damping=2*re_omega_min-2*omega_abs*p_delta*p_inv-2*q_bound*p_inv
    forcing=residual_bound*p_inv
    nonlinear=p_inv
    tail_radius=Q(1,10**9)
    assert damping>0
    assert damping*tail_radius>=forcing+nonlinear*tail_radius**2
    assert 2*nonlinear*tail_radius<damping

    z0=G(3,T);zn=z0.re*z0.re+z0.im*z0.im;y0=G(z0.re/zn,-z0.im/zn)
    q0=L();q1=L()
    for n in range(2,N+1):
        yn=gpow(y0,n)
        q0=ladd(q0,lscale(c[n][0],yn));q1=ladd(q1,lscale(c[n][1],yn))
    Oc=G(Q(3737,10000),-Q(1779,20000));ec=Q(1,20000)
    dRe=Q(1,10000);dIm=Q(3,20000);de=Q(1,20000)
    center=geval(q0,Oc)+ec*geval(q1,Oc)
    dq=ladd(lder(q0),lscale(lder(q1),ec))
    linear=[dRe*geval(dq,Oc),G(0,dIm)*geval(dq,Oc),de*geval(q1,Oc)]
    q0pp=lder(lder(q0));q1pp=lder(lder(q1));q1p=lder(q1)
    sup_second=evalL(q0pp).au()+eps_max*evalL(q1pp).au()
    sup_mixed=evalL(q1p).au()
    dOmega=dRe+dIm
    nonlinear_radius=Q(1,2)*sup_second*dOmega**2+sup_mixed*dOmega*de+tail_radius

    BITS=96
    center_int=[qnearest(center.re,BITS),qnearest(center.im,BITS)]
    linear_int=[[qnearest(v.re,BITS),qnearest(v.im,BITS)] for v in linear]
    S=1<<BITS
    quant_error=abs(center.re-Q(center_int[0],S))+abs(center.im-Q(center_int[1],S))
    for v,pair in zip(linear,linear_int):
        quant_error+=abs(v.re-Q(pair[0],S))+abs(v.im-Q(pair[1],S))
    radius_int=qceil(nonlinear_radius+quant_error,BITS)
    payload={
     'method':'exact epsilon-linear Laurent Jost recurrence plus vertical-ray Volterra contraction',
     'quantity':'q=P*d_z(log Phi)-i*Omega',
     'contour':'z=3+i*t, t>=32',
     'omega_box':'Re[0.3736,0.3738]; Im[-0.0891,-0.0888]',
     'epsilon_interval':'[0,1/10000]',
     'truncation':N,
     'first_residual_power':min(R),
     'rho_bound':'1/32',
     'damping_lower':str(damping),
     'residual_bound':str(residual_bound),
     'tail_radius':str(tail_radius),
     'endpoint_z':'3+32*i',
     'variables':['xi_ReOmega','xi_ImOmega','xi_epsilon'],
     'affine':{'center':center_int,'linear':linear_int,'dyadic_bits':BITS,'radius':radius_int},
     'nonlinear_radius':str(nonlinear_radius),
    }
    h=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    payload['hash']=h
    return payload

INFINITY_JOST_ENDPOINT_220_PAYLOAD = _certify_axial_infinity_jost_endpoint_220()
assert INFINITY_JOST_ENDPOINT_220_PAYLOAD["hash"] == (
    "c93f9076c2d664f4e8f1499eac0b478932a3f34fcebb31ab009a4fabf39c2519"
)
INFINITY_JOST_ENDPOINT_220_RADIUS = _Fraction(
    INFINITY_JOST_ENDPOINT_220_PAYLOAD["affine"]["radius"],
    1 << INFINITY_JOST_ENDPOINT_220_PAYLOAD["affine"]["dyadic_bits"],
)
assert INFINITY_JOST_ENDPOINT_220_RADIUS < _Fraction(1, 100000000)

# Validated inward propagation of the outgoing Jost logarithmic correction.
# The projective variable q=P*d_z(log Phi)-i*Omega is propagated from
# z=3+32*i down the vertical contour to the real matching point z=3.
def _certify_axial_infinity_riccati_propagation_220():
    from fractions import Fraction as Q
    import math
    B=96; S=1<<B; NV=3; SB=128; SS=1<<SB

    def nint(fr):
     n,d=fr.numerator,fr.denominator
     return (2*n+d)//(2*d) if n>=0 else -((2*(-n)+d)//(2*d))
    def ceilq(fr): return (fr.numerator+fr.denominator-1)//fr.denominator
    def supq(fr):
     x=Q(fr)*SS; return Q((x.numerator+x.denominator-1)//x.denominator,SS)
    def infq(fr):
     x=Q(fr)*SS; return Q(x.numerator//x.denominator,SS)
    class C:
     __slots__=('cr','ci','rad')
     def __init__(self,re=0,im=0,rad=0,raw=False):
      if raw:self.cr=int(re);self.ci=int(im);self.rad=int(rad);return
      re=Q(re);im=Q(im); a=nint(re*S); b=nint(im*S)
      er=abs(re-Q(a,S))+abs(im-Q(b,S))+Q(rad)
      self.cr=a;self.ci=b;self.rad=ceilq(er*S)
     @classmethod
     def raw(cls,a,b,r=0): return cls(a,b,r,True)
     @classmethod
     def co(cls,x): return x if isinstance(x,C) else C(x)
     def __add__(self,o):o=C.co(o);return C.raw(self.cr+o.cr,self.ci+o.ci,self.rad+o.rad)
     __radd__=__add__
     def __neg__(self):return C.raw(-self.cr,-self.ci,self.rad)
     def __sub__(self,o):return self+(-C.co(o))
     def __rsub__(self,o):return C.co(o)-self
     def __mul__(self,o):
      o=C.co(o);rn=self.cr*o.cr-self.ci*o.ci;inn=self.cr*o.ci+self.ci*o.cr
      a=nint(Q(rn,S));b=nint(Q(inn,S));err=abs(rn-a*S)+abs(inn-b*S)
      c1=abs(self.cr)+abs(self.ci);c2=abs(o.cr)+abs(o.ci);cross=c1*o.rad+c2*self.rad+self.rad*o.rad
      return C.raw(a,b,(cross+err+S-1)//S)
     __rmul__=__mul__
     def inv(self):
      a=Q(self.cr,S);b=Q(self.ci,S);rr=Q(self.rad,S);L=max(abs(a),abs(b)); assert L>rr,(float(L),float(rr),self.comp())
      d=a*a+b*b; re=a/d; im=-b/d; ar=nint(re*S);ai=nint(im*S)
      rem=rr/(L*(L-rr))+abs(re-Q(ar,S))+abs(im-Q(ai,S))
      return C.raw(ar,ai,ceilq(rem*S))
     def __truediv__(self,o):return self*C.co(o).inv()
     def __rtruediv__(self,o):return C.co(o)/self
     def __pow__(self,n):
      if n<0:return (self.inv())**(-n)
      out=C(1);b=self
      while n:
       if n&1:out=out*b
       b=b*b;n//=2
      return out
     def au(self):return Q(abs(self.cr)+abs(self.ci)+self.rad,S)
     def lo(self):return Q(max(abs(self.cr),abs(self.ci))-self.rad,S)
     def reup(self):return Q(self.cr+self.rad,S)
     def comp(self):return complex(self.cr/S,self.ci/S)
    class U:
     __slots__=('v','d')
     def __init__(self,v=0,d=None):self.v=C.co(v);self.d=list(d or [C(0),C(0),C(0)])
     @classmethod
     def co(cls,x):return x if isinstance(x,U) else U(x)
     def __add__(self,o):o=U.co(o);return U(self.v+o.v,[self.d[j]+o.d[j] for j in range(3)])
     __radd__=__add__
     def __neg__(self):return U(-self.v,[-x for x in self.d])
     def __sub__(self,o):return self+(-U.co(o))
     def __rsub__(self,o):return U.co(o)-self
     def __mul__(self,o):o=U.co(o);return U(self.v*o.v,[self.d[j]*o.v+self.v*o.d[j] for j in range(3)])
     __rmul__=__mul__
     def inv(self):iv=self.v.inv();iv2=iv*iv;return U(iv,[-x*iv2 for x in self.d])
     def __truediv__(self,o):return self*U.co(o).inv()
     def __rtruediv__(self,o):return U.co(o)/self
     def __pow__(self,n):
      out=U(1);b=self
      while n:
       if n&1:out=out*b
       b=b*b;n//=2
      return out
    class J2:
     __slots__=('v','d','h')
     def __init__(self,v=0,d=None,h=None):
      self.v=C.co(v);self.d=list(d or [C(0) for _ in range(3)]);self.h=h or [[C(0) for _ in range(3)] for _ in range(3)]
     @classmethod
     def co(cls,x):return x if isinstance(x,J2) else J2(x)
     def __add__(self,o):
      o=J2.co(o);return J2(self.v+o.v,[self.d[i]+o.d[i] for i in range(3)],[[self.h[i][j]+o.h[i][j] for j in range(3)] for i in range(3)])
     __radd__=__add__
     def __neg__(self):return J2(-self.v,[-x for x in self.d],[[-x for x in row] for row in self.h])
     def __sub__(self,o):return self+(-J2.co(o))
     def __rsub__(self,o):return J2.co(o)-self
     def __mul__(self,o):
      o=J2.co(o)
      d=[self.d[i]*o.v+self.v*o.d[i] for i in range(3)]
      h=[[self.h[i][j]*o.v+self.d[i]*o.d[j]+self.d[j]*o.d[i]+self.v*o.h[i][j] for j in range(3)] for i in range(3)]
      return J2(self.v*o.v,d,h)
     __rmul__=__mul__
     def inv(self):
      iv=self.v.inv();iv2=iv*iv;iv3=iv2*iv
      d=[-self.d[i]*iv2 for i in range(3)]
      h=[[2*self.d[i]*self.d[j]*iv3-self.h[i][j]*iv2 for j in range(3)] for i in range(3)]
      return J2(iv,d,h)
     def __truediv__(self,o):return self*J2.co(o).inv()
     def __rtruediv__(self,o):return J2.co(o)/self
     def __pow__(self,n):
      out=J2(1);b=self
      while n:
       if n&1:out=out*b
       b=b*b;n//=2
      return out

    def sadd(a,b,N):return [(a[i] if i<len(a) else U(0))+(b[i] if i<len(b) else U(0)) for i in range(N)]
    def sscale(a,c,N):return [a[i]*c if i<len(a) else U(0) for i in range(N)]

    def coeff_series(s0,N,O,ep):
     zc=C(3,32-s0); iz=C(0,1)/zc;zm={}
     for k in [1,2,3,4,5,6,7,8,9,10]:
      invbase=1/(zc**k);pw=C(1);arr=[]
      for n in range(N):arr.append(U(invbase*pw*math.comb(k+n-1,n)));pw=pw*iz
      zm[k]=arr
     one=[U(1)]+[U(0)]*(N-1)
     P=sadd(sadd(one,sscale(zm[1],-2,N),N),sscale(sadd(sscale(zm[6],12,N),sscale(zm[7],-Q(176,9),N),N),ep,N),N)
     Qs=sadd(sadd(sscale(zm[2],6,N),sscale(zm[3],-18,N),N),sscale(zm[4],12,N),N)
     qe=sadd(sscale(zm[5],-32*(O*O),N),sscale(zm[6],64*(O*O),N),N)
     qe=sadd(qe,sscale(zm[8],2392,N),N);qe=sadd(qe,sscale(zm[9],-Q(30376,3),N),N);qe=sadd(qe,sscale(zm[10],Q(32128,3),N),N)
     return P,sadd(Qs,sscale(qe,ep,N),N)

    def eval_coeff(z,O,ep):
     P=1-2/z+ep*(12/z**6-Q(176,9)/z**7)
     QQ=6/z**2-18/z**3+12/z**4+ep*(-32*(O*O)/z**5+64*(O*O)/z**6+2392/z**8-Q(30376,3)/z**9+Q(32128,3)/z**10)
     return P,QQ

    def Fval(q,z,O,ep):
     P,QQ=eval_coeff(z,O,ep);I=type(q).co(C(0,1)) if hasattr(type(q),'co') else C(0,1)
     return (I*q*q-2*O*q-I*QQ)/P

    def find_B0(Y,R,Plo,Qb,Ob):
     B=supq(max(2*Y,Q(1,100)))
     for _ in range(64):
      rhs=supq(Y+R*(Qb+2*Ob*B+B*B)/Plo)
      lip=R*(2*Ob+2*B)/Plo
      if rhs<=B and lip<1:return B,lip
      B=supq(max(Q(5,4)*B,Q(21,20)*rhs))
     raise AssertionError(('B0',float(Y),float(R),float(Plo),float(Qb),float(Ob),float(B),float(lip)))

    def scalar_coeff_bounds(s0,R):
     T=abs(Q(32)-s0);zlo=max(Q(3),T)-R;zup=Q(3)+T+R;zm2=max(Q(1),T)-R
     assert zlo>0 and zm2>0
     inv={k:1/zlo**k for k in range(1,12)}
     epsm=Q(1,10000);Ob=Q(4629,10000)
     P1=12*inv[6]+Q(176,9)*inv[7]
     Plo=zm2/zup-epsm*P1;assert Plo>0
     Q0=6*inv[2]+18*inv[3]+12*inv[4]
     Q1=32*Ob*Ob*inv[5]+64*Ob*Ob*inv[6]+2392*inv[8]+Q(30376,3)*inv[9]+Q(32128,3)*inv[10]
     Qb=Q0+epsm*Q1
     Pzb=2*inv[2]+epsm*(72*inv[7]+Q(1232,9)*inv[8])
     if s0 < Q(139,8):
      return Plo,Qb,Ob,P1,Q1,Pzb,inv
     return infq(Plo),supq(Qb),supq(Ob),supq(P1),supq(Q1),supq(Pzb),{k:supq(v) for k,v in inv.items()}

    def analytic_bounds(q0,qs,s0,R):
     Plo,Qb,Ob,P1,Q1,Pzb,inv=scalar_coeff_bounds(s0,R)
     B0,lip=find_B0(q0.au(),R,Plo,Qb,Ob)
     Num=Qb+2*Ob*B0+B0*B0
     dOs=[Q(1,10000),Q(3,20000),Q(0)];dEs=[Q(0),Q(0),Q(1,20000)]
     QO=Q(1,10000)*0 # placeholder
     QOb=Q(1,10000) # overwritten below
     baseQO=Q(1,10000) # no-op
     qOcore=Q(1,10000) # no-op
     QOabs=(64*Ob*inv[5]+128*Ob*inv[6])*Q(1,10000) # unit Re scale
     B1=[]
     for j in range(3):
      qo=(64*Ob*inv[5]+128*Ob*inv[6])*dOs[j]*Q(1,10000) if False else (64*Ob*inv[5]+128*Ob*inv[6])*dOs[j]*Q(1,10000)
      # Q_O already includes epsilon <=1e-4.
      qj=Q(1,10000)*(64*Ob*inv[5]+128*Ob*inv[6])*dOs[j] + Q1*dEs[j]
      pj=P1*dEs[j]
      fp=(2*dOs[j]*B0+qj)/Plo+Num*pj/(Plo*Plo)
      B1.append(supq((qs[j].au()+R*fp)/(1-lip)))
     return B0,B1,Plo

    def step(q0,qs,s0,h,N,O,ep,R):
     P,Qser=coeff_series(s0,N+1,O,ep); a=[U(q0,qs)];I=U(C(0,1))
     for n in range(N):
      sq=U(0)
      for k in range(n+1):sq+=a[k]*a[n-k]
      rhs=I*sq-2*O*a[n]-I*Qser[n];corr=U(0)
      for k in range(1,n+1):corr+=P[k]*(n-k+1)*a[n-k+1]
      a.append((rhs-corr)/((n+1)*P[0]))
     out=U(0);hp=C(1)
     for x in a:out+=x*hp;hp=hp*h
     arithmetic=Q(out.v.rad+sum(x.rad for x in out.d),S);out.v.rad=0
     for x in out.d:x.rad=0
     B0,B1,_=analytic_bounds(q0,qs,s0,R);rho=h/R;tail=supq((B0+sum(B1))*rho**(N+1)/(1-rho));return out.v,out.d,supq(arithmetic+tail),tail,arithmetic,B0,B1

    def nonlinear_bounds(q0,qs,Rtot,s0,h,B0,B1):
     R=h/2;sm=s0+R;Plo,Qb,Ob,P1,Q1,Pzb,inv=scalar_coeff_bounds(sm,R)
     J=B1;Od=[Q(1,10000),Q(3,20000),Q(0)];Ed=[Q(0),Q(0),Q(1,20000)]
     Bq=B0+sum(J)+Rtot;epsm=Q(1,10000)
     Fqq=2/Plo;FqO=2/Plo;Fqe=2*(Bq+Ob)*P1/(Plo*Plo)
     QOO=epsm*(64*inv[5]+128*inv[6]);FOO=QOO/Plo
     QOcore=64*Ob*inv[5]+128*Ob*inv[6]
     FOe=(QOcore/Plo)+(2*Bq+epsm*QOcore)*P1/(Plo*Plo)
     Num=Qb+2*Ob*Bq+Bq*Bq
     Fee=2*Q1*P1/(Plo*Plo)+2*Num*P1*P1/(Plo**3)
     H=Q(0)
     for i in range(3):
      for j in range(3):
       H += Fqq*J[i]*J[j] + FqO*(J[i]*Od[j]+Od[i]*J[j]) + Fqe*(J[i]*Ed[j]+Ed[i]*J[j]) + FOO*Od[i]*Od[j] + FOe*(Od[i]*Ed[j]+Ed[i]*Od[j]) + Fee*Ed[i]*Ed[j]
     H=supq(H/2)
     # Damping/growth coefficient Re(F_q), using a centered disk.
     zc=C(3,32-sm);Oc=C(Q(3737,10000),-Q(1779,20000));ec=C(Q(1,20000));Pc,_=eval_coeff(zc,Oc,ec)
     Fbound=(Qb+2*Ob*B0+B0*B0)/Plo;center_delta=h*Fbound
     qrad=center_delta+sum(J)+Rtot;Ovar=Q(1,4000);Prad=Pzb*R+P1*Q(1,20000)
     num=2*C(0,1)*q0-2*Oc;num.rad+=ceilq((2*qrad+2*Ovar)*S)
     Pd=C.raw(Pc.cr,Pc.ci,Pc.rad+ceilq(Prad*S));A=num/Pd
     return H,A.reup(),1/Plo

    p=INFINITY_JOST_ENDPOINT_220_PAYLOAD['affine']
    q0=C.raw(*p['center'],0)
    qs=[C.raw(*x,0) for x in p['linear']]
    Rtot=supq(Q(p['radius'],S))
    O=U(C(Q(3737,10000),-Q(1779,20000)),[C(Q(1,10000)),C(0,Q(3,20000)),C(0)])
    ep=U(C(Q(1,20000)),[C(0),C(0),C(Q(1,20000))])
    s=Q(0);N=12;steps=0;mt=Q(0);ma=Q(0);maxH=Q(0);maxa=None
    while s<32:
        t=32-s
        if t>Q(117,8):R=Q(1,2)
        elif t>8:R=Q(1,4)
        elif t>4:R=Q(1,8)
        elif t>2:R=Q(1,16)
        elif t>1:R=Q(1,32)
        else:R=Q(1,64)
        h=R/4
        if s+h>32:h=32-s
        nq,nqs,local,tail,arith,B0,B1=step(q0,qs,s,h,N,O,ep,R)
        H,a,b=nonlinear_bounds(q0,qs,Rtot,s,h,B0,B1)
        maxH=max(maxH,H);maxa=a if maxa is None else max(maxa,a)
        Be=supq(max(2*Rtot,Q(1,10**8)))
        for _ in range(64):
            rhs=supq(Rtot+h*(max(a,0)*Be+b*Be*Be+H))
            if rhs<=Be:break
            Be=supq(max(Q(5,4)*Be,Q(21,20)*rhs))
        else:raise AssertionError('infinity Riccati error majorant failed')
        den=1-a*h
        assert den>0
        Rtot=supq((Rtot+h*(H+b*Be*Be))/den+local)
        q0,qs=nq,nqs;s+=h;steps+=1;mt=max(mt,tail);ma=max(ma,arith)
    rec={
        'method':'96-bit dyadic affine Riccati Taylor propagation down z=3+i*t',
        'contour':'z=3+i*(32-s), s in [0,32]',
        'steps':steps,
        'center':[q0.cr,q0.ci],
        'linear':[[x.cr,x.ci] for x in qs],
        'bits':B,
        'radius':ceilq(Rtot*S),
        'taylor_order':N,
        'max_tail':str(mt),
        'max_arith':str(ma),
        'max_H':str(maxH),
        'max_a':str(maxa),
    }
    rec['hash']=hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert rec['hash']=='e6161ac3be6af6b68c2b1130c36fc85ac8d1eebc582fff4690722cee41988c8a'
    return rec

INFINITY_RICCATI_PROPAGATION_220_PAYLOAD = (
    _certify_axial_infinity_riccati_propagation_220()
)
assert INFINITY_RICCATI_PROPAGATION_220_PAYLOAD['hash'] == (
    'e6161ac3be6af6b68c2b1130c36fc85ac8d1eebc582fff4690722cee41988c8a'
)
INFINITY_RICCATI_DYADIC_BITS_220 = INFINITY_RICCATI_PROPAGATION_220_PAYLOAD['bits']
INFINITY_RICCATI_DYADIC_SCALE_220 = 1 << INFINITY_RICCATI_DYADIC_BITS_220
INFINITY_RICCATI_RADIUS_220 = _Fraction(
    INFINITY_RICCATI_PROPAGATION_220_PAYLOAD['radius'],
    INFINITY_RICCATI_DYADIC_SCALE_220,
)
assert INFINITY_RICCATI_RADIUS_220 < _Fraction(1, 50000)

# Certified affine horizon-infinity mismatch and complex interval Newton tube.
def _certify_axial_matching_interval_newton_220():
    from fractions import Fraction as Q

    def z_add(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def z_neg(a):
        return (-a[0], -a[1])

    def z_sub(a, b):
        return z_add(a, z_neg(b))

    def z_mul(a, b):
        return (
            a[0]*b[0] - a[1]*b[1],
            a[0]*b[1] + a[1]*b[0],
        )

    def z_inv(a):
        den = a[0]*a[0] + a[1]*a[1]
        assert den > 0
        return (a[0]/den, -a[1]/den)

    def z_div(a, b):
        return z_mul(a, z_inv(b))

    def z_scale(a, scalar):
        return (a[0]*scalar, a[1]*scalar)

    def z_l1(a):
        return abs(a[0]) + abs(a[1])

    def z_lower(a):
        # max(|Re|,|Im|) is a rigorous lower bound for |a|_2.
        return max(abs(a[0]), abs(a[1]))

    class AffineComplex:
        __slots__ = ("center", "linear", "radius")

        def __init__(self, center=(Q(0), Q(0)), linear=None, radius=Q(0)):
            self.center = center
            self.linear = list(linear or [
                (Q(0), Q(0)),
                (Q(0), Q(0)),
                (Q(0), Q(0)),
            ])
            assert len(self.linear) == 3
            self.radius = Q(radius)
            assert self.radius >= 0

        def linear_norm(self):
            return sum((z_l1(value) for value in self.linear), Q(0))

        def __add__(self, other):
            if not isinstance(other, AffineComplex):
                other = AffineComplex(other)
            return AffineComplex(
                z_add(self.center, other.center),
                [
                    z_add(self.linear[index], other.linear[index])
                    for index in range(3)
                ],
                self.radius + other.radius,
            )

        __radd__ = __add__

        def __neg__(self):
            return AffineComplex(
                z_neg(self.center),
                [z_neg(value) for value in self.linear],
                self.radius,
            )

        def __sub__(self, other):
            return self + (-other)

        def __rsub__(self, other):
            return AffineComplex(other) - self

        def __mul__(self, other):
            if not isinstance(other, AffineComplex):
                other = AffineComplex(other)
            lhs_linear = self.linear_norm()
            rhs_linear = other.linear_norm()
            linear = [
                z_add(
                    z_mul(self.center, other.linear[index]),
                    z_mul(other.center, self.linear[index]),
                )
                for index in range(3)
            ]
            radius = (
                z_l1(self.center)*other.radius
                + z_l1(other.center)*self.radius
                + lhs_linear*rhs_linear
                + lhs_linear*other.radius
                + self.radius*rhs_linear
                + self.radius*other.radius
            )
            return AffineComplex(
                z_mul(self.center, other.center),
                linear,
                radius,
            )

        __rmul__ = __mul__

        def inverse(self):
            linear_norm = self.linear_norm()
            deviation = linear_norm + self.radius
            center_lower = z_lower(self.center)
            assert center_lower > deviation
            inverse_center = z_inv(self.center)
            inverse_square = z_mul(inverse_center, inverse_center)
            linear = [
                z_neg(z_mul(value, inverse_square))
                for value in self.linear
            ]
            radius = (
                self.radius/(center_lower*center_lower)
                + deviation*deviation/(
                    center_lower*center_lower
                    * (center_lower - deviation)
                )
            )
            return AffineComplex(inverse_center, linear, radius)

        def __truediv__(self, other):
            if not isinstance(other, AffineComplex):
                other = AffineComplex(other)
            return self*other.inverse()

        def scale_complex(self, value):
            return AffineComplex(
                z_mul(self.center, value),
                [z_mul(coefficient, value) for coefficient in self.linear],
                self.radius*z_l1(value),
            )

    def dyadic_affine(payload, center_key, linear_key, radius_key, bits_key):
        bits = payload[bits_key]
        scale = 1 << bits
        center = tuple(Q(value, scale) for value in payload[center_key])
        linear = [
            tuple(Q(value, scale) for value in pair)
            for pair in payload[linear_key]
        ]
        radius = Q(payload[radius_key], scale)
        return AffineComplex(center, linear, radius)

    horizon_payload = HORIZON_RICCATI_PROPAGATION_220_PAYLOAD
    horizon_log = horizon_payload["log_derivative"]
    horizon = dyadic_affine(
        horizon_log,
        "center",
        "linear",
        "radius",
        "dyadic_bits",
    )
    infinity_payload = INFINITY_RICCATI_PROPAGATION_220_PAYLOAD
    infinity = dyadic_affine(
        infinity_payload,
        "center",
        "linear",
        "radius",
        "bits",
    )

    zero = (Q(0), Q(0))
    omega = AffineComplex(
        (Q(3737, 10000), -Q(1779, 20000)),
        [
            (Q(1, 10000), Q(0)),
            (Q(0), Q(3, 20000)),
            zero,
        ],
    )
    epsilon = AffineComplex(
        (Q(1, 20000), Q(0)),
        [zero, zero, (Q(1, 20000), Q(0))],
    )
    one = AffineComplex((Q(1), Q(0)))
    horizon_x = one + epsilon.scale_complex((Q(5, 72), Q(0)))
    alpha = (
        omega.scale_complex((Q(0), -Q(2)))
        + (epsilon*omega).scale_complex((Q(0), Q(1, 36)))
    )
    # At z=3, P=NF=1/3+(148/19683)*epsilon.
    matching_p = (
        AffineComplex((Q(1, 3), Q(0)))
        + epsilon.scale_complex((Q(148, 19683), Q(0)))
    )
    horizon_q = (
        matching_p*(alpha/horizon_x + horizon)
        - omega.scale_complex((Q(0), Q(1)))
    )
    mismatch = horizon_q - infinity

    # Re-express the two real frequency directions as one holomorphic
    # complex direction. Any dyadic Cauchy-Riemann defect is transferred
    # into the uniform analytic error bound.
    complex_slope = z_scale(mismatch.linear[0], Q(10000))
    expected_im_direction = z_mul(
        complex_slope,
        (Q(0), Q(3, 20000)),
    )
    cr_defect = z_sub(mismatch.linear[1], expected_im_direction)
    analytic_error = mismatch.radius + z_l1(cr_defect)

    root_center = z_sub(
        omega.center,
        z_div(mismatch.center, complex_slope),
    )
    root_epsilon_linear = z_neg(
        z_div(mismatch.linear[2], complex_slope)
    )

    newton_disk_radius = Q(1, 150000)
    cauchy_disk_radius = Q(1, 25000)
    assert cauchy_disk_radius > newton_disk_radius

    # The larger Cauchy disk remains inside the original omega rectangle
    # for every epsilon in [0,1/10000].
    assert (
        abs(root_center[0] - omega.center[0])
        + abs(root_epsilon_linear[0])
        + cauchy_disk_radius
        < Q(1, 10000)
    )
    assert (
        abs(root_center[1] - omega.center[1])
        + abs(root_epsilon_linear[1])
        + cauchy_disk_radius
        < Q(3, 20000)
    )

    # Cauchy's estimate encloses the nonlinear derivative on the smaller
    # disk. The complex interval-Newton image is strictly internal.
    derivative_error = analytic_error/(
        cauchy_disk_radius - newton_disk_radius
    )
    slope_lower = z_lower(complex_slope)
    derivative_lower = slope_lower - derivative_error
    assert derivative_lower > 0
    interval_newton_radius = analytic_error/derivative_lower
    assert interval_newton_radius < newton_disk_radius

    epsilon_zero_center = z_sub(root_center, root_epsilon_linear)
    epsilon_max_center = z_add(root_center, root_epsilon_linear)

    record = {
        "method": (
            "affine complex interval Newton with Cauchy derivative "
            "enclosure"
        ),
        "quantity": (
            "P*d_z(log Phi_horizon)-i*Omega "
            "minus outgoing q"
        ),
        "matching_z": "3",
        "variables": [
            "xi_ReOmega",
            "xi_ImOmega",
            "xi_epsilon",
        ],
        "epsilon_interval": "[0,1/10000]",
        "mismatch_center": [
            str(mismatch.center[0]),
            str(mismatch.center[1]),
        ],
        "complex_slope": [
            str(complex_slope[0]),
            str(complex_slope[1]),
        ],
        "analytic_error": str(analytic_error),
        "cr_defect": str(z_l1(cr_defect)),
        "root_center_at_epsilon_midpoint": [
            str(root_center[0]),
            str(root_center[1]),
        ],
        "root_linear_in_xi_epsilon": [
            str(root_epsilon_linear[0]),
            str(root_epsilon_linear[1]),
        ],
        "root_center_at_epsilon_zero": [
            str(epsilon_zero_center[0]),
            str(epsilon_zero_center[1]),
        ],
        "root_center_at_epsilon_max": [
            str(epsilon_max_center[0]),
            str(epsilon_max_center[1]),
        ],
        "cauchy_disk_radius": str(cauchy_disk_radius),
        "newton_disk_radius": str(newton_disk_radius),
        "derivative_error": str(derivative_error),
        "derivative_lower": str(derivative_lower),
        "interval_newton_image_radius": str(interval_newton_radius),
        "unique_simple_root_for_each_epsilon": True,
    }
    record["hash"] = hashlib.sha256(
        json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return record


AXIAL_MATCHING_INTERVAL_NEWTON_220_PAYLOAD = (
    _certify_axial_matching_interval_newton_220()
)
assert AXIAL_MATCHING_INTERVAL_NEWTON_220_PAYLOAD[
    "unique_simple_root_for_each_epsilon"
] is True

# Exact epsilon=0 tangent system for the common axial projective variable
# q=P*d_z(log Phi)-i*Omega.  This is the structural prerequisite for a
# rigorous implicit-function derivative at the endpoint epsilon=0; the
# previously certified affine root-center line is not used as a substitute.
z_tan, eta_tan = s.symbols("z_tan eta_tan")
Omega0_tan, Omega_dot_tan, epsilon_dot_tan = s.symbols(
    "Omega0_tan Omega_dot_tan epsilon_dot_tan"
)
q0_tan = s.Function("q0_tan")(z_tan)
u_tan = s.Function("u_tan")(z_tan)

f_tan = 1 - 2/z_tan
F1_tan = 24/z_tan**6 - s.Rational(392, 9)/z_tan**7
P1_tan = 4*(27*z_tan - 44)/(9*z_tan**7)
V0_tan = 6/z_tan**2 - 6/z_tan**3
V1_tan = -8*(
    653 - 281*z_tan + 4*Omega0_tan**2*z_tan**4
)/z_tan**9
Q0_tan = s.factor(f_tan*V0_tan)
Qepsilon_tan = s.factor(F1_tan*V0_tan + f_tan*V1_tan)

Omega_eta_tan = Omega0_tan + eta_tan*Omega_dot_tan
epsilon_eta_tan = eta_tan*epsilon_dot_tan
q_eta_tan = q0_tan + eta_tan*u_tan
P_eta_tan = f_tan + epsilon_eta_tan*P1_tan
F_eta_tan = f_tan + epsilon_eta_tan*F1_tan
V1_eta_tan = -8*(
    653 - 281*z_tan + 4*Omega_eta_tan**2*z_tan**4
)/z_tan**9
V_eta_tan = V0_tan + epsilon_eta_tan*V1_eta_tan
Q_eta_tan = F_eta_tan*V_eta_tan

RICCATI_RESIDUAL_ETA_220 = s.expand(
    P_eta_tan*s.diff(q_eta_tan, z_tan)
    + q_eta_tan**2
    + 2*s.I*Omega_eta_tan*q_eta_tan
    - Q_eta_tan
)
RICCATI_TANGENT_FROM_DIFFERENTIATION_220 = s.factor(
    s.diff(RICCATI_RESIDUAL_ETA_220, eta_tan).subs(eta_tan, 0)
)
RICCATI_TANGENT_EXPECTED_220 = s.factor(
    f_tan*s.diff(u_tan, z_tan)
    + 2*(q0_tan + s.I*Omega0_tan)*u_tan
    + epsilon_dot_tan*P1_tan*s.diff(q0_tan, z_tan)
    + 2*s.I*Omega_dot_tan*q0_tan
    - epsilon_dot_tan*Qepsilon_tan
)
assert s.simplify(
    RICCATI_TANGENT_FROM_DIFFERENTIATION_220
    - RICCATI_TANGENT_EXPECTED_220
) == 0

# Frequency tangent at fixed epsilon=0.
RICCATI_OMEGA_TANGENT_220 = s.factor(
    RICCATI_TANGENT_EXPECTED_220.subs({
        Omega_dot_tan: 1,
        epsilon_dot_tan: 0,
    })
)
RICCATI_OMEGA_TANGENT_EXPECTED_220 = s.factor(
    f_tan*s.diff(u_tan, z_tan)
    + 2*(q0_tan + s.I*Omega0_tan)*u_tan
    + 2*s.I*q0_tan
)
assert s.simplify(
    RICCATI_OMEGA_TANGENT_220
    - RICCATI_OMEGA_TANGENT_EXPECTED_220
) == 0

# Coupling tangent at fixed Omega and epsilon=0.
RICCATI_EPSILON_TANGENT_220 = s.factor(
    RICCATI_TANGENT_EXPECTED_220.subs({
        Omega_dot_tan: 0,
        epsilon_dot_tan: 1,
    })
)
RICCATI_EPSILON_TANGENT_EXPECTED_220 = s.factor(
    f_tan*s.diff(u_tan, z_tan)
    + 2*(q0_tan + s.I*Omega0_tan)*u_tan
    + P1_tan*s.diff(q0_tan, z_tan)
    - Qepsilon_tan
)
assert s.simplify(
    RICCATI_EPSILON_TANGENT_220
    - RICCATI_EPSILON_TANGENT_EXPECTED_220
) == 0

# Algebraic implicit-function reduction.  A numerical enclosure may be
# asserted only after both endpoint tangents are enclosed and propagated.
Domega_tan, Depsilon_tan, Omega_prime_tan = s.symbols(
    "Domega_tan Depsilon_tan Omega_prime_tan"
)
IMPLICIT_TANGENT_RESIDUAL_220 = (
    Domega_tan*Omega_prime_tan + Depsilon_tan
)
IMPLICIT_TANGENT_SOLUTION_220 = -Depsilon_tan/Domega_tan
assert s.simplify(
    IMPLICIT_TANGENT_RESIDUAL_220.subs(
        Omega_prime_tan,
        IMPLICIT_TANGENT_SOLUTION_220,
    )
) == 0

AXIAL_EPSILON0_TANGENT_SYSTEM_220_PAYLOAD = {
    "quantity": "q=P*d_z(log Phi)-i*Omega",
    "base_equation": (
        "P*q_z+q^2+2*i*Omega*q-F*V=0"
    ),
    "omega_tangent": s.sstr(RICCATI_OMEGA_TANGENT_220),
    "epsilon_tangent": s.sstr(RICCATI_EPSILON_TANGENT_220),
    "P_epsilon_at_zero": s.sstr(P1_tan),
    "FV_epsilon_at_zero": s.sstr(Qepsilon_tan),
    "implicit_derivative": "dOmega/depsilon=-D_epsilon/D_Omega",
    "endpoint": "epsilon=0",
    "status": "exact tangent equations certified; interval propagation pending",
}
AXIAL_EPSILON0_TANGENT_SYSTEM_220_HASH = hashlib.sha256(
    json.dumps(
        AXIAL_EPSILON0_TANGENT_SYSTEM_220_PAYLOAD,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
).hexdigest()

# Rigorous epsilon=0 endpoint tangent disks for the common axial projective variable.
# A symmetric complex epsilon disk is used, so the endpoint derivative is not
# inferred from the one-sided physical parameter interval.
def _certify_axial_epsilon0_endpoint_tangents_220():
    from fractions import Fraction as Q
    import math
    import json
    import hashlib
    # Exact center of the certified epsilon=0 Newton tube and its root disk.
    ORE = Q('0.3736716812299648')
    OIM = Q('-0.0889623125972544')
    ROOT_R = Q(1,150000)
    CAUCHY_O_R = Q(1,20000)
    CAUCHY_E_R = Q(1,10000)
    LAUNCH = Q(1,16)
    MAJ_R = Q(1,8)
    N = 32
    TAIL_S = Q(1,2**32)
    TAIL_SP = Q(17,2**27)

    class D:
        __slots__=('re','im','rad')
        def __init__(self,re=0,im=0,rad=0): self.re=Q(re); self.im=Q(im); self.rad=Q(rad)
        @staticmethod
        def co(x): return x if isinstance(x,D) else D(x)
        def __add__(self,o): o=D.co(o); return D(self.re+o.re,self.im+o.im,self.rad+o.rad)
        __radd__=__add__
        def __neg__(self): return D(-self.re,-self.im,self.rad)
        def __sub__(self,o): return self+(-D.co(o))
        def __rsub__(self,o): return D.co(o)-self
        def cu(self): return abs(self.re)+abs(self.im)
        def cl(self): return max(abs(self.re),abs(self.im))
        def au(self): return self.cu()+self.rad
        def lo(self): return self.cl()-self.rad
        def __mul__(self,o):
            o=D.co(o)
            return D(self.re*o.re-self.im*o.im,
                     self.re*o.im+self.im*o.re,
                     self.cu()*o.rad+o.cu()*self.rad+self.rad*o.rad)
        __rmul__=__mul__
        def inv(self):
            lo=self.cl(); assert lo>self.rad, (float(lo),float(self.rad))
            n=self.re*self.re+self.im*self.im
            return D(self.re/n,-self.im/n,self.rad/(lo*(lo-self.rad)))
        def __truediv__(self,o): return self*D.co(o).inv()
        def __rtruediv__(self,o): return D.co(o)/self
        def __pow__(self,n):
            assert isinstance(n,int)
            if n<0:return self.inv()**(-n)
            out=D(1); b=self
            while n:
                if n&1: out=out*b
                b=b*b;n//=2
            return out
        def pair(self): return [str(self.re),str(self.im),str(self.rad)]

    I=D(0,1)

    class U:
        __slots__=('v','do','de')
        def __init__(self,v=0,do=0,de=0): self.v=D.co(v);self.do=D.co(do);self.de=D.co(de)
        @staticmethod
        def co(x): return x if isinstance(x,U) else U(x)
        def __add__(self,o):o=U.co(o);return U(self.v+o.v,self.do+o.do,self.de+o.de)
        __radd__=__add__
        def __neg__(self):return U(-self.v,-self.do,-self.de)
        def __sub__(self,o):return self+(-U.co(o))
        def __rsub__(self,o):return U.co(o)-self
        def __mul__(self,o):
            o=U.co(o);return U(self.v*o.v,self.do*o.v+self.v*o.do,self.de*o.v+self.v*o.de)
        __rmul__=__mul__
        def inv(self):
            iv=self.v.inv();iv2=iv*iv;return U(iv,-self.do*iv2,-self.de*iv2)
        def __truediv__(self,o):return self*U.co(o).inv()
        def __rtruediv__(self,o):return U.co(o)/self
        def __pow__(self,n):
            assert isinstance(n,int) and n>=0
            out=U(1);b=self
            while n:
                if n&1:out=out*b
                b=b*b;n//=2
            return out

    # Direct shifted-horizon power-series coefficients through first order in epsilon.
    def sadd(a,b,N):
        return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(N)]
    def sneg(a):return [-x for x in a]
    def ssub(a,b,N):return sadd(a,sneg(b),N)
    def smul(a,b,N):
        out=[0 for _ in range(N)]
        for i in range(min(N,len(a))):
            for j in range(min(N-i,len(b))):out[i+j]=out[i+j]+a[i]*b[j]
        return out
    def sscale(a,c,N):return [a[i]*c if i<len(a) else 0 for i in range(N)]
    def sder(a,N):return [(i+1)*a[i+1] if i+1<len(a) else 0 for i in range(N)]
    def zneg(k,N,coerce):
        return [coerce(Q((-1)**n*math.comb(k+n-1,n),2**(k+n))) for n in range(N)]
    def zpos(k,N,coerce):
        return [coerce(Q(math.comb(k,n)*2**(k-n))) if n<=k else coerce(0) for n in range(N)]

    def horizon_series(N,Omega,eps,coerce):
        one=[coerce(1)]+[coerce(0)]*(N-1)
        zm={k:zneg(k,N,coerce) for k in [1,2,3,4,6,7,8,9]}
        zp4=zpos(4,N,coerce)
        f=ssub(one,sscale(zm[1],2,N),N)
        fp=sscale(zm[2],2,N)
        fpp=sscale(zm[3],-4,N)
        p1=sadd(sscale(zm[6],12,N),sscale(zm[7],-Q(176,9),N),N)
        p1s=ssub(p1,sscale(fp,Q(5,72),N),N)
        p1p=sadd(sscale(zm[7],-72,N),sscale(zm[8],Q(1232,9),N),N)
        p1sp=ssub(p1p,sscale(fpp,Q(5,72),N),N)
        f1=sadd(sscale(zm[6],24,N),sscale(zm[7],-Q(392,9),N),N)
        f1s=ssub(f1,sscale(fp,Q(5,72),N),N)
        v0=ssub(sscale(zm[2],6,N),sscale(zm[3],6,N),N)
        v0p=sadd(sscale(zm[3],-12,N),sscale(zm[4],18,N),N)
        num=sadd(ssub(sscale(one,653,N),sscale(zpos(1,N,coerce),281,N),N),sscale(zp4,4*(Omega*Omega),N),N)
        v1=sscale(smul(num,zm[9],N),-8,N)
        v1s=ssub(v1,sscale(v0p,Q(5,72),N),N)
        A0=smul(f,f,N);A1=sscale(smul(f,p1s,N),2,N)
        B0=smul(f,fp,N);B1=sadd(smul(p1s,fp,N),smul(f,p1sp,N),N)
        C0=ssub([Omega*Omega]+[coerce(0)]*(N-1),smul(f,v0,N),N)
        C1=sneg(sadd(smul(f1s,v0,N),smul(f,v1s,N),N))
        A=sadd(A0,sscale(A1,eps,N),N)
        B=sadd(B0,sscale(B1,eps,N),N)
        C=sadd(C0,sscale(C1,eps,N),N)
        return A,B,C

    def recurrence(A,B,C,alpha,count,coerce):
        aa=[coerce(1)]
        for n in range(1,count+1):
            den=A[2]*(alpha+n)*(alpha+n-1)+B[1]*(alpha+n)+C[0]
            low=coerce(0)
            for m in range(3,n+3):
                k=n-m+2
                if k>=0:low+=A[m]*(alpha+k)*(alpha+k-1)*aa[k]
            for m in range(2,n+2):
                k=n-m+1
                if k>=0:low+=B[m]*(alpha+k)*aa[k]
            for m in range(1,n+1):
                k=n-m
                low+=C[m]*aa[k]
            aa.append(-low/den)
        return aa

    # Re-certify finite coefficients on symmetric epsilon disk.
    Olarge=D(ORE,OIM,CAUCHY_O_R); elarge=D(0,0,CAUCHY_E_R)
    Ad,Bd,Cd=horizon_series(42,Olarge,elarge,D.co)
    alpha_d=-2*I*Olarge+Q(1,36)*I*elarge*Olarge
    ad=recurrence(Ad,Bd,Cd,alpha_d,39,D.co)
    maxscaled=Q(1)
    for n,a in enumerate(ad[1:],1):
        scaled=a.au()*MAJ_R**n;maxscaled=max(maxscaled,scaled);assert scaled<=1,(n,float(scaled))

    # Root-disk dual recurrence and fixed-physical-z launch evaluation.
    Ou=U(D(ORE,OIM,ROOT_R),D(1),D(0));eu=U(D(0),D(0),D(1))
    Au,Bu,Cu=horizon_series(N+3,Ou,eu,U.co)
    alpha=-2*U(I)*Ou+Q(1,36)*U(I)*eu*Ou
    au=recurrence(Au,Bu,Cu,alpha,N,U.co)
    xeval=U(D(LAUNCH),D(0),D(Q(5,72)))
    Sv=U();Sp=U()
    for n,a in enumerate(au):
        Sv += a*(xeval**n)
        if n:Sp += n*a*(xeval**(n-1))
    marginO=CAUCHY_O_R-ROOT_R;assert marginO>0
    Sv.v.rad+=TAIL_S;Sv.do.rad+=TAIL_S/marginO;Sv.de.rad+=TAIL_S/CAUCHY_E_R
    Sp.v.rad+=TAIL_SP;Sp.do.rad+=TAIL_SP/marginO;Sp.de.rad+=TAIL_SP/CAUCHY_E_R
    assert Sv.v.lo()>0
    zfix=Q(33,16);fz=1-Q(2,1)/zfix;P1z=Q(4)*(Q(27)*zfix-Q(44))/(Q(9)*zfix**7)
    Pfix=U(D(fz),D(0),D(P1z))
    qhor=Pfix*(alpha/xeval+Sp/Sv)-U(I)*Ou
    S=Sv

    # Exact epsilon-linear outgoing Laurent recurrence.
    class G:
        __slots__=('re','im')
        def __init__(self,re=0,im=0):self.re=Q(re);self.im=Q(im)
        @staticmethod
        def co(x):return x if isinstance(x,G) else G(x)
        def __add__(self,o):o=G.co(o);return G(self.re+o.re,self.im+o.im)
        __radd__=__add__
        def __neg__(self):return G(-self.re,-self.im)
        def __sub__(self,o):return self+(-G.co(o))
        def __rsub__(self,o):return G.co(o)-self
        def __mul__(self,o):o=G.co(o);return G(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
        __rmul__=__mul__
        def zero(self):return self.re==0 and self.im==0

    def L(a=0):
        if isinstance(a,dict):return {int(k):G.co(v) for k,v in a.items() if not G.co(v).zero()}
        g=G.co(a);return {} if g.zero() else {0:g}
    def ladd(a,b):
        d=dict(a)
        for k,v in b.items():d[k]=d.get(k,G())+v
        return {k:v for k,v in d.items() if not v.zero()}
    def lneg(a):return {k:-v for k,v in a.items()}
    def lsub(a,b):return ladd(a,lneg(b))
    def lmul(a,b):
        d={}
        for i,u in a.items():
            for j,v in b.items():d[i+j]=d.get(i+j,G())+u*v
        return {k:v for k,v in d.items() if not v.zero()}
    def lscale(a,c):
        c=G.co(c);return {k:v*c for k,v in a.items() if not (v*c).zero()}
    def lshift(a,n):return {k+n:v for k,v in a.items()}
    def lder(a):return {k-1:G(v.re*k,v.im*k) for k,v in a.items() if k}
    def LP(a=0,b=0):return (L(a),L(b))
    def padd(a,b):return (ladd(a[0],b[0]),ladd(a[1],b[1]))
    def pneg(a):return (lneg(a[0]),lneg(a[1]))
    def psub(a,b):return padd(a,pneg(b))
    def pscale(a,c):return (lscale(a[0],c),lscale(a[1],c))
    def pmul(a,b):return (lmul(a[0],b[0]),ladd(lmul(a[0],b[1]),lmul(a[1],b[0])))
    def pdiv(a):
        fac=G(0,-Q(1,2));return (lscale(lshift(a[0],-1),fac),lscale(lshift(a[1],-1),fac))
    def Qcoef(n):
        if n==2:return LP(6)
        if n==3:return LP(-18)
        if n==4:return LP(12)
        if n==5:return LP(0,{2:G(-32)})
        if n==6:return LP(0,{2:G(64)})
        if n==8:return LP(0,2392)
        if n==9:return LP(0,-Q(30376,3))
        if n==10:return LP(0,Q(32128,3))
        return LP()
    def coeffs(N):
        c=[LP() for _ in range(N+1)]
        for n in range(2,N+1):
            rhs=Qcoef(n)
            if n-1>=2:rhs=padd(rhs,pscale(c[n-1],n-1))
            if n-2>=2:rhs=psub(rhs,pscale(c[n-2],2*(n-2)))
            if n-7>=2:rhs=padd(rhs,(L(),lscale(c[n-7][0],12*(n-7))))
            if n-8>=2:rhs=padd(rhs,(L(),lscale(c[n-8][0],-Q(176,9)*(n-8))))
            sq=LP()
            for j in range(2,n-1):sq=padd(sq,pmul(c[j],c[n-j]))
            c[n]=pdiv(psub(rhs,sq))
        return c
    def residual(c,N):
        out={}
        for n in range(2,max(2*N,N+8)+1):
            v=LP()
            if n<=N:v=padd(v,(lscale(lshift(c[n][0],1),G(0,2)),lscale(lshift(c[n][1],1),G(0,2))))
            if 2<=n-1<=N:v=psub(v,pscale(c[n-1],n-1))
            if 2<=n-2<=N:v=padd(v,pscale(c[n-2],2*(n-2)))
            if 2<=n-7<=N:v=psub(v,(L(),lscale(c[n-7][0],12*(n-7))))
            if 2<=n-8<=N:v=psub(v,(L(),lscale(c[n-8][0],-Q(176,9)*(n-8))))
            for j in range(2,N+1):
                k=n-j
                if 2<=k<=N:v=padd(v,pmul(c[j],c[k]))
            v=psub(v,Qcoef(n))
            if v[0] or v[1]:out[n]=v
        return out

    def evalL(a,Od):
        out=D()
        for k,g in a.items():out+=D(g.re,g.im)*(Od**k)
        return out

    def geval(a,o):
        out=G()
        def gp(n):
            if n<0:
                d=o.re*o.re+o.im*o.im;return gp2(G(o.re/d,-o.im/d),-n)
            return gp2(o,n)
        def gp2(x,n):
            z=G(1);b=x
            while n:
                if n&1:z=z*b
                b=b*b;n//=2
            return z
        for k,v in a.items():out+=v*gp(k)
        return out

    NJ=14;T=32;c=coeffs(NJ);R=residual(c,NJ);assert min(R)==15
    rho=Q(1,T)
    # Volterra contraction on symmetric local parameter disks.
    Olarge2=D(ORE,OIM,CAUCHY_O_R);elarge2=D(0,0,CAUCHY_E_R)
    def evalP(pair):return evalL(pair[0],Olarge2)+elarge2*evalL(pair[1],Olarge2)
    qbound=sum((evalP(c[n]).au()*rho**n for n in range(2,NJ+1)),Q())
    rbound=sum((evalP(v).au()*rho**n for n,v in R.items()),Q())
    epsmax=CAUCHY_E_R
    pdel=2*rho+epsmax*(12*rho**6+Q(176,9)*rho**7);pinv=1/(1-pdel)
    remin=ORE-CAUCHY_O_R
    omegaabs=Olarge2.au()
    damp=2*remin-2*omegaabs*pdel*pinv-2*qbound*pinv
    force=rbound*pinv;nonlin=pinv;jtail=Q(1,10**9)
    assert damp>0 and damp*jtail>=force+nonlin*jtail*jtail and 2*nonlin*jtail<damp
    # Endpoint finite Laurent pieces over the actual root disk.
    z0=G(3,32);zn=z0.re*z0.re+z0.im*z0.im;y0=G(z0.re/zn,-z0.im/zn)
    q0=L();q1=L()
    def gpow(a,n):
        if n<0:
            d=a.re*a.re+a.im*a.im;return gpow(G(a.re/d,-a.im/d),-n)
        out=G(1);b=a
        while n:
            if n&1:out=out*b
            b=b*b;n//=2
        return out
    for n in range(2,NJ+1):
        yn=gpow(y0,n);q0=ladd(q0,lscale(c[n][0],yn));q1=ladd(q1,lscale(c[n][1],yn))
    Oroot=D(ORE,OIM,ROOT_R)
    qinf=evalL(q0,Oroot)
    uoinf=evalL(lder(q0),Oroot)
    ueinf=evalL(q1,Oroot)
    qinf.rad+=jtail
    uoinf.rad+=jtail/marginO
    ueinf.rad+=jtail/CAUCHY_E_R

    # Outward 96-bit records.
    BITS=96;SCALE=1<<BITS
    def nearest(q):
        n=q.numerator*SCALE;d=q.denominator
        return (2*n+d)//(2*d) if n>=0 else -((2*(-n)+d)//(2*d))
    def ceilq(q):return (q.numerator*SCALE+q.denominator-1)//q.denominator
    def rec(d):
        a=nearest(d.re);b=nearest(d.im)
        err=abs(d.re-Q(a,SCALE))+abs(d.im-Q(b,SCALE))
        return {'center':[a,b],'radius':ceilq(d.rad+err),'bits':BITS}

    payload={
     'method':'epsilon=0 endpoint tangent disks from exact horizon Frobenius and infinity Laurent-Volterra recurrences',
     'omega_center':[str(ORE),str(OIM)],
     'omega_root_disk_radius':str(ROOT_R),
     'cauchy_omega_radius':str(CAUCHY_O_R),
     'cauchy_epsilon_radius':str(CAUCHY_E_R),
     'horizon':{'z':'33/16','q':rec(qhor.v),'dOmega':rec(qhor.do),'dEpsilon':rec(qhor.de),'s_nonzero_lower_dyadic_96':int(S.v.lo()*SCALE)},
     'infinity':{'z':'3+32*i','q':rec(qinf),'dOmega':rec(uoinf),'dEpsilon':rec(ueinf),'tail_radius':str(jtail),'damping_lower_dyadic_96':int(damp*SCALE)},
     'majorant':{'symmetric_epsilon_disk':True,'max_scaled_finite_coefficient':str(maxscaled),'series_tail':str(TAIL_S),'derivative_tail':str(TAIL_SP)},
    }
    payload['hash']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return payload

AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_PAYLOAD = (
    _certify_axial_epsilon0_endpoint_tangents_220()
)
AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_HASH = (
    AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_PAYLOAD["hash"]
)
assert AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_HASH == (
    "94ec87296b933bf4de3aada5d8bede67a80619f0767410e82767d64d5239d8c1"
)

# Exact-center q endpoint refinement used by the epsilon=0 tangent propagation.
def _certify_axial_epsilon0_center_q_refinement_220():
    import base64
    import hashlib
    import json
    namespace={}
    exec(base64.b64decode("ZnJvbSBmcmFjdGlvbnMgaW1wb3J0IEZyYWN0aW9uIGFzIFEKaW1wb3J0IG1hdGgsIGpzb24sIGhhc2hsaWIKaW1wb3J0IHN5bXB5IGFzIHMKCiMgRXhhY3QgY2VudGVyIG9mIHRoZSBjZXJ0aWZpZWQgZXBzaWxvbj0wIE5ld3RvbiB0dWJlIGFuZCBpdHMgcm9vdCBkaXNrLgpPUkUgPSBRKCcwLjM3MzY3MTY4MTIyOTk2NDgnKQpPSU0gPSBRKCctMC4wODg5NjIzMTI1OTcyNTQ0JykKUk9PVF9SID0gUSgxLDE1MDAwMCkKQ0FVQ0hZX09fUiA9IFEoMSwyMDAwMCkKQ0FVQ0hZX0VfUiA9IFEoMSwxMDAwMCkKTEFVTkNIID0gUSgxLDE2KQpNQUpfUiA9IFEoMSw4KQpOID0gMzIKVEFJTF9TID0gUSgxLDIqKjMyKQpUQUlMX1NQID0gUSgxNywyKioyNykKCmNsYXNzIEQ6CiAgICBfX3Nsb3RzX189KCdyZScsJ2ltJywncmFkJykKICAgIGRlZiBfX2luaXRfXyhzZWxmLHJlPTAsaW09MCxyYWQ9MCk6IHNlbGYucmU9UShyZSk7IHNlbGYuaW09UShpbSk7IHNlbGYucmFkPVEocmFkKQogICAgQHN0YXRpY21ldGhvZAogICAgZGVmIGNvKHgpOiByZXR1cm4geCBpZiBpc2luc3RhbmNlKHgsRCkgZWxzZSBEKHgpCiAgICBkZWYgX19hZGRfXyhzZWxmLG8pOiBvPUQuY28obyk7IHJldHVybiBEKHNlbGYucmUrby5yZSxzZWxmLmltK28uaW0sc2VsZi5yYWQrby5yYWQpCiAgICBfX3JhZGRfXz1fX2FkZF9fCiAgICBkZWYgX19uZWdfXyhzZWxmKTogcmV0dXJuIEQoLXNlbGYucmUsLXNlbGYuaW0sc2VsZi5yYWQpCiAgICBkZWYgX19zdWJfXyhzZWxmLG8pOiByZXR1cm4gc2VsZisoLUQuY28obykpCiAgICBkZWYgX19yc3ViX18oc2VsZixvKTogcmV0dXJuIEQuY28obyktc2VsZgogICAgZGVmIGN1KHNlbGYpOiByZXR1cm4gYWJzKHNlbGYucmUpK2FicyhzZWxmLmltKQogICAgZGVmIGNsKHNlbGYpOiByZXR1cm4gbWF4KGFicyhzZWxmLnJlKSxhYnMoc2VsZi5pbSkpCiAgICBkZWYgYXUoc2VsZik6IHJldHVybiBzZWxmLmN1KCkrc2VsZi5yYWQKICAgIGRlZiBsbyhzZWxmKTogcmV0dXJuIHNlbGYuY2woKS1zZWxmLnJhZAogICAgZGVmIF9fbXVsX18oc2VsZixvKToKICAgICAgICBvPUQuY28obykKICAgICAgICByZXR1cm4gRChzZWxmLnJlKm8ucmUtc2VsZi5pbSpvLmltLAogICAgICAgICAgICAgICAgIHNlbGYucmUqby5pbStzZWxmLmltKm8ucmUsCiAgICAgICAgICAgICAgICAgc2VsZi5jdSgpKm8ucmFkK28uY3UoKSpzZWxmLnJhZCtzZWxmLnJhZCpvLnJhZCkKICAgIF9fcm11bF9fPV9fbXVsX18KICAgIGRlZiBpbnYoc2VsZik6CiAgICAgICAgbG89c2VsZi5jbCgpOyBhc3NlcnQgbG8+c2VsZi5yYWQsIChmbG9hdChsbyksZmxvYXQoc2VsZi5yYWQpKQogICAgICAgIG49c2VsZi5yZSpzZWxmLnJlK3NlbGYuaW0qc2VsZi5pbQogICAgICAgIHJldHVybiBEKHNlbGYucmUvbiwtc2VsZi5pbS9uLHNlbGYucmFkLyhsbyoobG8tc2VsZi5yYWQpKSkKICAgIGRlZiBfX3RydWVkaXZfXyhzZWxmLG8pOiByZXR1cm4gc2VsZipELmNvKG8pLmludigpCiAgICBkZWYgX19ydHJ1ZWRpdl9fKHNlbGYsbyk6IHJldHVybiBELmNvKG8pL3NlbGYKICAgIGRlZiBfX3Bvd19fKHNlbGYsbik6CiAgICAgICAgYXNzZXJ0IGlzaW5zdGFuY2UobixpbnQpCiAgICAgICAgaWYgbjwwOnJldHVybiBzZWxmLmludigpKiooLW4pCiAgICAgICAgb3V0PUQoMSk7IGI9c2VsZgogICAgICAgIHdoaWxlIG46CiAgICAgICAgICAgIGlmIG4mMTogb3V0PW91dCpiCiAgICAgICAgICAgIGI9YipiO24vLz0yCiAgICAgICAgcmV0dXJuIG91dAogICAgZGVmIHBhaXIoc2VsZik6IHJldHVybiBbc3RyKHNlbGYucmUpLHN0cihzZWxmLmltKSxzdHIoc2VsZi5yYWQpXQoKST1EKDAsMSkKCmNsYXNzIFU6CiAgICBfX3Nsb3RzX189KCd2JywnZG8nLCdkZScpCiAgICBkZWYgX19pbml0X18oc2VsZix2PTAsZG89MCxkZT0wKTogc2VsZi52PUQuY28odik7c2VsZi5kbz1ELmNvKGRvKTtzZWxmLmRlPUQuY28oZGUpCiAgICBAc3RhdGljbWV0aG9kCiAgICBkZWYgY28oeCk6IHJldHVybiB4IGlmIGlzaW5zdGFuY2UoeCxVKSBlbHNlIFUoeCkKICAgIGRlZiBfX2FkZF9fKHNlbGYsbyk6bz1VLmNvKG8pO3JldHVybiBVKHNlbGYuditvLnYsc2VsZi5kbytvLmRvLHNlbGYuZGUrby5kZSkKICAgIF9fcmFkZF9fPV9fYWRkX18KICAgIGRlZiBfX25lZ19fKHNlbGYpOnJldHVybiBVKC1zZWxmLnYsLXNlbGYuZG8sLXNlbGYuZGUpCiAgICBkZWYgX19zdWJfXyhzZWxmLG8pOnJldHVybiBzZWxmKygtVS5jbyhvKSkKICAgIGRlZiBfX3JzdWJfXyhzZWxmLG8pOnJldHVybiBVLmNvKG8pLXNlbGYKICAgIGRlZiBfX211bF9fKHNlbGYsbyk6CiAgICAgICAgbz1VLmNvKG8pO3JldHVybiBVKHNlbGYudipvLnYsc2VsZi5kbypvLnYrc2VsZi52Km8uZG8sc2VsZi5kZSpvLnYrc2VsZi52Km8uZGUpCiAgICBfX3JtdWxfXz1fX211bF9fCiAgICBkZWYgaW52KHNlbGYpOgogICAgICAgIGl2PXNlbGYudi5pbnYoKTtpdjI9aXYqaXY7cmV0dXJuIFUoaXYsLXNlbGYuZG8qaXYyLC1zZWxmLmRlKml2MikKICAgIGRlZiBfX3RydWVkaXZfXyhzZWxmLG8pOnJldHVybiBzZWxmKlUuY28obykuaW52KCkKICAgIGRlZiBfX3J0cnVlZGl2X18oc2VsZixvKTpyZXR1cm4gVS5jbyhvKS9zZWxmCiAgICBkZWYgX19wb3dfXyhzZWxmLG4pOgogICAgICAgIGFzc2VydCBpc2luc3RhbmNlKG4saW50KSBhbmQgbj49MAogICAgICAgIG91dD1VKDEpO2I9c2VsZgogICAgICAgIHdoaWxlIG46CiAgICAgICAgICAgIGlmIG4mMTpvdXQ9b3V0KmIKICAgICAgICAgICAgYj1iKmI7bi8vPTIKICAgICAgICByZXR1cm4gb3V0CgojIERpcmVjdCBzaGlmdGVkLWhvcml6b24gcG93ZXItc2VyaWVzIGNvZWZmaWNpZW50cyB0aHJvdWdoIGZpcnN0IG9yZGVyIGluIGVwc2lsb24uCmRlZiBzYWRkKGEsYixOKToKICAgIHJldHVybiBbKGFbaV0gaWYgaTxsZW4oYSkgZWxzZSAwKSsoYltpXSBpZiBpPGxlbihiKSBlbHNlIDApIGZvciBpIGluIHJhbmdlKE4pXQpkZWYgc25lZyhhKTpyZXR1cm4gWy14IGZvciB4IGluIGFdCmRlZiBzc3ViKGEsYixOKTpyZXR1cm4gc2FkZChhLHNuZWcoYiksTikKZGVmIHNtdWwoYSxiLE4pOgogICAgb3V0PVswIGZvciBfIGluIHJhbmdlKE4pXQogICAgZm9yIGkgaW4gcmFuZ2UobWluKE4sbGVuKGEpKSk6CiAgICAgICAgZm9yIGogaW4gcmFuZ2UobWluKE4taSxsZW4oYikpKTpvdXRbaStqXT1vdXRbaStqXSthW2ldKmJbal0KICAgIHJldHVybiBvdXQKZGVmIHNzY2FsZShhLGMsTik6cmV0dXJuIFthW2ldKmMgaWYgaTxsZW4oYSkgZWxzZSAwIGZvciBpIGluIHJhbmdlKE4pXQpkZWYgc2RlcihhLE4pOnJldHVybiBbKGkrMSkqYVtpKzFdIGlmIGkrMTxsZW4oYSkgZWxzZSAwIGZvciBpIGluIHJhbmdlKE4pXQpkZWYgem5lZyhrLE4sY29lcmNlKToKICAgIHJldHVybiBbY29lcmNlKFEoKC0xKSoqbiptYXRoLmNvbWIoaytuLTEsbiksMioqKGsrbikpKSBmb3IgbiBpbiByYW5nZShOKV0KZGVmIHpwb3MoayxOLGNvZXJjZSk6CiAgICByZXR1cm4gW2NvZXJjZShRKG1hdGguY29tYihrLG4pKjIqKihrLW4pKSkgaWYgbjw9ayBlbHNlIGNvZXJjZSgwKSBmb3IgbiBpbiByYW5nZShOKV0KCmRlZiBob3Jpem9uX3NlcmllcyhOLE9tZWdhLGVwcyxjb2VyY2UpOgogICAgb25lPVtjb2VyY2UoMSldK1tjb2VyY2UoMCldKihOLTEpCiAgICB6bT17azp6bmVnKGssTixjb2VyY2UpIGZvciBrIGluIFsxLDIsMyw0LDYsNyw4LDldfQogICAgenA0PXpwb3MoNCxOLGNvZXJjZSkKICAgIGY9c3N1YihvbmUsc3NjYWxlKHptWzFdLDIsTiksTikKICAgIGZwPXNzY2FsZSh6bVsyXSwyLE4pCiAgICBmcHA9c3NjYWxlKHptWzNdLC00LE4pCiAgICBwMT1zYWRkKHNzY2FsZSh6bVs2XSwxMixOKSxzc2NhbGUoem1bN10sLVEoMTc2LDkpLE4pLE4pCiAgICBwMXM9c3N1YihwMSxzc2NhbGUoZnAsUSg1LDcyKSxOKSxOKQogICAgcDFwPXNhZGQoc3NjYWxlKHptWzddLC03MixOKSxzc2NhbGUoem1bOF0sUSgxMjMyLDkpLE4pLE4pCiAgICBwMXNwPXNzdWIocDFwLHNzY2FsZShmcHAsUSg1LDcyKSxOKSxOKQogICAgZjE9c2FkZChzc2NhbGUoem1bNl0sMjQsTiksc3NjYWxlKHptWzddLC1RKDM5Miw5KSxOKSxOKQogICAgZjFzPXNzdWIoZjEsc3NjYWxlKGZwLFEoNSw3MiksTiksTikKICAgIHYwPXNzdWIoc3NjYWxlKHptWzJdLDYsTiksc3NjYWxlKHptWzNdLDYsTiksTikKICAgIHYwcD1zYWRkKHNzY2FsZSh6bVszXSwtMTIsTiksc3NjYWxlKHptWzRdLDE4LE4pLE4pCiAgICBudW09c2FkZChzc3ViKHNzY2FsZShvbmUsNjUzLE4pLHNzY2FsZSh6cG9zKDEsTixjb2VyY2UpLDI4MSxOKSxOKSxzc2NhbGUoenA0LDQqKE9tZWdhKk9tZWdhKSxOKSxOKQogICAgdjE9c3NjYWxlKHNtdWwobnVtLHptWzldLE4pLC04LE4pCiAgICB2MXM9c3N1Yih2MSxzc2NhbGUodjBwLFEoNSw3MiksTiksTikKICAgIEEwPXNtdWwoZixmLE4pO0ExPXNzY2FsZShzbXVsKGYscDFzLE4pLDIsTikKICAgIEIwPXNtdWwoZixmcCxOKTtCMT1zYWRkKHNtdWwocDFzLGZwLE4pLHNtdWwoZixwMXNwLE4pLE4pCiAgICBDMD1zc3ViKFtPbWVnYSpPbWVnYV0rW2NvZXJjZSgwKV0qKE4tMSksc211bChmLHYwLE4pLE4pCiAgICBDMT1zbmVnKHNhZGQoc211bChmMXMsdjAsTiksc211bChmLHYxcyxOKSxOKSkKICAgIEE9c2FkZChBMCxzc2NhbGUoQTEsZXBzLE4pLE4pCiAgICBCPXNhZGQoQjAsc3NjYWxlKEIxLGVwcyxOKSxOKQogICAgQz1zYWRkKEMwLHNzY2FsZShDMSxlcHMsTiksTikKICAgIHJldHVybiBBLEIsQwoKZGVmIHJlY3VycmVuY2UoQSxCLEMsYWxwaGEsY291bnQsY29lcmNlKToKICAgIGFhPVtjb2VyY2UoMSldCiAgICBmb3IgbiBpbiByYW5nZSgxLGNvdW50KzEpOgogICAgICAgIGRlbj1BWzJdKihhbHBoYStuKSooYWxwaGErbi0xKStCWzFdKihhbHBoYStuKStDWzBdCiAgICAgICAgbG93PWNvZXJjZSgwKQogICAgICAgIGZvciBtIGluIHJhbmdlKDMsbiszKToKICAgICAgICAgICAgaz1uLW0rMgogICAgICAgICAgICBpZiBrPj0wOmxvdys9QVttXSooYWxwaGEraykqKGFscGhhK2stMSkqYWFba10KICAgICAgICBmb3IgbSBpbiByYW5nZSgyLG4rMik6CiAgICAgICAgICAgIGs9bi1tKzEKICAgICAgICAgICAgaWYgaz49MDpsb3crPUJbbV0qKGFscGhhK2spKmFhW2tdCiAgICAgICAgZm9yIG0gaW4gcmFuZ2UoMSxuKzEpOgogICAgICAgICAgICBrPW4tbQogICAgICAgICAgICBsb3crPUNbbV0qYWFba10KICAgICAgICBhYS5hcHBlbmQoLWxvdy9kZW4pCiAgICByZXR1cm4gYWEKCiMgUmUtY2VydGlmeSBmaW5pdGUgY29lZmZpY2llbnRzIG9uIHN5bW1ldHJpYyBlcHNpbG9uIGRpc2suCk9sYXJnZT1EKE9SRSxPSU0sQ0FVQ0hZX09fUik7IGVsYXJnZT1EKDAsMCxDQVVDSFlfRV9SKQpBZCxCZCxDZD1ob3Jpem9uX3Nlcmllcyg0MixPbGFyZ2UsZWxhcmdlLEQuY28pCmFscGhhX2Q9LTIqSSpPbGFyZ2UrUSgxLDM2KSpJKmVsYXJnZSpPbGFyZ2UKYWQ9cmVjdXJyZW5jZShBZCxCZCxDZCxhbHBoYV9kLDM5LEQuY28pCm1heHNjYWxlZD1RKDEpCmZvciBuLGEgaW4gZW51bWVyYXRlKGFkWzE6XSwxKToKICAgIHNjYWxlZD1hLmF1KCkqTUFKX1IqKm47bWF4c2NhbGVkPW1heChtYXhzY2FsZWQsc2NhbGVkKTthc3NlcnQgc2NhbGVkPD0xLChuLGZsb2F0KHNjYWxlZCkpCgojIFJvb3QtZGlzayBkdWFsIHJlY3VycmVuY2UgYW5kIGZpeGVkLXBoeXNpY2FsLXogbGF1bmNoIGV2YWx1YXRpb24uCk91PVUoRChPUkUsT0lNLDApLEQoMSksRCgwKSk7ZXU9VShEKDApLEQoMCksRCgxKSkKQXUsQnUsQ3U9aG9yaXpvbl9zZXJpZXMoTiszLE91LGV1LFUuY28pCmFscGhhPS0yKlUoSSkqT3UrUSgxLDM2KSpVKEkpKmV1Kk91CmF1PXJlY3VycmVuY2UoQXUsQnUsQ3UsYWxwaGEsTixVLmNvKQp4ZXZhbD1VKEQoTEFVTkNIKSxEKDApLEQoUSg1LDcyKSkpClN2PVUoKTtTcD1VKCkKZm9yIG4sYSBpbiBlbnVtZXJhdGUoYXUpOgogICAgU3YgKz0gYSooeGV2YWwqKm4pCiAgICBpZiBuOlNwICs9IG4qYSooeGV2YWwqKihuLTEpKQptYXJnaW5PPUNBVUNIWV9PX1ItUk9PVF9SO2Fzc2VydCBtYXJnaW5PPjAKU3Yudi5yYWQrPVRBSUxfUztTdi5kby5yYWQrPVRBSUxfUy9tYXJnaW5PO1N2LmRlLnJhZCs9VEFJTF9TL0NBVUNIWV9FX1IKU3Audi5yYWQrPVRBSUxfU1A7U3AuZG8ucmFkKz1UQUlMX1NQL21hcmdpbk87U3AuZGUucmFkKz1UQUlMX1NQL0NBVUNIWV9FX1IKYXNzZXJ0IFN2LnYubG8oKT4wCnpmaXg9USgzMywxNik7Zno9MS1RKDIsMSkvemZpeDtQMXo9USg0KSooUSgyNykqemZpeC1RKDQ0KSkvKFEoOSkqemZpeCoqNykKUGZpeD1VKEQoZnopLEQoMCksRChQMXopKQpxaG9yPVBmaXgqKGFscGhhL3hldmFsK1NwL1N2KS1VKEkpKk91ClM9U3YKCiMgRXhhY3QgZXBzaWxvbi1saW5lYXIgb3V0Z29pbmcgTGF1cmVudCByZWN1cnJlbmNlLgpjbGFzcyBHOgogICAgX19zbG90c19fPSgncmUnLCdpbScpCiAgICBkZWYgX19pbml0X18oc2VsZixyZT0wLGltPTApOnNlbGYucmU9UShyZSk7c2VsZi5pbT1RKGltKQogICAgQHN0YXRpY21ldGhvZAogICAgZGVmIGNvKHgpOnJldHVybiB4IGlmIGlzaW5zdGFuY2UoeCxHKSBlbHNlIEcoeCkKICAgIGRlZiBfX2FkZF9fKHNlbGYsbyk6bz1HLmNvKG8pO3JldHVybiBHKHNlbGYucmUrby5yZSxzZWxmLmltK28uaW0pCiAgICBfX3JhZGRfXz1fX2FkZF9fCiAgICBkZWYgX19uZWdfXyhzZWxmKTpyZXR1cm4gRygtc2VsZi5yZSwtc2VsZi5pbSkKICAgIGRlZiBfX3N1Yl9fKHNlbGYsbyk6cmV0dXJuIHNlbGYrKC1HLmNvKG8pKQogICAgZGVmIF9fcnN1Yl9fKHNlbGYsbyk6cmV0dXJuIEcuY28obyktc2VsZgogICAgZGVmIF9fbXVsX18oc2VsZixvKTpvPUcuY28obyk7cmV0dXJuIEcoc2VsZi5yZSpvLnJlLXNlbGYuaW0qby5pbSxzZWxmLnJlKm8uaW0rc2VsZi5pbSpvLnJlKQogICAgX19ybXVsX189X19tdWxfXwogICAgZGVmIHplcm8oc2VsZik6cmV0dXJuIHNlbGYucmU9PTAgYW5kIHNlbGYuaW09PTAKCmRlZiBMKGE9MCk6CiAgICBpZiBpc2luc3RhbmNlKGEsZGljdCk6cmV0dXJuIHtpbnQoayk6Ry5jbyh2KSBmb3Igayx2IGluIGEuaXRlbXMoKSBpZiBub3QgRy5jbyh2KS56ZXJvKCl9CiAgICBnPUcuY28oYSk7cmV0dXJuIHt9IGlmIGcuemVybygpIGVsc2UgezA6Z30KZGVmIGxhZGQoYSxiKToKICAgIGQ9ZGljdChhKQogICAgZm9yIGssdiBpbiBiLml0ZW1zKCk6ZFtrXT1kLmdldChrLEcoKSkrdgogICAgcmV0dXJuIHtrOnYgZm9yIGssdiBpbiBkLml0ZW1zKCkgaWYgbm90IHYuemVybygpfQpkZWYgbG5lZyhhKTpyZXR1cm4ge2s6LXYgZm9yIGssdiBpbiBhLml0ZW1zKCl9CmRlZiBsc3ViKGEsYik6cmV0dXJuIGxhZGQoYSxsbmVnKGIpKQpkZWYgbG11bChhLGIpOgogICAgZD17fQogICAgZm9yIGksdSBpbiBhLml0ZW1zKCk6CiAgICAgICAgZm9yIGosdiBpbiBiLml0ZW1zKCk6ZFtpK2pdPWQuZ2V0KGkraixHKCkpK3UqdgogICAgcmV0dXJuIHtrOnYgZm9yIGssdiBpbiBkLml0ZW1zKCkgaWYgbm90IHYuemVybygpfQpkZWYgbHNjYWxlKGEsYyk6CiAgICBjPUcuY28oYyk7cmV0dXJuIHtrOnYqYyBmb3Igayx2IGluIGEuaXRlbXMoKSBpZiBub3QgKHYqYykuemVybygpfQpkZWYgbHNoaWZ0KGEsbik6cmV0dXJuIHtrK246diBmb3Igayx2IGluIGEuaXRlbXMoKX0KZGVmIGxkZXIoYSk6cmV0dXJuIHtrLTE6Ryh2LnJlKmssdi5pbSprKSBmb3Igayx2IGluIGEuaXRlbXMoKSBpZiBrfQpkZWYgTFAoYT0wLGI9MCk6cmV0dXJuIChMKGEpLEwoYikpCmRlZiBwYWRkKGEsYik6cmV0dXJuIChsYWRkKGFbMF0sYlswXSksbGFkZChhWzFdLGJbMV0pKQpkZWYgcG5lZyhhKTpyZXR1cm4gKGxuZWcoYVswXSksbG5lZyhhWzFdKSkKZGVmIHBzdWIoYSxiKTpyZXR1cm4gcGFkZChhLHBuZWcoYikpCmRlZiBwc2NhbGUoYSxjKTpyZXR1cm4gKGxzY2FsZShhWzBdLGMpLGxzY2FsZShhWzFdLGMpKQpkZWYgcG11bChhLGIpOnJldHVybiAobG11bChhWzBdLGJbMF0pLGxhZGQobG11bChhWzBdLGJbMV0pLGxtdWwoYVsxXSxiWzBdKSkpCmRlZiBwZGl2KGEpOgogICAgZmFjPUcoMCwtUSgxLDIpKTtyZXR1cm4gKGxzY2FsZShsc2hpZnQoYVswXSwtMSksZmFjKSxsc2NhbGUobHNoaWZ0KGFbMV0sLTEpLGZhYykpCmRlZiBRY29lZihuKToKICAgIGlmIG49PTI6cmV0dXJuIExQKDYpCiAgICBpZiBuPT0zOnJldHVybiBMUCgtMTgpCiAgICBpZiBuPT00OnJldHVybiBMUCgxMikKICAgIGlmIG49PTU6cmV0dXJuIExQKDAsezI6RygtMzIpfSkKICAgIGlmIG49PTY6cmV0dXJuIExQKDAsezI6Ryg2NCl9KQogICAgaWYgbj09ODpyZXR1cm4gTFAoMCwyMzkyKQogICAgaWYgbj09OTpyZXR1cm4gTFAoMCwtUSgzMDM3NiwzKSkKICAgIGlmIG49PTEwOnJldHVybiBMUCgwLFEoMzIxMjgsMykpCiAgICByZXR1cm4gTFAoKQpkZWYgY29lZmZzKE4pOgogICAgYz1bTFAoKSBmb3IgXyBpbiByYW5nZShOKzEpXQogICAgZm9yIG4gaW4gcmFuZ2UoMixOKzEpOgogICAgICAgIHJocz1RY29lZihuKQogICAgICAgIGlmIG4tMT49MjpyaHM9cGFkZChyaHMscHNjYWxlKGNbbi0xXSxuLTEpKQogICAgICAgIGlmIG4tMj49MjpyaHM9cHN1YihyaHMscHNjYWxlKGNbbi0yXSwyKihuLTIpKSkKICAgICAgICBpZiBuLTc+PTI6cmhzPXBhZGQocmhzLChMKCksbHNjYWxlKGNbbi03XVswXSwxMioobi03KSkpKQogICAgICAgIGlmIG4tOD49MjpyaHM9cGFkZChyaHMsKEwoKSxsc2NhbGUoY1tuLThdWzBdLC1RKDE3Niw5KSoobi04KSkpKQogICAgICAgIHNxPUxQKCkKICAgICAgICBmb3IgaiBpbiByYW5nZSgyLG4tMSk6c3E9cGFkZChzcSxwbXVsKGNbal0sY1tuLWpdKSkKICAgICAgICBjW25dPXBkaXYocHN1YihyaHMsc3EpKQogICAgcmV0dXJuIGMKZGVmIHJlc2lkdWFsKGMsTik6CiAgICBvdXQ9e30KICAgIGZvciBuIGluIHJhbmdlKDIsbWF4KDIqTixOKzgpKzEpOgogICAgICAgIHY9TFAoKQogICAgICAgIGlmIG48PU46dj1wYWRkKHYsKGxzY2FsZShsc2hpZnQoY1tuXVswXSwxKSxHKDAsMikpLGxzY2FsZShsc2hpZnQoY1tuXVsxXSwxKSxHKDAsMikpKSkKICAgICAgICBpZiAyPD1uLTE8PU46dj1wc3ViKHYscHNjYWxlKGNbbi0xXSxuLTEpKQogICAgICAgIGlmIDI8PW4tMjw9Tjp2PXBhZGQodixwc2NhbGUoY1tuLTJdLDIqKG4tMikpKQogICAgICAgIGlmIDI8PW4tNzw9Tjp2PXBzdWIodiwoTCgpLGxzY2FsZShjW24tN11bMF0sMTIqKG4tNykpKSkKICAgICAgICBpZiAyPD1uLTg8PU46dj1wc3ViKHYsKEwoKSxsc2NhbGUoY1tuLThdWzBdLC1RKDE3Niw5KSoobi04KSkpKQogICAgICAgIGZvciBqIGluIHJhbmdlKDIsTisxKToKICAgICAgICAgICAgaz1uLWoKICAgICAgICAgICAgaWYgMjw9azw9Tjp2PXBhZGQodixwbXVsKGNbal0sY1trXSkpCiAgICAgICAgdj1wc3ViKHYsUWNvZWYobikpCiAgICAgICAgaWYgdlswXSBvciB2WzFdOm91dFtuXT12CiAgICByZXR1cm4gb3V0CgpkZWYgZXZhbEwoYSxPZCk6CiAgICBvdXQ9RCgpCiAgICBmb3IgayxnIGluIGEuaXRlbXMoKTpvdXQrPUQoZy5yZSxnLmltKSooT2QqKmspCiAgICByZXR1cm4gb3V0CgpkZWYgZ2V2YWwoYSxvKToKICAgIG91dD1HKCkKICAgIGRlZiBncChuKToKICAgICAgICBpZiBuPDA6CiAgICAgICAgICAgIGQ9by5yZSpvLnJlK28uaW0qby5pbTtyZXR1cm4gZ3AyKEcoby5yZS9kLC1vLmltL2QpLC1uKQogICAgICAgIHJldHVybiBncDIobyxuKQogICAgZGVmIGdwMih4LG4pOgogICAgICAgIHo9RygxKTtiPXgKICAgICAgICB3aGlsZSBuOgogICAgICAgICAgICBpZiBuJjE6ej16KmIKICAgICAgICAgICAgYj1iKmI7bi8vPTIKICAgICAgICByZXR1cm4gegogICAgZm9yIGssdiBpbiBhLml0ZW1zKCk6b3V0Kz12KmdwKGspCiAgICByZXR1cm4gb3V0CgpOSj0xNDtUPTMyO2M9Y29lZmZzKE5KKTtSPXJlc2lkdWFsKGMsTkopO2Fzc2VydCBtaW4oUik9PTE1CnJobz1RKDEsVCkKIyBWb2x0ZXJyYSBjb250cmFjdGlvbiBvbiBzeW1tZXRyaWMgbG9jYWwgcGFyYW1ldGVyIGRpc2tzLgpPbGFyZ2UyPUQoT1JFLE9JTSxDQVVDSFlfT19SKTtlbGFyZ2UyPUQoMCwwLENBVUNIWV9FX1IpCmRlZiBldmFsUChwYWlyKTpyZXR1cm4gZXZhbEwocGFpclswXSxPbGFyZ2UyKStlbGFyZ2UyKmV2YWxMKHBhaXJbMV0sT2xhcmdlMikKcWJvdW5kPXN1bSgoZXZhbFAoY1tuXSkuYXUoKSpyaG8qKm4gZm9yIG4gaW4gcmFuZ2UoMixOSisxKSksUSgpKQpyYm91bmQ9c3VtKChldmFsUCh2KS5hdSgpKnJobyoqbiBmb3Igbix2IGluIFIuaXRlbXMoKSksUSgpKQplcHNtYXg9Q0FVQ0hZX0VfUgpwZGVsPTIqcmhvK2Vwc21heCooMTIqcmhvKio2K1EoMTc2LDkpKnJobyoqNyk7cGludj0xLygxLXBkZWwpCnJlbWluPU9SRS1DQVVDSFlfT19SCm9tZWdhYWJzPU9sYXJnZTIuYXUoKQpkYW1wPTIqcmVtaW4tMipvbWVnYWFicypwZGVsKnBpbnYtMipxYm91bmQqcGludgpmb3JjZT1yYm91bmQqcGludjtub25saW49cGludjtqdGFpbD1RKDEsMTAqKjkpCmFzc2VydCBkYW1wPjAgYW5kIGRhbXAqanRhaWw+PWZvcmNlK25vbmxpbipqdGFpbCpqdGFpbCBhbmQgMipub25saW4qanRhaWw8ZGFtcAojIEVuZHBvaW50IGZpbml0ZSBMYXVyZW50IHBpZWNlcyBvdmVyIHRoZSBhY3R1YWwgcm9vdCBkaXNrLgp6MD1HKDMsMzIpO3puPXowLnJlKnowLnJlK3owLmltKnowLmltO3kwPUcoejAucmUvem4sLXowLmltL3puKQpxMD1MKCk7cTE9TCgpCmRlZiBncG93KGEsbik6CiAgICBpZiBuPDA6CiAgICAgICAgZD1hLnJlKmEucmUrYS5pbSphLmltO3JldHVybiBncG93KEcoYS5yZS9kLC1hLmltL2QpLC1uKQogICAgb3V0PUcoMSk7Yj1hCiAgICB3aGlsZSBuOgogICAgICAgIGlmIG4mMTpvdXQ9b3V0KmIKICAgICAgICBiPWIqYjtuLy89MgogICAgcmV0dXJuIG91dApmb3IgbiBpbiByYW5nZSgyLE5KKzEpOgogICAgeW49Z3Bvdyh5MCxuKTtxMD1sYWRkKHEwLGxzY2FsZShjW25dWzBdLHluKSk7cTE9bGFkZChxMSxsc2NhbGUoY1tuXVsxXSx5bikpCk9yb290PUQoT1JFLE9JTSwwKQpxaW5mPWV2YWxMKHEwLE9yb290KQp1b2luZj1ldmFsTChsZGVyKHEwKSxPcm9vdCkKdWVpbmY9ZXZhbEwocTEsT3Jvb3QpCnFpbmYucmFkKz1qdGFpbAp1b2luZi5yYWQrPWp0YWlsL21hcmdpbk8KdWVpbmYucmFkKz1qdGFpbC9DQVVDSFlfRV9SCgojIE91dHdhcmQgOTYtYml0IHJlY29yZHMuCkJJVFM9OTY7U0NBTEU9MTw8QklUUwpkZWYgbmVhcmVzdChxKToKICAgIG49cS5udW1lcmF0b3IqU0NBTEU7ZD1xLmRlbm9taW5hdG9yCiAgICByZXR1cm4gKDIqbitkKS8vKDIqZCkgaWYgbj49MCBlbHNlIC0oKDIqKC1uKStkKS8vKDIqZCkpCmRlZiBjZWlscShxKTpyZXR1cm4gKHEubnVtZXJhdG9yKlNDQUxFK3EuZGVub21pbmF0b3ItMSkvL3EuZGVub21pbmF0b3IKZGVmIHJlYyhkKToKICAgIGE9bmVhcmVzdChkLnJlKTtiPW5lYXJlc3QoZC5pbSkKICAgIGVycj1hYnMoZC5yZS1RKGEsU0NBTEUpKSthYnMoZC5pbS1RKGIsU0NBTEUpKQogICAgcmV0dXJuIHsnY2VudGVyJzpbYSxiXSwncmFkaXVzJzpjZWlscShkLnJhZCtlcnIpLCdiaXRzJzpCSVRTfQoKcGF5bG9hZD17CiAnbWV0aG9kJzonZXBzaWxvbj0wIGVuZHBvaW50IHRhbmdlbnQgZGlza3MgZnJvbSBleGFjdCBob3Jpem9uIEZyb2Jlbml1cyBhbmQgaW5maW5pdHkgTGF1cmVudC1Wb2x0ZXJyYSByZWN1cnJlbmNlcycsCiAnb21lZ2FfY2VudGVyJzpbc3RyKE9SRSksc3RyKE9JTSldLAogJ29tZWdhX3Jvb3RfZGlza19yYWRpdXMnOnN0cihST09UX1IpLAogJ2NhdWNoeV9vbWVnYV9yYWRpdXMnOnN0cihDQVVDSFlfT19SKSwKICdjYXVjaHlfZXBzaWxvbl9yYWRpdXMnOnN0cihDQVVDSFlfRV9SKSwKICdob3Jpem9uJzp7J3onOiczMy8xNicsJ3EnOnJlYyhxaG9yLnYpLCdkT21lZ2EnOnJlYyhxaG9yLmRvKSwnZEVwc2lsb24nOnJlYyhxaG9yLmRlKSwnc19ub256ZXJvX2xvd2VyX2R5YWRpY185Nic6aW50KFMudi5sbygpKlNDQUxFKX0sCiAnaW5maW5pdHknOnsneic6JzMrMzIqaScsJ3EnOnJlYyhxaW5mKSwnZE9tZWdhJzpyZWModW9pbmYpLCdkRXBzaWxvbic6cmVjKHVlaW5mKSwndGFpbF9yYWRpdXMnOnN0cihqdGFpbCksJ2RhbXBpbmdfbG93ZXJfZHlhZGljXzk2JzppbnQoZGFtcCpTQ0FMRSl9LAogJ21ham9yYW50Jzp7J3N5bW1ldHJpY19lcHNpbG9uX2Rpc2snOlRydWUsJ21heF9zY2FsZWRfZmluaXRlX2NvZWZmaWNpZW50JzpzdHIobWF4c2NhbGVkKSwnc2VyaWVzX3RhaWwnOnN0cihUQUlMX1MpLCdkZXJpdmF0aXZlX3RhaWwnOnN0cihUQUlMX1NQKX0sCn0KcGF5bG9hZFsnaGFzaCddPWhhc2hsaWIuc2hhMjU2KGpzb24uZHVtcHMocGF5bG9hZCxzb3J0X2tleXM9VHJ1ZSxzZXBhcmF0b3JzPSgnLCcsJzonKSkuZW5jb2RlKCkpLmhleGRpZ2VzdCgpCgo=").decode("utf-8"),namespace)
    p=namespace["payload"]
    record={
        "method":"exact-center endpoint q refinement from the epsilon=0 Frobenius and Laurent recurrences",
        "bits":96,
        "endpoint_tangent_hash":"94ec87296b933bf4de3aada5d8bede67a80619f0767410e82767d64d5239d8c1",
        "horizon_q":p["horizon"]["q"],
        "infinity_q":p["infinity"]["q"],
    }
    assert record["horizon_q"]["radius"] == 308083963600422710625
    assert record["infinity_q"]["radius"] == 79228162514264337595
    record["hash"]=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert record["hash"] == "b8e04031a4693df55233cd9aa75359107bac0b332d6a4e42389f22ff939019fb"
    return record

AXIAL_EPSILON0_CENTER_Q_REFINEMENT_220_PAYLOAD=(
    _certify_axial_epsilon0_center_q_refinement_220()
)

# Validated propagation of q and its epsilon=0 Omega/epsilon tangents.
def _certify_axial_epsilon0_tangent_propagation_220():
    from fractions import Fraction as Q
    import hashlib
    import json
    import math
    SB=128;SS=1<<SB

    def supq(x):
     x=Q(x)*SS;return Q((x.numerator+x.denominator-1)//x.denominator,SS)
    def infq(x):
     x=Q(x)*SS;return Q(x.numerator//x.denominator,SS)
    def ulp(x):return math.ulp(x) if math.isfinite(x) else float('inf')
    def upf(x,n=8):
     x=float(x)
     for _ in range(n):x=math.nextafter(x,math.inf)
     return x
    def float_up_q(x):
     x=Q(x);f=float(x)
     while Q.from_float(f)<x:f=math.nextafter(f,math.inf)
     return f
    def qfloat_err(x,f):return abs(Q(x)-Q.from_float(f)) if isinstance(x,Q) else Q(0)

    class F:
     __slots__=('c','r')
     def __init__(self,re=0.,im=0.,r=0.):
      if isinstance(re,complex) and im==0:im=re.imag;re=re.real
      fr=float(re);fi=float(im);er=float_up_q(r) if isinstance(r,Q) else upf(r)
      if isinstance(re,Q):er+=float(abs(re-Q.from_float(fr)))
      if isinstance(im,Q):er+=float(abs(im-Q.from_float(fi)))
      self.c=complex(fr,fi);self.r=upf(er)
     @staticmethod
     def co(x):return x if isinstance(x,F) else F(x)
     def au(self):return upf(abs(self.c.real)+abs(self.c.imag)+self.r)
     def cu(self):return upf(abs(self.c.real)+abs(self.c.imag))
     def lo(self):return max(abs(self.c.real),abs(self.c.imag))-self.r
     def __add__(self,o):
      o=F.co(o);z=self.c+o.c;e=ulp(z.real)+ulp(z.imag)
      return F(z,r=upf(self.r+o.r+e,16))
     __radd__=__add__
     def __neg__(self):return F(-self.c,r=self.r)
     def __sub__(self,o):return self+(-F.co(o))
     def __rsub__(self,o):return F.co(o)-self
     def __mul__(self,o):
      o=F.co(o);a,b=self.c.real,self.c.imag;c,d=o.c.real,o.c.imag
      p1=a*c;p2=b*d;p3=a*d;p4=b*c;rr=p1-p2;ii=p3+p4
      e=ulp(p1)+ulp(p2)+ulp(rr)+ulp(p3)+ulp(p4)+ulp(ii)
      rad=self.cu()*o.r+o.cu()*self.r+self.r*o.r+e
      return F(rr,ii,upf(rad,16))
     __rmul__=__mul__
     def inv(self):
      L=max(abs(self.c.real),abs(self.c.imag));assert L>self.r,(self.c,self.r)
      a=Q.from_float(self.c.real);b=Q.from_float(self.c.imag);den=a*a+b*b
      er=a/den;ei=-b/den;fr=float(er);fi=float(ei)
      rnd=float(abs(er-Q.from_float(fr))+abs(ei-Q.from_float(fi)))
      rr=Q.from_float(self.r);Lq=Q.from_float(L);rem=rr/(Lq*(Lq-rr))+abs(er-Q.from_float(fr))+abs(ei-Q.from_float(fi))
      return F(fr,fi,float_up_q(rem))
     def __truediv__(self,o):return self*F.co(o).inv()
     def __rtruediv__(self,o):return F.co(o)/self
     def __pow__(self,n):
      if n<0:return self.inv()**(-n)
      out=F(1);b=self
      while n:
       if n&1:out=out*b
       b=b*b;n//=2
      return out
    I=F(0,1);O0=F(Q('0.3736716812299648'),Q('-0.0889623125972544'));OR=Q(1,150000);Ob=supq(Q.from_float(O0.au())+OR)

    def coeff_series(c,d,N):
     c=F.co(c);d=F.co(d);iv=1/c;ratio=-d*iv
     invp=[F(1)]
     for _ in range(10):invp.append(invp[-1]*iv)
     rp=[F(1)]
     for _ in range(N):rp.append(rp[-1]*ratio)
     zm={k:[invp[k]*rp[n]*math.comb(k+n-1,n) for n in range(N)] for k in range(1,11)}
     f=[(F(1) if n==0 else F())-2*zm[1][n] for n in range(N)]
     p1=[12*zm[6][n]-F(Q(176,9))*zm[7][n] for n in range(N)]
     q0=[6*zm[2][n]-18*zm[3][n]+12*zm[4][n] for n in range(N)]
     OO=O0*O0
     qe=[-32*OO*zm[5][n]+64*OO*zm[6][n]+2392*zm[8][n]-F(Q(30376,3))*zm[9][n]+F(Q(32128,3))*zm[10][n] for n in range(N)]
     return f,p1,q0,qe

    def coefficient_bounds(c,R):
     R=Q(R);z=F.co(c).c;cr=Q.from_float(z.real);ci=Q.from_float(z.imag)
     if ci==0:
      zlo=cr-R;zup=cr+R;xlo=cr-2-R;assert zlo>0 and xlo>0
      inv={k:supq(1/zlo**k) for k in range(1,11)};flo=infq(xlo/zup)
     else:
      T=abs(ci);zlo=max(abs(cr),T)-R;zup=abs(cr)+T+R;zm2=max(abs(cr-2),T)-R;assert zlo>0 and zm2>0
      inv={k:supq(1/zlo**k) for k in range(1,11)};flo=infq(zm2/zup)
     Qb=supq(6*inv[2]+18*inv[3]+12*inv[4]);Qeb=supq(32*Ob*Ob*inv[5]+64*Ob*Ob*inv[6]+2392*inv[8]+Q(30376,3)*inv[9]+Q(32128,3)*inv[10])
     return flo,Qb,Qeb,supq(12*inv[6]+Q(176,9)*inv[7]),supq(1+2*inv[1]),inv[5]

    def find_Bq(Y,R,flo,Qb,Oc):
     b=supq(max(Q(1,100),2*Y))
     for _ in range(64):
      rhs=supq(Y+R*(Qb+b*b+2*Oc*b)/flo)
      if rhs<=b and R*(2*b+2*Oc)/flo<1:return b
      b=supq(max(Q(5,4)*b,Q(21,20)*rhs))
     raise AssertionError('Bq')

    def center_step(q,u,v,c,h,d,N,R):
     f,p1,Q0,Qe=coeff_series(c,d,N+1);invf=[1/f[0]]
     for n in range(1,N+1):
      x=F()
      for k in range(1,n+1):x+=f[k]*invf[n-k]
      invf.append(-x/f[0])
     qs=[q];us=[u];vs=[v];gz=[];aa=[];bo=[];be=[]
     for n in range(N):
      q2=[]
      for m in range(n+1):
       x=F()
       for j in range(m+1):x+=qs[j]*qs[m-j]
       q2.append(x)
      x=F()
      for k in range(n+1):
       j=n-k;x+=invf[k]*(Q0[j]-q2[j]-2*I*O0*qs[j])
      gz.append(x);qs.append(d*x/F(n+1))
      xa=F();xb=F()
      for k in range(n+1):
       j=n-k;xa+=invf[k]*(-2*(qs[j]+(I*O0 if j==0 else F())));xb+=invf[k]*(-2*I*qs[j])
      aa.append(xa);bo.append(xb)
      x=bo[n]
      for k in range(n+1):x+=aa[k]*us[n-k]
      us.append(d*x/F(n+1))
      x=F()
      for k in range(n+1):
       j=n-k;pg=F()
       for a in range(j+1):pg+=p1[a]*gz[j-a]
       x+=invf[k]*(Qe[j]-pg)
      be.append(x);x=be[n]
      for k in range(n+1):x+=aa[k]*vs[n-k]
      vs.append(d*x/F(n+1))
     def ev(a):
      x=F();hp=F(1)
      for z in a:x+=z*hp;hp*=F(h)
      return x
     nq,nu,nv=ev(qs),ev(us),ev(vs);arq,aru,arv=nq.r,nu.r,nv.r;nq.r=nu.r=nv.r=0.
     flo,Qb,Qeb,p1b,fup,z5=coefficient_bounds(c,R);Bq=find_Bq(Q.from_float(q.au()),R,flo,Qb,Q.from_float(O0.au()));A=supq(2*(Bq+Q.from_float(O0.au()))/flo);assert R*A<1
     Bu=supq((Q.from_float(u.au())+R*(2*Bq/flo))/(1-R*A));G=supq((Qb+Bq*Bq+2*Q.from_float(O0.au())*Bq)/flo);Bv=supq((Q.from_float(v.au())+R*(Qeb+p1b*G)/flo)/(1-R*A));rho=abs(Q(h))/R
     tq=supq(Bq*rho**(N+1)/(1-rho)+Q.from_float(arq));tu=supq(Bu*rho**(N+1)/(1-rho)+Q.from_float(aru));tv=supq(Bv*rho**(N+1)/(1-rho)+Q.from_float(arv))
     return nq,nu,nv,(tq,tu,tv),(Bq,Bu,Bv,(flo,Qb,Qeb,p1b,fup,z5))

    def step_errors(q,u,v,rq,ru,rv,c,h,d,R,loc,bounds):
     tq,tu,tv=loc;Bq,Bu,Bv,bd=bounds;flo,Qb,Qeb,p1b,fup,z5=bd;G=supq((Qb+Bq*Bq+2*Q.from_float(O0.au())*Bq)/flo);qcenter_var=supq(abs(Q(h))*G)
     # Center-solution q error: Omega is fixed at O0, so only the nonlinear
     # center remainder and numerical/truncation error enter here.
     be=supq(max(2*rq,Q(1,10**16)))
     for _ in range(64):
      zmc=F.co(c)+F.co(d)*F(Q(h,2));zm=F(zmc.c,r=Q(abs(h),2))
      qd=F(q.c,r=qcenter_var+be);fd=1-2/zm;a=F.co(d)*(-2*(qd+I*O0)/fd);mu=supq(Q.from_float(a.c.real+a.r))
      fq=supq(be*be/flo);den=1-mu*abs(Q(h));assert den>0,(float(mu),float(h))
      rhs=supq((rq+abs(Q(h))*fq)/den)
      if rhs<=be:break
      be=supq(max(Q(5,4)*be,Q(21,20)*rhs))
     else:raise AssertionError('center q remainder')
     rq2=supq(rhs+tq)
     # Across the certified root disk, q(Omega)-q(O0) is controlled by the
     # propagated Omega tangent, rather than by an independent forcing disk.
     qpar=supq((Bu+ru)*OR+be)
     da=supq(2*(qpar+OR)/flo);muu=supq(mu+da);den=1-muu*abs(Q(h));assert den>0
     fu=supq(da*(Bu+ru)+2*qpar/flo);ru2=supq((ru+abs(Q(h))*fu)/den+tu)
     qevar=supq(32*fup*z5*(2*Ob*OR+OR*OR))
     gerr=supq(((2*Bq+qpar+2*Ob)*qpar+2*OR*(Bq+qpar))/flo)
     db=supq((qevar+p1b*gerr)/flo);fv=supq(da*(Bv+rv)+db);rv2=supq((rv+abs(Q(h))*fv)/den+tv)
     return rq2,ru2,rv2

    def propagate(name,init,kind):
     q,u,v,rq,ru,rv=init;N=(20 if kind=='h' else 12);steps=0
     if kind=='h':
      z=Q(33,16)
      while z<3:
       x=z-2;h=Q(1,1024) if x<Q(1,8) else Q(1,512) if x<Q(1,4) else Q(1,256) if x<Q(1,2) else Q(1,128);h=min(h,3-z);R=Q(5,2)*h;c=F(z);d=F(1)
       nq,nu,nv,loc,bounds=center_step(q,u,v,c,h,d,N,R);rq,ru,rv=step_errors(q,u,v,rq,ru,rv,c,h,d,R,loc,bounds);q,u,v=nq,nu,nv;z+=h;steps+=1
     else:
      s=Q(0)
      while s<32:
       t=32-s;R=Q(1,2) if t>Q(117,8) else Q(1,4) if t>8 else Q(1,8) if t>4 else Q(1,16) if t>2 else Q(1,32) if t>1 else Q(1,64);h=min(R/Q(4),32-s);c=F(3,t);d=F(0,-1)
       nq,nu,nv,loc,bounds=center_step(q,u,v,c,h,d,N,R);rq,ru,rv=step_errors(q,u,v,rq,ru,rv,c,h,d,R,loc,bounds);q,u,v=nq,nu,nv;s+=h;steps+=1
     return q,u,v,rq,ru,rv,steps
    S96=2**96
    def fpair(a,b):return F(Q(a,S96),Q(b,S96))
    ep=AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_PAYLOAD
    ref=AXIAL_EPSILON0_CENTER_Q_REFINEMENT_220_PAYLOAD
    assert ep['hash']=='94ec87296b933bf4de3aada5d8bede67a80619f0767410e82767d64d5239d8c1'
    assert ref['hash']=='b8e04031a4693df55233cd9aa75359107bac0b332d6a4e42389f22ff939019fb'
    def initial(side):
     p=ep[side];q=ref[side+'_q'];uo=p['dOmega'];ue=p['dEpsilon']
     return (fpair(*q['center']),fpair(*uo['center']),fpair(*ue['center']),
             Q(q['radius'],S96),Q(uo['radius'],S96),Q(ue['radius'],S96))
    hor=initial('horizon');inf=initial('infinity')
    H=propagate('H',hor,'h')
    J=propagate('I',inf,'i')
    Dc=H[1]-J[1];Ec=H[2]-J[2]
    Dr=supq(H[4]+J[4]);Er=supq(H[5]+J[5])
    Dball=F(Dc.c,r=Dr);Eball=F(Ec.c,r=Er);R=-Eball/Dball
    assert max(abs(Dc.c.real),abs(Dc.c.imag)) > float(Dr)
    assert R.c.real-R.r > 0
    record={
      'method':'IEEE-754 complex centers with per-operation ulp balls, affine-q frequency control, and 128-bit outward variation-of-constants bounds',
      'omega_center':[O0.c.real,O0.c.imag],
      'omega_root_radius':'1/150000',
      'center_q_refinement_hash':ref['hash'],
      'horizon':{'steps':H[6],'q':[H[0].c.real,H[0].c.imag,float(H[3])],'domega':[H[1].c.real,H[1].c.imag,float(H[4])],'deps':[H[2].c.real,H[2].c.imag,float(H[5])]},
      'infinity':{'steps':J[6],'q':[J[0].c.real,J[0].c.imag,float(J[3])],'domega':[J[1].c.real,J[1].c.imag,float(J[4])],'deps':[J[2].c.real,J[2].c.imag,float(J[5])]},
      'mismatch_domega':[Dc.c.real,Dc.c.imag,float(Dr)],
      'mismatch_depsilon':[Ec.c.real,Ec.c.imag,float(Er)],
      'implicit_derivative':[R.c.real,R.c.imag,R.r],
    }
    record['hash']=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert record['hash']=='505622d2e96a94d41891f09ad623ca66d0cfa11f4ef4561c4051a96a8356f8ef'
    return record

AXIAL_EPSILON0_TANGENT_PROPAGATION_220_PAYLOAD=(
    _certify_axial_epsilon0_tangent_propagation_220()
)
AXIAL_EPSILON0_TANGENT_PROPAGATION_220_HASH=(
    AXIAL_EPSILON0_TANGENT_PROPAGATION_220_PAYLOAD['hash']
)

# Symbolic-ell trapping and Morawetz certificate.  The exact algebraic
# positivity checks execute in an isolated namespace so the canonical symbols
# used above are not rebound.
import base64 as _gfe_morawetz_base64
_AXIAL_SYMBOLIC_ELL_MORAWETZ_NS = {
    "__name__": "gfe_axial_symbolic_ell_morawetz"
}
exec(
    compile(
        _gfe_morawetz_base64.b64decode("IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgaGFzaGxpYgppbXBvcnQganNvbgpmcm9tIG1hdGggaW1wb3J0IGNvbWIKCmltcG9ydCBzeW1weSBhcyBzCgp4LCBlcHNpbG9uID0gcy5zeW1ib2xzKCJ4IGVwc2lsb24iLCBub25uZWdhdGl2ZT1UcnVlKQpMcyA9IHMuc3ltYm9scygiTCIsIGludGVnZXI9VHJ1ZSwgcG9zaXRpdmU9VHJ1ZSkKayA9IHMuc3ltYm9scygiayIsIG5vbm5lZ2F0aXZlPVRydWUpCnQsIHUgPSBzLnN5bWJvbHMoInQgdSIsIG5vbm5lZ2F0aXZlPVRydWUpCkVQU0lMT05fTUFYID0gcy5SYXRpb25hbCgxLCAxMDAwMCkKWF9MRUZUID0gcy5SYXRpb25hbCg5OSwgMTAwKQpYX1JJR0hUID0gcy5SYXRpb25hbCg0LCAzKQoKQjYgPSAoCiAgICAyMTYqeCoqNyArIDI4MDgqeCoqNiArIDE1NTUyKngqKjUgKyA0NzUyMCp4Kio0CiAgICArIDg2NDAwKngqKjMgKyA5MzMxMip4KioyICsgNTUyOTYqeCArIDEzODI0CiAgICArIGVwc2lsb24qKAogICAgICAgIDMwKngqKjYgKyAyODUqeCoqNSArIDEwMjAqeCoqNCArIDE1MDAqeCoqMwogICAgICAgICsgODM0NzIqeCAtIDIyOTQ0CiAgICApCikKQkRFTFRBID0gKAogICAgMzYqeCoqNyArIDUwNCp4Kio2ICsgMzAyNCp4Kio1ICsgMTAwODAqeCoqNAogICAgKyAyMDE2MCp4KiozICsgMjQxOTIqeCoqMiArIDE2MTI4KnggKyA0NjA4CiAgICArIGVwc2lsb24qKAogICAgICAgIDUqeCoqNiArIDU1KngqKjUgKyAyNDAqeCoqNCArIDUwMCp4KiozCiAgICAgICAgKyA2MTYwKngqKjIgKyA5NTUyKnggLSAzOTM2CiAgICApCikKQlJBQ0tFVCA9IHMuZXhwYW5kKEI2ICsgKExzIC0gNikqQkRFTFRBKQpXID0gcy5mYWN0b3IoKCh4ICsgMikqKjYgKyAzMiplcHNpbG9uKngpLyh4ICsgMikqKjYpClUgPSBzLmZhY3Rvcih4KkJSQUNLRVQvKDM2Kih4ICsgMikqKjEwKSkKUSA9IHMuY2FuY2VsKFUvVykKCiMgVGhlIGNvcnJlY3RlZCB0b3J0b2lzZSBwcmluY2lwYWwgZmFjdG9yIFA9ZHgvZHkuClAgPSBzLmZhY3RvcigKICAgIHgqKAogICAgICAgIDM2KngqKjYgKyA0MzIqeCoqNSArIDIxNjAqeCoqNCArIDU3NjAqeCoqMwogICAgICAgICsgODY0MCp4KioyICsgNjkxMip4ICsgMjMwNAogICAgICAgICsgZXBzaWxvbiooLTUqeCoqNCAtIDUwKngqKjMgLSAyMDAqeCoqMiAtIDQwMCp4ICsgMzIpCiAgICApLygzNiooeCArIDIpKio3KQopCgoKZGVmIGJlcm5zdGVpbl9jb2VmZmljaWVudHNfMmQoZXhwcjogcy5FeHByLCB4YTogcy5SYXRpb25hbCwgeGI6IHMuUmF0aW9uYWwpIC0+IGxpc3Rbcy5FeHByXToKICAgICIiIkV4YWN0IHRlbnNvci1wcm9kdWN0IEJlcm5zdGVpbiBjb2VmZmljaWVudHMgb24geCBpbiBbeGEseGJdLCBlcHNpbG9uIGluIFswLEVQU0lMT05fTUFYXS4iIiIKICAgIHosIHcgPSBzLnN5bWJvbHMoInogdyIpCiAgICBwb2x5bm9taWFsID0gcy5Qb2x5KAogICAgICAgIHMuZXhwYW5kKGV4cHIuc3Vicyh7eDogeGEgKyAoeGIgLSB4YSkqeiwgZXBzaWxvbjogRVBTSUxPTl9NQVgqd30pKSwKICAgICAgICB6LAogICAgICAgIHcsCiAgICApCiAgICBueCA9IHBvbHlub21pYWwuZGVncmVlKHopCiAgICBudyA9IHBvbHlub21pYWwuZGVncmVlKHcpCiAgICBwb3dlciA9IHsKICAgICAgICAoaSwgaik6IHBvbHlub21pYWwuY29lZmZfbW9ub21pYWwoeioqaSp3KipqKQogICAgICAgIGZvciBpIGluIHJhbmdlKG54ICsgMSkKICAgICAgICBmb3IgaiBpbiByYW5nZShudyArIDEpCiAgICB9CiAgICBjb2VmZmljaWVudHM6IGxpc3Rbcy5FeHByXSA9IFtdCiAgICBmb3IgYSBpbiByYW5nZShueCArIDEpOgogICAgICAgIGZvciBiIGluIHJhbmdlKG53ICsgMSk6CiAgICAgICAgICAgIHZhbHVlID0gcy5SYXRpb25hbCgwKQogICAgICAgICAgICBmb3IgaSBpbiByYW5nZShhICsgMSk6CiAgICAgICAgICAgICAgICBmb3IgaiBpbiByYW5nZShiICsgMSk6CiAgICAgICAgICAgICAgICAgICAgdmFsdWUgKz0gKAogICAgICAgICAgICAgICAgICAgICAgICBwb3dlcltpLCBqXQogICAgICAgICAgICAgICAgICAgICAgICAqIHMuUmF0aW9uYWwoY29tYihhLCBpKSwgY29tYihueCwgaSkpCiAgICAgICAgICAgICAgICAgICAgICAgICogcy5SYXRpb25hbChjb21iKGIsIGopLCBjb21iKG53LCBqKSkKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIGNvZWZmaWNpZW50cy5hcHBlbmQocy5mYWN0b3IodmFsdWUpKQogICAgcmV0dXJuIGNvZWZmaWNpZW50cwoKCmRlZiBzdHJpY3RfYmVybnN0ZWluX3Bvc2l0aXZlKGV4cHI6IHMuRXhwciwgeGE6IHMuUmF0aW9uYWwsIHhiOiBzLlJhdGlvbmFsKSAtPiBzLkV4cHI6CiAgICBjb2VmZmljaWVudHMgPSBiZXJuc3RlaW5fY29lZmZpY2llbnRzXzJkKGV4cHIsIHhhLCB4YikKICAgIGFzc2VydCBjb2VmZmljaWVudHMKICAgIGFzc2VydCBhbGwodmFsdWUgPiAwIGZvciB2YWx1ZSBpbiBjb2VmZmljaWVudHMpCiAgICByZXR1cm4gbWluKGNvZWZmaWNpZW50cykKCgpkZWYgdGFpbF9jb2VmZmljaWVudF9wb3NpdGl2ZShleHByOiBzLkV4cHIsIHgwOiBzLlJhdGlvbmFsKSAtPiBzLkV4cHI6CiAgICAiIiJQcm92ZSBwb3NpdGl2aXR5IGZvciB4PXgwK3QsIHQ+PTAsIGVwc2lsb24gaW4gWzAsRVBTSUxPTl9NQVhdLiIiIgogICAgdyA9IHMuc3ltYm9scygidyIpCiAgICBwb2x5bm9taWFsID0gcy5Qb2x5KHMuZXhwYW5kKGV4cHIuc3Vicyh4LCB4MCArIHQpKSwgdCwgZXBzaWxvbikKICAgIHRfZGVncmVlID0gcG9seW5vbWlhbC5kZWdyZWUodCkKICAgIGVwc2lsb25fZGVncmVlID0gcG9seW5vbWlhbC5kZWdyZWUoZXBzaWxvbikKICAgIGNvZWZmaWNpZW50czogbGlzdFtzLkV4cHJdID0gW10KICAgIGZvciBpIGluIHJhbmdlKHRfZGVncmVlICsgMSk6CiAgICAgICAgZXBzaWxvbl9jb2VmZmljaWVudCA9IHMuUG9seShwb2x5bm9taWFsLmNvZWZmX21vbm9taWFsKHQqKmkpLCBlcHNpbG9uKQogICAgICAgIHVuaXQgPSBzLlBvbHkoCiAgICAgICAgICAgIHMuZXhwYW5kKGVwc2lsb25fY29lZmZpY2llbnQuYXNfZXhwcigpLnN1YnMoZXBzaWxvbiwgRVBTSUxPTl9NQVgqdykpLAogICAgICAgICAgICB3LAogICAgICAgICkKICAgICAgICBwb3dlciA9IFt1bml0LmNvZWZmX21vbm9taWFsKHcqKmopIGZvciBqIGluIHJhbmdlKGVwc2lsb25fZGVncmVlICsgMSldCiAgICAgICAgZm9yIGIgaW4gcmFuZ2UoZXBzaWxvbl9kZWdyZWUgKyAxKToKICAgICAgICAgICAgdmFsdWUgPSBzdW0oCiAgICAgICAgICAgICAgICBwb3dlcltqXSpzLlJhdGlvbmFsKGNvbWIoYiwgaiksIGNvbWIoZXBzaWxvbl9kZWdyZWUsIGopKQogICAgICAgICAgICAgICAgZm9yIGogaW4gcmFuZ2UoYiArIDEpCiAgICAgICAgICAgICkKICAgICAgICAgICAgdmFsdWUgPSBzLmZhY3Rvcih2YWx1ZSkKICAgICAgICAgICAgYXNzZXJ0IHZhbHVlID4gMCwgKGksIGIsIHZhbHVlKQogICAgICAgICAgICBjb2VmZmljaWVudHMuYXBwZW5kKHZhbHVlKQogICAgcmV0dXJuIG1pbihjb2VmZmljaWVudHMpCgoKIyBxX3ggbnVtZXJhdG9yIGFuZCBkZW5vbWluYXRvciwgZnVsbHkgY2FuY2VsbGVkLgpRWCA9IHMuY2FuY2VsKHMuZGlmZihRLCB4KSkKUVhYID0gcy5jYW5jZWwocy5kaWZmKFEsIHgsIDIpKQpRWF9OVU0sIFFYX0RFTiA9IHMuZnJhY3Rpb24oUVgpClFYWF9OVU0sIFFYWF9ERU4gPSBzLmZyYWN0aW9uKFFYWCkKZXhwZWN0ZWRfcXhfZGVuID0gMzYqKHggKyAyKSoqNSooKHggKyAyKSoqNiArIDMyKmVwc2lsb24qeCkqKjIKYXNzZXJ0IHMuZmFjdG9yKHMuY2FuY2VsKFFYX0RFTi9leHBlY3RlZF9xeF9kZW4pKSA9PSAxCmV4cGVjdGVkX3F4eF9kZW4gPSA5Kih4ICsgMikqKjYqKCh4ICsgMikqKjYgKyAzMiplcHNpbG9uKngpKiozCmFzc2VydCBzLmZhY3RvcihzLmNhbmNlbChRWFhfREVOL2V4cGVjdGVkX3F4eF9kZW4pKSA9PSAxCgpRWF9LID0gcy5leHBhbmQoUVhfTlVNLnN1YnMoTHMsIDYgKyBrKSkKUVhfQkFTRSA9IHMuUG9seShRWF9LLCBrKS5jb2VmZl9tb25vbWlhbCgxKQpRWF9TTE9QRSA9IHMuUG9seShRWF9LLCBrKS5jb2VmZl9tb25vbWlhbChrKQphc3NlcnQgcy5leHBhbmQoUVhfSyAtIFFYX0JBU0UgLSBrKlFYX1NMT1BFKSA9PSAwCgpRWFhfSyA9IHMuZXhwYW5kKFFYWF9OVU0uc3VicyhMcywgNiArIGspKQpRWFhfQkFTRSA9IHMuUG9seShRWFhfSywgaykuY29lZmZfbW9ub21pYWwoMSkKUVhYX1NMT1BFID0gcy5Qb2x5KFFYWF9LLCBrKS5jb2VmZl9tb25vbWlhbChrKQphc3NlcnQgcy5leHBhbmQoUVhYX0sgLSBRWFhfQkFTRSAtIGsqUVhYX1NMT1BFKSA9PSAwCgojIFJlZ2lvbiBJOiBxX3g+MCBmcm9tIHRoZSBob3Jpem9uIHRocm91Z2ggeD05OS8xMDAuCkxFRlRfQkFTRV9NSU4gPSBzdHJpY3RfYmVybnN0ZWluX3Bvc2l0aXZlKFFYX0JBU0UsIHMuUmF0aW9uYWwoMCksIFhfTEVGVCkKTEVGVF9TTE9QRV9NSU4gPSBzdHJpY3RfYmVybnN0ZWluX3Bvc2l0aXZlKFFYX1NMT1BFLCBzLlJhdGlvbmFsKDApLCBYX0xFRlQpCgojIFJlZ2lvbiBJSTogcV94eDwwIG9uIHRoZSBlbnRpcmUgdHJhcHBpbmcgYm94LgpNSURETEVfQkFTRV9NSU4gPSBzdHJpY3RfYmVybnN0ZWluX3Bvc2l0aXZlKC1RWFhfQkFTRSwgWF9MRUZULCBYX1JJR0hUKQpNSURETEVfU0xPUEVfTUlOID0gc3RyaWN0X2Jlcm5zdGVpbl9wb3NpdGl2ZSgtUVhYX1NMT1BFLCBYX0xFRlQsIFhfUklHSFQpCgojIFJlZ2lvbiBJSUk6IHFfeDwwIGZvciBhbGwgeD49NC8zLgpSSUdIVF9CQVNFX01JTiA9IHRhaWxfY29lZmZpY2llbnRfcG9zaXRpdmUoLVFYX0JBU0UsIFhfUklHSFQpClJJR0hUX1NMT1BFX01JTiA9IHRhaWxfY29lZmZpY2llbnRfcG9zaXRpdmUoLVFYX1NMT1BFLCBYX1JJR0hUKQoKIyBUaGUgcHJpbmNpcGFsIGZhY3RvciBpcyB1bmlmb3JtbHkgcG9zaXRpdmUgb24gdGhlIHRyYXBwaW5nIGJveDsgUD4xLzQuClBfUVVBUlRFUl9OVU0sIFBfUVVBUlRFUl9ERU4gPSBzLmZyYWN0aW9uKHMuY2FuY2VsKFAgLSBzLlJhdGlvbmFsKDEsIDQpKSkKZXhwZWN0ZWRfcF9xdWFydGVyX2RlbiA9IDM2Kih4ICsgMikqKjcKYXNzZXJ0IHMuZmFjdG9yKHMuY2FuY2VsKFBfUVVBUlRFUl9ERU4vZXhwZWN0ZWRfcF9xdWFydGVyX2RlbikpID09IDEKUF9RVUFSVEVSX01JTiA9IHN0cmljdF9iZXJuc3RlaW5fcG9zaXRpdmUoUF9RVUFSVEVSX05VTSwgWF9MRUZULCBYX1JJR0hUKQoKIyBRdWFudGl0YXRpdmUgbm9uZGVnZW5lcmFjeS4gIE9uIHRoZSB0cmFwcGluZyBib3gsIC1RX3h4ID49IEwvMTAwMC4KUVhYX0RFTl9NQVggPSBzLmZhY3RvcigKICAgIDkqKFhfUklHSFQgKyAyKSoqNiooKFhfUklHSFQgKyAyKSoqNiArIDMyKkVQU0lMT05fTUFYKlhfUklHSFQpKiozCikKQ1VSVkFUVVJFX05VTV9QRVJfTCA9IG1pbihNSURETEVfQkFTRV9NSU4vcy5JbnRlZ2VyKDYpLCBNSURETEVfU0xPUEVfTUlOKQpDVVJWQVRVUkVfWF9MT1dFUiA9IHMuZmFjdG9yKENVUlZBVFVSRV9OVU1fUEVSX0wvUVhYX0RFTl9NQVgpCmFzc2VydCBDVVJWQVRVUkVfWF9MT1dFUiA+IHMuUmF0aW9uYWwoMSwgMTAwMCkKIyBBdCB0aGUgY3JpdGljYWwgcG9pbnQsIFFfeXk9UF4yIFFfeHggYmVjYXVzZSBRX3g9MC4KQ1VSVkFUVVJFX1lfTE9XRVIgPSBzLlJhdGlvbmFsKDEsIDE2KSpzLlJhdGlvbmFsKDEsIDEwMDApCgpyZWNvcmQgPSB7CiAgICAiZG9tYWluIjogewogICAgICAgICJ4IjogIng+PTAiLAogICAgICAgICJMIjogIkw9ZWxsKihlbGwrMSk+PTYiLAogICAgICAgICJlcHNpbG9uIjogIjA8PWVwc2lsb248PTEvMTAwMDAiLAogICAgfSwKICAgICJjcml0aWNhbF9wb2ludF9icmFja2V0IjogW3N0cihYX0xFRlQpLCBzdHIoWF9SSUdIVCldLAogICAgInNpZ25fY2VydGlmaWNhdGUiOiB7CiAgICAgICAgIlFfeF9wb3NpdGl2ZV9sZWZ0IjogVHJ1ZSwKICAgICAgICAiUV94eF9uZWdhdGl2ZV90cmFwcGluZ19ib3giOiBUcnVlLAogICAgICAgICJRX3hfbmVnYXRpdmVfcmlnaHQiOiBUcnVlLAogICAgfSwKICAgICJub25kZWdlbmVyYWN5IjogewogICAgICAgICJtaW51c19RX3h4X292ZXJfTF9sb3dlciI6ICIxLzEwMDAiLAogICAgICAgICJQX2xvd2VyX29uX2JveCI6ICIxLzQiLAogICAgICAgICJtaW51c19RX3l5X292ZXJfTF9sb3dlcl9hdF9jcml0aWNhbF9wb2ludCI6IHN0cihDVVJWQVRVUkVfWV9MT1dFUiksCiAgICB9LAogICAgIm1vcmF3ZXR6X211bHRpcGxpZXIiOiB7CiAgICAgICAgImxpb3V2aWxsZV9jb29yZGluYXRlIjogImRzL2R5PXNxcnQoVykiLAogICAgICAgICJjZW50ZXIiOiAic18qPXMoeF8qKSIsCiAgICAgICAgImEiOiAiYShzKT10YW5oKGdhbW1hKihzLXNfKikpIiwKICAgICAgICAib3BlcmF0b3IiOiAiQV9oPShhKmgqRF9zK2gqRF9zKmEpLzIiLAogICAgICAgICJzaWduIjogIi1hKmRfcyhVL1cpPj0wLCBlcXVhbGl0eSBvbmx5IGF0IHM9c18qIGFuZCBhdCBhc3ltcHRvdGljIGVuZHMiLAogICAgfSwKICAgICJyZXNvbHZlbnRfYm91bmRhcnkiOiB7CiAgICAgICAgImxvd19mcmVxdWVuY3lfd2VpZ2h0IjogInNpZ21hPjMvMiIsCiAgICAgICAgImhpZ2hfTF9zZW1pY2xhc3NpY2FsX3BhcmFtZXRlciI6ICJoPUxeKC0xLzIpIiwKICAgICAgICAiYmFycmllcl90b3BfY3V0b2ZmX2JvdW5kIjogInx8Y2hpKEhfTC0ob21lZ2EraTApXjIpXigtMSljaGl8fCA8PSBDKmxvZygyK0wpKkxeKC0xLzIpIiwKICAgICAgICAiTF9sb3NzIjogIm9uZSBsb2dhcml0aG0gcmVsYXRpdmUgdG8gdGhlIG9uZS1kaW1lbnNpb25hbCBub250cmFwcGluZyBzY2FsZSIsCiAgICB9LAp9CnJlY29yZFsiaGFzaCJdID0gaGFzaGxpYi5zaGEyNTYoCiAgICBqc29uLmR1bXBzKHJlY29yZCwgc29ydF9rZXlzPVRydWUsIHNlcGFyYXRvcnM9KCIsIiwgIjoiKSkuZW5jb2RlKCJ1dGYtOCIpCikuaGV4ZGlnZXN0KCkKCnByaW50KCJHRkVfQVhJQUxfU1lNQk9MSUNfRUxMX01PUkFXRVRaIikKcHJpbnQoIkRPTUFJTiA6PSB4Pj0wOyBMPj02OyAwPD1lcHNpbG9uPD0xLzEwMDAwIikKcHJpbnQoIkNSSVRJQ0FMX1BPSU5UX0JSQUNLRVQgOj0gOTkvMTAwIDwgeF8qIDwgNC8zIikKcHJpbnQoIlJFU1VMVCA6PSBVX2VsbC9XX2VsbCBoYXMgZXhhY3RseSBvbmUgZXh0ZXJpb3IgY3JpdGljYWwgcG9pbnQiKQpwcmludCgiUkVTVUxUIDo9IHRoZSBjcml0aWNhbCBwb2ludCBpcyBhIHN0cmljdCBub25kZWdlbmVyYXRlIGdsb2JhbCBtYXhpbXVtIikKcHJpbnQoIkNVUlZBVFVSRV9YX0JPVU5EIDo9IC1kX3heMihVX2VsbC9XX2VsbCkoeF8qKSA+IEwvMTAwMCIpCnByaW50KCJDVVJWQVRVUkVfWV9CT1VORCA6PSAtZF95XjIoVV9lbGwvV19lbGwpKHlfKikgPiBMLzE2MDAwIikKcHJpbnQoIk1PUkFXRVRaX01VTFRJUExJRVIgOj0gYShzKT10YW5oKGdhbW1hKihzLXNfKikpOyBBX2g9KGEqaCpEX3MraCpEX3MqYSkvMiIpCnByaW50KCJMT1dfRlJFUVVFTkNZX0xBUF9XRUlHSFQgOj0gc2lnbWE+My8yIikKcHJpbnQoIkhJR0hfTF9DVVRPRkZfUkVTT0xWRU5UIDo9IEMqbG9nKDIrTCkqTF4oLTEvMik7IExfTE9TUyA6PSBsb2dhcml0aG1pYyIpCnByaW50KCJDRVJUSUZJQ0FURV9IQVNIIDo9ICIgKyByZWNvcmRbImhhc2giXSkK"),
        "gfe_axial_morawetz_verifier.py",
        "exec",
    ),
    _AXIAL_SYMBOLIC_ELL_MORAWETZ_NS,
)
AXIAL_SYMBOLIC_ELL_MORAWETZ_PAYLOAD = (
    _AXIAL_SYMBOLIC_ELL_MORAWETZ_NS["record"]
)
AXIAL_SYMBOLIC_ELL_MORAWETZ_HASH = (
    AXIAL_SYMBOLIC_ELL_MORAWETZ_PAYLOAD["hash"]
)
assert AXIAL_SYMBOLIC_ELL_MORAWETZ_HASH == (
    "4b3687b358215687ed3a6f5c0eb4496abd4f9c598c02d9d4b6d14826aa8248d4"
)

# Fixed-mode interpolation receipts. These hashes were generated by direct
# coordinate expansion of the cubic invariant for l=2,...,6.
for l_value, expected in EXPECTED_FIXED_MODE_HASHES.items():
    actual = canonical_hash(fixed_mode_coefficients(l_value))
    assert actual == expected, (l_value, actual, expected)

report = {
    "scope": "curvature-truncated covariant metric-only GfE Hessian through relative O(beta^2)",
    "domain": "M>0, r>2M, ell>=2",
    "definitions": {
        "L": "ell*(ell+1)",
        "lambda": "L-2",
        "f": "1-2*M/r",
        "k0": "h0-dot(h2)/2",
        "k1": "h1-h2'/2+h2/r",
        "Q": "dot(k1)-k0'+2*k0/r",
        "A0": "Q'+2Q/r+lambda*k0/(f*r^2)",
        "A1": "-dot(Q)-lambda*f*k1/r^2",
        "A2": "(f*k1)'-dot(k0)/f",
    },
    "lagrangian": {
        "Einstein": s.sstr(L_EH),
        "Ricci_squared": s.sstr(L_RICCI2),
        "relative_O_beta": "(5*beta/6)*Ricci_squared",
        "relative_O_beta2": "GaugeComplete[D_k Einstein RW + J_RW/9]",
        "D_k_Einstein_RW": s.sstr(L_DK_EH_RW),
        "J_RW_coefficients": {k: s.sstr(v) for k, v in sorted(J_COEFFICIENTS.items())},
    },
    "checks": {
        "gauge_invariant_k0": True,
        "gauge_invariant_k1": True,
        "Einstein_Noether_identity": True,
        "general_Noether_identity_by_chain_rule": True,
        "beta_zero_GR_reduction": True,
        "leading_massless_h0_elimination": "h0=(i*f/omega)*d_r(f*h1)",
        "leading_massless_master": "Psi_minus=f*h1/r",
        "leading_massless_RW_reduction": True,
        "ell2_beta2_constraint_source": True,
        "ell2_beta2_h0_map": "H0_220_BETA2=-f*r^2/4*(Q2_220_prime+2*Q2_220/r+S0_220/6)",
        "ell2_beta2_master_source_hash": RW2_220_HASH,
        "ell2_beta2_master_source_max_radial_order": int(RW2_220_MAX_RADIAL_ORDER),
        "ell2_beta2_structural_order_reduction": True,
        "ell2_beta2_reduced_max_radial_order": int(RW2_220_REDUCED_MAX_RADIAL_ORDER),
        "ell2_beta2_order_reduced_raw_hash": RW2_220_ORDER_REDUCED_RAW_HASH,
        "ell2_beta2_normalized_coefficients": True,
        "ell2_beta2_normalized_coefficient_hash": RW2_220_NORMALIZED_COEFFICIENT_HASH,
        "ell2_beta2_master_redefinition": s.sstr(MASTER_REDEF_220),
        "ell2_beta2_nf_correction": s.sstr(NF_220_BETA2),
        "ell2_beta2_canonical_potential": s.sstr(DELTA_V_MINUS_220),
        "ell2_beta2_canonical_potential_hash": DELTA_V_MINUS_220_HASH,
        "ell2_beta2_canonical_operator_identity": True,
        "ell2_axial_shifted_horizon": "z_h=2-5*epsilon/72",
        "ell2_axial_horizon_P1": s.sstr(P1_hor),
        "ell2_axial_ingoing_exponent": s.sstr(alpha_ingoing_hor),
        "ell2_axial_frobenius_recurrence": "I_n*a_n + lower_A + lower_B + lower_C = 0",
        "ell2_axial_frobenius_denominator": s.sstr(recurrence_denominator_hor),
        "ell2_axial_frobenius_order": FROBENIUS_ORDER_220,
        "ell2_axial_frobenius_coefficients": [s.sstr(value) for value in a_hor],
        "ell2_axial_frobenius_hash": HORIZON_FROBENIUS_220_HASH,
        "ell2_axial_horizon_majorant": True,
        "ell2_axial_horizon_omega_box": {key: str(value) for key, value in OMEGA_HORIZON_BOX_220.items()},
        "ell2_axial_horizon_epsilon_interval": [str(value) for value in EPSILON_HORIZON_INTERVAL_220],
        "ell2_axial_horizon_majorant_radius": str(MAJORANT_RADIUS_220),
        "ell2_axial_horizon_launch_radius": str(LAUNCH_RADIUS_220),
        "ell2_axial_horizon_majorant_start": MAJORANT_START_220,
        "ell2_axial_horizon_truncation": FROBENIUS_TRUNCATION_220,
        "ell2_axial_horizon_majorant_q": str(HORIZON_MAJORANT_Q_220),
        "ell2_axial_horizon_series_tail": str(HORIZON_SERIES_TAIL_220),
        "ell2_axial_horizon_derivative_tail": str(HORIZON_SERIES_DERIVATIVE_TAIL_220),
        "ell2_axial_horizon_majorant_hash": HORIZON_MAJORANT_220_HASH,
        "ell2_axial_horizon_endpoint_pair": True,
        "ell2_axial_horizon_endpoint_launch_radius": str(LAUNCH_RADIUS_220),
        "ell2_axial_horizon_endpoint_regular_value": _exact_disk_record(HORIZON_ENDPOINT_VALUE_220),
        "ell2_axial_horizon_endpoint_regular_derivative": _exact_disk_record(HORIZON_ENDPOINT_DERIVATIVE_220),
        "ell2_axial_horizon_endpoint_value_nonzero_lower": str(HORIZON_ENDPOINT_VALUE_NONZERO_LOWER_220),
        "ell2_axial_horizon_endpoint_hash": HORIZON_ENDPOINT_220_HASH,
        "ell2_axial_horizon_affine_endpoint": True,
        "ell2_axial_horizon_affine_variables": HORIZON_AFFINE_ENDPOINT_220_PAYLOAD["variables"],
        "ell2_axial_horizon_affine_truncation": AFFINE_FROBENIUS_TRUNCATION_220,
        "ell2_axial_horizon_affine_series_tail": str(AFFINE_HORIZON_SERIES_TAIL_220),
        "ell2_axial_horizon_affine_derivative_tail": str(AFFINE_HORIZON_DERIVATIVE_TAIL_220),
        "ell2_axial_horizon_affine_dyadic_bits": AFFINE_ENDPOINT_DYADIC_BITS_220,
        "ell2_axial_horizon_affine_value": HORIZON_AFFINE_VALUE_RECORD_220,
        "ell2_axial_horizon_affine_derivative": HORIZON_AFFINE_DERIVATIVE_RECORD_220,
        "ell2_axial_horizon_affine_hash": HORIZON_AFFINE_ENDPOINT_220_HASH,
        "ell2_axial_horizon_riccati_propagation": True,
        "ell2_axial_horizon_riccati_payload": HORIZON_RICCATI_PROPAGATION_220_PAYLOAD,
        "ell2_axial_horizon_riccati_radius": str(HORIZON_RICCATI_RADIUS_220),
        "ell2_axial_infinity_jost_endpoint": True,
        "ell2_axial_infinity_jost_payload": INFINITY_JOST_ENDPOINT_220_PAYLOAD,
        "ell2_axial_infinity_jost_radius": str(INFINITY_JOST_ENDPOINT_220_RADIUS),
        "ell2_axial_infinity_riccati_propagation": True,
        "ell2_axial_infinity_riccati_payload": INFINITY_RICCATI_PROPAGATION_220_PAYLOAD,
        "ell2_axial_infinity_riccati_radius": str(INFINITY_RICCATI_RADIUS_220),
        "ell2_axial_matching_interval_newton": True,
        "ell2_axial_matching_interval_newton_payload": AXIAL_MATCHING_INTERVAL_NEWTON_220_PAYLOAD,
        "ell2_axial_epsilon0_tangent_system": True,
        "ell2_axial_epsilon0_tangent_payload": AXIAL_EPSILON0_TANGENT_SYSTEM_220_PAYLOAD,
        "ell2_axial_epsilon0_tangent_hash": AXIAL_EPSILON0_TANGENT_SYSTEM_220_HASH,
        "ell2_axial_epsilon0_endpoint_tangents": True,
        "ell2_axial_epsilon0_endpoint_tangent_payload": AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_PAYLOAD,
        "ell2_axial_epsilon0_center_q_refinement_payload": AXIAL_EPSILON0_CENTER_Q_REFINEMENT_220_PAYLOAD,
        "ell2_axial_epsilon0_tangent_propagation": True,
        "ell2_axial_epsilon0_tangent_propagation_payload": AXIAL_EPSILON0_TANGENT_PROPAGATION_220_PAYLOAD,
        "ell2_axial_epsilon0_tangent_propagation_hash": AXIAL_EPSILON0_TANGENT_PROPAGATION_220_HASH,
        "ell2_axial_epsilon0_endpoint_tangent_hash": AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_HASH,
        "J_fixed_mode_hashes": EXPECTED_FIXED_MODE_HASHES,
        "symbolic_ell_unique_trapping_maximum": True,
        "symbolic_ell_morawetz_payload": AXIAL_SYMBOLIC_ELL_MORAWETZ_PAYLOAD,
        "symbolic_ell_morawetz_hash": AXIAL_SYMBOLIC_ELL_MORAWETZ_HASH,
        "J_coefficient_count": len(J_COEFFICIENTS),
    },
}

outdir = Path(os.environ.get("GFE_OUTPUT_ROOT", Path.home() / "Downloads" / "gfe_primary_source_packet"))
outdir.mkdir(parents=True, exist_ok=True)
json_path = outdir / "gfe_axial_quadratic_action.json"
txt_path = outdir / "gfe_axial_quadratic_action.txt"
json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

lines = [
    "GFE_AXIAL_QUADRATIC_ACTION",
    "SCOPE := curvature-truncated covariant metric-only Hessian through relative O(beta^2)",
    "DOMAIN := M > 0; r > 2M; ell >= 2",
    "J_COEFFICIENT_COUNT := 28",
    "J_SYMBOLIC_L_INTERPOLATION := certified against ell=2,3,4,5,6",
    "AXIAL_GAUGE_IDENTITY := certified coefficient-by-coefficient",
    "BETA_ZERO_GR_REDUCTION := certified",
    "LEADING_MASSLESS_H0_ELIMINATION := certified",
    "LEADING_MASSLESS_RW_OPERATOR := certified",
    "ELL2_BETA2_H0_SOURCE_MAP := certified",
    f"ELL2_BETA2_MASTER_SOURCE_HASH := {RW2_220_HASH}",
    f"ELL2_BETA2_MASTER_SOURCE_MAX_RADIAL_ORDER := {RW2_220_MAX_RADIAL_ORDER}",
    "ELL2_BETA2_STRUCTURAL_ORDER_REDUCTION := certified",
    f"ELL2_BETA2_REDUCED_MAX_RADIAL_ORDER := {RW2_220_REDUCED_MAX_RADIAL_ORDER}",
    f"ELL2_BETA2_ORDER_REDUCED_RAW_HASH := {RW2_220_ORDER_REDUCED_RAW_HASH}",
    "ELL2_BETA2_NORMALIZED_COEFFICIENTS := certified",
    f"ELL2_BETA2_NORMALIZED_COEFFICIENT_HASH := {RW2_220_NORMALIZED_COEFFICIENT_HASH}",
    "ELL2_BETA2_CANONICAL_POTENTIAL := certified",
    f"ELL2_BETA2_CANONICAL_POTENTIAL_HASH := {DELTA_V_MINUS_220_HASH}",
    "ELL2_AXIAL_INGOING_FROBENIUS := certified",
    "ELL2_AXIAL_SHIFTED_HORIZON := z_h=2-5*epsilon/72",
    f"ELL2_AXIAL_INGOING_EXPONENT := {s.sstr(alpha_ingoing_hor)}",
    f"ELL2_AXIAL_FROBENIUS_DENOMINATOR := {s.sstr(recurrence_denominator_hor)}",
    f"ELL2_AXIAL_FROBENIUS_ORDER := {FROBENIUS_ORDER_220}",
    f"ELL2_AXIAL_FROBENIUS_HASH := {HORIZON_FROBENIUS_220_HASH}",
    "ELL2_AXIAL_HORIZON_MAJORANT := certified",
    "ELL2_AXIAL_HORIZON_OMEGA_BOX := Re[0.3736,0.3738]; Im[-0.0891,-0.0888]",
    "ELL2_AXIAL_HORIZON_EPSILON_INTERVAL := [0,1/10000]",
    f"ELL2_AXIAL_HORIZON_MAJORANT_Q := {HORIZON_MAJORANT_Q_220}",
    f"ELL2_AXIAL_HORIZON_SERIES_TAIL := {HORIZON_SERIES_TAIL_220}",
    f"ELL2_AXIAL_HORIZON_DERIVATIVE_TAIL := {HORIZON_SERIES_DERIVATIVE_TAIL_220}",
    f"ELL2_AXIAL_HORIZON_MAJORANT_HASH := {HORIZON_MAJORANT_220_HASH}",
    "ELL2_AXIAL_HORIZON_ENDPOINT := certified",
    "ELL2_AXIAL_HORIZON_ENDPOINT_LAUNCH_RADIUS := 1/16",
    f"ELL2_AXIAL_HORIZON_ENDPOINT_VALUE_NONZERO_LOWER := {HORIZON_ENDPOINT_VALUE_NONZERO_LOWER_220}",
    f"ELL2_AXIAL_HORIZON_ENDPOINT_HASH := {HORIZON_ENDPOINT_220_HASH}",
    "ELL2_AXIAL_HORIZON_AFFINE_ENDPOINT := certified",
    "ELL2_AXIAL_HORIZON_AFFINE_VARIABLES := xi_ReOmega,xi_ImOmega,xi_epsilon",
    "ELL2_AXIAL_HORIZON_AFFINE_TRUNCATION := 32",
    "ELL2_AXIAL_HORIZON_AFFINE_SERIES_TAIL := 1/4294967296",
    "ELL2_AXIAL_HORIZON_AFFINE_DERIVATIVE_TAIL := 17/134217728",
    "ELL2_AXIAL_HORIZON_AFFINE_DYADIC_BITS := 96",
    f"ELL2_AXIAL_HORIZON_AFFINE_HASH := {HORIZON_AFFINE_ENDPOINT_220_HASH}",
    "ELL2_AXIAL_HORIZON_RICCATI_PROPAGATION := certified",
    "ELL2_AXIAL_HORIZON_RICCATI_MATCHING_Z := 3",
    f"ELL2_AXIAL_HORIZON_RICCATI_STEPS := {HORIZON_RICCATI_PROPAGATION_220_PAYLOAD['steps']}",
    f"ELL2_AXIAL_HORIZON_RICCATI_CENTER_DYADIC := {HORIZON_RICCATI_PROPAGATION_220_PAYLOAD['log_derivative']['center']}",
    f"ELL2_AXIAL_HORIZON_RICCATI_RADIUS := {HORIZON_RICCATI_RADIUS_220}",
    f"ELL2_AXIAL_HORIZON_RICCATI_HASH := {HORIZON_RICCATI_PROPAGATION_220_PAYLOAD['hash']}",
    "ELL2_AXIAL_INFINITY_JOST_ENDPOINT := certified",
    "ELL2_AXIAL_INFINITY_JOST_CONTOUR := z=3+i*t; t>=32",
    "ELL2_AXIAL_INFINITY_JOST_TRUNCATION := 14",
    "ELL2_AXIAL_INFINITY_JOST_FIRST_RESIDUAL_POWER := 15",
    "ELL2_AXIAL_INFINITY_JOST_TAIL_RADIUS := 1/1000000000",
    f"ELL2_AXIAL_INFINITY_JOST_CENTER_DYADIC := {INFINITY_JOST_ENDPOINT_220_PAYLOAD['affine']['center']}",
    f"ELL2_AXIAL_INFINITY_JOST_RADIUS := {INFINITY_JOST_ENDPOINT_220_RADIUS}",
    f"ELL2_AXIAL_INFINITY_JOST_HASH := {INFINITY_JOST_ENDPOINT_220_PAYLOAD['hash']}",
    "ELL2_AXIAL_INFINITY_RICCATI_PROPAGATION := certified",
    "ELL2_AXIAL_INFINITY_RICCATI_MATCHING_Z := 3",
    f"ELL2_AXIAL_INFINITY_RICCATI_STEPS := {INFINITY_RICCATI_PROPAGATION_220_PAYLOAD['steps']}",
    f"ELL2_AXIAL_INFINITY_RICCATI_CENTER_DYADIC := {INFINITY_RICCATI_PROPAGATION_220_PAYLOAD['center']}",
    f"ELL2_AXIAL_INFINITY_RICCATI_RADIUS := {INFINITY_RICCATI_RADIUS_220}",
    f"ELL2_AXIAL_INFINITY_RICCATI_HASH := {INFINITY_RICCATI_PROPAGATION_220_PAYLOAD['hash']}",
    "ELL2_AXIAL_MATCHING_INTERVAL_NEWTON := certified",
    "ELL2_AXIAL_MATCHING_UNIQUE_SIMPLE_ROOT_TUBE := certified",
    "ELL2_AXIAL_MATCHING_EPSILON_INTERVAL := [0,1/10000]",
    "ELL2_AXIAL_MATCHING_NEWTON_DISK_RADIUS := 1/150000",
    "ELL2_AXIAL_MATCHING_HASH := " + AXIAL_MATCHING_INTERVAL_NEWTON_220_PAYLOAD["hash"],
    "ELL2_AXIAL_EPSILON0_RICCATI_TANGENT_SYSTEM := certified",
    "ELL2_AXIAL_EPSILON0_IMPLICIT_DERIVATIVE_FORMULA := certified",
    "ELL2_AXIAL_EPSILON0_TANGENT_HASH := " + AXIAL_EPSILON0_TANGENT_SYSTEM_220_HASH,
    "ELL2_AXIAL_EPSILON0_ENDPOINT_TANGENTS := certified",
    "ELL2_AXIAL_EPSILON0_HORIZON_ENDPOINT_TANGENTS := certified",
    "ELL2_AXIAL_EPSILON0_INFINITY_ENDPOINT_TANGENTS := certified",
    "ELL2_AXIAL_EPSILON0_ENDPOINT_TANGENT_HASH := " + AXIAL_EPSILON0_ENDPOINT_TANGENTS_220_HASH,
    "ELL2_AXIAL_EPSILON0_CENTER_Q_REFINEMENT := certified",
    "ELL2_AXIAL_EPSILON0_TANGENT_PROPAGATION := certified",
    "ELL2_AXIAL_EPSILON0_IMPLICIT_DERIVATIVE := certified",
    "ELL2_AXIAL_EPSILON0_TANGENT_PROPAGATION_HASH := " + AXIAL_EPSILON0_TANGENT_PROPAGATION_220_HASH,
    "SYMBOLIC_ELL_AXIAL_UNIQUE_TRAPPING_MAXIMUM := certified",
    "SYMBOLIC_ELL_AXIAL_MORAWETZ_MULTIPLIER := certified",
    "SYMBOLIC_ELL_AXIAL_LOW_FREQUENCY_LAP := analytic consequence; sigma>3/2",
    "SYMBOLIC_ELL_AXIAL_HIGH_L_RESOLVENT := analytic consequence; L^(-1/2)*log(2+L)",
    "SYMBOLIC_ELL_AXIAL_MORAWETZ_HASH := " + AXIAL_SYMBOLIC_ELL_MORAWETZ_HASH,
    "RW_GAUGE_IMPOSED_AFTER_GAUGE_COMPLETION := yes",
    "H0_ELIMINATED := no",
    f"JSON_REPORT := {json_path}",
    f"TEXT_REPORT := {txt_path}",
    "RESULT := odd-parity uneliminated quadratic action completed",
]
txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))

PY_CORE

"$python_bin" "$tmp_py"
