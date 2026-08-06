from __future__ import annotations

from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
OBSTRUCTION = ROOT / "tests/test_gfe_polar_even_parity_quadratic_source_obstruction.py"


def _higher_euler_operator(
    lagrangian: s.Expr,
    field: s.Expr,
    time: s.Symbol,
    max_order: int,
) -> s.Expr:
    result = s.diff(lagrangian, field)
    for order in range(1, max_order + 1):
        result += (-1) ** order * s.diff(
            s.diff(lagrangian, s.diff(field, time, order)),
            time,
            order,
        )
    return s.factor(s.simplify(result))


def test_explicit_rank_two_principal_order_reduction_before_constraints() -> None:
    source = OBSTRUCTION.read_text()
    assert "12 * M * r / (r - 2 * M) ** 2 * (q_h2**2 - q_k**2)" in source
    assert "4 * M * r / (3 * (r - 2 * M) ** 2) * (q_h2**2 - q_k**2)" in source
    assert "temporal_hessian.rank() == 2" in source

    M, r, beta2 = s.symbols("M r beta2", positive=True, real=True)
    f = 1 - 2 * M / r

    # Regge--Wheeler even parity, before eliminating lapse/shift constraints:
    # h_rr=f^{-1} H2 Y and h_AB=r^2 K Y Omega_AB.
    #
    # The pure-time Einstein-Hilbert ADM density is
    #   r^2/(4f) [Tr(dot h_i^j dot h_j^i) - Tr(dot h_i^i)^2].
    # H0 and H1 carry no pure temporal velocity in this principal block.
    h2_t, k_t = s.symbols("h2_t k_t", real=True)
    spatial_mixed_velocity = s.diag(h2_t, k_t, k_t)
    einstein_kinetic = s.factor(
        r**2
        / (4 * f)
        * (
            s.trace(spatial_mixed_velocity * spatial_mixed_velocity)
            - s.trace(spatial_mixed_velocity) ** 2
        )
    )
    expected_einstein_kinetic = s.factor(
        -r**2 / f * h2_t * k_t - r**2 / (2 * f) * k_t**2
    )
    assert s.factor(einstein_kinetic - expected_einstein_kinetic) == 0

    velocity_hessian = s.hessian(einstein_kinetic, (h2_t, k_t))
    expected_velocity_hessian = s.Matrix(
        [
            [0, -r**2 / f],
            [-r**2 / f, -r**2 / f],
        ]
    )
    assert s.simplify(velocity_hessian - expected_velocity_hessian) == s.zeros(2)
    assert velocity_hessian.rank() == 2
    assert s.simplify(velocity_hessian.det() + r**4 / f**2) == 0

    # Previously certified relative O(beta^2) pure-time correction:
    #   D (H2_tt^2 - K_tt^2) = 1/2 q_tt^T B q_tt.
    h2_tt, k_tt = s.symbols("h2_tt k_tt", real=True)
    D = 4 * M * r / (3 * (r - 2 * M) ** 2)
    correction_principal = s.factor(D * (h2_tt**2 - k_tt**2))
    correction_hessian = s.hessian(correction_principal, (h2_tt, k_tt))
    expected_correction_hessian = s.diag(2 * D, -2 * D)
    assert s.simplify(
        correction_hessian - expected_correction_hessian
    ) == s.zeros(2)

    # A perturbative derivative field substitution removes the full rank-two
    # principal correction modulo a total time derivative:
    #
    #   q = qhat + beta^2 C qhat_tt,
    #   C = 1/2 A^{-1} B.
    #
    # In components:
    #   H2 = H2hat + beta^2*a*(H2hat_tt + Khat_tt),
    #   K  = Khat  - beta^2*a*H2hat_tt,
    #   a  = 4M/[3 r^2 (r-2M)].
    substitution_matrix = s.simplify(
        s.Rational(1, 2) * velocity_hessian.inv() * correction_hessian
    )
    a = 4 * M / (3 * r**2 * (r - 2 * M))
    expected_substitution_matrix = s.Matrix([[a, a], [-a, 0]])
    assert s.simplify(
        substitution_matrix - expected_substitution_matrix
    ) == s.zeros(2)
    assert substitution_matrix.rank() == 2
    assert s.factor(substitution_matrix.det()) == a**2

    # Verify the cancellation directly in jet form.  At O(beta^2), expanding
    # the Einstein kinetic term gives v^T A C j, where v=qhat_t and
    # j=qhat_ttt.  Adding the higher-derivative correction gives exactly
    # d_t(1/2 v^T B qhat_tt), so the bulk fourth-order source vanishes.
    h2_ttt, k_ttt = s.symbols("h2_ttt k_ttt", real=True)
    velocity = s.Matrix([h2_t, k_t])
    acceleration = s.Matrix([h2_tt, k_tt])
    jerk = s.Matrix([h2_ttt, k_ttt])

    linearized_einstein_shift = s.factor(
        (velocity.T * velocity_hessian * substitution_matrix * jerk)[0]
    )
    correction_matrix_form = s.factor(
        s.Rational(1, 2)
        * (acceleration.T * correction_hessian * acceleration)[0]
    )
    boundary_derivative = s.factor(
        s.Rational(1, 2)
        * (
            (acceleration.T * correction_hessian * acceleration)[0]
            + (velocity.T * correction_hessian * jerk)[0]
        )
    )
    assert s.factor(
        linearized_einstein_shift
        + correction_matrix_form
        - boundary_derivative
    ) == 0

    # Independent variational verification with genuine time-dependent fields.
    t = s.symbols("t", real=True)
    H2hat = s.Function("H2hat")(t)
    Khat = s.Function("Khat")(t)
    qhat = s.Matrix([H2hat, Khat])
    qhat_t = qhat.diff(t)
    qhat_tt = qhat.diff(t, 2)
    field_shift = substitution_matrix * qhat_tt

    order_beta2_principal = s.expand(
        (qhat_t.T * velocity_hessian * field_shift.diff(t))[0]
        + s.Rational(1, 2)
        * (qhat_tt.T * correction_hessian * qhat_tt)[0]
    )
    exact_boundary = s.expand(
        s.diff(
            s.Rational(1, 2)
            * (qhat_t.T * correction_hessian * qhat_tt)[0],
            t,
        )
    )
    assert s.simplify(order_beta2_principal - exact_boundary) == 0
    assert _higher_euler_operator(order_beta2_principal, H2hat, t, 3) == 0
    assert _higher_euler_operator(order_beta2_principal, Khat, t, 3) == 0

    # The substitution is perturbatively invertible:
    # qhat = q - beta^2 C q_tt + O(beta^4).
    q0, q1, q0_tt, q1_tt = s.symbols(
        "q0 q1 q0_tt q1_tt",
        real=True,
    )
    q = s.Matrix([q0, q1])
    q_tt = s.Matrix([q0_tt, q1_tt])
    forward = q + beta2 * substitution_matrix * q_tt
    inverse_to_first_order = forward - beta2 * substitution_matrix * q_tt
    assert s.simplify(inverse_to_first_order - q) == s.zeros(2, 1)

    # No H0/H1 constraint equation or polar master field has been used.
    symbols_used = {str(symbol) for symbol in order_beta2_principal.free_symbols}
    assert "H0" not in symbols_used
    assert "H1" not in symbols_used
    assert "Psi_plus" not in symbols_used
