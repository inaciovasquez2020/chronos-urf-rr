from __future__ import annotations

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


def test_n3_exceptional_rank_one_and_surviving_compatibility(monkeypatch) -> None:
    """Certify the exact rank-one n=3 system on beta=90*M^2/31."""
    M, beta, lam, _, _ = rankloss._symbols()
    a0 = sp.Symbol("a0")
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

    pivot = 1000 * lam * (lam - 2) / (961 * M)
    expected_matrix = sp.Matrix([[0, 0], [0, pivot]])
    assert matrix_exceptional == expected_matrix
    assert sp.factor(sp.cancel(matrix_exceptional.det())) == 0
    assert sp.factor(sp.cancel(matrix_exceptional[1, 1] - pivot)) == 0

    # With M != 0, lam != 0, and lam - 2 != 0, the displayed pivot is
    # nonzero, hence the exceptional coefficient matrix has rank exactly one.
    assert sp.factor(pivot) == 1000 * lam * (lam - 2) / (961 * M)

    compatibility = source_exceptional[0]
    expected_compatibility = (
        5
        * a0
        * lam
        * (lam - 2) ** 2
        * (196575 * lam - 770891)
        / (18458888 * M**3)
    )
    assert sp.factor(sp.cancel(compatibility - expected_compatibility)) == 0
    assert compatibility != 0

    # The zero coefficient row therefore survives as source compatibility.
    # On the nontrivial branch a0 != 0 and under the existing lam guards,
    # its only remaining root is lam = 770891/196575.
    stripped = sp.cancel(
        compatibility
        * 18458888 * M**3
        / (5 * a0 * lam * (lam - 2) ** 2)
    )
    assert sp.factor(stripped - (196575 * lam - 770891)) == 0
    assert sp.solve(stripped, lam) == [sp.Rational(770891, 196575)]
