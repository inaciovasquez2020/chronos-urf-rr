from __future__ import annotations

import warnings

import sympy as sp

from tests import test_gfe_corrected_descriptor_rankloss as rankloss


def test_n3_compatibility_determinant_factor_diagnostic(monkeypatch) -> None:
    """Expose the already-certified n=3 determinant factorization without changing its derivation."""
    original_factor = sp.factor
    factored = []

    def recording_factor(expr, *args, **kwargs):
        result = original_factor(expr, *args, **kwargs)
        factored.append(result)
        return result

    monkeypatch.setattr(sp, "factor", recording_factor)
    rankloss.test_horizon_special_frequency_n3_compatibility_rank()
    determinant = factored[-1]
    assert determinant != 0
    warnings.warn(f"N3_COMPATIBILITY_DETERMINANT={determinant}", stacklevel=1)
