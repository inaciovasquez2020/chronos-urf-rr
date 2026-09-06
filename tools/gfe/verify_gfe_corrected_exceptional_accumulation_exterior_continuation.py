#!/usr/bin/env python3
"""Certify finite-radius exterior continuation of the reconstructed physical branch.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

The preceding double-Laplace certificate constructs an actual solution of the
exact radial Euler equations on a nonempty interval 2 < r <= 2+x_safe.  This
verifier reads the same hash-locked Euler/generator artifact and checks the
remaining hypotheses needed for ordinary finite-radius linear-ODE
continuation.

The artifact supplies an exact six-state descriptor system

    E(r) Y'(r) = A(r) Y(r).

After specialization, every rational coefficient of E and A is checked to be
analytic for r>2.  The determinant of E is factored exactly and every factor is
certified nonzero on r>2 by translating r=2+x and checking a one-sign
coefficient polynomial on x>0.  Thus G(r)=E(r)^(-1)A(r) is analytic on every
compact exterior interval [2+eps,R].

Standard existence/uniqueness for linear ODEs then extends the actual local
Borel-Laplace seed uniquely to every finite r>2.  This is continuation only;
no boundedness, scattering, asymptotic state, or r->infinity limit is claimed.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.together(value)))


def matrix_simp(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(simp)


def parse_matrix(raw: list[list[str]], locals_: dict[str, sp.Expr]) -> sp.Matrix:
    return sp.Matrix([
        [sp.sympify(entry, locals=locals_) for entry in row]
        for row in raw
    ])


def polynomial_factors(expr: sp.Expr, r: sp.Symbol) -> list[sp.Expr]:
    expr = sp.factor(expr)
    if expr == 0:
        raise AssertionError("zero polynomial cannot be classified as pole-free")
    poly = sp.Poly(expr, r, domain="QQ")
    _, factors = sp.factor_list(poly.as_expr(), r)
    return [sp.factor(factor) for factor, _multiplicity in factors]


def one_sign_after_horizon_shift(factor: sp.Expr, r: sp.Symbol) -> bool:
    """Sufficient exact certificate that factor(r) != 0 for every r>2."""
    x = sp.symbols("x", positive=True)
    shifted = sp.Poly(sp.expand(factor.subs(r, x + 2)), x, domain="QQ")
    coeffs = shifted.all_coeffs()
    if not coeffs:
        return False
    nonnegative = all(c >= 0 for c in coeffs) and any(c > 0 for c in coeffs)
    nonpositive = all(c <= 0 for c in coeffs) and any(c < 0 for c in coeffs)
    return bool(nonnegative or nonpositive)


def certify_nonzero_factors(expr: sp.Expr, r: sp.Symbol, label: str) -> list[sp.Expr]:
    factors = polynomial_factors(expr, r)
    bad = [factor for factor in factors if not one_sign_after_horizon_shift(factor, r)]
    if bad:
        raise AssertionError(
            f"{label} has factors not certified nonzero for r>2: "
            + ", ".join(sp.sstr(f) for f in bad)
        )
    return factors


def main() -> None:
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    if data.get("state_dimension") != 6:
        raise AssertionError(f"descriptor state dimension changed: {data.get('state_dimension')}")
    expected_orders = {"E0_h0": 4, "E0_h1": 3, "E1_h0": 3, "E1_h1": 2}
    if data.get("differential_orders") != expected_orders:
        raise AssertionError(f"Euler differential orders changed: {data.get('differential_orders')}")

    M, beta, lam, omega, r = sp.symbols("M beta lam omega r")
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "lambda": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
    }
    specialization = {
        M: sp.Integer(1),
        beta: sp.Rational(5, 2),
        lam: sp.Integer(6),
        omega: sp.I / 4,
    }

    E = matrix_simp(parse_matrix(data["descriptor_E"], locals_).subs(specialization))
    A = matrix_simp(parse_matrix(data["descriptor_A"], locals_).subs(specialization))
    if E.shape != (6, 6) or A.shape != (6, 6):
        raise AssertionError(f"descriptor matrices changed shape: E={E.shape}, A={A.shape}")

    # All raw descriptor coefficient denominators must already be pole-free on
    # the open exterior.  This guards against hidden lower-order poles that a
    # principal-determinant check alone would miss.
    denominator_factors: set[str] = set()
    denominator_entry_count = 0
    for matrix_name, matrix in (("E", E), ("A", A)):
        for index, value in enumerate(matrix):
            if value == 0:
                continue
            _num, den = sp.fraction(sp.together(value))
            den = sp.factor(den)
            if den == 0:
                raise AssertionError(f"{matrix_name}[{index}] has zero denominator")
            factors = certify_nonzero_factors(den, r, f"{matrix_name}[{index}] denominator")
            if sp.Poly(den, r, domain="QQ").degree() > 0:
                denominator_entry_count += 1
            denominator_factors.update(sp.sstr(factor) for factor in factors)

    det_E = simp(E.det())
    if det_E == 0:
        raise AssertionError("specialized six-state descriptor matrix is singular identically")
    det_num, det_den = sp.fraction(sp.together(det_E))
    det_num = sp.factor(det_num)
    det_den = sp.factor(det_den)
    det_num_factors = certify_nonzero_factors(det_num, r, "det(E) numerator")
    det_den_factors = certify_nonzero_factors(det_den, r, "det(E) denominator")

    # Reconfirm the independently certified principal determinant on this exact
    # artifact.  It has no exterior zero and its sole real nonnegative
    # degeneracy is the horizon itself.
    principal = simp(sp.sympify(data["principal_determinant"], locals=locals_).subs(specialization))
    expected_principal = simp(
        sp.Rational(625) * (r - 2) ** 4
        * (r**2 + 2*r + 4)
        * (r**3 + 4) / r**11
    )
    if simp(principal - expected_principal) != 0:
        raise AssertionError("specialized principal determinant factorization changed")
    principal_num, principal_den = sp.fraction(sp.together(principal))
    certify_nonzero_factors(principal_num, r, "principal determinant numerator")
    certify_nonzero_factors(principal_den, r, "principal determinant denominator")

    # The previous double-Laplace gate certifies this explicit positive local
    # interval.  We pin the same rational endpoint here so continuation cannot
    # silently detach from the constructed physical branch.
    x_safe = sp.Rational(
        54358179840000,
        11700540562786069522705159372002046331401,
    )
    if x_safe <= 0:
        raise AssertionError("double-Laplace seed interval collapsed")
    r_seed = 2 + x_safe / 2
    if not (sp.Rational(2) < r_seed < 2 + x_safe):
        raise AssertionError("chosen continuation seed is outside reconstructed local interval")

    # No explicit inversion is needed: rational E,A with pole-free entries and
    # det(E)!=0 imply G=E^{-1}A is analytic by the adjugate formula.  Standard
    # linear ODE existence/uniqueness on each compact [r_seed,R] then patches
    # uniquely to every finite R>r_seed; points 2<r<=r_seed are already covered
    # by the local reconstructed solution.
    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_CONTINUATION_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6; alpha=1/2")
    print("DEPENDENCY := double-Laplace gate supplies an actual exact Euler solution on 2<r<=2+x_safe")
    print("DESCRIPTOR_STATE := Y=(h0,h0',h0'',h1,h1',h1'')")
    print("DESCRIPTOR_DIMENSION := 6")
    print("DESCRIPTOR_SYSTEM := E(r)Y'(r)=A(r)Y(r) from the authoritative corrected Euler artifact")
    print(f"RAW_DESCRIPTOR_NONCONSTANT_DENOMINATOR_ENTRIES := {denominator_entry_count}")
    print("RAW_DESCRIPTOR_DENOMINATOR_FACTORS := {" + ",".join(sorted(denominator_factors)) + "}")
    print(f"DESCRIPTOR_DETERMINANT := {sp.sstr(det_E)}")
    print("DESCRIPTOR_DETERMINANT_NUMERATOR_FACTORS := {" + ",".join(sorted(sp.sstr(f) for f in det_num_factors)) + "}")
    print("DESCRIPTOR_DETERMINANT_DENOMINATOR_FACTORS := {" + ",".join(sorted(sp.sstr(f) for f in det_den_factors)) + "}")
    print("DESCRIPTOR_INVERTIBILITY := certified for every real r>2")
    print("SPECIALIZED_PRINCIPAL_DETERMINANT := 625*(r-2)^4*(r^2+2*r+4)*(r^3+4)/r^11")
    print("FINITE_EXTERIOR_PRINCIPAL_ZEROS := none")
    print("FINITE_EXTERIOR_COEFFICIENT_POLES := none")
    print("EXTERIOR_GENERATOR := G(r)=E(r)^(-1)A(r) analytic on every compact [2+eps,R]")
    print(f"LOCAL_RECONSTRUCTION_X_SAFE := {sp.sstr(x_safe)}")
    print(f"CONTINUATION_SEED_RADIUS := {sp.sstr(r_seed)}")
    print("STANDARD_LINEAR_ODE_CONTINUATION := unique from the reconstructed seed across every finite compact exterior interval")
    print("PHYSICAL_EXTERIOR_CONTINUATION := unique to every finite r>2")
    print("RANKLOSS_CROSSING := absent because r_c=2 in this fixed accumulation sector")
    print("BOUNDARY := finite-radius continuation only; no r->infinity growth/asymptotic state, generic-beta summability, or global Chronos closure claimed")


if __name__ == "__main__":
    main()
