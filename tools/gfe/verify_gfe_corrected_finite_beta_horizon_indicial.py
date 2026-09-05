#!/usr/bin/env python3
"""Verify the weighted horizon Frobenius structure of the exact finite-beta odd equations.

This verifier starts from the hash-locked corrected AEH=1/2 Fourier-radial
Euler artifact. It does not use the perturbative beta expansion or a
hand-entered master equation.

Near the Schwarzschild horizon x = r - 2 M, the natural Schwarzschild-coordinate
ingoing weights are

    h0 ~ A x^p,
    h1 ~ B x^(p-1),

with p = -2 i M omega for the exp(-i omega t) convention. The leading weighted
Euler matrix is constrained. At the physical ingoing exponent the n=1 shifted
leading matrix vanishes completely, so a projected scalar compatibility test is
not sufficient: the full first-correction source must vanish for an ordinary
pure-power Frobenius series to continue.

The exact finite-beta equations instead produce a nonzero beta^2 obstruction
proportional to lambda(lambda-2). This verifier certifies that obstruction and
then tests generalized repairs at the same n=1 resonance. A single
x^(p+1) log(x) correction is generically obstructed because L'(p+1) has rank
one and misses the source direction. The minimal log^2 chain also fails: its
log equation forces the log^2 coefficient into ker L', and L'' maps that kernel
back into im L'. Therefore the log^2 term cannot change the one-log quotient
obstruction. No pure-power, one-log, or minimal log^2 continuation is claimed.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "artifacts/chronos/gfe_corrected_AEH_half_euler_generator.json"

M, beta, lam, omega, r, p = sp.symbols("M beta lam omega r p")
I = sp.I
LOCALS = {
    "M": M,
    "beta": beta,
    "lam": lam,
    "lambda": lam,
    "omega": omega,
    "r": r,
    "I": I,
}
FIELD = sp.QQ_I.frac_field(M, beta, lam, omega)
RING_ROOT = sp.Poly(r - 2 * M, r, domain=FIELD)


def _falling(z: sp.Expr, order: int) -> sp.Expr:
    out = sp.Integer(1)
    for j in range(order):
        out *= z - j
    return sp.expand(out)


def _root_order_and_reduced_poly(poly: sp.Poly) -> tuple[int, sp.Poly]:
    """Remove the complete (r-2M) multiplicity from a nonzero polynomial."""
    order = 0
    current = poly
    while current:
        quotient, remainder = sp.div(current, RING_ROOT)
        if remainder:
            break
        current = quotient
        order += 1
    if current.eval(2 * M) == FIELD.zero:
        raise AssertionError("failed to remove complete horizon-root multiplicity")
    return order, current


def _horizon_valuation_lead_next(expr: sp.Expr) -> tuple[int, sp.Expr, sp.Expr]:
    """Exact valuation plus the first two Laurent coefficients at r=2M."""
    numerator, denominator = sp.fraction(sp.together(expr))
    numerator_poly = sp.Poly(numerator, r, domain=FIELD)
    denominator_poly = sp.Poly(denominator, r, domain=FIELD)
    n_order, n_reduced = _root_order_and_reduced_poly(numerator_poly)
    d_order, d_reduced = _root_order_and_reduced_poly(denominator_poly)

    n0 = FIELD.convert(n_reduced.eval(2 * M))
    d0 = FIELD.convert(d_reduced.eval(2 * M))
    n1 = FIELD.convert(n_reduced.diff().eval(2 * M))
    d1 = FIELD.convert(d_reduced.diff().eval(2 * M))

    lead = n0 / d0
    next_coefficient = (n1 * d0 - n0 * d1) / (d0 * d0)
    return (
        n_order - d_order,
        sp.cancel(FIELD.to_sympy(lead)),
        sp.cancel(FIELD.to_sympy(next_coefficient)),
    )


def _parse_equations() -> tuple[list[sp.Expr], list[list[sp.Symbol]]]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    h = [
        [sp.Symbol(f"h{field}r{order}") for order in range(5)]
        for field in range(2)
    ]
    local_map = dict(LOCALS)
    local_map.update({str(symbol): symbol for row in h for symbol in row})
    equations = [
        sp.sympify(text, locals=local_map)
        for text in source["euler_equations"]
    ]
    return equations, h


def _right_kernel_vector(matrix: sp.Matrix) -> sp.Matrix:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    if a != 0 or b != 0:
        return sp.Matrix([-b, a])
    if c != 0 or d != 0:
        return sp.Matrix([-d, c])
    raise AssertionError("leading weighted horizon matrix is identically zero")


def _left_kernel_vector(matrix: sp.Matrix) -> sp.Matrix:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    if a != 0 or c != 0:
        return sp.Matrix([-c, a])
    if b != 0 or d != 0:
        return sp.Matrix([-d, b])
    raise AssertionError("shifted leading weighted horizon matrix is identically zero")


def _simplified_matrix(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.applyfunc(lambda value: sp.factor(sp.cancel(value)))


def _is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.factor(sp.cancel(value)) == 0 for value in matrix)


def _rank_one_preimage(matrix: sp.Matrix, target: sp.Matrix) -> sp.Matrix:
    """Construct an exact preimage after target membership has been verified."""
    for column_index in range(2):
        column = matrix[:, column_index]
        for row_index in range(2):
            pivot = sp.factor(sp.cancel(column[row_index]))
            if pivot == 0:
                continue
            scale = sp.factor(sp.cancel(target[row_index] / pivot))
            coefficient = sp.zeros(2, 1)
            coefficient[column_index] = scale
            if _is_zero_matrix(_simplified_matrix(matrix * coefficient - target)):
                return _simplified_matrix(coefficient)
    raise AssertionError("target was expected in rank-one image but no preimage was found")


def derive_weighted_horizon_frobenius_system() -> tuple[
    list[int], sp.Matrix, sp.Matrix, sp.Expr
]:
    equations, h = _parse_equations()
    field_shifts = (0, -1)

    row_orders: list[int] = []
    row_terms: list[list[tuple[int, int, int, sp.Expr, sp.Expr]]] = []

    for equation in equations:
        terms: list[tuple[int, int, int, sp.Expr, sp.Expr]] = []
        for field in range(2):
            for derivative_order in range(5):
                coefficient = sp.diff(equation, h[field][derivative_order])
                if coefficient == 0:
                    continue
                valuation, lead, next_coefficient = _horizon_valuation_lead_next(
                    coefficient
                )
                weighted_order = valuation + field_shifts[field] - derivative_order
                terms.append(
                    (field, derivative_order, weighted_order, lead, next_coefficient)
                )
        if not terms:
            raise AssertionError("Euler row contains no field-derivative terms")
        row_orders.append(min(term[2] for term in terms))
        row_terms.append(terms)

    leading = sp.zeros(2, 2)
    subleading = sp.zeros(2, 2)
    for equation_index, terms in enumerate(row_terms):
        leading_order = row_orders[equation_index]
        for field, derivative_order, weighted_order, lead, next_coefficient in terms:
            falling = _falling(p + field_shifts[field], derivative_order)
            if weighted_order == leading_order:
                leading[equation_index, field] += lead * falling
                subleading[equation_index, field] += next_coefficient * falling
            elif weighted_order == leading_order + 1:
                subleading[equation_index, field] += lead * falling

    leading = _simplified_matrix(leading)
    subleading = _simplified_matrix(subleading)

    leading_determinant = sp.factor(sp.cancel(leading.det()))
    if leading_determinant != 0:
        raise AssertionError(
            "expected constrained leading weighted horizon system, but its "
            f"determinant is {sp.sstr(leading_determinant)}"
        )

    seed = _right_kernel_vector(leading)
    if any(sp.factor(sp.cancel(value)) != 0 for value in leading * seed):
        raise AssertionError("constructed leading right-kernel vector is invalid")

    shifted_leading = _simplified_matrix(leading.subs(p, p + 1))
    left_null = _left_kernel_vector(shifted_leading)
    if any(
        sp.factor(sp.cancel(value)) != 0
        for value in (left_null.T * shifted_leading)
    ):
        raise AssertionError("constructed shifted left-kernel vector is invalid")

    projected_compatibility = sp.factor(
        sp.cancel((left_null.T * subleading * seed)[0])
    )
    return row_orders, leading, subleading, projected_compatibility


def main() -> None:
    row_orders, leading, subleading, projected_compatibility = (
        derive_weighted_horizon_frobenius_system()
    )

    if projected_compatibility == 0:
        raise AssertionError(
            "projected subleading compatibility is identically zero; "
            "unexpected loss of the symbolic diagnostic"
        )

    physical_ingoing_exponent = -2 * I * M * omega
    physical_seed = sp.Matrix([1, 2 * M])
    physical_leading = _simplified_matrix(
        leading.subs(p, physical_ingoing_exponent)
    )
    physical_seed_residual = _simplified_matrix(physical_leading * physical_seed)
    if not _is_zero_matrix(physical_seed_residual):
        raise AssertionError(
            "expected ingoing seed (A0,B0)=(1,2M) is not in the exact "
            "finite-beta leading horizon kernel; "
            f"residual={physical_seed_residual.tolist()}"
        )

    resonant_exponent = physical_ingoing_exponent + 1
    physical_shifted_leading = _simplified_matrix(leading.subs(p, resonant_exponent))
    if not _is_zero_matrix(physical_shifted_leading):
        raise AssertionError(
            "expected n=1 rank-zero resonance at the physical ingoing exponent; "
            f"shifted={physical_shifted_leading.tolist()}"
        )

    physical_first_residual = _simplified_matrix(
        subleading.subs(p, physical_ingoing_exponent) * physical_seed
    )
    expected_obstruction = _simplified_matrix(
        sp.Matrix(
            [
                -5 * beta**2 * lam * (lam - 2) / (144 * M**4),
                -5 * beta**2 * lam * (lam - 2) / (288 * M**5),
            ]
        )
    )
    if not _is_zero_matrix(
        _simplified_matrix(physical_first_residual - expected_obstruction)
    ):
        raise AssertionError(
            "finite-beta n=1 obstruction changed; "
            f"actual={physical_first_residual.tolist()}, "
            f"expected={expected_obstruction.tolist()}"
        )

    gr_limit_residual = _simplified_matrix(physical_first_residual.subs(beta, 0))
    if not _is_zero_matrix(gr_limit_residual):
        raise AssertionError(
            "finite-beta horizon obstruction does not vanish in the GR limit; "
            f"residual={gr_limit_residual.tolist()}"
        )

    flagship_ell2_residual = _simplified_matrix(physical_first_residual.subs(lam, 6))
    expected_flagship = _simplified_matrix(
        sp.Matrix(
            [
                -5 * beta**2 / (6 * M**4),
                -5 * beta**2 / (12 * M**5),
            ]
        )
    )
    if not _is_zero_matrix(
        _simplified_matrix(flagship_ell2_residual - expected_flagship)
    ):
        raise AssertionError(
            "ell=2 (lambda=6) horizon obstruction specialization changed; "
            f"actual={flagship_ell2_residual.tolist()}"
        )

    # Weakest generalized repair: add x^(p+1) log(x) times a coefficient vector.
    # At the resonance L(p+1)=0, the non-log contribution of that term is
    # dL/dp evaluated at p+1. Thus the one-log correction exists only if
    # -physical_first_residual lies in the image of this derivative matrix.
    log_matrix = _simplified_matrix(leading.diff(p).subs(p, resonant_exponent))
    log_matrix_determinant = sp.factor(sp.cancel(log_matrix.det()))
    if log_matrix_determinant != 0:
        raise AssertionError(
            "expected rank-one logarithmic correction matrix; "
            f"det={sp.sstr(log_matrix_determinant)}"
        )
    if _is_zero_matrix(log_matrix):
        raise AssertionError("logarithmic correction matrix unexpectedly vanished")

    log_left_null = sp.Matrix([omega, 2 * M * omega - I])
    log_left_null_residual = _simplified_matrix(log_left_null.T * log_matrix)
    if not _is_zero_matrix(log_left_null_residual):
        raise AssertionError(
            "polynomial left-null vector for logarithmic correction matrix changed; "
            f"residual={log_left_null_residual.tolist()}"
        )

    log_image_obstruction = sp.factor(
        sp.cancel((log_left_null.T * physical_first_residual)[0])
    )
    expected_log_image_obstruction = sp.factor(
        -5
        * beta**2
        * lam
        * (lam - 2)
        * (4 * M * omega - I)
        / (288 * M**5)
    )
    if sp.factor(sp.cancel(log_image_obstruction - expected_log_image_obstruction)) != 0:
        raise AssertionError(
            "one-log image obstruction changed; "
            f"actual={sp.sstr(log_image_obstruction)}, "
            f"expected={sp.sstr(expected_log_image_obstruction)}"
        )

    flagship_log_image_obstruction = sp.factor(
        sp.cancel(log_image_obstruction.subs(lam, 6))
    )
    expected_flagship_log_image_obstruction = sp.factor(
        -5 * beta**2 * (4 * M * omega - I) / (12 * M**5)
    )
    if sp.factor(
        sp.cancel(
            flagship_log_image_obstruction
            - expected_flagship_log_image_obstruction
        )
    ) != 0:
        raise AssertionError(
            "ell=2 one-log image obstruction changed; "
            f"actual={sp.sstr(flagship_log_image_obstruction)}"
        )

    exceptional_frequency_residual = sp.factor(
        sp.cancel(log_image_obstruction.subs(omega, I / (4 * M)))
    )
    if exceptional_frequency_residual != 0:
        raise AssertionError(
            "one-log obstruction does not vanish at exceptional frequency; "
            f"residual={sp.sstr(exceptional_frequency_residual)}"
        )

    # Minimal log^2 generalized chain at the same n=1 resonance:
    #   c log^2(x) + b log(x) + a1.
    # Because L(q*)=0, the log coefficient requires 2 L'(q*) c = 0, so c
    # must lie in ker L'. The constant equation is
    #   R1 + L''(q*) c + L'(q*) b = 0.
    # Exact computation shows L''(q*) maps ker L' back into im L'. Thus a
    # log^2 term cannot alter the one-dimensional quotient obstruction already
    # detected by the left-null vector of L'.
    log2_kernel = _simplified_matrix(_right_kernel_vector(log_matrix))
    if not _is_zero_matrix(_simplified_matrix(log_matrix * log2_kernel)):
        raise AssertionError("constructed log^2 kernel vector is invalid")

    log2_matrix = _simplified_matrix(
        leading.diff(p, 2).subs(p, resonant_exponent)
    )
    log2_kernel_lift = _simplified_matrix(log2_matrix * log2_kernel)
    log2_kernel_lift_pairing = sp.factor(
        sp.cancel((log_left_null.T * log2_kernel_lift)[0])
    )
    if log2_kernel_lift_pairing != 0:
        raise AssertionError(
            "log^2 kernel lift unexpectedly leaves im L'; "
            f"pairing={sp.sstr(log2_kernel_lift_pairing)}"
        )

    print("GFE_CORRECTED_FINITE_BETA_HORIZON_FROBENIUS_OBSTRUCTION")
    print(f"SOURCE := {SOURCE.relative_to(ROOT)}")
    print("WEIGHTS := h0:x^p, h1:x^(p-1)")
    print(f"ROW_ORDERS := {row_orders}")
    print("PHYSICAL_INGOING_EXPONENT := -2*I*M*omega")
    print("PHYSICAL_INGOING_SEED := [1, 2*M]")
    print("PHYSICAL_N1_SHIFTED_LEADING_RANK := 0")
    print(
        "PHYSICAL_N1_OBSTRUCTION := ["
        + ", ".join(sp.sstr(value) for value in physical_first_residual)
        + "]"
    )
    print("PURE_POWER_FINITE_BETA_FROBENIUS := obstructed when beta*lambda*(lambda-2) != 0")
    print("GR_LIMIT_BETA_ZERO := obstruction vanishes")
    print(
        "FLAGSHIP_ELL2_LAMBDA6_OBSTRUCTION := ["
        + ", ".join(sp.sstr(value) for value in flagship_ell2_residual)
        + "]"
    )
    print("LOG_N1_CORRECTION_MATRIX_RANK := 1")
    print("LOG_N1_LEFT_NULL := [omega, 2*M*omega - I]")
    print(f"LOG_N1_IMAGE_OBSTRUCTION := {sp.sstr(log_image_obstruction)}")
    print(
        "ONE_LOG_FINITE_BETA_FROBENIUS := obstructed when "
        "beta*lambda*(lambda-2)*(4*M*omega-I) != 0"
    )
    print(
        "FLAGSHIP_ELL2_ONE_LOG_OBSTRUCTION := "
        + sp.sstr(flagship_log_image_obstruction)
    )
    print("EXCEPTIONAL_ONE_LOG_FREQUENCY := omega = I/(4*M)")
    print(
        "LOG2_N1_KERNEL := ["
        + ", ".join(sp.sstr(value) for value in log2_kernel)
        + "]"
    )
    print(
        "LOG2_N1_KERNEL_LIFT := ["
        + ", ".join(sp.sstr(value) for value in log2_kernel_lift)
        + "]"
    )
    print("LOG2_N1_KERNEL_LIFT_PAIRING := 0")
    print(
        "MINIMAL_LOG2_N1_CHAIN := cannot change the one-log quotient obstruction"
    )
    print(
        "LOG2_FINITE_BETA_FROBENIUS := obstructed whenever "
        "beta*lambda*(lambda-2)*(4*M*omega-I) != 0"
    )
    print("NEXT_ROUTE := test the log^3 generalized Frobenius chain, where L''' is the first remaining possible new quotient direction")


if __name__ == "__main__":
    main()
