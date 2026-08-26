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
