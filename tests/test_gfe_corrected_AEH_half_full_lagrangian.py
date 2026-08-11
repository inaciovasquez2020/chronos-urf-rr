from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_full_lagrangian.json"

EXPECTED_SHA256 = (
    "508ba40f34719d1a9ec1943f092f28e077022369dec58d04cb0ec0407917d7a1"
)


def test_corrected_aeh_half_full_lagrangian_certificate() -> None:
    raw = ARTIFACT.read_bytes()

    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256

    d = json.loads(raw)

    assert d["scope"] == (
        "corrected AEH=1/2 normalized full Regge-Wheeler Lagrangian only"
    )

    assert d["normalization"] == (
        "L_full=(1/2)L_EH_unit+(5 beta/6)L_Ricci2+beta^2 L_joint"
    )

    gates = d["gates"]

    assert gates["corrected_Einstein_seed_match"] is True
    assert gates["L_full_beta0_equals_half_Einstein_unit"] is True
    assert gates["coeff_h0_r_squared_beta0_lambda6"] == "3"
    assert gates["beta1_equals_5_over_6_L_Ricci2"] is True
    assert gates["beta2_equals_L_joint"] is True
    assert gates["beta_degree_at_most_2"] is True

    # --------------------------------------------------------
    # Independently verify the two directly reconstructible
    # action-level identities from the serialized Lagrangian.
    # --------------------------------------------------------

    M, r, beta, lam = sp.symbols("M r beta lam", nonzero=True)

    local_dict = {
        "M": M,
        "r": r,
        "beta": beta,
        "lambda": lam,
        "lam": lam,
    }

    # Every jet name in this certificate is algebraic here.
    for field in (0, 1):
        for to in range(3):
            for ro in range(4):
                name = f"h{field}t{to}r{ro}"
                local_dict[name] = sp.Symbol(name)

    L = sp.sympify(
        d["full_lagrangian"].replace("lambda", "lam"),
        locals=local_dict,
        evaluate=False,
    )

    h0 = local_dict["h0t0r0"]
    h0r = local_dict["h0t0r1"]
    h1 = local_dict["h1t0r0"]
    h1t = local_dict["h1t1r0"]

    f = (r - 2 * M) / r
    mu = lam - 2
    Q = h1t - h0r + 2 * h0 / r

    expected_einstein = sp.Rational(1, 2) * lam * (
        Q**2
        + mu * h0**2 / (f * r**2)
        - f * mu * h1**2 / r**2
    )

    q0_residual = sp.factor(
        sp.cancel(sp.expand(L.subs(beta, 0) - expected_einstein))
    )

    assert q0_residual == 0

    coeff_h0r2 = sp.factor(
        sp.diff(L.subs({beta: 0, lam: 6}), h0r, 2) / 2
    )

    assert sp.simplify(coeff_h0r2 - 3) == 0

    # No beta^3 or higher term is permitted.
    assert sp.simplify(sp.diff(L, beta, 3)) == 0

    # --------------------------------------------------------
    # Fail closed on downstream claims.
    # --------------------------------------------------------

    downstream = d["downstream"]

    assert downstream == {
        "Euler_equations_constructed": False,
        "auxiliary_Hamiltonian_constructed": False,
        "PQ_blocks_constructed": False,
        "GQQ_constructed": False,
    }
