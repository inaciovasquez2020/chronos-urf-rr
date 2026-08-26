from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"


def _symbols():
    return sp.symbols("M beta lam omega r")


def test_principal_determinant_factorization_and_exterior_root() -> None:
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
    }

    det = sp.sympify(data["principal_determinant"], locals=locals_)
    expected = (
        beta**2
        * lam**2
        * (lam - 2)
        * (r - 2 * M) ** 3
        * (-16 * M * beta + 5 * r**3)
        * (8 * M * beta + 5 * r**3)
        / (36 * r**11)
    )
    assert sp.factor(det - expected) == 0

    beta_c = 5 * r**3 / (16 * M)
    assert sp.simplify(det.subs(beta, beta_c)) == 0


def test_principal_null_direction_at_descriptor_surface() -> None:
    data = json.loads(ARTIFACT.read_text())
    M, beta, lam, omega, r = _symbols()
    locals_ = {
        "M": M,
        "beta": beta,
        "lam": lam,
        "omega": omega,
        "r": r,
        "I": sp.I,
    }

    principal = sp.Matrix(
        [[sp.sympify(entry, locals=locals_) for entry in row]
         for row in data["principal_matrix"]]
    )
    beta_c = 5 * r**3 / (16 * M)
    principal_c = principal.applyfunc(lambda x: sp.factor(x.subs(beta, beta_c)))

    A_c = -25 * lam * r**2 * (r - 2 * M) / (64 * M)
    expected = A_c * sp.Matrix([
        [1, sp.I * omega],
        [sp.I * omega, -omega**2],
    ])
    assert principal_c.applyfunc(sp.factor) == expected.applyfunc(sp.factor)

    v_c = sp.Matrix([-sp.I * omega, 1])
    w_c = sp.Matrix([[-sp.I * omega, 1]])
    assert (principal_c * v_c).applyfunc(sp.simplify) == sp.zeros(2, 1)
    assert (w_c * principal_c).applyfunc(sp.simplify) == sp.zeros(1, 2)

    # Under the ordinary exterior guards M != 0, r != 2M, lam != 0,
    # A_c is nonzero, so the matrix has rank exactly one rather than zero.
    assert sp.factor(principal_c[0, 0] - A_c) == 0


def test_backtrack_boundary_is_not_overclaimed() -> None:
    """The local certificate does not decide the horizon-selected branch.

    This regression deliberately records only the algebraic rank-loss and null
    direction.  Whether the physical ingoing solution satisfies the projected
    compatibility condition at r_c is a separate global connection problem.
    """
    data = json.loads(ARTIFACT.read_text())
    assert data["differential_orders"] == {
        "E0_h0": 4,
        "E0_h1": 3,
        "E1_h0": 3,
        "E1_h1": 2,
    }
