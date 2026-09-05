#!/usr/bin/env python3
"""Certify the exact infinity Newton data of the reduced Borel Ore operator.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6, alpha=1/2.

Dependencies already certified earlier in CI:

* the exact reduced two-row Borel Ore operator has row theta-orders [22,21];
* every reduced-row theta coefficient is polynomial in z;
* the physical Borel germ continues along the positive real ray.

For large-z asymptotics we first expose only the algebraic characteristic data.
Replace the noncommuting Euler operator theta by a commuting indeterminate eta in
the already-normal-ordered reduced rows and form

    Delta_inf(z,eta) = det M(z,eta).

This verifier computes the exact monomial support, the upper Newton polygon in
(theta-degree,z-degree) coordinates, and the characteristic polynomial attached
to every upper edge.  If an edge has slope s, a formal WKB balance eta~c*z^rho
has rho=-s.  This is an algebraic infinity-symbol certificate only: it does not
claim existence of WKB solutions, select the physical branch, or prove any
solution-growth/Laplace estimate.
"""
from __future__ import annotations

from fractions import Fraction
import sympy as sp

import verify_gfe_corrected_exceptional_accumulation_borel_reduced_denominators as rd
import verify_gfe_corrected_exceptional_accumulation_borel_row_reduction as rr


def upper_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Upper convex hull for unique integer (x,y) points ordered by x."""
    by_x: dict[int, int] = {}
    for x, y in points:
        by_x[x] = max(y, by_x.get(x, y))
    pts = sorted(by_x.items())
    hull: list[tuple[int, int]] = []
    for p in pts:
        while len(hull) >= 2:
            a, b = hull[-2], hull[-1]
            cross = (b[0] - a[0]) * (p[1] - b[1]) - (b[1] - a[1]) * (p[0] - b[0])
            # For the upper hull from left to right, remove non-clockwise turns.
            if cross >= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def edge_characteristic(
    poly: sp.Poly,
    eta: sp.Symbol,
    z: sp.Symbol,
    a: tuple[int, int],
    b: tuple[int, int],
) -> tuple[sp.Rational, sp.Expr]:
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    if dx <= 0:
        raise AssertionError("Newton edge must increase eta-degree")
    rho = -sp.Rational(dy, dx)
    c = sp.symbols("c")
    weight = sp.Rational(a[1]) + rho * a[0]
    out = sp.Integer(0)
    for (k, j), coeff in poly.terms():
        if sp.Rational(j) + rho * k == weight:
            out += coeff * c**k
    out = sp.factor(out)
    if out == 0:
        raise AssertionError("empty edge characteristic polynomial")
    return rho, out


def main() -> None:
    rows, z, theta, _ = rd.reconstruct_reduced_rows()
    if [rr.row_order(row, theta) for row in rows] != [22, 21]:
        raise AssertionError("reduced row orders changed")

    eta = sp.symbols("eta")
    M = sp.Matrix([
        [sp.expand(rows[i][j].subs(theta, eta)) for j in range(2)]
        for i in range(2)
    ])
    det = sp.expand(M.det())
    if rr.is_zero_expr(det):
        raise AssertionError("commutative characteristic determinant vanished")

    poly = sp.Poly(det, eta, z, domain="QQ")
    support = [(int(k), int(j)) for (k, j), coeff in poly.terms() if coeff != 0]
    if not support:
        raise AssertionError("empty infinity characteristic support")

    eta_degree = int(poly.degree(eta))
    z_degree = int(poly.degree(z))
    hull = upper_hull(support)
    if len(hull) < 2:
        raise AssertionError("infinity Newton upper hull is degenerate")

    edge_data: list[tuple[sp.Rational, sp.Expr]] = []
    for a, b in zip(hull, hull[1:]):
        edge_data.append(edge_characteristic(poly, eta, z, a, b))

    # Exact sanity link to the already-certified row-leading determinant.
    top_eta_coeff = sp.Poly(det, eta, domain="EX").coeff_monomial(eta**eta_degree)
    expected_top = sp.Rational(625, 64) * z * (18 * z + 5)
    if eta_degree != 43:
        raise AssertionError(f"commutative determinant eta-degree changed: {eta_degree}")
    if not rr.is_zero_expr(top_eta_coeff - expected_top):
        raise AssertionError(
            "top eta coefficient no longer matches reduced row-leading determinant"
        )

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_BOREL_INFINITY_NEWTON_CERTIFIED")
    print(f"COMMUTATIVE_CHARACTERISTIC_ETA_DEGREE := {eta_degree}")
    print(f"COMMUTATIVE_CHARACTERISTIC_Z_DEGREE := {z_degree}")
    print(f"COMMUTATIVE_CHARACTERISTIC_MONOMIAL_COUNT := {len(support)}")
    print(f"INFINITY_NEWTON_UPPER_HULL := {hull}")
    print(f"INFINITY_NEWTON_EDGE_COUNT := {len(edge_data)}")
    for idx, ((a, b), (rho, charpoly)) in enumerate(zip(zip(hull, hull[1:]), edge_data), start=1):
        print(f"EDGE_{idx}_POINTS := {a}->{b}")
        print(f"EDGE_{idx}_WKB_POWER_RHO := {sp.sstr(rho)}")
        print(f"EDGE_{idx}_CHARACTERISTIC := {sp.sstr(charpoly)}")
    print("TOP_ETA_COEFFICIENT := 625*z*(18*z+5)/64")
    print("INTERPRETATION := eta~c*z^rho balances are algebraically exposed by upper Newton edges")
    print("BOUNDARY := infinity characteristic/Newton data only; no WKB existence theorem, physical-mode selection, solution-growth bound, or Laplace-summability claim")


if __name__ == "__main__":
    main()
