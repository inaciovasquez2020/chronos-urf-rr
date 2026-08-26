from __future__ import annotations

import warnings

import sympy as sp

from tests import test_gfe_corrected_descriptor_rankloss as rankloss


def test_n3_compatibility_determinant_factor_and_physical_zero_locus(monkeypatch) -> None:
    """Factor the certified n=3 determinant and isolate its physical zero locus."""
    M, beta, lam, _, _ = rankloss._symbols()
    original_factor = sp.factor
    factored = []

    def recording_factor(expr, *args, **kwargs):
        result = original_factor(expr, *args, **kwargs)
        factored.append(result)
        return result

    monkeypatch.setattr(sp, "factor", recording_factor)
    rankloss.test_horizon_special_frequency_n3_compatibility_rank()
    determinant = factored[-1]

    expected = (
        -beta**2
        * lam**2
        * (90 * M**2 - 31 * beta) ** 2
        * (lam - 2) ** 2
        / (2916 * M**10)
    )
    assert original_factor(sp.cancel(determinant - expected)) == 0

    # Under M != 0, beta != 0, lam != 0, and lam - 2 != 0,
    # only the repeated factor 90*M^2 - 31*beta can vanish.
    guard_stripped = sp.cancel(
        determinant
        * (-2916 * M**10)
        / (beta**2 * lam**2 * (lam - 2) ** 2)
    )
    assert original_factor(
        guard_stripped - (90 * M**2 - 31 * beta) ** 2
    ) == 0
    assert sp.solve(guard_stripped, beta) == [90 * M**2 / 31]

    beta_exceptional = 90 * M**2 / 31
    assert sp.cancel(determinant.subs(beta, beta_exceptional)) == 0

    # The exceptional surface intersects the existing physical M>0, beta>0 domain.
    M_pos = sp.Symbol("M_pos", positive=True)
    assert beta_exceptional.subs(M, M_pos).is_positive is True


def test_n3_exceptional_rank_diagnostic(monkeypatch) -> None:
    """Expose the exceptional n=3 matrix and source for the bounded rank certificate."""
    M, beta, _, _, _ = rankloss._symbols()
    original_linear_eq_to_matrix = sp.linear_eq_to_matrix
    captured = []

    def recording_linear_eq_to_matrix(equations, symbols):
        result = original_linear_eq_to_matrix(equations, symbols)
        captured.append(result)
        return result

    monkeypatch.setattr(sp, "linear_eq_to_matrix", recording_linear_eq_to_matrix)
    rankloss.test_horizon_special_frequency_n3_compatibility_rank()
    matrix, source = captured[-1]
    beta_exceptional = 90 * M**2 / 31
    matrix_exceptional = matrix.applyfunc(
        lambda entry: sp.factor(sp.cancel(entry.subs(beta, beta_exceptional)))
    )
    source_exceptional = source.applyfunc(
        lambda entry: sp.factor(sp.cancel(entry.subs(beta, beta_exceptional)))
    )

    assert sp.factor(sp.cancel(matrix_exceptional.det())) == 0
    assert matrix_exceptional != sp.zeros(2, 2)
    warnings.warn(
        "N3_EXCEPTIONAL_MATRIX=" + repr(matrix_exceptional)
        + ";N3_EXCEPTIONAL_SOURCE=" + repr(source_exceptional),
        stacklevel=1,
    )
